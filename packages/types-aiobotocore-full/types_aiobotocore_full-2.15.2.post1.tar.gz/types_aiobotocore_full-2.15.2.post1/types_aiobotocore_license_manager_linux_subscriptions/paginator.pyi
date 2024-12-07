"""
Type annotations for license-manager-linux-subscriptions service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_license_manager_linux_subscriptions.client import LicenseManagerLinuxSubscriptionsClient
    from types_aiobotocore_license_manager_linux_subscriptions.paginator import (
        ListLinuxSubscriptionInstancesPaginator,
        ListLinuxSubscriptionsPaginator,
        ListRegisteredSubscriptionProvidersPaginator,
    )

    session = get_session()
    with session.create_client("license-manager-linux-subscriptions") as client:
        client: LicenseManagerLinuxSubscriptionsClient

        list_linux_subscription_instances_paginator: ListLinuxSubscriptionInstancesPaginator = client.get_paginator("list_linux_subscription_instances")
        list_linux_subscriptions_paginator: ListLinuxSubscriptionsPaginator = client.get_paginator("list_linux_subscriptions")
        list_registered_subscription_providers_paginator: ListRegisteredSubscriptionProvidersPaginator = client.get_paginator("list_registered_subscription_providers")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListLinuxSubscriptionInstancesRequestListLinuxSubscriptionInstancesPaginateTypeDef,
    ListLinuxSubscriptionInstancesResponseTypeDef,
    ListLinuxSubscriptionsRequestListLinuxSubscriptionsPaginateTypeDef,
    ListLinuxSubscriptionsResponseTypeDef,
    ListRegisteredSubscriptionProvidersRequestListRegisteredSubscriptionProvidersPaginateTypeDef,
    ListRegisteredSubscriptionProvidersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListLinuxSubscriptionInstancesPaginator",
    "ListLinuxSubscriptionsPaginator",
    "ListRegisteredSubscriptionProvidersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListLinuxSubscriptionInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/paginator/ListLinuxSubscriptionInstances.html#LicenseManagerLinuxSubscriptions.Paginator.ListLinuxSubscriptionInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/paginators/#listlinuxsubscriptioninstancespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListLinuxSubscriptionInstancesRequestListLinuxSubscriptionInstancesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListLinuxSubscriptionInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/paginator/ListLinuxSubscriptionInstances.html#LicenseManagerLinuxSubscriptions.Paginator.ListLinuxSubscriptionInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/paginators/#listlinuxsubscriptioninstancespaginator)
        """

class ListLinuxSubscriptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/paginator/ListLinuxSubscriptions.html#LicenseManagerLinuxSubscriptions.Paginator.ListLinuxSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/paginators/#listlinuxsubscriptionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLinuxSubscriptionsRequestListLinuxSubscriptionsPaginateTypeDef]
    ) -> AsyncIterator[ListLinuxSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/paginator/ListLinuxSubscriptions.html#LicenseManagerLinuxSubscriptions.Paginator.ListLinuxSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/paginators/#listlinuxsubscriptionspaginator)
        """

class ListRegisteredSubscriptionProvidersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/paginator/ListRegisteredSubscriptionProviders.html#LicenseManagerLinuxSubscriptions.Paginator.ListRegisteredSubscriptionProviders)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/paginators/#listregisteredsubscriptionproviderspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListRegisteredSubscriptionProvidersRequestListRegisteredSubscriptionProvidersPaginateTypeDef
        ],
    ) -> AsyncIterator[ListRegisteredSubscriptionProvidersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-linux-subscriptions/paginator/ListRegisteredSubscriptionProviders.html#LicenseManagerLinuxSubscriptions.Paginator.ListRegisteredSubscriptionProviders.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_linux_subscriptions/paginators/#listregisteredsubscriptionproviderspaginator)
        """
