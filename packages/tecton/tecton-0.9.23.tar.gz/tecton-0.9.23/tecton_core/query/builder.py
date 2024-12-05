from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

import pendulum

from tecton_core import conf
from tecton_core import errors
from tecton_core import feature_definition_wrapper
from tecton_core import specs
from tecton_core import time_utils
from tecton_core.compute_mode import ComputeMode
from tecton_core.embeddings.config import TextEmbeddingInferenceConfig
from tecton_core.embeddings.config import TextEmbeddingModel
from tecton_core.feature_set_config import FeatureDefinitionAndJoinConfig
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.feature_set_config import find_dependent_feature_set_items
from tecton_core.pipeline_common import get_time_window_from_data_source_node
from tecton_core.query import compaction_utils
from tecton_core.query.dialect import Dialect
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.node_interface import DataframeWrapper
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import AddAnchorTimeNode
from tecton_core.query.nodes import AddDurationNode
from tecton_core.query.nodes import AddEffectiveTimestampNode
from tecton_core.query.nodes import AddRetrievalAnchorTimeNode
from tecton_core.query.nodes import AddUniqueIdNode
from tecton_core.query.nodes import AggregationSecondaryKeyExplodeNode
from tecton_core.query.nodes import AggregationSecondaryKeyRollupNode
from tecton_core.query.nodes import AsofJoinFullAggNode
from tecton_core.query.nodes import AsofJoinInputContainer
from tecton_core.query.nodes import AsofJoinNode
from tecton_core.query.nodes import AsofSecondaryKeyExplodeNode
from tecton_core.query.nodes import ConvertEpochToTimestampNode
from tecton_core.query.nodes import ConvertTimestampToUTCNode
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import DeriveValidityPeriodNode
from tecton_core.query.nodes import ExplodeTimestampByTimeWindowsNode
from tecton_core.query.nodes import FeatureTimeFilterNode
from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import InnerJoinOnRangeNode
from tecton_core.query.nodes import JoinNode
from tecton_core.query.nodes import MetricsCollectorNode
from tecton_core.query.nodes import MultiOdfvPipelineNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import OnlinePartialAggNodeV2
from tecton_core.query.nodes import PartialAggNode
from tecton_core.query.nodes import PythonDataNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import RespectFeatureStartTimeNode
from tecton_core.query.nodes import RespectTTLNode
from tecton_core.query.nodes import SelectDistinctNode
from tecton_core.query.nodes import StagingNode
from tecton_core.query.nodes import StreamWatermarkNode
from tecton_core.query.nodes import TakeLastRowNode
from tecton_core.query.nodes import TemporalBatchTableFormatNode
from tecton_core.query.nodes import TextEmbeddingInferenceNode
from tecton_core.query.nodes import TrimValidityPeriodNode
from tecton_core.query.nodes import UserSpecifiedDataNode
from tecton_core.query.nodes import WildcardJoinNode
from tecton_core.query_consts import aggregation_group_id
from tecton_core.query_consts import anchor_time
from tecton_core.query_consts import default_case
from tecton_core.query_consts import effective_timestamp
from tecton_core.query_consts import exclusive_end_time
from tecton_core.query_consts import expiration_timestamp
from tecton_core.query_consts import inclusive_start_time
from tecton_core.query_consts import interval_end_time
from tecton_core.query_consts import interval_start_time
from tecton_core.query_consts import odfv_internal_staging_table
from tecton_core.query_consts import tecton_unique_id_col
from tecton_core.query_consts import timestamp_plus_ttl
from tecton_core.query_consts import udf_internal
from tecton_core.query_consts import window_end_column_name
from tecton_core.specs import DataSourceSpec
from tecton_proto.args.pipeline_pb2 import DataSourceNode as ProtoDataSourceNode
from tecton_proto.data import feature_view_pb2 as feature_view__data_pb2


def build_datasource_scan_node(
    dialect: Dialect,
    compute_mode: ComputeMode,
    ds: specs.DataSourceSpec,
    for_stream: bool,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> NodeRef:
    tree = DataSourceScanNode(
        dialect=dialect,
        compute_mode=compute_mode,
        ds=ds,
        ds_node=None,
        is_stream=for_stream,
        start_time=start_time,
        end_time=end_time,
    ).as_ref()
    return StagingNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=tree,
        staging_table_name=f"{ds.name}",
        query_tree_step=QueryTreeStep.DATA_SOURCE,
    ).as_ref()


def _get_ds_time_limits(
    feature_data_time_limits: Optional[pendulum.Period],
    schedule_interval: Optional[pendulum.Duration],
    data_source_node: ProtoDataSourceNode,
) -> Tuple[Optional[datetime], Optional[datetime]]:
    ds_time_limits = get_time_window_from_data_source_node(
        feature_data_time_limits, schedule_interval, data_source_node
    )
    if ds_time_limits:
        return ds_time_limits.start, ds_time_limits.end
    return None, None


def _build_datasource_input_querynodes(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    for_stream: bool,
    feature_data_time_limits: Optional[pendulum.Period] = None,
) -> Dict[str, NodeRef]:
    """
    Starting in FWV5, data sources of FVs with incremental backfills may contain transformations that are only
    correct if the data has been filtered to a specific range.
    """
    schedule_interval = fdw.get_tile_interval if fdw.is_temporal else None
    ds_inputs = feature_definition_wrapper.pipeline_to_ds_inputs(fdw.pipeline)

    input_querynodes = {}
    for input_name, node in ds_inputs.items():
        start_time, end_time = _get_ds_time_limits(feature_data_time_limits, schedule_interval, node)
        ds = fdw.fco_container.get_by_id_proto(node.virtual_data_source_id)
        assert isinstance(ds, DataSourceSpec)
        tree = DataSourceScanNode(
            dialect=dialect,
            compute_mode=compute_mode,
            ds=ds,
            ds_node=node,
            is_stream=for_stream,
            start_time=start_time,
            end_time=end_time,
        ).as_ref()
        input_querynodes[input_name] = StagingNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=tree,
            staging_table_name=f"{ds.name}",
            query_tree_step=QueryTreeStep.DATA_SOURCE,
        ).as_ref()
    return input_querynodes


def _get_stream_watermark(fdw: feature_definition_wrapper.FeatureDefinitionWrapper) -> Optional[str]:
    ds_inputs = feature_definition_wrapper.pipeline_to_ds_inputs(fdw.pipeline)
    for input_name, node in ds_inputs.items():
        ds_spec = fdw.fco_container.get_by_id_proto(node.virtual_data_source_id)
        assert isinstance(ds_spec, DataSourceSpec)
        if ds_spec.stream_source is not None:
            watermark_delay_threshold_seconds = ds_spec.stream_source.watermark_delay_threshold.total_seconds()
            # NOTE: we do not want to set an explicit '0 seconds' watermark as
            # that can lead to data loss (data source functions supports
            # user-specified watermark configuration in function).
            if watermark_delay_threshold_seconds:
                return f"{watermark_delay_threshold_seconds} seconds"
    return None


