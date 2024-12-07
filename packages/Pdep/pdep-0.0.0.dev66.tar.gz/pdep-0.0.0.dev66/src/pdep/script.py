from pathlib import Path
import sys
import importlib.metadata
import argparse
import json


def is_standard_library(module_name: str) -> bool:
    """Check whether a module is part of the current Python version's standard library."""
    return module_name in sys.stdlib_module_names


def get_all_package_name_to_distribution_names_mapping() -> dict[str, tuple[str, ...]]:
    """Get a mapping of all installed top-level import package names
    to their corresponding distribution package names.

    Returns
    -------
    mapping : dict[str, tuple[str, ...]]
        Mapping of top-level import package names to distribution package names.
        Each top-level import package may correspond to multiple distribution packages.
        Therefore, the values are tuples of distribution package names.
    """
    mapping = importlib.metadata.packages_distributions()
    print(mapping)
    # Sometimes the list of distribution names for a package contains duplicates (seen in editable installs).
    mapping_unique_dist_names = {
        package_name: tuple(sorted(distribution_names, key=lambda name: name.lower()))
        for package_name, distribution_names in mapping.items()
    }
    return mapping_unique_dist_names


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path_import_name_json")
    args = parser.parse_args()
    path = Path(args.path_import_name_json)
    import_names = json.loads(path.read_text())
    standard_lib = [name for name in import_names if is_standard_library(name)]
    path_is_standard_lib_json = path.with_name("standard_lib.json")
    path_is_standard_lib_json.write_text(json.dumps(standard_lib))
    mappings = get_all_package_name_to_distribution_names_mapping()
    path_mappings_json = path.with_name("pkg_to_dist_mapping.json")
    path_mappings_json.write_text(json.dumps(mappings))
