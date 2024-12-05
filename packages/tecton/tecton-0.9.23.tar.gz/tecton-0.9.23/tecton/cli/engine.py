import io
import os
import platform
import sys
import tarfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

import click
import requests
from google.protobuf import json_format
from yaspin.spinners import Spinners

import tecton
from tecton import tecton_context
from tecton._internals import metadata_service
from tecton._internals.analytics import StateUpdateEventMetrics
from tecton._internals.analytics import StateUpdateResult
from tecton._internals.utils import plural
from tecton.cli import cli_utils
from tecton.cli import printer
from tecton.cli import repo_utils
from tecton.cli.command import TectonCommand
from tecton.cli.engine_renderer import PlanRenderingClient
from tecton.cli.error_utils import format_server_errors
from tecton.cli.repo_config import DEFAULT_REPO_CONFIG_NAME
from tecton.cli.test import run_tests
from tecton.cli.workspace_utils import WorkspaceType
from tecton.framework import base_tecton_object
from tecton_core import http
from tecton_core.errors import TectonAPIValidationError
from tecton_core.errors import TectonInternalError
from tecton_core.errors import TectonNotFoundError
from tecton_core.id_helper import IdHelper
from tecton_proto.args import fco_args_pb2
from tecton_proto.args import repo_metadata_pb2
from tecton_proto.data import state_update_pb2
from tecton_proto.metadataservice import metadata_service_pb2


class EngineCommand(TectonCommand):
    def __init__(
        self,
        *args,
        apply: bool,
        upgrade_all: bool = False,
        destroy: bool = False,
        allows_suppress_recreates: bool = False,
        has_plan_id: bool = False,
        **kwargs,
    ):
        @click.pass_context
        def callback(
            ctx,
            yes,
            json_out,
            suppress_warnings,
            workspace,  # Not used but it needs to be here to match params list.
            config: Optional[Path],
            suppress_recreates=False,
            plan_id=None,
            skip_tests=None,
        ):
            args = EngineArgs(
                skip_tests=skip_tests,
                json_out=json_out,
                no_safety_checks=yes,
                suppress_warnings=suppress_warnings,
                debug=cli_utils.get_debug(ctx),
                repo_config_path=config,
            )

            assert not (plan_id and suppress_recreates), (
                "The flag --suppress-recreates is only used when computing a new plan. If the plan passed "
                "in using --plan-id was already computed using --suppress-recreates, that behavior persists "
                "as part of the plan."
            )

            if plan_id:
                args.plan_id = plan_id
            if suppress_recreates:
                args.suppress_recreates = suppress_recreates

            return run_engine(args, apply=apply, upgrade_all=upgrade_all, destroy=destroy)

        params = [
            click.Option(
                ["--yes", "-y"],
                is_flag=True,
                default=False,
                help="Skip all confirmation prompts.",
            ),
            click.Option(
                ["--json-out"],
                default="",
                help="Output the tecton state update diff (as JSON) to the file path provided.",
            ),
            click.Option(
                ["--suppress-warnings"],
                is_flag=True,
                default=False,
                help="Disable tecton plan linting warnings.",
            ),
            click.Option(
                ["--workspace"],
                default=None,
                type=WorkspaceType(),
                help="Name of the target workspace that tecton state update request applies to.",
            ),
            click.Option(
                ["--config"],
                help="Path to the repo config yaml file. Defaults to the repo.yaml file at the Tecton repo root.",
                default=None,
                type=click.Path(exists=True, dir_okay=False, path_type=Path, readable=True),
            ),
        ]

        if has_plan_id:
            params.append(
                click.Option(["--plan-id"], default=None, type=str, help="Id of a previously computed plan to apply.")
            )
        if not destroy:
            params.append(
                click.Option(
                    ["--skip-tests/--no-skip-tests"],
                    default=False,
                    help="Disable running tests.",
                )
            )
        if allows_suppress_recreates:
            params.append(
                click.Option(
                    ["--suppress-recreates"],
                    is_flag=True,
                    default=False,
                    help="Force suppression of all recreates into in-place updates.",
                ),
            )

        super().__init__(*args, callback=callback, params=params, uses_workspace=True, **kwargs)


