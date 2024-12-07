"""
Type annotations for redshift service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_redshift.client import RedshiftClient
    from types_aiobotocore_redshift.paginator import (
        DescribeClusterDbRevisionsPaginator,
        DescribeClusterParameterGroupsPaginator,
        DescribeClusterParametersPaginator,
        DescribeClusterSecurityGroupsPaginator,
        DescribeClusterSnapshotsPaginator,
        DescribeClusterSubnetGroupsPaginator,
        DescribeClusterTracksPaginator,
        DescribeClusterVersionsPaginator,
        DescribeClustersPaginator,
        DescribeCustomDomainAssociationsPaginator,
        DescribeDataSharesForConsumerPaginator,
        DescribeDataSharesForProducerPaginator,
        DescribeDataSharesPaginator,
        DescribeDefaultClusterParametersPaginator,
        DescribeEndpointAccessPaginator,
        DescribeEndpointAuthorizationPaginator,
        DescribeEventSubscriptionsPaginator,
        DescribeEventsPaginator,
        DescribeHsmClientCertificatesPaginator,
        DescribeHsmConfigurationsPaginator,
        DescribeInboundIntegrationsPaginator,
        DescribeNodeConfigurationOptionsPaginator,
        DescribeOrderableClusterOptionsPaginator,
        DescribeRedshiftIdcApplicationsPaginator,
        DescribeReservedNodeExchangeStatusPaginator,
        DescribeReservedNodeOfferingsPaginator,
        DescribeReservedNodesPaginator,
        DescribeScheduledActionsPaginator,
        DescribeSnapshotCopyGrantsPaginator,
        DescribeSnapshotSchedulesPaginator,
        DescribeTableRestoreStatusPaginator,
        DescribeTagsPaginator,
        DescribeUsageLimitsPaginator,
        GetReservedNodeExchangeConfigurationOptionsPaginator,
        GetReservedNodeExchangeOfferingsPaginator,
        ListRecommendationsPaginator,
    )

    session = get_session()
    with session.create_client("redshift") as client:
        client: RedshiftClient

        describe_cluster_db_revisions_paginator: DescribeClusterDbRevisionsPaginator = client.get_paginator("describe_cluster_db_revisions")
        describe_cluster_parameter_groups_paginator: DescribeClusterParameterGroupsPaginator = client.get_paginator("describe_cluster_parameter_groups")
        describe_cluster_parameters_paginator: DescribeClusterParametersPaginator = client.get_paginator("describe_cluster_parameters")
        describe_cluster_security_groups_paginator: DescribeClusterSecurityGroupsPaginator = client.get_paginator("describe_cluster_security_groups")
        describe_cluster_snapshots_paginator: DescribeClusterSnapshotsPaginator = client.get_paginator("describe_cluster_snapshots")
        describe_cluster_subnet_groups_paginator: DescribeClusterSubnetGroupsPaginator = client.get_paginator("describe_cluster_subnet_groups")
        describe_cluster_tracks_paginator: DescribeClusterTracksPaginator = client.get_paginator("describe_cluster_tracks")
        describe_cluster_versions_paginator: DescribeClusterVersionsPaginator = client.get_paginator("describe_cluster_versions")
        describe_clusters_paginator: DescribeClustersPaginator = client.get_paginator("describe_clusters")
        describe_custom_domain_associations_paginator: DescribeCustomDomainAssociationsPaginator = client.get_paginator("describe_custom_domain_associations")
        describe_data_shares_for_consumer_paginator: DescribeDataSharesForConsumerPaginator = client.get_paginator("describe_data_shares_for_consumer")
        describe_data_shares_for_producer_paginator: DescribeDataSharesForProducerPaginator = client.get_paginator("describe_data_shares_for_producer")
        describe_data_shares_paginator: DescribeDataSharesPaginator = client.get_paginator("describe_data_shares")
        describe_default_cluster_parameters_paginator: DescribeDefaultClusterParametersPaginator = client.get_paginator("describe_default_cluster_parameters")
        describe_endpoint_access_paginator: DescribeEndpointAccessPaginator = client.get_paginator("describe_endpoint_access")
        describe_endpoint_authorization_paginator: DescribeEndpointAuthorizationPaginator = client.get_paginator("describe_endpoint_authorization")
        describe_event_subscriptions_paginator: DescribeEventSubscriptionsPaginator = client.get_paginator("describe_event_subscriptions")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_hsm_client_certificates_paginator: DescribeHsmClientCertificatesPaginator = client.get_paginator("describe_hsm_client_certificates")
        describe_hsm_configurations_paginator: DescribeHsmConfigurationsPaginator = client.get_paginator("describe_hsm_configurations")
        describe_inbound_integrations_paginator: DescribeInboundIntegrationsPaginator = client.get_paginator("describe_inbound_integrations")
        describe_node_configuration_options_paginator: DescribeNodeConfigurationOptionsPaginator = client.get_paginator("describe_node_configuration_options")
        describe_orderable_cluster_options_paginator: DescribeOrderableClusterOptionsPaginator = client.get_paginator("describe_orderable_cluster_options")
        describe_redshift_idc_applications_paginator: DescribeRedshiftIdcApplicationsPaginator = client.get_paginator("describe_redshift_idc_applications")
        describe_reserved_node_exchange_status_paginator: DescribeReservedNodeExchangeStatusPaginator = client.get_paginator("describe_reserved_node_exchange_status")
        describe_reserved_node_offerings_paginator: DescribeReservedNodeOfferingsPaginator = client.get_paginator("describe_reserved_node_offerings")
        describe_reserved_nodes_paginator: DescribeReservedNodesPaginator = client.get_paginator("describe_reserved_nodes")
        describe_scheduled_actions_paginator: DescribeScheduledActionsPaginator = client.get_paginator("describe_scheduled_actions")
        describe_snapshot_copy_grants_paginator: DescribeSnapshotCopyGrantsPaginator = client.get_paginator("describe_snapshot_copy_grants")
        describe_snapshot_schedules_paginator: DescribeSnapshotSchedulesPaginator = client.get_paginator("describe_snapshot_schedules")
        describe_table_restore_status_paginator: DescribeTableRestoreStatusPaginator = client.get_paginator("describe_table_restore_status")
        describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
        describe_usage_limits_paginator: DescribeUsageLimitsPaginator = client.get_paginator("describe_usage_limits")
        get_reserved_node_exchange_configuration_options_paginator: GetReservedNodeExchangeConfigurationOptionsPaginator = client.get_paginator("get_reserved_node_exchange_configuration_options")
        get_reserved_node_exchange_offerings_paginator: GetReservedNodeExchangeOfferingsPaginator = client.get_paginator("get_reserved_node_exchange_offerings")
        list_recommendations_paginator: ListRecommendationsPaginator = client.get_paginator("list_recommendations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ClusterDbRevisionsMessageTypeDef,
    ClusterParameterGroupDetailsTypeDef,
    ClusterParameterGroupsMessageTypeDef,
    ClusterSecurityGroupMessageTypeDef,
    ClustersMessageTypeDef,
    ClusterSubnetGroupMessageTypeDef,
    ClusterVersionsMessageTypeDef,
    CustomDomainAssociationsMessageTypeDef,
    DescribeClusterDbRevisionsMessageDescribeClusterDbRevisionsPaginateTypeDef,
    DescribeClusterParameterGroupsMessageDescribeClusterParameterGroupsPaginateTypeDef,
    DescribeClusterParametersMessageDescribeClusterParametersPaginateTypeDef,
    DescribeClusterSecurityGroupsMessageDescribeClusterSecurityGroupsPaginateTypeDef,
    DescribeClustersMessageDescribeClustersPaginateTypeDef,
    DescribeClusterSnapshotsMessageDescribeClusterSnapshotsPaginateTypeDef,
    DescribeClusterSubnetGroupsMessageDescribeClusterSubnetGroupsPaginateTypeDef,
    DescribeClusterTracksMessageDescribeClusterTracksPaginateTypeDef,
    DescribeClusterVersionsMessageDescribeClusterVersionsPaginateTypeDef,
    DescribeCustomDomainAssociationsMessageDescribeCustomDomainAssociationsPaginateTypeDef,
    DescribeDataSharesForConsumerMessageDescribeDataSharesForConsumerPaginateTypeDef,
    DescribeDataSharesForConsumerResultTypeDef,
    DescribeDataSharesForProducerMessageDescribeDataSharesForProducerPaginateTypeDef,
    DescribeDataSharesForProducerResultTypeDef,
    DescribeDataSharesMessageDescribeDataSharesPaginateTypeDef,
    DescribeDataSharesResultTypeDef,
    DescribeDefaultClusterParametersMessageDescribeDefaultClusterParametersPaginateTypeDef,
    DescribeDefaultClusterParametersResultTypeDef,
    DescribeEndpointAccessMessageDescribeEndpointAccessPaginateTypeDef,
    DescribeEndpointAuthorizationMessageDescribeEndpointAuthorizationPaginateTypeDef,
    DescribeEventsMessageDescribeEventsPaginateTypeDef,
    DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef,
    DescribeHsmClientCertificatesMessageDescribeHsmClientCertificatesPaginateTypeDef,
    DescribeHsmConfigurationsMessageDescribeHsmConfigurationsPaginateTypeDef,
    DescribeInboundIntegrationsMessageDescribeInboundIntegrationsPaginateTypeDef,
    DescribeNodeConfigurationOptionsMessageDescribeNodeConfigurationOptionsPaginateTypeDef,
    DescribeOrderableClusterOptionsMessageDescribeOrderableClusterOptionsPaginateTypeDef,
    DescribeRedshiftIdcApplicationsMessageDescribeRedshiftIdcApplicationsPaginateTypeDef,
    DescribeRedshiftIdcApplicationsResultTypeDef,
    DescribeReservedNodeExchangeStatusInputMessageDescribeReservedNodeExchangeStatusPaginateTypeDef,
    DescribeReservedNodeExchangeStatusOutputMessageTypeDef,
    DescribeReservedNodeOfferingsMessageDescribeReservedNodeOfferingsPaginateTypeDef,
    DescribeReservedNodesMessageDescribeReservedNodesPaginateTypeDef,
    DescribeScheduledActionsMessageDescribeScheduledActionsPaginateTypeDef,
    DescribeSnapshotCopyGrantsMessageDescribeSnapshotCopyGrantsPaginateTypeDef,
    DescribeSnapshotSchedulesMessageDescribeSnapshotSchedulesPaginateTypeDef,
    DescribeSnapshotSchedulesOutputMessageTypeDef,
    DescribeTableRestoreStatusMessageDescribeTableRestoreStatusPaginateTypeDef,
    DescribeTagsMessageDescribeTagsPaginateTypeDef,
    DescribeUsageLimitsMessageDescribeUsageLimitsPaginateTypeDef,
    EndpointAccessListTypeDef,
    EndpointAuthorizationListTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    GetReservedNodeExchangeConfigurationOptionsInputMessageGetReservedNodeExchangeConfigurationOptionsPaginateTypeDef,
    GetReservedNodeExchangeConfigurationOptionsOutputMessageTypeDef,
    GetReservedNodeExchangeOfferingsInputMessageGetReservedNodeExchangeOfferingsPaginateTypeDef,
    GetReservedNodeExchangeOfferingsOutputMessageTypeDef,
    HsmClientCertificateMessageTypeDef,
    HsmConfigurationMessageTypeDef,
    InboundIntegrationsMessageTypeDef,
    ListRecommendationsMessageListRecommendationsPaginateTypeDef,
    ListRecommendationsResultTypeDef,
    NodeConfigurationOptionsMessageTypeDef,
    OrderableClusterOptionsMessageTypeDef,
    ReservedNodeOfferingsMessageTypeDef,
    ReservedNodesMessageTypeDef,
    ScheduledActionsMessageTypeDef,
    SnapshotCopyGrantMessageTypeDef,
    SnapshotMessageTypeDef,
    TableRestoreStatusMessageTypeDef,
    TaggedResourceListMessageTypeDef,
    TrackListMessageTypeDef,
    UsageLimitListTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeClusterDbRevisionsPaginator",
    "DescribeClusterParameterGroupsPaginator",
    "DescribeClusterParametersPaginator",
    "DescribeClusterSecurityGroupsPaginator",
    "DescribeClusterSnapshotsPaginator",
    "DescribeClusterSubnetGroupsPaginator",
    "DescribeClusterTracksPaginator",
    "DescribeClusterVersionsPaginator",
    "DescribeClustersPaginator",
    "DescribeCustomDomainAssociationsPaginator",
    "DescribeDataSharesForConsumerPaginator",
    "DescribeDataSharesForProducerPaginator",
    "DescribeDataSharesPaginator",
    "DescribeDefaultClusterParametersPaginator",
    "DescribeEndpointAccessPaginator",
    "DescribeEndpointAuthorizationPaginator",
    "DescribeEventSubscriptionsPaginator",
    "DescribeEventsPaginator",
    "DescribeHsmClientCertificatesPaginator",
    "DescribeHsmConfigurationsPaginator",
    "DescribeInboundIntegrationsPaginator",
    "DescribeNodeConfigurationOptionsPaginator",
    "DescribeOrderableClusterOptionsPaginator",
    "DescribeRedshiftIdcApplicationsPaginator",
    "DescribeReservedNodeExchangeStatusPaginator",
    "DescribeReservedNodeOfferingsPaginator",
    "DescribeReservedNodesPaginator",
    "DescribeScheduledActionsPaginator",
    "DescribeSnapshotCopyGrantsPaginator",
    "DescribeSnapshotSchedulesPaginator",
    "DescribeTableRestoreStatusPaginator",
    "DescribeTagsPaginator",
    "DescribeUsageLimitsPaginator",
    "GetReservedNodeExchangeConfigurationOptionsPaginator",
    "GetReservedNodeExchangeOfferingsPaginator",
    "ListRecommendationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeClusterDbRevisionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterDbRevisions.html#Redshift.Paginator.DescribeClusterDbRevisions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclusterdbrevisionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeClusterDbRevisionsMessageDescribeClusterDbRevisionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ClusterDbRevisionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterDbRevisions.html#Redshift.Paginator.DescribeClusterDbRevisions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclusterdbrevisionspaginator)
        """

class DescribeClusterParameterGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterParameterGroups.html#Redshift.Paginator.DescribeClusterParameterGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclusterparametergroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeClusterParameterGroupsMessageDescribeClusterParameterGroupsPaginateTypeDef
        ],
    ) -> AsyncIterator[ClusterParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterParameterGroups.html#Redshift.Paginator.DescribeClusterParameterGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclusterparametergroupspaginator)
        """

class DescribeClusterParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterParameters.html#Redshift.Paginator.DescribeClusterParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclusterparameterspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeClusterParametersMessageDescribeClusterParametersPaginateTypeDef],
    ) -> AsyncIterator[ClusterParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterParameters.html#Redshift.Paginator.DescribeClusterParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclusterparameterspaginator)
        """

class DescribeClusterSecurityGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterSecurityGroups.html#Redshift.Paginator.DescribeClusterSecurityGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclustersecuritygroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeClusterSecurityGroupsMessageDescribeClusterSecurityGroupsPaginateTypeDef
        ],
    ) -> AsyncIterator[ClusterSecurityGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterSecurityGroups.html#Redshift.Paginator.DescribeClusterSecurityGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclustersecuritygroupspaginator)
        """

class DescribeClusterSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterSnapshots.html#Redshift.Paginator.DescribeClusterSnapshots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclustersnapshotspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeClusterSnapshotsMessageDescribeClusterSnapshotsPaginateTypeDef],
    ) -> AsyncIterator[SnapshotMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterSnapshots.html#Redshift.Paginator.DescribeClusterSnapshots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclustersnapshotspaginator)
        """

class DescribeClusterSubnetGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterSubnetGroups.html#Redshift.Paginator.DescribeClusterSubnetGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclustersubnetgroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeClusterSubnetGroupsMessageDescribeClusterSubnetGroupsPaginateTypeDef
        ],
    ) -> AsyncIterator[ClusterSubnetGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterSubnetGroups.html#Redshift.Paginator.DescribeClusterSubnetGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclustersubnetgroupspaginator)
        """

class DescribeClusterTracksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterTracks.html#Redshift.Paginator.DescribeClusterTracks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclustertrackspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeClusterTracksMessageDescribeClusterTracksPaginateTypeDef]
    ) -> AsyncIterator[TrackListMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterTracks.html#Redshift.Paginator.DescribeClusterTracks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclustertrackspaginator)
        """

class DescribeClusterVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterVersions.html#Redshift.Paginator.DescribeClusterVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclusterversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeClusterVersionsMessageDescribeClusterVersionsPaginateTypeDef]
    ) -> AsyncIterator[ClusterVersionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusterVersions.html#Redshift.Paginator.DescribeClusterVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclusterversionspaginator)
        """

class DescribeClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusters.html#Redshift.Paginator.DescribeClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeClustersMessageDescribeClustersPaginateTypeDef]
    ) -> AsyncIterator[ClustersMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeClusters.html#Redshift.Paginator.DescribeClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeclusterspaginator)
        """

class DescribeCustomDomainAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeCustomDomainAssociations.html#Redshift.Paginator.DescribeCustomDomainAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describecustomdomainassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeCustomDomainAssociationsMessageDescribeCustomDomainAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[CustomDomainAssociationsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeCustomDomainAssociations.html#Redshift.Paginator.DescribeCustomDomainAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describecustomdomainassociationspaginator)
        """

class DescribeDataSharesForConsumerPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeDataSharesForConsumer.html#Redshift.Paginator.DescribeDataSharesForConsumer)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describedatasharesforconsumerpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDataSharesForConsumerMessageDescribeDataSharesForConsumerPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeDataSharesForConsumerResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeDataSharesForConsumer.html#Redshift.Paginator.DescribeDataSharesForConsumer.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describedatasharesforconsumerpaginator)
        """

class DescribeDataSharesForProducerPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeDataSharesForProducer.html#Redshift.Paginator.DescribeDataSharesForProducer)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describedatasharesforproducerpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDataSharesForProducerMessageDescribeDataSharesForProducerPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeDataSharesForProducerResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeDataSharesForProducer.html#Redshift.Paginator.DescribeDataSharesForProducer.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describedatasharesforproducerpaginator)
        """

class DescribeDataSharesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeDataShares.html#Redshift.Paginator.DescribeDataShares)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describedatasharespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeDataSharesMessageDescribeDataSharesPaginateTypeDef]
    ) -> AsyncIterator[DescribeDataSharesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeDataShares.html#Redshift.Paginator.DescribeDataShares.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describedatasharespaginator)
        """

class DescribeDefaultClusterParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeDefaultClusterParameters.html#Redshift.Paginator.DescribeDefaultClusterParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describedefaultclusterparameterspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDefaultClusterParametersMessageDescribeDefaultClusterParametersPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeDefaultClusterParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeDefaultClusterParameters.html#Redshift.Paginator.DescribeDefaultClusterParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describedefaultclusterparameterspaginator)
        """

class DescribeEndpointAccessPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeEndpointAccess.html#Redshift.Paginator.DescribeEndpointAccess)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeendpointaccesspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEndpointAccessMessageDescribeEndpointAccessPaginateTypeDef]
    ) -> AsyncIterator[EndpointAccessListTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeEndpointAccess.html#Redshift.Paginator.DescribeEndpointAccess.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeendpointaccesspaginator)
        """

class DescribeEndpointAuthorizationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeEndpointAuthorization.html#Redshift.Paginator.DescribeEndpointAuthorization)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeendpointauthorizationpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEndpointAuthorizationMessageDescribeEndpointAuthorizationPaginateTypeDef
        ],
    ) -> AsyncIterator[EndpointAuthorizationListTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeEndpointAuthorization.html#Redshift.Paginator.DescribeEndpointAuthorization.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeendpointauthorizationpaginator)
        """

class DescribeEventSubscriptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeEventSubscriptions.html#Redshift.Paginator.DescribeEventSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeeventsubscriptionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef
        ],
    ) -> AsyncIterator[EventSubscriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeEventSubscriptions.html#Redshift.Paginator.DescribeEventSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeeventsubscriptionspaginator)
        """

class DescribeEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeEvents.html#Redshift.Paginator.DescribeEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeeventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeEventsMessageDescribeEventsPaginateTypeDef]
    ) -> AsyncIterator[EventsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeEvents.html#Redshift.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeeventspaginator)
        """

class DescribeHsmClientCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeHsmClientCertificates.html#Redshift.Paginator.DescribeHsmClientCertificates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describehsmclientcertificatespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeHsmClientCertificatesMessageDescribeHsmClientCertificatesPaginateTypeDef
        ],
    ) -> AsyncIterator[HsmClientCertificateMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeHsmClientCertificates.html#Redshift.Paginator.DescribeHsmClientCertificates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describehsmclientcertificatespaginator)
        """

class DescribeHsmConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeHsmConfigurations.html#Redshift.Paginator.DescribeHsmConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describehsmconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeHsmConfigurationsMessageDescribeHsmConfigurationsPaginateTypeDef],
    ) -> AsyncIterator[HsmConfigurationMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeHsmConfigurations.html#Redshift.Paginator.DescribeHsmConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describehsmconfigurationspaginator)
        """

class DescribeInboundIntegrationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeInboundIntegrations.html#Redshift.Paginator.DescribeInboundIntegrations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeinboundintegrationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInboundIntegrationsMessageDescribeInboundIntegrationsPaginateTypeDef
        ],
    ) -> AsyncIterator[InboundIntegrationsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeInboundIntegrations.html#Redshift.Paginator.DescribeInboundIntegrations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeinboundintegrationspaginator)
        """

class DescribeNodeConfigurationOptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeNodeConfigurationOptions.html#Redshift.Paginator.DescribeNodeConfigurationOptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describenodeconfigurationoptionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeNodeConfigurationOptionsMessageDescribeNodeConfigurationOptionsPaginateTypeDef
        ],
    ) -> AsyncIterator[NodeConfigurationOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeNodeConfigurationOptions.html#Redshift.Paginator.DescribeNodeConfigurationOptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describenodeconfigurationoptionspaginator)
        """

class DescribeOrderableClusterOptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeOrderableClusterOptions.html#Redshift.Paginator.DescribeOrderableClusterOptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeorderableclusteroptionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeOrderableClusterOptionsMessageDescribeOrderableClusterOptionsPaginateTypeDef
        ],
    ) -> AsyncIterator[OrderableClusterOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeOrderableClusterOptions.html#Redshift.Paginator.DescribeOrderableClusterOptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeorderableclusteroptionspaginator)
        """

class DescribeRedshiftIdcApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeRedshiftIdcApplications.html#Redshift.Paginator.DescribeRedshiftIdcApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeredshiftidcapplicationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeRedshiftIdcApplicationsMessageDescribeRedshiftIdcApplicationsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeRedshiftIdcApplicationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeRedshiftIdcApplications.html#Redshift.Paginator.DescribeRedshiftIdcApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeredshiftidcapplicationspaginator)
        """

class DescribeReservedNodeExchangeStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeReservedNodeExchangeStatus.html#Redshift.Paginator.DescribeReservedNodeExchangeStatus)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describereservednodeexchangestatuspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReservedNodeExchangeStatusInputMessageDescribeReservedNodeExchangeStatusPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeReservedNodeExchangeStatusOutputMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeReservedNodeExchangeStatus.html#Redshift.Paginator.DescribeReservedNodeExchangeStatus.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describereservednodeexchangestatuspaginator)
        """

class DescribeReservedNodeOfferingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeReservedNodeOfferings.html#Redshift.Paginator.DescribeReservedNodeOfferings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describereservednodeofferingspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeReservedNodeOfferingsMessageDescribeReservedNodeOfferingsPaginateTypeDef
        ],
    ) -> AsyncIterator[ReservedNodeOfferingsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeReservedNodeOfferings.html#Redshift.Paginator.DescribeReservedNodeOfferings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describereservednodeofferingspaginator)
        """

class DescribeReservedNodesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeReservedNodes.html#Redshift.Paginator.DescribeReservedNodes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describereservednodespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeReservedNodesMessageDescribeReservedNodesPaginateTypeDef]
    ) -> AsyncIterator[ReservedNodesMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeReservedNodes.html#Redshift.Paginator.DescribeReservedNodes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describereservednodespaginator)
        """

class DescribeScheduledActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeScheduledActions.html#Redshift.Paginator.DescribeScheduledActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describescheduledactionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeScheduledActionsMessageDescribeScheduledActionsPaginateTypeDef],
    ) -> AsyncIterator[ScheduledActionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeScheduledActions.html#Redshift.Paginator.DescribeScheduledActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describescheduledactionspaginator)
        """

class DescribeSnapshotCopyGrantsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeSnapshotCopyGrants.html#Redshift.Paginator.DescribeSnapshotCopyGrants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describesnapshotcopygrantspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeSnapshotCopyGrantsMessageDescribeSnapshotCopyGrantsPaginateTypeDef
        ],
    ) -> AsyncIterator[SnapshotCopyGrantMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeSnapshotCopyGrants.html#Redshift.Paginator.DescribeSnapshotCopyGrants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describesnapshotcopygrantspaginator)
        """

class DescribeSnapshotSchedulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeSnapshotSchedules.html#Redshift.Paginator.DescribeSnapshotSchedules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describesnapshotschedulespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeSnapshotSchedulesMessageDescribeSnapshotSchedulesPaginateTypeDef],
    ) -> AsyncIterator[DescribeSnapshotSchedulesOutputMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeSnapshotSchedules.html#Redshift.Paginator.DescribeSnapshotSchedules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describesnapshotschedulespaginator)
        """

class DescribeTableRestoreStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeTableRestoreStatus.html#Redshift.Paginator.DescribeTableRestoreStatus)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describetablerestorestatuspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeTableRestoreStatusMessageDescribeTableRestoreStatusPaginateTypeDef
        ],
    ) -> AsyncIterator[TableRestoreStatusMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeTableRestoreStatus.html#Redshift.Paginator.DescribeTableRestoreStatus.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describetablerestorestatuspaginator)
        """

class DescribeTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeTags.html#Redshift.Paginator.DescribeTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describetagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeTagsMessageDescribeTagsPaginateTypeDef]
    ) -> AsyncIterator[TaggedResourceListMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeTags.html#Redshift.Paginator.DescribeTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describetagspaginator)
        """

class DescribeUsageLimitsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeUsageLimits.html#Redshift.Paginator.DescribeUsageLimits)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeusagelimitspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeUsageLimitsMessageDescribeUsageLimitsPaginateTypeDef]
    ) -> AsyncIterator[UsageLimitListTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/DescribeUsageLimits.html#Redshift.Paginator.DescribeUsageLimits.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#describeusagelimitspaginator)
        """

class GetReservedNodeExchangeConfigurationOptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/GetReservedNodeExchangeConfigurationOptions.html#Redshift.Paginator.GetReservedNodeExchangeConfigurationOptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#getreservednodeexchangeconfigurationoptionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetReservedNodeExchangeConfigurationOptionsInputMessageGetReservedNodeExchangeConfigurationOptionsPaginateTypeDef
        ],
    ) -> AsyncIterator[GetReservedNodeExchangeConfigurationOptionsOutputMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/GetReservedNodeExchangeConfigurationOptions.html#Redshift.Paginator.GetReservedNodeExchangeConfigurationOptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#getreservednodeexchangeconfigurationoptionspaginator)
        """

class GetReservedNodeExchangeOfferingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/GetReservedNodeExchangeOfferings.html#Redshift.Paginator.GetReservedNodeExchangeOfferings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#getreservednodeexchangeofferingspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetReservedNodeExchangeOfferingsInputMessageGetReservedNodeExchangeOfferingsPaginateTypeDef
        ],
    ) -> AsyncIterator[GetReservedNodeExchangeOfferingsOutputMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/GetReservedNodeExchangeOfferings.html#Redshift.Paginator.GetReservedNodeExchangeOfferings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#getreservednodeexchangeofferingspaginator)
        """

class ListRecommendationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/ListRecommendations.html#Redshift.Paginator.ListRecommendations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#listrecommendationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRecommendationsMessageListRecommendationsPaginateTypeDef]
    ) -> AsyncIterator[ListRecommendationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/paginator/ListRecommendations.html#Redshift.Paginator.ListRecommendations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/paginators/#listrecommendationspaginator)
        """
