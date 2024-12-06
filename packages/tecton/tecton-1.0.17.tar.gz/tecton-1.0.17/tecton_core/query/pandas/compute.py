import inspect
import uuid
from typing import Optional
from typing import Union

import attrs
import pandas
import pyarrow

from tecton_core import conf
from tecton_core.query.dialect import Dialect
from tecton_core.query.duckdb.compute import DuckDBCompute
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.pandas.nodes import PandasDataSourceScanNode
from tecton_core.query.query_tree_compute import ComputeMonitor
from tecton_core.query.query_tree_compute import SQLCompute
from tecton_core.query.query_tree_compute import logger
from tecton_core.schema import Schema
from tecton_core.secrets import SecretResolver
from tecton_core.specs import FileSourceSpec


@attrs.frozen
class PandasCompute(SQLCompute):
    # For executing pipelines, Pandas will execute only the data source scan + pipeline nodes. Other
    # logic e.g. around asof joins are executed using DuckDB.
    sql_compute: DuckDBCompute

    @staticmethod
    def from_context() -> "PandasCompute":
        return PandasCompute(sql_compute=DuckDBCompute.from_context())

    def run_sql(
        self,
        sql_string: str,
        return_dataframe: bool = False,
        expected_output_schema: Optional[Schema] = None,
        monitor: Optional[ComputeMonitor] = None,
    ) -> Optional[pyarrow.RecordBatchReader]:
        return self.sql_compute.run_sql(
            sql_string,
            return_dataframe,
            expected_output_schema=expected_output_schema,
            monitor=monitor,
        )

    def get_dialect(self) -> Dialect:
        return Dialect.DUCKDB

    def register_temp_table_from_pandas(self, table_name: str, pandas_df: pandas.DataFrame) -> None:
        self.sql_compute.register_temp_table_from_pandas(table_name, pandas_df)

    def register_temp_table(
        self, table_name: str, table_or_reader: Union[pyarrow.Table, pyarrow.RecordBatchReader]
    ) -> None:
        self.sql_compute.register_temp_table(table_name, table_or_reader)

    def _register_temp_table_from_data_source(
        self,
        table_name: str,
        ds: DataSourceScanNode,
        secret_resolver: Optional[SecretResolver] = None,
        monitor: Optional[ComputeMonitor] = None,
    ) -> None:
        if isinstance(ds.ds.batch_source, FileSourceSpec):
            return self.sql_compute.register_temp_table_from_data_source(table_name, ds, secret_resolver, monitor)

        pandas_node = PandasDataSourceScanNode.from_node_inputs(
            query_node=ds, input_node=None, secret_resolver=secret_resolver
        )

        if monitor:
            try:
                monitor.set_query(inspect.getsource(ds.ds.batch_source.function))
            except OSError:
                pass

        self.register_temp_table_from_pandas(table_name, pandas_node.to_dataframe())

    def _load_table(
        self, table_name: str, expected_output_schema: Optional[Schema] = None
    ) -> pyarrow.RecordBatchReader:
        return self.sql_compute.load_table(table_name, expected_output_schema=expected_output_schema)

    def load_from_data_source(
        self,
        ds: DataSourceScanNode,
        expected_output_schema: Optional[Schema] = None,
        secret_resolver: Optional[SecretResolver] = None,
        monitor: Optional[ComputeMonitor] = None,
    ) -> pyarrow.RecordBatchReader:
        tmp_table_name = f"TEMP_{ds.node_id.hex[:10]}_{uuid.uuid4().hex[:5]}"
        self._register_temp_table_from_data_source(
            tmp_table_name,
            ds,
            secret_resolver,
            monitor,
        )
        return self._load_table(tmp_table_name, expected_output_schema)

    def run_odfv(
        self, qt_node: NodeRef, input: pyarrow.RecordBatchReader, monitor: Optional[ComputeMonitor] = None
    ) -> pyarrow.RecordBatchReader:
        from tecton_core.query.pandas.translate import pandas_convert_odfv_only

        if conf.get_bool("DUCKDB_DEBUG"):
            logger.warning(f"Input dataframe to ODFV execution: {input.schema}")

        pandas_node = pandas_convert_odfv_only(qt_node, input)
        # ToDo: extract code from pandas_node and send it to monitor
        df = pandas_node.to_arrow()
        return df
