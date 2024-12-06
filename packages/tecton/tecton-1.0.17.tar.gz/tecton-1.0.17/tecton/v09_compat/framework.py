import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import attrs
from typeguard import typechecked

from tecton import FeatureMetadata
from tecton import FeatureReference
from tecton import types
from tecton._internals import type_utils
from tecton.framework import base_tecton_object
from tecton.framework import configs
from tecton.framework import data_source as framework_data_source
from tecton.framework import entity as framework_entity
from tecton.framework import repo_config
from tecton.framework import utils
from tecton.framework.configs import PushConfig
from tecton.framework.data_source import BatchConfigType
from tecton.framework.data_source import BatchSource as BatchSource_v1_0
from tecton.framework.data_source import DataSource as DataSource_v1_0
from tecton.framework.data_source import FilteredSource
from tecton.framework.data_source import StreamSource as StreamSource_v1_0
from tecton.framework.entity import Entity as Entity_v1_0
from tecton.framework.feature_service import FeatureService as FeatureService_v1_0
from tecton.framework.feature_view import PIPELINE_MODE
from tecton.framework.feature_view import AggregationLeadingEdge
from tecton.framework.feature_view import BatchFeatureView as BatchFeatureView_v1_0
from tecton.framework.feature_view import BatchTriggerType
from tecton.framework.feature_view import FeatureTable as FeatureTable_v1_0
from tecton.framework.feature_view import FeatureView
from tecton.framework.feature_view import RealtimeFeatureView as RealtimeFeatureView_v1_0
from tecton.framework.feature_view import StreamFeatureView as StreamFeatureView_v1_0
from tecton.framework.feature_view import StreamProcessingMode
from tecton.framework.feature_view import infer_batch_compute_mode
from tecton.framework.transformation import Transformation as Transformation_v1_0
from tecton_core import conf
from tecton_core import feature_definition_wrapper
from tecton_core import id_helper
from tecton_core import specs
from tecton_core import time_utils
from tecton_core.compute_mode import BatchComputeMode
from tecton_core.data_types import UnknownType
from tecton_core.errors import TectonValidationError
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_proto.args import basic_info__client_pb2 as basic_info_pb2
from tecton_proto.args import entity__client_pb2 as entity__args_pb2
from tecton_proto.args import feature_view__client_pb2 as feature_view__args_pb2
from tecton_proto.common import schema__client_pb2 as schema_pb2
from tecton_spark import spark_schema_wrapper


class Entity(Entity_v1_0):
    """A Tecton Entity, used to organize and join features.

    An Entity is a class that represents an Entity that is being modeled in Tecton. Entities are used to index and
    organize features - a :class:`FeatureView` contains at least one Entity.

    Entities contain metadata about *join keys*, which represent the columns that are used to join features together.

    Example of an Entity declaration:

    .. code-block:: python

        from tecton import Entity

        customer = Entity(
            name='customer',
            join_keys=['customer_id'],
            description='A customer subscribing to a Sports TV subscription service',
            owner='matt@tecton.ai',
            tags={'release': 'development'}
    """

    _framework_version = FrameworkVersion.FWV5

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        prevent_destroy: bool = False,
        join_keys: Optional[Union[str, List[str]]] = None,
        options: Optional[Dict[str, str]] = None,
    ):
        """Declare a new Entity.

        :param name: Unique name for the new entity.
        :param description: Short description of the new entity.
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
        :param join_keys: Names of columns that uniquely identify the entity in FeatureView's SQL statement
            for which features should be aggregated. Defaults to using ``name`` as the entity's join key.
        :param options: Additional options to configure the Entity. Used for advanced use cases and beta features.

        :raises TectonValidationError: if the input non-parameters are invalid.
        """
        from tecton_core.repo_file_handler import construct_fco_source_info

        if not join_keys:
            resolved_join_keys = schema_pb2.Column(name=name, offline_data_type=UnknownType().proto)
        elif isinstance(join_keys, str):
            resolved_join_keys = [schema_pb2.Column(name=join_keys, offline_data_type=UnknownType().proto)]
        else:
            resolved_join_keys = [
                schema_pb2.Column(name=join_key, offline_data_type=UnknownType().proto) for join_key in join_keys
            ]

        args = entity__args_pb2.EntityArgs(
            entity_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            join_keys=resolved_join_keys,
            version=feature_definition_wrapper.FrameworkVersion.FWV5.value,
            prevent_destroy=prevent_destroy,
            options=options,
        )
        info = base_tecton_object.TectonObjectInfo.from_args_proto(args.info, args.entity_id)
        source_info = construct_fco_source_info(args.entity_id)
        self.__attrs_init__(info=info, spec=None, args=args, source_info=source_info)

        # Note! This is 1.0 behavior required by validation on creation
        if not conf.get_bool("TECTON_SKIP_OBJECT_VALIDATION"):
            self._validate()
        self._spec = specs.EntitySpec.from_args_proto(self._args)
        base_tecton_object._register_local_object(self)