# build QueryTree that executes all transformations
def build_pipeline_querytree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    for_stream: bool,
    feature_data_time_limits: Optional[pendulum.Period] = None,
) -> NodeRef:
    inputs_map = _build_datasource_input_querynodes(dialect, compute_mode, fdw, for_stream, feature_data_time_limits)
    base = FeatureViewPipelineNode(
        dialect=dialect,
        compute_mode=compute_mode,
        inputs_map=inputs_map,
        feature_definition_wrapper=fdw,
        feature_time_limits=feature_data_time_limits,
        check_view_schema=fdw.has_explicit_view_schema,
    ).as_ref()
    base = ConvertTimestampToUTCNode.for_feature_definition(
        dialect=dialect,
        compute_mode=compute_mode,
        fd=fdw,
        input_node=base,
    )

    if feature_data_time_limits:
        return FeatureTimeFilterNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=base,
            feature_data_time_limits=feature_data_time_limits,
            policy=fdw.time_range_policy,
            start_timestamp_field=fdw.timestamp_key,
            end_timestamp_field=fdw.timestamp_key,
        ).as_ref()
    return base


def build_snowflake_materialization_querytree(
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    feature_data_time_limits: Optional[pendulum.Period] = None,
) -> NodeRef:
    materialization_node = build_materialization_querytree(
        dialect=Dialect.SNOWFLAKE,
        compute_mode=ComputeMode.SNOWFLAKE,
        fdw=fdw,
        for_stream=False,
        feature_data_time_limits=feature_data_time_limits,
        use_timestamp_key=True,
    )
    return materialization_node


def build_materialization_querytree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    for_stream: bool,
    feature_data_time_limits: Optional[pendulum.Period] = None,
    include_window_end_time: bool = False,
    aggregation_anchor_time: Optional[datetime] = None,
    enable_feature_metrics: bool = False,
    use_timestamp_key: bool = False,
) -> NodeRef:
    """Builds a querytree to construct a dataframe for materialization.

    For example, WAFVs are partially aggregated, and BFVs are augmented with an anchor time column. The resulting
    dataframe can also be easily modified to be used for `fv.run`.

    Args:
        dialect: The SQL dialect
        compute_mode: Current compute mode
        fdw: The feature view to be materialized.
        for_stream: If True, the underlying data source is a streaming source.
        feature_data_time_limits: If set, the resulting features will be filtered with respect to these time limits.
        include_window_end_time: If True, a tile end time column with name "tile_end_time" will be included for WAFVs.
            Should only be set for WAFVs.
        aggregation_anchor_time: If set, it will be used as the offset for aggregations. Should only be set for WAFVs.
        enable_feature_metrics: If True, metrics will be collected on the querytree.
        use_timestamp_key: If True, the timestamp key will be used instead of _ANCHOR_TIME. This is used for Snowflake Compute only.
    """
    assert not for_stream or feature_data_time_limits is None, "Cannot run with time limits on a stream source"
    tree = build_pipeline_querytree(dialect, compute_mode, fdw, for_stream, feature_data_time_limits)
    if for_stream:
        watermark = _get_stream_watermark(fdw)
        if watermark:
            tree = StreamWatermarkNode(dialect, compute_mode, tree, fdw.time_key, watermark).as_ref()
    if enable_feature_metrics:
        tree = MetricsCollectorNode(dialect, compute_mode, tree).as_ref()

    if fdw.compaction_enabled and not for_stream:
        return _build_compaction_materialization_querytree(
            dialect=dialect,
            compute_mode=compute_mode,
            fdw=fdw,
            pipeline_tree=tree,
        )

    anchor_time_field = anchor_time()
    if fdw.is_temporal:
        tree = StagingNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=tree,
            staging_table_name=f"{fdw.name}",
            query_tree_step=QueryTreeStep.PIPELINE,
        ).as_ref()

        if "DEV_EMBEDDINGS_INPUT_COLUMNS" in fdw.fv_spec.options:
            tree = _add_text_embedding_inference_node(fdw=fdw, compute_mode=compute_mode, pipeline_tree=tree)

        # BFVs require an anchor time column, but SFVs do not.
        if not for_stream:
            assert not include_window_end_time, "Not supported window end time for temporal"
            if not use_timestamp_key:
                tree = AddAnchorTimeNode.for_feature_definition(dialect, compute_mode, fdw, tree)
    elif fdw.is_temporal_aggregate:
        end_column_name = window_end_column_name() if include_window_end_time else None
        tree = StagingNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=tree,
            staging_table_name=f"{fdw.name}",
            query_tree_step=QueryTreeStep.PIPELINE,
        ).as_ref()
        tree = PartialAggNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=tree,
            fdw=fdw,
            window_start_column_name=anchor_time_field,
            window_end_column_name=end_column_name,
            aggregation_anchor_time=aggregation_anchor_time,
        ).as_ref()
        if use_timestamp_key:
            tree = ConvertEpochToTimestampNode(
                dialect, compute_mode, tree, {anchor_time(): fdw.get_feature_store_format_version}
            ).as_ref()
            tree = RenameColsNode(
                dialect, compute_mode, input_node=tree, mapping={anchor_time(): fdw.time_key}
            ).as_ref()
    else:
        msg = "unexpected FV type"
        raise Exception(msg)
    return tree


def _add_text_embedding_inference_node(
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper, compute_mode: ComputeMode, pipeline_tree: NodeRef
) -> NodeRef:
    if compute_mode != ComputeMode.RIFT:
        msg = "text embeddings are only supported on Rift"
        raise ValueError(msg)

    input_columns = fdw.fv_spec.options["DEV_EMBEDDINGS_INPUT_COLUMNS"].split(",")

    qt_node = TextEmbeddingInferenceNode(
        dialect=Dialect.TORCH,
        compute_mode=ComputeMode.RIFT,
        input_node=pipeline_tree,
        inference_configs=tuple(
            TextEmbeddingInferenceConfig(
                input_column=col, output_column=f"{col}_embedding", model=TextEmbeddingModel.ALL_MINILM_L6_V2
            )
            for col in input_columns
        ),
    )

    staging_node = StagingNode(
        dialect=Dialect.DUCKDB,
        compute_mode=ComputeMode.RIFT,
        input_node=qt_node.as_ref(),
        staging_table_name="model_inference",
        query_tree_step=QueryTreeStep.MODEL_INFERENCE,
    )
    return staging_node.as_ref()


