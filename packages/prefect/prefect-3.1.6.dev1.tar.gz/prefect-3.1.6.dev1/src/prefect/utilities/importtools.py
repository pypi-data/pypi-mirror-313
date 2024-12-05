import ast
import importlib
import importlib.util
import os
import runpy
import sys
import warnings
from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import ModuleSpec
from pathlib import Path
from tempfile import NamedTemporaryFile
from types import ModuleType
from typing import Any, Callable, Dict, Iterable, NamedTuple, Optional, Union

import fsspec

from prefect.exceptions import ScriptError
from prefect.logging.loggers import get_logger
from prefect.utilities.filesystem import filename, is_local_path, tmpchdir

logger = get_logger(__name__)


def to_qualified_name(obj: Any) -> str:
    """
    Given an object, returns its fully-qualified name: a string that represents its
    Python import path.

    Args:
        obj (Any): an importable Python object

    Returns:
        str: the qualified name
    """
    if sys.version_info < (3, 10):
        # These attributes are only available in Python 3.10+
        if isinstance(obj, (classmethod, staticmethod)):
            obj = obj.__func__
    return obj.__module__ + "." + obj.__qualname__


def from_qualified_name(name: str) -> Any:
    """
    Import an object given a fully-qualified name.

    Args:
        name: The fully-qualified name of the object to import.

    Returns:
        the imported object

    Examples:
        >>> obj = from_qualified_name("random.randint")
        >>> import random
        >>> obj == random.randint
        True
    """
    # Try importing it first so we support "module" or "module.sub_module"
    try:
        module = importlib.import_module(name)
        return module
    except ImportError:
        # If no subitem was included raise the import error
        if "." not in name:
            raise

    # Otherwise, we'll try to load it as an attribute of a module
    mod_name, attr_name = name.rsplit(".", 1)
    module = importlib.import_module(mod_name)
    return getattr(module, attr_name)


def objects_from_script(path: str, text: Union[str, bytes] = None) -> Dict[str, Any]:
    """
    Run a python script and return all the global variables

    Supports remote paths by copying to a local temporary file.

    WARNING: The Python documentation does not recommend using runpy for this pattern.

    > Furthermore, any functions and classes defined by the executed code are not
    > guaranteed to work correctly after a runpy function has returned. If that
    > limitation is not acceptable for a given use case, importlib is likely to be a
    > more suitable choice than this module.

    The function `load_script_as_module` uses importlib instead and should be used
    instead for loading objects from scripts.

    Args:
        path: The path to the script to run
        text: Optionally, the text of the script. Skips loading the contents if given.

    Returns:
        A dictionary mapping variable name to value

    Raises:
        ScriptError: if the script raises an exception during execution
    """

    def run_script(run_path: str):
        # Cast to an absolute path before changing directories to ensure relative paths
        # are not broken
        abs_run_path = os.path.abspath(run_path)
        with tmpchdir(run_path):
            try:
                return runpy.run_path(abs_run_path)
            except Exception as exc:
                raise ScriptError(user_exc=exc, path=path) from exc

    if text:
        with NamedTemporaryFile(
            mode="wt" if isinstance(text, str) else "wb",
            prefix=f"run-{filename(path)}",
            suffix=".py",
        ) as tmpfile:
            tmpfile.write(text)
            tmpfile.flush()
            return run_script(tmpfile.name)

    else:
        if not is_local_path(path):
            # Remote paths need to be local to run
            with fsspec.open(path) as f:
                contents = f.read()
            return objects_from_script(path, contents)
        else:
            return run_script(path)


