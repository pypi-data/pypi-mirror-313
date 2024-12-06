from __future__ import annotations

import importlib.util as imputil
import inspect
import sys
import typing
from importlib import import_module
from os import path
from pathlib import Path
from types import ModuleType
from typing import Callable

from digitalhub.entities.workflow.crud import get_workflow
from digitalhub.utils.generic_utils import decode_base64_string, extract_archive, requests_chunk_download
from digitalhub.utils.git_utils import clone_repository
from digitalhub.utils.logger import LOGGER
from digitalhub.utils.s3_utils import get_bucket_and_key, get_s3_source
from digitalhub.utils.uri_utils import has_git_scheme, has_remote_scheme, has_s3_scheme

if typing.TYPE_CHECKING:
    from digitalhub.entities.workflow._base.entity import Workflow

    from digitalhub_runtime_kfp.entities.workflow.kfp.spec import WorkflowSpecKfp


def get_dhcore_workflow(workflow_string: str) -> Workflow:
    """
    Get DHCore workflow.

    Parameters
    ----------
    workflow_string : str
        Function string.

    Returns
    -------
    Workflow
        DHCore workflow.
    """
    splitted = workflow_string.split("://")[1].split("/")
    name, uuid = splitted[1].split(":")
    LOGGER.info(f"Getting workflow {name}:{uuid}.")
    try:
        return get_workflow(name, project=splitted[0], entity_id=uuid)
    except Exception as e:
        msg = f"Error getting workflow {name}:{uuid}. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg) from e


def save_workflow_source(path: Path, source_spec: dict) -> str:
    """
    Save workflow source.

    Parameters
    ----------
    path : Path
        Path where to save the workflow source.
    source_spec : dict
        Workflow source spec.

    Returns
    -------
    path
        Workflow code.
    """
    # Prepare path
    path.mkdir(parents=True, exist_ok=True)

    # Get relevant information
    base64 = source_spec.get("base64")
    source = source_spec.get("source")
    handler = source_spec.get("handler")

    # Base64
    if base64 is not None:
        base64_path = path / "main.py"
        base64_path.write_text(decode_base64_string(base64))
        return base64_path

    # Git repo
    if has_git_scheme(source):
        clone_repository(path, source)

    # Http(s) or s3 presigned urls
    elif has_remote_scheme(source):
        filename = path / "archive.zip"
        requests_chunk_download(source, filename)
        extract_archive(path, filename)

    # S3 path
    elif has_s3_scheme(source):
        filename = path / "archive.zip"
        bucket, key = get_bucket_and_key(source)
        get_s3_source(bucket, key, filename)
        extract_archive(path, filename)

    # Unsupported scheme
    else:
        raise RuntimeError("Unable to collect source.")

    if ":" in handler:
        handler = handler.split(":")[0].split(".")
        return str(Path(path, *handler).with_suffix(".py"))
    else:
        return str(path.with_suffix(".py"))


def parse_workflow_specs(spec: WorkflowSpecKfp) -> dict:
    """
    Parse workflow specs.

    Parameters
    ----------
    spec : WorkflowSpecKFP
        DHCore workflow spec.

    Returns
    -------
    dict
        Workflow specs.
    """
    try:
        return {
            "image": spec.image,
            "tag": spec.tag,
            "handler": spec.source.get("handler"),
        }
    except AttributeError as e:
        msg = f"Error parsing workflow specs. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.error(msg)
        raise RuntimeError(msg)


def get_kfp_pipeline(name: str, workflow_source: str, workflow_specs: dict) -> Callable:
    """
    Get KFP pipeline.

    Parameters
    ----------
    name : str
        Name of the KFP pipeline.
    workflow_source : str
        Source of the workflow.
    workflow_specs : dict
        specifications.of the workflow.

    Returns
    -------
    Callable
        KFP pipeline.
    """
    try:
        if not path.isfile(workflow_source):
            raise OSError(f"Source file {workflow_source} not found.")

        abspath = path.abspath(workflow_source)
        if abspath not in sys.path:
            sys.path.append(abspath)

        handler = workflow_specs.get("handler").split(":")[-1]
        return _load_module(workflow_source, handler)
    except Exception as e:
        msg = f"Error getting '{name}' KFP pipeline. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg) from e


def _load_module(file_name: str, handler: str) -> Callable:
    """
    Load module from file.

    Parameters
    ----------
    file_name : str
        Path where the function source is located.
    handler : str
        Function name.

    Returns
    -------
    Callable
        Function.
    """
    mod_name = Path(file_name).stem
    spec = imputil.spec_from_file_location(mod_name, file_name)

    if spec is None:
        msg = "Error loading KFP pipeline source."
        LOGGER.exception(msg)
        raise RuntimeError(msg)

    module = imputil.module_from_spec(spec)
    spec.loader.exec_module(module)

    return _get_handler_extended(handler, namespaces=module)


