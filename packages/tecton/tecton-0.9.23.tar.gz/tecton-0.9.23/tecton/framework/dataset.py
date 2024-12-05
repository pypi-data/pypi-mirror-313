import base64
import glob
import io
import json
import logging
import os
from typing import Optional
from typing import Union
from urllib.parse import urlparse

import boto3
import pandas as pd
import pyspark
from google.protobuf.json_format import MessageToJson
from pyspark.sql.types import StructType

from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals.display import Displayable
from tecton._internals.sdk_decorators import sdk_public_method
from tecton.framework.data_frame import TectonDataFrame
from tecton.tecton_context import TectonContext
from tecton_core.id_helper import IdHelper
from tecton_proto.data.saved_feature_data_frame_pb2 import SavedFeatureDataFrame
from tecton_proto.data.saved_feature_data_frame_pb2 import SavedFeatureDataFrameType
from tecton_proto.metadataservice.metadata_service_pb2 import ArchiveSavedFeatureDataFrameRequest
from tecton_proto.metadataservice.metadata_service_pb2 import CreateSavedFeatureDataFrameRequest
from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper


logger = logging.getLogger(__name__)


class Dataset(TectonDataFrame):
    """
    Dataset class.

    Persisted data consisting of entity & request keys, timestamps, and calculated features. Datasets are
    associated with either a :class:`FeatureService` or :class:`FeatureView`.

    There are 2 types of Datasets: Saved and Logged.

    Saved Datasets are generated manually when calling :meth:`tecton.get_historical_features` by setting the ``save``
    parameter.

    Logged Datasets are generated automatically when declaring a :class:`FeatureService` with :class:`tecton.LoggingConfig`,
    and the data is continuously added to it when requesting online data from the FeatureService.

    To get an existing Dataset, call :py:meth:`tecton.get_dataset`.
    """

    _proto: SavedFeatureDataFrame = None

    def __init__(self, proto: SavedFeatureDataFrame, spark_df: pyspark.sql.DataFrame, pandas_df: pd.DataFrame):
        super().__init__(spark_df, pandas_df, snowflake_df=None, querytree=None)
        self._proto = proto

    @classmethod
    def _from_proto(cls, proto):
        return cls(proto, None, None)

    @sdk_public_method
    def to_spark(self) -> pyspark.sql.DataFrame:
        """Converts the Dataset to a Spark DataFrame and returns it."""
        self._try_fetch_spark_df()
        return super().to_spark()

    @sdk_public_method
    def to_pandas(self) -> pd.DataFrame:
        """Converts the Dataset to a Pandas DataFrame and returns it."""
        if self._pandas_df is not None:
            return self._pandas_df

        self._try_fetch_spark_df()
        return super().to_pandas()

    @sdk_public_method
    def fetch_as_pandas(self, n_samples: Optional[int] = None, **kwargs) -> pd.DataFrame:
        """
        Fetches a saved dataset from S3 as a pandas DataFrame.

        :param n_samples: Number of samples to read from parquet files. If None, read all.
        :param kwargs: Additional arguments to pass to pd.read_parquet function.
        :return: pandas DataFrame containing the saved dataset
        """
        # TODO: support Logged datasets and mimic how we use spark schema to correct avro types
        if self._type == SavedFeatureDataFrameType.LOGGED:
            raise errors.UNSUPPORTED_FETCH_AS_PANDAS_AVRO

        # TODO: allow other storage options for datasets
        # at the moment, Datasets are created with s3 as the only option
        # local path support is just for debugging
        if self._path.startswith("s3://"):
            o = urlparse(self._path, allow_fragments=False)
            s3_bucket, path_prefix = o.netloc, o.path.lstrip("/")
            # TODO: assumes user has local aws creds setup
            s3_client = boto3.client("s3")
            s3 = boto3.resource("s3")

            keys = [
                item.key
                for item in s3.Bucket(s3_bucket).objects.filter(Prefix=path_prefix)
                if item.key.endswith(".parquet")
            ]

            def read_func(key):
                obj = s3_client.get_object(Bucket=s3_bucket, Key=key)
                return pd.read_parquet(io.BytesIO(obj["Body"].read()), **kwargs)

        elif os.path.exists(self._path):
            keys = glob.glob(os.path.join(self._path, "*.parquet"))

            def read_func(key):
                return pd.read_parquet(key, **kwargs)

        else:
            raise errors.INVALID_DATASET_PATH(self._path)

        if not keys:
            logger.warning(f"Dataset {self.name} does not have any materialized data in {self.storage_location}.")
            schema = self._get_schema()
            return pd.DataFrame(columns=[field.name for field in schema.fields])

        def read_parquet_files(keys, n_samples):
            total_yielded = 0
            for key in keys:
                if n_samples is not None and total_yielded >= n_samples:
                    break
                df = read_func(key)
                rows_to_yield = (n_samples - total_yielded) if n_samples is not None else None
                yield df.iloc[:rows_to_yield] if rows_to_yield else df
                total_yielded += len(df)

        self._pandas_df = pd.concat(read_parquet_files(keys, n_samples), ignore_index=True)
        return self._pandas_df

    # Creates and returns an empty Spark dataframe & pandas dataframe with desired schema
    def _create_empty_dfs(self):
        schema = self._get_schema()
        spark = TectonContext.get_instance()._get_spark()

        spark_df = spark.createDataFrame(spark.sparkContext.emptyRDD(), schema)
        pandas_df = pd.DataFrame(columns=[field.name for field in schema.fields])
        return spark_df, pandas_df

    def _get_schema(self) -> StructType:
        schema_json = json.loads(MessageToJson(self._proto.schema))
        fields = []
        for field in schema_json["fields"]:
            fields.append(json.loads(field["structfieldJson"]))

        return StructType.fromJson({"fields": fields})

    # Tries fetching self._spark_df. As long as the underlying data exists,
    # it's expected to succeed. However, in certain cases self._spark_df may stay None.
    # For example, if this is a logged dataset and there are not feature requests logged
    # yet, self._spark_df will stay None after the execution of this method.
    def _try_fetch_spark_df(self):
        if self._spark_df is not None:
            return
        spark = TectonContext.get_instance()._get_spark()
        try:
            if self._type == SavedFeatureDataFrameType.LOGGED:
                # Logged datasets are in Avro format
                self._spark_df = spark.read.format("avro").load(self._path)
                self._spark_df = _convert_logged_df_schema(self._spark_df)
            else:
                self._spark_df = spark.read.parquet(self._path)
        except pyspark.sql.utils.AnalysisException as e:
            # If the path doesn't exist in S3, there is no data
            # This can happen for logged features when there is no logs yet,
            # so we don't want to throw an error in this case
            if "Path does not exist" in e.desc:
                self._spark_df, self._pandas_df = self._create_empty_dfs()
            else:
                raise e

    @sdk_public_method
    def summary(self) -> Displayable:
        """
        Print out a summary of this class's attributes.
        """
        return Displayable.from_properties(items=self._summary_items())

    def _summary_items(self):
        items = [
            ("Name", self.name),
            ("Id", IdHelper.to_string(self._proto.saved_feature_dataframe_id)),
            ("Created At", self._proto.info.created_at.ToJsonString()),
            ("Workspace", self._proto.info.workspace or "prod"),
            ("Tecton Log Commit Id", self._proto.state_update_entry_commit_id),
            ("Type", "Logged" if self._type == SavedFeatureDataFrameType.LOGGED else "Saved"),
        ]
        items.append(self._get_source())
        if len(self._proto.join_key_column_names) > 0:
            items.append(("Join & Request Keys", ", ".join(self._proto.join_key_column_names)))
        if self._proto.HasField("timestamp_column_name"):
            items.append(("Timestamp Key", self._proto.timestamp_column_name))
        return items

    def _get_source(self):
        if self._proto.HasField("feature_package_name"):
            return ("Source FeatureView", self._proto.feature_package_name)
        elif self._proto.HasField("feature_service_name"):
            return ("Source FeatureService", self._proto.feature_service_name)
        else:
            # should be unreachable
            assert False, "Neither feature_package_name nor feature_service_name set in the proto"

    def _delete(self):
        """
        Delete this Dataset. Note that this deletes the underlying data as well as removing the Dataset object from
        Tecton.
        """
        request = ArchiveSavedFeatureDataFrameRequest()
        request.saved_feature_dataframe_id.CopyFrom(IdHelper.from_string(self._id))
        metadata_service.instance().ArchiveSavedFeatureDataFrame(request)
        logger.info(f"Dataset {self.name} deleted")

    @sdk_public_method
    def get_spine_dataframe(self) -> TectonDataFrame:
        logger.warning(errors.GET_SPINE_DF_DEPRECATED)
        return self.get_events_dataframe()

    @sdk_public_method
    def get_events_dataframe(self) -> TectonDataFrame:
        """
        Get a :py:class:`tecton.TectonDataFrame` containing the spine.
        """
        if not (self._proto.join_key_column_names and self._proto.timestamp_column_name):
            raise errors.DATASET_SPINE_COLUMNS_NOT_SET

        if self._pandas_df is not None:
            spine_pandas_df = self._pandas_df[
                self._proto.join_key_column_names[:] + [self._proto.timestamp_column_name]
            ].copy()
            return TectonDataFrame(None, spine_pandas_df)

        self._try_fetch_spark_df()
        spine_spark_df = self._spark_df.select(
            self._proto.join_key_column_names[:] + [self._proto.timestamp_column_name]
        )
        return TectonDataFrame(spine_spark_df, None)

    @property
    def name(self):
        """
        Dataset name
        """
        return self._proto.info.name

    @property
    def is_archived(self) -> bool:
        """
        Whether the dataset record is archived.
        Stored data associated with archived datasets will be cleaned up.
        """
        return self._proto.info.is_archived

    @property
    def storage_location(self):
        """
        Dataset storage location
        """
        return self._path

    @property
    def _id(self):
        return IdHelper.to_string(self._proto.saved_feature_dataframe_id)

    @property
    def _path(self):
        return self._proto.dataframe_location

    @property
    def _feature_service_id(self):
        return IdHelper.to_string(self._proto.feature_service_id)

    @property
    def _type(self):
        return self._proto.type

    @classmethod
    def _create(
        cls,
        df: TectonDataFrame,
        save_as: Optional[str] = None,
        workspace: Optional[str] = None,
        feature_definition_id: Optional[str] = None,
        feature_service_id: Optional[str] = None,
        spine: Optional[Union[pyspark.sql.dataframe.DataFrame, pd.DataFrame]] = None,
        timestamp_key: Optional[str] = None,
    ) -> TectonDataFrame:
        assert (
            feature_definition_id or feature_service_id
        ), "Either feature_definition_id or feature_service_id must be provided"

        create_request = CreateSavedFeatureDataFrameRequest()
        if save_as:
            create_request.name = save_as
        create_request.workspace = workspace
        if feature_definition_id:
            create_request.feature_package_id.CopyFrom(IdHelper.from_string(feature_definition_id))
        if feature_service_id:
            create_request.feature_service_id.CopyFrom(IdHelper.from_string(feature_service_id))
        if spine is not None:
            # note that spine.columns works for both pandas and spark dfs
            spine_cols = [s for s in spine.columns if s != timestamp_key]
            create_request.join_key_column_names.extend(spine_cols)
            if timestamp_key is not None:  # timestamp_key can be none for odfvs
                create_request.timestamp_column_name = timestamp_key
        create_request.schema.CopyFrom(SparkSchemaWrapper.from_spark_schema(df.to_spark().schema))
        response = metadata_service.instance().CreateSavedFeatureDataFrame(create_request)
        proto = response.saved_feature_dataframe
        logger.info(f"Saved Dataset with name {proto.info.name}")
        logger.debug(f"Path is {proto.dataframe_location}")

        df.to_spark().write.save(path=proto.dataframe_location, format="parquet", mode="errorifexists")
        return cls(proto, df._spark_df, df._pandas_df)

    def __repr__(self):
        source_type, source_value = self._get_source()
        source_str = f"{source_type}='{source_value}'"
        return (
            f"{type(self).__name__}(name='{self.name}', "
            + f"{source_str}, created_at='{self._proto.info.created_at.ToJsonString()}')"
        )


def _convert_logged_df_schema(spark_df: pyspark.sql.DataFrame):
    if spark_df is None:
        return
    # Note: _partition column is not used right now, but in future
    # it can be used to optimize time-range access of this dataframe
    spark_df = spark_df.drop("_partition")
    # Note: the rest of the column names are base16 encoded due to strict
    # Avro column name validation (only [_a-zA-Z0-9] allowed). The encoding
    # happens here:
    for column in spark_df.columns:
        new_column = base64.b16decode(column[1:], casefold=True).decode()
        spark_df = spark_df.withColumnRenamed(column, new_column)
    return spark_df
