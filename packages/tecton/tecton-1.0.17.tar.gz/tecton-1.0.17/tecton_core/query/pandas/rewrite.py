import logging
import uuid
from typing import Dict

import pyarrow

from tecton_core.query import nodes
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.pandas import nodes as pandas_nodes
from tecton_core.query.query_tree_compute import QueryTreeCompute
from tecton_core.schema_validation import arrow_schema_to_tecton_schema


logger = logging.getLogger(__name__)


class PandasTreeRewriter:
    def rewrite(
        self,
        tree: NodeRef,
        pipeline_compute: QueryTreeCompute,
        data_sources: Dict[str, pyarrow.RecordBatchReader],
    ) -> None:
        """Finds all FeatureViewPipelineNodes, executes their subtrees, and replaces them with StagedTableScanNodes.

        Assumes that the inputs to the FeatureViewPipelineNodes have already been replaced with StagedTableScanNodes,
        and that each such StagedTableScanNode corresponds to a pyarrow table contained in 'data_sources'.
        """
        tree_node = tree.node

        if isinstance(tree_node, nodes.FeatureViewPipelineNode):
            for _, fv_input_node_ref in tree_node.inputs_map.items():
                self._rewrite_fv_input_node(fv_input_node_ref, data_sources)

            pipeline_node = pandas_nodes.PandasFeatureViewPipelineNode.from_node_inputs(
                query_node=tree_node,
                input_node=None,
            )
            pipeline_result = pipeline_node.to_arrow()
            staging_table_name = f"{pipeline_node.feature_definition_wrapper.name}_{uuid.uuid4().hex[:16]}_pandas"
            tree.node = nodes.StagedTableScanNode(
                tree_node.dialect,
                tree_node.compute_mode,
                staged_schema=arrow_schema_to_tecton_schema(pipeline_result.schema),
                staging_table_name=staging_table_name,
            )
            pipeline_compute.register_temp_table(staging_table_name, pipeline_result)
        else:
            for i in tree.inputs:
                self.rewrite(tree=i, pipeline_compute=pipeline_compute, data_sources=data_sources)

    def _rewrite_fv_input_node(self, tree: NodeRef, data_sources: Dict[str, pyarrow.RecordBatchReader]) -> None:
        # Certain StagedTableScanNodes are duplicated. If one of them has already been converted to a PandasDataNode,
        # the other does not need to be converted.
        if isinstance(tree.node, pandas_nodes.PandasDataNode):
            return
        assert isinstance(tree.node, nodes.StagedTableScanNode)
        table_name = tree.node.staging_table_name
        assert table_name in data_sources
        # A rewrite should only leave NodeRefs. However, this PandasDataNode is temporary. It will be removed above.
        tree.node = pandas_nodes.PandasDataNode(
            input_reader=data_sources[table_name],
            input_node=None,
            columns=tree.node.columns,
            column_name_updater=lambda x: x,
            secret_resolver=None,
        )
