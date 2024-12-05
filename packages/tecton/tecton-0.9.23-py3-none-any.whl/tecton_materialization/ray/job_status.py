import contextlib
import logging
import traceback
import typing
from datetime import datetime
from typing import Optional

from tecton_core.query.executor_utils import QueryTreeMonitor
from tecton_materialization.common.job_metadata import JobMetadataClient
from tecton_proto.materialization.job_metadata_pb2 import JobMetadata
from tecton_proto.materialization.job_metadata_pb2 import TectonManagedStage


logger = logging.getLogger(__name__)

ProgressLogger = typing.Callable[[float], None]
SQLParam = typing.Optional[str]


class MonitoringContextProvider(typing.Protocol):
    def __call__(self, p: SQLParam = None) -> typing.ContextManager[ProgressLogger]: ...


class JobStatusClient(QueryTreeMonitor):
    def __init__(self, metadata_client: JobMetadataClient):
        self._metadata_client = metadata_client
        self._started = False
        self._query_count = 1
        self._query_index = 0

    def set_query_index(self, index: int, count: int):
        if count != self._query_count and self._started:
            msg = "Can't change query count after stages have been created"
            raise ValueError(msg)
        self._query_index = index
        self._query_count = count

    def create_stage(self, stage_type: TectonManagedStage.StageType, description: str) -> int:
        """
        Returns created stage index
        """
        self._started = True

        def _update(job_metadata: JobMetadata) -> Optional[JobMetadata]:
            if any(
                s.stage_type == stage_type and s.description == description
                for s in job_metadata.tecton_managed_info.stages
            ):
                return None
            new_proto = JobMetadata()
            new_proto.CopyFrom(job_metadata)

            new_stage = TectonManagedStage(
                description=description,
                stage_type=stage_type,
                state=TectonManagedStage.State.PENDING,
            )
            new_proto.tecton_managed_info.stages.append(new_stage)
            return new_proto

        metadata = self._metadata_client.update(_update)
        for i, stage in enumerate(metadata.tecton_managed_info.stages):
            if stage.stage_type == stage_type and stage.description == description:
                return i
        msg = f"Stage {stage_type} does not exist"
        raise ValueError(msg)

    def set_query(self, stage_idx, sql: str):
        def _update(job_metadata: JobMetadata) -> JobMetadata:
            new_proto = JobMetadata()
            new_proto.CopyFrom(job_metadata)

            stage = new_proto.tecton_managed_info.stages[stage_idx]
            if not stage.compiled_sql_query:
                stage.compiled_sql_query = sql

            return new_proto

        self._metadata_client.update(_update)

    def update_progress(self, stage_idx: int, progress: float):
        job_progress = (float(self._query_index) / float(self._query_count)) + progress * (
            1.0 / float(self._query_count)
        )

        def _update(job_metadata: JobMetadata) -> JobMetadata:
            new_proto = JobMetadata()
            new_proto.CopyFrom(job_metadata)

            stage = new_proto.tecton_managed_info.stages[stage_idx]

            if stage.state == TectonManagedStage.PENDING:
                stage.state = TectonManagedStage.State.RUNNING
                stage.start_time.GetCurrentTime()

            stage.progress = job_progress
            stage.duration.FromSeconds(int((datetime.now() - stage.start_time.ToDatetime()).total_seconds()))

            return new_proto

        self._metadata_client.update(_update)

    def set_completed(self, stage_idx: int):
        if self._query_index < (self._query_count - 1):
            return

        def _update(job_metadata: JobMetadata) -> JobMetadata:
            new_proto = JobMetadata()
            new_proto.CopyFrom(job_metadata)

            stage = new_proto.tecton_managed_info.stages[stage_idx]
            stage.state = TectonManagedStage.State.SUCCESS

            return new_proto

        self._metadata_client.update(_update)

    def set_failed(self, stage_idx: int, user_error: bool):
        def _update(job_metadata: JobMetadata) -> JobMetadata:
            new_proto = JobMetadata()
            new_proto.CopyFrom(job_metadata)

            stage = new_proto.tecton_managed_info.stages[stage_idx]
            stage.error_type = (
                TectonManagedStage.ErrorType.USER_ERROR if user_error else TectonManagedStage.ErrorType.UNEXPECTED_ERROR
            )
            stage.error_detail = traceback.format_exc()
            stage.state = TectonManagedStage.State.ERROR

            return new_proto

        self._metadata_client.update(_update)

    def set_current_stage_failed(self, error_type: TectonManagedStage.ErrorType):
        def _update(job_metadata: JobMetadata) -> JobMetadata:
            new_proto = JobMetadata()
            new_proto.CopyFrom(job_metadata)

            if any(s.state == TectonManagedStage.State.ERROR for s in new_proto.tecton_managed_info.stages):
                return new_proto

            current_stage = None
            for stage in new_proto.tecton_managed_info.stages:
                # Select first RUNNING or PENDING stage
                # Or if all stages are complete - just the last one
                current_stage = stage
                if stage.state in (TectonManagedStage.State.RUNNING, TectonManagedStage.State.PENDING):
                    break

            if not current_stage:
                # if there are no stages - we will create a dummy one
                current_stage = TectonManagedStage(
                    description="Setting up materialization job",
                    state=TectonManagedStage.State.ERROR,
                    stage_type=TectonManagedStage.StageType.PYTHON,
                    error_type=error_type,
                    error_detail=traceback.format_exc(),
                )
                new_proto.tecton_managed_info.stages.append(current_stage)
            else:
                current_stage.error_type = error_type
                current_stage.error_detail = traceback.format_exc()
                current_stage.state = TectonManagedStage.State.ERROR

            return new_proto

        self._metadata_client.update(_update)

    def create_stage_monitor(
        self,
        stage_type: TectonManagedStage.StageType,
        description: str,
    ) -> MonitoringContextProvider:
        stage_idx = self.create_stage(stage_type, description)

        @contextlib.contextmanager
        def monitor(sql: Optional[str] = None):
            if sql:
                self.set_query(stage_idx, sql)

            self.update_progress(stage_idx, 0)

            try:
                yield lambda p: self.update_progress(stage_idx, p)
            except Exception:
                self.set_failed(stage_idx, user_error=False)
                raise
            else:
                self.update_progress(stage_idx, 1)
                self.set_completed(stage_idx)

        return monitor
