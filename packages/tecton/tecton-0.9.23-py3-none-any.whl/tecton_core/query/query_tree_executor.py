import contextlib
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from typing import Iterable
from typing import Iterator
from typing import Optional
from typing import Tuple

import attrs
import pandas as pd
import pyarrow

from tecton_core import conf
from tecton_core import schema
from tecton_core.offline_store import DEFAULT_OPTIONS_PROVIDERS
from tecton_core.offline_store import OfflineStoreOptionsProvider
from tecton_core.query.dialect import Dialect
from tecton_core.query.duckdb.rewrite import DuckDBTreeRewriter
from tecton_core.query.errors import UserDefinedTransformationError
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.executor_utils import DebugOutput
from tecton_core.query.executor_utils import QueryTreeMonitor
from tecton_core.query.executor_utils import get_stage_type_for_dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import QueryNode
from tecton_core.query.node_interface import recurse_query_tree
from tecton_core.query.node_utils import get_data_source_dialect
from tecton_core.query.node_utils import get_first_input_node_of_class
from tecton_core.query.node_utils import get_pipeline_dialect
from tecton_core.query.node_utils import get_staging_nodes
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import MockDataSourceScanNode
from tecton_core.query.nodes import MultiOdfvPipelineNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import StagedTableScanNode
from tecton_core.query.nodes import StagingNode
from tecton_core.query.nodes import TextEmbeddingInferenceNode
from tecton_core.query.nodes import UserSpecifiedDataNode
from tecton_core.query.pandas.rewrite import OfflineScanner
from tecton_core.query.pandas.rewrite import PandasTreeRewriter
from tecton_core.query.query_tree_compute import ComputeMonitor
from tecton_core.query.query_tree_compute import ModelInferenceCompute
from tecton_core.query.query_tree_compute import QueryTreeCompute
from tecton_core.query.query_tree_compute import SQLCompute
from tecton_core.secrets import SecretResolver
from tecton_proto.materialization.job_metadata_pb2 import TectonManagedStage


logger = logging.getLogger(__name__)


def _pyarrow_type_contains_map_type(pyarrow_type: pyarrow.DataType) -> bool:
    if isinstance(pyarrow_type, pyarrow.MapType):
        return True
    elif isinstance(pyarrow_type, pyarrow.StructType):
        return any(_pyarrow_type_contains_map_type(field.type) for field in pyarrow_type)
    elif isinstance(pyarrow_type, pyarrow.ListType):
        return _pyarrow_type_contains_map_type(pyarrow_type.value_type)
    return False


@dataclass
class QueryTreeOutput:
    # Maps name to pyarrow batch reader containing a data source
    data_source_readers: Dict[str, pyarrow.RecordBatchReader]
    # Maps name to pyarrow batch reader containing a feature view
    feature_view_readers: Dict[str, pyarrow.RecordBatchReader]
    odfv_input: Optional[pyarrow.RecordBatchReader] = None
    odfv_output: Optional[pd.DataFrame] = None

    @property
    def result_df(self) -> pd.DataFrame:
        if self.odfv_output is not None:
            return self.odfv_output
        assert self.odfv_input is not None

        contains_map_type = any(_pyarrow_type_contains_map_type(field.type) for field in self.odfv_input.schema)
        if contains_map_type:
            # The `maps_as_pydicts` parameter for pyarrow.Table.to_pandas is only supported starting in pyarrow 13.0.0.
            if pyarrow.__version__ < "13.0.0":
                msg = f"Rift requires pyarrow>=13.0.0 to perform feature retrieval for Map features. You have version {pyarrow.__version__}."
                raise RuntimeError(msg)
            return self.odfv_input.read_pandas(maps_as_pydicts="strict")

        return self.odfv_input.read_pandas()

    @property
    def result_table(self) -> pyarrow.Table:
        assert self.odfv_output is None, "Can't retrieve ODFV output as a pyarrow table"
        return self.odfv_input