def _build_compaction_materialization_querytree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    pipeline_tree: NodeRef,
) -> NodeRef:
    # Offline materialization query for fvs with compaction_enabled=True
    tree = StagingNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=pipeline_tree,
        staging_table_name=f"{fdw.name}",
        query_tree_step=QueryTreeStep.PIPELINE,
    ).as_ref()
    tree = ConvertTimestampToUTCNode.for_feature_definition(
        dialect=dialect, compute_mode=compute_mode, fd=fdw, input_node=tree
    )
    return AddAnchorTimeNode.for_feature_definition(dialect, compute_mode, fdw, tree)


def build_get_partial_aggregates_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    from_source: Optional[bool],
    limits: pendulum.Period,
    entities: Optional[DataframeWrapper],
) -> NodeRef:
    qt = build_get_features(
        dialect=dialect,
        compute_mode=compute_mode,
        fdw=fdw,
        from_source=from_source,
        feature_data_time_limits=limits,
        include_window_end_time=True,
    )

    rename_mapping = {
        anchor_time(): interval_start_time(),
        window_end_column_name(): interval_end_time(),
    }

    qt = RenameColsNode(dialect, compute_mode, qt, mapping=rename_mapping).as_ref()

    qt = ConvertEpochToTimestampNode(
        dialect,
        compute_mode,
        qt,
        {
            interval_start_time(): fdw.get_feature_store_format_version,
            interval_end_time(): fdw.get_feature_store_format_version,
        },
    ).as_ref()

    if entities is not None:
        qt = _filter_entity_dataframe(dialect, compute_mode, qt, entities)

    return qt


def build_get_features(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    from_source: Optional[bool],
    feature_data_time_limits: Optional[pendulum.Period] = None,
    aggregation_anchor_time: Optional[datetime] = None,
    include_window_end_time: Optional[bool] = False,
) -> NodeRef:
    # NOTE: this is ideally the *only* place where we validate
    # from_source arguments. However, until Snowflake and Athena are migrated
    # to QueryTree, we also need validations to live in the interactive/unified
    # SDK.
    #
    # Behavior:
    #   from_source is True: force compute from source
    #   from_source is False: force compute from materialized data
    #   from_source is None: compute from materialized data if feature
    #       definition offline=True, otherwise compute from source
    if from_source is None:
        from_source = not fdw.materialization_enabled or not fdw.writes_to_offline_store

    if from_source is False:
        assert not aggregation_anchor_time, "aggregation anchor time is not allowed when fetching features from source"
        if not fdw.materialization_enabled or not fdw.writes_to_offline_store:
            raise errors.FV_NEEDS_TO_BE_MATERIALIZED(fdw.name)
        tree = OfflineStoreScanNode(
            dialect=dialect,
            compute_mode=compute_mode,
            feature_definition_wrapper=fdw,
            partition_time_filter=feature_data_time_limits,
        ).as_ref()
    else:
        if dialect == "athena":
            msg = "When Athena compute is enabled, features can only be read from the offline store. Please set from_source = False"
            raise errors.TectonAthenaValidationError(msg)
        # TODO(TEC-13005)
        # TODO(pooja): raise an appropriate error here for push source
        if fdw.is_incremental_backfill:
            raise errors.FV_BFC_SINGLE_FROM_SOURCE

        tree = build_materialization_querytree(
            dialect,
            compute_mode,
            fdw,
            for_stream=False,
            feature_data_time_limits=feature_data_time_limits,
            aggregation_anchor_time=aggregation_anchor_time,
            include_window_end_time=include_window_end_time,
        )

    if fdw.compaction_enabled and fdw.is_temporal_aggregate:
        end_column_name = window_end_column_name() if include_window_end_time else None
        tree = PartialAggNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=tree,
            fdw=fdw,
            window_start_column_name=anchor_time(),
            window_end_column_name=end_column_name,
            aggregation_anchor_time=aggregation_anchor_time,
            create_tiles=fdw.get_tile_interval_seconds_for_offline_store > 0,
        ).as_ref()

    return tree


def build_temporal_time_range_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fd: feature_definition_wrapper.FeatureDefinitionWrapper,
    from_source: Optional[bool],
    query_time_range: pendulum.Period,
    entities: Optional[DataframeWrapper],
) -> NodeRef:
    qt = build_get_features(
        dialect=dialect,
        compute_mode=compute_mode,
        fdw=fd,
        from_source=from_source,
        feature_data_time_limits=query_time_range,
    )
    qt = RenameColsNode(dialect, compute_mode, qt, drop=[anchor_time()]).as_ref()
    batch_schedule_seconds = 0 if fd.is_feature_table else fd.batch_materialization_schedule.in_seconds()

    qt = AddEffectiveTimestampNode(
        dialect,
        compute_mode,
        qt,
        timestamp_field=fd.timestamp_key,
        effective_timestamp_name=effective_timestamp(),
        batch_schedule_seconds=batch_schedule_seconds,
        data_delay_seconds=fd.online_store_data_delay_seconds,
        is_stream=fd.is_stream,
        is_temporal_aggregate=False,
    ).as_ref()

    if entities is not None:
        qt = _filter_entity_dataframe(dialect, compute_mode, qt, entities)

    qt = _filter_by_time_range(dialect, compute_mode, qt, query_time_range, fd.timestamp_key, fd.timestamp_key)
    return qt


def build_temporal_time_range_validity_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fd: feature_definition_wrapper.FeatureDefinitionWrapper,
    from_source: Optional[bool],
    query_time_range: pendulum.Period,
    lookback_time_range: pendulum.Period,
    entities: Optional[DataframeWrapper],
) -> NodeRef:
    qt = build_get_features(
        dialect=dialect,
        compute_mode=compute_mode,
        fdw=fd,
        from_source=from_source,
        feature_data_time_limits=lookback_time_range,
    )
    qt = RenameColsNode(dialect, compute_mode, qt, drop=[anchor_time()]).as_ref()
    batch_schedule_seconds = 0 if fd.is_feature_table else fd.batch_materialization_schedule.in_seconds()

    qt = AddEffectiveTimestampNode(
        dialect,
        compute_mode,
        qt,
        timestamp_field=fd.timestamp_key,
        effective_timestamp_name=effective_timestamp(),
        batch_schedule_seconds=batch_schedule_seconds,
        data_delay_seconds=fd.online_store_data_delay_seconds,
        is_stream=fd.is_stream,
        is_temporal_aggregate=False,
    ).as_ref()

    qt = TakeLastRowNode(
        dialect,
        compute_mode,
        input_node=qt,
        partition_by_columns=(*fd.join_keys, effective_timestamp()),
        order_by_column=fd.timestamp_key,
    ).as_ref()

    qt = DeriveValidityPeriodNode(dialect, compute_mode, qt, fd, effective_timestamp()).as_ref()

    if entities is not None:
        qt = _filter_entity_dataframe(dialect, compute_mode, qt, entities)

    qt = TrimValidityPeriodNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=qt,
        start=query_time_range.start,
        end=query_time_range.end,
    ).as_ref()

    return qt


