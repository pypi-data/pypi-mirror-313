"""
Type annotations for chatbot service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/type_defs/)

Usage::

    ```python
    from types_aiobotocore_chatbot.type_defs import AccountPreferencesTypeDef

    data: AccountPreferencesTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Sequence

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AccountPreferencesTypeDef",
    "ChimeWebhookConfigurationTypeDef",
    "ConfiguredTeamTypeDef",
    "CreateChimeWebhookConfigurationRequestRequestTypeDef",
    "CreateChimeWebhookConfigurationResultTypeDef",
    "CreateSlackChannelConfigurationRequestRequestTypeDef",
    "CreateSlackChannelConfigurationResultTypeDef",
    "CreateTeamsChannelConfigurationRequestRequestTypeDef",
    "CreateTeamsChannelConfigurationResultTypeDef",
    "DeleteChimeWebhookConfigurationRequestRequestTypeDef",
    "DeleteMicrosoftTeamsUserIdentityRequestRequestTypeDef",
    "DeleteSlackChannelConfigurationRequestRequestTypeDef",
    "DeleteSlackUserIdentityRequestRequestTypeDef",
    "DeleteSlackWorkspaceAuthorizationRequestRequestTypeDef",
    "DeleteTeamsChannelConfigurationRequestRequestTypeDef",
    "DeleteTeamsConfiguredTeamRequestRequestTypeDef",
    "DescribeChimeWebhookConfigurationsRequestDescribeChimeWebhookConfigurationsPaginateTypeDef",
    "DescribeChimeWebhookConfigurationsRequestRequestTypeDef",
    "DescribeChimeWebhookConfigurationsResultTypeDef",
    "DescribeSlackChannelConfigurationsRequestDescribeSlackChannelConfigurationsPaginateTypeDef",
    "DescribeSlackChannelConfigurationsRequestRequestTypeDef",
    "DescribeSlackChannelConfigurationsResultTypeDef",
    "DescribeSlackUserIdentitiesRequestDescribeSlackUserIdentitiesPaginateTypeDef",
    "DescribeSlackUserIdentitiesRequestRequestTypeDef",
    "DescribeSlackUserIdentitiesResultTypeDef",
    "DescribeSlackWorkspacesRequestDescribeSlackWorkspacesPaginateTypeDef",
    "DescribeSlackWorkspacesRequestRequestTypeDef",
    "DescribeSlackWorkspacesResultTypeDef",
    "GetAccountPreferencesResultTypeDef",
    "GetTeamsChannelConfigurationRequestRequestTypeDef",
    "GetTeamsChannelConfigurationResultTypeDef",
    "ListMicrosoftTeamsConfiguredTeamsRequestListMicrosoftTeamsConfiguredTeamsPaginateTypeDef",
    "ListMicrosoftTeamsConfiguredTeamsRequestRequestTypeDef",
    "ListMicrosoftTeamsConfiguredTeamsResultTypeDef",
    "ListMicrosoftTeamsUserIdentitiesRequestListMicrosoftTeamsUserIdentitiesPaginateTypeDef",
    "ListMicrosoftTeamsUserIdentitiesRequestRequestTypeDef",
    "ListMicrosoftTeamsUserIdentitiesResultTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTeamsChannelConfigurationsRequestListMicrosoftTeamsChannelConfigurationsPaginateTypeDef",
    "ListTeamsChannelConfigurationsRequestRequestTypeDef",
    "ListTeamsChannelConfigurationsResultTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "SlackChannelConfigurationTypeDef",
    "SlackUserIdentityTypeDef",
    "SlackWorkspaceTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TeamsChannelConfigurationTypeDef",
    "TeamsUserIdentityTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccountPreferencesRequestRequestTypeDef",
    "UpdateAccountPreferencesResultTypeDef",
    "UpdateChimeWebhookConfigurationRequestRequestTypeDef",
    "UpdateChimeWebhookConfigurationResultTypeDef",
    "UpdateSlackChannelConfigurationRequestRequestTypeDef",
    "UpdateSlackChannelConfigurationResultTypeDef",
    "UpdateTeamsChannelConfigurationRequestRequestTypeDef",
    "UpdateTeamsChannelConfigurationResultTypeDef",
)


class AccountPreferencesTypeDef(TypedDict):
    UserAuthorizationRequired: NotRequired[bool]
    TrainingDataCollectionEnabled: NotRequired[bool]


class TagTypeDef(TypedDict):
    TagKey: str
    TagValue: str


class ConfiguredTeamTypeDef(TypedDict):
    TenantId: str
    TeamId: str
    TeamName: NotRequired[str]
    State: NotRequired[str]
    StateReason: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeleteChimeWebhookConfigurationRequestRequestTypeDef(TypedDict):
    ChatConfigurationArn: str


class DeleteMicrosoftTeamsUserIdentityRequestRequestTypeDef(TypedDict):
    ChatConfigurationArn: str
    UserId: str


class DeleteSlackChannelConfigurationRequestRequestTypeDef(TypedDict):
    ChatConfigurationArn: str


class DeleteSlackUserIdentityRequestRequestTypeDef(TypedDict):
    ChatConfigurationArn: str
    SlackTeamId: str
    SlackUserId: str


class DeleteSlackWorkspaceAuthorizationRequestRequestTypeDef(TypedDict):
    SlackTeamId: str


class DeleteTeamsChannelConfigurationRequestRequestTypeDef(TypedDict):
    ChatConfigurationArn: str


class DeleteTeamsConfiguredTeamRequestRequestTypeDef(TypedDict):
    TeamId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeChimeWebhookConfigurationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ChatConfigurationArn: NotRequired[str]


class DescribeSlackChannelConfigurationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ChatConfigurationArn: NotRequired[str]


class DescribeSlackUserIdentitiesRequestRequestTypeDef(TypedDict):
    ChatConfigurationArn: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class SlackUserIdentityTypeDef(TypedDict):
    IamRoleArn: str
    ChatConfigurationArn: str
    SlackTeamId: str
    SlackUserId: str
    AwsUserIdentity: NotRequired[str]


class DescribeSlackWorkspacesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class SlackWorkspaceTypeDef(TypedDict):
    SlackTeamId: str
    SlackTeamName: str
    State: NotRequired[str]
    StateReason: NotRequired[str]


class GetTeamsChannelConfigurationRequestRequestTypeDef(TypedDict):
    ChatConfigurationArn: str


class ListMicrosoftTeamsConfiguredTeamsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListMicrosoftTeamsUserIdentitiesRequestRequestTypeDef(TypedDict):
    ChatConfigurationArn: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class TeamsUserIdentityTypeDef(TypedDict):
    IamRoleArn: str
    ChatConfigurationArn: str
    TeamId: str
    UserId: NotRequired[str]
    AwsUserIdentity: NotRequired[str]
    TeamsChannelId: NotRequired[str]
    TeamsTenantId: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str


class ListTeamsChannelConfigurationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    TeamId: NotRequired[str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


class UpdateAccountPreferencesRequestRequestTypeDef(TypedDict):
    UserAuthorizationRequired: NotRequired[bool]
    TrainingDataCollectionEnabled: NotRequired[bool]


class UpdateChimeWebhookConfigurationRequestRequestTypeDef(TypedDict):
    ChatConfigurationArn: str
    WebhookDescription: NotRequired[str]
    WebhookUrl: NotRequired[str]
    SnsTopicArns: NotRequired[Sequence[str]]
    IamRoleArn: NotRequired[str]
    LoggingLevel: NotRequired[str]


class UpdateSlackChannelConfigurationRequestRequestTypeDef(TypedDict):
    ChatConfigurationArn: str
    SlackChannelId: str
    SlackChannelName: NotRequired[str]
    SnsTopicArns: NotRequired[Sequence[str]]
    IamRoleArn: NotRequired[str]
    LoggingLevel: NotRequired[str]
    GuardrailPolicyArns: NotRequired[Sequence[str]]
    UserAuthorizationRequired: NotRequired[bool]


class UpdateTeamsChannelConfigurationRequestRequestTypeDef(TypedDict):
    ChatConfigurationArn: str
    ChannelId: str
    ChannelName: NotRequired[str]
    SnsTopicArns: NotRequired[Sequence[str]]
    IamRoleArn: NotRequired[str]
    LoggingLevel: NotRequired[str]
    GuardrailPolicyArns: NotRequired[Sequence[str]]
    UserAuthorizationRequired: NotRequired[bool]


class ChimeWebhookConfigurationTypeDef(TypedDict):
    WebhookDescription: str
    ChatConfigurationArn: str
    IamRoleArn: str
    SnsTopicArns: List[str]
    ConfigurationName: NotRequired[str]
    LoggingLevel: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]
    State: NotRequired[str]
    StateReason: NotRequired[str]


class CreateChimeWebhookConfigurationRequestRequestTypeDef(TypedDict):
    WebhookDescription: str
    WebhookUrl: str
    SnsTopicArns: Sequence[str]
    IamRoleArn: str
    ConfigurationName: str
    LoggingLevel: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateSlackChannelConfigurationRequestRequestTypeDef(TypedDict):
    SlackTeamId: str
    SlackChannelId: str
    IamRoleArn: str
    ConfigurationName: str
    SlackChannelName: NotRequired[str]
    SnsTopicArns: NotRequired[Sequence[str]]
    LoggingLevel: NotRequired[str]
    GuardrailPolicyArns: NotRequired[Sequence[str]]
    UserAuthorizationRequired: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateTeamsChannelConfigurationRequestRequestTypeDef(TypedDict):
    ChannelId: str
    TeamId: str
    TenantId: str
    IamRoleArn: str
    ConfigurationName: str
    ChannelName: NotRequired[str]
    TeamName: NotRequired[str]
    SnsTopicArns: NotRequired[Sequence[str]]
    LoggingLevel: NotRequired[str]
    GuardrailPolicyArns: NotRequired[Sequence[str]]
    UserAuthorizationRequired: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]


class SlackChannelConfigurationTypeDef(TypedDict):
    SlackTeamName: str
    SlackTeamId: str
    SlackChannelId: str
    SlackChannelName: str
    ChatConfigurationArn: str
    IamRoleArn: str
    SnsTopicArns: List[str]
    ConfigurationName: NotRequired[str]
    LoggingLevel: NotRequired[str]
    GuardrailPolicyArns: NotRequired[List[str]]
    UserAuthorizationRequired: NotRequired[bool]
    Tags: NotRequired[List[TagTypeDef]]
    State: NotRequired[str]
    StateReason: NotRequired[str]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


class TeamsChannelConfigurationTypeDef(TypedDict):
    ChannelId: str
    TeamId: str
    TenantId: str
    ChatConfigurationArn: str
    IamRoleArn: str
    SnsTopicArns: List[str]
    ChannelName: NotRequired[str]
    TeamName: NotRequired[str]
    ConfigurationName: NotRequired[str]
    LoggingLevel: NotRequired[str]
    GuardrailPolicyArns: NotRequired[List[str]]
    UserAuthorizationRequired: NotRequired[bool]
    Tags: NotRequired[List[TagTypeDef]]
    State: NotRequired[str]
    StateReason: NotRequired[str]


class GetAccountPreferencesResultTypeDef(TypedDict):
    AccountPreferences: AccountPreferencesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListMicrosoftTeamsConfiguredTeamsResultTypeDef(TypedDict):
    ConfiguredTeams: List[ConfiguredTeamTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAccountPreferencesResultTypeDef(TypedDict):
    AccountPreferences: AccountPreferencesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeChimeWebhookConfigurationsRequestDescribeChimeWebhookConfigurationsPaginateTypeDef(
    TypedDict
):
    ChatConfigurationArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSlackChannelConfigurationsRequestDescribeSlackChannelConfigurationsPaginateTypeDef(
    TypedDict
):
    ChatConfigurationArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSlackUserIdentitiesRequestDescribeSlackUserIdentitiesPaginateTypeDef(TypedDict):
    ChatConfigurationArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSlackWorkspacesRequestDescribeSlackWorkspacesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMicrosoftTeamsConfiguredTeamsRequestListMicrosoftTeamsConfiguredTeamsPaginateTypeDef(
    TypedDict
):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMicrosoftTeamsUserIdentitiesRequestListMicrosoftTeamsUserIdentitiesPaginateTypeDef(
    TypedDict
):
    ChatConfigurationArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTeamsChannelConfigurationsRequestListMicrosoftTeamsChannelConfigurationsPaginateTypeDef(
    TypedDict
):
    TeamId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSlackUserIdentitiesResultTypeDef(TypedDict):
    SlackUserIdentities: List[SlackUserIdentityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeSlackWorkspacesResultTypeDef(TypedDict):
    SlackWorkspaces: List[SlackWorkspaceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListMicrosoftTeamsUserIdentitiesResultTypeDef(TypedDict):
    TeamsUserIdentities: List[TeamsUserIdentityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateChimeWebhookConfigurationResultTypeDef(TypedDict):
    WebhookConfiguration: ChimeWebhookConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeChimeWebhookConfigurationsResultTypeDef(TypedDict):
    WebhookConfigurations: List[ChimeWebhookConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateChimeWebhookConfigurationResultTypeDef(TypedDict):
    WebhookConfiguration: ChimeWebhookConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSlackChannelConfigurationResultTypeDef(TypedDict):
    ChannelConfiguration: SlackChannelConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSlackChannelConfigurationsResultTypeDef(TypedDict):
    SlackChannelConfigurations: List[SlackChannelConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateSlackChannelConfigurationResultTypeDef(TypedDict):
    ChannelConfiguration: SlackChannelConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTeamsChannelConfigurationResultTypeDef(TypedDict):
    ChannelConfiguration: TeamsChannelConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetTeamsChannelConfigurationResultTypeDef(TypedDict):
    ChannelConfiguration: TeamsChannelConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListTeamsChannelConfigurationsResultTypeDef(TypedDict):
    TeamChannelConfigurations: List[TeamsChannelConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateTeamsChannelConfigurationResultTypeDef(TypedDict):
    ChannelConfiguration: TeamsChannelConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
