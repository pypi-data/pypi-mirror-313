# Generated by ariadne-codegen
# Source: ./documents

from typing import Any, List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import (
    AzureDocumentIntelligenceModels,
    AzureDocumentIntelligenceVersions,
    ContentIndexingServiceTypes,
    ContentTypes,
    DeepgramModels,
    EntityEnrichmentServiceTypes,
    EntityExtractionServiceTypes,
    EntityState,
    FilePreparationServiceTypes,
    FileTypes,
    IntegrationServiceTypes,
    LinkTypes,
    ObservableTypes,
    SummarizationTypes,
)


class CreateWorkflow(BaseModel):
    create_workflow: Optional["CreateWorkflowCreateWorkflow"] = Field(
        alias="createWorkflow"
    )


class CreateWorkflowCreateWorkflow(BaseModel):
    id: str
    name: str
    state: EntityState
    ingestion: Optional["CreateWorkflowCreateWorkflowIngestion"]
    indexing: Optional["CreateWorkflowCreateWorkflowIndexing"]
    preparation: Optional["CreateWorkflowCreateWorkflowPreparation"]
    extraction: Optional["CreateWorkflowCreateWorkflowExtraction"]
    enrichment: Optional["CreateWorkflowCreateWorkflowEnrichment"]
    actions: Optional[List[Optional["CreateWorkflowCreateWorkflowActions"]]]


class CreateWorkflowCreateWorkflowIngestion(BaseModel):
    if_: Optional["CreateWorkflowCreateWorkflowIngestionIf"] = Field(alias="if")
    collections: Optional[
        List[Optional["CreateWorkflowCreateWorkflowIngestionCollections"]]
    ]


class CreateWorkflowCreateWorkflowIngestionIf(BaseModel):
    types: Optional[List[ContentTypes]]
    file_types: Optional[List[FileTypes]] = Field(alias="fileTypes")
    allowed_paths: Optional[List[str]] = Field(alias="allowedPaths")
    excluded_paths: Optional[List[str]] = Field(alias="excludedPaths")


class CreateWorkflowCreateWorkflowIngestionCollections(BaseModel):
    id: str


class CreateWorkflowCreateWorkflowIndexing(BaseModel):
    jobs: Optional[List[Optional["CreateWorkflowCreateWorkflowIndexingJobs"]]]


class CreateWorkflowCreateWorkflowIndexingJobs(BaseModel):
    connector: Optional["CreateWorkflowCreateWorkflowIndexingJobsConnector"]


class CreateWorkflowCreateWorkflowIndexingJobsConnector(BaseModel):
    type: Optional[ContentIndexingServiceTypes]
    content_type: Optional[ContentTypes] = Field(alias="contentType")
    file_type: Optional[FileTypes] = Field(alias="fileType")


class CreateWorkflowCreateWorkflowPreparation(BaseModel):
    disable_smart_capture: Optional[bool] = Field(alias="disableSmartCapture")
    summarizations: Optional[
        List[Optional["CreateWorkflowCreateWorkflowPreparationSummarizations"]]
    ]
    jobs: Optional[List[Optional["CreateWorkflowCreateWorkflowPreparationJobs"]]]


class CreateWorkflowCreateWorkflowPreparationSummarizations(BaseModel):
    type: SummarizationTypes
    specification: Optional[
        "CreateWorkflowCreateWorkflowPreparationSummarizationsSpecification"
    ]
    tokens: Optional[int]
    items: Optional[int]
    prompt: Optional[str]


class CreateWorkflowCreateWorkflowPreparationSummarizationsSpecification(BaseModel):
    id: str


class CreateWorkflowCreateWorkflowPreparationJobs(BaseModel):
    connector: Optional["CreateWorkflowCreateWorkflowPreparationJobsConnector"]


class CreateWorkflowCreateWorkflowPreparationJobsConnector(BaseModel):
    type: FilePreparationServiceTypes
    file_types: Optional[List[FileTypes]] = Field(alias="fileTypes")
    azure_document: Optional[
        "CreateWorkflowCreateWorkflowPreparationJobsConnectorAzureDocument"
    ] = Field(alias="azureDocument")
    deepgram: Optional["CreateWorkflowCreateWorkflowPreparationJobsConnectorDeepgram"]
    document: Optional["CreateWorkflowCreateWorkflowPreparationJobsConnectorDocument"]
    email: Optional["CreateWorkflowCreateWorkflowPreparationJobsConnectorEmail"]
    model_document: Optional[
        "CreateWorkflowCreateWorkflowPreparationJobsConnectorModelDocument"
    ] = Field(alias="modelDocument")