def build_aggregated_time_range_validity_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    from_source: Optional[bool],
    # query_time_range is the validated time range passed in the query
    query_time_range: pendulum.Period,
    # feature_data_time_limits is the aligned time range after taking the spine and aggregations into account
    feature_data_time_limits: pendulum.Period,
    entities: Optional[DataframeWrapper],
) -> NodeRef:
    partial_aggs = build_get_features(
        dialect,
        compute_mode,
        fdw,
        from_source,
        feature_data_time_limits=feature_data_time_limits,
    )

    if entities is not None:
        partial_aggs = _filter_entity_dataframe(dialect, compute_mode, partial_aggs, entities)

    spine = _build_internal_spine(
        dialect, compute_mode, fdw, partial_aggs, query_time_range=query_time_range, explode_anchor_time=True
    )

    full_aggregation_node = AsofJoinFullAggNode(
        dialect=dialect,
        compute_mode=compute_mode,
        spine=spine,
        partial_agg_node=partial_aggs,
        fdw=fdw,
        # Do not push down the timestamp if the spine is completely from partial agg, such as `ghf` and `run` with time
        # range.
        enable_spine_time_pushdown_rewrite=False,
        enable_spine_entity_pushdown_rewrite=False,
    ).as_ref()

    if fdw.aggregation_secondary_key:
        full_aggregation_node = AggregationSecondaryKeyRollupNode(
            dialect=dialect,
            compute_mode=compute_mode,
            full_aggregation_node=full_aggregation_node,
            fdw=fdw,
            group_by_columns=[*list(fdw.join_keys), anchor_time()],
        ).as_ref()

    qt = _filter_and_update_timestamp_columns(
        full_aggregation_node,
        dialect,
        compute_mode,
        fdw,
        show_effective_time=True,
    )

    qt = TakeLastRowNode(
        dialect,
        compute_mode,
        input_node=qt,
        partition_by_columns=(*fdw.join_keys, effective_timestamp()),
        order_by_column=fdw.timestamp_key,
    ).as_ref()

    qt = DeriveValidityPeriodNode(dialect, compute_mode, qt, fdw, effective_timestamp()).as_ref()

    qt = TrimValidityPeriodNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=qt,
        start=query_time_range.start,
        end=query_time_range.end,
    ).as_ref()

    return qt


def build_aggregated_time_range_ghf_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    from_source: Optional[bool],
    feature_data_time_limits: pendulum.Period,
    query_time_range: pendulum.Period,
    entities: Optional[DataframeWrapper] = None,
) -> NodeRef:
    partial_aggs = build_get_features(
        dialect,
        compute_mode,
        fdw,
        from_source,
        feature_data_time_limits=feature_data_time_limits,
    )
    spine = _build_internal_spine(dialect, compute_mode, fdw, partial_aggs)

    # TODO(danny): Don't represent the partial_agg node twice (in the spine + in the agg node)
    #  When this QT is compiled to SQL, the partial agg node is doubly represented and executed.
    full_aggregation_node = AsofJoinFullAggNode(
        dialect=dialect,
        compute_mode=compute_mode,
        spine=spine,
        partial_agg_node=partial_aggs,
        fdw=fdw,
        # Do not push down the timestamp if the spine is completely from partial agg, such as `ghf` and `run` with time
        # range.
        enable_spine_time_pushdown_rewrite=False,
        enable_spine_entity_pushdown_rewrite=False,
    ).as_ref()

    if fdw.aggregation_secondary_key:
        full_aggregation_node = AggregationSecondaryKeyRollupNode(
            dialect=dialect,
            compute_mode=compute_mode,
            full_aggregation_node=full_aggregation_node,
            fdw=fdw,
            group_by_columns=[*list(fdw.join_keys), anchor_time()],
        ).as_ref()

    qt = _filter_and_update_timestamp_columns(
        full_aggregation_node,
        dialect,
        compute_mode,
        fdw,
        respect_feature_start_time=True,
        show_effective_time=True,
    )

    if entities is not None:
        qt = _filter_entity_dataframe(dialect, compute_mode, qt, entities)

    qt = _filter_by_time_range(dialect, compute_mode, qt, query_time_range, fdw.timestamp_key, fdw.timestamp_key)

    return qt


def build_aggregated_time_range_run_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    feature_data_time_limits: pendulum.Period,
    aggregation_anchor_time: Optional[datetime] = None,
) -> NodeRef:
    partial_aggs = build_get_features(
        dialect,
        compute_mode,
        fdw,
        from_source=True,
        feature_data_time_limits=feature_data_time_limits,
        aggregation_anchor_time=aggregation_anchor_time,
    )
    spine = _build_internal_spine(dialect, compute_mode, fdw, partial_aggs)

    # TODO(danny): Don't represent the partial_agg node twice (in the spine + in the agg node)
    #  When this QT is compiled to SQL, the partial agg node is doubly represented and executed.
    full_aggregation_node = AsofJoinFullAggNode(
        dialect=dialect,
        compute_mode=compute_mode,
        spine=spine,
        partial_agg_node=partial_aggs,
        fdw=fdw,
        # Do not push down the timestamp if the spine is completely from partial agg, such as `ghf` and `run` with time
        # range.
        enable_spine_time_pushdown_rewrite=False,
        enable_spine_entity_pushdown_rewrite=False,
    ).as_ref()

    if fdw.aggregation_secondary_key:
        full_aggregation_node = AggregationSecondaryKeyRollupNode(
            dialect=dialect,
            compute_mode=compute_mode,
            full_aggregation_node=full_aggregation_node,
            fdw=fdw,
            group_by_columns=[*list(fdw.join_keys), anchor_time()],
        ).as_ref()
    qt = _filter_and_update_timestamp_columns(
        full_aggregation_node,
        dialect,
        compute_mode,
        fdw,
        respect_feature_start_time=False,
        show_effective_time=False,
    )

    return qt


def _filter_by_time_range(
    dialect: Dialect,
    compute_mode: ComputeMode,
    qt: NodeRef,
    time_range: pendulum.Period,
    start_timestamp_field: str,
    end_timestamp_field: str,
) -> NodeRef:
    qt = FeatureTimeFilterNode(
        dialect,
        compute_mode,
        qt,
        feature_data_time_limits=time_range,
        policy=feature_view__data_pb2.MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FILTER_TO_RANGE,
        start_timestamp_field=start_timestamp_field,
        end_timestamp_field=end_timestamp_field,
    ).as_ref()

    return qt