# TODO: This class was created to match the old style arg parse struct when we were migrating to click to avoid having
# do a deep refactoring of the code that depends on it. It should be replaced.
@dataclass
class EngineArgs:
    skip_tests: bool
    no_safety_checks: bool
    json_out: str
    suppress_warnings: bool
    debug: bool
    repo_config_path: Optional[Path]


def update_tecton_state(
    objects: List[base_tecton_object.BaseTectonObject],
    repo_files: List[Path],
    repo_config: Optional[Path],
    repo_root: Optional[str],
    apply,
    debug,
    interactive,
    upgrade_all: bool,
    workspace_name: str,
    suppress_warnings: bool = False,
    suppress_recreates: bool = False,
    json_out_path: Optional[Path] = None,
    timeout_seconds=90 * 60,
    plan_id: Optional[str] = None,
    no_color: bool = False,
) -> StateUpdateResult:
    # In debug mode we compute the plan synchronously, do not save it in the database, and do not allow to apply it.
    # Primary goal is allowing local development/debugging plans against remote clusters in read-only mode.
    assert not (debug and apply), "Cannot apply in debug mode"
    json_out = json_out_path is not None

    if apply and plan_id:
        # Applying an existing plan, so skip preparing args.
        state_id = IdHelper.from_string(plan_id)
        query_state_update_request = metadata_service_pb2.QueryStateUpdateRequestV2(
            state_id=state_id,
            workspace=workspace_name,
            no_color=no_color,
            json_output=json_out,
            suppress_warnings=suppress_warnings,
        )

        try:
            query_state_update_response = metadata_service.instance().QueryStateUpdateV2(query_state_update_request)
        except (
            TectonInternalError,
            TectonAPIValidationError,
        ) as e:
            printer.safe_print(e)
            return StateUpdateResult.from_error_message(str(e), suppress_recreates)

        if query_state_update_response.error:
            printer.safe_print(query_state_update_response.error)
            return StateUpdateResult.from_error_message(query_state_update_response.error, suppress_recreates)
        if len(query_state_update_response.validation_errors.errors) > 0:
            # Cannot pretty-print validation result using format_server_errors(), because collected local objects
            # might have changed since this plan was generated, so can't accurately match with this plan's FCOs.
            message = "Cannot apply plan because it had errors."
            printer.safe_print(message)
            return StateUpdateResult.from_error_message(message, suppress_recreates)

    else:
        with printer.safe_yaspin(Spinners.earth, text="Collecting local feature declarations") as sp:
            fco_args, repo_source_info = _get_declared_fco_args(objects)
            sp.ok(printer.safe_string("✅"))

        new_state_update_request = metadata_service_pb2.NewStateUpdateRequestV2(
            request=state_update_pb2.StateUpdateRequest(
                workspace=workspace_name,
                upgrade_all=upgrade_all,
                sdk_version=tecton.version.get_semantic_version(),
                fco_args=fco_args,
                repo_source_info=repo_source_info,
                suppress_recreates=suppress_recreates,
            ),
            no_color=no_color,
            json_output=json_out,
            suppress_warnings=suppress_warnings,
            blocking_dry_run_mode=debug,
            enable_eager_response=not debug,
        )

        server_side_msg_prefix = "Performing server-side feature validation"
        with printer.safe_yaspin(Spinners.earth, text=f"{server_side_msg_prefix}: Initializing.") as sp:
            try:
                new_state_update_response = metadata_service.instance().NewStateUpdateV2(new_state_update_request)

                if new_state_update_response.HasField("signed_url_for_repo_upload"):
                    _upload_files(
                        repo_files, repo_config, repo_root, new_state_update_response.signed_url_for_repo_upload
                    )
                if new_state_update_response.HasField("eager_response"):
                    query_state_update_response = new_state_update_response.eager_response
                else:
                    seconds_slept = 0
                    query_state_update_request = metadata_service_pb2.QueryStateUpdateRequestV2(
                        state_id=new_state_update_response.state_id,
                        workspace=workspace_name,
                        no_color=no_color,
                        json_output=json_out,
                        suppress_warnings=suppress_warnings,
                    )
                    while True:
                        query_state_update_response = metadata_service.instance().QueryStateUpdateV2(
                            query_state_update_request
                        )
                        if query_state_update_response.latest_status_message:
                            sp.text = f"{server_side_msg_prefix}: {query_state_update_response.latest_status_message}"
                        if query_state_update_response.ready:
                            break
                        seconds_to_sleep = 5
                        time.sleep(seconds_to_sleep)
                        seconds_slept += seconds_to_sleep
                        if seconds_slept > timeout_seconds:
                            sp.fail(printer.safe_string("⛔"))
                            printer.safe_print("Validation timed out.")
                            return StateUpdateResult.from_error_message("Validation timed out.", suppress_recreates)

                if query_state_update_response.error:
                    sp.fail(printer.safe_string("⛔"))
                    printer.safe_print(query_state_update_response.error)
                    return StateUpdateResult.from_error_message(query_state_update_response.error, suppress_recreates)
                validation_errors = query_state_update_response.validation_errors.errors
                if len(validation_errors) > 0:
                    sp.fail(printer.safe_string("⛔"))
                    format_server_errors(validation_errors, objects, repo_root)
                    return StateUpdateResult.from_error_message(str(validation_errors), suppress_recreates)
                sp.ok(printer.safe_string("✅"))
            except (TectonInternalError, TectonAPIValidationError, TectonNotFoundError) as e:
                sp.fail(printer.safe_string("⛔"))
                printer.safe_print(e)
                return StateUpdateResult.from_error_message(str(e), suppress_recreates)

        state_id = new_state_update_response.state_id

    plan_rendering_client = PlanRenderingClient(query_state_update_response)

    if not plan_rendering_client.has_diffs():
        plan_rendering_client.print_empty_plan()
    else:
        plan_rendering_client.print_plan()

        if apply:
            plan_rendering_client.print_apply_warnings()
            if interactive:
                cli_utils.confirm_or_exit(f'Are you sure you want to apply this plan to: "{workspace_name}"?')

            apply_request = metadata_service_pb2.ApplyStateUpdateRequest(state_id=state_id)
            metadata_service.instance().ApplyStateUpdate(apply_request)

            num_fcos = plan_rendering_client.num_fcos_changed
            printer.safe_print(
                f'🎉 Done! Applied changes to {num_fcos} {plural(num_fcos, "object", "objects")} in workspace "{workspace_name}".'
            )

    if json_out_path:
        repo_diff_summary = plan_rendering_client.get_json_plan_output()
        json_out_path.parent.mkdir(parents=True, exist_ok=True)
        json_out_path.write_text(repo_diff_summary)

    return StateUpdateResult(
        state_update_event_metrics=StateUpdateEventMetrics(
            num_total_fcos=len(objects),
            suppress_recreates=suppress_recreates,
            json_out=(json_out_path is not None),
            error_message=None,
            num_fcos_changed=query_state_update_response.successful_plan_output.num_fcos_changed,
            num_warnings=query_state_update_response.successful_plan_output.num_warnings,
        ),
        success_response=query_state_update_response,
    )


