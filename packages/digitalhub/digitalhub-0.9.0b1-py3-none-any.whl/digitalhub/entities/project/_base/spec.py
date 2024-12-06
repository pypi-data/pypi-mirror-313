from __future__ import annotations

from digitalhub.entities._base.entity.spec import Spec, SpecValidator


class ProjectSpec(Spec):
    """
    ProjectSpec specifications.
    """

    def __init__(
        self,
        context: str | None = None,
        functions: list | None = None,
        artifacts: list | None = None,
        workflows: list | None = None,
        dataitems: list | None = None,
        models: list | None = None,
        **kwargs,
    ) -> None:
        self.context = context if context is not None else "./"
        self.functions = functions if functions is not None else []
        self.artifacts = artifacts if artifacts is not None else []
        self.workflows = workflows if workflows is not None else []
        self.dataitems = dataitems if dataitems is not None else []
        self.models = models if models is not None else []


class ProjectValidator(SpecValidator):
    """
    ProjectValidator validator.
    """

    context: str = None
    """The project's context."""

    functions: list = None
    """List of project's functions."""

    artifacts: list = None
    """List of project's artifacts."""

    workflows: list = None
    """List of project's workflows."""

    dataitems: list = None
    """List of project's dataitems."""

    models: list = None
    """List of project's models."""
