from dataclasses import dataclass
from dataclasses import field
from typing import Callable
from typing import Dict
from typing import List
from typing import Union

import pandas
import pyarrow
import pyarrow as pa

from tecton_core import data_types
from tecton_core.errors import TectonValidationError
from tecton_core.schema import Schema


@dataclass
class FieldTypeDiff:
    field: str
    msg: str


@dataclass
class DiffResult:
    missing_fields: List[str] = field(default_factory=list)
    missmatch_types: List[FieldTypeDiff] = field(default_factory=list)

    def __bool__(self):
        return len(self.missing_fields) > 0 or len(self.missmatch_types) > 0

    def as_str(self):
        def lines():
            if self.missing_fields:
                yield f"Missing fields: {', '.join(self.missing_fields)}"

            if self.missmatch_types:
                yield "Types do not match:"
                for item in self.missmatch_types:
                    yield f"  Field {item.field}: {item.msg}"

        return "\n".join(lines())


class CastError(TectonValidationError):
    def __init__(self, msg):
        super().__init__(msg, can_drop_traceback=True)

    @staticmethod
    def for_diff(diff_result: DiffResult) -> "CastError":
        return CastError("Schema mismatch:\n" + diff_result.as_str())


_ColumnGetter = Callable[[str, pa.DataType], pa.Array]


def cast(obj: Union[pa.Table, pa.RecordBatch, pandas.DataFrame], schema: Union[Schema, pyarrow.Schema]) -> pa.Table:
    if isinstance(schema, Schema):
        arrow_schema = tecton_schema_to_arrow_schema(schema)
    elif isinstance(schema, pyarrow.Schema):
        arrow_schema = schema
    else:
        msg = f"Unsupported schema type: {type(schema)}"
        raise TypeError(msg)

    if isinstance(obj, (pa.RecordBatch, pa.Table)):

        def get_column(name: str, dtype: pa.DataType) -> pa.Array:
            return obj.column(name).cast(dtype)

    elif isinstance(obj, pandas.DataFrame):
        columns = _pandas_columns(obj)

        def get_column(name: str, dtype: pa.DataType) -> pa.Array:
            series = columns[name]
            if len(series) != 1:
                msg = f"Ambiguous column label {name}. Ensure only one column exists with a given label."
                raise CastError(msg)
            return pyarrow.Array.from_pandas(series[0], type=dtype)

    else:
        msg = f"Unexpected type: {type(obj)}"
        raise TypeError(msg)
    arrays = cast_columns(get_column, arrow_schema)
    return pyarrow.Table.from_arrays(arrays, schema=arrow_schema)


def _pandas_columns(df: pandas.DataFrame) -> Dict[str, List[pandas.Series]]:
    def _series_iter():
        axes = df.axes
        if len(axes) != 2:
            msg = f"Pandas DataFrame should have 2 axes; not {len(axes)}"
            raise CastError(msg)

        index = df.index
        if isinstance(index, pandas.MultiIndex):
            for level_name in index.names:
                yield level_name, index.get_level_values(level_name)
        elif isinstance(index, pandas.Index):
            if index.name is not None:
                yield index.name, index
        else:
            msg = "First axis of a Pandas DataFrame should be an Index"
            raise CastError(msg)

        yield from df.items()

    ret = {}
    for label, series in _series_iter():
        ret.setdefault(label, []).append(series)
    return ret


def cast_columns(column_getter: _ColumnGetter, schema: pa.Schema) -> List[pa.Array]:
    diff = DiffResult()
    arrays = []
    for name, dtype in zip(schema.names, schema.types):
        try:
            arrays.append(column_getter(name, dtype))
        except KeyError:
            diff.missing_fields.append(name)
        except pa.ArrowTypeError as e:
            diff.missmatch_types.append(FieldTypeDiff(name, str(e)))
        except pa.ArrowInvalid as e:
            diff.missmatch_types.append(FieldTypeDiff(name, str(e)))
    if diff:
        raise CastError.for_diff(diff)
    else:
        return arrays


_PRIMITIVE_TECTON_TYPE_TO_ARROW_TYPE: Dict[data_types.DataType, pa.DataType] = {
    data_types.Int32Type(): pa.int32(),
    data_types.Int64Type(): pa.int64(),
    data_types.Float32Type(): pa.float32(),
    data_types.Float64Type(): pa.float64(),
    data_types.StringType(): pa.string(),
    data_types.TimestampType(): pa.timestamp("ns", "UTC"),
    data_types.BoolType(): pa.bool_(),
}


def _tecton_type_to_arrow_type(tecton_type: data_types.DataType) -> pa.DataType:
    if tecton_type in _PRIMITIVE_TECTON_TYPE_TO_ARROW_TYPE:
        return _PRIMITIVE_TECTON_TYPE_TO_ARROW_TYPE[tecton_type]

    if isinstance(tecton_type, data_types.ArrayType):
        return pa.list_(_tecton_type_to_arrow_type(tecton_type.element_type))

    if isinstance(tecton_type, data_types.MapType):
        return pa.map_(
            _tecton_type_to_arrow_type(tecton_type.key_type),
            _tecton_type_to_arrow_type(tecton_type.value_type),
        )

    if isinstance(tecton_type, data_types.StructType):
        fields = []
        for tecton_field in tecton_type.fields:
            fields.append(pa.field(tecton_field.name, _tecton_type_to_arrow_type(tecton_field.data_type)))
        return pa.struct(fields)

    msg = f"Tecton type {tecton_type} can't be converted to arrow type"
    raise ValueError(msg)


def tecton_schema_to_arrow_schema(schema: Schema) -> pa.Schema:
    fields = []
    for column, data_type in schema.column_name_and_data_types():
        fields.append(pa.field(column, _tecton_type_to_arrow_type(data_type)))
    return pa.schema(fields)