def _get_or_create_pipeline_function(
    name: str,
    mode: str,
    description: Optional[str],
    owner: Optional[str],
    tags: Optional[Dict[str, str]],
    feature_view_function,
):
    """Helper method for creating the pipeline function from args"""
    if mode == PIPELINE_MODE:
        pipeline_function = feature_view_function
    else:
        # Use transformation from v09_compat (this file)
        inferred_transform = transformation(mode, name, description, owner, tags=tags)(feature_view_function)

        def pipeline_function(**kwargs):
            return inferred_transform(**kwargs)

    return pipeline_function


class OnDemandFeatureView(RealtimeFeatureView_v1_0):
    # TODO(FE-2269): Move deprecated function implementations to v09 objects
    _framework_version = FrameworkVersion.FWV5

    # override this function to ensure transformation associated with feature view gets the right framework version set
    @staticmethod
    def _get_or_create_pipeline_function(
        name: str,
        mode: str,
        description: Optional[str],
        owner: Optional[str],
        tags: Optional[Dict[str, str]],
        feature_view_function,
    ):
        return _get_or_create_pipeline_function(
            name=name,
            mode=mode,
            description=description,
            owner=owner,
            tags=tags,
            feature_view_function=feature_view_function,
        )

    def feature_metadata(self) -> List[FeatureMetadata]:
        msg = "v09_compat feature views do not support feature metadata"
        raise NotImplementedError(msg)


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
            # Tecton 1.0 parameters.
            features=None,
            context_parameter_name=None,
        )

    return decorator


@typechecked
def batch_feature_view(
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    prevent_destroy: bool = False,
    mode: str,
    sources: Sequence[Union[framework_data_source.BatchSource, FilteredSource]],
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

        from tecton.v09_compat import batch_feature_view, Aggregation, FilteredSource

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

        from tecton.v09_compat import batch_feature_view, Aggregation, FilteredSource

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
            features=None,
        )

    return decorator


class BatchFeatureView(BatchFeatureView_v1_0):
    _framework_version = FrameworkVersion.FWV5

    # override this function to ensure transformation associated with feature view gets the right framework version set
    @staticmethod
    def _get_or_create_pipeline_function(
        name: str,
        mode: str,
        description: Optional[str],
        owner: Optional[str],
        tags: Optional[Dict[str, str]],
        feature_view_function,
    ):
        return _get_or_create_pipeline_function(
            name=name,
            mode=mode,
            description=description,
            owner=owner,
            tags=tags,
            feature_view_function=feature_view_function,
        )

    def feature_metadata(self) -> List[FeatureMetadata]:
        msg = "v09_compat feature views do not support feature metadata"
        raise NotImplementedError(msg)

    def _convert_data_sources_to_explicitly_filtered_objects(
        self,
        sources: Sequence[
            Union[
                framework_data_source.DataSource,
                FilteredSource,
                configs.RequestSource,
                FeatureView,
                FeatureReference,
            ]
        ],
    ) -> Sequence[Union[FilteredSource]]:
        new_sources = []
        for source in sources:
            # Invalid data sources for a materialized FV
            if isinstance(source, (FeatureReference, FeatureView, configs.RequestSource)):
                err = f"Unexpected source type {source.__class__} for Materialized Feature View"
                raise RuntimeError(err)
            elif isinstance(source, framework_data_source.DataSource):
                # Non-Filtered-Source Data Sources are always unfiltered in 0.9
                new_sources.append(source.unfiltered())
            else:
                new_sources.append(source)
        return new_sources


@typechecked
def stream_feature_view(
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    prevent_destroy: bool = False,
    source: Union[framework_data_source.StreamSource, FilteredSource],
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
            aggregation_leading_edge=AggregationLeadingEdge.LATEST_EVENT_TIME,  # new default for v09_compat objects
        )

    return decorator


class StreamFeatureView(StreamFeatureView_v1_0):
    _framework_version = FrameworkVersion.FWV5

    def feature_metadata(self) -> List[FeatureMetadata]:
        msg = "v09_compat feature views do not support feature metadata"
        raise NotImplementedError(msg)

    # override this function to ensure transformation associated with feature view gets the right framework version set
    @staticmethod
    def _get_or_create_pipeline_function(
        name: str,
        mode: str,
        description: Optional[str],
        owner: Optional[str],
        tags: Optional[Dict[str, str]],
        feature_view_function,
    ):
        return _get_or_create_pipeline_function(
            name=name,
            mode=mode,
            description=description,
            owner=owner,
            tags=tags,
            feature_view_function=feature_view_function,
        )

    def _convert_data_sources_to_explicitly_filtered_objects(
        self,
        sources: Sequence[
            Union[
                framework_data_source.DataSource,
                FilteredSource,
                configs.RequestSource,
                FeatureView,
                FeatureReference,
            ]
        ],
    ) -> Sequence[Union[FilteredSource]]:
        new_sources = []
        for source in sources:
            # Invalid data sources for a materialized FV
            if isinstance(source, (FeatureReference, FeatureView, configs.RequestSource)):
                err = f"Unexpected source type {source.__class__} for Materialized Feature View"
                raise RuntimeError(err)
            elif isinstance(source, framework_data_source.DataSource):
                # Non-Filtered-Source Data Sources are always unfiltered in 0.9
                new_sources.append(source.unfiltered())
            else:
                new_sources.append(source)
        return new_sources


