import contextlib
import logging
from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import Iterable
from typing import Optional
from typing import Union

import attrs
import pandas
import pyarrow

from tecton_core.embeddings.model_artifacts import ModelArtifactProvider
from tecton_core.offline_store import OfflineStoreOptionsProvider
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.schema import Schema
from tecton_core.secrets import SecretResolver


logger = logging.getLogger(__name__)


@attrs.define
class QueryTreeCompute(ABC):
    """
    Base class for compute (e.g. DWH compute or Python compute) which can be
    used for different stages of executing the query tree.
    """


@attrs.define
class ComputeMonitor:
    log_progress: Callable[[float], None] = lambda _: _  # noqa: E731
    set_query: Callable[[str], None] = lambda _: _  # noqa: E731


@attrs.define
class SQLCompute(QueryTreeCompute, contextlib.AbstractContextManager):
    """
    Base class for compute backed by a SQL engine (e.g. Snowflake and DuckDB).
    """

    @staticmethod
    def for_dialect(
        dialect: Dialect,
        qt_root: Optional[NodeRef] = None,
        secret_resolver: Optional[SecretResolver] = None,
        offline_store_options: Iterable[OfflineStoreOptionsProvider] = (),
    ) -> "SQLCompute":
        # Conditional imports are used so that optional dependencies such as the Snowflake connector are only imported
        # if they're needed for a query
        if dialect == Dialect.SNOWFLAKE:
            from tecton_core.query.snowflake.compute import SnowflakeCompute
            from tecton_core.query.snowflake.compute import create_snowflake_connection

            if SnowflakeCompute.is_context_initialized():
                return SnowflakeCompute.from_context()
            return SnowflakeCompute.for_connection(create_snowflake_connection(qt_root, secret_resolver))
        if dialect == Dialect.DUCKDB:
            from tecton_core.query.duckdb.compute import DuckDBCompute

            return DuckDBCompute.from_context(offline_store_options=offline_store_options)
        if dialect == Dialect.PANDAS:
            from tecton_core.query.pandas.compute import PandasCompute

            return PandasCompute.from_context()
        if dialect == Dialect.BIGQUERY:
            from tecton_core.query.bigquery.compute import BigqueryCompute

            return BigqueryCompute()

    @abstractmethod
    def get_dialect(self) -> Dialect:
        pass

    @abstractmethod
    def run_sql(
        self,
        sql_string: str,
        return_dataframe: bool = False,
        expected_output_schema: Optional[Schema] = None,
        monitor: Optional[ComputeMonitor] = None,
    ) -> Optional[pyarrow.RecordBatchReader]:
        pass

    @abstractmethod
    def register_temp_table(
        self, table_name: str, table_or_reader: Union[pyarrow.Table, pyarrow.RecordBatchReader]
    ) -> None:
        pass

    # TODO(danny): remove this once we convert connectors to return arrow tables instead of pandas dataframes
    @abstractmethod
    def register_temp_table_from_pandas(self, table_name: str, pandas_df: pandas.DataFrame) -> None:
        pass

    @abstractmethod
    def load_from_data_source(
        self,
        ds: DataSourceScanNode,
        expected_output_schema: Optional[Schema] = None,
        secret_resolver: Optional[SecretResolver] = None,
        monitor: Optional[ComputeMonitor] = None,
    ) -> pyarrow.RecordBatchReader:
        pass

    def cleanup_temp_tables(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup_temp_tables()


@attrs.define
class ModelInferenceCompute(QueryTreeCompute, ABC):
    """
    Base class for compute that executes model inference (e.g. Torch).
    """

    @staticmethod
    def for_dialect(dialect: Dialect, model_artifact_provider: ModelArtifactProvider) -> "ModelInferenceCompute":
        if dialect == Dialect.TORCH:
            from tecton_core.embeddings.compute import TorchCompute

            return TorchCompute.from_context(model_artifact_provider)

    @abstractmethod
    def run_inference(
        self, qt_node: NodeRef, input_data: Union[pyarrow.Table, pyarrow.RecordBatchReader]
    ) -> pyarrow.RecordBatchReader:
        pass
