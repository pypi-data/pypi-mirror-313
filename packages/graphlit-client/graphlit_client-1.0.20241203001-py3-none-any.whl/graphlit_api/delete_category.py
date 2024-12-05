# Generated by ariadne-codegen
# Source: ./documents

from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import EntityState


class DeleteCategory(BaseModel):
    delete_category: Optional["DeleteCategoryDeleteCategory"] = Field(
        alias="deleteCategory"
    )


class DeleteCategoryDeleteCategory(BaseModel):
    id: str
    state: EntityState


DeleteCategory.model_rebuild()
