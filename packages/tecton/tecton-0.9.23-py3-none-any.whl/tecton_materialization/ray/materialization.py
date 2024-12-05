import base64
import contextlib
import logging
import os
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

import pyarrow.fs
import ray

from tecton_core import conf
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.query_tree_compute import SQLCompute
from tecton_core.query.query_tree_executor import QueryTreeExecutor
from tecton_core.query.snowflake.compute import SnowflakeCompute
from tecton_core.secrets import SecretResolver
from tecton_core.snowflake_context import SnowflakeContext
from tecton_materialization.common.job_metadata import JobMetadataClient
from tecton_materialization.common.task_params import feature_definition_from_task_params
from tecton_materialization.ray.batch_materialization import run_batch_materialization
from tecton_materialization.ray.delta import DeltaWriter
from tecton_materialization.ray.feature_export import get_feature_export_qt
from tecton_materialization.ray.feature_export import get_feature_export_store_params
from tecton_materialization.ray.ingest_materialization import ingest_pushed_df
from tecton_materialization.ray.job_status import JobStatusClient
from tecton_materialization.ray.job_status import MonitoringContextProvider
from tecton_materialization.ray.materialization_utils import get_delta_writer
from tecton_materialization.ray.materialization_utils import run_online_store_copier
from tecton_materialization.secrets import MDSSecretResolver
from tecton_proto.materialization.job_metadata_pb2 import TectonManagedStage
from tecton_proto.materialization.params_pb2 import MaterializationTaskParams
from tecton_proto.materialization.params_pb2 import SecretMaterializationTaskParams
from tecton_proto.materialization.params_pb2 import SecretServiceParams
from tecton_proto.offlinestore.delta import metadata_pb2
from tecton_proto.online_store_writer.copier_pb2 import DeletionRequest
from tecton_proto.online_store_writer.copier_pb2 import OnlineStoreCopierRequest


logger = logging.getLogger(__name__)

FEATURE_EXPORT_TASK_TYPE = "feature_export"

_DIALECT_TO_STAGE_TYPE = {
    Dialect.PANDAS: TectonManagedStage.PYTHON,
    Dialect.DUCKDB: TectonManagedStage.PYTHON,
    Dialect.SNOWFLAKE: TectonManagedStage.SNOWFLAKE,
}

_DIALECT_TO_UI_STRING = {
    Dialect.PANDAS: "Python",
    Dialect.DUCKDB: "Python",
    Dialect.SNOWFLAKE: "Snowflake",
}


def _get_compute(dialect: Dialect, qt: NodeRef, secret_resolver: Optional[SecretResolver]) -> SQLCompute:
    if dialect == Dialect.SNOWFLAKE:
        if SnowflakeContext.is_initialized():
            return SnowflakeCompute.for_connection(SnowflakeContext.get_instance().get_connection())
        else:
            return SnowflakeCompute.for_query_tree(qt, secret_resolver)
    return SQLCompute.for_dialect(dialect)


def _delete_from_online_store(
    materialization_task_params: MaterializationTaskParams, job_status_client: JobStatusClient
) -> None:
    online_stage_monitor = job_status_client.create_stage_monitor(
        TectonManagedStage.StageType.ONLINE_STORE,
        "Unload features to online store",
    )
    with online_stage_monitor() as progress_callback:
        if materialization_task_params.deletion_task_info.deletion_parameters.HasField("online_join_keys_path"):
            deletion_request = DeletionRequest(
                online_join_keys_path=materialization_task_params.deletion_task_info.deletion_parameters.online_join_keys_path,
            )
        else:
            deletion_request = DeletionRequest(
                online_join_keys_full_path=materialization_task_params.deletion_task_info.deletion_parameters.online_join_keys_full_path,
            )
        request = OnlineStoreCopierRequest(
            online_store_writer_configuration=materialization_task_params.online_store_writer_config,
            feature_view=materialization_task_params.feature_view,
            deletion_request=deletion_request,
        )
        run_online_store_copier(request)
    progress_callback(1.0)


