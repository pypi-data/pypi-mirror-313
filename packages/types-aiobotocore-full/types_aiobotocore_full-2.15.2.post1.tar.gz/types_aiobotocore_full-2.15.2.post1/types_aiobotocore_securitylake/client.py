"""
Type annotations for securitylake service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_securitylake.client import SecurityLakeClient

    session = get_session()
    async with session.create_client("securitylake") as client:
        client: SecurityLakeClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    GetDataLakeSourcesPaginator,
    ListDataLakeExceptionsPaginator,
    ListLogSourcesPaginator,
    ListSubscribersPaginator,
)
from .type_defs import (
    CreateAwsLogSourceRequestRequestTypeDef,
    CreateAwsLogSourceResponseTypeDef,
    CreateCustomLogSourceRequestRequestTypeDef,
    CreateCustomLogSourceResponseTypeDef,
    CreateDataLakeExceptionSubscriptionRequestRequestTypeDef,
    CreateDataLakeOrganizationConfigurationRequestRequestTypeDef,
    CreateDataLakeRequestRequestTypeDef,
    CreateDataLakeResponseTypeDef,
    CreateSubscriberNotificationRequestRequestTypeDef,
    CreateSubscriberNotificationResponseTypeDef,
    CreateSubscriberRequestRequestTypeDef,
    CreateSubscriberResponseTypeDef,
    DeleteAwsLogSourceRequestRequestTypeDef,
    DeleteAwsLogSourceResponseTypeDef,
    DeleteCustomLogSourceRequestRequestTypeDef,
    DeleteDataLakeOrganizationConfigurationRequestRequestTypeDef,
    DeleteDataLakeRequestRequestTypeDef,
    DeleteSubscriberNotificationRequestRequestTypeDef,
    DeleteSubscriberRequestRequestTypeDef,
    GetDataLakeExceptionSubscriptionResponseTypeDef,
    GetDataLakeOrganizationConfigurationResponseTypeDef,
    GetDataLakeSourcesRequestRequestTypeDef,
    GetDataLakeSourcesResponseTypeDef,
    GetSubscriberRequestRequestTypeDef,
    GetSubscriberResponseTypeDef,
    ListDataLakeExceptionsRequestRequestTypeDef,
    ListDataLakeExceptionsResponseTypeDef,
    ListDataLakesRequestRequestTypeDef,
    ListDataLakesResponseTypeDef,
    ListLogSourcesRequestRequestTypeDef,
    ListLogSourcesResponseTypeDef,
    ListSubscribersRequestRequestTypeDef,
    ListSubscribersResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RegisterDataLakeDelegatedAdministratorRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDataLakeExceptionSubscriptionRequestRequestTypeDef,
    UpdateDataLakeRequestRequestTypeDef,
    UpdateDataLakeResponseTypeDef,
    UpdateSubscriberNotificationRequestRequestTypeDef,
    UpdateSubscriberNotificationResponseTypeDef,
    UpdateSubscriberRequestRequestTypeDef,
    UpdateSubscriberResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("SecurityLakeClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class SecurityLakeClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SecurityLakeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#close)
        """

    async def create_aws_log_source(
        self, **kwargs: Unpack[CreateAwsLogSourceRequestRequestTypeDef]
    ) -> CreateAwsLogSourceResponseTypeDef:
        """
        Adds a natively supported Amazon Web Service as an Amazon Security Lake source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/create_aws_log_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#create_aws_log_source)
        """

    async def create_custom_log_source(
        self, **kwargs: Unpack[CreateCustomLogSourceRequestRequestTypeDef]
    ) -> CreateCustomLogSourceResponseTypeDef:
        """
        Adds a third-party custom source in Amazon Security Lake, from the Amazon Web
        Services Region where you want to create a custom source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/create_custom_log_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#create_custom_log_source)
        """

    async def create_data_lake(
        self, **kwargs: Unpack[CreateDataLakeRequestRequestTypeDef]
    ) -> CreateDataLakeResponseTypeDef:
        """
        Initializes an Amazon Security Lake instance with the provided (or default)
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/create_data_lake.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#create_data_lake)
        """

    async def create_data_lake_exception_subscription(
        self, **kwargs: Unpack[CreateDataLakeExceptionSubscriptionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates the specified notification subscription in Amazon Security Lake for the
        organization you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/create_data_lake_exception_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#create_data_lake_exception_subscription)
        """

    async def create_data_lake_organization_configuration(
        self, **kwargs: Unpack[CreateDataLakeOrganizationConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Automatically enables Amazon Security Lake for new member accounts in your
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/create_data_lake_organization_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#create_data_lake_organization_configuration)
        """

    async def create_subscriber(
        self, **kwargs: Unpack[CreateSubscriberRequestRequestTypeDef]
    ) -> CreateSubscriberResponseTypeDef:
        """
        Creates a subscription permission for accounts that are already enabled in
        Amazon Security Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/create_subscriber.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#create_subscriber)
        """

    async def create_subscriber_notification(
        self, **kwargs: Unpack[CreateSubscriberNotificationRequestRequestTypeDef]
    ) -> CreateSubscriberNotificationResponseTypeDef:
        """
        Notifies the subscriber when new data is written to the data lake for the
        sources that the subscriber consumes in Security Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/create_subscriber_notification.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#create_subscriber_notification)
        """

    async def delete_aws_log_source(
        self, **kwargs: Unpack[DeleteAwsLogSourceRequestRequestTypeDef]
    ) -> DeleteAwsLogSourceResponseTypeDef:
        """
        Removes a natively supported Amazon Web Service as an Amazon Security Lake
        source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/delete_aws_log_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#delete_aws_log_source)
        """

    async def delete_custom_log_source(
        self, **kwargs: Unpack[DeleteCustomLogSourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a custom log source from Amazon Security Lake, to stop sending data
        from the custom source to Security Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/delete_custom_log_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#delete_custom_log_source)
        """

    async def delete_data_lake(
        self, **kwargs: Unpack[DeleteDataLakeRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        When you disable Amazon Security Lake from your account, Security Lake is
        disabled in all Amazon Web Services Regions and it stops collecting data from
        your sources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/delete_data_lake.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#delete_data_lake)
        """

    async def delete_data_lake_exception_subscription(self) -> Dict[str, Any]:
        """
        Deletes the specified notification subscription in Amazon Security Lake for the
        organization you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/delete_data_lake_exception_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#delete_data_lake_exception_subscription)
        """

    async def delete_data_lake_organization_configuration(
        self, **kwargs: Unpack[DeleteDataLakeOrganizationConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Turns off automatic enablement of Amazon Security Lake for member accounts that
        are added to an organization in Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/delete_data_lake_organization_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#delete_data_lake_organization_configuration)
        """

    async def delete_subscriber(
        self, **kwargs: Unpack[DeleteSubscriberRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the subscription permission and all notification settings for accounts
        that are already enabled in Amazon Security Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/delete_subscriber.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#delete_subscriber)
        """

    async def delete_subscriber_notification(
        self, **kwargs: Unpack[DeleteSubscriberNotificationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified notification subscription in Amazon Security Lake for the
        organization you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/delete_subscriber_notification.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#delete_subscriber_notification)
        """

    async def deregister_data_lake_delegated_administrator(self) -> Dict[str, Any]:
        """
        Deletes the Amazon Security Lake delegated administrator account for the
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/deregister_data_lake_delegated_administrator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#deregister_data_lake_delegated_administrator)
        """

    async def get_data_lake_exception_subscription(
        self,
    ) -> GetDataLakeExceptionSubscriptionResponseTypeDef:
        """
        Retrieves the details of exception notifications for the account in Amazon
        Security Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/get_data_lake_exception_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#get_data_lake_exception_subscription)
        """

    async def get_data_lake_organization_configuration(
        self,
    ) -> GetDataLakeOrganizationConfigurationResponseTypeDef:
        """
        Retrieves the configuration that will be automatically set up for accounts
        added to the organization after the organization has onboarded to Amazon
        Security Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/get_data_lake_organization_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#get_data_lake_organization_configuration)
        """

    async def get_data_lake_sources(
        self, **kwargs: Unpack[GetDataLakeSourcesRequestRequestTypeDef]
    ) -> GetDataLakeSourcesResponseTypeDef:
        """
        Retrieves a snapshot of the current Region, including whether Amazon Security
        Lake is enabled for those accounts and which sources Security Lake is
        collecting data from.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/get_data_lake_sources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#get_data_lake_sources)
        """

    async def get_subscriber(
        self, **kwargs: Unpack[GetSubscriberRequestRequestTypeDef]
    ) -> GetSubscriberResponseTypeDef:
        """
        Retrieves the subscription information for the specified subscription ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/get_subscriber.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#get_subscriber)
        """

    async def list_data_lake_exceptions(
        self, **kwargs: Unpack[ListDataLakeExceptionsRequestRequestTypeDef]
    ) -> ListDataLakeExceptionsResponseTypeDef:
        """
        Lists the Amazon Security Lake exceptions that you can use to find the source
        of problems and fix them.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/list_data_lake_exceptions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#list_data_lake_exceptions)
        """

    async def list_data_lakes(
        self, **kwargs: Unpack[ListDataLakesRequestRequestTypeDef]
    ) -> ListDataLakesResponseTypeDef:
        """
        Retrieves the Amazon Security Lake configuration object for the specified
        Amazon Web Services Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/list_data_lakes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#list_data_lakes)
        """

    async def list_log_sources(
        self, **kwargs: Unpack[ListLogSourcesRequestRequestTypeDef]
    ) -> ListLogSourcesResponseTypeDef:
        """
        Retrieves the log sources in the current Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/list_log_sources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#list_log_sources)
        """

    async def list_subscribers(
        self, **kwargs: Unpack[ListSubscribersRequestRequestTypeDef]
    ) -> ListSubscribersResponseTypeDef:
        """
        List all subscribers for the specific Amazon Security Lake account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/list_subscribers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#list_subscribers)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the tags (keys and values) that are associated with an Amazon
        Security Lake resource: a subscriber, or the data lake configuration for your
        Amazon Web Services account in a particular Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#list_tags_for_resource)
        """

    async def register_data_lake_delegated_administrator(
        self, **kwargs: Unpack[RegisterDataLakeDelegatedAdministratorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Designates the Amazon Security Lake delegated administrator account for the
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/register_data_lake_delegated_administrator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#register_data_lake_delegated_administrator)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds or updates one or more tags that are associated with an Amazon Security
        Lake resource: a subscriber, or the data lake configuration for your Amazon Web
        Services account in a particular Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags (keys and values) from an Amazon Security Lake
        resource: a subscriber, or the data lake configuration for your Amazon Web
        Services account in a particular Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#untag_resource)
        """

    async def update_data_lake(
        self, **kwargs: Unpack[UpdateDataLakeRequestRequestTypeDef]
    ) -> UpdateDataLakeResponseTypeDef:
        """
        Specifies where to store your security data and for how long.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/update_data_lake.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#update_data_lake)
        """

    async def update_data_lake_exception_subscription(
        self, **kwargs: Unpack[UpdateDataLakeExceptionSubscriptionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the specified notification subscription in Amazon Security Lake for the
        organization you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/update_data_lake_exception_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#update_data_lake_exception_subscription)
        """

    async def update_subscriber(
        self, **kwargs: Unpack[UpdateSubscriberRequestRequestTypeDef]
    ) -> UpdateSubscriberResponseTypeDef:
        """
        Updates an existing subscription for the given Amazon Security Lake account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/update_subscriber.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#update_subscriber)
        """

    async def update_subscriber_notification(
        self, **kwargs: Unpack[UpdateSubscriberNotificationRequestRequestTypeDef]
    ) -> UpdateSubscriberNotificationResponseTypeDef:
        """
        Updates an existing notification method for the subscription (SQS or HTTPs
        endpoint) or switches the notification subscription endpoint for a subscriber.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/update_subscriber_notification.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#update_subscriber_notification)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_data_lake_sources"]
    ) -> GetDataLakeSourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_lake_exceptions"]
    ) -> ListDataLakeExceptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_log_sources"]) -> ListLogSourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_subscribers"]
    ) -> ListSubscribersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/#get_paginator)
        """

    async def __aenter__(self) -> "SecurityLakeClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/client/)
        """
