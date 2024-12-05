from tecton_proto.auth import authorization_service_pb2
from tecton_proto.materializationjobservice import materialization_job_service_pb2
from tecton_proto.metadataservice import metadata_service_pb2
from tecton_proto.remoteenvironmentservice import remote_environment_service_pb2
from tecton_proto.secrets import secrets_service_pb2
from tecton_proto.testhelperservice import test_helper_service_pb2


GRPC_SERVICE_MODULES = [
    metadata_service_pb2,
    materialization_job_service_pb2,
    authorization_service_pb2,
    remote_environment_service_pb2,
    test_helper_service_pb2,
    secrets_service_pb2,
]
