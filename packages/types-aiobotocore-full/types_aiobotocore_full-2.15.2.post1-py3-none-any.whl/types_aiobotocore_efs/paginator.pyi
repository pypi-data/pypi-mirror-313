"""
Type annotations for efs service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_efs.client import EFSClient
    from types_aiobotocore_efs.paginator import (
        DescribeAccessPointsPaginator,
        DescribeFileSystemsPaginator,
        DescribeMountTargetsPaginator,
        DescribeReplicationConfigurationsPaginator,
        DescribeTagsPaginator,
    )

    session = get_session()
    with session.create_client("efs") as client:
        client: EFSClient

        describe_access_points_paginator: DescribeAccessPointsPaginator = client.get_paginator("describe_access_points")
        describe_file_systems_paginator: DescribeFileSystemsPaginator = client.get_paginator("describe_file_systems")
        describe_mount_targets_paginator: DescribeMountTargetsPaginator = client.get_paginator("describe_mount_targets")
        describe_replication_configurations_paginator: DescribeReplicationConfigurationsPaginator = client.get_paginator("describe_replication_configurations")
        describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeAccessPointsRequestDescribeAccessPointsPaginateTypeDef,
    DescribeAccessPointsResponseTypeDef,
    DescribeFileSystemsRequestDescribeFileSystemsPaginateTypeDef,
    DescribeFileSystemsResponseTypeDef,
    DescribeMountTargetsRequestDescribeMountTargetsPaginateTypeDef,
    DescribeMountTargetsResponseTypeDef,
    DescribeReplicationConfigurationsRequestDescribeReplicationConfigurationsPaginateTypeDef,
    DescribeReplicationConfigurationsResponseTypeDef,
    DescribeTagsRequestDescribeTagsPaginateTypeDef,
    DescribeTagsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeAccessPointsPaginator",
    "DescribeFileSystemsPaginator",
    "DescribeMountTargetsPaginator",
    "DescribeReplicationConfigurationsPaginator",
    "DescribeTagsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeAccessPointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeAccessPoints.html#EFS.Paginator.DescribeAccessPoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describeaccesspointspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeAccessPointsRequestDescribeAccessPointsPaginateTypeDef]
    ) -> AsyncIterator[DescribeAccessPointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeAccessPoints.html#EFS.Paginator.DescribeAccessPoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describeaccesspointspaginator)
        """

class DescribeFileSystemsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeFileSystems.html#EFS.Paginator.DescribeFileSystems)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describefilesystemspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeFileSystemsRequestDescribeFileSystemsPaginateTypeDef]
    ) -> AsyncIterator[DescribeFileSystemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeFileSystems.html#EFS.Paginator.DescribeFileSystems.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describefilesystemspaginator)
        """

class DescribeMountTargetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeMountTargets.html#EFS.Paginator.DescribeMountTargets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describemounttargetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeMountTargetsRequestDescribeMountTargetsPaginateTypeDef]
    ) -> AsyncIterator[DescribeMountTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeMountTargets.html#EFS.Paginator.DescribeMountTargets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describemounttargetspaginator)
        """

class DescribeReplicationConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeReplicationConfigurations.html#EFS.Paginator.DescribeReplicationConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describereplicationconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReplicationConfigurationsRequestDescribeReplicationConfigurationsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeReplicationConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeReplicationConfigurations.html#EFS.Paginator.DescribeReplicationConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describereplicationconfigurationspaginator)
        """

class DescribeTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeTags.html#EFS.Paginator.DescribeTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describetagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeTagsRequestDescribeTagsPaginateTypeDef]
    ) -> AsyncIterator[DescribeTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/paginator/DescribeTags.html#EFS.Paginator.DescribeTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_efs/paginators/#describetagspaginator)
        """
