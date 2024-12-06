from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
import pypika
from pypika import AliasedQuery
from pypika import JoinType
from pypika.functions import Cast
from pypika.functions import Coalesce
from pypika.functions import Sum
from pypika.queries import QueryBuilder
from pypika.queries import Selectable
from pypika.terms import Criterion
from pypika.terms import Field
from pypika.terms import Function
from pypika.terms import LiteralValue
from pypika.terms import Term

from tecton_core import conf
from tecton_core.aggregation_utils import get_aggregation_function_result_type
from tecton_core.data_types import ArrayType
from tecton_core.data_types import DataType
from tecton_core.data_types import Float32Type
from tecton_core.data_types import Float64Type
from tecton_core.data_types import Int32Type
from tecton_core.data_types import Int64Type
from tecton_core.data_types import StringType
from tecton_core.query import nodes
from tecton_core.query.aggregation_plans import AGGREGATION_PLANS
from tecton_core.query.aggregation_plans import FilterAggregationInput
from tecton_core.query.node_interface import QueryNode
from tecton_core.query.sql_compat import DuckDBTupleTerm
from tecton_core.query_consts import anchor_time
from tecton_core.query_consts import tecton_secondary_key_aggregation_indicator_col
from tecton_core.query_consts import temp_indictor_column_name
from tecton_core.specs import create_time_window_spec_from_data_proto
from tecton_core.specs.time_window_spec import LifetimeWindowSpec
from tecton_core.specs.time_window_spec import RelativeTimeWindowSpec
from tecton_core.specs.time_window_spec import TimeWindowSeriesSpec
from tecton_core.specs.time_window_spec import TimeWindowSpec
from tecton_core.time_utils import convert_timedelta_for_version


class DuckDBArray(Term):
    def __init__(self, element_type: Union[str, Term]) -> None:
        super().__init__()
        self.element_type = element_type

    def get_sql(self, **kwargs):
        element_type_sql = (
            self.element_type.get_sql(**kwargs) if isinstance(self.element_type, Term) else self.element_type
        )
        return f"{element_type_sql}[]"


DATA_TYPE_TO_DUCKDB_TYPE: Dict[DataType, str] = {
    Int32Type(): "INT32",
    Int64Type(): "INT64",
    Float32Type(): "FLOAT",
    Float64Type(): "DOUBLE",
    StringType(): "VARCHAR",
}


def _data_type_to_duckdb_type(data_type: DataType) -> Union[str, Term]:
    if not isinstance(data_type, ArrayType):
        return DATA_TYPE_TO_DUCKDB_TYPE.get(data_type, str(data_type))

    return DuckDBArray(_data_type_to_duckdb_type(data_type.element_type))


def _join_condition(left: Selectable, right: Selectable, join_keys: List[str]) -> Criterion:
    left_join_struct = DuckDBTupleTerm(*[left.field(col) for col in join_keys])
    right_join_struct = DuckDBTupleTerm(*[right.field(col) for col in join_keys])
    return left_join_struct == right_join_struct


def _column_with_default(table: Selectable, column: str, default: Optional[Term] = None) -> Term:
    if not default:
        return table[column]

    return Coalesce(table[column], default).as_(column)


class TableFunction(Term):
    def __init__(self, function: Function, table_name: str, columns: List[str]) -> None:
        self.function = function
        self.table_name = table_name
        self.columns = columns

    def get_sql(self, **kwargs):
        return f"{self.function.get_sql(**kwargs)} {self.table_name}({', '.join(self.columns)})"


