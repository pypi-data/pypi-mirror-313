"""
Type annotations for docdb service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_docdb.client import DocDBClient
    from types_aiobotocore_docdb.paginator import (
        DescribeCertificatesPaginator,
        DescribeDBClusterParameterGroupsPaginator,
        DescribeDBClusterParametersPaginator,
        DescribeDBClusterSnapshotsPaginator,
        DescribeDBClustersPaginator,
        DescribeDBEngineVersionsPaginator,
        DescribeDBInstancesPaginator,
        DescribeDBSubnetGroupsPaginator,
        DescribeEventSubscriptionsPaginator,
        DescribeEventsPaginator,
        DescribeGlobalClustersPaginator,
        DescribeOrderableDBInstanceOptionsPaginator,
        DescribePendingMaintenanceActionsPaginator,
    )

    session = get_session()
    with session.create_client("docdb") as client:
        client: DocDBClient

        describe_certificates_paginator: DescribeCertificatesPaginator = client.get_paginator("describe_certificates")
        describe_db_cluster_parameter_groups_paginator: DescribeDBClusterParameterGroupsPaginator = client.get_paginator("describe_db_cluster_parameter_groups")
        describe_db_cluster_parameters_paginator: DescribeDBClusterParametersPaginator = client.get_paginator("describe_db_cluster_parameters")
        describe_db_cluster_snapshots_paginator: DescribeDBClusterSnapshotsPaginator = client.get_paginator("describe_db_cluster_snapshots")
        describe_db_clusters_paginator: DescribeDBClustersPaginator = client.get_paginator("describe_db_clusters")
        describe_db_engine_versions_paginator: DescribeDBEngineVersionsPaginator = client.get_paginator("describe_db_engine_versions")
        describe_db_instances_paginator: DescribeDBInstancesPaginator = client.get_paginator("describe_db_instances")
        describe_db_subnet_groups_paginator: DescribeDBSubnetGroupsPaginator = client.get_paginator("describe_db_subnet_groups")
        describe_event_subscriptions_paginator: DescribeEventSubscriptionsPaginator = client.get_paginator("describe_event_subscriptions")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_global_clusters_paginator: DescribeGlobalClustersPaginator = client.get_paginator("describe_global_clusters")
        describe_orderable_db_instance_options_paginator: DescribeOrderableDBInstanceOptionsPaginator = client.get_paginator("describe_orderable_db_instance_options")
        describe_pending_maintenance_actions_paginator: DescribePendingMaintenanceActionsPaginator = client.get_paginator("describe_pending_maintenance_actions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    CertificateMessageTypeDef,
    DBClusterMessageTypeDef,
    DBClusterParameterGroupDetailsTypeDef,
    DBClusterParameterGroupsMessageTypeDef,
    DBClusterSnapshotMessageTypeDef,
    DBEngineVersionMessageTypeDef,
    DBInstanceMessageTypeDef,
    DBSubnetGroupMessageTypeDef,
    DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef,
    DescribeDBClusterParameterGroupsMessageDescribeDBClusterParameterGroupsPaginateTypeDef,
    DescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef,
    DescribeDBClustersMessageDescribeDBClustersPaginateTypeDef,
    DescribeDBClusterSnapshotsMessageDescribeDBClusterSnapshotsPaginateTypeDef,
    DescribeDBEngineVersionsMessageDescribeDBEngineVersionsPaginateTypeDef,
    DescribeDBInstancesMessageDescribeDBInstancesPaginateTypeDef,
    DescribeDBSubnetGroupsMessageDescribeDBSubnetGroupsPaginateTypeDef,
    DescribeEventsMessageDescribeEventsPaginateTypeDef,
    DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef,
    DescribeGlobalClustersMessageDescribeGlobalClustersPaginateTypeDef,
    DescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef,
    DescribePendingMaintenanceActionsMessageDescribePendingMaintenanceActionsPaginateTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    GlobalClustersMessageTypeDef,
    OrderableDBInstanceOptionsMessageTypeDef,
    PendingMaintenanceActionsMessageTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeCertificatesPaginator",
    "DescribeDBClusterParameterGroupsPaginator",
    "DescribeDBClusterParametersPaginator",
    "DescribeDBClusterSnapshotsPaginator",
    "DescribeDBClustersPaginator",
    "DescribeDBEngineVersionsPaginator",
    "DescribeDBInstancesPaginator",
    "DescribeDBSubnetGroupsPaginator",
    "DescribeEventSubscriptionsPaginator",
    "DescribeEventsPaginator",
    "DescribeGlobalClustersPaginator",
    "DescribeOrderableDBInstanceOptionsPaginator",
    "DescribePendingMaintenanceActionsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeCertificates.html#DocDB.Paginator.DescribeCertificates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describecertificatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef]
    ) -> AsyncIterator[CertificateMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeCertificates.html#DocDB.Paginator.DescribeCertificates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describecertificatespaginator)
        """


class DescribeDBClusterParameterGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterParameterGroups.html#DocDB.Paginator.DescribeDBClusterParameterGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbclusterparametergroupspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDBClusterParameterGroupsMessageDescribeDBClusterParameterGroupsPaginateTypeDef
        ],
    ) -> AsyncIterator[DBClusterParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterParameterGroups.html#DocDB.Paginator.DescribeDBClusterParameterGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbclusterparametergroupspaginator)
        """


class DescribeDBClusterParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterParameters.html#DocDB.Paginator.DescribeDBClusterParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbclusterparameterspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef
        ],
    ) -> AsyncIterator[DBClusterParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterParameters.html#DocDB.Paginator.DescribeDBClusterParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbclusterparameterspaginator)
        """


class DescribeDBClusterSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterSnapshots.html#DocDB.Paginator.DescribeDBClusterSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbclustersnapshotspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDBClusterSnapshotsMessageDescribeDBClusterSnapshotsPaginateTypeDef
        ],
    ) -> AsyncIterator[DBClusterSnapshotMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusterSnapshots.html#DocDB.Paginator.DescribeDBClusterSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbclustersnapshotspaginator)
        """


class DescribeDBClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusters.html#DocDB.Paginator.DescribeDBClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbclusterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeDBClustersMessageDescribeDBClustersPaginateTypeDef]
    ) -> AsyncIterator[DBClusterMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBClusters.html#DocDB.Paginator.DescribeDBClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbclusterspaginator)
        """


class DescribeDBEngineVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBEngineVersions.html#DocDB.Paginator.DescribeDBEngineVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbengineversionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeDBEngineVersionsMessageDescribeDBEngineVersionsPaginateTypeDef],
    ) -> AsyncIterator[DBEngineVersionMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBEngineVersions.html#DocDB.Paginator.DescribeDBEngineVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbengineversionspaginator)
        """


class DescribeDBInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBInstances.html#DocDB.Paginator.DescribeDBInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbinstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeDBInstancesMessageDescribeDBInstancesPaginateTypeDef]
    ) -> AsyncIterator[DBInstanceMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBInstances.html#DocDB.Paginator.DescribeDBInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbinstancespaginator)
        """


class DescribeDBSubnetGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBSubnetGroups.html#DocDB.Paginator.DescribeDBSubnetGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbsubnetgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeDBSubnetGroupsMessageDescribeDBSubnetGroupsPaginateTypeDef]
    ) -> AsyncIterator[DBSubnetGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeDBSubnetGroups.html#DocDB.Paginator.DescribeDBSubnetGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describedbsubnetgroupspaginator)
        """


class DescribeEventSubscriptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeEventSubscriptions.html#DocDB.Paginator.DescribeEventSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describeeventsubscriptionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef
        ],
    ) -> AsyncIterator[EventSubscriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeEventSubscriptions.html#DocDB.Paginator.DescribeEventSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describeeventsubscriptionspaginator)
        """


class DescribeEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeEvents.html#DocDB.Paginator.DescribeEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describeeventspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeEventsMessageDescribeEventsPaginateTypeDef]
    ) -> AsyncIterator[EventsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeEvents.html#DocDB.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describeeventspaginator)
        """


class DescribeGlobalClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeGlobalClusters.html#DocDB.Paginator.DescribeGlobalClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describeglobalclusterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeGlobalClustersMessageDescribeGlobalClustersPaginateTypeDef]
    ) -> AsyncIterator[GlobalClustersMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeGlobalClusters.html#DocDB.Paginator.DescribeGlobalClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describeglobalclusterspaginator)
        """


class DescribeOrderableDBInstanceOptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeOrderableDBInstanceOptions.html#DocDB.Paginator.DescribeOrderableDBInstanceOptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describeorderabledbinstanceoptionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef
        ],
    ) -> AsyncIterator[OrderableDBInstanceOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribeOrderableDBInstanceOptions.html#DocDB.Paginator.DescribeOrderableDBInstanceOptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describeorderabledbinstanceoptionspaginator)
        """


class DescribePendingMaintenanceActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribePendingMaintenanceActions.html#DocDB.Paginator.DescribePendingMaintenanceActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describependingmaintenanceactionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribePendingMaintenanceActionsMessageDescribePendingMaintenanceActionsPaginateTypeDef
        ],
    ) -> AsyncIterator[PendingMaintenanceActionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb/paginator/DescribePendingMaintenanceActions.html#DocDB.Paginator.DescribePendingMaintenanceActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb/paginators/#describependingmaintenanceactionspaginator)
        """