class CreateWorkflowCreateWorkflowPreparationJobsConnectorAzureDocument(BaseModel):
    version: Optional[AzureDocumentIntelligenceVersions]
    model: Optional[AzureDocumentIntelligenceModels]
    endpoint: Optional[Any]
    key: Optional[str]


class CreateWorkflowCreateWorkflowPreparationJobsConnectorDeepgram(BaseModel):
    model: Optional[DeepgramModels]
    key: Optional[str]
    enable_redaction: Optional[bool] = Field(alias="enableRedaction")
    enable_speaker_diarization: Optional[bool] = Field(alias="enableSpeakerDiarization")
    detect_language: Optional[bool] = Field(alias="detectLanguage")
    language: Optional[str]


class CreateWorkflowCreateWorkflowPreparationJobsConnectorDocument(BaseModel):
    include_images: Optional[bool] = Field(alias="includeImages")


class CreateWorkflowCreateWorkflowPreparationJobsConnectorEmail(BaseModel):
    include_attachments: Optional[bool] = Field(alias="includeAttachments")


class CreateWorkflowCreateWorkflowPreparationJobsConnectorModelDocument(BaseModel):
    specification: Optional[
        "CreateWorkflowCreateWorkflowPreparationJobsConnectorModelDocumentSpecification"
    ]


class CreateWorkflowCreateWorkflowPreparationJobsConnectorModelDocumentSpecification(
    BaseModel
):
    id: str


class CreateWorkflowCreateWorkflowExtraction(BaseModel):
    jobs: Optional[List[Optional["CreateWorkflowCreateWorkflowExtractionJobs"]]]


class CreateWorkflowCreateWorkflowExtractionJobs(BaseModel):
    connector: Optional["CreateWorkflowCreateWorkflowExtractionJobsConnector"]


class CreateWorkflowCreateWorkflowExtractionJobsConnector(BaseModel):
    type: EntityExtractionServiceTypes
    content_types: Optional[List[ContentTypes]] = Field(alias="contentTypes")
    file_types: Optional[List[FileTypes]] = Field(alias="fileTypes")
    extracted_types: Optional[List[ObservableTypes]] = Field(alias="extractedTypes")
    extracted_count: Optional[int] = Field(alias="extractedCount")
    azure_text: Optional[
        "CreateWorkflowCreateWorkflowExtractionJobsConnectorAzureText"
    ] = Field(alias="azureText")
    azure_image: Optional[
        "CreateWorkflowCreateWorkflowExtractionJobsConnectorAzureImage"
    ] = Field(alias="azureImage")
    model_image: Optional[
        "CreateWorkflowCreateWorkflowExtractionJobsConnectorModelImage"
    ] = Field(alias="modelImage")
    model_text: Optional[
        "CreateWorkflowCreateWorkflowExtractionJobsConnectorModelText"
    ] = Field(alias="modelText")


class CreateWorkflowCreateWorkflowExtractionJobsConnectorAzureText(BaseModel):
    confidence_threshold: Optional[float] = Field(alias="confidenceThreshold")
    enable_pii: Optional[bool] = Field(alias="enablePII")


class CreateWorkflowCreateWorkflowExtractionJobsConnectorAzureImage(BaseModel):
    confidence_threshold: Optional[float] = Field(alias="confidenceThreshold")


class CreateWorkflowCreateWorkflowExtractionJobsConnectorModelImage(BaseModel):
    specification: Optional[
        "CreateWorkflowCreateWorkflowExtractionJobsConnectorModelImageSpecification"
    ]


class CreateWorkflowCreateWorkflowExtractionJobsConnectorModelImageSpecification(
    BaseModel
):
    id: str


class CreateWorkflowCreateWorkflowExtractionJobsConnectorModelText(BaseModel):
    specification: Optional[
        "CreateWorkflowCreateWorkflowExtractionJobsConnectorModelTextSpecification"
    ]


