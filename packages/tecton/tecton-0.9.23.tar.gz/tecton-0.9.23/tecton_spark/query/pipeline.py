from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import attrs
import pendulum
import pyspark
import pyspark.sql.types as spark_types

from tecton_core import query_consts
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query.compaction_utils import AggregationGroup
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query_consts import aggregation_group_id
from tecton_core.query_consts import exclusive_end_time
from tecton_core.query_consts import inclusive_start_time
from tecton_spark import data_observability
from tecton_spark import partial_aggregations
from tecton_spark.feature_view_spark_utils import validate_df_columns_and_feature_types
from tecton_spark.pipeline_helper import _PipelineBuilder
from tecton_spark.pipeline_helper import build_odfv_udf_col
from tecton_spark.query.node import SparkExecNode
from tecton_spark.schema_spark_utils import schema_to_spark


@attrs.frozen
class MultiOdfvPipelineSparkNode(SparkExecNode):
    input_node: SparkExecNode
    feature_definition_wrappers_namespaces: List[Tuple[FeatureDefinitionWrapper, str]]
    use_namespace_feature_prefix: bool

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        """
        Executes multiple ODFV transformations on the same input dataframe.

        Note: If the user defines their transformation to produce extra columns
        (besides what's specified in output_schema), they will be ignored. If
        there are missing columns they will fail in this function during
        runtime.
        """
        udf_select_columns = []
        odfv_output_columns = []
        input_df = self.input_node.to_dataframe(spark)
        for fdw, namespace in self.feature_definition_wrappers_namespaces:
            select_col, output_cols = build_odfv_udf_col(
                input_df, fdw, namespace, use_namespace_feature_prefix=self.use_namespace_feature_prefix
            )
            udf_select_columns.append(select_col)
            odfv_output_columns.extend(output_cols)

        # Execute odfvs in parallel, then deserialize outputs into columns
        input_columns = [f"`{c.name}`" for c in input_df.schema]
        odfv_tmp_outputs = input_df.select(*input_columns, *udf_select_columns)
        return odfv_tmp_outputs.select(*input_columns, *odfv_output_columns)


@attrs.frozen
class PipelineEvalSparkNode(SparkExecNode):
    inputs_map: Dict[str, SparkExecNode]
    feature_definition_wrapper: FeatureDefinitionWrapper

    # Needed for correct behavior by tecton_sliding_window udf if it exists in the pipeline
    feature_time_limits: Optional[pendulum.Period]

    check_view_schema: bool

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        df = _PipelineBuilder(
            spark,
            self.feature_definition_wrapper.pipeline,
            consume_streaming_data_sources=False,
            data_sources=self.feature_definition_wrapper.data_sources,
            transformations=self.feature_definition_wrapper.transformations,
            feature_time_limits=self.feature_time_limits,
            schedule_interval=self.feature_definition_wrapper.batch_materialization_schedule,
            passed_in_inputs={k: self.inputs_map[k].to_dataframe(spark) for k in self.inputs_map},
            output_schema=schema_to_spark(self.feature_definition_wrapper.view_schema),
        ).get_dataframe()
        if self.feature_time_limits is None and self.feature_definition_wrapper.materialization_start_timestamp:
            df = df.filter(
                df[self.feature_definition_wrapper.timestamp_key]
                >= self.feature_definition_wrapper.materialization_start_timestamp
            )

        if self.check_view_schema:
            validate_df_columns_and_feature_types(
                df, self.feature_definition_wrapper.view_schema, allow_extraneous_columns=False
            )

        return df


@attrs.frozen
class PartialAggSparkNode(SparkExecNode):
    input_node: SparkExecNode
    fdw: FeatureDefinitionWrapper = attrs.field()
    window_start_column_name: str
    window_end_column_name: Optional[str] = None
    aggregation_anchor_time: Optional[datetime] = None
    create_tiles: Optional[bool] = None

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        df = partial_aggregations.construct_partial_time_aggregation_df(
            self.input_node.to_dataframe(spark),
            self.fdw.partial_aggregate_group_by_columns,
            self.fdw.trailing_time_window_aggregation,
            self.fdw.get_feature_store_format_version,
            self.fdw.view_schema,
            window_start_column_name=self.window_start_column_name,
            window_end_column_name=self.window_end_column_name,
            aggregation_anchor_time=self.aggregation_anchor_time,
            create_tiles=self.create_tiles,
        )
        return df


@attrs.frozen
class OnlinePartialAggSparkNodeV2(SparkExecNode):
    input_node: SparkExecNode
    fdw: FeatureDefinitionWrapper = attrs.field()
    aggregation_groups: Tuple[AggregationGroup, ...]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        df = partial_aggregations.construct_online_partial_agg_v2_df(
            self.input_node.to_dataframe(spark),
            [*self.fdw.partial_aggregate_group_by_columns, query_consts.aggregation_group_id()],
            self.aggregation_groups,
            time_key=self.fdw.trailing_time_window_aggregation.time_key,
            view_schema=self.fdw.view_schema,
            is_continuous=self.fdw.is_continuous,
        )
        return df


@attrs.frozen
class MetricsCollectorSparkNode(SparkExecNode):
    input_node: SparkExecNode
    metrics_collector: data_observability.MetricsCollector = attrs.field(
        factory=data_observability.get_active_metrics_collector
    )

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        return self.metrics_collector.observe(self.input_node.to_dataframe(spark))


@attrs.frozen
class StagingSparkNode(SparkExecNode):
    input_node: SparkExecNode
    staging_table_name: str
    query_tree_step: QueryTreeStep

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        # TODO(danny): consider implementing this in Spark, but for now this is unnecessary and is a passthrough
        return self.input_node.to_dataframe(spark)


@attrs.frozen
class PythonDataSparkNode(SparkExecNode):
    columns: Tuple[str, ...]
    data: Tuple[Tuple[Any, ...]]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        # HACK: due to not having great way to pass through types. We need to declare the types since `inclusive_start_time` can be null.
        if self.columns == (aggregation_group_id(), inclusive_start_time(), exclusive_end_time()):
            schema = spark_types.StructType(
                [
                    spark_types.StructField(aggregation_group_id(), spark_types.LongType()),
                    spark_types.StructField(inclusive_start_time(), spark_types.TimestampType()),
                    spark_types.StructField(exclusive_end_time(), spark_types.TimestampType()),
                ]
            )
            return spark.createDataFrame(self.data, schema)
        return spark.createDataFrame(self.data, self.columns)
