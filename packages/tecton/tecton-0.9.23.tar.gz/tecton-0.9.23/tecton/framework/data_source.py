from __future__ import annotations

import datetime
import json
import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import attrs
import pandas
from pyspark.sql import dataframe as pyspark_dataframe
from pyspark.sql import streaming as pyspark_streaming
from typeguard import typechecked

from tecton import types
from tecton._internals import display
from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals import querytree_api
from tecton._internals import sdk_decorators
from tecton._internals import snowflake_api
from tecton._internals import spark_api
from tecton._internals import type_utils
from tecton._internals import validations_api
from tecton._internals.ingestion import IngestionClient
from tecton.framework import base_tecton_object
from tecton.framework import configs
from tecton.framework import data_frame
from tecton_core import conf
from tecton_core import id_helper
from tecton_core import specs
from tecton_core.compute_mode import BatchComputeMode
from tecton_core.compute_mode import ComputeMode
from tecton_core.compute_mode import default_batch_compute_mode
from tecton_core.compute_mode import offline_retrieval_compute_mode
from tecton_core.specs.utils import get_field_or_none
from tecton_proto.args import basic_info_pb2
from tecton_proto.args import fco_args_pb2
from tecton_proto.args import virtual_data_source_pb2 as virtual_data_source__args_pb2
from tecton_proto.common import data_source_type_pb2
from tecton_proto.common import fco_locator_pb2
from tecton_proto.common import framework_version_pb2
from tecton_proto.common import schema_container_pb2
from tecton_proto.common import spark_schema_pb2
from tecton_proto.common.spark_schema_pb2 import SparkSchema
from tecton_proto.metadataservice import metadata_service_pb2
from tecton_proto.validation import validator_pb2
from tecton_spark import spark_schema_wrapper
from tecton_spark.type_annotations import is_pyspark_df


BatchConfigType = Union[
    configs.FileConfig,
    configs.HiveConfig,
    configs.RedshiftConfig,
    configs.SnowflakeConfig,
    configs.SparkBatchConfig,
    configs.UnityConfig,
    configs.PandasBatchConfig,
]

StreamConfigType = Union[configs.KinesisConfig, configs.KafkaConfig, configs.SparkStreamConfig, configs.PushConfig]

logger = logging.getLogger(__name__)


