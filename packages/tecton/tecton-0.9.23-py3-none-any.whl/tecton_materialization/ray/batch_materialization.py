import contextlib
from typing import List
from typing import Tuple

import pyarrow

from tecton_core import offline_store
from tecton_core.compute_mode import ComputeMode
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query.builder import build_materialization_querytree
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.query_tree_executor import QueryTreeExecutor
from tecton_materialization.common.task_params import TimeInterval
from tecton_materialization.common.task_params import feature_definition_from_task_params
from tecton_materialization.common.task_params import job_query_intervals
from tecton_materialization.ray.job_status import JobStatusClient
from tecton_materialization.ray.materialization_utils import get_delta_writer
from tecton_materialization.ray.materialization_utils import write_to_online_store
from tecton_materialization.ray.nodes import AddTimePartitionNode
from tecton_proto.materialization.job_metadata_pb2 import TectonManagedStage
from tecton_proto.materialization.params_pb2 import MaterializationTaskParams
from tecton_proto.offlinestore.delta import metadata_pb2


PYARROW_ASC = "ascending"
PYARROW_DESC = "descending"


def run_batch_materialization(
    materialization_task_params: MaterializationTaskParams,
    job_status_client: JobStatusClient,
    executor: QueryTreeExecutor,
):
    intervals = job_query_intervals(materialization_task_params)
    for idx, interval in enumerate(intervals):
        job_status_client.set_query_index(idx, len(intervals))
        materialize_interval(
            interval=interval,
            materialization_task_params=materialization_task_params,
            job_status_client=job_status_client,
            executor=executor,
        )


def materialize_interval(
    interval: TimeInterval,
    materialization_task_params: MaterializationTaskParams,
    job_status_client: JobStatusClient,
    executor: QueryTreeExecutor,
):
    fd = feature_definition_from_task_params(materialization_task_params)
    assert fd.writes_to_offline_store, f"Offline materialization is required for FeatureView {fd.id} ({fd.name})"
    assert fd.has_delta_offline_store, f"Delta is required for FeatureView {fd.id} ({fd.name})"

    qt = _get_batch_materialization_plan(fd, interval)
    materialized_data = executor.exec_qt(qt).result_table

    # Sorting rows withing batches helps improve writing parquet files: fewer partitions are written in parallel.
    # Also, secondary sorting by join keys can improve reading performance (if filter by join key will be pushed down to arrow reader).
    materialized_data = sort_rows_in_batches(
        materialized_data,
        by=[(offline_store.TIME_PARTITION, PYARROW_ASC), *[(key, PYARROW_ASC) for key in fd.join_keys]],
    )

    should_write_to_online_store = (
        materialization_task_params.batch_task_info.batch_parameters.write_to_online_feature_store
    )

    offline_stage_monitor = job_status_client.create_stage_monitor(
        TectonManagedStage.StageType.OFFLINE_STORE,
        "Unload features to offline store",
    )
    online_stage_monitor = (
        job_status_client.create_stage_monitor(
            TectonManagedStage.StageType.ONLINE_STORE,
            "Unload features to online store",
        )
        if should_write_to_online_store
        else None
    )

    is_overwrite = materialization_task_params.batch_task_info.batch_parameters.is_overwrite

    delta_writer = get_delta_writer(materialization_task_params)
    parts = None
    with offline_stage_monitor():
        transaction_metadata = metadata_pb2.TectonDeltaMetadata()
        transaction_metadata.feature_start_time.FromDatetime(interval.start)
        transaction_exists = delta_writer.transaction_exists(transaction_metadata)
        if not is_overwrite and transaction_exists:
            print(
                f"Found previous commit with metadata {transaction_metadata} for data in range {interval.start} - {interval.end}. Skipping writing to delta table."
            )
        else:

            @delta_writer.transaction(transaction_metadata)
            def txn() -> List[str]:
                if is_overwrite:
                    delta_writer.delete_time_range(interval)
                return delta_writer.write(materialized_data)

            parts = txn()

    if should_write_to_online_store:
        with online_stage_monitor(), contextlib.ExitStack() as stack:
            if parts is None:
                # We skipped the txn because of matching metadata, but we still need to write out the parquet files for
                # the online store writer. We can accomplish this by using write() and then later abort() to delete
                # the files when we're done with them.
                parts = delta_writer.write(materialized_data)
                stack.callback(delta_writer.abort)

            # TODO(meastham): Probably should send these all at once to the online store copier
            for uri in parts:
                write_to_online_store(
                    materialization_task_params.online_store_writer_config,
                    materialization_task_params.feature_view,
                    materialization_task_params.batch_task_info.batch_parameters.feature_end_time,
                    fd,
                    uri,
                )


def _get_batch_materialization_plan(fd: FeatureDefinitionWrapper, interval: TimeInterval) -> NodeRef:
    tree = build_materialization_querytree(
        dialect=Dialect.DUCKDB,
        compute_mode=ComputeMode.RIFT,
        fdw=fd,
        for_stream=False,
        feature_data_time_limits=interval.to_pendulum(),
    )
    return AddTimePartitionNode.for_feature_definition(fd, tree)


def sort_rows_in_batches(reader: pyarrow.RecordBatchReader, by: List[Tuple[str, str]]) -> pyarrow.RecordBatchReader:
    """
    Create new RecordBatchReader with rows sorted within each batch.

    :param reader: iterator over record batches
    :param by: sorting conditions - list of tuple(name, order)
    """

    def batch_iter():
        while True:
            try:
                next_batch = reader.read_next_batch()
            except StopIteration:
                return

            yield next_batch.sort_by(by)

    return pyarrow.RecordBatchReader.from_batches(reader.schema, batch_iter())
