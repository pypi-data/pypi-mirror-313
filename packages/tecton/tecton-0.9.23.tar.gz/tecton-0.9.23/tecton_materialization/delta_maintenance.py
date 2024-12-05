import logging

from pyspark.sql import SparkSession

from tecton_proto.materialization.params_pb2 import MaterializationTaskParams
from tecton_spark.offline_store import DeltaMetadataWriter


logger = logging.getLogger(__name__)


def run_delta_maintenance(spark: SparkSession, materialization_task_params: MaterializationTaskParams):
    path = materialization_task_params.offline_store_path
    delta_metadata_writer = DeltaMetadataWriter(spark)
    delta_maintenance_params = materialization_task_params.delta_maintenance_task_info.delta_maintenance_parameters
    if delta_maintenance_params.generate_manifest:
        # regardless, the manual run is necessary because the auto generation
        # is not safe to race conditions. see https://docs.delta.io/latest/presto-integration.html#language-python
        delta_metadata_writer.generate_symlink_manifest(path)
    if delta_maintenance_params.execute_compaction:
        delta_metadata_writer.optimize_execute_compaction(path)
    if delta_maintenance_params.vacuum:
        delta_metadata_writer.vacuum(path)
