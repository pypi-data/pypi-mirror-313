import contextlib
import logging
import time
import typing
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import attrs
import numpy
import pandas
import pyspark
import pytz

import tecton_core.query.dialect
from tecton._internals.offline_store_credentials import INTERACTIVE_OFFLINE_STORE_OPTIONS_PROVIDERS
from tecton._internals.pandas_compat import pandas_to_spark
from tecton._internals.rewrite import rewrite_tree_for_spine
from tecton._internals.sdk_decorators import sdk_public_method
from tecton._internals.secret_resolver import LocalDevSecretResolver
from tecton.snowflake_context import SnowflakeContext
from tecton_athena import athena_session
from tecton_athena.data_catalog_helper import register_feature_view_as_athena_table_if_necessary
from tecton_athena.query.translate import AthenaSqlExecutor
from tecton_athena.query.translate import athena_convert
from tecton_core import data_types
from tecton_core.compute_mode import ComputeMode
from tecton_core.query.dialect import Dialect
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.node_interface import DataframeWrapper
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import recurse_query_tree
from tecton_core.query.node_utils import get_first_input_node_of_class
from tecton_core.query.node_utils import get_pipeline_dialect
from tecton_core.query.node_utils import get_staging_nodes
from tecton_core.query.node_utils import tree_contains
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import MultiOdfvPipelineNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import StagingNode
from tecton_core.query.nodes import UserSpecifiedDataNode
from tecton_core.query.pandas import node
from tecton_core.schema import Schema
from tecton_core.time_utils import convert_pandas_df_for_snowflake_upload
from tecton_spark import schema_spark_utils
from tecton_spark.query import translate
from tecton_spark.type_annotations import PySparkDataFrame
from tecton_spark.type_annotations import PySparkSession
from tecton_spark.type_annotations import is_pyspark_df


if typing.TYPE_CHECKING:
    import snowflake.snowpark

logger = logging.getLogger(__name__)

# We have to use Any here because snowflake.snowpark.DataFrame is not a direct dependency of the SDK.
snowpark_dataframe = Any

_internal_index_column = "_tecton_internal_index_col"


def set_pandas_timezone_from_spark(pandas_df):
    """Match pandas timezone to that of Spark, s.t. the timestamps are correctly displayed."""
    from tecton.tecton_context import TectonContext

    tz = TectonContext.get_instance()._spark.conf.get("spark.sql.session.timeZone")
    for col in pandas_df.columns:
        if pandas.core.dtypes.common.is_datetime64_dtype(pandas_df[col]):
            pandas_df[col] = pandas_df[col].dt.tz_localize(pytz.timezone(tz))
            pandas_df[col] = pandas_df[col].dt.tz_convert(pytz.timezone("UTC"))
            pandas_df[col] = pandas_df[col].dt.tz_localize(None)
    return pandas_df


def _remove_timezones(df: pandas.DataFrame) -> pandas.DataFrame:
    for col in df.columns:
        if pandas.core.dtypes.common.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)
    return df


@attrs.define(auto_attribs=True)
class FeatureVector(object):
    """
    FeatureVector Class.

    A FeatureVector is a representation of a single feature vector. Usage of a FeatureVector typically involves
    extracting the feature vector using ``to_pandas()``, ``to_dict()``, or ``to_numpy()``.

    """

    _names: List[str]
    _values: List[Union[int, str, bytes, float, list]]
    _effective_times: List[Optional[datetime]]
    slo_info: Optional[Dict[str, str]] = None

    @sdk_public_method
    def to_dict(
        self, return_effective_times: bool = False
    ) -> Dict[str, Union[int, str, bytes, float, list, dict, None]]:
        """Turns vector into a Python dict.

        :param: return_effective_times: Whether to return the effective time of the feature.

        :return: A Python dict.
        """
        if return_effective_times:
            return {
                name: {"value": self._values[i], "effective_time": self._effective_times[i]}
                for i, name in enumerate(self._names)
            }

        return dict(zip(self._names, self._values))

    @sdk_public_method
    def to_pandas(self, return_effective_times: bool = False) -> pandas.DataFrame:
        """Turns vector into a Pandas DataFrame.

        :param: return_effective_times: Whether to return the effective time of the feature as part of the DataFrame.

        :return: A Pandas DataFrame.
        """
        if return_effective_times:
            return pandas.DataFrame(
                list(zip(self._names, self._values, self._effective_times)), columns=["name", "value", "effective_time"]
            )

        return pandas.DataFrame([self._values], columns=self._names)

    @sdk_public_method
    def to_numpy(self, return_effective_times: bool = False) -> numpy.array:
        """Turns vector into a numpy array.

        :param: return_effective_times: Whether to return the effective time of the feature as part of the list.

        :return: A numpy array.
        """
        if return_effective_times:
            return numpy.array([self._values, self._effective_times])

        return numpy.array(self._values)

    def _update(self, other: "FeatureVector"):
        self._names.extend(other._names)
        self._values.extend(other._values)
        self._effective_times.extend(other._effective_times)


