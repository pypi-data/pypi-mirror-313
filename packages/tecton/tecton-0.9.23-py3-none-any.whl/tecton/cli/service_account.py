import json
import sys

import click

from tecton._internals import metadata_service
from tecton.cli import printer
from tecton.cli.command import TectonGroup
from tecton_core.errors import TectonAPIValidationError
from tecton_proto.metadataservice.metadata_service_pb2 import CreateServiceAccountRequest
from tecton_proto.metadataservice.metadata_service_pb2 import DeleteServiceAccountRequest
from tecton_proto.metadataservice.metadata_service_pb2 import GetServiceAccountsRequest
from tecton_proto.metadataservice.metadata_service_pb2 import UpdateServiceAccountRequest


@click.command("service-account", cls=TectonGroup)
def service_account():
    """Manage Service Accounts"""


@service_account.command()
@click.option("-n", "--name", required=True, help="Name of the Service Account")
@click.option(
    "-d", "--description", default="", help="An optional, human readable description for this Service Account"
)
@click.option("--json-out", default=False, is_flag=True, help="Format Output as JSON")
def create(name, description, json_out):
    """Create a new Service Account."""
    try:
        request = CreateServiceAccountRequest(name=name, description=description)
        response = metadata_service.instance().CreateServiceAccount(request)
    except TectonAPIValidationError as e:
        printer.safe_print(f"Failed to create service account: {e}", file=sys.stderr)
        sys.exit(1)
    if json_out:
        service_account = {}
        service_account["api_key"] = response.api_key
        service_account["id"] = response.id
        printer.safe_print(json.dumps(service_account, indent=4))
    else:
        printer.safe_print("Save this API Key - you will not be able to get it again.")
        printer.safe_print(f"API Key:            {response.api_key}")
        printer.safe_print(f"Service Account ID: {response.id}")
        printer.safe_print("Use `tecton access-control assign-role` to assign roles to your new service account.")


@service_account.command()
@click.argument("id", required=True)
def delete(id):
    """Permanently delete a Service Account by its ID."""
    request = DeleteServiceAccountRequest(id=id)
    try:
        response = metadata_service.instance().DeleteServiceAccount(request)
    except TectonAPIValidationError as e:
        printer.safe_print(f"Failed to delete service account: {e}", file=sys.stderr)
        sys.exit(1)
    printer.safe_print("Successfully deleted Service Account")


@service_account.command()
@click.option("-n", "--name", help="Name of the Service Account")
@click.option("-d", "--description", help="An optional, human readable description for this Service Account")
@click.argument("id", required=True)
def update(id, name, description):
    """Update the name or description of a Service Account."""
    request = UpdateServiceAccountRequest(id=id)

    if name is None and description is None:
        msg = "Please mention the field to update using --name or --description."
        raise click.ClickException(msg)

    if name:
        request.name = name

    if description is not None:
        request.description = description

    try:
        response = metadata_service.instance().UpdateServiceAccount(request)
    except TectonAPIValidationError as e:
        printer.safe_print(f"Failed to Update Service Account: {e}", file=sys.stderr)
        sys.exit(1)

    printer.safe_print("Successfully updated Service Account")


@service_account.command()
@click.argument("id", required=True)
def activate(id):
    """Activate a Service Account by its ID."""
    request = UpdateServiceAccountRequest(id=id, is_active=True)
    try:
        response = metadata_service.instance().UpdateServiceAccount(request)
    except TectonAPIValidationError as e:
        printer.safe_print(f"Failed to Activate Service Account: {e}", file=sys.stderr)
        sys.exit(1)
    printer.safe_print("Successfully activated Service Account")


@service_account.command()
@click.argument("id", required=True)
def deactivate(id):
    """Deactivate a Service Account by its ID. This disables the Service Account but does not permanently delete it."""
    request = UpdateServiceAccountRequest(id=id, is_active=False)
    try:
        response = metadata_service.instance().UpdateServiceAccount(request)
    except TectonAPIValidationError as e:
        printer.safe_print(f"Failed to Deactivate Service Account: {e}", file=sys.stderr)
        sys.exit(1)
    printer.safe_print("Successfully deactivated Service Account")


@service_account.command()
@click.option("--json-out", default=False, is_flag=True, help="Format Output as JSON")
@click.option("-s", "--search-string", help="Search String to search by ID, Name or Description")
def list(json_out, search_string):
    """List Service Accounts."""
    request = GetServiceAccountsRequest()

    if search_string is not None:
        request.search = search_string

    response = metadata_service.instance().GetServiceAccounts(request)
    service_accounts = []

    if len(response.service_accounts) == 0:
        printer.safe_print("No Service Accounts Found")
        return

    for k in response.service_accounts:
        if json_out:
            account = {}
            account["name"] = k.name
            account["id"] = k.id
            account["description"] = k.description
            account["active"] = k.is_active
            service_accounts.append(account)
        else:
            printer.safe_print(f"{'Name: ': <15}{k.name}")
            printer.safe_print(f"{'ID: ': <15}{k.id}")
            if k.description:
                printer.safe_print(f"{'Description: ': <15}{k.description}")
            printer.safe_print(f"{'Active: ': <15}{k.is_active}")
            printer.safe_print()
    if json_out:
        printer.safe_print(json.dumps(service_accounts, indent=4))