def load_script_as_module(path: str) -> ModuleType:
    """
    Execute a script at the given path.

    Sets the module name to `__prefect_loader__`.

    If an exception occurs during execution of the script, a
    `prefect.exceptions.ScriptError` is created to wrap the exception and raised.

    During the duration of this function call, `sys` is modified to support loading.
    These changes are reverted after completion, but this function is not thread safe
    and use of it in threaded contexts may result in undesirable behavior.

    See https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    """
    # We will add the parent directory to search locations to support relative imports
    # during execution of the script
    if not path.endswith(".py"):
        raise ValueError(f"The provided path does not point to a python file: {path!r}")

    parent_path = str(Path(path).resolve().parent)
    working_directory = os.getcwd()

    spec = importlib.util.spec_from_file_location(
        "__prefect_loader__",
        path,
        # Support explicit relative imports i.e. `from .foo import bar`
        submodule_search_locations=[parent_path, working_directory],
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["__prefect_loader__"] = module

    # Support implicit relative imports i.e. `from foo import bar`
    sys.path.insert(0, working_directory)
    sys.path.insert(0, parent_path)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise ScriptError(user_exc=exc, path=path) from exc
    finally:
        sys.modules.pop("__prefect_loader__")
        sys.path.remove(parent_path)
        sys.path.remove(working_directory)

    return module


def load_module(module_name: str) -> ModuleType:
    """
    Import a module with support for relative imports within the module.
    """
    # Ensure relative imports within the imported module work if the user is in the
    # correct working directory
    working_directory = os.getcwd()
    sys.path.insert(0, working_directory)

    try:
        return importlib.import_module(module_name)
    finally:
        sys.path.remove(working_directory)


def import_object(import_path: str):
    """
    Load an object from an import path.

    Import paths can be formatted as one of:
    - module.object
    - module:object
    - /path/to/script.py:object

    This function is not thread safe as it modifies the 'sys' module during execution.
    """
    if ".py:" in import_path:
        script_path, object_name = import_path.rsplit(":", 1)
        module = load_script_as_module(script_path)
    else:
        if ":" in import_path:
            module_name, object_name = import_path.rsplit(":", 1)
        elif "." in import_path:
            module_name, object_name = import_path.rsplit(".", 1)
        else:
            raise ValueError(
                f"Invalid format for object import. Received {import_path!r}."
            )

        module = load_module(module_name)

    return getattr(module, object_name)


class DelayedImportErrorModule(ModuleType):
    """
    A fake module returned by `lazy_import` when the module cannot be found. When any
    of the module's attributes are accessed, we will throw a `ModuleNotFoundError`.

    Adapted from [lazy_loader][1]

    [1]: https://github.com/scientific-python/lazy_loader
    """

    def __init__(self, error_message, help_message, *args, **kwargs):
        self.__error_message = error_message
        self.__help_message = (
            help_message or "Import errors for this module are only reported when used."
        )
        super().__init__(*args, **kwargs)

    def __getattr__(self, attr):
        if attr in ("__class__", "__file__", "__help_message"):
            super().__getattr__(attr)
        else:
            raise ModuleNotFoundError(self.__error_message)


def lazy_import(
    name: str, error_on_import: bool = False, help_message: str = ""
) -> ModuleType:
    """
    Create a lazily-imported module to use in place of the module of the given name.
    Use this to retain module-level imports for libraries that we don't want to
    actually import until they are needed.

    NOTE: Lazy-loading a subpackage can cause the subpackage to be imported
    twice if another non-lazy import also imports the subpackage. For example,
    using both `lazy_import("docker.errors")` and `import docker.errors` in the
    same codebase will import `docker.errors` twice and can lead to unexpected
    behavior, e.g. type check failures and import-time side effects running
    twice.

    Adapted from the [Python documentation][1] and [lazy_loader][2]

    [1]: https://docs.python.org/3/library/importlib.html#implementing-lazy-imports
    [2]: https://github.com/scientific-python/lazy_loader
    """

    try:
        return sys.modules[name]
    except KeyError:
        pass

    if "." in name:
        warnings.warn(
            "Lazy importing subpackages can lead to unexpected behavior.",
            RuntimeWarning,
        )

    spec = importlib.util.find_spec(name)

    if spec is None:
        import_error_message = f"No module named '{name}'.\n{help_message}"

        if error_on_import:
            raise ModuleNotFoundError(import_error_message)

        return DelayedImportErrorModule(
            import_error_message, help_message, "DelayedImportErrorModule"
        )

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module

    loader = importlib.util.LazyLoader(spec.loader)
    loader.exec_module(module)

    return module


class AliasedModuleDefinition(NamedTuple):
    """
    A definition for the `AliasedModuleFinder`.

    Args:
        alias: The import name to create
        real: The import name of the module to reference for the alias
        callback: A function to call when the alias module is loaded
    """

    alias: str
    real: str
    callback: Optional[Callable[[str], None]]


class AliasedModuleFinder(MetaPathFinder):
    def __init__(self, aliases: Iterable[AliasedModuleDefinition]):
        """
        See `AliasedModuleDefinition` for alias specification.

        Aliases apply to all modules nested within an alias.
        """
        self.aliases = aliases

    def find_spec(
        self,
        fullname: str,
        path=None,
        target=None,
    ) -> Optional[ModuleSpec]:
        """
        The fullname is the imported path, e.g. "foo.bar". If there is an alias "phi"
        for "foo" then on import of "phi.bar" we will find the spec for "foo.bar" and
        create a new spec for "phi.bar" that points to "foo.bar".
        """
        for alias, real, callback in self.aliases:
            if fullname.startswith(alias):
                # Retrieve the spec of the real module
                real_spec = importlib.util.find_spec(fullname.replace(alias, real, 1))
                # Create a new spec for the alias
                return ModuleSpec(
                    fullname,
                    AliasedModuleLoader(fullname, callback, real_spec),
                    origin=real_spec.origin,
                    is_package=real_spec.submodule_search_locations is not None,
                )


class AliasedModuleLoader(Loader):
    def __init__(
        self,
        alias: str,
        callback: Optional[Callable[[str], None]],
        real_spec: ModuleSpec,
    ):
        self.alias = alias
        self.callback = callback
        self.real_spec = real_spec

    def exec_module(self, _: ModuleType) -> None:
        root_module = importlib.import_module(self.real_spec.name)
        if self.callback is not None:
            self.callback(self.alias)
        sys.modules[self.alias] = root_module


def safe_load_namespace(
    source_code: str, filepath: Optional[str] = None
) -> Dict[str, Any]:
    """
    Safely load a namespace from source code, optionally handling relative imports.

    If a `filepath` is provided, `sys.path` is modified to support relative imports.
    Changes to `sys.path` are reverted after completion, but this function is not thread safe
    and use of it in threaded contexts may result in undesirable behavior.

    Args:
        source_code: The source code to load
        filepath: Optional file path of the source code. If provided, enables relative imports.

    Returns:
        The namespace loaded from the source code.
    """
    parsed_code = ast.parse(source_code)

    namespace: Dict[str, Any] = {"__name__": "prefect_safe_namespace_loader"}

    # Remove the body of the if __name__ == "__main__": block
    new_body = [node for node in parsed_code.body if not _is_main_block(node)]
    parsed_code.body = new_body

    temp_module = None
    original_sys_path = None

    if filepath:
        # Setup for relative imports
        file_dir = os.path.dirname(os.path.abspath(filepath))
        package_name = os.path.basename(file_dir)
        parent_dir = os.path.dirname(file_dir)

        # Save original sys.path and modify it
        original_sys_path = sys.path.copy()
        sys.path.insert(0, parent_dir)
        sys.path.insert(0, file_dir)

        # Create a temporary module for import context
        temp_module = ModuleType(package_name)
        temp_module.__file__ = filepath
        temp_module.__package__ = package_name

        # Create a spec for the module
        temp_module.__spec__ = ModuleSpec(package_name, None)
        temp_module.__spec__.loader = None
        temp_module.__spec__.submodule_search_locations = [file_dir]

    try:
        for node in parsed_code.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name
                    as_name = alias.asname or module_name
                    try:
                        namespace[as_name] = importlib.import_module(module_name)
                        logger.debug("Successfully imported %s", module_name)
                    except ImportError as e:
                        logger.debug(f"Failed to import {module_name}: {e}")
            elif isinstance(node, ast.ImportFrom):
                module_name = node.module or ""
                if filepath:
                    try:
                        if node.level > 0:
                            # For relative imports, use the parent package to inform the import
                            package_parts = temp_module.__package__.split(".")
                            if len(package_parts) < node.level:
                                raise ImportError(
                                    "Attempted relative import beyond top-level package"
                                )
                            parent_package = ".".join(
                                package_parts[: (1 - node.level)]
                                if node.level > 1
                                else package_parts
                            )
                            module = importlib.import_module(
                                f".{module_name}" if module_name else "",
                                package=parent_package,
                            )
                        else:
                            # Absolute imports are handled as normal
                            module = importlib.import_module(module_name)

                        for alias in node.names:
                            name = alias.name
                            asname = alias.asname or name
                            if name == "*":
                                # Handle 'from module import *'
                                module_dict = {
                                    k: v
                                    for k, v in module.__dict__.items()
                                    if not k.startswith("_")
                                }
                                namespace.update(module_dict)
                            else:
                                try:
                                    attribute = getattr(module, name)
                                    namespace[asname] = attribute
                                except AttributeError as e:
                                    logger.debug(
                                        "Failed to retrieve %s from %s: %s",
                                        name,
                                        module_name,
                                        e,
                                    )
                    except ImportError as e:
                        logger.debug("Failed to import from %s: %s", module_name, e)
                else:
                    # Handle as absolute import when no filepath is provided
                    try:
                        module = importlib.import_module(module_name)
                        for alias in node.names:
                            name = alias.name
                            asname = alias.asname or name
                            if name == "*":
                                # Handle 'from module import *'
                                module_dict = {
                                    k: v
                                    for k, v in module.__dict__.items()
                                    if not k.startswith("_")
                                }
                                namespace.update(module_dict)
                            else:
                                try:
                                    attribute = getattr(module, name)
                                    namespace[asname] = attribute
                                except AttributeError as e:
                                    logger.debug(
                                        "Failed to retrieve %s from %s: %s",
                                        name,
                                        module_name,
                                        e,
                                    )
                    except ImportError as e:
                        logger.debug("Failed to import from %s: %s", module_name, e)
        # Handle local definitions
        for node in parsed_code.body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.Assign)):
                try:
                    code = compile(
                        ast.Module(body=[node], type_ignores=[]),
                        filename="<ast>",
                        mode="exec",
                    )
                    exec(code, namespace)
                except Exception as e:
                    logger.debug("Failed to compile: %s", e)

    finally:
        # Restore original sys.path if it was modified
        if original_sys_path:
            sys.path[:] = original_sys_path

    return namespace


def _is_main_block(node: ast.AST):
    """
    Check if the node is an `if __name__ == "__main__":` block.
    """
    if isinstance(node, ast.If):
        try:
            # Check if the condition is `if __name__ == "__main__":`
            if (
                isinstance(node.test, ast.Compare)
                and isinstance(node.test.left, ast.Name)
                and node.test.left.id == "__name__"
                and isinstance(node.test.comparators[0], ast.Constant)
                and node.test.comparators[0].value == "__main__"
            ):
                return True
        except AttributeError:
            pass
    return False