def run_engine(args: EngineArgs, apply: bool = False, destroy=False, upgrade_all=False) -> StateUpdateResult:
    cli_utils.check_version()

    # Resolve the json_out_filename prior to running `get_tecton_objects(...)` so
    # that relative directories in the file name are supported (`get_tecton_objects`
    # changes the working directory).
    json_out_path = None
    if args.json_out:
        json_out_path = Path(args.json_out).resolve()

    # Must use hasattr instead of args.plan_id, because only `apply` has the plan_id arg, but this
    # code path is also used by `plan`, `destroy`, and `upgrade`, which will fail on args.plan_id
    plan_id = None
    if hasattr(args, "plan_id"):
        plan_id = args.plan_id
    suppress_recreates = False
    if hasattr(args, "suppress_recreates") and args.suppress_recreates:
        suppress_recreates = True

    if destroy or plan_id:
        # There is no need to run tests when destroying a repo or when a plan_id is provided.
        top_level_objects: List[base_tecton_object.BaseTectonObject] = []
        repo_root = None
        repo_files: List[Path] = []
        repo_config = None
    else:
        top_level_objects, repo_root, repo_files, repo_config = repo_utils.get_tecton_objects(
            args.debug, args.repo_config_path
        )

        if args.skip_tests == False:
            run_tests(args.debug, args.repo_config_path)

    # When using server-side plan rendering, use no colors on Windows
    # or if NO_COLOR is set
    no_color = platform.system() == "Windows" or cli_utils.no_color_convention()

    return update_tecton_state(
        objects=top_level_objects,
        apply=apply,
        debug=args.debug,
        interactive=not args.no_safety_checks,
        repo_files=repo_files,
        repo_config=repo_config,
        repo_root=repo_root,
        upgrade_all=upgrade_all,
        suppress_warnings=args.suppress_warnings,
        suppress_recreates=suppress_recreates,
        json_out_path=json_out_path,
        plan_id=plan_id,
        workspace_name=tecton_context.get_current_workspace(),
        no_color=no_color,
    )


