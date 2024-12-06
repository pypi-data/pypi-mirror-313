import typing
from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from typing import Optional
from typing import Union

from typeguard import typechecked

import tecton_core.tecton_pendulum as pendulum
from tecton_core.errors import TectonValidationError


if typing.TYPE_CHECKING:
    import pyspark


@dataclass
class MaterializationContext:
    _feature_start_time_DONT_ACCESS_DIRECTLY: datetime
    _feature_end_time_DONT_ACCESS_DIRECTLY: datetime
    _batch_schedule_DONT_ACCESS_DIRECTLY: timedelta

    @property
    def start_time(self) -> datetime:
        return self._feature_start_time_DONT_ACCESS_DIRECTLY

    @property
    def end_time(self) -> datetime:
        return self._feature_end_time_DONT_ACCESS_DIRECTLY

    @property
    def batch_schedule(self) -> timedelta:
        return self._batch_schedule_DONT_ACCESS_DIRECTLY

    @typechecked
    def time_filter_sql(self, timestamp_expr: str) -> str:
        # Use atom string to include the timezone.
        return f"('{self.start_time.isoformat()}' <= ({timestamp_expr}) AND ({timestamp_expr}) < '{self.end_time.isoformat()}')"

    def time_filter_pyspark(self, timestamp_expr: Union[str, "pyspark.sql.Column"]) -> "pyspark.sql.Column":  # type: ignore
        from pyspark.sql.functions import expr
        from pyspark.sql.functions import lit

        if isinstance(timestamp_expr, str):
            timestamp_expr = expr(timestamp_expr)

        # Use atom string to include the timezone.
        return (lit(self.start_time.isoformat()) <= timestamp_expr) & (timestamp_expr < lit(self.end_time.isoformat()))

    def feature_time_filter_pyspark(self, timestamp_expr: Union[str, "pyspark.sql.Column"]) -> "pyspark.sql.Column":  # type: ignore
        return self.time_filter_pyspark(timestamp_expr)

    # Everything below is deprecated but kept for backwards compatibility since Snowflake Materialization Runtime
    # is not versioned.
    @property
    def feature_start_time(self) -> datetime:
        return self._feature_start_time_DONT_ACCESS_DIRECTLY

    @property
    def feature_end_time(self) -> datetime:
        return self._feature_end_time_DONT_ACCESS_DIRECTLY

    @property
    def feature_start_time_string(self) -> str:
        return self.feature_start_time.isoformat()

    @property
    def feature_end_time_string(self) -> str:
        return self.feature_end_time.isoformat()

    @typechecked
    def feature_time_filter_sql(self, timestamp_expr: str) -> str:
        return self.time_filter_sql(timestamp_expr)


@dataclass
class UnboundMaterializationContext(MaterializationContext):
    """
    This is only meant for instantiation in transformation default args. Using it directly will fail.
    """

    @property
    def batch_schedule(self):
        msg = "tecton.materialization_context() must be passed in via a kwarg default only. Instantiation in function body is not allowed."
        raise TectonValidationError(msg)

    @property
    def start_time(self):
        msg = "tecton.materialization_context() must be passed in via a kwarg default only. Instantiation in function body is not allowed."
        raise TectonValidationError(msg)

    @property
    def end_time(self):
        msg = "tecton.materialization_context() must be passed in via a kwarg default only. Instantiation in function body is not allowed."
        raise TectonValidationError(msg)

    @property
    def feature_start_time(self):
        msg = "tecton.materialization_context() must be passed in via a kwarg default only. Instantiation in function body is not allowed."
        raise TectonValidationError(msg)

    @property
    def feature_end_time(self):
        msg = "tecton.materialization_context() must be passed in via a kwarg default only. Instantiation in function body is not allowed."
        raise TectonValidationError(msg)


