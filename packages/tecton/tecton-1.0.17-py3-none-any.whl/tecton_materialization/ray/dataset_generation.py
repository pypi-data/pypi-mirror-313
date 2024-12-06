import multiprocessing

import attrs
import boto3
import pyarrow.parquet as pq

from tecton_core import conf
from tecton_core.compute_mode import ComputeMode
from tecton_core.data_processing_utils import split_spine
from tecton_core.offline_store import DATASET_PARTITION_SIZE
from tecton_core.query.dialect import Dialect
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import PandasDataframeWrapper
from tecton_core.query.nodes import StagingNode
from tecton_core.query.query_tree_executor import QueryTreeExecutor
from tecton_core.query.retrieval_params import GetFeaturesForEventsParams
from tecton_core.query.retrieval_params import GetFeaturesInRangeParams
from tecton_core.query.rewrite import rewrite_tree_for_spine
from tecton_core.query_consts import valid_to
from tecton_materialization.common.dataset_generation import get_features_from_params
from tecton_materialization.common.task_params import get_features_params_from_task_params
from tecton_materialization.ray.delta import OfflineStoreParams
from tecton_materialization.ray.job_status import JobStatusClient
from tecton_materialization.ray.materialization_utils import get_delta_writer
from tecton_materialization.ray.nodes import AddTimePartitionNode
from tecton_materialization.ray.nodes import TimeSpec
from tecton_proto.materialization.job_metadata__client_pb2 import TectonManagedStage
from tecton_proto.materialization.params__client_pb2 import MaterializationTaskParams


# fewer threads means more memory per thread
DEFAULT_NUM_THREADS = multiprocessing.cpu_count() // 2


def run_dataset_generation(
    materialization_task_params: MaterializationTaskParams,
    job_status_client: JobStatusClient,
    executor: QueryTreeExecutor,
):
    # retrieve current region
    conf.set("CLUSTER_REGION", boto3.Session().region_name)

    assert materialization_task_params.dataset_generation_task_info.HasField("dataset_generation_parameters")
    dataset_generation_params = materialization_task_params.dataset_generation_task_info.dataset_generation_parameters
    params = get_features_params_from_task_params(materialization_task_params, compute_mode=ComputeMode.RIFT)

    num_threads = dataset_generation_params.extra_config.get("num_threads", DEFAULT_NUM_THREADS)
    conf.set("DUCKDB_NTHREADS", str(num_threads))

    qts = []

    if isinstance(params, GetFeaturesForEventsParams):
        time_column = params.timestamp_key
        spine_data = pq.read_table(params.events).to_pandas()
        if conf.get_bool("DUCKDB_ENABLE_SPINE_SPLIT"):
            spine_split = split_spine(spine_data, params.join_keys)
            for spine_chunk in spine_split:
                qt = get_features_from_params(params, spine=PandasDataframeWrapper(spine_chunk))
                qts.append(qt)
        else:
            qts.append(get_features_from_params(params, spine=PandasDataframeWrapper(spine_data)))
    elif isinstance(params, GetFeaturesInRangeParams):
        time_column = valid_to()
        entities = (
            PandasDataframeWrapper(pq.read_table(params.entities).to_pandas()) if params.entities is not None else None
        )
        qts.append(get_features_from_params(params, entities=entities))
    else:
        error = f"Unsupported params type: {type(params)}"
        raise ValueError(error)

    qts = [_add_partition_column(qt, time_column) for qt in qts]

    store_params = OfflineStoreParams(
        feature_view_id=params.fco.id,
        feature_view_name=params.fco.name,
        schema=dataset_generation_params.expected_schema,
        time_spec=None,
        feature_store_format_version=None,
        batch_schedule=None,
    )

    table = get_delta_writer(
        materialization_task_params,
        store_params=store_params,
        table_uri=dataset_generation_params.result_path,
        join_keys=params.join_keys,
    )
    offline_stage_monitor = job_status_client.create_stage_monitor(
        TectonManagedStage.StageType.OFFLINE_STORE,
        "Store results to dataset location",
    )
    for idx, qt in enumerate(qts):
        job_status_client.set_query_index(idx, len(qts))

        rewrite_tree_for_spine(qt)
        reader = executor.exec_qt(qt).result_table

        with offline_stage_monitor():
            table.write(reader)

    table.commit()


def _add_partition_column(qt: NodeRef, time_column) -> NodeRef:
    """
    Injects AddTimePartitionNode either before StagingNode(step=AGGREGATION) or at the top of the tree.
    The aim is to run this node before ODFV (if it is present) to make it part of DuckDB query.
    """

    def create_node(input_node: NodeRef) -> NodeRef:
        return AddTimePartitionNode(
            dialect=Dialect.DUCKDB,
            compute_mode=ComputeMode.RIFT,
            input_node=input_node,
            time_spec=TimeSpec(
                timestamp_key=time_column,
                time_column=time_column,
                partition_size=DATASET_PARTITION_SIZE,
                partition_is_anchor=False,
            ),
        ).as_ref()

    def inject(tree: NodeRef) -> bool:
        """
        Traverse over the tree and return True if AddTimePartitionNode was injected before StagingNode(step=AGGREGATION)
        """
        injected = False

        if isinstance(tree.node, StagingNode) and QueryTreeStep.AGGREGATION == tree.node.query_tree_step:
            prev_input = tree.node.input_node
            new_input = create_node(prev_input)
            tree.node = attrs.evolve(tree.node, input_node=new_input)
            injected = True

        return injected or any(inject(tree=i) for i in tree.inputs)

    if inject(qt):
        return qt

    # add node at the top
    return create_node(qt)
