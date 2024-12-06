from __future__ import annotations

import importlib
import importlib.metadata
import pkgutil
import re
from types import ModuleType

from digitalhub.factory.factory import factory


def import_module(package: str) -> ModuleType:
    """
    Import modules from package name.

    Parameters
    ----------
    package : str
        Package name.

    Returns
    -------
    ModuleType
        Module.
    """
    try:
        return importlib.import_module(package)
    except ModuleNotFoundError:
        raise ModuleNotFoundError(f"Package {package} not found.")
    except Exception as e:
        raise e


def list_runtimes() -> list[str]:
    """
    List installed runtimes for digitalhub.

    Returns
    -------
    list
        List of installed runtimes names.
    """
    pattern = r"digitalhub_runtime_.*"
    runtimes = []
    try:
        for _, name, _ in pkgutil.iter_modules():
            if re.match(pattern, name):
                runtimes.append(name)
        return runtimes
    except Exception:
        raise RuntimeError("Error listing installed runtimes.")


def register_runtimes_entities() -> None:
    """
    Register runtimes and related entities into registry.

    Returns
    -------
    None
    """
    for package in list_runtimes():
        module = import_module(package)
        entity_builders = getattr(module, "entity_builders")
        for entity_builder_tuple in entity_builders:
            kind, builder = entity_builder_tuple
            factory.add_entity_builder(kind, builder)

        runtime_builders = getattr(module, "runtime_builders")
        for runtime_builder_tuple in runtime_builders:
            kind, builder = runtime_builder_tuple
            factory.add_runtime_builder(kind, builder)


def register_entities() -> None:
    """
    Register layer and related entities into registry.

    Returns
    -------
    None
    """
    try:
        module = import_module("digitalhub.entities.builders")
        entities_builders_list = getattr(module, "entity_builders")
        for entity_builder_tuple in entities_builders_list:
            kind, builder = entity_builder_tuple
            factory.add_entity_builder(kind, builder)
    except Exception:
        raise
