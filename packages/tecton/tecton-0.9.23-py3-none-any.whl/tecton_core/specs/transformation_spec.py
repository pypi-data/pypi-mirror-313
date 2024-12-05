from typing import Callable
from typing import Optional

import attrs
from typeguard import typechecked

from tecton_core import function_deserialization
from tecton_core.specs import tecton_object_spec
from tecton_core.specs import utils
from tecton_proto.args import transformation_pb2 as transformation__args_pb2
from tecton_proto.data import transformation_pb2 as transformation__data_pb2
from tecton_proto.validation import validator_pb2


__all__ = ["TransformationSpec"]


@utils.frozen_strict
class TransformationSpec(tecton_object_spec.TectonObjectSpec):
    transformation_mode: transformation__args_pb2.TransformationMode.ValueType
    user_function: Callable = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: transformation__data_pb2.Transformation, deserialize_funcs_to_main: bool = False
    ) -> "TransformationSpec":
        user_function = None
        if proto.HasField("user_function"):
            if deserialize_funcs_to_main:
                user_function = function_deserialization.from_proto_to_main(proto.user_function)
            else:
                user_function = function_deserialization.from_proto(proto.user_function)

        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.transformation_id, proto.fco_metadata
            ),
            transformation_mode=proto.transformation_mode,
            user_function=user_function,
            validation_args=validator_pb2.FcoValidationArgs(transformation=proto.validation_args),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: transformation__args_pb2.TransformationArgs, user_function: Optional[Callable]
    ) -> "TransformationSpec":
        # If a function was serialized for this transformation (e.g. because it was defined in a repo), then prefer to
        # use the serialized function over directly using the Python function.
        if proto.HasField("user_function"):
            user_function = function_deserialization.from_proto(proto.user_function)

        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(proto.transformation_id, proto.info),
            transformation_mode=proto.transformation_mode,
            user_function=user_function,
            validation_args=None,
        )
