import time
from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from typing import List
from typing import Optional

from tecton._internals import metadata_service
from tecton._internals import utils
from tecton._internals.display import Displayable
from tecton_proto.common import id_pb2
from tecton_proto.data.materialization_status_pb2 import MaterializationStatus
from tecton_proto.materializationjobservice.materialization_job_service_pb2 import CancelJobRequest
from tecton_proto.materializationjobservice.materialization_job_service_pb2 import GetJobRequest
from tecton_proto.materializationjobservice.materialization_job_service_pb2 import GetLatestReadyTimeRequest
from tecton_proto.materializationjobservice.materialization_job_service_pb2 import GetLatestReadyTimeResponse
from tecton_proto.materializationjobservice.materialization_job_service_pb2 import JobAttempt
from tecton_proto.materializationjobservice.materialization_job_service_pb2 import ListJobsRequest
from tecton_proto.materializationjobservice.materialization_job_service_pb2 import MaterializationJob
from tecton_proto.materializationjobservice.materialization_job_service_pb2 import MaterializationJobRequest
from tecton_proto.metadataservice.metadata_service_pb2 import GetMaterializationStatusRequest


class MaterializationTimeoutException(Exception):
    pass


class MaterializationJobFailedException(Exception):
    pass


@dataclass
class MaterializationAttemptData:
    """
    Data representation of the materialization job attempt.

    Materialization job may have multiple attempts to materialize features.

    :param id: ID string of the materialization attempt.
    :param run_url: URL to track materialization attempt.
    :param state: State of the materialization attempt.
    :param created_at: Materialization attempt creation timestamp.
    :param updated_at: Materialization attempt update timestamp.
    """

    id: str
    run_url: str
    state: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_proto(cls, proto: JobAttempt):
        created_at = datetime.utcfromtimestamp(proto.created_at.seconds)
        updated_at = datetime.utcfromtimestamp(proto.updated_at.seconds)
        return cls(id=proto.id, run_url=proto.run_url, state=proto.state, created_at=created_at, updated_at=updated_at)


@dataclass
class MaterializationJobData:
    """
    Data representation of the materialization job

    :param id: ID string of the materialization job.
    :param workspace: Name of the project workspace.
    :param feature_view: Name of the Feature View.
    :param state: State of the materialization job.
    :param online: Whether the job materializes features to the online store.
    :param offline: Whether the job materializes features to the offline store.
    :param start_time: Start timestamp of the batch materialization window.
    :param end_time: End timestamp of the batch materialization window.
    :param created_at: Job creation timestamp.
    :param updated_at: Job update timestamp.
    :param attempts: Materialization attempts. List of :class:`MaterializationAttemptData`
    :param next_attempt_at: If job needs another attempt, Start timestamp the next materialization attempt.
    :param job_type: Type of materialization. One of 'BATCH' or 'STREAM'.
    """

    id: str
    workspace: str
    feature_view: str
    state: str
    online: bool
    offline: bool
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    attempts: List[MaterializationAttemptData]
    next_attempt_at: Optional[datetime]
    job_type: str

    @classmethod
    def from_proto(cls, proto: MaterializationJob):
        start_time = datetime.utcfromtimestamp(proto.start_time.seconds) if proto.HasField("start_time") else None
        end_time = datetime.utcfromtimestamp(proto.end_time.seconds) if proto.HasField("end_time") else None
        created_at = datetime.utcfromtimestamp(proto.created_at.seconds)
        updated_at = datetime.utcfromtimestamp(proto.updated_at.seconds)
        attempts = [MaterializationAttemptData.from_proto(attempt_proto) for attempt_proto in proto.attempts]
        next_attempt_at = (
            datetime.utcfromtimestamp(proto.next_attempt_at.seconds) if proto.HasField("next_attempt_at") else None
        )
        return cls(
            id=proto.id,
            workspace=proto.workspace,
            feature_view=proto.feature_view,
            state=proto.state,
            online=proto.online,
            offline=proto.offline,
            start_time=start_time,
            end_time=end_time,
            created_at=created_at,
            updated_at=updated_at,
            attempts=attempts,
            next_attempt_at=next_attempt_at,
            job_type=proto.job_type,
        )


def trigger_materialization_job(
    feature_view: str,
    workspace: str,
    start_time: datetime,
    end_time: datetime,
    online: bool,
    offline: bool,
    use_tecton_managed_retries: bool = True,
    overwrite: bool = False,
) -> str:
    """
    Starts a batch materialization job for this Feature View.

    :param start_time: The job will materialize feature values between the start_time and end_time.
    :param end_time: The job will materialize feature values between the start_time and end_time.
    :param online: Whether the job will materialize features to the online store.
        The Feature View must be configured with online=True in order to materialize features online.
    :param offline: Whether the job will materialize features to the offline store.
        The Feature View must be configured with offline=True in order to materialize features offline.
    :param use_tecton_managed_retries: If enabled, Tecton will automatically retry failed attempts.
        Disable to manage your own retry behavior.
    :param overwrite: If enabled, you will be able to run materialization jobs for periods that previously have materialized data.
        This operation can be sensitive for feature views with existing materialized online data.
        For the offline store, all previously materialized data between the start time and end time will be dropped.
        For the online store, all previous data will remain, but may be overwritten by this job.
    :return: ID string of the created materialization job.
    :raises TectonValidationError: If job params are not valid.
    """
    request = MaterializationJobRequest()
    request.feature_view = feature_view
    request.workspace = workspace
    request.start_time.FromDatetime(start_time)
    request.end_time.FromDatetime(end_time)
    request.online = online
    request.offline = offline
    request.use_tecton_managed_retries = use_tecton_managed_retries
    request.overwrite = overwrite

    mds_instance = metadata_service.instance()
    response = mds_instance.SubmitMaterializationJob(request)
    return response.job.id


