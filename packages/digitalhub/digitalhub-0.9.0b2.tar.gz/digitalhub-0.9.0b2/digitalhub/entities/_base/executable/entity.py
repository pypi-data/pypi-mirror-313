from __future__ import annotations

import typing

from digitalhub.entities._base.versioned.entity import VersionedEntity
from digitalhub.entities._commons.enums import EntityTypes
from digitalhub.entities._operations.processor import processor
from digitalhub.entities.run.crud import delete_run, get_run, list_runs
from digitalhub.entities.task.crud import delete_task
from digitalhub.factory.api import build_entity_from_dict, build_entity_from_params
from digitalhub.utils.exceptions import EntityAlreadyExistsError, EntityError

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata
    from digitalhub.entities._base.entity.spec import Spec
    from digitalhub.entities._base.entity.status import Status
    from digitalhub.entities.run._base.entity import Run
    from digitalhub.entities.task._base.entity import Task


class ExecutableEntity(VersionedEntity):
    """
    A class representing an entity that can be executed.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: Spec,
        status: Status,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        # Initialize tasks
        self._tasks: dict[str, Task] = {}

    ##############################
    #  Helpers
    ##############################

    def _get_executable_string(self) -> str:
        """
        Get executable string.

        Returns
        -------
        str
            Executable string.
        """
        return f"{self.kind}://{self.project}/{self.name}:{self.id}"

    ##############################
    #  Tasks
    ##############################

    def _get_or_create_task(self, kind: str) -> Task:
        """
        Get or create task.

        Parameters
        ----------
        kind : str
            Kind the object.

        Returns
        -------
        Task
            Task.
        """
        if self._tasks.get(kind) is None:
            try:
                self._tasks[kind] = self.get_task(kind)
            except EntityError:
                self._tasks[kind] = self.new_task(kind)
        return self._tasks[kind]

    def import_tasks(self, tasks: list[dict]) -> None:
        """
        Import tasks from yaml.

        Parameters
        ----------
        tasks : list[dict]
            List of tasks to import.

        Returns
        -------
        None
        """
        # Loop over tasks list, in the case where the function
        # is imported from local file.
        for task in tasks:
            # If task is not a dictionary, skip it
            if not isinstance(task, dict):
                continue

            # Create a new object from dictionary.
            # the form in which tasks are stored in function
            # status
            task_obj = build_entity_from_dict(task)

            # Try to save it in backend to been able to use
            # it for launching runs. In fact, tasks must be
            # persisted in backend to be able to launch runs.
            # Ignore if task already exists
            try:
                task_obj.save()
            except EntityAlreadyExistsError:
                pass

            # Set task if function is the same. Overwrite
            # status task dict with the new task object
            if task_obj.spec.function == self._get_executable_string():
                self._tasks[task_obj.kind] = task_obj

    def new_task(self, task_kind: str, **kwargs) -> Task:
        """
        Create new task. If the task already exists, update it.

        Parameters
        ----------
        task_kind : str
            Kind the object.
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        Task
            New task.
        """
        self._raise_if_exists(task_kind)

        if kwargs is None:
            kwargs = {}

        # Override kwargs
        kwargs["project"] = self.project
        kwargs[self.ENTITY_TYPE] = self._get_executable_string()
        kwargs["kind"] = task_kind

        # Create object instance
        task = build_entity_from_params(**kwargs)
        task.save()

        self._tasks[task_kind] = task
        return task

    def get_task(self, kind: str) -> Task:
        """
        Get task.

        Parameters
        ----------
        kind : str
            Kind the object.

        Returns
        -------
        Task
            Task.

        Raises
        ------
        EntityError
            If task is not created.
        """
        try:
            return self._tasks[kind]
        except KeyError:
            resp = self._get_task_from_backend(kind)
            if not resp:
                raise EntityError(f"Task {kind} is not created")
            self._tasks[kind] = resp[0]
            return self._tasks[kind]

    def update_task(self, kind: str, **kwargs) -> Task:
        """
        Update task.

        Parameters
        ----------
        kind : str
            Kind the object.
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        Task
            Task.
        """
        self._raise_if_not_exists(kind)

        if kwargs is None:
            kwargs = {}

        # Update kwargs
        kwargs["project"] = self.project
        kwargs["kind"] = kind
        kwargs[self.ENTITY_TYPE] = self._get_executable_string()
        kwargs["uuid"] = self._tasks[kind].id

        # Update task
        task = build_entity_from_params(**kwargs)
        task.save(update=True)
        self._tasks[kind] = task
        return task

    def delete_task(self, kind: str, cascade: bool = True) -> dict:
        """
        Delete task.

        Parameters
        ----------
        kind : str
            Kind the object.
        cascade : bool
            Flag to determine if cascade deletion must be performed.

        Returns
        -------
        dict
            Response from backend.
        """
        resp = delete_task(self._tasks[kind].key, cascade=cascade)
        self._tasks.pop(kind, None)
        return resp

    def _get_task_from_backend(self, kind: str) -> list:
        """
        List tasks from backend filtered by function and kind.

        Parameters
        ----------
        kind : str
            Kind the object.

        Returns
        -------
        list
            Response from backend.
        """
        params = {self.ENTITY_TYPE: self._get_executable_string(), "kind": kind}
        return processor.list_context_entities(self.project, EntityTypes.TASK.value, params=params)

    def _check_task_in_backend(self, kind: str) -> bool:
        """
        Check if task exists in backend.

        Parameters
        ----------
        kind : str
            Kind the object.

        Returns
        -------
        bool
            Flag to determine if task exists in backend.
        """
        resp = self._get_task_from_backend(kind)
        if not resp:
            return False
        return True

    def _raise_if_exists(self, kind: str) -> None:
        """
        Raise error if task is created.

        Parameters
        ----------
        kind : str
            Kind the object.

        Returns
        -------
        None

        Raises
        ------
        EntityError
            If task already exists.
        """
        if self._check_task_in_backend(kind):
            raise EntityError(f"Task '{kind}' already exists.")

    def _raise_if_not_exists(self, kind: str) -> None:
        """
        Raise error if task is not created.

        Parameters
        ----------
        kind : str
            Kind the object.

        Returns
        -------
        None

        Raises
        ------
        EntityError
            If task does not exist.
        """
        if self._tasks.get(kind) is None:
            raise EntityError(f"Task '{kind}' does not exist.")

    ##############################
    #  Runs
    ##############################

    def get_run(
        self,
        identifier: str,
        **kwargs,
    ) -> Run:
        """
        Get object from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Run
            Object instance.

        Examples
        --------
        Using entity key:
        >>> obj = executable.get_run("store://my-secret-key")

        Using entity ID:
        >>> obj = executable.get_run("123")
        """
        obj = get_run(
            identifier=identifier,
            project=self.project,
            **kwargs,
        )
        self.refresh()
        return obj

    def list_runs(self, **kwargs) -> list[Run]:
        """
        List all runs from backend.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[Run]
            List of object instances.

        Examples
        --------
        >>> objs = executable.list_runs()
        """
        if kwargs is None:
            kwargs = {}
        kwargs["params"] = {self.ENTITY_TYPE: self._get_executable_string()}
        return list_runs(self.project, **kwargs)

    def delete_run(
        self,
        identifier: str,
        **kwargs,
    ) -> None:
        """
        Delete run from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.

        Examples
        --------
        >>> executable.delete_run("store://my-run-key")

        """
        delete_run(
            identifier=identifier,
            project=self.project,
            **kwargs,
        )
