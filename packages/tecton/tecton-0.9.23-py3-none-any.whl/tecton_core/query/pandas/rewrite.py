import logging
import uuid
from typing import Dict
from typing import Iterable
from typing import Iterator
from typing import Tuple

import pyarrow

from tecton_core import errors
from tecton_core.offline_store import DeltaReader
from tecton_core.offline_store import OfflineStoreOptionsProvider
from tecton_core.offline_store import OfflineStoreReaderParams
from tecton_core.offline_store import ParquetReader
from tecton_core.query import nodes
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.pandas import nodes as pandas_nodes
from tecton_core.query.query_tree_compute import QueryTreeCompute


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
                staged_columns=pipeline_node.columns,
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


class OfflineScanner:
    def __init__(self, options_providers: Iterable[OfflineStoreOptionsProvider]) -> None:
        self._options_providers = options_providers

    def read_and_rewrite(
        self,
        tree: NodeRef,
    ) -> Iterator[Tuple[str, pyarrow.RecordBatchReader]]:
        """
        Finds all OfflineStoreScanNode nodes in the given tree.
        Executes them and then replaces each with a StagedTableScanNode in the tree.
        The function is a generator that yields tuples (staging table name, arrow reader),
        which should be registered in a compute in order for StagedTabledScanNodes to work.
        """
        for i in tree.inputs:
            yield from self.read_and_rewrite(tree=i)

        tree_node = tree.node
        if isinstance(tree_node, nodes.OfflineStoreScanNode):
            fdw = tree_node.feature_definition_wrapper
            if fdw.has_delta_offline_store:
                reader_params = OfflineStoreReaderParams(delta_table_uri=fdw.materialized_data_path)
                reader = DeltaReader(params=reader_params, fd=fdw, options_providers=self._options_providers)
            elif fdw.has_parquet_offline_store:
                reader = ParquetReader(fd=fdw, options_providers=self._options_providers)
            else:
                msg = f"Offline store is not configured for FeatureView {fdw.name}"
                raise errors.TectonValidationError(msg)

            table = reader.read(tree_node.partition_time_filter)

            staged_table_name = f"{fdw.name}_offline_store_scan_{uuid.uuid4().hex[:16]}"
            tree.node = nodes.StagedTableScanNode(
                tree_node.dialect,
                tree_node.compute_mode,
                staged_columns=tree_node.columns,
                staging_table_name=staged_table_name,
            )
            yield staged_table_name, table