def list_materialization_jobs(feature_view: str, workspace: str) -> List[MaterializationJobData]:
    """
    Retrieves the list of all materialization jobs for this Feature View.

    :return: List of :class:`MaterializationJobData` objects.
    """
    request = ListJobsRequest()
    request.feature_view = feature_view
    request.workspace = workspace

    mds_instance = metadata_service.instance()
    response = mds_instance.ListMaterializationJobs(request)
    return [MaterializationJobData.from_proto(job) for job in response.jobs]


def get_materialization_job(feature_view: str, workspace: str, job_id: str) -> MaterializationJobData:
    """
    Retrieves data about the specified materialization job for this Feature View.

    This data includes information about job attempts.

    :param job_id: ID string of the materialization job.
    :return: :class:`MaterializationJobData` object for the job.
    """
    request = GetJobRequest()
    request.feature_view = feature_view
    request.workspace = workspace
    request.job_id = job_id

    mds_instance = metadata_service.instance()
    response = mds_instance.GetMaterializationJob(request)
    return MaterializationJobData.from_proto(response.job)


def get_latest_ready_time(feature_view: str, workspace: str) -> GetLatestReadyTimeResponse:
    request = GetLatestReadyTimeRequest()
    request.feature_view = feature_view
    request.workspace = workspace

    mds_instance = metadata_service.instance()
    return mds_instance.GetLatestReadyTime(request)


def cancel_materialization_job(feature_view: str, workspace: str, job_id: str) -> MaterializationJobData:
    """
    Cancels the scheduled or running batch materialization job for this Feature View specified by the job identifier.
    Once cancelled, a job will not be retried further.

    Job run state will be set to MANUAL_CANCELLATION_REQUESTED.
    Note that cancellation is asynchronous, so it may take some time for the cancellation to complete.
    If job run is already in MANUAL_CANCELLATION_REQUESTED or in a terminal state then it'll return the job.

    :param job_id: ID string of the materialization job.
    :return: :class:`MaterializationJobData` object for the cancelled job.
    """
    request = CancelJobRequest()
    request.feature_view = feature_view
    request.workspace = workspace
    request.job_id = job_id

    mds_instance = metadata_service.instance()
    response = mds_instance.CancelMaterializationJob(request)
    return MaterializationJobData.from_proto(response.job)


def wait_for_materialization_job(
    feature_view: str,
    workspace: str,
    job_id: str,
    timeout: Optional[timedelta] = None,
) -> MaterializationJobData:
    """
    Blocks until the specified job has been completed.

    :param job_id: ID string of the materialization job.
    :param timeout: (Optional) timeout for this function.
        An exception is raised if the job does not complete within the specified time.
    :return: :class:`MaterializationJobData` object for the successful job.
    :raises MaterializationTimeoutException:
        If timeout param is specified and job does not complete within the specified time.
    :raises MaterializationJobFailedException: If materialization job did not reach a successful state.
    """
    wait_start_time = datetime.now()
    while True:
        job_data = get_materialization_job(feature_view, workspace, job_id)
        run_state = job_data.state

        if run_state == "SUCCESS":
            return job_data
        elif timeout and ((datetime.now() - wait_start_time) > timeout):
            msg = f"job {job_id} timed out, last job state {run_state}"
            raise MaterializationTimeoutException(msg)
        elif run_state == "RUNNING":
            time.sleep(60)
        else:
            msg = f"job {job_id} failed, last job state {run_state}"
            raise MaterializationJobFailedException(msg)


def get_materialization_status_response(id_proto: id_pb2.Id, workspace: str) -> MaterializationStatus:
    """Returns MaterializationStatus proto for the FeatureView."""
    request = GetMaterializationStatusRequest()
    request.feature_package_id.CopyFrom(id_proto)
    request.workspace = workspace

    response = metadata_service.instance().GetMaterializationStatus(request)
    return response.materialization_status


def _create_materialization_table(column_names: List[str], materialization_status_rows: List[List]) -> Displayable:
    # Setting `max_width=0` creates a table with an unlimited width.
    table = Displayable.from_table(headings=column_names, rows=materialization_status_rows, max_width=0)
    # Align columns in the middle horizontally
    table._text_table.set_cols_align(["c" for _ in range(len(column_names))])

    return table


def get_materialization_status_for_display(
    id_proto: id_pb2.Id, workspace: str, verbose: bool, limit: int, sort_columns: Optional[str], errors_only: bool
) -> Displayable:
    materialization_attempts = get_materialization_status_response(id_proto, workspace).materialization_attempts
    column_names, materialization_status_rows = utils.format_materialization_attempts(
        materialization_attempts, verbose, limit, sort_columns, errors_only
    )

    return _create_materialization_table(column_names, materialization_status_rows)