# NOTE: use repr=False to avoid printing out the underlying dataframes when used in REPL/notebook.
@attrs.define(repr=False)
class TectonDataFrame(DataframeWrapper):
    """
    A thin wrapper around Pandas, Spark, and Snowflake dataframes.
    """

    _spark_df: Optional[PySparkDataFrame] = None
    _pandas_df: Optional[pandas.DataFrame] = None
    # TODO: Change the type to snowflake.snowpark.DataFrame, currently it will
    # fail type checking for our auto generated doc.
    _snowflake_df: Optional[Any] = None
    # should already by optimized
    _querytree: Optional[NodeRef] = attrs.field(default=None, repr=lambda x: "TectonQueryTree")

    # _schema is the schema of TectonDataFrame. It is present only if the TectonDataFrame is built from a pandas
    # dataframe as a spine and it is used when converting a pandas datafarme to a spark dataframe. Note the _schema only
    # contains the name and data type for those columns Tecton manages. If the spine contains extra columns like `label`
    # etc, those columns are converted to their default spark data types.
    _schema: Optional[Schema] = None

    @sdk_public_method
    def explain(
        self,
        node_id: bool = True,
        name: bool = True,
        description: bool = True,
        columns: bool = False,
    ):
        """Prints the query tree. Should only be used when this TectonDataFrame is backed by a query tree.

        Args:
            node_id: If True, the unique id associated with each node will be rendered.
            name: If True, the class names of the nodes will be rendered.
            description: If True, the actions of the nodes will be rendered.
            columns: If True, the columns of each node will be rendered as an appendix after tree itself.
        """
        if self._querytree:
            if not name and not description:
                msg = "At least one of 'name' or 'description' must be True."
                raise RuntimeError(msg)
            if columns and not node_id:
                msg = "Can only show columns if 'node_id' is True."
                raise RuntimeError(msg)
            print(self._querytree.pretty_str(node_id=node_id, name=name, description=description, columns=columns))
        else:
            print("Explain is only available for TectonDataFrames backed by a query tree.")

    @sdk_public_method
    def to_spark(self) -> PySparkDataFrame:
        """Returns data as a Spark DataFrame.

        :return: A Spark DataFrame.
        """
        if self._spark_df is not None:
            return self._spark_df
        else:
            from tecton.tecton_context import TectonContext

            tc = TectonContext.get_instance()
            if self._querytree is not None:
                return self._to_spark(tc._spark)
            elif self._pandas_df is not None:
                if self._schema is not None:
                    extra_columns = list(set(self._pandas_df.columns) - set(self._schema.column_names()))
                    if len(extra_columns) == 0:
                        pdf = self._pandas_df[self._schema.column_names()]
                        return pandas_to_spark(tc._spark, pdf, schema=schema_spark_utils.schema_to_spark(self._schema))
                    else:
                        # If there are extra columns beyond Tecton's management sopce, it splits the spine into two
                        # parts:
                        #   1. sub_df_1, which contains Tecton managed columns, is built with explicit schema.
                        #   2. sub_df_2, which contains those extra columns, is built with spark default schema(no
                        #      explicit schema passed in.
                        # Eventually these two parts are joined together using an internal index column, which is
                        # dropped afterwards. Note the join operation isn't expensive here given it is backed by a
                        # pandas dataframe that is already loaded into memory.
                        pdf = self._pandas_df.rename_axis(_internal_index_column).reset_index()
                        pdf_schema = self._schema + Schema.from_dict({_internal_index_column: data_types.Int64Type()})
                        sub_df_1 = pandas_to_spark(
                            tc._spark,
                            pdf[pdf_schema.column_names()],
                            schema=schema_spark_utils.schema_to_spark(pdf_schema),
                        )
                        sub_df_2 = pandas_to_spark(tc._spark, pdf[[_internal_index_column, *extra_columns]])
                        return sub_df_1.join(sub_df_2, on=_internal_index_column).drop(_internal_index_column)
                else:
                    return pandas_to_spark(tc._spark, self._pandas_df)
            else:
                raise NotImplementedError

    @sdk_public_method
    def to_pandas(self, pretty_sql: bool = False) -> pandas.DataFrame:
        """Returns data as a Pandas DataFrame.

         Args:
            pretty_sql: Not applicable when using spark. For Snowflake and Athena, to_pandas() will generate a SQL string, execute it, and then return the resulting data in a pandas DataFrame.
            If True, the sql will be reformatted and executed as a more readable,
            multiline string. If False, the SQL will be executed as a one line string. Use pretty_sql=False for better performance.

        :return: A Pandas DataFrame.
        """
        if self._pandas_df is not None:
            return self._pandas_df

        assert self._spark_df is not None or self._snowflake_df is not None or self._querytree is not None

        if self._spark_df is not None:
            return set_pandas_timezone_from_spark(self._spark_df.toPandas())

        if self._snowflake_df is not None:
            return self._snowflake_df.to_pandas(statement_params={"SF_PARTNER": "tecton-ai"})

        if self._querytree is not None:
            if self._compute_mode == ComputeMode.ATHENA:
                output = self._to_pandas_from_athena(pretty_sql)
            elif self._compute_mode == ComputeMode.RIFT:
                output = _remove_timezones(self._to_pandas_from_duckdb(pretty_sql))
            elif self._compute_mode == ComputeMode.SNOWFLAKE:
                output = self._to_pandas_from_snowflake(pretty_sql)
            elif self._compute_mode == ComputeMode.SPARK:
                output = set_pandas_timezone_from_spark(self.to_spark().toPandas())
            else:
                raise ValueError(self._compute_mode)
            # Cache this since it's important to keep this around. We call this method repeatedly e.g. to do spine
            # validation, infer timestamps, etc. We also generate a unique id based on this object and rely on that
            # to be stable.
            self._pandas_df = output
            return output

    @property
    def _compute_mode(self):
        assert self._querytree is not None, "Must be called on a QueryTree DataFrame"
        return self._querytree.node.compute_mode

    def _to_spark(self, spark: PySparkSession) -> PySparkDataFrame:
        return translate.spark_convert(self._querytree, spark).to_dataframe(spark)

    def _to_pandas_from_duckdb(self, pretty_sql: bool) -> pandas.DataFrame:
        from tecton_core.query import query_tree_executor

        # TODO(danny): support pretty_sql
        fv_dialect = get_pipeline_dialect(self._querytree)
        if fv_dialect is not None and fv_dialect not in (
            Dialect.SNOWFLAKE,
            Dialect.PANDAS,
        ):
            msg = f"Rift does not support feature views of {fv_dialect.value} dialect."
            raise Exception(msg)

        executor = query_tree_executor.QueryTreeExecutor(
            secret_resolver=LocalDevSecretResolver(),
            offline_store_options_providers=INTERACTIVE_OFFLINE_STORE_OPTIONS_PROVIDERS,
        )

        qt_output_df = executor.exec_qt(self._querytree).result_df
        return qt_output_df

    def _to_pandas_from_athena(self, pretty_sql: bool) -> pandas.DataFrame:
        with self._register_tables(tecton_core.query.dialect.Dialect.ATHENA):
            session = athena_session.get_session()
            recurse_query_tree(
                self._querytree,
                lambda node: register_feature_view_as_athena_table_if_necessary(
                    node.feature_definition_wrapper, session
                )
                if isinstance(node, OfflineStoreScanNode)
                else None,
            )
            views = self._register_querytree_views_or_tables(pretty_sql=pretty_sql)
            try:
                athena_sql_executor = AthenaSqlExecutor(session)
                df = athena_convert(self._querytree, athena_sql_executor, pretty_sql).to_dataframe()
            finally:
                # A tree and its subtree can share the same temp tables. If to_pandas() is called
                # concurrently, tables can be deleted when they are still being used by the other tree.
                for view_name, _ in views:
                    session.delete_view_if_exists(view_name)
            return df

    def _to_pandas_from_snowflake(self, pretty_sql: bool) -> pandas.DataFrame:
        with self._register_tables(tecton_core.query.dialect.Dialect.SNOWFLAKE):
            return self._get_snowflake_exec_node(pretty_sql=pretty_sql).to_dataframe()

    def _get_snowflake_exec_node(self, pretty_sql: bool) -> node.SqlExecNode:
        """Helper method used to create Snowflake QT"""
        from tecton_snowflake.query.translate import SnowparkExecutor
        from tecton_snowflake.query.translate import snowflake_convert

        # TODO(TEC-15833): This requires snowpark. Decide if we will allow a snowflake connection instead of snowpark session
        snowflake_session = SnowflakeContext.get_instance().get_session()
        snowpark_executor = SnowparkExecutor(snowflake_session)
        # This rewrites the tree and needs to be called before registering temp tables/views.
        sql_exec_node = snowflake_convert(self._querytree, snowpark_executor, pretty_sql=pretty_sql)

        views = self._register_querytree_views_or_tables(pretty_sql=pretty_sql)
        return sql_exec_node

    def _to_sql(self, pretty_sql: bool = False):
        if self._querytree is not None:
            if tree_contains(self._querytree, MultiOdfvPipelineNode):
                # SQL is not available for ODFVs. Showing SQL only for the subtree below the ODFV pipeline
                subtree = self.get_sql_node(self._querytree)
                return subtree.to_sql(pretty_sql=pretty_sql)
            else:
                return self._querytree.to_sql(pretty_sql=pretty_sql)
        else:
            raise NotImplementedError

    def get_sql_node(self, tree: NodeRef):
        # Returns the first node from which SQL can be generated(subtree below ODFV pipeline)
        can_be_pushed = (
            MultiOdfvPipelineNode,
            RenameColsNode,
        )
        if isinstance(tree.node, can_be_pushed):
            return self.get_sql_node(tree.node.input_node)
        return tree

    @contextlib.contextmanager
    def _register_tables(self, dialect: tecton_core.query.dialect.Dialect):
        tables = set()

        def maybe_register_temp_table(node):
            if isinstance(node, UserSpecifiedDataNode):
                assert isinstance(node.data, TectonDataFrame), "Must be called with a TectonDataFrame"
                # Don't register the same table twice
                if node.data._temp_table_name not in tables:
                    tmp_table_name = node.data._register_temp_table(dialect)
                    tables.add(tmp_table_name)

        recurse_query_tree(
            self._querytree,
            maybe_register_temp_table,
        )

        try:
            yield
        finally:
            self._drop_temp_tables(dialect, tables)

    def _get_querytree_sql_views(self, pretty_sql=False):
        qt_views = []
        recurse_query_tree(self._querytree, lambda node: qt_views.extend(node.get_sql_views(pretty_sql=pretty_sql)))
        return qt_views

    def _register_querytree_views_or_tables(self, pretty_sql=False) -> typing.Sequence[Tuple[str, str]]:
        views = self._get_querytree_sql_views(pretty_sql=pretty_sql)
        if self._compute_mode == ComputeMode.ATHENA:
            session = athena_session.get_session()
            for view_name, view_sql in views:
                session.create_view(view_sql, view_name)
        elif self._compute_mode == ComputeMode.SNOWFLAKE:
            import tecton_snowflake.query.dataframe_helper as snowflake_dataframe_helper

            snowpark_session = SnowflakeContext.get_instance().get_session()
            snowflake_dataframe_helper.register_temp_views_or_tables(views=views, snowpark_session=snowpark_session)
        else:
            raise ValueError(self._compute_mode)
        return views

    def _to_snowpark_from_snowflake(self, pretty_sql: bool) -> snowpark_dataframe:
        with self._register_tables(tecton_core.query.dialect.Dialect.SNOWFLAKE):
            return self._get_snowflake_exec_node(pretty_sql=pretty_sql).to_snowpark()

    @sdk_public_method
    def to_snowpark(self, pretty_sql: bool = False) -> snowpark_dataframe:
        """
        Returns data as a Snowpark DataFrame.

        Args:
            pretty_sql: to_snowpark() will generate a SQL string, execute it, and then return the resulting data in a snowpark DataFrame.
            If True, the sql will be reformatted and executed as a more readable, multiline string.
            If False, the SQL will be executed as a one line string. Use pretty_sql=False for better performance.

        :return: A Snowpark DataFrame.
        """
        if self._snowflake_df is not None:
            return self._snowflake_df

        if self._querytree is not None and self._compute_mode == ComputeMode.SNOWFLAKE:
            return self._to_snowpark_from_snowflake(pretty_sql)

        assert self._pandas_df is not None
        return SnowflakeContext.get_instance().get_session().createDataFrame(self._pandas_df)

    @classmethod
    def _create(
        cls,
        df: Union[PySparkDataFrame, pandas.DataFrame, NodeRef],
        rewrite: bool = True,
    ):
        """Creates a Tecton DataFrame from a Spark or Pandas DataFrame."""
        if isinstance(df, pandas.DataFrame):
            return cls(spark_df=None, pandas_df=df, snowflake_df=None)
        elif is_pyspark_df(df):
            return cls(spark_df=df, pandas_df=None, snowflake_df=None)
        elif isinstance(df, NodeRef):
            if rewrite:
                rewrite_tree_for_spine(df)
            return cls(spark_df=None, pandas_df=None, snowflake_df=None, querytree=df)

        msg = f"DataFrame must be of type pandas.DataFrame or pyspark.sql.Dataframe, not {type(df)}"
        raise TypeError(msg)

    @classmethod
    def _create_from_pandas_with_schema(cls, df: pandas.DataFrame, schema: Schema):
        if isinstance(df, pandas.DataFrame):
            return cls(spark_df=None, pandas_df=df, snowflake_df=None, schema=schema)
        msg = f"DataFrame must be pandas.DataFrame when using _create_from_pandas, not {type(df)}"
        raise TypeError(msg)

    @classmethod
    # This should be merged into _create once snowpark is installed with pip
    def _create_with_snowflake(cls, df: "snowflake.snowpark.DataFrame"):
        """Creates a Tecton DataFrame from a Snowflake DataFrame."""
        from snowflake.snowpark import DataFrame as SnowflakeDataFrame

        if isinstance(df, SnowflakeDataFrame):
            return cls(spark_df=None, pandas_df=None, snowflake_df=df)

        msg = f"DataFrame must be of type snowflake.snowpark.Dataframe, not {type(df)}"
        raise TypeError(msg)

    @classmethod
    def _create_with_snowflake_sql(cls, sql: str):
        if isinstance(sql, str):
            return cls(
                spark_df=None, pandas_df=None, snowflake_df=SnowflakeContext.get_instance().get_session().sql(sql)
            )

        msg = f"sql must be of type str, not {type(sql)}"
        raise TypeError(msg)

    def subtree(self, node_id: int) -> "TectonDataFrame":
        """Creates a TectonDataFrame from a subtree of prior querytree labeled by a node id in .explain()."""
        if not self._querytree:
            msg = "Cannot construct a TectonDataFrame from a node id."
            raise RuntimeError(msg)

        tree = self._querytree.create_tree()
        qt_root = NodeRef(tree.get_node(node_id).data)

        if self._compute_mode == ComputeMode.RIFT:
            # Rift requires StagingNodes to properly execute a querytree with a DataSourceScanNode or a
            # FeatureViewPipelineNode. If a StagingNode is not present, we add one.
            data_source_staging_nodes = get_staging_nodes(qt_root, QueryTreeStep.DATA_SOURCE)
            data_source_scan_node = get_first_input_node_of_class(qt_root, node_class=DataSourceScanNode)
            pipeline_staging_nodes = get_staging_nodes(qt_root, QueryTreeStep.PIPELINE)
            feature_view_pipeline_node = get_first_input_node_of_class(qt_root, node_class=FeatureViewPipelineNode)
            if len(data_source_staging_nodes) == 0 and data_source_scan_node is not None:
                staging_node = StagingNode(
                    dialect=Dialect.DUCKDB,
                    compute_mode=ComputeMode.RIFT,
                    input_node=qt_root.deepcopy(),
                    staging_table_name=data_source_scan_node.ds.name,
                    query_tree_step=QueryTreeStep.DATA_SOURCE,
                )
                qt_root.node = staging_node
            elif len(pipeline_staging_nodes) == 0 and feature_view_pipeline_node is not None:
                staging_node = StagingNode(
                    dialect=Dialect.DUCKDB,
                    compute_mode=ComputeMode.RIFT,
                    input_node=qt_root.deepcopy(),
                    staging_table_name=feature_view_pipeline_node.feature_definition_wrapper.name,
                    query_tree_step=QueryTreeStep.PIPELINE,
                )
                qt_root.node = staging_node

        # Do not apply rewrites again as they should have already been applied when generating the query tree for this
        # TectonDataFrame.
        return TectonDataFrame._create(qt_root, rewrite=False)

    def _timed_to_pandas(self):
        """Convenience method for measuring performance."""
        start = time.time()
        ret = self.to_spark().toPandas()
        end = time.time()
        print(f"took {end - start} seconds")
        return ret

    # The methods below implement the DataframeWrapper interface
    def _register_temp_table(self, dialect: tecton_core.query.dialect.Dialect):
        if dialect == tecton_core.query.dialect.Dialect.SPARK:
            self.to_spark().createOrReplaceTempView(self._temp_table_name)
            return
        if dialect == tecton_core.query.dialect.Dialect.ATHENA:
            session = athena_session.get_session()
            session.write_pandas(self.to_pandas(), self._temp_table_name)
        elif dialect == tecton_core.query.dialect.Dialect.SNOWFLAKE:
            session = SnowflakeContext.get_instance().get_session()
            if self._snowflake_df:
                self._snowflake_df.write.mode("overwrite").save_as_table(
                    table_name=self._temp_table_name, table_type="temporary"
                )
            else:
                df_to_write = self.to_pandas()
                convert_pandas_df_for_snowflake_upload(df_to_write)
                session.write_pandas(
                    df_to_write,
                    table_name=self._temp_table_name,
                    auto_create_table=True,
                    table_type="temporary",
                    quote_identifiers=False,
                    overwrite=True,
                    parallel=64,
                    chunk_size=1000000,
                    use_logical_type=True,
                )
        elif dialect == tecton_core.query.dialect.Dialect.DUCKDB:
            from tecton_core.duckdb_context import DuckDBContext

            pandas_df = self.to_pandas()
            connection = DuckDBContext.get_instance().get_connection()
            connection.sql(f"CREATE OR REPLACE TABLE {self._temp_table_name} AS SELECT * FROM pandas_df")
        else:
            msg = f"Unexpected dialect {dialect}"
            raise Exception(msg)

        return self._temp_table_name

    def _drop_temp_tables(self, dialect: tecton_core.query.dialect.Dialect, tables: typing.Collection[str]):
        if dialect == tecton_core.query.dialect.Dialect.ATHENA:
            session = athena_session.get_session()
            for temp_table in tables:
                session.delete_table_if_exists(session.get_database(), temp_table)
        elif dialect == tecton_core.query.dialect.Dialect.SPARK:
            from tecton.tecton_context import TectonContext

            spark = TectonContext.get_instance()._spark
            for temp_table in tables:
                # DROP VIEW/DROP TABLE sql syntax is invalidated when spark_catalog is set to DeltaCatalog on EMR clusters
                if (
                    spark.conf.get("spark.sql.catalog.spark_catalog", "")
                    == "org.apache.spark.sql.delta.catalog.DeltaCatalog"
                ):
                    spark.catalog.dropTempView(temp_table)
                else:
                    spark.sql(f"DROP VIEW IF EXISTS {temp_table}")
        elif dialect == tecton_core.query.dialect.Dialect.SNOWFLAKE:
            # Snowpark automatically drops temp views when the session ends
            # All other temp views/tables are created with 'overwrite' mode
            pass

    def _select_distinct(self, columns: List[str]) -> DataframeWrapper:
        if self._pandas_df is not None:
            return TectonDataFrame._create(self._pandas_df[columns].drop_duplicates())
        elif self._spark_df is not None:
            return TectonDataFrame._create(self._spark_df.select(columns).distinct())
        else:
            raise NotImplementedError

    @property
    def _dataframe(self) -> Union[pyspark.sql.DataFrame, pandas.DataFrame]:
        if self._spark_df is not None:
            return self._spark_df
        elif self._pandas_df is not None:
            return self._pandas_df
        elif self._snowflake_df is not None:
            return self._snowflake_df
        elif self._querytree:
            if self._compute_mode == ComputeMode.SPARK:
                return self.to_spark()
            else:
                return self.to_pandas()
        else:
            raise NotImplementedError

    @property
    def columns(self) -> Sequence[str]:
        if self._querytree:
            return self._querytree.columns
        elif self._spark_df is not None:
            return self._spark_df.columns
        elif self._pandas_df is not None:
            return list(self._pandas_df.columns)
        elif self._snowflake_df is not None:
            return self._snowflake_df.columns
        else:
            raise NotImplementedError


# for legacy compat
DataFrame = TectonDataFrame