def _filter_entity_dataframe(
    dialect: Dialect,
    compute_mode: ComputeMode,
    qt: NodeRef,
    entities: Optional[DataframeWrapper],
) -> NodeRef:
    columns = list(entities.columns)
    entities_df = SelectDistinctNode(
        dialect, compute_mode, UserSpecifiedDataNode(dialect, compute_mode, entities).as_ref(), columns
    ).as_ref()
    qt = JoinNode(dialect, compute_mode, qt, entities_df, columns, how="right").as_ref()
    return qt


def _filter_and_update_timestamp_columns(
    full_aggregation_node: NodeRef,
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    respect_feature_start_time: bool = True,
    show_effective_time: bool = False,
) -> NodeRef:
    """
    1. Filters rows by Feature Start Time
    2. Converts the anchor time to a timestamp from epoch ns.
    3. Adjusts the anchor time to reflect the end of the materialization window
    4. Optionally adds the _effective_time column
    """

    if respect_feature_start_time and fdw.feature_start_timestamp:
        full_aggregation_node = RespectFeatureStartTimeNode.for_anchor_time_column(
            dialect,
            compute_mode,
            full_aggregation_node,
            anchor_time(),
            fdw,
        ).as_ref()

    # The `AsofJoinFullAggNode` returned by `build_get_full_agg_features` converts timestamps to epochs. We convert back
    # from epochs to timestamps so that we can add an effective timestamp column.
    qt = ConvertEpochToTimestampNode(
        dialect, compute_mode, full_aggregation_node, {anchor_time(): fdw.get_feature_store_format_version}
    ).as_ref()

    # We want the time to be on the end of the window not the start.
    qt = AddDurationNode(
        dialect,
        compute_mode,
        qt,
        timestamp_field=anchor_time(),
        duration=fdw.get_tile_interval_duration_for_offline_store,
        new_column_name=fdw.trailing_time_window_aggregation.time_key,
    ).as_ref()
    qt = RenameColsNode(dialect, compute_mode, qt, drop=[anchor_time()]).as_ref()

    if show_effective_time:
        batch_schedule_seconds = 0 if fdw.is_feature_table else fdw.batch_materialization_schedule.in_seconds()
        qt = AddEffectiveTimestampNode(
            dialect,
            compute_mode,
            qt,
            timestamp_field=fdw.trailing_time_window_aggregation.time_key,
            effective_timestamp_name=effective_timestamp(),
            batch_schedule_seconds=batch_schedule_seconds,
            data_delay_seconds=fdw.online_store_data_delay_seconds,
            is_stream=fdw.is_stream,
            is_temporal_aggregate=True,
        ).as_ref()

    return qt


def _build_internal_spine(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    partial_aggs: NodeRef,
    explode_anchor_time: Optional[bool] = False,
    query_time_range: Optional[pendulum.Period] = None,
) -> NodeRef:
    if fdw.aggregation_secondary_key:
        cols_to_drop = list(
            set(partial_aggs.columns) - {*list(fdw.join_keys), anchor_time(), fdw.aggregation_secondary_key}
        )
    else:
        cols_to_drop = list(set(partial_aggs.columns) - {*list(fdw.join_keys), anchor_time()})

    spine = RenameColsNode(dialect, compute_mode, partial_aggs, drop=cols_to_drop).as_ref()

    # TODO (ajeya): remove flag after GHF is deprecated
    if explode_anchor_time:
        earliest_valid_anchor_time = time_utils.get_nearest_anchor_time(
            timestamp=query_time_range.start,
            max_source_data_delay=fdw.max_source_data_delay,
            batch_materialization_schedule=fdw.batch_materialization_schedule,
            min_scheduling_interval=fdw.min_scheduling_interval,
        )
        spine_filter = pendulum.Period(earliest_valid_anchor_time, query_time_range.end)
        spine = ExplodeTimestampByTimeWindowsNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=spine,
            timestamp_field=anchor_time(),
            time_filter=spine_filter,
            fdw=fdw,
        ).as_ref()

    if fdw.aggregation_secondary_key:
        spine = AggregationSecondaryKeyExplodeNode.for_feature_definition(
            dialect=dialect, compute_mode=compute_mode, spine=spine, fdw=fdw
        )

    return spine


