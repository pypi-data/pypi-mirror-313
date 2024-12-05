from typing import Dict
from typing import List
from typing import Optional

import attrs
import pendulum

from tecton._internals import errors
from tecton._internals import time_utils
from tecton._internals.data_frame_helper import get_time_limits_of_dataframe
from tecton._internals.utils import get_time_limits_of_pandas_dataframe
from tecton_core import conf
from tecton_core.compute_mode import ComputeMode
from tecton_core.pipeline_common import get_time_window_from_data_source_node
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import QueryNode
from tecton_core.query.node_utils import get_first_input_node_of_class
from tecton_core.query.nodes import AddAnchorTimeNode
from tecton_core.query.nodes import AddDurationNode
from tecton_core.query.nodes import AddEffectiveTimestampNode
from tecton_core.query.nodes import AsofJoinFullAggNode
from tecton_core.query.nodes import AsofJoinNode
from tecton_core.query.nodes import ConvertTimestampToUTCNode
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import EntityFilterNode
from tecton_core.query.nodes import FeatureTimeFilterNode
from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import MockDataSourceScanNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import PartialAggNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import RespectFeatureStartTimeNode
from tecton_core.query.nodes import SelectDistinctNode
from tecton_core.query.nodes import StagingNode
from tecton_core.query.nodes import TextEmbeddingInferenceNode
from tecton_core.query.nodes import UserSpecifiedDataNode
from tecton_core.query.rewrite import Rewrite


class MockDataRewrite(Rewrite):
    """
    Replace DataSourceScanNode with MockDataSourceScanNode based on DataSource ID map.
    """

    def __init__(self, mock_data: Dict[str, NodeRef]):
        self.mock_data = mock_data

    def rewrite(self, tree: NodeRef):
        if isinstance(tree.node, DataSourceScanNode):
            node = tree.node
            if node.ds.id in self.mock_data:
                # Replace with mock data
                tree.node = MockDataSourceScanNode(
                    node.dialect,
                    node.compute_mode,
                    self.mock_data[node.ds.id],
                    node.ds,
                    self.mock_data[node.ds.id].columns,
                    node.start_time,
                    node.end_time,
                )
        else:
            for i in tree.inputs:
                self.rewrite(i)


class SpineEntityPushdown(Rewrite):
    """Filters the original feature data with respect to the entities contained in a spine.

    This should be applied to AsofJoinNodes and AsofJoinFullAggNodes since both of have sorts (as part of windows), for
    which we would like to minimize memory usage.
    """

    def __init__(self):
        pass

    def rewrite(self, tree: NodeRef):
        if isinstance(tree.node, AsofJoinNode):
            self.rewrite_asof(tree)
        elif isinstance(tree.node, AsofJoinFullAggNode):
            self.rewrite_asof_full_agg(tree)
        else:
            for i in tree.inputs:
                self.rewrite(i)

    def rewrite_asof(self, tree: NodeRef):
        node = tree.node
        # In our current usage of AsofJoinNode, we always pass in the spine on the left.
        spine_df = node.left_container.node.deepcopy()
        self.pushdown_entities(node.right_container.node, spine_df, node.join_cols)

    def rewrite_asof_full_agg(self, tree: NodeRef):
        node = tree.node

        if not node.enable_spine_entity_pushdown_rewrite:
            return

        user_provided_spine_node_ref = get_first_input_node_of_class(node.spine, UserSpecifiedDataNode).as_ref()

        # Note: we can't simply using join keys to pushdown entity because wildcard FV can have a spine missing wildcard
        # key, so we need to check what exact entities are used in spine if wildcard key is present, and only push those
        # entities down.
        entities_to_push_down = node.fdw.join_keys
        if node.fdw.wildcard_join_key and node.fdw.wildcard_join_key not in user_provided_spine_node_ref.columns:
            entities_to_push_down = set(entities_to_push_down) - {node.fdw.wildcard_join_key}

        # entity_rewritable ensures there is a UserSpecifiedDataNode in the spine.
        self.pushdown_entities(
            node.partial_agg_node, user_provided_spine_node_ref.deepcopy(), list(entities_to_push_down)
        )

    def pushdown_entities(self, tree: NodeRef, spine: NodeRef, join_cols: List[str]):
        node = tree.node
        can_be_pushed_down = (
            RespectFeatureStartTimeNode,
            RenameColsNode,
            FeatureTimeFilterNode,
            AddAnchorTimeNode,
            AddDurationNode,
            AddEffectiveTimestampNode,
            PartialAggNode,
            StagingNode,
            ConvertTimestampToUTCNode,
            TextEmbeddingInferenceNode,
        )
        if isinstance(node, can_be_pushed_down):
            self.pushdown_entities(node.input_node, spine, join_cols)
        else:
            entities_node = SelectDistinctNode(node.dialect, node.compute_mode, spine, join_cols).as_ref()
            tree.node = EntityFilterNode(node.dialect, node.compute_mode, node.as_ref(), entities_node, join_cols)


