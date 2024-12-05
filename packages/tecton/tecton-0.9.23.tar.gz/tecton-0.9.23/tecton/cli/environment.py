import json
import math
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from dataclasses import dataclass
from datetime import datetime
from datetime import timezone
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple

import click
from google.protobuf import timestamp_pb2
from tqdm import tqdm

from tecton import version
from tecton._internals import metadata_service
from tecton.cli import printer
from tecton.cli.cli_utils import display_table
from tecton.cli.command import TectonGroup
from tecton.cli.environment_utils import EnvironmentDependencies
from tecton.cli.environment_utils import create_requirements_from_lock_file
from tecton.cli.environment_utils import download_dependencies
from tecton.cli.environment_utils import is_valid_environment_name
from tecton.cli.environment_utils import resolve_dependencies
from tecton_core import http
from tecton_core import id_helper
from tecton_proto.common.container_image_pb2 import ContainerImage
from tecton_proto.data.remote_compute_environment_pb2 import ObjectStoreUploadPart
from tecton_proto.data.remote_compute_environment_pb2 import RemoteComputeType
from tecton_proto.data.remote_compute_environment_pb2 import RemoteEnvironmentStatus
from tecton_proto.data.remote_compute_environment_pb2 import RemoteEnvironmentUploadInfo
from tecton_proto.data.remote_compute_environment_pb2 import S3UploadInfo
from tecton_proto.data.remote_compute_environment_pb2 import S3UploadPart
from tecton_proto.remoteenvironmentservice.remote_environment_service_pb2 import CompletePackagesUploadRequest
from tecton_proto.remoteenvironmentservice.remote_environment_service_pb2 import CreateRemoteEnvironmentRequest
from tecton_proto.remoteenvironmentservice.remote_environment_service_pb2 import DeleteRemoteEnvironmentsRequest
from tecton_proto.remoteenvironmentservice.remote_environment_service_pb2 import GetDependentFeatureServicesRequest
from tecton_proto.remoteenvironmentservice.remote_environment_service_pb2 import GetPackagesUploadUrlRequest
from tecton_proto.remoteenvironmentservice.remote_environment_service_pb2 import ListRemoteEnvironmentsRequest
from tecton_proto.remoteenvironmentservice.remote_environment_service_pb2 import StartPackagesUploadRequest


# libraries may have Requires: Python >=3.8.1
DEFAULT_PYTHON_VERSION = "3.8.17"
RESOLVED_REQUIREMENTS_FILENAME = "resolved_requirements.txt"
ERROR_MESSAGE_PREFIX = "⛔ ERROR: "
DEBUG_MESSAGE_PREFIX = "🔎 "
DEPENDENCY_RESOLUTION_TIMEOUT_SECONDS = 600
TECTON_RIFT_MATERIALIZATION_RUNTIME_PACKAGE = "tecton"
TECTON_TRANSFORM_RUNTIME_PACKAGE = "tecton-runtime"
DEFAULT_ARCHITECTURE = "x86_64"
CHECK_MARK = "✅"
ERROR_SIGN = "⛔"

# boto3 defaults to 8MB for multi-part uploads using upload_file.
DEFAULT_UPLOAD_PART_SIZE_MB = 16

# 5 was arbitrarily selected. We want to be conservative as this will run in customer's environments
DEFAULT_MAX_WORKERS_THREADS = 5

# The maximum size of all dependencies allowed for upload
MAX_ALLOWED_DEPENDENCIES_SIZE_GB = 10

MEGABYTE = 1024 * 1024
GIGABYTE = 1024 * MEGABYTE


@dataclass
class UploadPart:
    """
    Represents an individual part of a file that needs to be uploaded in chunks or parts.
    :param part_number (int): The 1-indexed number of the part to be uploaded.
    :param offset (int): The starting byte offset of this part in the file.
    :param part_size (int): The size of this part in bytes.
    """

    part_number: int
    offset: int
    part_size: int


