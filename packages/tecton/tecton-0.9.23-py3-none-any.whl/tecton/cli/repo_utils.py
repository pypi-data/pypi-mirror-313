import importlib
import inspect
import logging
import os
import re
import site
import sys
from pathlib import Path
from types import ModuleType
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple

import yaspin.spinners

from tecton.cli import cli_utils
from tecton.cli import printer
from tecton.cli import repo_config as cli__repo_config
from tecton.cli.error_utils import pretty_error
from tecton.framework import base_tecton_object
from tecton.framework import repo_config as framework__repo_config
from tecton_core import repo_file_handler
from tecton_core.errors import TectonAPIInaccessibleError
from tecton_core.errors import TectonValidationError
from tecton_proto.args import repo_metadata_pb2
from tecton_proto.common import id_pb2


# Matches frame strings such as "<string>"
SKIP_FRAME_REGEX = re.compile("\<.*\>")

logger = logging.getLogger(__name__)


# TODO (ajeya): Move this to a more appropriate location closer to framework code
def construct_fco_source_info(fco_id: id_pb2.Id) -> repo_metadata_pb2.SourceInfo:
    """Get the SourceInfo (file name and line number) for an FCO.

    How it works:
    - This function assumed it is being called from the constructor of an FCO
    - inspect.stack() returns the call stack (starting with this function)
    - Walk up the stack frames until the first file within a tecton repo (a child of .tecton) is found
    - The first valid tecton repo file is considered the filename of the FCO.
    """
    from tecton_core.repo_file_handler import _maybe_get_repo_root

    source_info = repo_metadata_pb2.SourceInfo(fco_id=fco_id)
    repo_root = _maybe_get_repo_root()
    if not repo_root:
        return source_info

    # 'getsitepackages' and 'getusersitepackages' are not avaiable in some python envs such as EMR notebook with
    # Python 3.7.
    if not (hasattr(site, "getsitepackages") and hasattr(site, "getusersitepackages")):
        logger.warn(
            "Python 'site' pakcage doesn't contain 'getsitepackages' or 'getusersitepackages' methods. SourceInfo is not going to be populated."
        )
        return source_info

    excluded_site_pkgs = [*site.getsitepackages(), site.getusersitepackages()]

    frames = inspect.stack()
    repo_root_path = Path(repo_root)
    for frame in frames:
        if SKIP_FRAME_REGEX.match(frame.frame.f_code.co_filename) is not None:
            continue
        frame_path = Path(frame.frame.f_code.co_filename).resolve()
        if not frame_path.exists():
            continue
        if any(pkg in frame.frame.f_code.co_filename for pkg in excluded_site_pkgs):
            # This filtering is needed in case `tecton` is installed using a virtual
            # environment that's created *inside* the repo root. Without this check,
            # Tecton SDK files would incorrectly be considered a valid repo files
            # and would be listed as the FCO's source filename.
            continue
        if repo_root_path in frame_path.parents:
            rel_filename = frame_path.relative_to(repo_root_path)
            source_info.source_lineno = str(frame.lineno)
            source_info.source_filename = str(rel_filename)
            break
    return source_info


def _import_module_with_pretty_errors(
    file_path: Path,
    module_path: str,
    py_files: List[Path],
    repo_root: Path,
    debug: bool,
    before_error: Callable[[], None],
) -> ModuleType:
    from pyspark.sql.utils import AnalysisException

    try:
        module = importlib.import_module(module_path)
        if Path(module.__file__) != file_path:
            before_error()
            relpath = file_path.relative_to(repo_root)
            printer.safe_print(
                f"Python module name {cli_utils.bold(module_path)} ({relpath}) conflicts with module {module_path} from {module.__file__}. Please use a different name.",
                file=sys.stderr,
            )
            sys.exit(1)

        return module
    except AnalysisException as e:
        before_error()
        pretty_error(
            Path(file_path),
            py_files,
            exception=e,
            repo_root=repo_root,
            error_message="Analysis error",
            error_details=e.desc,
            debug=debug,
        )
        sys.exit(1)
    except TectonValidationError as e:
        before_error()
        pretty_error(Path(file_path), py_files, exception=e, repo_root=repo_root, error_message=e.args[0], debug=debug)
        sys.exit(1)
    except SyntaxError as e:
        before_error()
        details = None
        if e.text and e.offset:
            details = e.text + (" " * e.offset) + "^^^"
        pretty_error(
            Path(file_path),
            py_files,
            exception=e,
            repo_root=repo_root,
            error_message=e.args[0],
            error_details=details,
            debug=debug,
        )
        sys.exit(1)
    except TectonAPIInaccessibleError as e:
        before_error()
        printer.safe_print("Failed to connect to Tecton server at", e.args[1], ":", e.args[0])
        sys.exit(1)
    except Exception as e:
        before_error()
        pretty_error(Path(file_path), py_files, exception=e, repo_root=repo_root, error_message=e.args[0], debug=debug)
        sys.exit(1)


def collect_top_level_objects(
    py_files: List[Path], repo_root: Path, debug: bool, pretty_errors: bool
) -> List[base_tecton_object.BaseTectonObject]:
    modules = [cli_utils.py_path_to_module(p, repo_root) for p in py_files]

    with printer.safe_yaspin(yaspin.spinners.Spinners.earth, text="Importing feature repository modules") as sp:
        for file_path, module_path in zip(py_files, modules):
            sp.text = f"Processing feature repository module {module_path}"

            if pretty_errors:
                module = _import_module_with_pretty_errors(
                    file_path=file_path,
                    module_path=module_path,
                    py_files=py_files,
                    repo_root=repo_root,
                    debug=debug,
                    before_error=lambda: sp.fail(printer.safe_string("⛔")),
                )
            else:
                module = importlib.import_module(module_path)

        num_modules = len(modules)
        sp.text = f"Imported {num_modules} Python {cli_utils.plural(num_modules, 'module', 'modules')} from the feature repository"
        sp.ok(printer.safe_string("✅"))

        return list(base_tecton_object._LOCAL_TECTON_OBJECTS)


def get_tecton_objects(
    debug: bool, specified_repo_config: Optional[Path]
) -> Tuple[List[base_tecton_object.BaseTectonObject], str, List[Path], Path]:
    repo_file_handler.ensure_prepare_repo()
    repo_files = repo_file_handler.repo_files()
    repo_root = repo_file_handler.repo_root()

    repo_config = _maybe_load_repo_config_or_default(specified_repo_config)

    py_files = [p for p in repo_files if p.suffix == ".py"]
    os.chdir(Path(repo_root))

    top_level_objects = collect_top_level_objects(py_files, repo_root=Path(repo_root), debug=debug, pretty_errors=True)

    return top_level_objects, repo_root, repo_files, repo_config


def _maybe_load_repo_config_or_default(repo_config_path: Optional[Path]) -> Path:
    if repo_config_path is None:
        repo_config_path = cli__repo_config.get_default_repo_config_path()

    if framework__repo_config.get_repo_config() is None:
        # Load the repo config. The repo config may have already been loaded if tecton objects were collected multiple
        # times, e.g. during `tecton plan` the objects are collected for tests and then the plan.
        cli__repo_config.load_repo_config(repo_config_path)

    return repo_config_path
