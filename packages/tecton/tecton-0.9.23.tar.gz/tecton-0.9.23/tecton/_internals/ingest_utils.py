"""This files contains utilities for running feature_table.ingest()."""

import io
import logging

import pandas as pd
from pyspark.sql import dataframe as pyspark_dataframe
from pyspark.sql.types import ArrayType
from pyspark.sql.types import DoubleType
from pyspark.sql.types import FloatType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import LongType
from pyspark.sql.types import StructType

from tecton import tecton_context
from tecton._internals.pandas_compat import pandas_to_spark
from tecton_core import errors
from tecton_core import http
from tecton_core import schema
from tecton_core.arrow import PARQUET_WRITE_OPTIONS_KWARGS
from tecton_spark import schema_spark_utils


logger = logging.getLogger(__name__)


def upload_df_pandas(upload_url: str, df: pd.DataFrame, parquet: bool = True):
    out_buffer = io.BytesIO()
    if parquet:
        df.to_parquet(out_buffer, index=False, engine="pyarrow", **PARQUET_WRITE_OPTIONS_KWARGS)
    else:
        df.to_csv(out_buffer, index=False, header=False)

    # Maximum 1GB per ingestion
    if out_buffer.__sizeof__() > 1_000_000_000:
        raise errors.FT_DF_TOO_LARGE

    r = http.session().put(upload_url, data=out_buffer.getvalue())
    if r.status_code != 200:
        raise errors.FT_UPLOAD_FAILED(r.reason)


def convert_pandas_to_spark_df(df: pd.DataFrame, view_schema: schema.Schema) -> pyspark_dataframe.DataFrame:
    tc = tecton_context.TectonContext.get_instance()
    spark = tc._spark
    spark_df = pandas_to_spark(spark, df)

    converted_schema = _convert_ingest_schema(spark_df.schema, view_schema)

    if converted_schema != spark_df.schema:
        spark_df = pandas_to_spark(df, schema=converted_schema)

    return spark_df


def _convert_ingest_schema(ingest_schema: StructType, view_schema: schema.Schema) -> StructType:
    """Convert pandas-derived spark schema to Tecton-compatible schema for Feature Tables.

    The Pandas to Spark dataframe conversion implicitly derives the Spark schema.
    We handle converting/correcting for some type conversions where the derived schema and the feature table schema do not match.
    """
    ft_columns = schema_spark_utils.column_name_spark_data_types(view_schema)
    ingest_columns = schema_spark_utils.column_name_spark_data_types(
        schema_spark_utils.schema_from_spark(ingest_schema)
    )

    converted_ingest_schema = StructType()
    int_converted_columns = []

    for col_name, col_type in ingest_columns:
        if col_type == LongType() and (col_name, IntegerType()) in ft_columns:
            int_converted_columns.append(col_name)
            converted_ingest_schema.add(col_name, IntegerType())
        elif col_type == ArrayType(DoubleType()) and (col_name, ArrayType(FloatType())) in ft_columns:
            converted_ingest_schema.add(col_name, ArrayType(FloatType()))
        else:
            converted_ingest_schema.add(col_name, col_type)

    if int_converted_columns:
        logger.warning(
            f"Tecton is casting field(s) {', '.join(int_converted_columns)} to type Integer (was type Long). To remove this warning, use a Long type in the schema."
        )

    return converted_ingest_schema
