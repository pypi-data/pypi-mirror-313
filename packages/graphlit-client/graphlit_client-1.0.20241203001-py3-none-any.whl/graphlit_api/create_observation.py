# Generated by ariadne-codegen
# Source: ./documents

from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import EntityState


class CreateObservation(BaseModel):
    create_observation: Optional["CreateObservationCreateObservation"] = Field(
        alias="createObservation"
    )


class CreateObservationCreateObservation(BaseModel):
    id: str
    state: EntityState


CreateObservation.model_rebuild()
