from pathlib import Path
import tomllib as _tomllib
import os
import re as _re
import tempfile
import json

import importlib.resources as _importlib_resources
from packaging.requirements import Requirement as _Req
import requirements as _reqs
import pysyntax as _pysyntax
from loggerman import logger as _logger
import mdit as _mdit
import pyshellman as _pyshellman


def _log_extracted_import_names(pkg_name: str, imports: dict[str, list[str]]) -> None:
    field_list_items = []
    for module_name, module_imports in imports.items():
        if module_imports:
            imports_list = _mdit.inline_container(
                *[_mdit.element.code_span(import_name) for import_name in module_imports],
                separator="  ",
            )
            field_list_items.append(
                _mdit.element.field_list_item(_mdit.element.code_span(module_name), imports_list)
            )
    _logger.debug(
        _mdit.inline_container(
            "Extracted import names from package ",
            _mdit.element.code_span(pkg_name)
        ),
        _mdit.element.field_list(field_list_items) if field_list_items else "No imports found.",
    )
    return


def run(
    path_package: str | Path,
    path_requirements: str | Path,
    python_version: str | None = None,
):
    pkg_name = Path(path_package).name
    imports = extract_import_names_from_package_path(path_package, top_level=True)
    _log_extracted_import_names(pkg_name=pkg_name, imports=imports)
    req_path = Path(path_requirements)
    if req_path.name.lower() == "pyproject.toml":
        dep_specs, dep_names = extract_dependencies_from_pyproject_path(req_path)
        path_requirements_txt = None
        _logger.debug(
            "Extracted dependencies from pyproject.toml",
            _logger.pretty(dep_names) if dep_names else "No dependencies found.",
        )
    else:
        dep_specs = None
        dep_names = extract_dependency_names_from_requirements_path(req_path)
        path_requirements_txt = req_path
        _logger.debug(
            "Extracted dependencies from requirements.txt",
            _logger.pretty(dep_names) if dep_names else "No dependencies found.",
        )
    all_imports = set([import_name for module_imports in imports.values() for import_name in module_imports])
    stand_libs, mappings = analyze_imports(
        import_names=list(all_imports),
        python_version=python_version,
        dependencies=dep_specs,
        path_requirements=path_requirements_txt,
    )
    non_standard_imports = sorted([import_name for import_name in all_imports if import_name not in stand_libs])
    add_to_reqs = {}  # mapping of package name to distribution names that should be added to requirements
    correct_reqs = {}
    dep_names_normalized = [normalize_distribution_name(dep_name) for dep_name in dep_names]
    for non_stand_import in non_standard_imports:
        dist_names = mappings.get(non_stand_import.split(".")[0])
        if not dist_names:
            add_to_reqs[non_stand_import] = None
            continue
        for dist_name in dist_names:
            if normalize_distribution_name(dist_name) in dep_names_normalized:
                correct_reqs.setdefault(non_stand_import, []).append(dist_name)
        if non_stand_import not in correct_reqs:
            add_to_reqs[non_stand_import] = dist_names
    used_reqs_normalized = [normalize_distribution_name(dep_name) for dep_names in correct_reqs.values() for dep_name in dep_names]
    unused_reqs = sorted([dep_name for dep_name in dep_names if normalize_distribution_name(dep_name) not in used_reqs_normalized])
    if not add_to_reqs and not unused_reqs:
        import_list_md = _mdit.element.field_list()
        for import_name, dist_names in correct_reqs.items():
            for dist_name in dist_names:
                import_list_md.append(dist_name, _mdit.element.code_span(import_name))
        list_stand_libs = _mdit.inline_container(
            *[_mdit.element.code_span(stand_lib) for stand_lib in stand_libs],
            separator=" ",
        )
        import_list_md.append("Standard Library", list_stand_libs)
        _logger.success(
            "All imports and dependencies match",
            import_list_md,
        )
    else:
        if add_to_reqs:
            _log_missing_deps(add_to_reqs, imports)
        if unused_reqs:
            _logger.warning(
                "Unused dependencies",
                "Following dependencies are not required by the package:",
                _mdit.element.unordered_list([_mdit.element.code_span(dep_name) for dep_name in unused_reqs]),
            )
    return stand_libs, non_standard_imports, dep_names, add_to_reqs, unused_reqs