@attrs.frozen
class PartialAggDuckDBNode(nodes.PartialAggNode):
    @classmethod
    def from_query_node(cls, query_node: nodes.PartialAggNode) -> QueryNode:
        return cls(
            dialect=query_node.dialect,
            compute_mode=query_node.compute_mode,
            input_node=query_node.input_node,
            fdw=query_node.fdw,
            window_start_column_name=query_node.window_start_column_name,
            aggregation_tile_interval=query_node.aggregation_tile_interval,
            window_end_column_name=query_node.window_end_column_name,
            aggregation_anchor_time=query_node.aggregation_anchor_time,
        )

    def _get_partial_agg_columns_and_names(self) -> List[Tuple[Term, str]]:
        """
        Primarily overwritten to do additional type casts to make DuckDB's post-aggregation types consistent with Spark

        The two main cases:
        - Integer SUMs: DuckDB will automatically convert all integer SUMs to cast to DuckDB INT128's, regardless
        of its original type. Note that when copying this out into parquet, DuckDB will convert these to doubles.
        - Averages: DuckDB will always widen the precision to doubles

        Spark, in contrast, maintains the same type for both of these cases
        """
        normal_agg_cols_with_names = super()._get_partial_agg_columns_and_names()
        schema = self.fdw.materialization_schema.to_dict()

        final_agg_cols = []
        for col, alias in normal_agg_cols_with_names:
            data_type = schema[alias]
            sql_type = _data_type_to_duckdb_type(data_type)

            final_agg_cols.append((Cast(col, sql_type), alias))

        return final_agg_cols


@attrs.frozen
class AsofJoinFullAggNodeDuckDBNode(nodes.AsofJoinFullAggNode):
    @classmethod
    def from_query_node(cls, query_node: nodes.AsofJoinFullAggNode) -> QueryNode:
        return cls(
            dialect=query_node.dialect,
            compute_mode=query_node.compute_mode,
            spine=query_node.spine,
            partial_agg_node=query_node.partial_agg_node,
            fdw=query_node.fdw,
            enable_spine_time_pushdown_rewrite=query_node.enable_spine_time_pushdown_rewrite,
            enable_spine_entity_pushdown_rewrite=query_node.enable_spine_entity_pushdown_rewrite,
        )

    def _get_aggregations(self, window_order_col: str, partition_cols: List[str]) -> List[Term]:
        aggregations = super()._get_aggregations(window_order_col, partition_cols)
        features = self.fdw.fv_spec.aggregate_features
        secondary_key_indicators = (
            [
                temp_indictor_column_name(secondary_key_output.time_window)
                for secondary_key_output in self.fdw.materialized_fv_spec.secondary_key_rollup_outputs
            ]
            if self.fdw.aggregation_secondary_key
            else []
        )

        view_schema = self.fdw.view_schema.to_dict()

        # (column name, column type)
        output_columns: List[Tuple["str", DataType]] = []

        for feature in features:
            input_type = view_schema[feature.input_feature_name]
            result_type = get_aggregation_function_result_type(feature.function, input_type)
            window_spec = create_time_window_spec_from_data_proto(feature.time_window)
            if isinstance(window_spec, TimeWindowSeriesSpec):
                for relative_time_window in window_spec.time_windows:
                    output_columns.append(
                        (feature.output_feature_name + "_" + relative_time_window.to_string(), result_type)
                    )
            else:
                output_columns.append((feature.output_feature_name, result_type))

        for column_name in secondary_key_indicators:
            output_columns.append((column_name, Int64Type()))

        assert len(aggregations) == len(
            output_columns
        ), "List of aggregations and list of output columns must have the same length"
        return [
            Cast(aggregation, _data_type_to_duckdb_type(tecton_type)).as_(column_name)
            for aggregation, (column_name, tecton_type) in zip(aggregations, output_columns)
        ]


