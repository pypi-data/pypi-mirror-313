import dataclasses
import logging
import re
import time
import typing
import uuid
from datetime import datetime
from functools import reduce
from operator import and_
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
import pyarrow.compute as pc


try:
    import duckdb
except ImportError:
    msg = (
        "Couldn't initialize Rift compute. "
        "To use Rift install all Rift dependencies first by executing `pip install tecton[rift]`."
    )
    raise RuntimeError(msg)
import pandas
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
from tecton_core.offline_store import JoinKeyBoundaries
from tecton_core.offline_store import OfflineStoreOptionsProvider
from tecton_core.query.dialect import Dialect
from tecton_core.query.errors import SQLCompilationError
from tecton_core.query.errors import UserCodeError
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.query_tree_compute import ComputeMonitor
from tecton_core.query.query_tree_compute import SQLCompute
from tecton_core.schema import Schema
from tecton_core.schema_validation import CastError
from tecton_core.schema_validation import tecton_schema_to_arrow_schema
from tecton_core.secrets import SecretResolver
from tecton_core.specs import DatetimePartitionColumnSpec
from tecton_core.specs import FileSourceSpec
from tecton_core.specs import PushTableSourceSpec
from tecton_core.time_utils import get_timezone_aware_datetime
from tecton_proto.data import batch_data_source__client_pb2 as batch_data_source_pb2


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


ARROW_TYPE_TO_DUCKDB_TYPE = {
    pyarrow.int32(): duckdb.dtype("INTEGER"),
    pyarrow.int64(): duckdb.dtype("LONG"),
    pyarrow.float32(): duckdb.dtype("FLOAT"),
    pyarrow.float64(): duckdb.dtype("DOUBLE"),
    pyarrow.string(): duckdb.dtype("STRING"),
    pyarrow.bool_(): duckdb.dtype("BOOLEAN"),
    pyarrow.timestamp("ns"): duckdb.dtype("TIMESTAMP"),
    pyarrow.timestamp("us"): duckdb.dtype("TIMESTAMP"),
    pyarrow.timestamp("ms"): duckdb.dtype("TIMESTAMP"),
    pyarrow.timestamp("ns", "UTC"): duckdb.dtype("TIMESTAMPTZ"),
    pyarrow.timestamp("us", "UTC"): duckdb.dtype("TIMESTAMPTZ"),
    pyarrow.timestamp("ms", "UTC"): duckdb.dtype("TIMESTAMPTZ"),
    pyarrow.date32(): duckdb.dtype("DATE"),
    pyarrow.date64(): duckdb.dtype("DATE"),
}


