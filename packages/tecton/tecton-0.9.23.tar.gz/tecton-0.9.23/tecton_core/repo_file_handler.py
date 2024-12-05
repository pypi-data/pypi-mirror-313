import sys
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Iterable
from typing import List
from typing import Optional
from typing import Set

from tecton_core import conf


# TODO(brian): refactor functions/callers here to use the RepoData class and
# remove these duplicative helpers.


@dataclass
class RepoData:
    # paths and file set are different representations of the same data
    root: str
    paths: List[Path] = field(default_factory=list)
    file_set: Set[str] = field(default_factory=set)


_repo_data: Optional[RepoData] = None


def get_repo_data() -> Optional[RepoData]:
    return _repo_data


def set_repo_data(repo_data: RepoData) -> None:
    global _repo_data
    _repo_data = repo_data


# Prepare a repo for tecton objects to be processed.
# If file_in_repo is not set, expects the current directory to be inside the feature repo.
def ensure_prepare_repo(file_in_repo: Optional[str] = None) -> None:
    repo_data = get_repo_data()
    if repo_data:
        # repo is already prepared
        return
    root = _maybe_get_repo_root(file_in_repo)
    if root is None:
        msg = "Feature repository root not found. Run `tecton init` to set it."
        raise Exception(msg)
    paths = get_repo_files(root)
    file_set = {str(f) for f in paths}
    set_repo_data(RepoData(paths=paths, file_set=file_set, root=root))


def repo_files() -> List[Path]:
    repo_data = get_repo_data()
    if repo_data is None:
        msg = "Repo is not prepared"
        raise Exception(msg)
    return repo_data.paths


def repo_files_set() -> Set[str]:
    repo_data = get_repo_data()
    if repo_data is None:
        msg = "Repo is not prepared"
        raise Exception(msg)
    return repo_data.file_set


def repo_root() -> str:
    repo_data = get_repo_data()
    if repo_data is None:
        msg = "Repo is not prepared"
        raise Exception(msg)
    return repo_data.root


def _fake_init_for_testing(root: str = "") -> None:
    fake_root = Path(root)
    set_repo_data(RepoData(paths=[fake_root], file_set={str(fake_root)}, root=str(fake_root)))


# Finds the repo root of a given python file (a parent directory containing ".tecton")
# If a file is not passed in, searches the current directory's parents.
# Returns None if the root is not found
def _maybe_get_repo_root(file_in_repo: Optional[str] = None) -> Optional[str]:
    repo_data = get_repo_data()
    if repo_data is not None and repo_data.root:
        return repo_data.root

    if file_in_repo is None:
        d = Path().resolve()
    else:
        d = Path(file_in_repo)

    while d.parent != d and d != Path.home():
        tecton_cfg = d / Path(".tecton")
        if tecton_cfg.exists():
            # NOTE: we are not caching this since traversing up the file system
            # should be quick and calls to this should be infrequent.
            #
            # Previous implementations did cache this in our `_repo_data` and
            # that caused a bug for `tecton test`.
            return str(d)
        d = d.parent
    return None


def is_file_in_a_tecton_repo(file: str) -> bool:
    """Determines if the file is in a Tecton repo, i.e. a parent directory contains a .tecton file."""
    d = Path(file)
    while d.parent != d and d != Path.home():
        tecton_cfg = d / Path(".tecton")
        if tecton_cfg.exists():
            return True
        d = d.parent
    return False


def _get_ignored_files(repo_root: Path) -> Set[Path]:
    import pathspec

    ignorefile = repo_root / Path(".tectonignore")
    if not ignorefile.exists():
        return set()

    with open(ignorefile, "r") as f:
        spec = pathspec.PathSpec.from_lines("gitwildmatch", f)
        return {repo_root / file_name for file_name in spec.match_tree(str(repo_root))}


def get_repo_files(root: str, suffixes: Iterable[str] = (".py", ".yml", "yaml")) -> List[Path]:
    root_path = Path(root)
    repo_files = [p.resolve() for p in root_path.glob("**/*") if p.suffix in suffixes]

    # Ignore virtualenv directory if any, typically you'd have /some/path/bin/python as an
    # interpreter, so we want to skip anything under /some/path/
    if sys.executable:
        python_dir = Path(sys.executable).parent.parent

        # we might be dealing with virtualenv
        if root_path.resolve() in python_dir.parents:
            repo_files = [p for p in repo_files if python_dir not in p.parents]

    # NOTE: we added this behind a flag so that customers can disable this behavior if their environment
    # places their repo in a hidden directory as part of its execution. This happened with a customer
    # that used Bazel which configured the repo under the `~/.cache/bazel/...` directory.
    # https://tecton.atlassian.net/browse/CS-3509
    if conf.get_bool("TECTON_REPO_IGNORE_ALL_HIDDEN_DIRS"):
        # Filter out files under hidden dirs starting with "/." for PosixPath or "\." for WindowsPath
        repo_files = list(filter(lambda p: "/." not in str(p) and "\." not in str(p), repo_files))

    # Filter out files that match glob expressions in .tectonignore
    ignored_files = _get_ignored_files(root_path)
    filtered_files = [p for p in repo_files if p not in ignored_files]

    return filtered_files
