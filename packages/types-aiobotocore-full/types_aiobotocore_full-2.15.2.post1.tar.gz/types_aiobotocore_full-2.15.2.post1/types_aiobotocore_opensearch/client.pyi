"""
Type annotations for opensearch service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_opensearch.client import OpenSearchServiceClient

    session = get_session()
    async with session.create_client("opensearch") as client:
        client: OpenSearchServiceClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    AcceptInboundConnectionRequestRequestTypeDef,
    AcceptInboundConnectionResponseTypeDef,
    AddDataSourceRequestRequestTypeDef,
    AddDataSourceResponseTypeDef,
    AddTagsRequestRequestTypeDef,
    AssociatePackageRequestRequestTypeDef,
    AssociatePackageResponseTypeDef,
    AuthorizeVpcEndpointAccessRequestRequestTypeDef,
    AuthorizeVpcEndpointAccessResponseTypeDef,
    CancelDomainConfigChangeRequestRequestTypeDef,
    CancelDomainConfigChangeResponseTypeDef,
    CancelServiceSoftwareUpdateRequestRequestTypeDef,
    CancelServiceSoftwareUpdateResponseTypeDef,
    CreateDomainRequestRequestTypeDef,
    CreateDomainResponseTypeDef,
    CreateOutboundConnectionRequestRequestTypeDef,
    CreateOutboundConnectionResponseTypeDef,
    CreatePackageRequestRequestTypeDef,
    CreatePackageResponseTypeDef,
    CreateVpcEndpointRequestRequestTypeDef,
    CreateVpcEndpointResponseTypeDef,
    DeleteDataSourceRequestRequestTypeDef,
    DeleteDataSourceResponseTypeDef,
    DeleteDomainRequestRequestTypeDef,
    DeleteDomainResponseTypeDef,
    DeleteInboundConnectionRequestRequestTypeDef,
    DeleteInboundConnectionResponseTypeDef,
    DeleteOutboundConnectionRequestRequestTypeDef,
    DeleteOutboundConnectionResponseTypeDef,
    DeletePackageRequestRequestTypeDef,
    DeletePackageResponseTypeDef,
    DeleteVpcEndpointRequestRequestTypeDef,
    DeleteVpcEndpointResponseTypeDef,
    DescribeDomainAutoTunesRequestRequestTypeDef,
    DescribeDomainAutoTunesResponseTypeDef,
    DescribeDomainChangeProgressRequestRequestTypeDef,
    DescribeDomainChangeProgressResponseTypeDef,
    DescribeDomainConfigRequestRequestTypeDef,
    DescribeDomainConfigResponseTypeDef,
    DescribeDomainHealthRequestRequestTypeDef,
    DescribeDomainHealthResponseTypeDef,
    DescribeDomainNodesRequestRequestTypeDef,
    DescribeDomainNodesResponseTypeDef,
    DescribeDomainRequestRequestTypeDef,
    DescribeDomainResponseTypeDef,
    DescribeDomainsRequestRequestTypeDef,
    DescribeDomainsResponseTypeDef,
    DescribeDryRunProgressRequestRequestTypeDef,
    DescribeDryRunProgressResponseTypeDef,
    DescribeInboundConnectionsRequestRequestTypeDef,
    DescribeInboundConnectionsResponseTypeDef,
    DescribeInstanceTypeLimitsRequestRequestTypeDef,
    DescribeInstanceTypeLimitsResponseTypeDef,
    DescribeOutboundConnectionsRequestRequestTypeDef,
    DescribeOutboundConnectionsResponseTypeDef,
    DescribePackagesRequestRequestTypeDef,
    DescribePackagesResponseTypeDef,
    DescribeReservedInstanceOfferingsRequestRequestTypeDef,
    DescribeReservedInstanceOfferingsResponseTypeDef,
    DescribeReservedInstancesRequestRequestTypeDef,
    DescribeReservedInstancesResponseTypeDef,
    DescribeVpcEndpointsRequestRequestTypeDef,
    DescribeVpcEndpointsResponseTypeDef,
    DissociatePackageRequestRequestTypeDef,
    DissociatePackageResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCompatibleVersionsRequestRequestTypeDef,
    GetCompatibleVersionsResponseTypeDef,
    GetDataSourceRequestRequestTypeDef,
    GetDataSourceResponseTypeDef,
    GetDomainMaintenanceStatusRequestRequestTypeDef,
    GetDomainMaintenanceStatusResponseTypeDef,
    GetPackageVersionHistoryRequestRequestTypeDef,
    GetPackageVersionHistoryResponseTypeDef,
    GetUpgradeHistoryRequestRequestTypeDef,
    GetUpgradeHistoryResponseTypeDef,
    GetUpgradeStatusRequestRequestTypeDef,
    GetUpgradeStatusResponseTypeDef,
    ListDataSourcesRequestRequestTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDomainMaintenancesRequestRequestTypeDef,
    ListDomainMaintenancesResponseTypeDef,
    ListDomainNamesRequestRequestTypeDef,
    ListDomainNamesResponseTypeDef,
    ListDomainsForPackageRequestRequestTypeDef,
    ListDomainsForPackageResponseTypeDef,
    ListInstanceTypeDetailsRequestRequestTypeDef,
    ListInstanceTypeDetailsResponseTypeDef,
    ListPackagesForDomainRequestRequestTypeDef,
    ListPackagesForDomainResponseTypeDef,
    ListScheduledActionsRequestRequestTypeDef,
    ListScheduledActionsResponseTypeDef,
    ListTagsRequestRequestTypeDef,
    ListTagsResponseTypeDef,
    ListVersionsRequestRequestTypeDef,
    ListVersionsResponseTypeDef,
    ListVpcEndpointAccessRequestRequestTypeDef,
    ListVpcEndpointAccessResponseTypeDef,
    ListVpcEndpointsForDomainRequestRequestTypeDef,
    ListVpcEndpointsForDomainResponseTypeDef,
    ListVpcEndpointsRequestRequestTypeDef,
    ListVpcEndpointsResponseTypeDef,
    PurchaseReservedInstanceOfferingRequestRequestTypeDef,
    PurchaseReservedInstanceOfferingResponseTypeDef,
    RejectInboundConnectionRequestRequestTypeDef,
    RejectInboundConnectionResponseTypeDef,
    RemoveTagsRequestRequestTypeDef,
    RevokeVpcEndpointAccessRequestRequestTypeDef,
    StartDomainMaintenanceRequestRequestTypeDef,
    StartDomainMaintenanceResponseTypeDef,
    StartServiceSoftwareUpdateRequestRequestTypeDef,
    StartServiceSoftwareUpdateResponseTypeDef,
    UpdateDataSourceRequestRequestTypeDef,
    UpdateDataSourceResponseTypeDef,
    UpdateDomainConfigRequestRequestTypeDef,
    UpdateDomainConfigResponseTypeDef,
    UpdatePackageRequestRequestTypeDef,
    UpdatePackageResponseTypeDef,
    UpdateScheduledActionRequestRequestTypeDef,
    UpdateScheduledActionResponseTypeDef,
    UpdateVpcEndpointRequestRequestTypeDef,
    UpdateVpcEndpointResponseTypeDef,
    UpgradeDomainRequestRequestTypeDef,
    UpgradeDomainResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("OpenSearchServiceClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BaseException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DependencyFailureException: Type[BotocoreClientError]
    DisabledOperationException: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidPaginationTokenException: Type[BotocoreClientError]
    InvalidTypeException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    SlotNotAvailableException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class OpenSearchServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OpenSearchServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#close)
        """

    async def accept_inbound_connection(
        self, **kwargs: Unpack[AcceptInboundConnectionRequestRequestTypeDef]
    ) -> AcceptInboundConnectionResponseTypeDef:
        """
        Allows the destination Amazon OpenSearch Service domain owner to accept an
        inbound cross-cluster search connection request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/accept_inbound_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#accept_inbound_connection)
        """

    async def add_data_source(
        self, **kwargs: Unpack[AddDataSourceRequestRequestTypeDef]
    ) -> AddDataSourceResponseTypeDef:
        """
        Creates a new direct-query data source to the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/add_data_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#add_data_source)
        """

    async def add_tags(
        self, **kwargs: Unpack[AddTagsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches tags to an existing Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/add_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#add_tags)
        """

    async def associate_package(
        self, **kwargs: Unpack[AssociatePackageRequestRequestTypeDef]
    ) -> AssociatePackageResponseTypeDef:
        """
        Associates a package with an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/associate_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#associate_package)
        """

    async def authorize_vpc_endpoint_access(
        self, **kwargs: Unpack[AuthorizeVpcEndpointAccessRequestRequestTypeDef]
    ) -> AuthorizeVpcEndpointAccessResponseTypeDef:
        """
        Provides access to an Amazon OpenSearch Service domain through the use of an
        interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/authorize_vpc_endpoint_access.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#authorize_vpc_endpoint_access)
        """

    async def cancel_domain_config_change(
        self, **kwargs: Unpack[CancelDomainConfigChangeRequestRequestTypeDef]
    ) -> CancelDomainConfigChangeResponseTypeDef:
        """
        Cancels a pending configuration change on an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/cancel_domain_config_change.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#cancel_domain_config_change)
        """

    async def cancel_service_software_update(
        self, **kwargs: Unpack[CancelServiceSoftwareUpdateRequestRequestTypeDef]
    ) -> CancelServiceSoftwareUpdateResponseTypeDef:
        """
        Cancels a scheduled service software update for an Amazon OpenSearch Service
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/cancel_service_software_update.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#cancel_service_software_update)
        """

    async def create_domain(
        self, **kwargs: Unpack[CreateDomainRequestRequestTypeDef]
    ) -> CreateDomainResponseTypeDef:
        """
        Creates an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/create_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#create_domain)
        """

    async def create_outbound_connection(
        self, **kwargs: Unpack[CreateOutboundConnectionRequestRequestTypeDef]
    ) -> CreateOutboundConnectionResponseTypeDef:
        """
        Creates a new cross-cluster search connection from a source Amazon OpenSearch
        Service domain to a destination domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/create_outbound_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#create_outbound_connection)
        """

    async def create_package(
        self, **kwargs: Unpack[CreatePackageRequestRequestTypeDef]
    ) -> CreatePackageResponseTypeDef:
        """
        Creates a package for use with Amazon OpenSearch Service domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/create_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#create_package)
        """

    async def create_vpc_endpoint(
        self, **kwargs: Unpack[CreateVpcEndpointRequestRequestTypeDef]
    ) -> CreateVpcEndpointResponseTypeDef:
        """
        Creates an Amazon OpenSearch Service-managed VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/create_vpc_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#create_vpc_endpoint)
        """

    async def delete_data_source(
        self, **kwargs: Unpack[DeleteDataSourceRequestRequestTypeDef]
    ) -> DeleteDataSourceResponseTypeDef:
        """
        Deletes a direct-query data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/delete_data_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#delete_data_source)
        """

    async def delete_domain(
        self, **kwargs: Unpack[DeleteDomainRequestRequestTypeDef]
    ) -> DeleteDomainResponseTypeDef:
        """
        Deletes an Amazon OpenSearch Service domain and all of its data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/delete_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#delete_domain)
        """

    async def delete_inbound_connection(
        self, **kwargs: Unpack[DeleteInboundConnectionRequestRequestTypeDef]
    ) -> DeleteInboundConnectionResponseTypeDef:
        """
        Allows the destination Amazon OpenSearch Service domain owner to delete an
        existing inbound cross-cluster search connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/delete_inbound_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#delete_inbound_connection)
        """

    async def delete_outbound_connection(
        self, **kwargs: Unpack[DeleteOutboundConnectionRequestRequestTypeDef]
    ) -> DeleteOutboundConnectionResponseTypeDef:
        """
        Allows the source Amazon OpenSearch Service domain owner to delete an existing
        outbound cross-cluster search connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/delete_outbound_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#delete_outbound_connection)
        """

    async def delete_package(
        self, **kwargs: Unpack[DeletePackageRequestRequestTypeDef]
    ) -> DeletePackageResponseTypeDef:
        """
        Deletes an Amazon OpenSearch Service package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/delete_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#delete_package)
        """

    async def delete_vpc_endpoint(
        self, **kwargs: Unpack[DeleteVpcEndpointRequestRequestTypeDef]
    ) -> DeleteVpcEndpointResponseTypeDef:
        """
        Deletes an Amazon OpenSearch Service-managed interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/delete_vpc_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#delete_vpc_endpoint)
        """

    async def describe_domain(
        self, **kwargs: Unpack[DescribeDomainRequestRequestTypeDef]
    ) -> DescribeDomainResponseTypeDef:
        """
        Describes the domain configuration for the specified Amazon OpenSearch Service
        domain, including the domain ID, domain service endpoint, and domain ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/describe_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_domain)
        """

    async def describe_domain_auto_tunes(
        self, **kwargs: Unpack[DescribeDomainAutoTunesRequestRequestTypeDef]
    ) -> DescribeDomainAutoTunesResponseTypeDef:
        """
        Returns the list of optimizations that Auto-Tune has made to an Amazon
        OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/describe_domain_auto_tunes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_domain_auto_tunes)
        """

    async def describe_domain_change_progress(
        self, **kwargs: Unpack[DescribeDomainChangeProgressRequestRequestTypeDef]
    ) -> DescribeDomainChangeProgressResponseTypeDef:
        """
        Returns information about the current blue/green deployment happening on an
        Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/describe_domain_change_progress.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_domain_change_progress)
        """

    async def describe_domain_config(
        self, **kwargs: Unpack[DescribeDomainConfigRequestRequestTypeDef]
    ) -> DescribeDomainConfigResponseTypeDef:
        """
        Returns the configuration of an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/describe_domain_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_domain_config)
        """

    async def describe_domain_health(
        self, **kwargs: Unpack[DescribeDomainHealthRequestRequestTypeDef]
    ) -> DescribeDomainHealthResponseTypeDef:
        """
        Returns information about domain and node health, the standby Availability
        Zone, number of nodes per Availability Zone, and shard count per node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/describe_domain_health.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_domain_health)
        """

    async def describe_domain_nodes(
        self, **kwargs: Unpack[DescribeDomainNodesRequestRequestTypeDef]
    ) -> DescribeDomainNodesResponseTypeDef:
        """
        Returns information about domain and nodes, including data nodes, master nodes,
        ultrawarm nodes, Availability Zone(s), standby nodes, node configurations, and
        node states.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/describe_domain_nodes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_domain_nodes)
        """

    async def describe_domains(
        self, **kwargs: Unpack[DescribeDomainsRequestRequestTypeDef]
    ) -> DescribeDomainsResponseTypeDef:
        """
        Returns domain configuration information about the specified Amazon OpenSearch
        Service domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/describe_domains.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_domains)
        """

    async def describe_dry_run_progress(
        self, **kwargs: Unpack[DescribeDryRunProgressRequestRequestTypeDef]
    ) -> DescribeDryRunProgressResponseTypeDef:
        """
        Describes the progress of a pre-update dry run analysis on an Amazon OpenSearch
        Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/describe_dry_run_progress.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_dry_run_progress)
        """

    async def describe_inbound_connections(
        self, **kwargs: Unpack[DescribeInboundConnectionsRequestRequestTypeDef]
    ) -> DescribeInboundConnectionsResponseTypeDef:
        """
        Lists all the inbound cross-cluster search connections for a destination
        (remote) Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/describe_inbound_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_inbound_connections)
        """

    async def describe_instance_type_limits(
        self, **kwargs: Unpack[DescribeInstanceTypeLimitsRequestRequestTypeDef]
    ) -> DescribeInstanceTypeLimitsResponseTypeDef:
        """
        Describes the instance count, storage, and master node limits for a given
        OpenSearch or Elasticsearch version and instance type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/describe_instance_type_limits.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_instance_type_limits)
        """

    async def describe_outbound_connections(
        self, **kwargs: Unpack[DescribeOutboundConnectionsRequestRequestTypeDef]
    ) -> DescribeOutboundConnectionsResponseTypeDef:
        """
        Lists all the outbound cross-cluster connections for a local (source) Amazon
        OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/describe_outbound_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_outbound_connections)
        """

    async def describe_packages(
        self, **kwargs: Unpack[DescribePackagesRequestRequestTypeDef]
    ) -> DescribePackagesResponseTypeDef:
        """
        Describes all packages available to OpenSearch Service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/describe_packages.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_packages)
        """

    async def describe_reserved_instance_offerings(
        self, **kwargs: Unpack[DescribeReservedInstanceOfferingsRequestRequestTypeDef]
    ) -> DescribeReservedInstanceOfferingsResponseTypeDef:
        """
        Describes the available Amazon OpenSearch Service Reserved Instance offerings
        for a given Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/describe_reserved_instance_offerings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_reserved_instance_offerings)
        """

    async def describe_reserved_instances(
        self, **kwargs: Unpack[DescribeReservedInstancesRequestRequestTypeDef]
    ) -> DescribeReservedInstancesResponseTypeDef:
        """
        Describes the Amazon OpenSearch Service instances that you have reserved in a
        given Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/describe_reserved_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_reserved_instances)
        """

    async def describe_vpc_endpoints(
        self, **kwargs: Unpack[DescribeVpcEndpointsRequestRequestTypeDef]
    ) -> DescribeVpcEndpointsResponseTypeDef:
        """
        Describes one or more Amazon OpenSearch Service-managed VPC endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/describe_vpc_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_vpc_endpoints)
        """

    async def dissociate_package(
        self, **kwargs: Unpack[DissociatePackageRequestRequestTypeDef]
    ) -> DissociatePackageResponseTypeDef:
        """
        Removes a package from the specified Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/dissociate_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#dissociate_package)
        """

    async def get_compatible_versions(
        self, **kwargs: Unpack[GetCompatibleVersionsRequestRequestTypeDef]
    ) -> GetCompatibleVersionsResponseTypeDef:
        """
        Returns a map of OpenSearch or Elasticsearch versions and the versions you can
        upgrade them to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/get_compatible_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#get_compatible_versions)
        """

    async def get_data_source(
        self, **kwargs: Unpack[GetDataSourceRequestRequestTypeDef]
    ) -> GetDataSourceResponseTypeDef:
        """
        Retrieves information about a direct query data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/get_data_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#get_data_source)
        """

    async def get_domain_maintenance_status(
        self, **kwargs: Unpack[GetDomainMaintenanceStatusRequestRequestTypeDef]
    ) -> GetDomainMaintenanceStatusResponseTypeDef:
        """
        The status of the maintenance action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/get_domain_maintenance_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#get_domain_maintenance_status)
        """

    async def get_package_version_history(
        self, **kwargs: Unpack[GetPackageVersionHistoryRequestRequestTypeDef]
    ) -> GetPackageVersionHistoryResponseTypeDef:
        """
        Returns a list of Amazon OpenSearch Service package versions, along with their
        creation time, commit message, and plugin properties (if the package is a zip
        plugin package).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/get_package_version_history.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#get_package_version_history)
        """

    async def get_upgrade_history(
        self, **kwargs: Unpack[GetUpgradeHistoryRequestRequestTypeDef]
    ) -> GetUpgradeHistoryResponseTypeDef:
        """
        Retrieves the complete history of the last 10 upgrades performed on an Amazon
        OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/get_upgrade_history.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#get_upgrade_history)
        """

    async def get_upgrade_status(
        self, **kwargs: Unpack[GetUpgradeStatusRequestRequestTypeDef]
    ) -> GetUpgradeStatusResponseTypeDef:
        """
        Returns the most recent status of the last upgrade or upgrade eligibility check
        performed on an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/get_upgrade_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#get_upgrade_status)
        """

    async def list_data_sources(
        self, **kwargs: Unpack[ListDataSourcesRequestRequestTypeDef]
    ) -> ListDataSourcesResponseTypeDef:
        """
        Lists direct-query data sources for a specific domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/list_data_sources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_data_sources)
        """

    async def list_domain_maintenances(
        self, **kwargs: Unpack[ListDomainMaintenancesRequestRequestTypeDef]
    ) -> ListDomainMaintenancesResponseTypeDef:
        """
        A list of maintenance actions for the domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/list_domain_maintenances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_domain_maintenances)
        """

    async def list_domain_names(
        self, **kwargs: Unpack[ListDomainNamesRequestRequestTypeDef]
    ) -> ListDomainNamesResponseTypeDef:
        """
        Returns the names of all Amazon OpenSearch Service domains owned by the current
        user in the active Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/list_domain_names.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_domain_names)
        """

    async def list_domains_for_package(
        self, **kwargs: Unpack[ListDomainsForPackageRequestRequestTypeDef]
    ) -> ListDomainsForPackageResponseTypeDef:
        """
        Lists all Amazon OpenSearch Service domains associated with a given package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/list_domains_for_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_domains_for_package)
        """

    async def list_instance_type_details(
        self, **kwargs: Unpack[ListInstanceTypeDetailsRequestRequestTypeDef]
    ) -> ListInstanceTypeDetailsResponseTypeDef:
        """
        Lists all instance types and available features for a given OpenSearch or
        Elasticsearch version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/list_instance_type_details.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_instance_type_details)
        """

    async def list_packages_for_domain(
        self, **kwargs: Unpack[ListPackagesForDomainRequestRequestTypeDef]
    ) -> ListPackagesForDomainResponseTypeDef:
        """
        Lists all packages associated with an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/list_packages_for_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_packages_for_domain)
        """

    async def list_scheduled_actions(
        self, **kwargs: Unpack[ListScheduledActionsRequestRequestTypeDef]
    ) -> ListScheduledActionsResponseTypeDef:
        """
        Retrieves a list of configuration changes that are scheduled for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/list_scheduled_actions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_scheduled_actions)
        """

    async def list_tags(
        self, **kwargs: Unpack[ListTagsRequestRequestTypeDef]
    ) -> ListTagsResponseTypeDef:
        """
        Returns all resource tags for an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/list_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_tags)
        """

    async def list_versions(
        self, **kwargs: Unpack[ListVersionsRequestRequestTypeDef]
    ) -> ListVersionsResponseTypeDef:
        """
        Lists all versions of OpenSearch and Elasticsearch that Amazon OpenSearch
        Service supports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/list_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_versions)
        """

    async def list_vpc_endpoint_access(
        self, **kwargs: Unpack[ListVpcEndpointAccessRequestRequestTypeDef]
    ) -> ListVpcEndpointAccessResponseTypeDef:
        """
        Retrieves information about each Amazon Web Services principal that is allowed
        to access a given Amazon OpenSearch Service domain through the use of an
        interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/list_vpc_endpoint_access.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_vpc_endpoint_access)
        """

    async def list_vpc_endpoints(
        self, **kwargs: Unpack[ListVpcEndpointsRequestRequestTypeDef]
    ) -> ListVpcEndpointsResponseTypeDef:
        """
        Retrieves all Amazon OpenSearch Service-managed VPC endpoints in the current
        Amazon Web Services account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/list_vpc_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_vpc_endpoints)
        """

    async def list_vpc_endpoints_for_domain(
        self, **kwargs: Unpack[ListVpcEndpointsForDomainRequestRequestTypeDef]
    ) -> ListVpcEndpointsForDomainResponseTypeDef:
        """
        Retrieves all Amazon OpenSearch Service-managed VPC endpoints associated with a
        particular domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/list_vpc_endpoints_for_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_vpc_endpoints_for_domain)
        """

    async def purchase_reserved_instance_offering(
        self, **kwargs: Unpack[PurchaseReservedInstanceOfferingRequestRequestTypeDef]
    ) -> PurchaseReservedInstanceOfferingResponseTypeDef:
        """
        Allows you to purchase Amazon OpenSearch Service Reserved Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/purchase_reserved_instance_offering.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#purchase_reserved_instance_offering)
        """

    async def reject_inbound_connection(
        self, **kwargs: Unpack[RejectInboundConnectionRequestRequestTypeDef]
    ) -> RejectInboundConnectionResponseTypeDef:
        """
        Allows the remote Amazon OpenSearch Service domain owner to reject an inbound
        cross-cluster connection request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/reject_inbound_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#reject_inbound_connection)
        """

    async def remove_tags(
        self, **kwargs: Unpack[RemoveTagsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified set of tags from an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/remove_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#remove_tags)
        """

    async def revoke_vpc_endpoint_access(
        self, **kwargs: Unpack[RevokeVpcEndpointAccessRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Revokes access to an Amazon OpenSearch Service domain that was provided through
        an interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/revoke_vpc_endpoint_access.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#revoke_vpc_endpoint_access)
        """

    async def start_domain_maintenance(
        self, **kwargs: Unpack[StartDomainMaintenanceRequestRequestTypeDef]
    ) -> StartDomainMaintenanceResponseTypeDef:
        """
        Starts the node maintenance process on the data node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/start_domain_maintenance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#start_domain_maintenance)
        """

    async def start_service_software_update(
        self, **kwargs: Unpack[StartServiceSoftwareUpdateRequestRequestTypeDef]
    ) -> StartServiceSoftwareUpdateResponseTypeDef:
        """
        Schedules a service software update for an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/start_service_software_update.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#start_service_software_update)
        """

    async def update_data_source(
        self, **kwargs: Unpack[UpdateDataSourceRequestRequestTypeDef]
    ) -> UpdateDataSourceResponseTypeDef:
        """
        Updates a direct-query data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/update_data_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#update_data_source)
        """

    async def update_domain_config(
        self, **kwargs: Unpack[UpdateDomainConfigRequestRequestTypeDef]
    ) -> UpdateDomainConfigResponseTypeDef:
        """
        Modifies the cluster configuration of the specified Amazon OpenSearch Service
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/update_domain_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#update_domain_config)
        """

    async def update_package(
        self, **kwargs: Unpack[UpdatePackageRequestRequestTypeDef]
    ) -> UpdatePackageResponseTypeDef:
        """
        Updates a package for use with Amazon OpenSearch Service domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/update_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#update_package)
        """

    async def update_scheduled_action(
        self, **kwargs: Unpack[UpdateScheduledActionRequestRequestTypeDef]
    ) -> UpdateScheduledActionResponseTypeDef:
        """
        Reschedules a planned domain configuration change for a later time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/update_scheduled_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#update_scheduled_action)
        """

    async def update_vpc_endpoint(
        self, **kwargs: Unpack[UpdateVpcEndpointRequestRequestTypeDef]
    ) -> UpdateVpcEndpointResponseTypeDef:
        """
        Modifies an Amazon OpenSearch Service-managed interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/update_vpc_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#update_vpc_endpoint)
        """

    async def upgrade_domain(
        self, **kwargs: Unpack[UpgradeDomainRequestRequestTypeDef]
    ) -> UpgradeDomainResponseTypeDef:
        """
        Allows you to either upgrade your Amazon OpenSearch Service domain or perform
        an upgrade eligibility check to a compatible version of OpenSearch or
        Elasticsearch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch/client/upgrade_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#upgrade_domain)
        """

    async def __aenter__(self) -> "OpenSearchServiceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/)
        """
