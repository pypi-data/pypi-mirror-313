"""
Type annotations for codeartifact service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codeartifact.client import CodeArtifactClient
    from types_aiobotocore_codeartifact.paginator import (
        ListAllowedRepositoriesForGroupPaginator,
        ListAssociatedPackagesPaginator,
        ListDomainsPaginator,
        ListPackageGroupsPaginator,
        ListPackageVersionAssetsPaginator,
        ListPackageVersionsPaginator,
        ListPackagesPaginator,
        ListRepositoriesInDomainPaginator,
        ListRepositoriesPaginator,
        ListSubPackageGroupsPaginator,
    )

    session = get_session()
    with session.create_client("codeartifact") as client:
        client: CodeArtifactClient

        list_allowed_repositories_for_group_paginator: ListAllowedRepositoriesForGroupPaginator = client.get_paginator("list_allowed_repositories_for_group")
        list_associated_packages_paginator: ListAssociatedPackagesPaginator = client.get_paginator("list_associated_packages")
        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_package_groups_paginator: ListPackageGroupsPaginator = client.get_paginator("list_package_groups")
        list_package_version_assets_paginator: ListPackageVersionAssetsPaginator = client.get_paginator("list_package_version_assets")
        list_package_versions_paginator: ListPackageVersionsPaginator = client.get_paginator("list_package_versions")
        list_packages_paginator: ListPackagesPaginator = client.get_paginator("list_packages")
        list_repositories_in_domain_paginator: ListRepositoriesInDomainPaginator = client.get_paginator("list_repositories_in_domain")
        list_repositories_paginator: ListRepositoriesPaginator = client.get_paginator("list_repositories")
        list_sub_package_groups_paginator: ListSubPackageGroupsPaginator = client.get_paginator("list_sub_package_groups")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAllowedRepositoriesForGroupRequestListAllowedRepositoriesForGroupPaginateTypeDef,
    ListAllowedRepositoriesForGroupResultTypeDef,
    ListAssociatedPackagesRequestListAssociatedPackagesPaginateTypeDef,
    ListAssociatedPackagesResultTypeDef,
    ListDomainsRequestListDomainsPaginateTypeDef,
    ListDomainsResultTypeDef,
    ListPackageGroupsRequestListPackageGroupsPaginateTypeDef,
    ListPackageGroupsResultTypeDef,
    ListPackagesRequestListPackagesPaginateTypeDef,
    ListPackagesResultTypeDef,
    ListPackageVersionAssetsRequestListPackageVersionAssetsPaginateTypeDef,
    ListPackageVersionAssetsResultTypeDef,
    ListPackageVersionsRequestListPackageVersionsPaginateTypeDef,
    ListPackageVersionsResultTypeDef,
    ListRepositoriesInDomainRequestListRepositoriesInDomainPaginateTypeDef,
    ListRepositoriesInDomainResultTypeDef,
    ListRepositoriesRequestListRepositoriesPaginateTypeDef,
    ListRepositoriesResultTypeDef,
    ListSubPackageGroupsRequestListSubPackageGroupsPaginateTypeDef,
    ListSubPackageGroupsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAllowedRepositoriesForGroupPaginator",
    "ListAssociatedPackagesPaginator",
    "ListDomainsPaginator",
    "ListPackageGroupsPaginator",
    "ListPackageVersionAssetsPaginator",
    "ListPackageVersionsPaginator",
    "ListPackagesPaginator",
    "ListRepositoriesInDomainPaginator",
    "ListRepositoriesPaginator",
    "ListSubPackageGroupsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAllowedRepositoriesForGroupPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListAllowedRepositoriesForGroup.html#CodeArtifact.Paginator.ListAllowedRepositoriesForGroup)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listallowedrepositoriesforgrouppaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAllowedRepositoriesForGroupRequestListAllowedRepositoriesForGroupPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAllowedRepositoriesForGroupResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListAllowedRepositoriesForGroup.html#CodeArtifact.Paginator.ListAllowedRepositoriesForGroup.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listallowedrepositoriesforgrouppaginator)
        """

class ListAssociatedPackagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListAssociatedPackages.html#CodeArtifact.Paginator.ListAssociatedPackages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listassociatedpackagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAssociatedPackagesRequestListAssociatedPackagesPaginateTypeDef]
    ) -> AsyncIterator[ListAssociatedPackagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListAssociatedPackages.html#CodeArtifact.Paginator.ListAssociatedPackages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listassociatedpackagespaginator)
        """

class ListDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListDomains.html#CodeArtifact.Paginator.ListDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listdomainspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDomainsRequestListDomainsPaginateTypeDef]
    ) -> AsyncIterator[ListDomainsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListDomains.html#CodeArtifact.Paginator.ListDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listdomainspaginator)
        """

class ListPackageGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListPackageGroups.html#CodeArtifact.Paginator.ListPackageGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listpackagegroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPackageGroupsRequestListPackageGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListPackageGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListPackageGroups.html#CodeArtifact.Paginator.ListPackageGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listpackagegroupspaginator)
        """

class ListPackageVersionAssetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListPackageVersionAssets.html#CodeArtifact.Paginator.ListPackageVersionAssets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listpackageversionassetspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListPackageVersionAssetsRequestListPackageVersionAssetsPaginateTypeDef],
    ) -> AsyncIterator[ListPackageVersionAssetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListPackageVersionAssets.html#CodeArtifact.Paginator.ListPackageVersionAssets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listpackageversionassetspaginator)
        """

class ListPackageVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListPackageVersions.html#CodeArtifact.Paginator.ListPackageVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listpackageversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPackageVersionsRequestListPackageVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListPackageVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListPackageVersions.html#CodeArtifact.Paginator.ListPackageVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listpackageversionspaginator)
        """

class ListPackagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListPackages.html#CodeArtifact.Paginator.ListPackages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listpackagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPackagesRequestListPackagesPaginateTypeDef]
    ) -> AsyncIterator[ListPackagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListPackages.html#CodeArtifact.Paginator.ListPackages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listpackagespaginator)
        """

class ListRepositoriesInDomainPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListRepositoriesInDomain.html#CodeArtifact.Paginator.ListRepositoriesInDomain)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listrepositoriesindomainpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListRepositoriesInDomainRequestListRepositoriesInDomainPaginateTypeDef],
    ) -> AsyncIterator[ListRepositoriesInDomainResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListRepositoriesInDomain.html#CodeArtifact.Paginator.ListRepositoriesInDomain.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listrepositoriesindomainpaginator)
        """

class ListRepositoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListRepositories.html#CodeArtifact.Paginator.ListRepositories)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listrepositoriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRepositoriesRequestListRepositoriesPaginateTypeDef]
    ) -> AsyncIterator[ListRepositoriesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListRepositories.html#CodeArtifact.Paginator.ListRepositories.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listrepositoriespaginator)
        """

class ListSubPackageGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListSubPackageGroups.html#CodeArtifact.Paginator.ListSubPackageGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listsubpackagegroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSubPackageGroupsRequestListSubPackageGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListSubPackageGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListSubPackageGroups.html#CodeArtifact.Paginator.ListSubPackageGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listsubpackagegroupspaginator)
        """