@attrs.define(eq=False)
class DataSource(base_tecton_object.BaseTectonObject):
    """Base class for Data Source classes."""

    # A data source spec, i.e. a dataclass representation of the Tecton object that is used in most functional use
    # cases, e.g. constructing queries. Set only after the object has been validated. Remote objects, i.e. applied
    # objects fetched from the backend, are assumed valid.
    _spec: Optional[specs.DataSourceSpec] = attrs.field(repr=False)

    # A Tecton "args" proto. Only set if this object was defined locally, i.e. this object was not applied and
    # fetched from the Tecton backend.
    _args: Optional[virtual_data_source__args_pb2.VirtualDataSourceArgs] = attrs.field(
        repr=False, on_setattr=attrs.setters.frozen
    )

    # A supplement to the _args proto that is needed to create the Data Source spec.
    _args_supplement: Optional[specs.DataSourceSpecArgsSupplement] = attrs.field(
        repr=False, on_setattr=attrs.setters.frozen
    )

    @sdk_decorators.assert_local_object
    def _build_args(self) -> fco_args_pb2.FcoArgs:
        return fco_args_pb2.FcoArgs(virtual_data_source=self._args)

    def _build_fco_validation_args(self) -> validator_pb2.FcoValidationArgs:
        if self.info._is_local_object:
            return validator_pb2.FcoValidationArgs(
                virtual_data_source=validator_pb2.VirtualDataSourceValidationArgs(
                    args=self._args,
                    batch_schema=self._args_supplement.batch_schema,
                    stream_schema=self._args_supplement.stream_schema,
                )
            )
        else:
            return self._spec.validation_args

    @property
    def _is_valid(self) -> bool:
        return self._spec is not None

    def _validate(self, indentation_level: int = 0) -> None:
        if self._is_valid:
            return

        try:
            self._derive_schemas(indentation_level)
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
            validator_pb2.ValidationRequest(validation_args=[self._build_fco_validation_args()]),
            indentation_level,
        )

        self._spec = specs.DataSourceSpec.from_args_proto(self._args, self._args_supplement)

    @sdk_decorators.assert_local_object
    def _create_unvalidated_spec(
        self, mock_data: Union[pandas.DataFrame, pyspark_dataframe.DataFrame]
    ) -> specs.DataSourceSpec:
        """Create an unvalidated spec. Used for user unit testing, where backend validation is unavailable."""
        if is_pyspark_df(mock_data):
            schema = spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(mock_data.schema)
        elif isinstance(mock_data, pandas.DataFrame):
            # Using a empty schema for Rift, since Rift does not use the schema for batch sources.
            schema = SparkSchema()
        else:
            msg = f"Unexpected mock source type {type(mock_data)}"
            raise TypeError(msg)
        # Use the mock schema as both the batch and stream schema because StreamSource specs expect a non-nil stream
        # schema.
        supplement = attrs.evolve(self._args_supplement, batch_schema=schema, stream_schema=schema)
        return specs.DataSourceSpec.from_args_proto(self._args, supplement)

    def _derive_schemas(self, indentation_level: int) -> None:
        raise NotImplementedError

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def summary(self) -> display.Displayable:
        """Displays a human readable summary of this Data Source."""
        request = metadata_service_pb2.GetVirtualDataSourceSummaryRequest(
            fco_locator=fco_locator_pb2.FcoLocator(id=self._spec.id_proto, workspace=self._spec.workspace)
        )
        response = metadata_service.instance().GetVirtualDataSourceSummary(request)
        return display.Displayable.from_fco_summary(response.fco_summary)

    @sdk_decorators.sdk_public_method(requires_validation=True)
    def get_dataframe(
        self,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        *,
        apply_translator: bool = True,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> data_frame.TectonDataFrame:
        """Returns the data in this Data Source as a Tecton DataFrame.

        :param start_time: The interval start time from when we want to retrieve source data.
            If no timezone is specified, will default to using UTC.
            Can only be defined if ``apply_translator`` is True.
        :param end_time: The interval end time until when we want to retrieve source data.
            If no timezone is specified, will default to using UTC.
            Can only be defined if ``apply_translator`` is True.
        :param apply_translator: If True, the transformation specified by ``post_processor``
            will be applied to the dataframe for the data source. ``apply_translator`` is not applicable
            to batch sources configured with ``spark_batch_config`` because it does not have a
            ``post_processor``.
        :param compute_mode: Compute mode to use to produce the data frame.

        :return: A Tecton DataFrame containing the data source's raw or translated source data.

        :raises TectonValidationError: If ``apply_translator`` is False, but ``start_time`` or
            ``end_time`` filters are passed in.
        """
        compute_mode = offline_retrieval_compute_mode(compute_mode)
        _apply_translator = apply_translator
        if self._spec.type == data_source_type_pb2.DataSourceType.PUSH_NO_BATCH:
            if self._args is not None:
                # Object defined locally, and we can't really call get_dataframe on that.
                raise errors.DATA_SOURCE_HAS_NO_BATCH_CONFIG(self.name)
            else:
                _apply_translator = False

        if compute_mode == ComputeMode.SNOWFLAKE and conf.get_bool("USE_DEPRECATED_SNOWFLAKE_RETRIEVAL"):
            return snowflake_api.get_dataframe_for_data_source(self._spec, start_time, end_time)
        else:
            return querytree_api.get_dataframe_for_data_source(
                compute_mode.default_dialect(), compute_mode, self._spec, start_time, end_time, _apply_translator
            )

    @property
    def _data_source_type(self) -> data_source_type_pb2.DataSourceType.ValueType:
        if self._spec is not None:
            return self._spec.type
        else:
            return self._args.type

    @property
    def data_delay(self) -> Optional[datetime.timedelta]:
        """Returns the duration that materialization jobs wait after the ``batch_schedule`` before starting, typically to ensure that all data has landed."""
        if self._spec is not None:
            return self._spec.batch_source.data_delay if self._spec.batch_source is not None else None

        # This args data delay utility is needed so that feature view args can be constructed from unvalidated
        # data sources objects.
        if self._args.HasField("hive_ds_config"):
            return self._args.hive_ds_config.common_args.data_delay.ToTimedelta()
        elif self._args.HasField("unity_ds_config"):
            return self._args.unity_ds_config.common_args.data_delay.ToTimedelta()
        elif self._args.HasField("spark_batch_config"):
            return self._args.spark_batch_config.data_delay.ToTimedelta()
        elif self._args.HasField("pandas_batch_config"):
            return self._args.pandas_batch_config.data_delay.ToTimedelta()
        elif self._args.HasField("redshift_ds_config"):
            return self._args.redshift_ds_config.common_args.data_delay.ToTimedelta()
        elif self._args.HasField("snowflake_ds_config"):
            return self._args.snowflake_ds_config.common_args.data_delay.ToTimedelta()
        elif self._args.HasField("file_ds_config"):
            return self._args.file_ds_config.common_args.data_delay.ToTimedelta()
        elif self._args.type == data_source_type_pb2.DataSourceType.PUSH_NO_BATCH:
            return None
        else:
            msg = f"Invalid batch source args: {self._args}"
            raise ValueError(msg)

    def _rebuild_spec_with_schema(self) -> specs.DataSourceSpec:
        # This should only ever be called on a remote DS which is missing schema!
        def _raise_internal_validation_error(msg: str):
            full_message = f"Error rebuilding spec schema: {msg}"
            raise errors.TectonInternalError(full_message)

        if not self._is_valid:
            _raise_internal_validation_error("Object is not validated")
        if self._spec.schema is not None:
            _raise_internal_validation_error("Schema is already defined")
        if self._is_local_object:
            _raise_internal_validation_error("Refusing to rebuild schema for a local object")

        fco_validation_args = self._build_fco_validation_args()
        validation_args = fco_validation_args.virtual_data_source
        virtual_data_source_args = get_field_or_none(validation_args, "args")
        if virtual_data_source_args is None:
            _raise_internal_validation_error("Missing virtual data source args")

        batch_schema = None
        stream_schema = None
        if self._spec.batch_source:
            post_processor = getattr(self._spec.batch_source, "post_processor", None)
            function = getattr(self._spec.batch_source, "function", None)
            batch_schema = spark_api.derive_batch_schema(
                virtual_data_source_args,
                post_processor,
                function,
            )
        if self._spec.stream_source:
            post_processor = getattr(self._spec.stream_source, "post_processor", None)
            function = getattr(self._spec.stream_source, "function", None)
            stream_schema = spark_api.derive_stream_schema(
                virtual_data_source_args,
                post_processor,
                function,
            )
        supplement = specs.DataSourceSpecArgsSupplement(
            batch_schema=batch_schema,
            stream_schema=stream_schema,
        )
        return specs.DataSourceSpec.from_args_proto(
            virtual_data_source_args,
            supplement,
        )


@attrs.define(eq=False)
class BatchSource(DataSource):
    """A Tecton BatchSource, used to read batch data into Tecton for use in a BatchFeatureView.

    Example of a BatchSource declaration:

    .. code-block:: python

        # Declare a BatchSource with a HiveConfig instance as its batch_config parameter.
        # Refer to the "Configs Classes and Helpers" section for other batch_config types.
        from tecton import HiveConfig, BatchSource

        credit_scores_batch = BatchSource(
            name='credit_scores_batch',
            batch_config=HiveConfig(
                database='demo_fraud',
                table='credit_scores',
                timestamp_field='timestamp'
            ),
            owner='matt@tecton.ai',
            tags={'release': 'production'}
        )
    """

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        prevent_destroy: bool = False,
        batch_config: BatchConfigType,
        options: Optional[Dict[str, str]] = None,
    ):
        """Creates a new BatchSource.

        :param name: A unique name of the DataSource.
        :param description: A human-readable description.
        :param tags: Tags associated with this Tecton Data Source (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
            destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be
            set to False via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to prevent
            accidental changes such as inadvertantly deleting a Feature Service used in production or recreating a Feature
            View that triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton
            objects that would trigger a recreate of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
            that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
            only enforced in live (i.e. non-dev) workspaces.
        :param batch_config: BatchConfig object containing the configuration of the Batch Data Source to be included
            in this Data Source.
        :param options: Additional options to configure the Source. Used for advanced use cases and beta features.
        """
        from tecton.cli import repo_utils as cli_common

        ds_args = virtual_data_source__args_pb2.VirtualDataSourceArgs(
            virtual_data_source_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            version=framework_version_pb2.FrameworkVersion.FWV5,
            type=data_source_type_pb2.DataSourceType.BATCH,
            prevent_destroy=prevent_destroy,
            options=options,
        )
        batch_config._merge_batch_args(ds_args)

        info = base_tecton_object.TectonObjectInfo.from_args_proto(ds_args.info, ds_args.virtual_data_source_id)
        source_info = cli_common.construct_fco_source_info(ds_args.virtual_data_source_id)

        self.__attrs_init__(
            info=info,
            spec=None,
            args=ds_args,
            source_info=source_info,
            args_supplement=_build_args_supplement(batch_config, None),
        )

        base_tecton_object._register_local_object(self)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.DataSourceSpec) -> "BatchSource":
        """Create a BatchSource from directly from a spec. Specs are assumed valid and will not be re-validated."""
        info = base_tecton_object.TectonObjectInfo.from_spec(spec)
        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(
            info=info,
            spec=spec,
            args=None,
            source_info=None,
            args_supplement=None,
        )
        return obj

    def _derive_schemas(self, indentation_level: int) -> None:
        batch_compute_mode = default_batch_compute_mode()
        if batch_compute_mode == BatchComputeMode.RIFT:
            # Tecton Batch only supports explicit FV schemas & doesn't require data source schema inference.
            # TODO(TEC-16975): Remove when DataSource schema evaluation is lazy
            self._args_supplement.batch_schema = spark_schema_pb2.SparkSchema()
            return
        validations_api.print_deriving_schemas(self, indentation_level)
        if batch_compute_mode == BatchComputeMode.SNOWFLAKE:
            self._args_supplement.batch_schema = snowflake_api.derive_batch_schema(self._args)
        elif batch_compute_mode == BatchComputeMode.SPARK:
            self._args_supplement.batch_schema = spark_api.derive_batch_schema(
                self._args, self._args_supplement.batch_post_processor, self._args_supplement.batch_data_source_function
            )
        else:
            raise ValueError(batch_compute_mode)

    @sdk_decorators.sdk_public_method(requires_validation=True)
    def get_columns(self) -> List[str]:
        """Returns the column names of the Data Source's schema."""
        # TODO(jiadong): Add public doc to explain the context of this error message and put the link in the msg.
        # Internal context: Optional Data Source schema derivation(https://www.notion.so/tecton/Optional-Data-Source-Schema-82e7ca00d2664f6890b526bcbac50688)
        if self._spec.batch_source.spark_schema is None:
            msg = "`get_columns()` is not supported for this Data Source. Tecton did not pre-derive its schema. Use `get_dataframe()` to get the schema of this data source, e.g. `ds.get_dataframe().to_spark().schema` or `ds.get_dataframe().to_pandas().dtypes`."
            raise ValueError(msg)

        schema = self._spec.batch_source.spark_schema
        return [field.name for field in schema.fields]


