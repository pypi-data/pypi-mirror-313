from typing import List
from typing import Optional

from tecton._internals import metadata_service
from tecton._internals.sdk_decorators import sdk_public_method
from tecton_core import errors
from tecton_proto.metadataservice.metadata_service_pb2 import ListWorkspacesRequest


@sdk_public_method
def list_workspaces() -> List[str]:
    """
    Returns a list of the names of all registered Workspaces.

    :return: A list of strings.
    """
    request = ListWorkspacesRequest()
    response = metadata_service.instance().ListWorkspaces(request)
    return sorted([workspace.name for workspace in response.workspaces])


@sdk_public_method
def list_feature_views(workspace_name: Optional[str] = None):
    msg = 'list_feature_views() must be called from a Workspace object. E.g. tecton.get_workspace("<workspace>").list_feature_views().'
    raise errors.TectonValidationError(msg)


@sdk_public_method
def list_feature_tables(workspace_name: Optional[str] = None):
    msg = 'list_feature_tables() must be called from a Workspace object. E.g. tecton.get_workspace("<workspace>").list_feature_tables().'
    raise errors.TectonValidationError(msg)


@sdk_public_method
def list_feature_services(workspace_name: Optional[str] = None):
    msg = 'list_feature_services() must be called from a Workspace object. E.g. tecton.get_workspace("<workspace>").list_feature_services().'
    raise errors.TectonValidationError(msg)


@sdk_public_method
def list_transformations(workspace_name: Optional[str] = None):
    msg = 'list_transformations() must be called from a Workspace object. E.g. tecton.get_workspace("<workspace>").list_transformations().'
    raise errors.TectonValidationError(msg)


@sdk_public_method
def list_entities(workspace_name: Optional[str] = None):
    msg = 'list_entities() must be called from a Workspace object. E.g. tecton.get_workspace("<workspace>").list_entities().'
    raise errors.TectonValidationError(msg)


@sdk_public_method
def list_data_sources(workspace_name: Optional[str] = None):
    msg = 'list_data_sources() must be called from a Workspace object. E.g. tecton.get_workspace("<workspace>").list_data_sources().'
    raise errors.TectonValidationError(msg)


@sdk_public_method
def list_datasets(workspace_name: Optional[str] = None):
    msg = 'list_datasets() must be called from a Workspace object. E.g. tecton.get_workspace("<workspace>").list_datasets().'
    raise errors.TectonValidationError(msg)
