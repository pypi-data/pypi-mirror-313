from abc import ABC
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from pypika.terms import Equality

from tecton_core.data_types import DataType
from tecton_core.data_types import data_type_from_proto
from tecton_core.errors import TectonInternalError
from tecton_core.specs import utils
from tecton_proto.common import calculation_node__client_pb2 as calculation_node_pb2


COMPARISON_OPERATION_TYPE_TO_PYPIKA_EQUALITY: Dict[calculation_node_pb2.OperationType.ValueType, Equality] = {
    calculation_node_pb2.OperationType.EQUALS: Equality.eq,
    calculation_node_pb2.OperationType.NOT_EQUALS: Equality.ne,
    calculation_node_pb2.OperationType.GREATER_THAN: Equality.gt,
    calculation_node_pb2.OperationType.GREATER_THAN_EQUALS: Equality.gte,
    calculation_node_pb2.OperationType.LESS_THAN: Equality.lt,
    calculation_node_pb2.OperationType.LESS_THAN_EQUALS: Equality.lte,
}


@utils.frozen_strict
class AbstractSyntaxTreeNodeSpec(ABC):
    dtype: Optional[DataType]

    @classmethod
    def from_proto(cls, node: calculation_node_pb2.AbstractSyntaxTreeNode) -> "AbstractSyntaxTreeNodeSpec":
        value_type = node.WhichOneof("value")
        if value_type == "literal_value":
            return LiteralValueNodeSpec.from_proto(node)
        elif value_type == "column_reference":
            return ColumnReferenceNodeSpec.from_proto(node)
        elif value_type == "operation":
            return OperationNodeSpec.from_proto(node)
        elif value_type == "date_part":
            return DatePartNodeSpec.from_proto(node)
        else:
            msg = "Unknown AbstractSyntaxTreeNode Type"
            raise TectonInternalError(msg)


@utils.frozen_strict
class OperationNodeSpec(AbstractSyntaxTreeNodeSpec):
    dtype: DataType
    operation: calculation_node_pb2.OperationType
    operands: List[AbstractSyntaxTreeNodeSpec]

    @classmethod
    def from_proto(cls, proto: calculation_node_pb2.AbstractSyntaxTreeNode) -> "OperationNodeSpec":
        operation_proto = proto.operation
        return cls(
            dtype=data_type_from_proto(proto.dtype),
            operation=operation_proto.operation,
            operands=[AbstractSyntaxTreeNodeSpec.from_proto(operand) for operand in operation_proto.operands],
        )


@utils.frozen_strict
class LiteralValueNodeSpec(AbstractSyntaxTreeNodeSpec):
    dtype: Optional[DataType]
    value: Optional[Union[float, int, bool, str]]

    @classmethod
    def from_proto(cls, proto: calculation_node_pb2.AbstractSyntaxTreeNode) -> "LiteralValueNodeSpec":
        literal_value_proto = proto.literal_value
        value_type = literal_value_proto.WhichOneof("value")
        if value_type == "null_value":
            return cls(dtype=None, value=None)
        else:
            return cls(dtype=data_type_from_proto(proto.dtype), value=getattr(literal_value_proto, value_type))


@utils.frozen_strict
class ColumnReferenceNodeSpec(AbstractSyntaxTreeNodeSpec):
    dtype: DataType
    value: str

    @classmethod
    def from_proto(cls, proto: calculation_node_pb2.AbstractSyntaxTreeNode) -> "ColumnReferenceNodeSpec":
        return cls(dtype=data_type_from_proto(proto.dtype), value=proto.column_reference)


@utils.frozen_strict
class DatePartNodeSpec(AbstractSyntaxTreeNodeSpec):
    value: calculation_node_pb2.DatePart.ValueType

    @classmethod
    def from_proto(cls, proto: calculation_node_pb2.AbstractSyntaxTreeNode) -> "DatePartNodeSpec":
        return cls(value=proto.date_part, dtype=None)
