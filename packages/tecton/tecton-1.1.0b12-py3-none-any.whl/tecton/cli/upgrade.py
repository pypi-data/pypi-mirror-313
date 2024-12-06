import re
from collections import defaultdict
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

import click

from tecton.cli.command import TectonCommand
from tecton.cli.printer import safe_print
from tecton.cli.upgrade_utils import BatchFeatureViewGuidance
from tecton.cli.upgrade_utils import DataSourceGuidance
from tecton.cli.upgrade_utils import EntityGuidance
from tecton.cli.upgrade_utils import FeatureTableGuidance
from tecton.cli.upgrade_utils import OnDemandFeatureViewGuidance
from tecton.cli.upgrade_utils import StreamFeatureViewGuidance
from tecton.framework.base_tecton_object import BaseTectonObject
from tecton.repo_utils import collect_top_level_objects
from tecton_core import conf
from tecton_core import repo_file_handler
from tecton_core.feature_definition_wrapper import FrameworkVersion


OBJECTS_TO_MIGRATE = {
    "BatchSource",
    "StreamSource",
    "PushSource",
    "Entity",
    "BatchFeatureView",
    "StreamFeatureView",
    "OnDemandFeatureView",
    "FeatureTable",
}

# if an object to migrate (Entity) is not in OBJECT_TO_MIGRATE_SECTION_OVERRIDE_NAME,
# it is stored as "Entity"
OBJECT_TO_MIGRATE_SECTION_OVERRIDE_NAME = {
    "BatchSource": "DataSource",
    "StreamSource": "DataSource",
    "PushSource": "DataSource",
}

OBJECT_TO_MIGRATE_TO_GUIDANCE_STEPS = [
    ("DataSource", DataSourceGuidance),
    ("Entity", EntityGuidance),
    ("BatchFeatureView", BatchFeatureViewGuidance),
    ("StreamFeatureView", StreamFeatureViewGuidance),
    ("OnDemandFeatureView", OnDemandFeatureViewGuidance),
    ("FeatureTable", FeatureTableGuidance),
]


def _fco_to_pretty_print(fco: str, count: int):
    if fco == "Entity":
        if count == 1:
            return "Entity"
        return "Entities"
    else:
        # converts camelcase to words with space
        # Ex: camelCase -> camel case
        pretty_string = re.sub(r"(?<!^)(?=[A-Z])", " ", fco)
        if count == 1:
            return pretty_string
        return f"{pretty_string}s"


def process_files(py_files: List[Path], repo_root: Path) -> Dict[str, List[Dict[str, any]]]:
    all_objects = defaultdict(list)

    # First, collect all FCOs
    fcos = collect_top_level_objects(py_files, repo_root, True)
    for tecton_object in fcos:
        fco_type = type(tecton_object).__name__
        key = (
            OBJECT_TO_MIGRATE_SECTION_OVERRIDE_NAME.get(fco_type, fco_type)
            if fco_type in OBJECTS_TO_MIGRATE
            else "Other"
        )
        all_objects[key].append(tecton_object)

    # Next, go through all files and collect non-FCO imports
    # TODO: handling "Other" imports and getting precision on them is kind of hard
    # How do you differentiate between an explicit transformation and one that is not explicit but baked into a FV?
    # Probably not worth all the extra effort; just say "Convert everything else".
    # Will revisit later.
    # with printer.safe_yaspin(yaspin.spinners.Spinners.earth, text="Analyzing feature repository modules") as sp:
    #     for file_path in py_files:
    #         sp.text = f"Processing {file_path.relative_to(repo_root)}"
    #         fcos = collect_non_fco_imports(file_path, repo_root, py_files)
    #         all_objects["Other"].extend(fcos)
    return dict(all_objects)


def print_migration_progress(all_objects: Dict[str, BaseTectonObject]):
    print("\nMigration Progress:")
    steps = [
        ("Data Sources", "DataSource"),
        ("Entities", "Entity"),
        ("Batch Feature Views", "BatchFeatureView"),
        ("Stream Feature Views", "StreamFeatureView"),
        ("On-Demand Feature Views", "OnDemandFeatureView"),
        ("Feature Tables", "FeatureTable"),
    ]

    for i, (step_name, obj_type) in enumerate(steps, 1):
        objects = all_objects.get(obj_type, [])
        total = len(objects)
        migrated = sum(1 for obj in objects if obj._framework_version == FrameworkVersion.FWV6)
        status = "✅" if migrated == total else "🟨" if migrated > 0 else "🚫"
        migrate_text = (
            f"{migrated}/{total} {_fco_to_pretty_print(obj_type, migrated)} migrated"
            if total > 0
            else f"No {_fco_to_pretty_print(obj_type, 0)} to migrate"
        )
        safe_print(f"  Step {i}: Migrate {step_name} - {status} ({migrate_text}).")
    safe_print(f"  Step {len(steps) + 1}: Migrate all other imports from `tecton.v09_compat` to `tecton`.")


