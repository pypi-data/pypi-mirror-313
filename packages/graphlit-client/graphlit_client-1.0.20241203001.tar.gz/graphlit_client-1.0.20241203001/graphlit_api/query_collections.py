# Generated by ariadne-codegen
# Source: ./documents

from typing import Any, List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import CollectionTypes, EntityState


class QueryCollections(BaseModel):
    collections: Optional["QueryCollectionsCollections"]


class QueryCollectionsCollections(BaseModel):
    results: Optional[List[Optional["QueryCollectionsCollectionsResults"]]]


class QueryCollectionsCollectionsResults(BaseModel):
    id: str
    name: str
    creation_date: Any = Field(alias="creationDate")
    relevance: Optional[float]
    owner: "QueryCollectionsCollectionsResultsOwner"
    state: EntityState
    type: Optional[CollectionTypes]
    contents: Optional[List[Optional["QueryCollectionsCollectionsResultsContents"]]]


class QueryCollectionsCollectionsResultsOwner(BaseModel):
    id: str


class QueryCollectionsCollectionsResultsContents(BaseModel):
    id: str
    name: str


QueryCollections.model_rebuild()
QueryCollectionsCollections.model_rebuild()
QueryCollectionsCollectionsResults.model_rebuild()