@dataclass
class BoundMaterializationContext(MaterializationContext):
    @classmethod
    def create(cls, feature_start_time, feature_end_time):
        start_dt = datetime.fromtimestamp(feature_start_time.timestamp(), pendulum.tz.UTC)
        end_dt = datetime.fromtimestamp(feature_end_time.timestamp(), pendulum.tz.UTC)

        # user facing version
        return BoundMaterializationContext(
            _feature_start_time_DONT_ACCESS_DIRECTLY=start_dt,
            _feature_end_time_DONT_ACCESS_DIRECTLY=end_dt,
            # batch_schedule is passed by pipeline helper
            _batch_schedule_DONT_ACCESS_DIRECTLY=timedelta(seconds=0),
        )

    @classmethod
    def _create_internal(
        cls,
        feature_start_time: Optional[pendulum.DateTime],
        feature_end_time: Optional[pendulum.DateTime],
        batch_schedule: Optional[pendulum.Duration],
    ) -> "BoundMaterializationContext":
        start_dt = datetime.fromtimestamp(feature_start_time.timestamp(), pendulum.tz.UTC)
        end_dt = datetime.fromtimestamp(feature_end_time.timestamp(), pendulum.tz.UTC)

        # should only be used in pipeline_helper
        return BoundMaterializationContext(
            _feature_start_time_DONT_ACCESS_DIRECTLY=start_dt,
            _feature_end_time_DONT_ACCESS_DIRECTLY=end_dt,
            _batch_schedule_DONT_ACCESS_DIRECTLY=batch_schedule.as_timedelta(),
        )

    @classmethod
    def _create_from_period(
        cls, feature_time_limits: Optional[pendulum.Period], batch_schedule: pendulum.Duration
    ) -> "BoundMaterializationContext":
        feature_start_time = (
            feature_time_limits.start
            if feature_time_limits is not None
            else pendulum.from_timestamp(0, pendulum.tz.UTC)
        )
        feature_end_time = feature_time_limits.end if feature_time_limits is not None else pendulum.datetime(2100, 1, 1)

        start_dt = datetime.fromtimestamp(feature_start_time.timestamp(), pendulum.tz.UTC)
        end_dt = datetime.fromtimestamp(feature_end_time.timestamp(), pendulum.tz.UTC)

        return BoundMaterializationContext(
            _feature_start_time_DONT_ACCESS_DIRECTLY=start_dt,
            _feature_end_time_DONT_ACCESS_DIRECTLY=end_dt,
            _batch_schedule_DONT_ACCESS_DIRECTLY=batch_schedule.as_timedelta(),
        )


def materialization_context():
    """
    Used as a default value for a Feature View or Transformation with a materialization context parameter.

    ``context.start_time`` and ``context.end_time`` return a `datetime.datetime` object equal to the beginning and end of the period being materialized respectively. For example for a batch feature view materializing data from May 1st, 2022, ``context.start_time = datetime(2022, 5, 1)`` and ``context.end_time = datetime(2022, 5, 2)``.

    The datetimes can be used in SQL query strings directly (the datetime object will be cast to an atom-formatted timestamp string and inlined as a constant in the SQL query).

    Example usage:

    .. code-block:: python

        from tecton import batch_feature_view, materialization_context
        from datetime import datetime, timedelta

        @batch_feature_view(
            sources=[transactions],
            entities=[user],
            mode='spark_sql',
            features=[Attribute("AMOUNT", Float64)],
            batch_schedule=timedelta(days=1),
            feature_start_time=datetime(2020, 10, 10),
        )
        def user_last_transaction_amount(transactions, context=materialization_context()):
            return f'''
                SELECT
                    USER_ID,
                    AMOUNT,
                    TIMESTAMP
                FROM
                    {transactions}
                WHERE TIMESTAMP >= TO_TIMESTAMP("{context.start_time}") -- e.g. TO_TIMESTAMP("2022-05-01T00:00:00+00:00")
                    AND TIMESTAMP < TO_TIMESTAMP("{context.end_time}") -- e.g. TO_TIMESTAMP("2022-05-02T00:00:00+00:00")
                '''
    """
    dummy_time = pendulum.datetime(1970, 1, 1)
    dummy_period = timedelta()
    return UnboundMaterializationContext(
        _feature_start_time_DONT_ACCESS_DIRECTLY=dummy_time,
        _feature_end_time_DONT_ACCESS_DIRECTLY=dummy_time,
        _batch_schedule_DONT_ACCESS_DIRECTLY=dummy_period,
    )
