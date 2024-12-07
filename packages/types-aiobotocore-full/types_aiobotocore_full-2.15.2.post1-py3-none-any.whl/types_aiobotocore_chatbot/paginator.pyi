"""
Type annotations for chatbot service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_chatbot.client import ChatbotClient
    from types_aiobotocore_chatbot.paginator import (
        DescribeChimeWebhookConfigurationsPaginator,
        DescribeSlackChannelConfigurationsPaginator,
        DescribeSlackUserIdentitiesPaginator,
        DescribeSlackWorkspacesPaginator,
        ListMicrosoftTeamsChannelConfigurationsPaginator,
        ListMicrosoftTeamsConfiguredTeamsPaginator,
        ListMicrosoftTeamsUserIdentitiesPaginator,
    )

    session = get_session()
    with session.create_client("chatbot") as client:
        client: ChatbotClient

        describe_chime_webhook_configurations_paginator: DescribeChimeWebhookConfigurationsPaginator = client.get_paginator("describe_chime_webhook_configurations")
        describe_slack_channel_configurations_paginator: DescribeSlackChannelConfigurationsPaginator = client.get_paginator("describe_slack_channel_configurations")
        describe_slack_user_identities_paginator: DescribeSlackUserIdentitiesPaginator = client.get_paginator("describe_slack_user_identities")
        describe_slack_workspaces_paginator: DescribeSlackWorkspacesPaginator = client.get_paginator("describe_slack_workspaces")
        list_microsoft_teams_channel_configurations_paginator: ListMicrosoftTeamsChannelConfigurationsPaginator = client.get_paginator("list_microsoft_teams_channel_configurations")
        list_microsoft_teams_configured_teams_paginator: ListMicrosoftTeamsConfiguredTeamsPaginator = client.get_paginator("list_microsoft_teams_configured_teams")
        list_microsoft_teams_user_identities_paginator: ListMicrosoftTeamsUserIdentitiesPaginator = client.get_paginator("list_microsoft_teams_user_identities")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeChimeWebhookConfigurationsRequestDescribeChimeWebhookConfigurationsPaginateTypeDef,
    DescribeChimeWebhookConfigurationsResultTypeDef,
    DescribeSlackChannelConfigurationsRequestDescribeSlackChannelConfigurationsPaginateTypeDef,
    DescribeSlackChannelConfigurationsResultTypeDef,
    DescribeSlackUserIdentitiesRequestDescribeSlackUserIdentitiesPaginateTypeDef,
    DescribeSlackUserIdentitiesResultTypeDef,
    DescribeSlackWorkspacesRequestDescribeSlackWorkspacesPaginateTypeDef,
    DescribeSlackWorkspacesResultTypeDef,
    ListMicrosoftTeamsConfiguredTeamsRequestListMicrosoftTeamsConfiguredTeamsPaginateTypeDef,
    ListMicrosoftTeamsConfiguredTeamsResultTypeDef,
    ListMicrosoftTeamsUserIdentitiesRequestListMicrosoftTeamsUserIdentitiesPaginateTypeDef,
    ListMicrosoftTeamsUserIdentitiesResultTypeDef,
    ListTeamsChannelConfigurationsRequestListMicrosoftTeamsChannelConfigurationsPaginateTypeDef,
    ListTeamsChannelConfigurationsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeChimeWebhookConfigurationsPaginator",
    "DescribeSlackChannelConfigurationsPaginator",
    "DescribeSlackUserIdentitiesPaginator",
    "DescribeSlackWorkspacesPaginator",
    "ListMicrosoftTeamsChannelConfigurationsPaginator",
    "ListMicrosoftTeamsConfiguredTeamsPaginator",
    "ListMicrosoftTeamsUserIdentitiesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeChimeWebhookConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeChimeWebhookConfigurations.html#Chatbot.Paginator.DescribeChimeWebhookConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#describechimewebhookconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeChimeWebhookConfigurationsRequestDescribeChimeWebhookConfigurationsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeChimeWebhookConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeChimeWebhookConfigurations.html#Chatbot.Paginator.DescribeChimeWebhookConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#describechimewebhookconfigurationspaginator)
        """

class DescribeSlackChannelConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackChannelConfigurations.html#Chatbot.Paginator.DescribeSlackChannelConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#describeslackchannelconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeSlackChannelConfigurationsRequestDescribeSlackChannelConfigurationsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeSlackChannelConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackChannelConfigurations.html#Chatbot.Paginator.DescribeSlackChannelConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#describeslackchannelconfigurationspaginator)
        """

class DescribeSlackUserIdentitiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackUserIdentities.html#Chatbot.Paginator.DescribeSlackUserIdentities)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#describeslackuseridentitiespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeSlackUserIdentitiesRequestDescribeSlackUserIdentitiesPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeSlackUserIdentitiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackUserIdentities.html#Chatbot.Paginator.DescribeSlackUserIdentities.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#describeslackuseridentitiespaginator)
        """

class DescribeSlackWorkspacesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackWorkspaces.html#Chatbot.Paginator.DescribeSlackWorkspaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#describeslackworkspacespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeSlackWorkspacesRequestDescribeSlackWorkspacesPaginateTypeDef]
    ) -> AsyncIterator[DescribeSlackWorkspacesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackWorkspaces.html#Chatbot.Paginator.DescribeSlackWorkspaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#describeslackworkspacespaginator)
        """

class ListMicrosoftTeamsChannelConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsChannelConfigurations.html#Chatbot.Paginator.ListMicrosoftTeamsChannelConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#listmicrosoftteamschannelconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListTeamsChannelConfigurationsRequestListMicrosoftTeamsChannelConfigurationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListTeamsChannelConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsChannelConfigurations.html#Chatbot.Paginator.ListMicrosoftTeamsChannelConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#listmicrosoftteamschannelconfigurationspaginator)
        """

class ListMicrosoftTeamsConfiguredTeamsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsConfiguredTeams.html#Chatbot.Paginator.ListMicrosoftTeamsConfiguredTeams)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#listmicrosoftteamsconfiguredteamspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListMicrosoftTeamsConfiguredTeamsRequestListMicrosoftTeamsConfiguredTeamsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListMicrosoftTeamsConfiguredTeamsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsConfiguredTeams.html#Chatbot.Paginator.ListMicrosoftTeamsConfiguredTeams.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#listmicrosoftteamsconfiguredteamspaginator)
        """

class ListMicrosoftTeamsUserIdentitiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsUserIdentities.html#Chatbot.Paginator.ListMicrosoftTeamsUserIdentities)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#listmicrosoftteamsuseridentitiespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListMicrosoftTeamsUserIdentitiesRequestListMicrosoftTeamsUserIdentitiesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListMicrosoftTeamsUserIdentitiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsUserIdentities.html#Chatbot.Paginator.ListMicrosoftTeamsUserIdentities.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#listmicrosoftteamsuseridentitiespaginator)
        """
