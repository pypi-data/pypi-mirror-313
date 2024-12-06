from abc import ABC
from abc import abstractmethod
from typing import Dict

import attrs
import pypika.functions as fn
from pypika import NULL
from pypika.enums import Equality
from pypika.terms import BasicCriterion
from pypika.terms import Field
from pypika.terms import LiteralValue
from pypika.terms import Term
from pypika.terms import ValueWrapper

from tecton_core import data_types
from tecton_core.compute_mode import ComputeMode
from tecton_core.errors import TectonInternalError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query.column_reference_resolver import ColumnReferenceResolver
from tecton_core.specs.calculation_node_spec import AbstractSyntaxTreeNodeSpec
from tecton_core.specs.calculation_node_spec import ColumnReferenceNodeSpec
from tecton_core.specs.calculation_node_spec import LiteralValueNodeSpec
from tecton_core.specs.calculation_node_spec import OperationNodeSpec
from tecton_proto.common import calculation_node__client_pb2 as calculation_node_pb2


COMPARISON_OPERATION_TYPE_TO_PYPIKA_EQUALITY: Dict[calculation_node_pb2.OperationType.ValueType, Equality] = {
    calculation_node_pb2.OperationType.EQUALS: Equality.eq,
    calculation_node_pb2.OperationType.NOT_EQUALS: Equality.ne,
    calculation_node_pb2.OperationType.GREATER_THAN: Equality.gt,
    calculation_node_pb2.OperationType.GREATER_THAN_EQUALS: Equality.gte,
    calculation_node_pb2.OperationType.LESS_THAN: Equality.lt,
    calculation_node_pb2.OperationType.LESS_THAN_EQUALS: Equality.lte,
}

DATE_PART_TO_INTERVAL_STRING: Dict[calculation_node_pb2.DatePart.ValueType, str] = {
    calculation_node_pb2.DatePart.DAY: "day",
    calculation_node_pb2.DatePart.MONTH: "month",
    calculation_node_pb2.DatePart.WEEK: "week",
    calculation_node_pb2.DatePart.YEAR: "year",
    calculation_node_pb2.DatePart.SECOND: "second",
    calculation_node_pb2.DatePart.HOUR: "hour",
    calculation_node_pb2.DatePart.MINUTE: "minute",
    calculation_node_pb2.DatePart.MILLENNIUM: "millennium",
    calculation_node_pb2.DatePart.CENTURY: "century",
    calculation_node_pb2.DatePart.DECADE: "decade",
    calculation_node_pb2.DatePart.QUARTER: "quarter",
    calculation_node_pb2.DatePart.MILLISECONDS: "milliseconds",
    calculation_node_pb2.DatePart.MICROSECONDS: "microseconds",
}


@attrs.define
class CalculationSqlBuilder(ABC):
    fdw: FeatureDefinitionWrapper
    column_reference_resolver: ColumnReferenceResolver

    def _operation_node_to_query_term(self, operation_node: OperationNodeSpec) -> Term:
        if operation_node.operation == calculation_node_pb2.OperationType.COALESCE:
            return self._build_coalesce_query(operation_node)
        elif operation_node.operation in COMPARISON_OPERATION_TYPE_TO_PYPIKA_EQUALITY:
            return self._build_comparison_query(operation_node)
        elif operation_node.operation == calculation_node_pb2.OperationType.DATE_DIFF:
            return self._build_date_diff_query(operation_node)
        else:
            msg = f"In Calculation sql generation, calculation operation {operation_node.operation.name} not supported."
            raise TectonInternalError(msg)

    def _build_coalesce_query(self, operation_node: OperationNodeSpec) -> Term:
        if len(operation_node.operands) < 1:
            msg = "Calculation function Coalesce must have at least 1 operand."
            raise TectonInternalError(msg)
        operand_sqls = [self.ast_node_to_query_term(operand) for operand in operation_node.operands]
        return fn.Coalesce(*operand_sqls)

    def _build_comparison_query(self, operation_node: OperationNodeSpec) -> Term:
        if len(operation_node.operands) != 2:
            msg = "Calculation function must have exactly 2 operands."
            raise TectonInternalError(msg)
        left = self.ast_node_to_query_term(operation_node.operands[0])
        right = self.ast_node_to_query_term(operation_node.operands[1])

        comparator_term = COMPARISON_OPERATION_TYPE_TO_PYPIKA_EQUALITY[operation_node.operation]
        return BasicCriterion(comparator_term, left, right)

    @abstractmethod
    def _build_date_diff_query(self, operation_node: OperationNodeSpec) -> Term:
        raise NotImplementedError

    @staticmethod
    def _literal_value_node_to_query_term(literal_value_node: LiteralValueNodeSpec) -> Term:
        if literal_value_node.dtype is None or literal_value_node.value is None:
            return NULL
        sql = ValueWrapper(literal_value_node.value)
        if isinstance(literal_value_node.dtype, data_types.Int64Type):
            sql = fn.Cast(sql, "BIGINT")
        elif isinstance(literal_value_node.dtype, data_types.Float64Type):
            sql = fn.Cast(sql, "DOUBLE")
        return sql

    def _column_reference_node_to_query_term(self, column_reference_node: ColumnReferenceNodeSpec) -> Term:
        internal_column_name = self.column_reference_resolver.get_internal_column_name(
            column_reference_node.value, self.fdw
        )
        return Field(internal_column_name)

    def ast_node_to_query_term(self, ast_node: AbstractSyntaxTreeNodeSpec) -> Term:
        if isinstance(ast_node, OperationNodeSpec):
            return self._operation_node_to_query_term(ast_node)
        elif isinstance(ast_node, LiteralValueNodeSpec):
            return self._literal_value_node_to_query_term(ast_node)
        elif isinstance(ast_node, ColumnReferenceNodeSpec):
            return self._column_reference_node_to_query_term(ast_node)
        else:
            msg = f"AST node type {ast_node.__class__.__name__} not recognized. Cannot extract calculation."
            raise TectonInternalError(msg)