def _delete_from_offline_store(params: MaterializationTaskParams, job_status_client: JobStatusClient):
    offline_uri = params.deletion_task_info.deletion_parameters.offline_join_keys_path
    fs, path = pyarrow.fs.FileSystem.from_uri(offline_uri)
    keys_table = pyarrow.dataset.dataset(source=path, filesystem=fs).to_table()
    offline_stage_monitor = job_status_client.create_stage_monitor(
        TectonManagedStage.StageType.OFFLINE_STORE, "Delete keys from offline store"
    )
    with offline_stage_monitor():
        delta_writer = get_delta_writer(params)
        delta_writer.delete_keys(keys_table)
        delta_writer.commit()


def _feature_export(
    fd: FeatureDefinitionWrapper,
    task_params: MaterializationTaskParams,
    job_status_client: JobStatusClient,
    executor: QueryTreeExecutor,
):
    export_params = task_params.feature_export_info.feature_export_parameters
    start_time = export_params.feature_start_time.ToDatetime()
    end_time = export_params.feature_end_time.ToDatetime()
    table_uri = export_params.export_store_path
    store_params = get_feature_export_store_params(fd)
    delta_writer = get_delta_writer(task_params, store_params_override=store_params, table_uri_override=table_uri)
    delta_write_monitor = job_status_client.create_stage_monitor(
        TectonManagedStage.StageType.OFFLINE_STORE,
        "Write full features to offline store.",
    )

    _run_export(fd, start_time, end_time, executor, delta_writer, delta_write_monitor)


def _run_export(
    fd: FeatureDefinitionWrapper,
    start_time: datetime,
    end_time: datetime,
    qt_executor: QueryTreeExecutor,
    delta_writer: DeltaWriter,
    write_monitor: MonitoringContextProvider,
):
    qt, interval = get_feature_export_qt(fd, start_time, end_time)
    feature_data = qt_executor.exec_qt(qt).result_table

    with write_monitor():
        # TODO (TEC-18865): add support for is_overwrite flag for feature_export jobs
        transaction_metadata = metadata_pb2.TectonDeltaMetadata()
        transaction_metadata.feature_start_time.FromDatetime(interval.start)

        @delta_writer.transaction(transaction_metadata)
        def txn():
            delta_writer.delete_time_range(interval)
            delta_writer.write(feature_data)

        txn()


@contextlib.contextmanager
def _ray():
    print(f"Initializing Ray from classpath: {os.environ['CLASSPATH']}")
    ray.init(
        job_config=ray.job_config.JobConfig(code_search_path=os.environ["CLASSPATH"].split(":")),
        include_dashboard=False,
    )
    try:
        yield
    finally:
        ray.shutdown()


def run_materialization(
    materialization_task_params: MaterializationTaskParams,
    secret_materialization_task_params: SecretMaterializationTaskParams,
) -> None:
    logger.info(f"Starting materialization job for task: {materialization_task_params.materialization_task_id}")
    conf.set("DUCKDB_DEBUG", "true")
    conf.set("TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE", "rift")
    conf.set("TECTON_RUNTIME_MODE", "MATERIALIZATION")
    assert materialization_task_params.feature_view.schemas.HasField("materialization_schema"), "missing schema"
    job_status_client = JobStatusClient(JobMetadataClient.for_params(materialization_task_params))
    try:
        with _ray():
            run_ray_job(materialization_task_params, secret_materialization_task_params, job_status_client)
    except Exception:
        job_status_client.set_current_stage_failed(TectonManagedStage.ErrorType.UNEXPECTED_ERROR)
        raise