def checkpoint(
    root: NodeRef, query_tree_step: Optional[QueryTreeStep] = None, staging_node: Optional[QueryNode] = None
) -> None:
    """Checkpointing in QueryTreeExecutor is somewhat similar to one in the Spark DAG:
    (1) QT is being executed up until StagingNode
    (2) The result of this execution is then cached (as pyarrow Table / RecordBatchReader)
    (3) Corresponding StagingNode is replaced with StagedTableScanNode to read cached result on the next stage

    However, for stages that return RecordBatchReader the result is lazily evaluated and will be
    completely unrolled by the next stage.
    """

    def traverse(tree: NodeRef) -> None:
        for i in tree.inputs:
            traverse(tree=i)

        if isinstance(tree.node, StagingNode) and (
            (staging_node and tree.node == staging_node)
            or (query_tree_step and query_tree_step == tree.node.query_tree_step)
        ):
            tree.node = StagedTableScanNode.from_staging_node(tree.node.dialect, tree.node.compute_mode, tree.node)

    traverse(root)


UserErrors = (UserDefinedTransformationError,)


@attrs.define
class QueryTreeExecutor:
    offline_store_options_providers: Iterable[OfflineStoreOptionsProvider] = DEFAULT_OPTIONS_PROVIDERS
    secret_resolver: Optional[SecretResolver] = None
    monitor: QueryTreeMonitor = DebugOutput()
    is_debug: bool = attrs.field(init=False)
    # Used to track temp tables per dialect so we can clean them up appropriately & avoid re-registering duplicates
    _dialect_to_temp_table_name: Optional[Dict[Dialect, set]] = attrs.field(init=False)

    def __attrs_post_init__(self):
        # TODO(danny): Expose as configs
        self.is_debug = conf.get_bool("DUCKDB_DEBUG")
        self._dialect_to_temp_table_name = None

    @contextlib.contextmanager
    def _monitor_stage(
        self,
        step: str,
        type_: Optional[int] = None,
        dialect: Optional[Dialect] = None,
    ) -> Iterator[ComputeMonitor]:
        assert type_ or dialect, "Either type or dialect must be provided"
        if not type_:
            type_ = get_stage_type_for_dialect(dialect)

        monitor_stage_id = self.monitor.create_stage(type_, step)

        try:
            self.monitor.update_progress(monitor_stage_id, 0)
            yield ComputeMonitor(
                log_progress=lambda p: self.monitor.update_progress(monitor_stage_id, p),
                set_query=lambda q: self.monitor.set_query(monitor_stage_id, q),
            )
        except UserErrors:
            self.monitor.set_failed(monitor_stage_id, user_error=True)
            raise
        except Exception:
            self.monitor.set_failed(monitor_stage_id, user_error=False)
            raise
        else:
            self.monitor.update_progress(monitor_stage_id, 1)
            self.monitor.set_completed(monitor_stage_id)

    def exec_qt(self, qt_root: NodeRef) -> QueryTreeOutput:
        # Make copy so the execution doesn't mutate the original QT visible to users
        qt_root = qt_root.deepcopy()
        if self.is_debug:
            logger.warning("---------------------------------- Executing overall QT ----------------------------------")
            logger.warning(f"QT: \n{qt_root.pretty_str(columns=True)}")

        rewriter = DuckDBTreeRewriter()
        rewriter.rewrite(qt_root)

        output = self._execute_data_source_step(qt_root)

        # This can only happen if the initial query tree was a single DataSourceScanNode followed by a
        # StagingNode. In that case, we can skip the rest of the query tree.
        if len(output.data_source_readers) == 1 and isinstance(qt_root.node, StagedTableScanNode):
            table_name, pa_reader = output.data_source_readers.popitem()
            return QueryTreeOutput(data_source_readers={}, feature_view_readers={}, odfv_input=pa_reader)

        # Executes the feature view pipeline and stages into memory
        output = self._execute_pipeline_step(output, qt_root)

        if get_first_input_node_of_class(qt_root, OfflineStoreScanNode) is not None:
            with self._monitor_stage("Reading offline store", type_=TectonManagedStage.StageType.OFFLINE_STORE):
                offline_scanner = OfflineScanner(options_providers=self.offline_store_options_providers)
                readers = offline_scanner.read_and_rewrite(qt_root)
                output.feature_view_readers.update(readers)

        output = self._execute_model_inference_step(output, qt_root)

        # Does partial aggregations (if applicable) and spine joins
        qt_root.node = qt_root.node.with_dialect(Dialect.DUCKDB)
        output = self._execute_agg_step(output, qt_root)

        # Runs ODFVs (if applicable)
        output = self._execute_odfv_step(output, qt_root)
        return output

    def _execute_data_source_step(self, qt_root: NodeRef) -> QueryTreeOutput:
        staging_nodes_to_process = get_staging_nodes(qt_root, QueryTreeStep.DATA_SOURCE)
        if len(staging_nodes_to_process) == 0:
            # This is possible if, for example, the querytree is reading from the offline store instead from a data source.
            return QueryTreeOutput(data_source_readers={}, feature_view_readers={})

        data_source_readers = {}
        for name, staging_node in staging_nodes_to_process.items():
            data_source_node_ref = staging_node.input_node
            data_source_node = data_source_node_ref.node

            # No data source dialect will be returned for MockedDataSource
            dialect = get_data_source_dialect(data_source_node_ref) or Dialect.DUCKDB
            with self._monitor_stage("Reading Data Source", dialect=dialect) as monitor:
                compute = SQLCompute.for_dialect(
                    dialect,
                    qt_root,
                    secret_resolver=self.secret_resolver,
                    offline_store_options=self.offline_store_options_providers,
                )

                assert isinstance(data_source_node, (DataSourceScanNode, MockDataSourceScanNode))

                if not isinstance(data_source_node, MockDataSourceScanNode):
                    compute.register_temp_table_from_data_source(name, data_source_node, self.secret_resolver, monitor)
                    if dialect == get_pipeline_dialect(qt_root) and dialect != Dialect.PANDAS:
                        # No need to export from compute, it will be shared between stages
                        output_pa = None
                    else:
                        expected_schema = (
                            schema.Schema(data_source_node.ds.schema.tecton_schema)
                            if data_source_node.ds.schema
                            else None
                        )
                        output_pa = compute.load_table(table_name=name, expected_output_schema=expected_schema)
                else:
                    self._maybe_register_temp_tables(qt_root=qt_root, compute=compute)
                    output_pa = compute.run_sql(data_source_node.to_sql(), return_dataframe=True, monitor=monitor)
                data_source_readers[name] = output_pa

                if output_pa:
                    # checkpoint StagingNode (one at a time) only if there's something to checkpoint
                    checkpoint(qt_root, staging_node=staging_node)

        return QueryTreeOutput(data_source_readers=data_source_readers, feature_view_readers={})

    def _execute_pipeline_step(self, output: QueryTreeOutput, qt_node: NodeRef) -> QueryTreeOutput:
        pipeline_dialect = get_pipeline_dialect(qt_node)
        if not pipeline_dialect:
            # bypass
            return QueryTreeOutput(feature_view_readers=output.data_source_readers, data_source_readers={})

        compute = SQLCompute.for_dialect(pipeline_dialect, qt_node, secret_resolver=self.secret_resolver)
        with self._monitor_stage("Evaluating Feature View pipelines", dialect=pipeline_dialect) as monitor, compute:
            if pipeline_dialect == Dialect.PANDAS:
                rewriter = PandasTreeRewriter()
                rewriter.rewrite(qt_node, compute, output.data_source_readers)
                if self.is_debug:
                    logger.warning(f"PANDAS PRE INIT: \n{qt_node.pretty_str(description=False)}")
            else:
                for table_name, pa_reader in output.data_source_readers.items():
                    if not pa_reader:
                        # assuming that we're sharing computes and table is already loaded
                        continue

                    if self.is_debug:
                        logger.warning(
                            f"Registering staged table {table_name} to pipeline compute with schema:\n{pa_reader.schema}"
                        )
                    compute.register_temp_table(table_name, pa_reader)

            self._maybe_register_temp_tables(qt_root=qt_node, compute=compute)

            staging_nodes_to_process = get_staging_nodes(qt_node, QueryTreeStep.PIPELINE)
            if len(staging_nodes_to_process) == 0:
                # It's possible that with Pandas transformations there's no staging node,
                # but Pandas rewrite above already replaced Pandas pipeline node with StagedTableScanNode
                return QueryTreeOutput(data_source_readers={}, feature_view_readers={})

            feature_view_tables = self._stage_tables_and_load_pa(
                nodes_to_process=staging_nodes_to_process,
                compute=compute,
                monitor=monitor,
            )
            checkpoint(qt_node, QueryTreeStep.PIPELINE)
            return QueryTreeOutput(data_source_readers={}, feature_view_readers=feature_view_tables)

    def _execute_model_inference_step(self, prev_step_output: QueryTreeOutput, qt_node: NodeRef) -> QueryTreeOutput:
        has_models = get_first_input_node_of_class(qt_node, node_class=TextEmbeddingInferenceNode) is not None

        if not has_models:
            return prev_step_output

        # NOTE: only torch supports model inference
        model_compute = ModelInferenceCompute.for_dialect(Dialect.TORCH)

        with self._monitor_stage("Computing model inference", type_=TectonManagedStage.StageType.PYTHON):
            staging_nodes_to_process = get_staging_nodes(qt_node, QueryTreeStep.MODEL_INFERENCE)
            if len(staging_nodes_to_process) == 0:
                msg = "No `MODEL_INFERENCE` staging nodes, despite having an `TextEmbeddingInferenceNode`"
                raise ValueError(msg)

            # We make a copy since we need to pass through any FVs which do not
            # have a model inference step.
            feature_view_readers = prev_step_output.feature_view_readers.copy()

            for name, staging_node in staging_nodes_to_process.items():
                inference_node_ref = staging_node.input_node
                inference_node = inference_node_ref.node
                assert isinstance(inference_node, TextEmbeddingInferenceNode)

                if not isinstance(inference_node.input_node.node, StagedTableScanNode):
                    msg = "Only supports `StagedTableScanNode` input"
                    raise ValueError(msg)

                input_table_name = inference_node.input_node.node.staging_table_name

                # We get+remove the input_table from feature_view_readers (since we will use `feature_view_readers` to return).
                table_reader = feature_view_readers.pop(input_table_name)
                output_table = model_compute.run_inference(inference_node, table_reader)
                feature_view_readers[staging_node.staging_table_name_unique()] = output_table

            checkpoint(qt_node, QueryTreeStep.MODEL_INFERENCE)
            return QueryTreeOutput(
                data_source_readers={},
                feature_view_readers=feature_view_readers,
            )

    def _execute_agg_step(self, output: QueryTreeOutput, qt_node: NodeRef) -> QueryTreeOutput:
        compute = SQLCompute.for_dialect(Dialect.DUCKDB)

        with self._monitor_stage(
            "Computing aggregated features & joining results", type_=TectonManagedStage.StageType.AGGREGATE
        ) as monitor, compute:
            # The AsOfJoins need access to a spine, which are registered here.
            self._maybe_register_temp_tables(qt_root=qt_node, compute=compute)

            # Register staged pyarrow tables in agg compute
            for table_name, pa_reader in output.feature_view_readers.items():
                if self.is_debug:
                    logger.warning(
                        f"Registering staged table {table_name} to agg compute with schema:\n{pa_reader.schema}"
                    )
                compute.register_temp_table(table_name, pa_reader)

            next_output = self._process_agg_join(output, compute, qt_node, monitor)
            checkpoint(qt_node, QueryTreeStep.AGGREGATION)
            return next_output

    def _execute_odfv_step(self, prev_step_output: QueryTreeOutput, qt_node: NodeRef) -> QueryTreeOutput:
        assert prev_step_output
        assert prev_step_output.odfv_input is not None
        has_odfvs = get_first_input_node_of_class(qt_node, node_class=MultiOdfvPipelineNode) is not None
        if has_odfvs:
            compute = SQLCompute.for_dialect(Dialect.PANDAS)
            # TODO(meastham): Use pyarrow typemapper after upgrading pandas
            with self._monitor_stage(
                "Evaluating On-Demand Feature Views", type_=TectonManagedStage.StageType.PYTHON
            ) as monitor, compute:
                output_df = compute.run_odfv(qt_node, prev_step_output.odfv_input.read_pandas(), monitor=monitor)
        else:
            output_df = None
        return QueryTreeOutput(
            data_source_readers={},
            feature_view_readers=prev_step_output.feature_view_readers,
            odfv_input=prev_step_output.odfv_input,
            odfv_output=output_df,
        )

    def _process_agg_join(
        self,
        output: QueryTreeOutput,
        compute: QueryTreeCompute,
        qt_node: NodeRef,
        monitor: ComputeMonitor,
    ) -> QueryTreeOutput:
        # TODO(danny): change the "stage" in the StagingNode to be more for the destination stage
        staging_nodes_to_process = get_staging_nodes(qt_node, QueryTreeStep.AGGREGATION)

        if len(staging_nodes_to_process) > 0:
            # There should be a single StagingNode. It is either there for materialization or ODFVs.
            assert len(staging_nodes_to_process) == 1
            readers = self._stage_tables_and_load_pa(
                nodes_to_process=staging_nodes_to_process,
                compute=compute,
                monitor=monitor,
            )
            assert len(readers) == 1
            pa_reader = next(iter(readers.values()))
            return QueryTreeOutput(
                data_source_readers={}, feature_view_readers=output.feature_view_readers, odfv_input=pa_reader
            )

        # There are no StagingNodes, so we can execute the remainder of the query tree.
        output_df_pa = compute.run_sql(qt_node.to_sql(), return_dataframe=True, monitor=monitor)
        return QueryTreeOutput(
            data_source_readers={}, feature_view_readers=output.feature_view_readers, odfv_input=output_df_pa
        )

    def _stage_tables_and_load_pa(
        self,
        nodes_to_process: Dict[str, QueryNode],
        compute: QueryTreeCompute,
        monitor: ComputeMonitor,
    ) -> Dict[str, pyarrow.RecordBatchReader]:
        readers = {}
        for _, node in nodes_to_process.items():
            if isinstance(node, StagingNode):
                name, reader = self._process_staging_node(node, compute, monitor)
                readers[name] = reader
        return readers

    def _process_staging_node(
        self,
        qt_node: StagingNode,
        compute: QueryTreeCompute,
        monitor: ComputeMonitor,
    ) -> Tuple[str, pyarrow.RecordBatchReader]:
        start_time = datetime.now()
        staging_table_name = qt_node.staging_table_name_unique()
        sql_string = qt_node.with_dialect(compute.get_dialect())._to_staging_query_sql()
        reader = compute.run_sql(
            sql_string, return_dataframe=True, expected_output_schema=qt_node.output_schema, monitor=monitor
        )
        staging_done_time = datetime.now()
        if self.is_debug:
            elapsed_staging_time = (staging_done_time - start_time).total_seconds()
            logger.warning(f"STAGE_{staging_table_name}_TIME_SEC: {elapsed_staging_time}")

        return staging_table_name, reader

    def _maybe_register_temp_tables(self, qt_root: NodeRef, compute: QueryTreeCompute) -> None:
        self._dialect_to_temp_table_name = self._dialect_to_temp_table_name or {}

        dialect = compute.get_dialect()
        if dialect not in self._dialect_to_temp_table_name:
            self._dialect_to_temp_table_name[dialect] = set()

        def maybe_register_temp_table(node):
            if isinstance(node, UserSpecifiedDataNode):
                tmp_table_name = node.data._temp_table_name
                if tmp_table_name in self._dialect_to_temp_table_name[dialect]:
                    return
                df = node.data.to_pandas()
                if self.is_debug:
                    logger.warning(
                        f"Registering user specified data {tmp_table_name} to {compute.get_dialect()} with schema:\n{df.dtypes}"
                    )
                compute.register_temp_table_from_pandas(tmp_table_name, df)
                self._dialect_to_temp_table_name[dialect].add(tmp_table_name)

        recurse_query_tree(
            qt_root,
            maybe_register_temp_table,
        )
