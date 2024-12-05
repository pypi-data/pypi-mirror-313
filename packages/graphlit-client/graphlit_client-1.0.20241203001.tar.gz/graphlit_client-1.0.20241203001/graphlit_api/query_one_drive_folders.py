# Generated by ariadne-codegen
# Source: ./documents

from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class QueryOneDriveFolders(BaseModel):
    one_drive_folders: Optional["QueryOneDriveFoldersOneDriveFolders"] = Field(
        alias="oneDriveFolders"
    )


class QueryOneDriveFoldersOneDriveFolders(BaseModel):
    results: Optional[List[Optional["QueryOneDriveFoldersOneDriveFoldersResults"]]]


class QueryOneDriveFoldersOneDriveFoldersResults(BaseModel):
    folder_name: Optional[str] = Field(alias="folderName")
    folder_id: Optional[str] = Field(alias="folderId")


QueryOneDriveFolders.model_rebuild()
QueryOneDriveFoldersOneDriveFolders.model_rebuild()
