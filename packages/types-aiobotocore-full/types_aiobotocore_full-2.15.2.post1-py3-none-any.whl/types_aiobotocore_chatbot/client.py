"""
Type annotations for chatbot service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chatbot.client import ChatbotClient

    session = get_session()
    async with session.create_client("chatbot") as client:
        client: ChatbotClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    DescribeChimeWebhookConfigurationsPaginator,
    DescribeSlackChannelConfigurationsPaginator,
    DescribeSlackUserIdentitiesPaginator,
    DescribeSlackWorkspacesPaginator,
    ListMicrosoftTeamsChannelConfigurationsPaginator,
    ListMicrosoftTeamsConfiguredTeamsPaginator,
    ListMicrosoftTeamsUserIdentitiesPaginator,
)
from .type_defs import (
    CreateChimeWebhookConfigurationRequestRequestTypeDef,
    CreateChimeWebhookConfigurationResultTypeDef,
    CreateSlackChannelConfigurationRequestRequestTypeDef,
    CreateSlackChannelConfigurationResultTypeDef,
    CreateTeamsChannelConfigurationRequestRequestTypeDef,
    CreateTeamsChannelConfigurationResultTypeDef,
    DeleteChimeWebhookConfigurationRequestRequestTypeDef,
    DeleteMicrosoftTeamsUserIdentityRequestRequestTypeDef,
    DeleteSlackChannelConfigurationRequestRequestTypeDef,
    DeleteSlackUserIdentityRequestRequestTypeDef,
    DeleteSlackWorkspaceAuthorizationRequestRequestTypeDef,
    DeleteTeamsChannelConfigurationRequestRequestTypeDef,
    DeleteTeamsConfiguredTeamRequestRequestTypeDef,
    DescribeChimeWebhookConfigurationsRequestRequestTypeDef,
    DescribeChimeWebhookConfigurationsResultTypeDef,
    DescribeSlackChannelConfigurationsRequestRequestTypeDef,
    DescribeSlackChannelConfigurationsResultTypeDef,
    DescribeSlackUserIdentitiesRequestRequestTypeDef,
    DescribeSlackUserIdentitiesResultTypeDef,
    DescribeSlackWorkspacesRequestRequestTypeDef,
    DescribeSlackWorkspacesResultTypeDef,
    GetAccountPreferencesResultTypeDef,
    GetTeamsChannelConfigurationRequestRequestTypeDef,
    GetTeamsChannelConfigurationResultTypeDef,
    ListMicrosoftTeamsConfiguredTeamsRequestRequestTypeDef,
    ListMicrosoftTeamsConfiguredTeamsResultTypeDef,
    ListMicrosoftTeamsUserIdentitiesRequestRequestTypeDef,
    ListMicrosoftTeamsUserIdentitiesResultTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTeamsChannelConfigurationsRequestRequestTypeDef,
    ListTeamsChannelConfigurationsResultTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAccountPreferencesRequestRequestTypeDef,
    UpdateAccountPreferencesResultTypeDef,
    UpdateChimeWebhookConfigurationRequestRequestTypeDef,
    UpdateChimeWebhookConfigurationResultTypeDef,
    UpdateSlackChannelConfigurationRequestRequestTypeDef,
    UpdateSlackChannelConfigurationResultTypeDef,
    UpdateTeamsChannelConfigurationRequestRequestTypeDef,
    UpdateTeamsChannelConfigurationResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ChatbotClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    CreateChimeWebhookConfigurationException: Type[BotocoreClientError]
    CreateSlackChannelConfigurationException: Type[BotocoreClientError]
    CreateTeamsChannelConfigurationException: Type[BotocoreClientError]
    DeleteChimeWebhookConfigurationException: Type[BotocoreClientError]
    DeleteMicrosoftTeamsUserIdentityException: Type[BotocoreClientError]
    DeleteSlackChannelConfigurationException: Type[BotocoreClientError]
    DeleteSlackUserIdentityException: Type[BotocoreClientError]
    DeleteSlackWorkspaceAuthorizationFault: Type[BotocoreClientError]
    DeleteTeamsChannelConfigurationException: Type[BotocoreClientError]
    DeleteTeamsConfiguredTeamException: Type[BotocoreClientError]
    DescribeChimeWebhookConfigurationsException: Type[BotocoreClientError]
    DescribeSlackChannelConfigurationsException: Type[BotocoreClientError]
    DescribeSlackUserIdentitiesException: Type[BotocoreClientError]
    DescribeSlackWorkspacesException: Type[BotocoreClientError]
    GetAccountPreferencesException: Type[BotocoreClientError]
    GetTeamsChannelConfigurationException: Type[BotocoreClientError]
    InternalServiceError: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ListMicrosoftTeamsConfiguredTeamsException: Type[BotocoreClientError]
    ListMicrosoftTeamsUserIdentitiesException: Type[BotocoreClientError]
    ListTeamsChannelConfigurationsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UpdateAccountPreferencesException: Type[BotocoreClientError]
    UpdateChimeWebhookConfigurationException: Type[BotocoreClientError]
    UpdateSlackChannelConfigurationException: Type[BotocoreClientError]
    UpdateTeamsChannelConfigurationException: Type[BotocoreClientError]


class ChatbotClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChatbotClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#close)
        """

    async def create_chime_webhook_configuration(
        self, **kwargs: Unpack[CreateChimeWebhookConfigurationRequestRequestTypeDef]
    ) -> CreateChimeWebhookConfigurationResultTypeDef:
        """
        Creates an AWS Chatbot configuration for Amazon Chime.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/create_chime_webhook_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#create_chime_webhook_configuration)
        """

    async def create_microsoft_teams_channel_configuration(
        self, **kwargs: Unpack[CreateTeamsChannelConfigurationRequestRequestTypeDef]
    ) -> CreateTeamsChannelConfigurationResultTypeDef:
        """
        Creates an AWS Chatbot configuration for Microsoft Teams.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/create_microsoft_teams_channel_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#create_microsoft_teams_channel_configuration)
        """

    async def create_slack_channel_configuration(
        self, **kwargs: Unpack[CreateSlackChannelConfigurationRequestRequestTypeDef]
    ) -> CreateSlackChannelConfigurationResultTypeDef:
        """
        Creates an AWS Chatbot confugration for Slack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/create_slack_channel_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#create_slack_channel_configuration)
        """

    async def delete_chime_webhook_configuration(
        self, **kwargs: Unpack[DeleteChimeWebhookConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Amazon Chime webhook configuration for AWS Chatbot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/delete_chime_webhook_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#delete_chime_webhook_configuration)
        """

    async def delete_microsoft_teams_channel_configuration(
        self, **kwargs: Unpack[DeleteTeamsChannelConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Microsoft Teams channel configuration for AWS Chatbot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/delete_microsoft_teams_channel_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#delete_microsoft_teams_channel_configuration)
        """

    async def delete_microsoft_teams_configured_team(
        self, **kwargs: Unpack[DeleteTeamsConfiguredTeamRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the Microsoft Teams team authorization allowing for channels to be
        configured in that Microsoft Teams team.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/delete_microsoft_teams_configured_team.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#delete_microsoft_teams_configured_team)
        """

    async def delete_microsoft_teams_user_identity(
        self, **kwargs: Unpack[DeleteMicrosoftTeamsUserIdentityRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Identifes a user level permission for a channel configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/delete_microsoft_teams_user_identity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#delete_microsoft_teams_user_identity)
        """

    async def delete_slack_channel_configuration(
        self, **kwargs: Unpack[DeleteSlackChannelConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Slack channel configuration for AWS Chatbot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/delete_slack_channel_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#delete_slack_channel_configuration)
        """

    async def delete_slack_user_identity(
        self, **kwargs: Unpack[DeleteSlackUserIdentityRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a user level permission for a Slack channel configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/delete_slack_user_identity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#delete_slack_user_identity)
        """

    async def delete_slack_workspace_authorization(
        self, **kwargs: Unpack[DeleteSlackWorkspaceAuthorizationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the Slack workspace authorization that allows channels to be configured
        in that workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/delete_slack_workspace_authorization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#delete_slack_workspace_authorization)
        """

    async def describe_chime_webhook_configurations(
        self, **kwargs: Unpack[DescribeChimeWebhookConfigurationsRequestRequestTypeDef]
    ) -> DescribeChimeWebhookConfigurationsResultTypeDef:
        """
        Lists Amazon Chime webhook configurations optionally filtered by
        ChatConfigurationArn.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/describe_chime_webhook_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#describe_chime_webhook_configurations)
        """

    async def describe_slack_channel_configurations(
        self, **kwargs: Unpack[DescribeSlackChannelConfigurationsRequestRequestTypeDef]
    ) -> DescribeSlackChannelConfigurationsResultTypeDef:
        """
        Lists Slack channel configurations optionally filtered by ChatConfigurationArn.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/describe_slack_channel_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#describe_slack_channel_configurations)
        """

    async def describe_slack_user_identities(
        self, **kwargs: Unpack[DescribeSlackUserIdentitiesRequestRequestTypeDef]
    ) -> DescribeSlackUserIdentitiesResultTypeDef:
        """
        Lists all Slack user identities with a mapped role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/describe_slack_user_identities.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#describe_slack_user_identities)
        """

    async def describe_slack_workspaces(
        self, **kwargs: Unpack[DescribeSlackWorkspacesRequestRequestTypeDef]
    ) -> DescribeSlackWorkspacesResultTypeDef:
        """
        List all authorized Slack workspaces connected to the AWS Account onboarded
        with AWS Chatbot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/describe_slack_workspaces.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#describe_slack_workspaces)
        """

    async def get_account_preferences(self) -> GetAccountPreferencesResultTypeDef:
        """
        Returns AWS Chatbot account preferences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/get_account_preferences.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#get_account_preferences)
        """

    async def get_microsoft_teams_channel_configuration(
        self, **kwargs: Unpack[GetTeamsChannelConfigurationRequestRequestTypeDef]
    ) -> GetTeamsChannelConfigurationResultTypeDef:
        """
        Returns a Microsoft Teams channel configuration in an AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/get_microsoft_teams_channel_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#get_microsoft_teams_channel_configuration)
        """

    async def list_microsoft_teams_channel_configurations(
        self, **kwargs: Unpack[ListTeamsChannelConfigurationsRequestRequestTypeDef]
    ) -> ListTeamsChannelConfigurationsResultTypeDef:
        """
        Lists all AWS Chatbot Microsoft Teams channel configurations in an AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/list_microsoft_teams_channel_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#list_microsoft_teams_channel_configurations)
        """

    async def list_microsoft_teams_configured_teams(
        self, **kwargs: Unpack[ListMicrosoftTeamsConfiguredTeamsRequestRequestTypeDef]
    ) -> ListMicrosoftTeamsConfiguredTeamsResultTypeDef:
        """
        Lists all authorized Microsoft Teams for an AWS Account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/list_microsoft_teams_configured_teams.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#list_microsoft_teams_configured_teams)
        """

    async def list_microsoft_teams_user_identities(
        self, **kwargs: Unpack[ListMicrosoftTeamsUserIdentitiesRequestRequestTypeDef]
    ) -> ListMicrosoftTeamsUserIdentitiesResultTypeDef:
        """
        A list all Microsoft Teams user identities with a mapped role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/list_microsoft_teams_user_identities.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#list_microsoft_teams_user_identities)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all of the tags associated with the Amazon Resource Name (ARN) that you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#list_tags_for_resource)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Attaches a key-value pair to a resource, as identified by its Amazon Resource
        Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Detaches a key-value pair from a resource, as identified by its Amazon Resource
        Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#untag_resource)
        """

    async def update_account_preferences(
        self, **kwargs: Unpack[UpdateAccountPreferencesRequestRequestTypeDef]
    ) -> UpdateAccountPreferencesResultTypeDef:
        """
        Updates AWS Chatbot account preferences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/update_account_preferences.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#update_account_preferences)
        """

    async def update_chime_webhook_configuration(
        self, **kwargs: Unpack[UpdateChimeWebhookConfigurationRequestRequestTypeDef]
    ) -> UpdateChimeWebhookConfigurationResultTypeDef:
        """
        Updates a Amazon Chime webhook configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/update_chime_webhook_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#update_chime_webhook_configuration)
        """

    async def update_microsoft_teams_channel_configuration(
        self, **kwargs: Unpack[UpdateTeamsChannelConfigurationRequestRequestTypeDef]
    ) -> UpdateTeamsChannelConfigurationResultTypeDef:
        """
        Updates an Microsoft Teams channel configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/update_microsoft_teams_channel_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#update_microsoft_teams_channel_configuration)
        """

    async def update_slack_channel_configuration(
        self, **kwargs: Unpack[UpdateSlackChannelConfigurationRequestRequestTypeDef]
    ) -> UpdateSlackChannelConfigurationResultTypeDef:
        """
        Updates a Slack channel configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/update_slack_channel_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#update_slack_channel_configuration)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_chime_webhook_configurations"]
    ) -> DescribeChimeWebhookConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_slack_channel_configurations"]
    ) -> DescribeSlackChannelConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_slack_user_identities"]
    ) -> DescribeSlackUserIdentitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_slack_workspaces"]
    ) -> DescribeSlackWorkspacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_microsoft_teams_channel_configurations"]
    ) -> ListMicrosoftTeamsChannelConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_microsoft_teams_configured_teams"]
    ) -> ListMicrosoftTeamsConfiguredTeamsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_microsoft_teams_user_identities"]
    ) -> ListMicrosoftTeamsUserIdentitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/#get_paginator)
        """

    async def __aenter__(self) -> "ChatbotClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot.html#Chatbot.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/client/)
        """
