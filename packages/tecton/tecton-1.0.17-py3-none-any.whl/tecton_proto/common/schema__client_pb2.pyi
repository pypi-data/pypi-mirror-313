from google.protobuf import duration_pb2 as _duration_pb2
from tecton_proto.common import column_type__client_pb2 as _column_type__client_pb2
from tecton_proto.common import data_type__client_pb2 as _data_type__client_pb2
from tecton_proto.common import time_window__client_pb2 as _time_window__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Column(_message.Message):
    __slots__ = ["feature_server_data_type", "feature_server_type", "name", "offline_data_type", "raw_snowflake_type", "raw_spark_type"]
    FEATURE_SERVER_DATA_TYPE_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVER_TYPE_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    OFFLINE_DATA_TYPE_FIELD_NUMBER: ClassVar[int]
    RAW_SNOWFLAKE_TYPE_FIELD_NUMBER: ClassVar[int]
    RAW_SPARK_TYPE_FIELD_NUMBER: ClassVar[int]
    feature_server_data_type: _data_type__client_pb2.DataType
    feature_server_type: _column_type__client_pb2.ColumnType
    name: str
    offline_data_type: _data_type__client_pb2.DataType
    raw_snowflake_type: str
    raw_spark_type: str
    def __init__(self, name: Optional[str] = ..., offline_data_type: Optional[Union[_data_type__client_pb2.DataType, Mapping]] = ..., feature_server_data_type: Optional[Union[_data_type__client_pb2.DataType, Mapping]] = ..., raw_spark_type: Optional[str] = ..., raw_snowflake_type: Optional[str] = ..., feature_server_type: Optional[Union[_column_type__client_pb2.ColumnType, str]] = ...) -> None: ...

class Field(_message.Message):
    __slots__ = ["dtype", "name"]
    DTYPE_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    dtype: _data_type__client_pb2.DataType
    name: str
    def __init__(self, name: Optional[str] = ..., dtype: Optional[Union[_data_type__client_pb2.DataType, Mapping]] = ...) -> None: ...

class OnlineBatchTableFormat(_message.Message):
    __slots__ = ["online_batch_table_parts"]
    ONLINE_BATCH_TABLE_PARTS_FIELD_NUMBER: ClassVar[int]
    online_batch_table_parts: _containers.RepeatedCompositeFieldContainer[OnlineBatchTablePart]
    def __init__(self, online_batch_table_parts: Optional[Iterable[Union[OnlineBatchTablePart, Mapping]]] = ...) -> None: ...

class OnlineBatchTablePart(_message.Message):
    __slots__ = ["schema", "tiles", "time_window", "window_index"]
    SCHEMA_FIELD_NUMBER: ClassVar[int]
    TILES_FIELD_NUMBER: ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: ClassVar[int]
    WINDOW_INDEX_FIELD_NUMBER: ClassVar[int]
    schema: Schema
    tiles: _containers.RepeatedCompositeFieldContainer[OnlineBatchTablePartTile]
    time_window: _time_window__client_pb2.TimeWindow
    window_index: int
    def __init__(self, window_index: Optional[int] = ..., time_window: Optional[Union[_time_window__client_pb2.TimeWindow, Mapping]] = ..., schema: Optional[Union[Schema, Mapping]] = ..., tiles: Optional[Iterable[Union[OnlineBatchTablePartTile, Mapping]]] = ...) -> None: ...

class OnlineBatchTablePartTile(_message.Message):
    __slots__ = ["relative_end_time_exclusive", "relative_start_time_inclusive"]
    RELATIVE_END_TIME_EXCLUSIVE_FIELD_NUMBER: ClassVar[int]
    RELATIVE_START_TIME_INCLUSIVE_FIELD_NUMBER: ClassVar[int]
    relative_end_time_exclusive: _duration_pb2.Duration
    relative_start_time_inclusive: _duration_pb2.Duration
    def __init__(self, relative_start_time_inclusive: Optional[Union[_duration_pb2.Duration, Mapping]] = ..., relative_end_time_exclusive: Optional[Union[_duration_pb2.Duration, Mapping]] = ...) -> None: ...

class Schema(_message.Message):
    __slots__ = ["columns"]
    COLUMNS_FIELD_NUMBER: ClassVar[int]
    columns: _containers.RepeatedCompositeFieldContainer[Column]
    def __init__(self, columns: Optional[Iterable[Union[Column, Mapping]]] = ...) -> None: ...
