import logging
from typing import Optional

import pendulum
from pyspark.sql import DataFrame
from pyspark.sql import functions


logger = logging.getLogger(__name__)


def get_time_limits_of_dataframe(df: DataFrame, time_key: str) -> Optional[pendulum.Period]:
    """The returned range is inclusive at the beginning & exclusive at the end: [start, end)."""
    # Fetch lower and upper time bound of the spine so that we can demand the individual feature definitions
    # to limit the amount of data they fetch from the raw data sources.
    # Returns None if df is empty.
    collected_df = df.select(
        functions.min(df[time_key]).alias("time_start"), functions.max(df[time_key]).alias("time_end")
    ).collect()
    time_start = collected_df[0]["time_start"]
    time_end = collected_df[0]["time_end"]
    if time_start is None or time_end is None:
        return None

    # Need to add 1 microsecond to the end time, since the range is exclusive at the end, and we need
    # to make sure to include the very last feature value (in terms of the event timestamp).
    return pendulum.instance(time_end).add(microseconds=1) - pendulum.instance(time_start)
