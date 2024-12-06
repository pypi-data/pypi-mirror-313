import datetime
from dataclasses import dataclass
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

from tecton import tecton_context
from tecton.aggregation_functions import AggregationFunction
from tecton.cli.error_utils import format_validation_location_fancy
from tecton.cli.printer import safe_print
from tecton.framework import base_tecton_object
from tecton.framework.base_tecton_object import BaseTectonObject
from tecton.framework.configs import LifetimeWindow
from tecton.framework.configs import TimeWindow
from tecton.framework.configs import TimeWindowSeries
from tecton.framework.configs import build_aggregation_default_name
from tecton.framework.feature_view import AggregationLeadingEdge
from tecton.framework.feature_view import FeatureView
from tecton.framework.feature_view import MaterializedFeatureView
from tecton.framework.workspace import get_workspace
from tecton.types import Array
from tecton.types import Field
from tecton.types import Map
from tecton.types import SdkDataType
from tecton.types import Struct
from tecton.v09_compat.framework import BatchFeatureView
from tecton.v09_compat.framework import DataSource
from tecton.v09_compat.framework import Entity
from tecton.v09_compat.framework import FeatureTable
from tecton.v09_compat.framework import OnDemandFeatureView
from tecton.v09_compat.framework import PushSource
from tecton.v09_compat.framework import StreamFeatureView
from tecton_core.data_types import ArrayType
from tecton_core.data_types import DataType
from tecton_core.data_types import MapType
from tecton_core.data_types import StructField
from tecton_core.data_types import StructType
from tecton_core.specs.utils import get_field_or_none
from tecton_core.time_utils import proto_to_duration
from tecton_proto.args.pipeline__client_pb2 import PipelineNode
from tecton_proto.common.aggregation_function__client_pb2 import AggregationFunctionParams


def _get_imports_for_type(type: Union[SdkDataType, Field, DataType]) -> Set[str]:
    if isinstance(type, (Array, ArrayType)):
        element_types = _get_imports_for_type(type.element_type)
        element_types.add("Array")
        return element_types
    elif isinstance(type, (Struct, StructType)):
        types = set()
        for field in type.fields:
            element_types = _get_imports_for_type(field)
            for type in element_types:
                types.add(type)
        types.add("Struct")
        return types
    elif isinstance(type, (Map, MapType)):
        key_types = _get_imports_for_type(type.key_type)
        value_types = _get_imports_for_type(type.value_type)
        return key_types | value_types | {"Map"}
    elif isinstance(type, Field):
        types = _get_imports_for_type(type.dtype)
        types.add("Field")
        return types
    elif isinstance(type, StructField):
        types = _get_imports_for_type(type.data_type)
        types.add("Field")
        return types
    else:
        return {type.__repr__()}


def timedelta_to_string(td):
    if td < datetime.timedelta(0):
        return f"-{timedelta_to_string(-td)}"

    components = []
    days = td.days
    seconds = td.seconds
    microseconds = td.microseconds

    if days:
        components.append(f"days={days}")
    if seconds:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            components.append(f"hours={hours}")
        if minutes:
            components.append(f"minutes={minutes}")
        if seconds:
            components.append(f"seconds={seconds}")
    if microseconds:
        components.append(f"microseconds={microseconds}")

    if not components:
        return "timedelta()"

    return f"timedelta({', '.join(components)})"


def _aggregation_function_to_string_render(
    aggregation_function: AggregationFunction, params: Optional[AggregationFunctionParams]
) -> str:
    if aggregation_function.base_name == "lastn":
        return f"last_distinct({params.last_n.n})"
    elif aggregation_function.base_name == "last_non_distinct_n":
        return f"last({params.last_n.n})"
    elif aggregation_function.base_name == "first_distinct_n":
        return f"first_distinct({params.first_n.n})"
    elif aggregation_function.base_name == "first_non_distinct_n":
        return f"first({params.first_n.n})"
    elif aggregation_function.base_name == "approx_count_distinct":
        return f"approx_count_distinct({params.approx_count_distinct.precision})"
    elif aggregation_function.base_name == "approx_percentile":
        return f"approx_percentile{params.approx_percentile.percentile, params.approx_percentile.precision}"
    else:
        # All other functions without explicit AggregationFunction class-overrides (ex: "mean") are passed as strings; thus the double quotes
        return f'"{aggregation_function.base_name}"'