@attrs.define(eq=False)
class FeatureTable(FeatureTable_v1_0):
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

    _framework_version = FrameworkVersion.FWV5

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
        from tecton_core.repo_file_handler import construct_fco_source_info

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
        source_info = construct_fco_source_info(args.feature_view_id)
        self.__attrs_init__(
            info=info,
            feature_definition=None,
            args=args,
            source_info=source_info,
            entities=tuple(entities),
            args_supplement=None,
        )

        # Note! This is 1.0 behavior required by validation on creation
        schemas = self._get_schemas()
        self._args_supplement = self._get_args_supplement(schemas)
        if not conf.get_bool("TECTON_SKIP_OBJECT_VALIDATION"):
            self._validate()
        self._populate_spec()
        base_tecton_object._register_local_object(self)

    def feature_metadata(self) -> List[FeatureMetadata]:
        msg = "v09_compat feature views do not support feature metadata"
        raise NotImplementedError(msg)


class DataSource(DataSource_v1_0):
    _framework_version = FrameworkVersion.FWV5


class BatchSource(BatchSource_v1_0):
    _framework_version = FrameworkVersion.FWV5


class StreamSource(StreamSource_v1_0):
    _framework_version = FrameworkVersion.FWV5


class Transformation(Transformation_v1_0):
    _framework_version = FrameworkVersion.FWV5


@typechecked
def transformation(
    mode: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    prevent_destroy: bool = False,
    options: Optional[Dict[str, str]] = None,
):
    """Declares a Transformation that wraps a user function. Transformations are assembled in a pipeline function of a Feature View.

    :param mode: The mode for this transformation must be one of "spark_sql", "pyspark", "snowflake_sql", "snowpark", "pandas" or "python".
    :param name: Unique, human friendly name that identifies the Transformation. Defaults to the function name.
    :param description: A human readable description.
    :param owner: Owner name (typically the email of the primary maintainer).
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
        destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be set to
        False via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to prevent accidental changes
        such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
        triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton objects
        that would trigger a recreate of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
        that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
        only enforced in live (i.e. non-dev) workspaces.
    :param options: Additional options to configure the Transformation. Used for advanced use cases and beta features.
    :return: A wrapped transformation

    Examples of Spark SQL, PySpark, Pandas, and Python transformation declarations:

        .. code-block:: python

            from tecton import transformation
            from pyspark.sql import DataFrame
            import pandas as pd

            # Create a Spark SQL transformation.
            @transformation(mode="spark_sql",
                            description="Create new column by splitting the string in an existing column")
            def str_split(input_data, column_to_split, new_column_name, delimiter):
                return f'''
                    SELECT
                        *,
                        split({column_to_split}, {delimiter}) AS {new_column_name}
                    FROM {input_data}
                '''

            # Create a PySpark transformation.
            @transformation(mode="pyspark",
                            description="Add a new column 'user_has_good_credit' if score is > 670")
            def user_has_good_credit_transformation(credit_scores):
                from pyspark.sql import functions as F

                (df = credit_scores.withColumn("user_has_good_credit",
                    F.when(credit_scores["credit_score"] > 670, 1).otherwise(0))
                return df.select("user_id", df["date"].alias("timestamp"), "user_has_good_credit") )

            # Create a Pandas transformation.
            @transformation(mode="pandas",
                            description="Whether the transaction amount is considered high (over $10000)")
            def transaction_amount_is_high(transaction_request):
                import pandas as pd

                df = pd.DataFrame()
                df['amount_is_high'] = (request['amount'] >= 10000).astype('int64')
                return df

            @transformation(mode="python",
                            description="Whether the transaction amount is considered high (over $10000)")
            # Create a Python transformation.
            def transaction_amount_is_high(transaction_request):

                result = {}
                result['transaction_amount_is_high'] = int(transaction_request['amount'] >= 10000)
                return result
    """

    def decorator(user_function):
        transform_name = name or user_function.__name__
        transform = Transformation(
            name=transform_name,
            description=description,
            owner=owner,
            tags=tags,
            prevent_destroy=prevent_destroy,
            mode=mode,
            user_function=user_function,
            options=options,
        )

        return transform

    return decorator


class FeatureService(FeatureService_v1_0):
    _framework_version = FrameworkVersion.FWV5

    def feature_metadata(self) -> List[FeatureMetadata]:
        msg = "v09_compat feature views do not support feature metadata"
        raise NotImplementedError(msg)


class PushSource(StreamSource):
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
        super().__init__(
            name=name,
            description=description,
            tags=tags,
            owner=owner,
            prevent_destroy=prevent_destroy,
            batch_config=batch_config,
            stream_config=PushConfig(),
            options=options,
            schema=schema,
        )
