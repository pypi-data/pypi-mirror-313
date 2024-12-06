from __future__ import annotations

import typing
from pathlib import Path

from digitalhub.client.api import get_client
from digitalhub.context.api import build_context
from digitalhub.entities._base.entity.entity import Entity
from digitalhub.entities._commons.enums import EntityTypes
from digitalhub.entities._operations.processor import processor
from digitalhub.factory.api import build_entity_from_dict
from digitalhub.utils.exceptions import BackendError, EntityAlreadyExistsError, EntityError
from digitalhub.utils.generic_utils import get_timestamp
from digitalhub.utils.io_utils import write_yaml
from digitalhub.utils.uri_utils import has_local_scheme

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.context.entity import ContextEntity
    from digitalhub.entities._base.entity.metadata import Metadata
    from digitalhub.entities._base.entity.spec import Spec
    from digitalhub.entities._base.entity.status import Status


class ProjectEntity(Entity):
    """
    Base entity for Project entity.
    Used to abstract a bit by handling I/O CRUD.
    """

    def __init__(
        self,
        name: str,
        kind: str,
        metadata: Metadata,
        spec: Spec,
        status: Status,
        user: str | None = None,
        local: bool = False,
    ) -> None:
        super().__init__(kind, metadata, spec, status, user)
        self.id = name
        self.name = name
        self.key = f"store://{name}"

        self._obj_attr.extend(["id", "name"])

        # Set client
        self._client = get_client(local)

        # Set context
        build_context(self)

    ##############################
    #  Save / Refresh / Export
    ##############################

    def save(self, update: bool = False) -> ProjectEntity:
        """
        Save entity into backend.

        Parameters
        ----------
        update : bool
            If True, the object will be updated.

        Returns
        -------
        Project
            Entity saved.
        """
        if update:
            if self._client.is_local():
                self.metadata.updated = get_timestamp()
            new_obj = processor.update_project_entity(
                entity_type=self.ENTITY_TYPE,
                entity_name=self.name,
                entity_dict=self.to_dict(),
                local=self._client.is_local(),
            )
        else:
            new_obj = processor.create_project_entity(_entity=self)
        self._update_attributes(new_obj)
        return self

    def refresh(self) -> ProjectEntity:
        """
        Refresh object from backend.

        Returns
        -------
        Project
            Project object.
        """
        new_obj = processor.read_project_entity(
            entity_type=self.ENTITY_TYPE,
            entity_name=self.name,
            local=self._client.is_local(),
        )
        self._update_attributes(new_obj)
        return self

    def search_entity(
        self,
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
        objs = processor.search_entity(
            self.name,
            query=query,
            entity_types=entity_types,
            name=name,
            kind=kind,
            created=created,
            updated=updated,
            description=description,
            labels=labels,
            **kwargs,
        )
        self.refresh()
        return objs

    def export(self) -> str:
        """
        Export object as a YAML file in the context folder.
        If the objects are not embedded, the objects are exported as a YAML file.

        Returns
        -------
        str
            Exported filepath.
        """
        obj = self._refresh_to_dict()
        pth = Path(self.spec.context) / f"{self.ENTITY_TYPE}s-{self.name}.yaml"
        obj = self._export_not_embedded(obj)
        write_yaml(pth, obj)
        return str(pth)

    def _refresh_to_dict(self) -> dict:
        """
        Try to refresh object to collect entities related to project.

        Returns
        -------
        dict
            Entity object in dictionary format.
        """
        try:
            return self.refresh().to_dict()
        except BackendError:
            return self.to_dict()

    def _export_not_embedded(self, obj: dict) -> dict:
        """
        Export project objects if not embedded.

        Parameters
        ----------
        obj : dict
            Project object in dictionary format.

        Returns
        -------
        dict
            Updatated project object in dictionary format with referenced entities.
        """
        # Cycle over entity types
        for entity_type in self._get_entity_types():
            # Entity types are stored as a list of entities
            for idx, entity in enumerate(obj.get("spec", {}).get(entity_type, [])):
                # Export entity if not embedded is in metadata, else do nothing
                if not self._is_embedded(entity):
                    # Get entity object from backend
                    ent = processor.read_context_entity(entity["key"])

                    # Export and store ref in object metadata inside project
                    pth = ent.export()
                    obj["spec"][entity_type][idx]["metadata"]["ref"] = pth

        # Return updated object
        return obj

    def _import_entities(self, obj: dict) -> None:
        """
        Import project entities.

        Parameters
        ----------
        obj : dict
            Project object in dictionary format.

        Returns
        -------
        None
        """
        entity_types = self._get_entity_types()

        # Cycle over entity types
        for entity_type in entity_types:
            # Entity types are stored as a list of entities
            for entity in obj.get("spec", {}).get(entity_type, []):
                embedded = self._is_embedded(entity)
                ref = entity["metadata"].get("ref")

                # Import entity if not embedded and there is a ref
                if not embedded and ref is not None:
                    # Import entity from local ref
                    if has_local_scheme(ref):
                        try:
                            # Artifacts, Dataitems and Models
                            if entity_type in entity_types[:3]:
                                processor.import_context_entity(ref)

                            # Functions and Workflows
                            elif entity_type in entity_types[3:]:
                                processor.import_executable_entity(ref)

                        except FileNotFoundError:
                            msg = f"File not found: {ref}."
                            raise EntityError(msg)

                # If entity is embedded, create it and try to save
                elif embedded:
                    # It's possible that embedded field in metadata is not shown
                    if entity["metadata"].get("embedded") is None:
                        entity["metadata"]["embedded"] = True

                    try:
                        build_entity_from_dict(entity).save()
                    except EntityAlreadyExistsError:
                        pass

    def _load_entities(self, obj: dict) -> None:
        """
        Load project entities.

        Parameters
        ----------
        obj : dict
            Project object in dictionary format.

        Returns
        -------
        None
        """
        entity_types = self._get_entity_types()

        # Cycle over entity types
        for entity_type in entity_types:
            # Entity types are stored as a list of entities
            for entity in obj.get("spec", {}).get(entity_type, []):
                embedded = self._is_embedded(entity)
                ref = entity["metadata"].get("ref")

                # Load entity if not embedded and there is a ref
                if not embedded and ref is not None:
                    # Load entity from local ref
                    if has_local_scheme(ref):
                        try:
                            # Artifacts, Dataitems and Models
                            if entity_type in entity_types[:3]:
                                processor.load_context_entity(ref)

                            # Functions and Workflows
                            elif entity_type in entity_types[3:]:
                                processor.load_executable_entity(ref)

                        except FileNotFoundError:
                            msg = f"File not found: {ref}."
                            raise EntityError(msg)

    def _is_embedded(self, entity: dict) -> bool:
        """
        Check if entity is embedded.

        Parameters
        ----------
        entity : dict
            Entity in dictionary format.

        Returns
        -------
        bool
            True if entity is embedded.
        """
        metadata_embedded = entity["metadata"].get("embedded", False)
        no_status = entity.get("status", None) is None
        no_spec = entity.get("spec", None) is None
        return metadata_embedded or not (no_status and no_spec)

    def _get_entity_types(self) -> list[str]:
        """
        Get entity types.

        Returns
        -------
        list
            Entity types.
        """
        return [
            f"{EntityTypes.ARTIFACT.value}s",
            f"{EntityTypes.DATAITEM.value}s",
            f"{EntityTypes.MODEL.value}s",
            f"{EntityTypes.FUNCTION.value}s",
            f"{EntityTypes.WORKFLOW.value}s",
        ]
