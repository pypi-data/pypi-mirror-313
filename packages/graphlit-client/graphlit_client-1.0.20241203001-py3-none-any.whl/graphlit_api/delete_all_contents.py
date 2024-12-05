# Generated by ariadne-codegen
# Source: ./documents

from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import EntityState


class DeleteAllContents(BaseModel):
    delete_all_contents: Optional[
        List[Optional["DeleteAllContentsDeleteAllContents"]]
    ] = Field(alias="deleteAllContents")


class DeleteAllContentsDeleteAllContents(BaseModel):
    id: str
    state: EntityState


DeleteAllContents.model_rebuild()
