"""
Type annotations for qbusiness service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/type_defs/)

Usage::

    ```python
    from types_aiobotocore_qbusiness.type_defs import S3TypeDef

    data: S3TypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from aiobotocore.eventstream import AioEventStream
from aiobotocore.response import StreamingBody

from .literals import (
    ActionPayloadFieldTypeType,
    ApplicationStatusType,
    AttachmentsControlModeType,
    AttachmentStatusType,
    AttributeTypeType,
    AutoSubscriptionStatusType,
    ChatModeType,
    ContentTypeType,
    CreatorModeControlType,
    DataSourceStatusType,
    DataSourceSyncJobStatusType,
    DocumentAttributeBoostingLevelType,
    DocumentEnrichmentConditionOperatorType,
    DocumentStatusType,
    ErrorCodeType,
    GroupStatusType,
    IdentityTypeType,
    IndexStatusType,
    IndexTypeType,
    MemberRelationType,
    MembershipTypeType,
    MessageTypeType,
    MessageUsefulnessReasonType,
    MessageUsefulnessType,
    NumberAttributeBoostingTypeType,
    PersonalizationControlModeType,
    PluginBuildStatusType,
    PluginStateType,
    PluginTypeType,
    QAppsControlModeType,
    ReadAccessTypeType,
    ResponseScopeType,
    RetrieverStatusType,
    RetrieverTypeType,
    RuleTypeType,
    StatusType,
    StringAttributeValueBoostingLevelType,
    SubscriptionTypeType,
    WebExperienceSamplePromptsControlModeType,
    WebExperienceStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "APISchemaTypeDef",
    "AccessConfigurationTypeDef",
    "AccessControlTypeDef",
    "ActionExecutionEventTypeDef",
    "ActionExecutionOutputTypeDef",
    "ActionExecutionPayloadFieldOutputTypeDef",
    "ActionExecutionPayloadFieldTypeDef",
    "ActionExecutionPayloadFieldUnionTypeDef",
    "ActionExecutionTypeDef",
    "ActionReviewEventTypeDef",
    "ActionReviewPayloadFieldAllowedValueTypeDef",
    "ActionReviewPayloadFieldTypeDef",
    "ActionReviewTypeDef",
    "ApplicationTypeDef",
    "AppliedAttachmentsConfigurationTypeDef",
    "AppliedCreatorModeConfigurationTypeDef",
    "AttachmentInputEventTypeDef",
    "AttachmentInputTypeDef",
    "AttachmentOutputTypeDef",
    "AttachmentsConfigurationTypeDef",
    "AttributeFilterTypeDef",
    "AuthChallengeRequestEventTypeDef",
    "AuthChallengeRequestTypeDef",
    "AuthChallengeResponseEventTypeDef",
    "AuthChallengeResponseTypeDef",
    "AutoSubscriptionConfigurationTypeDef",
    "BasicAuthConfigurationTypeDef",
    "BatchDeleteDocumentRequestRequestTypeDef",
    "BatchDeleteDocumentResponseTypeDef",
    "BatchPutDocumentRequestRequestTypeDef",
    "BatchPutDocumentResponseTypeDef",
    "BlobTypeDef",
    "BlockedPhrasesConfigurationTypeDef",
    "BlockedPhrasesConfigurationUpdateTypeDef",
    "ChatInputRequestTypeDef",
    "ChatInputStreamTypeDef",
    "ChatModeConfigurationTypeDef",
    "ChatOutputStreamTypeDef",
    "ChatOutputTypeDef",
    "ChatSyncInputRequestTypeDef",
    "ChatSyncOutputTypeDef",
    "ConfigurationEventTypeDef",
    "ContentBlockerRuleTypeDef",
    "ContentRetrievalRuleOutputTypeDef",
    "ContentRetrievalRuleTypeDef",
    "ContentRetrievalRuleUnionTypeDef",
    "ConversationTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateDataSourceRequestRequestTypeDef",
    "CreateDataSourceResponseTypeDef",
    "CreateIndexRequestRequestTypeDef",
    "CreateIndexResponseTypeDef",
    "CreatePluginRequestRequestTypeDef",
    "CreatePluginResponseTypeDef",
    "CreateRetrieverRequestRequestTypeDef",
    "CreateRetrieverResponseTypeDef",
    "CreateUserRequestRequestTypeDef",
    "CreateWebExperienceRequestRequestTypeDef",
    "CreateWebExperienceResponseTypeDef",
    "CreatorModeConfigurationTypeDef",
    "CustomPluginConfigurationTypeDef",
    "DataSourceSyncJobMetricsTypeDef",
    "DataSourceSyncJobTypeDef",
    "DataSourceTypeDef",
    "DataSourceVpcConfigurationOutputTypeDef",
    "DataSourceVpcConfigurationTypeDef",
    "DateAttributeBoostingConfigurationTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteChatControlsConfigurationRequestRequestTypeDef",
    "DeleteConversationRequestRequestTypeDef",
    "DeleteDataSourceRequestRequestTypeDef",
    "DeleteDocumentTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DeleteIndexRequestRequestTypeDef",
    "DeletePluginRequestRequestTypeDef",
    "DeleteRetrieverRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DeleteWebExperienceRequestRequestTypeDef",
    "DocumentAttributeBoostingConfigurationOutputTypeDef",
    "DocumentAttributeBoostingConfigurationTypeDef",
    "DocumentAttributeBoostingConfigurationUnionTypeDef",
    "DocumentAttributeConditionOutputTypeDef",
    "DocumentAttributeConditionTypeDef",
    "DocumentAttributeConditionUnionTypeDef",
    "DocumentAttributeConfigurationTypeDef",
    "DocumentAttributeTargetOutputTypeDef",
    "DocumentAttributeTargetTypeDef",
    "DocumentAttributeTargetUnionTypeDef",
    "DocumentAttributeTypeDef",
    "DocumentAttributeValueOutputTypeDef",
    "DocumentAttributeValueTypeDef",
    "DocumentAttributeValueUnionTypeDef",
    "DocumentContentTypeDef",
    "DocumentDetailsTypeDef",
    "DocumentEnrichmentConfigurationOutputTypeDef",
    "DocumentEnrichmentConfigurationTypeDef",
    "DocumentEnrichmentConfigurationUnionTypeDef",
    "DocumentTypeDef",
    "EligibleDataSourceTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionConfigurationTypeDef",
    "ErrorDetailTypeDef",
    "FailedAttachmentEventTypeDef",
    "FailedDocumentTypeDef",
    "GetApplicationRequestRequestTypeDef",
    "GetApplicationResponseTypeDef",
    "GetChatControlsConfigurationRequestGetChatControlsConfigurationPaginateTypeDef",
    "GetChatControlsConfigurationRequestRequestTypeDef",
    "GetChatControlsConfigurationResponseTypeDef",
    "GetDataSourceRequestRequestTypeDef",
    "GetDataSourceResponseTypeDef",
    "GetGroupRequestRequestTypeDef",
    "GetGroupResponseTypeDef",
    "GetIndexRequestRequestTypeDef",
    "GetIndexResponseTypeDef",
    "GetPluginRequestRequestTypeDef",
    "GetPluginResponseTypeDef",
    "GetRetrieverRequestRequestTypeDef",
    "GetRetrieverResponseTypeDef",
    "GetUserRequestRequestTypeDef",
    "GetUserResponseTypeDef",
    "GetWebExperienceRequestRequestTypeDef",
    "GetWebExperienceResponseTypeDef",
    "GroupMembersTypeDef",
    "GroupStatusDetailTypeDef",
    "GroupSummaryTypeDef",
    "HookConfigurationOutputTypeDef",
    "HookConfigurationTypeDef",
    "HookConfigurationUnionTypeDef",
    "IdentityProviderConfigurationTypeDef",
    "IndexCapacityConfigurationTypeDef",
    "IndexStatisticsTypeDef",
    "IndexTypeDef",
    "InlineDocumentEnrichmentConfigurationOutputTypeDef",
    "InlineDocumentEnrichmentConfigurationTypeDef",
    "InlineDocumentEnrichmentConfigurationUnionTypeDef",
    "KendraIndexConfigurationTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListConversationsRequestListConversationsPaginateTypeDef",
    "ListConversationsRequestRequestTypeDef",
    "ListConversationsResponseTypeDef",
    "ListDataSourceSyncJobsRequestListDataSourceSyncJobsPaginateTypeDef",
    "ListDataSourceSyncJobsRequestRequestTypeDef",
    "ListDataSourceSyncJobsResponseTypeDef",
    "ListDataSourcesRequestListDataSourcesPaginateTypeDef",
    "ListDataSourcesRequestRequestTypeDef",
    "ListDataSourcesResponseTypeDef",
    "ListDocumentsRequestListDocumentsPaginateTypeDef",
    "ListDocumentsRequestRequestTypeDef",
    "ListDocumentsResponseTypeDef",
    "ListGroupsRequestListGroupsPaginateTypeDef",
    "ListGroupsRequestRequestTypeDef",
    "ListGroupsResponseTypeDef",
    "ListIndicesRequestListIndicesPaginateTypeDef",
    "ListIndicesRequestRequestTypeDef",
    "ListIndicesResponseTypeDef",
    "ListMessagesRequestListMessagesPaginateTypeDef",
    "ListMessagesRequestRequestTypeDef",
    "ListMessagesResponseTypeDef",
    "ListPluginsRequestListPluginsPaginateTypeDef",
    "ListPluginsRequestRequestTypeDef",
    "ListPluginsResponseTypeDef",
    "ListRetrieversRequestListRetrieversPaginateTypeDef",
    "ListRetrieversRequestRequestTypeDef",
    "ListRetrieversResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListWebExperiencesRequestListWebExperiencesPaginateTypeDef",
    "ListWebExperiencesRequestRequestTypeDef",
    "ListWebExperiencesResponseTypeDef",
    "MemberGroupTypeDef",
    "MemberUserTypeDef",
    "MessageTypeDef",
    "MessageUsefulnessFeedbackTypeDef",
    "MetadataEventTypeDef",
    "NativeIndexConfigurationOutputTypeDef",
    "NativeIndexConfigurationTypeDef",
    "NativeIndexConfigurationUnionTypeDef",
    "NumberAttributeBoostingConfigurationTypeDef",
    "OAuth2ClientCredentialConfigurationTypeDef",
    "OpenIDConnectProviderConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PersonalizationConfigurationTypeDef",
    "PluginAuthConfigurationOutputTypeDef",
    "PluginAuthConfigurationTypeDef",
    "PluginConfigurationTypeDef",
    "PluginTypeDef",
    "PrincipalGroupTypeDef",
    "PrincipalTypeDef",
    "PrincipalUserTypeDef",
    "PutFeedbackRequestRequestTypeDef",
    "PutGroupRequestRequestTypeDef",
    "QAppsConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "RetrieverConfigurationOutputTypeDef",
    "RetrieverConfigurationTypeDef",
    "RetrieverTypeDef",
    "RuleConfigurationOutputTypeDef",
    "RuleConfigurationTypeDef",
    "RuleConfigurationUnionTypeDef",
    "RuleOutputTypeDef",
    "RuleTypeDef",
    "RuleUnionTypeDef",
    "S3TypeDef",
    "SamlConfigurationTypeDef",
    "SamlProviderConfigurationTypeDef",
    "SnippetExcerptTypeDef",
    "SourceAttributionTypeDef",
    "StartDataSourceSyncJobRequestRequestTypeDef",
    "StartDataSourceSyncJobResponseTypeDef",
    "StopDataSourceSyncJobRequestRequestTypeDef",
    "StringAttributeBoostingConfigurationOutputTypeDef",
    "StringAttributeBoostingConfigurationTypeDef",
    "StringAttributeBoostingConfigurationUnionTypeDef",
    "StringListAttributeBoostingConfigurationTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TextDocumentStatisticsTypeDef",
    "TextInputEventTypeDef",
    "TextOutputEventTypeDef",
    "TextSegmentTypeDef",
    "TimestampTypeDef",
    "TopicConfigurationOutputTypeDef",
    "TopicConfigurationTypeDef",
    "TopicConfigurationUnionTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateChatControlsConfigurationRequestRequestTypeDef",
    "UpdateDataSourceRequestRequestTypeDef",
    "UpdateIndexRequestRequestTypeDef",
    "UpdatePluginRequestRequestTypeDef",
    "UpdateRetrieverRequestRequestTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "UpdateUserResponseTypeDef",
    "UpdateWebExperienceRequestRequestTypeDef",
    "UserAliasTypeDef",
    "UsersAndGroupsOutputTypeDef",
    "UsersAndGroupsTypeDef",
    "UsersAndGroupsUnionTypeDef",
    "WebExperienceAuthConfigurationTypeDef",
    "WebExperienceTypeDef",
)


class S3TypeDef(TypedDict):
    bucket: str
    key: str


class ActionExecutionPayloadFieldOutputTypeDef(TypedDict):
    value: Dict[str, Any]


class ActionExecutionPayloadFieldTypeDef(TypedDict):
    value: Mapping[str, Any]


class ActionReviewPayloadFieldAllowedValueTypeDef(TypedDict):
    value: NotRequired[Dict[str, Any]]
    displayValue: NotRequired[Dict[str, Any]]


class ApplicationTypeDef(TypedDict):
    displayName: NotRequired[str]
    applicationId: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    status: NotRequired[ApplicationStatusType]
    identityType: NotRequired[IdentityTypeType]


class AppliedAttachmentsConfigurationTypeDef(TypedDict):
    attachmentsControlMode: NotRequired[AttachmentsControlModeType]


class AppliedCreatorModeConfigurationTypeDef(TypedDict):
    creatorModeControl: CreatorModeControlType


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class ErrorDetailTypeDef(TypedDict):
    errorMessage: NotRequired[str]
    errorCode: NotRequired[ErrorCodeType]


class AttachmentsConfigurationTypeDef(TypedDict):
    attachmentsControlMode: AttachmentsControlModeType


class AuthChallengeRequestEventTypeDef(TypedDict):
    authorizationUrl: str


class AuthChallengeRequestTypeDef(TypedDict):
    authorizationUrl: str


class AuthChallengeResponseEventTypeDef(TypedDict):
    responseMap: Mapping[str, str]


class AuthChallengeResponseTypeDef(TypedDict):
    responseMap: Mapping[str, str]


class AutoSubscriptionConfigurationTypeDef(TypedDict):
    autoSubscribe: AutoSubscriptionStatusType
    defaultSubscriptionType: NotRequired[SubscriptionTypeType]


class BasicAuthConfigurationTypeDef(TypedDict):
    secretArn: str
    roleArn: str


class DeleteDocumentTypeDef(TypedDict):
    documentId: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class BlockedPhrasesConfigurationTypeDef(TypedDict):
    blockedPhrases: NotRequired[List[str]]
    systemMessageOverride: NotRequired[str]


class BlockedPhrasesConfigurationUpdateTypeDef(TypedDict):
    blockedPhrasesToCreateOrUpdate: NotRequired[Sequence[str]]
    blockedPhrasesToDelete: NotRequired[Sequence[str]]
    systemMessageOverride: NotRequired[str]


class TextInputEventTypeDef(TypedDict):
    userMessage: str


class PluginConfigurationTypeDef(TypedDict):
    pluginId: str


class TextOutputEventTypeDef(TypedDict):
    conversationId: NotRequired[str]
    userMessageId: NotRequired[str]
    systemMessageId: NotRequired[str]
    systemMessage: NotRequired[str]


class ContentBlockerRuleTypeDef(TypedDict):
    systemMessageOverride: NotRequired[str]


class EligibleDataSourceTypeDef(TypedDict):
    indexId: NotRequired[str]
    dataSourceId: NotRequired[str]


class ConversationTypeDef(TypedDict):
    conversationId: NotRequired[str]
    title: NotRequired[str]
    startTime: NotRequired[datetime]


class EncryptionConfigurationTypeDef(TypedDict):
    kmsKeyId: NotRequired[str]


class PersonalizationConfigurationTypeDef(TypedDict):
    personalizationControlMode: PersonalizationControlModeType


class QAppsConfigurationTypeDef(TypedDict):
    qAppsControlMode: QAppsControlModeType


class TagTypeDef(TypedDict):
    key: str
    value: str


class DataSourceVpcConfigurationTypeDef(TypedDict):
    subnetIds: Sequence[str]
    securityGroupIds: Sequence[str]


class IndexCapacityConfigurationTypeDef(TypedDict):
    units: NotRequired[int]


class UserAliasTypeDef(TypedDict):
    userId: str
    indexId: NotRequired[str]
    dataSourceId: NotRequired[str]


class CreatorModeConfigurationTypeDef(TypedDict):
    creatorModeControl: CreatorModeControlType


class DataSourceSyncJobMetricsTypeDef(TypedDict):
    documentsAdded: NotRequired[str]
    documentsModified: NotRequired[str]
    documentsDeleted: NotRequired[str]
    documentsFailed: NotRequired[str]
    documentsScanned: NotRequired[str]


DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "displayName": NotRequired[str],
        "dataSourceId": NotRequired[str],
        "type": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "status": NotRequired[DataSourceStatusType],
    },
)


class DataSourceVpcConfigurationOutputTypeDef(TypedDict):
    subnetIds: List[str]
    securityGroupIds: List[str]


class DateAttributeBoostingConfigurationTypeDef(TypedDict):
    boostingLevel: DocumentAttributeBoostingLevelType
    boostingDurationInSeconds: NotRequired[int]


class DeleteApplicationRequestRequestTypeDef(TypedDict):
    applicationId: str


class DeleteChatControlsConfigurationRequestRequestTypeDef(TypedDict):
    applicationId: str


class DeleteConversationRequestRequestTypeDef(TypedDict):
    conversationId: str
    applicationId: str
    userId: NotRequired[str]


class DeleteDataSourceRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    dataSourceId: str


class DeleteGroupRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    groupName: str
    dataSourceId: NotRequired[str]


class DeleteIndexRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str


class DeletePluginRequestRequestTypeDef(TypedDict):
    applicationId: str
    pluginId: str


class DeleteRetrieverRequestRequestTypeDef(TypedDict):
    applicationId: str
    retrieverId: str


class DeleteUserRequestRequestTypeDef(TypedDict):
    applicationId: str
    userId: str


class DeleteWebExperienceRequestRequestTypeDef(TypedDict):
    applicationId: str
    webExperienceId: str


class NumberAttributeBoostingConfigurationTypeDef(TypedDict):
    boostingLevel: DocumentAttributeBoostingLevelType
    boostingType: NotRequired[NumberAttributeBoostingTypeType]


class StringAttributeBoostingConfigurationOutputTypeDef(TypedDict):
    boostingLevel: DocumentAttributeBoostingLevelType
    attributeValueBoosting: NotRequired[Dict[str, StringAttributeValueBoostingLevelType]]


class StringListAttributeBoostingConfigurationTypeDef(TypedDict):
    boostingLevel: DocumentAttributeBoostingLevelType


class DocumentAttributeValueOutputTypeDef(TypedDict):
    stringValue: NotRequired[str]
    stringListValue: NotRequired[List[str]]
    longValue: NotRequired[int]
    dateValue: NotRequired[datetime]


DocumentAttributeConfigurationTypeDef = TypedDict(
    "DocumentAttributeConfigurationTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[AttributeTypeType],
        "search": NotRequired[StatusType],
    },
)
TimestampTypeDef = Union[datetime, str]


class GetApplicationRequestRequestTypeDef(TypedDict):
    applicationId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetChatControlsConfigurationRequestRequestTypeDef(TypedDict):
    applicationId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class GetDataSourceRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    dataSourceId: str


class GetGroupRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    groupName: str
    dataSourceId: NotRequired[str]


class GetIndexRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str


class GetPluginRequestRequestTypeDef(TypedDict):
    applicationId: str
    pluginId: str


class GetRetrieverRequestRequestTypeDef(TypedDict):
    applicationId: str
    retrieverId: str


class GetUserRequestRequestTypeDef(TypedDict):
    applicationId: str
    userId: str


class GetWebExperienceRequestRequestTypeDef(TypedDict):
    applicationId: str
    webExperienceId: str


MemberGroupTypeDef = TypedDict(
    "MemberGroupTypeDef",
    {
        "groupName": str,
        "type": NotRequired[MembershipTypeType],
    },
)
MemberUserTypeDef = TypedDict(
    "MemberUserTypeDef",
    {
        "userId": str,
        "type": NotRequired[MembershipTypeType],
    },
)


class GroupSummaryTypeDef(TypedDict):
    groupName: NotRequired[str]


class OpenIDConnectProviderConfigurationTypeDef(TypedDict):
    secretsArn: str
    secretsRole: str


class SamlProviderConfigurationTypeDef(TypedDict):
    authenticationUrl: str


class TextDocumentStatisticsTypeDef(TypedDict):
    indexedTextBytes: NotRequired[int]
    indexedTextDocumentCount: NotRequired[int]


class IndexTypeDef(TypedDict):
    displayName: NotRequired[str]
    indexId: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    status: NotRequired[IndexStatusType]


class KendraIndexConfigurationTypeDef(TypedDict):
    indexId: str


class ListApplicationsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListConversationsRequestRequestTypeDef(TypedDict):
    applicationId: str
    userId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDataSourcesRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDocumentsRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    dataSourceIds: NotRequired[Sequence[str]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListIndicesRequestRequestTypeDef(TypedDict):
    applicationId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListMessagesRequestRequestTypeDef(TypedDict):
    conversationId: str
    applicationId: str
    userId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListPluginsRequestRequestTypeDef(TypedDict):
    applicationId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


PluginTypeDef = TypedDict(
    "PluginTypeDef",
    {
        "pluginId": NotRequired[str],
        "displayName": NotRequired[str],
        "type": NotRequired[PluginTypeType],
        "serverUrl": NotRequired[str],
        "state": NotRequired[PluginStateType],
        "buildStatus": NotRequired[PluginBuildStatusType],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
    },
)


class ListRetrieversRequestRequestTypeDef(TypedDict):
    applicationId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


RetrieverTypeDef = TypedDict(
    "RetrieverTypeDef",
    {
        "applicationId": NotRequired[str],
        "retrieverId": NotRequired[str],
        "type": NotRequired[RetrieverTypeType],
        "status": NotRequired[RetrieverStatusType],
        "displayName": NotRequired[str],
    },
)


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str


class ListWebExperiencesRequestRequestTypeDef(TypedDict):
    applicationId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class WebExperienceTypeDef(TypedDict):
    webExperienceId: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    defaultEndpoint: NotRequired[str]
    status: NotRequired[WebExperienceStatusType]


class OAuth2ClientCredentialConfigurationTypeDef(TypedDict):
    secretArn: str
    roleArn: str


class PrincipalGroupTypeDef(TypedDict):
    access: ReadAccessTypeType
    name: NotRequired[str]
    membershipType: NotRequired[MembershipTypeType]


PrincipalUserTypeDef = TypedDict(
    "PrincipalUserTypeDef",
    {
        "access": ReadAccessTypeType,
        "id": NotRequired[str],
        "membershipType": NotRequired[MembershipTypeType],
    },
)


class UsersAndGroupsOutputTypeDef(TypedDict):
    userIds: NotRequired[List[str]]
    userGroups: NotRequired[List[str]]


class SamlConfigurationTypeDef(TypedDict):
    metadataXML: str
    roleArn: str
    userIdAttribute: str
    userGroupAttribute: NotRequired[str]


class SnippetExcerptTypeDef(TypedDict):
    text: NotRequired[str]


class StartDataSourceSyncJobRequestRequestTypeDef(TypedDict):
    dataSourceId: str
    applicationId: str
    indexId: str


class StopDataSourceSyncJobRequestRequestTypeDef(TypedDict):
    dataSourceId: str
    applicationId: str
    indexId: str


class StringAttributeBoostingConfigurationTypeDef(TypedDict):
    boostingLevel: DocumentAttributeBoostingLevelType
    attributeValueBoosting: NotRequired[Mapping[str, StringAttributeValueBoostingLevelType]]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str
    tagKeys: Sequence[str]


class UsersAndGroupsTypeDef(TypedDict):
    userIds: NotRequired[Sequence[str]]
    userGroups: NotRequired[Sequence[str]]


class APISchemaTypeDef(TypedDict):
    payload: NotRequired[str]
    s3: NotRequired[S3TypeDef]


class ActionExecutionOutputTypeDef(TypedDict):
    pluginId: str
    payload: Dict[str, ActionExecutionPayloadFieldOutputTypeDef]
    payloadFieldNameSeparator: str


ActionExecutionPayloadFieldUnionTypeDef = Union[
    ActionExecutionPayloadFieldTypeDef, ActionExecutionPayloadFieldOutputTypeDef
]
ActionReviewPayloadFieldTypeDef = TypedDict(
    "ActionReviewPayloadFieldTypeDef",
    {
        "displayName": NotRequired[str],
        "displayOrder": NotRequired[int],
        "displayDescription": NotRequired[str],
        "type": NotRequired[ActionPayloadFieldTypeType],
        "value": NotRequired[Dict[str, Any]],
        "allowedValues": NotRequired[List[ActionReviewPayloadFieldAllowedValueTypeDef]],
        "allowedFormat": NotRequired[str],
        "required": NotRequired[bool],
    },
)


class AttachmentInputTypeDef(TypedDict):
    name: str
    data: BlobTypeDef


class DocumentContentTypeDef(TypedDict):
    blob: NotRequired[BlobTypeDef]
    s3: NotRequired[S3TypeDef]


class AttachmentOutputTypeDef(TypedDict):
    name: NotRequired[str]
    status: NotRequired[AttachmentStatusType]
    error: NotRequired[ErrorDetailTypeDef]


class DocumentDetailsTypeDef(TypedDict):
    documentId: NotRequired[str]
    status: NotRequired[DocumentStatusType]
    error: NotRequired[ErrorDetailTypeDef]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


FailedDocumentTypeDef = TypedDict(
    "FailedDocumentTypeDef",
    {
        "id": NotRequired[str],
        "error": NotRequired[ErrorDetailTypeDef],
        "dataSourceId": NotRequired[str],
    },
)


class GroupStatusDetailTypeDef(TypedDict):
    status: NotRequired[GroupStatusType]
    lastUpdatedAt: NotRequired[datetime]
    errorDetail: NotRequired[ErrorDetailTypeDef]


class BatchDeleteDocumentRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    documents: Sequence[DeleteDocumentTypeDef]
    dataSourceSyncId: NotRequired[str]


class CreateApplicationResponseTypeDef(TypedDict):
    applicationId: str
    applicationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataSourceResponseTypeDef(TypedDict):
    dataSourceId: str
    dataSourceArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIndexResponseTypeDef(TypedDict):
    indexId: str
    indexArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePluginResponseTypeDef(TypedDict):
    pluginId: str
    pluginArn: str
    buildStatus: PluginBuildStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRetrieverResponseTypeDef(TypedDict):
    retrieverId: str
    retrieverArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateWebExperienceResponseTypeDef(TypedDict):
    webExperienceId: str
    webExperienceArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ListApplicationsResponseTypeDef(TypedDict):
    applications: List[ApplicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StartDataSourceSyncJobResponseTypeDef(TypedDict):
    executionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ChatModeConfigurationTypeDef(TypedDict):
    pluginConfiguration: NotRequired[PluginConfigurationTypeDef]


class ContentRetrievalRuleOutputTypeDef(TypedDict):
    eligibleDataSources: NotRequired[List[EligibleDataSourceTypeDef]]


class ContentRetrievalRuleTypeDef(TypedDict):
    eligibleDataSources: NotRequired[Sequence[EligibleDataSourceTypeDef]]


class ListConversationsResponseTypeDef(TypedDict):
    conversations: List[ConversationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetApplicationResponseTypeDef(TypedDict):
    displayName: str
    applicationId: str
    applicationArn: str
    identityType: IdentityTypeType
    iamIdentityProviderArn: str
    identityCenterApplicationArn: str
    roleArn: str
    status: ApplicationStatusType
    description: str
    encryptionConfiguration: EncryptionConfigurationTypeDef
    createdAt: datetime
    updatedAt: datetime
    error: ErrorDetailTypeDef
    attachmentsConfiguration: AppliedAttachmentsConfigurationTypeDef
    qAppsConfiguration: QAppsConfigurationTypeDef
    personalizationConfiguration: PersonalizationConfigurationTypeDef
    autoSubscriptionConfiguration: AutoSubscriptionConfigurationTypeDef
    clientIdsForOIDC: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateApplicationRequestRequestTypeDef(TypedDict):
    applicationId: str
    identityCenterInstanceArn: NotRequired[str]
    displayName: NotRequired[str]
    description: NotRequired[str]
    roleArn: NotRequired[str]
    attachmentsConfiguration: NotRequired[AttachmentsConfigurationTypeDef]
    qAppsConfiguration: NotRequired[QAppsConfigurationTypeDef]
    personalizationConfiguration: NotRequired[PersonalizationConfigurationTypeDef]
    autoSubscriptionConfiguration: NotRequired[AutoSubscriptionConfigurationTypeDef]


class CreateApplicationRequestRequestTypeDef(TypedDict):
    displayName: str
    roleArn: NotRequired[str]
    identityType: NotRequired[IdentityTypeType]
    iamIdentityProviderArn: NotRequired[str]
    identityCenterInstanceArn: NotRequired[str]
    clientIdsForOIDC: NotRequired[Sequence[str]]
    description: NotRequired[str]
    encryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]
    clientToken: NotRequired[str]
    attachmentsConfiguration: NotRequired[AttachmentsConfigurationTypeDef]
    qAppsConfiguration: NotRequired[QAppsConfigurationTypeDef]
    personalizationConfiguration: NotRequired[PersonalizationConfigurationTypeDef]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str
    tags: Sequence[TagTypeDef]


CreateIndexRequestRequestTypeDef = TypedDict(
    "CreateIndexRequestRequestTypeDef",
    {
        "applicationId": str,
        "displayName": str,
        "type": NotRequired[IndexTypeType],
        "description": NotRequired[str],
        "tags": NotRequired[Sequence[TagTypeDef]],
        "capacityConfiguration": NotRequired[IndexCapacityConfigurationTypeDef],
        "clientToken": NotRequired[str],
    },
)


class CreateUserRequestRequestTypeDef(TypedDict):
    applicationId: str
    userId: str
    userAliases: NotRequired[Sequence[UserAliasTypeDef]]
    clientToken: NotRequired[str]


class GetUserResponseTypeDef(TypedDict):
    userAliases: List[UserAliasTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateUserRequestRequestTypeDef(TypedDict):
    applicationId: str
    userId: str
    userAliasesToUpdate: NotRequired[Sequence[UserAliasTypeDef]]
    userAliasesToDelete: NotRequired[Sequence[UserAliasTypeDef]]


class UpdateUserResponseTypeDef(TypedDict):
    userAliasesAdded: List[UserAliasTypeDef]
    userAliasesUpdated: List[UserAliasTypeDef]
    userAliasesDeleted: List[UserAliasTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DataSourceSyncJobTypeDef(TypedDict):
    executionId: NotRequired[str]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    status: NotRequired[DataSourceSyncJobStatusType]
    error: NotRequired[ErrorDetailTypeDef]
    dataSourceErrorCode: NotRequired[str]
    metrics: NotRequired[DataSourceSyncJobMetricsTypeDef]


class ListDataSourcesResponseTypeDef(TypedDict):
    dataSources: List[DataSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DocumentAttributeBoostingConfigurationOutputTypeDef(TypedDict):
    numberConfiguration: NotRequired[NumberAttributeBoostingConfigurationTypeDef]
    stringConfiguration: NotRequired[StringAttributeBoostingConfigurationOutputTypeDef]
    dateConfiguration: NotRequired[DateAttributeBoostingConfigurationTypeDef]
    stringListConfiguration: NotRequired[StringListAttributeBoostingConfigurationTypeDef]


DocumentAttributeConditionOutputTypeDef = TypedDict(
    "DocumentAttributeConditionOutputTypeDef",
    {
        "key": str,
        "operator": DocumentEnrichmentConditionOperatorType,
        "value": NotRequired[DocumentAttributeValueOutputTypeDef],
    },
)


class DocumentAttributeTargetOutputTypeDef(TypedDict):
    key: str
    value: NotRequired[DocumentAttributeValueOutputTypeDef]
    attributeValueOperator: NotRequired[Literal["DELETE"]]


class UpdateIndexRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    displayName: NotRequired[str]
    description: NotRequired[str]
    capacityConfiguration: NotRequired[IndexCapacityConfigurationTypeDef]
    documentAttributeConfigurations: NotRequired[Sequence[DocumentAttributeConfigurationTypeDef]]


class DocumentAttributeValueTypeDef(TypedDict):
    stringValue: NotRequired[str]
    stringListValue: NotRequired[Sequence[str]]
    longValue: NotRequired[int]
    dateValue: NotRequired[TimestampTypeDef]


class ListDataSourceSyncJobsRequestRequestTypeDef(TypedDict):
    dataSourceId: str
    applicationId: str
    indexId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    statusFilter: NotRequired[DataSourceSyncJobStatusType]


class ListGroupsRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    updatedEarlierThan: TimestampTypeDef
    dataSourceId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class MessageUsefulnessFeedbackTypeDef(TypedDict):
    usefulness: MessageUsefulnessType
    submittedAt: TimestampTypeDef
    reason: NotRequired[MessageUsefulnessReasonType]
    comment: NotRequired[str]


class GetChatControlsConfigurationRequestGetChatControlsConfigurationPaginateTypeDef(TypedDict):
    applicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListApplicationsRequestListApplicationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListConversationsRequestListConversationsPaginateTypeDef(TypedDict):
    applicationId: str
    userId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataSourceSyncJobsRequestListDataSourceSyncJobsPaginateTypeDef(TypedDict):
    dataSourceId: str
    applicationId: str
    indexId: str
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    statusFilter: NotRequired[DataSourceSyncJobStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataSourcesRequestListDataSourcesPaginateTypeDef(TypedDict):
    applicationId: str
    indexId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDocumentsRequestListDocumentsPaginateTypeDef(TypedDict):
    applicationId: str
    indexId: str
    dataSourceIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupsRequestListGroupsPaginateTypeDef(TypedDict):
    applicationId: str
    indexId: str
    updatedEarlierThan: TimestampTypeDef
    dataSourceId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIndicesRequestListIndicesPaginateTypeDef(TypedDict):
    applicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMessagesRequestListMessagesPaginateTypeDef(TypedDict):
    conversationId: str
    applicationId: str
    userId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPluginsRequestListPluginsPaginateTypeDef(TypedDict):
    applicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRetrieversRequestListRetrieversPaginateTypeDef(TypedDict):
    applicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWebExperiencesRequestListWebExperiencesPaginateTypeDef(TypedDict):
    applicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GroupMembersTypeDef(TypedDict):
    memberGroups: NotRequired[Sequence[MemberGroupTypeDef]]
    memberUsers: NotRequired[Sequence[MemberUserTypeDef]]


class ListGroupsResponseTypeDef(TypedDict):
    items: List[GroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class IdentityProviderConfigurationTypeDef(TypedDict):
    samlConfiguration: NotRequired[SamlProviderConfigurationTypeDef]
    openIDConnectConfiguration: NotRequired[OpenIDConnectProviderConfigurationTypeDef]


class IndexStatisticsTypeDef(TypedDict):
    textDocumentStatistics: NotRequired[TextDocumentStatisticsTypeDef]


class ListIndicesResponseTypeDef(TypedDict):
    indices: List[IndexTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPluginsResponseTypeDef(TypedDict):
    plugins: List[PluginTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListRetrieversResponseTypeDef(TypedDict):
    retrievers: List[RetrieverTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListWebExperiencesResponseTypeDef(TypedDict):
    webExperiences: List[WebExperienceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PluginAuthConfigurationOutputTypeDef(TypedDict):
    basicAuthConfiguration: NotRequired[BasicAuthConfigurationTypeDef]
    oAuth2ClientCredentialConfiguration: NotRequired[OAuth2ClientCredentialConfigurationTypeDef]
    noAuthConfiguration: NotRequired[Dict[str, Any]]


class PluginAuthConfigurationTypeDef(TypedDict):
    basicAuthConfiguration: NotRequired[BasicAuthConfigurationTypeDef]
    oAuth2ClientCredentialConfiguration: NotRequired[OAuth2ClientCredentialConfigurationTypeDef]
    noAuthConfiguration: NotRequired[Mapping[str, Any]]


class PrincipalTypeDef(TypedDict):
    user: NotRequired[PrincipalUserTypeDef]
    group: NotRequired[PrincipalGroupTypeDef]


class WebExperienceAuthConfigurationTypeDef(TypedDict):
    samlConfiguration: NotRequired[SamlConfigurationTypeDef]


class TextSegmentTypeDef(TypedDict):
    beginOffset: NotRequired[int]
    endOffset: NotRequired[int]
    snippetExcerpt: NotRequired[SnippetExcerptTypeDef]


StringAttributeBoostingConfigurationUnionTypeDef = Union[
    StringAttributeBoostingConfigurationTypeDef, StringAttributeBoostingConfigurationOutputTypeDef
]
UsersAndGroupsUnionTypeDef = Union[UsersAndGroupsTypeDef, UsersAndGroupsOutputTypeDef]


class CustomPluginConfigurationTypeDef(TypedDict):
    description: str
    apiSchemaType: Literal["OPEN_API_V3"]
    apiSchema: APISchemaTypeDef


class ActionExecutionEventTypeDef(TypedDict):
    pluginId: str
    payload: Mapping[str, ActionExecutionPayloadFieldUnionTypeDef]
    payloadFieldNameSeparator: str


class ActionExecutionTypeDef(TypedDict):
    pluginId: str
    payload: Mapping[str, ActionExecutionPayloadFieldUnionTypeDef]
    payloadFieldNameSeparator: str


class ActionReviewEventTypeDef(TypedDict):
    conversationId: NotRequired[str]
    userMessageId: NotRequired[str]
    systemMessageId: NotRequired[str]
    pluginId: NotRequired[str]
    pluginType: NotRequired[PluginTypeType]
    payload: NotRequired[Dict[str, ActionReviewPayloadFieldTypeDef]]
    payloadFieldNameSeparator: NotRequired[str]


class ActionReviewTypeDef(TypedDict):
    pluginId: NotRequired[str]
    pluginType: NotRequired[PluginTypeType]
    payload: NotRequired[Dict[str, ActionReviewPayloadFieldTypeDef]]
    payloadFieldNameSeparator: NotRequired[str]


class AttachmentInputEventTypeDef(TypedDict):
    attachment: NotRequired[AttachmentInputTypeDef]


class FailedAttachmentEventTypeDef(TypedDict):
    conversationId: NotRequired[str]
    userMessageId: NotRequired[str]
    systemMessageId: NotRequired[str]
    attachment: NotRequired[AttachmentOutputTypeDef]


class ListDocumentsResponseTypeDef(TypedDict):
    documentDetailList: List[DocumentDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class BatchDeleteDocumentResponseTypeDef(TypedDict):
    failedDocuments: List[FailedDocumentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchPutDocumentResponseTypeDef(TypedDict):
    failedDocuments: List[FailedDocumentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetGroupResponseTypeDef(TypedDict):
    status: GroupStatusDetailTypeDef
    statusHistory: List[GroupStatusDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RuleConfigurationOutputTypeDef(TypedDict):
    contentBlockerRule: NotRequired[ContentBlockerRuleTypeDef]
    contentRetrievalRule: NotRequired[ContentRetrievalRuleOutputTypeDef]


ContentRetrievalRuleUnionTypeDef = Union[
    ContentRetrievalRuleTypeDef, ContentRetrievalRuleOutputTypeDef
]


class ListDataSourceSyncJobsResponseTypeDef(TypedDict):
    history: List[DataSourceSyncJobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class NativeIndexConfigurationOutputTypeDef(TypedDict):
    indexId: str
    boostingOverride: NotRequired[Dict[str, DocumentAttributeBoostingConfigurationOutputTypeDef]]


class HookConfigurationOutputTypeDef(TypedDict):
    invocationCondition: NotRequired[DocumentAttributeConditionOutputTypeDef]
    lambdaArn: NotRequired[str]
    s3BucketName: NotRequired[str]
    roleArn: NotRequired[str]


class InlineDocumentEnrichmentConfigurationOutputTypeDef(TypedDict):
    condition: NotRequired[DocumentAttributeConditionOutputTypeDef]
    target: NotRequired[DocumentAttributeTargetOutputTypeDef]
    documentContentOperator: NotRequired[Literal["DELETE"]]


DocumentAttributeValueUnionTypeDef = Union[
    DocumentAttributeValueTypeDef, DocumentAttributeValueOutputTypeDef
]


class PutFeedbackRequestRequestTypeDef(TypedDict):
    applicationId: str
    conversationId: str
    messageId: str
    userId: NotRequired[str]
    messageCopiedAt: NotRequired[TimestampTypeDef]
    messageUsefulness: NotRequired[MessageUsefulnessFeedbackTypeDef]


PutGroupRequestRequestTypeDef = TypedDict(
    "PutGroupRequestRequestTypeDef",
    {
        "applicationId": str,
        "indexId": str,
        "groupName": str,
        "type": MembershipTypeType,
        "groupMembers": GroupMembersTypeDef,
        "dataSourceId": NotRequired[str],
    },
)


class CreateWebExperienceRequestRequestTypeDef(TypedDict):
    applicationId: str
    title: NotRequired[str]
    subtitle: NotRequired[str]
    welcomeMessage: NotRequired[str]
    samplePromptsControlMode: NotRequired[WebExperienceSamplePromptsControlModeType]
    roleArn: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    clientToken: NotRequired[str]
    identityProviderConfiguration: NotRequired[IdentityProviderConfigurationTypeDef]


GetIndexResponseTypeDef = TypedDict(
    "GetIndexResponseTypeDef",
    {
        "applicationId": str,
        "indexId": str,
        "displayName": str,
        "type": IndexTypeType,
        "indexArn": str,
        "status": IndexStatusType,
        "description": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "capacityConfiguration": IndexCapacityConfigurationTypeDef,
        "documentAttributeConfigurations": List[DocumentAttributeConfigurationTypeDef],
        "error": ErrorDetailTypeDef,
        "indexStatistics": IndexStatisticsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class AccessControlTypeDef(TypedDict):
    principals: Sequence[PrincipalTypeDef]
    memberRelation: NotRequired[MemberRelationType]


class GetWebExperienceResponseTypeDef(TypedDict):
    applicationId: str
    webExperienceId: str
    webExperienceArn: str
    defaultEndpoint: str
    status: WebExperienceStatusType
    createdAt: datetime
    updatedAt: datetime
    title: str
    subtitle: str
    welcomeMessage: str
    samplePromptsControlMode: WebExperienceSamplePromptsControlModeType
    roleArn: str
    identityProviderConfiguration: IdentityProviderConfigurationTypeDef
    authenticationConfiguration: WebExperienceAuthConfigurationTypeDef
    error: ErrorDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateWebExperienceRequestRequestTypeDef(TypedDict):
    applicationId: str
    webExperienceId: str
    roleArn: NotRequired[str]
    authenticationConfiguration: NotRequired[WebExperienceAuthConfigurationTypeDef]
    title: NotRequired[str]
    subtitle: NotRequired[str]
    welcomeMessage: NotRequired[str]
    samplePromptsControlMode: NotRequired[WebExperienceSamplePromptsControlModeType]
    identityProviderConfiguration: NotRequired[IdentityProviderConfigurationTypeDef]


class SourceAttributionTypeDef(TypedDict):
    title: NotRequired[str]
    snippet: NotRequired[str]
    url: NotRequired[str]
    citationNumber: NotRequired[int]
    updatedAt: NotRequired[datetime]
    textMessageSegments: NotRequired[List[TextSegmentTypeDef]]


class DocumentAttributeBoostingConfigurationTypeDef(TypedDict):
    numberConfiguration: NotRequired[NumberAttributeBoostingConfigurationTypeDef]
    stringConfiguration: NotRequired[StringAttributeBoostingConfigurationUnionTypeDef]
    dateConfiguration: NotRequired[DateAttributeBoostingConfigurationTypeDef]
    stringListConfiguration: NotRequired[StringListAttributeBoostingConfigurationTypeDef]


CreatePluginRequestRequestTypeDef = TypedDict(
    "CreatePluginRequestRequestTypeDef",
    {
        "applicationId": str,
        "displayName": str,
        "type": PluginTypeType,
        "authConfiguration": PluginAuthConfigurationTypeDef,
        "serverUrl": NotRequired[str],
        "customPluginConfiguration": NotRequired[CustomPluginConfigurationTypeDef],
        "tags": NotRequired[Sequence[TagTypeDef]],
        "clientToken": NotRequired[str],
    },
)
GetPluginResponseTypeDef = TypedDict(
    "GetPluginResponseTypeDef",
    {
        "applicationId": str,
        "pluginId": str,
        "displayName": str,
        "type": PluginTypeType,
        "serverUrl": str,
        "authConfiguration": PluginAuthConfigurationOutputTypeDef,
        "customPluginConfiguration": CustomPluginConfigurationTypeDef,
        "buildStatus": PluginBuildStatusType,
        "pluginArn": str,
        "state": PluginStateType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class UpdatePluginRequestRequestTypeDef(TypedDict):
    applicationId: str
    pluginId: str
    displayName: NotRequired[str]
    state: NotRequired[PluginStateType]
    serverUrl: NotRequired[str]
    customPluginConfiguration: NotRequired[CustomPluginConfigurationTypeDef]
    authConfiguration: NotRequired[PluginAuthConfigurationTypeDef]


class RuleOutputTypeDef(TypedDict):
    ruleType: RuleTypeType
    includedUsersAndGroups: NotRequired[UsersAndGroupsOutputTypeDef]
    excludedUsersAndGroups: NotRequired[UsersAndGroupsOutputTypeDef]
    ruleConfiguration: NotRequired[RuleConfigurationOutputTypeDef]


class RuleConfigurationTypeDef(TypedDict):
    contentBlockerRule: NotRequired[ContentBlockerRuleTypeDef]
    contentRetrievalRule: NotRequired[ContentRetrievalRuleUnionTypeDef]


class RetrieverConfigurationOutputTypeDef(TypedDict):
    nativeIndexConfiguration: NotRequired[NativeIndexConfigurationOutputTypeDef]
    kendraIndexConfiguration: NotRequired[KendraIndexConfigurationTypeDef]


class DocumentEnrichmentConfigurationOutputTypeDef(TypedDict):
    inlineConfigurations: NotRequired[List[InlineDocumentEnrichmentConfigurationOutputTypeDef]]
    preExtractionHookConfiguration: NotRequired[HookConfigurationOutputTypeDef]
    postExtractionHookConfiguration: NotRequired[HookConfigurationOutputTypeDef]


DocumentAttributeConditionTypeDef = TypedDict(
    "DocumentAttributeConditionTypeDef",
    {
        "key": str,
        "operator": DocumentEnrichmentConditionOperatorType,
        "value": NotRequired[DocumentAttributeValueUnionTypeDef],
    },
)


class DocumentAttributeTargetTypeDef(TypedDict):
    key: str
    value: NotRequired[DocumentAttributeValueUnionTypeDef]
    attributeValueOperator: NotRequired[Literal["DELETE"]]


class DocumentAttributeTypeDef(TypedDict):
    name: str
    value: DocumentAttributeValueUnionTypeDef


class AccessConfigurationTypeDef(TypedDict):
    accessControls: Sequence[AccessControlTypeDef]
    memberRelation: NotRequired[MemberRelationType]


class ChatSyncOutputTypeDef(TypedDict):
    conversationId: str
    systemMessage: str
    systemMessageId: str
    userMessageId: str
    actionReview: ActionReviewTypeDef
    authChallengeRequest: AuthChallengeRequestTypeDef
    sourceAttributions: List[SourceAttributionTypeDef]
    failedAttachments: List[AttachmentOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


MessageTypeDef = TypedDict(
    "MessageTypeDef",
    {
        "messageId": NotRequired[str],
        "body": NotRequired[str],
        "time": NotRequired[datetime],
        "type": NotRequired[MessageTypeType],
        "attachments": NotRequired[List[AttachmentOutputTypeDef]],
        "sourceAttribution": NotRequired[List[SourceAttributionTypeDef]],
        "actionReview": NotRequired[ActionReviewTypeDef],
        "actionExecution": NotRequired[ActionExecutionOutputTypeDef],
    },
)


class MetadataEventTypeDef(TypedDict):
    conversationId: NotRequired[str]
    userMessageId: NotRequired[str]
    systemMessageId: NotRequired[str]
    sourceAttributions: NotRequired[List[SourceAttributionTypeDef]]
    finalTextMessage: NotRequired[str]


DocumentAttributeBoostingConfigurationUnionTypeDef = Union[
    DocumentAttributeBoostingConfigurationTypeDef,
    DocumentAttributeBoostingConfigurationOutputTypeDef,
]


class TopicConfigurationOutputTypeDef(TypedDict):
    name: str
    rules: List[RuleOutputTypeDef]
    description: NotRequired[str]
    exampleChatMessages: NotRequired[List[str]]


RuleConfigurationUnionTypeDef = Union[RuleConfigurationTypeDef, RuleConfigurationOutputTypeDef]
GetRetrieverResponseTypeDef = TypedDict(
    "GetRetrieverResponseTypeDef",
    {
        "applicationId": str,
        "retrieverId": str,
        "retrieverArn": str,
        "type": RetrieverTypeType,
        "status": RetrieverStatusType,
        "displayName": str,
        "configuration": RetrieverConfigurationOutputTypeDef,
        "roleArn": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDataSourceResponseTypeDef = TypedDict(
    "GetDataSourceResponseTypeDef",
    {
        "applicationId": str,
        "indexId": str,
        "dataSourceId": str,
        "dataSourceArn": str,
        "displayName": str,
        "type": str,
        "configuration": Dict[str, Any],
        "vpcConfiguration": DataSourceVpcConfigurationOutputTypeDef,
        "createdAt": datetime,
        "updatedAt": datetime,
        "description": str,
        "status": DataSourceStatusType,
        "syncSchedule": str,
        "roleArn": str,
        "error": ErrorDetailTypeDef,
        "documentEnrichmentConfiguration": DocumentEnrichmentConfigurationOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DocumentAttributeConditionUnionTypeDef = Union[
    DocumentAttributeConditionTypeDef, DocumentAttributeConditionOutputTypeDef
]
DocumentAttributeTargetUnionTypeDef = Union[
    DocumentAttributeTargetTypeDef, DocumentAttributeTargetOutputTypeDef
]


class AttributeFilterTypeDef(TypedDict):
    andAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    orAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    notFilter: NotRequired[Mapping[str, Any]]
    equalsTo: NotRequired[DocumentAttributeTypeDef]
    containsAll: NotRequired[DocumentAttributeTypeDef]
    containsAny: NotRequired[DocumentAttributeTypeDef]
    greaterThan: NotRequired[DocumentAttributeTypeDef]
    greaterThanOrEquals: NotRequired[DocumentAttributeTypeDef]
    lessThan: NotRequired[DocumentAttributeTypeDef]
    lessThanOrEquals: NotRequired[DocumentAttributeTypeDef]


class ListMessagesResponseTypeDef(TypedDict):
    messages: List[MessageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ChatOutputStreamTypeDef(TypedDict):
    textEvent: NotRequired[TextOutputEventTypeDef]
    metadataEvent: NotRequired[MetadataEventTypeDef]
    actionReviewEvent: NotRequired[ActionReviewEventTypeDef]
    failedAttachmentEvent: NotRequired[FailedAttachmentEventTypeDef]
    authChallengeRequestEvent: NotRequired[AuthChallengeRequestEventTypeDef]


class NativeIndexConfigurationTypeDef(TypedDict):
    indexId: str
    boostingOverride: NotRequired[Mapping[str, DocumentAttributeBoostingConfigurationUnionTypeDef]]


class GetChatControlsConfigurationResponseTypeDef(TypedDict):
    responseScope: ResponseScopeType
    blockedPhrases: BlockedPhrasesConfigurationTypeDef
    topicConfigurations: List[TopicConfigurationOutputTypeDef]
    creatorModeConfiguration: AppliedCreatorModeConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RuleTypeDef(TypedDict):
    ruleType: RuleTypeType
    includedUsersAndGroups: NotRequired[UsersAndGroupsUnionTypeDef]
    excludedUsersAndGroups: NotRequired[UsersAndGroupsUnionTypeDef]
    ruleConfiguration: NotRequired[RuleConfigurationUnionTypeDef]


class HookConfigurationTypeDef(TypedDict):
    invocationCondition: NotRequired[DocumentAttributeConditionUnionTypeDef]
    lambdaArn: NotRequired[str]
    s3BucketName: NotRequired[str]
    roleArn: NotRequired[str]


class InlineDocumentEnrichmentConfigurationTypeDef(TypedDict):
    condition: NotRequired[DocumentAttributeConditionUnionTypeDef]
    target: NotRequired[DocumentAttributeTargetUnionTypeDef]
    documentContentOperator: NotRequired[Literal["DELETE"]]


class ChatSyncInputRequestTypeDef(TypedDict):
    applicationId: str
    userId: NotRequired[str]
    userGroups: NotRequired[Sequence[str]]
    userMessage: NotRequired[str]
    attachments: NotRequired[Sequence[AttachmentInputTypeDef]]
    actionExecution: NotRequired[ActionExecutionTypeDef]
    authChallengeResponse: NotRequired[AuthChallengeResponseTypeDef]
    conversationId: NotRequired[str]
    parentMessageId: NotRequired[str]
    attributeFilter: NotRequired[AttributeFilterTypeDef]
    chatMode: NotRequired[ChatModeType]
    chatModeConfiguration: NotRequired[ChatModeConfigurationTypeDef]
    clientToken: NotRequired[str]


class ConfigurationEventTypeDef(TypedDict):
    chatMode: NotRequired[ChatModeType]
    chatModeConfiguration: NotRequired[ChatModeConfigurationTypeDef]
    attributeFilter: NotRequired[AttributeFilterTypeDef]


class ChatOutputTypeDef(TypedDict):
    outputStream: "AioEventStream[ChatOutputStreamTypeDef]"
    ResponseMetadata: ResponseMetadataTypeDef


NativeIndexConfigurationUnionTypeDef = Union[
    NativeIndexConfigurationTypeDef, NativeIndexConfigurationOutputTypeDef
]
RuleUnionTypeDef = Union[RuleTypeDef, RuleOutputTypeDef]
HookConfigurationUnionTypeDef = Union[HookConfigurationTypeDef, HookConfigurationOutputTypeDef]
InlineDocumentEnrichmentConfigurationUnionTypeDef = Union[
    InlineDocumentEnrichmentConfigurationTypeDef, InlineDocumentEnrichmentConfigurationOutputTypeDef
]


class ChatInputStreamTypeDef(TypedDict):
    configurationEvent: NotRequired[ConfigurationEventTypeDef]
    textEvent: NotRequired[TextInputEventTypeDef]
    attachmentEvent: NotRequired[AttachmentInputEventTypeDef]
    actionExecutionEvent: NotRequired[ActionExecutionEventTypeDef]
    endOfInputEvent: NotRequired[Mapping[str, Any]]
    authChallengeResponseEvent: NotRequired[AuthChallengeResponseEventTypeDef]


class RetrieverConfigurationTypeDef(TypedDict):
    nativeIndexConfiguration: NotRequired[NativeIndexConfigurationUnionTypeDef]
    kendraIndexConfiguration: NotRequired[KendraIndexConfigurationTypeDef]


class TopicConfigurationTypeDef(TypedDict):
    name: str
    rules: Sequence[RuleUnionTypeDef]
    description: NotRequired[str]
    exampleChatMessages: NotRequired[Sequence[str]]


class DocumentEnrichmentConfigurationTypeDef(TypedDict):
    inlineConfigurations: NotRequired[Sequence[InlineDocumentEnrichmentConfigurationUnionTypeDef]]
    preExtractionHookConfiguration: NotRequired[HookConfigurationUnionTypeDef]
    postExtractionHookConfiguration: NotRequired[HookConfigurationUnionTypeDef]


class ChatInputRequestTypeDef(TypedDict):
    applicationId: str
    userId: NotRequired[str]
    userGroups: NotRequired[Sequence[str]]
    conversationId: NotRequired[str]
    parentMessageId: NotRequired[str]
    clientToken: NotRequired[str]
    inputStream: NotRequired["AioEventStream[ChatInputStreamTypeDef]"]


CreateRetrieverRequestRequestTypeDef = TypedDict(
    "CreateRetrieverRequestRequestTypeDef",
    {
        "applicationId": str,
        "type": RetrieverTypeType,
        "displayName": str,
        "configuration": RetrieverConfigurationTypeDef,
        "roleArn": NotRequired[str],
        "clientToken": NotRequired[str],
        "tags": NotRequired[Sequence[TagTypeDef]],
    },
)


class UpdateRetrieverRequestRequestTypeDef(TypedDict):
    applicationId: str
    retrieverId: str
    configuration: NotRequired[RetrieverConfigurationTypeDef]
    displayName: NotRequired[str]
    roleArn: NotRequired[str]


TopicConfigurationUnionTypeDef = Union[TopicConfigurationTypeDef, TopicConfigurationOutputTypeDef]


class CreateDataSourceRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    displayName: str
    configuration: Mapping[str, Any]
    vpcConfiguration: NotRequired[DataSourceVpcConfigurationTypeDef]
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    syncSchedule: NotRequired[str]
    roleArn: NotRequired[str]
    clientToken: NotRequired[str]
    documentEnrichmentConfiguration: NotRequired[DocumentEnrichmentConfigurationTypeDef]


DocumentEnrichmentConfigurationUnionTypeDef = Union[
    DocumentEnrichmentConfigurationTypeDef, DocumentEnrichmentConfigurationOutputTypeDef
]


class UpdateDataSourceRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    dataSourceId: str
    displayName: NotRequired[str]
    configuration: NotRequired[Mapping[str, Any]]
    vpcConfiguration: NotRequired[DataSourceVpcConfigurationTypeDef]
    description: NotRequired[str]
    syncSchedule: NotRequired[str]
    roleArn: NotRequired[str]
    documentEnrichmentConfiguration: NotRequired[DocumentEnrichmentConfigurationTypeDef]


class UpdateChatControlsConfigurationRequestRequestTypeDef(TypedDict):
    applicationId: str
    clientToken: NotRequired[str]
    responseScope: NotRequired[ResponseScopeType]
    blockedPhrasesConfigurationUpdate: NotRequired[BlockedPhrasesConfigurationUpdateTypeDef]
    topicConfigurationsToCreateOrUpdate: NotRequired[Sequence[TopicConfigurationUnionTypeDef]]
    topicConfigurationsToDelete: NotRequired[Sequence[TopicConfigurationTypeDef]]
    creatorModeConfiguration: NotRequired[CreatorModeConfigurationTypeDef]


DocumentTypeDef = TypedDict(
    "DocumentTypeDef",
    {
        "id": str,
        "attributes": NotRequired[Sequence[DocumentAttributeTypeDef]],
        "content": NotRequired[DocumentContentTypeDef],
        "contentType": NotRequired[ContentTypeType],
        "title": NotRequired[str],
        "accessConfiguration": NotRequired[AccessConfigurationTypeDef],
        "documentEnrichmentConfiguration": NotRequired[DocumentEnrichmentConfigurationUnionTypeDef],
    },
)


class BatchPutDocumentRequestRequestTypeDef(TypedDict):
    applicationId: str
    indexId: str
    documents: Sequence[DocumentTypeDef]
    roleArn: NotRequired[str]
    dataSourceSyncId: NotRequired[str]
