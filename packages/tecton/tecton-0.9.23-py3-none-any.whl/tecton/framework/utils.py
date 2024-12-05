from typing import Tuple

from tecton._internals import errors
from tecton.framework import base_tecton_object
from tecton_proto.args import transformation_pb2 as transformation__args_proto


SPARK_SQL_MODE = "spark_sql"
PYSPARK_MODE = "pyspark"
SNOWFLAKE_SQL_MODE = "snowflake_sql"
SNOWPARK_MODE = "snowpark"
PANDAS_MODE = "pandas"
PYTHON_MODE = "python"


def short_tecton_objects_repr(tecton_objects: Tuple[base_tecton_object.BaseTectonObject]) -> str:
    """Returns a shortened printable representation for a tuple of Tecton objects. Used for printing summaries."""
    short_strings = tuple(short_tecton_object_repr(obj) for obj in tecton_objects)
    return repr(short_strings)


def short_tecton_object_repr(tecton_object: base_tecton_object.BaseTectonObject) -> str:
    """Returns a shortened printable representation for a Tecton object. Used for printing summaries."""
    return f"{type(tecton_object).__name__}('{tecton_object.info.name}')"


def get_transformation_mode_enum(mode: str, name: str) -> transformation__args_proto.TransformationMode.ValueType:
    """Returns the TransformationMode type from string"""
    if mode == SPARK_SQL_MODE:
        return transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_SPARK_SQL
    elif mode == PYSPARK_MODE:
        return transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PYSPARK
    elif mode == SNOWFLAKE_SQL_MODE:
        return transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_SNOWFLAKE_SQL
    elif mode == SNOWPARK_MODE:
        return transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_SNOWPARK
    elif mode == PANDAS_MODE:
        return transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PANDAS
    elif mode == PYTHON_MODE:
        return transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PYTHON
    else:
        raise errors.InvalidTransformationMode(
            name,
            mode,
            [SPARK_SQL_MODE, PYSPARK_MODE, SNOWFLAKE_SQL_MODE, SNOWPARK_MODE, PANDAS_MODE, PYTHON_MODE],
        )
