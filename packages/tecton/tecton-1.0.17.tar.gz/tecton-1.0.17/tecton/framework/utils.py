from typing import Tuple

from tecton._internals import errors
from tecton.framework import base_tecton_object
from tecton_proto.args import transformation__client_pb2 as transformation__args_proto


SPARK_SQL_MODE = "spark_sql"
PYSPARK_MODE = "pyspark"
SNOWFLAKE_SQL_MODE = "snowflake_sql"
SNOWPARK_MODE = "snowpark"
PANDAS_MODE = "pandas"
PYTHON_MODE = "python"
BIGQUERY_SQL_MODE = "bigquery_sql"

mode_str_to_proto_enum = {
    SPARK_SQL_MODE: transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_SPARK_SQL,
    PYSPARK_MODE: transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PYSPARK,
    SNOWFLAKE_SQL_MODE: transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_SNOWFLAKE_SQL,
    SNOWPARK_MODE: transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_SNOWPARK,
    PANDAS_MODE: transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PANDAS,
    PYTHON_MODE: transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PYTHON,
    BIGQUERY_SQL_MODE: transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_BIGQUERY_SQL,
}


def short_tecton_objects_repr(tecton_objects: Tuple[base_tecton_object.BaseTectonObject]) -> str:
    """Returns a shortened printable representation for a tuple of Tecton objects. Used for printing summaries."""
    short_strings = tuple(short_tecton_object_repr(obj) for obj in tecton_objects)
    return repr(short_strings)


def short_tecton_object_repr(tecton_object: base_tecton_object.BaseTectonObject) -> str:
    """Returns a shortened printable representation for a Tecton object. Used for printing summaries."""
    return f"{type(tecton_object).__name__}('{tecton_object.info.name}')"


def get_transformation_mode_name(mode_proto_enum: mode_str_to_proto_enum) -> str:
    mode_proto_enum_to_str = dict(map(reversed, mode_str_to_proto_enum.items()))
    return mode_proto_enum_to_str.get(mode_proto_enum)


def get_transformation_mode_enum(mode: str, name: str) -> transformation__args_proto.TransformationMode.ValueType:
    """Returns the TransformationMode type from string"""
    mode_enum = mode_str_to_proto_enum.get(mode)
    if mode_enum is None:
        raise errors.InvalidTransformationMode(
            name,
            mode,
            [SPARK_SQL_MODE, PYSPARK_MODE, SNOWFLAKE_SQL_MODE, SNOWPARK_MODE, PANDAS_MODE, PYTHON_MODE],
        )
    else:
        return mode_enum
