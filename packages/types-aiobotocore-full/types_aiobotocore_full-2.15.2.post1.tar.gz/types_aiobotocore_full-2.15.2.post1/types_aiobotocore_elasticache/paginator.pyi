"""
Type annotations for elasticache service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elasticache.client import ElastiCacheClient
    from types_aiobotocore_elasticache.paginator import (
        DescribeCacheClustersPaginator,
        DescribeCacheEngineVersionsPaginator,
        DescribeCacheParameterGroupsPaginator,
        DescribeCacheParametersPaginator,
        DescribeCacheSecurityGroupsPaginator,
        DescribeCacheSubnetGroupsPaginator,
        DescribeEngineDefaultParametersPaginator,
        DescribeEventsPaginator,
        DescribeGlobalReplicationGroupsPaginator,
        DescribeReplicationGroupsPaginator,
        DescribeReservedCacheNodesOfferingsPaginator,
        DescribeReservedCacheNodesPaginator,
        DescribeServerlessCacheSnapshotsPaginator,
        DescribeServerlessCachesPaginator,
        DescribeServiceUpdatesPaginator,
        DescribeSnapshotsPaginator,
        DescribeUpdateActionsPaginator,
        DescribeUserGroupsPaginator,
        DescribeUsersPaginator,
    )

    session = get_session()
    with session.create_client("elasticache") as client:
        client: ElastiCacheClient

        describe_cache_clusters_paginator: DescribeCacheClustersPaginator = client.get_paginator("describe_cache_clusters")
        describe_cache_engine_versions_paginator: DescribeCacheEngineVersionsPaginator = client.get_paginator("describe_cache_engine_versions")
        describe_cache_parameter_groups_paginator: DescribeCacheParameterGroupsPaginator = client.get_paginator("describe_cache_parameter_groups")
        describe_cache_parameters_paginator: DescribeCacheParametersPaginator = client.get_paginator("describe_cache_parameters")
        describe_cache_security_groups_paginator: DescribeCacheSecurityGroupsPaginator = client.get_paginator("describe_cache_security_groups")
        describe_cache_subnet_groups_paginator: DescribeCacheSubnetGroupsPaginator = client.get_paginator("describe_cache_subnet_groups")
        describe_engine_default_parameters_paginator: DescribeEngineDefaultParametersPaginator = client.get_paginator("describe_engine_default_parameters")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_global_replication_groups_paginator: DescribeGlobalReplicationGroupsPaginator = client.get_paginator("describe_global_replication_groups")
        describe_replication_groups_paginator: DescribeReplicationGroupsPaginator = client.get_paginator("describe_replication_groups")
        describe_reserved_cache_nodes_offerings_paginator: DescribeReservedCacheNodesOfferingsPaginator = client.get_paginator("describe_reserved_cache_nodes_offerings")
        describe_reserved_cache_nodes_paginator: DescribeReservedCacheNodesPaginator = client.get_paginator("describe_reserved_cache_nodes")
        describe_serverless_cache_snapshots_paginator: DescribeServerlessCacheSnapshotsPaginator = client.get_paginator("describe_serverless_cache_snapshots")
        describe_serverless_caches_paginator: DescribeServerlessCachesPaginator = client.get_paginator("describe_serverless_caches")
        describe_service_updates_paginator: DescribeServiceUpdatesPaginator = client.get_paginator("describe_service_updates")
        describe_snapshots_paginator: DescribeSnapshotsPaginator = client.get_paginator("describe_snapshots")
        describe_update_actions_paginator: DescribeUpdateActionsPaginator = client.get_paginator("describe_update_actions")
        describe_user_groups_paginator: DescribeUserGroupsPaginator = client.get_paginator("describe_user_groups")
        describe_users_paginator: DescribeUsersPaginator = client.get_paginator("describe_users")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    CacheClusterMessageTypeDef,
    CacheEngineVersionMessageTypeDef,
    CacheParameterGroupDetailsTypeDef,
    CacheParameterGroupsMessageTypeDef,
    CacheSecurityGroupMessageTypeDef,
    CacheSubnetGroupMessageTypeDef,
    DescribeCacheClustersMessageDescribeCacheClustersPaginateTypeDef,
    DescribeCacheEngineVersionsMessageDescribeCacheEngineVersionsPaginateTypeDef,
    DescribeCacheParameterGroupsMessageDescribeCacheParameterGroupsPaginateTypeDef,
    DescribeCacheParametersMessageDescribeCacheParametersPaginateTypeDef,
    DescribeCacheSecurityGroupsMessageDescribeCacheSecurityGroupsPaginateTypeDef,
    DescribeCacheSubnetGroupsMessageDescribeCacheSubnetGroupsPaginateTypeDef,
    DescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef,
    DescribeEngineDefaultParametersResultTypeDef,
    DescribeEventsMessageDescribeEventsPaginateTypeDef,
    DescribeGlobalReplicationGroupsMessageDescribeGlobalReplicationGroupsPaginateTypeDef,
    DescribeGlobalReplicationGroupsResultTypeDef,
    DescribeReplicationGroupsMessageDescribeReplicationGroupsPaginateTypeDef,
    DescribeReservedCacheNodesMessageDescribeReservedCacheNodesPaginateTypeDef,
    DescribeReservedCacheNodesOfferingsMessageDescribeReservedCacheNodesOfferingsPaginateTypeDef,
    DescribeServerlessCacheSnapshotsRequestDescribeServerlessCacheSnapshotsPaginateTypeDef,
    DescribeServerlessCacheSnapshotsResponseTypeDef,
    DescribeServerlessCachesRequestDescribeServerlessCachesPaginateTypeDef,
    DescribeServerlessCachesResponseTypeDef,
    DescribeServiceUpdatesMessageDescribeServiceUpdatesPaginateTypeDef,
    DescribeSnapshotsListMessageTypeDef,
    DescribeSnapshotsMessageDescribeSnapshotsPaginateTypeDef,
    DescribeUpdateActionsMessageDescribeUpdateActionsPaginateTypeDef,
    DescribeUserGroupsMessageDescribeUserGroupsPaginateTypeDef,
    DescribeUserGroupsResultTypeDef,
    DescribeUsersMessageDescribeUsersPaginateTypeDef,
    DescribeUsersResultTypeDef,
    EventsMessageTypeDef,
    ReplicationGroupMessageTypeDef,
    ReservedCacheNodeMessageTypeDef,
    ReservedCacheNodesOfferingMessageTypeDef,
    ServiceUpdatesMessageTypeDef,
    UpdateActionsMessageTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeCacheClustersPaginator",
    "DescribeCacheEngineVersionsPaginator",
    "DescribeCacheParameterGroupsPaginator",
    "DescribeCacheParametersPaginator",
    "DescribeCacheSecurityGroupsPaginator",
    "DescribeCacheSubnetGroupsPaginator",
    "DescribeEngineDefaultParametersPaginator",
    "DescribeEventsPaginator",
    "DescribeGlobalReplicationGroupsPaginator",
    "DescribeReplicationGroupsPaginator",
    "DescribeReservedCacheNodesOfferingsPaginator",
    "DescribeReservedCacheNodesPaginator",
    "DescribeServerlessCacheSnapshotsPaginator",
    "DescribeServerlessCachesPaginator",
    "DescribeServiceUpdatesPaginator",
    "DescribeSnapshotsPaginator",
    "DescribeUpdateActionsPaginator",
    "DescribeUserGroupsPaginator",
    "DescribeUsersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeCacheClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheClusters.html#ElastiCache.Paginator.DescribeCacheClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecacheclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeCacheClustersMessageDescribeCacheClustersPaginateTypeDef]
    ) -> AsyncIterator[CacheClusterMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheClusters.html#ElastiCache.Paginator.DescribeCacheClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecacheclusterspaginator)
        """

class DescribeCacheEngineVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheEngineVersions.html#ElastiCache.Paginator.DescribeCacheEngineVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecacheengineversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeCacheEngineVersionsMessageDescribeCacheEngineVersionsPaginateTypeDef
        ],
    ) -> AsyncIterator[CacheEngineVersionMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheEngineVersions.html#ElastiCache.Paginator.DescribeCacheEngineVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecacheengineversionspaginator)
        """

class DescribeCacheParameterGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheParameterGroups.html#ElastiCache.Paginator.DescribeCacheParameterGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecacheparametergroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeCacheParameterGroupsMessageDescribeCacheParameterGroupsPaginateTypeDef
        ],
    ) -> AsyncIterator[CacheParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheParameterGroups.html#ElastiCache.Paginator.DescribeCacheParameterGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecacheparametergroupspaginator)
        """

class DescribeCacheParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheParameters.html#ElastiCache.Paginator.DescribeCacheParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecacheparameterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeCacheParametersMessageDescribeCacheParametersPaginateTypeDef]
    ) -> AsyncIterator[CacheParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheParameters.html#ElastiCache.Paginator.DescribeCacheParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecacheparameterspaginator)
        """

class DescribeCacheSecurityGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheSecurityGroups.html#ElastiCache.Paginator.DescribeCacheSecurityGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecachesecuritygroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeCacheSecurityGroupsMessageDescribeCacheSecurityGroupsPaginateTypeDef
        ],
    ) -> AsyncIterator[CacheSecurityGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheSecurityGroups.html#ElastiCache.Paginator.DescribeCacheSecurityGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecachesecuritygroupspaginator)
        """

class DescribeCacheSubnetGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheSubnetGroups.html#ElastiCache.Paginator.DescribeCacheSubnetGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecachesubnetgroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeCacheSubnetGroupsMessageDescribeCacheSubnetGroupsPaginateTypeDef],
    ) -> AsyncIterator[CacheSubnetGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeCacheSubnetGroups.html#ElastiCache.Paginator.DescribeCacheSubnetGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describecachesubnetgroupspaginator)
        """

class DescribeEngineDefaultParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeEngineDefaultParameters.html#ElastiCache.Paginator.DescribeEngineDefaultParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeenginedefaultparameterspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeEngineDefaultParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeEngineDefaultParameters.html#ElastiCache.Paginator.DescribeEngineDefaultParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeenginedefaultparameterspaginator)
        """

class DescribeEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeEvents.html#ElastiCache.Paginator.DescribeEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeeventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEventsMessageDescribeEventsPaginateTypeDef]
    ) -> AsyncIterator[EventsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeEvents.html#ElastiCache.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeeventspaginator)
        """

class DescribeGlobalReplicationGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeGlobalReplicationGroups.html#ElastiCache.Paginator.DescribeGlobalReplicationGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeglobalreplicationgroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeGlobalReplicationGroupsMessageDescribeGlobalReplicationGroupsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeGlobalReplicationGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeGlobalReplicationGroups.html#ElastiCache.Paginator.DescribeGlobalReplicationGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeglobalreplicationgroupspaginator)
        """

class DescribeReplicationGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReplicationGroups.html#ElastiCache.Paginator.DescribeReplicationGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describereplicationgroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeReplicationGroupsMessageDescribeReplicationGroupsPaginateTypeDef],
    ) -> AsyncIterator[ReplicationGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReplicationGroups.html#ElastiCache.Paginator.DescribeReplicationGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describereplicationgroupspaginator)
        """

class DescribeReservedCacheNodesOfferingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReservedCacheNodesOfferings.html#ElastiCache.Paginator.DescribeReservedCacheNodesOfferings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describereservedcachenodesofferingspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReservedCacheNodesOfferingsMessageDescribeReservedCacheNodesOfferingsPaginateTypeDef
        ],
    ) -> AsyncIterator[ReservedCacheNodesOfferingMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReservedCacheNodesOfferings.html#ElastiCache.Paginator.DescribeReservedCacheNodesOfferings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describereservedcachenodesofferingspaginator)
        """

class DescribeReservedCacheNodesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReservedCacheNodes.html#ElastiCache.Paginator.DescribeReservedCacheNodes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describereservedcachenodespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReservedCacheNodesMessageDescribeReservedCacheNodesPaginateTypeDef
        ],
    ) -> AsyncIterator[ReservedCacheNodeMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeReservedCacheNodes.html#ElastiCache.Paginator.DescribeReservedCacheNodes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describereservedcachenodespaginator)
        """

class DescribeServerlessCacheSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServerlessCacheSnapshots.html#ElastiCache.Paginator.DescribeServerlessCacheSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeserverlesscachesnapshotspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeServerlessCacheSnapshotsRequestDescribeServerlessCacheSnapshotsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeServerlessCacheSnapshotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServerlessCacheSnapshots.html#ElastiCache.Paginator.DescribeServerlessCacheSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeserverlesscachesnapshotspaginator)
        """

class DescribeServerlessCachesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServerlessCaches.html#ElastiCache.Paginator.DescribeServerlessCaches)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeserverlesscachespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeServerlessCachesRequestDescribeServerlessCachesPaginateTypeDef],
    ) -> AsyncIterator[DescribeServerlessCachesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServerlessCaches.html#ElastiCache.Paginator.DescribeServerlessCaches.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeserverlesscachespaginator)
        """

class DescribeServiceUpdatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServiceUpdates.html#ElastiCache.Paginator.DescribeServiceUpdates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeserviceupdatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeServiceUpdatesMessageDescribeServiceUpdatesPaginateTypeDef]
    ) -> AsyncIterator[ServiceUpdatesMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeServiceUpdates.html#ElastiCache.Paginator.DescribeServiceUpdates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeserviceupdatespaginator)
        """

class DescribeSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeSnapshots.html#ElastiCache.Paginator.DescribeSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describesnapshotspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeSnapshotsMessageDescribeSnapshotsPaginateTypeDef]
    ) -> AsyncIterator[DescribeSnapshotsListMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeSnapshots.html#ElastiCache.Paginator.DescribeSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describesnapshotspaginator)
        """

class DescribeUpdateActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUpdateActions.html#ElastiCache.Paginator.DescribeUpdateActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeupdateactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeUpdateActionsMessageDescribeUpdateActionsPaginateTypeDef]
    ) -> AsyncIterator[UpdateActionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUpdateActions.html#ElastiCache.Paginator.DescribeUpdateActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeupdateactionspaginator)
        """

class DescribeUserGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUserGroups.html#ElastiCache.Paginator.DescribeUserGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeusergroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeUserGroupsMessageDescribeUserGroupsPaginateTypeDef]
    ) -> AsyncIterator[DescribeUserGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUserGroups.html#ElastiCache.Paginator.DescribeUserGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeusergroupspaginator)
        """

class DescribeUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUsers.html#ElastiCache.Paginator.DescribeUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeuserspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeUsersMessageDescribeUsersPaginateTypeDef]
    ) -> AsyncIterator[DescribeUsersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/paginator/DescribeUsers.html#ElastiCache.Paginator.DescribeUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/paginators/#describeuserspaginator)
        """