@dataclass
class EnvironmentIdentifier:
    id: str
    name: str

    def __post_init__(self):
        if not self.id and not self.name:
            printer.safe_print(
                f"{ERROR_MESSAGE_PREFIX} At least one of `environment-id` or `name` must be provided", file=sys.stderr
            )
            sys.exit(1)

    def __str__(self):
        if self.id:
            return f"id: {self.id}"
        elif self.name:
            return f"name: {self.name}"
        else:
            return "No name or id set"

    def __eq__(self, identifier):
        if isinstance(identifier, EnvironmentIdentifier):
            if self.id:
                return self.id == identifier.id
            elif self.name:
                return self.name == identifier.name
        return False


@click.command("environment", cls=TectonGroup)
def environment():
    """Manage Environments for ODFV Execution"""


@environment.command("list")
def list():
    """List all available Python Environments"""
    remote_environments = _list_environments()
    _display_environments(remote_environments)


@environment.command("get")
@click.option("--environment-id", help="Environment Id", required=False, type=str)
@click.option("--name", help="Environment Name", required=False, type=str)
def get(environment_id: Optional[str] = None, name: Optional[str] = None):
    """Get Python Environment(s) matching a name or an ID"""
    environment_identifier = EnvironmentIdentifier(id=environment_id, name=name)
    remote_environments = _list_environments(environment_identifier=environment_identifier)
    if len(remote_environments) < 1:
        error_message = f"⛔ Could not find a match for environment with {environment_identifier.__str__()}!"
        printer.safe_print(error_message, file=sys.stderr)
        sys.exit(1)
    _display_environments(remote_environments)


@environment.command("resolve-dependencies")
@click.option("-r", "--requirements", help="Path to a requirements file", required=True, type=click.Path(exists=True))
@click.option(
    "-o",
    "--output-file",
    help="Output file to write resolved and fully pinned requirements to. If not specified, the pinned requirements will be printed to stdout",
    required=False,
    type=click.Path(exists=False),
)
@click.option(
    "-p",
    "--python-version",
    help=f"Python Version for the environment, defaults to {DEFAULT_PYTHON_VERSION}",
    required=False,
)
@click.option("--verbose", help="Prints verbose output for the dependency resolution process", is_flag=True)
def resolve_requirements(
    requirements: str,
    output_file: Optional[str] = None,
    python_version: Optional[str] = None,
    verbose: Optional[bool] = False,
):
    """Resolve dependencies and return a fully resolved set of requirements for a given requirements.txt"""
    _python_version = python_version or DEFAULT_PYTHON_VERSION

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            resolved_requirements_path, lock_output_path = _run_dependency_resolution(
                requirements_path=Path(requirements),
                resolved_requirements_directory=Path(tmpdir),
                python_version=_python_version,
                verbose=verbose,
            )
        except ValueError as e:
            printer.safe_print(f"{ERROR_MESSAGE_PREFIX} {e}", file=sys.stderr)
            sys.exit(1)

        _validate_and_get_dependencies(lock_output_path)
        printer.safe_print("✅ Successfully resolved dependencies")

        if output_file is not None:
            output_path = Path(output_file)
            resolved_requirements_str = resolved_requirements_path.read_bytes()
            output_path.write_bytes(resolved_requirements_str)
        else:
            printer.safe_print("\n🎉 Fully Resolved Requirements: \n")
            _display_requirements(requirements_path=resolved_requirements_path, verbose=verbose)


@environment.command("create")
@click.option("-n", "--name", help="Name of the environment", required=True, type=str)
@click.option(
    "-r",
    "--requirements",
    help="Path to the requirements.txt file containing all dependencies for the environment",
    required=True,
    type=click.Path(exists=True),
)
@click.option("-d", "--description", help="A description for the environment", required=False, type=str)
@click.option(
    "-p",
    "--python-version",
    help=f"Python Version for the environment, defaults to {DEFAULT_PYTHON_VERSION}",
    required=False,
)
@click.option(
    "--verbose",
    help="Activates debug mode and provides verbose output to assist in troubleshooting.",
    is_flag=True,
)
def create(
    name: str,
    requirements: str,
    description: Optional[str] = None,
    python_version: Optional[str] = None,
    verbose: Optional[bool] = False,
):
    """Create a custom Python Environment for ODFVs"""
    _python_version = python_version or DEFAULT_PYTHON_VERSION
    if not is_valid_environment_name(name):
        printer.safe_print(
            f"{ERROR_MESSAGE_PREFIX} Invalid name. Custom environment names can only contain letters, numbers, hyphens, and underscores",
            file=sys.stderr,
        )
        sys.exit(1)

    environment_names = [e.name for e in _list_environments()]
    if name in environment_names:
        printer.safe_print(
            f"{ERROR_MESSAGE_PREFIX} An environment with the name `{name}` already exists in Tecton!",
            file=sys.stderr,
        )
        sys.exit(1)

    resp = _create_environment_with_requirements(
        name,
        description,
        Path(requirements),
        _python_version,
        verbose=verbose,
    )
    if resp:
        _display_environments([resp.remote_environment])
        printer.safe_print(
            f"\n🎉 Successfully created environment {name} with Status=PENDING. Please run `tecton environment get --name <environment-name>` to monitor the status of the environment"
        )