def _log_missing_deps(add_to_reqs: dict[str, list[str]], module_imports: dict[str, list[str]]) -> None:

    def get_modules_with_import(import_name: str) -> _mdit.element.UnOrderedListItem:
        modules_list = _mdit.inline_container(
            "Affected modules:",
            *[
                _mdit.element.code_span(module_name)
                for module_name, imports in module_imports.items()
                if import_name in imports
            ],
            separator=" ",
        )
        return _mdit.element.unordered_list_item(modules_list)

    list_missing = _mdit.element.field_list()
    list_implicit = _mdit.element.field_list()
    for import_name, possible_dist_names in add_to_reqs.items():
        field_list_body = _mdit.container(get_modules_with_import(import_name), content_separator="\n")
        if possible_dist_names is None:
            list_missing.append(
                _mdit.element.code_span(import_name),
                field_list_body,
            )
        else:
            possible_list = _mdit.inline_container(
                "Possible dist names:",
                *[_mdit.element.code_span(dist_name) for dist_name in possible_dist_names],
                separator=" ",
            )
            field_list_body.append(_mdit.element.unordered_list_item(possible_list))
            list_implicit.append(
                _mdit.element.code_span(import_name),
                field_list_body,
            )
    if list_missing.content.elements():
        _logger.error(
            "Missing dependencies",
            "Following imports are not covered by the declared dependencies:",
            list_missing,
        )
    if list_implicit.content.elements():
        _logger.warning(
            "Implicit dependencies",
            "Following imports are only implicitly covered by the declared dependencies:",
            list_implicit,
        )
    return


def analyze_imports(
    import_names: list[str],
    dependencies: list[str] | None = None,
    path_requirements: str | Path | None = None,
    python_version: str | None = None,
):
    python_executable = f"python{python_version or ''}"
    # Check if the given Python version is installed
    py_ver = _pyshellman.run(
        [python_executable, "--version"],
        raise_execution=False,
        raise_exit_code=False,
        raise_stderr=False,
    )
    if not py_ver.succeeded:
        _logger.critical(
            f"Python version {python_version} not found",
            _mdit.element.rich(py_ver.__rich__())
        )
        raise RuntimeError()
    # Create a virtual environment using the specified Python version
    path_script = Path(_importlib_resources.files("pdep")) / "script.py"
    with tempfile.TemporaryDirectory() as temp_dir:
        path_json_import_names = os.path.join(temp_dir, 'import_names.json')
        with open(path_json_import_names, 'w') as f:
            json.dump(import_names, f)
        env_dir = os.path.join(temp_dir, '.venv')
        # TODO: Make it also work with other python versions
        # Currently if the python executable is different than the current python executable,
        # the mapping of package names to distribution names will not be complete.
        # See also: https://stackoverflow.com/questions/8052926/running-subprocess-within-different-virtualenv-with-python
        venv_out = _pyshellman.run(
            [python_executable, "-m", "venv", env_dir],
            raise_execution=False,
            raise_exit_code=False,
            raise_stderr=False,
        )
        if not venv_out.succeeded:
            _logger.critical(
                f"Failed to create virtual environment",
                _mdit.element.rich(venv_out.__rich__())
            )
            raise RuntimeError()
        _logger.debug(
            "Created virtual environment",
            _mdit.element.rich(venv_out.__rich__())
        )
        # Activate the virtual environment's pip and install dependencies
        pip_executable = os.path.join(env_dir, 'bin', 'pip') if os.name != 'nt' else os.path.join(
            env_dir, 'Scripts', 'pip.exe'
        )
        if dependencies:
            pip_install = _pyshellman.run(
                [pip_executable, "install"] + dependencies,
                raise_execution=False,
                raise_exit_code=False,
                raise_stderr=False,
            )
            if not pip_install.succeeded:
                _logger.critical(
                    f"Failed to install dependencies",
                    _mdit.element.rich(pip_install.__rich__())
                )
                raise RuntimeError()
            _logger.debug(
                "Installed dependencies",
                _mdit.element.rich(pip_install.__rich__())
            )
        if path_requirements:
            pip_install_r = _pyshellman.run(
                [pip_executable, "install", "-r", path_requirements],
                raise_execution=False,
                raise_exit_code=False,
                raise_stderr=False,
            )
            if not pip_install_r.succeeded:
                _logger.critical(
                    f"Failed to install dependencies",
                    _mdit.element.rich(pip_install_r.__rich__())
                )
                raise RuntimeError()
            _logger.debug(
                "Installed dependencies",
                _mdit.element.rich(pip_install_r.__rich__())
            )
        # Run the script in the virtual environment
        python_executable = os.path.join(env_dir, 'bin', 'python') if os.name != 'nt' else os.path.join(
            env_dir, 'Scripts', 'python.exe'
        )
        out = _pyshellman.run(
            [python_executable, str(path_script), str(path_json_import_names)],
            raise_execution=False,
            raise_exit_code=False,
            raise_stderr=False,
        )
        if not out.succeeded:
            _logger.critical(
                f"Failed to run script in virtual environment",
                _mdit.element.rich(out.__rich__())
            )
            raise RuntimeError()
        path_standard_lib = Path(temp_dir) / "standard_lib.json"
        path_mappings = Path(temp_dir) / "pkg_to_dist_mapping.json"
        standard_lib = sorted(json.loads(path_standard_lib.read_text()))
        _logger.debug(
            "Identified standard library imports",
            _logger.pretty(standard_lib) if standard_lib else "No standard library imports found."
        )
        mappings = dict(sorted(json.loads(path_mappings.read_text()).items()))
        _logger.debug(
            "Identified package to distribution mappings",
            _logger.pretty(mappings) if mappings else "No packages found."
        )
        return standard_lib, mappings


