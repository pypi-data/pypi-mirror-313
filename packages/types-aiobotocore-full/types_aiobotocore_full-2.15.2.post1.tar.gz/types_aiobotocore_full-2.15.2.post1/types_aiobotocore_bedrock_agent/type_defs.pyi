"""
Type annotations for bedrock-agent service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent/type_defs/)

Usage::

    ```python
    from types_aiobotocore_bedrock_agent.type_defs import S3IdentifierTypeDef

    data: S3IdentifierTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    ActionGroupSignatureType,
    ActionGroupStateType,
    AgentAliasStatusType,
    AgentStatusType,
    ChunkingStrategyType,
    ConfluenceAuthTypeType,
    CreationModeType,
    DataDeletionPolicyType,
    DataSourceStatusType,
    DataSourceTypeType,
    FlowConnectionTypeType,
    FlowNodeIODataTypeType,
    FlowNodeTypeType,
    FlowStatusType,
    FlowValidationSeverityType,
    IngestionJobSortByAttributeType,
    IngestionJobStatusType,
    KnowledgeBaseStateType,
    KnowledgeBaseStatusType,
    KnowledgeBaseStorageTypeType,
    PromptStateType,
    PromptTypeType,
    RequireConfirmationType,
    SortOrderType,
    TypeType,
    WebScopeTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "APISchemaTypeDef",
    "ActionGroupExecutorTypeDef",
    "ActionGroupSummaryTypeDef",
    "AgentActionGroupTypeDef",
    "AgentAliasHistoryEventTypeDef",
    "AgentAliasRoutingConfigurationListItemTypeDef",
    "AgentAliasSummaryTypeDef",
    "AgentAliasTypeDef",
    "AgentFlowNodeConfigurationTypeDef",
    "AgentKnowledgeBaseSummaryTypeDef",
    "AgentKnowledgeBaseTypeDef",
    "AgentSummaryTypeDef",
    "AgentTypeDef",
    "AgentVersionSummaryTypeDef",
    "AgentVersionTypeDef",
    "AssociateAgentKnowledgeBaseRequestRequestTypeDef",
    "AssociateAgentKnowledgeBaseResponseTypeDef",
    "BedrockEmbeddingModelConfigurationTypeDef",
    "BedrockFoundationModelConfigurationTypeDef",
    "ChunkingConfigurationOutputTypeDef",
    "ChunkingConfigurationTypeDef",
    "ChunkingConfigurationUnionTypeDef",
    "ConditionFlowNodeConfigurationOutputTypeDef",
    "ConditionFlowNodeConfigurationTypeDef",
    "ConditionFlowNodeConfigurationUnionTypeDef",
    "ConfluenceCrawlerConfigurationOutputTypeDef",
    "ConfluenceCrawlerConfigurationTypeDef",
    "ConfluenceCrawlerConfigurationUnionTypeDef",
    "ConfluenceDataSourceConfigurationOutputTypeDef",
    "ConfluenceDataSourceConfigurationTypeDef",
    "ConfluenceDataSourceConfigurationUnionTypeDef",
    "ConfluenceSourceConfigurationTypeDef",
    "CrawlFilterConfigurationOutputTypeDef",
    "CrawlFilterConfigurationTypeDef",
    "CrawlFilterConfigurationUnionTypeDef",
    "CreateAgentActionGroupRequestRequestTypeDef",
    "CreateAgentActionGroupResponseTypeDef",
    "CreateAgentAliasRequestRequestTypeDef",
    "CreateAgentAliasResponseTypeDef",
    "CreateAgentRequestRequestTypeDef",
    "CreateAgentResponseTypeDef",
    "CreateDataSourceRequestRequestTypeDef",
    "CreateDataSourceResponseTypeDef",
    "CreateFlowAliasRequestRequestTypeDef",
    "CreateFlowAliasResponseTypeDef",
    "CreateFlowRequestRequestTypeDef",
    "CreateFlowResponseTypeDef",
    "CreateFlowVersionRequestRequestTypeDef",
    "CreateFlowVersionResponseTypeDef",
    "CreateKnowledgeBaseRequestRequestTypeDef",
    "CreateKnowledgeBaseResponseTypeDef",
    "CreatePromptRequestRequestTypeDef",
    "CreatePromptResponseTypeDef",
    "CreatePromptVersionRequestRequestTypeDef",
    "CreatePromptVersionResponseTypeDef",
    "CustomTransformationConfigurationOutputTypeDef",
    "CustomTransformationConfigurationTypeDef",
    "CustomTransformationConfigurationUnionTypeDef",
    "DataSourceConfigurationOutputTypeDef",
    "DataSourceConfigurationTypeDef",
    "DataSourceSummaryTypeDef",
    "DataSourceTypeDef",
    "DeleteAgentActionGroupRequestRequestTypeDef",
    "DeleteAgentAliasRequestRequestTypeDef",
    "DeleteAgentAliasResponseTypeDef",
    "DeleteAgentRequestRequestTypeDef",
    "DeleteAgentResponseTypeDef",
    "DeleteAgentVersionRequestRequestTypeDef",
    "DeleteAgentVersionResponseTypeDef",
    "DeleteDataSourceRequestRequestTypeDef",
    "DeleteDataSourceResponseTypeDef",
    "DeleteFlowAliasRequestRequestTypeDef",
    "DeleteFlowAliasResponseTypeDef",
    "DeleteFlowRequestRequestTypeDef",
    "DeleteFlowResponseTypeDef",
    "DeleteFlowVersionRequestRequestTypeDef",
    "DeleteFlowVersionResponseTypeDef",
    "DeleteKnowledgeBaseRequestRequestTypeDef",
    "DeleteKnowledgeBaseResponseTypeDef",
    "DeletePromptRequestRequestTypeDef",
    "DeletePromptResponseTypeDef",
    "DisassociateAgentKnowledgeBaseRequestRequestTypeDef",
    "EmbeddingModelConfigurationTypeDef",
    "FixedSizeChunkingConfigurationTypeDef",
    "FlowAliasRoutingConfigurationListItemTypeDef",
    "FlowAliasSummaryTypeDef",
    "FlowConditionTypeDef",
    "FlowConditionalConnectionConfigurationTypeDef",
    "FlowConnectionConfigurationTypeDef",
    "FlowConnectionTypeDef",
    "FlowDataConnectionConfigurationTypeDef",
    "FlowDefinitionOutputTypeDef",
    "FlowDefinitionTypeDef",
    "FlowNodeConfigurationOutputTypeDef",
    "FlowNodeConfigurationTypeDef",
    "FlowNodeConfigurationUnionTypeDef",
    "FlowNodeExtraOutputTypeDef",
    "FlowNodeInputTypeDef",
    "FlowNodeOutputTypeDef",
    "FlowNodeTypeDef",
    "FlowNodeUnionTypeDef",
    "FlowSummaryTypeDef",
    "FlowValidationTypeDef",
    "FlowVersionSummaryTypeDef",
    "FunctionOutputTypeDef",
    "FunctionSchemaOutputTypeDef",
    "FunctionSchemaTypeDef",
    "FunctionTypeDef",
    "FunctionUnionTypeDef",
    "GetAgentActionGroupRequestRequestTypeDef",
    "GetAgentActionGroupResponseTypeDef",
    "GetAgentAliasRequestRequestTypeDef",
    "GetAgentAliasResponseTypeDef",
    "GetAgentKnowledgeBaseRequestRequestTypeDef",
    "GetAgentKnowledgeBaseResponseTypeDef",
    "GetAgentRequestRequestTypeDef",
    "GetAgentResponseTypeDef",
    "GetAgentVersionRequestRequestTypeDef",
    "GetAgentVersionResponseTypeDef",
    "GetDataSourceRequestRequestTypeDef",
    "GetDataSourceResponseTypeDef",
    "GetFlowAliasRequestRequestTypeDef",
    "GetFlowAliasResponseTypeDef",
    "GetFlowRequestRequestTypeDef",
    "GetFlowResponseTypeDef",
    "GetFlowVersionRequestRequestTypeDef",
    "GetFlowVersionResponseTypeDef",
    "GetIngestionJobRequestRequestTypeDef",
    "GetIngestionJobResponseTypeDef",
    "GetKnowledgeBaseRequestRequestTypeDef",
    "GetKnowledgeBaseResponseTypeDef",
    "GetPromptRequestRequestTypeDef",
    "GetPromptResponseTypeDef",
    "GuardrailConfigurationTypeDef",
    "HierarchicalChunkingConfigurationOutputTypeDef",
    "HierarchicalChunkingConfigurationTypeDef",
    "HierarchicalChunkingConfigurationUnionTypeDef",
    "HierarchicalChunkingLevelConfigurationTypeDef",
    "InferenceConfigurationOutputTypeDef",
    "InferenceConfigurationTypeDef",
    "InferenceConfigurationUnionTypeDef",
    "IngestionJobFilterTypeDef",
    "IngestionJobSortByTypeDef",
    "IngestionJobStatisticsTypeDef",
    "IngestionJobSummaryTypeDef",
    "IngestionJobTypeDef",
    "IntermediateStorageTypeDef",
    "KnowledgeBaseConfigurationTypeDef",
    "KnowledgeBaseFlowNodeConfigurationTypeDef",
    "KnowledgeBaseSummaryTypeDef",
    "KnowledgeBaseTypeDef",
    "LambdaFunctionFlowNodeConfigurationTypeDef",
    "LexFlowNodeConfigurationTypeDef",
    "ListAgentActionGroupsRequestListAgentActionGroupsPaginateTypeDef",
    "ListAgentActionGroupsRequestRequestTypeDef",
    "ListAgentActionGroupsResponseTypeDef",
    "ListAgentAliasesRequestListAgentAliasesPaginateTypeDef",
    "ListAgentAliasesRequestRequestTypeDef",
    "ListAgentAliasesResponseTypeDef",
    "ListAgentKnowledgeBasesRequestListAgentKnowledgeBasesPaginateTypeDef",
    "ListAgentKnowledgeBasesRequestRequestTypeDef",
    "ListAgentKnowledgeBasesResponseTypeDef",
    "ListAgentVersionsRequestListAgentVersionsPaginateTypeDef",
    "ListAgentVersionsRequestRequestTypeDef",
    "ListAgentVersionsResponseTypeDef",
    "ListAgentsRequestListAgentsPaginateTypeDef",
    "ListAgentsRequestRequestTypeDef",
    "ListAgentsResponseTypeDef",
    "ListDataSourcesRequestListDataSourcesPaginateTypeDef",
    "ListDataSourcesRequestRequestTypeDef",
    "ListDataSourcesResponseTypeDef",
    "ListFlowAliasesRequestListFlowAliasesPaginateTypeDef",
    "ListFlowAliasesRequestRequestTypeDef",
    "ListFlowAliasesResponseTypeDef",
    "ListFlowVersionsRequestListFlowVersionsPaginateTypeDef",
    "ListFlowVersionsRequestRequestTypeDef",
    "ListFlowVersionsResponseTypeDef",
    "ListFlowsRequestListFlowsPaginateTypeDef",
    "ListFlowsRequestRequestTypeDef",
    "ListFlowsResponseTypeDef",
    "ListIngestionJobsRequestListIngestionJobsPaginateTypeDef",
    "ListIngestionJobsRequestRequestTypeDef",
    "ListIngestionJobsResponseTypeDef",
    "ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef",
    "ListKnowledgeBasesRequestRequestTypeDef",
    "ListKnowledgeBasesResponseTypeDef",
    "ListPromptsRequestListPromptsPaginateTypeDef",
    "ListPromptsRequestRequestTypeDef",
    "ListPromptsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MemoryConfigurationOutputTypeDef",
    "MemoryConfigurationTypeDef",
    "MongoDbAtlasConfigurationTypeDef",
    "MongoDbAtlasFieldMappingTypeDef",
    "OpenSearchServerlessConfigurationTypeDef",
    "OpenSearchServerlessFieldMappingTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterDetailTypeDef",
    "ParsingConfigurationTypeDef",
    "ParsingPromptTypeDef",
    "PatternObjectFilterConfigurationOutputTypeDef",
    "PatternObjectFilterConfigurationTypeDef",
    "PatternObjectFilterConfigurationUnionTypeDef",
    "PatternObjectFilterOutputTypeDef",
    "PatternObjectFilterTypeDef",
    "PatternObjectFilterUnionTypeDef",
    "PineconeConfigurationTypeDef",
    "PineconeFieldMappingTypeDef",
    "PrepareAgentRequestRequestTypeDef",
    "PrepareAgentResponseTypeDef",
    "PrepareFlowRequestRequestTypeDef",
    "PrepareFlowResponseTypeDef",
    "PromptConfigurationOutputTypeDef",
    "PromptConfigurationTypeDef",
    "PromptConfigurationUnionTypeDef",
    "PromptFlowNodeConfigurationOutputTypeDef",
    "PromptFlowNodeConfigurationTypeDef",
    "PromptFlowNodeConfigurationUnionTypeDef",
    "PromptFlowNodeInlineConfigurationOutputTypeDef",
    "PromptFlowNodeInlineConfigurationTypeDef",
    "PromptFlowNodeInlineConfigurationUnionTypeDef",
    "PromptFlowNodeResourceConfigurationTypeDef",
    "PromptFlowNodeSourceConfigurationOutputTypeDef",
    "PromptFlowNodeSourceConfigurationTypeDef",
    "PromptFlowNodeSourceConfigurationUnionTypeDef",
    "PromptInferenceConfigurationOutputTypeDef",
    "PromptInferenceConfigurationTypeDef",
    "PromptInferenceConfigurationUnionTypeDef",
    "PromptInputVariableTypeDef",
    "PromptMetadataEntryTypeDef",
    "PromptModelInferenceConfigurationOutputTypeDef",
    "PromptModelInferenceConfigurationTypeDef",
    "PromptModelInferenceConfigurationUnionTypeDef",
    "PromptOverrideConfigurationOutputTypeDef",
    "PromptOverrideConfigurationTypeDef",
    "PromptSummaryTypeDef",
    "PromptTemplateConfigurationOutputTypeDef",
    "PromptTemplateConfigurationTypeDef",
    "PromptTemplateConfigurationUnionTypeDef",
    "PromptVariantOutputTypeDef",
    "PromptVariantTypeDef",
    "PromptVariantUnionTypeDef",
    "RdsConfigurationTypeDef",
    "RdsFieldMappingTypeDef",
    "RedisEnterpriseCloudConfigurationTypeDef",
    "RedisEnterpriseCloudFieldMappingTypeDef",
    "ResponseMetadataTypeDef",
    "RetrievalFlowNodeConfigurationTypeDef",
    "RetrievalFlowNodeS3ConfigurationTypeDef",
    "RetrievalFlowNodeServiceConfigurationTypeDef",
    "S3DataSourceConfigurationOutputTypeDef",
    "S3DataSourceConfigurationTypeDef",
    "S3DataSourceConfigurationUnionTypeDef",
    "S3IdentifierTypeDef",
    "S3LocationTypeDef",
    "SalesforceCrawlerConfigurationOutputTypeDef",
    "SalesforceCrawlerConfigurationTypeDef",
    "SalesforceCrawlerConfigurationUnionTypeDef",
    "SalesforceDataSourceConfigurationOutputTypeDef",
    "SalesforceDataSourceConfigurationTypeDef",
    "SalesforceDataSourceConfigurationUnionTypeDef",
    "SalesforceSourceConfigurationTypeDef",
    "SeedUrlTypeDef",
    "SemanticChunkingConfigurationTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "SharePointCrawlerConfigurationOutputTypeDef",
    "SharePointCrawlerConfigurationTypeDef",
    "SharePointCrawlerConfigurationUnionTypeDef",
    "SharePointDataSourceConfigurationOutputTypeDef",
    "SharePointDataSourceConfigurationTypeDef",
    "SharePointDataSourceConfigurationUnionTypeDef",
    "SharePointSourceConfigurationOutputTypeDef",
    "SharePointSourceConfigurationTypeDef",
    "SharePointSourceConfigurationUnionTypeDef",
    "StartIngestionJobRequestRequestTypeDef",
    "StartIngestionJobResponseTypeDef",
    "StopIngestionJobRequestRequestTypeDef",
    "StopIngestionJobResponseTypeDef",
    "StorageConfigurationTypeDef",
    "StorageFlowNodeConfigurationTypeDef",
    "StorageFlowNodeS3ConfigurationTypeDef",
    "StorageFlowNodeServiceConfigurationTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TextPromptTemplateConfigurationOutputTypeDef",
    "TextPromptTemplateConfigurationTypeDef",
    "TextPromptTemplateConfigurationUnionTypeDef",
    "TransformationFunctionTypeDef",
    "TransformationLambdaConfigurationTypeDef",
    "TransformationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAgentActionGroupRequestRequestTypeDef",
    "UpdateAgentActionGroupResponseTypeDef",
    "UpdateAgentAliasRequestRequestTypeDef",
    "UpdateAgentAliasResponseTypeDef",
    "UpdateAgentKnowledgeBaseRequestRequestTypeDef",
    "UpdateAgentKnowledgeBaseResponseTypeDef",
    "UpdateAgentRequestRequestTypeDef",
    "UpdateAgentResponseTypeDef",
    "UpdateDataSourceRequestRequestTypeDef",
    "UpdateDataSourceResponseTypeDef",
    "UpdateFlowAliasRequestRequestTypeDef",
    "UpdateFlowAliasResponseTypeDef",
    "UpdateFlowRequestRequestTypeDef",
    "UpdateFlowResponseTypeDef",
    "UpdateKnowledgeBaseRequestRequestTypeDef",
    "UpdateKnowledgeBaseResponseTypeDef",
    "UpdatePromptRequestRequestTypeDef",
    "UpdatePromptResponseTypeDef",
    "UrlConfigurationOutputTypeDef",
    "UrlConfigurationTypeDef",
    "UrlConfigurationUnionTypeDef",
    "VectorIngestionConfigurationOutputTypeDef",
    "VectorIngestionConfigurationTypeDef",
    "VectorKnowledgeBaseConfigurationTypeDef",
    "WebCrawlerConfigurationOutputTypeDef",
    "WebCrawlerConfigurationTypeDef",
    "WebCrawlerConfigurationUnionTypeDef",
    "WebCrawlerLimitsTypeDef",
    "WebDataSourceConfigurationOutputTypeDef",
    "WebDataSourceConfigurationTypeDef",
    "WebDataSourceConfigurationUnionTypeDef",
    "WebSourceConfigurationOutputTypeDef",
    "WebSourceConfigurationTypeDef",
    "WebSourceConfigurationUnionTypeDef",
)

class S3IdentifierTypeDef(TypedDict):
    s3BucketName: NotRequired[str]
    s3ObjectKey: NotRequired[str]

ActionGroupExecutorTypeDef = TypedDict(
    "ActionGroupExecutorTypeDef",
    {
        "customControl": NotRequired[Literal["RETURN_CONTROL"]],
        "lambda": NotRequired[str],
    },
)

class ActionGroupSummaryTypeDef(TypedDict):
    actionGroupId: str
    actionGroupName: str
    actionGroupState: ActionGroupStateType
    updatedAt: datetime
    description: NotRequired[str]

class AgentAliasRoutingConfigurationListItemTypeDef(TypedDict):
    agentVersion: NotRequired[str]
    provisionedThroughput: NotRequired[str]

class AgentFlowNodeConfigurationTypeDef(TypedDict):
    agentAliasArn: str

class AgentKnowledgeBaseSummaryTypeDef(TypedDict):
    knowledgeBaseId: str
    knowledgeBaseState: KnowledgeBaseStateType
    updatedAt: datetime
    description: NotRequired[str]

class AgentKnowledgeBaseTypeDef(TypedDict):
    agentId: str
    agentVersion: str
    createdAt: datetime
    description: str
    knowledgeBaseId: str
    knowledgeBaseState: KnowledgeBaseStateType
    updatedAt: datetime

class GuardrailConfigurationTypeDef(TypedDict):
    guardrailIdentifier: NotRequired[str]
    guardrailVersion: NotRequired[str]

class MemoryConfigurationOutputTypeDef(TypedDict):
    enabledMemoryTypes: List[Literal["SESSION_SUMMARY"]]
    storageDays: NotRequired[int]

class AssociateAgentKnowledgeBaseRequestRequestTypeDef(TypedDict):
    agentId: str
    agentVersion: str
    description: str
    knowledgeBaseId: str
    knowledgeBaseState: NotRequired[KnowledgeBaseStateType]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BedrockEmbeddingModelConfigurationTypeDef(TypedDict):
    dimensions: NotRequired[int]

class ParsingPromptTypeDef(TypedDict):
    parsingPromptText: str

class FixedSizeChunkingConfigurationTypeDef(TypedDict):
    maxTokens: int
    overlapPercentage: int

class SemanticChunkingConfigurationTypeDef(TypedDict):
    breakpointPercentileThreshold: int
    bufferSize: int
    maxTokens: int

class FlowConditionTypeDef(TypedDict):
    name: str
    expression: NotRequired[str]

class ConfluenceSourceConfigurationTypeDef(TypedDict):
    authType: ConfluenceAuthTypeType
    credentialsSecretArn: str
    hostType: Literal["SAAS"]
    hostUrl: str

class MemoryConfigurationTypeDef(TypedDict):
    enabledMemoryTypes: Sequence[Literal["SESSION_SUMMARY"]]
    storageDays: NotRequired[int]

class ServerSideEncryptionConfigurationTypeDef(TypedDict):
    kmsKeyArn: NotRequired[str]

class FlowAliasRoutingConfigurationListItemTypeDef(TypedDict):
    flowVersion: NotRequired[str]

class CreateFlowVersionRequestRequestTypeDef(TypedDict):
    flowIdentifier: str
    clientToken: NotRequired[str]
    description: NotRequired[str]

class CreatePromptVersionRequestRequestTypeDef(TypedDict):
    promptIdentifier: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class S3DataSourceConfigurationOutputTypeDef(TypedDict):
    bucketArn: str
    bucketOwnerAccountId: NotRequired[str]
    inclusionPrefixes: NotRequired[List[str]]

class DataSourceSummaryTypeDef(TypedDict):
    dataSourceId: str
    knowledgeBaseId: str
    name: str
    status: DataSourceStatusType
    updatedAt: datetime
    description: NotRequired[str]

class DeleteAgentActionGroupRequestRequestTypeDef(TypedDict):
    actionGroupId: str
    agentId: str
    agentVersion: str
    skipResourceInUseCheck: NotRequired[bool]

class DeleteAgentAliasRequestRequestTypeDef(TypedDict):
    agentAliasId: str
    agentId: str

class DeleteAgentRequestRequestTypeDef(TypedDict):
    agentId: str
    skipResourceInUseCheck: NotRequired[bool]

class DeleteAgentVersionRequestRequestTypeDef(TypedDict):
    agentId: str
    agentVersion: str
    skipResourceInUseCheck: NotRequired[bool]

class DeleteDataSourceRequestRequestTypeDef(TypedDict):
    dataSourceId: str
    knowledgeBaseId: str

class DeleteFlowAliasRequestRequestTypeDef(TypedDict):
    aliasIdentifier: str
    flowIdentifier: str

class DeleteFlowRequestRequestTypeDef(TypedDict):
    flowIdentifier: str
    skipResourceInUseCheck: NotRequired[bool]

class DeleteFlowVersionRequestRequestTypeDef(TypedDict):
    flowIdentifier: str
    flowVersion: str
    skipResourceInUseCheck: NotRequired[bool]

class DeleteKnowledgeBaseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str

class DeletePromptRequestRequestTypeDef(TypedDict):
    promptIdentifier: str
    promptVersion: NotRequired[str]

class DisassociateAgentKnowledgeBaseRequestRequestTypeDef(TypedDict):
    agentId: str
    agentVersion: str
    knowledgeBaseId: str

class FlowConditionalConnectionConfigurationTypeDef(TypedDict):
    condition: str

class FlowDataConnectionConfigurationTypeDef(TypedDict):
    sourceOutput: str
    targetInput: str

class KnowledgeBaseFlowNodeConfigurationTypeDef(TypedDict):
    knowledgeBaseId: str
    modelId: NotRequired[str]

class LambdaFunctionFlowNodeConfigurationTypeDef(TypedDict):
    lambdaArn: str

class LexFlowNodeConfigurationTypeDef(TypedDict):
    botAliasArn: str
    localeId: str

FlowNodeInputTypeDef = TypedDict(
    "FlowNodeInputTypeDef",
    {
        "expression": str,
        "name": str,
        "type": FlowNodeIODataTypeType,
    },
)
FlowNodeOutputTypeDef = TypedDict(
    "FlowNodeOutputTypeDef",
    {
        "name": str,
        "type": FlowNodeIODataTypeType,
    },
)
FlowSummaryTypeDef = TypedDict(
    "FlowSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "id": str,
        "name": str,
        "status": FlowStatusType,
        "updatedAt": datetime,
        "version": str,
        "description": NotRequired[str],
    },
)

class FlowValidationTypeDef(TypedDict):
    message: str
    severity: FlowValidationSeverityType

FlowVersionSummaryTypeDef = TypedDict(
    "FlowVersionSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "id": str,
        "status": FlowStatusType,
        "version": str,
    },
)
ParameterDetailTypeDef = TypedDict(
    "ParameterDetailTypeDef",
    {
        "type": TypeType,
        "description": NotRequired[str],
        "required": NotRequired[bool],
    },
)

class GetAgentActionGroupRequestRequestTypeDef(TypedDict):
    actionGroupId: str
    agentId: str
    agentVersion: str

class GetAgentAliasRequestRequestTypeDef(TypedDict):
    agentAliasId: str
    agentId: str

class GetAgentKnowledgeBaseRequestRequestTypeDef(TypedDict):
    agentId: str
    agentVersion: str
    knowledgeBaseId: str

class GetAgentRequestRequestTypeDef(TypedDict):
    agentId: str

class GetAgentVersionRequestRequestTypeDef(TypedDict):
    agentId: str
    agentVersion: str

class GetDataSourceRequestRequestTypeDef(TypedDict):
    dataSourceId: str
    knowledgeBaseId: str

class GetFlowAliasRequestRequestTypeDef(TypedDict):
    aliasIdentifier: str
    flowIdentifier: str

class GetFlowRequestRequestTypeDef(TypedDict):
    flowIdentifier: str

class GetFlowVersionRequestRequestTypeDef(TypedDict):
    flowIdentifier: str
    flowVersion: str

class GetIngestionJobRequestRequestTypeDef(TypedDict):
    dataSourceId: str
    ingestionJobId: str
    knowledgeBaseId: str

class GetKnowledgeBaseRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str

class GetPromptRequestRequestTypeDef(TypedDict):
    promptIdentifier: str
    promptVersion: NotRequired[str]

class HierarchicalChunkingLevelConfigurationTypeDef(TypedDict):
    maxTokens: int

class InferenceConfigurationOutputTypeDef(TypedDict):
    maximumLength: NotRequired[int]
    stopSequences: NotRequired[List[str]]
    temperature: NotRequired[float]
    topK: NotRequired[int]
    topP: NotRequired[float]

class InferenceConfigurationTypeDef(TypedDict):
    maximumLength: NotRequired[int]
    stopSequences: NotRequired[Sequence[str]]
    temperature: NotRequired[float]
    topK: NotRequired[int]
    topP: NotRequired[float]

IngestionJobFilterTypeDef = TypedDict(
    "IngestionJobFilterTypeDef",
    {
        "attribute": Literal["STATUS"],
        "operator": Literal["EQ"],
        "values": Sequence[str],
    },
)

class IngestionJobSortByTypeDef(TypedDict):
    attribute: IngestionJobSortByAttributeType
    order: SortOrderType

class IngestionJobStatisticsTypeDef(TypedDict):
    numberOfDocumentsDeleted: NotRequired[int]
    numberOfDocumentsFailed: NotRequired[int]
    numberOfDocumentsScanned: NotRequired[int]
    numberOfMetadataDocumentsModified: NotRequired[int]
    numberOfMetadataDocumentsScanned: NotRequired[int]
    numberOfModifiedDocumentsIndexed: NotRequired[int]
    numberOfNewDocumentsIndexed: NotRequired[int]

class S3LocationTypeDef(TypedDict):
    uri: str

class KnowledgeBaseSummaryTypeDef(TypedDict):
    knowledgeBaseId: str
    name: str
    status: KnowledgeBaseStatusType
    updatedAt: datetime
    description: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAgentActionGroupsRequestRequestTypeDef(TypedDict):
    agentId: str
    agentVersion: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAgentAliasesRequestRequestTypeDef(TypedDict):
    agentId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAgentKnowledgeBasesRequestRequestTypeDef(TypedDict):
    agentId: str
    agentVersion: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAgentVersionsRequestRequestTypeDef(TypedDict):
    agentId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAgentsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListDataSourcesRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListFlowAliasesRequestRequestTypeDef(TypedDict):
    flowIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListFlowVersionsRequestRequestTypeDef(TypedDict):
    flowIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListFlowsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListKnowledgeBasesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListPromptsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    promptIdentifier: NotRequired[str]

PromptSummaryTypeDef = TypedDict(
    "PromptSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "id": str,
        "name": str,
        "updatedAt": datetime,
        "version": str,
        "description": NotRequired[str],
    },
)

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class MongoDbAtlasFieldMappingTypeDef(TypedDict):
    metadataField: str
    textField: str
    vectorField: str

class OpenSearchServerlessFieldMappingTypeDef(TypedDict):
    metadataField: str
    textField: str
    vectorField: str

class PatternObjectFilterOutputTypeDef(TypedDict):
    objectType: str
    exclusionFilters: NotRequired[List[str]]
    inclusionFilters: NotRequired[List[str]]

class PatternObjectFilterTypeDef(TypedDict):
    objectType: str
    exclusionFilters: NotRequired[Sequence[str]]
    inclusionFilters: NotRequired[Sequence[str]]

class PineconeFieldMappingTypeDef(TypedDict):
    metadataField: str
    textField: str

class PrepareAgentRequestRequestTypeDef(TypedDict):
    agentId: str

class PrepareFlowRequestRequestTypeDef(TypedDict):
    flowIdentifier: str

class PromptFlowNodeResourceConfigurationTypeDef(TypedDict):
    promptArn: str

class PromptModelInferenceConfigurationOutputTypeDef(TypedDict):
    maxTokens: NotRequired[int]
    stopSequences: NotRequired[List[str]]
    temperature: NotRequired[float]
    topK: NotRequired[int]
    topP: NotRequired[float]

class PromptInputVariableTypeDef(TypedDict):
    name: NotRequired[str]

class PromptMetadataEntryTypeDef(TypedDict):
    key: str
    value: str

class PromptModelInferenceConfigurationTypeDef(TypedDict):
    maxTokens: NotRequired[int]
    stopSequences: NotRequired[Sequence[str]]
    temperature: NotRequired[float]
    topK: NotRequired[int]
    topP: NotRequired[float]

class RdsFieldMappingTypeDef(TypedDict):
    metadataField: str
    primaryKeyField: str
    textField: str
    vectorField: str

class RedisEnterpriseCloudFieldMappingTypeDef(TypedDict):
    metadataField: str
    textField: str
    vectorField: str

class RetrievalFlowNodeS3ConfigurationTypeDef(TypedDict):
    bucketName: str

class S3DataSourceConfigurationTypeDef(TypedDict):
    bucketArn: str
    bucketOwnerAccountId: NotRequired[str]
    inclusionPrefixes: NotRequired[Sequence[str]]

class SalesforceSourceConfigurationTypeDef(TypedDict):
    authType: Literal["OAUTH2_CLIENT_CREDENTIALS"]
    credentialsSecretArn: str
    hostUrl: str

class SeedUrlTypeDef(TypedDict):
    url: NotRequired[str]

class SharePointSourceConfigurationOutputTypeDef(TypedDict):
    authType: Literal["OAUTH2_CLIENT_CREDENTIALS"]
    credentialsSecretArn: str
    domain: str
    hostType: Literal["ONLINE"]
    siteUrls: List[str]
    tenantId: NotRequired[str]

class SharePointSourceConfigurationTypeDef(TypedDict):
    authType: Literal["OAUTH2_CLIENT_CREDENTIALS"]
    credentialsSecretArn: str
    domain: str
    hostType: Literal["ONLINE"]
    siteUrls: Sequence[str]
    tenantId: NotRequired[str]

class StartIngestionJobRequestRequestTypeDef(TypedDict):
    dataSourceId: str
    knowledgeBaseId: str
    clientToken: NotRequired[str]
    description: NotRequired[str]

class StopIngestionJobRequestRequestTypeDef(TypedDict):
    dataSourceId: str
    ingestionJobId: str
    knowledgeBaseId: str

class StorageFlowNodeS3ConfigurationTypeDef(TypedDict):
    bucketName: str

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class TransformationLambdaConfigurationTypeDef(TypedDict):
    lambdaArn: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateAgentKnowledgeBaseRequestRequestTypeDef(TypedDict):
    agentId: str
    agentVersion: str
    knowledgeBaseId: str
    description: NotRequired[str]
    knowledgeBaseState: NotRequired[KnowledgeBaseStateType]

class WebCrawlerLimitsTypeDef(TypedDict):
    rateLimit: NotRequired[int]

class APISchemaTypeDef(TypedDict):
    payload: NotRequired[str]
    s3: NotRequired[S3IdentifierTypeDef]

class AgentAliasHistoryEventTypeDef(TypedDict):
    endDate: NotRequired[datetime]
    routingConfiguration: NotRequired[List[AgentAliasRoutingConfigurationListItemTypeDef]]
    startDate: NotRequired[datetime]

class AgentAliasSummaryTypeDef(TypedDict):
    agentAliasId: str
    agentAliasName: str
    agentAliasStatus: AgentAliasStatusType
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]
    routingConfiguration: NotRequired[List[AgentAliasRoutingConfigurationListItemTypeDef]]

class CreateAgentAliasRequestRequestTypeDef(TypedDict):
    agentAliasName: str
    agentId: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    routingConfiguration: NotRequired[Sequence[AgentAliasRoutingConfigurationListItemTypeDef]]
    tags: NotRequired[Mapping[str, str]]

class UpdateAgentAliasRequestRequestTypeDef(TypedDict):
    agentAliasId: str
    agentAliasName: str
    agentId: str
    description: NotRequired[str]
    routingConfiguration: NotRequired[Sequence[AgentAliasRoutingConfigurationListItemTypeDef]]

class AgentSummaryTypeDef(TypedDict):
    agentId: str
    agentName: str
    agentStatus: AgentStatusType
    updatedAt: datetime
    description: NotRequired[str]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    latestAgentVersion: NotRequired[str]

class AgentVersionSummaryTypeDef(TypedDict):
    agentName: str
    agentStatus: AgentStatusType
    agentVersion: str
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]

class AssociateAgentKnowledgeBaseResponseTypeDef(TypedDict):
    agentKnowledgeBase: AgentKnowledgeBaseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAgentAliasResponseTypeDef(TypedDict):
    agentAliasId: str
    agentAliasStatus: AgentAliasStatusType
    agentId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAgentResponseTypeDef(TypedDict):
    agentId: str
    agentStatus: AgentStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAgentVersionResponseTypeDef(TypedDict):
    agentId: str
    agentStatus: AgentStatusType
    agentVersion: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDataSourceResponseTypeDef(TypedDict):
    dataSourceId: str
    knowledgeBaseId: str
    status: DataSourceStatusType
    ResponseMetadata: ResponseMetadataTypeDef

DeleteFlowAliasResponseTypeDef = TypedDict(
    "DeleteFlowAliasResponseTypeDef",
    {
        "flowId": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteFlowResponseTypeDef = TypedDict(
    "DeleteFlowResponseTypeDef",
    {
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteFlowVersionResponseTypeDef = TypedDict(
    "DeleteFlowVersionResponseTypeDef",
    {
        "id": str,
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class DeleteKnowledgeBaseResponseTypeDef(TypedDict):
    knowledgeBaseId: str
    status: KnowledgeBaseStatusType
    ResponseMetadata: ResponseMetadataTypeDef

DeletePromptResponseTypeDef = TypedDict(
    "DeletePromptResponseTypeDef",
    {
        "id": str,
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class GetAgentKnowledgeBaseResponseTypeDef(TypedDict):
    agentKnowledgeBase: AgentKnowledgeBaseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAgentActionGroupsResponseTypeDef(TypedDict):
    actionGroupSummaries: List[ActionGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAgentKnowledgeBasesResponseTypeDef(TypedDict):
    agentKnowledgeBaseSummaries: List[AgentKnowledgeBaseSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PrepareAgentResponseTypeDef(TypedDict):
    agentId: str
    agentStatus: AgentStatusType
    agentVersion: str
    preparedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

PrepareFlowResponseTypeDef = TypedDict(
    "PrepareFlowResponseTypeDef",
    {
        "id": str,
        "status": FlowStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class UpdateAgentKnowledgeBaseResponseTypeDef(TypedDict):
    agentKnowledgeBase: AgentKnowledgeBaseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class EmbeddingModelConfigurationTypeDef(TypedDict):
    bedrockEmbeddingModelConfiguration: NotRequired[BedrockEmbeddingModelConfigurationTypeDef]

class BedrockFoundationModelConfigurationTypeDef(TypedDict):
    modelArn: str
    parsingPrompt: NotRequired[ParsingPromptTypeDef]

class ConditionFlowNodeConfigurationOutputTypeDef(TypedDict):
    conditions: List[FlowConditionTypeDef]

class ConditionFlowNodeConfigurationTypeDef(TypedDict):
    conditions: Sequence[FlowConditionTypeDef]

class CreateFlowAliasRequestRequestTypeDef(TypedDict):
    flowIdentifier: str
    name: str
    routingConfiguration: Sequence[FlowAliasRoutingConfigurationListItemTypeDef]
    clientToken: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

CreateFlowAliasResponseTypeDef = TypedDict(
    "CreateFlowAliasResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "description": str,
        "flowId": str,
        "id": str,
        "name": str,
        "routingConfiguration": List[FlowAliasRoutingConfigurationListItemTypeDef],
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FlowAliasSummaryTypeDef = TypedDict(
    "FlowAliasSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "flowId": str,
        "id": str,
        "name": str,
        "routingConfiguration": List[FlowAliasRoutingConfigurationListItemTypeDef],
        "updatedAt": datetime,
        "description": NotRequired[str],
    },
)
GetFlowAliasResponseTypeDef = TypedDict(
    "GetFlowAliasResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "description": str,
        "flowId": str,
        "id": str,
        "name": str,
        "routingConfiguration": List[FlowAliasRoutingConfigurationListItemTypeDef],
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class UpdateFlowAliasRequestRequestTypeDef(TypedDict):
    aliasIdentifier: str
    flowIdentifier: str
    name: str
    routingConfiguration: Sequence[FlowAliasRoutingConfigurationListItemTypeDef]
    description: NotRequired[str]

UpdateFlowAliasResponseTypeDef = TypedDict(
    "UpdateFlowAliasResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "description": str,
        "flowId": str,
        "id": str,
        "name": str,
        "routingConfiguration": List[FlowAliasRoutingConfigurationListItemTypeDef],
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ListDataSourcesResponseTypeDef(TypedDict):
    dataSourceSummaries: List[DataSourceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class FlowConnectionConfigurationTypeDef(TypedDict):
    conditional: NotRequired[FlowConditionalConnectionConfigurationTypeDef]
    data: NotRequired[FlowDataConnectionConfigurationTypeDef]

class ListFlowsResponseTypeDef(TypedDict):
    flowSummaries: List[FlowSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListFlowVersionsResponseTypeDef(TypedDict):
    flowVersionSummaries: List[FlowVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class FunctionOutputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    parameters: NotRequired[Dict[str, ParameterDetailTypeDef]]
    requireConfirmation: NotRequired[RequireConfirmationType]

class FunctionTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    parameters: NotRequired[Mapping[str, ParameterDetailTypeDef]]
    requireConfirmation: NotRequired[RequireConfirmationType]

class HierarchicalChunkingConfigurationOutputTypeDef(TypedDict):
    levelConfigurations: List[HierarchicalChunkingLevelConfigurationTypeDef]
    overlapTokens: int

class HierarchicalChunkingConfigurationTypeDef(TypedDict):
    levelConfigurations: Sequence[HierarchicalChunkingLevelConfigurationTypeDef]
    overlapTokens: int

class PromptConfigurationOutputTypeDef(TypedDict):
    basePromptTemplate: NotRequired[str]
    inferenceConfiguration: NotRequired[InferenceConfigurationOutputTypeDef]
    parserMode: NotRequired[CreationModeType]
    promptCreationMode: NotRequired[CreationModeType]
    promptState: NotRequired[PromptStateType]
    promptType: NotRequired[PromptTypeType]

InferenceConfigurationUnionTypeDef = Union[
    InferenceConfigurationTypeDef, InferenceConfigurationOutputTypeDef
]

class ListIngestionJobsRequestRequestTypeDef(TypedDict):
    dataSourceId: str
    knowledgeBaseId: str
    filters: NotRequired[Sequence[IngestionJobFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[IngestionJobSortByTypeDef]

class IngestionJobSummaryTypeDef(TypedDict):
    dataSourceId: str
    ingestionJobId: str
    knowledgeBaseId: str
    startedAt: datetime
    status: IngestionJobStatusType
    updatedAt: datetime
    description: NotRequired[str]
    statistics: NotRequired[IngestionJobStatisticsTypeDef]

class IngestionJobTypeDef(TypedDict):
    dataSourceId: str
    ingestionJobId: str
    knowledgeBaseId: str
    startedAt: datetime
    status: IngestionJobStatusType
    updatedAt: datetime
    description: NotRequired[str]
    failureReasons: NotRequired[List[str]]
    statistics: NotRequired[IngestionJobStatisticsTypeDef]

class IntermediateStorageTypeDef(TypedDict):
    s3Location: S3LocationTypeDef

class ListKnowledgeBasesResponseTypeDef(TypedDict):
    knowledgeBaseSummaries: List[KnowledgeBaseSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAgentActionGroupsRequestListAgentActionGroupsPaginateTypeDef(TypedDict):
    agentId: str
    agentVersion: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAgentAliasesRequestListAgentAliasesPaginateTypeDef(TypedDict):
    agentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAgentKnowledgeBasesRequestListAgentKnowledgeBasesPaginateTypeDef(TypedDict):
    agentId: str
    agentVersion: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAgentVersionsRequestListAgentVersionsPaginateTypeDef(TypedDict):
    agentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAgentsRequestListAgentsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDataSourcesRequestListDataSourcesPaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFlowAliasesRequestListFlowAliasesPaginateTypeDef(TypedDict):
    flowIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFlowVersionsRequestListFlowVersionsPaginateTypeDef(TypedDict):
    flowIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFlowsRequestListFlowsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListIngestionJobsRequestListIngestionJobsPaginateTypeDef(TypedDict):
    dataSourceId: str
    knowledgeBaseId: str
    filters: NotRequired[Sequence[IngestionJobFilterTypeDef]]
    sortBy: NotRequired[IngestionJobSortByTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPromptsRequestListPromptsPaginateTypeDef(TypedDict):
    promptIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPromptsResponseTypeDef(TypedDict):
    promptSummaries: List[PromptSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class MongoDbAtlasConfigurationTypeDef(TypedDict):
    collectionName: str
    credentialsSecretArn: str
    databaseName: str
    endpoint: str
    fieldMapping: MongoDbAtlasFieldMappingTypeDef
    vectorIndexName: str
    endpointServiceName: NotRequired[str]

class OpenSearchServerlessConfigurationTypeDef(TypedDict):
    collectionArn: str
    fieldMapping: OpenSearchServerlessFieldMappingTypeDef
    vectorIndexName: str

class PatternObjectFilterConfigurationOutputTypeDef(TypedDict):
    filters: List[PatternObjectFilterOutputTypeDef]

PatternObjectFilterUnionTypeDef = Union[
    PatternObjectFilterTypeDef, PatternObjectFilterOutputTypeDef
]

class PineconeConfigurationTypeDef(TypedDict):
    connectionString: str
    credentialsSecretArn: str
    fieldMapping: PineconeFieldMappingTypeDef
    namespace: NotRequired[str]

class PromptInferenceConfigurationOutputTypeDef(TypedDict):
    text: NotRequired[PromptModelInferenceConfigurationOutputTypeDef]

class TextPromptTemplateConfigurationOutputTypeDef(TypedDict):
    text: str
    inputVariables: NotRequired[List[PromptInputVariableTypeDef]]

class TextPromptTemplateConfigurationTypeDef(TypedDict):
    text: str
    inputVariables: NotRequired[Sequence[PromptInputVariableTypeDef]]

PromptModelInferenceConfigurationUnionTypeDef = Union[
    PromptModelInferenceConfigurationTypeDef, PromptModelInferenceConfigurationOutputTypeDef
]

class RdsConfigurationTypeDef(TypedDict):
    credentialsSecretArn: str
    databaseName: str
    fieldMapping: RdsFieldMappingTypeDef
    resourceArn: str
    tableName: str

class RedisEnterpriseCloudConfigurationTypeDef(TypedDict):
    credentialsSecretArn: str
    endpoint: str
    fieldMapping: RedisEnterpriseCloudFieldMappingTypeDef
    vectorIndexName: str

class RetrievalFlowNodeServiceConfigurationTypeDef(TypedDict):
    s3: NotRequired[RetrievalFlowNodeS3ConfigurationTypeDef]

S3DataSourceConfigurationUnionTypeDef = Union[
    S3DataSourceConfigurationTypeDef, S3DataSourceConfigurationOutputTypeDef
]

class UrlConfigurationOutputTypeDef(TypedDict):
    seedUrls: NotRequired[List[SeedUrlTypeDef]]

class UrlConfigurationTypeDef(TypedDict):
    seedUrls: NotRequired[Sequence[SeedUrlTypeDef]]

SharePointSourceConfigurationUnionTypeDef = Union[
    SharePointSourceConfigurationTypeDef, SharePointSourceConfigurationOutputTypeDef
]

class StorageFlowNodeServiceConfigurationTypeDef(TypedDict):
    s3: NotRequired[StorageFlowNodeS3ConfigurationTypeDef]

class TransformationFunctionTypeDef(TypedDict):
    transformationLambdaConfiguration: TransformationLambdaConfigurationTypeDef

class WebCrawlerConfigurationOutputTypeDef(TypedDict):
    crawlerLimits: NotRequired[WebCrawlerLimitsTypeDef]
    exclusionFilters: NotRequired[List[str]]
    inclusionFilters: NotRequired[List[str]]
    scope: NotRequired[WebScopeTypeType]

class WebCrawlerConfigurationTypeDef(TypedDict):
    crawlerLimits: NotRequired[WebCrawlerLimitsTypeDef]
    exclusionFilters: NotRequired[Sequence[str]]
    inclusionFilters: NotRequired[Sequence[str]]
    scope: NotRequired[WebScopeTypeType]

class AgentAliasTypeDef(TypedDict):
    agentAliasArn: str
    agentAliasId: str
    agentAliasName: str
    agentAliasStatus: AgentAliasStatusType
    agentId: str
    createdAt: datetime
    routingConfiguration: List[AgentAliasRoutingConfigurationListItemTypeDef]
    updatedAt: datetime
    agentAliasHistoryEvents: NotRequired[List[AgentAliasHistoryEventTypeDef]]
    clientToken: NotRequired[str]
    description: NotRequired[str]
    failureReasons: NotRequired[List[str]]

class ListAgentAliasesResponseTypeDef(TypedDict):
    agentAliasSummaries: List[AgentAliasSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAgentsResponseTypeDef(TypedDict):
    agentSummaries: List[AgentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAgentVersionsResponseTypeDef(TypedDict):
    agentVersionSummaries: List[AgentVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class VectorKnowledgeBaseConfigurationTypeDef(TypedDict):
    embeddingModelArn: str
    embeddingModelConfiguration: NotRequired[EmbeddingModelConfigurationTypeDef]

class ParsingConfigurationTypeDef(TypedDict):
    parsingStrategy: Literal["BEDROCK_FOUNDATION_MODEL"]
    bedrockFoundationModelConfiguration: NotRequired[BedrockFoundationModelConfigurationTypeDef]

ConditionFlowNodeConfigurationUnionTypeDef = Union[
    ConditionFlowNodeConfigurationTypeDef, ConditionFlowNodeConfigurationOutputTypeDef
]

class ListFlowAliasesResponseTypeDef(TypedDict):
    flowAliasSummaries: List[FlowAliasSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

FlowConnectionTypeDef = TypedDict(
    "FlowConnectionTypeDef",
    {
        "name": str,
        "source": str,
        "target": str,
        "type": FlowConnectionTypeType,
        "configuration": NotRequired[FlowConnectionConfigurationTypeDef],
    },
)

class FunctionSchemaOutputTypeDef(TypedDict):
    functions: NotRequired[List[FunctionOutputTypeDef]]

FunctionUnionTypeDef = Union[FunctionTypeDef, FunctionOutputTypeDef]

class ChunkingConfigurationOutputTypeDef(TypedDict):
    chunkingStrategy: ChunkingStrategyType
    fixedSizeChunkingConfiguration: NotRequired[FixedSizeChunkingConfigurationTypeDef]
    hierarchicalChunkingConfiguration: NotRequired[HierarchicalChunkingConfigurationOutputTypeDef]
    semanticChunkingConfiguration: NotRequired[SemanticChunkingConfigurationTypeDef]

HierarchicalChunkingConfigurationUnionTypeDef = Union[
    HierarchicalChunkingConfigurationTypeDef, HierarchicalChunkingConfigurationOutputTypeDef
]

class PromptOverrideConfigurationOutputTypeDef(TypedDict):
    promptConfigurations: List[PromptConfigurationOutputTypeDef]
    overrideLambda: NotRequired[str]

class PromptConfigurationTypeDef(TypedDict):
    basePromptTemplate: NotRequired[str]
    inferenceConfiguration: NotRequired[InferenceConfigurationUnionTypeDef]
    parserMode: NotRequired[CreationModeType]
    promptCreationMode: NotRequired[CreationModeType]
    promptState: NotRequired[PromptStateType]
    promptType: NotRequired[PromptTypeType]

class ListIngestionJobsResponseTypeDef(TypedDict):
    ingestionJobSummaries: List[IngestionJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetIngestionJobResponseTypeDef(TypedDict):
    ingestionJob: IngestionJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartIngestionJobResponseTypeDef(TypedDict):
    ingestionJob: IngestionJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StopIngestionJobResponseTypeDef(TypedDict):
    ingestionJob: IngestionJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

CrawlFilterConfigurationOutputTypeDef = TypedDict(
    "CrawlFilterConfigurationOutputTypeDef",
    {
        "type": Literal["PATTERN"],
        "patternObjectFilter": NotRequired[PatternObjectFilterConfigurationOutputTypeDef],
    },
)

class PatternObjectFilterConfigurationTypeDef(TypedDict):
    filters: Sequence[PatternObjectFilterUnionTypeDef]

class PromptTemplateConfigurationOutputTypeDef(TypedDict):
    text: NotRequired[TextPromptTemplateConfigurationOutputTypeDef]

TextPromptTemplateConfigurationUnionTypeDef = Union[
    TextPromptTemplateConfigurationTypeDef, TextPromptTemplateConfigurationOutputTypeDef
]

class PromptInferenceConfigurationTypeDef(TypedDict):
    text: NotRequired[PromptModelInferenceConfigurationUnionTypeDef]

StorageConfigurationTypeDef = TypedDict(
    "StorageConfigurationTypeDef",
    {
        "type": KnowledgeBaseStorageTypeType,
        "mongoDbAtlasConfiguration": NotRequired[MongoDbAtlasConfigurationTypeDef],
        "opensearchServerlessConfiguration": NotRequired[OpenSearchServerlessConfigurationTypeDef],
        "pineconeConfiguration": NotRequired[PineconeConfigurationTypeDef],
        "rdsConfiguration": NotRequired[RdsConfigurationTypeDef],
        "redisEnterpriseCloudConfiguration": NotRequired[RedisEnterpriseCloudConfigurationTypeDef],
    },
)

class RetrievalFlowNodeConfigurationTypeDef(TypedDict):
    serviceConfiguration: RetrievalFlowNodeServiceConfigurationTypeDef

class WebSourceConfigurationOutputTypeDef(TypedDict):
    urlConfiguration: UrlConfigurationOutputTypeDef

UrlConfigurationUnionTypeDef = Union[UrlConfigurationTypeDef, UrlConfigurationOutputTypeDef]

class StorageFlowNodeConfigurationTypeDef(TypedDict):
    serviceConfiguration: StorageFlowNodeServiceConfigurationTypeDef

class TransformationTypeDef(TypedDict):
    stepToApply: Literal["POST_CHUNKING"]
    transformationFunction: TransformationFunctionTypeDef

WebCrawlerConfigurationUnionTypeDef = Union[
    WebCrawlerConfigurationTypeDef, WebCrawlerConfigurationOutputTypeDef
]

class CreateAgentAliasResponseTypeDef(TypedDict):
    agentAlias: AgentAliasTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAgentAliasResponseTypeDef(TypedDict):
    agentAlias: AgentAliasTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAgentAliasResponseTypeDef(TypedDict):
    agentAlias: AgentAliasTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

KnowledgeBaseConfigurationTypeDef = TypedDict(
    "KnowledgeBaseConfigurationTypeDef",
    {
        "type": Literal["VECTOR"],
        "vectorKnowledgeBaseConfiguration": NotRequired[VectorKnowledgeBaseConfigurationTypeDef],
    },
)

class AgentActionGroupTypeDef(TypedDict):
    actionGroupId: str
    actionGroupName: str
    actionGroupState: ActionGroupStateType
    agentId: str
    agentVersion: str
    createdAt: datetime
    updatedAt: datetime
    actionGroupExecutor: NotRequired[ActionGroupExecutorTypeDef]
    apiSchema: NotRequired[APISchemaTypeDef]
    clientToken: NotRequired[str]
    description: NotRequired[str]
    functionSchema: NotRequired[FunctionSchemaOutputTypeDef]
    parentActionSignature: NotRequired[ActionGroupSignatureType]

class FunctionSchemaTypeDef(TypedDict):
    functions: NotRequired[Sequence[FunctionUnionTypeDef]]

class ChunkingConfigurationTypeDef(TypedDict):
    chunkingStrategy: ChunkingStrategyType
    fixedSizeChunkingConfiguration: NotRequired[FixedSizeChunkingConfigurationTypeDef]
    hierarchicalChunkingConfiguration: NotRequired[HierarchicalChunkingConfigurationUnionTypeDef]
    semanticChunkingConfiguration: NotRequired[SemanticChunkingConfigurationTypeDef]

class AgentTypeDef(TypedDict):
    agentArn: str
    agentId: str
    agentName: str
    agentResourceRoleArn: str
    agentStatus: AgentStatusType
    agentVersion: str
    createdAt: datetime
    idleSessionTTLInSeconds: int
    updatedAt: datetime
    clientToken: NotRequired[str]
    customerEncryptionKeyArn: NotRequired[str]
    description: NotRequired[str]
    failureReasons: NotRequired[List[str]]
    foundationModel: NotRequired[str]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    instruction: NotRequired[str]
    memoryConfiguration: NotRequired[MemoryConfigurationOutputTypeDef]
    preparedAt: NotRequired[datetime]
    promptOverrideConfiguration: NotRequired[PromptOverrideConfigurationOutputTypeDef]
    recommendedActions: NotRequired[List[str]]

class AgentVersionTypeDef(TypedDict):
    agentArn: str
    agentId: str
    agentName: str
    agentResourceRoleArn: str
    agentStatus: AgentStatusType
    createdAt: datetime
    idleSessionTTLInSeconds: int
    updatedAt: datetime
    version: str
    customerEncryptionKeyArn: NotRequired[str]
    description: NotRequired[str]
    failureReasons: NotRequired[List[str]]
    foundationModel: NotRequired[str]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    instruction: NotRequired[str]
    memoryConfiguration: NotRequired[MemoryConfigurationOutputTypeDef]
    promptOverrideConfiguration: NotRequired[PromptOverrideConfigurationOutputTypeDef]
    recommendedActions: NotRequired[List[str]]

PromptConfigurationUnionTypeDef = Union[
    PromptConfigurationTypeDef, PromptConfigurationOutputTypeDef
]

class ConfluenceCrawlerConfigurationOutputTypeDef(TypedDict):
    filterConfiguration: NotRequired[CrawlFilterConfigurationOutputTypeDef]

class SalesforceCrawlerConfigurationOutputTypeDef(TypedDict):
    filterConfiguration: NotRequired[CrawlFilterConfigurationOutputTypeDef]

class SharePointCrawlerConfigurationOutputTypeDef(TypedDict):
    filterConfiguration: NotRequired[CrawlFilterConfigurationOutputTypeDef]

PatternObjectFilterConfigurationUnionTypeDef = Union[
    PatternObjectFilterConfigurationTypeDef, PatternObjectFilterConfigurationOutputTypeDef
]

class PromptFlowNodeInlineConfigurationOutputTypeDef(TypedDict):
    modelId: str
    templateConfiguration: PromptTemplateConfigurationOutputTypeDef
    templateType: Literal["TEXT"]
    inferenceConfiguration: NotRequired[PromptInferenceConfigurationOutputTypeDef]

class PromptVariantOutputTypeDef(TypedDict):
    name: str
    templateType: Literal["TEXT"]
    inferenceConfiguration: NotRequired[PromptInferenceConfigurationOutputTypeDef]
    metadata: NotRequired[List[PromptMetadataEntryTypeDef]]
    modelId: NotRequired[str]
    templateConfiguration: NotRequired[PromptTemplateConfigurationOutputTypeDef]

class PromptTemplateConfigurationTypeDef(TypedDict):
    text: NotRequired[TextPromptTemplateConfigurationUnionTypeDef]

PromptInferenceConfigurationUnionTypeDef = Union[
    PromptInferenceConfigurationTypeDef, PromptInferenceConfigurationOutputTypeDef
]

class WebDataSourceConfigurationOutputTypeDef(TypedDict):
    sourceConfiguration: WebSourceConfigurationOutputTypeDef
    crawlerConfiguration: NotRequired[WebCrawlerConfigurationOutputTypeDef]

class WebSourceConfigurationTypeDef(TypedDict):
    urlConfiguration: UrlConfigurationUnionTypeDef

class CustomTransformationConfigurationOutputTypeDef(TypedDict):
    intermediateStorage: IntermediateStorageTypeDef
    transformations: List[TransformationTypeDef]

class CustomTransformationConfigurationTypeDef(TypedDict):
    intermediateStorage: IntermediateStorageTypeDef
    transformations: Sequence[TransformationTypeDef]

class CreateKnowledgeBaseRequestRequestTypeDef(TypedDict):
    knowledgeBaseConfiguration: KnowledgeBaseConfigurationTypeDef
    name: str
    roleArn: str
    storageConfiguration: StorageConfigurationTypeDef
    clientToken: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class KnowledgeBaseTypeDef(TypedDict):
    createdAt: datetime
    knowledgeBaseArn: str
    knowledgeBaseConfiguration: KnowledgeBaseConfigurationTypeDef
    knowledgeBaseId: str
    name: str
    roleArn: str
    status: KnowledgeBaseStatusType
    storageConfiguration: StorageConfigurationTypeDef
    updatedAt: datetime
    description: NotRequired[str]
    failureReasons: NotRequired[List[str]]

class UpdateKnowledgeBaseRequestRequestTypeDef(TypedDict):
    knowledgeBaseConfiguration: KnowledgeBaseConfigurationTypeDef
    knowledgeBaseId: str
    name: str
    roleArn: str
    storageConfiguration: StorageConfigurationTypeDef
    description: NotRequired[str]

class CreateAgentActionGroupResponseTypeDef(TypedDict):
    agentActionGroup: AgentActionGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAgentActionGroupResponseTypeDef(TypedDict):
    agentActionGroup: AgentActionGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAgentActionGroupResponseTypeDef(TypedDict):
    agentActionGroup: AgentActionGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAgentActionGroupRequestRequestTypeDef(TypedDict):
    actionGroupName: str
    agentId: str
    agentVersion: str
    actionGroupExecutor: NotRequired[ActionGroupExecutorTypeDef]
    actionGroupState: NotRequired[ActionGroupStateType]
    apiSchema: NotRequired[APISchemaTypeDef]
    clientToken: NotRequired[str]
    description: NotRequired[str]
    functionSchema: NotRequired[FunctionSchemaTypeDef]
    parentActionGroupSignature: NotRequired[ActionGroupSignatureType]

class UpdateAgentActionGroupRequestRequestTypeDef(TypedDict):
    actionGroupId: str
    actionGroupName: str
    agentId: str
    agentVersion: str
    actionGroupExecutor: NotRequired[ActionGroupExecutorTypeDef]
    actionGroupState: NotRequired[ActionGroupStateType]
    apiSchema: NotRequired[APISchemaTypeDef]
    description: NotRequired[str]
    functionSchema: NotRequired[FunctionSchemaTypeDef]
    parentActionGroupSignature: NotRequired[ActionGroupSignatureType]

ChunkingConfigurationUnionTypeDef = Union[
    ChunkingConfigurationTypeDef, ChunkingConfigurationOutputTypeDef
]

class CreateAgentResponseTypeDef(TypedDict):
    agent: AgentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAgentResponseTypeDef(TypedDict):
    agent: AgentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAgentResponseTypeDef(TypedDict):
    agent: AgentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAgentVersionResponseTypeDef(TypedDict):
    agentVersion: AgentVersionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PromptOverrideConfigurationTypeDef(TypedDict):
    promptConfigurations: Sequence[PromptConfigurationUnionTypeDef]
    overrideLambda: NotRequired[str]

class ConfluenceDataSourceConfigurationOutputTypeDef(TypedDict):
    sourceConfiguration: ConfluenceSourceConfigurationTypeDef
    crawlerConfiguration: NotRequired[ConfluenceCrawlerConfigurationOutputTypeDef]

class SalesforceDataSourceConfigurationOutputTypeDef(TypedDict):
    sourceConfiguration: SalesforceSourceConfigurationTypeDef
    crawlerConfiguration: NotRequired[SalesforceCrawlerConfigurationOutputTypeDef]

class SharePointDataSourceConfigurationOutputTypeDef(TypedDict):
    sourceConfiguration: SharePointSourceConfigurationOutputTypeDef
    crawlerConfiguration: NotRequired[SharePointCrawlerConfigurationOutputTypeDef]

CrawlFilterConfigurationTypeDef = TypedDict(
    "CrawlFilterConfigurationTypeDef",
    {
        "type": Literal["PATTERN"],
        "patternObjectFilter": NotRequired[PatternObjectFilterConfigurationUnionTypeDef],
    },
)

class PromptFlowNodeSourceConfigurationOutputTypeDef(TypedDict):
    inline: NotRequired[PromptFlowNodeInlineConfigurationOutputTypeDef]
    resource: NotRequired[PromptFlowNodeResourceConfigurationTypeDef]

CreatePromptResponseTypeDef = TypedDict(
    "CreatePromptResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "defaultVariant": str,
        "description": str,
        "id": str,
        "name": str,
        "updatedAt": datetime,
        "variants": List[PromptVariantOutputTypeDef],
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreatePromptVersionResponseTypeDef = TypedDict(
    "CreatePromptVersionResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "defaultVariant": str,
        "description": str,
        "id": str,
        "name": str,
        "updatedAt": datetime,
        "variants": List[PromptVariantOutputTypeDef],
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetPromptResponseTypeDef = TypedDict(
    "GetPromptResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "defaultVariant": str,
        "description": str,
        "id": str,
        "name": str,
        "updatedAt": datetime,
        "variants": List[PromptVariantOutputTypeDef],
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdatePromptResponseTypeDef = TypedDict(
    "UpdatePromptResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "defaultVariant": str,
        "description": str,
        "id": str,
        "name": str,
        "updatedAt": datetime,
        "variants": List[PromptVariantOutputTypeDef],
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PromptTemplateConfigurationUnionTypeDef = Union[
    PromptTemplateConfigurationTypeDef, PromptTemplateConfigurationOutputTypeDef
]
WebSourceConfigurationUnionTypeDef = Union[
    WebSourceConfigurationTypeDef, WebSourceConfigurationOutputTypeDef
]

class VectorIngestionConfigurationOutputTypeDef(TypedDict):
    chunkingConfiguration: NotRequired[ChunkingConfigurationOutputTypeDef]
    customTransformationConfiguration: NotRequired[CustomTransformationConfigurationOutputTypeDef]
    parsingConfiguration: NotRequired[ParsingConfigurationTypeDef]

CustomTransformationConfigurationUnionTypeDef = Union[
    CustomTransformationConfigurationTypeDef, CustomTransformationConfigurationOutputTypeDef
]

class CreateKnowledgeBaseResponseTypeDef(TypedDict):
    knowledgeBase: KnowledgeBaseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetKnowledgeBaseResponseTypeDef(TypedDict):
    knowledgeBase: KnowledgeBaseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateKnowledgeBaseResponseTypeDef(TypedDict):
    knowledgeBase: KnowledgeBaseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAgentRequestRequestTypeDef(TypedDict):
    agentName: str
    agentResourceRoleArn: NotRequired[str]
    clientToken: NotRequired[str]
    customerEncryptionKeyArn: NotRequired[str]
    description: NotRequired[str]
    foundationModel: NotRequired[str]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    idleSessionTTLInSeconds: NotRequired[int]
    instruction: NotRequired[str]
    memoryConfiguration: NotRequired[MemoryConfigurationTypeDef]
    promptOverrideConfiguration: NotRequired[PromptOverrideConfigurationTypeDef]
    tags: NotRequired[Mapping[str, str]]

class UpdateAgentRequestRequestTypeDef(TypedDict):
    agentId: str
    agentName: str
    agentResourceRoleArn: str
    foundationModel: str
    customerEncryptionKeyArn: NotRequired[str]
    description: NotRequired[str]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    idleSessionTTLInSeconds: NotRequired[int]
    instruction: NotRequired[str]
    memoryConfiguration: NotRequired[MemoryConfigurationTypeDef]
    promptOverrideConfiguration: NotRequired[PromptOverrideConfigurationTypeDef]

DataSourceConfigurationOutputTypeDef = TypedDict(
    "DataSourceConfigurationOutputTypeDef",
    {
        "type": DataSourceTypeType,
        "confluenceConfiguration": NotRequired[ConfluenceDataSourceConfigurationOutputTypeDef],
        "s3Configuration": NotRequired[S3DataSourceConfigurationOutputTypeDef],
        "salesforceConfiguration": NotRequired[SalesforceDataSourceConfigurationOutputTypeDef],
        "sharePointConfiguration": NotRequired[SharePointDataSourceConfigurationOutputTypeDef],
        "webConfiguration": NotRequired[WebDataSourceConfigurationOutputTypeDef],
    },
)
CrawlFilterConfigurationUnionTypeDef = Union[
    CrawlFilterConfigurationTypeDef, CrawlFilterConfigurationOutputTypeDef
]

class PromptFlowNodeConfigurationOutputTypeDef(TypedDict):
    sourceConfiguration: PromptFlowNodeSourceConfigurationOutputTypeDef

class PromptFlowNodeInlineConfigurationTypeDef(TypedDict):
    modelId: str
    templateConfiguration: PromptTemplateConfigurationUnionTypeDef
    templateType: Literal["TEXT"]
    inferenceConfiguration: NotRequired[PromptInferenceConfigurationUnionTypeDef]

class PromptVariantTypeDef(TypedDict):
    name: str
    templateType: Literal["TEXT"]
    inferenceConfiguration: NotRequired[PromptInferenceConfigurationUnionTypeDef]
    metadata: NotRequired[Sequence[PromptMetadataEntryTypeDef]]
    modelId: NotRequired[str]
    templateConfiguration: NotRequired[PromptTemplateConfigurationUnionTypeDef]

class WebDataSourceConfigurationTypeDef(TypedDict):
    sourceConfiguration: WebSourceConfigurationUnionTypeDef
    crawlerConfiguration: NotRequired[WebCrawlerConfigurationUnionTypeDef]

class VectorIngestionConfigurationTypeDef(TypedDict):
    chunkingConfiguration: NotRequired[ChunkingConfigurationUnionTypeDef]
    customTransformationConfiguration: NotRequired[CustomTransformationConfigurationUnionTypeDef]
    parsingConfiguration: NotRequired[ParsingConfigurationTypeDef]

class DataSourceTypeDef(TypedDict):
    createdAt: datetime
    dataSourceConfiguration: DataSourceConfigurationOutputTypeDef
    dataSourceId: str
    knowledgeBaseId: str
    name: str
    status: DataSourceStatusType
    updatedAt: datetime
    dataDeletionPolicy: NotRequired[DataDeletionPolicyType]
    description: NotRequired[str]
    failureReasons: NotRequired[List[str]]
    serverSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    vectorIngestionConfiguration: NotRequired[VectorIngestionConfigurationOutputTypeDef]

class ConfluenceCrawlerConfigurationTypeDef(TypedDict):
    filterConfiguration: NotRequired[CrawlFilterConfigurationUnionTypeDef]

class SalesforceCrawlerConfigurationTypeDef(TypedDict):
    filterConfiguration: NotRequired[CrawlFilterConfigurationUnionTypeDef]

class SharePointCrawlerConfigurationTypeDef(TypedDict):
    filterConfiguration: NotRequired[CrawlFilterConfigurationUnionTypeDef]

FlowNodeConfigurationOutputTypeDef = TypedDict(
    "FlowNodeConfigurationOutputTypeDef",
    {
        "agent": NotRequired[AgentFlowNodeConfigurationTypeDef],
        "collector": NotRequired[Dict[str, Any]],
        "condition": NotRequired[ConditionFlowNodeConfigurationOutputTypeDef],
        "input": NotRequired[Dict[str, Any]],
        "iterator": NotRequired[Dict[str, Any]],
        "knowledgeBase": NotRequired[KnowledgeBaseFlowNodeConfigurationTypeDef],
        "lambdaFunction": NotRequired[LambdaFunctionFlowNodeConfigurationTypeDef],
        "lex": NotRequired[LexFlowNodeConfigurationTypeDef],
        "output": NotRequired[Dict[str, Any]],
        "prompt": NotRequired[PromptFlowNodeConfigurationOutputTypeDef],
        "retrieval": NotRequired[RetrievalFlowNodeConfigurationTypeDef],
        "storage": NotRequired[StorageFlowNodeConfigurationTypeDef],
    },
)
PromptFlowNodeInlineConfigurationUnionTypeDef = Union[
    PromptFlowNodeInlineConfigurationTypeDef, PromptFlowNodeInlineConfigurationOutputTypeDef
]
PromptVariantUnionTypeDef = Union[PromptVariantTypeDef, PromptVariantOutputTypeDef]

class UpdatePromptRequestRequestTypeDef(TypedDict):
    name: str
    promptIdentifier: str
    customerEncryptionKeyArn: NotRequired[str]
    defaultVariant: NotRequired[str]
    description: NotRequired[str]
    variants: NotRequired[Sequence[PromptVariantTypeDef]]

WebDataSourceConfigurationUnionTypeDef = Union[
    WebDataSourceConfigurationTypeDef, WebDataSourceConfigurationOutputTypeDef
]

class CreateDataSourceResponseTypeDef(TypedDict):
    dataSource: DataSourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetDataSourceResponseTypeDef(TypedDict):
    dataSource: DataSourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDataSourceResponseTypeDef(TypedDict):
    dataSource: DataSourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ConfluenceCrawlerConfigurationUnionTypeDef = Union[
    ConfluenceCrawlerConfigurationTypeDef, ConfluenceCrawlerConfigurationOutputTypeDef
]
SalesforceCrawlerConfigurationUnionTypeDef = Union[
    SalesforceCrawlerConfigurationTypeDef, SalesforceCrawlerConfigurationOutputTypeDef
]
SharePointCrawlerConfigurationUnionTypeDef = Union[
    SharePointCrawlerConfigurationTypeDef, SharePointCrawlerConfigurationOutputTypeDef
]
FlowNodeExtraOutputTypeDef = TypedDict(
    "FlowNodeExtraOutputTypeDef",
    {
        "name": str,
        "type": FlowNodeTypeType,
        "configuration": NotRequired[FlowNodeConfigurationOutputTypeDef],
        "inputs": NotRequired[List[FlowNodeInputTypeDef]],
        "outputs": NotRequired[List[FlowNodeOutputTypeDef]],
    },
)

class PromptFlowNodeSourceConfigurationTypeDef(TypedDict):
    inline: NotRequired[PromptFlowNodeInlineConfigurationUnionTypeDef]
    resource: NotRequired[PromptFlowNodeResourceConfigurationTypeDef]

class CreatePromptRequestRequestTypeDef(TypedDict):
    name: str
    clientToken: NotRequired[str]
    customerEncryptionKeyArn: NotRequired[str]
    defaultVariant: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    variants: NotRequired[Sequence[PromptVariantUnionTypeDef]]

class ConfluenceDataSourceConfigurationTypeDef(TypedDict):
    sourceConfiguration: ConfluenceSourceConfigurationTypeDef
    crawlerConfiguration: NotRequired[ConfluenceCrawlerConfigurationUnionTypeDef]

class SalesforceDataSourceConfigurationTypeDef(TypedDict):
    sourceConfiguration: SalesforceSourceConfigurationTypeDef
    crawlerConfiguration: NotRequired[SalesforceCrawlerConfigurationUnionTypeDef]

class SharePointDataSourceConfigurationTypeDef(TypedDict):
    sourceConfiguration: SharePointSourceConfigurationUnionTypeDef
    crawlerConfiguration: NotRequired[SharePointCrawlerConfigurationUnionTypeDef]

class FlowDefinitionOutputTypeDef(TypedDict):
    connections: NotRequired[List[FlowConnectionTypeDef]]
    nodes: NotRequired[List[FlowNodeExtraOutputTypeDef]]

PromptFlowNodeSourceConfigurationUnionTypeDef = Union[
    PromptFlowNodeSourceConfigurationTypeDef, PromptFlowNodeSourceConfigurationOutputTypeDef
]
ConfluenceDataSourceConfigurationUnionTypeDef = Union[
    ConfluenceDataSourceConfigurationTypeDef, ConfluenceDataSourceConfigurationOutputTypeDef
]
SalesforceDataSourceConfigurationUnionTypeDef = Union[
    SalesforceDataSourceConfigurationTypeDef, SalesforceDataSourceConfigurationOutputTypeDef
]
SharePointDataSourceConfigurationUnionTypeDef = Union[
    SharePointDataSourceConfigurationTypeDef, SharePointDataSourceConfigurationOutputTypeDef
]
CreateFlowResponseTypeDef = TypedDict(
    "CreateFlowResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "definition": FlowDefinitionOutputTypeDef,
        "description": str,
        "executionRoleArn": str,
        "id": str,
        "name": str,
        "status": FlowStatusType,
        "updatedAt": datetime,
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateFlowVersionResponseTypeDef = TypedDict(
    "CreateFlowVersionResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "definition": FlowDefinitionOutputTypeDef,
        "description": str,
        "executionRoleArn": str,
        "id": str,
        "name": str,
        "status": FlowStatusType,
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetFlowResponseTypeDef = TypedDict(
    "GetFlowResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "definition": FlowDefinitionOutputTypeDef,
        "description": str,
        "executionRoleArn": str,
        "id": str,
        "name": str,
        "status": FlowStatusType,
        "updatedAt": datetime,
        "validations": List[FlowValidationTypeDef],
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetFlowVersionResponseTypeDef = TypedDict(
    "GetFlowVersionResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "definition": FlowDefinitionOutputTypeDef,
        "description": str,
        "executionRoleArn": str,
        "id": str,
        "name": str,
        "status": FlowStatusType,
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateFlowResponseTypeDef = TypedDict(
    "UpdateFlowResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "definition": FlowDefinitionOutputTypeDef,
        "description": str,
        "executionRoleArn": str,
        "id": str,
        "name": str,
        "status": FlowStatusType,
        "updatedAt": datetime,
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class PromptFlowNodeConfigurationTypeDef(TypedDict):
    sourceConfiguration: PromptFlowNodeSourceConfigurationUnionTypeDef

DataSourceConfigurationTypeDef = TypedDict(
    "DataSourceConfigurationTypeDef",
    {
        "type": DataSourceTypeType,
        "confluenceConfiguration": NotRequired[ConfluenceDataSourceConfigurationUnionTypeDef],
        "s3Configuration": NotRequired[S3DataSourceConfigurationUnionTypeDef],
        "salesforceConfiguration": NotRequired[SalesforceDataSourceConfigurationUnionTypeDef],
        "sharePointConfiguration": NotRequired[SharePointDataSourceConfigurationUnionTypeDef],
        "webConfiguration": NotRequired[WebDataSourceConfigurationUnionTypeDef],
    },
)
PromptFlowNodeConfigurationUnionTypeDef = Union[
    PromptFlowNodeConfigurationTypeDef, PromptFlowNodeConfigurationOutputTypeDef
]

class CreateDataSourceRequestRequestTypeDef(TypedDict):
    dataSourceConfiguration: DataSourceConfigurationTypeDef
    knowledgeBaseId: str
    name: str
    clientToken: NotRequired[str]
    dataDeletionPolicy: NotRequired[DataDeletionPolicyType]
    description: NotRequired[str]
    serverSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    vectorIngestionConfiguration: NotRequired[VectorIngestionConfigurationTypeDef]

class UpdateDataSourceRequestRequestTypeDef(TypedDict):
    dataSourceConfiguration: DataSourceConfigurationTypeDef
    dataSourceId: str
    knowledgeBaseId: str
    name: str
    dataDeletionPolicy: NotRequired[DataDeletionPolicyType]
    description: NotRequired[str]
    serverSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    vectorIngestionConfiguration: NotRequired[VectorIngestionConfigurationTypeDef]

FlowNodeConfigurationTypeDef = TypedDict(
    "FlowNodeConfigurationTypeDef",
    {
        "agent": NotRequired[AgentFlowNodeConfigurationTypeDef],
        "collector": NotRequired[Mapping[str, Any]],
        "condition": NotRequired[ConditionFlowNodeConfigurationUnionTypeDef],
        "input": NotRequired[Mapping[str, Any]],
        "iterator": NotRequired[Mapping[str, Any]],
        "knowledgeBase": NotRequired[KnowledgeBaseFlowNodeConfigurationTypeDef],
        "lambdaFunction": NotRequired[LambdaFunctionFlowNodeConfigurationTypeDef],
        "lex": NotRequired[LexFlowNodeConfigurationTypeDef],
        "output": NotRequired[Mapping[str, Any]],
        "prompt": NotRequired[PromptFlowNodeConfigurationUnionTypeDef],
        "retrieval": NotRequired[RetrievalFlowNodeConfigurationTypeDef],
        "storage": NotRequired[StorageFlowNodeConfigurationTypeDef],
    },
)
FlowNodeConfigurationUnionTypeDef = Union[
    FlowNodeConfigurationTypeDef, FlowNodeConfigurationOutputTypeDef
]
FlowNodeTypeDef = TypedDict(
    "FlowNodeTypeDef",
    {
        "name": str,
        "type": FlowNodeTypeType,
        "configuration": NotRequired[FlowNodeConfigurationUnionTypeDef],
        "inputs": NotRequired[Sequence[FlowNodeInputTypeDef]],
        "outputs": NotRequired[Sequence[FlowNodeOutputTypeDef]],
    },
)
FlowNodeUnionTypeDef = Union[FlowNodeTypeDef, FlowNodeExtraOutputTypeDef]

class FlowDefinitionTypeDef(TypedDict):
    connections: NotRequired[Sequence[FlowConnectionTypeDef]]
    nodes: NotRequired[Sequence[FlowNodeUnionTypeDef]]

class CreateFlowRequestRequestTypeDef(TypedDict):
    executionRoleArn: str
    name: str
    clientToken: NotRequired[str]
    customerEncryptionKeyArn: NotRequired[str]
    definition: NotRequired[FlowDefinitionTypeDef]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class UpdateFlowRequestRequestTypeDef(TypedDict):
    executionRoleArn: str
    flowIdentifier: str
    name: str
    customerEncryptionKeyArn: NotRequired[str]
    definition: NotRequired[FlowDefinitionTypeDef]
    description: NotRequired[str]
