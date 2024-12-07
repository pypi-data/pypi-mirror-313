"""
Type annotations for servicecatalog-appregistry service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_servicecatalog_appregistry.client import AppRegistryClient
    from types_aiobotocore_servicecatalog_appregistry.paginator import (
        ListApplicationsPaginator,
        ListAssociatedAttributeGroupsPaginator,
        ListAssociatedResourcesPaginator,
        ListAttributeGroupsForApplicationPaginator,
        ListAttributeGroupsPaginator,
    )

    session = get_session()
    with session.create_client("servicecatalog-appregistry") as client:
        client: AppRegistryClient

        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
        list_associated_attribute_groups_paginator: ListAssociatedAttributeGroupsPaginator = client.get_paginator("list_associated_attribute_groups")
        list_associated_resources_paginator: ListAssociatedResourcesPaginator = client.get_paginator("list_associated_resources")
        list_attribute_groups_for_application_paginator: ListAttributeGroupsForApplicationPaginator = client.get_paginator("list_attribute_groups_for_application")
        list_attribute_groups_paginator: ListAttributeGroupsPaginator = client.get_paginator("list_attribute_groups")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListApplicationsRequestListApplicationsPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef,
    ListAssociatedAttributeGroupsResponseTypeDef,
    ListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef,
    ListAssociatedResourcesResponseTypeDef,
    ListAttributeGroupsForApplicationRequestListAttributeGroupsForApplicationPaginateTypeDef,
    ListAttributeGroupsForApplicationResponseTypeDef,
    ListAttributeGroupsRequestListAttributeGroupsPaginateTypeDef,
    ListAttributeGroupsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListApplicationsPaginator",
    "ListAssociatedAttributeGroupsPaginator",
    "ListAssociatedResourcesPaginator",
    "ListAttributeGroupsForApplicationPaginator",
    "ListAttributeGroupsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListApplications.html#AppRegistry.Paginator.ListApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators/#listapplicationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListApplicationsRequestListApplicationsPaginateTypeDef]
    ) -> AsyncIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListApplications.html#AppRegistry.Paginator.ListApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators/#listapplicationspaginator)
        """

class ListAssociatedAttributeGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListAssociatedAttributeGroups.html#AppRegistry.Paginator.ListAssociatedAttributeGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators/#listassociatedattributegroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAssociatedAttributeGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListAssociatedAttributeGroups.html#AppRegistry.Paginator.ListAssociatedAttributeGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators/#listassociatedattributegroupspaginator)
        """

class ListAssociatedResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListAssociatedResources.html#AppRegistry.Paginator.ListAssociatedResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators/#listassociatedresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef]
    ) -> AsyncIterator[ListAssociatedResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListAssociatedResources.html#AppRegistry.Paginator.ListAssociatedResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators/#listassociatedresourcespaginator)
        """

class ListAttributeGroupsForApplicationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListAttributeGroupsForApplication.html#AppRegistry.Paginator.ListAttributeGroupsForApplication)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators/#listattributegroupsforapplicationpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAttributeGroupsForApplicationRequestListAttributeGroupsForApplicationPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAttributeGroupsForApplicationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListAttributeGroupsForApplication.html#AppRegistry.Paginator.ListAttributeGroupsForApplication.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators/#listattributegroupsforapplicationpaginator)
        """

class ListAttributeGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListAttributeGroups.html#AppRegistry.Paginator.ListAttributeGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators/#listattributegroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAttributeGroupsRequestListAttributeGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListAttributeGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/paginator/ListAttributeGroups.html#AppRegistry.Paginator.ListAttributeGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog_appregistry/paginators/#listattributegroupspaginator)
        """
