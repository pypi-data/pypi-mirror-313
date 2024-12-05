from __future__ import annotations

import dataclasses
import datetime
import enum
import inspect
import logging
from datetime import timedelta
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union
from typing import overload

import attrs
import numpy as np
import pandas
import pendulum
from google.protobuf import duration_pb2
from pyspark.sql import dataframe as pyspark_dataframe
from pyspark.sql import streaming
from typeguard import typechecked

from tecton import run_api_consts
from tecton import tecton_context
from tecton import types
from tecton._internals import athena_api
from tecton._internals import delete_keys_api
from tecton._internals import display
from tecton._internals import errors
from tecton._internals import materialization_api
from tecton._internals import metadata_service
from tecton._internals import mock_source_utils
from tecton._internals import query_helper
from tecton._internals import querytree_api
from tecton._internals import run_api
from tecton._internals import sdk_decorators
from tecton._internals import snowflake_api
from tecton._internals import spark_api
from tecton._internals import type_utils
from tecton._internals import utils as internal_utils
from tecton._internals import validations_api
from tecton._internals.pandas_compat import pandas_to_spark
from tecton.framework import base_tecton_object
from tecton.framework import configs
from tecton.framework import data_source as framework_data_source
from tecton.framework import entity as framework_entity
from tecton.framework import filtered_source
from tecton.framework import repo_config
from tecton.framework import transformation as framework_transformation
from tecton.framework import utils
from tecton.framework.data_frame import FeatureVector
from tecton.framework.data_frame import TectonDataFrame
from tecton.framework.transformation import PipelineNodeWrapper
from tecton.framework.validation_mode import ValidationMode
from tecton_core import aggregation_utils
from tecton_core import conf
from tecton_core import errors as core_errors
from tecton_core import fco_container
from tecton_core import feature_definition_wrapper
from tecton_core import feature_set_config
from tecton_core import id_helper
from tecton_core import materialization_context
from tecton_core import pipeline_common
from tecton_core import request_context
from tecton_core import schema_derivation_utils
from tecton_core import specs
from tecton_core import time_utils
from tecton_core.compute_mode import BatchComputeMode
from tecton_core.compute_mode import ComputeMode
from tecton_core.compute_mode import default_batch_compute_mode
from tecton_core.compute_mode import offline_retrieval_compute_mode
from tecton_core.errors import TectonValidationError
from tecton_core.schema import Schema
from tecton_core.specs import MaterializedFeatureViewSpec
from tecton_core.specs.data_source_spec import DataSourceSpec
from tecton_core.specs.time_window_spec import LifetimeWindowSpec
from tecton_core.specs.time_window_spec import RelativeTimeWindowSpec
from tecton_core.specs.time_window_spec import TimeWindowSeriesSpec
from tecton_core.specs.time_window_spec import create_time_window_spec_from_data_proto
from tecton_core.specs.transformation_spec import TransformationSpec
from tecton_proto.args import basic_info_pb2
from tecton_proto.args import fco_args_pb2
from tecton_proto.args import feature_service_pb2
from tecton_proto.args import feature_view_pb2 as feature_view__args_pb2
from tecton_proto.args import pipeline_pb2
from tecton_proto.args import transformation_pb2
from tecton_proto.common import data_source_type_pb2
from tecton_proto.common import fco_locator_pb2
from tecton_proto.common import id_pb2
from tecton_proto.common import schema_pb2
from tecton_proto.common.data_source_type_pb2 import DataSourceType
from tecton_proto.data import materialization_status_pb2
from tecton_proto.metadataservice import metadata_service_pb2
from tecton_proto.validation import validator_pb2
from tecton_spark import pipeline_helper
from tecton_spark import spark_schema_wrapper
from tecton_spark.type_annotations import is_pyspark_df


# FilteredSource start offsets smaller (more negative) than this offset will be considered UNBOUNDED_PRECEEDING.
MIN_START_OFFSET = datetime.timedelta(days=-365 * 100)  # 100 years

# This is the mode used when the feature view decorator is used on a pipeline function, i.e. one that only contains
# references to transformations and constants.
PIPELINE_MODE = "pipeline"

logger = logging.getLogger(__name__)


# Create a parallel enum class since Python proto extensions do not use an enum class.
# Keep up-to-date with StreamProcessingMode from tecton_proto/args/feature_view.proto.
class StreamProcessingMode(enum.Enum):
    TIME_INTERVAL = feature_view__args_pb2.StreamProcessingMode.STREAM_PROCESSING_MODE_TIME_INTERVAL
    CONTINUOUS = feature_view__args_pb2.StreamProcessingMode.STREAM_PROCESSING_MODE_CONTINUOUS


# Keep up-to-date with BatchTriggerType from tecton_proto/args/feature_view.proto.
class BatchTriggerType(enum.Enum):
    SCHEDULED = feature_view__args_pb2.BatchTriggerType.BATCH_TRIGGER_TYPE_SCHEDULED
    MANUAL = feature_view__args_pb2.BatchTriggerType.BATCH_TRIGGER_TYPE_MANUAL
    NO_BATCH_MATERIALIZATION = feature_view__args_pb2.BatchTriggerType.BATCH_TRIGGER_TYPE_NO_BATCH_MATERIALIZATION


@attrs.define(auto_attribs=True)
class QuerySources:
    from_source_count: int = 0
    offline_store_count: int = 0
    on_demand_count: int = 0
    feature_table_count: int = 0

    def __add__(self, other: "QuerySources"):
        return QuerySources(
            from_source_count=self.from_source_count + other.from_source_count,
            offline_store_count=self.offline_store_count + other.offline_store_count,
            on_demand_count=self.on_demand_count + other.on_demand_count,
            feature_table_count=self.feature_table_count + other.feature_table_count,
        )

    def _print_from_source_message(self, count: int, single: str, message: str):
        if count > 0:
            feature_view_text = internal_utils.plural(count, f"{single} is", f"{single}s are")
            logger.info(f"{count} {feature_view_text} {message}")

    def display(self):
        self._print_from_source_message(
            self.offline_store_count, "Feature View", "being read from data in the offline store."
        )
        self._print_from_source_message(
            self.from_source_count, "Feature View", "being computed directly from raw data sources."
        )
        self._print_from_source_message(
            self.feature_table_count, "Feature Table", "being loaded from the offline store."
        )
        self._print_from_source_message(self.on_demand_count, "On-Demand Feature View", "being computed ad hoc.")


def _to_pyspark_mocks(
    mock_inputs: Dict[str, Union[pyspark_dataframe.DataFrame, pandas.DataFrame]],
) -> Dict[str, pyspark_dataframe.DataFrame]:
    pyspark_mock_inputs = {}
    for input_name, mock_data in mock_inputs.items():
        if is_pyspark_df(mock_data):
            pyspark_mock_inputs[input_name] = mock_data
        elif isinstance(mock_data, pandas.DataFrame):
            spark = tecton_context.TectonContext.get_instance()._spark
            pyspark_mock_inputs[input_name] = pandas_to_spark(spark, mock_data)
        else:
            msg = f"Unexpected mock source type for kwarg {input_name}: {type(mock_data)}"
            raise TypeError(msg)
    return pyspark_mock_inputs


@dataclasses.dataclass
class _Schemas:
    view_schema: Optional[schema_pb2.Schema]
    materialization_schema: Optional[schema_pb2.Schema]
    online_batch_table_format: Optional[schema_pb2.OnlineBatchTableFormat]


@attrs.define(eq=False)
class FeatureView(base_tecton_object.BaseTectonObject):
    """Base class for Feature View classes (including Feature Tables)."""

    # A FeatureDefinitionWrapper instance, which contains the Feature View spec for this Feature View and dependent
    # FCO specs (e.g. Data Source specs). Set only after the object has been validated. Remote objects, i.e. applied
    # objects fetched from the backend, are assumed valid.
    _feature_definition: Optional[feature_definition_wrapper.FeatureDefinitionWrapper] = attrs.field(repr=False)

    # A Tecton "args" proto. Only set if this object was defined locally, i.e. this object was not applied and fetched
    # from the Tecton backend.
    _args: Optional[feature_view__args_pb2.FeatureViewArgs] = attrs.field(repr=False, on_setattr=attrs.setters.frozen)

    # A supplement to the _args proto that is needed to create the Feature View spec.
    _args_supplement: Optional[specs.FeatureViewSpecArgsSupplement] = attrs.field(repr=False)

    @property
    def _spec(self) -> Optional[specs.FeatureViewSpec]:
        return self._feature_definition.fv_spec if self._feature_definition is not None else None

    @sdk_decorators.assert_local_object
    def _build_args(self) -> fco_args_pb2.FcoArgs:
        return fco_args_pb2.FcoArgs(feature_view=self._args)

    def _build_fco_validation_args(self) -> validator_pb2.FcoValidationArgs:
        if self.info._is_local_object:
            assert self._args_supplement is not None
            return validator_pb2.FcoValidationArgs(
                feature_view=validator_pb2.FeatureViewValidationArgs(
                    args=self._args,
                    view_schema=self._args_supplement.view_schema,
                    materialization_schema=self._args_supplement.materialization_schema,
                )
            )
        else:
            return self._spec.validation_args

    @property
    def _is_valid(self) -> bool:
        return self._spec is not None

    def _derive_schemas(self) -> _Schemas:
        raise NotImplementedError

    def _get_dependent_objects(self, include_indirect_dependencies: bool) -> List[base_tecton_object.BaseTectonObject]:
        raise NotImplementedError

    def _validate_dependencies(self, indentation_level: int) -> None:
        dependent_objects = self._get_dependent_objects(include_indirect_dependencies=False)
        validations_api.print_validating_dependencies(self, dependent_objects, indentation_level)
        for dependent_object in dependent_objects:
            dependent_object._validate(indentation_level + 1)

    def _get_dependent_specs(self) -> List[specs.TectonObjectSpec]:
        """Returns all of the specs dependend on by this Feature View."""
        dependent_objects = self._get_dependent_objects(include_indirect_dependencies=True)
        assert all(
            obj._is_valid for obj in dependent_objects
        ), "_get_dependent_specs expects that dependent objects have been validated."
        return [obj._spec for obj in dependent_objects]

    @sdk_decorators.assert_valid
    def _check_can_query_from_source(self, from_source: Optional[bool]) -> QuerySources:
        raise NotImplementedError

    @property
    @sdk_decorators.sdk_public_method
    def join_keys(self) -> List[str]:
        """The join key column names."""
        if self._args is not None:
            return list(specs.get_join_keys_from_feature_view_args(self._args))
        else:
            return list(self._feature_definition.fv_spec.join_keys)

    @property
    @sdk_decorators.sdk_public_method
    def online_serving_index(self) -> List[str]:
        """The set of join keys that will be indexed and queryable during online serving.

        Defaults to the complete set of join keys.
        """
        if self._args is not None:
            return list(specs.get_online_serving_keys_from_feature_view_args(self._args))
        else:
            return list(self._spec.online_serving_keys)

    @property
    @sdk_decorators.sdk_public_method
    def wildcard_join_key(self) -> Optional[set]:
        """Returns a wildcard join key column name if it exists; Otherwise returns None."""
        wildcard_keys = set(self.join_keys) - set(self.online_serving_index)
        if len(wildcard_keys) == 0:
            return None
        elif len(wildcard_keys) == 1:
            return next(iter(wildcard_keys))
        else:
            msg = "The online serving index must either be equal to join_keys or only be missing a single key."
            raise ValueError(msg)

    @property
    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def url(self) -> str:
        """Returns a link to the Tecton Web UI."""
        return self._feature_definition.fv_spec.url

    @sdk_decorators.sdk_public_method(requires_validation=True)
    def get_feature_columns(self) -> List[str]:
        """The features produced by this FeatureView."""
        return self._feature_definition.features

    @sdk_decorators.sdk_public_method(requires_validation=True)
    def print_transformation_schema(self) -> None:
        """Pretty prints the transformation schema. See transformation_schema() for more information."""

        transformation_schema = self.transformation_schema()
        print(
            "If copy/pasting the schema below, import the specified datatypes from tecton.types\n"
            + type_utils.schema_pretty_str(transformation_schema)
        )

    @sdk_decorators.sdk_public_method(requires_validation=True)
    def transformation_schema(self) -> List[types.Field]:
        """Returns the transformation schema for the feature view.

        The transformation schema may be explicitly defined (via the schema parameter), and in that case this method will return
        the explicitly defined schema. If the schema is not provided, then this method will return the derived schema.
        For locally defined objects, this schema will be derived locally by executing the feature view transformation(s).
        For backend applied objects, this schema will have been derived during tecton plan/apply.
        """

        view_schema = self._feature_definition.view_schema.to_proto()
        return querytree_api.get_fields_list_from_tecton_schema(view_schema)

    def _validate(self, indentation_level: int = 0) -> None:
        if self._is_valid:
            return

        self._validate_dependencies(indentation_level)
        try:
            schemas = self._derive_schemas()
            self._args_supplement = specs.FeatureViewSpecArgsSupplement(
                view_schema=schemas.view_schema,
                materialization_schema=schemas.materialization_schema,
                online_batch_table_format=schemas.online_batch_table_format,
            )
        except Exception:
            # Use logger.exception() to print/log the validation error message followed by the exception trace and then
            # re-raise. This approach is preferred to exception chaining because it's a better notebook UX - especially
            # for EMR notebooks, where chained exceptions are not rendered.
            logger.exception(
                f"An error occured when attempting to run {self.__class__.__name__} '{self.name}' during validation."
            )
            raise

        validations_api.run_backend_validation_and_assert_valid(
            self,
            validator_pb2.ValidationRequest(
                validation_args=[
                    dependent_obj._build_fco_validation_args()
                    for dependent_obj in self._get_dependent_objects(include_indirect_dependencies=True)
                ]
                + [self._build_fco_validation_args()],
            ),
            indentation_level,
        )

        fv_spec = specs.create_feature_view_spec_from_args_proto(self._args, self._args_supplement)
        fco_container_specs = [*self._get_dependent_specs(), fv_spec]
        fco_container_ = fco_container.FcoContainer.from_specs(specs=fco_container_specs, root_ids=[fv_spec.id])
        self._feature_definition = feature_definition_wrapper.FeatureDefinitionWrapper(fv_spec, fco_container_)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def summary(self) -> display.Displayable:
        """Displays a human readable summary of this data source."""
        request = metadata_service_pb2.GetFeatureViewSummaryRequest(
            fco_locator=fco_locator_pb2.FcoLocator(id=self._spec.id_proto, workspace=self.info.workspace)
        )
        response = metadata_service.instance().GetFeatureViewSummary(request)
        return display.Displayable.from_fco_summary(response.fco_summary)

    def _construct_feature_set_config(self) -> feature_set_config.FeatureSetConfig:
        return feature_set_config.FeatureSetConfig.from_feature_definition(self._feature_definition)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.documented_by(materialization_api.cancel_materialization_job)
    @sdk_decorators.assert_remote_object
    def cancel_materialization_job(self, job_id: str) -> materialization_api.MaterializationJobData:
        return materialization_api.cancel_materialization_job(self.name, self.workspace, job_id)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.documented_by(materialization_api.get_materialization_job)
    @sdk_decorators.assert_remote_object
    def get_materialization_job(self, job_id: str) -> materialization_api.MaterializationJobData:
        return materialization_api.get_materialization_job(self.name, self.workspace, job_id)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.documented_by(materialization_api.list_materialization_jobs)
    @sdk_decorators.assert_remote_object
    def list_materialization_jobs(self) -> List[materialization_api.MaterializationJobData]:
        return materialization_api.list_materialization_jobs(self.name, self.workspace)

    @sdk_decorators.assert_remote_object
    def _get_materialization_status(self) -> materialization_status_pb2.MaterializationStatus:
        # TODO(TEC-13080): delete this private method when integration tests no longer use it.
        return materialization_api.get_materialization_status_response(self._spec.id_proto, self.workspace)

    @sdk_decorators.assert_remote_object
    def _get_serving_status(self):
        request = metadata_service_pb2.GetServingStatusRequest(
            feature_package_id=id_helper.IdHelper.from_string(self._feature_definition.id), workspace=self.workspace
        )
        return metadata_service.instance().GetServingStatus(request)

    def __getitem__(self, features: List[str]) -> FeatureReference:
        """
        Used to select a subset of features from a Feature View for use within a Feature Service.

        .. code-block:: python

            from tecton import FeatureService

            # `my_feature_view` is a feature view that contains three features: `my_feature_1/2/3`. The Feature Service
            # can be configured to include only two of those features like this:
            feature_service = FeatureService(
                name="feature_service",
                features=[
                    my_feature_view[["my_feature_1", "my_feature_2"]]
                ],
            )
        """
        if not isinstance(features, list):
            msg = "The `features` field must be a list"
            raise TypeError(msg)

        return FeatureReference(feature_definition=self, features=features)

    def with_name(self, namespace: str) -> FeatureReference:
        """Rename a Feature View used in a Feature Service.

        .. code-block:: python

            from tecton import FeatureService

            # The feature view in this feature service will be named "new_named_feature_view" in training data dataframe
            # columns and other metadata.
            feature_service = FeatureService(
                name="feature_service",
                features=[
                    my_feature_view.with_name("new_named_feature_view")
                ],
            )

            # Here is a more sophisticated example. The join keys for this feature service will be "transaction_id",
            # "sender_id", and "recipient_id" and will contain three feature views named "transaction_features",
            # "sender_features", and "recipient_features".
            transaction_fraud_service = FeatureService(
                name="transaction_fraud_service",
                features=[
                    # Select a subset of features from a feature view.
                    transaction_features[["amount"]],

                    # Rename a feature view and/or rebind its join keys. In this example, we want user features for both the
                    # transaction sender and recipient, so include the feature view twice and bind it to two different feature
                    # service join keys.
                    user_features.with_name("sender_features").with_join_key_map({"user_id" : "sender_id"}),
                    user_features.with_name("recipient_features").with_join_key_map({"user_id" : "recipient_id"}),
                ],
            )
        """
        return FeatureReference(feature_definition=self, namespace=namespace)

    def with_join_key_map(self, join_key_map: Dict[str, str]) -> FeatureReference:
        """Rebind join keys for a Feature View used in a Feature Service.

        The keys in `join_key_map` should be the feature view join keys, and the values should be the feature service overrides.

        .. code-block:: python

            from tecton import FeatureService

            # The join key for this feature service will be "feature_service_user_id".
            feature_service = FeatureService(
                name="feature_service",
                features=[
                    my_feature_view.with_join_key_map({"user_id" : "feature_service_user_id"}),
                ],
            )

            # Here is a more sophisticated example. The join keys for this feature service will be "transaction_id",
            # "sender_id", and "recipient_id" and will contain three feature views named "transaction_features",
            # "sender_features", and "recipient_features".
            transaction_fraud_service = FeatureService(
                name="transaction_fraud_service",
                features=[
                    # Select a subset of features from a feature view.
                    transaction_features[["amount"]],

                    # Rename a feature view and/or rebind its join keys. In this example, we want user features for both the
                    # transaction sender and recipient, so include the feature view twice and bind it to two different feature
                    # service join keys.
                    user_features.with_name("sender_features").with_join_key_map({"user_id" : "sender_id"}),
                    user_features.with_name("recipient_features").with_join_key_map({"user_id" : "recipient_id"}),
                ],
            )
        """
        return FeatureReference(feature_definition=self, override_join_keys=join_key_map.copy())


