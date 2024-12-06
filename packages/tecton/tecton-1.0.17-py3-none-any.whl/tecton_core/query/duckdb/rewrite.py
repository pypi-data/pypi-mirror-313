from tecton_core import conf
from tecton_core.query import nodes
from tecton_core.query.duckdb import nodes as duckdb_nodes
from tecton_core.query.node_interface import NodeRef


class DuckDBTreeRewriter:
    node_mapping = {
        nodes.PartialAggNode: duckdb_nodes.PartialAggDuckDBNode,
        nodes.AsofJoinFullAggNode: duckdb_nodes.AsofJoinFullAggNodeDuckDBNode,
        nodes.AsofJoinNode: duckdb_nodes.AsofJoinDuckDBNode,
    }

    def rewrite(
        self,
        tree: NodeRef,
    ) -> None:
        for i in tree.inputs:
            self.rewrite(tree=i)
        tree_node = tree.node
        if isinstance(tree_node, nodes.AsofJoinFullAggNode) and conf.get_bool("DUCKDB_ENABLE_OPTIMIZED_FULL_AGG"):
            tree.node = duckdb_nodes.AsofJoinFullAggDuckDBNodeV2.from_query_node(tree_node)
        elif tree_node.__class__ in self.node_mapping:
            tree.node = self.node_mapping[tree_node.__class__].from_query_node(tree_node)
