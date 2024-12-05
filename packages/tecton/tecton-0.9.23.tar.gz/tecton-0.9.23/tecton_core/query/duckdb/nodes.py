from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import attrs
import pypika
from pypika import AliasedQuery
from pypika import JoinType
from pypika.functions import Cast
from pypika.terms import Criterion
from pypika.terms import Term

from tecton_core.aggregation_utils import get_aggregation_function_result_type
from tecton_core.data_types import ArrayType
from tecton_core.data_types import DataType
from tecton_core.data_types import Float32Type
from tecton_core.data_types import Float64Type
from tecton_core.data_types import Int32Type
from tecton_core.data_types import Int64Type
from tecton_core.data_types import StringType
from tecton_core.query import nodes
from tecton_core.query.node_interface import QueryNode
from tecton_core.query.sql_compat import DuckDBTupleTerm
from tecton_core.query_consts import temp_indictor_column_name


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
            window_end_column_name=query_node.window_end_column_name,
            aggregation_anchor_time=query_node.aggregation_anchor_time,
            create_tiles=query_node.create_tiles,
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