def print_interactive_migration_guidance(all_objects: Dict[str, List[Dict[str, any]]], repo_root: str) -> None:
    step = 1
    index = 0

    while step <= len(OBJECT_TO_MIGRATE_TO_GUIDANCE_STEPS):
        obj_type, guildanceBuilder = OBJECT_TO_MIGRATE_TO_GUIDANCE_STEPS[step - 1]
        objects_to_migrate = sorted(
            [obj for obj in all_objects.get(obj_type, []) if obj._framework_version != FrameworkVersion.FWV6],
            key=lambda obj: (obj._source_info.source_filename, int(obj._source_info.source_lineno)),
        )

        if not objects_to_migrate:
            step += 1
            continue

        if index == 0:
            safe_print(f"\nStep {step}: Migrate {_fco_to_pretty_print(obj_type, len(objects_to_migrate))}.")
            safe_print(
                f"\nDetected {len(objects_to_migrate)} {_fco_to_pretty_print(obj_type, len(objects_to_migrate))} in need of an upgrade:\n"
            )

        safe_print(
            f"\nNumber {index + 1} of {len(objects_to_migrate)} {_fco_to_pretty_print(obj_type, len(objects_to_migrate))}:\n"
        )
        guildanceBuilder(objects_to_migrate[index], repo_root).print_guidance()

        # Display options
        if index > 0 and index < len(objects_to_migrate) - 1:
            options = "[n]ext, [p]revious, [q]uit"
        elif index == 0:
            options = "[n]ext, [q]uit"
        elif index == len(objects_to_migrate) - 1:
            options = "[p]revious, [q]uit"
        else:
            msg = f"Invalid index {index}."
            raise ValueError(msg)

        user_input = click.prompt(f"Continue migration? {options}", type=str).lower()

        if user_input == "n":
            if index < len(objects_to_migrate) - 1:
                index += 1
            else:
                safe_print(
                    f"Step {step}: Migrate {_fco_to_pretty_print(obj_type, len(objects_to_migrate))} complete. Run `tecton plan` to ensure these objects were correctly migrated (you may apply this plan to commit your progress). Then run `tecton upgrade` to continue the migration."
                )
                return
        elif user_input == "p" and index > 0:
            index -= 1
        elif user_input == "q":
            safe_print("Process quit by user.")
            return
        elif user_input == "p" and index == 0 and step > 1:
            step -= 1
            index = len(objects_to_migrate) - 1
        else:
            safe_print(f"Unknown input {user_input}. Try again.")


def print_non_interactive_migration_guidance(all_objects: Dict[str, List[Dict[str, any]]], repo_root: str) -> None:
    for step, (obj_type, GuidanceBuilder) in enumerate(
        OBJECT_TO_MIGRATE_TO_GUIDANCE_STEPS,
        1,
    ):
        objects_to_migrate = sorted(
            [obj for obj in all_objects.get(obj_type, []) if obj._framework_version != FrameworkVersion.FWV6],
            key=lambda obj: (obj._source_info.source_filename, int(obj._source_info.source_lineno)),
        )
        if bool(objects_to_migrate):
            safe_print(f"\nStep {step}: Migrate {_fco_to_pretty_print(obj_type, len(objects_to_migrate))}.")
            safe_print(
                f"\nDetected {len(objects_to_migrate)} {_fco_to_pretty_print(obj_type, len(objects_to_migrate))} in need of an upgrade:\n"
            )
            for obj in objects_to_migrate:
                GuidanceBuilder(obj, repo_root).print_guidance()
            break
    safe_print(
        "Run `tecton plan` when complete to ensure there are no destructive changes. Then run `tecton upgrade` to get the updated set of instructions."
    )


def print_migration_guidance(all_objects: Dict[str, List[Dict[str, any]]], repo_root: str, interactive: bool) -> None:
    if interactive:
        print_interactive_migration_guidance(all_objects=all_objects, repo_root=repo_root)
    else:
        print_non_interactive_migration_guidance(all_objects=all_objects, repo_root=repo_root)


@click.command(cls=TectonCommand)
@click.argument(
    "path",
    required=False,
    default=None,
    type=click.Path(exists=True, dir_okay=True, path_type=Path, readable=True),
)
@click.option("--non-interactive", is_flag=True, help="Run in non-interactive mode.")
def upgrade(path: Optional[Path] = None, non_interactive: bool = False):
    """Analyze Tecton objects in the feature repository and provide migration guidance.

    If PATH is provided, analyze the specified file or directory.
    If PATH is not provided, analyze all Python files in the repository root.
    """
    repo_file_handler.ensure_prepare_repo()
    repo_root = repo_file_handler.repo_root()
    repo_files = repo_file_handler.repo_files()
    py_files = [p for p in repo_files if p.suffix == ".py"]

    if path:
        full_path = path.resolve()
        if full_path.is_file():
            py_files = [full_path]
        elif full_path.is_dir():
            py_files = [p for p in full_path.rglob("*.py") if p.is_file()]
        else:
            print(f"Error: {full_path} is not a valid file or directory.")
            return

    interactive = not non_interactive
    # Skip `validate` so that it is safe to execute 0.9 objects
    with conf._temporary_set("TECTON_SKIP_OBJECT_VALIDATION", True), conf._temporary_set(
        "TECTON_REQUIRE_SCHEMA", False
    ):
        all_objects = process_files(py_files, Path(repo_root))
        print_migration_progress(all_objects)
        print_migration_guidance(all_objects, repo_root, interactive)
