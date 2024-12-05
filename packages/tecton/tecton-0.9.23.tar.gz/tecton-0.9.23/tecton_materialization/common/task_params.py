import datetime
import functools
import itertools
import typing
from typing import List

import pendulum

from tecton_core import specs
from tecton_core.fco_container import DataProto
from tecton_core.fco_container import create_fco_container
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_proto.materialization.params_pb2 import MaterializationTaskParams


@functools.lru_cache(maxsize=0)
def feature_definition_from_task_params(params: MaterializationTaskParams) -> FeatureDefinitionWrapper:
    fco_container = create_fco_container(
        itertools.chain(
            *(
                # The cast helps out various type inference implementations which otherwise would complain that
                # the different FCO lists are not hte same type
                typing.cast(typing.Iterable[DataProto], p)
                for p in (params.virtual_data_sources, params.transformations, params.entities)
            )
        ),
        deserialize_funcs_to_main=True,
    )
    fv_spec = specs.create_feature_view_spec_from_data_proto(params.feature_view)
    return FeatureDefinitionWrapper(fv_spec, fco_container)


class TimeInterval(typing.NamedTuple):
    start: datetime.datetime
    end: datetime.datetime

    def to_pendulum(self) -> pendulum.Period:
        return pendulum.instance(self.end) - pendulum.instance(self.start)


def _backfill_job_periods(
    start_time: datetime.datetime, end_time: datetime.datetime, interval: datetime.timedelta
) -> List[TimeInterval]:
    jobs = []
    while start_time < end_time:
        jobs.append(TimeInterval(start_time, start_time + interval))
        start_time = start_time + interval
    assert start_time == end_time, "Start and end times were not aligned to `interval`"
    return jobs


def job_query_intervals(task_params: MaterializationTaskParams) -> typing.List[TimeInterval]:
    """
    Return a list of start/end tuples of size batch_schedule.
    For use of breaking up a large backfill window into incremental sizes.
    """
    fd = feature_definition_from_task_params(task_params)
    assert task_params.batch_task_info.HasField("batch_parameters")
    task_feature_start_time = task_params.batch_task_info.batch_parameters.feature_start_time.ToDatetime()
    task_feature_end_time = task_params.batch_task_info.batch_parameters.feature_end_time.ToDatetime()
    # for incremental backfills, we split the job into each batch interval
    if fd.is_incremental_backfill:
        return _backfill_job_periods(task_feature_start_time, task_feature_end_time, fd.batch_materialization_schedule)
    else:
        return [TimeInterval(task_feature_start_time, task_feature_end_time)]
