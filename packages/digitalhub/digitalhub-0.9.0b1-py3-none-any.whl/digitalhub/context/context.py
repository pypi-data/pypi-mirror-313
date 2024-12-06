from __future__ import annotations

import typing
from pathlib import Path

if typing.TYPE_CHECKING:
    from digitalhub.entities.project._base.entity import Project


class Context:
    """
    Context class built forom a `Project` instance. It contains
    some information about the project, such as the project name,
    a client instance (local or non-local), the local context
    project path and information about client locality.
    """

    def __init__(self, project: Project) -> None:
        self.name = project.name
        self.client = project._client
        self.local = project._client.is_local()
        self.root = Path(project.spec.context)
        self.root.mkdir(parents=True, exist_ok=True)

        self.is_running: bool = False
        self._run_ctx: str = None

    def set_run(self, run_ctx: str) -> None:
        """
        Set run identifier.

        Parameters
        ----------
        run_ctx : str
            Run key.

        Returns
        -------
        None
        """
        self.is_running = True
        self._run_ctx = run_ctx

    def unset_run(self) -> None:
        """
        Unset run identifier.

        Returns
        -------
        None
        """
        self.is_running = False
        self._run_ctx = None

    def get_run_ctx(self) -> str:
        """
        Get run identifier.

        Returns
        -------
        str
            Run key.
        """
        return self._run_ctx