@attrs.define
class DuckDBCalculationSqlBuilder(CalculationSqlBuilder):
    def _build_date_diff_query(self, operation_node: OperationNodeSpec) -> Term:
        if len(operation_node.operands) != 3:
            msg = "Calculation function date diff must have exactly 3 operands."
            raise TectonInternalError(msg)
        [date_part_operand, start_date_operand, end_date_operand] = operation_node.operands
        date_part_str = DATE_PART_TO_INTERVAL_STRING[date_part_operand.value]
        start_date_operand = self.ast_node_to_query_term(start_date_operand)
        end_date_operand = self.ast_node_to_query_term(end_date_operand)

        return fn.DateDiff(date_part_str, start_date_operand, end_date_operand)


@attrs.define
class SparkCalculationSqlBuilder(CalculationSqlBuilder):
    @staticmethod
    def _get_spark_date_diff_sql_str(
        date_part: calculation_node_pb2.DatePart.ValueType, start_date_sql: str, end_date_sql: str
    ) -> str:
        if date_part == calculation_node_pb2.DatePart.DAY:
            return f"FLOOR(DATEDIFF(DATE_TRUNC('day', {end_date_sql}), DATE_TRUNC('day', {start_date_sql})))"
        elif date_part == calculation_node_pb2.DatePart.MONTH:
            return f"FLOOR(MONTHS_BETWEEN(DATE_TRUNC('month', {end_date_sql}), DATE_TRUNC('month', {start_date_sql})))"
        elif date_part == calculation_node_pb2.DatePart.WEEK:
            return f"FLOOR(DATEDIFF({end_date_sql}, {start_date_sql})/7)"
        elif date_part == calculation_node_pb2.DatePart.YEAR:
            return f"YEAR({end_date_sql}) - YEAR({start_date_sql})"
        elif date_part == calculation_node_pb2.DatePart.SECOND:
            return f"UNIX_TIMESTAMP(DATE_TRUNC('second', {end_date_sql})) - UNIX_TIMESTAMP(DATE_TRUNC('second', {start_date_sql}))"
        elif date_part == calculation_node_pb2.DatePart.HOUR:
            return f"( UNIX_TIMESTAMP(DATE_TRUNC('hour', {end_date_sql})) - UNIX_TIMESTAMP(DATE_TRUNC('hour', {start_date_sql})) ) / 3600"
        elif date_part == calculation_node_pb2.DatePart.MINUTE:
            return f"( UNIX_TIMESTAMP(DATE_TRUNC('minute', {end_date_sql})) - UNIX_TIMESTAMP(DATE_TRUNC('minute', {start_date_sql})) ) / 60"
        elif date_part == calculation_node_pb2.DatePart.MILLENNIUM:
            return f"FLOOR(YEAR({end_date_sql}) / 1000) - FLOOR(YEAR({start_date_sql}) / 1000)"
        elif date_part == calculation_node_pb2.DatePart.CENTURY:
            return f"FLOOR(YEAR({end_date_sql}) / 100) - FLOOR(YEAR({start_date_sql}) / 100)"
        elif date_part == calculation_node_pb2.DatePart.DECADE:
            return f"FLOOR(YEAR({end_date_sql}) / 10) - FLOOR(YEAR({start_date_sql}) / 10)"
        elif date_part == calculation_node_pb2.DatePart.QUARTER:
            return f"4 * (YEAR({end_date_sql}) - YEAR({start_date_sql})) + FLOOR((MONTH({end_date_sql})-1 )/ 3) - FLOOR((MONTH({start_date_sql})-1 )/ 3)"
        elif date_part == calculation_node_pb2.DatePart.MILLISECONDS:
            return f"UNIX_MILLIS({end_date_sql}) - UNIX_MILLIS({start_date_sql})"
        elif date_part == calculation_node_pb2.DatePart.MICROSECONDS:
            return f"UNIX_MICROS({end_date_sql}) - UNIX_MICROS({start_date_sql})"
        else:
            msg = f"Date part {date_part} is not supported."
            raise TectonInternalError(msg)

    def _build_date_diff_query(self, operation_node: OperationNodeSpec) -> Term:
        if len(operation_node.operands) != 3:
            msg = "Calculation function date diff must have exactly 3 operands."
            raise TectonInternalError(msg)

        [date_part_operand, start_date_operand, end_date_operand] = operation_node.operands
        start_date_sql = self.ast_node_to_query_term(start_date_operand).get_sql()
        end_date_sql = self.ast_node_to_query_term(end_date_operand).get_sql()

        date_value = date_part_operand.value
        spark_sql = SparkCalculationSqlBuilder._get_spark_date_diff_sql_str(date_value, start_date_sql, end_date_sql)
        return LiteralValue(spark_sql)


class CalculationSqlBuilderFactory:
    @classmethod
    def create_builder(
        cls,
        fdw: FeatureDefinitionWrapper,
        column_reference_resolver: ColumnReferenceResolver,
        compute_mode: ComputeMode,
    ) -> CalculationSqlBuilder:
        sql_builders = {
            ComputeMode.SPARK: SparkCalculationSqlBuilder,
            ComputeMode.RIFT: DuckDBCalculationSqlBuilder,
        }
        return sql_builders[compute_mode](fdw, column_reference_resolver)
