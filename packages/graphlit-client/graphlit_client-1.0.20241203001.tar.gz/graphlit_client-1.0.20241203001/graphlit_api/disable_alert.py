# Generated by ariadne-codegen
# Source: ./documents

from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import EntityState


class DisableAlert(BaseModel):
    disable_alert: Optional["DisableAlertDisableAlert"] = Field(alias="disableAlert")


class DisableAlertDisableAlert(BaseModel):
    id: str
    state: EntityState


DisableAlert.model_rebuild()