def run_ray_job(
    materialization_task_params: MaterializationTaskParams,
    secret_materialization_task_params: SecretMaterializationTaskParams,
    job_status_client: JobStatusClient,
) -> None:
    fd = feature_definition_from_task_params(materialization_task_params)
    secret_resolver = _get_secret_resolver(secret_materialization_task_params.secret_service_params)
    task_type = _get_task_type(materialization_task_params)
    executor = QueryTreeExecutor(monitor=job_status_client, secret_resolver=secret_resolver)

    if task_type == "deletion_task":
        _delete_from_offline_store(materialization_task_params, job_status_client)
        _delete_from_online_store(materialization_task_params, job_status_client)
    elif task_type == "delta_maintenance_task":
        # TODO (TEC-19141): delta-rs maintenance commits are incompatible with delta standalone library
        # delta_writer = get_delta_writer(materialization_task_params)
        # maintenance_params = materialization_task_params.delta_maintenance_task_info.delta_maintenance_parameters
        # delta_log_table_name = materialization_task_params.delta_log_table
        # delta_log_table_region = materialization_task_params.dynamodb_table_region
        # cross_account_role = (
        #     materialization_task_params.dynamodb_cross_account_role
        #     if materialization_task_params.HasField("dynamodb_cross_account_role")
        #     else None
        # )
        # delta_writer.run_maintenance(
        #     maintenance_params.execute_compaction,
        #     maintenance_params.vacuum,
        #     delta_log_table_name,
        #     delta_log_table_region,
        #     cross_account_role,
        # )
        print("Delta maintenance not supported.")
    elif task_type == "ingest_task":
        ingest_pushed_df(materialization_task_params, fd, job_status_client)
    elif task_type == FEATURE_EXPORT_TASK_TYPE:
        _feature_export(fd, materialization_task_params, job_status_client, executor)
    elif task_type == "batch_task":
        run_batch_materialization(materialization_task_params, job_status_client, executor)
    else:
        msg = f"Task type {task_type} is not supported by Ray materialization job"
        raise ValueError(msg)


def _get_task_type(materialization_task_params: MaterializationTaskParams) -> str:
    return materialization_task_params.WhichOneof("task_info")[:-5]  # removesuffix("_info")


def _get_secret_resolver(
    secret_service_params: SecretServiceParams,
) -> Optional[SecretResolver]:
    if not secret_service_params.secrets_api_service_url:
        return None

    assert secret_service_params.secret_access_api_key, "Secret access key is required when using secret service"
    return MDSSecretResolver(
        secret_service_params.secrets_api_service_url,
        secret_service_params.secret_access_api_key,
    )


def main():
    params = MaterializationTaskParams()
    secret_params = SecretMaterializationTaskParams()

    # Extract secret m13n params from env vars. VM-based Rift passes secrets via this env var.
    if "SECRET_MATERIALIZATION_PARAMS" in os.environ:
        logger.info("Found secret materialization params, parsing...")
        secret_params.ParseFromString(base64.standard_b64decode(os.environ["SECRET_MATERIALIZATION_PARAMS"]))

    # Legacy way of passing standard m13n params via env vars. Required for compatibility with Anyscale and GCP.
    if "MATERIALIZATION_TASK_PARAMS" in os.environ:
        logger.info("Found legacy materialization task params in env vars, parsing...")
        params.ParseFromString(base64.standard_b64decode(os.environ["MATERIALIZATION_TASK_PARAMS"]))

        # Backwards compatibility for fetching secret access key from materialization task params, if not already found in the secret env var. Anyscale relies on this. Should be removed once Anyscale is completely gone
        # See https://tecton.atlassian.net/browse/TEC-20193
        if params.secrets_api_service_url and not secret_params.secret_service_params:
            secret_service_params = SecretServiceParams()
            secret_service_params.secrets_api_service_url = params.secrets_api_service_url
            secret_service_params.secret_access_api_key = params.secret_access_api_key

            secret_params.secret_service_params = secret_service_params

        run_materialization(params, secret_params)
        return

    # Extract standard m13n params from the object store
    if "MATERIALIZATION_TASK_PARAMS_S3_URL" in os.environ:
        parsed = urlparse(os.environ["MATERIALIZATION_TASK_PARAMS_S3_URL"])
        logger.info(f"Found materialization task params at {parsed}, parsing...")
        import boto3

        bucket = parsed.netloc
        key = parsed.path.lstrip("/")
        s3 = boto3.client("s3")
        resp = s3.get_object(Bucket=bucket, Key=key)
        params.ParseFromString(resp["Body"].read())

        run_materialization(params, secret_params)
        return

    msg = "Materialization params were not provided"
    raise ValueError(msg)


if __name__ == "__main__":
    main()
