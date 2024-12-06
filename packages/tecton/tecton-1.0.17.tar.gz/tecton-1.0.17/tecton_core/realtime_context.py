from datetime import datetime
from typing import Optional

import pandas


REQUEST_TIMESTAMP_FIELD_NAME = "request_timestamp"


class RealtimeContext:
    """
    RealtimeContext is a class that is used to pass context metadata such as the request_timestamp
    to the `context` parameter of a Realtime Feature Views.
    """

    _is_python_mode: Optional[bool] = None
    _request_timestamp: Optional[datetime] = None
    _row_level_data: Optional[pandas.DataFrame] = None

    def __init__(
        self,
        request_timestamp: Optional[datetime] = None,
        row_level_data: Optional[pandas.DataFrame] = None,
        _is_python_mode: Optional[bool] = None,
    ) -> None:
        """
        Initialize the RealtimeContext object.

        :param _is_python_mode: Whether the Realtime Feature View is in Python mode.
        :param request_timestamp: The timestamp of the request made to the Tecton Feature Server. Used for Python mode offline and for both modes online.
        :param row_level_data: The row-level context data for the Realtime Feature View for each row in the events data frame. Only populated in Pandas mode during Offline Retrieval.
        """
        self._is_python_mode = _is_python_mode
        self._request_timestamp = request_timestamp
        self._row_level_data = row_level_data

    def set_mode(self, is_python: bool) -> None:
        """
        Set the mode of the Realtime Feature View.

        :param is_python: Whether the Realtime Feature View is in Python mode.
        """
        self._is_python_mode = is_python

    @property
    def request_timestamp(self) -> Optional[datetime]:
        """
        The request_timestamp is the timestamp of the request made to the Tecton Feature Server.
        """
        if not self._is_python_mode:
            str = "The field `request_timestamp` is only available in Realtime Feature Views with Python mode. Please use `context.request_timestamp_series` when using Pandas mode."
            raise ValueError(str)

        return self._request_timestamp

    @property
    def request_timestamp_series(self) -> Optional[pandas.Series]:
        """
        The request_timestamp_series is a pandas Series with the request_timestamp as the only element. Each element in the
        Series is the request_timestamp for the corresponding row in the input data.
        """
        if self._is_python_mode:
            str = "The field `request_timestamp_series` is only available in Realtime Feature Views with Pandas mode. Please use `context.request_timestamp` when using Python mode."
            raise ValueError(str)

        # For online retrieval, we build a Series with the request_timestamp as the only element
        if self._request_timestamp is not None:
            return pandas.Series([self._request_timestamp], name=REQUEST_TIMESTAMP_FIELD_NAME)

        if self._row_level_data is None:
            return None

        return self._row_level_data[REQUEST_TIMESTAMP_FIELD_NAME]