def _get_feature_view(feature_view_name: str) -> FeatureView:
    ws = get_workspace(tecton_context.get_current_workspace())
    return ws.get_feature_view(feature_view_name)


def _get_feature_table(feature_table_name: str) -> FeatureTable:
    ws = get_workspace(tecton_context.get_current_workspace())
    return ws.get_feature_table(feature_table_name)


def _get_complete_status_emoji(is_complete: bool) -> str:
    return "✅" if is_complete else "🚫"


@dataclass
class ImportGuidance:
    tecton_import: str
    tecton_type_import: str

    def to_pretty_string(self):
        import_msg = "💡If needed, add imports:\n"
        if self.tecton_import and not self.tecton_type_import:
            return f"{import_msg}{self.tecton_import}\n"
        elif self.tecton_type_import and not self.tecton_import:
            return f"{import_msg}{self.tecton_type_import}\n"
        elif self.tecton_type_import and self.tecton_import:
            return f"{import_msg}{self.tecton_import}\n{self.tecton_type_import}\n"
        else:
            return ""


class BaseGuidance:
    _object: BaseTectonObject
    _obj_type: str
    _repo_root: str

    _tecton_imports: Set[str]
    _tecton_type_imports: Set[DataType]

    def __init__(self, _object: BaseTectonObject, _repo_root: str):
        self._object = _object
        self._repo_root = _repo_root
        self._tecton_imports = set()
        self._tecton_type_imports = set()

    def _get_upgrade_guidance(self) -> List[str]:
        raise NotImplementedError

    def _build_import_guidance(
        self,
    ) -> ImportGuidance:
        tecton_import_str = ""
        if bool(self._tecton_imports):
            tecton_import_str = f'from tecton import {", ".join(self._tecton_imports)}'

        tecton_type_import_str = ""
        if bool(self._tecton_type_imports):
            tecton_type_import_str_list = ", ".join(
                [str(tecton_type_import) for tecton_type_import in self._tecton_type_imports]
            )
            tecton_type_import_str = f"from tecton.types import {tecton_type_import_str_list}"

        return ImportGuidance(tecton_import=tecton_import_str, tecton_type_import=tecton_type_import_str)

    def _append_final_guidance(self, current_guidance: List[str]):
        if current_guidance:
            current_guidance.append("Update import from `tecton.v09_compat` to `tecton`.")
        else:
            current_guidance.append("No code change needed - just update import from `tecton.v09_compat` to `tecton`.")

    def print_guidance(self) -> None:
        format_validation_location_fancy(self._object, self._repo_root)
        safe_print("\n".join(self._get_upgrade_guidance()))
        safe_print("\n")


class DataSourceGuidance(BaseGuidance):
    _object: DataSource
    _obj_type = "DataSource"

    def _get_upgrade_guidance(self) -> List[str]:
        guidance = []
        if isinstance(self._object, PushSource):
            guidance.append(
                f"{_get_complete_status_emoji(False)} PushSource was deprecated in 0.9. Replace `PushSource` with `StreamSource` and set `stream_config=PushConfig()`. \nSee https://docs.tecton.ai/docs/release-notes/upgrade-process/to-09-upgrade-guide#step-by-step-upgrade-flow (Replace PushSource objects with a StreamSource that uses a PushConfig) for an example."
            )
        self._append_final_guidance(guidance)
        return guidance