def _get_handler_extended(
    handler_path: str,
    class_args: dict | None = None,
    namespaces: ModuleType | None = None,
) -> Callable:
    """
    Get function handler from [class_name::]handler string.

    Parameters
    ----------
    handler_path : str
        Path to the function ([class_name::]handler).
    class_args : dict
        Optional dict of class init kwargs.
    namespaces : ModuleType
        One or list of namespaces/modules to search the handler in.

    Returns
    -------
    Callable
        Function handler (callable)
    """
    if class_args is None:
        class_args = {}

    # Get function if class path is not provided
    # before the '::' separator
    if "::" not in handler_path:
        return _get_function_to_exec(handler_path, namespaces)

    # Get class if class path is provided
    splitted = handler_path.split("::")
    class_path = splitted[0].strip()
    handler_path = splitted[1].strip()
    class_object = _get_class(class_path, namespaces)

    # Initialize class
    try:
        instance = class_object(**class_args)
    except TypeError as e:
        raise TypeError(f"Failed to init class {class_path}\n args={class_args}") from e

    # Get handler from class attributes
    if not hasattr(instance, handler_path):
        raise ValueError(f"Handler ({handler_path}) specified but doesnt exist in class {class_path}")
    return getattr(instance, handler_path)


def _get_function_to_exec(function: str | Callable, namespace: ModuleType | None = None) -> Callable:
    """
    Return function callable object.

    Parameters
    ----------
    function : str | Callable
        Function name or function.
    namespace : ModuleType
        One or list of namespaces/modules to search the handler in.

    Returns
    -------
    Callable
        Function handler (callable)
    """
    if callable(function):
        return function

    function = function.strip()
    if function.startswith("("):
        if not function.endswith(")"):
            raise ValueError('function expression must start with "(" and end with ")"')
        return eval("lambda event: " + function[1:-1], {}, {})

    function_object = _search_in_namespaces(function, namespace)
    if function_object is not None:
        return function_object

    try:
        function_object = _create_function(function)
    except (ImportError, ValueError) as e:
        raise ImportError(f"State/function init failed, handler '{function}' not found") from e
    return function_object


def _search_in_namespaces(name: str, namespaces: ModuleType | None = None) -> Callable | None:
    """
    Search the class/function in a list of modules.

    Parameters
    ----------
    name : str
        Name of the class/function.
    namespaces : list
        List of modules.

    Returns
    -------
    object
        Class/function object.
    """
    if namespaces is None:
        return
    if not isinstance(namespaces, list):
        namespaces: list[ModuleType] = [namespaces]
    for namespace in namespaces:
        namespace = _module_to_namespace(namespace)
        if name in namespace:
            return namespace[name]


def _module_to_namespace(namespace: ModuleType) -> dict:
    """
    Convert module to namespace.

    Parameters
    ----------
    namespace : ModuleType
        Module to convert.

    Returns
    -------
    dict
        Namespace.
    """
    members = inspect.getmembers(namespace, lambda o: inspect.isfunction(o) or isinstance(o, type))
    return {key: mod for key, mod in members}


def _create_function(func: str) -> Callable:
    """
    Create a function from a package.module.function string.

    Parameters
    ----------
    func : str
        Function location.

    Returns
    -------
    Callable
        Function.
    """
    splits = func.split(".")
    pkg_module = ".".join(splits[:-1])
    cb_fname = splits[-1]
    pkg_module = __import__(pkg_module, fromlist=[cb_fname])
    function_ = getattr(pkg_module, cb_fname)
    return function_


def _get_class(class_name: str, namespace: ModuleType | None = None) -> type:
    """
    Return class object from class name string.

    Parameters
    ----------
    class_name : str
        Class name.
    namespace : ModuleType
        One or list of namespaces/modules to search the handler in.

    Returns
    -------
    type
        Class object.
    """
    if isinstance(class_name, type):
        return class_name

    class_object = _search_in_namespaces(class_name, namespace)
    if class_object is not None:
        return class_object

    try:
        class_object = _create_class(class_name)
    except (ImportError, ValueError) as e:
        raise ImportError(f"Failed to import {class_name}") from e
    return class_object


def _create_class(pkg_class: str) -> type:
    """
    Create a class from a package.module.class string.

    Parameters
    ----------
    pkg_class : str
        Class location. Example: mlflow.sklearn.SklearnModel.

    Returns
    -------
    type
        Class object.
    """
    splits = pkg_class.split(".")
    clfclass = splits[-1]
    pkg_module = splits[:-1]
    class_ = getattr(import_module(".".join(pkg_module)), clfclass)
    return class_