@attrs.define(eq=False)
class MaterializedFeatureView(FeatureView):
    """Class for BatchFeatureView and StreamFeatureView to inherit common methods from.

    Attributes:
        sources: The Data Sources for this Feature View.
        tranformations: The Transformations for this Feature View.
        entities: The Entities for this Feature View.
    """

    sources: Tuple[framework_data_source.DataSource, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )
    transformations: Tuple[framework_transformation.Transformation, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )
    entities: Tuple[framework_entity.Entity, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )

    @property
    def _batch_compute_mode(self) -> BatchComputeMode:
        if self._spec:
            spec = self._spec
            assert isinstance(spec, MaterializedFeatureViewSpec), spec
            return spec.batch_compute_mode
        else:
            return BatchComputeMode(self._args.batch_compute_mode)

    def _assert_supports_skip_validation(self):
        if not self._is_valid and self._batch_compute_mode not in (BatchComputeMode.SPARK, BatchComputeMode.RIFT):
            msg = f"ValidationMode.SKIP is not supported for {self._batch_compute_mode.name} FeatureViews"
            raise TectonValidationError(msg)

    @classmethod
    @typechecked
    def _from_spec(
        cls, spec: specs.MaterializedFeatureViewSpec, fco_container_: fco_container.FcoContainer
    ) -> "FeatureView":
        """Create a FeatureView from directly from a spec. Specs are assumed valid and will not be re-validated."""
        feature_definition = feature_definition_wrapper.FeatureDefinitionWrapper(spec, fco_container_)
        info = base_tecton_object.TectonObjectInfo.from_spec(spec)

        sources = []
        for data_source_spec in feature_definition.data_sources:
            sources.append(framework_data_source.data_source_from_spec(data_source_spec))

        entities = []
        for entity_spec in feature_definition.entities:
            entities.append(framework_entity.Entity._from_spec(entity_spec))

        transformations = []
        for transformation_spec in feature_definition.transformations:
            transformations.append(framework_transformation.Transformation._from_spec(transformation_spec))

        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(
            info=info,
            feature_definition=feature_definition,
            args=None,
            source_info=None,
            sources=tuple(sources),
            entities=tuple(entities),
            transformations=tuple(transformations),
            args_supplement=None,
        )

        return obj

    def _get_dependent_objects(self, include_indirect_dependencies: bool) -> List[base_tecton_object.BaseTectonObject]:
        return list(self.sources) + list(self.entities) + list(self.transformations)

    def _build_ds_specs_with_derived_schema(self) -> List[specs.DataSourceSpec]:
        specs_with_schema = []
        for ds in self.sources:
            ds_spec = ds._spec
            ds_spec_requires_schema = ds._is_valid and not ds._is_local_object and not ds_spec.schema
            if self._batch_compute_mode == BatchComputeMode.SPARK and ds_spec_requires_schema:
                # A DataSource may not have derived schema IFF it was applied without a FeatureView
                # In those cases, NDD FeatureView definitions will fail unless we force the schema derivation here.
                #
                # See https://tecton.atlassian.net/browse/TEC-18736 for additional context
                specs_with_schema.append(ds._rebuild_spec_with_schema())
            else:
                specs_with_schema.append(ds._spec)
        return specs_with_schema

    def _derive_schemas(self) -> _Schemas:
        assert all(
            obj._is_valid for obj in self.transformations + self.sources
        ), "_derive_schemas expects that dependent objects have been validated."
        return self._derive_schemas_with_specs(
            transformation_specs=[transformation._spec for transformation in self.transformations],
            data_source_specs=self._build_ds_specs_with_derived_schema(),
        )

    def _derive_schemas_with_specs(
        self,
        transformation_specs: Optional[List[specs.TransformationSpec]],
        data_source_specs: Optional[List[specs.DataSourceSpec]],
    ) -> _Schemas:
        # Note that this DOES NOT apply for Snowflake in Unified Tecton
        has_legacy_snowflake_hacks = self._batch_compute_mode == BatchComputeMode.SNOWFLAKE

        explicit_schema = None
        if self._args.materialized_feature_view_args.HasField("schema"):
            explicit_schema = self._args.materialized_feature_view_args.schema

        derived_schema = self._maybe_derive_view_schema(transformation_specs, data_source_specs)
        view_schema = explicit_schema or derived_schema
        if not view_schema:
            raise errors.SchemaRequired(self.name)

        if explicit_schema and derived_schema and not Schema(explicit_schema).is_equivalent(Schema(derived_schema)):
            raise errors.SCHEMAS_DO_NOT_MATCH(explicit_schema, derived_schema)

        materialization_schema = schema_derivation_utils.compute_aggregate_materialization_schema_from_view_schema(
            view_schema, self._args, use_anchor_time=(not has_legacy_snowflake_hacks)
        )

        if has_legacy_snowflake_hacks:
            for column in materialization_schema.columns:
                column.name = column.name.upper()

        online_batch_table_format = None
        if self._args.materialized_feature_view_args.compaction_enabled:
            online_batch_table_format = schema_derivation_utils.compute_batch_table_format(self._args, view_schema)

        return _Schemas(
            view_schema=view_schema,
            materialization_schema=materialization_schema,
            online_batch_table_format=online_batch_table_format,
        )

    def _maybe_derive_view_schema(
        self, transformation_specs: List[specs.TransformationSpec], data_source_specs: List[specs.DataSourceSpec]
    ) -> Optional[schema_pb2.Schema]:
        """Attempts to derive the view schema. Returns None if schema derivation is not supported in this configuration."""
        has_push_source = any(
            d.type
            in (
                data_source_type_pb2.DataSourceType.PUSH_NO_BATCH,
                data_source_type_pb2.DataSourceType.PUSH_WITH_BATCH,
            )
            for d in data_source_specs
        )
        if has_push_source:
            assert self._batch_compute_mode != BatchComputeMode.SNOWFLAKE
            return self._derive_push_source_schema(transformation_specs, data_source_specs)
        elif self._batch_compute_mode == BatchComputeMode.SNOWFLAKE:
            return snowflake_api.derive_view_schema_for_feature_view(
                self._args, transformation_specs, data_source_specs
            )
        elif self._batch_compute_mode == BatchComputeMode.SPARK:
            return spark_api.derive_view_schema_for_feature_view(self._args, transformation_specs, data_source_specs)
        else:
            return None

    def _derive_push_source_schema(
        self, transformation_specs: List[TransformationSpec], push_sources: List[DataSourceSpec]
    ) -> Optional[schema_pb2.Schema]:
        if len(transformation_specs) > 0:
            return None
        else:
            assert len(push_sources) == 1, "If there is a Push Source, there should be exactly one data source."
            ds_spec = push_sources[0]
            push_source_schema = ds_spec.schema.tecton_schema
            schema_derivation_utils.populate_schema_with_derived_fields(push_source_schema)
            return push_source_schema

    @sdk_decorators.assert_valid
    def _check_can_query_from_source(self, from_source: Optional[bool]) -> QuerySources:
        fd = self._feature_definition

        if fd.is_incremental_backfill:
            if self.info._is_local_object:
                raise errors.FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_IN_LOCAL_MODE(
                    self.name,
                )
            if not fd.materialization_enabled:
                raise errors.FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(
                    self.name, self.info.workspace
                )

            if from_source:
                raise core_errors.FV_BFC_SINGLE_FROM_SOURCE

            # from_source=None + offline=False computes from source which is not supported for incremental
            if from_source is None and (not fd.materialization_enabled or not fd.writes_to_offline_store):
                raise core_errors.FV_BFC_SINGLE_FROM_SOURCE
        elif from_source is False:
            if self._is_local_object:
                raise errors.FD_GET_MATERIALIZED_FEATURES_FROM_LOCAL_OBJECT(self.name, "Feature View")
            elif not fd.writes_to_offline_store:
                raise errors.FD_GET_FEATURES_MATERIALIZATION_DISABLED(self.name)
            elif not fd.materialization_enabled:
                raise errors.FD_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE_GFD(self.name, self.workspace)

        if from_source is None:
            from_source = not fd.materialization_enabled or not fd.writes_to_offline_store

        if from_source:
            return QuerySources(from_source_count=1)
        else:
            return QuerySources(offline_store_count=1)

    @sdk_decorators.sdk_public_method(
        requires_validation=True,
        supports_skip_validation=True,
    )
    def get_features_in_range(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        entities: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        max_lookback: Optional[datetime.timedelta] = None,
        from_source: Optional[bool] = None,
        mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        # TODO(ajeya): Add docstring for get_features_in_range
        compute_mode = offline_retrieval_compute_mode(compute_mode)
        if compute_mode != ComputeMode.SPARK and compute_mode != ComputeMode.RIFT:
            raise errors.GET_FEATURES_IN_RANGE_UNSUPPORTED

        if start_time >= end_time:
            raise core_errors.START_TIME_NOT_BEFORE_END_TIME(start_time, end_time)

        if self._is_valid:
            sources = self._check_can_query_from_source(from_source)
            sources.display()

        if self._feature_definition is None:
            # NOTE: when unvalidated we are requiring all the sources to be specified.
            # technically it's 'possible' that we can only require the ones
            # that are from unvalidated sources.
            feature_definition = self._create_unvalidated_feature_definition(mock_inputs)

            if from_source == False:
                raise errors.UNVALIDATED_FEATURE_VIEWS_FROM_SOURCE_FALSE(self.name, self.get_features_in_range.__name__)

            if feature_definition.is_incremental_backfill:
                raise errors.FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_MOCK_DATA(
                    self.name, self.get_features_in_range.__name__
                )
        else:
            feature_definition = self._feature_definition

        dialect = compute_mode.default_dialect()

        mock_data_sources = {}
        if mock_inputs:
            mock_data_sources = mock_source_utils.convert_mock_inputs_to_mock_sources(
                dialect, compute_mode, feature_definition, mock_inputs
            )

        return querytree_api.get_features_in_range(
            dialect=dialect,
            compute_mode=compute_mode,
            feature_definition=feature_definition,
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            max_lookback=max_lookback,
            from_source=from_source,
            mock_data_sources=mock_data_sources,
        )

    @sdk_decorators.sdk_public_method(
        requires_validation=True,
        supports_skip_validation=True,
    )
    def get_features_for_events(
        self,
        events: Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame, str],
        timestamp_key: Optional[str] = None,
        from_source: Optional[bool] = None,
        save: bool = False,
        save_as: Optional[str] = None,
        mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        """Returns a Tecton :class:`TectonDataFrame` of historical values for this feature view.

        By default (i.e. ``from_source=None``), this method fetches feature values from the Offline Store for Feature
        Views that have offline materialization enabled and otherwise computes feature values on the fly from raw data.

        :param events: A dataframe containing the join key combinations and timestamps that specify which feature values
            to fetch.
            If present, the returned DataFrame will contain rollups for all (join key, timestamp)
            combinations that are required to compute a full frame from the spine.
            To distinguish between spine columns and feature columns, feature columns are labeled as
            `feature_view_name.feature_name` in the returned DataFrame.
        :type events: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param timestamp_key: Name of the time column in the spine.
            This method will fetch the latest features computed before the specified timestamps in this column.
            If unspecified, will default to the time column of the spine if there is only one present.
            If more than one time column is present in the spine, you must specify which column you'd like to use.
        :type timestamp_key: str
        :param from_source: Whether feature values should be recomputed from the original data source. If ``None``,
            feature values will be fetched from the Offline Store for Feature Views that have offline materialization
            enabled and otherwise computes feature values on the fly from raw data. Use ``from_source=True`` to force
            computing from raw data and ``from_source=False`` to error if any Feature Views are not materialized.
            Defaults to None.
        :type from_source: bool
        :param save: Whether to persist the DataFrame as a Dataset object. Default is False.
        :type save: bool
        :param save_as: Name to save the DataFrame as.
            If unspecified and save=True, a name will be generated.
        :type save_as: str
        :param mock_inputs: mock sources that should be used instead of fetching directly from raw data
            sources. The keys of the dictionary should match the feature view's function parameters. For feature views with multiple sources, mocking some data sources and using raw data for others is supported.
        :type mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]]
        :param compute_mode: Compute mode to use to produce the data frame.
        :type compute_mode: Optional[Union[ComputeMode, str]]




        Examples:
            A FeatureView :py:mod:`fv` with join key :py:mod:`user_id`.

            1) :py:mod:`fv.get_features_for_events(spine)` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3],
            'date': [datetime(...), datetime(...), datetime(...)]})`
            Fetch features from the offline store for users 1, 2, and 3 for the specified timestamps in the spine.

            2) :py:mod:`fv.get_features_for_events(spine, save_as='my_dataset)` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date': [datetime(...), datetime(...), datetime(...)]})`
            Fetch features from the offline store for users 1, 2, and 3 for the specified timestamps in the spine. Save the DataFrame as dataset with the name :py:mod`my_dataset`.

            3) :py:mod:`fv.get_features_for_events(spine, timestamp_key='date_1')` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date_1': [datetime(...), datetime(...), datetime(...)], 'date_2': [datetime(...), datetime(...), datetime(...)]})`
            Fetch features from the offline store for users 1, 2, and 3 for the specified timestamps in the 'date_1' column in the spine.

        :return: A Tecton :class:`TectonDataFrame`.
        """
        self._assert_supports_skip_validation()
        compute_mode = offline_retrieval_compute_mode(compute_mode)
        dialect = compute_mode.default_dialect()
        if compute_mode == ComputeMode.SNOWFLAKE or compute_mode == ComputeMode.ATHENA:
            raise errors.GET_FEATURES_FOR_EVENTS_UNSUPPORTED

        if self._is_valid:
            # NOTE: we don't want to call `_check_can_query_from_source` on
            # unvalidated feature view. We implement our own checks for
            # unvalidated feature views after constructing the unvalidated
            # feature definition.
            sources = self._check_can_query_from_source(from_source)
            sources.display()

        if self._feature_definition is None:
            # NOTE: when unvalidated we are requiring all the sources to be specified.
            # technically it's 'possible' that we can only require the ones
            # that are from unvalidated sources.
            feature_definition = self._create_unvalidated_feature_definition(mock_inputs)

            if from_source == False:
                raise errors.UNVALIDATED_FEATURE_VIEWS_FROM_SOURCE_FALSE(
                    self.name, self.get_features_for_events.__name__
                )

            if feature_definition.is_incremental_backfill:
                raise errors.FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_MOCK_DATA(
                    self.name, self.get_features_for_events.__name__
                )
        else:
            feature_definition = self._feature_definition

        mock_data_sources = {}
        if mock_inputs:
            mock_data_sources = mock_source_utils.convert_mock_inputs_to_mock_sources(
                dialect, compute_mode, feature_definition, mock_inputs
            )

        return querytree_api.get_features_for_events(
            dialect=dialect,
            compute_mode=compute_mode,
            feature_definition=feature_definition,
            spine=events,
            timestamp_key=timestamp_key,
            from_source=from_source,
            save=save,
            save_as=save_as,
            mock_data_sources=mock_data_sources,
        )

    # if spine is provided, then timestamp_key is optional, but start_time, end_time, and entities cannot be used
    @overload
    def get_historical_features(
        self,
        spine: Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame, str],
        timestamp_key: Optional[str] = None,
        from_source: Optional[bool] = None,
        save: bool = False,
        save_as: Optional[str] = None,
        mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame: ...

    # if spine not provided, then timestamp_key should also not be provided.
    # start_time, end_time, and entities can be used instead.
    @overload
    def get_historical_features(
        self,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        entities: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        from_source: Optional[bool] = None,
        save: bool = False,
        save_as: Optional[str] = None,
        mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame: ...

    @sdk_decorators.sdk_public_method(
        requires_validation=True,
        supports_skip_validation=True,
    )
    def get_historical_features(
        self,
        spine: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame, str]] = None,
        timestamp_key: Optional[str] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        entities: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        from_source: Optional[bool] = None,
        save: bool = False,
        save_as: Optional[str] = None,
        mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        """Returns a Tecton :class:`TectonDataFrame` of historical values for this feature view.

        By default (i.e. ``from_source=None``), this method fetches feature values from the Offline Store for Feature
        Views that have offline materialization enabled and otherwise computes feature values on the fly from raw data.

        If no arguments are passed in, all feature values for this feature view will be returned in a Tecton DataFrame.

        Note:
        The `timestamp_key` parameter is only applicable when a spine is passed in.
        Parameters `start_time`, `end_time`, and `entities` are only applicable when a spine is not passed in.

        :param spine: The spine to join against, as a dataframe.
            If present, the returned DataFrame will contain rollups for all (join key, temporal key)
            combinations that are required to compute a full frame from the spine.
            To distinguish between spine columns and feature columns, feature columns are labeled as
            `feature_view_name.feature_name` in the returned DataFrame.
            If spine is not specified, it'll return a DataFrame of feature values in the specified time range.
        :type spine: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param timestamp_key: Name of the time column in the spine.
            This method will fetch the latest features computed before the specified timestamps in this column.
            If unspecified, will default to the time column of the spine if there is only one present.
            If more than one time column is present in the spine, you must specify which column you'd like to use.
        :type timestamp_key: str
        :param start_time: The interval start time from when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type start_time: datetime.datetime
        :param end_time: The interval end time until when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type end_time: datetime.datetime
        :param entities: Filter feature data returned to a set of entity IDs.
            If specified, this DataFrame should only contain join key columns.
        :type entities: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param from_source: Whether feature values should be recomputed from the original data source. If ``None``,
            feature values will be fetched from the Offline Store for Feature Views that have offline materialization
            enabled and otherwise computes feature values on the fly from raw data. Use ``from_source=True`` to force
            computing from raw data and ``from_source=False`` to error if any Feature Views are not materialized.
            Defaults to None.
        :type from_source: bool
        :param save: Whether to persist the DataFrame as a Dataset object. Default is False.
        :type save: bool
        :param save_as: Name to save the DataFrame as.
            If unspecified and save=True, a name will be generated.
        :type save_as: str

        :param mock_inputs: mock sources that should be used instead of fetching directly from raw data
            sources. The keys of the dictionary should match the feature view's function parameters. For feature views with multiple sources, mocking some data sources and using raw data for others is supported.
        :type mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]]
        :param compute_mode: Compute mode to use to produce the data frame.
        :type compute_mode: Optional[Union[ComputeMode, str]]




        Examples:
            A FeatureView :py:mod:`fv` with join key :py:mod:`user_id`.

            1) :py:mod:`fv.get_historical_features(spine)` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3],
            'date': [datetime(...), datetime(...), datetime(...)]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps in the spine.

            2) :py:mod:`fv.get_historical_features(spine, save_as='my_dataset)` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date': [datetime(...), datetime(...), datetime(...)]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps in the spine. Save the DataFrame as dataset with the name :py:mod`my_dataset`.

            3) :py:mod:`fv.get_historical_features(spine, timestamp_key='date_1')` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date_1': [datetime(...), datetime(...), datetime(...)], 'date_2': [datetime(...), datetime(...), datetime(...)]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps in the 'date_1' column in the spine.

            4) :py:mod:`fv.get_historical_features(start_time=datetime(...), end_time=datetime(...))`
            Fetch all historical features from the offline store in the time range specified by `start_time` and `end_time`.

        :return: A Tecton :class:`TectonDataFrame`.
        """
        self._assert_supports_skip_validation()
        if self._is_valid:
            # NOTE: we don't want to call `_check_can_query_from_source` on
            # unvalidated feature view. We implement our own checks for
            # unvalidated feature views after constructing the unvalidated
            # feature definition.
            sources = self._check_can_query_from_source(from_source)
            sources.display()

            # We need a validated feature definition to check that it has an offset window
            if self._feature_definition.has_offset_window and spine is None:
                logger.warning(
                    "Calling get_historical_features() with a specified time range on a feature view that has an offset "
                    "aggregation will not return all features. Please use get_features_in_range() to return all features in"
                    "a specified time range."
                )

        # if spine is not provided, timestamp_key cannot be set
        if spine is None and timestamp_key is not None:
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(["timestamp_key"], "the spine parameter is not provided")

        # start_time, end_time, and entities are incompatible with spine
        if spine is not None and (start_time is not None or end_time is not None or entities is not None):
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(
                ["start_time", "end_time", "entities"], "the spine parameter is provided"
            )

        if start_time is not None and end_time is not None and start_time >= end_time:
            raise core_errors.START_TIME_NOT_BEFORE_END_TIME(start_time, end_time)

        compute_mode = offline_retrieval_compute_mode(compute_mode)

        if compute_mode == ComputeMode.SNOWFLAKE and (
            conf.get_bool("USE_DEPRECATED_SNOWFLAKE_RETRIEVAL")
            or snowflake_api.has_snowpark_transformation([self._feature_definition])
        ):
            # Snowflake retrieval is now migrated to QT and this code path is deprecated.
            if snowflake_api.has_snowpark_transformation([self._feature_definition]):
                logger.warning(
                    "Snowpark transformations are deprecated in versions >=0.8. Consider using snowflake_sql transformations instead."
                )
            if mock_inputs:
                raise errors.SNOWFLAKE_COMPUTE_MOCK_SOURCES_UNSUPPORTED
            return snowflake_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                from_source=from_source,
                save=save,
                save_as=save_as,
                feature_set_config=self._construct_feature_set_config(),
                append_prefix=False,
            )

        if compute_mode == ComputeMode.ATHENA and conf.get_bool("USE_DEPRECATED_ATHENA_RETRIEVAL"):
            if self.info.workspace is None or not self._feature_definition.materialization_enabled:
                raise errors.ATHENA_COMPUTE_ONLY_SUPPORTED_IN_LIVE_WORKSPACE
            if mock_inputs:
                raise errors.ATHENA_COMPUTE_MOCK_SOURCES_UNSUPPORTED
            return athena_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                from_source=from_source,
                save=save,
                save_as=save_as,
                feature_set_config=self._construct_feature_set_config(),
            )

        dialect = compute_mode.default_dialect()
        mock_data_sources = {}

        if self._feature_definition is None:
            # NOTE: when unvalidated we are requiring all the sources to be specified.
            # technically it's 'possible' that we can only require the ones
            # that are from unvalidated sources.
            feature_definition = self._create_unvalidated_feature_definition(mock_inputs)

            if from_source == False:
                raise errors.UNVALIDATED_FEATURE_VIEWS_FROM_SOURCE_FALSE(
                    self.name, self.get_historical_features.__name__
                )

            if feature_definition.is_incremental_backfill:
                raise errors.FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_MOCK_DATA(self.name)
        else:
            feature_definition = self._feature_definition

        if mock_inputs:
            mock_data_sources = mock_source_utils.convert_mock_inputs_to_mock_sources(
                dialect, compute_mode, feature_definition, mock_inputs
            )

        return querytree_api.get_historical_features_for_feature_definition(
            dialect=dialect,
            compute_mode=compute_mode,
            feature_definition=feature_definition,
            spine=spine,
            timestamp_key=timestamp_key,
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            from_source=from_source,
            save=save,
            save_as=save_as,
            mock_data_sources=mock_data_sources,
        )

    @sdk_decorators.sdk_public_method(
        requires_validation=True,
        validation_error_message=errors.RUN_REQUIRES_VALIDATION,
        supports_skip_validation=True,
    )
    def get_partial_aggregates(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]] = None,
        entities: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        from_source: Optional[bool] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        if self._is_valid:
            sources = self._check_can_query_from_source(from_source)
            sources.display()

        if start_time is None or end_time is None:
            msg = "get_partial_aggregates() requires start_time and end_time to be set."
            raise TectonValidationError(msg)

        if start_time >= end_time:
            raise core_errors.START_TIME_NOT_BEFORE_END_TIME(start_time, end_time)

        if self._feature_definition:
            feature_definition = self._feature_definition
        else:
            # NOTE: when unvalidated we are requiring all the sources to be specified.
            # technically it's 'possible' that we can only require the ones
            # that are from unvalidated sources.
            feature_definition = self._create_unvalidated_feature_definition(mock_inputs)

            if from_source == False:
                raise errors.UNVALIDATED_FEATURE_VIEWS_FROM_SOURCE_FALSE(
                    self.name, self.get_partial_aggregates.__name__
                )

            if mock_inputs and feature_definition.is_incremental_backfill:
                raise errors.FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_MOCK_DATA(
                    self.name, self.get_partial_aggregates.__name__
                )

        if not feature_definition.is_temporal_aggregate:
            raise errors.GET_PARTIAL_AGGREGATES_UNSUPPORTED_NON_AGGREGATE()

        if feature_definition.compaction_enabled:
            raise errors.GET_PARTIAL_AGGREGATES_UNSUPPORTED_COMPACTED()

        if feature_definition.is_continuous:
            raise errors.GET_PARTIAL_AGGREGATES_UNSUPPORTED_CONTINUOUS()

        if any(ds._data_source_type == DataSourceType.PUSH_NO_BATCH for ds in self.sources):
            msg = "The `get_partial_aggregates()` method is currently unsupported for Feature Views that are backed by a PushSource without a batch_config."
            raise TectonValidationError(msg)

        if entities is not None:
            if not isinstance(entities, TectonDataFrame):
                entities = TectonDataFrame._create(entities)
            if not set(entities._dataframe.columns).issubset(set(feature_definition.join_keys)):
                msg = f"Entities should only contain columns that can be used as Join Keys: {feature_definition.join_keys}"
                raise TectonValidationError(msg)

        compute_mode = offline_retrieval_compute_mode(compute_mode)
        dialect = compute_mode.default_dialect()

        mock_data_sources = {}
        if mock_inputs:
            mock_data_sources = mock_source_utils.convert_mock_inputs_to_mock_sources(
                dialect, compute_mode, feature_definition, mock_inputs
            )

        return querytree_api.get_partial_aggregates(
            dialect=dialect,
            compute_mode=compute_mode,
            feature_definition=feature_definition,
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            mock_data_sources=mock_data_sources,
            from_source=from_source,
        )

    @sdk_decorators.sdk_public_method(
        requires_validation=True,
        validation_error_message=errors.RUN_TRANSFORMATION_REQUIRES_VALIDATION,
        supports_skip_validation=True,
    )
    def run_transformation(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        """Run the FeatureView Transformation. Supports transforming data directly from raw data sources or using mock data.

        To run the feature view transformation with data from raw data sources, the environment must have access to the data sources.

        :param start_time: The start time of the time window to materialize.
        :type start_time: datetime.datetime
        :param end_time: The end time of the time window to materialize.
        :type end_time: datetime.datetime
        :param mock_inputs: mock sources that should be used instead of fetching directly from raw data
            sources. The keys of the dictionary should match the feature view's function parameters. For feature views with multiple sources, mocking some data sources and using raw data for others is supported.
        :type mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]]
        :param compute_mode: Compute mode to use to produce the data frame.
        :type compute_mode: Optional[Union[ComputeMode, str]]

        :return: A tecton DataFrame of the results.

        Example:

        .. code-block:: python

            import tecton
            import pandas
            from datetime import datetime

            # Example running a non-aggregate feature view with mock data.
            feature_view = tecton.get_workspace("my_workspace").get_feature_view("my_feature_view")

            mock_fraud_user_data = pandas.DataFrame({
                "user_id": ["user_1", "user_2", "user_3"],
                "timestamp": [datetime(2022, 5, 1, 0), datetime(2022, 5, 1, 2), datetime(2022, 5, 1, 5)],
                "credit_card_number": [1000, 4000, 5000],
            })

            result = feature_view.run_transformation(
              start_time=datetime(2022, 5, 1),
              end_time=datetime(2022, 5, 2),
              mock_inputs={"fraud_users_batch": mock_fraud_user_data}
            )  # `fraud_users_batch` is the name of this FeatureView's data source parameter.

            # Example running an aggregate feature view with real data.
            aggregate_feature_view = tecton.get_workspace("my_workspace").get_feature_view("my_aggregate_feature_view")
            result = aggregate_feature_view.run_transformation(
              start_time=datetime(2022, 5, 1),
              end_time=datetime(2022, 5, 2)
            )
        """
        self._assert_supports_skip_validation()
        if self._feature_definition is None:
            feature_definition = self._create_unvalidated_feature_definition(mock_inputs)
        else:
            feature_definition = self._feature_definition

        if any(ds._data_source_type == DataSourceType.PUSH_NO_BATCH for ds in self.sources) and len(mock_inputs) == 0:
            msg = "The `run_transformation()` method is currently unsupported for Feature Views backed by a StreamSource without a batch_config unless mock_inputs are provided."
            raise TectonValidationError(msg)

        compute_mode = offline_retrieval_compute_mode(compute_mode)

        if compute_mode != ComputeMode.SPARK and compute_mode != ComputeMode.RIFT:
            raise errors.RUN_TRANSFORMATION_UNSUPPORTED

        if start_time is None or end_time is None:
            msg = "run_transformation() requires start_time and end_time to be set."
            raise TypeError(msg)

        if start_time >= end_time:
            raise core_errors.START_TIME_NOT_BEFORE_END_TIME(start_time, end_time)

        time_range = end_time - start_time
        if (
            feature_definition.is_incremental_backfill
            and time_range != feature_definition.batch_materialization_schedule
        ):
            logger.warning(
                f"run_transformation() time range ({start_time}, {end_time}) is not equivalent to the batch_schedule: {feature_definition.batch_materialization_schedule}. This may lead to incorrect feature values since feature views with incremental_backfills typically implicitly rely on the materialization range being equivalent to the batch_schedule."
            )

        dialect = compute_mode.default_dialect()

        mock_data_sources = {}
        if mock_inputs:
            mock_data_sources = mock_source_utils.convert_mock_inputs_to_mock_sources(
                dialect, compute_mode, feature_definition, mock_inputs
            )

        return querytree_api.run_transformation_batch(
            dialect,
            compute_mode,
            feature_definition,
            start_time,
            end_time,
            mock_data_sources,
        )

    @sdk_decorators.sdk_public_method(
        requires_validation=True,
        validation_error_message=errors.RUN_REQUIRES_VALIDATION,
        supports_skip_validation=True,
    )
    def run(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        aggregation_level: Optional[str] = None,
        mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
        **mock_inputs_kwargs: Union[pandas.DataFrame, pyspark_dataframe.DataFrame],
    ) -> TectonDataFrame:
        """Run the FeatureView. Supports transforming data directly from raw data sources or using mock data.

        To run the feature view with data from raw data sources, the environment must have access to the data sources.

        :param start_time: The start time of the time window to materialize.
        :param end_time: The end time of the time window to materialize.
        :param aggregation_level: For feature views with aggregations, `aggregation_level` configures which stage of
            the aggregation to run up to. The query for Aggregate Feature Views operates in three steps:

                1) The feature view query is run over the provided time range. The user defined transformations are applied over the data source.

                2) The result of #1 is aggregated into tiles the size of the aggregation_interval.

                3) The tiles from #2 are combined to form the final feature values. The number of tiles that are combined is based off of the time_window of the aggregation.

            For testing and debugging purposes, to see the output of #1, use ``aggregation_level="disabled"``. For #2, use ``aggregation_level="partial"``. For #3, use ``aggregation_level="full"``.

            ``aggregation_level="full"`` is the default behavior.


        :param mock_inputs: mock sources that should be used instead of fetching directly from raw data
            sources. The keys of the dictionary should match the feature view's function parameters. For feature views with multiple sources, mocking some data sources and using raw data for others is supported.
        :type mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]]

        :param compute_mode: Compute mode to use to produce the data frame.
        :type compute_mode: Optional[Union[ComputeMode, str]]

        :param \*\*mock_inputs_kwargs: kwargs for mock sources that should be used instead of fetching directly from raw data
            sources. The keys should match the feature view's function parameters. For feature views with multiple sources, mocking some data sources and using raw data for others is supported.

        :return: A tecton DataFrame of the results.

        Example:

        .. code-block:: python

            import tecton
            import pandas
            from datetime import datetime

            # Example running a non-aggregate feature view with mock data.
            feature_view = tecton.get_workspace("my_workspace").get_feature_view("my_feature_view")

            mock_fraud_user_data = pandas.DataFrame({
                "user_id": ["user_1", "user_2", "user_3"],
                "timestamp": [datetime(2022, 5, 1, 0), datetime(2022, 5, 1, 2), datetime(2022, 5, 1, 5)],
                "credit_card_number": [1000, 4000, 5000],
            })

            result = feature_view.run(
              start_time=datetime(2022, 5, 1),
              end_time=datetime(2022, 5, 2),
              fraud_users_batch=mock_fraud_user_data)  # `fraud_users_batch` is the name of this FeatureView's data source parameter.

            # Example running an aggregate feature view with real data.
            aggregate_feature_view = tecton.get_workspace("my_workspace").get_feature_view("my_aggregate_feature_view")

            result = aggregate_feature_view.run(
              start_time=datetime(2022, 5, 1),
              end_time=datetime(2022, 5, 2),
              aggregation_level="full")  # or "partial" or "disabled"
        """
        self._assert_supports_skip_validation()
        if mock_inputs:
            resolved_mock_inputs = mock_inputs
            if len(mock_inputs_kwargs) > 0:
                msg = "Mock sources cannot be configured using both the mock_inputs dictionary and using the kwargs to the `run` call."
                raise TectonValidationError(msg)
        else:
            resolved_mock_inputs = mock_inputs_kwargs

        if (
            any(ds._data_source_type == DataSourceType.PUSH_NO_BATCH for ds in self.sources)
            and len(resolved_mock_inputs) == 0
        ):
            msg = "The `run()` method is currently unsupported for Feature Views backed by a StreamSource without a batch_config unless mock_inputs are provided."
            raise TectonValidationError(msg)

        if start_time is None or end_time is None:
            msg = "run() requires start_time and end_time to be set."
            raise TypeError(msg)

        if start_time >= end_time:
            raise core_errors.START_TIME_NOT_BEFORE_END_TIME(start_time, end_time)

        if self._feature_definition is None:
            feature_definition = self._create_unvalidated_feature_definition(resolved_mock_inputs)
        else:
            feature_definition = self._feature_definition

        if feature_definition.is_temporal and aggregation_level is not None:
            raise errors.FV_UNSUPPORTED_AGGREGATION

        if feature_definition.compaction_enabled and aggregation_level == run_api_consts.AGGREGATION_LEVEL_PARTIAL:
            raise errors.RUN_API_PARTIAL_LEVEL_UNSUPPORTED_FOR_COMPACTION

        aggregation_level = run_api.validate_and_get_aggregation_level(feature_definition, aggregation_level)

        run_api.maybe_warn_incorrect_time_range_size(feature_definition, start_time, end_time, aggregation_level)

        compute_mode = offline_retrieval_compute_mode(compute_mode)

        if compute_mode == ComputeMode.SNOWFLAKE and (
            conf.get_bool("USE_DEPRECATED_SNOWFLAKE_RETRIEVAL")
            or snowflake_api.has_snowpark_transformation([self._feature_definition])
        ):
            # Snowflake retrieval is now migrated to QT and this code path is deprecated.
            if snowflake_api.has_snowpark_transformation([self._feature_definition]):
                logger.warning(
                    "Snowpark transformations are deprecated in versions >=0.8. Consider using snowflake_sql transformations instead."
                )
            return snowflake_api.run_batch(
                fd=self._feature_definition,
                feature_start_time=start_time,
                feature_end_time=end_time,
                mock_inputs=resolved_mock_inputs,
                aggregation_level=aggregation_level,
            )

        dialect = compute_mode.default_dialect()

        mock_data_sources = mock_source_utils.convert_mock_inputs_to_mock_sources(
            dialect, compute_mode, feature_definition, resolved_mock_inputs
        )

        return run_api.run_batch(
            dialect,
            compute_mode,
            feature_definition,
            start_time,
            end_time,
            mock_data_sources,
            aggregation_level=aggregation_level,
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_local_object(error_message=errors.CANNOT_USE_LOCAL_RUN_ON_REMOTE_OBJECT)
    def test_run(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        aggregation_level: Optional[str] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
        **mock_inputs: Union[pandas.DataFrame, pyspark_dataframe.DataFrame],
    ) -> TectonDataFrame:
        """Run the FeatureView using mock data sources. This requires a local spark session.

        Unlike :py:func:`run`, :py:func:`test_run` is intended for unit testing. It will not make calls to your
        connected Tecton cluster or attempt to read real data.

        :param start_time: The start time of the time window to materialize.
        :param end_time: The end time of the time window to materialize.
        :param aggregation_level: For feature views with aggregations, `aggregation_level` configures what stage of the aggregation to run up to.

            The query for Aggregate Feature Views operates in three logical steps:

                1) The feature view query is run over the provided time range. The user defined transformations are applied over the data source.

                2) The result of #1 is aggregated into tiles the size of the aggregation_interval.

                3) The tiles from #2 are combined to form the final feature values. The number of tiles that are combined is based off of the time_window of the aggregation.

            For testing and debugging purposes, to see the output of #1, use ``aggregation_level="disabled"``. For #2, use ``aggregation_level="partial"``. For #3, use ``aggregation_level="full"``.

            ``aggregation_level="full"`` is the default behavior.

        :param compute_mode: Compute mode to use to produce the data frame.
        :type compute_mode: Optional[Union[ComputeMode, str]]

        :param \*\*mock_inputs: kwargs with expected same keys as the FeatureView's inputs parameter. Each input name
            maps to a Spark DataFrame that should be evaluated for that node in the pipeline.

        Example:

        .. code-block:: python

            from datetime import datetime, timedelta
            import pandas
            from fraud.features.batch_features.user_credit_card_issuer import user_credit_card_issuer


            # The `tecton_pytest_spark_session` is a PyTest fixture that provides a
            # Tecton-defined PySpark session for testing Spark transformations and feature
            # views.
            def test_user_distinct_merchant_transaction_count_30d(tecton_pytest_spark_session):
                input_pandas_df = pandas.DataFrame({
                    "user_id": ["user_1", "user_2", "user_3", "user_4"],
                    "signup_timestamp": [datetime(2022, 5, 1)] * 4,
                    "cc_num": [1000000000000000, 4000000000000000, 5000000000000000, 6000000000000000],
                })
                input_spark_df = tecton_pytest_spark_session.createDataFrame(input_pandas_df)

                # Simulate materializing features for May 1st.
                output = user_credit_card_issuer.test_run(
                    start_time=datetime(2022, 5, 1),
                    end_time=datetime(2022, 5, 2),
                    fraud_users_batch=input_spark_df)

                actual = output.to_pandas()

                expected = pandas.DataFrame({
                    "user_id": ["user_1", "user_2", "user_3", "user_4"],
                    "signup_timestamp":  [datetime(2022, 5, 1)] * 4,
                    "credit_card_issuer": ["other", "Visa", "MasterCard", "Discover"],
                })

                pandas.testing.assert_frame_equal(actual, expected)


        :return: A :class:`tecton.TectonDataFrame` object.
        """
        # We set `TECTON_VALIDATION_MODE` here for full backwards compatibility
        # in case someone is not using the `tecton` pytest plugin.
        with conf._temporary_set("TECTON_VALIDATION_MODE", ValidationMode.SKIP.value):
            return self.run(
                start_time=start_time,
                end_time=end_time,
                aggregation_level=aggregation_level,
                compute_mode=compute_mode,
                mock_inputs=mock_inputs,
            )

    @sdk_decorators.assert_local_object
    def _create_unvalidated_feature_definition(
        self,
        mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]] = None,
    ) -> feature_definition_wrapper.FeatureDefinitionWrapper:
        compute_mode = offline_retrieval_compute_mode(conf.get_or_none("TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE"))
        # Only convert to PySpark DataFrames if we're in Spark mode.
        # For all other compute modes (RIFT, SNOWFLAKE) leave the mock_inputs as-is.
        if mock_inputs and compute_mode == ComputeMode.SPARK:
            mock_inputs = _to_pyspark_mocks(mock_inputs)
        elif not mock_inputs:
            mock_inputs = {}

        """Create an unvalidated feature definition. Used for user unit testing, where backend validation is unavailable."""
        input_name_to_ds_ids = pipeline_common.get_input_name_to_ds_id_map(self._args.pipeline)

        columns = mock_inputs.columns if isinstance(mock_inputs, pandas.DataFrame) else mock_inputs.keys()

        if set(input_name_to_ds_ids.keys()) != set(columns):
            raise errors.FV_INVALID_MOCK_SOURCES(list(columns), list(input_name_to_ds_ids.keys()))

        # It's possible to have the same data source included twice in mock_inputs under two different input names, but
        # we only need to generate an unvalidated spec once for data source. (Putting two conflicting specs with the
        # same id in the fco container will lead to erros.)
        ds_id_to_mock_df = {}
        for input_name, ds_id in input_name_to_ds_ids.items():
            mock_df = mock_inputs[input_name]
            ds_id_to_mock_df[ds_id] = mock_df

        data_source_specs = []
        for source in self.sources:
            mock_df = ds_id_to_mock_df[source.info.id]
            data_source_specs.append(source._create_unvalidated_spec(mock_df))

        transformation_specs = [transformation._create_unvalidated_spec() for transformation in self.transformations]
        entity_specs = [entity._create_unvalidated_spec() for entity in self.entities]

        schemas = self._derive_schemas_with_specs(transformation_specs, data_source_specs)

        supplement = specs.FeatureViewSpecArgsSupplement(
            view_schema=schemas.view_schema,
            materialization_schema=schemas.materialization_schema,
            online_batch_table_format=schemas.online_batch_table_format,
        )

        fv_spec = specs.create_feature_view_spec_from_args_proto(self._args, supplement)

        fco_container_specs = transformation_specs + data_source_specs + entity_specs + [fv_spec]
        fco_container_ = fco_container.FcoContainer.from_specs(specs=fco_container_specs, root_ids=[fv_spec.id])
        return feature_definition_wrapper.FeatureDefinitionWrapper(fv_spec, fco_container_)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def get_online_features(
        self,
        join_keys: Mapping[str, Union[int, np.int_, str, bytes]],
        include_join_keys_in_response: bool = False,
    ) -> FeatureVector:
        """Returns a single Tecton :class:`tecton.FeatureVector` from the Online Store.

        :param join_keys: The join keys to fetch from the online store.
        :param include_join_keys_in_response: Whether to include join keys as part of the response FeatureVector.

        Examples:
            A FeatureView :py:mod:`fv` with join key :py:mod:`user_id`.

            1) :py:mod:`fv.get_online_features(join_keys={'user_id': 1})`
            Fetch the latest features from the online store for user 1.

            2) :py:mod:`fv.get_online_features(join_keys={'user_id': 1}, include_join_keys_in_respone=True)`
            Fetch the latest features from the online store for user 1 and include the join key information (user_id=1) in the returned FeatureVector.

        :return: A :class:`tecton.FeatureVector` of the results.
        """
        if not self._feature_definition.writes_to_online_store:
            msg = "get_online_features"
            raise errors.UNSUPPORTED_OPERATION(msg, "online=True is not set for this FeatureView.")

        return query_helper._QueryHelper(self.info.workspace, feature_view_name=self.info.name).get_feature_vector(
            join_keys,
            include_join_keys_in_response,
            request_context_map={},
            request_context_schema=request_context.RequestContext({}),
        )

    @property
    @sdk_decorators.sdk_public_method
    def feature_start_time(self) -> Optional[datetime.datetime]:
        if self._args is not None:
            return (
                pendulum.instance(self._args.materialized_feature_view_args.feature_start_time.ToDatetime())
                if self._args.materialized_feature_view_args.HasField("feature_start_time")
                else None
            )
        else:
            return self._spec.feature_start_time

    @property
    @sdk_decorators.sdk_public_method
    def batch_trigger(self) -> BatchTriggerType:
        """The :class:`BatchTriggerType` for this FeatureView."""
        if self._args is not None:
            batch_trigger = specs.get_batch_trigger_from_feature_view_args(self._args)
        else:
            batch_trigger = self._spec.batch_trigger

        return BatchTriggerType(batch_trigger)

    @property
    def is_batch_trigger_manual(self) -> bool:
        """Whether this Feature View's batch trigger is BatchTriggerType.Manual."""
        return self.batch_trigger == BatchTriggerType.MANUAL

    @sdk_decorators.sdk_public_method(requires_validation=True)
    def get_timestamp_field(self) -> str:
        """Returns the nane of the timestamp field for this Feature View."""
        return self._feature_definition.fv_spec.timestamp_field

    @property
    @sdk_decorators.sdk_public_method
    def batch_schedule(self) -> Optional[datetime.timedelta]:
        """The batch schedule of this Feature View."""
        if self._args is not None:
            return specs.get_batch_schedule_from_feature_view_args(self._args)
        else:
            return self._spec.batch_schedule

    @property
    @sdk_decorators.sdk_public_method
    def aggregations(self) -> List[configs.Aggregation]:
        """List of :class:`Aggregation` configs used by this Feature View."""
        if self._args is not None:
            aggregate_features = specs.get_aggregate_features_from_feature_view_args(self._args)
        else:
            aggregate_features = self._spec.aggregate_features

        # Note that this isn't exactly what the user provided, functions like last(3) are returned as 'lastn'.
        aggregation_list = []
        for agg in aggregate_features:
            time_window_spec = create_time_window_spec_from_data_proto(agg.time_window)
            if isinstance(time_window_spec, TimeWindowSeriesSpec):
                time_window = configs.TimeWindowSeries(
                    series_start=time_window_spec.window_series_start,
                    series_end=time_window_spec.window_series_end,
                    step_size=time_window_spec.step_size,
                    window_size=time_window_spec.window_duration,
                )
            elif isinstance(time_window_spec, RelativeTimeWindowSpec):
                time_window = configs.TimeWindow(
                    window_size=time_window_spec.window_duration, offset=time_window_spec.offset
                )
            elif isinstance(time_window_spec, LifetimeWindowSpec):
                time_window = configs.LifetimeWindow()
            else:
                msg = f"Unexpected time window type: {type(time_window_spec)}"
                raise ValueError(msg)

            aggregation_list.append(
                configs.Aggregation(
                    column=agg.input_feature_name,
                    function=aggregation_utils.get_aggregation_function_name(agg.function),
                    time_window=time_window,
                    name=agg.output_feature_name,
                )
            )

        return aggregation_list

    @property
    @sdk_decorators.sdk_public_method
    def max_source_data_delay(self) -> datetime.timedelta:
        """Returns the maximum data delay of input sources for this feature view."""
        return max([source.data_delay for source in self.sources]) or datetime.timedelta(0)

    @property
    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def published_features_path(self) -> Optional[str]:
        """The location of published features in the offline store.

        Returns None if materialization has not been enabled for the feature view.
        """
        return self._feature_definition.published_features_path

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def delete_keys(
        self,
        keys: Union[pyspark_dataframe.DataFrame, pandas.DataFrame],
        online: bool = True,
        offline: bool = True,
    ) -> List[str]:
        """Deletes any materialized data that matches the specified join keys from the FeatureView.

        This method kicks off a job to delete the data in the offline and online stores.
        If a FeatureView has multiple entities, the full set of join keys must be specified.
        Only supports Delta as the offline store.(offline_store=DeltaConfig())
        Maximum 500,000 keys can be deleted per request.

        :param keys: The Dataframe to be deleted. Must conform to the FeatureView join keys.
        :param online: (Optional, default=True) Whether or not to delete from the online store.
        :param offline: (Optional, default=True) Whether or not to delete from the offline store.
        :return: List of job ids for jobs created for entity deletion.
        """
        is_live_workspace = internal_utils.is_live_workspace(self.info.workspace)
        if not is_live_workspace:
            msg = "delete_keys"
            raise errors.UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE(msg)

        return delete_keys_api.delete_keys(online, offline, keys, self._feature_definition)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def materialization_status(
        self, verbose=False, limit=1000, sort_columns=None, errors_only=False
    ) -> display.Displayable:
        """Displays materialization information for the FeatureView, which may include past jobs, scheduled jobs,
        and job failures.

        This method returns different information depending on the type of FeatureView.
        :param verbose: If set to true, method will display additional low level materialization information,
        useful for debugging.
        :param limit: Maximum number of jobs to return.
        :param sort_columns: A comma-separated list of column names by which to sort the rows.
        :param errors_only: If set to true, method will only return jobs that failed with an error.
        """
        return materialization_api.get_materialization_status_for_display(
            self._spec.id_proto, self.workspace, verbose, limit, sort_columns, errors_only
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.documented_by(materialization_api.trigger_materialization_job)
    @sdk_decorators.assert_remote_object
    def trigger_materialization_job(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        online: bool,
        offline: bool,
        use_tecton_managed_retries: bool = True,
        overwrite: bool = False,
    ) -> str:
        return materialization_api.trigger_materialization_job(
            self.name, self.workspace, start_time, end_time, online, offline, use_tecton_managed_retries, overwrite
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.documented_by(materialization_api.wait_for_materialization_job)
    @sdk_decorators.assert_remote_object
    def wait_for_materialization_job(
        self,
        job_id: str,
        timeout: Optional[datetime.timedelta] = None,
    ) -> materialization_api.MaterializationJobData:
        return materialization_api.wait_for_materialization_job(self.name, self.workspace, job_id, timeout)


@attrs.define(eq=False)
class BatchFeatureView(MaterializedFeatureView):
    """A Tecton Batch Feature View, used for materializing features on a batch schedule from a BatchSource.

    The BatchFeatureView should not be instantiated directly and the :py:func:`tecton.batch_feature_view`
    decorator is recommended instead.

    Attributes:
        entities: The Entities for this Feature View.
        info: A dataclass containing basic info about this Tecton Object.
        sources: The Source inputs for this Feature View.
        transformations: The Transformations used by this Feature View.
    """

    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        prevent_destroy: bool = False,
        feature_view_function: Callable,
        sources: Sequence[Union[framework_data_source.BatchSource, filtered_source.FilteredSource]],
        entities: Sequence[framework_entity.Entity],
        mode: str,
        aggregation_interval: Optional[datetime.timedelta] = None,
        aggregations: Optional[Sequence[configs.Aggregation]] = None,
        aggregation_secondary_key: Optional[str] = None,
        online: bool = False,
        offline: bool = False,
        ttl: Optional[datetime.timedelta] = None,
        feature_start_time: Optional[datetime.datetime] = None,
        lifetime_start_time: Optional[datetime.datetime] = None,
        manual_trigger_backfill_end_time: Optional[datetime.datetime] = None,
        batch_trigger: BatchTriggerType = BatchTriggerType.SCHEDULED,
        batch_schedule: Optional[datetime.timedelta] = None,
        online_serving_index: Optional[Sequence[str]] = None,
        batch_compute: Optional[configs.ComputeConfigTypes] = None,
        offline_store: Optional[Union[configs.OfflineStoreConfig, configs.ParquetConfig, configs.DeltaConfig]] = None,
        online_store: Optional[configs.OnlineStoreTypes] = None,
        monitor_freshness: bool = False,
        data_quality_enabled: Optional[bool] = None,
        skip_default_expectations: Optional[bool] = None,
        expected_feature_freshness: Optional[datetime.timedelta] = None,
        alert_email: Optional[str] = None,
        timestamp_field: Optional[str] = None,
        max_backfill_interval: Optional[datetime.timedelta] = None,
        incremental_backfills: bool = False,
        schema: Optional[List[types.Field]] = None,
        run_transformation_validation: Optional[bool] = None,
        options: Optional[Dict[str, str]] = None,
        tecton_materialization_runtime: Optional[str] = None,
        cache_config: Optional[configs.CacheConfig] = None,
        compaction_enabled: bool = False,
        environment: Optional[str] = None,
    ):
        from tecton.cli import repo_utils as cli_common

        if online_store is None:
            online_store = repo_config.get_batch_feature_view_defaults().online_store

        if offline_store is None:
            offline_store = repo_config.get_batch_feature_view_defaults().offline_store_config
        elif isinstance(offline_store, (configs.DeltaConfig, configs.ParquetConfig)):
            offline_store = configs.OfflineStoreConfig(staging_table_format=offline_store)

        if batch_compute is None:
            batch_compute = repo_config.get_batch_feature_view_defaults().batch_compute

        if tecton_materialization_runtime is None:
            tecton_materialization_runtime = (
                repo_config.get_batch_feature_view_defaults().tecton_materialization_runtime
            )

        if mode == PIPELINE_MODE:
            pipeline_function = feature_view_function
        else:
            # Separate out the Transformation and manually construct a simple pipeline function.
            # We infer owner/family/tags but not a description.
            inferred_transform = framework_transformation.transformation(mode, name, description, owner, tags=tags)(
                feature_view_function
            )

            def pipeline_function(**kwargs):
                return inferred_transform(**kwargs)

        _validate_fv_input_count(sources, feature_view_function)
        pipeline_root = _build_pipeline_for_materialized_feature_view(
            name, feature_view_function, pipeline_function, sources
        )

        # Batch Feature Views requiring a stream_processing_mode is a legacy of when stream_processing_mode was
        # called aggregation_mode (which existed in 0.6 and prior). Changing this would break `tecton plan` for
        # customers without some backend handling.
        stream_processing_mode = StreamProcessingMode.TIME_INTERVAL if aggregations else None

        if (
            environment is None
            and infer_batch_compute_mode(
                pipeline_root=pipeline_root, batch_compute_config=batch_compute, stream_compute_config=None
            )
            == BatchComputeMode.RIFT
        ):
            environment = repo_config.get_batch_feature_view_defaults().environment

        args = _build_materialized_feature_view_args(
            feature_view_type=feature_view__args_pb2.FeatureViewType.FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW,
            name=name,
            prevent_destroy=prevent_destroy,
            pipeline_root=pipeline_root,
            entities=entities,
            online=online,
            offline=offline,
            offline_store=offline_store,
            online_store=online_store,
            aggregation_interval=aggregation_interval,
            stream_processing_mode=stream_processing_mode,
            aggregations=aggregations,
            aggregation_secondary_key=aggregation_secondary_key,
            ttl=ttl,
            feature_start_time=feature_start_time,
            lifetime_start_time=lifetime_start_time,
            manual_trigger_backfill_end_time=manual_trigger_backfill_end_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=None,
            monitor_freshness=monitor_freshness,
            data_quality_enabled=data_quality_enabled,
            skip_default_expectations=skip_default_expectations,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            description=description,
            owner=owner,
            tags=tags,
            timestamp_field=timestamp_field,
            data_source_type=data_source_type_pb2.DataSourceType.BATCH,
            max_backfill_interval=max_backfill_interval,
            output_stream=None,
            incremental_backfills=incremental_backfills,
            schema=schema,
            run_transformation_validation=run_transformation_validation,
            options=options,
            tecton_materialization_runtime=tecton_materialization_runtime,
            cache_config=cache_config,
            compaction_enabled=compaction_enabled,
            environment=environment,
        )

        info = base_tecton_object.TectonObjectInfo.from_args_proto(args.info, args.feature_view_id)

        data_sources = tuple(
            source.source if isinstance(source, filtered_source.FilteredSource) else source for source in sources
        )

        source_info = cli_common.construct_fco_source_info(args.feature_view_id)
        self.__attrs_init__(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            sources=data_sources,
            entities=tuple(entities),
            transformations=tuple(pipeline_root.transformations),
            args_supplement=None,
        )
        base_tecton_object._register_local_object(self)


@typechecked
def batch_feature_view(
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    prevent_destroy: bool = False,
    mode: str,
    sources: Sequence[Union[framework_data_source.BatchSource, filtered_source.FilteredSource]],
    entities: Sequence[framework_entity.Entity],
    aggregation_interval: Optional[datetime.timedelta] = None,
    aggregations: Optional[Sequence[configs.Aggregation]] = None,
    aggregation_secondary_key: Optional[str] = None,
    online: bool = False,
    offline: bool = False,
    ttl: Optional[datetime.timedelta] = None,
    feature_start_time: Optional[datetime.datetime] = None,
    lifetime_start_time: Optional[datetime.datetime] = None,
    manual_trigger_backfill_end_time: Optional[datetime.datetime] = None,
    batch_trigger: BatchTriggerType = BatchTriggerType.SCHEDULED,
    batch_schedule: Optional[datetime.timedelta] = None,
    online_serving_index: Optional[Sequence[str]] = None,
    batch_compute: Optional[configs.ComputeConfigTypes] = None,
    offline_store: Optional[Union[configs.OfflineStoreConfig, configs.ParquetConfig, configs.DeltaConfig]] = None,
    online_store: Optional[configs.OnlineStoreTypes] = None,
    monitor_freshness: bool = False,
    data_quality_enabled: Optional[bool] = None,
    skip_default_expectations: Optional[bool] = None,
    expected_feature_freshness: Optional[datetime.timedelta] = None,
    alert_email: Optional[str] = None,
    timestamp_field: Optional[str] = None,
    max_backfill_interval: Optional[datetime.timedelta] = None,
    max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
    incremental_backfills: bool = False,
    schema: Optional[List[types.Field]] = None,
    run_transformation_validation: Optional[bool] = None,
    options: Optional[Dict[str, str]] = None,
    tecton_materialization_runtime: Optional[str] = None,
    cache_config: Optional[configs.CacheConfig] = None,
    batch_compaction_enabled: Optional[bool] = None,
    compaction_enabled: Optional[bool] = None,
    environment: Optional[str] = None,
):
    """Declare a Batch Feature View.

    :param mode: Whether the annotated function is a pipeline function ("pipeline" mode) or a transformation mode
        ("spark_sql", "pyspark", "snowflake_sql", "snowpark", "python", or "pandas"). For the non-pipeline mode, an
        inferred transformation will also be registered.
    :param sources: The data source inputs to the feature view.
    :param entities: The entities this feature view is associated with.
    :param aggregation_interval: How frequently the feature values are updated (for example, `"1h"` or `"6h"`). Only valid when using aggregations.
    :param aggregations: A list of :class:`Aggregation` structs.
    :param aggregation_secondary_key: Configures secondary key aggregates using the set column. Only valid when using aggregations.
    :param online: Whether the feature view should be materialized to the online feature store. (Default: False)
    :param offline: Whether the feature view should be materialized to the offline feature store. (Default: False)
    :param ttl: The TTL (or "look back window") for features defined by this feature view. This parameter determines how long features will live in the online store and how far to  "look back" relative to a training example's timestamp when generating offline training sets. Shorter TTLs improve performance and reduce costs.
    :param feature_start_time: When materialization for this feature view should start from. (Required if offline=true)
    :param lifetime_start_time: The start time for what data should be included in a lifetime aggregate. (Required if using lifetime windows)
    :param batch_schedule: The interval at which batch materialization should be scheduled.
    :param online_serving_index: (Advanced) Defines the set of join keys that will be indexed and queryable during online serving.
    :param batch_trigger: Defines the mechanism for initiating batch materialization jobs.
        One of ``BatchTriggerType.SCHEDULED`` or ``BatchTriggerType.MANUAL``.
        The default value is ``BatchTriggerType.SCHEDULED``, where Tecton will run materialization jobs based on the
        schedule defined by the ``batch_schedule`` parameter. If set to ``BatchTriggerType.MANUAL``, then batch
        materialization jobs must be explicitly initiated by the user through either the Tecton SDK or Airflow operator.
    :param batch_compute: Configuration for the batch materialization cluster.
    :param offline_store: Configuration for how data is written to the offline feature store.
    :param online_store: Configuration for how data is written to the online feature store.
    :param monitor_freshness: If true, enables monitoring when feature data is materialized to the online feature store.
    :param data_quality_enabled: If false, disables data quality metric computation and data quality dashboard.
    :param skip_default_expectations: If true, skips validating default expectations on the feature data.
    :param expected_feature_freshness: Threshold used to determine if recently materialized feature data is stale. Data is stale if ``now - most_recent_feature_value_timestamp > expected_feature_freshness``. For feature views using Tecton aggregations, data is stale if ``now - round_up_to_aggregation_interval(most_recent_feature_value_timestamp) > expected_feature_freshness``. Where ``round_up_to_aggregation_interval()`` rounds up the feature timestamp to the end of the ``aggregation_interval``. Value must be at least 2 times ``aggregation_interval``. If not specified, a value determined by the Tecton backend is used.
    :param alert_email: Email that alerts for this FeatureView will be sent to.
    :param description: A human readable description.
    :param owner: Owner name (typically the email of the primary maintainer).
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
        destructive update) during tecton plan/apply. To remove or update this object, ``prevent_destroy`` must be set to
        False via the same tecton apply or a separate tecton apply. ``prevent_destroy`` can be used to prevent accidental changes
        such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
        triggers expensive rematerialization jobs. ``prevent_destroy`` also blocks changes to dependent Tecton objects
        that would trigger a recreate of the tagged object, e.g. if ``prevent_destroy`` is set on a Feature Service,
        that will also prevent deletions or re-creates of Feature Views used in that service. ``prevent_destroy`` is
        only enforced in live (i.e. non-dev) workspaces.
    :param timestamp_field: The column name that refers to the timestamp for records that are produced by the
        feature view. This parameter is optional if exactly one column is a Timestamp type. This parameter is
        required if using Tecton on Snowflake without Snowpark.
    :param name: Unique, human friendly name that identifies the FeatureView. Defaults to the function name.
    :param max_batch_aggregation_interval: Deprecated. Use max_backfill_interval instead, which has the exact same usage.
    :param max_backfill_interval: (Advanced) The time interval for which each backfill job will run to materialize
        feature data. This affects the number of backfill jobs that will run, which is
        (`<feature registration time>` - `feature_start_time`) / `max_backfill_interval`.
        Configuring the `max_backfill_interval` parameter appropriately will help to optimize large backfill jobs.
        If this parameter is not specified, then 10 backfill jobs will run (the default).

    :param incremental_backfills: If set to `True`, the feature view will be backfilled one interval at a time as
        if it had been updated "incrementally" since its feature_start_time. For example, if ``batch_schedule`` is 1 day
        and ``feature_start_time`` is 1 year prior to the current time, then the backfill will run 365 separate
        backfill queries to fill the historical feature data.
    :param manual_trigger_backfill_end_time: If set, Tecton will schedule backfill materialization jobs for this feature
        view up to this time. Materialization jobs after this point must be triggered manually. (This param is only valid
        to set if BatchTriggerType is MANUAL.)
    :param options: Additional options to configure the Feature View. Used for advanced use cases and beta features.
    :param schema: The output schema of the Feature View transformation. If provided and ``run_transformation_validations=True``,
        then Tecton will validate that the Feature View matches the expected schema.
    :param run_transformation_validation: If `True`, Tecton will execute the Feature View transformations during tecton plan/apply
        validation. If `False`, then Tecton will not execute the transformations during validation and ``schema`` must be
        set. Skipping query validation can be useful to speed up tecton plan/apply or for Feature Views that have issues
        with Tecton's validation (e.g. some pip dependencies). Default is True for Spark and Snowflake Feature Views and
        False for Python and Pandas Feature Views.
    :param tecton_materialization_runtime: Version of `tecton` package used by your job cluster.
    :param cache_config: Cache config for the Feature View. Including this option enables the feature server to use the cache
        when retrieving features for this feature view. Will only be respected if the feature service containing this feature
        view has `enable_online_caching` set to `True`.
    :param batch_compaction_enabled: Deprecated: Please use `compaction_enabled` instead which has the exact same usage.
     :param compaction_enabled: (Private preview) If `True`, Tecton will run a compaction job after each batch
        materialization job to write to the online store. This requires the use of Dynamo and uses the ImportTable API.
        Because each batch job overwrites the online store, a larger compute cluster may be required.
    :param environment: The custom environment in which materialization jobs will be run. Defaults to `None`, which means
        jobs will execute in the default Tecton environment.

    :return: An object of type :class:`tecton.BatchFeatureView`.

    Example BatchFeatureView declaration:

    .. code-block:: python

        from datetime import datetime
        from datetime import timedelta

        from fraud.entities import user
        from fraud.data_sources.credit_scores_batch import credit_scores_batch

        from tecton import batch_feature_view, Aggregation, FilteredSource

        @batch_feature_view(
            sources=[FilteredSource(credit_scores_batch)],
            entities=[user],
            mode='spark_sql',
            online=True,
            offline=True,
            feature_start_time=datetime(2020, 10, 10),
            batch_schedule=timedelta(days=1),
            ttl=timedelta(days=60),
            description="Features about the users most recent transaction in the past 60 days. Updated daily.",
            )

        def user_last_transaction_features(credit_scores_batch):
            return f'''
                SELECT
                    USER_ID,
                    TIMESTAMP,
                    AMOUNT as LAST_TRANSACTION_AMOUNT,
                    CATEGORY as LAST_TRANSACTION_CATEGORY
                FROM
                    {credit_scores_batch}
            '''

    Example BatchFeatureView declaration using aggregates:

    .. code-block:: python

        from datetime import datetime
        from datetime import timedelta

        from fraud.entities import user
        from fraud.data_sources.credit_scores_batch import credit_scores_batch

        from tecton import batch_feature_view, Aggregation, FilteredSource

        @batch_feature_view(
            sources=[FilteredSource(credit_scores_batch)],
            entities=[user],
            mode='spark_sql',
            online=True,
            offline=True,
            feature_start_time=datetime(2020, 10, 10),
            aggregations=[
                Aggregation(column="amount", function="mean", time_window=timedelta(days=1)),
                Aggregation(column="amount", function="mean", time_window=timedelta(days=30)),
            ],
            aggregation_interval=timedelta(days=1),
            description="Transaction amount statistics and total over a series of time windows, updated daily.",
            )

        def user_recent_transaction_aggregate_features(credit_scores_batch):
            return f'''
                SELECT
                    USER_ID,
                    AMOUNT,
                    TIMESTAMP
                FROM
                    {credit_scores_batch}
            '''
    """

    # TODO(deprecate_after=0.8): This warning can be completely removed in 0.9, so it can be deleted once the 0.8 branch is cut.
    if max_batch_aggregation_interval is not None:
        msg = "FeatureView.max_batch_aggregation_interval is deprecated and is no longer supported in 0.8. Please use max_backfill_interval instead. max_backfill_interval has the same semantics and is just a new name."
        raise ValueError(msg)

    if batch_compaction_enabled is not None and compaction_enabled is not None:
        msg = "FeatureView.batch_compaction_enabled is deprecated. Please use compaction_enabled instead. compaction_enabled has the same semantics and is just a new name."
        raise TectonValidationError(msg)

    compaction_enabled = compaction_enabled or batch_compaction_enabled or False

    def decorator(feature_view_function):
        return BatchFeatureView(
            name=name or feature_view_function.__name__,
            description=description,
            owner=owner,
            tags=tags,
            prevent_destroy=prevent_destroy,
            feature_view_function=feature_view_function,
            mode=mode,
            sources=sources,
            entities=entities,
            aggregation_interval=aggregation_interval,
            aggregations=aggregations,
            aggregation_secondary_key=aggregation_secondary_key,
            online=online,
            offline=offline,
            ttl=ttl,
            feature_start_time=feature_start_time,
            lifetime_start_time=lifetime_start_time,
            manual_trigger_backfill_end_time=manual_trigger_backfill_end_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            offline_store=offline_store,
            online_store=online_store,
            monitor_freshness=monitor_freshness,
            data_quality_enabled=data_quality_enabled,
            skip_default_expectations=skip_default_expectations,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            timestamp_field=timestamp_field,
            max_backfill_interval=max_backfill_interval,
            incremental_backfills=incremental_backfills,
            schema=schema,
            run_transformation_validation=run_transformation_validation,
            options=options,
            tecton_materialization_runtime=tecton_materialization_runtime,
            cache_config=cache_config,
            compaction_enabled=compaction_enabled,
            environment=environment,
        )

    return decorator


@attrs.define(eq=False)
class StreamFeatureView(MaterializedFeatureView):
    """A Tecton Stream Feature View, used for transforming and materializing features from a StreamSource.

    The StreamFeatureView should not be instantiated directly and the :py:func:`tecton.stream_feature_view`
    decorator is recommended instead.

    Attributes:
        entities: The Entities for this Feature View.
        info: A dataclass containing basic info about this Tecton Object.
        sources: The Source inputs for this Feature View.
        transformations: The Transformations used by this Feature View.
    """

    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        prevent_destroy: bool = False,
        feature_view_function: Optional[Callable] = None,
        source: Union[
            framework_data_source.StreamSource, framework_data_source.PushSource, filtered_source.FilteredSource
        ],
        entities: Sequence[framework_entity.Entity],
        mode: Optional[str] = None,
        aggregation_interval: Optional[datetime.timedelta] = None,
        aggregations: Optional[Sequence[configs.Aggregation]] = None,
        aggregation_secondary_key: Optional[str] = None,
        stream_processing_mode: Optional[StreamProcessingMode] = None,
        online: bool = False,
        offline: bool = False,
        ttl: Optional[datetime.timedelta] = None,
        feature_start_time: Optional[datetime.datetime] = None,
        lifetime_start_time: Optional[datetime.datetime] = None,
        manual_trigger_backfill_end_time: Optional[datetime.datetime] = None,
        batch_trigger: BatchTriggerType = None,
        batch_schedule: Optional[datetime.timedelta] = None,
        online_serving_index: Optional[Sequence[str]] = None,
        batch_compute: Optional[configs.ComputeConfigTypes] = None,
        stream_compute: Optional[configs.ComputeConfigTypes] = None,
        offline_store: Optional[Union[configs.OfflineStoreConfig, configs.ParquetConfig, configs.DeltaConfig]] = None,
        online_store: Optional[configs.OnlineStoreTypes] = None,
        monitor_freshness: bool = False,
        data_quality_enabled: Optional[bool] = None,
        skip_default_expectations: Optional[bool] = None,
        expected_feature_freshness: Optional[datetime.timedelta] = None,
        alert_email: Optional[str] = None,
        timestamp_field: Optional[str] = None,
        max_backfill_interval: Optional[datetime.timedelta] = None,
        output_stream: Optional[configs.OutputStream] = None,
        schema: Optional[List[types.Field]] = None,
        run_transformation_validation: Optional[bool] = None,
        options: Optional[Dict[str, str]] = None,
        tecton_materialization_runtime: Optional[str] = None,
        cache_config: Optional[configs.CacheConfig] = None,
        compaction_enabled: bool = False,
        stream_tiling_enabled: bool = False,
        environment: Optional[str] = None,
    ):
        """Construct a StreamFeatureView.

        `init` should not be used directly, and instead :py:func:`tecton.stream_feature_view` decorator is recommended.
        """
        from tecton.cli import repo_utils as cli_common

        if online_store is None:
            online_store = repo_config.get_stream_feature_view_defaults().online_store

        if offline_store is None:
            offline_store = repo_config.get_stream_feature_view_defaults().offline_store_config
        elif isinstance(offline_store, (configs.DeltaConfig, configs.ParquetConfig)):
            offline_store = configs.OfflineStoreConfig(staging_table_format=offline_store)

        if batch_compute is None:
            batch_compute = repo_config.get_stream_feature_view_defaults().batch_compute

        if tecton_materialization_runtime is None:
            tecton_materialization_runtime = (
                repo_config.get_stream_feature_view_defaults().tecton_materialization_runtime
            )

        data_source = source.source if isinstance(source, filtered_source.FilteredSource) else source
        data_source_type = data_source._data_source_type

        has_push_source = data_source_type in {
            data_source_type_pb2.DataSourceType.PUSH_NO_BATCH,
            data_source_type_pb2.DataSourceType.PUSH_WITH_BATCH,
        }

        if stream_compute is None and not has_push_source:
            # The stream compute default should not be applied for Stream Feature Views with Push Sources, since they
            # don't have any stream compute.
            stream_compute = repo_config.get_stream_feature_view_defaults().stream_compute

        _validate_fv_input_count([source], feature_view_function)

        if stream_processing_mode is None:
            stream_processing_mode_ = _compute_default_stream_processing_mode(
                has_push_source,
                aggregations,
                compaction_enabled,
                stream_tiling_enabled,
            )
        else:
            if aggregations:
                stream_processing_mode_ = stream_processing_mode or StreamProcessingMode.TIME_INTERVAL
            else:
                stream_processing_mode_ = stream_processing_mode

        if feature_view_function:
            pipeline_function = _get_or_create_pipeline_function(
                name=name,
                mode=mode,
                description=description,
                owner=owner,
                tags=tags,
                feature_view_function=feature_view_function,
            )
            pipeline_root = _build_pipeline_for_materialized_feature_view(
                name,
                feature_view_function,
                pipeline_function,
                [source],
            )
        else:
            pipeline_root = _source_to_pipeline_node(source=source, input_name=data_source.name)

        if data_source_type == data_source_type_pb2.DataSourceType.PUSH_NO_BATCH:
            default_batch_trigger = BatchTriggerType.NO_BATCH_MATERIALIZATION
        else:
            default_batch_trigger = BatchTriggerType.SCHEDULED

        batch_trigger_ = batch_trigger or default_batch_trigger

        if (
            environment is None
            and infer_batch_compute_mode(
                pipeline_root=pipeline_root, batch_compute_config=batch_compute, stream_compute_config=stream_compute
            )
            == BatchComputeMode.RIFT
        ):
            environment = repo_config.get_stream_feature_view_defaults().environment

        args = _build_materialized_feature_view_args(
            feature_view_type=feature_view__args_pb2.FeatureViewType.FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW,
            name=name,
            prevent_destroy=prevent_destroy,
            pipeline_root=pipeline_root,
            entities=entities,
            online=online,
            offline=offline,
            offline_store=offline_store,
            online_store=online_store,
            aggregation_interval=aggregation_interval,
            stream_processing_mode=stream_processing_mode_,
            aggregations=aggregations,
            aggregation_secondary_key=aggregation_secondary_key,
            ttl=ttl,
            feature_start_time=feature_start_time,
            lifetime_start_time=lifetime_start_time,
            manual_trigger_backfill_end_time=manual_trigger_backfill_end_time,
            batch_trigger=batch_trigger_,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=stream_compute,
            monitor_freshness=monitor_freshness,
            data_quality_enabled=data_quality_enabled,
            skip_default_expectations=skip_default_expectations,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            description=description,
            owner=owner,
            tags=tags,
            timestamp_field=timestamp_field,
            data_source_type=data_source_type,
            max_backfill_interval=max_backfill_interval,
            output_stream=output_stream,
            incremental_backfills=False,
            schema=schema,
            run_transformation_validation=run_transformation_validation,
            options=options,
            tecton_materialization_runtime=tecton_materialization_runtime,
            cache_config=cache_config,
            stream_tiling_enabled=stream_tiling_enabled,
            compaction_enabled=compaction_enabled,
            environment=environment,
        )

        info = base_tecton_object.TectonObjectInfo.from_args_proto(args.info, args.feature_view_id)

        data_sources = (source.source if isinstance(source, filtered_source.FilteredSource) else source,)

        source_info = cli_common.construct_fco_source_info(args.feature_view_id)
        self.__attrs_init__(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            sources=data_sources,
            entities=tuple(entities),
            transformations=tuple(pipeline_root.transformations),
            args_supplement=None,
        )
        base_tecton_object._register_local_object(self)

    @sdk_decorators.sdk_public_method(requires_validation=True)
    def run_stream(self, output_temp_table: str, checkpoint_dir: Optional[str] = None) -> streaming.StreamingQuery:
        """Starts a streaming job to keep writing the output records of this FeatureView to a temporary table.

        The job will be running until the execution is terminated.

        After records have been written to the table, they can be queried using `spark.sql()`.
        If ran in a Databricks notebook, Databricks will also automatically visualize the number of incoming records.

        :param output_temp_table: The name of the temporary table to write to.
        :param checkpoint_dir: A root directory that the streaming job will checkpoint to.

        Example:

            1) :py:mod:`fv.run_stream(output_temp_table="temp_table")` Start a streaming job.

            2) :py:mod:`display(spark.sql("SELECT * FROM temp_table LIMIT 5"))` Query the output table, and display the output dataframe.
        """
        if self._spec.data_source_type != data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH:
            raise errors.FEATURE_VIEW_HAS_NO_STREAM_SOURCE(self.name)
        return run_api.run_stream(self._feature_definition, output_temp_table, checkpoint_dir)