class EntityGuidance(BaseGuidance):
    _object: Entity
    _obj_type = "Entity"

    def _find_feature_view_with_entity(self):
        for local_object in base_tecton_object._LOCAL_TECTON_OBJECTS:
            if issubclass(local_object.__class__, MaterializedFeatureView):
                fv_entities: List[Entity] = local_object.entities
                for entity in fv_entities:
                    if entity.name == self._object.name:
                        return local_object
        return None

    def _get_upgrade_guidance(self) -> List[str]:
        feature_view_with_entity = self._find_feature_view_with_entity()

        output_strs = []
        if feature_view_with_entity is None:
            output_strs.append(
                f"Unable to determine join key types of {self._object.name}. Please replace your entity with the below where <TYPE> is the type of your join key."
            )
            converted_join_keys = ", ".join(
                [f'Field("{join_key_name}", <TYPE>)' for join_key_name in self._object._spec.join_key_names]
            )
            self._tecton_type_imports.add("Field")
        else:
            feature_view = _get_feature_view(feature_view_with_entity.name)
            view_schema = feature_view._feature_definition.view_schema.to_dict()
            converted_join_keys = ", ".join(
                [
                    f'Field("{join_key_name}", {view_schema[join_key_name]})'
                    for join_key_name in self._object._spec.join_key_names
                ]
            )
            for tecton_type_import in ["Field"] + [
                view_schema[join_key_name] for join_key_name in self._object._spec.join_key_names
            ]:
                self._tecton_type_imports.add(tecton_type_import)

        output_strs.append(
            f"{_get_complete_status_emoji(False)} Replace `join_keys=[...]` with `join_keys=[{converted_join_keys}]`."
        )
        output_strs.append(self._build_import_guidance().to_pretty_string())
        self._append_final_guidance(output_strs)
        return output_strs


