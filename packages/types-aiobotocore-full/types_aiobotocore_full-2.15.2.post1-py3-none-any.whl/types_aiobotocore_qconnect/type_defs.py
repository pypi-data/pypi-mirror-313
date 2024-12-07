"""
Type annotations for qconnect service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/type_defs/)

Usage::

    ```python
    from types_aiobotocore_qconnect.type_defs import AIAgentConfigurationDataTypeDef

    data: AIAgentConfigurationDataTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AIAgentTypeType,
    AIPromptAPIFormatType,
    AIPromptTypeType,
    AssistantCapabilityTypeType,
    AssistantStatusType,
    ChunkingStrategyType,
    ContentStatusType,
    ImportJobStatusType,
    KnowledgeBaseSearchTypeType,
    KnowledgeBaseStatusType,
    KnowledgeBaseTypeType,
    OrderType,
    OriginType,
    PriorityType,
    QueryResultTypeType,
    QuickResponseFilterOperatorType,
    QuickResponseQueryOperatorType,
    QuickResponseStatusType,
    RecommendationSourceTypeType,
    RecommendationTriggerTypeType,
    RecommendationTypeType,
    ReferenceTypeType,
    RelevanceLevelType,
    RelevanceType,
    StatusType,
    SyncStatusType,
    TargetTypeType,
    VisibilityStatusType,
    WebScopeTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AIAgentConfigurationDataTypeDef",
    "AIAgentConfigurationOutputTypeDef",
    "AIAgentConfigurationTypeDef",
    "AIAgentDataTypeDef",
    "AIAgentSummaryTypeDef",
    "AIAgentVersionSummaryTypeDef",
    "AIPromptDataTypeDef",
    "AIPromptSummaryTypeDef",
    "AIPromptTemplateConfigurationTypeDef",
    "AIPromptVersionSummaryTypeDef",
    "AmazonConnectGuideAssociationDataTypeDef",
    "AnswerRecommendationAIAgentConfigurationOutputTypeDef",
    "AnswerRecommendationAIAgentConfigurationTypeDef",
    "AnswerRecommendationAIAgentConfigurationUnionTypeDef",
    "AppIntegrationsConfigurationOutputTypeDef",
    "AppIntegrationsConfigurationTypeDef",
    "AppIntegrationsConfigurationUnionTypeDef",
    "AssistantAssociationDataTypeDef",
    "AssistantAssociationInputDataTypeDef",
    "AssistantAssociationOutputDataTypeDef",
    "AssistantAssociationSummaryTypeDef",
    "AssistantCapabilityConfigurationTypeDef",
    "AssistantDataTypeDef",
    "AssistantIntegrationConfigurationTypeDef",
    "AssistantSummaryTypeDef",
    "AssociationConfigurationDataOutputTypeDef",
    "AssociationConfigurationDataTypeDef",
    "AssociationConfigurationDataUnionTypeDef",
    "AssociationConfigurationOutputTypeDef",
    "AssociationConfigurationTypeDef",
    "AssociationConfigurationUnionTypeDef",
    "BedrockFoundationModelConfigurationForParsingTypeDef",
    "ChunkingConfigurationOutputTypeDef",
    "ChunkingConfigurationTypeDef",
    "ChunkingConfigurationUnionTypeDef",
    "CitationSpanTypeDef",
    "ConfigurationTypeDef",
    "ConnectConfigurationTypeDef",
    "ContentAssociationContentsTypeDef",
    "ContentAssociationDataTypeDef",
    "ContentAssociationSummaryTypeDef",
    "ContentDataDetailsTypeDef",
    "ContentDataTypeDef",
    "ContentFeedbackDataTypeDef",
    "ContentReferenceTypeDef",
    "ContentSummaryTypeDef",
    "CreateAIAgentRequestRequestTypeDef",
    "CreateAIAgentResponseTypeDef",
    "CreateAIAgentVersionRequestRequestTypeDef",
    "CreateAIAgentVersionResponseTypeDef",
    "CreateAIPromptRequestRequestTypeDef",
    "CreateAIPromptResponseTypeDef",
    "CreateAIPromptVersionRequestRequestTypeDef",
    "CreateAIPromptVersionResponseTypeDef",
    "CreateAssistantAssociationRequestRequestTypeDef",
    "CreateAssistantAssociationResponseTypeDef",
    "CreateAssistantRequestRequestTypeDef",
    "CreateAssistantResponseTypeDef",
    "CreateContentAssociationRequestRequestTypeDef",
    "CreateContentAssociationResponseTypeDef",
    "CreateContentRequestRequestTypeDef",
    "CreateContentResponseTypeDef",
    "CreateKnowledgeBaseRequestRequestTypeDef",
    "CreateKnowledgeBaseResponseTypeDef",
    "CreateQuickResponseRequestRequestTypeDef",
    "CreateQuickResponseResponseTypeDef",
    "CreateSessionRequestRequestTypeDef",
    "CreateSessionResponseTypeDef",
    "DataDetailsPaginatorTypeDef",
    "DataDetailsTypeDef",
    "DataReferenceTypeDef",
    "DataSummaryPaginatorTypeDef",
    "DataSummaryTypeDef",
    "DeleteAIAgentRequestRequestTypeDef",
    "DeleteAIAgentVersionRequestRequestTypeDef",
    "DeleteAIPromptRequestRequestTypeDef",
    "DeleteAIPromptVersionRequestRequestTypeDef",
    "DeleteAssistantAssociationRequestRequestTypeDef",
    "DeleteAssistantRequestRequestTypeDef",
    "DeleteContentAssociationRequestRequestTypeDef",
    "DeleteContentRequestRequestTypeDef",
    "DeleteImportJobRequestRequestTypeDef",
    "DeleteKnowledgeBaseRequestRequestTypeDef",
    "DeleteQuickResponseRequestRequestTypeDef",
    "DocumentTextTypeDef",
    "DocumentTypeDef",
    "ExternalSourceConfigurationTypeDef",
    "FilterTypeDef",
    "FixedSizeChunkingConfigurationTypeDef",
    "GenerativeContentFeedbackDataTypeDef",
    "GenerativeDataDetailsPaginatorTypeDef",
    "GenerativeDataDetailsTypeDef",
    "GenerativeReferenceTypeDef",
    "GetAIAgentRequestRequestTypeDef",
    "GetAIAgentResponseTypeDef",
    "GetAIPromptRequestRequestTypeDef",
    "GetAIPromptResponseTypeDef",
    "GetAssistantAssociationRequestRequestTypeDef",
    "GetAssistantAssociationResponseTypeDef",
    "GetAssistantRequestRequestTypeDef",
    "GetAssistantResponseTypeDef",
    "GetContentAssociationRequestRequestTypeDef",
    "GetContentAssociationResponseTypeDef",
    "GetContentRequestRequestTypeDef",
    "GetContentResponseTypeDef",
    "GetContentSummaryRequestRequestTypeDef",
    "GetContentSummaryResponseTypeDef",
    "GetImportJobRequestRequestTypeDef",
    "GetImportJobResponseTypeDef",
    "GetKnowledgeBaseRequestRequestTypeDef",
    "GetKnowledgeBaseResponseTypeDef",
    "GetQuickResponseRequestRequestTypeDef",
    "GetQuickResponseResponseTypeDef",
    "GetRecommendationsRequestRequestTypeDef",
    "GetRecommendationsResponseTypeDef",
    "GetSessionRequestRequestTypeDef",
    "GetSessionResponseTypeDef",
    "GroupingConfigurationOutputTypeDef",
    "GroupingConfigurationTypeDef",
    "HierarchicalChunkingConfigurationOutputTypeDef",
    "HierarchicalChunkingConfigurationTypeDef",
    "HierarchicalChunkingConfigurationUnionTypeDef",
    "HierarchicalChunkingLevelConfigurationTypeDef",
    "HighlightTypeDef",
    "ImportJobDataTypeDef",
    "ImportJobSummaryTypeDef",
    "IntentDetectedDataDetailsTypeDef",
    "IntentInputDataTypeDef",
    "KnowledgeBaseAssociationConfigurationDataOutputTypeDef",
    "KnowledgeBaseAssociationConfigurationDataTypeDef",
    "KnowledgeBaseAssociationConfigurationDataUnionTypeDef",
    "KnowledgeBaseAssociationDataTypeDef",
    "KnowledgeBaseDataTypeDef",
    "KnowledgeBaseSummaryTypeDef",
    "ListAIAgentVersionsRequestListAIAgentVersionsPaginateTypeDef",
    "ListAIAgentVersionsRequestRequestTypeDef",
    "ListAIAgentVersionsResponseTypeDef",
    "ListAIAgentsRequestListAIAgentsPaginateTypeDef",
    "ListAIAgentsRequestRequestTypeDef",
    "ListAIAgentsResponseTypeDef",
    "ListAIPromptVersionsRequestListAIPromptVersionsPaginateTypeDef",
    "ListAIPromptVersionsRequestRequestTypeDef",
    "ListAIPromptVersionsResponseTypeDef",
    "ListAIPromptsRequestListAIPromptsPaginateTypeDef",
    "ListAIPromptsRequestRequestTypeDef",
    "ListAIPromptsResponseTypeDef",
    "ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef",
    "ListAssistantAssociationsRequestRequestTypeDef",
    "ListAssistantAssociationsResponseTypeDef",
    "ListAssistantsRequestListAssistantsPaginateTypeDef",
    "ListAssistantsRequestRequestTypeDef",
    "ListAssistantsResponseTypeDef",
    "ListContentAssociationsRequestListContentAssociationsPaginateTypeDef",
    "ListContentAssociationsRequestRequestTypeDef",
    "ListContentAssociationsResponseTypeDef",
    "ListContentsRequestListContentsPaginateTypeDef",
    "ListContentsRequestRequestTypeDef",
    "ListContentsResponseTypeDef",
    "ListImportJobsRequestListImportJobsPaginateTypeDef",
    "ListImportJobsRequestRequestTypeDef",
    "ListImportJobsResponseTypeDef",
    "ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef",
    "ListKnowledgeBasesRequestRequestTypeDef",
    "ListKnowledgeBasesResponseTypeDef",
    "ListQuickResponsesRequestListQuickResponsesPaginateTypeDef",
    "ListQuickResponsesRequestRequestTypeDef",
    "ListQuickResponsesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ManagedSourceConfigurationOutputTypeDef",
    "ManagedSourceConfigurationTypeDef",
    "ManagedSourceConfigurationUnionTypeDef",
    "ManualSearchAIAgentConfigurationOutputTypeDef",
    "ManualSearchAIAgentConfigurationTypeDef",
    "ManualSearchAIAgentConfigurationUnionTypeDef",
    "NotifyRecommendationsReceivedErrorTypeDef",
    "NotifyRecommendationsReceivedRequestRequestTypeDef",
    "NotifyRecommendationsReceivedResponseTypeDef",
    "OrConditionOutputTypeDef",
    "OrConditionTypeDef",
    "OrConditionUnionTypeDef",
    "PaginatorConfigTypeDef",
    "ParsingConfigurationTypeDef",
    "ParsingPromptTypeDef",
    "PutFeedbackRequestRequestTypeDef",
    "PutFeedbackResponseTypeDef",
    "QueryAssistantRequestQueryAssistantPaginateTypeDef",
    "QueryAssistantRequestRequestTypeDef",
    "QueryAssistantResponsePaginatorTypeDef",
    "QueryAssistantResponseTypeDef",
    "QueryConditionItemTypeDef",
    "QueryConditionTypeDef",
    "QueryInputDataTypeDef",
    "QueryRecommendationTriggerDataTypeDef",
    "QueryTextInputDataTypeDef",
    "QuickResponseContentProviderTypeDef",
    "QuickResponseContentsTypeDef",
    "QuickResponseDataProviderTypeDef",
    "QuickResponseDataTypeDef",
    "QuickResponseFilterFieldTypeDef",
    "QuickResponseOrderFieldTypeDef",
    "QuickResponseQueryFieldTypeDef",
    "QuickResponseSearchExpressionTypeDef",
    "QuickResponseSearchResultDataTypeDef",
    "QuickResponseSummaryTypeDef",
    "RankingDataTypeDef",
    "RecommendationDataTypeDef",
    "RecommendationTriggerDataTypeDef",
    "RecommendationTriggerTypeDef",
    "RemoveAssistantAIAgentRequestRequestTypeDef",
    "RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef",
    "RenderingConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "ResultDataPaginatorTypeDef",
    "ResultDataTypeDef",
    "RuntimeSessionDataTypeDef",
    "RuntimeSessionDataValueTypeDef",
    "SearchContentRequestRequestTypeDef",
    "SearchContentRequestSearchContentPaginateTypeDef",
    "SearchContentResponseTypeDef",
    "SearchExpressionTypeDef",
    "SearchQuickResponsesRequestRequestTypeDef",
    "SearchQuickResponsesRequestSearchQuickResponsesPaginateTypeDef",
    "SearchQuickResponsesResponseTypeDef",
    "SearchSessionsRequestRequestTypeDef",
    "SearchSessionsRequestSearchSessionsPaginateTypeDef",
    "SearchSessionsResponseTypeDef",
    "SeedUrlTypeDef",
    "SemanticChunkingConfigurationTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "SessionDataTypeDef",
    "SessionIntegrationConfigurationTypeDef",
    "SessionSummaryTypeDef",
    "SourceConfigurationOutputTypeDef",
    "SourceConfigurationTypeDef",
    "SourceContentDataDetailsTypeDef",
    "StartContentUploadRequestRequestTypeDef",
    "StartContentUploadResponseTypeDef",
    "StartImportJobRequestRequestTypeDef",
    "StartImportJobResponseTypeDef",
    "TagConditionTypeDef",
    "TagFilterOutputTypeDef",
    "TagFilterTypeDef",
    "TagFilterUnionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TextDataTypeDef",
    "TextFullAIPromptEditTemplateConfigurationTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAIAgentRequestRequestTypeDef",
    "UpdateAIAgentResponseTypeDef",
    "UpdateAIPromptRequestRequestTypeDef",
    "UpdateAIPromptResponseTypeDef",
    "UpdateAssistantAIAgentRequestRequestTypeDef",
    "UpdateAssistantAIAgentResponseTypeDef",
    "UpdateContentRequestRequestTypeDef",
    "UpdateContentResponseTypeDef",
    "UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef",
    "UpdateKnowledgeBaseTemplateUriResponseTypeDef",
    "UpdateQuickResponseRequestRequestTypeDef",
    "UpdateQuickResponseResponseTypeDef",
    "UpdateSessionDataRequestRequestTypeDef",
    "UpdateSessionDataResponseTypeDef",
    "UpdateSessionRequestRequestTypeDef",
    "UpdateSessionResponseTypeDef",
    "UrlConfigurationOutputTypeDef",
    "UrlConfigurationTypeDef",
    "UrlConfigurationUnionTypeDef",
    "VectorIngestionConfigurationOutputTypeDef",
    "VectorIngestionConfigurationTypeDef",
    "WebCrawlerConfigurationOutputTypeDef",
    "WebCrawlerConfigurationTypeDef",
    "WebCrawlerConfigurationUnionTypeDef",
    "WebCrawlerLimitsTypeDef",
)


class AIAgentConfigurationDataTypeDef(TypedDict):
    aiAgentId: str


AIPromptSummaryTypeDef = TypedDict(
    "AIPromptSummaryTypeDef",
    {
        "aiPromptArn": str,
        "aiPromptId": str,
        "apiFormat": AIPromptAPIFormatType,
        "assistantArn": str,
        "assistantId": str,
        "modelId": str,
        "name": str,
        "templateType": Literal["TEXT"],
        "type": AIPromptTypeType,
        "visibilityStatus": VisibilityStatusType,
        "description": NotRequired[str],
        "modifiedTime": NotRequired[datetime],
        "origin": NotRequired[OriginType],
        "status": NotRequired[StatusType],
        "tags": NotRequired[Dict[str, str]],
    },
)


class TextFullAIPromptEditTemplateConfigurationTypeDef(TypedDict):
    text: str


class AmazonConnectGuideAssociationDataTypeDef(TypedDict):
    flowId: NotRequired[str]


class AppIntegrationsConfigurationOutputTypeDef(TypedDict):
    appIntegrationArn: str
    objectFields: NotRequired[List[str]]


class AppIntegrationsConfigurationTypeDef(TypedDict):
    appIntegrationArn: str
    objectFields: NotRequired[Sequence[str]]


class AssistantAssociationInputDataTypeDef(TypedDict):
    knowledgeBaseId: NotRequired[str]


class KnowledgeBaseAssociationDataTypeDef(TypedDict):
    knowledgeBaseArn: NotRequired[str]
    knowledgeBaseId: NotRequired[str]


AssistantCapabilityConfigurationTypeDef = TypedDict(
    "AssistantCapabilityConfigurationTypeDef",
    {
        "type": NotRequired[AssistantCapabilityTypeType],
    },
)


class AssistantIntegrationConfigurationTypeDef(TypedDict):
    topicIntegrationArn: NotRequired[str]


class ServerSideEncryptionConfigurationTypeDef(TypedDict):
    kmsKeyId: NotRequired[str]


class ParsingPromptTypeDef(TypedDict):
    parsingPromptText: str


class FixedSizeChunkingConfigurationTypeDef(TypedDict):
    maxTokens: int
    overlapPercentage: int


class SemanticChunkingConfigurationTypeDef(TypedDict):
    breakpointPercentileThreshold: int
    bufferSize: int
    maxTokens: int


class CitationSpanTypeDef(TypedDict):
    beginOffsetInclusive: NotRequired[int]
    endOffsetExclusive: NotRequired[int]


class ConnectConfigurationTypeDef(TypedDict):
    instanceId: NotRequired[str]


class RankingDataTypeDef(TypedDict):
    relevanceLevel: NotRequired[RelevanceLevelType]
    relevanceScore: NotRequired[float]


class ContentDataTypeDef(TypedDict):
    contentArn: str
    contentId: str
    contentType: str
    knowledgeBaseArn: str
    knowledgeBaseId: str
    metadata: Dict[str, str]
    name: str
    revisionId: str
    status: ContentStatusType
    title: str
    url: str
    urlExpiry: datetime
    linkOutUri: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class GenerativeContentFeedbackDataTypeDef(TypedDict):
    relevance: RelevanceType


class ContentReferenceTypeDef(TypedDict):
    contentArn: NotRequired[str]
    contentId: NotRequired[str]
    knowledgeBaseArn: NotRequired[str]
    knowledgeBaseId: NotRequired[str]
    referenceType: NotRequired[ReferenceTypeType]
    sourceURL: NotRequired[str]


class ContentSummaryTypeDef(TypedDict):
    contentArn: str
    contentId: str
    contentType: str
    knowledgeBaseArn: str
    knowledgeBaseId: str
    metadata: Dict[str, str]
    name: str
    revisionId: str
    status: ContentStatusType
    title: str
    tags: NotRequired[Dict[str, str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class CreateContentRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    name: str
    uploadId: str
    clientToken: NotRequired[str]
    metadata: NotRequired[Mapping[str, str]]
    overrideLinkOutUri: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    title: NotRequired[str]


class RenderingConfigurationTypeDef(TypedDict):
    templateUri: NotRequired[str]


class GroupingConfigurationTypeDef(TypedDict):
    criteria: NotRequired[str]
    values: NotRequired[Sequence[str]]


class QuickResponseDataProviderTypeDef(TypedDict):
    content: NotRequired[str]


class IntentDetectedDataDetailsTypeDef(TypedDict):
    intent: str
    intentId: str


class GenerativeReferenceTypeDef(TypedDict):
    generationId: NotRequired[str]
    modelId: NotRequired[str]


class DeleteAIAgentRequestRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str


class DeleteAIAgentVersionRequestRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str
    versionNumber: int


class DeleteAIPromptRequestRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str


class DeleteAIPromptVersionRequestRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str
    versionNumber: int


class DeleteAssistantAssociationRequestRequestTypeDef(TypedDict):
    assistantAssociationId: str
    assistantId: str


class DeleteAssistantRequestRequestTypeDef(TypedDict):
    assistantId: str


class DeleteContentAssociationRequestRequestTypeDef(TypedDict):
    contentAssociationId: str
    contentId: str
    knowledgeBaseId: str


class DeleteContentRequestRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str


class DeleteImportJobRequestRequestTypeDef(TypedDict):
    importJobId: str
    knowledgeBaseId: str


class DeleteKnowledgeBaseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str


class DeleteQuickResponseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    quickResponseId: str


class HighlightTypeDef(TypedDict):
    beginOffsetInclusive: NotRequired[int]
    endOffsetExclusive: NotRequired[int]


FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "field": Literal["NAME"],
        "operator": Literal["EQUALS"],
        "value": str,
    },
)


class GetAIAgentRequestRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str


class GetAIPromptRequestRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str


class GetAssistantAssociationRequestRequestTypeDef(TypedDict):
    assistantAssociationId: str
    assistantId: str


class GetAssistantRequestRequestTypeDef(TypedDict):
    assistantId: str


class GetContentAssociationRequestRequestTypeDef(TypedDict):
    contentAssociationId: str
    contentId: str
    knowledgeBaseId: str


class GetContentRequestRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str


class GetContentSummaryRequestRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str


class GetImportJobRequestRequestTypeDef(TypedDict):
    importJobId: str
    knowledgeBaseId: str


class GetKnowledgeBaseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str


class GetQuickResponseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    quickResponseId: str


class GetRecommendationsRequestRequestTypeDef(TypedDict):
    assistantId: str
    sessionId: str
    maxResults: NotRequired[int]
    waitTimeSeconds: NotRequired[int]


class GetSessionRequestRequestTypeDef(TypedDict):
    assistantId: str
    sessionId: str


class GroupingConfigurationOutputTypeDef(TypedDict):
    criteria: NotRequired[str]
    values: NotRequired[List[str]]


class HierarchicalChunkingLevelConfigurationTypeDef(TypedDict):
    maxTokens: int


class IntentInputDataTypeDef(TypedDict):
    intentId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAIAgentVersionsRequestRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    origin: NotRequired[OriginType]


class ListAIAgentsRequestRequestTypeDef(TypedDict):
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    origin: NotRequired[OriginType]


class ListAIPromptVersionsRequestRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    origin: NotRequired[OriginType]


class ListAIPromptsRequestRequestTypeDef(TypedDict):
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    origin: NotRequired[OriginType]


class ListAssistantAssociationsRequestRequestTypeDef(TypedDict):
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListAssistantsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListContentAssociationsRequestRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListContentsRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListImportJobsRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListKnowledgeBasesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListQuickResponsesRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class QuickResponseSummaryTypeDef(TypedDict):
    contentType: str
    createdTime: datetime
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    name: str
    quickResponseArn: str
    quickResponseId: str
    status: QuickResponseStatusType
    channels: NotRequired[List[str]]
    description: NotRequired[str]
    isActive: NotRequired[bool]
    lastModifiedBy: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class NotifyRecommendationsReceivedErrorTypeDef(TypedDict):
    message: NotRequired[str]
    recommendationId: NotRequired[str]


class NotifyRecommendationsReceivedRequestRequestTypeDef(TypedDict):
    assistantId: str
    recommendationIds: Sequence[str]
    sessionId: str


class TagConditionTypeDef(TypedDict):
    key: str
    value: NotRequired[str]


class QueryConditionItemTypeDef(TypedDict):
    comparator: Literal["EQUALS"]
    field: Literal["RESULT_TYPE"]
    value: str


class QueryTextInputDataTypeDef(TypedDict):
    text: str


class QueryRecommendationTriggerDataTypeDef(TypedDict):
    text: NotRequired[str]


class QuickResponseContentProviderTypeDef(TypedDict):
    content: NotRequired[str]


QuickResponseFilterFieldTypeDef = TypedDict(
    "QuickResponseFilterFieldTypeDef",
    {
        "name": str,
        "operator": QuickResponseFilterOperatorType,
        "includeNoExistence": NotRequired[bool],
        "values": NotRequired[Sequence[str]],
    },
)


class QuickResponseOrderFieldTypeDef(TypedDict):
    name: str
    order: NotRequired[OrderType]


QuickResponseQueryFieldTypeDef = TypedDict(
    "QuickResponseQueryFieldTypeDef",
    {
        "name": str,
        "operator": QuickResponseQueryOperatorType,
        "values": Sequence[str],
        "allowFuzziness": NotRequired[bool],
        "priority": NotRequired[PriorityType],
    },
)


class RemoveAssistantAIAgentRequestRequestTypeDef(TypedDict):
    aiAgentType: AIAgentTypeType
    assistantId: str


class RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str


class RuntimeSessionDataValueTypeDef(TypedDict):
    stringValue: NotRequired[str]


class SessionSummaryTypeDef(TypedDict):
    assistantArn: str
    assistantId: str
    sessionArn: str
    sessionId: str


class SeedUrlTypeDef(TypedDict):
    url: NotRequired[str]


class SessionIntegrationConfigurationTypeDef(TypedDict):
    topicIntegrationArn: NotRequired[str]


class StartContentUploadRequestRequestTypeDef(TypedDict):
    contentType: str
    knowledgeBaseId: str
    presignedUrlTimeToLive: NotRequired[int]


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateContentRequestRequestTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str
    metadata: NotRequired[Mapping[str, str]]
    overrideLinkOutUri: NotRequired[str]
    removeOverrideLinkOutUri: NotRequired[bool]
    revisionId: NotRequired[str]
    title: NotRequired[str]
    uploadId: NotRequired[str]


class UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    templateUri: str


class WebCrawlerLimitsTypeDef(TypedDict):
    rateLimit: NotRequired[int]


class UpdateAssistantAIAgentRequestRequestTypeDef(TypedDict):
    aiAgentType: AIAgentTypeType
    assistantId: str
    configuration: AIAgentConfigurationDataTypeDef


class AIPromptVersionSummaryTypeDef(TypedDict):
    aiPromptSummary: NotRequired[AIPromptSummaryTypeDef]
    versionNumber: NotRequired[int]


class AIPromptTemplateConfigurationTypeDef(TypedDict):
    textFullAIPromptEditTemplateConfiguration: NotRequired[
        TextFullAIPromptEditTemplateConfigurationTypeDef
    ]


class ContentAssociationContentsTypeDef(TypedDict):
    amazonConnectGuideAssociation: NotRequired[AmazonConnectGuideAssociationDataTypeDef]


AppIntegrationsConfigurationUnionTypeDef = Union[
    AppIntegrationsConfigurationTypeDef, AppIntegrationsConfigurationOutputTypeDef
]


class CreateAssistantAssociationRequestRequestTypeDef(TypedDict):
    assistantId: str
    association: AssistantAssociationInputDataTypeDef
    associationType: Literal["KNOWLEDGE_BASE"]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class AssistantAssociationOutputDataTypeDef(TypedDict):
    knowledgeBaseAssociation: NotRequired[KnowledgeBaseAssociationDataTypeDef]


AssistantDataTypeDef = TypedDict(
    "AssistantDataTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "status": AssistantStatusType,
        "type": Literal["AGENT"],
        "aiAgentConfiguration": NotRequired[Dict[AIAgentTypeType, AIAgentConfigurationDataTypeDef]],
        "capabilityConfiguration": NotRequired[AssistantCapabilityConfigurationTypeDef],
        "description": NotRequired[str],
        "integrationConfiguration": NotRequired[AssistantIntegrationConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)
AssistantSummaryTypeDef = TypedDict(
    "AssistantSummaryTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "status": AssistantStatusType,
        "type": Literal["AGENT"],
        "aiAgentConfiguration": NotRequired[Dict[AIAgentTypeType, AIAgentConfigurationDataTypeDef]],
        "capabilityConfiguration": NotRequired[AssistantCapabilityConfigurationTypeDef],
        "description": NotRequired[str],
        "integrationConfiguration": NotRequired[AssistantIntegrationConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)
CreateAssistantRequestRequestTypeDef = TypedDict(
    "CreateAssistantRequestRequestTypeDef",
    {
        "name": str,
        "type": Literal["AGENT"],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Mapping[str, str]],
    },
)


class BedrockFoundationModelConfigurationForParsingTypeDef(TypedDict):
    modelArn: str
    parsingPrompt: NotRequired[ParsingPromptTypeDef]


class ConfigurationTypeDef(TypedDict):
    connectConfiguration: NotRequired[ConnectConfigurationTypeDef]


class GenerativeDataDetailsPaginatorTypeDef(TypedDict):
    completion: str
    rankingData: RankingDataTypeDef
    references: List[Dict[str, Any]]


class GenerativeDataDetailsTypeDef(TypedDict):
    completion: str
    rankingData: RankingDataTypeDef
    references: List[Dict[str, Any]]


class ContentFeedbackDataTypeDef(TypedDict):
    generativeContentFeedbackData: NotRequired[GenerativeContentFeedbackDataTypeDef]


class CreateContentResponseTypeDef(TypedDict):
    content: ContentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetContentResponseTypeDef(TypedDict):
    content: ContentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetContentSummaryResponseTypeDef(TypedDict):
    contentSummary: ContentSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAIPromptsResponseTypeDef(TypedDict):
    aiPromptSummaries: List[AIPromptSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListContentsResponseTypeDef(TypedDict):
    contentSummaries: List[ContentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class SearchContentResponseTypeDef(TypedDict):
    contentSummaries: List[ContentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StartContentUploadResponseTypeDef(TypedDict):
    headersToInclude: Dict[str, str]
    uploadId: str
    url: str
    urlExpiry: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateContentResponseTypeDef(TypedDict):
    content: ContentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAIAgentVersionRequestRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str
    clientToken: NotRequired[str]
    modifiedTime: NotRequired[TimestampTypeDef]


class CreateAIPromptVersionRequestRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str
    clientToken: NotRequired[str]
    modifiedTime: NotRequired[TimestampTypeDef]


class CreateQuickResponseRequestRequestTypeDef(TypedDict):
    content: QuickResponseDataProviderTypeDef
    knowledgeBaseId: str
    name: str
    channels: NotRequired[Sequence[str]]
    clientToken: NotRequired[str]
    contentType: NotRequired[str]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationTypeDef]
    isActive: NotRequired[bool]
    language: NotRequired[str]
    shortcutKey: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class UpdateQuickResponseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    quickResponseId: str
    channels: NotRequired[Sequence[str]]
    content: NotRequired[QuickResponseDataProviderTypeDef]
    contentType: NotRequired[str]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationTypeDef]
    isActive: NotRequired[bool]
    language: NotRequired[str]
    name: NotRequired[str]
    removeDescription: NotRequired[bool]
    removeGroupingConfiguration: NotRequired[bool]
    removeShortcutKey: NotRequired[bool]
    shortcutKey: NotRequired[str]


class DataReferenceTypeDef(TypedDict):
    contentReference: NotRequired[ContentReferenceTypeDef]
    generativeReference: NotRequired[GenerativeReferenceTypeDef]


class DocumentTextTypeDef(TypedDict):
    highlights: NotRequired[List[HighlightTypeDef]]
    text: NotRequired[str]


class SearchExpressionTypeDef(TypedDict):
    filters: Sequence[FilterTypeDef]


class HierarchicalChunkingConfigurationOutputTypeDef(TypedDict):
    levelConfigurations: List[HierarchicalChunkingLevelConfigurationTypeDef]
    overlapTokens: int


class HierarchicalChunkingConfigurationTypeDef(TypedDict):
    levelConfigurations: Sequence[HierarchicalChunkingLevelConfigurationTypeDef]
    overlapTokens: int


class ListAIAgentVersionsRequestListAIAgentVersionsPaginateTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str
    origin: NotRequired[OriginType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAIAgentsRequestListAIAgentsPaginateTypeDef(TypedDict):
    assistantId: str
    origin: NotRequired[OriginType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAIPromptVersionsRequestListAIPromptVersionsPaginateTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str
    origin: NotRequired[OriginType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAIPromptsRequestListAIPromptsPaginateTypeDef(TypedDict):
    assistantId: str
    origin: NotRequired[OriginType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef(TypedDict):
    assistantId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssistantsRequestListAssistantsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContentAssociationsRequestListContentAssociationsPaginateTypeDef(TypedDict):
    contentId: str
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContentsRequestListContentsPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListImportJobsRequestListImportJobsPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListQuickResponsesRequestListQuickResponsesPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListQuickResponsesResponseTypeDef(TypedDict):
    quickResponseSummaries: List[QuickResponseSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class NotifyRecommendationsReceivedResponseTypeDef(TypedDict):
    errors: List[NotifyRecommendationsReceivedErrorTypeDef]
    recommendationIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class OrConditionOutputTypeDef(TypedDict):
    andConditions: NotRequired[List[TagConditionTypeDef]]
    tagCondition: NotRequired[TagConditionTypeDef]


class OrConditionTypeDef(TypedDict):
    andConditions: NotRequired[Sequence[TagConditionTypeDef]]
    tagCondition: NotRequired[TagConditionTypeDef]


class QueryConditionTypeDef(TypedDict):
    single: NotRequired[QueryConditionItemTypeDef]


class QueryInputDataTypeDef(TypedDict):
    intentInputData: NotRequired[IntentInputDataTypeDef]
    queryTextInputData: NotRequired[QueryTextInputDataTypeDef]


class RecommendationTriggerDataTypeDef(TypedDict):
    query: NotRequired[QueryRecommendationTriggerDataTypeDef]


class QuickResponseContentsTypeDef(TypedDict):
    markdown: NotRequired[QuickResponseContentProviderTypeDef]
    plainText: NotRequired[QuickResponseContentProviderTypeDef]


class QuickResponseSearchExpressionTypeDef(TypedDict):
    filters: NotRequired[Sequence[QuickResponseFilterFieldTypeDef]]
    orderOnField: NotRequired[QuickResponseOrderFieldTypeDef]
    queries: NotRequired[Sequence[QuickResponseQueryFieldTypeDef]]


class RuntimeSessionDataTypeDef(TypedDict):
    key: str
    value: RuntimeSessionDataValueTypeDef


class SearchSessionsResponseTypeDef(TypedDict):
    sessionSummaries: List[SessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UrlConfigurationOutputTypeDef(TypedDict):
    seedUrls: NotRequired[List[SeedUrlTypeDef]]


class UrlConfigurationTypeDef(TypedDict):
    seedUrls: NotRequired[Sequence[SeedUrlTypeDef]]


class ListAIPromptVersionsResponseTypeDef(TypedDict):
    aiPromptVersionSummaries: List[AIPromptVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


AIPromptDataTypeDef = TypedDict(
    "AIPromptDataTypeDef",
    {
        "aiPromptArn": str,
        "aiPromptId": str,
        "apiFormat": AIPromptAPIFormatType,
        "assistantArn": str,
        "assistantId": str,
        "modelId": str,
        "name": str,
        "templateConfiguration": AIPromptTemplateConfigurationTypeDef,
        "templateType": Literal["TEXT"],
        "type": AIPromptTypeType,
        "visibilityStatus": VisibilityStatusType,
        "description": NotRequired[str],
        "modifiedTime": NotRequired[datetime],
        "origin": NotRequired[OriginType],
        "status": NotRequired[StatusType],
        "tags": NotRequired[Dict[str, str]],
    },
)
CreateAIPromptRequestRequestTypeDef = TypedDict(
    "CreateAIPromptRequestRequestTypeDef",
    {
        "apiFormat": AIPromptAPIFormatType,
        "assistantId": str,
        "modelId": str,
        "name": str,
        "templateConfiguration": AIPromptTemplateConfigurationTypeDef,
        "templateType": Literal["TEXT"],
        "type": AIPromptTypeType,
        "visibilityStatus": VisibilityStatusType,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)


class UpdateAIPromptRequestRequestTypeDef(TypedDict):
    aiPromptId: str
    assistantId: str
    visibilityStatus: VisibilityStatusType
    clientToken: NotRequired[str]
    description: NotRequired[str]
    templateConfiguration: NotRequired[AIPromptTemplateConfigurationTypeDef]


class ContentAssociationDataTypeDef(TypedDict):
    associationData: ContentAssociationContentsTypeDef
    associationType: Literal["AMAZON_CONNECT_GUIDE"]
    contentArn: str
    contentAssociationArn: str
    contentAssociationId: str
    contentId: str
    knowledgeBaseArn: str
    knowledgeBaseId: str
    tags: NotRequired[Dict[str, str]]


class ContentAssociationSummaryTypeDef(TypedDict):
    associationData: ContentAssociationContentsTypeDef
    associationType: Literal["AMAZON_CONNECT_GUIDE"]
    contentArn: str
    contentAssociationArn: str
    contentAssociationId: str
    contentId: str
    knowledgeBaseArn: str
    knowledgeBaseId: str
    tags: NotRequired[Dict[str, str]]


class CreateContentAssociationRequestRequestTypeDef(TypedDict):
    association: ContentAssociationContentsTypeDef
    associationType: Literal["AMAZON_CONNECT_GUIDE"]
    contentId: str
    knowledgeBaseId: str
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class AssistantAssociationDataTypeDef(TypedDict):
    assistantArn: str
    assistantAssociationArn: str
    assistantAssociationId: str
    assistantId: str
    associationData: AssistantAssociationOutputDataTypeDef
    associationType: Literal["KNOWLEDGE_BASE"]
    tags: NotRequired[Dict[str, str]]


class AssistantAssociationSummaryTypeDef(TypedDict):
    assistantArn: str
    assistantAssociationArn: str
    assistantAssociationId: str
    assistantId: str
    associationData: AssistantAssociationOutputDataTypeDef
    associationType: Literal["KNOWLEDGE_BASE"]
    tags: NotRequired[Dict[str, str]]


class CreateAssistantResponseTypeDef(TypedDict):
    assistant: AssistantDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAssistantResponseTypeDef(TypedDict):
    assistant: AssistantDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAssistantAIAgentResponseTypeDef(TypedDict):
    assistant: AssistantDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAssistantsResponseTypeDef(TypedDict):
    assistantSummaries: List[AssistantSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ParsingConfigurationTypeDef(TypedDict):
    parsingStrategy: Literal["BEDROCK_FOUNDATION_MODEL"]
    bedrockFoundationModelConfiguration: NotRequired[
        BedrockFoundationModelConfigurationForParsingTypeDef
    ]


class ExternalSourceConfigurationTypeDef(TypedDict):
    configuration: ConfigurationTypeDef
    source: Literal["AMAZON_CONNECT"]


class PutFeedbackRequestRequestTypeDef(TypedDict):
    assistantId: str
    contentFeedback: ContentFeedbackDataTypeDef
    targetId: str
    targetType: TargetTypeType


class PutFeedbackResponseTypeDef(TypedDict):
    assistantArn: str
    assistantId: str
    contentFeedback: ContentFeedbackDataTypeDef
    targetId: str
    targetType: TargetTypeType
    ResponseMetadata: ResponseMetadataTypeDef


class DocumentTypeDef(TypedDict):
    contentReference: ContentReferenceTypeDef
    excerpt: NotRequired[DocumentTextTypeDef]
    title: NotRequired[DocumentTextTypeDef]


class TextDataTypeDef(TypedDict):
    excerpt: NotRequired[DocumentTextTypeDef]
    title: NotRequired[DocumentTextTypeDef]


class SearchContentRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: SearchExpressionTypeDef
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SearchContentRequestSearchContentPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: SearchExpressionTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchSessionsRequestRequestTypeDef(TypedDict):
    assistantId: str
    searchExpression: SearchExpressionTypeDef
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SearchSessionsRequestSearchSessionsPaginateTypeDef(TypedDict):
    assistantId: str
    searchExpression: SearchExpressionTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ChunkingConfigurationOutputTypeDef(TypedDict):
    chunkingStrategy: ChunkingStrategyType
    fixedSizeChunkingConfiguration: NotRequired[FixedSizeChunkingConfigurationTypeDef]
    hierarchicalChunkingConfiguration: NotRequired[HierarchicalChunkingConfigurationOutputTypeDef]
    semanticChunkingConfiguration: NotRequired[SemanticChunkingConfigurationTypeDef]


HierarchicalChunkingConfigurationUnionTypeDef = Union[
    HierarchicalChunkingConfigurationTypeDef, HierarchicalChunkingConfigurationOutputTypeDef
]


class TagFilterOutputTypeDef(TypedDict):
    andConditions: NotRequired[List[TagConditionTypeDef]]
    orConditions: NotRequired[List[OrConditionOutputTypeDef]]
    tagCondition: NotRequired[TagConditionTypeDef]


OrConditionUnionTypeDef = Union[OrConditionTypeDef, OrConditionOutputTypeDef]


class QueryAssistantRequestQueryAssistantPaginateTypeDef(TypedDict):
    assistantId: str
    overrideKnowledgeBaseSearchType: NotRequired[KnowledgeBaseSearchTypeType]
    queryCondition: NotRequired[Sequence[QueryConditionTypeDef]]
    queryInputData: NotRequired[QueryInputDataTypeDef]
    queryText: NotRequired[str]
    sessionId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class QueryAssistantRequestRequestTypeDef(TypedDict):
    assistantId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    overrideKnowledgeBaseSearchType: NotRequired[KnowledgeBaseSearchTypeType]
    queryCondition: NotRequired[Sequence[QueryConditionTypeDef]]
    queryInputData: NotRequired[QueryInputDataTypeDef]
    queryText: NotRequired[str]
    sessionId: NotRequired[str]


RecommendationTriggerTypeDef = TypedDict(
    "RecommendationTriggerTypeDef",
    {
        "data": RecommendationTriggerDataTypeDef,
        "id": str,
        "recommendationIds": List[str],
        "source": RecommendationSourceTypeType,
        "type": RecommendationTriggerTypeType,
    },
)


class QuickResponseDataTypeDef(TypedDict):
    contentType: str
    createdTime: datetime
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    name: str
    quickResponseArn: str
    quickResponseId: str
    status: QuickResponseStatusType
    channels: NotRequired[List[str]]
    contents: NotRequired[QuickResponseContentsTypeDef]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationOutputTypeDef]
    isActive: NotRequired[bool]
    language: NotRequired[str]
    lastModifiedBy: NotRequired[str]
    shortcutKey: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class QuickResponseSearchResultDataTypeDef(TypedDict):
    contentType: str
    contents: QuickResponseContentsTypeDef
    createdTime: datetime
    isActive: bool
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    name: str
    quickResponseArn: str
    quickResponseId: str
    status: QuickResponseStatusType
    attributesInterpolated: NotRequired[List[str]]
    attributesNotInterpolated: NotRequired[List[str]]
    channels: NotRequired[List[str]]
    description: NotRequired[str]
    groupingConfiguration: NotRequired[GroupingConfigurationOutputTypeDef]
    language: NotRequired[str]
    lastModifiedBy: NotRequired[str]
    shortcutKey: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class SearchQuickResponsesRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: QuickResponseSearchExpressionTypeDef
    attributes: NotRequired[Mapping[str, str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SearchQuickResponsesRequestSearchQuickResponsesPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    searchExpression: QuickResponseSearchExpressionTypeDef
    attributes: NotRequired[Mapping[str, str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class UpdateSessionDataRequestRequestTypeDef(TypedDict):
    assistantId: str
    data: Sequence[RuntimeSessionDataTypeDef]
    sessionId: str
    namespace: NotRequired[Literal["Custom"]]


class UpdateSessionDataResponseTypeDef(TypedDict):
    data: List[RuntimeSessionDataTypeDef]
    namespace: Literal["Custom"]
    sessionArn: str
    sessionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class WebCrawlerConfigurationOutputTypeDef(TypedDict):
    urlConfiguration: UrlConfigurationOutputTypeDef
    crawlerLimits: NotRequired[WebCrawlerLimitsTypeDef]
    exclusionFilters: NotRequired[List[str]]
    inclusionFilters: NotRequired[List[str]]
    scope: NotRequired[WebScopeTypeType]


UrlConfigurationUnionTypeDef = Union[UrlConfigurationTypeDef, UrlConfigurationOutputTypeDef]


class CreateAIPromptResponseTypeDef(TypedDict):
    aiPrompt: AIPromptDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAIPromptVersionResponseTypeDef(TypedDict):
    aiPrompt: AIPromptDataTypeDef
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class GetAIPromptResponseTypeDef(TypedDict):
    aiPrompt: AIPromptDataTypeDef
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAIPromptResponseTypeDef(TypedDict):
    aiPrompt: AIPromptDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContentAssociationResponseTypeDef(TypedDict):
    contentAssociation: ContentAssociationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetContentAssociationResponseTypeDef(TypedDict):
    contentAssociation: ContentAssociationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListContentAssociationsResponseTypeDef(TypedDict):
    contentAssociationSummaries: List[ContentAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateAssistantAssociationResponseTypeDef(TypedDict):
    assistantAssociation: AssistantAssociationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAssistantAssociationResponseTypeDef(TypedDict):
    assistantAssociation: AssistantAssociationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAssistantAssociationsResponseTypeDef(TypedDict):
    assistantAssociationSummaries: List[AssistantAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ImportJobDataTypeDef(TypedDict):
    createdTime: datetime
    importJobId: str
    importJobType: Literal["QUICK_RESPONSES"]
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    status: ImportJobStatusType
    uploadId: str
    url: str
    urlExpiry: datetime
    externalSourceConfiguration: NotRequired[ExternalSourceConfigurationTypeDef]
    failedRecordReport: NotRequired[str]
    metadata: NotRequired[Dict[str, str]]


class ImportJobSummaryTypeDef(TypedDict):
    createdTime: datetime
    importJobId: str
    importJobType: Literal["QUICK_RESPONSES"]
    knowledgeBaseArn: str
    knowledgeBaseId: str
    lastModifiedTime: datetime
    status: ImportJobStatusType
    uploadId: str
    externalSourceConfiguration: NotRequired[ExternalSourceConfigurationTypeDef]
    metadata: NotRequired[Dict[str, str]]


class StartImportJobRequestRequestTypeDef(TypedDict):
    importJobType: Literal["QUICK_RESPONSES"]
    knowledgeBaseId: str
    uploadId: str
    clientToken: NotRequired[str]
    externalSourceConfiguration: NotRequired[ExternalSourceConfigurationTypeDef]
    metadata: NotRequired[Mapping[str, str]]


class ContentDataDetailsTypeDef(TypedDict):
    rankingData: RankingDataTypeDef
    textData: TextDataTypeDef


SourceContentDataDetailsTypeDef = TypedDict(
    "SourceContentDataDetailsTypeDef",
    {
        "id": str,
        "rankingData": RankingDataTypeDef,
        "textData": TextDataTypeDef,
        "type": Literal["KNOWLEDGE_CONTENT"],
        "citationSpan": NotRequired[CitationSpanTypeDef],
    },
)


class VectorIngestionConfigurationOutputTypeDef(TypedDict):
    chunkingConfiguration: NotRequired[ChunkingConfigurationOutputTypeDef]
    parsingConfiguration: NotRequired[ParsingConfigurationTypeDef]


class ChunkingConfigurationTypeDef(TypedDict):
    chunkingStrategy: ChunkingStrategyType
    fixedSizeChunkingConfiguration: NotRequired[FixedSizeChunkingConfigurationTypeDef]
    hierarchicalChunkingConfiguration: NotRequired[HierarchicalChunkingConfigurationUnionTypeDef]
    semanticChunkingConfiguration: NotRequired[SemanticChunkingConfigurationTypeDef]


class KnowledgeBaseAssociationConfigurationDataOutputTypeDef(TypedDict):
    contentTagFilter: NotRequired[TagFilterOutputTypeDef]
    maxResults: NotRequired[int]
    overrideKnowledgeBaseSearchType: NotRequired[KnowledgeBaseSearchTypeType]


class SessionDataTypeDef(TypedDict):
    name: str
    sessionArn: str
    sessionId: str
    aiAgentConfiguration: NotRequired[Dict[AIAgentTypeType, AIAgentConfigurationDataTypeDef]]
    description: NotRequired[str]
    integrationConfiguration: NotRequired[SessionIntegrationConfigurationTypeDef]
    tagFilter: NotRequired[TagFilterOutputTypeDef]
    tags: NotRequired[Dict[str, str]]


class TagFilterTypeDef(TypedDict):
    andConditions: NotRequired[Sequence[TagConditionTypeDef]]
    orConditions: NotRequired[Sequence[OrConditionUnionTypeDef]]
    tagCondition: NotRequired[TagConditionTypeDef]


class CreateQuickResponseResponseTypeDef(TypedDict):
    quickResponse: QuickResponseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetQuickResponseResponseTypeDef(TypedDict):
    quickResponse: QuickResponseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateQuickResponseResponseTypeDef(TypedDict):
    quickResponse: QuickResponseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchQuickResponsesResponseTypeDef(TypedDict):
    results: List[QuickResponseSearchResultDataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ManagedSourceConfigurationOutputTypeDef(TypedDict):
    webCrawlerConfiguration: NotRequired[WebCrawlerConfigurationOutputTypeDef]


class WebCrawlerConfigurationTypeDef(TypedDict):
    urlConfiguration: UrlConfigurationUnionTypeDef
    crawlerLimits: NotRequired[WebCrawlerLimitsTypeDef]
    exclusionFilters: NotRequired[Sequence[str]]
    inclusionFilters: NotRequired[Sequence[str]]
    scope: NotRequired[WebScopeTypeType]


class GetImportJobResponseTypeDef(TypedDict):
    importJob: ImportJobDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartImportJobResponseTypeDef(TypedDict):
    importJob: ImportJobDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListImportJobsResponseTypeDef(TypedDict):
    importJobSummaries: List[ImportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DataDetailsPaginatorTypeDef(TypedDict):
    contentData: NotRequired[ContentDataDetailsTypeDef]
    generativeData: NotRequired[GenerativeDataDetailsPaginatorTypeDef]
    intentDetectedData: NotRequired[IntentDetectedDataDetailsTypeDef]
    sourceContentData: NotRequired[SourceContentDataDetailsTypeDef]


class DataDetailsTypeDef(TypedDict):
    contentData: NotRequired[ContentDataDetailsTypeDef]
    generativeData: NotRequired[GenerativeDataDetailsTypeDef]
    intentDetectedData: NotRequired[IntentDetectedDataDetailsTypeDef]
    sourceContentData: NotRequired[SourceContentDataDetailsTypeDef]


ChunkingConfigurationUnionTypeDef = Union[
    ChunkingConfigurationTypeDef, ChunkingConfigurationOutputTypeDef
]


class AssociationConfigurationDataOutputTypeDef(TypedDict):
    knowledgeBaseAssociationConfigurationData: NotRequired[
        KnowledgeBaseAssociationConfigurationDataOutputTypeDef
    ]


class CreateSessionResponseTypeDef(TypedDict):
    session: SessionDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetSessionResponseTypeDef(TypedDict):
    session: SessionDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSessionResponseTypeDef(TypedDict):
    session: SessionDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSessionRequestRequestTypeDef(TypedDict):
    assistantId: str
    name: str
    aiAgentConfiguration: NotRequired[Mapping[AIAgentTypeType, AIAgentConfigurationDataTypeDef]]
    clientToken: NotRequired[str]
    description: NotRequired[str]
    tagFilter: NotRequired[TagFilterTypeDef]
    tags: NotRequired[Mapping[str, str]]


TagFilterUnionTypeDef = Union[TagFilterTypeDef, TagFilterOutputTypeDef]


class UpdateSessionRequestRequestTypeDef(TypedDict):
    assistantId: str
    sessionId: str
    aiAgentConfiguration: NotRequired[Mapping[AIAgentTypeType, AIAgentConfigurationDataTypeDef]]
    description: NotRequired[str]
    tagFilter: NotRequired[TagFilterTypeDef]


class SourceConfigurationOutputTypeDef(TypedDict):
    appIntegrations: NotRequired[AppIntegrationsConfigurationOutputTypeDef]
    managedSourceConfiguration: NotRequired[ManagedSourceConfigurationOutputTypeDef]


WebCrawlerConfigurationUnionTypeDef = Union[
    WebCrawlerConfigurationTypeDef, WebCrawlerConfigurationOutputTypeDef
]


class DataSummaryPaginatorTypeDef(TypedDict):
    details: DataDetailsPaginatorTypeDef
    reference: DataReferenceTypeDef


class DataSummaryTypeDef(TypedDict):
    details: DataDetailsTypeDef
    reference: DataReferenceTypeDef


class VectorIngestionConfigurationTypeDef(TypedDict):
    chunkingConfiguration: NotRequired[ChunkingConfigurationUnionTypeDef]
    parsingConfiguration: NotRequired[ParsingConfigurationTypeDef]


class AssociationConfigurationOutputTypeDef(TypedDict):
    associationConfigurationData: NotRequired[AssociationConfigurationDataOutputTypeDef]
    associationId: NotRequired[str]
    associationType: NotRequired[Literal["KNOWLEDGE_BASE"]]


class KnowledgeBaseAssociationConfigurationDataTypeDef(TypedDict):
    contentTagFilter: NotRequired[TagFilterUnionTypeDef]
    maxResults: NotRequired[int]
    overrideKnowledgeBaseSearchType: NotRequired[KnowledgeBaseSearchTypeType]


class KnowledgeBaseDataTypeDef(TypedDict):
    knowledgeBaseArn: str
    knowledgeBaseId: str
    knowledgeBaseType: KnowledgeBaseTypeType
    name: str
    status: KnowledgeBaseStatusType
    description: NotRequired[str]
    ingestionFailureReasons: NotRequired[List[str]]
    ingestionStatus: NotRequired[SyncStatusType]
    lastContentModificationTime: NotRequired[datetime]
    renderingConfiguration: NotRequired[RenderingConfigurationTypeDef]
    serverSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    sourceConfiguration: NotRequired[SourceConfigurationOutputTypeDef]
    tags: NotRequired[Dict[str, str]]
    vectorIngestionConfiguration: NotRequired[VectorIngestionConfigurationOutputTypeDef]


class KnowledgeBaseSummaryTypeDef(TypedDict):
    knowledgeBaseArn: str
    knowledgeBaseId: str
    knowledgeBaseType: KnowledgeBaseTypeType
    name: str
    status: KnowledgeBaseStatusType
    description: NotRequired[str]
    renderingConfiguration: NotRequired[RenderingConfigurationTypeDef]
    serverSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    sourceConfiguration: NotRequired[SourceConfigurationOutputTypeDef]
    tags: NotRequired[Dict[str, str]]
    vectorIngestionConfiguration: NotRequired[VectorIngestionConfigurationOutputTypeDef]


class ManagedSourceConfigurationTypeDef(TypedDict):
    webCrawlerConfiguration: NotRequired[WebCrawlerConfigurationUnionTypeDef]


ResultDataPaginatorTypeDef = TypedDict(
    "ResultDataPaginatorTypeDef",
    {
        "resultId": str,
        "data": NotRequired[DataSummaryPaginatorTypeDef],
        "document": NotRequired[DocumentTypeDef],
        "relevanceScore": NotRequired[float],
        "type": NotRequired[QueryResultTypeType],
    },
)
RecommendationDataTypeDef = TypedDict(
    "RecommendationDataTypeDef",
    {
        "recommendationId": str,
        "data": NotRequired[DataSummaryTypeDef],
        "document": NotRequired[DocumentTypeDef],
        "relevanceLevel": NotRequired[RelevanceLevelType],
        "relevanceScore": NotRequired[float],
        "type": NotRequired[RecommendationTypeType],
    },
)
ResultDataTypeDef = TypedDict(
    "ResultDataTypeDef",
    {
        "resultId": str,
        "data": NotRequired[DataSummaryTypeDef],
        "document": NotRequired[DocumentTypeDef],
        "relevanceScore": NotRequired[float],
        "type": NotRequired[QueryResultTypeType],
    },
)


class AnswerRecommendationAIAgentConfigurationOutputTypeDef(TypedDict):
    answerGenerationAIPromptId: NotRequired[str]
    associationConfigurations: NotRequired[List[AssociationConfigurationOutputTypeDef]]
    intentLabelingGenerationAIPromptId: NotRequired[str]
    queryReformulationAIPromptId: NotRequired[str]


class ManualSearchAIAgentConfigurationOutputTypeDef(TypedDict):
    answerGenerationAIPromptId: NotRequired[str]
    associationConfigurations: NotRequired[List[AssociationConfigurationOutputTypeDef]]


KnowledgeBaseAssociationConfigurationDataUnionTypeDef = Union[
    KnowledgeBaseAssociationConfigurationDataTypeDef,
    KnowledgeBaseAssociationConfigurationDataOutputTypeDef,
]


class CreateKnowledgeBaseResponseTypeDef(TypedDict):
    knowledgeBase: KnowledgeBaseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetKnowledgeBaseResponseTypeDef(TypedDict):
    knowledgeBase: KnowledgeBaseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateKnowledgeBaseTemplateUriResponseTypeDef(TypedDict):
    knowledgeBase: KnowledgeBaseDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListKnowledgeBasesResponseTypeDef(TypedDict):
    knowledgeBaseSummaries: List[KnowledgeBaseSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


ManagedSourceConfigurationUnionTypeDef = Union[
    ManagedSourceConfigurationTypeDef, ManagedSourceConfigurationOutputTypeDef
]


class QueryAssistantResponsePaginatorTypeDef(TypedDict):
    results: List[ResultDataPaginatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetRecommendationsResponseTypeDef(TypedDict):
    recommendations: List[RecommendationDataTypeDef]
    triggers: List[RecommendationTriggerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class QueryAssistantResponseTypeDef(TypedDict):
    results: List[ResultDataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AIAgentConfigurationOutputTypeDef(TypedDict):
    answerRecommendationAIAgentConfiguration: NotRequired[
        AnswerRecommendationAIAgentConfigurationOutputTypeDef
    ]
    manualSearchAIAgentConfiguration: NotRequired[ManualSearchAIAgentConfigurationOutputTypeDef]


class AssociationConfigurationDataTypeDef(TypedDict):
    knowledgeBaseAssociationConfigurationData: NotRequired[
        KnowledgeBaseAssociationConfigurationDataUnionTypeDef
    ]


class SourceConfigurationTypeDef(TypedDict):
    appIntegrations: NotRequired[AppIntegrationsConfigurationUnionTypeDef]
    managedSourceConfiguration: NotRequired[ManagedSourceConfigurationUnionTypeDef]


AIAgentDataTypeDef = TypedDict(
    "AIAgentDataTypeDef",
    {
        "aiAgentArn": str,
        "aiAgentId": str,
        "assistantArn": str,
        "assistantId": str,
        "configuration": AIAgentConfigurationOutputTypeDef,
        "name": str,
        "type": AIAgentTypeType,
        "visibilityStatus": VisibilityStatusType,
        "description": NotRequired[str],
        "modifiedTime": NotRequired[datetime],
        "origin": NotRequired[OriginType],
        "status": NotRequired[StatusType],
        "tags": NotRequired[Dict[str, str]],
    },
)
AIAgentSummaryTypeDef = TypedDict(
    "AIAgentSummaryTypeDef",
    {
        "aiAgentArn": str,
        "aiAgentId": str,
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "type": AIAgentTypeType,
        "visibilityStatus": VisibilityStatusType,
        "configuration": NotRequired[AIAgentConfigurationOutputTypeDef],
        "description": NotRequired[str],
        "modifiedTime": NotRequired[datetime],
        "origin": NotRequired[OriginType],
        "status": NotRequired[StatusType],
        "tags": NotRequired[Dict[str, str]],
    },
)
AssociationConfigurationDataUnionTypeDef = Union[
    AssociationConfigurationDataTypeDef, AssociationConfigurationDataOutputTypeDef
]


class CreateKnowledgeBaseRequestRequestTypeDef(TypedDict):
    knowledgeBaseType: KnowledgeBaseTypeType
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    renderingConfiguration: NotRequired[RenderingConfigurationTypeDef]
    serverSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    sourceConfiguration: NotRequired[SourceConfigurationTypeDef]
    tags: NotRequired[Mapping[str, str]]
    vectorIngestionConfiguration: NotRequired[VectorIngestionConfigurationTypeDef]


class CreateAIAgentResponseTypeDef(TypedDict):
    aiAgent: AIAgentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAIAgentVersionResponseTypeDef(TypedDict):
    aiAgent: AIAgentDataTypeDef
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class GetAIAgentResponseTypeDef(TypedDict):
    aiAgent: AIAgentDataTypeDef
    versionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAIAgentResponseTypeDef(TypedDict):
    aiAgent: AIAgentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AIAgentVersionSummaryTypeDef(TypedDict):
    aiAgentSummary: NotRequired[AIAgentSummaryTypeDef]
    versionNumber: NotRequired[int]


class ListAIAgentsResponseTypeDef(TypedDict):
    aiAgentSummaries: List[AIAgentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AssociationConfigurationTypeDef(TypedDict):
    associationConfigurationData: NotRequired[AssociationConfigurationDataUnionTypeDef]
    associationId: NotRequired[str]
    associationType: NotRequired[Literal["KNOWLEDGE_BASE"]]


class ListAIAgentVersionsResponseTypeDef(TypedDict):
    aiAgentVersionSummaries: List[AIAgentVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


AssociationConfigurationUnionTypeDef = Union[
    AssociationConfigurationTypeDef, AssociationConfigurationOutputTypeDef
]


class ManualSearchAIAgentConfigurationTypeDef(TypedDict):
    answerGenerationAIPromptId: NotRequired[str]
    associationConfigurations: NotRequired[Sequence[AssociationConfigurationTypeDef]]


class AnswerRecommendationAIAgentConfigurationTypeDef(TypedDict):
    answerGenerationAIPromptId: NotRequired[str]
    associationConfigurations: NotRequired[Sequence[AssociationConfigurationUnionTypeDef]]
    intentLabelingGenerationAIPromptId: NotRequired[str]
    queryReformulationAIPromptId: NotRequired[str]


ManualSearchAIAgentConfigurationUnionTypeDef = Union[
    ManualSearchAIAgentConfigurationTypeDef, ManualSearchAIAgentConfigurationOutputTypeDef
]
AnswerRecommendationAIAgentConfigurationUnionTypeDef = Union[
    AnswerRecommendationAIAgentConfigurationTypeDef,
    AnswerRecommendationAIAgentConfigurationOutputTypeDef,
]


class AIAgentConfigurationTypeDef(TypedDict):
    answerRecommendationAIAgentConfiguration: NotRequired[
        AnswerRecommendationAIAgentConfigurationUnionTypeDef
    ]
    manualSearchAIAgentConfiguration: NotRequired[ManualSearchAIAgentConfigurationUnionTypeDef]


CreateAIAgentRequestRequestTypeDef = TypedDict(
    "CreateAIAgentRequestRequestTypeDef",
    {
        "assistantId": str,
        "configuration": AIAgentConfigurationTypeDef,
        "name": str,
        "type": AIAgentTypeType,
        "visibilityStatus": VisibilityStatusType,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)


class UpdateAIAgentRequestRequestTypeDef(TypedDict):
    aiAgentId: str
    assistantId: str
    visibilityStatus: VisibilityStatusType
    clientToken: NotRequired[str]
    configuration: NotRequired[AIAgentConfigurationTypeDef]
    description: NotRequired[str]