class SpineTimePushdown(Rewrite):
    """
    Adds time filter ranges based on the time limits of the spine.

    For example, if the spine in a fv.ghf() has time range [start, end], then the rewrite might apply that time range
    as a filter to any FeatureViewPipelineNodes, OfflineStoreScanNodes, or DataSourceScanNodes that are part of the
    feature data (with the appropriate modifications to the time range to account for factors such as batch schedule,
    data delay, etc.).
    """

    def __init__(self):
        # The spine time limits are the same for all spines used throughout the query, so we only calculate once.
        self.spine_time_limits: Optional[pendulum.Period] = None

    def rewrite(self, tree: NodeRef):
        if isinstance(tree.node, AsofJoinNode):
            self.rewrite_asof(tree)
        elif isinstance(tree.node, AsofJoinFullAggNode):
            self.rewrite_asof_full_agg(tree)
        else:
            for i in tree.inputs:
                self.rewrite(i)

    def rewrite_asof(self, tree: NodeRef):
        node = tree.node
        # In our current usage of the code, we always pass in the spine on the left side of the asof join.
        # This rewrite is still applicable for any type of dataframe on the left, but referring to it as spine
        # to make the naming match up with the aggregate case (in which the spine is not on the left).
        if self.spine_time_limits is None:
            cur_node = node.left_container.node.node
            self.spine_time_limits = _get_spine_time_limits(cur_node)

        self.pushdown_time_range(node.right_container.node, self.spine_time_limits)

    def rewrite_asof_full_agg(self, tree: NodeRef):
        """Computes the spine time limits and pushes them down to all relevant nodes in the partial aggregates."""
        node = tree.node

        if not node.enable_spine_time_pushdown_rewrite:
            return

        if self.spine_time_limits is None:
            self.spine_time_limits = _get_spine_time_limits(node)
        self.pushdown_time_range(node.partial_agg_node, self.spine_time_limits)

    # Push down and convert spine time filter to either raw data or feature time filter at the DataSourceScanNode or OfflineStoreScanNode.
    # Nodes that do not affect the correlation with the spine time range are enumerated in the can_be_pushed_down list.
    def pushdown_time_range(self, tree: NodeRef, spine_time_limits: pendulum.Period):
        node = tree.node
        can_be_pushed_down = (
            RespectFeatureStartTimeNode,
            RenameColsNode,
            PartialAggNode,
            FeatureTimeFilterNode,
            AddAnchorTimeNode,
            AddDurationNode,
            AddEffectiveTimestampNode,
            StagingNode,
            ConvertTimestampToUTCNode,
        )
        if isinstance(node, can_be_pushed_down):
            self.pushdown_time_range(node.input_node, spine_time_limits)
        elif isinstance(node, (OfflineStoreScanNode, FeatureViewPipelineNode)):
            feature_time_limits = time_utils.get_feature_data_time_limits(
                fd=node.feature_definition_wrapper, spine_time_limits=spine_time_limits
            )
            if isinstance(node, FeatureViewPipelineNode):
                # swap the pipeline node to add new time limits
                node = FeatureViewPipelineNode(
                    node.dialect,
                    node.compute_mode,
                    node.inputs_map,
                    node.feature_definition_wrapper,
                    feature_time_limits,
                    node.check_view_schema,
                )

                for n in node.inputs:
                    data_source_scan_node_ref = get_first_input_node_of_class(n, DataSourceScanNode, as_node_ref=True)
                    if data_source_scan_node_ref is None:
                        continue
                    data_source_scan_node = data_source_scan_node_ref.node
                    if data_source_scan_node is not None:
                        # this method will convert aligned_feature_time_limits to raw data time limits by accounting for FilteredSource offsets etc.
                        data_time_filter = get_time_window_from_data_source_node(
                            feature_time_limits,
                            node.feature_definition_wrapper.batch_materialization_schedule,
                            data_source_scan_node.ds_node,
                        )
                        if data_time_filter is not None:
                            data_source_scan_node_ref.node = attrs.evolve(
                                data_source_scan_node_ref.node,
                                start_time=data_time_filter.start,
                                end_time=data_time_filter.end,
                            )

                tree.node = FeatureTimeFilterNode(
                    node.dialect,
                    node.compute_mode,
                    ConvertTimestampToUTCNode.for_feature_definition(
                        node.dialect, node.compute_mode, node.feature_definition_wrapper, node.as_ref()
                    ),
                    feature_time_limits,
                    node.feature_definition_wrapper.time_range_policy,
                    node.feature_definition_wrapper.timestamp_key,
                    node.feature_definition_wrapper.timestamp_key,
                )
            elif isinstance(node, OfflineStoreScanNode):
                tree.node = attrs.evolve(node, partition_time_filter=feature_time_limits)


# Mutates the input
def rewrite_tree_for_spine(tree: NodeRef):
    if not conf.get_bool("QUERY_REWRITE_ENABLED"):
        return
    rewrites = [SpineTimePushdown(), SpineEntityPushdown()]
    for rewrite in rewrites:
        rewrite.rewrite(tree)


def _get_spine_time_limits(cur_node: QueryNode) -> pendulum.Period:
    user_specified_data_node = get_first_input_node_of_class(cur_node.as_ref(), UserSpecifiedDataNode)
    if not user_specified_data_node:
        # We don't expect this to occur
        msg = "Expected spine to contain a UserSpecifiedDataNode, but it did not."
        raise ValueError(msg)
    timestamp_key = user_specified_data_node.metadata["timestamp_key"]
    data = user_specified_data_node.data
    if cur_node.compute_mode == ComputeMode.SPARK:
        limits = get_time_limits_of_dataframe(data.to_spark(), timestamp_key)
    else:
        limits = get_time_limits_of_pandas_dataframe(data.to_pandas(), timestamp_key)
    if limits is None:
        raise errors.INVALID_NULL_SPINE_TIME_KEY
    return limits
