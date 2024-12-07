"""
Type annotations for cloudhsmv2 service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudhsmv2.client import CloudHSMV2Client
    from types_aiobotocore_cloudhsmv2.paginator import (
        DescribeBackupsPaginator,
        DescribeClustersPaginator,
        ListTagsPaginator,
    )

    session = get_session()
    with session.create_client("cloudhsmv2") as client:
        client: CloudHSMV2Client

        describe_backups_paginator: DescribeBackupsPaginator = client.get_paginator("describe_backups")
        describe_clusters_paginator: DescribeClustersPaginator = client.get_paginator("describe_clusters")
        list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeBackupsRequestDescribeBackupsPaginateTypeDef,
    DescribeBackupsResponseTypeDef,
    DescribeClustersRequestDescribeClustersPaginateTypeDef,
    DescribeClustersResponseTypeDef,
    ListTagsRequestListTagsPaginateTypeDef,
    ListTagsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("DescribeBackupsPaginator", "DescribeClustersPaginator", "ListTagsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeBackupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/DescribeBackups.html#CloudHSMV2.Paginator.DescribeBackups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#describebackupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeBackupsRequestDescribeBackupsPaginateTypeDef]
    ) -> AsyncIterator[DescribeBackupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/DescribeBackups.html#CloudHSMV2.Paginator.DescribeBackups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#describebackupspaginator)
        """

class DescribeClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/DescribeClusters.html#CloudHSMV2.Paginator.DescribeClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#describeclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeClustersRequestDescribeClustersPaginateTypeDef]
    ) -> AsyncIterator[DescribeClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/DescribeClusters.html#CloudHSMV2.Paginator.DescribeClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#describeclusterspaginator)
        """

class ListTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/ListTags.html#CloudHSMV2.Paginator.ListTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#listtagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsRequestListTagsPaginateTypeDef]
    ) -> AsyncIterator[ListTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2/paginator/ListTags.html#CloudHSMV2.Paginator.ListTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#listtagspaginator)
        """