@typechecked
def stream_feature_view(
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    prevent_destroy: bool = False,
    source: Union[framework_data_source.StreamSource, framework_data_source.PushSource, filtered_source.FilteredSource],
    entities: Sequence[framework_entity.Entity],
    mode: str,
    aggregation_interval: Optional[datetime.timedelta] = None,
    aggregations: Optional[Sequence[configs.Aggregation]] = None,
    aggregation_secondary_key: Optional[str] = None,
    stream_processing_mode: Optional[StreamProcessingMode] = None,
    online: bool = False,
    offline: bool = False,
    ttl: Optional[datetime.timedelta] = None,
    feature_start_time: Optional[datetime.datetime] = None,
    lifetime_start_time: Optional[datetime.datetime] = None,
    manual_trigger_backfill_end_time: Optional[datetime.datetime] = None,
    batch_trigger: BatchTriggerType = None,
    batch_schedule: Optional[datetime.timedelta] = None,
    online_serving_index: Optional[Sequence[str]] = None,
    batch_compute: Optional[configs.ComputeConfigTypes] = None,
    stream_compute: Optional[configs.ComputeConfigTypes] = None,
    offline_store: Optional[Union[configs.OfflineStoreConfig, configs.ParquetConfig, configs.DeltaConfig]] = None,
    online_store: Optional[configs.OnlineStoreTypes] = None,
    monitor_freshness: bool = False,
    data_quality_enabled: Optional[bool] = None,
    skip_default_expectations: Optional[bool] = None,
    expected_feature_freshness: Optional[datetime.timedelta] = None,
    alert_email: Optional[str] = None,
    timestamp_field: Optional[str] = None,
    max_backfill_interval: Optional[datetime.timedelta] = None,
    max_batch_aggregation_interval: Optional[datetime.timedelta] = None,
    output_stream: Optional[configs.OutputStream] = None,
    schema: Optional[List[types.Field]] = None,
    options: Optional[Dict[str, str]] = None,
    run_transformation_validation: Optional[bool] = None,
    tecton_materialization_runtime: Optional[str] = None,
    cache_config: Optional[configs.CacheConfig] = None,
    stream_compaction_enabled: Optional[bool] = None,
    batch_compaction_enabled: Optional[bool] = None,
    compaction_enabled: Optional[bool] = None,
    stream_tiling_enabled: Optional[bool] = None,
    environment: Optional[str] = None,
):
    """Declare a Stream Feature View.

    :param mode: Whether the annotated function is a pipeline function ("pipeline" mode) or a transformation function ("spark_sql" or "pyspark" mode).
        For the non-pipeline mode, an inferred transformation will also be registered.
    :param source: The data source input to the feature view.
    :param entities: The entities this feature view is associated with.
    :param aggregation_interval: How frequently the feature value is updated (for example, `"1h"` or `"6h"`)
    :param stream_processing_mode: Whether aggregations should be "batched" in time intervals or be updated continuously.
        Continuously aggregated features are fresher but more expensive. One of ``StreamProcessingMode.TIME_INTERVAL`` or
        ``StreamProcessingMode.CONTINUOUS``. Defaults to ``StreamProcessingMode.TIME_INTERVAL``.
    :param aggregations: A list of :class:`Aggregation` structs
    :param aggregation_secondary_key: Configures secondary key aggregates using the set column. Only valid when using aggregations.
    :param online: Whether the feature view should be materialized to the online feature store. (Default: False)
    :param offline: Whether the feature view should be materialized to the offline feature store. (Default: False)
    :param ttl: The TTL (or "look back window") for features defined by this feature view. This parameter determines how long features will live in the online store and how far to  "look back" relative to a training example's timestamp when generating offline training sets. Shorter TTLs improve performance and reduce costs.
    :param feature_start_time: When materialization for this feature view should start from. (Required if offline=true)
    :param batch_trigger: Defines the mechanism for initiating batch materialization jobs.
        One of ``BatchTriggerType.SCHEDULED`` or ``BatchTriggerType.MANUAL``.
        The default value is ``BatchTriggerType.SCHEDULED``, where Tecton will run materialization jobs based on the
        schedule defined by the ``batch_schedule`` parameter. If set to ``BatchTriggerType.MANUAL``, then batch
        materialization jobs must be explicitly initiated by the user through either the Tecton SDK or Airflow operator.
    :param batch_schedule: The interval at which batch materialization should be scheduled.
    :param online_serving_index: (Advanced) Defines the set of join keys that will be indexed and queryable during online serving.
    :param batch_compute: Batch materialization cluster configuration.
    :param stream_compute: Streaming materialization cluster configuration.
    :param offline_store: Configuration for how data is written to the offline feature store.
    :param online_store: Configuration for how data is written to the online feature store.
    :param monitor_freshness: If true, enables monitoring when feature data is materialized to the online feature store.
    :param data_quality_enabled: If false, disables data quality metric computation and data quality dashboard.
    :param skip_default_expectations: If true, skips validating default expectations on the feature data.
    :param expected_feature_freshness: Threshold used to determine if recently materialized feature data is stale. Data is stale if ``now - most_recent_feature_value_timestamp > expected_feature_freshness``. For feature views using Tecton aggregations, data is stale if ``now - round_up_to_aggregation_interval(most_recent_feature_value_timestamp) > expected_feature_freshness``. Where ``round_up_to_aggregation_interval()`` rounds up the feature timestamp to the end of the ``aggregation_interval``. Value must be at least 2 times ``aggregation_interval``. If not specified, a value determined by the Tecton backend is used.
    :param alert_email: Email that alerts for this FeatureView will be sent to.
    :param description: A human readable description.
    :param owner: Owner name (typically the email of the primary maintainer).
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
        destructive update) during tecton plan/apply. To remove or update this object, ``prevent_destroy`` must be set
        to False via the same tecton apply or a separate tecton apply. ``prevent_destroy`` can be used to prevent accidental changes
        such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
        triggers expensive rematerialization jobs. ``prevent_destroy`` also blocks changes to dependent Tecton objects
        that would trigger a recreate of the tagged object, e.g. if ``prevent_destroy`` is set on a Feature Service,
        that will also prevent deletions or re-creates of Feature Views used in that service. ``prevent_destroy`` is
        only enforced in live (i.e. non-dev) workspaces.
    :param timestamp_field: The column name that refers to the timestamp for records that are produced by the
        feature view. This parameter is optional if exactly one column is a Timestamp type.
    :param name: Unique, human friendly name that identifies the FeatureView. Defaults to the function name.
    :param max_batch_aggregation_interval: Deprecated. Use max_backfill_interval instead, which has the exact same usage.
    :param max_backfill_interval: (Advanced) The time interval for which each backfill job will run to materialize
        feature data. This affects the number of backfill jobs that will run, which is
        (`<feature registration time>` - `feature_start_time`) / `max_backfill_interval`.
        Configuring the `max_backfill_interval` parameter appropriately will help to optimize large backfill jobs.
        If this parameter is not specified, then 10 backfill jobs will run (the default).
    :param output_stream: Configuration for a stream to write feature outputs to, specified as a :class:`tecton.framework.conifgs.KinesisOutputStream` or :class:`tecton.framework.configs.KafkaOutputStream`.
    :param schema: The output schema of the Feature View transformation. If provided and ``run_transformation_validations=True``,
        then Tecton will validate that the Feature View matches the expected schema.
    :param manual_trigger_backfill_end_time: If set, Tecton will schedule backfill materialization jobs for this feature view up to this time. Materialization jobs after this point must be triggered manually. (This param is only valid to set if BatchTriggerType is MANUAL.)
    :param options: Additional options to configure the Feature View. Used for advanced use cases and beta features.
    :param run_transformation_validation: If `True`, Tecton will execute the Feature View transformations during tecton plan/apply
        validation. If `False`, then Tecton will not execute the transformations during validation and ``schema`` must be
        set. Skipping query validation can be useful to speed up tecton plan/apply or for Feature Views that have issues
        with Tecton's validation (e.g. some pip dependencies). Default is True for Spark and Snowflake Feature Views and
        False for Python and Pandas Feature Views or Feature Views with Push Sources.
    :param tecton_materialization_runtime: Version of `tecton` package used by your job cluster.
    :param cache_config: Cache config for the Feature View. Including this option enables the feature server to use the cache
        when retrieving features for this feature view. Will only be respected if the feature service containing this feature
        view has `enable_online_caching` set to `True`.
    :param stream_compaction_enabled: Deprecated: Please use `stream_tiling_enabled` instead which has the exact same usage.
    :param batch_compaction_enabled: Deprecated: Please use `compaction_enabled` instead which has the exact same usage.
    :param stream_tiling_enabled: (Private preview) If `False`, Tecton transforms and writes all events from the stream to the online store (same as stream_processing_mode=``StreamProcessingMode.CONTINUOUS``) . If `True`, Tecton will store the partial aggregations of the events in the online store. Defaults to ``False``.
    :param compaction_enabled: (Private preview) If `True`, Tecton will run a compaction job after each batch
        materialization job to write to the online store. This requires the use of Dynamo and uses the ImportTable API.
        Becuase each batch job overwrites the online store, a larger compute cluster may be required. This is required to be True if `stream_compaction_enabled` is True. Defaults to ``False``.
    :param environment: The custom environment in which materialization jobs will be run. Defaults to `None`, which means
        jobs will execute in the default Tecton environment.

    :return: An object of type :class:`tecton.StreamFeatureView`.

    Example `StreamFeatureView` declaration:

    .. code-block:: python

        from datetime import datetime, timedelta
        from entities import user
        from transactions_stream import transactions_stream
        from tecton import Aggregation, FilteredSource, stream_feature_view

        @stream_feature_view(
            source=FilteredSource(transactions_stream),
            entities=[user],
            mode="spark_sql",
            ttl=timedelta(days=30),
            online=True,
            offline=True,
            batch_schedule=timedelta(days=1),
            feature_start_time=datetime(2020, 10, 10),
            tags={"release": "production"},
            owner="kevin@tecton.ai",
            description="Features about the users most recent transaction in the past 60 days. Updated continuously.",
        )
        def user_last_transaction_features(transactions_stream):
            return f'''
                SELECT
                    USER_ID,
                    TIMESTAMP,
                    AMOUNT as LAST_TRANSACTION_AMOUNT,
                    CATEGORY as LAST_TRANSACTION_CATEGORY
                FROM
                    {transactions_stream}
                '''

    Example `StreamFeatureView` declaration using aggregates:

    .. code-block:: python

        from datetime import datetime, timedelta
        from entities import user
        from transactions_stream import transactions_stream
        from tecton import Aggregation, FilteredSource, stream_feature_view

        @stream_feature_view(
            source=FilteredSource(transactions_stream),
            entities=[user],
            mode="spark_sql",
            aggregation_interval=timedelta(minutes=10),
            aggregations=[
                Aggregation(column="AMOUNT", function="mean", time_window=timedelta(hours=1)),
                Aggregation(column="AMOUNT", function="mean", time_window=timedelta(hours=24)),
                Aggregation(column="AMOUNT", function="mean", time_window=timedelta(hours=72)),
                Aggregation(column="AMOUNT", function="sum", time_window=timedelta(hours=1)),
                Aggregation(column="AMOUNT", function="sum", time_window=timedelta(hours=24)),
                Aggregation(column="AMOUNT", function="sum", time_window=timedelta(hours=72)),
            ],
            online=True,
            feature_start_time=datetime(2020, 10, 10),
            tags={"release": "production"},
            owner="kevin@tecton.ai",
            description="Transaction amount statistics and total over a series of time windows, updated every ten minutes.",
        )
        def user_recent_transaction_aggregate_features(transactions_stream):
            return f'''
                SELECT
                    USER_ID,
                    AMOUNT,
                    TIMESTAMP
                FROM
                    {transactions_stream}
                '''
    """

    # TODO(deprecate_after=0.8): This warning can be completely removed in 0.9, so it can be deleted once the 0.8 branch is cut.
    if max_batch_aggregation_interval is not None:
        msg = "FeatureView.max_batch_aggregation_interval is deprecated and is no longer supported in 0.8. Please use max_backfill_interval instead. max_backfill_interval has the same semantics and is just a new name."
        raise ValueError(msg)

    if batch_compaction_enabled is not None and compaction_enabled is not None:
        msg = "FeatureView.batch_compaction_enabled is deprecated. Please use compaction_enabled instead. compaction_enabled has the same semantics and is just a new name."
        raise TectonValidationError(msg)

    compaction_enabled = compaction_enabled or batch_compaction_enabled or False

    if stream_compaction_enabled is not None and stream_tiling_enabled is not None:
        msg = "FeatureView.stream_compaction_enabled is deprecated. Please use stream_tiling_enabled instead. stream_tiling_enabled has the same semantics and is just a new name."
        raise TectonValidationError(msg)

    stream_tiling_enabled = stream_tiling_enabled or stream_compaction_enabled or False

    def decorator(feature_view_function):
        return StreamFeatureView(
            name=name or feature_view_function.__name__,
            description=description,
            owner=owner,
            tags=tags,
            prevent_destroy=prevent_destroy,
            feature_view_function=feature_view_function,
            source=source,
            entities=entities,
            mode=mode,
            aggregation_interval=aggregation_interval,
            aggregations=aggregations,
            aggregation_secondary_key=aggregation_secondary_key,
            stream_processing_mode=stream_processing_mode,
            online=online,
            offline=offline,
            ttl=ttl,
            feature_start_time=feature_start_time,
            lifetime_start_time=lifetime_start_time,
            manual_trigger_backfill_end_time=manual_trigger_backfill_end_time,
            batch_trigger=batch_trigger,
            batch_schedule=batch_schedule,
            online_serving_index=online_serving_index,
            batch_compute=batch_compute,
            stream_compute=stream_compute,
            offline_store=offline_store,
            online_store=online_store,
            monitor_freshness=monitor_freshness,
            data_quality_enabled=data_quality_enabled,
            skip_default_expectations=skip_default_expectations,
            expected_feature_freshness=expected_feature_freshness,
            alert_email=alert_email,
            timestamp_field=timestamp_field,
            max_backfill_interval=max_backfill_interval,
            output_stream=output_stream,
            schema=schema,
            options=options,
            run_transformation_validation=run_transformation_validation,
            tecton_materialization_runtime=tecton_materialization_runtime,
            cache_config=cache_config,
            compaction_enabled=compaction_enabled,
            stream_tiling_enabled=stream_tiling_enabled,
            environment=environment,
        )

    return decorator


