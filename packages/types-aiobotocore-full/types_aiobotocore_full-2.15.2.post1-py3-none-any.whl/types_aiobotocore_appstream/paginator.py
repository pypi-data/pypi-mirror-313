"""
Type annotations for appstream service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_appstream.client import AppStreamClient
    from types_aiobotocore_appstream.paginator import (
        DescribeDirectoryConfigsPaginator,
        DescribeFleetsPaginator,
        DescribeImageBuildersPaginator,
        DescribeImagesPaginator,
        DescribeSessionsPaginator,
        DescribeStacksPaginator,
        DescribeUserStackAssociationsPaginator,
        DescribeUsersPaginator,
        ListAssociatedFleetsPaginator,
        ListAssociatedStacksPaginator,
    )

    session = get_session()
    with session.create_client("appstream") as client:
        client: AppStreamClient

        describe_directory_configs_paginator: DescribeDirectoryConfigsPaginator = client.get_paginator("describe_directory_configs")
        describe_fleets_paginator: DescribeFleetsPaginator = client.get_paginator("describe_fleets")
        describe_image_builders_paginator: DescribeImageBuildersPaginator = client.get_paginator("describe_image_builders")
        describe_images_paginator: DescribeImagesPaginator = client.get_paginator("describe_images")
        describe_sessions_paginator: DescribeSessionsPaginator = client.get_paginator("describe_sessions")
        describe_stacks_paginator: DescribeStacksPaginator = client.get_paginator("describe_stacks")
        describe_user_stack_associations_paginator: DescribeUserStackAssociationsPaginator = client.get_paginator("describe_user_stack_associations")
        describe_users_paginator: DescribeUsersPaginator = client.get_paginator("describe_users")
        list_associated_fleets_paginator: ListAssociatedFleetsPaginator = client.get_paginator("list_associated_fleets")
        list_associated_stacks_paginator: ListAssociatedStacksPaginator = client.get_paginator("list_associated_stacks")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeDirectoryConfigsRequestDescribeDirectoryConfigsPaginateTypeDef,
    DescribeDirectoryConfigsResultTypeDef,
    DescribeFleetsRequestDescribeFleetsPaginateTypeDef,
    DescribeFleetsResultTypeDef,
    DescribeImageBuildersRequestDescribeImageBuildersPaginateTypeDef,
    DescribeImageBuildersResultTypeDef,
    DescribeImagesRequestDescribeImagesPaginateTypeDef,
    DescribeImagesResultTypeDef,
    DescribeSessionsRequestDescribeSessionsPaginateTypeDef,
    DescribeSessionsResultTypeDef,
    DescribeStacksRequestDescribeStacksPaginateTypeDef,
    DescribeStacksResultTypeDef,
    DescribeUsersRequestDescribeUsersPaginateTypeDef,
    DescribeUsersResultTypeDef,
    DescribeUserStackAssociationsRequestDescribeUserStackAssociationsPaginateTypeDef,
    DescribeUserStackAssociationsResultTypeDef,
    ListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef,
    ListAssociatedFleetsResultTypeDef,
    ListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef,
    ListAssociatedStacksResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeDirectoryConfigsPaginator",
    "DescribeFleetsPaginator",
    "DescribeImageBuildersPaginator",
    "DescribeImagesPaginator",
    "DescribeSessionsPaginator",
    "DescribeStacksPaginator",
    "DescribeUserStackAssociationsPaginator",
    "DescribeUsersPaginator",
    "ListAssociatedFleetsPaginator",
    "ListAssociatedStacksPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeDirectoryConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeDirectoryConfigs.html#AppStream.Paginator.DescribeDirectoryConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describedirectoryconfigspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeDirectoryConfigsRequestDescribeDirectoryConfigsPaginateTypeDef],
    ) -> AsyncIterator[DescribeDirectoryConfigsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeDirectoryConfigs.html#AppStream.Paginator.DescribeDirectoryConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describedirectoryconfigspaginator)
        """


class DescribeFleetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeFleets.html#AppStream.Paginator.DescribeFleets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describefleetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeFleetsRequestDescribeFleetsPaginateTypeDef]
    ) -> AsyncIterator[DescribeFleetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeFleets.html#AppStream.Paginator.DescribeFleets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describefleetspaginator)
        """


class DescribeImageBuildersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeImageBuilders.html#AppStream.Paginator.DescribeImageBuilders)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describeimagebuilderspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeImageBuildersRequestDescribeImageBuildersPaginateTypeDef]
    ) -> AsyncIterator[DescribeImageBuildersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeImageBuilders.html#AppStream.Paginator.DescribeImageBuilders.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describeimagebuilderspaginator)
        """


class DescribeImagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeImages.html#AppStream.Paginator.DescribeImages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describeimagespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeImagesRequestDescribeImagesPaginateTypeDef]
    ) -> AsyncIterator[DescribeImagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeImages.html#AppStream.Paginator.DescribeImages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describeimagespaginator)
        """


class DescribeSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeSessions.html#AppStream.Paginator.DescribeSessions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describesessionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeSessionsRequestDescribeSessionsPaginateTypeDef]
    ) -> AsyncIterator[DescribeSessionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeSessions.html#AppStream.Paginator.DescribeSessions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describesessionspaginator)
        """


class DescribeStacksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeStacks.html#AppStream.Paginator.DescribeStacks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describestackspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeStacksRequestDescribeStacksPaginateTypeDef]
    ) -> AsyncIterator[DescribeStacksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeStacks.html#AppStream.Paginator.DescribeStacks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describestackspaginator)
        """


class DescribeUserStackAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeUserStackAssociations.html#AppStream.Paginator.DescribeUserStackAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describeuserstackassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeUserStackAssociationsRequestDescribeUserStackAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeUserStackAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeUserStackAssociations.html#AppStream.Paginator.DescribeUserStackAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describeuserstackassociationspaginator)
        """


class DescribeUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeUsers.html#AppStream.Paginator.DescribeUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describeuserspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeUsersRequestDescribeUsersPaginateTypeDef]
    ) -> AsyncIterator[DescribeUsersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/DescribeUsers.html#AppStream.Paginator.DescribeUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#describeuserspaginator)
        """


class ListAssociatedFleetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/ListAssociatedFleets.html#AppStream.Paginator.ListAssociatedFleets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#listassociatedfleetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssociatedFleetsRequestListAssociatedFleetsPaginateTypeDef]
    ) -> AsyncIterator[ListAssociatedFleetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/ListAssociatedFleets.html#AppStream.Paginator.ListAssociatedFleets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#listassociatedfleetspaginator)
        """


class ListAssociatedStacksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/ListAssociatedStacks.html#AppStream.Paginator.ListAssociatedStacks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#listassociatedstackspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssociatedStacksRequestListAssociatedStacksPaginateTypeDef]
    ) -> AsyncIterator[ListAssociatedStacksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/paginator/ListAssociatedStacks.html#AppStream.Paginator.ListAssociatedStacks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/paginators/#listassociatedstackspaginator)
        """
