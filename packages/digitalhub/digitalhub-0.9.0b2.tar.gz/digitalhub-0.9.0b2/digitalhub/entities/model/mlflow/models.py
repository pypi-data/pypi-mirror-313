from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Signature(BaseModel):
    """
    MLFlow model signature.
    """

    inputs: Optional[str] = None
    outputs: Optional[str] = None
    params: Optional[str] = None

    def to_dict(self):
        return self.model_dump()


class Dataset(BaseModel):
    """
    MLFlow model dataset.
    """

    name: Optional[str] = None
    digest: Optional[str] = None
    profile: Optional[str] = None
    schema_: Optional[str] = Field(default=None, alias="schema")
    source: Optional[str] = None
    source_type: Optional[str] = None

    def to_dict(self):
        return self.model_dump()
