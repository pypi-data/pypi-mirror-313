# Generated by ariadne-codegen
# Source: ./documents

from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class UpdateMedicalDevice(BaseModel):
    update_medical_device: Optional["UpdateMedicalDeviceUpdateMedicalDevice"] = Field(
        alias="updateMedicalDevice"
    )


class UpdateMedicalDeviceUpdateMedicalDevice(BaseModel):
    id: str
    name: str


UpdateMedicalDevice.model_rebuild()
