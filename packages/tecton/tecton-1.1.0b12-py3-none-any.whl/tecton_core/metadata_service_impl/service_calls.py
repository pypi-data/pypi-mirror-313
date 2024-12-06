"""creates a dictionary of MDS methods to the grpc call representation

we have multiple services running in the MDS server with their own service protos
combines the methods across the different service protos to a dictionary of method to grpc call repr obj
"""

from dataclasses import dataclass
from types import ModuleType
from typing import Callable
from typing import Dict
from typing import List

from google.protobuf.empty_pb2 import Empty


@dataclass
class GrpcCall:
    """
    grpc call data representation

    Attributes:
        method: grpc method name
        request_serializer: serialization function for the grpc request proto
        response_deserializer: deserialization function for the grpc response proto
    """

    method: str
    request_serializer: Callable
    response_deserializer: Callable


def get_method_name_to_grpc_call(grpc_service_modules: List[ModuleType]) -> Dict[str, GrpcCall]:
    """
    dictionary of mds methods to grpc call repr obj
    later used by the grpc stub and the http stub for MDS py client
    """
    method_name_to_call = {}
    for module in grpc_service_modules:
        for service_name, descriptor in module.DESCRIPTOR.services_by_name.items():
            for method in descriptor.methods:
                if method.input_type.name == "Empty":
                    request_serializer = Empty.SerializeToString
                else:
                    request_serializer = getattr(module, method.input_type.name).SerializeToString
                if method.output_type.name == "Empty":
                    response_deserializer = Empty.FromString
                else:
                    response_deserializer = getattr(module, method.output_type.name).FromString
                grpc_method = f"/{descriptor.full_name}/{method.name}"
                grpc_call = GrpcCall(grpc_method, request_serializer, response_deserializer)
                if method_name_to_call.get(method.name) is None:
                    method_name_to_call[method.name] = grpc_call
                else:
                    msg = f"Method name collision for method {method.name} in service {service_name} and {method_name_to_call.get(method.name).method}"
                    raise Exception(msg)
    return method_name_to_call
