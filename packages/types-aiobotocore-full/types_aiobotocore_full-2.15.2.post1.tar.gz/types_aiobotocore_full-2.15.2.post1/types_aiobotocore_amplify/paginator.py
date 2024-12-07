"""
Type annotations for amplify service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_amplify.client import AmplifyClient
    from types_aiobotocore_amplify.paginator import (
        ListAppsPaginator,
        ListBranchesPaginator,
        ListDomainAssociationsPaginator,
        ListJobsPaginator,
    )

    session = get_session()
    with session.create_client("amplify") as client:
        client: AmplifyClient

        list_apps_paginator: ListAppsPaginator = client.get_paginator("list_apps")
        list_branches_paginator: ListBranchesPaginator = client.get_paginator("list_branches")
        list_domain_associations_paginator: ListDomainAssociationsPaginator = client.get_paginator("list_domain_associations")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAppsRequestListAppsPaginateTypeDef,
    ListAppsResultTypeDef,
    ListBranchesRequestListBranchesPaginateTypeDef,
    ListBranchesResultTypeDef,
    ListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef,
    ListDomainAssociationsResultTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAppsPaginator",
    "ListBranchesPaginator",
    "ListDomainAssociationsPaginator",
    "ListJobsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAppsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListApps.html#Amplify.Paginator.ListApps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/#listappspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAppsRequestListAppsPaginateTypeDef]
    ) -> AsyncIterator[ListAppsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListApps.html#Amplify.Paginator.ListApps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/#listappspaginator)
        """


class ListBranchesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListBranches.html#Amplify.Paginator.ListBranches)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/#listbranchespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBranchesRequestListBranchesPaginateTypeDef]
    ) -> AsyncIterator[ListBranchesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListBranches.html#Amplify.Paginator.ListBranches.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/#listbranchespaginator)
        """


class ListDomainAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListDomainAssociations.html#Amplify.Paginator.ListDomainAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/#listdomainassociationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef]
    ) -> AsyncIterator[ListDomainAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListDomainAssociations.html#Amplify.Paginator.ListDomainAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/#listdomainassociationspaginator)
        """


class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListJobs.html#Amplify.Paginator.ListJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/#listjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> AsyncIterator[ListJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify/paginator/ListJobs.html#Amplify.Paginator.ListJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/paginators/#listjobspaginator)
        """
