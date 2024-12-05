import dataclasses
import logging
import re
import time
import typing
from typing import Iterable
from typing import Optional
from typing import Union

import attrs


try:
    import duckdb
except ImportError:
    msg = (
        "Couldn't initialize Rift compute. "
        "To use Rift install all Rift dependencies first by executing `pip install tecton[rift]`."
    )
    raise RuntimeError(msg)
import pandas as pd
import pyarrow
import pyarrow.dataset
import pyarrow.fs
import pyarrow.json
import sqlparse
from deltalake import DeltaTable
from duckdb import DuckDBPyConnection

from tecton_core import conf
from tecton_core import id_helper
from tecton_core.duckdb_context import DuckDBContext
from tecton_core.errors import TectonValidationError
from tecton_core.offline_store import BotoOfflineStoreOptionsProvider
from tecton_core.offline_store import OfflineStoreOptionsProvider
from tecton_core.query.dialect import Dialect
from tecton_core.query.errors import SQLCompilationError
from tecton_core.query.errors import UserCodeError
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.query_tree_compute import ComputeMonitor
from tecton_core.query.query_tree_compute import SQLCompute
from tecton_core.schema import Schema
from tecton_core.schema_validation import CastError
from tecton_core.schema_validation import tecton_schema_to_arrow_schema
from tecton_core.secrets import SecretResolver
from tecton_core.specs import FileSourceSpec
from tecton_core.specs import PushTableSourceSpec
from tecton_core.time_utils import get_timezone_aware_datetime
from tecton_proto.data import batch_data_source_pb2


@dataclasses.dataclass
class _Cause:
    type_name: str
    message: str


_input_error_pattern = re.compile(
    r"Invalid Input Error: arrow_scan: get_next failed\(\): "
    + r"(?:Unknown error|Invalid): (.*)\. Detail: Python exception: (.*)",
    re.DOTALL,
)


def extract_input_error_cause(e: duckdb.InvalidInputException) -> Optional[_Cause]:
    m = _input_error_pattern.match(str(e))
    if m:
        return _Cause(message=m.group(1), type_name=m.group(2))
    else:
        return None


