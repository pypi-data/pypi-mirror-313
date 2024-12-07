"""
Type annotations for bedrock-agent-runtime service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/type_defs/)

Usage::

    ```python
    from types_aiobotocore_bedrock_agent_runtime.type_defs import AccessDeniedExceptionTypeDef

    data: AccessDeniedExceptionTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from aiobotocore.eventstream import AioEventStream
from aiobotocore.response import StreamingBody

from .literals import (
    ActionInvocationTypeType,
    ConfirmationStateType,
    CreationModeType,
    ExecutionTypeType,
    ExternalSourceTypeType,
    FileSourceTypeType,
    FileUseCaseType,
    GuadrailActionType,
    GuardrailActionType,
    GuardrailContentFilterConfidenceType,
    GuardrailContentFilterTypeType,
    GuardrailPiiEntityTypeType,
    GuardrailSensitiveInformationPolicyActionType,
    InvocationTypeType,
    NodeTypeType,
    PromptTypeType,
    ResponseStateType,
    RetrievalResultLocationTypeType,
    RetrieveAndGenerateTypeType,
    SearchTypeType,
    SourceType,
    TypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccessDeniedExceptionTypeDef",
    "ActionGroupInvocationInputTypeDef",
    "ActionGroupInvocationOutputTypeDef",
    "ApiInvocationInputTypeDef",
    "ApiParameterTypeDef",
    "ApiRequestBodyTypeDef",
    "ApiResultTypeDef",
    "AttributionTypeDef",
    "BadGatewayExceptionTypeDef",
    "BlobTypeDef",
    "ByteContentDocTypeDef",
    "ByteContentFileTypeDef",
    "CitationTypeDef",
    "CodeInterpreterInvocationInputTypeDef",
    "CodeInterpreterInvocationOutputTypeDef",
    "ConflictExceptionTypeDef",
    "ContentBodyTypeDef",
    "DeleteAgentMemoryRequestRequestTypeDef",
    "DependencyFailedExceptionTypeDef",
    "ExternalSourceTypeDef",
    "ExternalSourcesGenerationConfigurationTypeDef",
    "ExternalSourcesRetrieveAndGenerateConfigurationTypeDef",
    "FailureTraceTypeDef",
    "FilePartTypeDef",
    "FileSourceTypeDef",
    "FilterAttributeTypeDef",
    "FinalResponseTypeDef",
    "FlowCompletionEventTypeDef",
    "FlowInputContentTypeDef",
    "FlowInputTypeDef",
    "FlowOutputContentTypeDef",
    "FlowOutputEventTypeDef",
    "FlowResponseStreamTypeDef",
    "FunctionInvocationInputTypeDef",
    "FunctionParameterTypeDef",
    "FunctionResultTypeDef",
    "GeneratedResponsePartTypeDef",
    "GenerationConfigurationTypeDef",
    "GetAgentMemoryRequestGetAgentMemoryPaginateTypeDef",
    "GetAgentMemoryRequestRequestTypeDef",
    "GetAgentMemoryResponseTypeDef",
    "GuardrailAssessmentTypeDef",
    "GuardrailConfigurationTypeDef",
    "GuardrailContentFilterTypeDef",
    "GuardrailContentPolicyAssessmentTypeDef",
    "GuardrailCustomWordTypeDef",
    "GuardrailManagedWordTypeDef",
    "GuardrailPiiEntityFilterTypeDef",
    "GuardrailRegexFilterTypeDef",
    "GuardrailSensitiveInformationPolicyAssessmentTypeDef",
    "GuardrailTopicPolicyAssessmentTypeDef",
    "GuardrailTopicTypeDef",
    "GuardrailTraceTypeDef",
    "GuardrailWordPolicyAssessmentTypeDef",
    "InferenceConfigTypeDef",
    "InferenceConfigurationTypeDef",
    "InputFileTypeDef",
    "InternalServerExceptionTypeDef",
    "InvocationInputMemberTypeDef",
    "InvocationInputTypeDef",
    "InvocationResultMemberTypeDef",
    "InvokeAgentRequestRequestTypeDef",
    "InvokeAgentResponseTypeDef",
    "InvokeFlowRequestRequestTypeDef",
    "InvokeFlowResponseTypeDef",
    "KnowledgeBaseConfigurationTypeDef",
    "KnowledgeBaseLookupInputTypeDef",
    "KnowledgeBaseLookupOutputTypeDef",
    "KnowledgeBaseQueryTypeDef",
    "KnowledgeBaseRetrievalConfigurationPaginatorTypeDef",
    "KnowledgeBaseRetrievalConfigurationTypeDef",
    "KnowledgeBaseRetrievalResultTypeDef",
    "KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef",
    "KnowledgeBaseVectorSearchConfigurationPaginatorTypeDef",
    "KnowledgeBaseVectorSearchConfigurationTypeDef",
    "MemorySessionSummaryTypeDef",
    "MemoryTypeDef",
    "MetadataTypeDef",
    "ModelInvocationInputTypeDef",
    "ObservationTypeDef",
    "OrchestrationConfigurationTypeDef",
    "OrchestrationModelInvocationOutputTypeDef",
    "OrchestrationTraceTypeDef",
    "OutputFileTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterTypeDef",
    "PayloadPartTypeDef",
    "PostProcessingModelInvocationOutputTypeDef",
    "PostProcessingParsedResponseTypeDef",
    "PostProcessingTraceTypeDef",
    "PreProcessingModelInvocationOutputTypeDef",
    "PreProcessingParsedResponseTypeDef",
    "PreProcessingTraceTypeDef",
    "PromptTemplateTypeDef",
    "PropertyParametersTypeDef",
    "QueryTransformationConfigurationTypeDef",
    "RationaleTypeDef",
    "RawResponseTypeDef",
    "RepromptResponseTypeDef",
    "RequestBodyTypeDef",
    "ResourceNotFoundExceptionTypeDef",
    "ResponseMetadataTypeDef",
    "ResponseStreamTypeDef",
    "RetrievalFilterPaginatorTypeDef",
    "RetrievalFilterTypeDef",
    "RetrievalResultConfluenceLocationTypeDef",
    "RetrievalResultContentTypeDef",
    "RetrievalResultLocationTypeDef",
    "RetrievalResultS3LocationTypeDef",
    "RetrievalResultSalesforceLocationTypeDef",
    "RetrievalResultSharePointLocationTypeDef",
    "RetrievalResultWebLocationTypeDef",
    "RetrieveAndGenerateConfigurationTypeDef",
    "RetrieveAndGenerateInputTypeDef",
    "RetrieveAndGenerateOutputTypeDef",
    "RetrieveAndGenerateRequestRequestTypeDef",
    "RetrieveAndGenerateResponseTypeDef",
    "RetrieveAndGenerateSessionConfigurationTypeDef",
    "RetrieveRequestRequestTypeDef",
    "RetrieveRequestRetrievePaginateTypeDef",
    "RetrieveResponseTypeDef",
    "RetrievedReferenceTypeDef",
    "ReturnControlPayloadTypeDef",
    "S3ObjectDocTypeDef",
    "S3ObjectFileTypeDef",
    "ServiceQuotaExceededExceptionTypeDef",
    "SessionStateTypeDef",
    "SpanTypeDef",
    "TextInferenceConfigTypeDef",
    "TextResponsePartTypeDef",
    "ThrottlingExceptionTypeDef",
    "TracePartTypeDef",
    "TraceTypeDef",
    "UsageTypeDef",
    "ValidationExceptionTypeDef",
)


class AccessDeniedExceptionTypeDef(TypedDict):
    message: NotRequired[str]


ParameterTypeDef = TypedDict(
    "ParameterTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "value": NotRequired[str],
    },
)


class ActionGroupInvocationOutputTypeDef(TypedDict):
    text: NotRequired[str]


ApiParameterTypeDef = TypedDict(
    "ApiParameterTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "value": NotRequired[str],
    },
)


class ContentBodyTypeDef(TypedDict):
    body: NotRequired[str]


class BadGatewayExceptionTypeDef(TypedDict):
    message: NotRequired[str]
    resourceName: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class CodeInterpreterInvocationInputTypeDef(TypedDict):
    code: NotRequired[str]
    files: NotRequired[List[str]]


class CodeInterpreterInvocationOutputTypeDef(TypedDict):
    executionError: NotRequired[str]
    executionOutput: NotRequired[str]
    executionTimeout: NotRequired[bool]
    files: NotRequired[List[str]]


class ConflictExceptionTypeDef(TypedDict):
    message: NotRequired[str]


class DeleteAgentMemoryRequestRequestTypeDef(TypedDict):
    agentAliasId: str
    agentId: str
    memoryId: NotRequired[str]


class DependencyFailedExceptionTypeDef(TypedDict):
    message: NotRequired[str]
    resourceName: NotRequired[str]


class S3ObjectDocTypeDef(TypedDict):
    uri: str


class GuardrailConfigurationTypeDef(TypedDict):
    guardrailId: str
    guardrailVersion: str


class PromptTemplateTypeDef(TypedDict):
    textPromptTemplate: NotRequired[str]


class FailureTraceTypeDef(TypedDict):
    failureReason: NotRequired[str]
    traceId: NotRequired[str]


OutputFileTypeDef = TypedDict(
    "OutputFileTypeDef",
    {
        "bytes": NotRequired[bytes],
        "name": NotRequired[str],
        "type": NotRequired[str],
    },
)


class S3ObjectFileTypeDef(TypedDict):
    uri: str


class FilterAttributeTypeDef(TypedDict):
    key: str
    value: Mapping[str, Any]


class FinalResponseTypeDef(TypedDict):
    text: NotRequired[str]


class FlowCompletionEventTypeDef(TypedDict):
    completionReason: Literal["SUCCESS"]


class FlowInputContentTypeDef(TypedDict):
    document: NotRequired[Mapping[str, Any]]


class FlowOutputContentTypeDef(TypedDict):
    document: NotRequired[Dict[str, Any]]


class InternalServerExceptionTypeDef(TypedDict):
    message: NotRequired[str]


class ResourceNotFoundExceptionTypeDef(TypedDict):
    message: NotRequired[str]


class ServiceQuotaExceededExceptionTypeDef(TypedDict):
    message: NotRequired[str]


class ThrottlingExceptionTypeDef(TypedDict):
    message: NotRequired[str]


class ValidationExceptionTypeDef(TypedDict):
    message: NotRequired[str]


FunctionParameterTypeDef = TypedDict(
    "FunctionParameterTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "value": NotRequired[str],
    },
)


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetAgentMemoryRequestRequestTypeDef(TypedDict):
    agentAliasId: str
    agentId: str
    memoryId: str
    memoryType: Literal["SESSION_SUMMARY"]
    maxItems: NotRequired[int]
    nextToken: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


GuardrailContentFilterTypeDef = TypedDict(
    "GuardrailContentFilterTypeDef",
    {
        "action": NotRequired[Literal["BLOCKED"]],
        "confidence": NotRequired[GuardrailContentFilterConfidenceType],
        "type": NotRequired[GuardrailContentFilterTypeType],
    },
)


class GuardrailCustomWordTypeDef(TypedDict):
    action: NotRequired[Literal["BLOCKED"]]
    match: NotRequired[str]


GuardrailManagedWordTypeDef = TypedDict(
    "GuardrailManagedWordTypeDef",
    {
        "action": NotRequired[Literal["BLOCKED"]],
        "match": NotRequired[str],
        "type": NotRequired[Literal["PROFANITY"]],
    },
)
GuardrailPiiEntityFilterTypeDef = TypedDict(
    "GuardrailPiiEntityFilterTypeDef",
    {
        "action": NotRequired[GuardrailSensitiveInformationPolicyActionType],
        "match": NotRequired[str],
        "type": NotRequired[GuardrailPiiEntityTypeType],
    },
)


class GuardrailRegexFilterTypeDef(TypedDict):
    action: NotRequired[GuardrailSensitiveInformationPolicyActionType]
    match: NotRequired[str]
    name: NotRequired[str]
    regex: NotRequired[str]


GuardrailTopicTypeDef = TypedDict(
    "GuardrailTopicTypeDef",
    {
        "action": NotRequired[Literal["BLOCKED"]],
        "name": NotRequired[str],
        "type": NotRequired[Literal["DENY"]],
    },
)


class TextInferenceConfigTypeDef(TypedDict):
    maxTokens: NotRequired[int]
    stopSequences: NotRequired[Sequence[str]]
    temperature: NotRequired[float]
    topP: NotRequired[float]


class InferenceConfigurationTypeDef(TypedDict):
    maximumLength: NotRequired[int]
    stopSequences: NotRequired[List[str]]
    temperature: NotRequired[float]
    topK: NotRequired[int]
    topP: NotRequired[float]


class KnowledgeBaseLookupInputTypeDef(TypedDict):
    knowledgeBaseId: NotRequired[str]
    text: NotRequired[str]


class KnowledgeBaseQueryTypeDef(TypedDict):
    text: str


class RetrievalResultContentTypeDef(TypedDict):
    text: str


class MemorySessionSummaryTypeDef(TypedDict):
    memoryId: NotRequired[str]
    sessionExpiryTime: NotRequired[datetime]
    sessionId: NotRequired[str]
    sessionStartTime: NotRequired[datetime]
    summaryText: NotRequired[str]


class UsageTypeDef(TypedDict):
    inputTokens: NotRequired[int]
    outputTokens: NotRequired[int]


class RepromptResponseTypeDef(TypedDict):
    source: NotRequired[SourceType]
    text: NotRequired[str]


QueryTransformationConfigurationTypeDef = TypedDict(
    "QueryTransformationConfigurationTypeDef",
    {
        "type": Literal["QUERY_DECOMPOSITION"],
    },
)


class RawResponseTypeDef(TypedDict):
    content: NotRequired[str]


class RationaleTypeDef(TypedDict):
    text: NotRequired[str]
    traceId: NotRequired[str]


class PostProcessingParsedResponseTypeDef(TypedDict):
    text: NotRequired[str]


class PreProcessingParsedResponseTypeDef(TypedDict):
    isValid: NotRequired[bool]
    rationale: NotRequired[str]


class RetrievalResultConfluenceLocationTypeDef(TypedDict):
    url: NotRequired[str]


class RetrievalResultS3LocationTypeDef(TypedDict):
    uri: NotRequired[str]


class RetrievalResultSalesforceLocationTypeDef(TypedDict):
    url: NotRequired[str]


class RetrievalResultSharePointLocationTypeDef(TypedDict):
    url: NotRequired[str]


class RetrievalResultWebLocationTypeDef(TypedDict):
    url: NotRequired[str]


class RetrieveAndGenerateInputTypeDef(TypedDict):
    text: str


class RetrieveAndGenerateOutputTypeDef(TypedDict):
    text: str


class RetrieveAndGenerateSessionConfigurationTypeDef(TypedDict):
    kmsKeyArn: str


class SpanTypeDef(TypedDict):
    end: NotRequired[int]
    start: NotRequired[int]


class PropertyParametersTypeDef(TypedDict):
    properties: NotRequired[List[ParameterTypeDef]]


class RequestBodyTypeDef(TypedDict):
    content: NotRequired[Dict[str, List[ParameterTypeDef]]]


class ApiResultTypeDef(TypedDict):
    actionGroup: str
    apiPath: NotRequired[str]
    confirmationState: NotRequired[ConfirmationStateType]
    httpMethod: NotRequired[str]
    httpStatusCode: NotRequired[int]
    responseBody: NotRequired[Mapping[str, ContentBodyTypeDef]]
    responseState: NotRequired[ResponseStateType]


class FunctionResultTypeDef(TypedDict):
    actionGroup: str
    confirmationState: NotRequired[ConfirmationStateType]
    function: NotRequired[str]
    responseBody: NotRequired[Mapping[str, ContentBodyTypeDef]]
    responseState: NotRequired[ResponseStateType]


class ByteContentDocTypeDef(TypedDict):
    contentType: str
    data: BlobTypeDef
    identifier: str


class ByteContentFileTypeDef(TypedDict):
    data: BlobTypeDef
    mediaType: str


class FilePartTypeDef(TypedDict):
    files: NotRequired[List[OutputFileTypeDef]]


RetrievalFilterPaginatorTypeDef = TypedDict(
    "RetrievalFilterPaginatorTypeDef",
    {
        "andAll": NotRequired[Sequence[Mapping[str, Any]]],
        "equals": NotRequired[FilterAttributeTypeDef],
        "greaterThan": NotRequired[FilterAttributeTypeDef],
        "greaterThanOrEquals": NotRequired[FilterAttributeTypeDef],
        "in": NotRequired[FilterAttributeTypeDef],
        "lessThan": NotRequired[FilterAttributeTypeDef],
        "lessThanOrEquals": NotRequired[FilterAttributeTypeDef],
        "listContains": NotRequired[FilterAttributeTypeDef],
        "notEquals": NotRequired[FilterAttributeTypeDef],
        "notIn": NotRequired[FilterAttributeTypeDef],
        "orAll": NotRequired[Sequence[Mapping[str, Any]]],
        "startsWith": NotRequired[FilterAttributeTypeDef],
        "stringContains": NotRequired[FilterAttributeTypeDef],
    },
)
RetrievalFilterTypeDef = TypedDict(
    "RetrievalFilterTypeDef",
    {
        "andAll": NotRequired[Sequence[Mapping[str, Any]]],
        "equals": NotRequired[FilterAttributeTypeDef],
        "greaterThan": NotRequired[FilterAttributeTypeDef],
        "greaterThanOrEquals": NotRequired[FilterAttributeTypeDef],
        "in": NotRequired[FilterAttributeTypeDef],
        "lessThan": NotRequired[FilterAttributeTypeDef],
        "lessThanOrEquals": NotRequired[FilterAttributeTypeDef],
        "listContains": NotRequired[FilterAttributeTypeDef],
        "notEquals": NotRequired[FilterAttributeTypeDef],
        "notIn": NotRequired[FilterAttributeTypeDef],
        "orAll": NotRequired[Sequence[Mapping[str, Any]]],
        "startsWith": NotRequired[FilterAttributeTypeDef],
        "stringContains": NotRequired[FilterAttributeTypeDef],
    },
)


class FlowInputTypeDef(TypedDict):
    content: FlowInputContentTypeDef
    nodeName: str
    nodeOutputName: str


class FlowOutputEventTypeDef(TypedDict):
    content: FlowOutputContentTypeDef
    nodeName: str
    nodeType: NodeTypeType


class FunctionInvocationInputTypeDef(TypedDict):
    actionGroup: str
    actionInvocationType: NotRequired[ActionInvocationTypeType]
    function: NotRequired[str]
    parameters: NotRequired[List[FunctionParameterTypeDef]]


class GetAgentMemoryRequestGetAgentMemoryPaginateTypeDef(TypedDict):
    agentAliasId: str
    agentId: str
    memoryId: str
    memoryType: Literal["SESSION_SUMMARY"]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GuardrailContentPolicyAssessmentTypeDef(TypedDict):
    filters: NotRequired[List[GuardrailContentFilterTypeDef]]


class GuardrailWordPolicyAssessmentTypeDef(TypedDict):
    customWords: NotRequired[List[GuardrailCustomWordTypeDef]]
    managedWordLists: NotRequired[List[GuardrailManagedWordTypeDef]]


class GuardrailSensitiveInformationPolicyAssessmentTypeDef(TypedDict):
    piiEntities: NotRequired[List[GuardrailPiiEntityFilterTypeDef]]
    regexes: NotRequired[List[GuardrailRegexFilterTypeDef]]


class GuardrailTopicPolicyAssessmentTypeDef(TypedDict):
    topics: NotRequired[List[GuardrailTopicTypeDef]]


class InferenceConfigTypeDef(TypedDict):
    textInferenceConfig: NotRequired[TextInferenceConfigTypeDef]


ModelInvocationInputTypeDef = TypedDict(
    "ModelInvocationInputTypeDef",
    {
        "inferenceConfiguration": NotRequired[InferenceConfigurationTypeDef],
        "overrideLambda": NotRequired[str],
        "parserMode": NotRequired[CreationModeType],
        "promptCreationMode": NotRequired[CreationModeType],
        "text": NotRequired[str],
        "traceId": NotRequired[str],
        "type": NotRequired[PromptTypeType],
    },
)


class MemoryTypeDef(TypedDict):
    sessionSummary: NotRequired[MemorySessionSummaryTypeDef]


class MetadataTypeDef(TypedDict):
    usage: NotRequired[UsageTypeDef]


class OrchestrationConfigurationTypeDef(TypedDict):
    queryTransformationConfiguration: QueryTransformationConfigurationTypeDef


RetrievalResultLocationTypeDef = TypedDict(
    "RetrievalResultLocationTypeDef",
    {
        "type": RetrievalResultLocationTypeType,
        "confluenceLocation": NotRequired[RetrievalResultConfluenceLocationTypeDef],
        "s3Location": NotRequired[RetrievalResultS3LocationTypeDef],
        "salesforceLocation": NotRequired[RetrievalResultSalesforceLocationTypeDef],
        "sharePointLocation": NotRequired[RetrievalResultSharePointLocationTypeDef],
        "webLocation": NotRequired[RetrievalResultWebLocationTypeDef],
    },
)


class TextResponsePartTypeDef(TypedDict):
    span: NotRequired[SpanTypeDef]
    text: NotRequired[str]


class ApiRequestBodyTypeDef(TypedDict):
    content: NotRequired[Dict[str, PropertyParametersTypeDef]]


class ActionGroupInvocationInputTypeDef(TypedDict):
    actionGroupName: NotRequired[str]
    apiPath: NotRequired[str]
    executionType: NotRequired[ExecutionTypeType]
    function: NotRequired[str]
    invocationId: NotRequired[str]
    parameters: NotRequired[List[ParameterTypeDef]]
    requestBody: NotRequired[RequestBodyTypeDef]
    verb: NotRequired[str]


class InvocationResultMemberTypeDef(TypedDict):
    apiResult: NotRequired[ApiResultTypeDef]
    functionResult: NotRequired[FunctionResultTypeDef]


class ExternalSourceTypeDef(TypedDict):
    sourceType: ExternalSourceTypeType
    byteContent: NotRequired[ByteContentDocTypeDef]
    s3Location: NotRequired[S3ObjectDocTypeDef]


class FileSourceTypeDef(TypedDict):
    sourceType: FileSourceTypeType
    byteContent: NotRequired[ByteContentFileTypeDef]
    s3Location: NotRequired[S3ObjectFileTypeDef]


KnowledgeBaseVectorSearchConfigurationPaginatorTypeDef = TypedDict(
    "KnowledgeBaseVectorSearchConfigurationPaginatorTypeDef",
    {
        "filter": NotRequired[RetrievalFilterPaginatorTypeDef],
        "numberOfResults": NotRequired[int],
        "overrideSearchType": NotRequired[SearchTypeType],
    },
)
KnowledgeBaseVectorSearchConfigurationTypeDef = TypedDict(
    "KnowledgeBaseVectorSearchConfigurationTypeDef",
    {
        "filter": NotRequired[RetrievalFilterTypeDef],
        "numberOfResults": NotRequired[int],
        "overrideSearchType": NotRequired[SearchTypeType],
    },
)


class InvokeFlowRequestRequestTypeDef(TypedDict):
    flowAliasIdentifier: str
    flowIdentifier: str
    inputs: Sequence[FlowInputTypeDef]


class FlowResponseStreamTypeDef(TypedDict):
    accessDeniedException: NotRequired[AccessDeniedExceptionTypeDef]
    badGatewayException: NotRequired[BadGatewayExceptionTypeDef]
    conflictException: NotRequired[ConflictExceptionTypeDef]
    dependencyFailedException: NotRequired[DependencyFailedExceptionTypeDef]
    flowCompletionEvent: NotRequired[FlowCompletionEventTypeDef]
    flowOutputEvent: NotRequired[FlowOutputEventTypeDef]
    internalServerException: NotRequired[InternalServerExceptionTypeDef]
    resourceNotFoundException: NotRequired[ResourceNotFoundExceptionTypeDef]
    serviceQuotaExceededException: NotRequired[ServiceQuotaExceededExceptionTypeDef]
    throttlingException: NotRequired[ThrottlingExceptionTypeDef]
    validationException: NotRequired[ValidationExceptionTypeDef]


class GuardrailAssessmentTypeDef(TypedDict):
    contentPolicy: NotRequired[GuardrailContentPolicyAssessmentTypeDef]
    sensitiveInformationPolicy: NotRequired[GuardrailSensitiveInformationPolicyAssessmentTypeDef]
    topicPolicy: NotRequired[GuardrailTopicPolicyAssessmentTypeDef]
    wordPolicy: NotRequired[GuardrailWordPolicyAssessmentTypeDef]


class ExternalSourcesGenerationConfigurationTypeDef(TypedDict):
    additionalModelRequestFields: NotRequired[Mapping[str, Mapping[str, Any]]]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    inferenceConfig: NotRequired[InferenceConfigTypeDef]
    promptTemplate: NotRequired[PromptTemplateTypeDef]


class GenerationConfigurationTypeDef(TypedDict):
    additionalModelRequestFields: NotRequired[Mapping[str, Mapping[str, Any]]]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    inferenceConfig: NotRequired[InferenceConfigTypeDef]
    promptTemplate: NotRequired[PromptTemplateTypeDef]


class GetAgentMemoryResponseTypeDef(TypedDict):
    memoryContents: List[MemoryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class OrchestrationModelInvocationOutputTypeDef(TypedDict):
    metadata: NotRequired[MetadataTypeDef]
    rawResponse: NotRequired[RawResponseTypeDef]
    traceId: NotRequired[str]


class PostProcessingModelInvocationOutputTypeDef(TypedDict):
    metadata: NotRequired[MetadataTypeDef]
    parsedResponse: NotRequired[PostProcessingParsedResponseTypeDef]
    rawResponse: NotRequired[RawResponseTypeDef]
    traceId: NotRequired[str]


class PreProcessingModelInvocationOutputTypeDef(TypedDict):
    metadata: NotRequired[MetadataTypeDef]
    parsedResponse: NotRequired[PreProcessingParsedResponseTypeDef]
    rawResponse: NotRequired[RawResponseTypeDef]
    traceId: NotRequired[str]


class KnowledgeBaseRetrievalResultTypeDef(TypedDict):
    content: RetrievalResultContentTypeDef
    location: NotRequired[RetrievalResultLocationTypeDef]
    metadata: NotRequired[Dict[str, Dict[str, Any]]]
    score: NotRequired[float]


class RetrievedReferenceTypeDef(TypedDict):
    content: NotRequired[RetrievalResultContentTypeDef]
    location: NotRequired[RetrievalResultLocationTypeDef]
    metadata: NotRequired[Dict[str, Dict[str, Any]]]


class GeneratedResponsePartTypeDef(TypedDict):
    textResponsePart: NotRequired[TextResponsePartTypeDef]


class ApiInvocationInputTypeDef(TypedDict):
    actionGroup: str
    actionInvocationType: NotRequired[ActionInvocationTypeType]
    apiPath: NotRequired[str]
    httpMethod: NotRequired[str]
    parameters: NotRequired[List[ApiParameterTypeDef]]
    requestBody: NotRequired[ApiRequestBodyTypeDef]


class InvocationInputTypeDef(TypedDict):
    actionGroupInvocationInput: NotRequired[ActionGroupInvocationInputTypeDef]
    codeInterpreterInvocationInput: NotRequired[CodeInterpreterInvocationInputTypeDef]
    invocationType: NotRequired[InvocationTypeType]
    knowledgeBaseLookupInput: NotRequired[KnowledgeBaseLookupInputTypeDef]
    traceId: NotRequired[str]


class InputFileTypeDef(TypedDict):
    name: str
    source: FileSourceTypeDef
    useCase: FileUseCaseType


class KnowledgeBaseRetrievalConfigurationPaginatorTypeDef(TypedDict):
    vectorSearchConfiguration: KnowledgeBaseVectorSearchConfigurationPaginatorTypeDef


class KnowledgeBaseRetrievalConfigurationTypeDef(TypedDict):
    vectorSearchConfiguration: KnowledgeBaseVectorSearchConfigurationTypeDef


class InvokeFlowResponseTypeDef(TypedDict):
    responseStream: "AioEventStream[FlowResponseStreamTypeDef]"
    ResponseMetadata: ResponseMetadataTypeDef


class GuardrailTraceTypeDef(TypedDict):
    action: NotRequired[GuardrailActionType]
    inputAssessments: NotRequired[List[GuardrailAssessmentTypeDef]]
    outputAssessments: NotRequired[List[GuardrailAssessmentTypeDef]]
    traceId: NotRequired[str]


class ExternalSourcesRetrieveAndGenerateConfigurationTypeDef(TypedDict):
    modelArn: str
    sources: Sequence[ExternalSourceTypeDef]
    generationConfiguration: NotRequired[ExternalSourcesGenerationConfigurationTypeDef]


class PostProcessingTraceTypeDef(TypedDict):
    modelInvocationInput: NotRequired[ModelInvocationInputTypeDef]
    modelInvocationOutput: NotRequired[PostProcessingModelInvocationOutputTypeDef]


class PreProcessingTraceTypeDef(TypedDict):
    modelInvocationInput: NotRequired[ModelInvocationInputTypeDef]
    modelInvocationOutput: NotRequired[PreProcessingModelInvocationOutputTypeDef]


class RetrieveResponseTypeDef(TypedDict):
    retrievalResults: List[KnowledgeBaseRetrievalResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class KnowledgeBaseLookupOutputTypeDef(TypedDict):
    retrievedReferences: NotRequired[List[RetrievedReferenceTypeDef]]


class CitationTypeDef(TypedDict):
    generatedResponsePart: NotRequired[GeneratedResponsePartTypeDef]
    retrievedReferences: NotRequired[List[RetrievedReferenceTypeDef]]


class InvocationInputMemberTypeDef(TypedDict):
    apiInvocationInput: NotRequired[ApiInvocationInputTypeDef]
    functionInvocationInput: NotRequired[FunctionInvocationInputTypeDef]


class RetrieveRequestRetrievePaginateTypeDef(TypedDict):
    knowledgeBaseId: str
    retrievalQuery: KnowledgeBaseQueryTypeDef
    retrievalConfiguration: NotRequired[KnowledgeBaseRetrievalConfigurationPaginatorTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class KnowledgeBaseConfigurationTypeDef(TypedDict):
    knowledgeBaseId: str
    retrievalConfiguration: KnowledgeBaseRetrievalConfigurationTypeDef


class KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef(TypedDict):
    knowledgeBaseId: str
    modelArn: str
    generationConfiguration: NotRequired[GenerationConfigurationTypeDef]
    orchestrationConfiguration: NotRequired[OrchestrationConfigurationTypeDef]
    retrievalConfiguration: NotRequired[KnowledgeBaseRetrievalConfigurationTypeDef]


class RetrieveRequestRequestTypeDef(TypedDict):
    knowledgeBaseId: str
    retrievalQuery: KnowledgeBaseQueryTypeDef
    nextToken: NotRequired[str]
    retrievalConfiguration: NotRequired[KnowledgeBaseRetrievalConfigurationTypeDef]


ObservationTypeDef = TypedDict(
    "ObservationTypeDef",
    {
        "actionGroupInvocationOutput": NotRequired[ActionGroupInvocationOutputTypeDef],
        "codeInterpreterInvocationOutput": NotRequired[CodeInterpreterInvocationOutputTypeDef],
        "finalResponse": NotRequired[FinalResponseTypeDef],
        "knowledgeBaseLookupOutput": NotRequired[KnowledgeBaseLookupOutputTypeDef],
        "repromptResponse": NotRequired[RepromptResponseTypeDef],
        "traceId": NotRequired[str],
        "type": NotRequired[TypeType],
    },
)


class AttributionTypeDef(TypedDict):
    citations: NotRequired[List[CitationTypeDef]]


class RetrieveAndGenerateResponseTypeDef(TypedDict):
    citations: List[CitationTypeDef]
    guardrailAction: GuadrailActionType
    output: RetrieveAndGenerateOutputTypeDef
    sessionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ReturnControlPayloadTypeDef(TypedDict):
    invocationId: NotRequired[str]
    invocationInputs: NotRequired[List[InvocationInputMemberTypeDef]]


class SessionStateTypeDef(TypedDict):
    files: NotRequired[Sequence[InputFileTypeDef]]
    invocationId: NotRequired[str]
    knowledgeBaseConfigurations: NotRequired[Sequence[KnowledgeBaseConfigurationTypeDef]]
    promptSessionAttributes: NotRequired[Mapping[str, str]]
    returnControlInvocationResults: NotRequired[Sequence[InvocationResultMemberTypeDef]]
    sessionAttributes: NotRequired[Mapping[str, str]]


RetrieveAndGenerateConfigurationTypeDef = TypedDict(
    "RetrieveAndGenerateConfigurationTypeDef",
    {
        "type": RetrieveAndGenerateTypeType,
        "externalSourcesConfiguration": NotRequired[
            ExternalSourcesRetrieveAndGenerateConfigurationTypeDef
        ],
        "knowledgeBaseConfiguration": NotRequired[
            KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef
        ],
    },
)


class OrchestrationTraceTypeDef(TypedDict):
    invocationInput: NotRequired[InvocationInputTypeDef]
    modelInvocationInput: NotRequired[ModelInvocationInputTypeDef]
    modelInvocationOutput: NotRequired[OrchestrationModelInvocationOutputTypeDef]
    observation: NotRequired[ObservationTypeDef]
    rationale: NotRequired[RationaleTypeDef]


PayloadPartTypeDef = TypedDict(
    "PayloadPartTypeDef",
    {
        "attribution": NotRequired[AttributionTypeDef],
        "bytes": NotRequired[bytes],
    },
)


class InvokeAgentRequestRequestTypeDef(TypedDict):
    agentAliasId: str
    agentId: str
    sessionId: str
    enableTrace: NotRequired[bool]
    endSession: NotRequired[bool]
    inputText: NotRequired[str]
    memoryId: NotRequired[str]
    sessionState: NotRequired[SessionStateTypeDef]


RetrieveAndGenerateRequestRequestTypeDef = TypedDict(
    "RetrieveAndGenerateRequestRequestTypeDef",
    {
        "input": RetrieveAndGenerateInputTypeDef,
        "retrieveAndGenerateConfiguration": NotRequired[RetrieveAndGenerateConfigurationTypeDef],
        "sessionConfiguration": NotRequired[RetrieveAndGenerateSessionConfigurationTypeDef],
        "sessionId": NotRequired[str],
    },
)


class TraceTypeDef(TypedDict):
    failureTrace: NotRequired[FailureTraceTypeDef]
    guardrailTrace: NotRequired[GuardrailTraceTypeDef]
    orchestrationTrace: NotRequired[OrchestrationTraceTypeDef]
    postProcessingTrace: NotRequired[PostProcessingTraceTypeDef]
    preProcessingTrace: NotRequired[PreProcessingTraceTypeDef]


class TracePartTypeDef(TypedDict):
    agentAliasId: NotRequired[str]
    agentId: NotRequired[str]
    agentVersion: NotRequired[str]
    sessionId: NotRequired[str]
    trace: NotRequired[TraceTypeDef]


class ResponseStreamTypeDef(TypedDict):
    accessDeniedException: NotRequired[AccessDeniedExceptionTypeDef]
    badGatewayException: NotRequired[BadGatewayExceptionTypeDef]
    chunk: NotRequired[PayloadPartTypeDef]
    conflictException: NotRequired[ConflictExceptionTypeDef]
    dependencyFailedException: NotRequired[DependencyFailedExceptionTypeDef]
    files: NotRequired[FilePartTypeDef]
    internalServerException: NotRequired[InternalServerExceptionTypeDef]
    resourceNotFoundException: NotRequired[ResourceNotFoundExceptionTypeDef]
    returnControl: NotRequired[ReturnControlPayloadTypeDef]
    serviceQuotaExceededException: NotRequired[ServiceQuotaExceededExceptionTypeDef]
    throttlingException: NotRequired[ThrottlingExceptionTypeDef]
    trace: NotRequired[TracePartTypeDef]
    validationException: NotRequired[ValidationExceptionTypeDef]


class InvokeAgentResponseTypeDef(TypedDict):
    completion: "AioEventStream[ResponseStreamTypeDef]"
    contentType: str
    memoryId: str
    sessionId: str
    ResponseMetadata: ResponseMetadataTypeDef