@attrs.frozen
class AsofJoinFullAggDuckDBNodeV2(nodes.AsofJoinFullAggNode):
    @classmethod
    def from_query_node(cls, query_node: nodes.AsofJoinFullAggNode) -> QueryNode:
        return cls(
            dialect=query_node.dialect,
            compute_mode=query_node.compute_mode,
            spine=query_node.spine,
            partial_agg_node=query_node.partial_agg_node,
            fdw=query_node.fdw,
            enable_spine_time_pushdown_rewrite=query_node.enable_spine_time_pushdown_rewrite,
            enable_spine_entity_pushdown_rewrite=query_node.enable_spine_entity_pushdown_rewrite,
        )

    def _get_aggregation_defaults(self) -> Dict[str, Term]:
        defaults = {}
        for feature in self.fdw.fv_spec.aggregate_features:
            aggregation_plan = AGGREGATION_PLANS.get(feature.function)
            if callable(aggregation_plan):
                aggregation_plan = aggregation_plan(None, feature.function_params, False)

            defaults[feature.output_feature_name] = aggregation_plan.full_aggregation_default_value or LiteralValue(
                "null"
            )

        return defaults

    def _get_aggregation_filter_for_window_spec(
        self, window_spec: TimeWindowSpec, feature_timestamp: Term, spine_timestamp: Term
    ) -> Criterion:
        if isinstance(window_spec, RelativeTimeWindowSpec):
            range_start = convert_timedelta_for_version(
                window_spec.window_start, self.fdw.get_feature_store_format_version
            )
            range_end = convert_timedelta_for_version(window_spec.window_end, self.fdw.get_feature_store_format_version)
            filter_ = feature_timestamp.between(spine_timestamp + range_start + 1, spine_timestamp + range_end)
        elif isinstance(window_spec, LifetimeWindowSpec):
            filter_ = LiteralValue("true")
        else:
            msg = f"Aggregation window of type {window_spec.__class__} is not supported by Rift"
            raise RuntimeError(msg)

        return filter_

    def _get_aggregations(self, feature_timestamp: Term, spine_timestamp: Term) -> List[Term]:
        features = self.fdw.fv_spec.aggregate_features
        aggregation_continuous = self.fdw.trailing_time_window_aggregation().is_continuous
        aggregations = []
        view_schema = self.fdw.view_schema.to_dict()
        # (column name, column type)
        output_columns: List[Tuple["str", DataType]] = []

        for feature in features:
            aggregation_plan = AGGREGATION_PLANS.get(feature.function)
            if callable(aggregation_plan):
                aggregation_plan = aggregation_plan(feature_timestamp, feature.function_params, aggregation_continuous)

            names = aggregation_plan.materialized_column_names(feature.input_feature_name)
            window_spec = create_time_window_spec_from_data_proto(feature.time_window)
            if isinstance(window_spec, TimeWindowSeriesSpec):
                msg = "TimeWindowSeriesSpec is currently not supported for the optimized Rift query tree. To use this feature, please set conf.set('DUCKDB_ENABLE_OPTIMIZED_FULL_AGG', False)"
                raise NotImplementedError(msg)
            filter_ = self._get_aggregation_filter_for_window_spec(window_spec, feature_timestamp, spine_timestamp)

            aggregations.append(aggregation_plan.full_aggregation_with_filter_query_term(names, filter_))
            input_type = view_schema[feature.input_feature_name]
            result_type = get_aggregation_function_result_type(feature.function, input_type)
            output_columns.append((feature.output_feature_name, result_type))

        if self.fdw.aggregation_secondary_key:
            for secondary_key_output in self.fdw.materialized_fv_spec.secondary_key_rollup_outputs:
                indicator_column = temp_indictor_column_name(secondary_key_output.time_window)
                filter_ = self._get_aggregation_filter_for_window_spec(
                    secondary_key_output.time_window, feature_timestamp, spine_timestamp
                )
                aggregations.append(
                    FilterAggregationInput(
                        aggregation=Sum(Field(tecton_secondary_key_aggregation_indicator_col())), filter_=filter_
                    )
                )
                output_columns.append((indicator_column, Int64Type()))

        assert len(aggregations) == len(
            output_columns
        ), "List of aggregations and list of output columns must have the same length"
        return [
            Cast(aggregation, _data_type_to_duckdb_type(tecton_type)).as_(column_name)
            for aggregation, (column_name, tecton_type) in zip(aggregations, output_columns)
        ]

    def _estimate_augmented_spine_factor(self) -> int:
        """Estimate multiplying factor (how much spine would explode) for spine augmentation"""
        assert not self.fdw.has_lifetime_aggregate and not self.fdw.is_continuous

        earliest_window_start = convert_timedelta_for_version(
            self.fdw.earliest_window_start, self.fdw.get_feature_store_format_version
        )
        tile_interval = convert_timedelta_for_version(
            self.fdw.get_tile_interval, self.fdw.get_feature_store_format_version
        )

        return abs(earliest_window_start // tile_interval)

    def _augment_spine_with_join_anchor_column(self, spine: AliasedQuery, column_name: str) -> QueryBuilder:
        """
        Explode spine rows by adding all possible anchor times (expected to be equal anchors in the feature input),
        that would be needed to calculate features for this spine row.

        This new column aimed to be used in JOIN condition with feature input.

        It's computed as:
            SELECT _anchor_time + delta FROM spine CROSS JOIN deltas
        where `deltas` is
            range(earliest_window_start, 0, tile_interval)

        Example:
            Given feature view with the earliest aggregation window = -7d

            input spine:
            |  join_key  | timestamp        | anchor_time         |
            |      AAAA  | 2024-02-05 11:00 | 1707091200000000000 |

            output spine:
            |  join_key  | timestamp        | anchor_time         |  _join_anchor_time  |
            |      AAAA  | 2024-02-05 11:00 | 1707091200000000000 | 1707091200000000000 |
            |      AAAA  | 2024-02-05 11:00 | 1707091200000000000 | 1707004800000000000 |
            |      AAAA  | 2024-02-05 11:00 | 1707091200000000000 | 1706918400000000000 |
            |      AAAA  | 2024-02-05 11:00 | 1707091200000000000 | 1706745600000000000 |
            |      AAAA  | 2024-02-05 11:00 | 1707091200000000000 | 1706659200000000000 |
            |      AAAA  | 2024-02-05 11:00 | 1707091200000000000 | 1706572800000000000 |
            |      AAAA  | 2024-02-05 11:00 | 1707091200000000000 | 1706486400000000000 |
        """
        assert not self.fdw.has_lifetime_aggregate and not self.fdw.is_continuous

        earliest_window_start = convert_timedelta_for_version(
            self.fdw.earliest_window_start, self.fdw.get_feature_store_format_version
        )
        tile_interval = convert_timedelta_for_version(
            self.fdw.get_tile_interval, self.fdw.get_feature_store_format_version
        )
        deltas = TableFunction(
            function=Function("GENERATE_SERIES", earliest_window_start, 0, tile_interval),
            table_name="deltas",
            columns=["delta"],
        )
        # we need here only join keys and anchor
        core_spine_columns = [*self.fdw.join_keys, anchor_time()]
        return (
            self.func.query()
            .from_(spine)
            .join(AliasedQuery("deltas", deltas))
            .cross()
            .select(
                *(
                    [spine.field(col) for col in core_spine_columns]
                    + [(spine.field(anchor_time()) + Field("delta")).as_(column_name)]
                )
            )
        )

    def _find_all_related_spine_rows(
        self, features: AliasedQuery, spine: AliasedQuery, spine_anchor_column: str
    ) -> QueryBuilder:
        """
        Performs "reverse" join: for each row in the feature input find all spine rows that would depend on this feature
        row in the full aggregation calculation.

        The resulting table contains all columns from the feature input and the `_anchor_time` for the spine input,
        renamed into {spine_anchor_column}. The output is expected to be bigger than the input, because a single feature
        row might be involved in calculating multiple spine rows.

        For BWAFV (except ones that contain lifetime aggregations) and non-continuous SWAFV we will use HASH JOIN.
        This is achieved by augmenting spine input by adding _join_anchor_time
        (see `_augment_spine_with_join_anchor_column` method).

        For continuous SWAFV and BWAFV with lifetime aggregations we will fallback to inequality-based JOIN,
        which is expected to be less efficient.
        """
        select_cols = [features.field(col) for col in self.partial_agg_node.columns]
        if self.fdw.aggregation_secondary_key:
            select_cols += [LiteralValue("1").as_(tecton_secondary_key_aggregation_indicator_col())]

        spine_distinct = self.func.query().from_(spine).select(*([*self.fdw.join_keys, anchor_time()])).distinct()

        max_explode_factor = int(conf.get_or_raise("DUCKDB_OPTIMIZED_FULL_AGG_MAX_EXPLODE"))
        if (
            self.fdw.has_lifetime_aggregate
            or self.fdw.is_continuous
            or self._estimate_augmented_spine_factor() > max_explode_factor
        ):
            join_condition = _join_condition(features, spine_distinct, self.fdw.join_keys)
            join_condition &= features.field(anchor_time()) <= spine_distinct.field(anchor_time())
            if not self.fdw.has_lifetime_aggregate:
                earliest_window_start = convert_timedelta_for_version(
                    self.fdw.earliest_window_start, self.fdw.get_feature_store_format_version
                )
                join_condition &= features.field(anchor_time()) > (
                    spine_distinct.field(anchor_time()) + earliest_window_start
                )
            return (
                self.func.query()
                .from_(features)
                .join(spine_distinct)
                .on(join_condition)
                .select(*[*select_cols, spine_distinct.field(anchor_time()).as_(spine_anchor_column)])
            )

        join_anchor_column = f"_join_{anchor_time()}"
        augmented_spine = self._augment_spine_with_join_anchor_column(spine_distinct, join_anchor_column)

        join_condition = _join_condition(features, augmented_spine, self.fdw.join_keys)
        join_condition &= features.field(anchor_time()) == augmented_spine.field(join_anchor_column)

        return (
            self.func.query()
            .from_(features)
            .join(augmented_spine)
            .on(join_condition)
            .select(*[*select_cols, augmented_spine.field(anchor_time()).as_(spine_anchor_column)])
        )

    def _to_query(self) -> QueryBuilder:
        """
        DuckDB-optimized query for Full Aggregation calculation.
        It's based on (1) JOINs instead of UNION and (2) FILTERing aggregation input instead of WINDOWing
        (see https://duckdb.org/docs/sql/query_syntax/filter.html for more details).

        The very high-level query plan looks like following:
        1. Explode spine to add all anchor_times (matching anchors in the feature input) required to calculate
           each spine row. (doesn't apply to continuous SWAFV and BWAFV with lifetime aggregations)

        2. Join the feature input with exploded spine: essentially assigning feature row to rows in the spine
          (rows from the feature input can be duplicated at this point).

        3. Group the feature input by join keys + assigned spine anchor time column.

        4. Calculate full aggregations w/ final timestamp filtering on column-level:
            SUM(sum_impression) FILTER (features._anchor_time <= spine._anchor_time AND
                                        features._anchor_time > spine._anchor_time - epoch_ns(INTERVAL 1 DAY))
                AS sum_impression_1d,
            SUM(sum_impression) FILTER (features._anchor_time <= spine._anchor_time AND
                                        features._anchor_time > spine._anchor_time - epoch_ns(INTERVAL 7 DAY))
                AS sum_impression_7d,
            SUM(sum_impression) FILTER (features._anchor_time <= spine._anchor_time - epoch_ns(INTERVAL 2 DAY) AND
                                        features._anchor_time > spine._anchor_time - epoch_ns(INTERVAL 7 DAY))
                AS sum_impression_offset_2d_7d
        """
        join_keys = self.fdw.join_keys
        if self.fdw.aggregation_secondary_key:
            join_keys += [self.fdw.aggregation_secondary_key]

        spine_anchor_time = f"_spine_{anchor_time()}"
        partition_cols = [*join_keys, spine_anchor_time]

        features_alias = self.partial_agg_node.name
        spine_alias = self.spine.name
        features_q = AliasedQuery(features_alias)
        spine_q = AliasedQuery(spine_alias)

        features_with_spine_anchor = self._find_all_related_spine_rows(features_q, spine_q, spine_anchor_time)
        aggregations = self._get_aggregations(
            spine_timestamp=features_with_spine_anchor[spine_anchor_time],
            feature_timestamp=features_with_spine_anchor[anchor_time()],
        )

        calculated_features = (
            self.func.query()
            .from_(features_with_spine_anchor)
            .groupby(*partition_cols)
            .select(*([features_with_spine_anchor.field(col) for col in partition_cols] + aggregations))
        )

        join_condition = _join_condition(spine_q, calculated_features, join_keys)
        join_condition &= spine_q[anchor_time()] == calculated_features[spine_anchor_time]

        aggregation_defaults = self._get_aggregation_defaults()

        return (
            self.func.query()
            .with_(self.spine.node._to_query(), spine_alias, materialized=True)
            .with_(self.partial_agg_node._to_query(), features_alias)
            .from_(spine_alias)
            .left_join(calculated_features)
            .on(join_condition)
            .select(
                *(
                    [spine_q[col] for col in self.spine.node.columns]
                    + [
                        _column_with_default(calculated_features, col, aggregation_defaults.get(col))
                        for col in self.columns
                        if col not in self.spine.node.columns
                    ]
                )
            )
        )


class AsofJoin(pypika.queries.JoinOn):
    def get_sql(self, **kwargs):
        return "ASOF " + super().get_sql(**kwargs)


@attrs.frozen
class AsofJoinDuckDBNode(nodes.AsofJoinNode):
    @classmethod
    def from_query_node(cls, query_node: nodes.AsofJoinNode) -> QueryNode:
        kwargs = attrs.asdict(query_node, recurse=False)
        del kwargs["node_id"]
        return cls(**kwargs)

    def _to_query(self) -> pypika.queries.QueryBuilder:
        left_df = self.left_container.node._to_query()
        right_df = self.right_container.node._to_query()
        right_name = self.right_container.node.name
        left_cols = list(self.left_container.node.columns)
        right_none_join_cols = [col for col in self.right_container.node.columns if col not in self.join_cols]
        columns = [left_df.field(col) for col in left_cols] + [
            AliasedQuery(right_name).field(col).as_(f"{self.right_container.prefix}_{col}")
            for col in right_none_join_cols
        ]
        # Using struct here to handle null values in the join columns
        left_join_struct = DuckDBTupleTerm(*[left_df.field(col) for col in self.join_cols])
        right_join_struct = DuckDBTupleTerm(*[AliasedQuery(right_name).field(col) for col in self.join_cols])
        # We need to use both the effective timestamp and the timestamp for the join condition, as the effective timestamp can be same for multiple rows
        left_join_condition_struct = DuckDBTupleTerm(
            left_df.field(self.left_container.timestamp_field), left_df.field(self.left_container.timestamp_field)
        )
        right_join_condition_struct = DuckDBTupleTerm(
            AliasedQuery(right_name).field(self.right_container.effective_timestamp_field),
            AliasedQuery(right_name).field(self.right_container.timestamp_field),
        )

        res = self.func.query().with_(right_df, right_name).select(*columns).from_(left_df)
        # do_join doesn't return new query, but updates in-place
        res.do_join(
            AsofJoin(
                item=AliasedQuery(right_name),
                how=JoinType.left,
                criteria=Criterion.all(
                    [left_join_condition_struct >= right_join_condition_struct, left_join_struct == right_join_struct]
                ),
            )
        )

        return res