@attrs.define
class DuckDBCompute(SQLCompute):
    session: "DuckDBPyConnection"
    is_debug: bool = attrs.field(init=False)
    created_views: typing.List[str] = attrs.field(init=False)
    offline_store_options: Iterable[OfflineStoreOptionsProvider] = ()

    @staticmethod
    def from_context(offline_store_options: Iterable[OfflineStoreOptionsProvider] = ()) -> "DuckDBCompute":
        return DuckDBCompute(
            session=DuckDBContext.get_instance().get_connection(), offline_store_options=offline_store_options
        )

    def __attrs_post_init__(self):
        self.is_debug = conf.get_bool("DUCKDB_DEBUG")
        self.created_views = []

    def run_sql(
        self,
        sql_string: str,
        return_dataframe: bool = False,
        expected_output_schema: Optional[Schema] = None,
        monitor: Optional[ComputeMonitor] = None,
    ) -> Optional[pyarrow.RecordBatchReader]:
        # Notes on case sensitivity:
        # 1. DuckDB is case insensitive when referring to column names, though preserves the
        #    underlying data casing when exporting to e.g. parquet.
        #    See https://duckdb.org/2022/05/04/friendlier-sql.html#case-insensitivity-while-maintaining-case
        #    This means that when using Snowflake for pipeline compute, the view + m13n schema is auto upper-cased
        # 2. When there is a spine provided, the original casing of that spine is used (since DuckDB separately
        #    registers the spine).
        # 3. When exporting values out of DuckDB (to user, or for ODFVs), we coerce the casing to respect the
        #    explicit schema specified. Thus ODFV definitions should reference the casing specified in the dependent
        #    FV's m13n schema.
        sql_string = sqlparse.format(sql_string, reindent=True)
        if self.is_debug:
            logging.warning(f"DUCKDB: run SQL {sql_string}")

        if monitor:
            monitor.set_query(sql_string)

        # Need to use DuckDB cursor (which creates a new connection based on the original connection)
        # to be thread-safe. It avoids a mysterious "unsuccessful or closed pending query result" error too.
        try:
            cursor = self.session.cursor()
            # Although we set timezone globally, DuckDB still needs this cursor-level config to produce
            # correct arrow result. Otherwise, timestamps in arrow table will have a local timezone.
            cursor.sql("SET TimeZone='UTC'")
            duckdb_relation = cursor.sql(sql_string)
            if return_dataframe:
                # increased batch_size (default value 1_000_000) should help Delta writer
                # to produce less fragmented files when data is not sorted by timestamp
                res = duckdb_relation.fetch_arrow_reader(batch_size=10_000_000)
            else:
                res = None

            return res
        except duckdb.InvalidInputException as e:
            # This means that the iterator we passed into DuckDB failed. If it failed due a TectonValidationError
            # we want to unwrap that to get rid of the noisy DuckDB context which is generally irrelevant to the
            # failure.
            cause = extract_input_error_cause(e)
            if not cause:
                raise
            for error_t in (CastError, TectonValidationError):
                if cause.type_name == error_t.__name__:
                    raise error_t(cause.message) from None
            raise
        except duckdb.Error as e:
            raise SQLCompilationError(str(e), sql_string) from None

        return None

    def get_dialect(self) -> Dialect:
        return Dialect.DUCKDB

    def register_temp_table_from_pandas(self, table_name: str, pandas_df: pd.DataFrame) -> None:
        self.session.from_df(pandas_df).create_view(table_name)
        self.created_views.append(table_name)

    def register_temp_table(
        self, table_name: str, table_or_reader: Union[pyarrow.Table, pyarrow.RecordBatchReader]
    ) -> None:
        self.session.from_arrow(table_or_reader).create_view(table_name)
        self.created_views.append(table_name)

    def register_temp_table_from_data_source(
        self,
        table_name: str,
        ds: DataSourceScanNode,
        secret_resolver: Optional[SecretResolver] = None,
        monitor: Optional[ComputeMonitor] = None,
    ) -> None:
        assert isinstance(
            ds.ds.batch_source,
            (
                FileSourceSpec,
                PushTableSourceSpec,
            ),
        ), "DuckDB compute supports only File and Push Table data sources"
        if isinstance(ds.ds.batch_source, FileSourceSpec):
            batch_source_spec = ds.ds.batch_source
            file_uri = batch_source_spec.uri
            timestamp_field = batch_source_spec.timestamp_field

            # ToDo: log loading progress via ComputeMonitor
            schema = Schema(ds.ds.schema.tecton_schema) if ds.ds.schema else None
            arrow_schema = tecton_schema_to_arrow_schema(schema) if schema else None
            if batch_source_spec.timestamp_format:
                # replace timestamp column type with string,
                # we will convert timestamp with DuckDB (see below)
                timestamp_pos = arrow_schema.names.index(timestamp_field)
                arrow_schema = arrow_schema.set(timestamp_pos, pyarrow.field(timestamp_field, pyarrow.string()))

            proto_format = batch_source_spec.file_format
            if proto_format == batch_data_source_pb2.FILE_DATA_SOURCE_FORMAT_CSV:
                arrow_format = "csv"
            elif proto_format == batch_data_source_pb2.FILE_DATA_SOURCE_FORMAT_JSON:
                arrow_format = "json"
            elif proto_format == batch_data_source_pb2.FILE_DATA_SOURCE_FORMAT_PARQUET:
                arrow_format = "parquet"
            else:
                raise ValueError(batch_data_source_pb2.FileDataSourceFormat.Name(batch_source_spec.file_format))

            fs, path = pyarrow.fs.FileSystem.from_uri(file_uri)
            if isinstance(fs, pyarrow.fs.S3FileSystem):
                options = BotoOfflineStoreOptionsProvider.static_options()
                if options is not None:
                    fs = pyarrow.fs.S3FileSystem(
                        access_key=options.access_key_id,
                        secret_key=options.secret_access_key,
                        session_token=options.session_token,
                        # When created via Filesystem.from_uri, the bucket region will be autodetected. This constructor
                        # does not have a bucket from which it can detect the region, so we need to copy it over from the
                        # previous instance.
                        region=fs.region,
                    )

            # There seems to be a bug in Arrow related to the explicit schema:
            # when we pass an explicit schema to `dataset` and both resolution and timezone in the timestamp column
            # don't match the schema in parquet files - filters that are pushed down by DuckDB will not work.
            # It is very likely that we will not guess both resolution and timezone correctly.
            # So we won't pass schema for now.
            arrow_schema = arrow_schema if arrow_format != "parquet" else None
            file_ds = pyarrow.dataset.dataset(source=path, schema=arrow_schema, filesystem=fs, format=arrow_format)
            if batch_source_spec.post_processor:
                reader = pyarrow.RecordBatchReader.from_batches(file_ds.schema, file_ds.to_batches())
                input_df = reader.read_pandas()
                try:
                    processed_df = batch_source_spec.post_processor(input_df)
                except Exception as exc:
                    msg = "Post processor function of data source " f"('{ds.ds.name}') " f"failed with exception"
                    raise UserCodeError(msg) from exc
                else:
                    relation = self.session.from_df(processed_df)
            else:
                relation = self.session.from_arrow(file_ds)

            column_types = dict(zip(relation.columns, relation.dtypes))

            if ds.start_time:
                if column_types[timestamp_field] == duckdb.typing.TIMESTAMP_TZ:
                    start_time = get_timezone_aware_datetime(ds.start_time)
                else:
                    start_time = ds.start_time.replace(tzinfo=None)
                relation = relation.filter(f"\"{timestamp_field}\" >= '{start_time}'")
            if ds.end_time:
                if column_types[timestamp_field] == duckdb.typing.TIMESTAMP_TZ:
                    end_time = get_timezone_aware_datetime(ds.end_time)
                else:
                    end_time = ds.end_time.replace(tzinfo=None)
                relation = relation.filter(f"\"{timestamp_field}\" < '{end_time}'")

            if batch_source_spec.timestamp_format:
                conversion_exp = f"strptime(\"{timestamp_field}\", '{batch_source_spec.timestamp_format}')"
                relation = relation.select(f'* REPLACE({conversion_exp} AS "{timestamp_field}")')

        elif isinstance(ds.ds.batch_source, PushTableSourceSpec):
            ds_id = id_helper.IdHelper.from_string(ds.ds.id)
            creds = next(
                filter(
                    lambda o: o is not None,
                    (p.get_s3_options_for_data_source(ds_id) for p in self.offline_store_options),
                ),
                None,
            )
            if not creds:
                msg = f"Unable to retrieve S3 store credentials for data source {ds.ds.name}"
                raise Exception(msg)
            storage_options = {
                "AWS_ACCESS_KEY_ID": creds.access_key_id,
                "AWS_SECRET_ACCESS_KEY": creds.secret_access_key,
                "AWS_SESSION_TOKEN": creds.session_token,
                "AWS_S3_LOCKING_PROVIDER": "dynamodb",
                "AWS_REGION": conf.get_or_raise("CLUSTER_REGION"),
            }
            saved_error = None
            for _ in range(20):
                try:
                    table = DeltaTable(
                        table_uri=ds.ds.batch_source.ingested_data_location, storage_options=storage_options
                    )
                    break
                except OSError as e:
                    saved_error = e
                    time.sleep(0.1)
            else:
                msg = "Failed to read from S3"
                raise TimeoutError(msg) from saved_error
            df = table.to_pyarrow_dataset()
            relation = self.session.from_arrow(df)
        else:
            msg = "DuckDB compute supports only File data sources and Push Table data sources"
            raise Exception(msg)

        relation.create_view(table_name)
        self.created_views.append(table_name)

    def load_table(self, table_name: str, expected_output_schema: Optional[Schema] = None) -> pyarrow.RecordBatchReader:
        return self.run_sql(
            f"select * from {table_name}", return_dataframe=True, expected_output_schema=expected_output_schema
        )

    def run_odfv(
        self, qt_node: NodeRef, input_df: pd.DataFrame, monitor: Optional[ComputeMonitor] = None
    ) -> pd.DataFrame:
        # TODO: leverage duckdb udfs
        pass

    def cleanup_temp_tables(self):
        for view in self.created_views:
            self.session.unregister(view)
        self.created_views = []
