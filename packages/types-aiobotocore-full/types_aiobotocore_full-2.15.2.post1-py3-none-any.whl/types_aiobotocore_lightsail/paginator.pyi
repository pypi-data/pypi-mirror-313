"""
Type annotations for lightsail service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lightsail.client import LightsailClient
    from types_aiobotocore_lightsail.paginator import (
        GetActiveNamesPaginator,
        GetBlueprintsPaginator,
        GetBundlesPaginator,
        GetCloudFormationStackRecordsPaginator,
        GetDiskSnapshotsPaginator,
        GetDisksPaginator,
        GetDomainsPaginator,
        GetExportSnapshotRecordsPaginator,
        GetInstanceSnapshotsPaginator,
        GetInstancesPaginator,
        GetKeyPairsPaginator,
        GetLoadBalancersPaginator,
        GetOperationsPaginator,
        GetRelationalDatabaseBlueprintsPaginator,
        GetRelationalDatabaseBundlesPaginator,
        GetRelationalDatabaseEventsPaginator,
        GetRelationalDatabaseParametersPaginator,
        GetRelationalDatabaseSnapshotsPaginator,
        GetRelationalDatabasesPaginator,
        GetStaticIpsPaginator,
    )

    session = get_session()
    with session.create_client("lightsail") as client:
        client: LightsailClient

        get_active_names_paginator: GetActiveNamesPaginator = client.get_paginator("get_active_names")
        get_blueprints_paginator: GetBlueprintsPaginator = client.get_paginator("get_blueprints")
        get_bundles_paginator: GetBundlesPaginator = client.get_paginator("get_bundles")
        get_cloud_formation_stack_records_paginator: GetCloudFormationStackRecordsPaginator = client.get_paginator("get_cloud_formation_stack_records")
        get_disk_snapshots_paginator: GetDiskSnapshotsPaginator = client.get_paginator("get_disk_snapshots")
        get_disks_paginator: GetDisksPaginator = client.get_paginator("get_disks")
        get_domains_paginator: GetDomainsPaginator = client.get_paginator("get_domains")
        get_export_snapshot_records_paginator: GetExportSnapshotRecordsPaginator = client.get_paginator("get_export_snapshot_records")
        get_instance_snapshots_paginator: GetInstanceSnapshotsPaginator = client.get_paginator("get_instance_snapshots")
        get_instances_paginator: GetInstancesPaginator = client.get_paginator("get_instances")
        get_key_pairs_paginator: GetKeyPairsPaginator = client.get_paginator("get_key_pairs")
        get_load_balancers_paginator: GetLoadBalancersPaginator = client.get_paginator("get_load_balancers")
        get_operations_paginator: GetOperationsPaginator = client.get_paginator("get_operations")
        get_relational_database_blueprints_paginator: GetRelationalDatabaseBlueprintsPaginator = client.get_paginator("get_relational_database_blueprints")
        get_relational_database_bundles_paginator: GetRelationalDatabaseBundlesPaginator = client.get_paginator("get_relational_database_bundles")
        get_relational_database_events_paginator: GetRelationalDatabaseEventsPaginator = client.get_paginator("get_relational_database_events")
        get_relational_database_parameters_paginator: GetRelationalDatabaseParametersPaginator = client.get_paginator("get_relational_database_parameters")
        get_relational_database_snapshots_paginator: GetRelationalDatabaseSnapshotsPaginator = client.get_paginator("get_relational_database_snapshots")
        get_relational_databases_paginator: GetRelationalDatabasesPaginator = client.get_paginator("get_relational_databases")
        get_static_ips_paginator: GetStaticIpsPaginator = client.get_paginator("get_static_ips")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetActiveNamesRequestGetActiveNamesPaginateTypeDef,
    GetActiveNamesResultTypeDef,
    GetBlueprintsRequestGetBlueprintsPaginateTypeDef,
    GetBlueprintsResultTypeDef,
    GetBundlesRequestGetBundlesPaginateTypeDef,
    GetBundlesResultTypeDef,
    GetCloudFormationStackRecordsRequestGetCloudFormationStackRecordsPaginateTypeDef,
    GetCloudFormationStackRecordsResultTypeDef,
    GetDiskSnapshotsRequestGetDiskSnapshotsPaginateTypeDef,
    GetDiskSnapshotsResultTypeDef,
    GetDisksRequestGetDisksPaginateTypeDef,
    GetDisksResultTypeDef,
    GetDomainsRequestGetDomainsPaginateTypeDef,
    GetDomainsResultTypeDef,
    GetExportSnapshotRecordsRequestGetExportSnapshotRecordsPaginateTypeDef,
    GetExportSnapshotRecordsResultTypeDef,
    GetInstanceSnapshotsRequestGetInstanceSnapshotsPaginateTypeDef,
    GetInstanceSnapshotsResultTypeDef,
    GetInstancesRequestGetInstancesPaginateTypeDef,
    GetInstancesResultTypeDef,
    GetKeyPairsRequestGetKeyPairsPaginateTypeDef,
    GetKeyPairsResultTypeDef,
    GetLoadBalancersRequestGetLoadBalancersPaginateTypeDef,
    GetLoadBalancersResultTypeDef,
    GetOperationsRequestGetOperationsPaginateTypeDef,
    GetOperationsResultTypeDef,
    GetRelationalDatabaseBlueprintsRequestGetRelationalDatabaseBlueprintsPaginateTypeDef,
    GetRelationalDatabaseBlueprintsResultTypeDef,
    GetRelationalDatabaseBundlesRequestGetRelationalDatabaseBundlesPaginateTypeDef,
    GetRelationalDatabaseBundlesResultTypeDef,
    GetRelationalDatabaseEventsRequestGetRelationalDatabaseEventsPaginateTypeDef,
    GetRelationalDatabaseEventsResultTypeDef,
    GetRelationalDatabaseParametersRequestGetRelationalDatabaseParametersPaginateTypeDef,
    GetRelationalDatabaseParametersResultTypeDef,
    GetRelationalDatabaseSnapshotsRequestGetRelationalDatabaseSnapshotsPaginateTypeDef,
    GetRelationalDatabaseSnapshotsResultTypeDef,
    GetRelationalDatabasesRequestGetRelationalDatabasesPaginateTypeDef,
    GetRelationalDatabasesResultTypeDef,
    GetStaticIpsRequestGetStaticIpsPaginateTypeDef,
    GetStaticIpsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetActiveNamesPaginator",
    "GetBlueprintsPaginator",
    "GetBundlesPaginator",
    "GetCloudFormationStackRecordsPaginator",
    "GetDiskSnapshotsPaginator",
    "GetDisksPaginator",
    "GetDomainsPaginator",
    "GetExportSnapshotRecordsPaginator",
    "GetInstanceSnapshotsPaginator",
    "GetInstancesPaginator",
    "GetKeyPairsPaginator",
    "GetLoadBalancersPaginator",
    "GetOperationsPaginator",
    "GetRelationalDatabaseBlueprintsPaginator",
    "GetRelationalDatabaseBundlesPaginator",
    "GetRelationalDatabaseEventsPaginator",
    "GetRelationalDatabaseParametersPaginator",
    "GetRelationalDatabaseSnapshotsPaginator",
    "GetRelationalDatabasesPaginator",
    "GetStaticIpsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetActiveNamesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetActiveNames.html#Lightsail.Paginator.GetActiveNames)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getactivenamespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetActiveNamesRequestGetActiveNamesPaginateTypeDef]
    ) -> AsyncIterator[GetActiveNamesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetActiveNames.html#Lightsail.Paginator.GetActiveNames.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getactivenamespaginator)
        """

class GetBlueprintsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetBlueprints.html#Lightsail.Paginator.GetBlueprints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getblueprintspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetBlueprintsRequestGetBlueprintsPaginateTypeDef]
    ) -> AsyncIterator[GetBlueprintsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetBlueprints.html#Lightsail.Paginator.GetBlueprints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getblueprintspaginator)
        """

class GetBundlesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetBundles.html#Lightsail.Paginator.GetBundles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getbundlespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetBundlesRequestGetBundlesPaginateTypeDef]
    ) -> AsyncIterator[GetBundlesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetBundles.html#Lightsail.Paginator.GetBundles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getbundlespaginator)
        """

class GetCloudFormationStackRecordsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetCloudFormationStackRecords.html#Lightsail.Paginator.GetCloudFormationStackRecords)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getcloudformationstackrecordspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetCloudFormationStackRecordsRequestGetCloudFormationStackRecordsPaginateTypeDef
        ],
    ) -> AsyncIterator[GetCloudFormationStackRecordsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetCloudFormationStackRecords.html#Lightsail.Paginator.GetCloudFormationStackRecords.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getcloudformationstackrecordspaginator)
        """

class GetDiskSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetDiskSnapshots.html#Lightsail.Paginator.GetDiskSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdisksnapshotspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDiskSnapshotsRequestGetDiskSnapshotsPaginateTypeDef]
    ) -> AsyncIterator[GetDiskSnapshotsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetDiskSnapshots.html#Lightsail.Paginator.GetDiskSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdisksnapshotspaginator)
        """

class GetDisksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetDisks.html#Lightsail.Paginator.GetDisks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdiskspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDisksRequestGetDisksPaginateTypeDef]
    ) -> AsyncIterator[GetDisksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetDisks.html#Lightsail.Paginator.GetDisks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdiskspaginator)
        """

class GetDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetDomains.html#Lightsail.Paginator.GetDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdomainspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDomainsRequestGetDomainsPaginateTypeDef]
    ) -> AsyncIterator[GetDomainsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetDomains.html#Lightsail.Paginator.GetDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdomainspaginator)
        """

class GetExportSnapshotRecordsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetExportSnapshotRecords.html#Lightsail.Paginator.GetExportSnapshotRecords)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getexportsnapshotrecordspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[GetExportSnapshotRecordsRequestGetExportSnapshotRecordsPaginateTypeDef],
    ) -> AsyncIterator[GetExportSnapshotRecordsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetExportSnapshotRecords.html#Lightsail.Paginator.GetExportSnapshotRecords.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getexportsnapshotrecordspaginator)
        """

class GetInstanceSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetInstanceSnapshots.html#Lightsail.Paginator.GetInstanceSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getinstancesnapshotspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetInstanceSnapshotsRequestGetInstanceSnapshotsPaginateTypeDef]
    ) -> AsyncIterator[GetInstanceSnapshotsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetInstanceSnapshots.html#Lightsail.Paginator.GetInstanceSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getinstancesnapshotspaginator)
        """

class GetInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetInstances.html#Lightsail.Paginator.GetInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getinstancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetInstancesRequestGetInstancesPaginateTypeDef]
    ) -> AsyncIterator[GetInstancesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetInstances.html#Lightsail.Paginator.GetInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getinstancespaginator)
        """

class GetKeyPairsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetKeyPairs.html#Lightsail.Paginator.GetKeyPairs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getkeypairspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetKeyPairsRequestGetKeyPairsPaginateTypeDef]
    ) -> AsyncIterator[GetKeyPairsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetKeyPairs.html#Lightsail.Paginator.GetKeyPairs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getkeypairspaginator)
        """

class GetLoadBalancersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetLoadBalancers.html#Lightsail.Paginator.GetLoadBalancers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getloadbalancerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetLoadBalancersRequestGetLoadBalancersPaginateTypeDef]
    ) -> AsyncIterator[GetLoadBalancersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetLoadBalancers.html#Lightsail.Paginator.GetLoadBalancers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getloadbalancerspaginator)
        """

class GetOperationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetOperations.html#Lightsail.Paginator.GetOperations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getoperationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetOperationsRequestGetOperationsPaginateTypeDef]
    ) -> AsyncIterator[GetOperationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetOperations.html#Lightsail.Paginator.GetOperations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getoperationspaginator)
        """

class GetRelationalDatabaseBlueprintsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseBlueprints.html#Lightsail.Paginator.GetRelationalDatabaseBlueprints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseblueprintspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetRelationalDatabaseBlueprintsRequestGetRelationalDatabaseBlueprintsPaginateTypeDef
        ],
    ) -> AsyncIterator[GetRelationalDatabaseBlueprintsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseBlueprints.html#Lightsail.Paginator.GetRelationalDatabaseBlueprints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseblueprintspaginator)
        """

class GetRelationalDatabaseBundlesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseBundles.html#Lightsail.Paginator.GetRelationalDatabaseBundles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasebundlespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetRelationalDatabaseBundlesRequestGetRelationalDatabaseBundlesPaginateTypeDef
        ],
    ) -> AsyncIterator[GetRelationalDatabaseBundlesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseBundles.html#Lightsail.Paginator.GetRelationalDatabaseBundles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasebundlespaginator)
        """

class GetRelationalDatabaseEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseEvents.html#Lightsail.Paginator.GetRelationalDatabaseEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseeventspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetRelationalDatabaseEventsRequestGetRelationalDatabaseEventsPaginateTypeDef
        ],
    ) -> AsyncIterator[GetRelationalDatabaseEventsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseEvents.html#Lightsail.Paginator.GetRelationalDatabaseEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseeventspaginator)
        """

class GetRelationalDatabaseParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseParameters.html#Lightsail.Paginator.GetRelationalDatabaseParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseparameterspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetRelationalDatabaseParametersRequestGetRelationalDatabaseParametersPaginateTypeDef
        ],
    ) -> AsyncIterator[GetRelationalDatabaseParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseParameters.html#Lightsail.Paginator.GetRelationalDatabaseParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseparameterspaginator)
        """

class GetRelationalDatabaseSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseSnapshots.html#Lightsail.Paginator.GetRelationalDatabaseSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasesnapshotspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetRelationalDatabaseSnapshotsRequestGetRelationalDatabaseSnapshotsPaginateTypeDef
        ],
    ) -> AsyncIterator[GetRelationalDatabaseSnapshotsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabaseSnapshots.html#Lightsail.Paginator.GetRelationalDatabaseSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasesnapshotspaginator)
        """

class GetRelationalDatabasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabases.html#Lightsail.Paginator.GetRelationalDatabases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetRelationalDatabasesRequestGetRelationalDatabasesPaginateTypeDef]
    ) -> AsyncIterator[GetRelationalDatabasesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetRelationalDatabases.html#Lightsail.Paginator.GetRelationalDatabases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasespaginator)
        """

class GetStaticIpsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetStaticIps.html#Lightsail.Paginator.GetStaticIps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getstaticipspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetStaticIpsRequestGetStaticIpsPaginateTypeDef]
    ) -> AsyncIterator[GetStaticIpsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/paginator/GetStaticIps.html#Lightsail.Paginator.GetStaticIps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getstaticipspaginator)
        """