def build_spine_join_querytree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    dac: FeatureDefinitionAndJoinConfig,
    spine_node: NodeRef,
    spine_time_field: str,
    from_source: Optional[bool],
    use_namespace_feature_prefix: bool = True,
) -> NodeRef:
    fdw = dac.feature_definition
    if fdw.timestamp_key is not None and spine_time_field != fdw.timestamp_key:
        spine_node = RenameColsNode(
            dialect, compute_mode, spine_node, mapping={spine_time_field: fdw.timestamp_key}
        ).as_ref()
    if any(jk[0] != jk[1] for jk in dac.join_keys):
        spine_node = RenameColsNode(
            dialect, compute_mode, spine_node, mapping={jk[0]: jk[1] for jk in dac.join_keys if jk[0] != jk[1]}
        ).as_ref()
    if fdw.is_temporal or fdw.is_feature_table:
        ret = _build_spine_query_tree_temporal_or_feature_table(
            dialect=dialect,
            compute_mode=compute_mode,
            spine_node=spine_node,
            dac=dac,
            data_delay_seconds=fdw.online_store_data_delay_seconds,
            from_source=from_source,
            use_namespace_feature_prefix=use_namespace_feature_prefix,
        )
    elif fdw.is_temporal_aggregate:
        partial_agg_node = build_get_features(
            dialect,
            compute_mode,
            fdw,
            from_source=from_source,
            # NOTE: feature_data_time_limits is set to None since time pushdown
            # should happen as part of a optimization rewrite.
            feature_data_time_limits=None,
            aggregation_anchor_time=None,
        )

        augmented_spine = _augment_spine_for_window_aggregation(
            dialect,
            compute_mode,
            fdw,
            spine_node,
            partial_agg_node,
        )

        full_agg_node = AsofJoinFullAggNode(
            dialect=dialect,
            compute_mode=compute_mode,
            spine=augmented_spine,
            partial_agg_node=partial_agg_node,
            fdw=fdw,
            # Allow timestamp push down if the spine is provided by users.
            enable_spine_time_pushdown_rewrite=True,
            enable_spine_entity_pushdown_rewrite=True,
        ).as_ref()

        if fdw.aggregation_secondary_key:
            full_agg_node = AggregationSecondaryKeyRollupNode(
                dialect=dialect,
                compute_mode=compute_mode,
                full_aggregation_node=full_agg_node,
                fdw=fdw,
                # Beside join keys and anchor time, we need to group by timestamp_key and TECTON_UNIQUE_ID_COL because:
                #   1. Grouping by timestamp_key is required to keep the timestamp column in the result.
                #   2. Grouping by TECTON_UNIQUE_ID_COL can distinguish duplicated rows in the spine.
                group_by_columns=[*list(fdw.join_keys), anchor_time(), fdw.timestamp_key, tecton_unique_id_col()],
            ).as_ref()
            full_agg_node = RenameColsNode(dialect, compute_mode, full_agg_node, drop=[tecton_unique_id_col()]).as_ref()

        if fdw.feature_start_timestamp:
            full_agg_node = RespectFeatureStartTimeNode.for_anchor_time_column(
                dialect,
                compute_mode,
                full_agg_node,
                anchor_time(),
                fdw,
            ).as_ref()
        ret = _rename_feature_columns_and_drop_non_feature_columns(
            dialect, compute_mode, dac, full_agg_node, use_namespace_feature_prefix
        )
    elif fdw.is_on_demand:
        inputs = find_dependent_feature_set_items(
            fdw.fco_container,
            fdw.pipeline.root,
            visited_inputs={},
            fv_id=fdw.id,
        )
        dac = FeatureDefinitionAndJoinConfig.from_feature_definition(fdw)
        fsc = FeatureSetConfig([*inputs, dac])
        ret = build_feature_set_config_querytree(
            dialect, compute_mode, fsc, spine_node, spine_time_field, from_source, use_namespace_feature_prefix
        )
    else:
        raise NotImplementedError
    if fdw.timestamp_key is not None and spine_time_field != fdw.timestamp_key:
        ret = RenameColsNode(dialect, compute_mode, ret, {fdw.timestamp_key: spine_time_field}).as_ref()
    if any(jk[0] != jk[1] for jk in dac.join_keys):
        ret = RenameColsNode(
            dialect, compute_mode, ret, {jk[1]: jk[0] for jk in dac.join_keys if jk[0] != jk[1]}
        ).as_ref()
    return ret


def _update_internal_cols(
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    dac: FeatureDefinitionAndJoinConfig,
    internal_cols: Set[str],
) -> None:
    if dac.namespace.startswith(udf_internal()):
        for feature in fdw.features:
            internal_cols.add(dac.namespace + fdw.namespace_separator + feature)
    for feature in dac.features:
        if udf_internal() in feature:
            internal_cols.add(feature)


# Construct each wildcard materialized fvtree by joining against distinct set of join keys.
# Then, outer join these using WildcardJoinNode which performs an outer join while handling null-valued features properly.
def _build_wild_fv_subtree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    spine_node: NodeRef,
    fv_dacs: List[FeatureDefinitionAndJoinConfig],
    spine_time_field: str,
    from_source: Optional[bool],
) -> NodeRef:
    newtree = None
    for dac in fv_dacs:
        fdw = dac.feature_definition

        subspine_join_keys = [jk[0] for jk in dac.join_keys if jk[0] != fdw.wildcard_join_key]
        # SelectDistinctNode is needed for correctness in order to filter out rows with duplicate join keys before
        # retrieving feature values. This avoids exploding wildcard rows when there are duplicates in both the spine and the
        # feature view tree.
        subspine = SelectDistinctNode(
            dialect, compute_mode, spine_node, [*subspine_join_keys, spine_time_field]
        ).as_ref()
        fvtree = build_spine_join_querytree(dialect, compute_mode, dac, subspine, spine_time_field, from_source)
        if len(dac.features) < len(fdw.features):
            fvtree = RenameColsNode(
                dialect,
                compute_mode,
                fvtree,
                drop=[f"{fdw.name}{fdw.namespace_separator}{f}" for f in fdw.features if f not in dac.features],
            ).as_ref()
        if newtree is None:
            newtree = fvtree
        else:
            join_cols = [*subspine_join_keys, spine_time_field, fdw.wildcard_join_key]
            newtree = WildcardJoinNode(dialect, compute_mode, newtree, fvtree, join_cols=join_cols).as_ref()
    return newtree


# Construct each non-wildcard materialized fvtree by joining against distinct set of join keys.
# Then, outer join these fvtrees together.
def _build_standard_fv_subtree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    spine_node: NodeRef,
    fv_dacs: List[FeatureDefinitionAndJoinConfig],
    spine_time_field: str,
    from_source: Optional[bool],
) -> Tuple[NodeRef, Set[str]]:
    newtree = spine_node
    internal_cols: Set[str] = set()
    for dac in fv_dacs:
        fdw = dac.feature_definition
        _update_internal_cols(fdw, dac, internal_cols)

        subspine_join_keys = [jk[0] for jk in dac.join_keys]
        # SelectDistinctNode is needed for correctness in the case that there are duplicate rows in the spine. The
        # alternative considered was to add a row_id as a hash of the row or a monotonically increasing id, however the
        # row_id as a hash is not unique for duplicate rows and a monotonically increasing id is non-deterministic.
        subspine = SelectDistinctNode(
            dialect, compute_mode, spine_node, [*subspine_join_keys, spine_time_field]
        ).as_ref()
        fvtree = build_spine_join_querytree(dialect, compute_mode, dac, subspine, spine_time_field, from_source)
        if len(dac.features) < len(fdw.features):
            fvtree = RenameColsNode(
                dialect,
                compute_mode,
                fvtree,
                drop=[f"{fdw.name}{fdw.namespace_separator}{f}" for f in fdw.features if f not in dac.features],
            ).as_ref()
        allow_null_features = conf.get_bool("ALLOW_NULL_FEATURES")
        newtree = JoinNode(
            dialect,
            compute_mode,
            newtree,
            fvtree,
            how="inner",
            join_cols=[*subspine_join_keys, spine_time_field],
            allow_nulls=allow_null_features,
        ).as_ref()
    return newtree, internal_cols


