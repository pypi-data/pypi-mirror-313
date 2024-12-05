from typing import Optional

from tecton_core.compute_mode import ComputeMode
from tecton_core.compute_mode import offline_retrieval_compute_mode
from tecton_core.specs import TimeWindowSpec


TECTON_TEMP_AGGREGATION_SECONDARY_KEY_COL: str = "_tecton_temp_agg_secondary_key_col"
TECTON_TEMP_STRUCT_PREFIX: str = "_tecton_internal_temp_struct"


def default_case(field_name: str, compute_mode: Optional[ComputeMode] = None) -> str:
    # Snowflake defaults to uppercase
    if (compute_mode or offline_retrieval_compute_mode(None)) == ComputeMode.SNOWFLAKE:
        return field_name.upper()
    else:
        return field_name


def anchor_time(compute_mode: Optional[ComputeMode] = None) -> str:
    return default_case("_anchor_time", compute_mode=compute_mode)


def effective_timestamp(compute_mode: Optional[ComputeMode] = None) -> str:
    return default_case("_effective_timestamp", compute_mode=compute_mode)


def expiration_timestamp(compute_mode: Optional[ComputeMode] = None) -> str:
    return default_case("_expiration_timestamp", compute_mode=compute_mode)


def timestamp_plus_ttl(compute_mode: Optional[ComputeMode] = None) -> str:
    return default_case("_timestamp_plus_ttl", compute_mode=compute_mode)


def tecton_secondary_key_aggregation_indicator_col(compute_mode: Optional[ComputeMode] = None) -> str:
    return default_case("_tecton_secondary_key_aggregation_indicator", compute_mode=compute_mode)


def temp_indictor_column_name(window: TimeWindowSpec) -> str:
    return f"{tecton_secondary_key_aggregation_indicator_col()}_{window.to_string()}"


def temp_struct_column_name(window: TimeWindowSpec) -> str:
    return f"{TECTON_TEMP_STRUCT_PREFIX}_{window.to_string()}"


def tecton_unique_id_col(compute_mode: Optional[ComputeMode] = None) -> str:
    return default_case("_tecton_unique_id", compute_mode=compute_mode)


def udf_internal(compute_mode: Optional[ComputeMode] = None) -> str:
    """Namespace used in `FeatureDefinitionAndJoinConfig` for dependent feature view
    columns. Dependent FVs to ODFVs have this prefix in the name and are
    filtered out before being returned to the user.
    """
    return default_case("_udf_internal", compute_mode=compute_mode)


def odfv_internal_staging_table(compute_mode: Optional[ComputeMode] = None) -> str:
    return default_case("_odfv_internal_table", compute_mode=compute_mode)


def aggregation_group_id(compute_mode: Optional[ComputeMode] = None) -> str:
    return default_case("_tecton_aggregation_window_id", compute_mode=compute_mode)


def inclusive_start_time(compute_mode: Optional[ComputeMode] = None) -> str:
    return default_case("_tecton_inclusive_start_time", compute_mode=compute_mode)


def exclusive_end_time(compute_mode: Optional[ComputeMode] = None) -> str:
    return default_case("_tecton_exclusive_end_time", compute_mode=compute_mode)


def window_end_column_name(compute_mode: Optional[ComputeMode] = None) -> str:
    return default_case("tile_end_time", compute_mode=compute_mode)


def valid_from() -> str:
    return default_case("_valid_from")


def valid_to() -> str:
    return default_case("_valid_to")


def interval_start_time() -> str:
    return default_case("_interval_start_time")


def interval_end_time() -> str:
    return default_case("_interval_end_time")