def dump_local_state(objects: Sequence[base_tecton_object.BaseTectonObject]):
    fco_args, repo_source_info = _get_declared_fco_args(objects)
    request_plan = metadata_service_pb2.NewStateUpdateRequest(
        request=state_update_pb2.StateUpdateRequest(fco_args=fco_args, repo_source_info=repo_source_info)
    )
    printer.safe_print(json_format.MessageToJson(request_plan, including_default_value_fields=True))


# upload tar.gz of python files to url via PUT request
def _upload_files(repo_files: List[Path], repo_config: Optional[Path], repo_root, url: str):
    tar_bytes = io.BytesIO()
    with tarfile.open(fileobj=tar_bytes, mode="w|gz") as targz:
        for f in repo_files:
            targz.add(f, arcname=os.path.relpath(f, repo_root))
        if repo_config:
            # Always upload the repo config to the default repo path. We use the default path because (a) the repo
            # config may not be under the repo root and (b) using the default path simplifies restoring and re-applying.
            targz.add(repo_config, arcname=os.path.relpath(DEFAULT_REPO_CONFIG_NAME, repo_root))
    for _ in range(3):
        try:
            r = http.session().put(url, data=tar_bytes.getbuffer())
            if r.status_code != 200:
                # We will get 403 (forbidden) when the signed url expires.
                if r.status_code == 403:
                    printer.safe_print(
                        "\nUploading feature repo failed due to expired session. Please retry the command."
                    )
                else:
                    printer.safe_print(f"\nUploading feature repo failed with reason: {r.reason}")
                sys.exit(1)
            return
        except requests.RequestException as e:
            last_error = e
    raise SystemExit(last_error)


def _get_declared_fco_args(
    objects: Sequence[base_tecton_object.BaseTectonObject],
) -> Tuple[List[fco_args_pb2.FcoArgs], repo_metadata_pb2.FeatureRepoSourceInfo]:
    all_args = []
    repo_source_info = repo_metadata_pb2.FeatureRepoSourceInfo()

    for fco_obj in objects:
        all_args.append(fco_obj._build_args())
        repo_source_info.source_info.append(fco_obj._source_info)

    return all_args, repo_source_info


plan = EngineCommand(
    name="plan",
    apply=False,
    allows_suppress_recreates=True,
    help="Compare your local feature definitions with remote state and *show* the plan to bring them in sync.",
)


apply = EngineCommand(
    name="apply",
    apply=True,
    allows_suppress_recreates=True,
    has_plan_id=True,
    help="Compare your local feature definitions with remote state and *apply* local changes to the remote.",
)

upgrade = EngineCommand(
    name="upgrade",
    apply=True,
    upgrade_all=True,
    help="Upgrade remote feature definitions.",
    hidden=True,
)

destroy = EngineCommand(
    name="destroy",
    destroy=True,
    apply=True,
    help="Destroy all registered objects in this workspace.",
)
