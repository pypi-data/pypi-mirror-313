from typing import Optional

from tecton._internals import metadata_service
from tecton_core import conf
from tecton_core.offline_store import DEFAULT_OPTIONS_PROVIDERS
from tecton_core.offline_store import OfflineStoreOptionsProvider
from tecton_core.offline_store import S3Options
from tecton_core.offline_store import S3OptionsSource
from tecton_proto.common.id_pb2 import Id
from tecton_proto.metadataservice.metadata_service_pb2 import GetOfflineStoreCredentialsRequest


class MDSOfflineStoreOptionsProvider(OfflineStoreOptionsProvider):
    def get_s3_options_for_feature_view(self, feature_view_id: Id) -> Optional[S3Options]:
        if conf.get_bool("USE_LOCAL_OFFLINE_STORE_CREDENTIALS"):
            return None
        request = GetOfflineStoreCredentialsRequest(feature_view_id=feature_view_id)
        response = metadata_service.instance().GetOfflineStoreCredentials(request)
        if not response.HasField("aws"):
            return None
        return S3Options(
            access_key_id=response.aws.access_key_id,
            secret_access_key=response.aws.secret_access_key,
            session_token=response.aws.session_token,
            region=conf.get_or_raise("CLUSTER_REGION"),
            options_source=S3OptionsSource.MDS,
        )

    def get_s3_options_for_data_source(self, data_source_id: Id) -> Optional[S3Options]:
        if conf.get_bool("USE_LOCAL_OFFLINE_STORE_CREDENTIALS"):
            return None
        request = GetOfflineStoreCredentialsRequest(data_source_id=data_source_id)
        response = metadata_service.instance().GetOfflineStoreCredentials(request)
        if not response.HasField("aws"):
            return None
        return S3Options(
            access_key_id=response.aws.access_key_id,
            secret_access_key=response.aws.secret_access_key,
            session_token=response.aws.session_token,
            region=conf.get_or_raise("CLUSTER_REGION"),
            options_source=S3OptionsSource.MDS,
        )


INTERACTIVE_OFFLINE_STORE_OPTIONS_PROVIDERS = [MDSOfflineStoreOptionsProvider(), *DEFAULT_OPTIONS_PROVIDERS]
