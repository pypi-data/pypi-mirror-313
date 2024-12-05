# Pdep

Pdep is a lightweight code analyzer for Python,
specialized in detecting missing and unused dependencies in your package:
It compares the import statements in your source code with
the dependencies declared in your dependency declaration file
(`requirements.txt` or `pyproject.toml` format) and generates a detailed report, including:
- Missing dependencies: imported modules that are not provided by any of the declared dependencies.
- Explicitly missing dependencies: dependencies that are both directly used by your imports
  and indirectly installed by your dependency declaration file, but not explicitly declared in it.
  These are dependencies that are only available because another declared dependency depends on them,
  while you are explicitly using them in your code.
- Unused dependencies: declared dependencies that are not used by any import statement in your code.


## Algorithm

1. Parses your source code and extracts a full list of all imported modules.
2. Parses your dependency declaration file (`requirements.txt` or `pyproject.toml` format)
   and extracts a full list of all declared dependencies.
3. Creates a temporary virtual environment, installs all declared dependencies,
   and uses the `importlib.metadata` module to create an accurate mapping
   from module (import) names to their corresponding distribution (dependency) names.
4. Uses `sys.stdlib_module_names` to filter out standard library modules from your imports.
5. For each non-standard-library import, checks whether the module is supplied by any of the installed dependencies:
   - If not, the import is marked as missing a dependency.
   - Otherwise, for each installed dependency that supplies the module, checks whether its (normalized) name
     is present in the (normalized) dependency declaration file:
     - If so, the import is marked as satisfied, and the dependency is marked as used.
     - If none of the supplying dependency names are present in the dependency declaration file,
       the import is marked as missing an explicit dependency declaration,
       meaning that the dependency is installed (due to being a transitive dependency of another dependency),
       but not explicitly declared in the dependency declaration file
       (which is bad, since you are explicitly using it in your code).
6. Any remaining dependency declarations that are not used by any import are marked as unused.

## Shortcomings

1. Declared dependencies that are not used in any import statement are marked as unused,
   even if they are used in other ways (e.g., in a subprocess call).
2. Missing sub-packages of a namespace package dependency are not detected.
   For example, consider the namespace package `foo` with sub-packages `foo-bar` (import name `foo.bar`)
   and `foo-baz` (import name `foo.baz`).
   If you use both sub-packages in your code, but only declare `foo-bar` in your dependency declaration file,
   `foo-baz` will not be detected as missing.
   
## Other tools
- [PyDeps](https://github.com/thebjorn/pydeps): Dependency visualization tool.
- [FindImports](https://github.com/mgedmin/findimports): Find unused imports in a module.