from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

AGGREGATION_FUNCTION_APPROX_COUNT_DISTINCT: AggregationFunction
AGGREGATION_FUNCTION_APPROX_PERCENTILE: AggregationFunction
AGGREGATION_FUNCTION_COUNT: AggregationFunction
AGGREGATION_FUNCTION_FIRST_DISTINCT_N: AggregationFunction
AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N: AggregationFunction
AGGREGATION_FUNCTION_LAST: AggregationFunction
AGGREGATION_FUNCTION_LAST_DISTINCT_N: AggregationFunction
AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N: AggregationFunction
AGGREGATION_FUNCTION_MAX: AggregationFunction
AGGREGATION_FUNCTION_MEAN: AggregationFunction
AGGREGATION_FUNCTION_MIN: AggregationFunction
AGGREGATION_FUNCTION_STDDEV_POP: AggregationFunction
AGGREGATION_FUNCTION_STDDEV_SAMP: AggregationFunction
AGGREGATION_FUNCTION_SUM: AggregationFunction
AGGREGATION_FUNCTION_UNKNOWN: AggregationFunction
AGGREGATION_FUNCTION_VAR_POP: AggregationFunction
AGGREGATION_FUNCTION_VAR_SAMP: AggregationFunction
DESCRIPTOR: _descriptor.FileDescriptor

class AggregationFunctionParams(_message.Message):
    __slots__ = ["approx_count_distinct", "approx_percentile", "first_n", "last_n"]
    APPROX_COUNT_DISTINCT_FIELD_NUMBER: ClassVar[int]
    APPROX_PERCENTILE_FIELD_NUMBER: ClassVar[int]
    FIRST_N_FIELD_NUMBER: ClassVar[int]
    LAST_N_FIELD_NUMBER: ClassVar[int]
    approx_count_distinct: ApproxCountDistinctParams
    approx_percentile: ApproxPercentileParams
    first_n: FirstNParams
    last_n: LastNParams
    def __init__(self, last_n: Optional[Union[LastNParams, Mapping]] = ..., first_n: Optional[Union[FirstNParams, Mapping]] = ..., approx_count_distinct: Optional[Union[ApproxCountDistinctParams, Mapping]] = ..., approx_percentile: Optional[Union[ApproxPercentileParams, Mapping]] = ...) -> None: ...

class ApproxCountDistinctParams(_message.Message):
    __slots__ = ["precision"]
    PRECISION_FIELD_NUMBER: ClassVar[int]
    precision: int
    def __init__(self, precision: Optional[int] = ...) -> None: ...

class ApproxPercentileParams(_message.Message):
    __slots__ = ["percentile", "precision"]
    PERCENTILE_FIELD_NUMBER: ClassVar[int]
    PRECISION_FIELD_NUMBER: ClassVar[int]
    percentile: float
    precision: int
    def __init__(self, percentile: Optional[float] = ..., precision: Optional[int] = ...) -> None: ...

class FirstNParams(_message.Message):
    __slots__ = ["n"]
    N_FIELD_NUMBER: ClassVar[int]
    n: int
    def __init__(self, n: Optional[int] = ...) -> None: ...

class LastNParams(_message.Message):
    __slots__ = ["n"]
    N_FIELD_NUMBER: ClassVar[int]
    n: int
    def __init__(self, n: Optional[int] = ...) -> None: ...

class AggregationFunction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
