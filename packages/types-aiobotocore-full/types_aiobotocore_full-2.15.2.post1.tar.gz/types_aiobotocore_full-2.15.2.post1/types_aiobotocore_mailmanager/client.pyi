"""
Type annotations for mailmanager service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mailmanager.client import MailManagerClient

    session = get_session()
    async with session.create_client("mailmanager") as client:
        client: MailManagerClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListAddonInstancesPaginator,
    ListAddonSubscriptionsPaginator,
    ListArchiveExportsPaginator,
    ListArchiveSearchesPaginator,
    ListArchivesPaginator,
    ListIngressPointsPaginator,
    ListRelaysPaginator,
    ListRuleSetsPaginator,
    ListTrafficPoliciesPaginator,
)
from .type_defs import (
    CreateAddonInstanceRequestRequestTypeDef,
    CreateAddonInstanceResponseTypeDef,
    CreateAddonSubscriptionRequestRequestTypeDef,
    CreateAddonSubscriptionResponseTypeDef,
    CreateArchiveRequestRequestTypeDef,
    CreateArchiveResponseTypeDef,
    CreateIngressPointRequestRequestTypeDef,
    CreateIngressPointResponseTypeDef,
    CreateRelayRequestRequestTypeDef,
    CreateRelayResponseTypeDef,
    CreateRuleSetRequestRequestTypeDef,
    CreateRuleSetResponseTypeDef,
    CreateTrafficPolicyRequestRequestTypeDef,
    CreateTrafficPolicyResponseTypeDef,
    DeleteAddonInstanceRequestRequestTypeDef,
    DeleteAddonSubscriptionRequestRequestTypeDef,
    DeleteArchiveRequestRequestTypeDef,
    DeleteIngressPointRequestRequestTypeDef,
    DeleteRelayRequestRequestTypeDef,
    DeleteRuleSetRequestRequestTypeDef,
    DeleteTrafficPolicyRequestRequestTypeDef,
    GetAddonInstanceRequestRequestTypeDef,
    GetAddonInstanceResponseTypeDef,
    GetAddonSubscriptionRequestRequestTypeDef,
    GetAddonSubscriptionResponseTypeDef,
    GetArchiveExportRequestRequestTypeDef,
    GetArchiveExportResponseTypeDef,
    GetArchiveMessageContentRequestRequestTypeDef,
    GetArchiveMessageContentResponseTypeDef,
    GetArchiveMessageRequestRequestTypeDef,
    GetArchiveMessageResponseTypeDef,
    GetArchiveRequestRequestTypeDef,
    GetArchiveResponseTypeDef,
    GetArchiveSearchRequestRequestTypeDef,
    GetArchiveSearchResponseTypeDef,
    GetArchiveSearchResultsRequestRequestTypeDef,
    GetArchiveSearchResultsResponseTypeDef,
    GetIngressPointRequestRequestTypeDef,
    GetIngressPointResponseTypeDef,
    GetRelayRequestRequestTypeDef,
    GetRelayResponseTypeDef,
    GetRuleSetRequestRequestTypeDef,
    GetRuleSetResponseTypeDef,
    GetTrafficPolicyRequestRequestTypeDef,
    GetTrafficPolicyResponseTypeDef,
    ListAddonInstancesRequestRequestTypeDef,
    ListAddonInstancesResponseTypeDef,
    ListAddonSubscriptionsRequestRequestTypeDef,
    ListAddonSubscriptionsResponseTypeDef,
    ListArchiveExportsRequestRequestTypeDef,
    ListArchiveExportsResponseTypeDef,
    ListArchiveSearchesRequestRequestTypeDef,
    ListArchiveSearchesResponseTypeDef,
    ListArchivesRequestRequestTypeDef,
    ListArchivesResponseTypeDef,
    ListIngressPointsRequestRequestTypeDef,
    ListIngressPointsResponseTypeDef,
    ListRelaysRequestRequestTypeDef,
    ListRelaysResponseTypeDef,
    ListRuleSetsRequestRequestTypeDef,
    ListRuleSetsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTrafficPoliciesRequestRequestTypeDef,
    ListTrafficPoliciesResponseTypeDef,
    StartArchiveExportRequestRequestTypeDef,
    StartArchiveExportResponseTypeDef,
    StartArchiveSearchRequestRequestTypeDef,
    StartArchiveSearchResponseTypeDef,
    StopArchiveExportRequestRequestTypeDef,
    StopArchiveSearchRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateArchiveRequestRequestTypeDef,
    UpdateIngressPointRequestRequestTypeDef,
    UpdateRelayRequestRequestTypeDef,
    UpdateRuleSetRequestRequestTypeDef,
    UpdateTrafficPolicyRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("MailManagerClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class MailManagerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager.html#MailManager.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MailManagerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager.html#MailManager.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#close)
        """

    async def create_addon_instance(
        self, **kwargs: Unpack[CreateAddonInstanceRequestRequestTypeDef]
    ) -> CreateAddonInstanceResponseTypeDef:
        """
        Creates an Add On instance for the subscription indicated in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_addon_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#create_addon_instance)
        """

    async def create_addon_subscription(
        self, **kwargs: Unpack[CreateAddonSubscriptionRequestRequestTypeDef]
    ) -> CreateAddonSubscriptionResponseTypeDef:
        """
        Creates a subscription for an Add On representing the acceptance of its terms
        of use and additional pricing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_addon_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#create_addon_subscription)
        """

    async def create_archive(
        self, **kwargs: Unpack[CreateArchiveRequestRequestTypeDef]
    ) -> CreateArchiveResponseTypeDef:
        """
        Creates a new email archive resource for storing and retaining emails.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_archive.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#create_archive)
        """

    async def create_ingress_point(
        self, **kwargs: Unpack[CreateIngressPointRequestRequestTypeDef]
    ) -> CreateIngressPointResponseTypeDef:
        """
        Provision a new ingress endpoint resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_ingress_point.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#create_ingress_point)
        """

    async def create_relay(
        self, **kwargs: Unpack[CreateRelayRequestRequestTypeDef]
    ) -> CreateRelayResponseTypeDef:
        """
        Creates a relay resource which can be used in rules to relay incoming emails to
        defined relay destinations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_relay.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#create_relay)
        """

    async def create_rule_set(
        self, **kwargs: Unpack[CreateRuleSetRequestRequestTypeDef]
    ) -> CreateRuleSetResponseTypeDef:
        """
        Provision a new rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_rule_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#create_rule_set)
        """

    async def create_traffic_policy(
        self, **kwargs: Unpack[CreateTrafficPolicyRequestRequestTypeDef]
    ) -> CreateTrafficPolicyResponseTypeDef:
        """
        Provision a new traffic policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_traffic_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#create_traffic_policy)
        """

    async def delete_addon_instance(
        self, **kwargs: Unpack[DeleteAddonInstanceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Add On instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_addon_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#delete_addon_instance)
        """

    async def delete_addon_subscription(
        self, **kwargs: Unpack[DeleteAddonSubscriptionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Add On subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_addon_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#delete_addon_subscription)
        """

    async def delete_archive(
        self, **kwargs: Unpack[DeleteArchiveRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Initiates deletion of an email archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_archive.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#delete_archive)
        """

    async def delete_ingress_point(
        self, **kwargs: Unpack[DeleteIngressPointRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete an ingress endpoint resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_ingress_point.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#delete_ingress_point)
        """

    async def delete_relay(
        self, **kwargs: Unpack[DeleteRelayRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an existing relay resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_relay.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#delete_relay)
        """

    async def delete_rule_set(
        self, **kwargs: Unpack[DeleteRuleSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete a rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_rule_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#delete_rule_set)
        """

    async def delete_traffic_policy(
        self, **kwargs: Unpack[DeleteTrafficPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete a traffic policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_traffic_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#delete_traffic_policy)
        """

    async def get_addon_instance(
        self, **kwargs: Unpack[GetAddonInstanceRequestRequestTypeDef]
    ) -> GetAddonInstanceResponseTypeDef:
        """
        Gets detailed information about an Add On instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_addon_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_addon_instance)
        """

    async def get_addon_subscription(
        self, **kwargs: Unpack[GetAddonSubscriptionRequestRequestTypeDef]
    ) -> GetAddonSubscriptionResponseTypeDef:
        """
        Gets detailed information about an Add On subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_addon_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_addon_subscription)
        """

    async def get_archive(
        self, **kwargs: Unpack[GetArchiveRequestRequestTypeDef]
    ) -> GetArchiveResponseTypeDef:
        """
        Retrieves the full details and current state of a specified email archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_archive)
        """

    async def get_archive_export(
        self, **kwargs: Unpack[GetArchiveExportRequestRequestTypeDef]
    ) -> GetArchiveExportResponseTypeDef:
        """
        Retrieves the details and current status of a specific email archive export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive_export.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_archive_export)
        """

    async def get_archive_message(
        self, **kwargs: Unpack[GetArchiveMessageRequestRequestTypeDef]
    ) -> GetArchiveMessageResponseTypeDef:
        """
        Returns a pre-signed URL that provides temporary download access to the
        specific email message stored in the archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive_message.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_archive_message)
        """

    async def get_archive_message_content(
        self, **kwargs: Unpack[GetArchiveMessageContentRequestRequestTypeDef]
    ) -> GetArchiveMessageContentResponseTypeDef:
        """
        Returns the textual content of a specific email message stored in the archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive_message_content.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_archive_message_content)
        """

    async def get_archive_search(
        self, **kwargs: Unpack[GetArchiveSearchRequestRequestTypeDef]
    ) -> GetArchiveSearchResponseTypeDef:
        """
        Retrieves the details and current status of a specific email archive search job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive_search.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_archive_search)
        """

    async def get_archive_search_results(
        self, **kwargs: Unpack[GetArchiveSearchResultsRequestRequestTypeDef]
    ) -> GetArchiveSearchResultsResponseTypeDef:
        """
        Returns the results of a completed email archive search job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive_search_results.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_archive_search_results)
        """

    async def get_ingress_point(
        self, **kwargs: Unpack[GetIngressPointRequestRequestTypeDef]
    ) -> GetIngressPointResponseTypeDef:
        """
        Fetch ingress endpoint resource attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_ingress_point.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_ingress_point)
        """

    async def get_relay(
        self, **kwargs: Unpack[GetRelayRequestRequestTypeDef]
    ) -> GetRelayResponseTypeDef:
        """
        Fetch the relay resource and it's attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_relay.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_relay)
        """

    async def get_rule_set(
        self, **kwargs: Unpack[GetRuleSetRequestRequestTypeDef]
    ) -> GetRuleSetResponseTypeDef:
        """
        Fetch attributes of a rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_rule_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_rule_set)
        """

    async def get_traffic_policy(
        self, **kwargs: Unpack[GetTrafficPolicyRequestRequestTypeDef]
    ) -> GetTrafficPolicyResponseTypeDef:
        """
        Fetch attributes of a traffic policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_traffic_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_traffic_policy)
        """

    async def list_addon_instances(
        self, **kwargs: Unpack[ListAddonInstancesRequestRequestTypeDef]
    ) -> ListAddonInstancesResponseTypeDef:
        """
        Lists all Add On instances in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_addon_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_addon_instances)
        """

    async def list_addon_subscriptions(
        self, **kwargs: Unpack[ListAddonSubscriptionsRequestRequestTypeDef]
    ) -> ListAddonSubscriptionsResponseTypeDef:
        """
        Lists all Add On subscriptions in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_addon_subscriptions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_addon_subscriptions)
        """

    async def list_archive_exports(
        self, **kwargs: Unpack[ListArchiveExportsRequestRequestTypeDef]
    ) -> ListArchiveExportsResponseTypeDef:
        """
        Returns a list of email archive export jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_archive_exports.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_archive_exports)
        """

    async def list_archive_searches(
        self, **kwargs: Unpack[ListArchiveSearchesRequestRequestTypeDef]
    ) -> ListArchiveSearchesResponseTypeDef:
        """
        Returns a list of email archive search jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_archive_searches.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_archive_searches)
        """

    async def list_archives(
        self, **kwargs: Unpack[ListArchivesRequestRequestTypeDef]
    ) -> ListArchivesResponseTypeDef:
        """
        Returns a list of all email archives in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_archives.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_archives)
        """

    async def list_ingress_points(
        self, **kwargs: Unpack[ListIngressPointsRequestRequestTypeDef]
    ) -> ListIngressPointsResponseTypeDef:
        """
        List all ingress endpoint resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_ingress_points.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_ingress_points)
        """

    async def list_relays(
        self, **kwargs: Unpack[ListRelaysRequestRequestTypeDef]
    ) -> ListRelaysResponseTypeDef:
        """
        Lists all the existing relay resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_relays.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_relays)
        """

    async def list_rule_sets(
        self, **kwargs: Unpack[ListRuleSetsRequestRequestTypeDef]
    ) -> ListRuleSetsResponseTypeDef:
        """
        List rule sets for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_rule_sets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_rule_sets)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the list of tags (keys and values) assigned to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_tags_for_resource)
        """

    async def list_traffic_policies(
        self, **kwargs: Unpack[ListTrafficPoliciesRequestRequestTypeDef]
    ) -> ListTrafficPoliciesResponseTypeDef:
        """
        List traffic policy resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_traffic_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_traffic_policies)
        """

    async def start_archive_export(
        self, **kwargs: Unpack[StartArchiveExportRequestRequestTypeDef]
    ) -> StartArchiveExportResponseTypeDef:
        """
        Initiates an export of emails from the specified archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/start_archive_export.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#start_archive_export)
        """

    async def start_archive_search(
        self, **kwargs: Unpack[StartArchiveSearchRequestRequestTypeDef]
    ) -> StartArchiveSearchResponseTypeDef:
        """
        Initiates a search across emails in the specified archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/start_archive_search.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#start_archive_search)
        """

    async def stop_archive_export(
        self, **kwargs: Unpack[StopArchiveExportRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops an in-progress export of emails from an archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/stop_archive_export.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#stop_archive_export)
        """

    async def stop_archive_search(
        self, **kwargs: Unpack[StopArchiveSearchRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops an in-progress archive search job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/stop_archive_search.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#stop_archive_search)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds one or more tags (keys and values) to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove one or more tags (keys and values) from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#untag_resource)
        """

    async def update_archive(
        self, **kwargs: Unpack[UpdateArchiveRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the attributes of an existing email archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/update_archive.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#update_archive)
        """

    async def update_ingress_point(
        self, **kwargs: Unpack[UpdateIngressPointRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update attributes of a provisioned ingress endpoint resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/update_ingress_point.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#update_ingress_point)
        """

    async def update_relay(
        self, **kwargs: Unpack[UpdateRelayRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the attributes of an existing relay resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/update_relay.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#update_relay)
        """

    async def update_rule_set(
        self, **kwargs: Unpack[UpdateRuleSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update attributes of an already provisioned rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/update_rule_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#update_rule_set)
        """

    async def update_traffic_policy(
        self, **kwargs: Unpack[UpdateTrafficPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update attributes of an already provisioned traffic policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/update_traffic_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#update_traffic_policy)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_addon_instances"]
    ) -> ListAddonInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_addon_subscriptions"]
    ) -> ListAddonSubscriptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_archive_exports"]
    ) -> ListArchiveExportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_archive_searches"]
    ) -> ListArchiveSearchesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_archives"]) -> ListArchivesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ingress_points"]
    ) -> ListIngressPointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_relays"]) -> ListRelaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_rule_sets"]) -> ListRuleSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_traffic_policies"]
    ) -> ListTrafficPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    async def __aenter__(self) -> "MailManagerClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager.html#MailManager.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager.html#MailManager.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/)
        """
