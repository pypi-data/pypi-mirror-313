# Generated by ariadne-codegen
# Source: ./documents

from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import EntityState, ModelServiceTypes, SpecificationTypes


class CreateSpecification(BaseModel):
    create_specification: Optional["CreateSpecificationCreateSpecification"] = Field(
        alias="createSpecification"
    )


class CreateSpecificationCreateSpecification(BaseModel):
    id: str
    name: str
    state: EntityState
    type: Optional[SpecificationTypes]
    service_type: Optional[ModelServiceTypes] = Field(alias="serviceType")


CreateSpecification.model_rebuild()
