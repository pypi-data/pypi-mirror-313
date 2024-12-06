from __future__ import annotations

import typing

from digitalhub.entities._base.context.entity import ContextEntity

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata
    from digitalhub.entities._base.entity.spec import Spec
    from digitalhub.entities._base.entity.status import Status


class UnversionedEntity(ContextEntity):
    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: Spec,
        status: Status,
        user: str | None = None,
    ) -> None:
        super().__init__(project, kind, metadata, spec, status, user)
        self.id = uuid
        self.name = uuid
        self.key = f"store://{project}/{self.ENTITY_TYPE}/{kind}/{uuid}"