class CreateWorkflowCreateWorkflowExtractionJobsConnectorModelTextSpecification(
    BaseModel
):
    id: str


class CreateWorkflowCreateWorkflowEnrichment(BaseModel):
    link: Optional["CreateWorkflowCreateWorkflowEnrichmentLink"]
    jobs: Optional[List[Optional["CreateWorkflowCreateWorkflowEnrichmentJobs"]]]


class CreateWorkflowCreateWorkflowEnrichmentLink(BaseModel):
    enable_crawling: Optional[bool] = Field(alias="enableCrawling")
    allowed_domains: Optional[List[str]] = Field(alias="allowedDomains")
    excluded_domains: Optional[List[str]] = Field(alias="excludedDomains")
    allowed_paths: Optional[List[str]] = Field(alias="allowedPaths")
    excluded_paths: Optional[List[str]] = Field(alias="excludedPaths")
    allowed_links: Optional[List[LinkTypes]] = Field(alias="allowedLinks")
    excluded_links: Optional[List[LinkTypes]] = Field(alias="excludedLinks")
    allowed_files: Optional[List[FileTypes]] = Field(alias="allowedFiles")
    excluded_files: Optional[List[FileTypes]] = Field(alias="excludedFiles")
    allow_content_domain: Optional[bool] = Field(alias="allowContentDomain")
    maximum_links: Optional[int] = Field(alias="maximumLinks")


class CreateWorkflowCreateWorkflowEnrichmentJobs(BaseModel):
    connector: Optional["CreateWorkflowCreateWorkflowEnrichmentJobsConnector"]


class CreateWorkflowCreateWorkflowEnrichmentJobsConnector(BaseModel):
    type: Optional[EntityEnrichmentServiceTypes]
    enriched_types: Optional[List[Optional[ObservableTypes]]] = Field(
        alias="enrichedTypes"
    )
    fhir: Optional["CreateWorkflowCreateWorkflowEnrichmentJobsConnectorFhir"]


class CreateWorkflowCreateWorkflowEnrichmentJobsConnectorFhir(BaseModel):
    endpoint: Optional[Any]


class CreateWorkflowCreateWorkflowActions(BaseModel):
    connector: Optional["CreateWorkflowCreateWorkflowActionsConnector"]


class CreateWorkflowCreateWorkflowActionsConnector(BaseModel):
    type: IntegrationServiceTypes
    uri: Optional[str]
    slack: Optional["CreateWorkflowCreateWorkflowActionsConnectorSlack"]


class CreateWorkflowCreateWorkflowActionsConnectorSlack(BaseModel):
    token: str
    channel: str


CreateWorkflow.model_rebuild()
CreateWorkflowCreateWorkflow.model_rebuild()
CreateWorkflowCreateWorkflowIngestion.model_rebuild()
CreateWorkflowCreateWorkflowIndexing.model_rebuild()
CreateWorkflowCreateWorkflowIndexingJobs.model_rebuild()
CreateWorkflowCreateWorkflowPreparation.model_rebuild()
CreateWorkflowCreateWorkflowPreparationSummarizations.model_rebuild()
CreateWorkflowCreateWorkflowPreparationJobs.model_rebuild()
CreateWorkflowCreateWorkflowPreparationJobsConnector.model_rebuild()
CreateWorkflowCreateWorkflowPreparationJobsConnectorModelDocument.model_rebuild()
CreateWorkflowCreateWorkflowExtraction.model_rebuild()
CreateWorkflowCreateWorkflowExtractionJobs.model_rebuild()
CreateWorkflowCreateWorkflowExtractionJobsConnector.model_rebuild()
CreateWorkflowCreateWorkflowExtractionJobsConnectorModelImage.model_rebuild()
CreateWorkflowCreateWorkflowExtractionJobsConnectorModelText.model_rebuild()
CreateWorkflowCreateWorkflowEnrichment.model_rebuild()
CreateWorkflowCreateWorkflowEnrichmentJobs.model_rebuild()
CreateWorkflowCreateWorkflowEnrichmentJobsConnector.model_rebuild()
CreateWorkflowCreateWorkflowActions.model_rebuild()
CreateWorkflowCreateWorkflowActionsConnector.model_rebuild()
