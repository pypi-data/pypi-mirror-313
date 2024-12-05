from typing import Iterable

from typeguard import typechecked

from tecton import version as tecton_version
from tecton._internals import metadata_service
from tecton.framework import base_tecton_object
from tecton_core import errors
from tecton_core import id_helper
from tecton_proto.data import state_update_pb2
from tecton_proto.metadataservice import metadata_service_pb2
from tecton_proto.validation import validator_pb2


_INDENTATION_SIZE = 4


def _get_validation_prefix(obj: base_tecton_object.BaseTectonObject, indentation_level: int) -> str:
    indent_prefix = " " * (indentation_level * _INDENTATION_SIZE)
    return f"{indent_prefix}{obj.__class__.__name__} '{obj.name}': "


def print_validation_success(
    obj: base_tecton_object.BaseTectonObject,
    indentation_level: int,
) -> None:
    prefix = _get_validation_prefix(obj, indentation_level)
    # TODO(TEC-14146): Use the logging module instead of print statements.
    print(f"{prefix}Successfully validated.")


def print_validating_dependencies(
    obj: base_tecton_object.BaseTectonObject,
    dependencies: Iterable[base_tecton_object.BaseTectonObject],
    indentation_level: int,
) -> None:
    num_unvalidated_dependencies = len([dep for dep in dependencies if not dep._is_valid])
    if num_unvalidated_dependencies == 0:
        return

    prefix = _get_validation_prefix(obj, indentation_level)
    num_validated_dependencies = len(dependencies) - num_unvalidated_dependencies

    # Example validation messages:
    # - Validating 1 dependency
    # - Validating 1 of 2 dependencies (1 already validated)
    # - Validating 2 dependencies
    cache_message = f" ({num_validated_dependencies} already validated)" if num_validated_dependencies > 0 else ""
    num_total_dependencies = len(dependencies)
    count_string = f"{num_unvalidated_dependencies}"
    if num_validated_dependencies > 0:
        count_string += f" of {num_total_dependencies}"
    dependency_string = "dependency" if num_total_dependencies == 1 else "dependencies"
    # TODO(TEC-14146): Use the logging module instead of print statements.
    print(f"{prefix}Validating {count_string} {dependency_string}." + cache_message)


def print_deriving_schemas(
    obj: base_tecton_object.BaseTectonObject,
    indentation_level: int,
) -> None:
    prefix = _get_validation_prefix(obj, indentation_level)
    # TODO(TEC-14146): Use the logging module instead of print statements.
    print(f"{prefix}Deriving schema.")


def format_server_errors(
    tecton_object: base_tecton_object.BaseTectonObject, response: metadata_service_pb2.ValidateLocalFcoResponse
) -> str:
    # If there's a server side error, print that instead of the validation errors.
    if response.error:
        return f"{tecton_object.__class__.__name__} '{tecton_object.info.name}' failed validation: {response.error}"

    validation_errors = response.validation_result.errors
    if len(validation_errors) == 1:
        # If there is a single error, print the entire exception on one line. This is better UX in notebooks, which
        # often only show the first line of an exception in a preview.
        error = validation_errors[0]
        _check_error_matches_tecton_object(tecton_object, error)
        return f"{tecton_object.__class__.__name__} '{tecton_object.info.name}' failed validation: {error.message}"
    else:
        error_strings = [
            f"{tecton_object.__class__.__name__} '{tecton_object.info.name}' failed validation with the following errors:"
        ]
        for error in validation_errors:
            _check_error_matches_tecton_object(tecton_object, error)
            error_strings.append(error.message)
        return "\n".join(error_strings)


def _check_error_matches_tecton_object(
    tecton_object: base_tecton_object.BaseTectonObject, error: state_update_pb2.ValidationMessage
) -> None:
    error_object_id = id_helper.IdHelper.to_string(error.fco_refs[0].fco_id)

    if error_object_id != tecton_object.id:
        msg = f"Backend validation error returned wrong object id: {error_object_id}. Expected {tecton_object.id}"
        raise errors.TectonInternalError(msg)


@typechecked
def run_backend_validation_and_assert_valid(
    tecton_object: base_tecton_object.BaseTectonObject,
    validation_request: validator_pb2.ValidationRequest,
    indentation_level: int,
) -> None:
    """Run validation against the Tecton backend.

    Raises an exception if validation fails. Prints message if successful.
    """
    validation_local_fco_request = metadata_service_pb2.ValidateLocalFcoRequest(
        sdk_version=tecton_version.get_semantic_version(),
        validation_request=validation_request,
    )
    response = metadata_service.instance().ValidateLocalFco(validation_local_fco_request).response_proto
    if response.success:
        print_validation_success(tecton_object, indentation_level)
    else:
        raise errors.TectonValidationError(format_server_errors(tecton_object, response))