@environment.command("describe")
@click.option("-i", "--environment-id", help="Environment ID", required=False, type=str)
@click.option("-n", "--name", help="Environment Name", required=False, type=str)
def describe(environment_id: Optional[str] = None, name: Optional[str] = None):
    """
    Print additional information about an environment
    """
    environment_identifier = EnvironmentIdentifier(id=environment_id, name=name)
    environments = _list_environments(environment_identifier)
    if not environments:
        error_message = f"⛔ Could not find a match for environment with {environment_identifier.__str__()}!"
        printer.safe_print(error_message, file=sys.stderr)
        sys.exit(1)
    if len(environments) > 1:
        message = (
            f"Could not find environment with {environment_identifier.__str__()}. Did you mean one of the following?"
        )
        printer.safe_print(f"⚠️ {message}")
        _display_environments(environments)
    else:
        environment_match = environments[0]
        printer.safe_print("\n💡 Environment Details: \n")
        _display_environments(environments)
        printer.safe_print("\n💡 Input Requirements: \n")
        _display_requirements(requirements_str=environment_match.requirements)
        printer.safe_print("\n✅ Fully Resolved Requirements: \n")
        _display_requirements(requirements_str=environment_match.resolved_requirements)


@environment.command("delete")
@click.option("-i", "--environment-id", help="Environment ID", required=False, type=str)
@click.option("-n", "--name", help="Environment Name", required=False, type=str)
def delete(environment_id: Optional[str] = None, name: Optional[str] = None):
    """Delete an existing custom Python Environment by name or ID"""
    environment_identifier = EnvironmentIdentifier(id=environment_id, name=name)
    environments = _list_environments(environment_identifier=environment_identifier)
    if not environments:
        printer.safe_print(
            f"⛔ No matching environment found for: {environment_identifier.__str__()}. Please verify available environments using the `tecton environment list` command",
            file=sys.stderr,
        )
        sys.exit(1)
    result_identifier = None
    environment_to_delete = None
    if len(environments) == 1:
        environment_to_delete = environments[0]
        result_identifier = EnvironmentIdentifier(id=environment_to_delete.id, name=environment_to_delete.name)

    if len(environments) > 1 or not environment_identifier.__eq__(identifier=result_identifier):
        printer.safe_print(
            f"⚠️ No matching environment found for: {environment_identifier.__str__()}. Did you mean one of the following environment(s)? \n\n",
            file=sys.stderr,
        )
        _display_environments(environments)
    else:
        _check_environment_usage(environment_to_delete.id)
        printer.safe_print(
            f"✅ Verified that the environment {environment_to_delete.name} has no dependent Feature Service(s)."
        )
        confirmation_text = f"⚠️  Are you sure you want to delete environment {environment_to_delete.name}? (y/n) :"
        confirmation = input(confirmation_text).lower().strip()
        if confirmation == "y":
            try:
                _delete_environment(environment_id=environment_to_delete.id)
                printer.safe_print(f"✅ Marked environment '{environment_identifier.__str__()}' for deletion.")
            except Exception as e:
                printer.safe_print(f"⛔ Failed to delete environment. error = {str(e)}, type= {type(e).__name__}")
        else:
            printer.safe_print(f"Cancelled deletion for environment: {environment_identifier.__str__()}")


