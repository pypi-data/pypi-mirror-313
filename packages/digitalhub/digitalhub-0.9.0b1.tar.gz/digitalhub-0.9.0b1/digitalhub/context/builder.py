from __future__ import annotations

import typing

from digitalhub.context.context import Context
from digitalhub.utils.exceptions import ContextError

if typing.TYPE_CHECKING:
    from digitalhub.entities.project._base.entity import Project


class ContextBuilder:
    """
    ContextBuilder class.
    It implements the builder pattern to create a context instance.
    It allows to use multiple projects as context at the same time
    by adding them to the _instances registry with their name.
    """

    def __init__(self) -> None:
        self._instances: dict[str, Context] = {}

    def build(self, project_object: Project, overwrite: bool = False) -> None:
        """
        Add a project as context.

        Parameters
        ----------
        project_object : Project
            The project to add.
        overwrite : bool
            If True, the project will be overwritten if it already exists.

        Returns
        -------
        None
        """
        if (project_object.name not in self._instances) or overwrite:
            self._instances[project_object.name] = Context(project_object)

    def get(self, project: str) -> Context:
        """
        Get a context from project name if it exists.

        Parameters
        ----------
        project : str
            The project name.

        Returns
        -------
        Context
            The project context.

        Raises
        ------
        ValueError
            If the project is not in the context.
        """
        try:
            return self._instances[project]
        except KeyError:
            raise ContextError(f"Context '{project}' not found. Get or create a project named '{project}'.")

    def remove(self, project: str) -> None:
        """
        Remove a project from the context.

        Parameters
        ----------
        project : str
            The project name.

        Returns
        -------
        None
        """
        self._instances.pop(project, None)


context_builder = ContextBuilder()
