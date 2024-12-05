from functools import reduce
from typing import Dict
from typing import List
from typing import Optional

import attrs
import pendulum
import pyspark
import pyspark.sql.window as spark_window
from pyspark.sql import functions as F
from pyspark.sql.functions import expr
from pyspark.sql.types import ArrayType
from pyspark.sql.types import LongType

from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query_consts import TECTON_TEMP_AGGREGATION_SECONDARY_KEY_COL
from tecton_core.query_consts import anchor_time
from tecton_core.query_consts import tecton_unique_id_col
from tecton_core.query_consts import valid_from
from tecton_core.query_consts import valid_to
from tecton_core.specs import MaterializedFeatureViewSpec
from tecton_core.specs import MaterializedFeatureViewType
from tecton_proto.common.aggregation_function_pb2 import AggregationFunction
from tecton_proto.data import feature_view_pb2 as feature_view__data_pb2
from tecton_spark.query.node import SparkExecNode
from tecton_spark.time_utils import convert_epoch_to_timestamp_column
from tecton_spark.time_utils import convert_timestamp_to_epoch


@attrs.frozen
class AddAnchorTimeSparkNode(SparkExecNode):
    input_node: SparkExecNode
    feature_store_format_version: int
    batch_schedule: int
    timestamp_field: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        anchor_time_val = convert_timestamp_to_epoch(F.col(self.timestamp_field), self.feature_store_format_version)
        df = input_df.withColumn(
            anchor_time(),
            anchor_time_val - anchor_time_val % self.batch_schedule,
        )
        return df


@attrs.frozen
class AddRetrievalAnchorTimeSparkNode(SparkExecNode):
    input_node: SparkExecNode
    name: str
    feature_store_format_version: int
    batch_schedule: int
    tile_interval: int
    timestamp_field: str
    is_stream: bool
    data_delay_seconds: Optional[int] = 0

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        anchor_time_val = convert_timestamp_to_epoch(
            F.col(self.timestamp_field) - expr(f"interval {self.data_delay_seconds} seconds"),
            self.feature_store_format_version,
        )
        # tile_interval will be 0 for continuous
        if self.tile_interval == 0:
            df = input_df.withColumn(anchor_time(), anchor_time_val)
        else:
            # For stream, we use the tile interval for bucketing since the data is available as soon as
            # the aggregation interval ends.
            # For BAFV, we use the batch schedule to get the last tile written.
            if self.is_stream:
                df = input_df.withColumn(
                    anchor_time(),
                    anchor_time_val - anchor_time_val % self.tile_interval - self.tile_interval,
                )
            else:
                df = input_df.withColumn(
                    anchor_time(),
                    anchor_time_val - anchor_time_val % self.batch_schedule - self.tile_interval,
                )
        return df


@attrs.frozen
class RenameColsSparkNode(SparkExecNode):
    input_node: SparkExecNode
    mapping: Optional[Dict[str, str]]
    drop: Optional[List[str]]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        if self.mapping:
            rename_cols = [F.col(old_name).alias(new_name) for old_name, new_name in self.mapping.items() if new_name]
            existing_cols = [col for col in input_df.columns if col not in self.mapping.keys()]
            input_df = input_df.select(*existing_cols, *rename_cols)

        if self.drop:
            input_df = input_df.drop(*self.drop)

        return input_df


@attrs.frozen
class ConvertEpochToTimestampSparkNode(SparkExecNode):
    input_node: SparkExecNode
    feature_store_formats: Dict[str, int]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        for name, feature_store_format_version in self.feature_store_formats.items():
            input_df = input_df.withColumn(
                name,
                convert_epoch_to_timestamp_column(F.col(name), feature_store_format_version),
            )
        return input_df


@attrs.frozen
class ConvertTimestampToUTCSparkNode(SparkExecNode):
    input_node: SparkExecNode
    timestamp_key: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        return self.input_node.to_dataframe(spark)


