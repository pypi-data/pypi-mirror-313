import pandas as pd
import pyarrow as pa

from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_utils import tree_contains
from tecton_core.query.nodes import MultiOdfvPipelineNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import StagedTableScanNode
from tecton_core.query.pandas.node import PandasExecNode
from tecton_core.query.pandas.nodes import PandasDataNode
from tecton_core.query.pandas.nodes import PandasMultiOdfvPipelineNode
from tecton_core.query.pandas.nodes import PandasRenameColsNode


def pandas_convert_odfv_only(tree: NodeRef, odfv_input_df: pd.DataFrame) -> PandasExecNode:
    assert tree_contains(tree, MultiOdfvPipelineNode)
    return _convert_to_pandas_nodes(tree, odfv_input_df)


def _convert_to_pandas_nodes(tree: NodeRef, odfv_input_df: pd.DataFrame) -> PandasExecNode:
    # Recurses over RenameColsNodes and MultiOdfvPipelineNode at the top of the tree and converts them to
    # PandasExecNodes and converts only the node immediately below these nodes to a SqlExecNode
    logical_tree_node = tree.node

    if isinstance(logical_tree_node, StagedTableScanNode):
        return PandasDataNode(
            input_reader=pa.Table.from_pandas(odfv_input_df).to_reader(),
            input_node=None,
            columns=logical_tree_node.columns,
            column_name_updater=lambda x: x,
            secret_resolver=None,
        )

    node_mapping = {
        MultiOdfvPipelineNode: PandasMultiOdfvPipelineNode,
        RenameColsNode: PandasRenameColsNode,
    }
    if logical_tree_node.__class__ in node_mapping:
        input_node = _convert_to_pandas_nodes(logical_tree_node.input_node, odfv_input_df)
        return node_mapping[logical_tree_node.__class__].from_node_inputs(logical_tree_node, input_node)
    else:
        msg = f"Unexpected logical node for ODFV Pandas execution {logical_tree_node.__class__}"
        raise Exception(msg)