class MaterializedFeatureViewGuidance(BaseGuidance):
    _object: Union[BatchFeatureView, StreamFeatureView]
    _obj_type: str
    _stored_feature_view: FeatureView

    def __init__(self, _object, _repo_root):
        super().__init__(_object, _repo_root)
        self._stored_feature_view = _get_feature_view(self._object.name)
        self._view_schema = self._stored_feature_view._feature_definition.view_schema.to_dict()

    def _build_timestamp_recommendation(self):
        timestamp_field = self._stored_feature_view._feature_definition.timestamp_key
        return f'timestamp_field="{timestamp_field}",'

    def __render_time_window(self, time_window: Union[TimeWindow, TimeWindowSeries, LifetimeWindow]) -> str:
        if isinstance(time_window, TimeWindow):
            if time_window.offset == datetime.timedelta(seconds=0):
                return f"{timedelta_to_string(time_window.window_size)}"
            return (
                f"TimeWindow(window_size={timedelta_to_string(time_window.window_size)}, offset={time_window.offset})"
            )
        return time_window._to_spec().to_string()

    def _build_aggregation_replacement(self) -> List[str]:
        aggregates = []
        aggregate_name_to_function_params = {
            aggregation.output_feature_name: get_field_or_none(aggregation, "function_params")
            for aggregation in self._object._spec.aggregate_features
        }

        is_continuous = self._stored_feature_view._feature_definition.is_continuous
        aggregation_interval = self._object.aggregation_interval
        compaction_enabled = self._stored_feature_view._feature_definition.compaction_enabled

        for aggregation in self._object.aggregations:
            input_column_name = aggregation.column
            input_column_type = self._view_schema.get(input_column_name)
            aggregation_default_name = build_aggregation_default_name(
                aggregation.column,
                aggregation.time_window,
                aggregation.function,
                aggregation_interval,
                is_continuous,
                compaction_enabled,
            )

            # only set name argument if the aggregation name is not the default
            # if the aggregation name is the default, implies the user did not set the aggregation name
            name_argument = f'name="{aggregation.name}", ' if aggregation.name != aggregation_default_name else ""

            if input_column_type:
                type_imports = _get_imports_for_type(input_column_type)
                for type_import in type_imports:
                    self._tecton_type_imports.add(type_import)
            print_input_column_type = input_column_type or "<COLUMN_TYPE>"
            function_render = _aggregation_function_to_string_render(
                aggregation.function, aggregate_name_to_function_params.get(aggregation.name)
            )
            time_window = self.__render_time_window(aggregation.time_window)
            aggregate_replacement = f'Aggregate({name_argument}input_column=Field("{input_column_name}", {print_input_column_type}), function={function_render}, time_window={time_window})'
            aggregates.append(aggregate_replacement)
        return aggregates

    # Embeddings and Inference were not live in 0.9, so only need to handle attributes
    def _build_attribute_replacement(self) -> List[str]:
        attributes = []
        for attribute in self._stored_feature_view._feature_definition.features:
            dtype = self._view_schema.get(attribute)
            if dtype:
                type_imports = _get_imports_for_type(dtype)
                for type_import in type_imports:
                    self._tecton_type_imports.add(type_import)
            print_attribute_dtype = dtype or "<COLUMN_TYPE>"
            attribute = f'Attribute("{attribute}", {print_attribute_dtype})'
            attributes.append(attribute)
        return attributes

    def _get_upgrade_guidance(self) -> List[str]:
        output_steps = []
        is_timestamp_field_set = self._object._args.materialized_feature_view_args.timestamp_field != ""

        if bool(self._object.aggregations):
            output_steps.append(f"{_get_complete_status_emoji(False)} Remove `aggregations=[...]`")
            aggregate_feature_suggestions = self._build_aggregation_replacement()
            feature_string = ",\n\t".join(aggregate_feature_suggestions)
            self._tecton_imports.add("Aggregate")
            self._tecton_type_imports.add("Field")
        else:
            attribute_feature_suggestions = self._build_attribute_replacement()
            feature_string = ",\n\t".join(attribute_feature_suggestions)
            self._tecton_imports.add("Attribute")

        is_schema_removed = not self._object._args.materialized_feature_view_args.schema.columns
        output_steps.append((f"{_get_complete_status_emoji(is_schema_removed)} Remove `schema=[...]`"))
        feature_view_arguments = []
        if not is_timestamp_field_set:
            feature_view_arguments.append(self._build_timestamp_recommendation())
        feature_view_arguments.append(f"features=[\n\t{feature_string}\n]")

        is_features_set = self._object._use_feature_param()
        feature_view_arguments_str = "\n".join(feature_view_arguments)
        output_steps.append(
            f"{_get_complete_status_emoji(is_features_set)} Add feature view arguments:\n```\n{feature_view_arguments_str}\n```."
        )
        return output_steps

    def _get_data_source_nodes(self, node: PipelineNode, data_source_nodes: List[PipelineNode]):
        if node.HasField("data_source_node"):
            if node not in data_source_nodes:
                data_source_nodes.append(node.data_source_node)
            return data_source_nodes

        if node.HasField("transformation_node"):
            for input in node.transformation_node.inputs:
                self._get_data_source_nodes(input.node, data_source_nodes)

        return data_source_nodes

    def _build_filtered_source_replacements(self) -> Tuple[List[str], List[str]]:
        filtered_source_replacements = []
        args_data_source_nodes = self._get_data_source_nodes(self._object._args.pipeline.root, [])

        data_proto_data_source_nodes = self._get_data_source_nodes(
            self._stored_feature_view._feature_definition.pipeline.root, []
        )
        data_proto_data_source_nodes_name_to_node = {node.input_name: node for node in data_proto_data_source_nodes}

        currently_existing = []
        for data_source_node in args_data_source_nodes:
            existing_data_source_node = data_proto_data_source_nodes_name_to_node.get(data_source_node.input_name)
            assert existing_data_source_node, f"Cannot find data source node named {data_source_node.input_name}"

            if proto_to_duration(existing_data_source_node.start_time_offset).as_timedelta() != datetime.timedelta(0):
                start_time_offset_as_duration = proto_to_duration(
                    existing_data_source_node.start_time_offset
                ).as_timedelta()
                start_time_offset_as_string = f"{'+ ' if start_time_offset_as_duration > datetime.timedelta(0) else ''}{timedelta_to_string(start_time_offset_as_duration)}"
                currently_existing.append(
                    f"FilteredSource({data_source_node.input_name}, start_time_offset={start_time_offset_as_string})"
                )
                filtered_source_replacements.append(
                    f"{data_source_node.input_name}.select_range(\n\tstart_time = TectonTimeConstant.MATERIALIZATION_START_TIME{start_time_offset_as_string},\n\tend_time = TectonTimeConstant.MATERIALIZATION_END_TIME\n)"
                )
                self._tecton_imports.add("TectonTimeConstant")
            elif existing_data_source_node.window_unbounded:
                currently_existing.append(data_source_node.input_name)
                filtered_source_replacements.append(f"{data_source_node.input_name}.unfiltered()")
            elif existing_data_source_node.window_unbounded_preceding:
                # we do not store the offset time delta on the data source node if it >= MIN_START_OFFSET (100 years), so just stub it for currently existing.
                currently_existing.append(
                    f"FilteredSource({data_source_node.input_name}, start_time_offset=timedelta())"
                )
                filtered_source_replacements.append(
                    f"{data_source_node.input_name}.select_range(\n\tstart_time = TectonTimeConstant.UNBOUNDED_PAST,\n\tend_time = TectonTimeConstant.MATERIALIZATION_END_TIME\n)"
                )
                self._tecton_imports.add("TectonTimeConstant")
            else:
                currently_existing.append(f"FilteredSource({data_source_node.input_name})")
                filtered_source_replacements.append(f"{data_source_node.input_name}")
        return currently_existing, filtered_source_replacements