@attrs.frozen
class AddEffectiveTimestampSparkNode(SparkExecNode):
    input_node: SparkExecNode
    timestamp_field: str
    effective_timestamp_name: str
    batch_schedule_seconds: int
    is_stream: bool
    data_delay_seconds: int
    is_temporal_aggregate: bool

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)

        # batch_schedule = 0 implies feature table.
        if self.batch_schedule_seconds == 0 or self.is_stream:
            effective_timestamp = F.col(self.timestamp_field)
        else:
            slide_str = f"{self.batch_schedule_seconds} seconds"
            timestamp_col = F.col(self.timestamp_field)
            # Timestamp of temporal aggregate is end of the anchor time window. Subtract 1 micro
            # to get the correct bucket for batch schedule.
            if self.is_temporal_aggregate:
                timestamp_col -= expr("interval 1 microseconds")
            window_spec = F.window(timestamp_col, slide_str, slide_str)
            effective_timestamp = window_spec.end + expr(f"interval {self.data_delay_seconds} seconds")

        df = input_df.withColumn(self.effective_timestamp_name, effective_timestamp)
        return df


@attrs.frozen
class AddDurationSparkNode(SparkExecNode):
    input_node: SparkExecNode
    timestamp_field: str
    duration: pendulum.Duration
    new_column_name: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        return input_df.withColumn(
            self.new_column_name,
            F.col(self.timestamp_field) + expr(f"interval {self.duration.total_seconds()} seconds"),
        )


@attrs.frozen
class SelectDistinctSparkNode(SparkExecNode):
    input_node: SparkExecNode
    columns: List[str]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        return input_df.select(self.columns).distinct()


@attrs.frozen
class AggregationSecondaryKeyExplodeSparkNode(SparkExecNode):
    """
    This node returns all <entity, aggregation secondary key> pairs from the input node. It's used for retrieving
    secondary key aggregate features without spine.

    This node is similar to AsofSecondaryKeyExplodeSparkNode but doesn't require as-of join. It uses entities and
    anchor time to look back the max aggregation window time to find all secondary key values, and build a spine with
    all of them.
    """

    input_node: SparkExecNode
    join_keys: List[str]
    aggregation_secondary_key: str
    has_lifetime_aggregate: bool
    earliest_anchor_time_from_window_start: Optional[int]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)

        window_start = (
            spark_window.Window.unboundedPreceding
            if self.has_lifetime_aggregate
            else self.earliest_anchor_time_from_window_start
        )

        window_spec = (
            spark_window.Window.partitionBy(self.join_keys)
            .orderBy([anchor_time()])
            .rangeBetween(window_start, spark_window.Window.currentRow)
        )

        # Collect all secondary key values within the aggregation window, and explode them to build a spine.
        # Note the window based `collect_set` applies to every single row, so if a single join key has multiple
        # aggregation secondary keys with the same anchor time, the result dataframe will have multiple same rows for
        # that particular join key and anchor time. We select distinct here to deduplicate.
        input_df = (
            input_df.withColumn(
                TECTON_TEMP_AGGREGATION_SECONDARY_KEY_COL,
                F.collect_set(self.aggregation_secondary_key).over(window_spec),
            )
            .drop(self.aggregation_secondary_key)
            .distinct()
        )
        return input_df.withColumn(
            self.aggregation_secondary_key, F.explode(TECTON_TEMP_AGGREGATION_SECONDARY_KEY_COL)
        ).drop(TECTON_TEMP_AGGREGATION_SECONDARY_KEY_COL)


@attrs.frozen
class AddUniqueIdSparkNode(SparkExecNode):
    """
    Add a '_tecton_unique_id' column to the input node. This column is used to uniquely identify rows in the input node.

    Warning: The generated unique ID is non-deterministic on Spark, so this column may not be safe to join on.
    """

    input_node: SparkExecNode

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        return self.input_node.to_dataframe(spark).withColumn(tecton_unique_id_col(), F.monotonically_increasing_id())


def _is_count_feature(feature: feature_view__data_pb2.AggregateFeature) -> bool:
    return (
        feature.function == AggregationFunction.AGGREGATION_FUNCTION_COUNT
        or feature.function == AggregationFunction.AGGREGATION_FUNCTION_APPROX_COUNT_DISTINCT
    )


