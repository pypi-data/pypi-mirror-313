import datetime
from collections import defaultdict
from typing import Optional
from typing import Tuple

import attrs
import pendulum

from tecton_core import feature_definition_wrapper
from tecton_core import schema
from tecton_core import time_utils
from tecton_core.specs import LifetimeWindowSpec
from tecton_core.specs import TimeWindowSpec
from tecton_core.specs import create_time_window_spec_from_data_proto
from tecton_proto.data import feature_view_pb2 as feature_view__data_pb2


@attrs.frozen
class AggregationGroup:
    """AggregationGroup represents a group of aggregate features to compute with a corresponding start/end.

    The typical usage of this will be in compaction jobs, where we will use the start/end time to determine
    eligible rows for each individual aggregate.
    """

    window_index: int
    inclusive_start_time: Optional[datetime.datetime]
    exclusive_end_time: datetime.datetime
    aggregate_features: Tuple[feature_view__data_pb2.AggregateFeature, ...]
    schema: schema.Schema


def _get_inclusive_start_time_for_window(
    exclusive_end_time: datetime.datetime, window: TimeWindowSpec
) -> Optional[datetime.datetime]:
    if isinstance(window, LifetimeWindowSpec):
        return None
    return time_utils.get_timezone_aware_datetime(exclusive_end_time + window.window_start)


def _get_exclusive_end_time_for_window(
    exclusive_end_time: datetime.datetime, window: TimeWindowSpec
) -> datetime.datetime:
    if isinstance(window, LifetimeWindowSpec):
        return time_utils.get_timezone_aware_datetime(exclusive_end_time)
    return time_utils.get_timezone_aware_datetime(exclusive_end_time + window.window_end)


def aggregation_groups(
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper, exclusive_end_time: datetime.datetime
) -> Tuple[AggregationGroup, ...]:
    aggregation_map = defaultdict(list)
    for aggregation in fdw.trailing_time_window_aggregation.features:
        aggregation_map[create_time_window_spec_from_data_proto(aggregation.time_window)].append(aggregation)

    agg_groups = fdw.fv_spec.online_batch_table_format.online_batch_table_parts

    if len(agg_groups) != len(aggregation_map):
        msg = "unexpected difference in length of the spec's online_batch_table_format and trailing_time_window_aggregation"
        raise ValueError(msg)

    return tuple(
        AggregationGroup(
            window_index=group.window_index,
            inclusive_start_time=_get_inclusive_start_time_for_window(exclusive_end_time, group.time_window),
            exclusive_end_time=_get_exclusive_end_time_for_window(exclusive_end_time, group.time_window),
            aggregate_features=tuple(aggregation_map[group.time_window]),
            schema=group.schema,
        )
        for group in agg_groups
    )


def _get_min_window_start_time(
    aggregation_groups: Tuple[AggregationGroup, ...], fdw: feature_definition_wrapper.FeatureDefinitionWrapper
) -> Optional[pendulum.DateTime]:
    contains_lifetime_agg = any(group.inclusive_start_time is None for group in aggregation_groups)
    if contains_lifetime_agg:
        return fdw.materialization_start_timestamp
    min_window_time = min(group.inclusive_start_time for group in aggregation_groups)
    return pendulum.instance(min_window_time)


def _get_max_window_end_time(aggregation_groups: Tuple[AggregationGroup, ...]) -> pendulum.DateTime:
    max_window_time = max(group.exclusive_end_time for group in aggregation_groups)
    return pendulum.instance(max_window_time)


def get_data_time_limits_for_compaction(
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper, compaction_job_end_time: datetime.datetime
) -> Optional[pendulum.Period]:
    """Compute the time filter to be used for online compaction jobs.

    This determines how much data to read from the offline store.
    For aggregate fvs,
        start_time=earliest agg window start
        end_time=latest agg window end
    For non agg fvs,
        start_time=max(feature start time, compaction_job_end_time - ttl)
        end_time=compaction_job_end_time"""
    if fdw.materialization_start_timestamp is None:
        return None

    if fdw.is_temporal_aggregate:
        agg_groups = aggregation_groups(fdw=fdw, exclusive_end_time=compaction_job_end_time)
        start_time = _get_min_window_start_time(agg_groups, fdw)
        end_time = _get_max_window_end_time(agg_groups)
        return pendulum.Period(start_time, end_time)

    if not fdw.is_temporal:
        msg = "Expected fv to be of type temporal or temporal aggregate."
        raise Exception(msg)

    # respect ttl and feature start time for temporal fvs
    end_time = pendulum.instance(compaction_job_end_time)
    if fdw.serving_ttl:
        if not fdw.feature_start_timestamp:
            msg = "Expected feature start time to be set for temporal fvs when ttl is set."
            raise Exception(msg)
        job_time_minus_ttl = end_time - fdw.serving_ttl
        start_time = max(fdw.feature_start_timestamp, job_time_minus_ttl)
    elif fdw.feature_start_timestamp:
        start_time = fdw.feature_start_timestamp
    else:
        msg = "Expected ttl or feature start time to be set for temporal fvs."
        raise Exception(msg)
    return pendulum.Period(start_time, end_time)
