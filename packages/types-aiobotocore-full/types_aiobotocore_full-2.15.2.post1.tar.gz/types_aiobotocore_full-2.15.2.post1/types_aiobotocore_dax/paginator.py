"""
Type annotations for dax service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dax.client import DAXClient
    from types_aiobotocore_dax.paginator import (
        DescribeClustersPaginator,
        DescribeDefaultParametersPaginator,
        DescribeEventsPaginator,
        DescribeParameterGroupsPaginator,
        DescribeParametersPaginator,
        DescribeSubnetGroupsPaginator,
        ListTagsPaginator,
    )

    session = get_session()
    with session.create_client("dax") as client:
        client: DAXClient

        describe_clusters_paginator: DescribeClustersPaginator = client.get_paginator("describe_clusters")
        describe_default_parameters_paginator: DescribeDefaultParametersPaginator = client.get_paginator("describe_default_parameters")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_parameter_groups_paginator: DescribeParameterGroupsPaginator = client.get_paginator("describe_parameter_groups")
        describe_parameters_paginator: DescribeParametersPaginator = client.get_paginator("describe_parameters")
        describe_subnet_groups_paginator: DescribeSubnetGroupsPaginator = client.get_paginator("describe_subnet_groups")
        list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeClustersRequestDescribeClustersPaginateTypeDef,
    DescribeClustersResponseTypeDef,
    DescribeDefaultParametersRequestDescribeDefaultParametersPaginateTypeDef,
    DescribeDefaultParametersResponseTypeDef,
    DescribeEventsRequestDescribeEventsPaginateTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeParameterGroupsRequestDescribeParameterGroupsPaginateTypeDef,
    DescribeParameterGroupsResponseTypeDef,
    DescribeParametersRequestDescribeParametersPaginateTypeDef,
    DescribeParametersResponseTypeDef,
    DescribeSubnetGroupsRequestDescribeSubnetGroupsPaginateTypeDef,
    DescribeSubnetGroupsResponseTypeDef,
    ListTagsRequestListTagsPaginateTypeDef,
    ListTagsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeClustersPaginator",
    "DescribeDefaultParametersPaginator",
    "DescribeEventsPaginator",
    "DescribeParameterGroupsPaginator",
    "DescribeParametersPaginator",
    "DescribeSubnetGroupsPaginator",
    "ListTagsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeClusters.html#DAX.Paginator.DescribeClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeclusterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeClustersRequestDescribeClustersPaginateTypeDef]
    ) -> AsyncIterator[DescribeClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeClusters.html#DAX.Paginator.DescribeClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeclusterspaginator)
        """


class DescribeDefaultParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeDefaultParameters.html#DAX.Paginator.DescribeDefaultParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describedefaultparameterspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeDefaultParametersRequestDescribeDefaultParametersPaginateTypeDef],
    ) -> AsyncIterator[DescribeDefaultParametersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeDefaultParameters.html#DAX.Paginator.DescribeDefaultParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describedefaultparameterspaginator)
        """


class DescribeEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeEvents.html#DAX.Paginator.DescribeEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeeventspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeEventsRequestDescribeEventsPaginateTypeDef]
    ) -> AsyncIterator[DescribeEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeEvents.html#DAX.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeeventspaginator)
        """


class DescribeParameterGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeParameterGroups.html#DAX.Paginator.DescribeParameterGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeparametergroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeParameterGroupsRequestDescribeParameterGroupsPaginateTypeDef]
    ) -> AsyncIterator[DescribeParameterGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeParameterGroups.html#DAX.Paginator.DescribeParameterGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeparametergroupspaginator)
        """


class DescribeParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeParameters.html#DAX.Paginator.DescribeParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeparameterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeParametersRequestDescribeParametersPaginateTypeDef]
    ) -> AsyncIterator[DescribeParametersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeParameters.html#DAX.Paginator.DescribeParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeparameterspaginator)
        """


class DescribeSubnetGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeSubnetGroups.html#DAX.Paginator.DescribeSubnetGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describesubnetgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeSubnetGroupsRequestDescribeSubnetGroupsPaginateTypeDef]
    ) -> AsyncIterator[DescribeSubnetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/DescribeSubnetGroups.html#DAX.Paginator.DescribeSubnetGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describesubnetgroupspaginator)
        """


class ListTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/ListTags.html#DAX.Paginator.ListTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#listtagspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTagsRequestListTagsPaginateTypeDef]
    ) -> AsyncIterator[ListTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax/paginator/ListTags.html#DAX.Paginator.ListTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#listtagspaginator)
        """
