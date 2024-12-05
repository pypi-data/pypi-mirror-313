from types import MappingProxyType
from typing import Mapping
from typing import Tuple

from typeguard import typechecked

from tecton_core.specs import tecton_object_spec
from tecton_core.specs import utils
from tecton_proto.args import entity_pb2 as entity__args_pb2
from tecton_proto.data import entity_pb2 as entity__data_pb2
from tecton_proto.validation import validator_pb2


__all__ = [
    "EntitySpec",
]


@utils.frozen_strict
class EntitySpec(tecton_object_spec.TectonObjectSpec):
    join_keys: Tuple[str, ...]
    options: Mapping[str, str]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: entity__data_pb2.Entity) -> "EntitySpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(proto.entity_id, proto.fco_metadata),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            validation_args=validator_pb2.FcoValidationArgs(entity=proto.validation_args),
            options=MappingProxyType(proto.options),
        )

    @classmethod
    @typechecked
    def from_args_proto(cls, proto: entity__args_pb2.EntityArgs) -> "EntitySpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(proto.entity_id, proto.info),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            validation_args=None,
            options=MappingProxyType(proto.options),
        )