@attrs.define(eq=False)
class StreamSource(DataSource):
    """A Tecton StreamSource, used to unify stream and batch data into Tecton for use in a StreamFeatureView.

    Example of a StreanSource declaration:

    .. code-block:: python

     import pyspark
        from tecton import KinesisConfig, HiveConfig, StreamSource
        from datetime import timedelta


        # Define our deserialization raw stream translator
        def raw_data_deserialization(df:pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
            from pyspark.sql.functions import col, from_json, from_utc_timestamp
            from pyspark.sql.types import StructType, StringType

            payload_schema = (
              StructType()
                    .add('amount', StringType(), False)
                    .add('isFraud', StringType(), False)
                    .add('timestamp', StringType(), False)
            )
            return (
                df.selectExpr('cast (data as STRING) jsonData')
                .select(from_json('jsonData', payload_schema).alias('payload'))
                .select(
                    col('payload.amount').cast('long').alias('amount'),
                    col('payload.isFraud').cast('long').alias('isFraud'),
                    from_utc_timestamp('payload.timestamp', 'UTC').alias('timestamp')
                )
            )

        # Declare a StreamSource with both a batch_config and a stream_config as parameters
        # See the API documentation for both BatchConfig and StreamConfig
        transactions_stream = StreamSource(
            name='transactions_stream',
            stream_config=KinesisConfig(
                stream_name='transaction_events',
                region='us-west-2',
                initial_stream_position='latest',
                watermark_delay_threshold=timedelta(minutes=30),
                timestamp_field='timestamp',
                post_processor=raw_data_deserialization, # deserialization function defined above
                options={'roleArn': 'arn:aws:iam::472542229217:role/demo-cross-account-kinesis-ro'}
            ),
            batch_config=HiveConfig(
                database='demo_fraud',
                table='transactions',
                timestamp_field='timestamp',
            ),
            owner='user@tecton.ai',
            tags={'release': 'staging'}
        )
    """

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        prevent_destroy: bool = False,
        batch_config: Optional[BatchConfigType] = None,
        stream_config: StreamConfigType,
        options: Optional[Dict[str, str]] = None,
        schema: Optional[List[types.Field]] = None,
    ):
        """Creates a new StreamSource.

        :param name: A unique name of the DataSource.
        :param description: A human-readable description.
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
            destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be
            set to False via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to prevent accidental changes
            such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
            triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton objects
            that would trigger a recreate of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
            that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
            only enforced in live (i.e. non-dev) workspaces.
        :param batch_config: BatchConfig object containing the configuration of the Batch Data Source that backs this
            Tecton Stream Source. This field is optional only if `stream_config` is a PushConfig.
        :param stream_config: StreamConfig object containing the configuration of the
            Stream Data Source that backs this Tecton Stream Source.
        :param options: Additional options to configure the Source. Used for advanced use cases and beta features.
        :param schema: A schema for the StreamSource. If not provided, the schema will be inferred from the underlying batch source.
            Right now, schemas can only be specified for StreamSources with a PushConfig, and that's also why the schema must be a list of Tecton types.
        """
        from tecton.cli import repo_utils as cli_common

        schema_container = (
            schema_container_pb2.SchemaContainer(tecton_schema=type_utils.to_tecton_schema(schema)) if schema else None
        )

        data_source_type: data_source_type_pb2.DataSourceType
        if isinstance(stream_config, configs.PushConfig):
            if batch_config:
                data_source_type = data_source_type_pb2.DataSourceType.PUSH_WITH_BATCH
            else:
                data_source_type = data_source_type_pb2.DataSourceType.PUSH_NO_BATCH
        else:
            assert batch_config is not None, f"batch_config must be provided for stream source {name}"
            data_source_type = data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH

        ds_args = virtual_data_source__args_pb2.VirtualDataSourceArgs(
            virtual_data_source_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            version=framework_version_pb2.FrameworkVersion.FWV5,
            type=data_source_type,
            prevent_destroy=prevent_destroy,
            options=options,
        )
        if schema_container:
            ds_args.schema.CopyFrom(schema_container)
        if batch_config:
            batch_config._merge_batch_args(ds_args)
        stream_config._merge_stream_args(ds_args)
        info = base_tecton_object.TectonObjectInfo.from_args_proto(ds_args.info, ds_args.virtual_data_source_id)
        source_info = cli_common.construct_fco_source_info(ds_args.virtual_data_source_id)

        self.__attrs_init__(
            info=info,
            spec=None,
            args=ds_args,
            source_info=source_info,
            args_supplement=_build_args_supplement(batch_config, stream_config),
        )

        base_tecton_object._register_local_object(self)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.DataSourceSpec) -> "StreamSource":
        """Create a StreamSource from directly from a spec. Specs are assumed valid and will not be re-validated."""
        info = base_tecton_object.TectonObjectInfo.from_spec(spec)
        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(
            info=info,
            spec=spec,
            args=None,
            source_info=None,
            args_supplement=None,
        )
        return obj

    def _derive_stream_schemas(self) -> None:
        if is_stream_ingest_data_source(self._args.type):
            if self._args.type == data_source_type_pb2.DataSourceType.PUSH_NO_BATCH:
                return
        else:
            self._args_supplement.stream_schema = spark_api.derive_stream_schema(
                self._args,
                self._args_supplement.stream_post_processor,
                self._args_supplement.stream_data_source_function,
            )

    def _derive_batch_schemas(self) -> None:
        batch_compute_mode = default_batch_compute_mode()
        if (
            batch_compute_mode == BatchComputeMode.RIFT
            or self._args.type == data_source_type_pb2.DataSourceType.PUSH_NO_BATCH
        ):
            # Tecton Batch only supports explicit FV schemas & doesn't require data source schema inference.
            # TODO(TEC-16975): Remove when DataSource schema evaluation is lazy
            self._args_supplement.batch_schema = spark_schema_pb2.SparkSchema()
            return
        elif batch_compute_mode == BatchComputeMode.SNOWFLAKE:
            # We can only hit this case for Stream Ingest On Snowflake
            self._args_supplement.batch_schema = snowflake_api.derive_batch_schema(self._args)
        elif batch_compute_mode == BatchComputeMode.SPARK:
            # Stream Ingest on Spark
            self._args_supplement.batch_schema = spark_api.derive_batch_schema(
                self._args, self._args_supplement.batch_post_processor, self._args_supplement.batch_data_source_function
            )

    def _derive_schemas(self, indentation_level: int) -> None:
        # Only two computes for Streaming, Stream Ingest and Spark.
        validations_api.print_deriving_schemas(self, indentation_level)
        self._derive_stream_schemas()
        self._derive_batch_schemas()

    @sdk_decorators.sdk_public_method(requires_validation=True)
    def start_stream_preview(
        self,
        table_name: str,
        *,
        apply_translator: bool = True,
        option_overrides: Optional[Dict[str, str]] = None,
        checkpoint_dir: Optional[str] = None,
    ) -> pyspark_streaming.StreamingQuery:
        """
        Starts a streaming job to write incoming records from this DS's stream to a temporary table with a given name.

        After records have been written to the table, they can be queried using ``spark.sql()``. If ran in a Databricks
        notebook, Databricks will also automatically visualize the number of incoming records.

        This is a testing method, most commonly used to verify a StreamDataSource is correctly receiving streaming events.
        Note that the table will grow infinitely large, so this is only really useful for debugging in notebooks.

        :param table_name: The name of the temporary table that this method will write to.
        :param apply_translator: Whether to apply this data source's ``raw_stream_translator``.
            When True, the translated data will be written to the table. When False, the
            raw, untranslated data will be written. ``apply_translator`` is not applicable to stream sources configured
            with ``spark_stream_config`` because it does not have a ``post_processor``.
        :param option_overrides: A dictionary of Spark readStream options that will override any readStream options set
            by the data source. Can be used to configure behavior only for the preview, e.g. setting
            ``startingOffsets:latest`` to preview only the most recent events in a Kafka stream.
        :param checkpoint_dir: A root directory that the streaming job will checkpoint to.
        """

        if is_stream_ingest_data_source(self._spec.type):
            msg = "Cannot preview stream ingest data sources"
            raise ValueError(msg)
        return spark_api.start_stream_preview(
            self._spec, table_name, apply_translator, option_overrides, checkpoint_dir
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def ingest(self, events: Union[Dict[str, Any], Sequence[Dict[str, Any]]], dry_run: bool = False) -> Dict[str, Any]:
        """Ingests a single event into the Tecton Online Ingest API.

        :param events: A list of dictionaries representing a sequence of events to be ingested. Also accepts a
            single dictionary.
        :param dry_run: If True, the ingest request will be validated, but the event will not be materialized.
            If False, the event will be materialized.
        """
        if not is_stream_ingest_data_source(self._spec.type):
            msg = "Can only ingest events for stream sources with push configs"
            raise ValueError(msg)
        if not self._spec:
            msg = "Cannot ingest events for a stream source that has not been applied"
            raise ValueError(msg)

        if isinstance(events, dict):
            events = [events]

        status_code, reason, response = IngestionClient().ingest(
            workspace_name=self._spec.workspace,
            push_source_name=self._spec.name,
            ingestion_records=events,
            dry_run=dry_run,
        )
        if status_code >= 500:
            raise errors.INTERNAL_ERROR(message=json.dumps(response))
        elif status_code >= 400:
            raise errors.INGESTAPI_USER_ERROR(
                status_code=status_code, reason=reason, error_message=json.dumps(response)
            )
        else:
            return response

    @sdk_decorators.sdk_public_method(requires_validation=True)
    def get_columns(self) -> List[str]:
        """Returns the column names of the data source's streaming schema."""
        if is_stream_ingest_data_source(self._spec.type):
            schema = self._spec.schema.tecton_schema
            return [column.name for column in schema.columns]

        # TODO(jiadong): Add public doc to explain the context of this error message and put the link in the msg.
        # Internal context: Optional Data Source schema derivation(https://www.notion.so/tecton/Optional-Data-Source-Schema-82e7ca00d2664f6890b526bcbac50688)
        if self._spec.stream_source.spark_schema is None:
            msg = "`get_columns()` is not supported for this Data Source. Tecton did not pre-derive its schema. Use `get_dataframe()` to get the schema of this data source, e.g. `ds.get_dataframe().to_spark().schema` or `ds.get_dataframe().to_pandas().dtypes`."
            raise ValueError(msg)

        schema = self._spec.stream_source.spark_schema
        return [field.name for field in schema.fields]


@attrs.define(eq=False)
class PushSource(StreamSource):
    """Deprecated. Use StreamSource with a PushConfig instead.
    A Tecton PushSource, used to configure the Tecton Online Ingest API for use in a StreamFeatureView.

    ``PushSource`` is currently in private preview, please contact Tecton support if you are interested in participating in the preview.

    A PushSource may also contain an optional batch config for backfilling and offline training data generation.

    Example of a PushSource declaration:

    .. code-block:: python

        from tecton import HiveConfig, PushSource, BatchSource
        from tecton.types import Field, Int64, String, Timestamp

        # Declare a schema for the Push Source
        input_schema = [
            Field(name='user_id', dtype=String),
            Field(name='event_timestamp', dtype=String),
            Field(name='clicked', dtype=Int64),
        ]

        # Declare a PushSource with a name, schema and a batch_config parameters
        # See the API documentation for BatchConfig
        click_event_source = PushSource(
                                name="click_event_source",
                                schema=input_schema,
                                batch_config=HiveConfig(
                                    database='demo_ads',
                                    table='impressions_batch',
                                ),
                                description="Sample Push Source for click events",
                                owner="pooja@tecton.ai",
                                tags={'release': 'staging'}
                                )
    """

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        prevent_destroy: bool = False,
        schema: List[types.Field],
        batch_config: Optional[BatchConfigType] = None,
        options: Optional[Dict[str, str]] = None,
    ):
        """Creates a new PushSource.

        :param name: A unique name of the DataSource.
        :param schema: A schema for the PushSource
        :param description: A human-readable description.
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
            destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be
            set to False via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to prevent accidental changes
            such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
            triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton objects
            that would trigger a recreate of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
            that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
            only enforced in live (i.e. non-dev) workspaces.
        :param batch_config: An optional BatchConfig object containing the configuration of the Batch Data Source that backs
            this Tecton Push Source. The Batch Source's schema must contain a super-set of all the columns defined in the Push Source schema.
        :param options: Additional options to configure the Source. Used for advanced use cases and beta features.
        """
        from tecton.cli import repo_utils as cli_common

        logger.warning("PushSource is deprecated. Please use StreamSource with a PushConfig instead")

        data_source_type = (
            data_source_type_pb2.DataSourceType.PUSH_WITH_BATCH
            if batch_config is not None
            else data_source_type_pb2.DataSourceType.PUSH_NO_BATCH
        )

        ds_args = virtual_data_source__args_pb2.VirtualDataSourceArgs(
            virtual_data_source_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            version=framework_version_pb2.FrameworkVersion.FWV5,
            type=data_source_type,
            prevent_destroy=prevent_destroy,
            schema=schema_container_pb2.SchemaContainer(tecton_schema=type_utils.to_tecton_schema(schema)),
            options=options,
        )
        if batch_config is not None:
            batch_config._merge_batch_args(ds_args)
        info = base_tecton_object.TectonObjectInfo.from_args_proto(ds_args.info, ds_args.virtual_data_source_id)
        source_info = cli_common.construct_fco_source_info(ds_args.virtual_data_source_id)

        self.__attrs_init__(
            info=info,
            spec=None,
            args=ds_args,
            source_info=source_info,
            args_supplement=_build_args_supplement(batch_config, None),
        )

        base_tecton_object._register_local_object(self)