# Compute odfvs via udf on the parent (not using joins)
def _build_odfv_subtree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    parent_tree: NodeRef,
    odfv_dacs: List[FeatureDefinitionAndJoinConfig],
    use_namespace_feature_prefix: bool = True,
) -> NodeRef:
    newtree = StagingNode(
        dialect=dialect,
        compute_mode=compute_mode,
        input_node=parent_tree,
        staging_table_name=odfv_internal_staging_table(),
        query_tree_step=QueryTreeStep.AGGREGATION,
    ).as_ref()
    feature_definitions_namespaces = [(dac.feature_definition, dac.namespace) for dac in odfv_dacs]
    newtree = MultiOdfvPipelineNode(
        dialect, compute_mode, newtree, feature_definitions_namespaces, use_namespace_feature_prefix
    ).as_ref()

    # Compute the union of the features to be computed
    dac_features = set()
    fdw_features = set()
    for dac in odfv_dacs:
        feature_prefix = f"{dac.namespace}{dac.feature_definition.namespace_separator}"
        dac_features.update({f"{feature_prefix}{f}" for f in dac.features})
        fdw_features.update({f"{feature_prefix}{f}" for f in dac.feature_definition.features})

    # Drop features if user queried a subset via feature services
    if len(dac_features) < len(fdw_features):
        newtree = RenameColsNode(
            dialect,
            compute_mode,
            newtree,
            drop=[namespaced_feat for namespaced_feat in fdw_features if namespaced_feat not in dac_features],
        ).as_ref()
    return newtree


# Construct each materialized fvtree by joining against distinct set of join keys.
# Then, join the full spine against each of those.
# Finally, compute odfvs via udf on top of the result (not using joins)
def build_feature_set_config_querytree(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fsc: FeatureSetConfig,
    spine_node: NodeRef,
    spine_time_field: str,
    from_source: Optional[bool],
    use_namespace_feature_prefix: bool = True,
) -> NodeRef:
    odfv_dacs: List[FeatureDefinitionAndJoinConfig] = []
    wildcard_dacs: List[FeatureDefinitionAndJoinConfig] = []
    normal_fv_dacs: List[FeatureDefinitionAndJoinConfig] = []

    for dac in fsc.definitions_and_configs:
        if dac.feature_definition.is_on_demand:
            odfv_dacs.append(dac)
        elif dac.feature_definition.wildcard_join_key is not None:
            if dac.feature_definition.wildcard_join_key in spine_node.columns:
                # Despite this being a wildcard FV, since we have the wildcard
                # key in the spine we will treat it like a normal FV.
                normal_fv_dacs.append(dac)
            else:
                wildcard_dacs.append(dac)
        else:
            normal_fv_dacs.append(dac)

    if wildcard_dacs:
        newtree = _build_wild_fv_subtree(
            dialect, compute_mode, spine_node, wildcard_dacs, spine_time_field, from_source
        )
    else:
        newtree = spine_node

    internal_cols: Set[str] = set()
    if normal_fv_dacs:
        newtree, internal_cols = _build_standard_fv_subtree(
            dialect, compute_mode, newtree, normal_fv_dacs, spine_time_field, from_source
        )

    if odfv_dacs:
        newtree = _build_odfv_subtree(dialect, compute_mode, newtree, odfv_dacs, use_namespace_feature_prefix)

    # drop all internal cols
    if len(internal_cols) > 0:
        newtree = RenameColsNode(dialect, compute_mode, newtree, drop=list(internal_cols)).as_ref()

    return newtree


def _build_spine_query_tree_temporal_or_feature_table(
    dialect: Dialect,
    compute_mode: ComputeMode,
    spine_node: NodeRef,
    dac: FeatureDefinitionAndJoinConfig,
    data_delay_seconds: int,
    from_source: Optional[bool],
    use_namespace_feature_prefix: bool = True,
) -> NodeRef:
    fdw = dac.feature_definition
    base = build_get_features(dialect, compute_mode, fdw, from_source=from_source)
    batch_schedule_seconds = 0 if fdw.is_feature_table else fdw.batch_materialization_schedule.in_seconds()
    base = AddEffectiveTimestampNode(
        dialect,
        compute_mode,
        base,
        timestamp_field=fdw.timestamp_key,
        effective_timestamp_name=effective_timestamp(),
        batch_schedule_seconds=batch_schedule_seconds,
        data_delay_seconds=data_delay_seconds,
        is_stream=fdw.is_stream,
        is_temporal_aggregate=False,
    ).as_ref()
    if fdw.serving_ttl is not None:
        base = AddDurationNode(
            dialect,
            compute_mode,
            base,
            timestamp_field=fdw.timestamp_key,
            duration=fdw.serving_ttl,
            new_column_name=timestamp_plus_ttl(),
        ).as_ref()
        # Calculate effective expiration time = window(feature_time + ttl, batch_schedule).end + data_delay
        batch_schedule_seconds = 0 if fdw.is_feature_table else fdw.batch_materialization_schedule.in_seconds()
        base = AddEffectiveTimestampNode(
            dialect,
            compute_mode,
            base,
            timestamp_field=timestamp_plus_ttl(),
            effective_timestamp_name=expiration_timestamp(),
            batch_schedule_seconds=batch_schedule_seconds,
            data_delay_seconds=data_delay_seconds,
            is_stream=fdw.is_stream,
            is_temporal_aggregate=False,
        ).as_ref()
    rightside_join_prefix = default_case("_tecton_right")
    join_prefixed_feature_names = [f"{rightside_join_prefix}_{f}" for f in fdw.features]
    prefix = f"{dac.namespace}{fdw.namespace_separator}" if use_namespace_feature_prefix else ""
    # we can't just ask for the correct right_prefix to begin with because the asofJoin always sticks an extra underscore in between
    rename_map: Dict[str, Optional[str]] = {}
    cols_to_drop = []
    for f in fdw.features:
        if f not in dac.features:
            cols_to_drop.append(f"{rightside_join_prefix}_{f}")
        else:
            rename_map[f"{rightside_join_prefix}_{f}"] = f"{prefix}{f}"

    expiration_timestamp_col = f"{rightside_join_prefix}_{expiration_timestamp()}"

    cols_to_drop.append(f"{rightside_join_prefix}_{fdw.timestamp_key}")
    cols_to_drop.append(f"{rightside_join_prefix}_{anchor_time()}")
    cols_to_drop.append(f"{rightside_join_prefix}_{effective_timestamp()}")
    if fdw.serving_ttl is not None:
        cols_to_drop.append(f"{rightside_join_prefix}_{timestamp_plus_ttl()}")
        cols_to_drop.append(expiration_timestamp_col)

    if fdw.feature_start_timestamp is not None:
        base = RespectFeatureStartTimeNode(
            dialect,
            compute_mode,
            base,
            fdw.timestamp_key,
            fdw.feature_start_timestamp,
            fdw.features,
            fdw.get_feature_store_format_version,
        ).as_ref()

    if fdw.wildcard_join_key is not None and fdw.wildcard_join_key not in spine_node.columns:
        # Need to copy base so that the left and right side are separate
        base_copy = base.deepcopy()
        spine_node = AsofSecondaryKeyExplodeNode(
            dialect, compute_mode, spine_node, fdw.timestamp_key, base_copy, effective_timestamp(), fdw
        ).as_ref()

    base = AsofJoinNode(
        dialect=dialect,
        compute_mode=compute_mode,
        left_container=AsofJoinInputContainer(spine_node, fdw.timestamp_key),
        right_container=AsofJoinInputContainer(
            base,
            timestamp_field=fdw.timestamp_key,
            effective_timestamp_field=effective_timestamp(),
            prefix=rightside_join_prefix,
            schema=fdw.view_schema,
        ),
        join_cols=fdw.join_keys,
    ).as_ref()

    if fdw.serving_ttl is not None:
        base = RespectTTLNode(
            dialect, compute_mode, base, fdw.timestamp_key, expiration_timestamp_col, join_prefixed_feature_names
        ).as_ref()
    # remove anchor cols/dupe timestamp cols
    return RenameColsNode(dialect, compute_mode, base, mapping=rename_map, drop=cols_to_drop).as_ref()