class BatchFeatureViewGuidance(MaterializedFeatureViewGuidance):
    _object: BatchFeatureView
    _obj_type = "BatchFeatureView"

    def _build_filtered_source_guidance(self) -> str:
        currently_existing, filtered_source_replacements = self._build_filtered_source_replacements()
        currently_existing_str = ", ".join(currently_existing)
        filtered_source_replacement_str = ", ".join(filtered_source_replacements)

        return f"{_get_complete_status_emoji(False)} Replace data sources:\n```\nsources=[{currently_existing_str}]\n```\nwith: \n```\nsources=[{filtered_source_replacement_str}]\n```."

    def _get_upgrade_guidance(self) -> List[str]:
        guidance = super()._get_upgrade_guidance()
        guidance.append(self._build_filtered_source_guidance())

        guidance.append(self._build_import_guidance().to_pretty_string())

        self._append_final_guidance(guidance)
        return guidance


class StreamFeatureViewGuidance(MaterializedFeatureViewGuidance):
    _object: StreamFeatureView
    _obj_type = "StreamFeatureView"

    def _build_filtered_source_guidance(self) -> str:
        currently_existing, filtered_source_replacements = self._build_filtered_source_replacements()
        currently_existing_str = ", ".join(currently_existing)
        filtered_source_replacement_str = ", ".join(filtered_source_replacements)
        return f"{_get_complete_status_emoji(False)} Replace `source={currently_existing_str}` with `source={filtered_source_replacement_str}`."

    def _get_aggregation_leading_edge_guidance(self) -> str:
        is_aggregation_leading_edge_set = (
            self._object._args.materialized_feature_view_args.aggregation_leading_edge
            == AggregationLeadingEdge.UNSPECIFIED
        )
        if not is_aggregation_leading_edge_set:
            self._tecton_imports.add("AggregationLeadingEdge")
        return f"{_get_complete_status_emoji(is_aggregation_leading_edge_set)} Set `aggregation_leading_edge=AggregationLeadingEdge.LATEST_EVENT_TIME`."

    def _get_upgrade_guidance(self) -> List[str]:
        guidance = super()._get_upgrade_guidance()
        guidance.append(self._build_filtered_source_guidance())
        guidance.append(self._get_aggregation_leading_edge_guidance())

        guidance.append(self._build_import_guidance().to_pretty_string())

        self._append_final_guidance(guidance)
        return guidance