def _display_environments(environments: list):
    headings = [
        "Id",
        "Name",
        "Description",
        "Type",
        "Status",
        "Materialization Version",
        "Tecton Runtime Version",
        "Created At",
    ]
    display_table(
        headings,
        [
            (
                i.id,
                i.name,
                i.description,
                RemoteComputeType.Name(i.type).split("_")[-1],
                RemoteEnvironmentStatus.Name(i.status).split("_")[-1],
                i.rift_batch_job_environment.tecton_materialization_runtime_version or "N/A",
                i.on_demand_job_environment.tecton_transform_runtime_version or "N/A",
                _timestamp_to_string(i.created_at),
            )
            for i in environments
        ],
    )


def _display_dependent_feature_services(dependent_feature_services: list):
    headings = ["Workspace Name", "Feature Service Name"]
    display_table(
        headings,
        [
            (
                i.workspace_name,
                i.feature_service_name,
            )
            for i in dependent_feature_services
        ],
    )


def _create_environment_with_image(name: str, description: str, image_uri):
    try:
        req = CreateRemoteEnvironmentRequest()
        req.name = name
        req.description = description

        image_info = ContainerImage()
        image_info.image_uri = image_uri

        req.image_info.CopyFrom(image_info)

        return metadata_service.instance().CreateRemoteEnvironment(req)
    except PermissionError as _:
        printer.safe_print(
            "The user is not authorized to create environment(s) in Tecton. Please reach out to your Admin to complete this "
            "action",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        printer.safe_print(f"Failed to create environment: {e}", file=sys.stderr)
        sys.exit(1)


def _create_environment_with_requirements(
    name: str,
    description: str,
    requirements_path: Path,
    python_version: str,
    verbose: bool,
):
    """Create a custom environment by resolving dependencies, downloading wheels and updating MDS
    Parameters:
        name(str): Name of the custom environment
        description(str): Description of the custom environment
        requirements_path(str): Path to the `requirements.txt` file
        python_version(str): The Python version to resolve the dependencies for
        verbose(bool): Activates verbose logging
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            resolved_requirements_path, lock_output_path = _run_dependency_resolution(
                requirements_path=requirements_path,
                resolved_requirements_directory=Path(tmpdir),
                python_version=python_version,
                verbose=verbose,
            )
        except ValueError as e:
            printer.safe_print(f"{ERROR_MESSAGE_PREFIX} {e}", file=sys.stderr)
            sys.exit(1)

        dependencies = _validate_and_get_dependencies(lock_output_path)

        printer.safe_print("✅ Successfully resolved dependencies")
        tecton_runtime_version = dependencies.get_version(dependency_name=TECTON_TRANSFORM_RUNTIME_PACKAGE)
        tecton_rift_version = dependencies.get_version(dependency_name=TECTON_RIFT_MATERIALIZATION_RUNTIME_PACKAGE)

        printer.safe_print(
            f"\n💡 Creating environment '{name}' for job types:\n"
            f"{CHECK_MARK if tecton_runtime_version else ERROR_SIGN} On Demand\n"
            f"{CHECK_MARK if tecton_rift_version else ERROR_SIGN} Rift Batch\n"
            f"{CHECK_MARK if tecton_rift_version and tecton_runtime_version else ERROR_SIGN} Rift Stream Ingest\n"
        )

        url_requirements_path = Path(tmpdir) / "url_requirements.txt"

        # doing this to use the url because some wheels maybe coming from different sources
        create_requirements_from_lock_file(lock_output_path, url_requirements_path)

        download_wheels_dir = Path(tmpdir) / "wheels"
        download_wheels_dir.mkdir()
        printer.safe_print("\n⏳ Downloading wheels. This may take a few seconds.....\n")
        download_dependencies(
            requirements_path=url_requirements_path,
            target_directory=download_wheels_dir,
            python_version=python_version,
            verbose=verbose,
        )
        printer.safe_print("\n✅ Successfully downloaded dependencies")

        directory_size = _get_directory_size(download_wheels_dir)
        if directory_size > (MAX_ALLOWED_DEPENDENCIES_SIZE_GB * GIGABYTE):
            printer.safe_print(
                f"{ERROR_MESSAGE_PREFIX} The total size of the downloaded dependencies exceeds the max allowed limit of {MAX_ALLOWED_DEPENDENCIES_SIZE_GB}GB. Please reduce the total number / size of dependencies and try again!",
                file=sys.stderr,
            )
            sys.exit(1)

        printer.safe_print("\n⏳ Uploading compressed wheels in parts to S3. This may take a few seconds.....")
        environment_id = id_helper.IdHelper.generate_string_id()
        try:
            location = _upload_dependencies(
                source_path=download_wheels_dir, environment_id=environment_id, verbose=verbose
            )
        except ValueError as e:
            printer.safe_print(f"{ERROR_MESSAGE_PREFIX} Unable to upload dependencies - {e}", file=sys.stderr)
            sys.exit(1)

        req = CreateRemoteEnvironmentRequest(
            name=name,
            id=environment_id,
            description=description,
            python_version=python_version,
            s3_wheels_location=location,
            requirements=requirements_path.read_text(),
            resolved_requirements=resolved_requirements_path.read_text(),
            transform_runtime_version=tecton_runtime_version,
            rift_materialization_runtime_version=tecton_rift_version,
            sdk_version=version.get_semantic_version(),
        )
        return metadata_service.instance().CreateRemoteEnvironment(req)


def _validate_and_get_dependencies(lock_file_path: Path) -> EnvironmentDependencies:
    with open(lock_file_path, "r") as lock_file:
        dependencies_data = json.load(lock_file)
    dependencies = EnvironmentDependencies(dependencies_data)
    tecton_runtime_version = dependencies.get_version(dependency_name=TECTON_TRANSFORM_RUNTIME_PACKAGE)
    tecton_rift_version = dependencies.get_version(dependency_name=TECTON_RIFT_MATERIALIZATION_RUNTIME_PACKAGE)

    if tecton_rift_version is not None:
        rift_extras = dependencies.get_dependency_extras(TECTON_RIFT_MATERIALIZATION_RUNTIME_PACKAGE)
        if "rift-materialization" not in rift_extras:
            printer.safe_print(
                f"{ERROR_MESSAGE_PREFIX} `rift-materialization` extra must be included for package `tecton` to support Rift materialization (tecton[rift-materialization]==x.x.x)",
                file=sys.stderr,
            )
            sys.exit(1)

    if not tecton_runtime_version and not tecton_rift_version:
        # TODO (vitaly): update the doc link for more information on custom Rift materialization envs
        printer.safe_print(
            f"{ERROR_MESSAGE_PREFIX} Please include at least one of the supporting Tecton libraries:\n"
            f"💡  `tecton-runtime` package (https://pypi.org/project/tecton-runtime) to support On Demand environments\n"
            f"💡  `tecton[rift-materialization]` package (https://pypi.org/project/tecton) to support Rift materialization environments",
            "\nFor more information, please see: https://docs.tecton.ai/docs/defining-features/feature-views/on-demand-feature-view/on-demand-feature-view-environments/custom-on-demand-feature-view-environments",
            file=sys.stderr,
        )
        sys.exit(1)
    return dependencies


def _run_dependency_resolution(
    requirements_path: Path, resolved_requirements_directory: Path, python_version: str, verbose: bool = False
) -> Tuple[Path, Path]:
    printer.safe_print(
        f"\n⏳ Resolving dependencies for Python {python_version} and architecture {DEFAULT_ARCHITECTURE}. This may take a few seconds....."
    )
    lock_output_path = resolved_requirements_directory / "lock.json"
    resolved_requirements_path = resolved_requirements_directory / RESOLVED_REQUIREMENTS_FILENAME
    resolve_dependencies(
        python_version=python_version,
        requirements_path=requirements_path,
        lock_output_path=lock_output_path,
        resolved_requirements_path=resolved_requirements_path,
        timeout_seconds=DEPENDENCY_RESOLUTION_TIMEOUT_SECONDS,
        verbose=verbose,
    )
    return resolved_requirements_path, lock_output_path


def _check_environment_usage(environment_id: str):
    request = GetDependentFeatureServicesRequest(environment_id=environment_id)
    response = metadata_service.instance().GetDependentFeatureServices(request)
    if response.dependent_feature_services:
        error_message = f"{ERROR_MESSAGE_PREFIX} Cannot delete environment as it is configured as the `on_demand_environment` for the following Feature Service(s). Please update the `on_demand_environment` and try again\n"
        printer.safe_print(error_message, file=sys.stderr)
        _display_dependent_feature_services(response.dependent_feature_services)
        sys.exit(1)


def _delete_environment(environment_id: str):
    try:
        req = DeleteRemoteEnvironmentsRequest()
        req.ids.append(environment_id)
        return metadata_service.instance().DeleteRemoteEnvironments(req)
    except PermissionError as _:
        printer.safe_print(
            "⛔ The user is not authorized to perform environment deletion. Please reach out to your Admin to complete this action.",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        printer.safe_print(f"⛔ Failed to delete environment: {e}", file=sys.stderr)
        sys.exit(1)


def _list_environments(environment_identifier: Optional[EnvironmentIdentifier] = None):
    try:
        req = ListRemoteEnvironmentsRequest()
        response = metadata_service.instance().ListRemoteEnvironments(req)
        if not environment_identifier:
            return response.remote_environments
        if environment_identifier.id:
            environments = [env for env in response.remote_environments if environment_identifier.id in env.id]
        else:
            # Look for an exact match. If there are no exact matches, we will return all substring matches
            environments = [env for env in response.remote_environments if environment_identifier.name == env.name]
            if not environments:
                environments = [env for env in response.remote_environments if environment_identifier.name in env.name]

        return environments

    except Exception as e:
        printer.safe_print(f"Failed to fetch environments: {e}", file=sys.stderr)
        sys.exit(1)


def _timestamp_to_string(value: timestamp_pb2.Timestamp) -> str:
    t = datetime.fromtimestamp(value.ToSeconds())
    return t.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")


def _upload_dependencies(source_path: Path, environment_id: str, verbose: bool) -> str:
    """Upload dependencies from the specified source path to S3.
    Args:
        source_path (str): The path to the dependencies to upload.
        environment_id (str): The ID of the environment.
        verbose (bool): Activates verbose logging
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output_zip_file = Path(tmpdir) / "wheels.zip"
        if verbose:
            printer.safe_print(f"{DEBUG_MESSAGE_PREFIX} Zipping dependencies at {output_zip_file}")

        shutil.make_archive(str(output_zip_file.with_suffix("")), "zip", str(source_path))
        file_size = output_zip_file.stat().st_size

        if verbose:
            printer.safe_print(f"{DEBUG_MESSAGE_PREFIX} Initiating Multi-Part Upload")
        start_request = StartPackagesUploadRequest(environment_id=environment_id)
        start_response = metadata_service.instance().StartPackagesUpload(start_request)

        upload_id = start_response.upload_info.s3_upload_info.upload_id
        upload_parts = _upload_file_in_parts(
            file_size=file_size,
            upload_id=upload_id,
            environment_id=environment_id,
            output_zip_file=output_zip_file,
        )

        complete_request = CompletePackagesUploadRequest(
            upload_info=RemoteEnvironmentUploadInfo(
                environment_id=environment_id,
                s3_upload_info=S3UploadInfo(upload_id=upload_id, upload_parts=upload_parts),
            )
        )
        complete_response = metadata_service.instance().CompletePackagesUpload(complete_request)
        location = complete_response.storage_location
        printer.safe_print("✅ Successfully uploaded dependencies")
        return location


def _upload_file_in_parts(
    file_size: int, upload_id: str, environment_id: str, output_zip_file: Path
) -> List[S3UploadPart]:
    """Upload a file in parallel, dividing it into parts.
    Args:
        file_size (int): The size of the file in bytes.
        upload_id (str): A unique identifier for the file upload, returned by S3.
        environment_id (str): The ID of the environment.
        output_zip_file (str): The path to the file to upload.
    Returns:
        list: A list of upload part results.
    """
    # Calculate all parts for multi part upload
    part_data_list = get_upload_parts(file_size=file_size)
    with ThreadPoolExecutor(DEFAULT_MAX_WORKERS_THREADS) as executor:
        upload_futures = [
            executor.submit(
                _upload_part,
                upload_part=part_data,
                parent_upload_id=upload_id,
                environment_id=environment_id,
                dependency_file_path=output_zip_file,
            )
            for part_data in part_data_list
        ]
        with tqdm(total=len(part_data_list), desc="Upload progress", ncols=100) as pbar:
            for future in as_completed(upload_futures):
                # Increment the tqdm progress bar whenever a future is done
                if future.result():
                    pbar.update(1)

        return [future.result() for future in upload_futures]


def get_upload_parts(file_size: int) -> List[UploadPart]:
    """
    Calculate UploadPart for each part of a file to be uploaded, given total file size.
    It considers the DEFAULT_UPLOAD_PART_SIZE_MB as the maximum size of each part.
    Args:
        file_size (int): The total size of the file being uploaded in bytes.
    Returns:
        List[UploadPart]: An list of UploadPart representing all parts to be uploaded with its part number,
                    starting offset, and size in bytes.
    """
    total_parts = _calculate_part_count(file_size, DEFAULT_UPLOAD_PART_SIZE_MB)
    chunk_size = DEFAULT_UPLOAD_PART_SIZE_MB * MEGABYTE
    upload_parts = []
    for i in range(1, total_parts + 1):
        offset = chunk_size * (i - 1)
        bytes_remaining = file_size - offset
        # Adjust the size for the last part if the remaining bytes are less than the DEFAULT_UPLOAD_PART_SIZE_MB
        current_chunk_size = chunk_size if bytes_remaining > chunk_size else bytes_remaining
        upload_parts.append(UploadPart(part_number=i, offset=offset, part_size=current_chunk_size))
    return upload_parts


def _get_directory_size(directory: Path) -> int:
    """
    Compute the size of a directory in bytes.
    Args:
        directory (Path): The directory path for which to compute the size.
    Returns:
        int: The size of the directory in bytes.
    """
    return sum(f.stat().st_size for f in directory.rglob("*") if f.is_file())


def _calculate_part_count(file_size: int, part_size_mb: int) -> int:
    """Calculate the number of parts the file will be divided into for uploading.
    Args:
        file_path (str): The path to the file to upload.
        part_size_mb (int): The size of each part in megabytes.
    Returns:
        int: The total number of parts.
    """
    chunk_size = part_size_mb * 1024 * 1024
    return int(math.ceil(file_size / chunk_size))


def _upload_part(
    upload_part: UploadPart,
    parent_upload_id: str,
    environment_id: str,
    dependency_file_path: str,
):
    """Upload a part of a file.
    Args:
        upload_part (UploadPart): The part to upload.
        parent_upload_id (str): The ID of the parent upload.
        environment_id (str): The ID of the environment.
        dependency_file_path (str): The path to the file to upload.
    Returns:
        S3UploadPart: An object representing the uploaded part.
    """
    request = GetPackagesUploadUrlRequest(
        environment_id=environment_id,
        upload_part=ObjectStoreUploadPart(
            s3_upload_part=S3UploadPart(parent_upload_id=parent_upload_id, part_number=upload_part.part_number)
        ),
    )
    response = metadata_service.instance().GetPackagesUploadUrl(request)
    signed_url = response.upload_url

    with open(dependency_file_path, "rb") as fp:
        fp.seek(upload_part.offset)
        file_data = fp.read(upload_part.part_size)
        response = http.session().put(signed_url, data=file_data)
        if response.ok:
            e_tag = response.headers["ETag"]
            return S3UploadPart(part_number=upload_part.part_number, e_tag=e_tag, parent_upload_id=parent_upload_id)
        else:
            msg = f"Upload failed with status {response.status_code} and error {response.text}"
            raise ValueError(msg)


def _display_requirements(
    requirements_path: Optional[Path] = None, requirements_str: Optional[str] = None, verbose: bool = False
):
    """
    Display requirements from a requirements.txt file after removing hashes from each line, if exists.
    Args:
        requirements_path (Path): Path to the requirements file.
        requirements_str (str): Contents of a requirements.txt file
        verbose (bool): If enabled, print debug information
    """
    cleaned_lines = []
    if requirements_path is not None:
        with requirements_path.open("r") as file:
            cleaned_lines = [line.strip() for line in file.readlines()]
    elif requirements_str is not None:
        cleaned_lines = [line.strip() for line in requirements_str.split("\n")]

    if not verbose:
        # Skip hashes and emptylines
        cleaned_lines = [line.rstrip("\\").strip() for line in cleaned_lines if line and not line.startswith("--hash")]
    printer.safe_print("\n".join(cleaned_lines))
