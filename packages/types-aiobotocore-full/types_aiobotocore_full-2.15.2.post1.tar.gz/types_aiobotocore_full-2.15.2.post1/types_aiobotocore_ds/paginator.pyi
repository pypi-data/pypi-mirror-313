"""
Type annotations for ds service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ds.client import DirectoryServiceClient
    from types_aiobotocore_ds.paginator import (
        DescribeClientAuthenticationSettingsPaginator,
        DescribeDirectoriesPaginator,
        DescribeDomainControllersPaginator,
        DescribeLDAPSSettingsPaginator,
        DescribeRegionsPaginator,
        DescribeSharedDirectoriesPaginator,
        DescribeSnapshotsPaginator,
        DescribeTrustsPaginator,
        DescribeUpdateDirectoryPaginator,
        ListCertificatesPaginator,
        ListIpRoutesPaginator,
        ListLogSubscriptionsPaginator,
        ListSchemaExtensionsPaginator,
        ListTagsForResourcePaginator,
    )

    session = get_session()
    with session.create_client("ds") as client:
        client: DirectoryServiceClient

        describe_client_authentication_settings_paginator: DescribeClientAuthenticationSettingsPaginator = client.get_paginator("describe_client_authentication_settings")
        describe_directories_paginator: DescribeDirectoriesPaginator = client.get_paginator("describe_directories")
        describe_domain_controllers_paginator: DescribeDomainControllersPaginator = client.get_paginator("describe_domain_controllers")
        describe_ldaps_settings_paginator: DescribeLDAPSSettingsPaginator = client.get_paginator("describe_ldaps_settings")
        describe_regions_paginator: DescribeRegionsPaginator = client.get_paginator("describe_regions")
        describe_shared_directories_paginator: DescribeSharedDirectoriesPaginator = client.get_paginator("describe_shared_directories")
        describe_snapshots_paginator: DescribeSnapshotsPaginator = client.get_paginator("describe_snapshots")
        describe_trusts_paginator: DescribeTrustsPaginator = client.get_paginator("describe_trusts")
        describe_update_directory_paginator: DescribeUpdateDirectoryPaginator = client.get_paginator("describe_update_directory")
        list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
        list_ip_routes_paginator: ListIpRoutesPaginator = client.get_paginator("list_ip_routes")
        list_log_subscriptions_paginator: ListLogSubscriptionsPaginator = client.get_paginator("list_log_subscriptions")
        list_schema_extensions_paginator: ListSchemaExtensionsPaginator = client.get_paginator("list_schema_extensions")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeClientAuthenticationSettingsRequestDescribeClientAuthenticationSettingsPaginateTypeDef,
    DescribeClientAuthenticationSettingsResultTypeDef,
    DescribeDirectoriesRequestDescribeDirectoriesPaginateTypeDef,
    DescribeDirectoriesResultTypeDef,
    DescribeDomainControllersRequestDescribeDomainControllersPaginateTypeDef,
    DescribeDomainControllersResultTypeDef,
    DescribeLDAPSSettingsRequestDescribeLDAPSSettingsPaginateTypeDef,
    DescribeLDAPSSettingsResultTypeDef,
    DescribeRegionsRequestDescribeRegionsPaginateTypeDef,
    DescribeRegionsResultTypeDef,
    DescribeSharedDirectoriesRequestDescribeSharedDirectoriesPaginateTypeDef,
    DescribeSharedDirectoriesResultTypeDef,
    DescribeSnapshotsRequestDescribeSnapshotsPaginateTypeDef,
    DescribeSnapshotsResultTypeDef,
    DescribeTrustsRequestDescribeTrustsPaginateTypeDef,
    DescribeTrustsResultTypeDef,
    DescribeUpdateDirectoryRequestDescribeUpdateDirectoryPaginateTypeDef,
    DescribeUpdateDirectoryResultTypeDef,
    ListCertificatesRequestListCertificatesPaginateTypeDef,
    ListCertificatesResultTypeDef,
    ListIpRoutesRequestListIpRoutesPaginateTypeDef,
    ListIpRoutesResultTypeDef,
    ListLogSubscriptionsRequestListLogSubscriptionsPaginateTypeDef,
    ListLogSubscriptionsResultTypeDef,
    ListSchemaExtensionsRequestListSchemaExtensionsPaginateTypeDef,
    ListSchemaExtensionsResultTypeDef,
    ListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    ListTagsForResourceResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeClientAuthenticationSettingsPaginator",
    "DescribeDirectoriesPaginator",
    "DescribeDomainControllersPaginator",
    "DescribeLDAPSSettingsPaginator",
    "DescribeRegionsPaginator",
    "DescribeSharedDirectoriesPaginator",
    "DescribeSnapshotsPaginator",
    "DescribeTrustsPaginator",
    "DescribeUpdateDirectoryPaginator",
    "ListCertificatesPaginator",
    "ListIpRoutesPaginator",
    "ListLogSubscriptionsPaginator",
    "ListSchemaExtensionsPaginator",
    "ListTagsForResourcePaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeClientAuthenticationSettingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeClientAuthenticationSettings.html#DirectoryService.Paginator.DescribeClientAuthenticationSettings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describeclientauthenticationsettingspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeClientAuthenticationSettingsRequestDescribeClientAuthenticationSettingsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeClientAuthenticationSettingsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeClientAuthenticationSettings.html#DirectoryService.Paginator.DescribeClientAuthenticationSettings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describeclientauthenticationsettingspaginator)
        """

class DescribeDirectoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeDirectories.html#DirectoryService.Paginator.DescribeDirectories)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describedirectoriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeDirectoriesRequestDescribeDirectoriesPaginateTypeDef]
    ) -> AsyncIterator[DescribeDirectoriesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeDirectories.html#DirectoryService.Paginator.DescribeDirectories.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describedirectoriespaginator)
        """

class DescribeDomainControllersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeDomainControllers.html#DirectoryService.Paginator.DescribeDomainControllers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describedomaincontrollerspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeDomainControllersRequestDescribeDomainControllersPaginateTypeDef],
    ) -> AsyncIterator[DescribeDomainControllersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeDomainControllers.html#DirectoryService.Paginator.DescribeDomainControllers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describedomaincontrollerspaginator)
        """

class DescribeLDAPSSettingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeLDAPSSettings.html#DirectoryService.Paginator.DescribeLDAPSSettings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describeldapssettingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeLDAPSSettingsRequestDescribeLDAPSSettingsPaginateTypeDef]
    ) -> AsyncIterator[DescribeLDAPSSettingsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeLDAPSSettings.html#DirectoryService.Paginator.DescribeLDAPSSettings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describeldapssettingspaginator)
        """

class DescribeRegionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeRegions.html#DirectoryService.Paginator.DescribeRegions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describeregionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeRegionsRequestDescribeRegionsPaginateTypeDef]
    ) -> AsyncIterator[DescribeRegionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeRegions.html#DirectoryService.Paginator.DescribeRegions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describeregionspaginator)
        """

class DescribeSharedDirectoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeSharedDirectories.html#DirectoryService.Paginator.DescribeSharedDirectories)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describeshareddirectoriespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeSharedDirectoriesRequestDescribeSharedDirectoriesPaginateTypeDef],
    ) -> AsyncIterator[DescribeSharedDirectoriesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeSharedDirectories.html#DirectoryService.Paginator.DescribeSharedDirectories.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describeshareddirectoriespaginator)
        """

class DescribeSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeSnapshots.html#DirectoryService.Paginator.DescribeSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describesnapshotspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeSnapshotsRequestDescribeSnapshotsPaginateTypeDef]
    ) -> AsyncIterator[DescribeSnapshotsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeSnapshots.html#DirectoryService.Paginator.DescribeSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describesnapshotspaginator)
        """

class DescribeTrustsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeTrusts.html#DirectoryService.Paginator.DescribeTrusts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describetrustspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeTrustsRequestDescribeTrustsPaginateTypeDef]
    ) -> AsyncIterator[DescribeTrustsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeTrusts.html#DirectoryService.Paginator.DescribeTrusts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describetrustspaginator)
        """

class DescribeUpdateDirectoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeUpdateDirectory.html#DirectoryService.Paginator.DescribeUpdateDirectory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describeupdatedirectorypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeUpdateDirectoryRequestDescribeUpdateDirectoryPaginateTypeDef]
    ) -> AsyncIterator[DescribeUpdateDirectoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/DescribeUpdateDirectory.html#DirectoryService.Paginator.DescribeUpdateDirectory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#describeupdatedirectorypaginator)
        """

class ListCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListCertificates.html#DirectoryService.Paginator.ListCertificates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#listcertificatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCertificatesRequestListCertificatesPaginateTypeDef]
    ) -> AsyncIterator[ListCertificatesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListCertificates.html#DirectoryService.Paginator.ListCertificates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#listcertificatespaginator)
        """

class ListIpRoutesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListIpRoutes.html#DirectoryService.Paginator.ListIpRoutes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#listiproutespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIpRoutesRequestListIpRoutesPaginateTypeDef]
    ) -> AsyncIterator[ListIpRoutesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListIpRoutes.html#DirectoryService.Paginator.ListIpRoutes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#listiproutespaginator)
        """

class ListLogSubscriptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListLogSubscriptions.html#DirectoryService.Paginator.ListLogSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#listlogsubscriptionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLogSubscriptionsRequestListLogSubscriptionsPaginateTypeDef]
    ) -> AsyncIterator[ListLogSubscriptionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListLogSubscriptions.html#DirectoryService.Paginator.ListLogSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#listlogsubscriptionspaginator)
        """

class ListSchemaExtensionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListSchemaExtensions.html#DirectoryService.Paginator.ListSchemaExtensions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#listschemaextensionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSchemaExtensionsRequestListSchemaExtensionsPaginateTypeDef]
    ) -> AsyncIterator[ListSchemaExtensionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListSchemaExtensions.html#DirectoryService.Paginator.ListSchemaExtensions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#listschemaextensionspaginator)
        """

class ListTagsForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListTagsForResource.html#DirectoryService.Paginator.ListTagsForResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#listtagsforresourcepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> AsyncIterator[ListTagsForResourceResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds/paginator/ListTagsForResource.html#DirectoryService.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/paginators/#listtagsforresourcepaginator)
        """