class OnDemandFeatureViewGuidance(BaseGuidance):
    _object: OnDemandFeatureView
    _obj_type = "OnDemandFeatureView"

    def __init__(self, _object, _repo_root):
        super().__init__(_object, _repo_root)
        self._stored_feature_view = _get_feature_view(self._object.name)
        self._view_schema = self._stored_feature_view._feature_definition.view_schema.to_dict()

    # Embeddings and Inference were not live in 0.9, so only need to handle attributes
    def _build_attribute_replacement(self) -> List[str]:
        self._tecton_imports.add("Attribute")
        attributes = []
        for attribute in self._stored_feature_view._feature_definition.features:
            attribute_dtype = self._view_schema.get(attribute)
            if attribute_dtype:
                type_imports = _get_imports_for_type(attribute_dtype)
                for type_import in type_imports:
                    self._tecton_type_imports.add(type_import)
            attribute_dtype_str = attribute_dtype or "<COLUMN_TYPE>"
            attribute = f'Attribute("{attribute}", {attribute_dtype_str})'
            attributes.append(attribute)
        return attributes

    def _get_upgrade_guidance(self) -> List[str]:
        output_steps = []
        is_schema_removed = not self._object._args.realtime_args.schema.fields
        output_steps.append((f"{_get_complete_status_emoji(is_schema_removed)} Remove `schema=[...]`"))

        is_features_set = self._object._use_feature_param()
        attribute_feature_suggestions = self._build_attribute_replacement()
        attribute_feature_string = ",\n\t".join(attribute_feature_suggestions)
        output_steps.append(
            f"{_get_complete_status_emoji(is_features_set)} Add \n```\nfeatures=[\n\t{attribute_feature_string}\n]\n```."
        )

        output_steps.append(self._build_import_guidance().to_pretty_string())

        output_steps.append(
            f"{_get_complete_status_emoji(False)} Rename from `on_demand_feature_view` to realtime_feature_view` and update import from `tecton.v09_compat.on_demand_feature_view` to `tecton.realtime_feature_view`."
        )
        return output_steps


class FeatureTableGuidance(BaseGuidance):
    _object: FeatureTable
    _obj_type = "FeatureTable"

    def __init__(self, _object, _repo_root):
        super().__init__(_object, _repo_root)
        self._stored_feature_view = _get_feature_table(self._object.name)
        self._view_schema = self._stored_feature_view._feature_definition.view_schema.to_dict()

    def _build_timestamp_recommendation(self):
        timestamp_field = self._stored_feature_view._feature_definition.timestamp_key
        return f'Set `timestamp_field="{timestamp_field}"`.'

    # Embeddings and Inference were not live in 0.9, so only need to handle attributes
    def _build_attribute_replacement(self) -> List[str]:
        self._tecton_imports.add("Attribute")
        attributes = []
        for attribute in self._stored_feature_view._feature_definition.features:
            attribute_dtype = self._view_schema.get(attribute)
            if attribute_dtype:
                type_imports = _get_imports_for_type(attribute_dtype)
                for type_import in type_imports:
                    self._tecton_type_imports.add(type_import)
            attribute_dtype_str = attribute_dtype or "<COLUMN_TYPE>"
            attribute = f'Attribute("{attribute}", {attribute_dtype_str})'
            attributes.append(attribute)
        return attributes

    def _get_upgrade_guidance(self) -> List[str]:
        output_steps = []
        is_timestamp_field_set = self._object._args.feature_table_args.timestamp_field != ""
        output_steps.append(
            f"{_get_complete_status_emoji(is_timestamp_field_set)} {self._build_timestamp_recommendation()}"
        )

        is_schema_removed = not self._object._args.feature_table_args.schema.fields
        output_steps.append((f"{_get_complete_status_emoji(is_schema_removed)} Remove `schema=[...]`"))

        is_features_set = self._object._use_feature_param()
        attribute_feature_suggestions = self._build_attribute_replacement()
        attribute_feature_string = ",\n\t".join(attribute_feature_suggestions)
        output_steps.append(
            f"{_get_complete_status_emoji(is_features_set)} Add \n```\nfeatures=[\n\t{attribute_feature_string}\n]\n```."
        )

        output_steps.append(self._build_import_guidance().to_pretty_string())

        self._append_final_guidance(output_steps)
        return output_steps