def _arrow_type_to_duckdb_type(arrow_type: pyarrow.DataType) -> duckdb.duckdb.typing.DuckDBPyType:
    if isinstance(arrow_type, pyarrow.ListType):
        return duckdb.list_type(_arrow_type_to_duckdb_type(arrow_type.value_type))

    if isinstance(arrow_type, pyarrow.MapType):
        return duckdb.map_type(
            _arrow_type_to_duckdb_type(arrow_type.key_type),
            _arrow_type_to_duckdb_type(arrow_type.value_type),
        )

    if isinstance(arrow_type, pyarrow.StructType):
        return duckdb.struct_type({field.name: _arrow_type_to_duckdb_type(field.type) for field in arrow_type})

    return ARROW_TYPE_TO_DUCKDB_TYPE[arrow_type]


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
                if error_t.__name__ in cause.type_name:
                    raise error_t(cause.message) from None
            raise
        except duckdb.Error as e:
            raise SQLCompilationError(str(e), sql_string) from None

    def get_dialect(self) -> Dialect:
        return Dialect.DUCKDB

    def register_temp_table_from_pandas(self, table_name: str, pandas_df: pandas.DataFrame) -> None:
        self.session.from_df(pandas_df).create_view(table_name)
        self.created_views.append(table_name)

    def register_temp_table(
        self, table_name: str, table_or_reader: Union[pyarrow.Table, pyarrow.RecordBatchReader]
    ) -> None:
        self.session.from_arrow(table_or_reader).create_view(table_name)
        self.created_views.append(table_name)

    def register_temp_table_from_offline_store(
        self,
        table_name: str,
        dataset: pyarrow.dataset.Dataset,
        join_keys_filter: Optional[Dict[str, JoinKeyBoundaries]],
        join_keys_table: Optional[pyarrow.Table],
    ) -> None:
        """
        Read an offline store (Delta or Parquet) using DuckDB's Parquet reader.
        Although this function receives pyarrow.Dataset, we don't actually use pyarrow to read the data.
        `pyarrow.Dataset` is just a container with a list of files (fragments) and a schema.
        Pyarrow's schema is converted into DuckDB types to verify that loaded data is consistent with expected schema.

        We use Python wrappers around DuckDB's relational API (https://duckdb.org/docs/api/python/relational_api)
        instead of SQL query, because it's easier to pass join keys filters this way.

        We also need to register S3 credentials in DuckDB to authenticate its Parquet reader.
        See docs for secrets API https://duckdb.org/docs/extensions/httpfs/s3api
        """
        if join_keys_table and join_keys_filter:
            conditions = []
            for col, boundaries in join_keys_filter.items():
                conditions.append(pc.field(col).isin(join_keys_table[col]))
                conditions.append((pc.field(col) >= boundaries.min) & (pc.field(col) <= boundaries.max))

            batches = dataset.to_batches(filter=reduce(and_, conditions))
        else:
            batches = dataset.to_batches()

        reader = pyarrow.RecordBatchReader.from_batches(dataset.schema, batches)
        relation = self.session.from_arrow(reader)
        relation.create_view(table_name)

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

            schema = Schema(ds.ds.schema.tecton_schema) if ds.ds.schema else None
            arrow_schema = tecton_schema_to_arrow_schema(schema) if schema else None
            if batch_source_spec.timestamp_format and arrow_schema:
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

            partitioning = None
            partition_filter = None
            # If source supports partitions then only read the relevant partitions
            if (ds.start_time or ds.end_time) and ds.ds.batch_source.datetime_partition_columns:
                partition_fields = []
                filter_conditions = []
                for i, partition in enumerate(ds.ds.batch_source.datetime_partition_columns):
                    partition_col = partition.column_name if partition.column_name else f"_dir_partition_{i}"
                    partition_type = None
                    partition_value_at_start = None
                    partition_value_at_end = None

                    if ds.start_time:
                        partition_value_at_start, partition_type = _partition_value_and_type_for_time(
                            partition, ds.start_time
                        )
                    if ds.end_time:
                        partition_value_at_end, partition_type = _partition_value_and_type_for_time(
                            partition, ds.end_time
                        )

                    if partition_value_at_start == partition_value_at_end:
                        # Use the partition path to reduce scanning for metadata when initializing the dataset
                        hive_key = f"{partition.column_name}=" if partition.column_name else ""
                        partition_value = ds.start_time.strftime(partition.format_string)
                        path = path.rstrip("/") + f"/{hive_key}{ds.start_time.strftime(partition_value)}"
                    else:
                        # Otherwise we use a range filter and break so we don't combine hierarchical partition filters
                        partition_fields.append(pyarrow.field(partition_col, partition_type))
                        filter_conditions.append((pyarrow.dataset.field(partition_col) >= partition_value_at_start))
                        filter_conditions.append((pyarrow.dataset.field(partition_col) <= partition_value_at_end))
                        # TODO: combine range filters on hierarchical partitions using nested 'Or' filters
                        break

                # Setup dataset partitioning if we used partition range filters
                if partition_fields:
                    partitioning = pyarrow.dataset.partitioning(
                        pyarrow.schema(partition_fields),
                        # default is a directory partition
                        flavor="hive" if ds.ds.batch_source.datetime_partition_columns[0].column_name else None,
                    )
                    partition_filter = reduce(and_, filter_conditions)

            file_dataset = pyarrow.dataset.dataset(
                source=path, schema=arrow_schema, filesystem=fs, format=arrow_format, partitioning=partitioning
            )

            if batch_source_spec.post_processor:
                reader = pyarrow.RecordBatchReader.from_batches(
                    file_dataset.schema, file_dataset.to_batches(filter=partition_filter)
                )
                input_df = reader.read_pandas()
                try:
                    processed_df = batch_source_spec.post_processor(input_df)
                except Exception as exc:
                    msg = "Post processor function of data source " f"('{ds.ds.name}') " f"failed with exception"
                    raise UserCodeError(msg) from exc
                else:
                    relation = self.session.from_df(processed_df)
            else:
                reader = pyarrow.RecordBatchReader.from_batches(
                    file_dataset.schema, file_dataset.to_batches(filter=partition_filter)
                )
                relation = self.session.from_arrow(reader)

            column_types = dict(zip(relation.columns, relation.dtypes))

            if column_types[timestamp_field] == duckdb.typing.VARCHAR:
                if batch_source_spec.timestamp_format:
                    conversion_exp = f"strptime(\"{timestamp_field}\", '{batch_source_spec.timestamp_format}')"
                else:
                    conversion_exp = f'CAST("{timestamp_field}" AS TIMESTAMP)'
                relation = relation.select(f'* REPLACE({conversion_exp} AS "{timestamp_field}")')

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

    def load_from_data_source(
        self,
        ds: DataSourceScanNode,
        expected_output_schema: Optional[Schema] = None,
        secret_resolver: Optional[SecretResolver] = None,
        monitor: Optional[ComputeMonitor] = None,
    ) -> pyarrow.RecordBatchReader:
        tmp_table_name = f"TEMP_{ds.node_id.hex[:10]}_{uuid.uuid4().hex[:5]}"
        self.register_temp_table_from_data_source(
            tmp_table_name,
            ds,
            secret_resolver,
            monitor,
        )
        return self.load_table(tmp_table_name, expected_output_schema)

    def cleanup_temp_tables(self):
        for view in self.created_views:
            self.session.unregister(view)
        self.created_views = []


def _duckdb_value(v: Union[str, int, float]) -> duckdb.Value:
    if isinstance(v, str):
        return duckdb.StringValue(v)

    if isinstance(v, int):
        return duckdb.IntegerValue(v)

    if isinstance(v, float):
        return duckdb.DoubleValue(v)

    msg = f"Unsupported value type {type(v)} for value: {v}"
    raise TypeError(msg)


def _partition_value_and_type_for_time(
    partition: DatetimePartitionColumnSpec, dt: datetime
) -> Tuple[Union[int, datetime.date], pyarrow.DataType]:
    fmt = partition.format_string
    if fmt == "%-Y" or fmt == "%Y":
        return dt.year, pyarrow.int32()
    elif fmt == "%-m" or fmt == "%m":
        return dt.month, pyarrow.int32()
    elif fmt == "%-d" or fmt == "%d":
        return dt.day, pyarrow.int32()
    elif fmt == "%-H" or fmt == "%H":
        return dt.hour, pyarrow.int32()
    elif fmt == "%Y-%m-%d":
        return dt.date(), pyarrow.date32()
    else:
        msg = f"Datetime format `{fmt}` not supported for partition column {partition.column_name}"
        raise ValueError(msg)