def data_source_from_spec(data_source_spec: specs.DataSourceSpec):
    """Create a Data Source (of the correct type) from the provided spec."""
    if data_source_spec.type in (
        data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH,
        data_source_type_pb2.DataSourceType.PUSH_WITH_BATCH,
        data_source_type_pb2.DataSourceType.PUSH_NO_BATCH,
    ):
        return StreamSource._from_spec(data_source_spec)
    elif data_source_spec.type == data_source_type_pb2.DataSourceType.BATCH:
        return BatchSource._from_spec(data_source_spec)
    else:
        msg = f"Unexpected Data Source Type. Spec: {data_source_spec}"
        raise ValueError(msg)


def _build_args_supplement(
    batch_config: Optional[BatchConfigType], stream_config: Optional[StreamConfigType]
) -> specs.DataSourceSpecArgsSupplement:
    supplement = specs.DataSourceSpecArgsSupplement()
    if isinstance(
        batch_config,
        (
            configs.FileConfig,
            configs.HiveConfig,
            configs.RedshiftConfig,
            configs.SnowflakeConfig,
            configs.UnityConfig,
        ),
    ):
        supplement.batch_post_processor = batch_config.post_processor
    elif isinstance(batch_config, (configs.PandasBatchConfig, configs.SparkBatchConfig)):
        supplement.batch_data_source_function = batch_config.data_source_function
    elif batch_config is not None:
        msg = f"Unexpected batch_config type: {batch_config}"
        raise TypeError(msg)

    if isinstance(stream_config, (configs.KinesisConfig, configs.KafkaConfig)):
        supplement.stream_post_processor = stream_config.post_processor
    elif isinstance(stream_config, configs.SparkStreamConfig):
        supplement.stream_data_source_function = stream_config.data_source_function
    elif isinstance(stream_config, configs.PushConfig):
        pass
    elif stream_config is not None:
        msg = f"Unexpected stream_config type: {stream_config}"
        raise TypeError(msg)

    return supplement


def is_stream_ingest_data_source(data_source_type: data_source_type_pb2.DataSourceType) -> bool:
    return data_source_type in {
        data_source_type_pb2.DataSourceType.PUSH_WITH_BATCH,
        data_source_type_pb2.DataSourceType.PUSH_NO_BATCH,
    }