def _augment_spine_for_window_aggregation(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    spine_node: NodeRef,
    partial_agg_node: NodeRef,
) -> NodeRef:
    augmented_spine = AddRetrievalAnchorTimeNode(
        dialect,
        compute_mode,
        spine_node,
        name=fdw.name,
        feature_store_format_version=fdw.get_feature_store_format_version,
        batch_schedule=fdw.get_batch_schedule_for_version,
        tile_interval=fdw.get_tile_interval_seconds_for_offline_store,
        timestamp_field=fdw.timestamp_key,
        is_stream=fdw.is_stream,
        data_delay_seconds=fdw.online_store_data_delay_seconds,
    ).as_ref()

    # We need to explode the spine for the secondary key if:
    #     1. A Feature View with an aggregation_secondary_key: an aggregation_secondary_key is never in the spine,
    #     so we always need to explode the spine for it.
    #     2. A Feature View with a wild card join key: a wild card join key is optional in the spine, so we need to
    #     check if the wild card join key is not in the spine before exploding the spine for it.
    is_wildcard_join_key_not_in_spine = fdw.wildcard_join_key and fdw.wildcard_join_key not in spine_node.columns
    is_secondary_key_agg = fdw.aggregation_secondary_key is not None
    if is_wildcard_join_key_not_in_spine or is_secondary_key_agg:
        # Add a unique id column if aggreagtion secondary key appears. The unique id column is used to make each spine
        # row unique so later the secondary key aggregation rollup doesn't merge duplicate rows.
        if is_secondary_key_agg:
            augmented_spine = AddUniqueIdNode(dialect, compute_mode, augmented_spine).as_ref()

        return AsofSecondaryKeyExplodeNode(
            dialect,
            compute_mode,
            augmented_spine,
            anchor_time(),
            partial_agg_node,
            anchor_time(),
            fdw,
        ).as_ref()

    return augmented_spine


def _rename_feature_columns_and_drop_non_feature_columns(
    dialect: Dialect,
    compute_mode: ComputeMode,
    dac: FeatureDefinitionAndJoinConfig,
    node: NodeRef,
    use_namespace_feature_prefix: bool = True,
) -> NodeRef:
    rename_map: Dict[str, Optional[str]] = {}
    cols_to_drop = [anchor_time()]
    for f in dac.feature_definition.features:
        if f not in dac.features:
            cols_to_drop.append(f)
        elif use_namespace_feature_prefix:
            # TODO: make a helper
            rename_map[f] = f"{dac.namespace}{dac.feature_definition.namespace_separator}{f}"
    return RenameColsNode(dialect, compute_mode, node, mapping=rename_map, drop=cols_to_drop).as_ref()


def _build_aggregation_group_data_node(
    dialect: Dialect, compute_mode: ComputeMode, aggregation_groups: Tuple[compaction_utils.AggregationGroup, ...]
) -> PythonDataNode:
    columns = (aggregation_group_id(), inclusive_start_time(), exclusive_end_time())
    data = tuple(
        (group.window_index, group.inclusive_start_time, group.exclusive_end_time) for group in aggregation_groups
    )
    return PythonDataNode(dialect, compute_mode, data=data, columns=columns)


def build_compaction_query(
    dialect: Dialect,
    compute_mode: ComputeMode,
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    compaction_job_end_time: datetime,
    enable_from_source_for_test: bool = False,
) -> NodeRef:
    """Build compaction query for online materialization jobs. Only used for fvs with batch compaction enabled.

    enable_from_source_for_test=True should only be used in local integration tests!"""
    feature_data_time_limits = compaction_utils.get_data_time_limits_for_compaction(
        fdw=fdw, compaction_job_end_time=compaction_job_end_time
    )
    if enable_from_source_for_test:
        # Only used for local testing
        base_node = build_pipeline_querytree(
            dialect, compute_mode, fdw, for_stream=False, feature_data_time_limits=feature_data_time_limits
        )
    else:
        base_node = OfflineStoreScanNode(
            dialect=dialect,
            compute_mode=compute_mode,
            feature_definition_wrapper=fdw,
            partition_time_filter=feature_data_time_limits,
        ).as_ref()
        if feature_data_time_limits:
            base_node = FeatureTimeFilterNode(
                dialect=dialect,
                compute_mode=compute_mode,
                input_node=base_node,
                feature_data_time_limits=feature_data_time_limits,
                policy=fdw.time_range_policy,
                start_timestamp_field=fdw.timestamp_key,
                end_timestamp_field=fdw.timestamp_key,
            ).as_ref()

    if fdw.is_temporal_aggregate:
        aggregation_groups = compaction_utils.aggregation_groups(fdw, compaction_job_end_time)
        compaction_ranges = _build_aggregation_group_data_node(dialect, compute_mode, aggregation_groups).as_ref()
        node = InnerJoinOnRangeNode(
            dialect=dialect,
            compute_mode=compute_mode,
            left=base_node,
            right=compaction_ranges,
            left_join_condition_column=fdw.timestamp_key,
            right_inclusive_start_column=inclusive_start_time(),
            right_exclusive_end_column=exclusive_end_time(),
        ).as_ref()
        node = OnlinePartialAggNodeV2(
            dialect,
            compute_mode,
            node,
            fdw=fdw,
            aggregation_groups=aggregation_groups,
        ).as_ref()
        return node
    elif fdw.is_temporal:
        node = TakeLastRowNode.for_feature_definition(
            dialect=dialect, compute_mode=compute_mode, fdw=fdw, input_node=base_node
        )
        node = TemporalBatchTableFormatNode.for_feature_definition(
            dialect=dialect, compute_mode=compute_mode, fdw=fdw, input_node=node
        )
        return node

    msg = "Unexpected FV type."
    raise Exception(msg)