@attrs.define(eq=False)
class FeatureTable(FeatureView):
    """A Tecton Feature Table.

    Feature Tables are used to batch push features into Tecton from external feature computation systems.

    An example declaration of a FeatureTable:

    .. code-block:: python

        from tecton import Entity, FeatureTable
        from tecton.types import Field, String, Timestamp, Int64
        import datetime

        # Declare your user Entity instance here or import it if defined elsewhere in
        # your Tecton repo.

        user = ...

        schema = [
            Field('user_id', String),
            Field('timestamp', Timestamp),
            Field('user_login_count_7d', Int64),
            Field('user_login_count_30d', Int64)
        ]

        user_login_counts = FeatureTable(
            name='user_login_counts',
            entities=[user],
            schema=schema,
            online=True,
            offline=True,
            ttl=datetime.timedelta(days=30)
        )

    Attributes:
        entities: The Entities for this Feature View.
        info: A dataclass containing basic info about this Tecton Object.
    """

    entities: Tuple[framework_entity.Entity, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        prevent_destroy: bool = False,
        entities: List[framework_entity.Entity],
        schema: List[types.Field],
        ttl: Optional[datetime.timedelta] = None,
        online: bool = False,
        offline: bool = False,
        offline_store: Optional[Union[configs.OfflineStoreConfig, configs.DeltaConfig]] = None,
        online_store: Optional[configs.OnlineStoreTypes] = None,
        batch_compute: Optional[configs.ComputeConfigTypes] = None,
        online_serving_index: Optional[List[str]] = None,
        alert_email: Optional[str] = None,
        tecton_materialization_runtime: Optional[str] = None,
        options: Optional[Dict[str, str]] = None,
    ):
        """Instantiate a new FeatureTable.

        :param name: Unique, human friendly name that identifies the FeatureTable.
        :param description: A human readable description.
        :param owner: Owner name (typically the email of the primary maintainer).
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
            destructive update) during tecton plan/apply. To remove or update this object, ``prevent_destroy`` must
            be set to False via the same tecton apply or a separate tecton apply. ``prevent_destroy`` can be used to prevent accidental changes
            such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
            triggers expensive rematerialization jobs. ``prevent_destroy`` also blocks changes to dependent Tecton objects
            that would trigger a recreate of the tagged object, e.g. if ``prevent_destroy`` is set on a Feature Service,
            that will also prevent deletions or re-creates of Feature Views used in that service. ``prevent_destroy`` is
            only enforced in live (i.e. non-dev) workspaces.
        :param entities: A list of Entity objects, used to organize features.
        :param schema: A schema for the FeatureTable. Supported types are: Int64, Float64, String, Bool and Array with Int64, Float32, Float64 and String typed elements. Additionally you must have exactly one Timestamp typed column for the feature timestamp.
        :param ttl: The TTL (or "look back window") for features defined by this feature table. This parameter determines how long features will live in the online store and how far to  "look back" relative to a training example's timestamp when generating offline training sets. Shorter TTLs improve performance and reduce costs.
        :param online: Enable writing to online feature store. (Default: False)
        :param offline: Enable writing to offline feature store. (Default: False)
        :param offline_store: Configuration for how data is written to the offline feature store.
        :param online_store: Configuration for how data is written to the online feature store.
        :param batch_compute: Configuration for batch materialization clusters. Should be one of:
            [:class:`EMRClusterConfig`, :class:`DatabricksClusterConfig`, :class:`EMRJsonClusterConfig`, :class:`DatabricksJsonClusterConfig`, :class:`DataprocJsonClusterConfig`]
        :param online_serving_index: (Advanced) Defines the set of join keys that will be indexed and queryable during online serving.
            Defaults to the complete set of join keys. Up to one join key may be omitted. If one key is omitted, online requests to a Feature Service will
            return all feature vectors that match the specified join keys.
        :param alert_email: Email that alerts for this FeatureTable will be sent to.
        :param tecton_materialization_runtime: Version of `tecton` package used by your job cluster.
        :param options: Additional options to configure the Feature Table. Used for advanced use cases and beta features.
        """
        from tecton.cli import repo_utils as cli_common

        if online_store is None:
            online_store = repo_config.get_feature_table_defaults().online_store

        if offline_store is None:
            offline_store = repo_config.get_feature_table_defaults().offline_store_config
        elif isinstance(offline_store, configs.DeltaConfig):
            offline_store = configs.OfflineStoreConfig(staging_table_format=offline_store)

        if batch_compute is None:
            batch_compute = repo_config.get_feature_table_defaults().batch_compute

        if tecton_materialization_runtime is None:
            tecton_materialization_runtime = repo_config.get_feature_table_defaults().tecton_materialization_runtime

        if isinstance(schema, list):
            wrapper = type_utils.to_spark_schema_wrapper(schema)
        else:
            wrapper = spark_schema_wrapper.SparkSchemaWrapper(schema)

        feature_table_args = feature_view__args_pb2.FeatureTableArgs(
            tecton_materialization_runtime=tecton_materialization_runtime,
            schema=wrapper.to_proto(),
            serving_ttl=time_utils.timedelta_to_proto(ttl),
            batch_compute=batch_compute._to_cluster_proto(),
            online_store=online_store._to_proto() if online_store else None,
            monitoring=configs.MonitoringConfig(monitor_freshness=False, alert_email=alert_email)._to_proto(),
            offline_store=offline_store._to_proto(),
        )

        # If unspecified, online_serving_index defaults to the join_keys of the Feature Table.
        join_keys = []
        for entity in entities:
            join_keys.extend(entity.join_keys)

        args = feature_view__args_pb2.FeatureViewArgs(
            feature_table_args=feature_table_args,
            feature_view_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            prevent_destroy=prevent_destroy,
            feature_view_type=feature_view__args_pb2.FeatureViewType.FEATURE_VIEW_TYPE_FEATURE_TABLE,
            version=feature_definition_wrapper.FrameworkVersion.FWV5.value,
            entities=[
                feature_view__args_pb2.EntityKeyOverride(entity_id=entity.info._id_proto, join_keys=entity.join_keys)
                for entity in entities
            ],
            online_enabled=online,
            offline_enabled=offline,
            online_serving_index=online_serving_index,
            batch_compute_mode=BatchComputeMode(
                infer_batch_compute_mode(
                    pipeline_root=None, batch_compute_config=batch_compute, stream_compute_config=None
                )
            ).value,
            options=options,
        )

        info = base_tecton_object.TectonObjectInfo.from_args_proto(args.info, args.feature_view_id)
        source_info = cli_common.construct_fco_source_info(args.feature_view_id)
        self.__attrs_init__(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            entities=tuple(entities),
            args_supplement=None,
        )
        base_tecton_object._register_local_object(self)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.FeatureTableSpec, fco_container_: fco_container.FcoContainer) -> "FeatureTable":
        """Create a FeatureTable from directly from a spec. Specs are assumed valid and will not be re-validated."""
        feature_definition = feature_definition_wrapper.FeatureDefinitionWrapper(spec, fco_container_)
        info = base_tecton_object.TectonObjectInfo.from_spec(spec)

        entities = []
        for entity_spec in feature_definition.entities:
            entities.append(framework_entity.Entity._from_spec(entity_spec))

        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(
            info=info,
            feature_definition=feature_definition,
            args=None,
            source_info=None,
            entities=tuple(entities),
            args_supplement=None,
        )

        return obj

    def _get_dependent_objects(self, include_indirect_dependencies: bool) -> List[base_tecton_object.BaseTectonObject]:
        return list(self.entities)

    def _derive_schemas(self) -> _Schemas:
        view_schema = spark_api.spark_schema_to_tecton_schema(self._args.feature_table_args.schema)

        # For feature tables, materialization and view schema are the same.
        return _Schemas(
            view_schema=view_schema,
            materialization_schema=view_schema,
            online_batch_table_format=None,
        )

    @sdk_decorators.assert_valid
    def _check_can_query_from_source(self, from_source: Optional[bool]) -> QuerySources:
        fd = self._feature_definition

        if self._is_local_object:
            raise errors.FD_GET_MATERIALIZED_FEATURES_FROM_LOCAL_OBJECT(self.name, "Feature Table")

        if not fd.materialization_enabled:
            raise errors.FEATURE_TABLE_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE(
                self.info.name, self.info.workspace
            )

        if from_source:
            raise errors.FROM_SOURCE_WITH_FT

        if not fd.writes_to_offline_store:
            raise errors.FEATURE_TABLE_GET_MATERIALIZED_FEATURES_OFFLINE_FALSE(self.info.name)

        return QuerySources(feature_table_count=1)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object(error_message=errors.INVALID_USAGE_FOR_LOCAL_FEATURE_TABLE_OBJECT)
    def get_features_for_events(
        self,
        spine: Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame],
        timestamp_key: Optional[str] = None,
        save: bool = False,
        save_as: Optional[str] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        """Returns a Tecton :class:`TectonDataFrame` of historical values for this feature table.

        If no arguments are passed in, all feature values for this feature table will be returned in a TectonDataFrame.
        Note:
        The `timestamp_key` parameter is only applicable when a spine is passed in.
        Parameters `start_time`, `end_time`, and `entities` are only applicable when a spine is not passed in.

        :param spine: The spine to join against, as a dataframe.
            If present, the returned DataFrame will contain rollups for all (join key, temporal key)
            combinations that are required to compute a full frame from the spine.
            To distinguish between spine columns and feature columns, feature columns are labeled as
            `feature_view_name.feature_name` in the returned DataFrame.
            If spine is not specified, it'll return a DataFrame of  feature values in the specified time range.
        :type spine: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param timestamp_key: Name of the time column in spine.
            This method will fetch the latest features computed before the specified timestamps in this column.
            If unspecified, will default to the time column of the spine if there is only one present.
        :type timestamp_key: str
        :param entities: A DataFrame that is used to filter down feature values.
            If specified, this DataFrame should only contain join key columns.
        :type entities: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param start_time: The interval start time from when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type start_time: Union[pendulum.DateTime, datetime.datetime]
        :param end_time:  The interval end time until when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type end_time: Union[pendulum.DateTime, datetime.datetime]
        :param save: Whether to persist the DataFrame as a Dataset object. Default is False.
        :type save: bool
        :param save_as: name to save the DataFrame as.
                If unspecified and save=True, a name will be generated.
        :type save_as: str
        :param compute_mode: Compute mode to use to produce the data frame.
        :type compute_mode: Optional[Union[ComputeMode, str]]


        Examples:
            A FeatureTable :py:mod:`ft` with join key :py:mod:`user_id`.

            1) :py:mod:`ft.get_historical_features(spine)` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date': [datetime(...), datetime(...), datetime(...)]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps in the spine.

            2) :py:mod:`ft.get_historical_features(spine, save_as='my_dataset)` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date': [datetime(...), datetime(...), datetime(...)]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps in the spine. Save the DataFrame as dataset with the name :py:mod`my_dataset`.

            3) :py:mod:`ft.get_historical_features(spine, timestamp_key='date_1')` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date_1': [datetime(...), datetime(...), datetime(...)], 'date_2': [datetime(...), datetime(...), datetime(...)]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps in the 'date_1' column in the spine.

            4) :py:mod:`ft.get_historical_features(start_time=datetime(...), end_time=datetime(...))`
            Fetch all historical features from the offline store in the time range specified by `start_time` and `end_time`.

        :return: A TectonDataFrame with features values.
        """

        sources = self._check_can_query_from_source(from_source=False)
        sources.display()

        compute_mode = offline_retrieval_compute_mode(compute_mode)

        if compute_mode == ComputeMode.ATHENA or compute_mode == ComputeMode.SNOWFLAKE:
            raise errors.GET_FEATURES_FOR_EVENTS_UNSUPPORTED

        return querytree_api.get_features_for_events(
            dialect=compute_mode.default_dialect(),
            compute_mode=compute_mode,
            feature_definition=self._feature_definition,
            spine=spine,
            timestamp_key=timestamp_key,
            from_source=False,
            save=save,
            save_as=save_as,
            mock_data_sources={},
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object(error_message=errors.INVALID_USAGE_FOR_LOCAL_FEATURE_TABLE_OBJECT)
    def get_features_in_range(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        max_lookback: Optional[datetime.timedelta] = None,
        entities: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        """Returns a Tecton :class:`TectonDataFrame` of historical values for this feature table.

        If no arguments are passed in, all feature values for this feature table will be returned in a TectonDataFrame.
        Note:

        :param start_time: The interval start time from when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type start_time: Union[pendulum.DateTime, datetime.datetime]
        :param end_time:  The interval end time until when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type end_time: Union[pendulum.DateTime, datetime.datetime]
        :param max_lookback: A performance optimization that configures how far back before start_time to compute features for.
        :type max_lookback: datetime.timedelta
        :param entities: A DataFrame that is used to filter down feature values.
            If specified, this DataFrame should only contain join key columns.
        :type entities: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param save: Whether to persist the DataFrame as a Dataset object. Default is False.
        :type save: bool
        :param save_as: name to save the DataFrame as.
                If unspecified and save=True, a name will be generated.
        :type save_as: str
        :param compute_mode: Compute mode to use to produce the data frame.
        :type compute_mode: Optional[Union[ComputeMode, str]]


        Examples:
            A FeatureTable :py:mod:`ft` with join key :py:mod:`user_id`.

            :py:mod:`ft.get_features_in_range(start_time=datetime(...), end_time=datetime(...))`
            Fetches all historical features from the offline store in the time range specified by `start_time` and `end_time`.

        :return: A TectonDataFrame with features values.
        """

        sources = self._check_can_query_from_source(from_source=False)
        sources.display()

        compute_mode = offline_retrieval_compute_mode(compute_mode)

        if compute_mode != ComputeMode.SPARK and compute_mode != ComputeMode.RIFT:
            raise errors.GET_FEATURES_IN_RANGE_UNSUPPORTED

        if start_time >= end_time:
            raise core_errors.START_TIME_NOT_BEFORE_END_TIME(start_time, end_time)

        return querytree_api.get_features_in_range(
            dialect=compute_mode.default_dialect(),
            compute_mode=compute_mode,
            feature_definition=self._feature_definition,
            start_time=start_time,
            end_time=end_time,
            max_lookback=max_lookback,
            entities=entities,
            from_source=False,
            mock_data_sources={},
        )

    # if spine is provided, then timestamp_key is optional, but start_time, end_time, and entities cannot be used
    @overload
    def get_historical_features(
        self,
        spine: Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame, str],
        timestamp_key: Optional[str] = None,
        from_source: Optional[bool] = None,
        save: bool = False,
        save_as: Optional[str] = None,
        mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame: ...

    # if spine not provided, then timestamp_key should also not be provided.
    # start_time, end_time, and entities can be used instead.
    @overload
    def get_historical_features(
        self,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        entities: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        from_source: Optional[bool] = None,
        save: bool = False,
        save_as: Optional[str] = None,
        mock_inputs: Optional[Dict[str, Union[pandas.DataFrame, pyspark_dataframe.DataFrame]]] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame: ...

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object(error_message=errors.INVALID_USAGE_FOR_LOCAL_FEATURE_TABLE_OBJECT)
    def get_historical_features(
        self,
        spine: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        timestamp_key: Optional[str] = None,
        entities: Optional[Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame]] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        save: bool = False,
        save_as: Optional[str] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        """Returns a Tecton :class:`TectonDataFrame` of historical values for this feature table.

        If no arguments are passed in, all feature values for this feature table will be returned in a TectonDataFrame.
        Note:
        The `timestamp_key` parameter is only applicable when a spine is passed in.
        Parameters `start_time`, `end_time`, and `entities` are only applicable when a spine is not passed in.

        :param spine: The spine to join against, as a dataframe.
            If present, the returned DataFrame will contain rollups for all (join key, temporal key)
            combinations that are required to compute a full frame from the spine.
            To distinguish between spine columns and feature columns, feature columns are labeled as
            `feature_view_name.feature_name` in the returned DataFrame.
            If spine is not specified, it'll return a DataFrame of  feature values in the specified time range.
        :type spine: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param timestamp_key: Name of the time column in spine.
            This method will fetch the latest features computed before the specified timestamps in this column.
            If unspecified, will default to the time column of the spine if there is only one present.
        :type timestamp_key: str
        :param entities: A DataFrame that is used to filter down feature values.
            If specified, this DataFrame should only contain join key columns.
        :type entities: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param start_time: The interval start time from when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type start_time: Union[pendulum.DateTime, datetime.datetime]
        :param end_time:  The interval end time until when we want to retrieve features.
            If no timezone is specified, will default to using UTC.
        :type end_time: Union[pendulum.DateTime, datetime.datetime]
        :param save: Whether to persist the DataFrame as a Dataset object. Default is False.
        :type save: bool
        :param save_as: name to save the DataFrame as.
                If unspecified and save=True, a name will be generated.
        :type save_as: str
        :param compute_mode: Compute mode to use to produce the data frame.
        :type compute_mode: Optional[Union[ComputeMode, str]]


        Examples:
            A FeatureTable :py:mod:`ft` with join key :py:mod:`user_id`.

            1) :py:mod:`ft.get_historical_features(spine)` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date': [datetime(...), datetime(...), datetime(...)]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps in the spine.

            2) :py:mod:`ft.get_historical_features(spine, save_as='my_dataset)` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date': [datetime(...), datetime(...), datetime(...)]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps in the spine. Save the DataFrame as dataset with the name :py:mod`my_dataset`.

            3) :py:mod:`ft.get_historical_features(spine, timestamp_key='date_1')` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date_1': [datetime(...), datetime(...), datetime(...)], 'date_2': [datetime(...), datetime(...), datetime(...)]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps in the 'date_1' column in the spine.

            4) :py:mod:`ft.get_historical_features(start_time=datetime(...), end_time=datetime(...))`
            Fetch all historical features from the offline store in the time range specified by `start_time` and `end_time`.

        :return: A TectonDataFrame with features values.
        """

        sources = self._check_can_query_from_source(from_source=False)
        sources.display()

        if spine is None and timestamp_key is not None:
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(["timestamp_key"], "the spine parameter is not provided")

        if spine is not None and (start_time is not None or end_time is not None or entities is not None):
            raise errors.GET_HISTORICAL_FEATURES_WRONG_PARAMS(
                ["start_time", "end_time", "entities"], "the spine parameter is provided"
            )

        if start_time is not None and end_time is not None and start_time >= end_time:
            raise core_errors.START_TIME_NOT_BEFORE_END_TIME(start_time, end_time)

        compute_mode = offline_retrieval_compute_mode(compute_mode)

        if compute_mode == ComputeMode.ATHENA and conf.get_bool("USE_DEPRECATED_ATHENA_RETRIEVAL"):
            return athena_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                start_time=start_time,
                end_time=end_time,
                entities=entities,
                from_source=False,
                save=save,
                save_as=save_as,
                feature_set_config=self._construct_feature_set_config(),
            )

        return querytree_api.get_historical_features_for_feature_definition(
            dialect=compute_mode.default_dialect(),
            compute_mode=compute_mode,
            feature_definition=self._feature_definition,
            spine=spine,
            timestamp_key=timestamp_key,
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            from_source=False,
            save=save,
            save_as=save_as,
            mock_data_sources={},
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def get_online_features(
        self,
        join_keys: Mapping[str, Union[int, np.int_, str, bytes]],
        include_join_keys_in_response: bool = False,
    ) -> FeatureVector:
        """Returns a single Tecton FeatureVector from the Online Store.

        :param join_keys: Join keys of the enclosed FeatureTable.
        :param include_join_keys_in_response: Whether to include join keys as part of the response FeatureVector.

        Examples:
            A FeatureTable :py:mod:`ft` with join key :py:mod:`user_id`.

            1) :py:mod:`ft.get_online_features(join_keys={'user_id': 1})`
            Fetch the latest features from the online store for user 1.

            2) :py:mod:`ft.get_online_features(join_keys={'user_id': 1}, include_join_keys_in_respone=True)`
            Fetch the latest features from the online store for user 1 and include the join key information (user_id=1) in the returned FeatureVector.

        :return: A FeatureVector of the results.
        """
        if not self._feature_definition.materialization_enabled:
            raise errors.FEATURE_TABLE_GET_ONLINE_FEATURES_FROM_DEVELOPMENT_WORKSPACE(
                self.info.name, self.info.workspace
            )

        if not self._feature_definition.writes_to_online_store:
            msg = "get_online_features"
            raise errors.UNSUPPORTED_OPERATION(msg, "online=True was not set for this Feature Table.")

        return query_helper._QueryHelper(self.info.workspace, feature_view_name=self.info.name).get_feature_vector(
            join_keys,
            include_join_keys_in_response,
            request_context_map={},
            request_context_schema=request_context.RequestContext({}),
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def ingest(self, df: Union[pyspark_dataframe.DataFrame, pandas.DataFrame]):
        """Ingests a Dataframe into the FeatureTable.

        This method kicks off a materialization job to write the data into the offline and online store, depending on
        the Feature Table configuration.

        :param df: The Dataframe to be ingested. Has to conform to the FeatureTable schema.
        """

        if not self._feature_definition.materialization_enabled:
            msg = "ingest"
            raise errors.UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE(msg)

        get_upload_info_request = metadata_service_pb2.GetNewIngestDataframeInfoRequest(
            feature_definition_id=self._spec.id_proto
        )
        upload_info_response = metadata_service.instance().GetNewIngestDataframeInfo(get_upload_info_request)

        df_path = upload_info_response.df_path
        upload_url = upload_info_response.signed_url_for_df_upload
        spark_api.write_dataframe_to_path_or_url(
            df, df_path, upload_url, self._feature_definition.view_schema, enable_schema_validation=True
        )

        ingest_request = metadata_service_pb2.IngestDataframeRequest(
            workspace=self.info.workspace, feature_definition_id=self._spec.id_proto, df_path=df_path
        )
        response = metadata_service.instance().IngestDataframe(ingest_request)

    @sdk_decorators.sdk_public_method(requires_validation=True)
    def get_timestamp_field(self) -> str:
        """Returns the name of the timestamp field of this Feature Table."""
        return self._feature_definition.fv_spec.timestamp_field

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def delete_keys(
        self,
        keys: Union[pyspark_dataframe.DataFrame, pandas.DataFrame],
        online: bool = True,
        offline: bool = True,
    ) -> List[str]:
        """Deletes any materialized data that matches the specified join keys from the FeatureTable.

        This method kicks off a job to delete the data in the offline and online stores.
        If a FeatureTable has multiple entities, the full set of join keys must be specified.
        Only supports Dynamo online store.
        Maximum 500,000 keys can be deleted per request.

        :param keys: The Dataframe to be deleted. Must conform to the FeatureTable join keys.
        :param online: (Optional, default=True) Whether or not to delete from the online store.
        :param offline: (Optional, default=True) Whether or not to delete from the offline store.
        :return: List of job ids for jobs created for entity deletion.
        """
        is_live_workspace = internal_utils.is_live_workspace(self.info.workspace)
        if not is_live_workspace:
            msg = "delete_keys"
            raise errors.UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE(msg)

        return delete_keys_api.delete_keys(online, offline, keys, self._feature_definition)

    @sdk_decorators.documented_by(MaterializedFeatureView.materialization_status)
    @sdk_decorators.assert_remote_object
    def materialization_status(
        self, verbose=False, limit=1000, sort_columns=None, errors_only=False
    ) -> display.Displayable:
        return materialization_api.get_materialization_status_for_display(
            self._spec.id_proto, self.workspace, verbose, limit, sort_columns, errors_only
        )


@attrs.define(eq=False)
class OnDemandFeatureView(FeatureView):
    """A Tecton On-Demand Feature View.

    The OnDemandFeatureView should not be instantiated directly and the :py:func:`tecton.on_demand_feature_view`
    decorator is recommended instead.

    Attributes:
        sources: The Request Sources and dependent Feature Views for this On Demand Feature View.
        tranformations: The Transformations for this Feature View.
    """

    sources: Tuple[Union["FeatureReference", configs.RequestSource], ...] = attrs.field(on_setattr=attrs.setters.frozen)
    transformations: Tuple[framework_transformation.Transformation, ...] = attrs.field(
        repr=utils.short_tecton_objects_repr, on_setattr=attrs.setters.frozen
    )

    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        prevent_destroy: bool = False,
        mode: str,
        sources: List[Union[configs.RequestSource, FeatureView, "FeatureReference"]],
        schema: List[types.Field],
        feature_view_function: Callable,
        environments: Optional[List[str]] = None,
    ):
        from tecton.cli import repo_utils as cli_common

        _validate_fv_input_count(sources, feature_view_function)

        if mode == PIPELINE_MODE:
            pipeline_function = feature_view_function
        else:
            # Separate out the Transformation and manually construct a simple pipeline function.
            # We infer owner/family/tags but not a description.
            inferred_transform = framework_transformation.transformation(mode, name, description, owner, tags=tags)(
                feature_view_function
            )

            def pipeline_function(**kwargs):
                return inferred_transform(**kwargs)

        pipeline_root = _build_pipeline_for_odfv(name, feature_view_function, pipeline_function, sources)

        spark_schema_wrapper = type_utils.to_spark_schema_wrapper(schema)

        on_demand_args = feature_view__args_pb2.OnDemandArgs(
            schema=spark_schema_wrapper.to_proto(),
            environments=environments if environments else [],
        )

        args = feature_view__args_pb2.FeatureViewArgs(
            feature_view_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            prevent_destroy=prevent_destroy,
            version=feature_definition_wrapper.FrameworkVersion.FWV5.value,
            pipeline=pipeline_pb2.Pipeline(root=pipeline_root.node_proto),
            feature_view_type=feature_view__args_pb2.FeatureViewType.FEATURE_VIEW_TYPE_ON_DEMAND,
            on_demand_args=on_demand_args,
        )

        info = base_tecton_object.TectonObjectInfo.from_args_proto(args.info, args.feature_view_id)
        source_info = cli_common.construct_fco_source_info(args.feature_view_id)

        references_and_request_sources = []
        for source in sources:
            if isinstance(source, FeatureView):
                references_and_request_sources.append(FeatureReference(feature_definition=source))
            else:
                references_and_request_sources.append(source)

        self.__attrs_init__(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            sources=tuple(references_and_request_sources),
            transformations=tuple(pipeline_root.transformations),
            args_supplement=None,
        )

        base_tecton_object._register_local_object(self)

    @classmethod
    @typechecked
    def _from_spec(
        cls, spec: specs.OnDemandFeatureViewSpec, fco_container_: fco_container.FcoContainer
    ) -> "FeatureView":
        """Create a FeatureView from directly from a spec. Specs are assumed valid and will not be re-validated."""
        feature_definition = feature_definition_wrapper.FeatureDefinitionWrapper(spec, fco_container_)
        info = base_tecton_object.TectonObjectInfo.from_spec(spec)

        transformations = []
        for transformation_spec in feature_definition.transformations:
            transformations.append(framework_transformation.Transformation._from_spec(transformation_spec))

        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(
            info=info,
            feature_definition=feature_definition,
            args=None,
            source_info=None,
            sources=_build_odfv_sources_from_spec(spec, fco_container_),
            transformations=tuple(transformations),
            args_supplement=None,
        )

        return obj

    def _get_dependent_objects(self, include_indirect_dependencies: bool) -> List[base_tecton_object.BaseTectonObject]:
        dependent_objects = list(self.transformations)
        for fv in self._get_dependent_feature_views():
            if include_indirect_dependencies:
                dependent_objects.extend([*fv._get_dependent_objects(include_indirect_dependencies=True), fv])
            else:
                dependent_objects.append(fv)

        # Dedupe by ID.
        return list({fco_obj.id: fco_obj for fco_obj in dependent_objects}.values())

    def _get_dependent_feature_views(self) -> List[FeatureView]:
        return [source.feature_definition for source in self.sources if isinstance(source, FeatureReference)]

    def _derive_schemas(self) -> _Schemas:
        view_schema = spark_api.spark_schema_to_tecton_schema(self._args.on_demand_args.schema)

        return _Schemas(
            view_schema=view_schema,
            materialization_schema=view_schema,
            online_batch_table_format=None,
        )

    @sdk_decorators.assert_valid
    def _check_can_query_from_source(self, from_source: Optional[bool]) -> QuerySources:
        all_sources = QuerySources(on_demand_count=1)
        for fv in self._get_dependent_feature_views():
            all_sources += fv._check_can_query_from_source(from_source)
        return all_sources

    @sdk_decorators.sdk_public_method(
        requires_validation=True,
        validation_error_message=errors.RUN_TRANSFORMATION_REQUIRES_VALIDATION,
        supports_skip_validation=True,
    )
    def run_transformation(self, input_data: Dict[str, Any]) -> Union[Dict[str, Any], TectonDataFrame]:
        """Run the OnDemandFeatureView using mock inputs.

        :param input_data: Required. Dict with the same expected keys as the OnDemandFeatureView's inputs parameters.
            For the "python" mode, each value must be a Dictionary representing a single row.
            For the "pandas" mode, each value must be a DataFrame with all of them containing the
            same number of rows and matching row ordering.

        Example:

        .. code-block:: python

            # Given a python on-demand feature view defined in your workspace:
            @on_demand_feature_view(
                sources=[transaction_request, user_transaction_amount_metrics],
                mode='python',
                schema=output_schema,
                description='The transaction amount is higher than the 1 day average.'
            )
            def transaction_amount_is_higher_than_average(request, user_metrics):
                return {'higher_than_average': request['amt'] > user_metrics['daily_average']}

        .. code-block:: python

            # Retrieve and run the feature view in a notebook using mock data:
            import tecton

            fv = tecton.get_workspace('prod').get_feature_view('transaction_amount_is_higher_than_average')

            input_data = {
                'request': {
                    'amt': 100
                },
                'user_metrics': {
                    'daily_average': 1000
                }
            }
            result = fv.run_transformation(input_data=input_data)

            print(result)
            # {'higher_than_average': False}

        :return: A `Dict` object for the "python" mode and a tecton DataFrame of the results for the "pandas" mode.
        """

        # unvalidated path for unit tests
        # TODO (Mary): These unvalidated forks should be cleaned up as part of the new validation strategy
        if self._feature_definition is None:
            return run_api.run_realtime_unvalidated(
                self.info.name, input_data, self.transformations, self._args.pipeline
            )
        # Snowflake compute uses the same code for run_realtime as Spark.
        return run_api.run_ondemand(
            self._feature_definition, self.info.name, input_data, self._feature_definition.transformation_mode
        )

    @sdk_decorators.sdk_public_method(
        requires_validation=True, validation_error_message=errors.RUN_REQUIRES_VALIDATION, supports_skip_validation=True
    )
    def run(
        self, **mock_inputs: Union[Dict[str, Any], pandas.DataFrame, pyspark_dataframe.DataFrame]
    ) -> Union[Dict[str, Any], TectonDataFrame]:
        """Run the OnDemandFeatureView using mock inputs.

        :param \*\*mock_inputs: Required. Keyword args with the same expected keys
            as the OnDemandFeatureView's inputs parameters.
            For the "python" mode, each input must be a Dictionary representing a single row.
            For the "pandas" mode, each input must be a DataFrame with all of them containing the
            same number of rows and matching row ordering.

        Example:

        .. code-block:: python

            # Given a python on-demand feature view defined in your workspace:
            @on_demand_feature_view(
                sources=[transaction_request, user_transaction_amount_metrics],
                mode='python',
                schema=output_schema,
                description='The transaction amount is higher than the 1 day average.'
            )
            def transaction_amount_is_higher_than_average(request, user_metrics):
                return {'higher_than_average': request['amt'] > user_metrics['daily_average']}

        .. code-block:: python

            # Retrieve and run the feature view in a notebook using mock data:
            import tecton

            fv = tecton.get_workspace('prod').get_feature_view('transaction_amount_is_higher_than_average')

            result = fv.run(request={'amt': 100}, user_metrics={'daily_average': 1000})

            print(result)
            # {'higher_than_average': False}

        :return: A `Dict` object for the "python" mode and a tecton DataFrame of the results for the "pandas" mode.
        """

        # unvalidated path for unit tests
        # TODO (Mary): These unvalidated forks should be cleaned up as part of the new validation strategy
        if self._feature_definition is None:
            return run_api.run_realtime_unvalidated(
                self.info.name, mock_inputs, self.transformations, self._args.pipeline
            )

        # Snowflake compute uses the same code for run_realtime as Spark.
        logger.warning(errors.RUN_DEPRECATED_TRANSFORMATION)
        return run_api.run_ondemand(
            self._feature_definition, self.info.name, mock_inputs, self._feature_definition.transformation_mode
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_local_object(error_message=errors.CANNOT_USE_LOCAL_RUN_ON_REMOTE_OBJECT)
    def test_run(
        self, **mock_inputs: Union[Dict[str, Any], pandas.DataFrame]
    ) -> Union[Dict[str, Any], pandas.DataFrame]:
        """Run the OnDemandFeatureView using mock sources.

        Unlike :py:func:`run`, :py:func:`test_run` is intended for unit testing. It will not make calls to your
        connected Tecton cluster to validate the OnDemandFeatureView.

        :param mock_inputs: Required. Keyword args with the same expected keys
            as the OnDemandFeatureView's inputs parameters.
            For the "python" mode, each input must be a Dictionary representing a single row.
            For the "pandas" mode, each input must be a DataFrame with all of them containing the
            same number of rows and matching row ordering.

        Example:
            .. code-block:: python

                @on_demand_feature_view(
                    sources=[transaction_request],
                    mode='python',
                    schema=output_schema,
                )
                def transaction_amount_is_high(transaction_request):
                    return {'transaction_amount_is_high': transaction_request['amount'] > 10000}

                # Test using `run` API.
                result = transaction_amount_is_high.test_run(transaction_request={'amount': 100})

        :return: A `Dict` object for the "python" mode and a `pandas.DataFrame` object for the "pandas" mode".
        """
        # TODO(adchia): Validate batch feature inputs here against BFV schema
        run_api.validate_ondemand_mock_inputs_match_expected_shape(mock_inputs, self._args.pipeline)

        transformation_specs = [transformation._create_unvalidated_spec() for transformation in self.transformations]

        return pipeline_helper.run_mock_odfv_pipeline(self._args.pipeline, transformation_specs, self.name, mock_inputs)

    @sdk_decorators.sdk_public_method(requires_validation=True)
    def get_features_for_events(
        self,
        events: Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame, str],
        timestamp_key: Optional[str] = None,
        from_source: Optional[bool] = None,
        save: bool = False,
        save_as: Optional[str] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        """Returns a Tecton :class:`TectonDataFrame` of historical values for this feature view.

        By default (i.e. ``from_source=None``), this method fetches feature values from the Offline Store for input
        Feature Views that have offline materialization enabled and otherwise computes input feature values on the fly
        from raw data.

        :param events: A dataframe of possible join keys, request data keys, and timestamps that specify which feature values to fetch.
            The returned data frame will contain rollups for all (join key, request data key)
            combinations that are required to compute a full frame from the `events` dataframe.
        :type events: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param timestamp_key: Name of the time column in spine.
            This method will fetch the latest features computed before the specified timestamps in this column.
            If unspecified and this feature view has feature view dependencies, `timestamp_key` will default to the time column of the spine if there is only one present.
        :type timestamp_key: str
        :param from_source: Whether feature values should be recomputed from the original data source. If ``None``,
            input feature values will be fetched from the Offline Store for Feature Views that have offline
            materialization enabled and otherwise computes feature values on the fly from raw data. Use
            ``from_source=True`` to force computing from raw data and ``from_source=False`` to error if any input
            Feature Views are not materialized. Defaults to None.
        :type from_source: bool
        :param save: Whether to persist the DataFrame as a Dataset object. Default is False.
        :type save: bool
        :param save_as: Name to save the DataFrame as. If unspecified and save=True, a name will be generated.
        :type: save_as: str
        :param compute_mode: Compute mode to use to produce the data frame.
        :type compute_mode: Optional[Union[ComputeMode, str]]

        Examples:
            An OnDemandFeatureView :py:mod:`fv` that expects request time data for the key :py:mod:`amount`.

            | The request time data is defined in the feature definition as such:
            | `request_schema = StructType()`
            | `request_schema.add(StructField('amount', DoubleType()))`
            | `transaction_request = RequestDataSource(request_schema=request_schema)`

            1) :py:mod:`fv.get_features_for_events(spine)` where :py:mod:`spine=pandas.Dataframe({'amount': [30, 50, 10000]})`
            Fetch features from the offline store with request time data inputs 30, 50, and 10000 for key 'amount'.

            2) :py:mod:`fv.get_features_for_events(spine, save_as='my_dataset')` where :py:mod:`spine=pandas.Dataframe({'amount': [30, 50, 10000]})`
            Fetch features from the offline store request time data inputs 30, 50, and 10000 for key 'amount'. Save the DataFrame as dataset with the name 'my_dataset'.

            An OnDemandFeatureView :py:mod:`fv` the expects request time data for the key :py:mod:`amount` and has a feature view dependency with join key :py:mod:`user_id`.

            1) :py:mod:`fv.get_features_for_events(spine)` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date_1': [datetime(...), datetime(...), datetime(...)], 'amount': [30, 50, 10000]})`
            Fetch features from the offline store for users 1, 2, and 3 for the specified timestamps and values for `amount` in the spine.

        :return: A Tecton :class:`TectonDataFrame`.
        """

        sources = self._check_can_query_from_source(from_source)
        sources.display()

        compute_mode = offline_retrieval_compute_mode(compute_mode)

        if compute_mode == ComputeMode.SNOWFLAKE or compute_mode == ComputeMode.ATHENA:
            raise errors.GET_FEATURES_FOR_EVENTS_UNSUPPORTED

        return querytree_api.get_features_for_events(
            dialect=compute_mode.default_dialect(),
            compute_mode=compute_mode,
            feature_definition=self._feature_definition,
            spine=events,
            timestamp_key=timestamp_key,
            from_source=from_source,
            save=save,
            save_as=save_as,
            mock_data_sources={},
        )

    @sdk_decorators.sdk_public_method(requires_validation=True)
    def get_historical_features(
        self,
        spine: Union[pyspark_dataframe.DataFrame, pandas.DataFrame, TectonDataFrame, str],
        timestamp_key: Optional[str] = None,
        from_source: Optional[bool] = None,
        save: bool = False,
        save_as: Optional[str] = None,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> TectonDataFrame:
        """Returns a Tecton :class:`TectonDataFrame` of historical values for this feature view.

        By default (i.e. ``from_source=None``), this method fetches feature values from the Offline Store for input
        Feature Views that have offline materialization enabled and otherwise computes input feature values on the fly
        from raw data.

        :param spine: The spine to join against, as a dataframe.
            The returned data frame will contain rollups for all (join key, request data key)
            combinations that are required to compute a full frame from the spine.
        :type spine: Union[pyspark.sql.DataFrame, pandas.DataFrame, TectonDataFrame]
        :param timestamp_key: Name of the time column in spine.
            This method will fetch the latest features computed before the specified timestamps in this column.
            If unspecified and this feature view has feature view dependencies, `timestamp_key` will default to the time column of the spine if there is only one present.
        :type timestamp_key: str
        :param from_source: Whether feature values should be recomputed from the original data source. If ``None``,
            input feature values will be fetched from the Offline Store for Feature Views that have offline
            materialization enabled and otherwise computes feature values on the fly from raw data. Use
            ``from_source=True`` to force computing from raw data and ``from_source=False`` to error if any input
            Feature Views are not materialized. Defaults to None.
        :type from_source: bool
        :param save: Whether to persist the DataFrame as a Dataset object. Default is False.
        :type save: bool
        :param save_as: Name to save the DataFrame as. If unspecified and save=True, a name will be generated.
        :type: save_as: str
        :param compute_mode: Compute mode to use to produce the data frame.
        :type compute_mode: Optional[Union[ComputeMode, str]]

        Examples:
            An OnDemandFeatureView :py:mod:`fv` that expects request time data for the key :py:mod:`amount`.

            | The request time data is defined in the feature definition as such:
            | `request_schema = StructType()`
            | `request_schema.add(StructField('amount', DoubleType()))`
            | `transaction_request = RequestDataSource(request_schema=request_schema)`

            1) :py:mod:`fv.get_historical_features(spine)` where :py:mod:`spine=pandas.Dataframe({'amount': [30, 50, 10000]})`
            Fetch historical features from the offline store with request time data inputs 30, 50, and 10000 for key 'amount'.

            2) :py:mod:`fv.get_historical_features(spine, save_as='my_dataset')` where :py:mod:`spine=pandas.Dataframe({'amount': [30, 50, 10000]})`
            Fetch historical features from the offline store request time data inputs 30, 50, and 10000 for key 'amount'. Save the DataFrame as dataset with the name 'my_dataset'.

            An OnDemandFeatureView :py:mod:`fv` the expects request time data for the key :py:mod:`amount` and has a feature view dependency with join key :py:mod:`user_id`.

            1) :py:mod:`fv.get_historical_features(spine)` where :py:mod:`spine=pandas.Dataframe({'user_id': [1,2,3], 'date_1': [datetime(...), datetime(...), datetime(...)], 'amount': [30, 50, 10000]})`
            Fetch historical features from the offline store for users 1, 2, and 3 for the specified timestamps and values for `amount` in the spine.

        :return: A Tecton :class:`TectonDataFrame`.
        """

        sources = self._check_can_query_from_source(from_source)
        sources.display()

        compute_mode = offline_retrieval_compute_mode(compute_mode)

        if compute_mode == ComputeMode.SNOWFLAKE and (
            conf.get_bool("USE_DEPRECATED_SNOWFLAKE_RETRIEVAL")
            or snowflake_api.has_snowpark_transformation([self._feature_definition])
        ):
            return snowflake_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                from_source=from_source,
                save=save,
                save_as=save_as,
                feature_set_config=feature_set_config.FeatureSetConfig.from_feature_definition(
                    self._feature_definition
                ),
                append_prefix=False,
            )

        if compute_mode == ComputeMode.ATHENA and conf.get_bool("USE_DEPRECATED_ATHENA_RETRIEVAL"):
            if not self._feature_definition.materialization_enabled:
                raise errors.ATHENA_COMPUTE_ONLY_SUPPORTED_IN_LIVE_WORKSPACE

            return athena_api.get_historical_features(
                spine=spine,
                timestamp_key=timestamp_key,
                from_source=from_source,
                save=save,
                save_as=save_as,
                feature_set_config=feature_set_config,
            )

        return querytree_api.get_historical_features_for_feature_definition(
            dialect=compute_mode.default_dialect(),
            compute_mode=compute_mode,
            feature_definition=self._feature_definition,
            spine=spine,
            timestamp_key=timestamp_key,
            start_time=None,
            end_time=None,
            entities=None,
            from_source=from_source,
            save=save,
            save_as=save_as,
            mock_data_sources={},
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def get_online_features(
        self,
        join_keys: Optional[Mapping[str, Union[int, np.int_, str, bytes]]] = None,
        include_join_keys_in_response: bool = False,
        request_data: Optional[Mapping[str, Union[int, np.int_, str, bytes, float]]] = None,
    ) -> FeatureVector:
        """Returns a single Tecton :class:`tecton.FeatureVector` from the Online Store.

        At least one of join_keys or request_data is required.

        :param join_keys: Join keys of the enclosed FeatureViews.
        :param include_join_keys_in_response: Whether to include join keys as part of the response FeatureVector.
        :param request_data: Dictionary of request context values used for OnDemandFeatureViews.

          Examples:
            An OnDemandFeatureView :py:mod:`fv` that expects request time data for the key :py:mod:`amount`.

            | The request time data is defined in the feature definition as such:
            | `request_schema = StructType()`
            | `request_schema.add(StructField('amount', DoubleType()))`
            | `transaction_request = RequestDataSource(request_schema=request_schema)`

            1) :py:mod:`fv.get_online_features(request_data={'amount': 50})`
            Fetch the latest features with input amount=50.

            An OnDemandFeatureView :py:mod:`fv` that has a feature view dependency with join key :py:mod:`user_id` and expects request time data for the key :py:mod:`amount`.

            1) :py:mod:`fv.get_online_features(join_keys={'user_id': 1}, request_data={'amount': 50}, include_join_keys_in_respone=True)`
            Fetch the latest features from the online store for user 1 with input amount=50.
            In the returned FeatureVector, nclude the join key information (user_id=1).


        :return: A :class:`tecton.FeatureVector` of the results.
        """
        # Default to empty dicts.
        join_keys = join_keys or {}
        request_data = request_data or {}

        if not join_keys and not request_data:
            raise errors.GET_ONLINE_FEATURES_REQUIRED_ARGS

        if not join_keys and self._get_dependent_feature_views():
            raise errors.GET_ONLINE_FEATURES_ODFV_JOIN_KEYS

        request_context = self._request_context
        required_request_context_keys = list(request_context.schema.keys())
        if len(required_request_context_keys) > 0 and request_data is None:
            raise errors.GET_ONLINE_FEATURES_FV_NO_REQUEST_DATA(required_request_context_keys)
        internal_utils.validate_request_data(request_data, required_request_context_keys)

        return query_helper._QueryHelper(self.workspace, feature_view_name=self.name).get_feature_vector(
            join_keys,
            include_join_keys_in_response,
            request_data,
            request_context,
        )

    @property
    @sdk_decorators.assert_valid
    def _request_context(self) -> request_context.RequestContext:
        rc = pipeline_common.find_request_context(self._feature_definition.pipeline.root)
        return request_context.RequestContext({}) if rc is None else request_context.RequestContext.from_proto(rc)


@typechecked
def on_demand_feature_view(
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    prevent_destroy: bool = False,
    mode: str,
    sources: List[Union[configs.RequestSource, FeatureView, "FeatureReference"]],
    schema: List[types.Field],
    environments: Optional[List[str]] = None,
):
    """
    Declare an On-Demand Feature View

    :param mode: Whether the annotated function is a pipeline function ("pipeline" mode) or a transformation function ("python" or "pandas" mode).
        For the non-pipeline mode, an inferred transformation will also be registered.
    :param sources: The data source inputs to the feature view. An input can be a RequestSource or a materialized Feature View.
    :param schema: Tecton schema matching the expected output of the transformation.
    :param description: A human readable description.
    :param owner: Owner name (typically the email of the primary maintainer).
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :param name: Unique, human friendly name that identifies the FeatureView. Defaults to the function name.
    :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
        destructive update) during tecton plan/apply. To remove or update this object, ``prevent_destroy`` must be
        set to False via the same tecton apply or a separate tecton apply. ``prevent_destroy`` can be used to prevent accidental changes
        such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
        triggers expensive rematerialization jobs. ``prevent_destroy`` also blocks changes to dependent Tecton objects
        that would trigger a recreate of the tagged object, e.g. if ``prevent_destroy`` is set on a Feature Service,
        that will also prevent deletions or re-creates of Feature Views used in that service. ``prevent_destroy`` is
        only enforced in live (i.e. non-dev) workspaces.
    :param environments: The environments in which this feature view can run. Defaults to `None`, which means
        the feature view can run in any environment. If specified, the feature view will only run in the specified
        environments. Learn more about environments at
        https://docs.tecton.ai/docs/defining-features/feature-views/on-demand-feature-view/on-demand-feature-view-environments.
    :return: An object of type :class:`tecton.OnDemandFeatureView`.

    An example declaration of an on-demand feature view using Python mode.
    With Python mode, the function sources will be dictionaries, and the function is expected to return a dictionary matching the schema from `output_schema`.
    Tecton recommends using Python mode for improved online serving performance.

    .. code-block:: python

        from tecton import RequestSource, on_demand_feature_view
        from tecton.types import Field, Float64, Int64

        # Define the request schema
        transaction_request = RequestSource(schema=[Field("amount", Float64)])

        # Define the output schema
        output_schema = [Field("transaction_amount_is_high", Int64)]

        # This On-Demand Feature View evaluates a transaction amount and declares it as "high", if it's higher than 10,000
        @on_demand_feature_view(
            sources=[transaction_request],
            mode='python',
            schema=output_schema,
            owner='matt@tecton.ai',
            tags={'release': 'production', 'prevent-destroy': 'true', 'prevent-recreate': 'true'},
            description='Whether the transaction amount is considered high (over $10000)'
        )

        def transaction_amount_is_high(transaction_request):
            result = {}
            result['transaction_amount_is_high'] = int(transaction_request['amount'] >= 10000)
            return result

    An example declaration of an on-demand feature view using Pandas mode.
    With Pandas mode, the function sources will be Pandas Dataframes, and the function is expected to return a Dataframe matching the schema from `output_schema`.

    .. code-block:: python

        from tecton import RequestSource, on_demand_feature_view
        from tecton.types import Field, Float64, Int64
        import pandas

        # Define the request schema
        transaction_request = RequestSource(schema=[Field("amount", Float64)])

        # Define the output schema
        output_schema = [Field("transaction_amount_is_high", Int64)]

        # This On-Demand Feature View evaluates a transaction amount and declares it as "high", if it's higher than 10,000
        @on_demand_feature_view(
            sources=[transaction_request],
            mode='pandas',
            schema=output_schema,
            owner='matt@tecton.ai',
            tags={'release': 'production', 'prevent-destroy': 'true', 'prevent-recreate': 'true'},
            description='Whether the transaction amount is considered high (over $10000)'
        )
        def transaction_amount_is_high(transaction_request):
            import pandas as pd

            df = pd.DataFrame()
            df['transaction_amount_is_high'] = (transaction_request['amount'] >= 10000).astype('int64')
            return df
    """

    def decorator(feature_view_function):
        return OnDemandFeatureView(
            name=name or feature_view_function.__name__,
            description=description,
            owner=owner,
            tags=tags,
            prevent_destroy=prevent_destroy,
            mode=mode,
            sources=sources,
            schema=schema,
            feature_view_function=feature_view_function,
            environments=environments,
        )

    return decorator


@attrs.define
class FeatureReference:
    """A reference to a Feature Definition used in Feature Service construction.

    By default, you can add all of the features in a Feature Definition (i.e. a Feature View or Feature Table) to a
    Feature Service by passing the Feature Definition into the ``features`` parameter of a Feature Service. However,
    if you want to specify a subset, you can use this class.

    You can use the double-bracket notation ``my_feature_view[[<features>]]`` as a short-hand for generating a
    FeatureReference from a Feature Defintion. This is the preferred way to select a subset of the features
    contained in a Feature Definition. As an example:

    .. highlight:: python
    .. code-block:: python

       from tecton import FeatureService
       from feature_repo.features import my_feature_view_1, my_feature_view_2

       my_feature_service = FeatureService(
           name='my_feature_service',
           features=[
               # Add all features from my_feature_view_1 to this FeatureService
               my_feature_view_1,
               # Add a single feature from my_feature_view_2, 'my_feature'
               my_feature_view_2[['my_feature']]
           ]
       )

    :param feature_definition: The Feature View or Feature Table.
    :param namespace: A namespace used to prefix the features joined from this FeatureView. By default, namespace
        is set to the FeatureView name.
    :param features: The subset of features to select from the FeatureView. If empty, all features will be included.
    :param override_join_keys: A map from feature view join key to spine join key override.
    """

    feature_definition: FeatureView = attrs.field(on_setattr=attrs.setters.frozen, repr=utils.short_tecton_object_repr)
    namespace: str
    features: Optional[List[str]]
    override_join_keys: Optional[Dict[str, str]]

    def __init__(
        self,
        *,
        feature_definition: FeatureView,
        namespace: Optional[str] = None,
        features: Optional[List[str]] = None,
        override_join_keys: Optional[Dict[str, str]] = None,
    ):
        namespace = namespace if namespace is not None else feature_definition.name
        self.__attrs_init__(
            feature_definition=feature_definition,
            namespace=namespace,
            features=features,
            override_join_keys=override_join_keys,
        )

    @property
    def id(self) -> id_pb2.Id:
        return self.feature_definition._id_proto

    @sdk_decorators.documented_by(FeatureView.with_name)
    def with_name(self, namespace: str) -> "FeatureReference":
        self.namespace = namespace
        return self

    @sdk_decorators.documented_by(FeatureView.with_join_key_map)
    def with_join_key_map(self, join_key_map: Dict[str, str]) -> "FeatureReference":
        self.override_join_keys = join_key_map.copy()
        return self


def _validate_fv_input_count(
    sources: Sequence[
        Union[
            filtered_source.FilteredSource,
            framework_data_source.BatchSource,
            framework_data_source.PushSource,
            framework_data_source.StreamSource,
            configs.RequestSource,
            FeatureReference,
            FeatureView,
        ]
    ],
    feature_view_function: Optional[Callable],
):
    if feature_view_function is None:
        return
    num_fn_params = len(_get_source_input_params(feature_view_function))
    num_sources = len(sources)
    if num_sources != num_fn_params:
        raise errors.INVALID_NUMBER_OF_FEATURE_VIEW_INPUTS(num_sources, num_fn_params)


@typechecked
def _build_pipeline_for_materialized_feature_view(
    fv_name: str,
    feature_view_function: Callable,
    pipeline_function: Callable[..., framework_transformation.PipelineNodeWrapper],
    sources: Sequence[Union[framework_data_source.DataSource, filtered_source.FilteredSource]],
) -> framework_transformation.PipelineNodeWrapper:
    fn_params = _get_source_input_params(feature_view_function)
    params_to_sources = dict(zip(fn_params, sources))
    pipeline_root = _transformation_to_pipeline_node(pipeline_function, params_to_sources)
    # we bind to user_function since pipeline_function may be artificially created and just accept **kwargs
    _test_binding_user_function(feature_view_function, params_to_sources)

    pipeline_common.transformation_type_checker(
        fv_name,
        pipeline_root.node_proto,
        "pipeline",
        ["pipeline", "spark_sql", "pyspark", "snowflake_sql", "athena", "snowpark"],
    )

    return pipeline_root


def _get_or_create_pipeline_function(
    name: str,
    mode: str,
    description: Optional[str],
    owner: Optional[str],
    tags: Optional[Dict[str, str]],
    feature_view_function,
):
    if mode == PIPELINE_MODE:
        pipeline_function = feature_view_function
    else:
        # Separate out the Transformation and manually construct a simple pipeline function.
        # We infer owner/family/tags but not a description.
        inferred_transform = framework_transformation.transformation(mode, name, description, owner, tags=tags)(
            feature_view_function
        )

        def pipeline_function(**kwargs):
            return inferred_transform(**kwargs)

    return pipeline_function


def feature_view_from_spec(feature_view_spec: specs.FeatureViewSpec, fco_container_: fco_container.FcoContainer):
    if isinstance(feature_view_spec, specs.OnDemandFeatureViewSpec):
        return OnDemandFeatureView._from_spec(feature_view_spec, fco_container_)
    elif isinstance(feature_view_spec, specs.FeatureTableSpec):
        return FeatureTable._from_spec(feature_view_spec, fco_container_)
    elif isinstance(feature_view_spec, specs.MaterializedFeatureViewSpec):
        if feature_view_spec.data_source_type == data_source_type_pb2.DataSourceType.BATCH:
            return BatchFeatureView._from_spec(feature_view_spec, fco_container_)
        if feature_view_spec.data_source_type in (
            data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH,
            data_source_type_pb2.DataSourceType.PUSH_WITH_BATCH,
            data_source_type_pb2.DataSourceType.PUSH_NO_BATCH,
        ):
            return StreamFeatureView._from_spec(feature_view_spec, fco_container_)
    msg = "Missing or unsupported FeatureView type."
    raise errors.INTERNAL_ERROR(msg)


def _build_odfv_sources_from_spec(
    spec: specs.OnDemandFeatureViewSpec, fco_container_: fco_container.FcoContainer
) -> Tuple[Union[FeatureReference, configs.RequestSource], ...]:
    sources = []
    request_context = pipeline_common.find_request_context(spec.pipeline.root)
    if request_context is not None:
        request_schema = querytree_api.get_fields_list_from_tecton_schema(request_context.tecton_schema)
        sources.append(configs.RequestSource(schema=request_schema))

    feature_view_nodes = pipeline_common.get_all_feature_view_nodes(spec.pipeline)
    for node in feature_view_nodes:
        fv_spec = fco_container_.get_by_id_proto(node.feature_view_node.feature_view_id)
        fv = feature_view_from_spec(fv_spec, fco_container_)
        override_join_keys = {
            colpair.feature_column: colpair.spine_column
            for colpair in node.feature_view_node.feature_reference.override_join_keys
        }
        feature_reference = FeatureReference(
            feature_definition=fv,
            namespace=node.feature_view_node.feature_reference.namespace,
            features=node.feature_view_node.feature_reference.features,
            override_join_keys=override_join_keys,
        )
        sources.append(feature_reference)

    return sources


def _get_source_input_params(user_function) -> List[str]:
    # Filter out the materailization context to avoid mapping data sources to it.
    return [
        param.name
        for param in inspect.signature(user_function).parameters.values()
        if not isinstance(param.default, materialization_context.BaseMaterializationContext)
    ]


def _source_to_pipeline_node(
    source: Union[
        framework_data_source.DataSource,
        filtered_source.FilteredSource,
        configs.RequestSource,
        FeatureView,
        FeatureReference,
    ],
    input_name: str,
) -> framework_transformation.PipelineNodeWrapper:
    if isinstance(source, FeatureView):
        source = FeatureReference(feature_definition=source)

    pipeline_node = pipeline_pb2.PipelineNode()
    if isinstance(source, framework_data_source.DataSource):
        node = pipeline_pb2.DataSourceNode(
            virtual_data_source_id=source._id_proto,
            window_unbounded=True,
            schedule_offset=time_utils.timedelta_to_proto(source.data_delay),
            input_name=input_name,
        )
        pipeline_node.data_source_node.CopyFrom(node)
    elif isinstance(source, filtered_source.FilteredSource):
        node = pipeline_pb2.DataSourceNode(
            virtual_data_source_id=source.source._id_proto,
            schedule_offset=time_utils.timedelta_to_proto(source.source.data_delay),
            input_name=input_name,
        )
        if source.start_time_offset <= MIN_START_OFFSET:
            node.window_unbounded_preceding = True
        else:
            node.start_time_offset.FromTimedelta(source.start_time_offset)

        pipeline_node.data_source_node.CopyFrom(node)
    elif isinstance(source, configs.RequestSource):
        request_schema = source.schema
        schema_proto = type_utils.to_tecton_schema(request_schema)

        node = pipeline_pb2.RequestDataSourceNode(
            request_context=pipeline_pb2.RequestContext(tecton_schema=schema_proto),
            input_name=input_name,
        )
        pipeline_node.request_data_source_node.CopyFrom(node)
    elif isinstance(source, FeatureReference):
        override_join_keys = None
        if source.override_join_keys:
            override_join_keys = [
                feature_service_pb2.ColumnPair(spine_column=spine_key, feature_column=fv_key)
                for fv_key, spine_key in sorted(source.override_join_keys.items())
            ]
        node = pipeline_pb2.FeatureViewNode(
            feature_view_id=source.id,
            input_name=input_name,
            feature_reference=feature_service_pb2.FeatureReference(
                feature_view_id=source.id,
                override_join_keys=override_join_keys,
                namespace=source.namespace,
                features=source.features,
            ),
        )
        pipeline_node.feature_view_node.CopyFrom(node)
    else:
        msg = f"Invalid source type: {type(source)}"
        raise TypeError(msg)
    return framework_transformation.PipelineNodeWrapper(node_proto=pipeline_node)


def _transformation_to_pipeline_node(
    pipeline_function: Callable,
    params_to_sources: Dict[
        str,
        Union[
            framework_data_source.DataSource,
            filtered_source.FilteredSource,
            configs.RequestSource,
            FeatureView,
            FeatureReference,
        ],
    ],
) -> framework_transformation.PipelineNodeWrapper:
    pipeline_kwargs = _sources_to_pipeline_nodes(params_to_sources)
    pipeline_fn_result = pipeline_function(**pipeline_kwargs)
    return pipeline_fn_result


def _test_binding_user_function(fn, inputs):
    # this function binds the top-level pipeline function only, for transformation binding, see transformation.__call__
    pipeline_signature = inspect.signature(fn)
    try:
        pipeline_signature.bind(**inputs)
    except TypeError as e:
        msg = f"while binding inputs to pipeline function, TypeError: {e}"
        raise TypeError(msg)


def _sources_to_pipeline_nodes(
    params_to_sources: Dict[
        str,
        Union[
            framework_data_source.DataSource,
            filtered_source.FilteredSource,
            configs.RequestSource,
            FeatureView,
            FeatureReference,
        ],
    ],
) -> Dict[str, framework_transformation.PipelineNodeWrapper]:
    kwargs = {}
    for param_name, source in params_to_sources.items():
        pipeline_node = _source_to_pipeline_node(source=source, input_name=param_name)
        kwargs[param_name] = pipeline_node

    return kwargs


def _build_default_cluster_config():
    return feature_view__args_pb2.ClusterConfig(
        implicit_config=feature_view__args_pb2.DefaultClusterConfig(
            **{
                **configs.DEFAULT_SPARK_VERSIONS,
                **configs.TECTON_COMPUTE_DEFAULTS,
            }
        )
    )


def _build_pipeline_for_odfv(
    fv_name: str,
    user_function: Callable,
    pipeline_function: Callable[..., framework_transformation.PipelineNodeWrapper],
    sources: Sequence[Union[configs.RequestSource, FeatureReference, FeatureView]],
) -> framework_transformation.PipelineNodeWrapper:
    fn_params = _get_source_input_params(user_function)
    params_to_sources = dict(zip(fn_params, sources))
    pipeline_root = _transformation_to_pipeline_node(pipeline_function, params_to_sources)
    # we bind to user_function since pipeline_function may be artificially created and just accept **kwargs
    _test_binding_user_function(user_function, params_to_sources)

    pipeline_common.transformation_type_checker(
        fv_name, pipeline_root.node_proto, "pipeline", ["pipeline", "pandas", "python"]
    )
    return pipeline_root


_SPARK_MODES = {
    transformation_pb2.TRANSFORMATION_MODE_PYSPARK,
    transformation_pb2.TRANSFORMATION_MODE_SPARK_SQL,
}


def _is_spark_config(config: Optional[configs.ComputeConfigTypes]) -> bool:
    if config is None:
        return False
    # This looks silly right now because it's all the possible types, but soon there will be e.g. a TectonComputeConfig
    # for managed compute.
    return isinstance(
        config,
        (
            configs.DatabricksClusterConfig,
            configs.EMRClusterConfig,
            configs.DatabricksJsonClusterConfig,
            configs.DataprocJsonClusterConfig,
            configs.EMRJsonClusterConfig,
        ),
    )


def infer_batch_compute_mode(
    pipeline_root: Optional[PipelineNodeWrapper],
    batch_compute_config: configs.ComputeConfigTypes,
    stream_compute_config: Optional[configs.ComputeConfigTypes],
) -> BatchComputeMode:
    has_spark_config = any(_is_spark_config(c) for c in (batch_compute_config, stream_compute_config))
    transformations = pipeline_root.transformations if pipeline_root is not None else []
    has_spark_transforms = any(t.transformation_mode in _SPARK_MODES for t in transformations)
    if has_spark_config or has_spark_transforms:
        return BatchComputeMode.SPARK
    else:
        return default_batch_compute_mode()


@typechecked
def _build_materialized_feature_view_args(
    name: str,
    pipeline_root: PipelineNodeWrapper,
    entities: Sequence[framework_entity.Entity],
    online: bool,
    offline: bool,
    offline_store: configs.OfflineStoreConfig,
    online_store: Optional[configs.OnlineStoreTypes],
    aggregation_interval: Optional[datetime.timedelta],
    aggregations: Optional[Sequence[configs.Aggregation]],
    aggregation_secondary_key: Optional[str],
    ttl: Optional[datetime.timedelta],
    feature_start_time: Optional[datetime.datetime],
    lifetime_start_time: Optional[datetime.datetime],
    manual_trigger_backfill_end_time: Optional[datetime.datetime],
    batch_schedule: Optional[datetime.timedelta],
    online_serving_index: Optional[Sequence[str]],
    batch_compute: configs.ComputeConfigTypes,
    stream_compute: Optional[configs.ComputeConfigTypes],
    monitor_freshness: bool,
    data_quality_enabled: Optional[bool],
    skip_default_expectations: Optional[bool],
    expected_feature_freshness: Optional[datetime.timedelta],
    alert_email: Optional[str],
    description: Optional[str],
    owner: Optional[str],
    tags: Optional[Dict[str, str]],
    feature_view_type: feature_view__args_pb2.FeatureViewType.ValueType,
    timestamp_field: Optional[str],
    data_source_type: data_source_type_pb2.DataSourceType.ValueType,
    incremental_backfills: bool,
    prevent_destroy: bool,
    run_transformation_validation: Optional[bool] = None,
    stream_processing_mode: Optional[StreamProcessingMode] = None,
    max_backfill_interval: Optional[datetime.timedelta] = None,
    output_stream: Optional[configs.OutputStream] = None,
    batch_trigger: Optional[BatchTriggerType] = None,
    schema: Optional[List[types.Field]] = None,
    options: Optional[Dict[str, str]] = None,
    tecton_materialization_runtime: Optional[str] = None,
    cache_config: Optional[configs.CacheConfig] = None,
    compaction_enabled: bool = False,
    stream_tiling_enabled: bool = False,
    environment: Optional[str] = None,
) -> feature_view__args_pb2.FeatureViewArgs:
    """Build feature view args proto for materialized feature views (i.e. batch and stream feature views)."""
    monitoring = configs.MonitoringConfig(
        monitor_freshness=monitor_freshness, expected_freshness=expected_feature_freshness, alert_email=alert_email
    )

    aggregation_protos = None
    if aggregations:
        is_continuous = stream_processing_mode == StreamProcessingMode.CONTINUOUS
        if compaction_enabled and stream_tiling_enabled and aggregation_interval:
            raise errors.AGGREGATION_INTERVAL_SET_COMPACTION()
        else:
            if aggregation_interval is None:
                aggregation_interval = datetime.timedelta(seconds=0)
        aggregation_protos = [
            agg._to_proto(aggregation_interval, is_continuous, compaction_enabled) for agg in aggregations
        ]

    secondary_key_output_columns = (
        _create_secondary_key_output_columns(aggregations, aggregation_secondary_key)
        if aggregation_secondary_key
        else None
    )

    schema_proto = type_utils.to_tecton_schema(schema) if schema else None
    # TODO(TEC-17296): populate default value for tecton_materialization_runtime from repo config
    return feature_view__args_pb2.FeatureViewArgs(
        feature_view_id=id_helper.IdHelper.generate_id(),
        version=feature_definition_wrapper.FrameworkVersion.FWV5.value,
        info=basic_info_pb2.BasicInfo(name=name, description=description, owner=owner, tags=tags),
        prevent_destroy=prevent_destroy,
        entities=[
            feature_view__args_pb2.EntityKeyOverride(entity_id=entity._id_proto, join_keys=entity.join_keys)
            for entity in entities
        ],
        pipeline=pipeline_pb2.Pipeline(root=pipeline_root.node_proto),
        feature_view_type=feature_view_type,
        online_serving_index=online_serving_index if online_serving_index else None,
        online_enabled=online,
        offline_enabled=offline,
        data_quality_config=feature_view__args_pb2.DataQualityConfig(
            data_quality_enabled=data_quality_enabled,
            skip_default_expectations=skip_default_expectations,
        ),
        batch_compute_mode=infer_batch_compute_mode(
            pipeline_root=pipeline_root, batch_compute_config=batch_compute, stream_compute_config=stream_compute
        ).value,
        materialized_feature_view_args=feature_view__args_pb2.MaterializedFeatureViewArgs(
            timestamp_field=timestamp_field,
            feature_start_time=time_utils.datetime_to_proto(feature_start_time),
            lifetime_start_time=time_utils.datetime_to_proto(lifetime_start_time),
            manual_trigger_backfill_end_time=time_utils.datetime_to_proto(manual_trigger_backfill_end_time),
            batch_schedule=time_utils.timedelta_to_proto(batch_schedule),
            online_store=online_store._to_proto() if online_store else None,
            max_backfill_interval=time_utils.timedelta_to_proto(max_backfill_interval),
            monitoring=monitoring._to_proto(),
            data_source_type=data_source_type,
            aggregation_secondary_key=aggregation_secondary_key,
            secondary_key_output_columns=secondary_key_output_columns,
            incremental_backfills=incremental_backfills,
            batch_trigger=batch_trigger.value,
            output_stream=output_stream._to_proto() if output_stream else None,
            batch_compute=batch_compute._to_cluster_proto(),
            stream_compute=stream_compute._to_cluster_proto() if stream_compute else None,
            serving_ttl=time_utils.timedelta_to_proto(ttl),
            stream_processing_mode=stream_processing_mode.value if stream_processing_mode else None,
            aggregations=aggregation_protos,
            aggregation_interval=time_utils.timedelta_to_proto(aggregation_interval),
            schema=schema_proto,
            run_transformation_validation=run_transformation_validation,
            tecton_materialization_runtime=tecton_materialization_runtime,
            offline_store=offline_store._to_proto(),
            stream_tiling_enabled=stream_tiling_enabled,
            stream_tile_size=_compute_compacted_fv_stream_tile_size(aggregations) if stream_tiling_enabled else None,
            compaction_enabled=compaction_enabled,
            environment=environment,
        ),
        options=options,
        cache_config=cache_config._to_proto() if cache_config else None,
    )


def _create_secondary_key_output_columns(
    aggregations: Sequence[configs.Aggregation], aggregation_secondary_key: str
) -> List[feature_view__args_pb2.SecondaryKeyOutputColumn]:
    secondary_time_windows: Sequence[specs.TimeWindowSpec] = sorted(
        # eliminates duplicates of time windows for secondary key output columns
        {agg.time_window._to_spec() for agg in aggregations},
        key=lambda tw: tw.to_sort_tuple(),
        reverse=True,
    )

    secondary_key_output_columns = []
    for window in secondary_time_windows:
        name = f"{aggregation_secondary_key}_keys_{window.to_string()}".replace(" ", "")
        if isinstance(window, LifetimeWindowSpec):
            output_col = feature_view__args_pb2.SecondaryKeyOutputColumn(
                lifetime_window=window.to_proto(),
                name=name,
            )
        elif isinstance(window, RelativeTimeWindowSpec):
            output_col = feature_view__args_pb2.SecondaryKeyOutputColumn(
                time_window=window.to_args_proto(),
                name=name,
            )
        elif isinstance(window, TimeWindowSeriesSpec):
            output_col = feature_view__args_pb2.SecondaryKeyOutputColumn(
                time_window_series=window.to_args_proto(),
                name=name,
            )
        else:
            msg = f"Unexpected time window type in agg args proto: {type(window)}"
            raise ValueError(msg)
        secondary_key_output_columns.append(output_col)
    return secondary_key_output_columns


def _compute_compacted_fv_stream_tile_size(
    aggregations: Optional[Sequence[configs.Aggregation]],
) -> Optional[duration_pb2.Duration]:
    """Calculate the compacted fv stream tile size.

    Only applicable for fvs with stream_tiling_enabled=True. This calculates the tile size used for the online stream table. Currently, this cannot be set by the user."""
    if aggregations is None or len(aggregations) == 0:
        msg = "Only feature views with aggregations can set `stream_tiling_enabled`=True"
        raise ValueError(msg)

    relative_time_windows = []
    for agg in aggregations:
        if isinstance(agg.time_window, configs.TimeWindow):
            relative_time_windows.append(agg.time_window)
        elif isinstance(agg.time_window, configs.TimeWindowSeries):
            raise errors.COMPACTION_TIME_WINDOW_SERIES_UNSUPPORTED()

    if relative_time_windows:
        min_time_window = min([window.window_size for window in relative_time_windows])
        if min_time_window < timedelta(hours=1):
            return time_utils.timedelta_to_proto(timedelta(minutes=1))
        elif min_time_window < timedelta(hours=10):
            return time_utils.timedelta_to_proto(timedelta(minutes=5))

    return time_utils.timedelta_to_proto(timedelta(hours=1))


def _compute_default_stream_processing_mode(
    has_push_source: bool,
    aggregations: Optional[Sequence[configs.Aggregation]],
    compaction_enabled: bool,
    stream_tiling_enabled: Optional[bool] = None,
):
    if has_push_source:
        # Stream Feature Views with Push Sources default to continuous-mode only.
        return StreamProcessingMode.CONTINUOUS
    elif compaction_enabled:
        # This is a Compacted stream feature view. We set defaults here for compacted feature views. The actual validations
        # will be in the validation server.
        return StreamProcessingMode.CONTINUOUS if not stream_tiling_enabled else None
    elif aggregations:
        return StreamProcessingMode.TIME_INTERVAL
    return None