@attrs.frozen
class DeriveValidityPeriodSparkNode(SparkExecNode):
    """
    Derives the `valid_from` and `valid_to` columns from a fully aggregated data frame
    and removes duplicates and rows with default values for all aggregation columns.
    """

    input_node: SparkExecNode
    fdw: FeatureDefinitionWrapper
    timestamp_field: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        join_keys = self.fdw.join_keys
        df = self.input_node.to_dataframe(spark)
        features = self.fdw.fv_spec.features
        window = spark_window.Window.partitionBy(*join_keys).orderBy(self.timestamp_field)

        df = df.withColumn(valid_from(), F.col(self.timestamp_field)).withColumn(
            valid_to(), F.lead(self.timestamp_field).over(window)
        )

        feature_value_update_conditions = [
            ~F.col(column).eqNullSafe(F.col(f"_tecton_prev_{column}")) for column in features
        ]
        track_changes_cols = list(features)

        if self.fdw.serving_ttl is not None:
            df = self._expire_ttl(df)

            # if `valid_from` is not equal to the previous `valid_to` (in the case of TTL expiry),
            # we should not merge the rows even though the feature values are equal
            track_changes_cols.append(valid_to())
            feature_value_update_conditions.append(~F.col(valid_from()).eqNullSafe(F.col(f"_tecton_prev_{valid_to()}")))

        previous_value_columns = [
            F.lag(column).over(window).alias(f"_tecton_prev_{column}") for column in track_changes_cols
        ]
        df = df.select("*", *previous_value_columns)

        # Check if any feature column changed in value, set is_new=1 for rows with changes
        df = df.withColumn(
            "_tecton_is_new", F.when(reduce(lambda x, y: x | y, feature_value_update_conditions), 1).otherwise(0)
        )

        # Cumulatively sum the `is_new` column to create "groups".
        # A group is a set of consecutive rows that has the same aggregated value.
        df = df.withColumn("_tecton_group", F.sum("_tecton_is_new").over(window))

        # if valid_to for a group is "null", we've reached the last event and the "max" should be null
        # since we don't know how long the value is valid
        null_check = F.max(F.when(F.col(valid_to()).isNull(), True).otherwise(False))
        df = df.groupBy(*join_keys, *features, "_tecton_group").agg(
            F.min(valid_from()).alias(valid_from()),
            F.when(null_check, F.lit(None)).otherwise(F.max(valid_to())).alias(valid_to()),
        )

        if isinstance(self.fdw.fv_spec, MaterializedFeatureViewSpec):
            if self.fdw.fv_spec.type == MaterializedFeatureViewType.TEMPORAL_AGGREGATE:
                df = self._remove_default_values(df)

        return df.drop("_tecton_group", self.timestamp_field)

    def _remove_default_values(self, df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
        """
        Removes rows with default values for all aggregation columns.
        """
        aggregate_features = self.fdw.fv_spec.aggregate_features
        is_default_value_conditions = []
        if self.fdw.aggregation_secondary_key:
            # For secondary key aggs, we remove rows that have empty rollup output lists
            column_names = [rollup_output.name for rollup_output in self.fdw.fv_spec.secondary_key_rollup_outputs]
            is_default_value_conditions.extend([F.size(F.col(column)) == 0 for column in column_names])
        else:
            for feature in aggregate_features:
                column_name = feature.output_feature_name
                if isinstance(df.schema[column_name].dataType, ArrayType):
                    all_counts_empty = F.size(F.array_except(column_name, F.array(F.lit(0)))) == 0
                    all_nulls = F.size(F.array_except(column_name, F.array(F.lit(None)))) == 0
                    if _is_count_feature(feature):
                        condition = all_counts_empty | all_nulls
                    else:
                        condition = all_nulls
                else:
                    if _is_count_feature(feature):
                        condition = F.col(column_name).isNull() | (F.col(column_name) == 0)
                    else:
                        condition = F.col(column_name).isNull()
                is_default_value_conditions.append(condition)

        return df.filter(~reduce(lambda x, y: x & y, is_default_value_conditions))

    def _expire_ttl(self, df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
        """
        Trims `valid_to` values according to TTL for non-aggregate feature views
        """
        ttl_seconds = self.fdw.serving_ttl.total_seconds()
        should_trim_valid_to = F.col(valid_to()).isNull() | (
            (F.col(valid_to()).cast(LongType()) - F.col(valid_from()).cast(LongType())) > ttl_seconds
        )
        df = df.withColumn(
            valid_to(),
            F.when(should_trim_valid_to, F.col(valid_from()) + expr(f"INTERVAL {ttl_seconds} SECONDS")).otherwise(
                F.col(valid_to())
            ),
        )

        return df
