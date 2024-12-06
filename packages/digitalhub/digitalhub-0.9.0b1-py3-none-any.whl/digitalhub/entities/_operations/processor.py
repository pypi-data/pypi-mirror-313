from __future__ import annotations

import typing

from digitalhub.client.api import get_client
from digitalhub.context.api import delete_context, get_context
from digitalhub.entities._commons.enums import ApiCategories, BackendOperations, EntityTypes, Relationship
from digitalhub.entities._commons.utils import get_project_from_key, parse_entity_key
from digitalhub.factory.api import build_entity_from_dict, build_entity_from_params
from digitalhub.utils.exceptions import ContextError, EntityAlreadyExistsError, EntityError, EntityNotExistsError
from digitalhub.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from digitalhub.client._base.client import Client
    from digitalhub.context.context import Context
    from digitalhub.entities._base.context.entity import ContextEntity
    from digitalhub.entities._base.executable.entity import ExecutableEntity
    from digitalhub.entities._base.material.entity import MaterialEntity
    from digitalhub.entities._base.project.entity import ProjectEntity
    from digitalhub.entities._base.unversioned.entity import UnversionedEntity


class OperationsProcessor:
    """
    Processor for Entity operations.

    This object interacts with the context, check the category of the object,
    and then calls the appropriate method to perform the requested operation.
    Operations can be CRUD, search, list, etc.
    """

    ##############################
    # CRUD base entity
    ##############################

    def _create_base_entity(
        self,
        client: Client,
        entity_type: str,
        entity_dict: dict,
        **kwargs,
    ) -> dict:
        """
        Create object in backend.

        Parameters
        ----------
        client : Client
            Client instance.
        entity_type : str
            Entity type.
        entity_dict : dict
            Object instance.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Object instance.
        """
        api = client.build_api(
            ApiCategories.BASE.value,
            BackendOperations.CREATE.value,
            entity_type=entity_type,
        )
        return client.create_object(api, entity_dict, **kwargs)

    def create_project_entity(
        self,
        _entity: ProjectEntity | None = None,
        **kwargs,
    ) -> ProjectEntity:
        """
        Create object in backend.

        Parameters
        ----------
        _entity : ProjectEntity
            Object instance.
        **kwargs : dict
            Parameters to pass to entity builder.

        Returns
        -------
        Project
            Object instance.
        """
        if _entity is not None:
            client = _entity._client
            obj = _entity
        else:
            client = get_client(kwargs.get("local"), kwargs.pop("config", None))
            obj = build_entity_from_params(**kwargs)
        ent = self._create_base_entity(client, obj.ENTITY_TYPE, obj.to_dict())
        ent["local"] = client.is_local()
        return build_entity_from_dict(ent)

    def _read_base_entity(
        self,
        client: Client,
        entity_type: str,
        entity_name: str,
        **kwargs,
    ) -> dict:
        """
        Read object from backend.

        Parameters
        ----------
        client : Client
            Client instance.
        entity_type : str
            Entity type.
        entity_name : str
            Entity name.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Object instance.
        """
        api = client.build_api(
            ApiCategories.BASE.value,
            BackendOperations.READ.value,
            entity_type=entity_type,
            entity_name=entity_name,
        )
        return client.read_object(api, **kwargs)

    def read_project_entity(
        self,
        entity_type: str,
        entity_name: str,
        **kwargs,
    ) -> ProjectEntity:
        """
        Read object from backend.

        Parameters
        ----------
        entity_type : str
            Entity type.
        entity_name : str
            Entity name.
        **kwargs : dict
            Parameters to pass to entity builder.

        Returns
        -------
        ProjectEntity
            Object instance.
        """
        client = get_client(kwargs.pop("local", False), kwargs.pop("config", None))
        obj = self._read_base_entity(client, entity_type, entity_name, **kwargs)
        obj["local"] = client.is_local()
        return build_entity_from_dict(obj)

    def import_project_entity(
        self,
        file: str,
        **kwargs,
    ) -> ProjectEntity:
        """
        Import object from a YAML file and create a new object into the backend.

        Parameters
        ----------
        file : str
            Path to YAML file.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        ProjectEntity
            Object instance.
        """
        client = get_client(kwargs.pop("local", False), kwargs.pop("config", None))
        obj: dict = read_yaml(file)
        obj["status"] = {}
        obj["local"] = client.is_local()
        ent: ProjectEntity = build_entity_from_dict(obj)

        try:
            self._create_base_entity(ent._client, ent.ENTITY_TYPE, ent.to_dict())
        except EntityAlreadyExistsError:
            raise EntityError(f"Entity {ent.name} already exists. If you want to update it, use load instead.")

        # Import related entities
        ent._import_entities(obj)
        ent.refresh()
        return ent

    def load_project_entity(
        self,
        file: str,
        **kwargs,
    ) -> ProjectEntity:
        """
        Load object from a YAML file and update an existing object into the backend.

        Parameters
        ----------
        file : str
            Path to YAML file.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        ProjectEntity
            Object instance.
        """
        client = get_client(kwargs.pop("local", False), kwargs.pop("config", None))
        obj: dict = read_yaml(file)
        obj["local"] = client.is_local()
        ent: ProjectEntity = build_entity_from_dict(obj)

        try:
            self._update_base_entity(ent._client, ent.ENTITY_TYPE, ent.name, ent.to_dict())
        except EntityNotExistsError:
            self._create_base_entity(ent._client, ent.ENTITY_TYPE, ent.to_dict())

        # Load related entities
        ent._load_entities(obj)
        ent.refresh()
        return ent

    def _list_base_entities(
        self,
        client: Client,
        entity_type: str,
        **kwargs,
    ) -> list[dict]:
        """
        List objects from backend.

        Parameters
        ----------
        client : Client
            Client instance.
        entity_type : str
            Entity type.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[dict]
            List of objects.
        """
        api = client.build_api(
            ApiCategories.BASE.value,
            BackendOperations.LIST.value,
            entity_type=entity_type,
        )
        return client.list_objects(api, **kwargs)

    def list_project_entities(
        self,
        entity_type: str,
        **kwargs,
    ) -> list[ProjectEntity]:
        """
        List objects from backend.

        Parameters
        ----------
        entity_type : str
            Entity type.
        **kwargs : dict
            Parameters to pass to API call.

        Returns
        -------
        list[ProjectEntity]
            List of objects.
        """
        client = get_client(kwargs.pop("local", False))
        objs = self._list_base_entities(client, entity_type, **kwargs)
        entities = []
        for obj in objs:
            obj["local"] = client.is_local()
            ent = build_entity_from_dict(obj)
            entities.append(ent)
        return entities

    def _update_base_entity(
        self,
        client: Client,
        entity_type: str,
        entity_name: str,
        entity_dict: dict,
        **kwargs,
    ) -> dict:
        """
        Update object method.

        Parameters
        ----------
        client : Client
            Client instance.
        entity_type : str
            Entity type.
        entity_name : str
            Entity name.
        entity_dict : dict
            Object instance.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Object instance.
        """
        api = client.build_api(
            ApiCategories.BASE.value,
            BackendOperations.UPDATE.value,
            entity_type=entity_type,
            entity_name=entity_name,
        )
        return client.update_object(api, entity_dict, **kwargs)

    def update_project_entity(
        self,
        entity_type: str,
        entity_name: str,
        entity_dict: dict,
        **kwargs,
    ) -> ProjectEntity:
        """
        Update object method.

        Parameters
        ----------
        entity_type : str
            Entity type.
        entity_name : str
            Entity name.
        entity_dict : dict
            Object instance.
        **kwargs : dict
            Parameters to pass to entity builder.

        Returns
        -------
        ProjectEntity
            Object instance.
        """
        client = get_client(kwargs.pop("local", False), kwargs.pop("config", None))
        obj = self._update_base_entity(client, entity_type, entity_name, entity_dict, **kwargs)
        obj["local"] = client.is_local()
        return build_entity_from_dict(obj)

    def _delete_base_entity(
        self,
        client: Client,
        entity_type: str,
        entity_name: str,
        **kwargs,
    ) -> dict:
        """
        Delete object method.

        Parameters
        ----------
        client : Client
            Client instance.
        entity_type : str
            Entity type.
        entity_name : str
            Entity name.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.
        """
        api = client.build_api(
            ApiCategories.BASE.value,
            BackendOperations.DELETE.value,
            entity_type=entity_type,
            entity_name=entity_name,
        )
        return client.delete_object(api, **kwargs)

    def delete_project_entity(
        self,
        entity_type: str,
        entity_name: str,
        **kwargs,
    ) -> dict:
        """
        Delete object method.

        Parameters
        ----------
        entity_type : str
            Entity type.
        entity_name : str
            Entity name.
        **kwargs : dict
            Parameters to pass to entity builder.

        Returns
        -------
        dict
            Response from backend.
        """
        kwargs = self._set_params(**kwargs)
        if cascade := kwargs.pop("cascade", None) is not None:
            kwargs["params"]["cascade"] = str(cascade).lower()
        if kwargs.pop("clean_context", True):
            delete_context(entity_name)

        client = get_client(kwargs.pop("local", False), kwargs.pop("config", None))
        return self._delete_base_entity(
            client,
            entity_type,
            entity_name,
            **kwargs,
        )

    def share_project_entity(
        self,
        entity_type: str,
        entity_name: str,
        **kwargs,
    ) -> None:
        """
        Share object method.

        Parameters
        ----------
        entity_type : str
            Entity type.
        entity_name : str
            Entity name.
        **kwargs : dict
            Parameters to pass to entity builder.

        Returns
        -------
        None
        """
        client = get_client(kwargs.pop("local", False), kwargs.pop("config", None))
        api = client.build_api(
            ApiCategories.BASE.value,
            BackendOperations.SHARE.value,
            entity_type=entity_type,
            entity_name=entity_name,
        )
        user = kwargs.pop("user")
        unshare = kwargs.pop("unshare", False)
        kwargs = self._set_params(**kwargs)

        # Unshare
        if unshare:
            users = client.read_object(api, **kwargs)
            for u in users:
                if u["user"] == user:
                    kwargs["params"]["id"] = u["id"]
                    client.delete_object(api, **kwargs)
                    break
            return

        # Share
        kwargs["params"]["user"] = user
        client.create_object(api, obj={}, **kwargs)

    ##############################
    # CRUD context entity
    ##############################

    def _create_context_entity(
        self,
        context: Context,
        entity_type: str,
        entity_dict: dict,
    ) -> dict:
        """
        Create object in backend.

        Parameters
        ----------
        context : Context
            Context instance.
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_dict : dict
            Object instance.

        Returns
        -------
        dict
            Object instance.
        """
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.CREATE.value,
            project=context.name,
            entity_type=entity_type,
        )
        return context.client.create_object(api, entity_dict)

    def create_context_entity(
        self,
        _entity: ContextEntity | None = None,
        **kwargs,
    ) -> dict:
        """
        Create object in backend.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to entity builder.

        Returns
        -------
        dict
            Object instance.
        """
        if _entity is not None:
            context = _entity._context()
            obj = _entity
        else:
            context = self._get_context(kwargs["project"])
            obj: ContextEntity = build_entity_from_params(**kwargs)
        new_obj = self._create_context_entity(context, obj.ENTITY_TYPE, obj.to_dict())
        return build_entity_from_dict(new_obj)

    def log_material_entity(
        self,
        **kwargs,
    ) -> MaterialEntity:
        """
        Create object in backend and upload file.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to entity builder.

        Returns
        -------
        MaterialEntity
            Object instance.
        """
        source = kwargs.pop("source")
        context = self._get_context(kwargs["project"])
        obj = build_entity_from_params(**kwargs)
        if context.is_running:
            obj.add_relationship(Relationship.PRODUCEDBY.value, obj.key, context.get_run_ctx())

        new_obj: MaterialEntity = self._create_context_entity(context, obj.ENTITY_TYPE, obj.to_dict())
        new_obj = build_entity_from_dict(new_obj)
        new_obj.upload(source)
        return new_obj

    def _read_context_entity(
        self,
        context: Context,
        identifier: str,
        entity_type: str | None = None,
        project: str | None = None,
        entity_id: str | None = None,
        **kwargs,
    ) -> dict:
        """
        Read object from backend.

        Parameters
        ----------
        context : Context
            Context instance.
        identifier : str
            Entity key (store://...) or entity name.
        entity_type : str
            Entity type.
        project : str
            Project name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Object instance.
        """
        if not identifier.startswith("store://"):
            if project is None or entity_type is None:
                raise ValueError("Project and entity type must be specified.")
            entity_name = identifier
        else:
            project, entity_type, _, entity_name, entity_id = parse_entity_key(identifier)

        kwargs = self._set_params(**kwargs)

        if entity_id is None:
            kwargs["params"]["name"] = entity_name
            api = context.client.build_api(
                ApiCategories.CONTEXT.value,
                BackendOperations.LIST.value,
                project=context.name,
                entity_type=entity_type,
            )
            return context.client.list_first_object(api, **kwargs)

        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.READ.value,
            project=context.name,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        return context.client.read_object(api, **kwargs)

    def read_context_entity(
        self,
        identifier: str,
        entity_type: str | None = None,
        project: str | None = None,
        entity_id: str | None = None,
        **kwargs,
    ) -> ContextEntity:
        """
        Read object from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        entity_type : str
            Entity type.
        project : str
            Project name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        VersionedEntity
            Object instance.
        """
        context = self._get_context_from_identifier(identifier, project)
        obj = self._read_context_entity(
            context,
            identifier,
            entity_type=entity_type,
            project=project,
            entity_id=entity_id,
            **kwargs,
        )
        return build_entity_from_dict(obj)

    def read_material_entity(
        self,
        identifier: str,
        entity_type: str | None = None,
        project: str | None = None,
        entity_id: str | None = None,
        **kwargs,
    ) -> MaterialEntity:
        """
        Read object from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        entity_type : str
            Entity type.
        project : str
            Project name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        MaterialEntity
            Object instance.
        """
        obj: MaterialEntity = self.read_context_entity(
            identifier,
            entity_type=entity_type,
            project=project,
            entity_id=entity_id,
            **kwargs,
        )
        obj._get_files_info()
        return obj

    def read_unversioned_entity(
        self,
        identifier: str,
        entity_type: str | None = None,
        project: str | None = None,
        entity_id: str | None = None,
        **kwargs,
    ) -> UnversionedEntity:
        """
        Read object from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        entity_type : str
            Entity type.
        project : str
            Project name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        UnversionedEntity
            Object instance.
        """
        if not identifier.startswith("store://"):
            entity_id = identifier
        return self.read_context_entity(
            identifier,
            entity_type=entity_type,
            project=project,
            entity_id=entity_id,
            **kwargs,
        )

    def import_context_entity(
        self,
        file: str,
    ) -> ContextEntity:
        """
        Import object from a YAML file and create a new object into the backend.

        Parameters
        ----------
        file : str
            Path to YAML file.

        Returns
        -------
        ContextEntity
            Object instance.
        """
        dict_obj: dict = read_yaml(file)
        dict_obj["status"] = {}
        context = self._get_context(dict_obj["project"])
        obj = build_entity_from_dict(dict_obj)
        try:
            self._create_context_entity(context, obj.ENTITY_TYPE, obj.to_dict())
        except EntityAlreadyExistsError:
            raise EntityError(f"Entity {obj.name} already exists. If you want to update it, use load instead.")
        return obj

    def import_executable_entity(
        self,
        file: str,
    ) -> ExecutableEntity:
        """
        Import object from a YAML file and create a new object into the backend.

        Parameters
        ----------
        file : str
            Path to YAML file.

        Returns
        -------
        ExecutableEntity
            Object instance.
        """
        dict_obj: dict | list[dict] = read_yaml(file)
        if isinstance(dict_obj, list):
            exec_dict = dict_obj[0]
            exec_dict["status"] = {}
            tsk_dicts = []
            for i in dict_obj[1:]:
                i["status"] = {}
                tsk_dicts.append(i)
        else:
            exec_dict = dict_obj
            tsk_dicts = []

        context = self._get_context(exec_dict["project"])
        obj: ExecutableEntity = build_entity_from_dict(exec_dict)
        try:
            self._create_context_entity(context, obj.ENTITY_TYPE, obj.to_dict())
        except EntityAlreadyExistsError:
            raise EntityError(f"Entity {obj.name} already exists. If you want to update it, use load instead.")

        obj.import_tasks(tsk_dicts)

        return obj

    def load_context_entity(
        self,
        file: str,
    ) -> ContextEntity:
        """
        Load object from a YAML file and update an existing object into the backend.

        Parameters
        ----------
        file : str
            Path to YAML file.

        Returns
        -------
        ContextEntity
            Object instance.
        """
        dict_obj: dict = read_yaml(file)
        context = self._get_context(dict_obj["project"])
        obj: ContextEntity = build_entity_from_dict(dict_obj)
        try:
            self._update_context_entity(context, obj.ENTITY_TYPE, obj.id, obj.to_dict())
        except EntityNotExistsError:
            self._create_context_entity(context, obj.ENTITY_TYPE, obj.to_dict())
        return obj

    def load_executable_entity(
        self,
        file: str,
    ) -> ExecutableEntity:
        """
        Load object from a YAML file and update an existing object into the backend.

        Parameters
        ----------
        file : str
            Path to YAML file.

        Returns
        -------
        ExecutableEntity
            Object instance.
        """
        dict_obj: dict | list[dict] = read_yaml(file)
        if isinstance(dict_obj, list):
            exec_dict = dict_obj[0]
            tsk_dicts = dict_obj[1:]
        else:
            exec_dict = dict_obj
            tsk_dicts = []

        context = self._get_context(exec_dict["project"])
        obj: ExecutableEntity = build_entity_from_dict(exec_dict)

        try:
            self._update_context_entity(context, obj.ENTITY_TYPE, obj.id, obj.to_dict())
        except EntityNotExistsError:
            self._create_context_entity(context, obj.ENTITY_TYPE, obj.to_dict())
        obj.import_tasks(tsk_dicts)
        return obj

    def _read_context_entity_versions(
        self,
        context: Context,
        identifier: str,
        entity_type: str | None = None,
        project: str | None = None,
        **kwargs,
    ) -> list[dict]:
        """
        Get all versions object from backend.

        Parameters
        ----------
        context : Context
            Context instance.
        identifier : str
            Entity key (store://...) or entity name.
        entity_type : str
            Entity type.
        project : str
            Project name.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[dict]
            Object instances.
        """
        if not identifier.startswith("store://"):
            if project is None or entity_type is None:
                raise ValueError("Project and entity type must be specified.")
            entity_name = identifier
        else:
            project, entity_type, _, entity_name, _ = parse_entity_key(identifier)

        kwargs = self._set_params(**kwargs)
        kwargs["params"]["name"] = entity_name
        kwargs["params"]["versions"] = "all"

        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.LIST.value,
            project=context.name,
            entity_type=entity_type,
        )
        return context.client.list_objects(api, **kwargs)

    def read_context_entity_versions(
        self,
        identifier: str,
        entity_type: str | None = None,
        project: str | None = None,
        **kwargs,
    ) -> list[ContextEntity]:
        """
        Read object versions from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        entity_type : str
            Entity type.
        project : str
            Project name.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[ContextEntity]
            List of object instances.
        """
        context = self._get_context_from_identifier(identifier, project)
        obj = self._read_context_entity_versions(
            context,
            identifier,
            entity_type=entity_type,
            project=project,
            **kwargs,
        )
        return [build_entity_from_dict(o) for o in obj]

    def read_material_entity_versions(
        self,
        identifier: str,
        entity_type: str | None = None,
        project: str | None = None,
        **kwargs,
    ) -> list[MaterialEntity]:
        """
        Read object versions from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        entity_type : str
            Entity type.
        project : str
            Project name.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[MaterialEntity]
            List of object instances.
        """
        context = self._get_context_from_identifier(identifier, project)
        objs = self._read_context_entity_versions(
            context,
            identifier,
            entity_type=entity_type,
            project=project,
            **kwargs,
        )
        objects = []
        for o in objs:
            entity: MaterialEntity = build_entity_from_dict(o)
            entity._get_files_info()
            objects.append(entity)
        return objects

    def _list_context_entities(
        self,
        context: Context,
        entity_type: str,
        **kwargs,
    ) -> list[dict]:
        """
        List objects from backend.

        Parameters
        ----------
        context : Context
            Context instance.
        entity_type : str
            Entity type.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[dict]
            List of objects.
        """
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.LIST.value,
            project=context.name,
            entity_type=entity_type,
        )
        return context.client.list_objects(api, **kwargs)

    def list_context_entities(
        self,
        project: str,
        entity_type: str,
        **kwargs,
    ) -> list[ContextEntity]:
        """
        List all latest version objects from backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[ContextEntity]
            List of object instances.
        """
        context = self._get_context(project)
        objs = self._list_context_entities(context, entity_type, **kwargs)
        return [build_entity_from_dict(obj) for obj in objs]

    def list_material_entities(
        self,
        project: str,
        entity_type: str,
        **kwargs,
    ) -> list[MaterialEntity]:
        """
        List all latest version objects from backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[MaterialEntity]
            List of object instances.
        """
        context = self._get_context(project)
        objs = self._list_context_entities(context, entity_type, **kwargs)
        objects = []
        for o in objs:
            entity: MaterialEntity = build_entity_from_dict(o)
            entity._get_files_info()
            objects.append(entity)
        return objects

    def _update_context_entity(
        self,
        context: Context,
        entity_type: str,
        entity_id: str,
        entity_dict: dict,
        **kwargs,
    ) -> dict:
        """
        Update object. Note that object spec are immutable.

        Parameters
        ----------
        context : Context
            Context instance.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        entity_dict : dict
            Entity dictionary.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.
        """
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.UPDATE.value,
            project=context.name,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        return context.client.update_object(api, entity_dict, **kwargs)

    def update_context_entity(
        self,
        project: str,
        entity_type: str,
        entity_id: str,
        entity_dict: dict,
        **kwargs,
    ) -> ContextEntity:
        """
        Update object. Note that object spec are immutable.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        entity_dict : dict
            Entity dictionary.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        ContextEntity
            Object instance.
        """
        context = self._get_context(project)
        obj = self._update_context_entity(
            context,
            entity_type,
            entity_id,
            entity_dict,
            **kwargs,
        )
        return build_entity_from_dict(obj)

    def _delete_context_entity(
        self,
        context: Context,
        identifier: str,
        entity_type: str | None = None,
        project: str | None = None,
        entity_id: str | None = None,
        **kwargs,
    ) -> dict:
        """
        Delete object from backend.

        Parameters
        ----------
        context : Context
            Context instance.
        identifier : str
            Entity key (store://...) or entity name.
        entity_type : str
            Entity type.
        project : str
            Project name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.
        """
        if not identifier.startswith("store://"):
            if project is None or entity_type is None:
                raise ValueError("Project must be provided.")
            entity_name = identifier
        else:
            project, _, _, entity_name, entity_id = parse_entity_key(identifier)

        kwargs = self._set_params(**kwargs)
        if cascade := kwargs.pop("cascade", None) is not None:
            kwargs["params"]["cascade"] = str(cascade).lower()

        delete_all_versions: bool = kwargs.pop("delete_all_versions", False)

        if not delete_all_versions and entity_id is None:
            raise ValueError(
                "If `delete_all_versions` is False, `entity_id` must be provided, either as an argument or in key `identifier`."
            )

        if delete_all_versions:
            api = context.client.build_api(
                ApiCategories.CONTEXT.value,
                BackendOperations.LIST.value,
                project=context.name,
                entity_type=entity_type,
            )
            kwargs["params"]["name"] = entity_name
        else:
            api = context.client.build_api(
                ApiCategories.CONTEXT.value,
                BackendOperations.DELETE.value,
                project=context.name,
                entity_type=entity_type,
                entity_id=entity_id,
            )
        return context.client.delete_object(api, **kwargs)

    def delete_context_entity(
        self,
        identifier: str,
        project: str | None = None,
        entity_type: str | None = None,
        entity_id: str | None = None,
        **kwargs,
    ) -> dict:
        """
        Delete object from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.
        """
        context = self._get_context_from_identifier(identifier, project)
        return self._delete_context_entity(
            context,
            identifier,
            entity_type,
            context.name,
            entity_id,
            **kwargs,
        )

    ##############################
    # Context entity operations
    ##############################

    def read_secret_data(
        self,
        project: str,
        entity_type: str,
        **kwargs,
    ) -> dict:
        """
        Get data from backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.
        """
        context = self._get_context(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.DATA.value,
            project=context.name,
            entity_type=entity_type,
        )
        return context.client.read_object(api, **kwargs)

    def update_secret_data(
        self,
        project: str,
        entity_type: str,
        data: dict,
        **kwargs,
    ) -> None:
        """
        Set data in backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        data : dict
            Data dictionary.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        None
        """
        context = self._get_context(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.DATA.value,
            project=context.name,
            entity_type=entity_type,
        )
        return context.client.update_object(api, data, **kwargs)

    def read_run_logs(
        self,
        project: str,
        entity_type: str,
        entity_id: str,
        **kwargs,
    ) -> dict:
        """
        Get logs from backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.
        """
        context = self._get_context(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.LOGS.value,
            project=context.name,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        return context.client.read_object(api, **kwargs)

    def stop_run(
        self,
        project: str,
        entity_type: str,
        entity_id: str,
        **kwargs,
    ) -> None:
        """
        Stop object in backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        None
        """
        context = self._get_context(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.STOP.value,
            project=context.name,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        return context.client.create_object(api, **kwargs)

    def resume_run(
        self,
        project: str,
        entity_type: str,
        entity_id: str,
        **kwargs,
    ) -> None:
        """
        Resume object in backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        None
        """
        context = self._get_context(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.RESUME.value,
            project=context.name,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        return context.client.create_object(api, **kwargs)

    def read_files_info(
        self,
        project: str,
        entity_type: str,
        entity_id: str,
        **kwargs,
    ) -> list[dict]:
        """
        Get files info from backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[dict]
            Response from backend.
        """
        context = self._get_context(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.FILES.value,
            project=context.name,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        return context.client.read_object(api, **kwargs)

    def update_files_info(
        self,
        project: str,
        entity_type: str,
        entity_id: str,
        entity_list: list[dict],
        **kwargs,
    ) -> None:
        """
        Get files info from backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        entity_list : list[dict]
            Entity list.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        None
        """
        context = self._get_context(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.FILES.value,
            project=context.name,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        return context.client.update_object(api, entity_list, **kwargs)

    def _search(
        self,
        project: str,
        **kwargs,
    ) -> dict:
        """
        Search in backend.

        Parameters
        ----------
        project : str
            Project name.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.
        """
        context = self._get_context(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.SEARCH.value,
            project=context.name,
        )
        return context.client.read_object(api, **kwargs)

    def search_entity(
        self,
        project: str,
        query: str | None = None,
        entity_types: list[str] | None = None,
        name: str | None = None,
        kind: str | None = None,
        created: str | None = None,
        updated: str | None = None,
        description: str | None = None,
        labels: list[str] | None = None,
        **kwargs,
    ) -> list[ContextEntity]:
        """
        Search objects from backend.

        Parameters
        ----------
        project : str
            Project name.
        query : str
            Search query.
        entity_types : list[str]
            Entity types.
        name : str
            Entity name.
        kind : str
            Entity kind.
        created : str
            Entity creation date.
        updated : str
            Entity update date.
        description : str
            Entity description.
        labels : list[str]
            Entity labels.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[ContextEntity]
            List of object instances.
        """
        context = self._get_context(project)

        kwargs = self._set_params(**kwargs)

        # Add search query
        if query is not None:
            kwargs["params"]["q"] = query

        # Add search filters
        fq = []

        # Entity types
        if entity_types is not None:
            if len(entity_types) == 1:
                entity_types = entity_types[0]
            else:
                entity_types = " OR ".join(entity_types)
            fq.append(f"type:({entity_types})")

        # Name
        if name is not None:
            fq.append(f'metadata.name:"{name}"')

        # Kind
        if kind is not None:
            fq.append(f'kind:"{kind}"')

        # Time
        created = created if created is not None else "*"
        updated = updated if updated is not None else "*"
        fq.append(f"metadata.updated:[{created} TO {updated}]")

        # Description
        if description is not None:
            fq.append(f'metadata.description:"{description}"')

        # Labels
        if labels is not None:
            if len(labels) == 1:
                labels = labels[0]
            else:
                labels = " AND ".join(labels)
            fq.append(f"metadata.labels:({labels})")

        # Add filters
        kwargs["params"]["fq"] = fq

        objs = self._search(context, **kwargs)
        return objs
        return [build_entity_from_dict(obj) for obj in objs]

    ##############################
    # Helpers
    ##############################

    @staticmethod
    def _set_params(**kwargs) -> dict:
        """
        Format params parameter.

        Parameters
        ----------
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        dict
            Parameters with initialized params.
        """
        if not kwargs:
            kwargs = {}
        if "params" not in kwargs:
            kwargs["params"] = {}
        return kwargs

    def _get_context_from_identifier(
        self,
        identifier: str,
        project: str | None = None,
    ) -> Context:
        """
        Get context from project.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        project : str
            Project name.

        Returns
        -------
        Context
            Context.
        """
        if not identifier.startswith("store://"):
            if project is None:
                raise EntityError("Specify project if you do not specify entity key.")
        else:
            project = get_project_from_key(identifier)

        return self._get_context(project)

    def _get_context(
        self,
        project: str,
    ) -> Context:
        """
        Check if the given project is in the context.
        Otherwise try to get the project from remote.
        Finally return the client.

        Parameters
        ----------
        project : str
            Project name.

        Returns
        -------
        Context
            Context.
        """
        try:
            return get_context(project)
        except ContextError:
            return self._get_context_from_remote(project)

    def _get_context_from_remote(
        self,
        project: str,
    ) -> Client:
        """
        Get context from remote.

        Parameters
        ----------
        project : str
            Project name.

        Returns
        -------
        Client
            Client.
        """
        try:
            client = get_client()
            obj = self._read_base_entity(client, EntityTypes.PROJECT.value, project)
            build_entity_from_dict(obj)
            return get_context(project)
        except EntityNotExistsError:
            raise ContextError(f"Project '{project}' not found.")


processor = OperationsProcessor()
