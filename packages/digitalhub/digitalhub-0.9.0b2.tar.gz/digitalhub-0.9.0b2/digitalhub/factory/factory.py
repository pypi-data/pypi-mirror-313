from __future__ import annotations

import typing

from digitalhub.utils.exceptions import BuilderError

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.builder import EntityBuilder
    from digitalhub.entities._base.entity.entity import Entity
    from digitalhub.entities._base.entity.metadata import Metadata
    from digitalhub.entities._base.entity.spec import Spec
    from digitalhub.entities._base.entity.status import Status
    from digitalhub.entities._base.runtime_entity.builder import RuntimeEntityBuilder
    from digitalhub.runtimes._base import Runtime
    from digitalhub.runtimes.builder import RuntimeBuilder


class Factory:
    """
    Factory class for building entities and runtimes.
    """

    def __init__(self):
        self._entity_builders: dict[str, EntityBuilder | RuntimeEntityBuilder] = {}
        self._runtime_builders: dict[str, RuntimeBuilder] = {}

    def add_entity_builder(self, name: str, builder: EntityBuilder | RuntimeEntityBuilder) -> None:
        """
        Add a builder to the factory.

        Parameters
        ----------
        name : str
            Builder name.
        builder : EntityBuilder
            Builder object.

        Returns
        -------
        None
        """
        if name in self._entity_builders:
            raise BuilderError(f"Builder {name} already exists.")
        self._entity_builders[name] = builder()

    def add_runtime_builder(self, name: str, builder: RuntimeBuilder) -> None:
        """
        Add a builder to the factory.

        Parameters
        ----------
        name : str
            Builder name.
        builder : RuntimeBuilder
            Builder object.

        Returns
        -------
        None
        """
        if name in self._runtime_builders:
            raise BuilderError(f"Builder {name} already exists.")
        self._runtime_builders[name] = builder()

    def build_entity_from_params(self, kind_to_build_from: str, **kwargs) -> Entity:
        """
        Build an entity from parameters.

        Parameters
        ----------
        kind_to_build_from : str
            Entity type.
        **kwargs
            Entity parameters.

        Returns
        -------
        Entity
            Entity object.
        """
        return self._entity_builders[kind_to_build_from].build(**kwargs)

    def build_entity_from_dict(self, kind_to_build_from: str, obj: dict) -> Entity:
        """
        Build an entity from a dictionary.

        Parameters
        ----------
        kind_to_build_from : str
            Entity type.
        dict_data : dict
            Dictionary with entity data.

        Returns
        -------
        Entity
            Entity object.
        """
        return self._entity_builders[kind_to_build_from].from_dict(obj)

    def build_spec(self, kind_to_build_from: str, **kwargs) -> Spec:
        """
        Build an entity spec.

        Parameters
        ----------
        kind_to_build_from : str
            Entity type.

        Returns
        -------
        Spec
            Spec object.
        """
        return self._entity_builders[kind_to_build_from].build_spec(**kwargs)

    def build_metadata(self, kind_to_build_from: str, **kwargs) -> Metadata:
        """
        Build an entity metadata.

        Parameters
        ----------
        kind_to_build_from : str
            Entity type.

        Returns
        -------
        Metadata
            Metadata object.
        """
        return self._entity_builders[kind_to_build_from].build_metadata(**kwargs)

    def build_status(self, kind_to_build_from: str, **kwargs) -> Status:
        """
        Build an entity status.

        Parameters
        ----------
        kind_to_build_from : str
            Entity type.

        Returns
        -------
        Status
            Status object.
        """
        return self._entity_builders[kind_to_build_from].build_status(**kwargs)

    def build_runtime(self, kind_to_build_from: str, project: str) -> Runtime:
        """
        Build a runtime.

        Parameters
        ----------
        kind_to_build_from : str
            Runtime type.
        project : str
            Project name.

        Returns
        -------
        Runtime
            Runtime object.
        """
        return self._runtime_builders[kind_to_build_from].build(project=project)

    def get_entity_type_from_kind(self, kind: str) -> str:
        """
        Get entity type from builder.

        Parameters
        ----------
        kind : str
            Entity type.

        Returns
        -------
        str
            Entity type.
        """
        return self._entity_builders[kind].get_entity_type()

    def get_executable_kind(self, kind: str) -> str:
        """
        Get executable kind.

        Parameters
        ----------
        kind : str
            Kind.

        Returns
        -------
        str
            Executable kind.
        """
        return self._entity_builders[kind].get_executable_kind()

    def get_action_from_task_kind(self, kind: str, task_kind: str) -> str:
        """
        Get action from task.

        Parameters
        ----------
        kind : str
            Kind.
        task_kind : str
            Task kind.

        Returns
        -------
        str
            Action.
        """
        return self._entity_builders[kind].get_action_from_task_kind(task_kind)

    def get_task_kind_from_action(self, kind: str, action: str) -> list[str]:
        """
        Get task kinds from action.

        Parameters
        ----------
        kind : str
            Kind.
        action : str
            Action.

        Returns
        -------
        list[str]
            Task kinds.
        """
        return self._entity_builders[kind].get_task_kind_from_action(action)

    def get_run_kind(self, kind: str) -> str:
        """
        Get run kind.

        Parameters
        ----------
        kind : str
            Kind.

        Returns
        -------
        str
            Run kind.
        """
        return self._entity_builders[kind].get_run_kind()

    def get_all_kinds(self, kind: str) -> list[str]:
        """
        Get all kinds.

        Parameters
        ----------
        kind : str
            Kind.

        Returns
        -------
        list[str]
            All kinds.
        """
        return self._entity_builders[kind].get_all_kinds()


factory = Factory()