def extract_import_names_from_package_path(path_package: str | Path, top_level: bool = True) -> dict[str, list[str]]:
    imports = {}
    pkg_path = Path(path_package).resolve()
    pkg_name = pkg_path.name
    for filepath in pkg_path.glob("**/*.py"):
        module_path = str(filepath.relative_to(pkg_path).with_suffix("").as_posix()).replace("/", ".")
        extracted_imports = extract_import_names_from_module_path(filepath, top_level=top_level)
        imports[module_path] = [
            import_name for import_name in extracted_imports if import_name.split(".")[0] != pkg_name
        ]
    return dict(sorted(imports.items()))


def extract_import_names_from_module_path(file_path: str | Path, top_level: bool = True) -> list[str]:
    return extract_import_names_from_module_string(Path(file_path).resolve().read_text(), top_level=top_level)


def extract_import_names_from_module_string(code: str, top_level: bool = True) -> list[str]:
    """Extract the names of imported modules in a Python code string.

    Parameters
    ----------
    code
        Python code string.
    top_level
        Only return the top-level name of each import, i.e., the part before the first dot.
    """
    import_names = _pysyntax.parse.imports(code)
    if top_level:
        import_names = [name.split(".")[0] for name in import_names]
    return sorted(list(set(import_names)))


def extract_dependencies_from_pyproject_path(path_pyproject: str | Path) -> tuple[list[str], list[str]]:
    pyproject_string = Path(path_pyproject).read_text()
    return extract_dependencies_from_pyproject_string(pyproject_string)


def extract_dependencies_from_pyproject_string(pyproject: str) -> tuple[list[str], list[str]]:
    return extract_dependencies_from_pyproject_data(_tomllib.loads(pyproject))


def extract_dependencies_from_pyproject_data(pyproject: dict) -> tuple[list[str], list[str]]:

    def add(deps: list[str]) -> None:
        for dep in deps:
            specs.append(dep)
            names.append(_Req(dep).name)
    specs = []
    names = []
    project = pyproject.get("project", {})
    add(project.get("dependencies", []))
    for group_name, dependencies in project.get("optional-dependencies", {}).items():
        add(dependencies)
    return sorted(specs), sorted(names)


def extract_dependency_names_from_requirements_path(path_requirements: str | Path) -> list[str]:
    return extract_dependency_names_from_requirements_string(Path(path_requirements).read_text())


def extract_dependency_names_from_requirements_string(requirements: str) -> list[str]:
    return sorted([req.name for req in _reqs.parse(requirements)])


def normalize_distribution_name(dist_name: str) -> str:
    """Normalize a distribution name to a canonical form.

    References
    ----------
    - [PyPA: Python Packaging User Guide: Name format](https://packaging.python.org/en/latest/specifications/name-normalization/)
    """
    return _re.sub(r"[-_.]+", "-", dist_name).lower()