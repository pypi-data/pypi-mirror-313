"""
Type annotations for ec2 service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ec2.client import EC2Client

    session = get_session()
    async with session.create_client("ec2") as client:
        client: EC2Client
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    DescribeAddressesAttributePaginator,
    DescribeAddressTransfersPaginator,
    DescribeAwsNetworkPerformanceMetricSubscriptionsPaginator,
    DescribeByoipCidrsPaginator,
    DescribeCapacityBlockOfferingsPaginator,
    DescribeCapacityReservationFleetsPaginator,
    DescribeCapacityReservationsPaginator,
    DescribeCarrierGatewaysPaginator,
    DescribeClassicLinkInstancesPaginator,
    DescribeClientVpnAuthorizationRulesPaginator,
    DescribeClientVpnConnectionsPaginator,
    DescribeClientVpnEndpointsPaginator,
    DescribeClientVpnRoutesPaginator,
    DescribeClientVpnTargetNetworksPaginator,
    DescribeCoipPoolsPaginator,
    DescribeDhcpOptionsPaginator,
    DescribeEgressOnlyInternetGatewaysPaginator,
    DescribeExportImageTasksPaginator,
    DescribeFastLaunchImagesPaginator,
    DescribeFastSnapshotRestoresPaginator,
    DescribeFleetsPaginator,
    DescribeFlowLogsPaginator,
    DescribeFpgaImagesPaginator,
    DescribeHostReservationOfferingsPaginator,
    DescribeHostReservationsPaginator,
    DescribeHostsPaginator,
    DescribeIamInstanceProfileAssociationsPaginator,
    DescribeImagesPaginator,
    DescribeImportImageTasksPaginator,
    DescribeImportSnapshotTasksPaginator,
    DescribeInstanceConnectEndpointsPaginator,
    DescribeInstanceCreditSpecificationsPaginator,
    DescribeInstanceEventWindowsPaginator,
    DescribeInstancesPaginator,
    DescribeInstanceStatusPaginator,
    DescribeInstanceTopologyPaginator,
    DescribeInstanceTypeOfferingsPaginator,
    DescribeInstanceTypesPaginator,
    DescribeInternetGatewaysPaginator,
    DescribeIpamPoolsPaginator,
    DescribeIpamResourceDiscoveriesPaginator,
    DescribeIpamResourceDiscoveryAssociationsPaginator,
    DescribeIpamScopesPaginator,
    DescribeIpamsPaginator,
    DescribeIpv6PoolsPaginator,
    DescribeLaunchTemplatesPaginator,
    DescribeLaunchTemplateVersionsPaginator,
    DescribeLocalGatewayRouteTablesPaginator,
    DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsPaginator,
    DescribeLocalGatewayRouteTableVpcAssociationsPaginator,
    DescribeLocalGatewaysPaginator,
    DescribeLocalGatewayVirtualInterfaceGroupsPaginator,
    DescribeLocalGatewayVirtualInterfacesPaginator,
    DescribeMacHostsPaginator,
    DescribeManagedPrefixListsPaginator,
    DescribeMovingAddressesPaginator,
    DescribeNatGatewaysPaginator,
    DescribeNetworkAclsPaginator,
    DescribeNetworkInsightsAccessScopeAnalysesPaginator,
    DescribeNetworkInsightsAccessScopesPaginator,
    DescribeNetworkInsightsAnalysesPaginator,
    DescribeNetworkInsightsPathsPaginator,
    DescribeNetworkInterfacePermissionsPaginator,
    DescribeNetworkInterfacesPaginator,
    DescribePrefixListsPaginator,
    DescribePrincipalIdFormatPaginator,
    DescribePublicIpv4PoolsPaginator,
    DescribeReplaceRootVolumeTasksPaginator,
    DescribeReservedInstancesModificationsPaginator,
    DescribeReservedInstancesOfferingsPaginator,
    DescribeRouteTablesPaginator,
    DescribeScheduledInstanceAvailabilityPaginator,
    DescribeScheduledInstancesPaginator,
    DescribeSecurityGroupRulesPaginator,
    DescribeSecurityGroupsPaginator,
    DescribeSnapshotsPaginator,
    DescribeSnapshotTierStatusPaginator,
    DescribeSpotFleetInstancesPaginator,
    DescribeSpotFleetRequestsPaginator,
    DescribeSpotInstanceRequestsPaginator,
    DescribeSpotPriceHistoryPaginator,
    DescribeStaleSecurityGroupsPaginator,
    DescribeStoreImageTasksPaginator,
    DescribeSubnetsPaginator,
    DescribeTagsPaginator,
    DescribeTrafficMirrorFiltersPaginator,
    DescribeTrafficMirrorSessionsPaginator,
    DescribeTrafficMirrorTargetsPaginator,
    DescribeTransitGatewayAttachmentsPaginator,
    DescribeTransitGatewayConnectPeersPaginator,
    DescribeTransitGatewayConnectsPaginator,
    DescribeTransitGatewayMulticastDomainsPaginator,
    DescribeTransitGatewayPeeringAttachmentsPaginator,
    DescribeTransitGatewayPolicyTablesPaginator,
    DescribeTransitGatewayRouteTableAnnouncementsPaginator,
    DescribeTransitGatewayRouteTablesPaginator,
    DescribeTransitGatewaysPaginator,
    DescribeTransitGatewayVpcAttachmentsPaginator,
    DescribeTrunkInterfaceAssociationsPaginator,
    DescribeVerifiedAccessEndpointsPaginator,
    DescribeVerifiedAccessGroupsPaginator,
    DescribeVerifiedAccessInstanceLoggingConfigurationsPaginator,
    DescribeVerifiedAccessInstancesPaginator,
    DescribeVerifiedAccessTrustProvidersPaginator,
    DescribeVolumesModificationsPaginator,
    DescribeVolumesPaginator,
    DescribeVolumeStatusPaginator,
    DescribeVpcClassicLinkDnsSupportPaginator,
    DescribeVpcEndpointConnectionNotificationsPaginator,
    DescribeVpcEndpointConnectionsPaginator,
    DescribeVpcEndpointServiceConfigurationsPaginator,
    DescribeVpcEndpointServicePermissionsPaginator,
    DescribeVpcEndpointServicesPaginator,
    DescribeVpcEndpointsPaginator,
    DescribeVpcPeeringConnectionsPaginator,
    DescribeVpcsPaginator,
    GetAssociatedIpv6PoolCidrsPaginator,
    GetAwsNetworkPerformanceDataPaginator,
    GetGroupsForCapacityReservationPaginator,
    GetInstanceTypesFromInstanceRequirementsPaginator,
    GetIpamAddressHistoryPaginator,
    GetIpamDiscoveredAccountsPaginator,
    GetIpamDiscoveredResourceCidrsPaginator,
    GetIpamPoolAllocationsPaginator,
    GetIpamPoolCidrsPaginator,
    GetIpamResourceCidrsPaginator,
    GetManagedPrefixListAssociationsPaginator,
    GetManagedPrefixListEntriesPaginator,
    GetNetworkInsightsAccessScopeAnalysisFindingsPaginator,
    GetSecurityGroupsForVpcPaginator,
    GetSpotPlacementScoresPaginator,
    GetTransitGatewayAttachmentPropagationsPaginator,
    GetTransitGatewayMulticastDomainAssociationsPaginator,
    GetTransitGatewayPolicyTableAssociationsPaginator,
    GetTransitGatewayPrefixListReferencesPaginator,
    GetTransitGatewayRouteTableAssociationsPaginator,
    GetTransitGatewayRouteTablePropagationsPaginator,
    GetVpnConnectionDeviceTypesPaginator,
    ListImagesInRecycleBinPaginator,
    ListSnapshotsInRecycleBinPaginator,
    SearchLocalGatewayRoutesPaginator,
    SearchTransitGatewayMulticastGroupsPaginator,
)
from .type_defs import (
    AcceptAddressTransferRequestRequestTypeDef,
    AcceptAddressTransferResultTypeDef,
    AcceptReservedInstancesExchangeQuoteRequestRequestTypeDef,
    AcceptReservedInstancesExchangeQuoteResultTypeDef,
    AcceptTransitGatewayMulticastDomainAssociationsRequestRequestTypeDef,
    AcceptTransitGatewayMulticastDomainAssociationsResultTypeDef,
    AcceptTransitGatewayPeeringAttachmentRequestRequestTypeDef,
    AcceptTransitGatewayPeeringAttachmentResultTypeDef,
    AcceptTransitGatewayVpcAttachmentRequestRequestTypeDef,
    AcceptTransitGatewayVpcAttachmentResultTypeDef,
    AcceptVpcEndpointConnectionsRequestRequestTypeDef,
    AcceptVpcEndpointConnectionsResultTypeDef,
    AcceptVpcPeeringConnectionRequestRequestTypeDef,
    AcceptVpcPeeringConnectionResultTypeDef,
    AdvertiseByoipCidrRequestRequestTypeDef,
    AdvertiseByoipCidrResultTypeDef,
    AllocateAddressRequestRequestTypeDef,
    AllocateAddressResultTypeDef,
    AllocateHostsRequestRequestTypeDef,
    AllocateHostsResultTypeDef,
    AllocateIpamPoolCidrRequestRequestTypeDef,
    AllocateIpamPoolCidrResultTypeDef,
    ApplySecurityGroupsToClientVpnTargetNetworkRequestRequestTypeDef,
    ApplySecurityGroupsToClientVpnTargetNetworkResultTypeDef,
    AssignIpv6AddressesRequestRequestTypeDef,
    AssignIpv6AddressesResultTypeDef,
    AssignPrivateIpAddressesRequestRequestTypeDef,
    AssignPrivateIpAddressesResultTypeDef,
    AssignPrivateNatGatewayAddressRequestRequestTypeDef,
    AssignPrivateNatGatewayAddressResultTypeDef,
    AssociateAddressRequestRequestTypeDef,
    AssociateAddressResultTypeDef,
    AssociateClientVpnTargetNetworkRequestRequestTypeDef,
    AssociateClientVpnTargetNetworkResultTypeDef,
    AssociateDhcpOptionsRequestRequestTypeDef,
    AssociateEnclaveCertificateIamRoleRequestRequestTypeDef,
    AssociateEnclaveCertificateIamRoleResultTypeDef,
    AssociateIamInstanceProfileRequestRequestTypeDef,
    AssociateIamInstanceProfileResultTypeDef,
    AssociateInstanceEventWindowRequestRequestTypeDef,
    AssociateInstanceEventWindowResultTypeDef,
    AssociateIpamByoasnRequestRequestTypeDef,
    AssociateIpamByoasnResultTypeDef,
    AssociateIpamResourceDiscoveryRequestRequestTypeDef,
    AssociateIpamResourceDiscoveryResultTypeDef,
    AssociateNatGatewayAddressRequestRequestTypeDef,
    AssociateNatGatewayAddressResultTypeDef,
    AssociateRouteTableRequestRequestTypeDef,
    AssociateRouteTableResultTypeDef,
    AssociateSubnetCidrBlockRequestRequestTypeDef,
    AssociateSubnetCidrBlockResultTypeDef,
    AssociateTransitGatewayMulticastDomainRequestRequestTypeDef,
    AssociateTransitGatewayMulticastDomainResultTypeDef,
    AssociateTransitGatewayPolicyTableRequestRequestTypeDef,
    AssociateTransitGatewayPolicyTableResultTypeDef,
    AssociateTransitGatewayRouteTableRequestRequestTypeDef,
    AssociateTransitGatewayRouteTableResultTypeDef,
    AssociateTrunkInterfaceRequestRequestTypeDef,
    AssociateTrunkInterfaceResultTypeDef,
    AssociateVpcCidrBlockRequestRequestTypeDef,
    AssociateVpcCidrBlockResultTypeDef,
    AttachClassicLinkVpcRequestRequestTypeDef,
    AttachClassicLinkVpcResultTypeDef,
    AttachInternetGatewayRequestRequestTypeDef,
    AttachNetworkInterfaceRequestRequestTypeDef,
    AttachNetworkInterfaceResultTypeDef,
    AttachVerifiedAccessTrustProviderRequestRequestTypeDef,
    AttachVerifiedAccessTrustProviderResultTypeDef,
    AttachVolumeRequestRequestTypeDef,
    AttachVpnGatewayRequestRequestTypeDef,
    AttachVpnGatewayResultTypeDef,
    AuthorizeClientVpnIngressRequestRequestTypeDef,
    AuthorizeClientVpnIngressResultTypeDef,
    AuthorizeSecurityGroupEgressRequestRequestTypeDef,
    AuthorizeSecurityGroupEgressResultTypeDef,
    AuthorizeSecurityGroupIngressRequestRequestTypeDef,
    AuthorizeSecurityGroupIngressResultTypeDef,
    BundleInstanceRequestRequestTypeDef,
    BundleInstanceResultTypeDef,
    CancelBundleTaskRequestRequestTypeDef,
    CancelBundleTaskResultTypeDef,
    CancelCapacityReservationFleetsRequestRequestTypeDef,
    CancelCapacityReservationFleetsResultTypeDef,
    CancelCapacityReservationRequestRequestTypeDef,
    CancelCapacityReservationResultTypeDef,
    CancelConversionRequestRequestTypeDef,
    CancelExportTaskRequestRequestTypeDef,
    CancelImageLaunchPermissionRequestRequestTypeDef,
    CancelImageLaunchPermissionResultTypeDef,
    CancelImportTaskRequestRequestTypeDef,
    CancelImportTaskResultTypeDef,
    CancelReservedInstancesListingRequestRequestTypeDef,
    CancelReservedInstancesListingResultTypeDef,
    CancelSpotFleetRequestsRequestRequestTypeDef,
    CancelSpotFleetRequestsResponseTypeDef,
    CancelSpotInstanceRequestsRequestRequestTypeDef,
    CancelSpotInstanceRequestsResultTypeDef,
    ClientCreateTagsRequestTypeDef,
    ClientDeleteTagsRequestTypeDef,
    ConfirmProductInstanceRequestRequestTypeDef,
    ConfirmProductInstanceResultTypeDef,
    CopyFpgaImageRequestRequestTypeDef,
    CopyFpgaImageResultTypeDef,
    CopyImageRequestRequestTypeDef,
    CopyImageResultTypeDef,
    CopySnapshotRequestRequestTypeDef,
    CopySnapshotResultTypeDef,
    CreateCapacityReservationBySplittingRequestRequestTypeDef,
    CreateCapacityReservationBySplittingResultTypeDef,
    CreateCapacityReservationFleetRequestRequestTypeDef,
    CreateCapacityReservationFleetResultTypeDef,
    CreateCapacityReservationRequestRequestTypeDef,
    CreateCapacityReservationResultTypeDef,
    CreateCarrierGatewayRequestRequestTypeDef,
    CreateCarrierGatewayResultTypeDef,
    CreateClientVpnEndpointRequestRequestTypeDef,
    CreateClientVpnEndpointResultTypeDef,
    CreateClientVpnRouteRequestRequestTypeDef,
    CreateClientVpnRouteResultTypeDef,
    CreateCoipCidrRequestRequestTypeDef,
    CreateCoipCidrResultTypeDef,
    CreateCoipPoolRequestRequestTypeDef,
    CreateCoipPoolResultTypeDef,
    CreateCustomerGatewayRequestRequestTypeDef,
    CreateCustomerGatewayResultTypeDef,
    CreateDefaultSubnetRequestRequestTypeDef,
    CreateDefaultSubnetResultTypeDef,
    CreateDefaultVpcRequestRequestTypeDef,
    CreateDefaultVpcResultTypeDef,
    CreateDhcpOptionsRequestRequestTypeDef,
    CreateDhcpOptionsResultTypeDef,
    CreateEgressOnlyInternetGatewayRequestRequestTypeDef,
    CreateEgressOnlyInternetGatewayResultTypeDef,
    CreateFleetRequestRequestTypeDef,
    CreateFleetResultTypeDef,
    CreateFlowLogsRequestRequestTypeDef,
    CreateFlowLogsResultTypeDef,
    CreateFpgaImageRequestRequestTypeDef,
    CreateFpgaImageResultTypeDef,
    CreateImageRequestRequestTypeDef,
    CreateImageResultTypeDef,
    CreateInstanceConnectEndpointRequestRequestTypeDef,
    CreateInstanceConnectEndpointResultTypeDef,
    CreateInstanceEventWindowRequestRequestTypeDef,
    CreateInstanceEventWindowResultTypeDef,
    CreateInstanceExportTaskRequestRequestTypeDef,
    CreateInstanceExportTaskResultTypeDef,
    CreateInternetGatewayRequestRequestTypeDef,
    CreateInternetGatewayResultTypeDef,
    CreateIpamExternalResourceVerificationTokenRequestRequestTypeDef,
    CreateIpamExternalResourceVerificationTokenResultTypeDef,
    CreateIpamPoolRequestRequestTypeDef,
    CreateIpamPoolResultTypeDef,
    CreateIpamRequestRequestTypeDef,
    CreateIpamResourceDiscoveryRequestRequestTypeDef,
    CreateIpamResourceDiscoveryResultTypeDef,
    CreateIpamResultTypeDef,
    CreateIpamScopeRequestRequestTypeDef,
    CreateIpamScopeResultTypeDef,
    CreateKeyPairRequestRequestTypeDef,
    CreateLaunchTemplateRequestRequestTypeDef,
    CreateLaunchTemplateResultTypeDef,
    CreateLaunchTemplateVersionRequestRequestTypeDef,
    CreateLaunchTemplateVersionResultTypeDef,
    CreateLocalGatewayRouteRequestRequestTypeDef,
    CreateLocalGatewayRouteResultTypeDef,
    CreateLocalGatewayRouteTableRequestRequestTypeDef,
    CreateLocalGatewayRouteTableResultTypeDef,
    CreateLocalGatewayRouteTableVirtualInterfaceGroupAssociationRequestRequestTypeDef,
    CreateLocalGatewayRouteTableVirtualInterfaceGroupAssociationResultTypeDef,
    CreateLocalGatewayRouteTableVpcAssociationRequestRequestTypeDef,
    CreateLocalGatewayRouteTableVpcAssociationResultTypeDef,
    CreateManagedPrefixListRequestRequestTypeDef,
    CreateManagedPrefixListResultTypeDef,
    CreateNatGatewayRequestRequestTypeDef,
    CreateNatGatewayResultTypeDef,
    CreateNetworkAclEntryRequestRequestTypeDef,
    CreateNetworkAclRequestRequestTypeDef,
    CreateNetworkAclResultTypeDef,
    CreateNetworkInsightsAccessScopeRequestRequestTypeDef,
    CreateNetworkInsightsAccessScopeResultTypeDef,
    CreateNetworkInsightsPathRequestRequestTypeDef,
    CreateNetworkInsightsPathResultTypeDef,
    CreateNetworkInterfacePermissionRequestRequestTypeDef,
    CreateNetworkInterfacePermissionResultTypeDef,
    CreateNetworkInterfaceRequestRequestTypeDef,
    CreateNetworkInterfaceResultTypeDef,
    CreatePlacementGroupRequestRequestTypeDef,
    CreatePlacementGroupResultTypeDef,
    CreatePublicIpv4PoolRequestRequestTypeDef,
    CreatePublicIpv4PoolResultTypeDef,
    CreateReplaceRootVolumeTaskRequestRequestTypeDef,
    CreateReplaceRootVolumeTaskResultTypeDef,
    CreateReservedInstancesListingRequestRequestTypeDef,
    CreateReservedInstancesListingResultTypeDef,
    CreateRestoreImageTaskRequestRequestTypeDef,
    CreateRestoreImageTaskResultTypeDef,
    CreateRouteRequestRequestTypeDef,
    CreateRouteResultTypeDef,
    CreateRouteTableRequestRequestTypeDef,
    CreateRouteTableResultTypeDef,
    CreateSecurityGroupRequestRequestTypeDef,
    CreateSecurityGroupResultTypeDef,
    CreateSnapshotRequestRequestTypeDef,
    CreateSnapshotsRequestRequestTypeDef,
    CreateSnapshotsResultTypeDef,
    CreateSpotDatafeedSubscriptionRequestRequestTypeDef,
    CreateSpotDatafeedSubscriptionResultTypeDef,
    CreateStoreImageTaskRequestRequestTypeDef,
    CreateStoreImageTaskResultTypeDef,
    CreateSubnetCidrReservationRequestRequestTypeDef,
    CreateSubnetCidrReservationResultTypeDef,
    CreateSubnetRequestRequestTypeDef,
    CreateSubnetResultTypeDef,
    CreateTrafficMirrorFilterRequestRequestTypeDef,
    CreateTrafficMirrorFilterResultTypeDef,
    CreateTrafficMirrorFilterRuleRequestRequestTypeDef,
    CreateTrafficMirrorFilterRuleResultTypeDef,
    CreateTrafficMirrorSessionRequestRequestTypeDef,
    CreateTrafficMirrorSessionResultTypeDef,
    CreateTrafficMirrorTargetRequestRequestTypeDef,
    CreateTrafficMirrorTargetResultTypeDef,
    CreateTransitGatewayConnectPeerRequestRequestTypeDef,
    CreateTransitGatewayConnectPeerResultTypeDef,
    CreateTransitGatewayConnectRequestRequestTypeDef,
    CreateTransitGatewayConnectResultTypeDef,
    CreateTransitGatewayMulticastDomainRequestRequestTypeDef,
    CreateTransitGatewayMulticastDomainResultTypeDef,
    CreateTransitGatewayPeeringAttachmentRequestRequestTypeDef,
    CreateTransitGatewayPeeringAttachmentResultTypeDef,
    CreateTransitGatewayPolicyTableRequestRequestTypeDef,
    CreateTransitGatewayPolicyTableResultTypeDef,
    CreateTransitGatewayPrefixListReferenceRequestRequestTypeDef,
    CreateTransitGatewayPrefixListReferenceResultTypeDef,
    CreateTransitGatewayRequestRequestTypeDef,
    CreateTransitGatewayResultTypeDef,
    CreateTransitGatewayRouteRequestRequestTypeDef,
    CreateTransitGatewayRouteResultTypeDef,
    CreateTransitGatewayRouteTableAnnouncementRequestRequestTypeDef,
    CreateTransitGatewayRouteTableAnnouncementResultTypeDef,
    CreateTransitGatewayRouteTableRequestRequestTypeDef,
    CreateTransitGatewayRouteTableResultTypeDef,
    CreateTransitGatewayVpcAttachmentRequestRequestTypeDef,
    CreateTransitGatewayVpcAttachmentResultTypeDef,
    CreateVerifiedAccessEndpointRequestRequestTypeDef,
    CreateVerifiedAccessEndpointResultTypeDef,
    CreateVerifiedAccessGroupRequestRequestTypeDef,
    CreateVerifiedAccessGroupResultTypeDef,
    CreateVerifiedAccessInstanceRequestRequestTypeDef,
    CreateVerifiedAccessInstanceResultTypeDef,
    CreateVerifiedAccessTrustProviderRequestRequestTypeDef,
    CreateVerifiedAccessTrustProviderResultTypeDef,
    CreateVolumeRequestRequestTypeDef,
    CreateVpcEndpointConnectionNotificationRequestRequestTypeDef,
    CreateVpcEndpointConnectionNotificationResultTypeDef,
    CreateVpcEndpointRequestRequestTypeDef,
    CreateVpcEndpointResultTypeDef,
    CreateVpcEndpointServiceConfigurationRequestRequestTypeDef,
    CreateVpcEndpointServiceConfigurationResultTypeDef,
    CreateVpcPeeringConnectionRequestRequestTypeDef,
    CreateVpcPeeringConnectionResultTypeDef,
    CreateVpcRequestRequestTypeDef,
    CreateVpcResultTypeDef,
    CreateVpnConnectionRequestRequestTypeDef,
    CreateVpnConnectionResultTypeDef,
    CreateVpnConnectionRouteRequestRequestTypeDef,
    CreateVpnGatewayRequestRequestTypeDef,
    CreateVpnGatewayResultTypeDef,
    DeleteCarrierGatewayRequestRequestTypeDef,
    DeleteCarrierGatewayResultTypeDef,
    DeleteClientVpnEndpointRequestRequestTypeDef,
    DeleteClientVpnEndpointResultTypeDef,
    DeleteClientVpnRouteRequestRequestTypeDef,
    DeleteClientVpnRouteResultTypeDef,
    DeleteCoipCidrRequestRequestTypeDef,
    DeleteCoipCidrResultTypeDef,
    DeleteCoipPoolRequestRequestTypeDef,
    DeleteCoipPoolResultTypeDef,
    DeleteCustomerGatewayRequestRequestTypeDef,
    DeleteDhcpOptionsRequestRequestTypeDef,
    DeleteEgressOnlyInternetGatewayRequestRequestTypeDef,
    DeleteEgressOnlyInternetGatewayResultTypeDef,
    DeleteFleetsRequestRequestTypeDef,
    DeleteFleetsResultTypeDef,
    DeleteFlowLogsRequestRequestTypeDef,
    DeleteFlowLogsResultTypeDef,
    DeleteFpgaImageRequestRequestTypeDef,
    DeleteFpgaImageResultTypeDef,
    DeleteInstanceConnectEndpointRequestRequestTypeDef,
    DeleteInstanceConnectEndpointResultTypeDef,
    DeleteInstanceEventWindowRequestRequestTypeDef,
    DeleteInstanceEventWindowResultTypeDef,
    DeleteInternetGatewayRequestRequestTypeDef,
    DeleteIpamExternalResourceVerificationTokenRequestRequestTypeDef,
    DeleteIpamExternalResourceVerificationTokenResultTypeDef,
    DeleteIpamPoolRequestRequestTypeDef,
    DeleteIpamPoolResultTypeDef,
    DeleteIpamRequestRequestTypeDef,
    DeleteIpamResourceDiscoveryRequestRequestTypeDef,
    DeleteIpamResourceDiscoveryResultTypeDef,
    DeleteIpamResultTypeDef,
    DeleteIpamScopeRequestRequestTypeDef,
    DeleteIpamScopeResultTypeDef,
    DeleteKeyPairRequestRequestTypeDef,
    DeleteKeyPairResultTypeDef,
    DeleteLaunchTemplateRequestRequestTypeDef,
    DeleteLaunchTemplateResultTypeDef,
    DeleteLaunchTemplateVersionsRequestRequestTypeDef,
    DeleteLaunchTemplateVersionsResultTypeDef,
    DeleteLocalGatewayRouteRequestRequestTypeDef,
    DeleteLocalGatewayRouteResultTypeDef,
    DeleteLocalGatewayRouteTableRequestRequestTypeDef,
    DeleteLocalGatewayRouteTableResultTypeDef,
    DeleteLocalGatewayRouteTableVirtualInterfaceGroupAssociationRequestRequestTypeDef,
    DeleteLocalGatewayRouteTableVirtualInterfaceGroupAssociationResultTypeDef,
    DeleteLocalGatewayRouteTableVpcAssociationRequestRequestTypeDef,
    DeleteLocalGatewayRouteTableVpcAssociationResultTypeDef,
    DeleteManagedPrefixListRequestRequestTypeDef,
    DeleteManagedPrefixListResultTypeDef,
    DeleteNatGatewayRequestRequestTypeDef,
    DeleteNatGatewayResultTypeDef,
    DeleteNetworkAclEntryRequestRequestTypeDef,
    DeleteNetworkAclRequestRequestTypeDef,
    DeleteNetworkInsightsAccessScopeAnalysisRequestRequestTypeDef,
    DeleteNetworkInsightsAccessScopeAnalysisResultTypeDef,
    DeleteNetworkInsightsAccessScopeRequestRequestTypeDef,
    DeleteNetworkInsightsAccessScopeResultTypeDef,
    DeleteNetworkInsightsAnalysisRequestRequestTypeDef,
    DeleteNetworkInsightsAnalysisResultTypeDef,
    DeleteNetworkInsightsPathRequestRequestTypeDef,
    DeleteNetworkInsightsPathResultTypeDef,
    DeleteNetworkInterfacePermissionRequestRequestTypeDef,
    DeleteNetworkInterfacePermissionResultTypeDef,
    DeleteNetworkInterfaceRequestRequestTypeDef,
    DeletePlacementGroupRequestRequestTypeDef,
    DeletePublicIpv4PoolRequestRequestTypeDef,
    DeletePublicIpv4PoolResultTypeDef,
    DeleteQueuedReservedInstancesRequestRequestTypeDef,
    DeleteQueuedReservedInstancesResultTypeDef,
    DeleteRouteRequestRequestTypeDef,
    DeleteRouteTableRequestRequestTypeDef,
    DeleteSecurityGroupRequestRequestTypeDef,
    DeleteSnapshotRequestRequestTypeDef,
    DeleteSpotDatafeedSubscriptionRequestRequestTypeDef,
    DeleteSubnetCidrReservationRequestRequestTypeDef,
    DeleteSubnetCidrReservationResultTypeDef,
    DeleteSubnetRequestRequestTypeDef,
    DeleteTrafficMirrorFilterRequestRequestTypeDef,
    DeleteTrafficMirrorFilterResultTypeDef,
    DeleteTrafficMirrorFilterRuleRequestRequestTypeDef,
    DeleteTrafficMirrorFilterRuleResultTypeDef,
    DeleteTrafficMirrorSessionRequestRequestTypeDef,
    DeleteTrafficMirrorSessionResultTypeDef,
    DeleteTrafficMirrorTargetRequestRequestTypeDef,
    DeleteTrafficMirrorTargetResultTypeDef,
    DeleteTransitGatewayConnectPeerRequestRequestTypeDef,
    DeleteTransitGatewayConnectPeerResultTypeDef,
    DeleteTransitGatewayConnectRequestRequestTypeDef,
    DeleteTransitGatewayConnectResultTypeDef,
    DeleteTransitGatewayMulticastDomainRequestRequestTypeDef,
    DeleteTransitGatewayMulticastDomainResultTypeDef,
    DeleteTransitGatewayPeeringAttachmentRequestRequestTypeDef,
    DeleteTransitGatewayPeeringAttachmentResultTypeDef,
    DeleteTransitGatewayPolicyTableRequestRequestTypeDef,
    DeleteTransitGatewayPolicyTableResultTypeDef,
    DeleteTransitGatewayPrefixListReferenceRequestRequestTypeDef,
    DeleteTransitGatewayPrefixListReferenceResultTypeDef,
    DeleteTransitGatewayRequestRequestTypeDef,
    DeleteTransitGatewayResultTypeDef,
    DeleteTransitGatewayRouteRequestRequestTypeDef,
    DeleteTransitGatewayRouteResultTypeDef,
    DeleteTransitGatewayRouteTableAnnouncementRequestRequestTypeDef,
    DeleteTransitGatewayRouteTableAnnouncementResultTypeDef,
    DeleteTransitGatewayRouteTableRequestRequestTypeDef,
    DeleteTransitGatewayRouteTableResultTypeDef,
    DeleteTransitGatewayVpcAttachmentRequestRequestTypeDef,
    DeleteTransitGatewayVpcAttachmentResultTypeDef,
    DeleteVerifiedAccessEndpointRequestRequestTypeDef,
    DeleteVerifiedAccessEndpointResultTypeDef,
    DeleteVerifiedAccessGroupRequestRequestTypeDef,
    DeleteVerifiedAccessGroupResultTypeDef,
    DeleteVerifiedAccessInstanceRequestRequestTypeDef,
    DeleteVerifiedAccessInstanceResultTypeDef,
    DeleteVerifiedAccessTrustProviderRequestRequestTypeDef,
    DeleteVerifiedAccessTrustProviderResultTypeDef,
    DeleteVolumeRequestRequestTypeDef,
    DeleteVpcEndpointConnectionNotificationsRequestRequestTypeDef,
    DeleteVpcEndpointConnectionNotificationsResultTypeDef,
    DeleteVpcEndpointServiceConfigurationsRequestRequestTypeDef,
    DeleteVpcEndpointServiceConfigurationsResultTypeDef,
    DeleteVpcEndpointsRequestRequestTypeDef,
    DeleteVpcEndpointsResultTypeDef,
    DeleteVpcPeeringConnectionRequestRequestTypeDef,
    DeleteVpcPeeringConnectionResultTypeDef,
    DeleteVpcRequestRequestTypeDef,
    DeleteVpnConnectionRequestRequestTypeDef,
    DeleteVpnConnectionRouteRequestRequestTypeDef,
    DeleteVpnGatewayRequestRequestTypeDef,
    DeprovisionByoipCidrRequestRequestTypeDef,
    DeprovisionByoipCidrResultTypeDef,
    DeprovisionIpamByoasnRequestRequestTypeDef,
    DeprovisionIpamByoasnResultTypeDef,
    DeprovisionIpamPoolCidrRequestRequestTypeDef,
    DeprovisionIpamPoolCidrResultTypeDef,
    DeprovisionPublicIpv4PoolCidrRequestRequestTypeDef,
    DeprovisionPublicIpv4PoolCidrResultTypeDef,
    DeregisterImageRequestRequestTypeDef,
    DeregisterInstanceEventNotificationAttributesRequestRequestTypeDef,
    DeregisterInstanceEventNotificationAttributesResultTypeDef,
    DeregisterTransitGatewayMulticastGroupMembersRequestRequestTypeDef,
    DeregisterTransitGatewayMulticastGroupMembersResultTypeDef,
    DeregisterTransitGatewayMulticastGroupSourcesRequestRequestTypeDef,
    DeregisterTransitGatewayMulticastGroupSourcesResultTypeDef,
    DescribeAccountAttributesRequestRequestTypeDef,
    DescribeAccountAttributesResultTypeDef,
    DescribeAddressesAttributeRequestRequestTypeDef,
    DescribeAddressesAttributeResultTypeDef,
    DescribeAddressesRequestRequestTypeDef,
    DescribeAddressesResultTypeDef,
    DescribeAddressTransfersRequestRequestTypeDef,
    DescribeAddressTransfersResultTypeDef,
    DescribeAggregateIdFormatRequestRequestTypeDef,
    DescribeAggregateIdFormatResultTypeDef,
    DescribeAvailabilityZonesRequestRequestTypeDef,
    DescribeAvailabilityZonesResultTypeDef,
    DescribeAwsNetworkPerformanceMetricSubscriptionsRequestRequestTypeDef,
    DescribeAwsNetworkPerformanceMetricSubscriptionsResultTypeDef,
    DescribeBundleTasksRequestRequestTypeDef,
    DescribeBundleTasksResultTypeDef,
    DescribeByoipCidrsRequestRequestTypeDef,
    DescribeByoipCidrsResultTypeDef,
    DescribeCapacityBlockOfferingsRequestRequestTypeDef,
    DescribeCapacityBlockOfferingsResultTypeDef,
    DescribeCapacityReservationFleetsRequestRequestTypeDef,
    DescribeCapacityReservationFleetsResultTypeDef,
    DescribeCapacityReservationsRequestRequestTypeDef,
    DescribeCapacityReservationsResultTypeDef,
    DescribeCarrierGatewaysRequestRequestTypeDef,
    DescribeCarrierGatewaysResultTypeDef,
    DescribeClassicLinkInstancesRequestRequestTypeDef,
    DescribeClassicLinkInstancesResultTypeDef,
    DescribeClientVpnAuthorizationRulesRequestRequestTypeDef,
    DescribeClientVpnAuthorizationRulesResultTypeDef,
    DescribeClientVpnConnectionsRequestRequestTypeDef,
    DescribeClientVpnConnectionsResultTypeDef,
    DescribeClientVpnEndpointsRequestRequestTypeDef,
    DescribeClientVpnEndpointsResultTypeDef,
    DescribeClientVpnRoutesRequestRequestTypeDef,
    DescribeClientVpnRoutesResultTypeDef,
    DescribeClientVpnTargetNetworksRequestRequestTypeDef,
    DescribeClientVpnTargetNetworksResultTypeDef,
    DescribeCoipPoolsRequestRequestTypeDef,
    DescribeCoipPoolsResultTypeDef,
    DescribeConversionTasksRequestRequestTypeDef,
    DescribeConversionTasksResultTypeDef,
    DescribeCustomerGatewaysRequestRequestTypeDef,
    DescribeCustomerGatewaysResultTypeDef,
    DescribeDhcpOptionsRequestRequestTypeDef,
    DescribeDhcpOptionsResultTypeDef,
    DescribeEgressOnlyInternetGatewaysRequestRequestTypeDef,
    DescribeEgressOnlyInternetGatewaysResultTypeDef,
    DescribeElasticGpusRequestRequestTypeDef,
    DescribeElasticGpusResultTypeDef,
    DescribeExportImageTasksRequestRequestTypeDef,
    DescribeExportImageTasksResultTypeDef,
    DescribeExportTasksRequestRequestTypeDef,
    DescribeExportTasksResultTypeDef,
    DescribeFastLaunchImagesRequestRequestTypeDef,
    DescribeFastLaunchImagesResultTypeDef,
    DescribeFastSnapshotRestoresRequestRequestTypeDef,
    DescribeFastSnapshotRestoresResultTypeDef,
    DescribeFleetHistoryRequestRequestTypeDef,
    DescribeFleetHistoryResultTypeDef,
    DescribeFleetInstancesRequestRequestTypeDef,
    DescribeFleetInstancesResultTypeDef,
    DescribeFleetsRequestRequestTypeDef,
    DescribeFleetsResultTypeDef,
    DescribeFlowLogsRequestRequestTypeDef,
    DescribeFlowLogsResultTypeDef,
    DescribeFpgaImageAttributeRequestRequestTypeDef,
    DescribeFpgaImageAttributeResultTypeDef,
    DescribeFpgaImagesRequestRequestTypeDef,
    DescribeFpgaImagesResultTypeDef,
    DescribeHostReservationOfferingsRequestRequestTypeDef,
    DescribeHostReservationOfferingsResultTypeDef,
    DescribeHostReservationsRequestRequestTypeDef,
    DescribeHostReservationsResultTypeDef,
    DescribeHostsRequestRequestTypeDef,
    DescribeHostsResultTypeDef,
    DescribeIamInstanceProfileAssociationsRequestRequestTypeDef,
    DescribeIamInstanceProfileAssociationsResultTypeDef,
    DescribeIdentityIdFormatRequestRequestTypeDef,
    DescribeIdentityIdFormatResultTypeDef,
    DescribeIdFormatRequestRequestTypeDef,
    DescribeIdFormatResultTypeDef,
    DescribeImageAttributeRequestRequestTypeDef,
    DescribeImagesRequestRequestTypeDef,
    DescribeImagesResultTypeDef,
    DescribeImportImageTasksRequestRequestTypeDef,
    DescribeImportImageTasksResultTypeDef,
    DescribeImportSnapshotTasksRequestRequestTypeDef,
    DescribeImportSnapshotTasksResultTypeDef,
    DescribeInstanceAttributeRequestRequestTypeDef,
    DescribeInstanceConnectEndpointsRequestRequestTypeDef,
    DescribeInstanceConnectEndpointsResultTypeDef,
    DescribeInstanceCreditSpecificationsRequestRequestTypeDef,
    DescribeInstanceCreditSpecificationsResultTypeDef,
    DescribeInstanceEventNotificationAttributesRequestRequestTypeDef,
    DescribeInstanceEventNotificationAttributesResultTypeDef,
    DescribeInstanceEventWindowsRequestRequestTypeDef,
    DescribeInstanceEventWindowsResultTypeDef,
    DescribeInstancesRequestRequestTypeDef,
    DescribeInstancesResultTypeDef,
    DescribeInstanceStatusRequestRequestTypeDef,
    DescribeInstanceStatusResultTypeDef,
    DescribeInstanceTopologyRequestRequestTypeDef,
    DescribeInstanceTopologyResultTypeDef,
    DescribeInstanceTypeOfferingsRequestRequestTypeDef,
    DescribeInstanceTypeOfferingsResultTypeDef,
    DescribeInstanceTypesRequestRequestTypeDef,
    DescribeInstanceTypesResultTypeDef,
    DescribeInternetGatewaysRequestRequestTypeDef,
    DescribeInternetGatewaysResultTypeDef,
    DescribeIpamByoasnRequestRequestTypeDef,
    DescribeIpamByoasnResultTypeDef,
    DescribeIpamExternalResourceVerificationTokensRequestRequestTypeDef,
    DescribeIpamExternalResourceVerificationTokensResultTypeDef,
    DescribeIpamPoolsRequestRequestTypeDef,
    DescribeIpamPoolsResultTypeDef,
    DescribeIpamResourceDiscoveriesRequestRequestTypeDef,
    DescribeIpamResourceDiscoveriesResultTypeDef,
    DescribeIpamResourceDiscoveryAssociationsRequestRequestTypeDef,
    DescribeIpamResourceDiscoveryAssociationsResultTypeDef,
    DescribeIpamScopesRequestRequestTypeDef,
    DescribeIpamScopesResultTypeDef,
    DescribeIpamsRequestRequestTypeDef,
    DescribeIpamsResultTypeDef,
    DescribeIpv6PoolsRequestRequestTypeDef,
    DescribeIpv6PoolsResultTypeDef,
    DescribeKeyPairsRequestRequestTypeDef,
    DescribeKeyPairsResultTypeDef,
    DescribeLaunchTemplatesRequestRequestTypeDef,
    DescribeLaunchTemplatesResultTypeDef,
    DescribeLaunchTemplateVersionsRequestRequestTypeDef,
    DescribeLaunchTemplateVersionsResultTypeDef,
    DescribeLocalGatewayRouteTablesRequestRequestTypeDef,
    DescribeLocalGatewayRouteTablesResultTypeDef,
    DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsRequestRequestTypeDef,
    DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsResultTypeDef,
    DescribeLocalGatewayRouteTableVpcAssociationsRequestRequestTypeDef,
    DescribeLocalGatewayRouteTableVpcAssociationsResultTypeDef,
    DescribeLocalGatewaysRequestRequestTypeDef,
    DescribeLocalGatewaysResultTypeDef,
    DescribeLocalGatewayVirtualInterfaceGroupsRequestRequestTypeDef,
    DescribeLocalGatewayVirtualInterfaceGroupsResultTypeDef,
    DescribeLocalGatewayVirtualInterfacesRequestRequestTypeDef,
    DescribeLocalGatewayVirtualInterfacesResultTypeDef,
    DescribeLockedSnapshotsRequestRequestTypeDef,
    DescribeLockedSnapshotsResultTypeDef,
    DescribeMacHostsRequestRequestTypeDef,
    DescribeMacHostsResultTypeDef,
    DescribeManagedPrefixListsRequestRequestTypeDef,
    DescribeManagedPrefixListsResultTypeDef,
    DescribeMovingAddressesRequestRequestTypeDef,
    DescribeMovingAddressesResultTypeDef,
    DescribeNatGatewaysRequestRequestTypeDef,
    DescribeNatGatewaysResultTypeDef,
    DescribeNetworkAclsRequestRequestTypeDef,
    DescribeNetworkAclsResultTypeDef,
    DescribeNetworkInsightsAccessScopeAnalysesRequestRequestTypeDef,
    DescribeNetworkInsightsAccessScopeAnalysesResultTypeDef,
    DescribeNetworkInsightsAccessScopesRequestRequestTypeDef,
    DescribeNetworkInsightsAccessScopesResultTypeDef,
    DescribeNetworkInsightsAnalysesRequestRequestTypeDef,
    DescribeNetworkInsightsAnalysesResultTypeDef,
    DescribeNetworkInsightsPathsRequestRequestTypeDef,
    DescribeNetworkInsightsPathsResultTypeDef,
    DescribeNetworkInterfaceAttributeRequestRequestTypeDef,
    DescribeNetworkInterfaceAttributeResultTypeDef,
    DescribeNetworkInterfacePermissionsRequestRequestTypeDef,
    DescribeNetworkInterfacePermissionsResultTypeDef,
    DescribeNetworkInterfacesRequestRequestTypeDef,
    DescribeNetworkInterfacesResultTypeDef,
    DescribePlacementGroupsRequestRequestTypeDef,
    DescribePlacementGroupsResultTypeDef,
    DescribePrefixListsRequestRequestTypeDef,
    DescribePrefixListsResultTypeDef,
    DescribePrincipalIdFormatRequestRequestTypeDef,
    DescribePrincipalIdFormatResultTypeDef,
    DescribePublicIpv4PoolsRequestRequestTypeDef,
    DescribePublicIpv4PoolsResultTypeDef,
    DescribeRegionsRequestRequestTypeDef,
    DescribeRegionsResultTypeDef,
    DescribeReplaceRootVolumeTasksRequestRequestTypeDef,
    DescribeReplaceRootVolumeTasksResultTypeDef,
    DescribeReservedInstancesListingsRequestRequestTypeDef,
    DescribeReservedInstancesListingsResultTypeDef,
    DescribeReservedInstancesModificationsRequestRequestTypeDef,
    DescribeReservedInstancesModificationsResultTypeDef,
    DescribeReservedInstancesOfferingsRequestRequestTypeDef,
    DescribeReservedInstancesOfferingsResultTypeDef,
    DescribeReservedInstancesRequestRequestTypeDef,
    DescribeReservedInstancesResultTypeDef,
    DescribeRouteTablesRequestRequestTypeDef,
    DescribeRouteTablesResultTypeDef,
    DescribeScheduledInstanceAvailabilityRequestRequestTypeDef,
    DescribeScheduledInstanceAvailabilityResultTypeDef,
    DescribeScheduledInstancesRequestRequestTypeDef,
    DescribeScheduledInstancesResultTypeDef,
    DescribeSecurityGroupReferencesRequestRequestTypeDef,
    DescribeSecurityGroupReferencesResultTypeDef,
    DescribeSecurityGroupRulesRequestRequestTypeDef,
    DescribeSecurityGroupRulesResultTypeDef,
    DescribeSecurityGroupsRequestRequestTypeDef,
    DescribeSecurityGroupsResultTypeDef,
    DescribeSnapshotAttributeRequestRequestTypeDef,
    DescribeSnapshotAttributeResultTypeDef,
    DescribeSnapshotsRequestRequestTypeDef,
    DescribeSnapshotsResultTypeDef,
    DescribeSnapshotTierStatusRequestRequestTypeDef,
    DescribeSnapshotTierStatusResultTypeDef,
    DescribeSpotDatafeedSubscriptionRequestRequestTypeDef,
    DescribeSpotDatafeedSubscriptionResultTypeDef,
    DescribeSpotFleetInstancesRequestRequestTypeDef,
    DescribeSpotFleetInstancesResponseTypeDef,
    DescribeSpotFleetRequestHistoryRequestRequestTypeDef,
    DescribeSpotFleetRequestHistoryResponseTypeDef,
    DescribeSpotFleetRequestsRequestRequestTypeDef,
    DescribeSpotFleetRequestsResponseTypeDef,
    DescribeSpotInstanceRequestsRequestRequestTypeDef,
    DescribeSpotInstanceRequestsResultTypeDef,
    DescribeSpotPriceHistoryRequestRequestTypeDef,
    DescribeSpotPriceHistoryResultTypeDef,
    DescribeStaleSecurityGroupsRequestRequestTypeDef,
    DescribeStaleSecurityGroupsResultTypeDef,
    DescribeStoreImageTasksRequestRequestTypeDef,
    DescribeStoreImageTasksResultTypeDef,
    DescribeSubnetsRequestRequestTypeDef,
    DescribeSubnetsResultTypeDef,
    DescribeTagsRequestRequestTypeDef,
    DescribeTagsResultTypeDef,
    DescribeTrafficMirrorFilterRulesRequestRequestTypeDef,
    DescribeTrafficMirrorFilterRulesResultTypeDef,
    DescribeTrafficMirrorFiltersRequestRequestTypeDef,
    DescribeTrafficMirrorFiltersResultTypeDef,
    DescribeTrafficMirrorSessionsRequestRequestTypeDef,
    DescribeTrafficMirrorSessionsResultTypeDef,
    DescribeTrafficMirrorTargetsRequestRequestTypeDef,
    DescribeTrafficMirrorTargetsResultTypeDef,
    DescribeTransitGatewayAttachmentsRequestRequestTypeDef,
    DescribeTransitGatewayAttachmentsResultTypeDef,
    DescribeTransitGatewayConnectPeersRequestRequestTypeDef,
    DescribeTransitGatewayConnectPeersResultTypeDef,
    DescribeTransitGatewayConnectsRequestRequestTypeDef,
    DescribeTransitGatewayConnectsResultTypeDef,
    DescribeTransitGatewayMulticastDomainsRequestRequestTypeDef,
    DescribeTransitGatewayMulticastDomainsResultTypeDef,
    DescribeTransitGatewayPeeringAttachmentsRequestRequestTypeDef,
    DescribeTransitGatewayPeeringAttachmentsResultTypeDef,
    DescribeTransitGatewayPolicyTablesRequestRequestTypeDef,
    DescribeTransitGatewayPolicyTablesResultTypeDef,
    DescribeTransitGatewayRouteTableAnnouncementsRequestRequestTypeDef,
    DescribeTransitGatewayRouteTableAnnouncementsResultTypeDef,
    DescribeTransitGatewayRouteTablesRequestRequestTypeDef,
    DescribeTransitGatewayRouteTablesResultTypeDef,
    DescribeTransitGatewaysRequestRequestTypeDef,
    DescribeTransitGatewaysResultTypeDef,
    DescribeTransitGatewayVpcAttachmentsRequestRequestTypeDef,
    DescribeTransitGatewayVpcAttachmentsResultTypeDef,
    DescribeTrunkInterfaceAssociationsRequestRequestTypeDef,
    DescribeTrunkInterfaceAssociationsResultTypeDef,
    DescribeVerifiedAccessEndpointsRequestRequestTypeDef,
    DescribeVerifiedAccessEndpointsResultTypeDef,
    DescribeVerifiedAccessGroupsRequestRequestTypeDef,
    DescribeVerifiedAccessGroupsResultTypeDef,
    DescribeVerifiedAccessInstanceLoggingConfigurationsRequestRequestTypeDef,
    DescribeVerifiedAccessInstanceLoggingConfigurationsResultTypeDef,
    DescribeVerifiedAccessInstancesRequestRequestTypeDef,
    DescribeVerifiedAccessInstancesResultTypeDef,
    DescribeVerifiedAccessTrustProvidersRequestRequestTypeDef,
    DescribeVerifiedAccessTrustProvidersResultTypeDef,
    DescribeVolumeAttributeRequestRequestTypeDef,
    DescribeVolumeAttributeResultTypeDef,
    DescribeVolumesModificationsRequestRequestTypeDef,
    DescribeVolumesModificationsResultTypeDef,
    DescribeVolumesRequestRequestTypeDef,
    DescribeVolumesResultTypeDef,
    DescribeVolumeStatusRequestRequestTypeDef,
    DescribeVolumeStatusResultTypeDef,
    DescribeVpcAttributeRequestRequestTypeDef,
    DescribeVpcAttributeResultTypeDef,
    DescribeVpcClassicLinkDnsSupportRequestRequestTypeDef,
    DescribeVpcClassicLinkDnsSupportResultTypeDef,
    DescribeVpcClassicLinkRequestRequestTypeDef,
    DescribeVpcClassicLinkResultTypeDef,
    DescribeVpcEndpointConnectionNotificationsRequestRequestTypeDef,
    DescribeVpcEndpointConnectionNotificationsResultTypeDef,
    DescribeVpcEndpointConnectionsRequestRequestTypeDef,
    DescribeVpcEndpointConnectionsResultTypeDef,
    DescribeVpcEndpointServiceConfigurationsRequestRequestTypeDef,
    DescribeVpcEndpointServiceConfigurationsResultTypeDef,
    DescribeVpcEndpointServicePermissionsRequestRequestTypeDef,
    DescribeVpcEndpointServicePermissionsResultTypeDef,
    DescribeVpcEndpointServicesRequestRequestTypeDef,
    DescribeVpcEndpointServicesResultTypeDef,
    DescribeVpcEndpointsRequestRequestTypeDef,
    DescribeVpcEndpointsResultTypeDef,
    DescribeVpcPeeringConnectionsRequestRequestTypeDef,
    DescribeVpcPeeringConnectionsResultTypeDef,
    DescribeVpcsRequestRequestTypeDef,
    DescribeVpcsResultTypeDef,
    DescribeVpnConnectionsRequestRequestTypeDef,
    DescribeVpnConnectionsResultTypeDef,
    DescribeVpnGatewaysRequestRequestTypeDef,
    DescribeVpnGatewaysResultTypeDef,
    DetachClassicLinkVpcRequestRequestTypeDef,
    DetachClassicLinkVpcResultTypeDef,
    DetachInternetGatewayRequestRequestTypeDef,
    DetachNetworkInterfaceRequestRequestTypeDef,
    DetachVerifiedAccessTrustProviderRequestRequestTypeDef,
    DetachVerifiedAccessTrustProviderResultTypeDef,
    DetachVolumeRequestRequestTypeDef,
    DetachVpnGatewayRequestRequestTypeDef,
    DisableAddressTransferRequestRequestTypeDef,
    DisableAddressTransferResultTypeDef,
    DisableAwsNetworkPerformanceMetricSubscriptionRequestRequestTypeDef,
    DisableAwsNetworkPerformanceMetricSubscriptionResultTypeDef,
    DisableEbsEncryptionByDefaultRequestRequestTypeDef,
    DisableEbsEncryptionByDefaultResultTypeDef,
    DisableFastLaunchRequestRequestTypeDef,
    DisableFastLaunchResultTypeDef,
    DisableFastSnapshotRestoresRequestRequestTypeDef,
    DisableFastSnapshotRestoresResultTypeDef,
    DisableImageBlockPublicAccessRequestRequestTypeDef,
    DisableImageBlockPublicAccessResultTypeDef,
    DisableImageDeprecationRequestRequestTypeDef,
    DisableImageDeprecationResultTypeDef,
    DisableImageDeregistrationProtectionRequestRequestTypeDef,
    DisableImageDeregistrationProtectionResultTypeDef,
    DisableImageRequestRequestTypeDef,
    DisableImageResultTypeDef,
    DisableIpamOrganizationAdminAccountRequestRequestTypeDef,
    DisableIpamOrganizationAdminAccountResultTypeDef,
    DisableSerialConsoleAccessRequestRequestTypeDef,
    DisableSerialConsoleAccessResultTypeDef,
    DisableSnapshotBlockPublicAccessRequestRequestTypeDef,
    DisableSnapshotBlockPublicAccessResultTypeDef,
    DisableTransitGatewayRouteTablePropagationRequestRequestTypeDef,
    DisableTransitGatewayRouteTablePropagationResultTypeDef,
    DisableVgwRoutePropagationRequestRequestTypeDef,
    DisableVpcClassicLinkDnsSupportRequestRequestTypeDef,
    DisableVpcClassicLinkDnsSupportResultTypeDef,
    DisableVpcClassicLinkRequestRequestTypeDef,
    DisableVpcClassicLinkResultTypeDef,
    DisassociateAddressRequestRequestTypeDef,
    DisassociateClientVpnTargetNetworkRequestRequestTypeDef,
    DisassociateClientVpnTargetNetworkResultTypeDef,
    DisassociateEnclaveCertificateIamRoleRequestRequestTypeDef,
    DisassociateEnclaveCertificateIamRoleResultTypeDef,
    DisassociateIamInstanceProfileRequestRequestTypeDef,
    DisassociateIamInstanceProfileResultTypeDef,
    DisassociateInstanceEventWindowRequestRequestTypeDef,
    DisassociateInstanceEventWindowResultTypeDef,
    DisassociateIpamByoasnRequestRequestTypeDef,
    DisassociateIpamByoasnResultTypeDef,
    DisassociateIpamResourceDiscoveryRequestRequestTypeDef,
    DisassociateIpamResourceDiscoveryResultTypeDef,
    DisassociateNatGatewayAddressRequestRequestTypeDef,
    DisassociateNatGatewayAddressResultTypeDef,
    DisassociateRouteTableRequestRequestTypeDef,
    DisassociateSubnetCidrBlockRequestRequestTypeDef,
    DisassociateSubnetCidrBlockResultTypeDef,
    DisassociateTransitGatewayMulticastDomainRequestRequestTypeDef,
    DisassociateTransitGatewayMulticastDomainResultTypeDef,
    DisassociateTransitGatewayPolicyTableRequestRequestTypeDef,
    DisassociateTransitGatewayPolicyTableResultTypeDef,
    DisassociateTransitGatewayRouteTableRequestRequestTypeDef,
    DisassociateTransitGatewayRouteTableResultTypeDef,
    DisassociateTrunkInterfaceRequestRequestTypeDef,
    DisassociateTrunkInterfaceResultTypeDef,
    DisassociateVpcCidrBlockRequestRequestTypeDef,
    DisassociateVpcCidrBlockResultTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableAddressTransferRequestRequestTypeDef,
    EnableAddressTransferResultTypeDef,
    EnableAwsNetworkPerformanceMetricSubscriptionRequestRequestTypeDef,
    EnableAwsNetworkPerformanceMetricSubscriptionResultTypeDef,
    EnableEbsEncryptionByDefaultRequestRequestTypeDef,
    EnableEbsEncryptionByDefaultResultTypeDef,
    EnableFastLaunchRequestRequestTypeDef,
    EnableFastLaunchResultTypeDef,
    EnableFastSnapshotRestoresRequestRequestTypeDef,
    EnableFastSnapshotRestoresResultTypeDef,
    EnableImageBlockPublicAccessRequestRequestTypeDef,
    EnableImageBlockPublicAccessResultTypeDef,
    EnableImageDeprecationRequestRequestTypeDef,
    EnableImageDeprecationResultTypeDef,
    EnableImageDeregistrationProtectionRequestRequestTypeDef,
    EnableImageDeregistrationProtectionResultTypeDef,
    EnableImageRequestRequestTypeDef,
    EnableImageResultTypeDef,
    EnableIpamOrganizationAdminAccountRequestRequestTypeDef,
    EnableIpamOrganizationAdminAccountResultTypeDef,
    EnableReachabilityAnalyzerOrganizationSharingRequestRequestTypeDef,
    EnableReachabilityAnalyzerOrganizationSharingResultTypeDef,
    EnableSerialConsoleAccessRequestRequestTypeDef,
    EnableSerialConsoleAccessResultTypeDef,
    EnableSnapshotBlockPublicAccessRequestRequestTypeDef,
    EnableSnapshotBlockPublicAccessResultTypeDef,
    EnableTransitGatewayRouteTablePropagationRequestRequestTypeDef,
    EnableTransitGatewayRouteTablePropagationResultTypeDef,
    EnableVgwRoutePropagationRequestRequestTypeDef,
    EnableVolumeIORequestRequestTypeDef,
    EnableVpcClassicLinkDnsSupportRequestRequestTypeDef,
    EnableVpcClassicLinkDnsSupportResultTypeDef,
    EnableVpcClassicLinkRequestRequestTypeDef,
    EnableVpcClassicLinkResultTypeDef,
    ExportClientVpnClientCertificateRevocationListRequestRequestTypeDef,
    ExportClientVpnClientCertificateRevocationListResultTypeDef,
    ExportClientVpnClientConfigurationRequestRequestTypeDef,
    ExportClientVpnClientConfigurationResultTypeDef,
    ExportImageRequestRequestTypeDef,
    ExportImageResultTypeDef,
    ExportTransitGatewayRoutesRequestRequestTypeDef,
    ExportTransitGatewayRoutesResultTypeDef,
    GetAssociatedEnclaveCertificateIamRolesRequestRequestTypeDef,
    GetAssociatedEnclaveCertificateIamRolesResultTypeDef,
    GetAssociatedIpv6PoolCidrsRequestRequestTypeDef,
    GetAssociatedIpv6PoolCidrsResultTypeDef,
    GetAwsNetworkPerformanceDataRequestRequestTypeDef,
    GetAwsNetworkPerformanceDataResultTypeDef,
    GetCapacityReservationUsageRequestRequestTypeDef,
    GetCapacityReservationUsageResultTypeDef,
    GetCoipPoolUsageRequestRequestTypeDef,
    GetCoipPoolUsageResultTypeDef,
    GetConsoleOutputRequestRequestTypeDef,
    GetConsoleOutputResultTypeDef,
    GetConsoleScreenshotRequestRequestTypeDef,
    GetConsoleScreenshotResultTypeDef,
    GetDefaultCreditSpecificationRequestRequestTypeDef,
    GetDefaultCreditSpecificationResultTypeDef,
    GetEbsDefaultKmsKeyIdRequestRequestTypeDef,
    GetEbsDefaultKmsKeyIdResultTypeDef,
    GetEbsEncryptionByDefaultRequestRequestTypeDef,
    GetEbsEncryptionByDefaultResultTypeDef,
    GetFlowLogsIntegrationTemplateRequestRequestTypeDef,
    GetFlowLogsIntegrationTemplateResultTypeDef,
    GetGroupsForCapacityReservationRequestRequestTypeDef,
    GetGroupsForCapacityReservationResultTypeDef,
    GetHostReservationPurchasePreviewRequestRequestTypeDef,
    GetHostReservationPurchasePreviewResultTypeDef,
    GetImageBlockPublicAccessStateRequestRequestTypeDef,
    GetImageBlockPublicAccessStateResultTypeDef,
    GetInstanceMetadataDefaultsRequestRequestTypeDef,
    GetInstanceMetadataDefaultsResultTypeDef,
    GetInstanceTpmEkPubRequestRequestTypeDef,
    GetInstanceTpmEkPubResultTypeDef,
    GetInstanceTypesFromInstanceRequirementsRequestRequestTypeDef,
    GetInstanceTypesFromInstanceRequirementsResultTypeDef,
    GetInstanceUefiDataRequestRequestTypeDef,
    GetInstanceUefiDataResultTypeDef,
    GetIpamAddressHistoryRequestRequestTypeDef,
    GetIpamAddressHistoryResultTypeDef,
    GetIpamDiscoveredAccountsRequestRequestTypeDef,
    GetIpamDiscoveredAccountsResultTypeDef,
    GetIpamDiscoveredPublicAddressesRequestRequestTypeDef,
    GetIpamDiscoveredPublicAddressesResultTypeDef,
    GetIpamDiscoveredResourceCidrsRequestRequestTypeDef,
    GetIpamDiscoveredResourceCidrsResultTypeDef,
    GetIpamPoolAllocationsRequestRequestTypeDef,
    GetIpamPoolAllocationsResultTypeDef,
    GetIpamPoolCidrsRequestRequestTypeDef,
    GetIpamPoolCidrsResultTypeDef,
    GetIpamResourceCidrsRequestRequestTypeDef,
    GetIpamResourceCidrsResultTypeDef,
    GetLaunchTemplateDataRequestRequestTypeDef,
    GetLaunchTemplateDataResultTypeDef,
    GetManagedPrefixListAssociationsRequestRequestTypeDef,
    GetManagedPrefixListAssociationsResultTypeDef,
    GetManagedPrefixListEntriesRequestRequestTypeDef,
    GetManagedPrefixListEntriesResultTypeDef,
    GetNetworkInsightsAccessScopeAnalysisFindingsRequestRequestTypeDef,
    GetNetworkInsightsAccessScopeAnalysisFindingsResultTypeDef,
    GetNetworkInsightsAccessScopeContentRequestRequestTypeDef,
    GetNetworkInsightsAccessScopeContentResultTypeDef,
    GetPasswordDataRequestRequestTypeDef,
    GetPasswordDataResultTypeDef,
    GetReservedInstancesExchangeQuoteRequestRequestTypeDef,
    GetReservedInstancesExchangeQuoteResultTypeDef,
    GetSecurityGroupsForVpcRequestRequestTypeDef,
    GetSecurityGroupsForVpcResultTypeDef,
    GetSerialConsoleAccessStatusRequestRequestTypeDef,
    GetSerialConsoleAccessStatusResultTypeDef,
    GetSnapshotBlockPublicAccessStateRequestRequestTypeDef,
    GetSnapshotBlockPublicAccessStateResultTypeDef,
    GetSpotPlacementScoresRequestRequestTypeDef,
    GetSpotPlacementScoresResultTypeDef,
    GetSubnetCidrReservationsRequestRequestTypeDef,
    GetSubnetCidrReservationsResultTypeDef,
    GetTransitGatewayAttachmentPropagationsRequestRequestTypeDef,
    GetTransitGatewayAttachmentPropagationsResultTypeDef,
    GetTransitGatewayMulticastDomainAssociationsRequestRequestTypeDef,
    GetTransitGatewayMulticastDomainAssociationsResultTypeDef,
    GetTransitGatewayPolicyTableAssociationsRequestRequestTypeDef,
    GetTransitGatewayPolicyTableAssociationsResultTypeDef,
    GetTransitGatewayPolicyTableEntriesRequestRequestTypeDef,
    GetTransitGatewayPolicyTableEntriesResultTypeDef,
    GetTransitGatewayPrefixListReferencesRequestRequestTypeDef,
    GetTransitGatewayPrefixListReferencesResultTypeDef,
    GetTransitGatewayRouteTableAssociationsRequestRequestTypeDef,
    GetTransitGatewayRouteTableAssociationsResultTypeDef,
    GetTransitGatewayRouteTablePropagationsRequestRequestTypeDef,
    GetTransitGatewayRouteTablePropagationsResultTypeDef,
    GetVerifiedAccessEndpointPolicyRequestRequestTypeDef,
    GetVerifiedAccessEndpointPolicyResultTypeDef,
    GetVerifiedAccessGroupPolicyRequestRequestTypeDef,
    GetVerifiedAccessGroupPolicyResultTypeDef,
    GetVpnConnectionDeviceSampleConfigurationRequestRequestTypeDef,
    GetVpnConnectionDeviceSampleConfigurationResultTypeDef,
    GetVpnConnectionDeviceTypesRequestRequestTypeDef,
    GetVpnConnectionDeviceTypesResultTypeDef,
    GetVpnTunnelReplacementStatusRequestRequestTypeDef,
    GetVpnTunnelReplacementStatusResultTypeDef,
    ImageAttributeTypeDef,
    ImportClientVpnClientCertificateRevocationListRequestRequestTypeDef,
    ImportClientVpnClientCertificateRevocationListResultTypeDef,
    ImportImageRequestRequestTypeDef,
    ImportImageResultTypeDef,
    ImportInstanceRequestRequestTypeDef,
    ImportInstanceResultTypeDef,
    ImportKeyPairRequestRequestTypeDef,
    ImportKeyPairResultTypeDef,
    ImportSnapshotRequestRequestTypeDef,
    ImportSnapshotResultTypeDef,
    ImportVolumeRequestRequestTypeDef,
    ImportVolumeResultTypeDef,
    InstanceAttributeTypeDef,
    KeyPairTypeDef,
    ListImagesInRecycleBinRequestRequestTypeDef,
    ListImagesInRecycleBinResultTypeDef,
    ListSnapshotsInRecycleBinRequestRequestTypeDef,
    ListSnapshotsInRecycleBinResultTypeDef,
    LockSnapshotRequestRequestTypeDef,
    LockSnapshotResultTypeDef,
    ModifyAddressAttributeRequestRequestTypeDef,
    ModifyAddressAttributeResultTypeDef,
    ModifyAvailabilityZoneGroupRequestRequestTypeDef,
    ModifyAvailabilityZoneGroupResultTypeDef,
    ModifyCapacityReservationFleetRequestRequestTypeDef,
    ModifyCapacityReservationFleetResultTypeDef,
    ModifyCapacityReservationRequestRequestTypeDef,
    ModifyCapacityReservationResultTypeDef,
    ModifyClientVpnEndpointRequestRequestTypeDef,
    ModifyClientVpnEndpointResultTypeDef,
    ModifyDefaultCreditSpecificationRequestRequestTypeDef,
    ModifyDefaultCreditSpecificationResultTypeDef,
    ModifyEbsDefaultKmsKeyIdRequestRequestTypeDef,
    ModifyEbsDefaultKmsKeyIdResultTypeDef,
    ModifyFleetRequestRequestTypeDef,
    ModifyFleetResultTypeDef,
    ModifyFpgaImageAttributeRequestRequestTypeDef,
    ModifyFpgaImageAttributeResultTypeDef,
    ModifyHostsRequestRequestTypeDef,
    ModifyHostsResultTypeDef,
    ModifyIdentityIdFormatRequestRequestTypeDef,
    ModifyIdFormatRequestRequestTypeDef,
    ModifyImageAttributeRequestRequestTypeDef,
    ModifyInstanceAttributeRequestRequestTypeDef,
    ModifyInstanceCapacityReservationAttributesRequestRequestTypeDef,
    ModifyInstanceCapacityReservationAttributesResultTypeDef,
    ModifyInstanceCpuOptionsRequestRequestTypeDef,
    ModifyInstanceCpuOptionsResultTypeDef,
    ModifyInstanceCreditSpecificationRequestRequestTypeDef,
    ModifyInstanceCreditSpecificationResultTypeDef,
    ModifyInstanceEventStartTimeRequestRequestTypeDef,
    ModifyInstanceEventStartTimeResultTypeDef,
    ModifyInstanceEventWindowRequestRequestTypeDef,
    ModifyInstanceEventWindowResultTypeDef,
    ModifyInstanceMaintenanceOptionsRequestRequestTypeDef,
    ModifyInstanceMaintenanceOptionsResultTypeDef,
    ModifyInstanceMetadataDefaultsRequestRequestTypeDef,
    ModifyInstanceMetadataDefaultsResultTypeDef,
    ModifyInstanceMetadataOptionsRequestRequestTypeDef,
    ModifyInstanceMetadataOptionsResultTypeDef,
    ModifyInstancePlacementRequestRequestTypeDef,
    ModifyInstancePlacementResultTypeDef,
    ModifyIpamPoolRequestRequestTypeDef,
    ModifyIpamPoolResultTypeDef,
    ModifyIpamRequestRequestTypeDef,
    ModifyIpamResourceCidrRequestRequestTypeDef,
    ModifyIpamResourceCidrResultTypeDef,
    ModifyIpamResourceDiscoveryRequestRequestTypeDef,
    ModifyIpamResourceDiscoveryResultTypeDef,
    ModifyIpamResultTypeDef,
    ModifyIpamScopeRequestRequestTypeDef,
    ModifyIpamScopeResultTypeDef,
    ModifyLaunchTemplateRequestRequestTypeDef,
    ModifyLaunchTemplateResultTypeDef,
    ModifyLocalGatewayRouteRequestRequestTypeDef,
    ModifyLocalGatewayRouteResultTypeDef,
    ModifyManagedPrefixListRequestRequestTypeDef,
    ModifyManagedPrefixListResultTypeDef,
    ModifyNetworkInterfaceAttributeRequestRequestTypeDef,
    ModifyPrivateDnsNameOptionsRequestRequestTypeDef,
    ModifyPrivateDnsNameOptionsResultTypeDef,
    ModifyReservedInstancesRequestRequestTypeDef,
    ModifyReservedInstancesResultTypeDef,
    ModifySecurityGroupRulesRequestRequestTypeDef,
    ModifySecurityGroupRulesResultTypeDef,
    ModifySnapshotAttributeRequestRequestTypeDef,
    ModifySnapshotTierRequestRequestTypeDef,
    ModifySnapshotTierResultTypeDef,
    ModifySpotFleetRequestRequestRequestTypeDef,
    ModifySpotFleetRequestResponseTypeDef,
    ModifySubnetAttributeRequestRequestTypeDef,
    ModifyTrafficMirrorFilterNetworkServicesRequestRequestTypeDef,
    ModifyTrafficMirrorFilterNetworkServicesResultTypeDef,
    ModifyTrafficMirrorFilterRuleRequestRequestTypeDef,
    ModifyTrafficMirrorFilterRuleResultTypeDef,
    ModifyTrafficMirrorSessionRequestRequestTypeDef,
    ModifyTrafficMirrorSessionResultTypeDef,
    ModifyTransitGatewayPrefixListReferenceRequestRequestTypeDef,
    ModifyTransitGatewayPrefixListReferenceResultTypeDef,
    ModifyTransitGatewayRequestRequestTypeDef,
    ModifyTransitGatewayResultTypeDef,
    ModifyTransitGatewayVpcAttachmentRequestRequestTypeDef,
    ModifyTransitGatewayVpcAttachmentResultTypeDef,
    ModifyVerifiedAccessEndpointPolicyRequestRequestTypeDef,
    ModifyVerifiedAccessEndpointPolicyResultTypeDef,
    ModifyVerifiedAccessEndpointRequestRequestTypeDef,
    ModifyVerifiedAccessEndpointResultTypeDef,
    ModifyVerifiedAccessGroupPolicyRequestRequestTypeDef,
    ModifyVerifiedAccessGroupPolicyResultTypeDef,
    ModifyVerifiedAccessGroupRequestRequestTypeDef,
    ModifyVerifiedAccessGroupResultTypeDef,
    ModifyVerifiedAccessInstanceLoggingConfigurationRequestRequestTypeDef,
    ModifyVerifiedAccessInstanceLoggingConfigurationResultTypeDef,
    ModifyVerifiedAccessInstanceRequestRequestTypeDef,
    ModifyVerifiedAccessInstanceResultTypeDef,
    ModifyVerifiedAccessTrustProviderRequestRequestTypeDef,
    ModifyVerifiedAccessTrustProviderResultTypeDef,
    ModifyVolumeAttributeRequestRequestTypeDef,
    ModifyVolumeRequestRequestTypeDef,
    ModifyVolumeResultTypeDef,
    ModifyVpcAttributeRequestRequestTypeDef,
    ModifyVpcEndpointConnectionNotificationRequestRequestTypeDef,
    ModifyVpcEndpointConnectionNotificationResultTypeDef,
    ModifyVpcEndpointRequestRequestTypeDef,
    ModifyVpcEndpointResultTypeDef,
    ModifyVpcEndpointServiceConfigurationRequestRequestTypeDef,
    ModifyVpcEndpointServiceConfigurationResultTypeDef,
    ModifyVpcEndpointServicePayerResponsibilityRequestRequestTypeDef,
    ModifyVpcEndpointServicePayerResponsibilityResultTypeDef,
    ModifyVpcEndpointServicePermissionsRequestRequestTypeDef,
    ModifyVpcEndpointServicePermissionsResultTypeDef,
    ModifyVpcPeeringConnectionOptionsRequestRequestTypeDef,
    ModifyVpcPeeringConnectionOptionsResultTypeDef,
    ModifyVpcTenancyRequestRequestTypeDef,
    ModifyVpcTenancyResultTypeDef,
    ModifyVpnConnectionOptionsRequestRequestTypeDef,
    ModifyVpnConnectionOptionsResultTypeDef,
    ModifyVpnConnectionRequestRequestTypeDef,
    ModifyVpnConnectionResultTypeDef,
    ModifyVpnTunnelCertificateRequestRequestTypeDef,
    ModifyVpnTunnelCertificateResultTypeDef,
    ModifyVpnTunnelOptionsRequestRequestTypeDef,
    ModifyVpnTunnelOptionsResultTypeDef,
    MonitorInstancesRequestRequestTypeDef,
    MonitorInstancesResultTypeDef,
    MoveAddressToVpcRequestRequestTypeDef,
    MoveAddressToVpcResultTypeDef,
    MoveByoipCidrToIpamRequestRequestTypeDef,
    MoveByoipCidrToIpamResultTypeDef,
    MoveCapacityReservationInstancesRequestRequestTypeDef,
    MoveCapacityReservationInstancesResultTypeDef,
    ProvisionByoipCidrRequestRequestTypeDef,
    ProvisionByoipCidrResultTypeDef,
    ProvisionIpamByoasnRequestRequestTypeDef,
    ProvisionIpamByoasnResultTypeDef,
    ProvisionIpamPoolCidrRequestRequestTypeDef,
    ProvisionIpamPoolCidrResultTypeDef,
    ProvisionPublicIpv4PoolCidrRequestRequestTypeDef,
    ProvisionPublicIpv4PoolCidrResultTypeDef,
    PurchaseCapacityBlockRequestRequestTypeDef,
    PurchaseCapacityBlockResultTypeDef,
    PurchaseHostReservationRequestRequestTypeDef,
    PurchaseHostReservationResultTypeDef,
    PurchaseReservedInstancesOfferingRequestRequestTypeDef,
    PurchaseReservedInstancesOfferingResultTypeDef,
    PurchaseScheduledInstancesRequestRequestTypeDef,
    PurchaseScheduledInstancesResultTypeDef,
    RebootInstancesRequestRequestTypeDef,
    RegisterImageRequestRequestTypeDef,
    RegisterImageResultTypeDef,
    RegisterInstanceEventNotificationAttributesRequestRequestTypeDef,
    RegisterInstanceEventNotificationAttributesResultTypeDef,
    RegisterTransitGatewayMulticastGroupMembersRequestRequestTypeDef,
    RegisterTransitGatewayMulticastGroupMembersResultTypeDef,
    RegisterTransitGatewayMulticastGroupSourcesRequestRequestTypeDef,
    RegisterTransitGatewayMulticastGroupSourcesResultTypeDef,
    RejectTransitGatewayMulticastDomainAssociationsRequestRequestTypeDef,
    RejectTransitGatewayMulticastDomainAssociationsResultTypeDef,
    RejectTransitGatewayPeeringAttachmentRequestRequestTypeDef,
    RejectTransitGatewayPeeringAttachmentResultTypeDef,
    RejectTransitGatewayVpcAttachmentRequestRequestTypeDef,
    RejectTransitGatewayVpcAttachmentResultTypeDef,
    RejectVpcEndpointConnectionsRequestRequestTypeDef,
    RejectVpcEndpointConnectionsResultTypeDef,
    RejectVpcPeeringConnectionRequestRequestTypeDef,
    RejectVpcPeeringConnectionResultTypeDef,
    ReleaseAddressRequestRequestTypeDef,
    ReleaseHostsRequestRequestTypeDef,
    ReleaseHostsResultTypeDef,
    ReleaseIpamPoolAllocationRequestRequestTypeDef,
    ReleaseIpamPoolAllocationResultTypeDef,
    ReplaceIamInstanceProfileAssociationRequestRequestTypeDef,
    ReplaceIamInstanceProfileAssociationResultTypeDef,
    ReplaceNetworkAclAssociationRequestRequestTypeDef,
    ReplaceNetworkAclAssociationResultTypeDef,
    ReplaceNetworkAclEntryRequestRequestTypeDef,
    ReplaceRouteRequestRequestTypeDef,
    ReplaceRouteTableAssociationRequestRequestTypeDef,
    ReplaceRouteTableAssociationResultTypeDef,
    ReplaceTransitGatewayRouteRequestRequestTypeDef,
    ReplaceTransitGatewayRouteResultTypeDef,
    ReplaceVpnTunnelRequestRequestTypeDef,
    ReplaceVpnTunnelResultTypeDef,
    ReportInstanceStatusRequestRequestTypeDef,
    RequestSpotFleetRequestRequestTypeDef,
    RequestSpotFleetResponseTypeDef,
    RequestSpotInstancesRequestRequestTypeDef,
    RequestSpotInstancesResultTypeDef,
    ReservationResponseTypeDef,
    ResetAddressAttributeRequestRequestTypeDef,
    ResetAddressAttributeResultTypeDef,
    ResetEbsDefaultKmsKeyIdRequestRequestTypeDef,
    ResetEbsDefaultKmsKeyIdResultTypeDef,
    ResetFpgaImageAttributeRequestRequestTypeDef,
    ResetFpgaImageAttributeResultTypeDef,
    ResetImageAttributeRequestRequestTypeDef,
    ResetInstanceAttributeRequestRequestTypeDef,
    ResetNetworkInterfaceAttributeRequestRequestTypeDef,
    ResetSnapshotAttributeRequestRequestTypeDef,
    RestoreAddressToClassicRequestRequestTypeDef,
    RestoreAddressToClassicResultTypeDef,
    RestoreImageFromRecycleBinRequestRequestTypeDef,
    RestoreImageFromRecycleBinResultTypeDef,
    RestoreManagedPrefixListVersionRequestRequestTypeDef,
    RestoreManagedPrefixListVersionResultTypeDef,
    RestoreSnapshotFromRecycleBinRequestRequestTypeDef,
    RestoreSnapshotFromRecycleBinResultTypeDef,
    RestoreSnapshotTierRequestRequestTypeDef,
    RestoreSnapshotTierResultTypeDef,
    RevokeClientVpnIngressRequestRequestTypeDef,
    RevokeClientVpnIngressResultTypeDef,
    RevokeSecurityGroupEgressRequestRequestTypeDef,
    RevokeSecurityGroupEgressResultTypeDef,
    RevokeSecurityGroupIngressRequestRequestTypeDef,
    RevokeSecurityGroupIngressResultTypeDef,
    RunInstancesRequestRequestTypeDef,
    RunScheduledInstancesRequestRequestTypeDef,
    RunScheduledInstancesResultTypeDef,
    SearchLocalGatewayRoutesRequestRequestTypeDef,
    SearchLocalGatewayRoutesResultTypeDef,
    SearchTransitGatewayMulticastGroupsRequestRequestTypeDef,
    SearchTransitGatewayMulticastGroupsResultTypeDef,
    SearchTransitGatewayRoutesRequestRequestTypeDef,
    SearchTransitGatewayRoutesResultTypeDef,
    SendDiagnosticInterruptRequestRequestTypeDef,
    SnapshotResponseTypeDef,
    StartInstancesRequestRequestTypeDef,
    StartInstancesResultTypeDef,
    StartNetworkInsightsAccessScopeAnalysisRequestRequestTypeDef,
    StartNetworkInsightsAccessScopeAnalysisResultTypeDef,
    StartNetworkInsightsAnalysisRequestRequestTypeDef,
    StartNetworkInsightsAnalysisResultTypeDef,
    StartVpcEndpointServicePrivateDnsVerificationRequestRequestTypeDef,
    StartVpcEndpointServicePrivateDnsVerificationResultTypeDef,
    StopInstancesRequestRequestTypeDef,
    StopInstancesResultTypeDef,
    TerminateClientVpnConnectionsRequestRequestTypeDef,
    TerminateClientVpnConnectionsResultTypeDef,
    TerminateInstancesRequestRequestTypeDef,
    TerminateInstancesResultTypeDef,
    UnassignIpv6AddressesRequestRequestTypeDef,
    UnassignIpv6AddressesResultTypeDef,
    UnassignPrivateIpAddressesRequestRequestTypeDef,
    UnassignPrivateNatGatewayAddressRequestRequestTypeDef,
    UnassignPrivateNatGatewayAddressResultTypeDef,
    UnlockSnapshotRequestRequestTypeDef,
    UnlockSnapshotResultTypeDef,
    UnmonitorInstancesRequestRequestTypeDef,
    UnmonitorInstancesResultTypeDef,
    UpdateSecurityGroupRuleDescriptionsEgressRequestRequestTypeDef,
    UpdateSecurityGroupRuleDescriptionsEgressResultTypeDef,
    UpdateSecurityGroupRuleDescriptionsIngressRequestRequestTypeDef,
    UpdateSecurityGroupRuleDescriptionsIngressResultTypeDef,
    VolumeAttachmentResponseTypeDef,
    VolumeResponseTypeDef,
    WithdrawByoipCidrRequestRequestTypeDef,
    WithdrawByoipCidrResultTypeDef,
)
from .waiter import (
    BundleTaskCompleteWaiter,
    ConversionTaskCancelledWaiter,
    ConversionTaskCompletedWaiter,
    ConversionTaskDeletedWaiter,
    CustomerGatewayAvailableWaiter,
    ExportTaskCancelledWaiter,
    ExportTaskCompletedWaiter,
    ImageAvailableWaiter,
    ImageExistsWaiter,
    InstanceExistsWaiter,
    InstanceRunningWaiter,
    InstanceStatusOkWaiter,
    InstanceStoppedWaiter,
    InstanceTerminatedWaiter,
    InternetGatewayExistsWaiter,
    KeyPairExistsWaiter,
    NatGatewayAvailableWaiter,
    NatGatewayDeletedWaiter,
    NetworkInterfaceAvailableWaiter,
    PasswordDataAvailableWaiter,
    SecurityGroupExistsWaiter,
    SnapshotCompletedWaiter,
    SnapshotImportedWaiter,
    SpotInstanceRequestFulfilledWaiter,
    StoreImageTaskCompleteWaiter,
    SubnetAvailableWaiter,
    SystemStatusOkWaiter,
    VolumeAvailableWaiter,
    VolumeDeletedWaiter,
    VolumeInUseWaiter,
    VpcAvailableWaiter,
    VpcExistsWaiter,
    VpcPeeringConnectionDeletedWaiter,
    VpcPeeringConnectionExistsWaiter,
    VpnConnectionAvailableWaiter,
    VpnConnectionDeletedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("EC2Client",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]


class EC2Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EC2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#close)
        """

    async def accept_address_transfer(
        self, **kwargs: Unpack[AcceptAddressTransferRequestRequestTypeDef]
    ) -> AcceptAddressTransferResultTypeDef:
        """
        Accepts an Elastic IP address transfer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/accept_address_transfer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#accept_address_transfer)
        """

    async def accept_reserved_instances_exchange_quote(
        self, **kwargs: Unpack[AcceptReservedInstancesExchangeQuoteRequestRequestTypeDef]
    ) -> AcceptReservedInstancesExchangeQuoteResultTypeDef:
        """
        Accepts the Convertible Reserved Instance exchange quote described in the
        <a>GetReservedInstancesExchangeQuote</a> call.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/accept_reserved_instances_exchange_quote.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#accept_reserved_instances_exchange_quote)
        """

    async def accept_transit_gateway_multicast_domain_associations(
        self, **kwargs: Unpack[AcceptTransitGatewayMulticastDomainAssociationsRequestRequestTypeDef]
    ) -> AcceptTransitGatewayMulticastDomainAssociationsResultTypeDef:
        """
        Accepts a request to associate subnets with a transit gateway multicast domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/accept_transit_gateway_multicast_domain_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#accept_transit_gateway_multicast_domain_associations)
        """

    async def accept_transit_gateway_peering_attachment(
        self, **kwargs: Unpack[AcceptTransitGatewayPeeringAttachmentRequestRequestTypeDef]
    ) -> AcceptTransitGatewayPeeringAttachmentResultTypeDef:
        """
        Accepts a transit gateway peering attachment request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/accept_transit_gateway_peering_attachment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#accept_transit_gateway_peering_attachment)
        """

    async def accept_transit_gateway_vpc_attachment(
        self, **kwargs: Unpack[AcceptTransitGatewayVpcAttachmentRequestRequestTypeDef]
    ) -> AcceptTransitGatewayVpcAttachmentResultTypeDef:
        """
        Accepts a request to attach a VPC to a transit gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/accept_transit_gateway_vpc_attachment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#accept_transit_gateway_vpc_attachment)
        """

    async def accept_vpc_endpoint_connections(
        self, **kwargs: Unpack[AcceptVpcEndpointConnectionsRequestRequestTypeDef]
    ) -> AcceptVpcEndpointConnectionsResultTypeDef:
        """
        Accepts connection requests to your VPC endpoint service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/accept_vpc_endpoint_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#accept_vpc_endpoint_connections)
        """

    async def accept_vpc_peering_connection(
        self, **kwargs: Unpack[AcceptVpcPeeringConnectionRequestRequestTypeDef]
    ) -> AcceptVpcPeeringConnectionResultTypeDef:
        """
        Accept a VPC peering connection request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/accept_vpc_peering_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#accept_vpc_peering_connection)
        """

    async def advertise_byoip_cidr(
        self, **kwargs: Unpack[AdvertiseByoipCidrRequestRequestTypeDef]
    ) -> AdvertiseByoipCidrResultTypeDef:
        """
        Advertises an IPv4 or IPv6 address range that is provisioned for use with your
        Amazon Web Services resources through bring your own IP addresses (BYOIP).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/advertise_byoip_cidr.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#advertise_byoip_cidr)
        """

    async def allocate_address(
        self, **kwargs: Unpack[AllocateAddressRequestRequestTypeDef]
    ) -> AllocateAddressResultTypeDef:
        """
        Allocates an Elastic IP address to your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/allocate_address.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#allocate_address)
        """

    async def allocate_hosts(
        self, **kwargs: Unpack[AllocateHostsRequestRequestTypeDef]
    ) -> AllocateHostsResultTypeDef:
        """
        Allocates a Dedicated Host to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/allocate_hosts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#allocate_hosts)
        """

    async def allocate_ipam_pool_cidr(
        self, **kwargs: Unpack[AllocateIpamPoolCidrRequestRequestTypeDef]
    ) -> AllocateIpamPoolCidrResultTypeDef:
        """
        Allocate a CIDR from an IPAM pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/allocate_ipam_pool_cidr.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#allocate_ipam_pool_cidr)
        """

    async def apply_security_groups_to_client_vpn_target_network(
        self, **kwargs: Unpack[ApplySecurityGroupsToClientVpnTargetNetworkRequestRequestTypeDef]
    ) -> ApplySecurityGroupsToClientVpnTargetNetworkResultTypeDef:
        """
        Applies a security group to the association between the target network and the
        Client VPN endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/apply_security_groups_to_client_vpn_target_network.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#apply_security_groups_to_client_vpn_target_network)
        """

    async def assign_ipv6_addresses(
        self, **kwargs: Unpack[AssignIpv6AddressesRequestRequestTypeDef]
    ) -> AssignIpv6AddressesResultTypeDef:
        """
        Assigns one or more IPv6 addresses to the specified network interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/assign_ipv6_addresses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#assign_ipv6_addresses)
        """

    async def assign_private_ip_addresses(
        self, **kwargs: Unpack[AssignPrivateIpAddressesRequestRequestTypeDef]
    ) -> AssignPrivateIpAddressesResultTypeDef:
        """
        Assigns one or more secondary private IP addresses to the specified network
        interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/assign_private_ip_addresses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#assign_private_ip_addresses)
        """

    async def assign_private_nat_gateway_address(
        self, **kwargs: Unpack[AssignPrivateNatGatewayAddressRequestRequestTypeDef]
    ) -> AssignPrivateNatGatewayAddressResultTypeDef:
        """
        Assigns private IPv4 addresses to a private NAT gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/assign_private_nat_gateway_address.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#assign_private_nat_gateway_address)
        """

    async def associate_address(
        self, **kwargs: Unpack[AssociateAddressRequestRequestTypeDef]
    ) -> AssociateAddressResultTypeDef:
        """
        Associates an Elastic IP address, or carrier IP address (for instances that are
        in subnets in Wavelength Zones) with an instance or a network interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/associate_address.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#associate_address)
        """

    async def associate_client_vpn_target_network(
        self, **kwargs: Unpack[AssociateClientVpnTargetNetworkRequestRequestTypeDef]
    ) -> AssociateClientVpnTargetNetworkResultTypeDef:
        """
        Associates a target network with a Client VPN endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/associate_client_vpn_target_network.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#associate_client_vpn_target_network)
        """

    async def associate_dhcp_options(
        self, **kwargs: Unpack[AssociateDhcpOptionsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates a set of DHCP options (that you've previously created) with the
        specified VPC, or associates no DHCP options with the VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/associate_dhcp_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#associate_dhcp_options)
        """

    async def associate_enclave_certificate_iam_role(
        self, **kwargs: Unpack[AssociateEnclaveCertificateIamRoleRequestRequestTypeDef]
    ) -> AssociateEnclaveCertificateIamRoleResultTypeDef:
        """
        Associates an Identity and Access Management (IAM) role with an Certificate
        Manager (ACM) certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/associate_enclave_certificate_iam_role.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#associate_enclave_certificate_iam_role)
        """

    async def associate_iam_instance_profile(
        self, **kwargs: Unpack[AssociateIamInstanceProfileRequestRequestTypeDef]
    ) -> AssociateIamInstanceProfileResultTypeDef:
        """
        Associates an IAM instance profile with a running or stopped instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/associate_iam_instance_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#associate_iam_instance_profile)
        """

    async def associate_instance_event_window(
        self, **kwargs: Unpack[AssociateInstanceEventWindowRequestRequestTypeDef]
    ) -> AssociateInstanceEventWindowResultTypeDef:
        """
        Associates one or more targets with an event window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/associate_instance_event_window.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#associate_instance_event_window)
        """

    async def associate_ipam_byoasn(
        self, **kwargs: Unpack[AssociateIpamByoasnRequestRequestTypeDef]
    ) -> AssociateIpamByoasnResultTypeDef:
        """
        Associates your Autonomous System Number (ASN) with a BYOIP CIDR that you own
        in the same Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/associate_ipam_byoasn.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#associate_ipam_byoasn)
        """

    async def associate_ipam_resource_discovery(
        self, **kwargs: Unpack[AssociateIpamResourceDiscoveryRequestRequestTypeDef]
    ) -> AssociateIpamResourceDiscoveryResultTypeDef:
        """
        Associates an IPAM resource discovery with an Amazon VPC IPAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/associate_ipam_resource_discovery.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#associate_ipam_resource_discovery)
        """

    async def associate_nat_gateway_address(
        self, **kwargs: Unpack[AssociateNatGatewayAddressRequestRequestTypeDef]
    ) -> AssociateNatGatewayAddressResultTypeDef:
        """
        Associates Elastic IP addresses (EIPs) and private IPv4 addresses with a public
        NAT gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/associate_nat_gateway_address.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#associate_nat_gateway_address)
        """

    async def associate_route_table(
        self, **kwargs: Unpack[AssociateRouteTableRequestRequestTypeDef]
    ) -> AssociateRouteTableResultTypeDef:
        """
        Associates a subnet in your VPC or an internet gateway or virtual private
        gateway attached to your VPC with a route table in your VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/associate_route_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#associate_route_table)
        """

    async def associate_subnet_cidr_block(
        self, **kwargs: Unpack[AssociateSubnetCidrBlockRequestRequestTypeDef]
    ) -> AssociateSubnetCidrBlockResultTypeDef:
        """
        Associates a CIDR block with your subnet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/associate_subnet_cidr_block.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#associate_subnet_cidr_block)
        """

    async def associate_transit_gateway_multicast_domain(
        self, **kwargs: Unpack[AssociateTransitGatewayMulticastDomainRequestRequestTypeDef]
    ) -> AssociateTransitGatewayMulticastDomainResultTypeDef:
        """
        Associates the specified subnets and transit gateway attachments with the
        specified transit gateway multicast domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/associate_transit_gateway_multicast_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#associate_transit_gateway_multicast_domain)
        """

    async def associate_transit_gateway_policy_table(
        self, **kwargs: Unpack[AssociateTransitGatewayPolicyTableRequestRequestTypeDef]
    ) -> AssociateTransitGatewayPolicyTableResultTypeDef:
        """
        Associates the specified transit gateway attachment with a transit gateway
        policy table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/associate_transit_gateway_policy_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#associate_transit_gateway_policy_table)
        """

    async def associate_transit_gateway_route_table(
        self, **kwargs: Unpack[AssociateTransitGatewayRouteTableRequestRequestTypeDef]
    ) -> AssociateTransitGatewayRouteTableResultTypeDef:
        """
        Associates the specified attachment with the specified transit gateway route
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/associate_transit_gateway_route_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#associate_transit_gateway_route_table)
        """

    async def associate_trunk_interface(
        self, **kwargs: Unpack[AssociateTrunkInterfaceRequestRequestTypeDef]
    ) -> AssociateTrunkInterfaceResultTypeDef:
        """
        Associates a branch network interface with a trunk network interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/associate_trunk_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#associate_trunk_interface)
        """

    async def associate_vpc_cidr_block(
        self, **kwargs: Unpack[AssociateVpcCidrBlockRequestRequestTypeDef]
    ) -> AssociateVpcCidrBlockResultTypeDef:
        """
        Associates a CIDR block with your VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/associate_vpc_cidr_block.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#associate_vpc_cidr_block)
        """

    async def attach_classic_link_vpc(
        self, **kwargs: Unpack[AttachClassicLinkVpcRequestRequestTypeDef]
    ) -> AttachClassicLinkVpcResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/attach_classic_link_vpc.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#attach_classic_link_vpc)
        """

    async def attach_internet_gateway(
        self, **kwargs: Unpack[AttachInternetGatewayRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches an internet gateway or a virtual private gateway to a VPC, enabling
        connectivity between the internet and the VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/attach_internet_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#attach_internet_gateway)
        """

    async def attach_network_interface(
        self, **kwargs: Unpack[AttachNetworkInterfaceRequestRequestTypeDef]
    ) -> AttachNetworkInterfaceResultTypeDef:
        """
        Attaches a network interface to an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/attach_network_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#attach_network_interface)
        """

    async def attach_verified_access_trust_provider(
        self, **kwargs: Unpack[AttachVerifiedAccessTrustProviderRequestRequestTypeDef]
    ) -> AttachVerifiedAccessTrustProviderResultTypeDef:
        """
        Attaches the specified Amazon Web Services Verified Access trust provider to
        the specified Amazon Web Services Verified Access instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/attach_verified_access_trust_provider.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#attach_verified_access_trust_provider)
        """

    async def attach_volume(
        self, **kwargs: Unpack[AttachVolumeRequestRequestTypeDef]
    ) -> VolumeAttachmentResponseTypeDef:
        """
        Attaches an EBS volume to a running or stopped instance and exposes it to the
        instance with the specified device name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/attach_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#attach_volume)
        """

    async def attach_vpn_gateway(
        self, **kwargs: Unpack[AttachVpnGatewayRequestRequestTypeDef]
    ) -> AttachVpnGatewayResultTypeDef:
        """
        Attaches an available virtual private gateway to a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/attach_vpn_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#attach_vpn_gateway)
        """

    async def authorize_client_vpn_ingress(
        self, **kwargs: Unpack[AuthorizeClientVpnIngressRequestRequestTypeDef]
    ) -> AuthorizeClientVpnIngressResultTypeDef:
        """
        Adds an ingress authorization rule to a Client VPN endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/authorize_client_vpn_ingress.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#authorize_client_vpn_ingress)
        """

    async def authorize_security_group_egress(
        self, **kwargs: Unpack[AuthorizeSecurityGroupEgressRequestRequestTypeDef]
    ) -> AuthorizeSecurityGroupEgressResultTypeDef:
        """
        Adds the specified outbound (egress) rules to a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/authorize_security_group_egress.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#authorize_security_group_egress)
        """

    async def authorize_security_group_ingress(
        self, **kwargs: Unpack[AuthorizeSecurityGroupIngressRequestRequestTypeDef]
    ) -> AuthorizeSecurityGroupIngressResultTypeDef:
        """
        Adds the specified inbound (ingress) rules to a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/authorize_security_group_ingress.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#authorize_security_group_ingress)
        """

    async def bundle_instance(
        self, **kwargs: Unpack[BundleInstanceRequestRequestTypeDef]
    ) -> BundleInstanceResultTypeDef:
        """
        Bundles an Amazon instance store-backed Windows instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/bundle_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#bundle_instance)
        """

    async def cancel_bundle_task(
        self, **kwargs: Unpack[CancelBundleTaskRequestRequestTypeDef]
    ) -> CancelBundleTaskResultTypeDef:
        """
        Cancels a bundling operation for an instance store-backed Windows instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/cancel_bundle_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#cancel_bundle_task)
        """

    async def cancel_capacity_reservation(
        self, **kwargs: Unpack[CancelCapacityReservationRequestRequestTypeDef]
    ) -> CancelCapacityReservationResultTypeDef:
        """
        Cancels the specified Capacity Reservation, releases the reserved capacity, and
        changes the Capacity Reservation's state to <code>cancelled</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/cancel_capacity_reservation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#cancel_capacity_reservation)
        """

    async def cancel_capacity_reservation_fleets(
        self, **kwargs: Unpack[CancelCapacityReservationFleetsRequestRequestTypeDef]
    ) -> CancelCapacityReservationFleetsResultTypeDef:
        """
        Cancels one or more Capacity Reservation Fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/cancel_capacity_reservation_fleets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#cancel_capacity_reservation_fleets)
        """

    async def cancel_conversion_task(
        self, **kwargs: Unpack[CancelConversionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels an active conversion task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/cancel_conversion_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#cancel_conversion_task)
        """

    async def cancel_export_task(
        self, **kwargs: Unpack[CancelExportTaskRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels an active export task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/cancel_export_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#cancel_export_task)
        """

    async def cancel_image_launch_permission(
        self, **kwargs: Unpack[CancelImageLaunchPermissionRequestRequestTypeDef]
    ) -> CancelImageLaunchPermissionResultTypeDef:
        """
        Removes your Amazon Web Services account from the launch permissions for the
        specified AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/cancel_image_launch_permission.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#cancel_image_launch_permission)
        """

    async def cancel_import_task(
        self, **kwargs: Unpack[CancelImportTaskRequestRequestTypeDef]
    ) -> CancelImportTaskResultTypeDef:
        """
        Cancels an in-process import virtual machine or import snapshot task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/cancel_import_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#cancel_import_task)
        """

    async def cancel_reserved_instances_listing(
        self, **kwargs: Unpack[CancelReservedInstancesListingRequestRequestTypeDef]
    ) -> CancelReservedInstancesListingResultTypeDef:
        """
        Cancels the specified Reserved Instance listing in the Reserved Instance
        Marketplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/cancel_reserved_instances_listing.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#cancel_reserved_instances_listing)
        """

    async def cancel_spot_fleet_requests(
        self, **kwargs: Unpack[CancelSpotFleetRequestsRequestRequestTypeDef]
    ) -> CancelSpotFleetRequestsResponseTypeDef:
        """
        Cancels the specified Spot Fleet requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/cancel_spot_fleet_requests.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#cancel_spot_fleet_requests)
        """

    async def cancel_spot_instance_requests(
        self, **kwargs: Unpack[CancelSpotInstanceRequestsRequestRequestTypeDef]
    ) -> CancelSpotInstanceRequestsResultTypeDef:
        """
        Cancels one or more Spot Instance requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/cancel_spot_instance_requests.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#cancel_spot_instance_requests)
        """

    async def confirm_product_instance(
        self, **kwargs: Unpack[ConfirmProductInstanceRequestRequestTypeDef]
    ) -> ConfirmProductInstanceResultTypeDef:
        """
        Determines whether a product code is associated with an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/confirm_product_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#confirm_product_instance)
        """

    async def copy_fpga_image(
        self, **kwargs: Unpack[CopyFpgaImageRequestRequestTypeDef]
    ) -> CopyFpgaImageResultTypeDef:
        """
        Copies the specified Amazon FPGA Image (AFI) to the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/copy_fpga_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#copy_fpga_image)
        """

    async def copy_image(
        self, **kwargs: Unpack[CopyImageRequestRequestTypeDef]
    ) -> CopyImageResultTypeDef:
        """
        Initiates an AMI copy operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/copy_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#copy_image)
        """

    async def copy_snapshot(
        self, **kwargs: Unpack[CopySnapshotRequestRequestTypeDef]
    ) -> CopySnapshotResultTypeDef:
        """
        Copies a point-in-time snapshot of an EBS volume and stores it in Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/copy_snapshot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#copy_snapshot)
        """

    async def create_capacity_reservation(
        self, **kwargs: Unpack[CreateCapacityReservationRequestRequestTypeDef]
    ) -> CreateCapacityReservationResultTypeDef:
        """
        Creates a new Capacity Reservation with the specified attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_capacity_reservation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_capacity_reservation)
        """

    async def create_capacity_reservation_by_splitting(
        self, **kwargs: Unpack[CreateCapacityReservationBySplittingRequestRequestTypeDef]
    ) -> CreateCapacityReservationBySplittingResultTypeDef:
        """
        Create a new Capacity Reservation by splitting the available capacity of the
        source Capacity Reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_capacity_reservation_by_splitting.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_capacity_reservation_by_splitting)
        """

    async def create_capacity_reservation_fleet(
        self, **kwargs: Unpack[CreateCapacityReservationFleetRequestRequestTypeDef]
    ) -> CreateCapacityReservationFleetResultTypeDef:
        """
        Creates a Capacity Reservation Fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_capacity_reservation_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_capacity_reservation_fleet)
        """

    async def create_carrier_gateway(
        self, **kwargs: Unpack[CreateCarrierGatewayRequestRequestTypeDef]
    ) -> CreateCarrierGatewayResultTypeDef:
        """
        Creates a carrier gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_carrier_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_carrier_gateway)
        """

    async def create_client_vpn_endpoint(
        self, **kwargs: Unpack[CreateClientVpnEndpointRequestRequestTypeDef]
    ) -> CreateClientVpnEndpointResultTypeDef:
        """
        Creates a Client VPN endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_client_vpn_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_client_vpn_endpoint)
        """

    async def create_client_vpn_route(
        self, **kwargs: Unpack[CreateClientVpnRouteRequestRequestTypeDef]
    ) -> CreateClientVpnRouteResultTypeDef:
        """
        Adds a route to a network to a Client VPN endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_client_vpn_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_client_vpn_route)
        """

    async def create_coip_cidr(
        self, **kwargs: Unpack[CreateCoipCidrRequestRequestTypeDef]
    ) -> CreateCoipCidrResultTypeDef:
        """
        Creates a range of customer-owned IP addresses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_coip_cidr.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_coip_cidr)
        """

    async def create_coip_pool(
        self, **kwargs: Unpack[CreateCoipPoolRequestRequestTypeDef]
    ) -> CreateCoipPoolResultTypeDef:
        """
        Creates a pool of customer-owned IP (CoIP) addresses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_coip_pool.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_coip_pool)
        """

    async def create_customer_gateway(
        self, **kwargs: Unpack[CreateCustomerGatewayRequestRequestTypeDef]
    ) -> CreateCustomerGatewayResultTypeDef:
        """
        Provides information to Amazon Web Services about your customer gateway device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_customer_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_customer_gateway)
        """

    async def create_default_subnet(
        self, **kwargs: Unpack[CreateDefaultSubnetRequestRequestTypeDef]
    ) -> CreateDefaultSubnetResultTypeDef:
        """
        Creates a default subnet with a size <code>/20</code> IPv4 CIDR block in the
        specified Availability Zone in your default VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_default_subnet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_default_subnet)
        """

    async def create_default_vpc(
        self, **kwargs: Unpack[CreateDefaultVpcRequestRequestTypeDef]
    ) -> CreateDefaultVpcResultTypeDef:
        """
        Creates a default VPC with a size <code>/16</code> IPv4 CIDR block and a
        default subnet in each Availability Zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_default_vpc.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_default_vpc)
        """

    async def create_dhcp_options(
        self, **kwargs: Unpack[CreateDhcpOptionsRequestRequestTypeDef]
    ) -> CreateDhcpOptionsResultTypeDef:
        """
        Creates a custom set of DHCP options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_dhcp_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_dhcp_options)
        """

    async def create_egress_only_internet_gateway(
        self, **kwargs: Unpack[CreateEgressOnlyInternetGatewayRequestRequestTypeDef]
    ) -> CreateEgressOnlyInternetGatewayResultTypeDef:
        """
        [IPv6 only] Creates an egress-only internet gateway for your VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_egress_only_internet_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_egress_only_internet_gateway)
        """

    async def create_fleet(
        self, **kwargs: Unpack[CreateFleetRequestRequestTypeDef]
    ) -> CreateFleetResultTypeDef:
        """
        Creates an EC2 Fleet that contains the configuration information for On-Demand
        Instances and Spot Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_fleet)
        """

    async def create_flow_logs(
        self, **kwargs: Unpack[CreateFlowLogsRequestRequestTypeDef]
    ) -> CreateFlowLogsResultTypeDef:
        """
        Creates one or more flow logs to capture information about IP traffic for a
        specific network interface, subnet, or VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_flow_logs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_flow_logs)
        """

    async def create_fpga_image(
        self, **kwargs: Unpack[CreateFpgaImageRequestRequestTypeDef]
    ) -> CreateFpgaImageResultTypeDef:
        """
        Creates an Amazon FPGA Image (AFI) from the specified design checkpoint (DCP).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_fpga_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_fpga_image)
        """

    async def create_image(
        self, **kwargs: Unpack[CreateImageRequestRequestTypeDef]
    ) -> CreateImageResultTypeDef:
        """
        Creates an Amazon EBS-backed AMI from an Amazon EBS-backed instance that is
        either running or stopped.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_image)
        """

    async def create_instance_connect_endpoint(
        self, **kwargs: Unpack[CreateInstanceConnectEndpointRequestRequestTypeDef]
    ) -> CreateInstanceConnectEndpointResultTypeDef:
        """
        Creates an EC2 Instance Connect Endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_instance_connect_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_instance_connect_endpoint)
        """

    async def create_instance_event_window(
        self, **kwargs: Unpack[CreateInstanceEventWindowRequestRequestTypeDef]
    ) -> CreateInstanceEventWindowResultTypeDef:
        """
        Creates an event window in which scheduled events for the associated Amazon EC2
        instances can run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_instance_event_window.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_instance_event_window)
        """

    async def create_instance_export_task(
        self, **kwargs: Unpack[CreateInstanceExportTaskRequestRequestTypeDef]
    ) -> CreateInstanceExportTaskResultTypeDef:
        """
        Exports a running or stopped instance to an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_instance_export_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_instance_export_task)
        """

    async def create_internet_gateway(
        self, **kwargs: Unpack[CreateInternetGatewayRequestRequestTypeDef]
    ) -> CreateInternetGatewayResultTypeDef:
        """
        Creates an internet gateway for use with a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_internet_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_internet_gateway)
        """

    async def create_ipam(
        self, **kwargs: Unpack[CreateIpamRequestRequestTypeDef]
    ) -> CreateIpamResultTypeDef:
        """
        Create an IPAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_ipam.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_ipam)
        """

    async def create_ipam_external_resource_verification_token(
        self, **kwargs: Unpack[CreateIpamExternalResourceVerificationTokenRequestRequestTypeDef]
    ) -> CreateIpamExternalResourceVerificationTokenResultTypeDef:
        """
        Create a verification token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_ipam_external_resource_verification_token.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_ipam_external_resource_verification_token)
        """

    async def create_ipam_pool(
        self, **kwargs: Unpack[CreateIpamPoolRequestRequestTypeDef]
    ) -> CreateIpamPoolResultTypeDef:
        """
        Create an IP address pool for Amazon VPC IP Address Manager (IPAM).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_ipam_pool.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_ipam_pool)
        """

    async def create_ipam_resource_discovery(
        self, **kwargs: Unpack[CreateIpamResourceDiscoveryRequestRequestTypeDef]
    ) -> CreateIpamResourceDiscoveryResultTypeDef:
        """
        Creates an IPAM resource discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_ipam_resource_discovery.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_ipam_resource_discovery)
        """

    async def create_ipam_scope(
        self, **kwargs: Unpack[CreateIpamScopeRequestRequestTypeDef]
    ) -> CreateIpamScopeResultTypeDef:
        """
        Create an IPAM scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_ipam_scope.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_ipam_scope)
        """

    async def create_key_pair(
        self, **kwargs: Unpack[CreateKeyPairRequestRequestTypeDef]
    ) -> KeyPairTypeDef:
        """
        Creates an ED25519 or 2048-bit RSA key pair with the specified name and in the
        specified PEM or PPK format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_key_pair.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_key_pair)
        """

    async def create_launch_template(
        self, **kwargs: Unpack[CreateLaunchTemplateRequestRequestTypeDef]
    ) -> CreateLaunchTemplateResultTypeDef:
        """
        Creates a launch template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_launch_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_launch_template)
        """

    async def create_launch_template_version(
        self, **kwargs: Unpack[CreateLaunchTemplateVersionRequestRequestTypeDef]
    ) -> CreateLaunchTemplateVersionResultTypeDef:
        """
        Creates a new version of a launch template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_launch_template_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_launch_template_version)
        """

    async def create_local_gateway_route(
        self, **kwargs: Unpack[CreateLocalGatewayRouteRequestRequestTypeDef]
    ) -> CreateLocalGatewayRouteResultTypeDef:
        """
        Creates a static route for the specified local gateway route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_local_gateway_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_local_gateway_route)
        """

    async def create_local_gateway_route_table(
        self, **kwargs: Unpack[CreateLocalGatewayRouteTableRequestRequestTypeDef]
    ) -> CreateLocalGatewayRouteTableResultTypeDef:
        """
        Creates a local gateway route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_local_gateway_route_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_local_gateway_route_table)
        """

    async def create_local_gateway_route_table_virtual_interface_group_association(
        self,
        **kwargs: Unpack[
            CreateLocalGatewayRouteTableVirtualInterfaceGroupAssociationRequestRequestTypeDef
        ],
    ) -> CreateLocalGatewayRouteTableVirtualInterfaceGroupAssociationResultTypeDef:
        """
        Creates a local gateway route table virtual interface group association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_local_gateway_route_table_virtual_interface_group_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_local_gateway_route_table_virtual_interface_group_association)
        """

    async def create_local_gateway_route_table_vpc_association(
        self, **kwargs: Unpack[CreateLocalGatewayRouteTableVpcAssociationRequestRequestTypeDef]
    ) -> CreateLocalGatewayRouteTableVpcAssociationResultTypeDef:
        """
        Associates the specified VPC with the specified local gateway route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_local_gateway_route_table_vpc_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_local_gateway_route_table_vpc_association)
        """

    async def create_managed_prefix_list(
        self, **kwargs: Unpack[CreateManagedPrefixListRequestRequestTypeDef]
    ) -> CreateManagedPrefixListResultTypeDef:
        """
        Creates a managed prefix list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_managed_prefix_list.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_managed_prefix_list)
        """

    async def create_nat_gateway(
        self, **kwargs: Unpack[CreateNatGatewayRequestRequestTypeDef]
    ) -> CreateNatGatewayResultTypeDef:
        """
        Creates a NAT gateway in the specified subnet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_nat_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_nat_gateway)
        """

    async def create_network_acl(
        self, **kwargs: Unpack[CreateNetworkAclRequestRequestTypeDef]
    ) -> CreateNetworkAclResultTypeDef:
        """
        Creates a network ACL in a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_network_acl.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_network_acl)
        """

    async def create_network_acl_entry(
        self, **kwargs: Unpack[CreateNetworkAclEntryRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates an entry (a rule) in a network ACL with the specified rule number.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_network_acl_entry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_network_acl_entry)
        """

    async def create_network_insights_access_scope(
        self, **kwargs: Unpack[CreateNetworkInsightsAccessScopeRequestRequestTypeDef]
    ) -> CreateNetworkInsightsAccessScopeResultTypeDef:
        """
        Creates a Network Access Scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_network_insights_access_scope.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_network_insights_access_scope)
        """

    async def create_network_insights_path(
        self, **kwargs: Unpack[CreateNetworkInsightsPathRequestRequestTypeDef]
    ) -> CreateNetworkInsightsPathResultTypeDef:
        """
        Creates a path to analyze for reachability.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_network_insights_path.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_network_insights_path)
        """

    async def create_network_interface(
        self, **kwargs: Unpack[CreateNetworkInterfaceRequestRequestTypeDef]
    ) -> CreateNetworkInterfaceResultTypeDef:
        """
        Creates a network interface in the specified subnet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_network_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_network_interface)
        """

    async def create_network_interface_permission(
        self, **kwargs: Unpack[CreateNetworkInterfacePermissionRequestRequestTypeDef]
    ) -> CreateNetworkInterfacePermissionResultTypeDef:
        """
        Grants an Amazon Web Services-authorized account permission to attach the
        specified network interface to an instance in their account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_network_interface_permission.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_network_interface_permission)
        """

    async def create_placement_group(
        self, **kwargs: Unpack[CreatePlacementGroupRequestRequestTypeDef]
    ) -> CreatePlacementGroupResultTypeDef:
        """
        Creates a placement group in which to launch instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_placement_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_placement_group)
        """

    async def create_public_ipv4_pool(
        self, **kwargs: Unpack[CreatePublicIpv4PoolRequestRequestTypeDef]
    ) -> CreatePublicIpv4PoolResultTypeDef:
        """
        Creates a public IPv4 address pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_public_ipv4_pool.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_public_ipv4_pool)
        """

    async def create_replace_root_volume_task(
        self, **kwargs: Unpack[CreateReplaceRootVolumeTaskRequestRequestTypeDef]
    ) -> CreateReplaceRootVolumeTaskResultTypeDef:
        """
        Replaces the EBS-backed root volume for a <code>running</code> instance with a
        new volume that is restored to the original root volume's launch state, that is
        restored to a specific snapshot taken from the original root volume, or that is
        restored from an AMI that has the same key characteristics...

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_replace_root_volume_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_replace_root_volume_task)
        """

    async def create_reserved_instances_listing(
        self, **kwargs: Unpack[CreateReservedInstancesListingRequestRequestTypeDef]
    ) -> CreateReservedInstancesListingResultTypeDef:
        """
        Creates a listing for Amazon EC2 Standard Reserved Instances to be sold in the
        Reserved Instance Marketplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_reserved_instances_listing.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_reserved_instances_listing)
        """

    async def create_restore_image_task(
        self, **kwargs: Unpack[CreateRestoreImageTaskRequestRequestTypeDef]
    ) -> CreateRestoreImageTaskResultTypeDef:
        """
        Starts a task that restores an AMI from an Amazon S3 object that was previously
        created by using <a
        href="https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateStoreImageTask.html">CreateStoreImageTask</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_restore_image_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_restore_image_task)
        """

    async def create_route(
        self, **kwargs: Unpack[CreateRouteRequestRequestTypeDef]
    ) -> CreateRouteResultTypeDef:
        """
        Creates a route in a route table within a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_route)
        """

    async def create_route_table(
        self, **kwargs: Unpack[CreateRouteTableRequestRequestTypeDef]
    ) -> CreateRouteTableResultTypeDef:
        """
        Creates a route table for the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_route_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_route_table)
        """

    async def create_security_group(
        self, **kwargs: Unpack[CreateSecurityGroupRequestRequestTypeDef]
    ) -> CreateSecurityGroupResultTypeDef:
        """
        Creates a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_security_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_security_group)
        """

    async def create_snapshot(
        self, **kwargs: Unpack[CreateSnapshotRequestRequestTypeDef]
    ) -> SnapshotResponseTypeDef:
        """
        Creates a snapshot of an EBS volume and stores it in Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_snapshot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_snapshot)
        """

    async def create_snapshots(
        self, **kwargs: Unpack[CreateSnapshotsRequestRequestTypeDef]
    ) -> CreateSnapshotsResultTypeDef:
        """
        Creates crash-consistent snapshots of multiple EBS volumes and stores the data
        in S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_snapshots.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_snapshots)
        """

    async def create_spot_datafeed_subscription(
        self, **kwargs: Unpack[CreateSpotDatafeedSubscriptionRequestRequestTypeDef]
    ) -> CreateSpotDatafeedSubscriptionResultTypeDef:
        """
        Creates a data feed for Spot Instances, enabling you to view Spot Instance
        usage logs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_spot_datafeed_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_spot_datafeed_subscription)
        """

    async def create_store_image_task(
        self, **kwargs: Unpack[CreateStoreImageTaskRequestRequestTypeDef]
    ) -> CreateStoreImageTaskResultTypeDef:
        """
        Stores an AMI as a single object in an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_store_image_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_store_image_task)
        """

    async def create_subnet(
        self, **kwargs: Unpack[CreateSubnetRequestRequestTypeDef]
    ) -> CreateSubnetResultTypeDef:
        """
        Creates a subnet in the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_subnet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_subnet)
        """

    async def create_subnet_cidr_reservation(
        self, **kwargs: Unpack[CreateSubnetCidrReservationRequestRequestTypeDef]
    ) -> CreateSubnetCidrReservationResultTypeDef:
        """
        Creates a subnet CIDR reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_subnet_cidr_reservation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_subnet_cidr_reservation)
        """

    async def create_tags(self, **kwargs: Unpack[ClientCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_tags)
        """

    async def create_traffic_mirror_filter(
        self, **kwargs: Unpack[CreateTrafficMirrorFilterRequestRequestTypeDef]
    ) -> CreateTrafficMirrorFilterResultTypeDef:
        """
        Creates a Traffic Mirror filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_traffic_mirror_filter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_traffic_mirror_filter)
        """

    async def create_traffic_mirror_filter_rule(
        self, **kwargs: Unpack[CreateTrafficMirrorFilterRuleRequestRequestTypeDef]
    ) -> CreateTrafficMirrorFilterRuleResultTypeDef:
        """
        Creates a Traffic Mirror filter rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_traffic_mirror_filter_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_traffic_mirror_filter_rule)
        """

    async def create_traffic_mirror_session(
        self, **kwargs: Unpack[CreateTrafficMirrorSessionRequestRequestTypeDef]
    ) -> CreateTrafficMirrorSessionResultTypeDef:
        """
        Creates a Traffic Mirror session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_traffic_mirror_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_traffic_mirror_session)
        """

    async def create_traffic_mirror_target(
        self, **kwargs: Unpack[CreateTrafficMirrorTargetRequestRequestTypeDef]
    ) -> CreateTrafficMirrorTargetResultTypeDef:
        """
        Creates a target for your Traffic Mirror session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_traffic_mirror_target.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_traffic_mirror_target)
        """

    async def create_transit_gateway(
        self, **kwargs: Unpack[CreateTransitGatewayRequestRequestTypeDef]
    ) -> CreateTransitGatewayResultTypeDef:
        """
        Creates a transit gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_transit_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_transit_gateway)
        """

    async def create_transit_gateway_connect(
        self, **kwargs: Unpack[CreateTransitGatewayConnectRequestRequestTypeDef]
    ) -> CreateTransitGatewayConnectResultTypeDef:
        """
        Creates a Connect attachment from a specified transit gateway attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_transit_gateway_connect.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_transit_gateway_connect)
        """

    async def create_transit_gateway_connect_peer(
        self, **kwargs: Unpack[CreateTransitGatewayConnectPeerRequestRequestTypeDef]
    ) -> CreateTransitGatewayConnectPeerResultTypeDef:
        """
        Creates a Connect peer for a specified transit gateway Connect attachment
        between a transit gateway and an appliance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_transit_gateway_connect_peer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_transit_gateway_connect_peer)
        """

    async def create_transit_gateway_multicast_domain(
        self, **kwargs: Unpack[CreateTransitGatewayMulticastDomainRequestRequestTypeDef]
    ) -> CreateTransitGatewayMulticastDomainResultTypeDef:
        """
        Creates a multicast domain using the specified transit gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_transit_gateway_multicast_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_transit_gateway_multicast_domain)
        """

    async def create_transit_gateway_peering_attachment(
        self, **kwargs: Unpack[CreateTransitGatewayPeeringAttachmentRequestRequestTypeDef]
    ) -> CreateTransitGatewayPeeringAttachmentResultTypeDef:
        """
        Requests a transit gateway peering attachment between the specified transit
        gateway (requester) and a peer transit gateway (accepter).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_transit_gateway_peering_attachment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_transit_gateway_peering_attachment)
        """

    async def create_transit_gateway_policy_table(
        self, **kwargs: Unpack[CreateTransitGatewayPolicyTableRequestRequestTypeDef]
    ) -> CreateTransitGatewayPolicyTableResultTypeDef:
        """
        Creates a transit gateway policy table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_transit_gateway_policy_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_transit_gateway_policy_table)
        """

    async def create_transit_gateway_prefix_list_reference(
        self, **kwargs: Unpack[CreateTransitGatewayPrefixListReferenceRequestRequestTypeDef]
    ) -> CreateTransitGatewayPrefixListReferenceResultTypeDef:
        """
        Creates a reference (route) to a prefix list in a specified transit gateway
        route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_transit_gateway_prefix_list_reference.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_transit_gateway_prefix_list_reference)
        """

    async def create_transit_gateway_route(
        self, **kwargs: Unpack[CreateTransitGatewayRouteRequestRequestTypeDef]
    ) -> CreateTransitGatewayRouteResultTypeDef:
        """
        Creates a static route for the specified transit gateway route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_transit_gateway_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_transit_gateway_route)
        """

    async def create_transit_gateway_route_table(
        self, **kwargs: Unpack[CreateTransitGatewayRouteTableRequestRequestTypeDef]
    ) -> CreateTransitGatewayRouteTableResultTypeDef:
        """
        Creates a route table for the specified transit gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_transit_gateway_route_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_transit_gateway_route_table)
        """

    async def create_transit_gateway_route_table_announcement(
        self, **kwargs: Unpack[CreateTransitGatewayRouteTableAnnouncementRequestRequestTypeDef]
    ) -> CreateTransitGatewayRouteTableAnnouncementResultTypeDef:
        """
        Advertises a new transit gateway route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_transit_gateway_route_table_announcement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_transit_gateway_route_table_announcement)
        """

    async def create_transit_gateway_vpc_attachment(
        self, **kwargs: Unpack[CreateTransitGatewayVpcAttachmentRequestRequestTypeDef]
    ) -> CreateTransitGatewayVpcAttachmentResultTypeDef:
        """
        Attaches the specified VPC to the specified transit gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_transit_gateway_vpc_attachment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_transit_gateway_vpc_attachment)
        """

    async def create_verified_access_endpoint(
        self, **kwargs: Unpack[CreateVerifiedAccessEndpointRequestRequestTypeDef]
    ) -> CreateVerifiedAccessEndpointResultTypeDef:
        """
        An Amazon Web Services Verified Access endpoint is where you define your
        application along with an optional endpoint-level access policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_verified_access_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_verified_access_endpoint)
        """

    async def create_verified_access_group(
        self, **kwargs: Unpack[CreateVerifiedAccessGroupRequestRequestTypeDef]
    ) -> CreateVerifiedAccessGroupResultTypeDef:
        """
        An Amazon Web Services Verified Access group is a collection of Amazon Web
        Services Verified Access endpoints who's associated applications have similar
        security requirements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_verified_access_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_verified_access_group)
        """

    async def create_verified_access_instance(
        self, **kwargs: Unpack[CreateVerifiedAccessInstanceRequestRequestTypeDef]
    ) -> CreateVerifiedAccessInstanceResultTypeDef:
        """
        An Amazon Web Services Verified Access instance is a regional entity that
        evaluates application requests and grants access only when your security
        requirements are met.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_verified_access_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_verified_access_instance)
        """

    async def create_verified_access_trust_provider(
        self, **kwargs: Unpack[CreateVerifiedAccessTrustProviderRequestRequestTypeDef]
    ) -> CreateVerifiedAccessTrustProviderResultTypeDef:
        """
        A trust provider is a third-party entity that creates, maintains, and manages
        identity information for users and devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_verified_access_trust_provider.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_verified_access_trust_provider)
        """

    async def create_volume(
        self, **kwargs: Unpack[CreateVolumeRequestRequestTypeDef]
    ) -> VolumeResponseTypeDef:
        """
        Creates an EBS volume that can be attached to an instance in the same
        Availability Zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_volume)
        """

    async def create_vpc(
        self, **kwargs: Unpack[CreateVpcRequestRequestTypeDef]
    ) -> CreateVpcResultTypeDef:
        """
        Creates a VPC with the specified CIDR blocks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_vpc.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_vpc)
        """

    async def create_vpc_endpoint(
        self, **kwargs: Unpack[CreateVpcEndpointRequestRequestTypeDef]
    ) -> CreateVpcEndpointResultTypeDef:
        """
        Creates a VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_vpc_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_vpc_endpoint)
        """

    async def create_vpc_endpoint_connection_notification(
        self, **kwargs: Unpack[CreateVpcEndpointConnectionNotificationRequestRequestTypeDef]
    ) -> CreateVpcEndpointConnectionNotificationResultTypeDef:
        """
        Creates a connection notification for a specified VPC endpoint or VPC endpoint
        service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_vpc_endpoint_connection_notification.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_vpc_endpoint_connection_notification)
        """

    async def create_vpc_endpoint_service_configuration(
        self, **kwargs: Unpack[CreateVpcEndpointServiceConfigurationRequestRequestTypeDef]
    ) -> CreateVpcEndpointServiceConfigurationResultTypeDef:
        """
        Creates a VPC endpoint service to which service consumers (Amazon Web Services
        accounts, users, and IAM roles) can connect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_vpc_endpoint_service_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_vpc_endpoint_service_configuration)
        """

    async def create_vpc_peering_connection(
        self, **kwargs: Unpack[CreateVpcPeeringConnectionRequestRequestTypeDef]
    ) -> CreateVpcPeeringConnectionResultTypeDef:
        """
        Requests a VPC peering connection between two VPCs: a requester VPC that you
        own and an accepter VPC with which to create the connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_vpc_peering_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_vpc_peering_connection)
        """

    async def create_vpn_connection(
        self, **kwargs: Unpack[CreateVpnConnectionRequestRequestTypeDef]
    ) -> CreateVpnConnectionResultTypeDef:
        """
        Creates a VPN connection between an existing virtual private gateway or transit
        gateway and a customer gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_vpn_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_vpn_connection)
        """

    async def create_vpn_connection_route(
        self, **kwargs: Unpack[CreateVpnConnectionRouteRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a static route associated with a VPN connection between an existing
        virtual private gateway and a VPN customer gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_vpn_connection_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_vpn_connection_route)
        """

    async def create_vpn_gateway(
        self, **kwargs: Unpack[CreateVpnGatewayRequestRequestTypeDef]
    ) -> CreateVpnGatewayResultTypeDef:
        """
        Creates a virtual private gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_vpn_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#create_vpn_gateway)
        """

    async def delete_carrier_gateway(
        self, **kwargs: Unpack[DeleteCarrierGatewayRequestRequestTypeDef]
    ) -> DeleteCarrierGatewayResultTypeDef:
        """
        Deletes a carrier gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_carrier_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_carrier_gateway)
        """

    async def delete_client_vpn_endpoint(
        self, **kwargs: Unpack[DeleteClientVpnEndpointRequestRequestTypeDef]
    ) -> DeleteClientVpnEndpointResultTypeDef:
        """
        Deletes the specified Client VPN endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_client_vpn_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_client_vpn_endpoint)
        """

    async def delete_client_vpn_route(
        self, **kwargs: Unpack[DeleteClientVpnRouteRequestRequestTypeDef]
    ) -> DeleteClientVpnRouteResultTypeDef:
        """
        Deletes a route from a Client VPN endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_client_vpn_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_client_vpn_route)
        """

    async def delete_coip_cidr(
        self, **kwargs: Unpack[DeleteCoipCidrRequestRequestTypeDef]
    ) -> DeleteCoipCidrResultTypeDef:
        """
        Deletes a range of customer-owned IP addresses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_coip_cidr.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_coip_cidr)
        """

    async def delete_coip_pool(
        self, **kwargs: Unpack[DeleteCoipPoolRequestRequestTypeDef]
    ) -> DeleteCoipPoolResultTypeDef:
        """
        Deletes a pool of customer-owned IP (CoIP) addresses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_coip_pool.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_coip_pool)
        """

    async def delete_customer_gateway(
        self, **kwargs: Unpack[DeleteCustomerGatewayRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified customer gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_customer_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_customer_gateway)
        """

    async def delete_dhcp_options(
        self, **kwargs: Unpack[DeleteDhcpOptionsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified set of DHCP options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_dhcp_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_dhcp_options)
        """

    async def delete_egress_only_internet_gateway(
        self, **kwargs: Unpack[DeleteEgressOnlyInternetGatewayRequestRequestTypeDef]
    ) -> DeleteEgressOnlyInternetGatewayResultTypeDef:
        """
        Deletes an egress-only internet gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_egress_only_internet_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_egress_only_internet_gateway)
        """

    async def delete_fleets(
        self, **kwargs: Unpack[DeleteFleetsRequestRequestTypeDef]
    ) -> DeleteFleetsResultTypeDef:
        """
        Deletes the specified EC2 Fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_fleets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_fleets)
        """

    async def delete_flow_logs(
        self, **kwargs: Unpack[DeleteFlowLogsRequestRequestTypeDef]
    ) -> DeleteFlowLogsResultTypeDef:
        """
        Deletes one or more flow logs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_flow_logs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_flow_logs)
        """

    async def delete_fpga_image(
        self, **kwargs: Unpack[DeleteFpgaImageRequestRequestTypeDef]
    ) -> DeleteFpgaImageResultTypeDef:
        """
        Deletes the specified Amazon FPGA Image (AFI).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_fpga_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_fpga_image)
        """

    async def delete_instance_connect_endpoint(
        self, **kwargs: Unpack[DeleteInstanceConnectEndpointRequestRequestTypeDef]
    ) -> DeleteInstanceConnectEndpointResultTypeDef:
        """
        Deletes the specified EC2 Instance Connect Endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_instance_connect_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_instance_connect_endpoint)
        """

    async def delete_instance_event_window(
        self, **kwargs: Unpack[DeleteInstanceEventWindowRequestRequestTypeDef]
    ) -> DeleteInstanceEventWindowResultTypeDef:
        """
        Deletes the specified event window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_instance_event_window.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_instance_event_window)
        """

    async def delete_internet_gateway(
        self, **kwargs: Unpack[DeleteInternetGatewayRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified internet gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_internet_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_internet_gateway)
        """

    async def delete_ipam(
        self, **kwargs: Unpack[DeleteIpamRequestRequestTypeDef]
    ) -> DeleteIpamResultTypeDef:
        """
        Delete an IPAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_ipam.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_ipam)
        """

    async def delete_ipam_external_resource_verification_token(
        self, **kwargs: Unpack[DeleteIpamExternalResourceVerificationTokenRequestRequestTypeDef]
    ) -> DeleteIpamExternalResourceVerificationTokenResultTypeDef:
        """
        Delete a verification token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_ipam_external_resource_verification_token.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_ipam_external_resource_verification_token)
        """

    async def delete_ipam_pool(
        self, **kwargs: Unpack[DeleteIpamPoolRequestRequestTypeDef]
    ) -> DeleteIpamPoolResultTypeDef:
        """
        Delete an IPAM pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_ipam_pool.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_ipam_pool)
        """

    async def delete_ipam_resource_discovery(
        self, **kwargs: Unpack[DeleteIpamResourceDiscoveryRequestRequestTypeDef]
    ) -> DeleteIpamResourceDiscoveryResultTypeDef:
        """
        Deletes an IPAM resource discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_ipam_resource_discovery.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_ipam_resource_discovery)
        """

    async def delete_ipam_scope(
        self, **kwargs: Unpack[DeleteIpamScopeRequestRequestTypeDef]
    ) -> DeleteIpamScopeResultTypeDef:
        """
        Delete the scope for an IPAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_ipam_scope.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_ipam_scope)
        """

    async def delete_key_pair(
        self, **kwargs: Unpack[DeleteKeyPairRequestRequestTypeDef]
    ) -> DeleteKeyPairResultTypeDef:
        """
        Deletes the specified key pair, by removing the public key from Amazon EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_key_pair.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_key_pair)
        """

    async def delete_launch_template(
        self, **kwargs: Unpack[DeleteLaunchTemplateRequestRequestTypeDef]
    ) -> DeleteLaunchTemplateResultTypeDef:
        """
        Deletes a launch template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_launch_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_launch_template)
        """

    async def delete_launch_template_versions(
        self, **kwargs: Unpack[DeleteLaunchTemplateVersionsRequestRequestTypeDef]
    ) -> DeleteLaunchTemplateVersionsResultTypeDef:
        """
        Deletes one or more versions of a launch template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_launch_template_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_launch_template_versions)
        """

    async def delete_local_gateway_route(
        self, **kwargs: Unpack[DeleteLocalGatewayRouteRequestRequestTypeDef]
    ) -> DeleteLocalGatewayRouteResultTypeDef:
        """
        Deletes the specified route from the specified local gateway route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_local_gateway_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_local_gateway_route)
        """

    async def delete_local_gateway_route_table(
        self, **kwargs: Unpack[DeleteLocalGatewayRouteTableRequestRequestTypeDef]
    ) -> DeleteLocalGatewayRouteTableResultTypeDef:
        """
        Deletes a local gateway route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_local_gateway_route_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_local_gateway_route_table)
        """

    async def delete_local_gateway_route_table_virtual_interface_group_association(
        self,
        **kwargs: Unpack[
            DeleteLocalGatewayRouteTableVirtualInterfaceGroupAssociationRequestRequestTypeDef
        ],
    ) -> DeleteLocalGatewayRouteTableVirtualInterfaceGroupAssociationResultTypeDef:
        """
        Deletes a local gateway route table virtual interface group association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_local_gateway_route_table_virtual_interface_group_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_local_gateway_route_table_virtual_interface_group_association)
        """

    async def delete_local_gateway_route_table_vpc_association(
        self, **kwargs: Unpack[DeleteLocalGatewayRouteTableVpcAssociationRequestRequestTypeDef]
    ) -> DeleteLocalGatewayRouteTableVpcAssociationResultTypeDef:
        """
        Deletes the specified association between a VPC and local gateway route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_local_gateway_route_table_vpc_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_local_gateway_route_table_vpc_association)
        """

    async def delete_managed_prefix_list(
        self, **kwargs: Unpack[DeleteManagedPrefixListRequestRequestTypeDef]
    ) -> DeleteManagedPrefixListResultTypeDef:
        """
        Deletes the specified managed prefix list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_managed_prefix_list.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_managed_prefix_list)
        """

    async def delete_nat_gateway(
        self, **kwargs: Unpack[DeleteNatGatewayRequestRequestTypeDef]
    ) -> DeleteNatGatewayResultTypeDef:
        """
        Deletes the specified NAT gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_nat_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_nat_gateway)
        """

    async def delete_network_acl(
        self, **kwargs: Unpack[DeleteNetworkAclRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified network ACL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_network_acl.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_network_acl)
        """

    async def delete_network_acl_entry(
        self, **kwargs: Unpack[DeleteNetworkAclEntryRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified ingress or egress entry (rule) from the specified network
        ACL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_network_acl_entry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_network_acl_entry)
        """

    async def delete_network_insights_access_scope(
        self, **kwargs: Unpack[DeleteNetworkInsightsAccessScopeRequestRequestTypeDef]
    ) -> DeleteNetworkInsightsAccessScopeResultTypeDef:
        """
        Deletes the specified Network Access Scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_network_insights_access_scope.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_network_insights_access_scope)
        """

    async def delete_network_insights_access_scope_analysis(
        self, **kwargs: Unpack[DeleteNetworkInsightsAccessScopeAnalysisRequestRequestTypeDef]
    ) -> DeleteNetworkInsightsAccessScopeAnalysisResultTypeDef:
        """
        Deletes the specified Network Access Scope analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_network_insights_access_scope_analysis.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_network_insights_access_scope_analysis)
        """

    async def delete_network_insights_analysis(
        self, **kwargs: Unpack[DeleteNetworkInsightsAnalysisRequestRequestTypeDef]
    ) -> DeleteNetworkInsightsAnalysisResultTypeDef:
        """
        Deletes the specified network insights analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_network_insights_analysis.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_network_insights_analysis)
        """

    async def delete_network_insights_path(
        self, **kwargs: Unpack[DeleteNetworkInsightsPathRequestRequestTypeDef]
    ) -> DeleteNetworkInsightsPathResultTypeDef:
        """
        Deletes the specified path.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_network_insights_path.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_network_insights_path)
        """

    async def delete_network_interface(
        self, **kwargs: Unpack[DeleteNetworkInterfaceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified network interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_network_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_network_interface)
        """

    async def delete_network_interface_permission(
        self, **kwargs: Unpack[DeleteNetworkInterfacePermissionRequestRequestTypeDef]
    ) -> DeleteNetworkInterfacePermissionResultTypeDef:
        """
        Deletes a permission for a network interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_network_interface_permission.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_network_interface_permission)
        """

    async def delete_placement_group(
        self, **kwargs: Unpack[DeletePlacementGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified placement group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_placement_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_placement_group)
        """

    async def delete_public_ipv4_pool(
        self, **kwargs: Unpack[DeletePublicIpv4PoolRequestRequestTypeDef]
    ) -> DeletePublicIpv4PoolResultTypeDef:
        """
        Delete a public IPv4 pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_public_ipv4_pool.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_public_ipv4_pool)
        """

    async def delete_queued_reserved_instances(
        self, **kwargs: Unpack[DeleteQueuedReservedInstancesRequestRequestTypeDef]
    ) -> DeleteQueuedReservedInstancesResultTypeDef:
        """
        Deletes the queued purchases for the specified Reserved Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_queued_reserved_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_queued_reserved_instances)
        """

    async def delete_route(
        self, **kwargs: Unpack[DeleteRouteRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified route from the specified route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_route)
        """

    async def delete_route_table(
        self, **kwargs: Unpack[DeleteRouteTableRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_route_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_route_table)
        """

    async def delete_security_group(
        self, **kwargs: Unpack[DeleteSecurityGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_security_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_security_group)
        """

    async def delete_snapshot(
        self, **kwargs: Unpack[DeleteSnapshotRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_snapshot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_snapshot)
        """

    async def delete_spot_datafeed_subscription(
        self, **kwargs: Unpack[DeleteSpotDatafeedSubscriptionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the data feed for Spot Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_spot_datafeed_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_spot_datafeed_subscription)
        """

    async def delete_subnet(
        self, **kwargs: Unpack[DeleteSubnetRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified subnet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_subnet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_subnet)
        """

    async def delete_subnet_cidr_reservation(
        self, **kwargs: Unpack[DeleteSubnetCidrReservationRequestRequestTypeDef]
    ) -> DeleteSubnetCidrReservationResultTypeDef:
        """
        Deletes a subnet CIDR reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_subnet_cidr_reservation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_subnet_cidr_reservation)
        """

    async def delete_tags(self, **kwargs: Unpack[ClientDeleteTagsRequestTypeDef]) -> None:
        """
        Deletes the specified set of tags from the specified set of resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_tags)
        """

    async def delete_traffic_mirror_filter(
        self, **kwargs: Unpack[DeleteTrafficMirrorFilterRequestRequestTypeDef]
    ) -> DeleteTrafficMirrorFilterResultTypeDef:
        """
        Deletes the specified Traffic Mirror filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_traffic_mirror_filter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_traffic_mirror_filter)
        """

    async def delete_traffic_mirror_filter_rule(
        self, **kwargs: Unpack[DeleteTrafficMirrorFilterRuleRequestRequestTypeDef]
    ) -> DeleteTrafficMirrorFilterRuleResultTypeDef:
        """
        Deletes the specified Traffic Mirror rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_traffic_mirror_filter_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_traffic_mirror_filter_rule)
        """

    async def delete_traffic_mirror_session(
        self, **kwargs: Unpack[DeleteTrafficMirrorSessionRequestRequestTypeDef]
    ) -> DeleteTrafficMirrorSessionResultTypeDef:
        """
        Deletes the specified Traffic Mirror session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_traffic_mirror_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_traffic_mirror_session)
        """

    async def delete_traffic_mirror_target(
        self, **kwargs: Unpack[DeleteTrafficMirrorTargetRequestRequestTypeDef]
    ) -> DeleteTrafficMirrorTargetResultTypeDef:
        """
        Deletes the specified Traffic Mirror target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_traffic_mirror_target.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_traffic_mirror_target)
        """

    async def delete_transit_gateway(
        self, **kwargs: Unpack[DeleteTransitGatewayRequestRequestTypeDef]
    ) -> DeleteTransitGatewayResultTypeDef:
        """
        Deletes the specified transit gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_transit_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_transit_gateway)
        """

    async def delete_transit_gateway_connect(
        self, **kwargs: Unpack[DeleteTransitGatewayConnectRequestRequestTypeDef]
    ) -> DeleteTransitGatewayConnectResultTypeDef:
        """
        Deletes the specified Connect attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_transit_gateway_connect.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_transit_gateway_connect)
        """

    async def delete_transit_gateway_connect_peer(
        self, **kwargs: Unpack[DeleteTransitGatewayConnectPeerRequestRequestTypeDef]
    ) -> DeleteTransitGatewayConnectPeerResultTypeDef:
        """
        Deletes the specified Connect peer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_transit_gateway_connect_peer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_transit_gateway_connect_peer)
        """

    async def delete_transit_gateway_multicast_domain(
        self, **kwargs: Unpack[DeleteTransitGatewayMulticastDomainRequestRequestTypeDef]
    ) -> DeleteTransitGatewayMulticastDomainResultTypeDef:
        """
        Deletes the specified transit gateway multicast domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_transit_gateway_multicast_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_transit_gateway_multicast_domain)
        """

    async def delete_transit_gateway_peering_attachment(
        self, **kwargs: Unpack[DeleteTransitGatewayPeeringAttachmentRequestRequestTypeDef]
    ) -> DeleteTransitGatewayPeeringAttachmentResultTypeDef:
        """
        Deletes a transit gateway peering attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_transit_gateway_peering_attachment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_transit_gateway_peering_attachment)
        """

    async def delete_transit_gateway_policy_table(
        self, **kwargs: Unpack[DeleteTransitGatewayPolicyTableRequestRequestTypeDef]
    ) -> DeleteTransitGatewayPolicyTableResultTypeDef:
        """
        Deletes the specified transit gateway policy table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_transit_gateway_policy_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_transit_gateway_policy_table)
        """

    async def delete_transit_gateway_prefix_list_reference(
        self, **kwargs: Unpack[DeleteTransitGatewayPrefixListReferenceRequestRequestTypeDef]
    ) -> DeleteTransitGatewayPrefixListReferenceResultTypeDef:
        """
        Deletes a reference (route) to a prefix list in a specified transit gateway
        route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_transit_gateway_prefix_list_reference.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_transit_gateway_prefix_list_reference)
        """

    async def delete_transit_gateway_route(
        self, **kwargs: Unpack[DeleteTransitGatewayRouteRequestRequestTypeDef]
    ) -> DeleteTransitGatewayRouteResultTypeDef:
        """
        Deletes the specified route from the specified transit gateway route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_transit_gateway_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_transit_gateway_route)
        """

    async def delete_transit_gateway_route_table(
        self, **kwargs: Unpack[DeleteTransitGatewayRouteTableRequestRequestTypeDef]
    ) -> DeleteTransitGatewayRouteTableResultTypeDef:
        """
        Deletes the specified transit gateway route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_transit_gateway_route_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_transit_gateway_route_table)
        """

    async def delete_transit_gateway_route_table_announcement(
        self, **kwargs: Unpack[DeleteTransitGatewayRouteTableAnnouncementRequestRequestTypeDef]
    ) -> DeleteTransitGatewayRouteTableAnnouncementResultTypeDef:
        """
        Advertises to the transit gateway that a transit gateway route table is deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_transit_gateway_route_table_announcement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_transit_gateway_route_table_announcement)
        """

    async def delete_transit_gateway_vpc_attachment(
        self, **kwargs: Unpack[DeleteTransitGatewayVpcAttachmentRequestRequestTypeDef]
    ) -> DeleteTransitGatewayVpcAttachmentResultTypeDef:
        """
        Deletes the specified VPC attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_transit_gateway_vpc_attachment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_transit_gateway_vpc_attachment)
        """

    async def delete_verified_access_endpoint(
        self, **kwargs: Unpack[DeleteVerifiedAccessEndpointRequestRequestTypeDef]
    ) -> DeleteVerifiedAccessEndpointResultTypeDef:
        """
        Delete an Amazon Web Services Verified Access endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_verified_access_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_verified_access_endpoint)
        """

    async def delete_verified_access_group(
        self, **kwargs: Unpack[DeleteVerifiedAccessGroupRequestRequestTypeDef]
    ) -> DeleteVerifiedAccessGroupResultTypeDef:
        """
        Delete an Amazon Web Services Verified Access group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_verified_access_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_verified_access_group)
        """

    async def delete_verified_access_instance(
        self, **kwargs: Unpack[DeleteVerifiedAccessInstanceRequestRequestTypeDef]
    ) -> DeleteVerifiedAccessInstanceResultTypeDef:
        """
        Delete an Amazon Web Services Verified Access instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_verified_access_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_verified_access_instance)
        """

    async def delete_verified_access_trust_provider(
        self, **kwargs: Unpack[DeleteVerifiedAccessTrustProviderRequestRequestTypeDef]
    ) -> DeleteVerifiedAccessTrustProviderResultTypeDef:
        """
        Delete an Amazon Web Services Verified Access trust provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_verified_access_trust_provider.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_verified_access_trust_provider)
        """

    async def delete_volume(
        self, **kwargs: Unpack[DeleteVolumeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified EBS volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_volume)
        """

    async def delete_vpc(
        self, **kwargs: Unpack[DeleteVpcRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_vpc.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_vpc)
        """

    async def delete_vpc_endpoint_connection_notifications(
        self, **kwargs: Unpack[DeleteVpcEndpointConnectionNotificationsRequestRequestTypeDef]
    ) -> DeleteVpcEndpointConnectionNotificationsResultTypeDef:
        """
        Deletes the specified VPC endpoint connection notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_vpc_endpoint_connection_notifications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_vpc_endpoint_connection_notifications)
        """

    async def delete_vpc_endpoint_service_configurations(
        self, **kwargs: Unpack[DeleteVpcEndpointServiceConfigurationsRequestRequestTypeDef]
    ) -> DeleteVpcEndpointServiceConfigurationsResultTypeDef:
        """
        Deletes the specified VPC endpoint service configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_vpc_endpoint_service_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_vpc_endpoint_service_configurations)
        """

    async def delete_vpc_endpoints(
        self, **kwargs: Unpack[DeleteVpcEndpointsRequestRequestTypeDef]
    ) -> DeleteVpcEndpointsResultTypeDef:
        """
        Deletes the specified VPC endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_vpc_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_vpc_endpoints)
        """

    async def delete_vpc_peering_connection(
        self, **kwargs: Unpack[DeleteVpcPeeringConnectionRequestRequestTypeDef]
    ) -> DeleteVpcPeeringConnectionResultTypeDef:
        """
        Deletes a VPC peering connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_vpc_peering_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_vpc_peering_connection)
        """

    async def delete_vpn_connection(
        self, **kwargs: Unpack[DeleteVpnConnectionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified VPN connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_vpn_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_vpn_connection)
        """

    async def delete_vpn_connection_route(
        self, **kwargs: Unpack[DeleteVpnConnectionRouteRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified static route associated with a VPN connection between an
        existing virtual private gateway and a VPN customer gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_vpn_connection_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_vpn_connection_route)
        """

    async def delete_vpn_gateway(
        self, **kwargs: Unpack[DeleteVpnGatewayRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified virtual private gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/delete_vpn_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#delete_vpn_gateway)
        """

    async def deprovision_byoip_cidr(
        self, **kwargs: Unpack[DeprovisionByoipCidrRequestRequestTypeDef]
    ) -> DeprovisionByoipCidrResultTypeDef:
        """
        Releases the specified address range that you provisioned for use with your
        Amazon Web Services resources through bring your own IP addresses (BYOIP) and
        deletes the corresponding address pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/deprovision_byoip_cidr.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#deprovision_byoip_cidr)
        """

    async def deprovision_ipam_byoasn(
        self, **kwargs: Unpack[DeprovisionIpamByoasnRequestRequestTypeDef]
    ) -> DeprovisionIpamByoasnResultTypeDef:
        """
        Deprovisions your Autonomous System Number (ASN) from your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/deprovision_ipam_byoasn.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#deprovision_ipam_byoasn)
        """

    async def deprovision_ipam_pool_cidr(
        self, **kwargs: Unpack[DeprovisionIpamPoolCidrRequestRequestTypeDef]
    ) -> DeprovisionIpamPoolCidrResultTypeDef:
        """
        Deprovision a CIDR provisioned from an IPAM pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/deprovision_ipam_pool_cidr.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#deprovision_ipam_pool_cidr)
        """

    async def deprovision_public_ipv4_pool_cidr(
        self, **kwargs: Unpack[DeprovisionPublicIpv4PoolCidrRequestRequestTypeDef]
    ) -> DeprovisionPublicIpv4PoolCidrResultTypeDef:
        """
        Deprovision a CIDR from a public IPv4 pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/deprovision_public_ipv4_pool_cidr.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#deprovision_public_ipv4_pool_cidr)
        """

    async def deregister_image(
        self, **kwargs: Unpack[DeregisterImageRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters the specified AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/deregister_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#deregister_image)
        """

    async def deregister_instance_event_notification_attributes(
        self, **kwargs: Unpack[DeregisterInstanceEventNotificationAttributesRequestRequestTypeDef]
    ) -> DeregisterInstanceEventNotificationAttributesResultTypeDef:
        """
        Deregisters tag keys to prevent tags that have the specified tag keys from
        being included in scheduled event notifications for resources in the Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/deregister_instance_event_notification_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#deregister_instance_event_notification_attributes)
        """

    async def deregister_transit_gateway_multicast_group_members(
        self, **kwargs: Unpack[DeregisterTransitGatewayMulticastGroupMembersRequestRequestTypeDef]
    ) -> DeregisterTransitGatewayMulticastGroupMembersResultTypeDef:
        """
        Deregisters the specified members (network interfaces) from the transit gateway
        multicast group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/deregister_transit_gateway_multicast_group_members.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#deregister_transit_gateway_multicast_group_members)
        """

    async def deregister_transit_gateway_multicast_group_sources(
        self, **kwargs: Unpack[DeregisterTransitGatewayMulticastGroupSourcesRequestRequestTypeDef]
    ) -> DeregisterTransitGatewayMulticastGroupSourcesResultTypeDef:
        """
        Deregisters the specified sources (network interfaces) from the transit gateway
        multicast group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/deregister_transit_gateway_multicast_group_sources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#deregister_transit_gateway_multicast_group_sources)
        """

    async def describe_account_attributes(
        self, **kwargs: Unpack[DescribeAccountAttributesRequestRequestTypeDef]
    ) -> DescribeAccountAttributesResultTypeDef:
        """
        Describes attributes of your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_account_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_account_attributes)
        """

    async def describe_address_transfers(
        self, **kwargs: Unpack[DescribeAddressTransfersRequestRequestTypeDef]
    ) -> DescribeAddressTransfersResultTypeDef:
        """
        Describes an Elastic IP address transfer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_address_transfers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_address_transfers)
        """

    async def describe_addresses(
        self, **kwargs: Unpack[DescribeAddressesRequestRequestTypeDef]
    ) -> DescribeAddressesResultTypeDef:
        """
        Describes the specified Elastic IP addresses or all of your Elastic IP
        addresses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_addresses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_addresses)
        """

    async def describe_addresses_attribute(
        self, **kwargs: Unpack[DescribeAddressesAttributeRequestRequestTypeDef]
    ) -> DescribeAddressesAttributeResultTypeDef:
        """
        Describes the attributes of the specified Elastic IP addresses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_addresses_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_addresses_attribute)
        """

    async def describe_aggregate_id_format(
        self, **kwargs: Unpack[DescribeAggregateIdFormatRequestRequestTypeDef]
    ) -> DescribeAggregateIdFormatResultTypeDef:
        """
        Describes the longer ID format settings for all resource types in a specific
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_aggregate_id_format.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_aggregate_id_format)
        """

    async def describe_availability_zones(
        self, **kwargs: Unpack[DescribeAvailabilityZonesRequestRequestTypeDef]
    ) -> DescribeAvailabilityZonesResultTypeDef:
        """
        Describes the Availability Zones, Local Zones, and Wavelength Zones that are
        available to you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_availability_zones.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_availability_zones)
        """

    async def describe_aws_network_performance_metric_subscriptions(
        self,
        **kwargs: Unpack[DescribeAwsNetworkPerformanceMetricSubscriptionsRequestRequestTypeDef],
    ) -> DescribeAwsNetworkPerformanceMetricSubscriptionsResultTypeDef:
        """
        Describes the current Infrastructure Performance metric subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_aws_network_performance_metric_subscriptions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_aws_network_performance_metric_subscriptions)
        """

    async def describe_bundle_tasks(
        self, **kwargs: Unpack[DescribeBundleTasksRequestRequestTypeDef]
    ) -> DescribeBundleTasksResultTypeDef:
        """
        Describes the specified bundle tasks or all of your bundle tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_bundle_tasks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_bundle_tasks)
        """

    async def describe_byoip_cidrs(
        self, **kwargs: Unpack[DescribeByoipCidrsRequestRequestTypeDef]
    ) -> DescribeByoipCidrsResultTypeDef:
        """
        Describes the IP address ranges that were specified in calls to
        <a>ProvisionByoipCidr</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_byoip_cidrs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_byoip_cidrs)
        """

    async def describe_capacity_block_offerings(
        self, **kwargs: Unpack[DescribeCapacityBlockOfferingsRequestRequestTypeDef]
    ) -> DescribeCapacityBlockOfferingsResultTypeDef:
        """
        Describes Capacity Block offerings available for purchase in the Amazon Web
        Services Region that you're currently using.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_capacity_block_offerings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_capacity_block_offerings)
        """

    async def describe_capacity_reservation_fleets(
        self, **kwargs: Unpack[DescribeCapacityReservationFleetsRequestRequestTypeDef]
    ) -> DescribeCapacityReservationFleetsResultTypeDef:
        """
        Describes one or more Capacity Reservation Fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_capacity_reservation_fleets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_capacity_reservation_fleets)
        """

    async def describe_capacity_reservations(
        self, **kwargs: Unpack[DescribeCapacityReservationsRequestRequestTypeDef]
    ) -> DescribeCapacityReservationsResultTypeDef:
        """
        Describes one or more of your Capacity Reservations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_capacity_reservations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_capacity_reservations)
        """

    async def describe_carrier_gateways(
        self, **kwargs: Unpack[DescribeCarrierGatewaysRequestRequestTypeDef]
    ) -> DescribeCarrierGatewaysResultTypeDef:
        """
        Describes one or more of your carrier gateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_carrier_gateways.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_carrier_gateways)
        """

    async def describe_classic_link_instances(
        self, **kwargs: Unpack[DescribeClassicLinkInstancesRequestRequestTypeDef]
    ) -> DescribeClassicLinkInstancesResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_classic_link_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_classic_link_instances)
        """

    async def describe_client_vpn_authorization_rules(
        self, **kwargs: Unpack[DescribeClientVpnAuthorizationRulesRequestRequestTypeDef]
    ) -> DescribeClientVpnAuthorizationRulesResultTypeDef:
        """
        Describes the authorization rules for a specified Client VPN endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_client_vpn_authorization_rules.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_client_vpn_authorization_rules)
        """

    async def describe_client_vpn_connections(
        self, **kwargs: Unpack[DescribeClientVpnConnectionsRequestRequestTypeDef]
    ) -> DescribeClientVpnConnectionsResultTypeDef:
        """
        Describes active client connections and connections that have been terminated
        within the last 60 minutes for the specified Client VPN endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_client_vpn_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_client_vpn_connections)
        """

    async def describe_client_vpn_endpoints(
        self, **kwargs: Unpack[DescribeClientVpnEndpointsRequestRequestTypeDef]
    ) -> DescribeClientVpnEndpointsResultTypeDef:
        """
        Describes one or more Client VPN endpoints in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_client_vpn_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_client_vpn_endpoints)
        """

    async def describe_client_vpn_routes(
        self, **kwargs: Unpack[DescribeClientVpnRoutesRequestRequestTypeDef]
    ) -> DescribeClientVpnRoutesResultTypeDef:
        """
        Describes the routes for the specified Client VPN endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_client_vpn_routes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_client_vpn_routes)
        """

    async def describe_client_vpn_target_networks(
        self, **kwargs: Unpack[DescribeClientVpnTargetNetworksRequestRequestTypeDef]
    ) -> DescribeClientVpnTargetNetworksResultTypeDef:
        """
        Describes the target networks associated with the specified Client VPN endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_client_vpn_target_networks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_client_vpn_target_networks)
        """

    async def describe_coip_pools(
        self, **kwargs: Unpack[DescribeCoipPoolsRequestRequestTypeDef]
    ) -> DescribeCoipPoolsResultTypeDef:
        """
        Describes the specified customer-owned address pools or all of your
        customer-owned address pools.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_coip_pools.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_coip_pools)
        """

    async def describe_conversion_tasks(
        self, **kwargs: Unpack[DescribeConversionTasksRequestRequestTypeDef]
    ) -> DescribeConversionTasksResultTypeDef:
        """
        Describes the specified conversion tasks or all your conversion tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_conversion_tasks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_conversion_tasks)
        """

    async def describe_customer_gateways(
        self, **kwargs: Unpack[DescribeCustomerGatewaysRequestRequestTypeDef]
    ) -> DescribeCustomerGatewaysResultTypeDef:
        """
        Describes one or more of your VPN customer gateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_customer_gateways.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_customer_gateways)
        """

    async def describe_dhcp_options(
        self, **kwargs: Unpack[DescribeDhcpOptionsRequestRequestTypeDef]
    ) -> DescribeDhcpOptionsResultTypeDef:
        """
        Describes your DHCP option sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_dhcp_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_dhcp_options)
        """

    async def describe_egress_only_internet_gateways(
        self, **kwargs: Unpack[DescribeEgressOnlyInternetGatewaysRequestRequestTypeDef]
    ) -> DescribeEgressOnlyInternetGatewaysResultTypeDef:
        """
        Describes your egress-only internet gateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_egress_only_internet_gateways.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_egress_only_internet_gateways)
        """

    async def describe_elastic_gpus(
        self, **kwargs: Unpack[DescribeElasticGpusRequestRequestTypeDef]
    ) -> DescribeElasticGpusResultTypeDef:
        """
        Amazon Elastic Graphics reached end of life on January 8, 2024.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_elastic_gpus.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_elastic_gpus)
        """

    async def describe_export_image_tasks(
        self, **kwargs: Unpack[DescribeExportImageTasksRequestRequestTypeDef]
    ) -> DescribeExportImageTasksResultTypeDef:
        """
        Describes the specified export image tasks or all of your export image tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_export_image_tasks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_export_image_tasks)
        """

    async def describe_export_tasks(
        self, **kwargs: Unpack[DescribeExportTasksRequestRequestTypeDef]
    ) -> DescribeExportTasksResultTypeDef:
        """
        Describes the specified export instance tasks or all of your export instance
        tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_export_tasks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_export_tasks)
        """

    async def describe_fast_launch_images(
        self, **kwargs: Unpack[DescribeFastLaunchImagesRequestRequestTypeDef]
    ) -> DescribeFastLaunchImagesResultTypeDef:
        """
        Describe details for Windows AMIs that are configured for Windows fast launch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_fast_launch_images.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_fast_launch_images)
        """

    async def describe_fast_snapshot_restores(
        self, **kwargs: Unpack[DescribeFastSnapshotRestoresRequestRequestTypeDef]
    ) -> DescribeFastSnapshotRestoresResultTypeDef:
        """
        Describes the state of fast snapshot restores for your snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_fast_snapshot_restores.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_fast_snapshot_restores)
        """

    async def describe_fleet_history(
        self, **kwargs: Unpack[DescribeFleetHistoryRequestRequestTypeDef]
    ) -> DescribeFleetHistoryResultTypeDef:
        """
        Describes the events for the specified EC2 Fleet during the specified time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_fleet_history.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_fleet_history)
        """

    async def describe_fleet_instances(
        self, **kwargs: Unpack[DescribeFleetInstancesRequestRequestTypeDef]
    ) -> DescribeFleetInstancesResultTypeDef:
        """
        Describes the running instances for the specified EC2 Fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_fleet_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_fleet_instances)
        """

    async def describe_fleets(
        self, **kwargs: Unpack[DescribeFleetsRequestRequestTypeDef]
    ) -> DescribeFleetsResultTypeDef:
        """
        Describes the specified EC2 Fleet or all of your EC2 Fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_fleets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_fleets)
        """

    async def describe_flow_logs(
        self, **kwargs: Unpack[DescribeFlowLogsRequestRequestTypeDef]
    ) -> DescribeFlowLogsResultTypeDef:
        """
        Describes one or more flow logs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_flow_logs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_flow_logs)
        """

    async def describe_fpga_image_attribute(
        self, **kwargs: Unpack[DescribeFpgaImageAttributeRequestRequestTypeDef]
    ) -> DescribeFpgaImageAttributeResultTypeDef:
        """
        Describes the specified attribute of the specified Amazon FPGA Image (AFI).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_fpga_image_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_fpga_image_attribute)
        """

    async def describe_fpga_images(
        self, **kwargs: Unpack[DescribeFpgaImagesRequestRequestTypeDef]
    ) -> DescribeFpgaImagesResultTypeDef:
        """
        Describes the Amazon FPGA Images (AFIs) available to you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_fpga_images.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_fpga_images)
        """

    async def describe_host_reservation_offerings(
        self, **kwargs: Unpack[DescribeHostReservationOfferingsRequestRequestTypeDef]
    ) -> DescribeHostReservationOfferingsResultTypeDef:
        """
        Describes the Dedicated Host reservations that are available to purchase.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_host_reservation_offerings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_host_reservation_offerings)
        """

    async def describe_host_reservations(
        self, **kwargs: Unpack[DescribeHostReservationsRequestRequestTypeDef]
    ) -> DescribeHostReservationsResultTypeDef:
        """
        Describes reservations that are associated with Dedicated Hosts in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_host_reservations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_host_reservations)
        """

    async def describe_hosts(
        self, **kwargs: Unpack[DescribeHostsRequestRequestTypeDef]
    ) -> DescribeHostsResultTypeDef:
        """
        Describes the specified Dedicated Hosts or all your Dedicated Hosts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_hosts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_hosts)
        """

    async def describe_iam_instance_profile_associations(
        self, **kwargs: Unpack[DescribeIamInstanceProfileAssociationsRequestRequestTypeDef]
    ) -> DescribeIamInstanceProfileAssociationsResultTypeDef:
        """
        Describes your IAM instance profile associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_iam_instance_profile_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_iam_instance_profile_associations)
        """

    async def describe_id_format(
        self, **kwargs: Unpack[DescribeIdFormatRequestRequestTypeDef]
    ) -> DescribeIdFormatResultTypeDef:
        """
        Describes the ID format settings for your resources on a per-Region basis, for
        example, to view which resource types are enabled for longer IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_id_format.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_id_format)
        """

    async def describe_identity_id_format(
        self, **kwargs: Unpack[DescribeIdentityIdFormatRequestRequestTypeDef]
    ) -> DescribeIdentityIdFormatResultTypeDef:
        """
        Describes the ID format settings for resources for the specified IAM user, IAM
        role, or root user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_identity_id_format.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_identity_id_format)
        """

    async def describe_image_attribute(
        self, **kwargs: Unpack[DescribeImageAttributeRequestRequestTypeDef]
    ) -> ImageAttributeTypeDef:
        """
        Describes the specified attribute of the specified AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_image_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_image_attribute)
        """

    async def describe_images(
        self, **kwargs: Unpack[DescribeImagesRequestRequestTypeDef]
    ) -> DescribeImagesResultTypeDef:
        """
        Describes the specified images (AMIs, AKIs, and ARIs) available to you or all
        of the images available to you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_images.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_images)
        """

    async def describe_import_image_tasks(
        self, **kwargs: Unpack[DescribeImportImageTasksRequestRequestTypeDef]
    ) -> DescribeImportImageTasksResultTypeDef:
        """
        Displays details about an import virtual machine or import snapshot tasks that
        are already created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_import_image_tasks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_import_image_tasks)
        """

    async def describe_import_snapshot_tasks(
        self, **kwargs: Unpack[DescribeImportSnapshotTasksRequestRequestTypeDef]
    ) -> DescribeImportSnapshotTasksResultTypeDef:
        """
        Describes your import snapshot tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_import_snapshot_tasks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_import_snapshot_tasks)
        """

    async def describe_instance_attribute(
        self, **kwargs: Unpack[DescribeInstanceAttributeRequestRequestTypeDef]
    ) -> InstanceAttributeTypeDef:
        """
        Describes the specified attribute of the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_instance_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_instance_attribute)
        """

    async def describe_instance_connect_endpoints(
        self, **kwargs: Unpack[DescribeInstanceConnectEndpointsRequestRequestTypeDef]
    ) -> DescribeInstanceConnectEndpointsResultTypeDef:
        """
        Describes the specified EC2 Instance Connect Endpoints or all EC2 Instance
        Connect Endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_instance_connect_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_instance_connect_endpoints)
        """

    async def describe_instance_credit_specifications(
        self, **kwargs: Unpack[DescribeInstanceCreditSpecificationsRequestRequestTypeDef]
    ) -> DescribeInstanceCreditSpecificationsResultTypeDef:
        """
        Describes the credit option for CPU usage of the specified burstable
        performance instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_instance_credit_specifications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_instance_credit_specifications)
        """

    async def describe_instance_event_notification_attributes(
        self, **kwargs: Unpack[DescribeInstanceEventNotificationAttributesRequestRequestTypeDef]
    ) -> DescribeInstanceEventNotificationAttributesResultTypeDef:
        """
        Describes the tag keys that are registered to appear in scheduled event
        notifications for resources in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_instance_event_notification_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_instance_event_notification_attributes)
        """

    async def describe_instance_event_windows(
        self, **kwargs: Unpack[DescribeInstanceEventWindowsRequestRequestTypeDef]
    ) -> DescribeInstanceEventWindowsResultTypeDef:
        """
        Describes the specified event windows or all event windows.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_instance_event_windows.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_instance_event_windows)
        """

    async def describe_instance_status(
        self, **kwargs: Unpack[DescribeInstanceStatusRequestRequestTypeDef]
    ) -> DescribeInstanceStatusResultTypeDef:
        """
        Describes the status of the specified instances or all of your instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_instance_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_instance_status)
        """

    async def describe_instance_topology(
        self, **kwargs: Unpack[DescribeInstanceTopologyRequestRequestTypeDef]
    ) -> DescribeInstanceTopologyResultTypeDef:
        """
        Describes a tree-based hierarchy that represents the physical host placement of
        your EC2 instances within an Availability Zone or Local Zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_instance_topology.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_instance_topology)
        """

    async def describe_instance_type_offerings(
        self, **kwargs: Unpack[DescribeInstanceTypeOfferingsRequestRequestTypeDef]
    ) -> DescribeInstanceTypeOfferingsResultTypeDef:
        """
        Lists the instance types that are offered for the specified location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_instance_type_offerings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_instance_type_offerings)
        """

    async def describe_instance_types(
        self, **kwargs: Unpack[DescribeInstanceTypesRequestRequestTypeDef]
    ) -> DescribeInstanceTypesResultTypeDef:
        """
        Describes the specified instance types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_instance_types.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_instance_types)
        """

    async def describe_instances(
        self, **kwargs: Unpack[DescribeInstancesRequestRequestTypeDef]
    ) -> DescribeInstancesResultTypeDef:
        """
        Describes the specified instances or all instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_instances)
        """

    async def describe_internet_gateways(
        self, **kwargs: Unpack[DescribeInternetGatewaysRequestRequestTypeDef]
    ) -> DescribeInternetGatewaysResultTypeDef:
        """
        Describes your internet gateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_internet_gateways.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_internet_gateways)
        """

    async def describe_ipam_byoasn(
        self, **kwargs: Unpack[DescribeIpamByoasnRequestRequestTypeDef]
    ) -> DescribeIpamByoasnResultTypeDef:
        """
        Describes your Autonomous System Numbers (ASNs), their provisioning statuses,
        and the BYOIP CIDRs with which they are associated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_ipam_byoasn.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_ipam_byoasn)
        """

    async def describe_ipam_external_resource_verification_tokens(
        self, **kwargs: Unpack[DescribeIpamExternalResourceVerificationTokensRequestRequestTypeDef]
    ) -> DescribeIpamExternalResourceVerificationTokensResultTypeDef:
        """
        Describe verification tokens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_ipam_external_resource_verification_tokens.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_ipam_external_resource_verification_tokens)
        """

    async def describe_ipam_pools(
        self, **kwargs: Unpack[DescribeIpamPoolsRequestRequestTypeDef]
    ) -> DescribeIpamPoolsResultTypeDef:
        """
        Get information about your IPAM pools.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_ipam_pools.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_ipam_pools)
        """

    async def describe_ipam_resource_discoveries(
        self, **kwargs: Unpack[DescribeIpamResourceDiscoveriesRequestRequestTypeDef]
    ) -> DescribeIpamResourceDiscoveriesResultTypeDef:
        """
        Describes IPAM resource discoveries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_ipam_resource_discoveries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_ipam_resource_discoveries)
        """

    async def describe_ipam_resource_discovery_associations(
        self, **kwargs: Unpack[DescribeIpamResourceDiscoveryAssociationsRequestRequestTypeDef]
    ) -> DescribeIpamResourceDiscoveryAssociationsResultTypeDef:
        """
        Describes resource discovery association with an Amazon VPC IPAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_ipam_resource_discovery_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_ipam_resource_discovery_associations)
        """

    async def describe_ipam_scopes(
        self, **kwargs: Unpack[DescribeIpamScopesRequestRequestTypeDef]
    ) -> DescribeIpamScopesResultTypeDef:
        """
        Get information about your IPAM scopes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_ipam_scopes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_ipam_scopes)
        """

    async def describe_ipams(
        self, **kwargs: Unpack[DescribeIpamsRequestRequestTypeDef]
    ) -> DescribeIpamsResultTypeDef:
        """
        Get information about your IPAM pools.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_ipams.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_ipams)
        """

    async def describe_ipv6_pools(
        self, **kwargs: Unpack[DescribeIpv6PoolsRequestRequestTypeDef]
    ) -> DescribeIpv6PoolsResultTypeDef:
        """
        Describes your IPv6 address pools.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_ipv6_pools.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_ipv6_pools)
        """

    async def describe_key_pairs(
        self, **kwargs: Unpack[DescribeKeyPairsRequestRequestTypeDef]
    ) -> DescribeKeyPairsResultTypeDef:
        """
        Describes the specified key pairs or all of your key pairs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_key_pairs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_key_pairs)
        """

    async def describe_launch_template_versions(
        self, **kwargs: Unpack[DescribeLaunchTemplateVersionsRequestRequestTypeDef]
    ) -> DescribeLaunchTemplateVersionsResultTypeDef:
        """
        Describes one or more versions of a specified launch template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_launch_template_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_launch_template_versions)
        """

    async def describe_launch_templates(
        self, **kwargs: Unpack[DescribeLaunchTemplatesRequestRequestTypeDef]
    ) -> DescribeLaunchTemplatesResultTypeDef:
        """
        Describes one or more launch templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_launch_templates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_launch_templates)
        """

    async def describe_local_gateway_route_table_virtual_interface_group_associations(
        self,
        **kwargs: Unpack[
            DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsRequestRequestTypeDef
        ],
    ) -> DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsResultTypeDef:
        """
        Describes the associations between virtual interface groups and local gateway
        route tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_local_gateway_route_table_virtual_interface_group_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_local_gateway_route_table_virtual_interface_group_associations)
        """

    async def describe_local_gateway_route_table_vpc_associations(
        self, **kwargs: Unpack[DescribeLocalGatewayRouteTableVpcAssociationsRequestRequestTypeDef]
    ) -> DescribeLocalGatewayRouteTableVpcAssociationsResultTypeDef:
        """
        Describes the specified associations between VPCs and local gateway route
        tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_local_gateway_route_table_vpc_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_local_gateway_route_table_vpc_associations)
        """

    async def describe_local_gateway_route_tables(
        self, **kwargs: Unpack[DescribeLocalGatewayRouteTablesRequestRequestTypeDef]
    ) -> DescribeLocalGatewayRouteTablesResultTypeDef:
        """
        Describes one or more local gateway route tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_local_gateway_route_tables.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_local_gateway_route_tables)
        """

    async def describe_local_gateway_virtual_interface_groups(
        self, **kwargs: Unpack[DescribeLocalGatewayVirtualInterfaceGroupsRequestRequestTypeDef]
    ) -> DescribeLocalGatewayVirtualInterfaceGroupsResultTypeDef:
        """
        Describes the specified local gateway virtual interface groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_local_gateway_virtual_interface_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_local_gateway_virtual_interface_groups)
        """

    async def describe_local_gateway_virtual_interfaces(
        self, **kwargs: Unpack[DescribeLocalGatewayVirtualInterfacesRequestRequestTypeDef]
    ) -> DescribeLocalGatewayVirtualInterfacesResultTypeDef:
        """
        Describes the specified local gateway virtual interfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_local_gateway_virtual_interfaces.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_local_gateway_virtual_interfaces)
        """

    async def describe_local_gateways(
        self, **kwargs: Unpack[DescribeLocalGatewaysRequestRequestTypeDef]
    ) -> DescribeLocalGatewaysResultTypeDef:
        """
        Describes one or more local gateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_local_gateways.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_local_gateways)
        """

    async def describe_locked_snapshots(
        self, **kwargs: Unpack[DescribeLockedSnapshotsRequestRequestTypeDef]
    ) -> DescribeLockedSnapshotsResultTypeDef:
        """
        Describes the lock status for a snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_locked_snapshots.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_locked_snapshots)
        """

    async def describe_mac_hosts(
        self, **kwargs: Unpack[DescribeMacHostsRequestRequestTypeDef]
    ) -> DescribeMacHostsResultTypeDef:
        """
        Describes the specified EC2 Mac Dedicated Host or all of your EC2 Mac Dedicated
        Hosts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_mac_hosts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_mac_hosts)
        """

    async def describe_managed_prefix_lists(
        self, **kwargs: Unpack[DescribeManagedPrefixListsRequestRequestTypeDef]
    ) -> DescribeManagedPrefixListsResultTypeDef:
        """
        Describes your managed prefix lists and any Amazon Web Services-managed prefix
        lists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_managed_prefix_lists.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_managed_prefix_lists)
        """

    async def describe_moving_addresses(
        self, **kwargs: Unpack[DescribeMovingAddressesRequestRequestTypeDef]
    ) -> DescribeMovingAddressesResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_moving_addresses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_moving_addresses)
        """

    async def describe_nat_gateways(
        self, **kwargs: Unpack[DescribeNatGatewaysRequestRequestTypeDef]
    ) -> DescribeNatGatewaysResultTypeDef:
        """
        Describes your NAT gateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_nat_gateways.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_nat_gateways)
        """

    async def describe_network_acls(
        self, **kwargs: Unpack[DescribeNetworkAclsRequestRequestTypeDef]
    ) -> DescribeNetworkAclsResultTypeDef:
        """
        Describes your network ACLs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_network_acls.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_network_acls)
        """

    async def describe_network_insights_access_scope_analyses(
        self, **kwargs: Unpack[DescribeNetworkInsightsAccessScopeAnalysesRequestRequestTypeDef]
    ) -> DescribeNetworkInsightsAccessScopeAnalysesResultTypeDef:
        """
        Describes the specified Network Access Scope analyses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_network_insights_access_scope_analyses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_network_insights_access_scope_analyses)
        """

    async def describe_network_insights_access_scopes(
        self, **kwargs: Unpack[DescribeNetworkInsightsAccessScopesRequestRequestTypeDef]
    ) -> DescribeNetworkInsightsAccessScopesResultTypeDef:
        """
        Describes the specified Network Access Scopes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_network_insights_access_scopes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_network_insights_access_scopes)
        """

    async def describe_network_insights_analyses(
        self, **kwargs: Unpack[DescribeNetworkInsightsAnalysesRequestRequestTypeDef]
    ) -> DescribeNetworkInsightsAnalysesResultTypeDef:
        """
        Describes one or more of your network insights analyses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_network_insights_analyses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_network_insights_analyses)
        """

    async def describe_network_insights_paths(
        self, **kwargs: Unpack[DescribeNetworkInsightsPathsRequestRequestTypeDef]
    ) -> DescribeNetworkInsightsPathsResultTypeDef:
        """
        Describes one or more of your paths.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_network_insights_paths.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_network_insights_paths)
        """

    async def describe_network_interface_attribute(
        self, **kwargs: Unpack[DescribeNetworkInterfaceAttributeRequestRequestTypeDef]
    ) -> DescribeNetworkInterfaceAttributeResultTypeDef:
        """
        Describes a network interface attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_network_interface_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_network_interface_attribute)
        """

    async def describe_network_interface_permissions(
        self, **kwargs: Unpack[DescribeNetworkInterfacePermissionsRequestRequestTypeDef]
    ) -> DescribeNetworkInterfacePermissionsResultTypeDef:
        """
        Describes the permissions for your network interfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_network_interface_permissions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_network_interface_permissions)
        """

    async def describe_network_interfaces(
        self, **kwargs: Unpack[DescribeNetworkInterfacesRequestRequestTypeDef]
    ) -> DescribeNetworkInterfacesResultTypeDef:
        """
        Describes one or more of your network interfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_network_interfaces.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_network_interfaces)
        """

    async def describe_placement_groups(
        self, **kwargs: Unpack[DescribePlacementGroupsRequestRequestTypeDef]
    ) -> DescribePlacementGroupsResultTypeDef:
        """
        Describes the specified placement groups or all of your placement groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_placement_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_placement_groups)
        """

    async def describe_prefix_lists(
        self, **kwargs: Unpack[DescribePrefixListsRequestRequestTypeDef]
    ) -> DescribePrefixListsResultTypeDef:
        """
        Describes available Amazon Web Services services in a prefix list format, which
        includes the prefix list name and prefix list ID of the service and the IP
        address range for the service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_prefix_lists.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_prefix_lists)
        """

    async def describe_principal_id_format(
        self, **kwargs: Unpack[DescribePrincipalIdFormatRequestRequestTypeDef]
    ) -> DescribePrincipalIdFormatResultTypeDef:
        """
        Describes the ID format settings for the root user and all IAM roles and IAM
        users that have explicitly specified a longer ID (17-character ID) preference.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_principal_id_format.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_principal_id_format)
        """

    async def describe_public_ipv4_pools(
        self, **kwargs: Unpack[DescribePublicIpv4PoolsRequestRequestTypeDef]
    ) -> DescribePublicIpv4PoolsResultTypeDef:
        """
        Describes the specified IPv4 address pools.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_public_ipv4_pools.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_public_ipv4_pools)
        """

    async def describe_regions(
        self, **kwargs: Unpack[DescribeRegionsRequestRequestTypeDef]
    ) -> DescribeRegionsResultTypeDef:
        """
        Describes the Regions that are enabled for your account, or all Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_regions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_regions)
        """

    async def describe_replace_root_volume_tasks(
        self, **kwargs: Unpack[DescribeReplaceRootVolumeTasksRequestRequestTypeDef]
    ) -> DescribeReplaceRootVolumeTasksResultTypeDef:
        """
        Describes a root volume replacement task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_replace_root_volume_tasks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_replace_root_volume_tasks)
        """

    async def describe_reserved_instances(
        self, **kwargs: Unpack[DescribeReservedInstancesRequestRequestTypeDef]
    ) -> DescribeReservedInstancesResultTypeDef:
        """
        Describes one or more of the Reserved Instances that you purchased.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_reserved_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_reserved_instances)
        """

    async def describe_reserved_instances_listings(
        self, **kwargs: Unpack[DescribeReservedInstancesListingsRequestRequestTypeDef]
    ) -> DescribeReservedInstancesListingsResultTypeDef:
        """
        Describes your account's Reserved Instance listings in the Reserved Instance
        Marketplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_reserved_instances_listings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_reserved_instances_listings)
        """

    async def describe_reserved_instances_modifications(
        self, **kwargs: Unpack[DescribeReservedInstancesModificationsRequestRequestTypeDef]
    ) -> DescribeReservedInstancesModificationsResultTypeDef:
        """
        Describes the modifications made to your Reserved Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_reserved_instances_modifications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_reserved_instances_modifications)
        """

    async def describe_reserved_instances_offerings(
        self, **kwargs: Unpack[DescribeReservedInstancesOfferingsRequestRequestTypeDef]
    ) -> DescribeReservedInstancesOfferingsResultTypeDef:
        """
        Describes Reserved Instance offerings that are available for purchase.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_reserved_instances_offerings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_reserved_instances_offerings)
        """

    async def describe_route_tables(
        self, **kwargs: Unpack[DescribeRouteTablesRequestRequestTypeDef]
    ) -> DescribeRouteTablesResultTypeDef:
        """
        Describes your route tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_route_tables.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_route_tables)
        """

    async def describe_scheduled_instance_availability(
        self, **kwargs: Unpack[DescribeScheduledInstanceAvailabilityRequestRequestTypeDef]
    ) -> DescribeScheduledInstanceAvailabilityResultTypeDef:
        """
        Finds available schedules that meet the specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_scheduled_instance_availability.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_scheduled_instance_availability)
        """

    async def describe_scheduled_instances(
        self, **kwargs: Unpack[DescribeScheduledInstancesRequestRequestTypeDef]
    ) -> DescribeScheduledInstancesResultTypeDef:
        """
        Describes the specified Scheduled Instances or all your Scheduled Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_scheduled_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_scheduled_instances)
        """

    async def describe_security_group_references(
        self, **kwargs: Unpack[DescribeSecurityGroupReferencesRequestRequestTypeDef]
    ) -> DescribeSecurityGroupReferencesResultTypeDef:
        """
        Describes the VPCs on the other side of a VPC peering connection that are
        referencing the security groups you've specified in this request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_security_group_references.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_security_group_references)
        """

    async def describe_security_group_rules(
        self, **kwargs: Unpack[DescribeSecurityGroupRulesRequestRequestTypeDef]
    ) -> DescribeSecurityGroupRulesResultTypeDef:
        """
        Describes one or more of your security group rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_security_group_rules.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_security_group_rules)
        """

    async def describe_security_groups(
        self, **kwargs: Unpack[DescribeSecurityGroupsRequestRequestTypeDef]
    ) -> DescribeSecurityGroupsResultTypeDef:
        """
        Describes the specified security groups or all of your security groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_security_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_security_groups)
        """

    async def describe_snapshot_attribute(
        self, **kwargs: Unpack[DescribeSnapshotAttributeRequestRequestTypeDef]
    ) -> DescribeSnapshotAttributeResultTypeDef:
        """
        Describes the specified attribute of the specified snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_snapshot_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_snapshot_attribute)
        """

    async def describe_snapshot_tier_status(
        self, **kwargs: Unpack[DescribeSnapshotTierStatusRequestRequestTypeDef]
    ) -> DescribeSnapshotTierStatusResultTypeDef:
        """
        Describes the storage tier status of one or more Amazon EBS snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_snapshot_tier_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_snapshot_tier_status)
        """

    async def describe_snapshots(
        self, **kwargs: Unpack[DescribeSnapshotsRequestRequestTypeDef]
    ) -> DescribeSnapshotsResultTypeDef:
        """
        Describes the specified EBS snapshots available to you or all of the EBS
        snapshots available to you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_snapshots.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_snapshots)
        """

    async def describe_spot_datafeed_subscription(
        self, **kwargs: Unpack[DescribeSpotDatafeedSubscriptionRequestRequestTypeDef]
    ) -> DescribeSpotDatafeedSubscriptionResultTypeDef:
        """
        Describes the data feed for Spot Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_spot_datafeed_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_spot_datafeed_subscription)
        """

    async def describe_spot_fleet_instances(
        self, **kwargs: Unpack[DescribeSpotFleetInstancesRequestRequestTypeDef]
    ) -> DescribeSpotFleetInstancesResponseTypeDef:
        """
        Describes the running instances for the specified Spot Fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_spot_fleet_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_spot_fleet_instances)
        """

    async def describe_spot_fleet_request_history(
        self, **kwargs: Unpack[DescribeSpotFleetRequestHistoryRequestRequestTypeDef]
    ) -> DescribeSpotFleetRequestHistoryResponseTypeDef:
        """
        Describes the events for the specified Spot Fleet request during the specified
        time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_spot_fleet_request_history.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_spot_fleet_request_history)
        """

    async def describe_spot_fleet_requests(
        self, **kwargs: Unpack[DescribeSpotFleetRequestsRequestRequestTypeDef]
    ) -> DescribeSpotFleetRequestsResponseTypeDef:
        """
        Describes your Spot Fleet requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_spot_fleet_requests.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_spot_fleet_requests)
        """

    async def describe_spot_instance_requests(
        self, **kwargs: Unpack[DescribeSpotInstanceRequestsRequestRequestTypeDef]
    ) -> DescribeSpotInstanceRequestsResultTypeDef:
        """
        Describes the specified Spot Instance requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_spot_instance_requests.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_spot_instance_requests)
        """

    async def describe_spot_price_history(
        self, **kwargs: Unpack[DescribeSpotPriceHistoryRequestRequestTypeDef]
    ) -> DescribeSpotPriceHistoryResultTypeDef:
        """
        Describes the Spot price history.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_spot_price_history.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_spot_price_history)
        """

    async def describe_stale_security_groups(
        self, **kwargs: Unpack[DescribeStaleSecurityGroupsRequestRequestTypeDef]
    ) -> DescribeStaleSecurityGroupsResultTypeDef:
        """
        Describes the stale security group rules for security groups in a specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_stale_security_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_stale_security_groups)
        """

    async def describe_store_image_tasks(
        self, **kwargs: Unpack[DescribeStoreImageTasksRequestRequestTypeDef]
    ) -> DescribeStoreImageTasksResultTypeDef:
        """
        Describes the progress of the AMI store tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_store_image_tasks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_store_image_tasks)
        """

    async def describe_subnets(
        self, **kwargs: Unpack[DescribeSubnetsRequestRequestTypeDef]
    ) -> DescribeSubnetsResultTypeDef:
        """
        Describes your subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_subnets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_subnets)
        """

    async def describe_tags(
        self, **kwargs: Unpack[DescribeTagsRequestRequestTypeDef]
    ) -> DescribeTagsResultTypeDef:
        """
        Describes the specified tags for your EC2 resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_tags)
        """

    async def describe_traffic_mirror_filter_rules(
        self, **kwargs: Unpack[DescribeTrafficMirrorFilterRulesRequestRequestTypeDef]
    ) -> DescribeTrafficMirrorFilterRulesResultTypeDef:
        """
        Describe traffic mirror filters that determine the traffic that is mirrored.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_traffic_mirror_filter_rules.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_traffic_mirror_filter_rules)
        """

    async def describe_traffic_mirror_filters(
        self, **kwargs: Unpack[DescribeTrafficMirrorFiltersRequestRequestTypeDef]
    ) -> DescribeTrafficMirrorFiltersResultTypeDef:
        """
        Describes one or more Traffic Mirror filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_traffic_mirror_filters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_traffic_mirror_filters)
        """

    async def describe_traffic_mirror_sessions(
        self, **kwargs: Unpack[DescribeTrafficMirrorSessionsRequestRequestTypeDef]
    ) -> DescribeTrafficMirrorSessionsResultTypeDef:
        """
        Describes one or more Traffic Mirror sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_traffic_mirror_sessions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_traffic_mirror_sessions)
        """

    async def describe_traffic_mirror_targets(
        self, **kwargs: Unpack[DescribeTrafficMirrorTargetsRequestRequestTypeDef]
    ) -> DescribeTrafficMirrorTargetsResultTypeDef:
        """
        Information about one or more Traffic Mirror targets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_traffic_mirror_targets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_traffic_mirror_targets)
        """

    async def describe_transit_gateway_attachments(
        self, **kwargs: Unpack[DescribeTransitGatewayAttachmentsRequestRequestTypeDef]
    ) -> DescribeTransitGatewayAttachmentsResultTypeDef:
        """
        Describes one or more attachments between resources and transit gateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_transit_gateway_attachments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_transit_gateway_attachments)
        """

    async def describe_transit_gateway_connect_peers(
        self, **kwargs: Unpack[DescribeTransitGatewayConnectPeersRequestRequestTypeDef]
    ) -> DescribeTransitGatewayConnectPeersResultTypeDef:
        """
        Describes one or more Connect peers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_transit_gateway_connect_peers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_transit_gateway_connect_peers)
        """

    async def describe_transit_gateway_connects(
        self, **kwargs: Unpack[DescribeTransitGatewayConnectsRequestRequestTypeDef]
    ) -> DescribeTransitGatewayConnectsResultTypeDef:
        """
        Describes one or more Connect attachments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_transit_gateway_connects.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_transit_gateway_connects)
        """

    async def describe_transit_gateway_multicast_domains(
        self, **kwargs: Unpack[DescribeTransitGatewayMulticastDomainsRequestRequestTypeDef]
    ) -> DescribeTransitGatewayMulticastDomainsResultTypeDef:
        """
        Describes one or more transit gateway multicast domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_transit_gateway_multicast_domains.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_transit_gateway_multicast_domains)
        """

    async def describe_transit_gateway_peering_attachments(
        self, **kwargs: Unpack[DescribeTransitGatewayPeeringAttachmentsRequestRequestTypeDef]
    ) -> DescribeTransitGatewayPeeringAttachmentsResultTypeDef:
        """
        Describes your transit gateway peering attachments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_transit_gateway_peering_attachments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_transit_gateway_peering_attachments)
        """

    async def describe_transit_gateway_policy_tables(
        self, **kwargs: Unpack[DescribeTransitGatewayPolicyTablesRequestRequestTypeDef]
    ) -> DescribeTransitGatewayPolicyTablesResultTypeDef:
        """
        Describes one or more transit gateway route policy tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_transit_gateway_policy_tables.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_transit_gateway_policy_tables)
        """

    async def describe_transit_gateway_route_table_announcements(
        self, **kwargs: Unpack[DescribeTransitGatewayRouteTableAnnouncementsRequestRequestTypeDef]
    ) -> DescribeTransitGatewayRouteTableAnnouncementsResultTypeDef:
        """
        Describes one or more transit gateway route table advertisements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_transit_gateway_route_table_announcements.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_transit_gateway_route_table_announcements)
        """

    async def describe_transit_gateway_route_tables(
        self, **kwargs: Unpack[DescribeTransitGatewayRouteTablesRequestRequestTypeDef]
    ) -> DescribeTransitGatewayRouteTablesResultTypeDef:
        """
        Describes one or more transit gateway route tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_transit_gateway_route_tables.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_transit_gateway_route_tables)
        """

    async def describe_transit_gateway_vpc_attachments(
        self, **kwargs: Unpack[DescribeTransitGatewayVpcAttachmentsRequestRequestTypeDef]
    ) -> DescribeTransitGatewayVpcAttachmentsResultTypeDef:
        """
        Describes one or more VPC attachments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_transit_gateway_vpc_attachments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_transit_gateway_vpc_attachments)
        """

    async def describe_transit_gateways(
        self, **kwargs: Unpack[DescribeTransitGatewaysRequestRequestTypeDef]
    ) -> DescribeTransitGatewaysResultTypeDef:
        """
        Describes one or more transit gateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_transit_gateways.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_transit_gateways)
        """

    async def describe_trunk_interface_associations(
        self, **kwargs: Unpack[DescribeTrunkInterfaceAssociationsRequestRequestTypeDef]
    ) -> DescribeTrunkInterfaceAssociationsResultTypeDef:
        """
        Describes one or more network interface trunk associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_trunk_interface_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_trunk_interface_associations)
        """

    async def describe_verified_access_endpoints(
        self, **kwargs: Unpack[DescribeVerifiedAccessEndpointsRequestRequestTypeDef]
    ) -> DescribeVerifiedAccessEndpointsResultTypeDef:
        """
        Describes the specified Amazon Web Services Verified Access endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_verified_access_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_verified_access_endpoints)
        """

    async def describe_verified_access_groups(
        self, **kwargs: Unpack[DescribeVerifiedAccessGroupsRequestRequestTypeDef]
    ) -> DescribeVerifiedAccessGroupsResultTypeDef:
        """
        Describes the specified Verified Access groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_verified_access_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_verified_access_groups)
        """

    async def describe_verified_access_instance_logging_configurations(
        self,
        **kwargs: Unpack[DescribeVerifiedAccessInstanceLoggingConfigurationsRequestRequestTypeDef],
    ) -> DescribeVerifiedAccessInstanceLoggingConfigurationsResultTypeDef:
        """
        Describes the specified Amazon Web Services Verified Access instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_verified_access_instance_logging_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_verified_access_instance_logging_configurations)
        """

    async def describe_verified_access_instances(
        self, **kwargs: Unpack[DescribeVerifiedAccessInstancesRequestRequestTypeDef]
    ) -> DescribeVerifiedAccessInstancesResultTypeDef:
        """
        Describes the specified Amazon Web Services Verified Access instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_verified_access_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_verified_access_instances)
        """

    async def describe_verified_access_trust_providers(
        self, **kwargs: Unpack[DescribeVerifiedAccessTrustProvidersRequestRequestTypeDef]
    ) -> DescribeVerifiedAccessTrustProvidersResultTypeDef:
        """
        Describes the specified Amazon Web Services Verified Access trust providers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_verified_access_trust_providers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_verified_access_trust_providers)
        """

    async def describe_volume_attribute(
        self, **kwargs: Unpack[DescribeVolumeAttributeRequestRequestTypeDef]
    ) -> DescribeVolumeAttributeResultTypeDef:
        """
        Describes the specified attribute of the specified volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_volume_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_volume_attribute)
        """

    async def describe_volume_status(
        self, **kwargs: Unpack[DescribeVolumeStatusRequestRequestTypeDef]
    ) -> DescribeVolumeStatusResultTypeDef:
        """
        Describes the status of the specified volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_volume_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_volume_status)
        """

    async def describe_volumes(
        self, **kwargs: Unpack[DescribeVolumesRequestRequestTypeDef]
    ) -> DescribeVolumesResultTypeDef:
        """
        Describes the specified EBS volumes or all of your EBS volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_volumes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_volumes)
        """

    async def describe_volumes_modifications(
        self, **kwargs: Unpack[DescribeVolumesModificationsRequestRequestTypeDef]
    ) -> DescribeVolumesModificationsResultTypeDef:
        """
        Describes the most recent volume modification request for the specified EBS
        volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_volumes_modifications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_volumes_modifications)
        """

    async def describe_vpc_attribute(
        self, **kwargs: Unpack[DescribeVpcAttributeRequestRequestTypeDef]
    ) -> DescribeVpcAttributeResultTypeDef:
        """
        Describes the specified attribute of the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpc_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_vpc_attribute)
        """

    async def describe_vpc_classic_link(
        self, **kwargs: Unpack[DescribeVpcClassicLinkRequestRequestTypeDef]
    ) -> DescribeVpcClassicLinkResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpc_classic_link.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_vpc_classic_link)
        """

    async def describe_vpc_classic_link_dns_support(
        self, **kwargs: Unpack[DescribeVpcClassicLinkDnsSupportRequestRequestTypeDef]
    ) -> DescribeVpcClassicLinkDnsSupportResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpc_classic_link_dns_support.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_vpc_classic_link_dns_support)
        """

    async def describe_vpc_endpoint_connection_notifications(
        self, **kwargs: Unpack[DescribeVpcEndpointConnectionNotificationsRequestRequestTypeDef]
    ) -> DescribeVpcEndpointConnectionNotificationsResultTypeDef:
        """
        Describes the connection notifications for VPC endpoints and VPC endpoint
        services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpc_endpoint_connection_notifications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_vpc_endpoint_connection_notifications)
        """

    async def describe_vpc_endpoint_connections(
        self, **kwargs: Unpack[DescribeVpcEndpointConnectionsRequestRequestTypeDef]
    ) -> DescribeVpcEndpointConnectionsResultTypeDef:
        """
        Describes the VPC endpoint connections to your VPC endpoint services, including
        any endpoints that are pending your acceptance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpc_endpoint_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_vpc_endpoint_connections)
        """

    async def describe_vpc_endpoint_service_configurations(
        self, **kwargs: Unpack[DescribeVpcEndpointServiceConfigurationsRequestRequestTypeDef]
    ) -> DescribeVpcEndpointServiceConfigurationsResultTypeDef:
        """
        Describes the VPC endpoint service configurations in your account (your
        services).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpc_endpoint_service_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_vpc_endpoint_service_configurations)
        """

    async def describe_vpc_endpoint_service_permissions(
        self, **kwargs: Unpack[DescribeVpcEndpointServicePermissionsRequestRequestTypeDef]
    ) -> DescribeVpcEndpointServicePermissionsResultTypeDef:
        """
        Describes the principals (service consumers) that are permitted to discover
        your VPC endpoint service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpc_endpoint_service_permissions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_vpc_endpoint_service_permissions)
        """

    async def describe_vpc_endpoint_services(
        self, **kwargs: Unpack[DescribeVpcEndpointServicesRequestRequestTypeDef]
    ) -> DescribeVpcEndpointServicesResultTypeDef:
        """
        Describes available services to which you can create a VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpc_endpoint_services.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_vpc_endpoint_services)
        """

    async def describe_vpc_endpoints(
        self, **kwargs: Unpack[DescribeVpcEndpointsRequestRequestTypeDef]
    ) -> DescribeVpcEndpointsResultTypeDef:
        """
        Describes your VPC endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpc_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_vpc_endpoints)
        """

    async def describe_vpc_peering_connections(
        self, **kwargs: Unpack[DescribeVpcPeeringConnectionsRequestRequestTypeDef]
    ) -> DescribeVpcPeeringConnectionsResultTypeDef:
        """
        Describes your VPC peering connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpc_peering_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_vpc_peering_connections)
        """

    async def describe_vpcs(
        self, **kwargs: Unpack[DescribeVpcsRequestRequestTypeDef]
    ) -> DescribeVpcsResultTypeDef:
        """
        Describes your VPCs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpcs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_vpcs)
        """

    async def describe_vpn_connections(
        self, **kwargs: Unpack[DescribeVpnConnectionsRequestRequestTypeDef]
    ) -> DescribeVpnConnectionsResultTypeDef:
        """
        Describes one or more of your VPN connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpn_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_vpn_connections)
        """

    async def describe_vpn_gateways(
        self, **kwargs: Unpack[DescribeVpnGatewaysRequestRequestTypeDef]
    ) -> DescribeVpnGatewaysResultTypeDef:
        """
        Describes one or more of your virtual private gateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpn_gateways.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#describe_vpn_gateways)
        """

    async def detach_classic_link_vpc(
        self, **kwargs: Unpack[DetachClassicLinkVpcRequestRequestTypeDef]
    ) -> DetachClassicLinkVpcResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/detach_classic_link_vpc.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#detach_classic_link_vpc)
        """

    async def detach_internet_gateway(
        self, **kwargs: Unpack[DetachInternetGatewayRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Detaches an internet gateway from a VPC, disabling connectivity between the
        internet and the VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/detach_internet_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#detach_internet_gateway)
        """

    async def detach_network_interface(
        self, **kwargs: Unpack[DetachNetworkInterfaceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Detaches a network interface from an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/detach_network_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#detach_network_interface)
        """

    async def detach_verified_access_trust_provider(
        self, **kwargs: Unpack[DetachVerifiedAccessTrustProviderRequestRequestTypeDef]
    ) -> DetachVerifiedAccessTrustProviderResultTypeDef:
        """
        Detaches the specified Amazon Web Services Verified Access trust provider from
        the specified Amazon Web Services Verified Access instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/detach_verified_access_trust_provider.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#detach_verified_access_trust_provider)
        """

    async def detach_volume(
        self, **kwargs: Unpack[DetachVolumeRequestRequestTypeDef]
    ) -> VolumeAttachmentResponseTypeDef:
        """
        Detaches an EBS volume from an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/detach_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#detach_volume)
        """

    async def detach_vpn_gateway(
        self, **kwargs: Unpack[DetachVpnGatewayRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Detaches a virtual private gateway from a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/detach_vpn_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#detach_vpn_gateway)
        """

    async def disable_address_transfer(
        self, **kwargs: Unpack[DisableAddressTransferRequestRequestTypeDef]
    ) -> DisableAddressTransferResultTypeDef:
        """
        Disables Elastic IP address transfer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disable_address_transfer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disable_address_transfer)
        """

    async def disable_aws_network_performance_metric_subscription(
        self, **kwargs: Unpack[DisableAwsNetworkPerformanceMetricSubscriptionRequestRequestTypeDef]
    ) -> DisableAwsNetworkPerformanceMetricSubscriptionResultTypeDef:
        """
        Disables Infrastructure Performance metric subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disable_aws_network_performance_metric_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disable_aws_network_performance_metric_subscription)
        """

    async def disable_ebs_encryption_by_default(
        self, **kwargs: Unpack[DisableEbsEncryptionByDefaultRequestRequestTypeDef]
    ) -> DisableEbsEncryptionByDefaultResultTypeDef:
        """
        Disables EBS encryption by default for your account in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disable_ebs_encryption_by_default.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disable_ebs_encryption_by_default)
        """

    async def disable_fast_launch(
        self, **kwargs: Unpack[DisableFastLaunchRequestRequestTypeDef]
    ) -> DisableFastLaunchResultTypeDef:
        """
        Discontinue Windows fast launch for a Windows AMI, and clean up existing
        pre-provisioned snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disable_fast_launch.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disable_fast_launch)
        """

    async def disable_fast_snapshot_restores(
        self, **kwargs: Unpack[DisableFastSnapshotRestoresRequestRequestTypeDef]
    ) -> DisableFastSnapshotRestoresResultTypeDef:
        """
        Disables fast snapshot restores for the specified snapshots in the specified
        Availability Zones.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disable_fast_snapshot_restores.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disable_fast_snapshot_restores)
        """

    async def disable_image(
        self, **kwargs: Unpack[DisableImageRequestRequestTypeDef]
    ) -> DisableImageResultTypeDef:
        """
        Sets the AMI state to <code>disabled</code> and removes all launch permissions
        from the AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disable_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disable_image)
        """

    async def disable_image_block_public_access(
        self, **kwargs: Unpack[DisableImageBlockPublicAccessRequestRequestTypeDef]
    ) -> DisableImageBlockPublicAccessResultTypeDef:
        """
        Disables <i>block public access for AMIs</i> at the account level in the
        specified Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disable_image_block_public_access.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disable_image_block_public_access)
        """

    async def disable_image_deprecation(
        self, **kwargs: Unpack[DisableImageDeprecationRequestRequestTypeDef]
    ) -> DisableImageDeprecationResultTypeDef:
        """
        Cancels the deprecation of the specified AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disable_image_deprecation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disable_image_deprecation)
        """

    async def disable_image_deregistration_protection(
        self, **kwargs: Unpack[DisableImageDeregistrationProtectionRequestRequestTypeDef]
    ) -> DisableImageDeregistrationProtectionResultTypeDef:
        """
        Disables deregistration protection for an AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disable_image_deregistration_protection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disable_image_deregistration_protection)
        """

    async def disable_ipam_organization_admin_account(
        self, **kwargs: Unpack[DisableIpamOrganizationAdminAccountRequestRequestTypeDef]
    ) -> DisableIpamOrganizationAdminAccountResultTypeDef:
        """
        Disable the IPAM account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disable_ipam_organization_admin_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disable_ipam_organization_admin_account)
        """

    async def disable_serial_console_access(
        self, **kwargs: Unpack[DisableSerialConsoleAccessRequestRequestTypeDef]
    ) -> DisableSerialConsoleAccessResultTypeDef:
        """
        Disables access to the EC2 serial console of all instances for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disable_serial_console_access.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disable_serial_console_access)
        """

    async def disable_snapshot_block_public_access(
        self, **kwargs: Unpack[DisableSnapshotBlockPublicAccessRequestRequestTypeDef]
    ) -> DisableSnapshotBlockPublicAccessResultTypeDef:
        """
        Disables the <i>block public access for snapshots</i> setting at the account
        level for the specified Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disable_snapshot_block_public_access.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disable_snapshot_block_public_access)
        """

    async def disable_transit_gateway_route_table_propagation(
        self, **kwargs: Unpack[DisableTransitGatewayRouteTablePropagationRequestRequestTypeDef]
    ) -> DisableTransitGatewayRouteTablePropagationResultTypeDef:
        """
        Disables the specified resource attachment from propagating routes to the
        specified propagation route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disable_transit_gateway_route_table_propagation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disable_transit_gateway_route_table_propagation)
        """

    async def disable_vgw_route_propagation(
        self, **kwargs: Unpack[DisableVgwRoutePropagationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disables a virtual private gateway (VGW) from propagating routes to a specified
        route table of a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disable_vgw_route_propagation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disable_vgw_route_propagation)
        """

    async def disable_vpc_classic_link(
        self, **kwargs: Unpack[DisableVpcClassicLinkRequestRequestTypeDef]
    ) -> DisableVpcClassicLinkResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disable_vpc_classic_link.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disable_vpc_classic_link)
        """

    async def disable_vpc_classic_link_dns_support(
        self, **kwargs: Unpack[DisableVpcClassicLinkDnsSupportRequestRequestTypeDef]
    ) -> DisableVpcClassicLinkDnsSupportResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disable_vpc_classic_link_dns_support.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disable_vpc_classic_link_dns_support)
        """

    async def disassociate_address(
        self, **kwargs: Unpack[DisassociateAddressRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates an Elastic IP address from the instance or network interface it's
        associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disassociate_address.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disassociate_address)
        """

    async def disassociate_client_vpn_target_network(
        self, **kwargs: Unpack[DisassociateClientVpnTargetNetworkRequestRequestTypeDef]
    ) -> DisassociateClientVpnTargetNetworkResultTypeDef:
        """
        Disassociates a target network from the specified Client VPN endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disassociate_client_vpn_target_network.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disassociate_client_vpn_target_network)
        """

    async def disassociate_enclave_certificate_iam_role(
        self, **kwargs: Unpack[DisassociateEnclaveCertificateIamRoleRequestRequestTypeDef]
    ) -> DisassociateEnclaveCertificateIamRoleResultTypeDef:
        """
        Disassociates an IAM role from an Certificate Manager (ACM) certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disassociate_enclave_certificate_iam_role.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disassociate_enclave_certificate_iam_role)
        """

    async def disassociate_iam_instance_profile(
        self, **kwargs: Unpack[DisassociateIamInstanceProfileRequestRequestTypeDef]
    ) -> DisassociateIamInstanceProfileResultTypeDef:
        """
        Disassociates an IAM instance profile from a running or stopped instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disassociate_iam_instance_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disassociate_iam_instance_profile)
        """

    async def disassociate_instance_event_window(
        self, **kwargs: Unpack[DisassociateInstanceEventWindowRequestRequestTypeDef]
    ) -> DisassociateInstanceEventWindowResultTypeDef:
        """
        Disassociates one or more targets from an event window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disassociate_instance_event_window.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disassociate_instance_event_window)
        """

    async def disassociate_ipam_byoasn(
        self, **kwargs: Unpack[DisassociateIpamByoasnRequestRequestTypeDef]
    ) -> DisassociateIpamByoasnResultTypeDef:
        """
        Remove the association between your Autonomous System Number (ASN) and your
        BYOIP CIDR.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disassociate_ipam_byoasn.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disassociate_ipam_byoasn)
        """

    async def disassociate_ipam_resource_discovery(
        self, **kwargs: Unpack[DisassociateIpamResourceDiscoveryRequestRequestTypeDef]
    ) -> DisassociateIpamResourceDiscoveryResultTypeDef:
        """
        Disassociates a resource discovery from an Amazon VPC IPAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disassociate_ipam_resource_discovery.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disassociate_ipam_resource_discovery)
        """

    async def disassociate_nat_gateway_address(
        self, **kwargs: Unpack[DisassociateNatGatewayAddressRequestRequestTypeDef]
    ) -> DisassociateNatGatewayAddressResultTypeDef:
        """
        Disassociates secondary Elastic IP addresses (EIPs) from a public NAT gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disassociate_nat_gateway_address.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disassociate_nat_gateway_address)
        """

    async def disassociate_route_table(
        self, **kwargs: Unpack[DisassociateRouteTableRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates a subnet or gateway from a route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disassociate_route_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disassociate_route_table)
        """

    async def disassociate_subnet_cidr_block(
        self, **kwargs: Unpack[DisassociateSubnetCidrBlockRequestRequestTypeDef]
    ) -> DisassociateSubnetCidrBlockResultTypeDef:
        """
        Disassociates a CIDR block from a subnet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disassociate_subnet_cidr_block.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disassociate_subnet_cidr_block)
        """

    async def disassociate_transit_gateway_multicast_domain(
        self, **kwargs: Unpack[DisassociateTransitGatewayMulticastDomainRequestRequestTypeDef]
    ) -> DisassociateTransitGatewayMulticastDomainResultTypeDef:
        """
        Disassociates the specified subnets from the transit gateway multicast domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disassociate_transit_gateway_multicast_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disassociate_transit_gateway_multicast_domain)
        """

    async def disassociate_transit_gateway_policy_table(
        self, **kwargs: Unpack[DisassociateTransitGatewayPolicyTableRequestRequestTypeDef]
    ) -> DisassociateTransitGatewayPolicyTableResultTypeDef:
        """
        Removes the association between an an attachment and a policy table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disassociate_transit_gateway_policy_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disassociate_transit_gateway_policy_table)
        """

    async def disassociate_transit_gateway_route_table(
        self, **kwargs: Unpack[DisassociateTransitGatewayRouteTableRequestRequestTypeDef]
    ) -> DisassociateTransitGatewayRouteTableResultTypeDef:
        """
        Disassociates a resource attachment from a transit gateway route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disassociate_transit_gateway_route_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disassociate_transit_gateway_route_table)
        """

    async def disassociate_trunk_interface(
        self, **kwargs: Unpack[DisassociateTrunkInterfaceRequestRequestTypeDef]
    ) -> DisassociateTrunkInterfaceResultTypeDef:
        """
        Removes an association between a branch network interface with a trunk network
        interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disassociate_trunk_interface.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disassociate_trunk_interface)
        """

    async def disassociate_vpc_cidr_block(
        self, **kwargs: Unpack[DisassociateVpcCidrBlockRequestRequestTypeDef]
    ) -> DisassociateVpcCidrBlockResultTypeDef:
        """
        Disassociates a CIDR block from a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/disassociate_vpc_cidr_block.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#disassociate_vpc_cidr_block)
        """

    async def enable_address_transfer(
        self, **kwargs: Unpack[EnableAddressTransferRequestRequestTypeDef]
    ) -> EnableAddressTransferResultTypeDef:
        """
        Enables Elastic IP address transfer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_address_transfer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_address_transfer)
        """

    async def enable_aws_network_performance_metric_subscription(
        self, **kwargs: Unpack[EnableAwsNetworkPerformanceMetricSubscriptionRequestRequestTypeDef]
    ) -> EnableAwsNetworkPerformanceMetricSubscriptionResultTypeDef:
        """
        Enables Infrastructure Performance subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_aws_network_performance_metric_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_aws_network_performance_metric_subscription)
        """

    async def enable_ebs_encryption_by_default(
        self, **kwargs: Unpack[EnableEbsEncryptionByDefaultRequestRequestTypeDef]
    ) -> EnableEbsEncryptionByDefaultResultTypeDef:
        """
        Enables EBS encryption by default for your account in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_ebs_encryption_by_default.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_ebs_encryption_by_default)
        """

    async def enable_fast_launch(
        self, **kwargs: Unpack[EnableFastLaunchRequestRequestTypeDef]
    ) -> EnableFastLaunchResultTypeDef:
        """
        When you enable Windows fast launch for a Windows AMI, images are
        pre-provisioned, using snapshots to launch instances up to 65% faster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_fast_launch.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_fast_launch)
        """

    async def enable_fast_snapshot_restores(
        self, **kwargs: Unpack[EnableFastSnapshotRestoresRequestRequestTypeDef]
    ) -> EnableFastSnapshotRestoresResultTypeDef:
        """
        Enables fast snapshot restores for the specified snapshots in the specified
        Availability Zones.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_fast_snapshot_restores.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_fast_snapshot_restores)
        """

    async def enable_image(
        self, **kwargs: Unpack[EnableImageRequestRequestTypeDef]
    ) -> EnableImageResultTypeDef:
        """
        Re-enables a disabled AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_image)
        """

    async def enable_image_block_public_access(
        self, **kwargs: Unpack[EnableImageBlockPublicAccessRequestRequestTypeDef]
    ) -> EnableImageBlockPublicAccessResultTypeDef:
        """
        Enables <i>block public access for AMIs</i> at the account level in the
        specified Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_image_block_public_access.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_image_block_public_access)
        """

    async def enable_image_deprecation(
        self, **kwargs: Unpack[EnableImageDeprecationRequestRequestTypeDef]
    ) -> EnableImageDeprecationResultTypeDef:
        """
        Enables deprecation of the specified AMI at the specified date and time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_image_deprecation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_image_deprecation)
        """

    async def enable_image_deregistration_protection(
        self, **kwargs: Unpack[EnableImageDeregistrationProtectionRequestRequestTypeDef]
    ) -> EnableImageDeregistrationProtectionResultTypeDef:
        """
        Enables deregistration protection for an AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_image_deregistration_protection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_image_deregistration_protection)
        """

    async def enable_ipam_organization_admin_account(
        self, **kwargs: Unpack[EnableIpamOrganizationAdminAccountRequestRequestTypeDef]
    ) -> EnableIpamOrganizationAdminAccountResultTypeDef:
        """
        Enable an Organizations member account as the IPAM admin account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_ipam_organization_admin_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_ipam_organization_admin_account)
        """

    async def enable_reachability_analyzer_organization_sharing(
        self, **kwargs: Unpack[EnableReachabilityAnalyzerOrganizationSharingRequestRequestTypeDef]
    ) -> EnableReachabilityAnalyzerOrganizationSharingResultTypeDef:
        """
        Establishes a trust relationship between Reachability Analyzer and
        Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_reachability_analyzer_organization_sharing.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_reachability_analyzer_organization_sharing)
        """

    async def enable_serial_console_access(
        self, **kwargs: Unpack[EnableSerialConsoleAccessRequestRequestTypeDef]
    ) -> EnableSerialConsoleAccessResultTypeDef:
        """
        Enables access to the EC2 serial console of all instances for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_serial_console_access.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_serial_console_access)
        """

    async def enable_snapshot_block_public_access(
        self, **kwargs: Unpack[EnableSnapshotBlockPublicAccessRequestRequestTypeDef]
    ) -> EnableSnapshotBlockPublicAccessResultTypeDef:
        """
        Enables or modifies the <i>block public access for snapshots</i> setting at the
        account level for the specified Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_snapshot_block_public_access.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_snapshot_block_public_access)
        """

    async def enable_transit_gateway_route_table_propagation(
        self, **kwargs: Unpack[EnableTransitGatewayRouteTablePropagationRequestRequestTypeDef]
    ) -> EnableTransitGatewayRouteTablePropagationResultTypeDef:
        """
        Enables the specified attachment to propagate routes to the specified
        propagation route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_transit_gateway_route_table_propagation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_transit_gateway_route_table_propagation)
        """

    async def enable_vgw_route_propagation(
        self, **kwargs: Unpack[EnableVgwRoutePropagationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables a virtual private gateway (VGW) to propagate routes to the specified
        route table of a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_vgw_route_propagation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_vgw_route_propagation)
        """

    async def enable_volume_io(
        self, **kwargs: Unpack[EnableVolumeIORequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables I/O operations for a volume that had I/O operations disabled because
        the data on the volume was potentially inconsistent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_volume_io.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_volume_io)
        """

    async def enable_vpc_classic_link(
        self, **kwargs: Unpack[EnableVpcClassicLinkRequestRequestTypeDef]
    ) -> EnableVpcClassicLinkResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_vpc_classic_link.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_vpc_classic_link)
        """

    async def enable_vpc_classic_link_dns_support(
        self, **kwargs: Unpack[EnableVpcClassicLinkDnsSupportRequestRequestTypeDef]
    ) -> EnableVpcClassicLinkDnsSupportResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/enable_vpc_classic_link_dns_support.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#enable_vpc_classic_link_dns_support)
        """

    async def export_client_vpn_client_certificate_revocation_list(
        self, **kwargs: Unpack[ExportClientVpnClientCertificateRevocationListRequestRequestTypeDef]
    ) -> ExportClientVpnClientCertificateRevocationListResultTypeDef:
        """
        Downloads the client certificate revocation list for the specified Client VPN
        endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/export_client_vpn_client_certificate_revocation_list.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#export_client_vpn_client_certificate_revocation_list)
        """

    async def export_client_vpn_client_configuration(
        self, **kwargs: Unpack[ExportClientVpnClientConfigurationRequestRequestTypeDef]
    ) -> ExportClientVpnClientConfigurationResultTypeDef:
        """
        Downloads the contents of the Client VPN endpoint configuration file for the
        specified Client VPN endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/export_client_vpn_client_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#export_client_vpn_client_configuration)
        """

    async def export_image(
        self, **kwargs: Unpack[ExportImageRequestRequestTypeDef]
    ) -> ExportImageResultTypeDef:
        """
        Exports an Amazon Machine Image (AMI) to a VM file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/export_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#export_image)
        """

    async def export_transit_gateway_routes(
        self, **kwargs: Unpack[ExportTransitGatewayRoutesRequestRequestTypeDef]
    ) -> ExportTransitGatewayRoutesResultTypeDef:
        """
        Exports routes from the specified transit gateway route table to the specified
        S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/export_transit_gateway_routes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#export_transit_gateway_routes)
        """

    async def get_associated_enclave_certificate_iam_roles(
        self, **kwargs: Unpack[GetAssociatedEnclaveCertificateIamRolesRequestRequestTypeDef]
    ) -> GetAssociatedEnclaveCertificateIamRolesResultTypeDef:
        """
        Returns the IAM roles that are associated with the specified ACM (ACM)
        certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_associated_enclave_certificate_iam_roles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_associated_enclave_certificate_iam_roles)
        """

    async def get_associated_ipv6_pool_cidrs(
        self, **kwargs: Unpack[GetAssociatedIpv6PoolCidrsRequestRequestTypeDef]
    ) -> GetAssociatedIpv6PoolCidrsResultTypeDef:
        """
        Gets information about the IPv6 CIDR block associations for a specified IPv6
        address pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_associated_ipv6_pool_cidrs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_associated_ipv6_pool_cidrs)
        """

    async def get_aws_network_performance_data(
        self, **kwargs: Unpack[GetAwsNetworkPerformanceDataRequestRequestTypeDef]
    ) -> GetAwsNetworkPerformanceDataResultTypeDef:
        """
        Gets network performance data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_aws_network_performance_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_aws_network_performance_data)
        """

    async def get_capacity_reservation_usage(
        self, **kwargs: Unpack[GetCapacityReservationUsageRequestRequestTypeDef]
    ) -> GetCapacityReservationUsageResultTypeDef:
        """
        Gets usage information about a Capacity Reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_capacity_reservation_usage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_capacity_reservation_usage)
        """

    async def get_coip_pool_usage(
        self, **kwargs: Unpack[GetCoipPoolUsageRequestRequestTypeDef]
    ) -> GetCoipPoolUsageResultTypeDef:
        """
        Describes the allocations from the specified customer-owned address pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_coip_pool_usage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_coip_pool_usage)
        """

    async def get_console_output(
        self, **kwargs: Unpack[GetConsoleOutputRequestRequestTypeDef]
    ) -> GetConsoleOutputResultTypeDef:
        """
        Gets the console output for the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_console_output.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_console_output)
        """

    async def get_console_screenshot(
        self, **kwargs: Unpack[GetConsoleScreenshotRequestRequestTypeDef]
    ) -> GetConsoleScreenshotResultTypeDef:
        """
        Retrieve a JPG-format screenshot of a running instance to help with
        troubleshooting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_console_screenshot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_console_screenshot)
        """

    async def get_default_credit_specification(
        self, **kwargs: Unpack[GetDefaultCreditSpecificationRequestRequestTypeDef]
    ) -> GetDefaultCreditSpecificationResultTypeDef:
        """
        Describes the default credit option for CPU usage of a burstable performance
        instance family.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_default_credit_specification.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_default_credit_specification)
        """

    async def get_ebs_default_kms_key_id(
        self, **kwargs: Unpack[GetEbsDefaultKmsKeyIdRequestRequestTypeDef]
    ) -> GetEbsDefaultKmsKeyIdResultTypeDef:
        """
        Describes the default KMS key for EBS encryption by default for your account in
        this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_ebs_default_kms_key_id.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_ebs_default_kms_key_id)
        """

    async def get_ebs_encryption_by_default(
        self, **kwargs: Unpack[GetEbsEncryptionByDefaultRequestRequestTypeDef]
    ) -> GetEbsEncryptionByDefaultResultTypeDef:
        """
        Describes whether EBS encryption by default is enabled for your account in the
        current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_ebs_encryption_by_default.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_ebs_encryption_by_default)
        """

    async def get_flow_logs_integration_template(
        self, **kwargs: Unpack[GetFlowLogsIntegrationTemplateRequestRequestTypeDef]
    ) -> GetFlowLogsIntegrationTemplateResultTypeDef:
        """
        Generates a CloudFormation template that streamlines and automates the
        integration of VPC flow logs with Amazon Athena.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_flow_logs_integration_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_flow_logs_integration_template)
        """

    async def get_groups_for_capacity_reservation(
        self, **kwargs: Unpack[GetGroupsForCapacityReservationRequestRequestTypeDef]
    ) -> GetGroupsForCapacityReservationResultTypeDef:
        """
        Lists the resource groups to which a Capacity Reservation has been added.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_groups_for_capacity_reservation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_groups_for_capacity_reservation)
        """

    async def get_host_reservation_purchase_preview(
        self, **kwargs: Unpack[GetHostReservationPurchasePreviewRequestRequestTypeDef]
    ) -> GetHostReservationPurchasePreviewResultTypeDef:
        """
        Preview a reservation purchase with configurations that match those of your
        Dedicated Host.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_host_reservation_purchase_preview.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_host_reservation_purchase_preview)
        """

    async def get_image_block_public_access_state(
        self, **kwargs: Unpack[GetImageBlockPublicAccessStateRequestRequestTypeDef]
    ) -> GetImageBlockPublicAccessStateResultTypeDef:
        """
        Gets the current state of <i>block public access for AMIs</i> at the account
        level in the specified Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_image_block_public_access_state.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_image_block_public_access_state)
        """

    async def get_instance_metadata_defaults(
        self, **kwargs: Unpack[GetInstanceMetadataDefaultsRequestRequestTypeDef]
    ) -> GetInstanceMetadataDefaultsResultTypeDef:
        """
        Gets the default instance metadata service (IMDS) settings that are set at the
        account level in the specified Amazon Web Services&#x2028; Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_instance_metadata_defaults.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_instance_metadata_defaults)
        """

    async def get_instance_tpm_ek_pub(
        self, **kwargs: Unpack[GetInstanceTpmEkPubRequestRequestTypeDef]
    ) -> GetInstanceTpmEkPubResultTypeDef:
        """
        Gets the public endorsement key associated with the Nitro Trusted Platform
        Module (NitroTPM) for the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_instance_tpm_ek_pub.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_instance_tpm_ek_pub)
        """

    async def get_instance_types_from_instance_requirements(
        self, **kwargs: Unpack[GetInstanceTypesFromInstanceRequirementsRequestRequestTypeDef]
    ) -> GetInstanceTypesFromInstanceRequirementsResultTypeDef:
        """
        Returns a list of instance types with the specified instance attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_instance_types_from_instance_requirements.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_instance_types_from_instance_requirements)
        """

    async def get_instance_uefi_data(
        self, **kwargs: Unpack[GetInstanceUefiDataRequestRequestTypeDef]
    ) -> GetInstanceUefiDataResultTypeDef:
        """
        A binary representation of the UEFI variable store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_instance_uefi_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_instance_uefi_data)
        """

    async def get_ipam_address_history(
        self, **kwargs: Unpack[GetIpamAddressHistoryRequestRequestTypeDef]
    ) -> GetIpamAddressHistoryResultTypeDef:
        """
        Retrieve historical information about a CIDR within an IPAM scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_ipam_address_history.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_ipam_address_history)
        """

    async def get_ipam_discovered_accounts(
        self, **kwargs: Unpack[GetIpamDiscoveredAccountsRequestRequestTypeDef]
    ) -> GetIpamDiscoveredAccountsResultTypeDef:
        """
        Gets IPAM discovered accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_ipam_discovered_accounts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_ipam_discovered_accounts)
        """

    async def get_ipam_discovered_public_addresses(
        self, **kwargs: Unpack[GetIpamDiscoveredPublicAddressesRequestRequestTypeDef]
    ) -> GetIpamDiscoveredPublicAddressesResultTypeDef:
        """
        Gets the public IP addresses that have been discovered by IPAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_ipam_discovered_public_addresses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_ipam_discovered_public_addresses)
        """

    async def get_ipam_discovered_resource_cidrs(
        self, **kwargs: Unpack[GetIpamDiscoveredResourceCidrsRequestRequestTypeDef]
    ) -> GetIpamDiscoveredResourceCidrsResultTypeDef:
        """
        Returns the resource CIDRs that are monitored as part of a resource discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_ipam_discovered_resource_cidrs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_ipam_discovered_resource_cidrs)
        """

    async def get_ipam_pool_allocations(
        self, **kwargs: Unpack[GetIpamPoolAllocationsRequestRequestTypeDef]
    ) -> GetIpamPoolAllocationsResultTypeDef:
        """
        Get a list of all the CIDR allocations in an IPAM pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_ipam_pool_allocations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_ipam_pool_allocations)
        """

    async def get_ipam_pool_cidrs(
        self, **kwargs: Unpack[GetIpamPoolCidrsRequestRequestTypeDef]
    ) -> GetIpamPoolCidrsResultTypeDef:
        """
        Get the CIDRs provisioned to an IPAM pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_ipam_pool_cidrs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_ipam_pool_cidrs)
        """

    async def get_ipam_resource_cidrs(
        self, **kwargs: Unpack[GetIpamResourceCidrsRequestRequestTypeDef]
    ) -> GetIpamResourceCidrsResultTypeDef:
        """
        Returns resource CIDRs managed by IPAM in a given scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_ipam_resource_cidrs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_ipam_resource_cidrs)
        """

    async def get_launch_template_data(
        self, **kwargs: Unpack[GetLaunchTemplateDataRequestRequestTypeDef]
    ) -> GetLaunchTemplateDataResultTypeDef:
        """
        Retrieves the configuration data of the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_launch_template_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_launch_template_data)
        """

    async def get_managed_prefix_list_associations(
        self, **kwargs: Unpack[GetManagedPrefixListAssociationsRequestRequestTypeDef]
    ) -> GetManagedPrefixListAssociationsResultTypeDef:
        """
        Gets information about the resources that are associated with the specified
        managed prefix list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_managed_prefix_list_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_managed_prefix_list_associations)
        """

    async def get_managed_prefix_list_entries(
        self, **kwargs: Unpack[GetManagedPrefixListEntriesRequestRequestTypeDef]
    ) -> GetManagedPrefixListEntriesResultTypeDef:
        """
        Gets information about the entries for a specified managed prefix list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_managed_prefix_list_entries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_managed_prefix_list_entries)
        """

    async def get_network_insights_access_scope_analysis_findings(
        self, **kwargs: Unpack[GetNetworkInsightsAccessScopeAnalysisFindingsRequestRequestTypeDef]
    ) -> GetNetworkInsightsAccessScopeAnalysisFindingsResultTypeDef:
        """
        Gets the findings for the specified Network Access Scope analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_network_insights_access_scope_analysis_findings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_network_insights_access_scope_analysis_findings)
        """

    async def get_network_insights_access_scope_content(
        self, **kwargs: Unpack[GetNetworkInsightsAccessScopeContentRequestRequestTypeDef]
    ) -> GetNetworkInsightsAccessScopeContentResultTypeDef:
        """
        Gets the content for the specified Network Access Scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_network_insights_access_scope_content.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_network_insights_access_scope_content)
        """

    async def get_password_data(
        self, **kwargs: Unpack[GetPasswordDataRequestRequestTypeDef]
    ) -> GetPasswordDataResultTypeDef:
        """
        Retrieves the encrypted administrator password for a running Windows instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_password_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_password_data)
        """

    async def get_reserved_instances_exchange_quote(
        self, **kwargs: Unpack[GetReservedInstancesExchangeQuoteRequestRequestTypeDef]
    ) -> GetReservedInstancesExchangeQuoteResultTypeDef:
        """
        Returns a quote and exchange information for exchanging one or more specified
        Convertible Reserved Instances for a new Convertible Reserved Instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_reserved_instances_exchange_quote.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_reserved_instances_exchange_quote)
        """

    async def get_security_groups_for_vpc(
        self, **kwargs: Unpack[GetSecurityGroupsForVpcRequestRequestTypeDef]
    ) -> GetSecurityGroupsForVpcResultTypeDef:
        """
        Gets security groups that can be associated by the Amazon Web Services account
        making the request with network interfaces in the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_security_groups_for_vpc.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_security_groups_for_vpc)
        """

    async def get_serial_console_access_status(
        self, **kwargs: Unpack[GetSerialConsoleAccessStatusRequestRequestTypeDef]
    ) -> GetSerialConsoleAccessStatusResultTypeDef:
        """
        Retrieves the access status of your account to the EC2 serial console of all
        instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_serial_console_access_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_serial_console_access_status)
        """

    async def get_snapshot_block_public_access_state(
        self, **kwargs: Unpack[GetSnapshotBlockPublicAccessStateRequestRequestTypeDef]
    ) -> GetSnapshotBlockPublicAccessStateResultTypeDef:
        """
        Gets the current state of <i>block public access for snapshots</i> setting for
        the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_snapshot_block_public_access_state.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_snapshot_block_public_access_state)
        """

    async def get_spot_placement_scores(
        self, **kwargs: Unpack[GetSpotPlacementScoresRequestRequestTypeDef]
    ) -> GetSpotPlacementScoresResultTypeDef:
        """
        Calculates the Spot placement score for a Region or Availability Zone based on
        the specified target capacity and compute requirements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_spot_placement_scores.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_spot_placement_scores)
        """

    async def get_subnet_cidr_reservations(
        self, **kwargs: Unpack[GetSubnetCidrReservationsRequestRequestTypeDef]
    ) -> GetSubnetCidrReservationsResultTypeDef:
        """
        Gets information about the subnet CIDR reservations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_subnet_cidr_reservations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_subnet_cidr_reservations)
        """

    async def get_transit_gateway_attachment_propagations(
        self, **kwargs: Unpack[GetTransitGatewayAttachmentPropagationsRequestRequestTypeDef]
    ) -> GetTransitGatewayAttachmentPropagationsResultTypeDef:
        """
        Lists the route tables to which the specified resource attachment propagates
        routes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_transit_gateway_attachment_propagations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_transit_gateway_attachment_propagations)
        """

    async def get_transit_gateway_multicast_domain_associations(
        self, **kwargs: Unpack[GetTransitGatewayMulticastDomainAssociationsRequestRequestTypeDef]
    ) -> GetTransitGatewayMulticastDomainAssociationsResultTypeDef:
        """
        Gets information about the associations for the transit gateway multicast
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_transit_gateway_multicast_domain_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_transit_gateway_multicast_domain_associations)
        """

    async def get_transit_gateway_policy_table_associations(
        self, **kwargs: Unpack[GetTransitGatewayPolicyTableAssociationsRequestRequestTypeDef]
    ) -> GetTransitGatewayPolicyTableAssociationsResultTypeDef:
        """
        Gets a list of the transit gateway policy table associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_transit_gateway_policy_table_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_transit_gateway_policy_table_associations)
        """

    async def get_transit_gateway_policy_table_entries(
        self, **kwargs: Unpack[GetTransitGatewayPolicyTableEntriesRequestRequestTypeDef]
    ) -> GetTransitGatewayPolicyTableEntriesResultTypeDef:
        """
        Returns a list of transit gateway policy table entries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_transit_gateway_policy_table_entries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_transit_gateway_policy_table_entries)
        """

    async def get_transit_gateway_prefix_list_references(
        self, **kwargs: Unpack[GetTransitGatewayPrefixListReferencesRequestRequestTypeDef]
    ) -> GetTransitGatewayPrefixListReferencesResultTypeDef:
        """
        Gets information about the prefix list references in a specified transit
        gateway route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_transit_gateway_prefix_list_references.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_transit_gateway_prefix_list_references)
        """

    async def get_transit_gateway_route_table_associations(
        self, **kwargs: Unpack[GetTransitGatewayRouteTableAssociationsRequestRequestTypeDef]
    ) -> GetTransitGatewayRouteTableAssociationsResultTypeDef:
        """
        Gets information about the associations for the specified transit gateway route
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_transit_gateway_route_table_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_transit_gateway_route_table_associations)
        """

    async def get_transit_gateway_route_table_propagations(
        self, **kwargs: Unpack[GetTransitGatewayRouteTablePropagationsRequestRequestTypeDef]
    ) -> GetTransitGatewayRouteTablePropagationsResultTypeDef:
        """
        Gets information about the route table propagations for the specified transit
        gateway route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_transit_gateway_route_table_propagations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_transit_gateway_route_table_propagations)
        """

    async def get_verified_access_endpoint_policy(
        self, **kwargs: Unpack[GetVerifiedAccessEndpointPolicyRequestRequestTypeDef]
    ) -> GetVerifiedAccessEndpointPolicyResultTypeDef:
        """
        Get the Verified Access policy associated with the endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_verified_access_endpoint_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_verified_access_endpoint_policy)
        """

    async def get_verified_access_group_policy(
        self, **kwargs: Unpack[GetVerifiedAccessGroupPolicyRequestRequestTypeDef]
    ) -> GetVerifiedAccessGroupPolicyResultTypeDef:
        """
        Shows the contents of the Verified Access policy associated with the group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_verified_access_group_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_verified_access_group_policy)
        """

    async def get_vpn_connection_device_sample_configuration(
        self, **kwargs: Unpack[GetVpnConnectionDeviceSampleConfigurationRequestRequestTypeDef]
    ) -> GetVpnConnectionDeviceSampleConfigurationResultTypeDef:
        """
        Download an Amazon Web Services-provided sample configuration file to be used
        with the customer gateway device specified for your Site-to-Site VPN
        connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_vpn_connection_device_sample_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_vpn_connection_device_sample_configuration)
        """

    async def get_vpn_connection_device_types(
        self, **kwargs: Unpack[GetVpnConnectionDeviceTypesRequestRequestTypeDef]
    ) -> GetVpnConnectionDeviceTypesResultTypeDef:
        """
        Obtain a list of customer gateway devices for which sample configuration files
        can be provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_vpn_connection_device_types.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_vpn_connection_device_types)
        """

    async def get_vpn_tunnel_replacement_status(
        self, **kwargs: Unpack[GetVpnTunnelReplacementStatusRequestRequestTypeDef]
    ) -> GetVpnTunnelReplacementStatusResultTypeDef:
        """
        Get details of available tunnel endpoint maintenance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_vpn_tunnel_replacement_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_vpn_tunnel_replacement_status)
        """

    async def import_client_vpn_client_certificate_revocation_list(
        self, **kwargs: Unpack[ImportClientVpnClientCertificateRevocationListRequestRequestTypeDef]
    ) -> ImportClientVpnClientCertificateRevocationListResultTypeDef:
        """
        Uploads a client certificate revocation list to the specified Client VPN
        endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/import_client_vpn_client_certificate_revocation_list.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#import_client_vpn_client_certificate_revocation_list)
        """

    async def import_image(
        self, **kwargs: Unpack[ImportImageRequestRequestTypeDef]
    ) -> ImportImageResultTypeDef:
        """
        To import your virtual machines (VMs) with a console-based experience, you can
        use the <i>Import virtual machine images to Amazon Web Services</i> template in
        the <a
        href="https://console.aws.amazon.com/migrationhub/orchestrator">Migration Hub
        Orchestrator console</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/import_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#import_image)
        """

    async def import_instance(
        self, **kwargs: Unpack[ImportInstanceRequestRequestTypeDef]
    ) -> ImportInstanceResultTypeDef:
        """
        We recommend that you use the <a
        href="https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ImportImage.html">
        <code>ImportImage</code> </a> API instead.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/import_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#import_instance)
        """

    async def import_key_pair(
        self, **kwargs: Unpack[ImportKeyPairRequestRequestTypeDef]
    ) -> ImportKeyPairResultTypeDef:
        """
        Imports the public key from an RSA or ED25519 key pair that you created with a
        third-party tool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/import_key_pair.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#import_key_pair)
        """

    async def import_snapshot(
        self, **kwargs: Unpack[ImportSnapshotRequestRequestTypeDef]
    ) -> ImportSnapshotResultTypeDef:
        """
        Imports a disk into an EBS snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/import_snapshot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#import_snapshot)
        """

    async def import_volume(
        self, **kwargs: Unpack[ImportVolumeRequestRequestTypeDef]
    ) -> ImportVolumeResultTypeDef:
        """
        This API action supports only single-volume VMs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/import_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#import_volume)
        """

    async def list_images_in_recycle_bin(
        self, **kwargs: Unpack[ListImagesInRecycleBinRequestRequestTypeDef]
    ) -> ListImagesInRecycleBinResultTypeDef:
        """
        Lists one or more AMIs that are currently in the Recycle Bin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/list_images_in_recycle_bin.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#list_images_in_recycle_bin)
        """

    async def list_snapshots_in_recycle_bin(
        self, **kwargs: Unpack[ListSnapshotsInRecycleBinRequestRequestTypeDef]
    ) -> ListSnapshotsInRecycleBinResultTypeDef:
        """
        Lists one or more snapshots that are currently in the Recycle Bin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/list_snapshots_in_recycle_bin.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#list_snapshots_in_recycle_bin)
        """

    async def lock_snapshot(
        self, **kwargs: Unpack[LockSnapshotRequestRequestTypeDef]
    ) -> LockSnapshotResultTypeDef:
        """
        Locks an Amazon EBS snapshot in either <i>governance</i> or <i>compliance</i>
        mode to protect it against accidental or malicious deletions for a specific
        duration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/lock_snapshot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#lock_snapshot)
        """

    async def modify_address_attribute(
        self, **kwargs: Unpack[ModifyAddressAttributeRequestRequestTypeDef]
    ) -> ModifyAddressAttributeResultTypeDef:
        """
        Modifies an attribute of the specified Elastic IP address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_address_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_address_attribute)
        """

    async def modify_availability_zone_group(
        self, **kwargs: Unpack[ModifyAvailabilityZoneGroupRequestRequestTypeDef]
    ) -> ModifyAvailabilityZoneGroupResultTypeDef:
        """
        Changes the opt-in status of the specified zone group for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_availability_zone_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_availability_zone_group)
        """

    async def modify_capacity_reservation(
        self, **kwargs: Unpack[ModifyCapacityReservationRequestRequestTypeDef]
    ) -> ModifyCapacityReservationResultTypeDef:
        """
        Modifies a Capacity Reservation's capacity, instance eligibility, and the
        conditions under which it is to be released.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_capacity_reservation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_capacity_reservation)
        """

    async def modify_capacity_reservation_fleet(
        self, **kwargs: Unpack[ModifyCapacityReservationFleetRequestRequestTypeDef]
    ) -> ModifyCapacityReservationFleetResultTypeDef:
        """
        Modifies a Capacity Reservation Fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_capacity_reservation_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_capacity_reservation_fleet)
        """

    async def modify_client_vpn_endpoint(
        self, **kwargs: Unpack[ModifyClientVpnEndpointRequestRequestTypeDef]
    ) -> ModifyClientVpnEndpointResultTypeDef:
        """
        Modifies the specified Client VPN endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_client_vpn_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_client_vpn_endpoint)
        """

    async def modify_default_credit_specification(
        self, **kwargs: Unpack[ModifyDefaultCreditSpecificationRequestRequestTypeDef]
    ) -> ModifyDefaultCreditSpecificationResultTypeDef:
        """
        Modifies the default credit option for CPU usage of burstable performance
        instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_default_credit_specification.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_default_credit_specification)
        """

    async def modify_ebs_default_kms_key_id(
        self, **kwargs: Unpack[ModifyEbsDefaultKmsKeyIdRequestRequestTypeDef]
    ) -> ModifyEbsDefaultKmsKeyIdResultTypeDef:
        """
        Changes the default KMS key for EBS encryption by default for your account in
        this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_ebs_default_kms_key_id.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_ebs_default_kms_key_id)
        """

    async def modify_fleet(
        self, **kwargs: Unpack[ModifyFleetRequestRequestTypeDef]
    ) -> ModifyFleetResultTypeDef:
        """
        Modifies the specified EC2 Fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_fleet)
        """

    async def modify_fpga_image_attribute(
        self, **kwargs: Unpack[ModifyFpgaImageAttributeRequestRequestTypeDef]
    ) -> ModifyFpgaImageAttributeResultTypeDef:
        """
        Modifies the specified attribute of the specified Amazon FPGA Image (AFI).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_fpga_image_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_fpga_image_attribute)
        """

    async def modify_hosts(
        self, **kwargs: Unpack[ModifyHostsRequestRequestTypeDef]
    ) -> ModifyHostsResultTypeDef:
        """
        Modify the auto-placement setting of a Dedicated Host.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_hosts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_hosts)
        """

    async def modify_id_format(
        self, **kwargs: Unpack[ModifyIdFormatRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies the ID format for the specified resource on a per-Region basis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_id_format.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_id_format)
        """

    async def modify_identity_id_format(
        self, **kwargs: Unpack[ModifyIdentityIdFormatRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies the ID format of a resource for a specified IAM user, IAM role, or the
        root user for an account; or all IAM users, IAM roles, and the root user for an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_identity_id_format.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_identity_id_format)
        """

    async def modify_image_attribute(
        self, **kwargs: Unpack[ModifyImageAttributeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies the specified attribute of the specified AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_image_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_image_attribute)
        """

    async def modify_instance_attribute(
        self, **kwargs: Unpack[ModifyInstanceAttributeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies the specified attribute of the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_instance_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_instance_attribute)
        """

    async def modify_instance_capacity_reservation_attributes(
        self, **kwargs: Unpack[ModifyInstanceCapacityReservationAttributesRequestRequestTypeDef]
    ) -> ModifyInstanceCapacityReservationAttributesResultTypeDef:
        """
        Modifies the Capacity Reservation settings for a stopped instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_instance_capacity_reservation_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_instance_capacity_reservation_attributes)
        """

    async def modify_instance_cpu_options(
        self, **kwargs: Unpack[ModifyInstanceCpuOptionsRequestRequestTypeDef]
    ) -> ModifyInstanceCpuOptionsResultTypeDef:
        """
        By default, all vCPUs for the instance type are active when you launch an
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_instance_cpu_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_instance_cpu_options)
        """

    async def modify_instance_credit_specification(
        self, **kwargs: Unpack[ModifyInstanceCreditSpecificationRequestRequestTypeDef]
    ) -> ModifyInstanceCreditSpecificationResultTypeDef:
        """
        Modifies the credit option for CPU usage on a running or stopped burstable
        performance instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_instance_credit_specification.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_instance_credit_specification)
        """

    async def modify_instance_event_start_time(
        self, **kwargs: Unpack[ModifyInstanceEventStartTimeRequestRequestTypeDef]
    ) -> ModifyInstanceEventStartTimeResultTypeDef:
        """
        Modifies the start time for a scheduled Amazon EC2 instance event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_instance_event_start_time.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_instance_event_start_time)
        """

    async def modify_instance_event_window(
        self, **kwargs: Unpack[ModifyInstanceEventWindowRequestRequestTypeDef]
    ) -> ModifyInstanceEventWindowResultTypeDef:
        """
        Modifies the specified event window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_instance_event_window.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_instance_event_window)
        """

    async def modify_instance_maintenance_options(
        self, **kwargs: Unpack[ModifyInstanceMaintenanceOptionsRequestRequestTypeDef]
    ) -> ModifyInstanceMaintenanceOptionsResultTypeDef:
        """
        Modifies the recovery behavior of your instance to disable simplified automatic
        recovery or set the recovery behavior to default.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_instance_maintenance_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_instance_maintenance_options)
        """

    async def modify_instance_metadata_defaults(
        self, **kwargs: Unpack[ModifyInstanceMetadataDefaultsRequestRequestTypeDef]
    ) -> ModifyInstanceMetadataDefaultsResultTypeDef:
        """
        Modifies the default instance metadata service (IMDS) settings at the account
        level in the specified Amazon Web Services&#x2028; Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_instance_metadata_defaults.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_instance_metadata_defaults)
        """

    async def modify_instance_metadata_options(
        self, **kwargs: Unpack[ModifyInstanceMetadataOptionsRequestRequestTypeDef]
    ) -> ModifyInstanceMetadataOptionsResultTypeDef:
        """
        Modify the instance metadata parameters on a running or stopped instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_instance_metadata_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_instance_metadata_options)
        """

    async def modify_instance_placement(
        self, **kwargs: Unpack[ModifyInstancePlacementRequestRequestTypeDef]
    ) -> ModifyInstancePlacementResultTypeDef:
        """
        Modifies the placement attributes for a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_instance_placement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_instance_placement)
        """

    async def modify_ipam(
        self, **kwargs: Unpack[ModifyIpamRequestRequestTypeDef]
    ) -> ModifyIpamResultTypeDef:
        """
        Modify the configurations of an IPAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_ipam.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_ipam)
        """

    async def modify_ipam_pool(
        self, **kwargs: Unpack[ModifyIpamPoolRequestRequestTypeDef]
    ) -> ModifyIpamPoolResultTypeDef:
        """
        Modify the configurations of an IPAM pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_ipam_pool.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_ipam_pool)
        """

    async def modify_ipam_resource_cidr(
        self, **kwargs: Unpack[ModifyIpamResourceCidrRequestRequestTypeDef]
    ) -> ModifyIpamResourceCidrResultTypeDef:
        """
        Modify a resource CIDR.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_ipam_resource_cidr.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_ipam_resource_cidr)
        """

    async def modify_ipam_resource_discovery(
        self, **kwargs: Unpack[ModifyIpamResourceDiscoveryRequestRequestTypeDef]
    ) -> ModifyIpamResourceDiscoveryResultTypeDef:
        """
        Modifies a resource discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_ipam_resource_discovery.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_ipam_resource_discovery)
        """

    async def modify_ipam_scope(
        self, **kwargs: Unpack[ModifyIpamScopeRequestRequestTypeDef]
    ) -> ModifyIpamScopeResultTypeDef:
        """
        Modify an IPAM scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_ipam_scope.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_ipam_scope)
        """

    async def modify_launch_template(
        self, **kwargs: Unpack[ModifyLaunchTemplateRequestRequestTypeDef]
    ) -> ModifyLaunchTemplateResultTypeDef:
        """
        Modifies a launch template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_launch_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_launch_template)
        """

    async def modify_local_gateway_route(
        self, **kwargs: Unpack[ModifyLocalGatewayRouteRequestRequestTypeDef]
    ) -> ModifyLocalGatewayRouteResultTypeDef:
        """
        Modifies the specified local gateway route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_local_gateway_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_local_gateway_route)
        """

    async def modify_managed_prefix_list(
        self, **kwargs: Unpack[ModifyManagedPrefixListRequestRequestTypeDef]
    ) -> ModifyManagedPrefixListResultTypeDef:
        """
        Modifies the specified managed prefix list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_managed_prefix_list.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_managed_prefix_list)
        """

    async def modify_network_interface_attribute(
        self, **kwargs: Unpack[ModifyNetworkInterfaceAttributeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies the specified network interface attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_network_interface_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_network_interface_attribute)
        """

    async def modify_private_dns_name_options(
        self, **kwargs: Unpack[ModifyPrivateDnsNameOptionsRequestRequestTypeDef]
    ) -> ModifyPrivateDnsNameOptionsResultTypeDef:
        """
        Modifies the options for instance hostnames for the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_private_dns_name_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_private_dns_name_options)
        """

    async def modify_reserved_instances(
        self, **kwargs: Unpack[ModifyReservedInstancesRequestRequestTypeDef]
    ) -> ModifyReservedInstancesResultTypeDef:
        """
        Modifies the configuration of your Reserved Instances, such as the Availability
        Zone, instance count, or instance type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_reserved_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_reserved_instances)
        """

    async def modify_security_group_rules(
        self, **kwargs: Unpack[ModifySecurityGroupRulesRequestRequestTypeDef]
    ) -> ModifySecurityGroupRulesResultTypeDef:
        """
        Modifies the rules of a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_security_group_rules.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_security_group_rules)
        """

    async def modify_snapshot_attribute(
        self, **kwargs: Unpack[ModifySnapshotAttributeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or removes permission settings for the specified snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_snapshot_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_snapshot_attribute)
        """

    async def modify_snapshot_tier(
        self, **kwargs: Unpack[ModifySnapshotTierRequestRequestTypeDef]
    ) -> ModifySnapshotTierResultTypeDef:
        """
        Archives an Amazon EBS snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_snapshot_tier.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_snapshot_tier)
        """

    async def modify_spot_fleet_request(
        self, **kwargs: Unpack[ModifySpotFleetRequestRequestRequestTypeDef]
    ) -> ModifySpotFleetRequestResponseTypeDef:
        """
        Modifies the specified Spot Fleet request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_spot_fleet_request.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_spot_fleet_request)
        """

    async def modify_subnet_attribute(
        self, **kwargs: Unpack[ModifySubnetAttributeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies a subnet attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_subnet_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_subnet_attribute)
        """

    async def modify_traffic_mirror_filter_network_services(
        self, **kwargs: Unpack[ModifyTrafficMirrorFilterNetworkServicesRequestRequestTypeDef]
    ) -> ModifyTrafficMirrorFilterNetworkServicesResultTypeDef:
        """
        Allows or restricts mirroring network services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_traffic_mirror_filter_network_services.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_traffic_mirror_filter_network_services)
        """

    async def modify_traffic_mirror_filter_rule(
        self, **kwargs: Unpack[ModifyTrafficMirrorFilterRuleRequestRequestTypeDef]
    ) -> ModifyTrafficMirrorFilterRuleResultTypeDef:
        """
        Modifies the specified Traffic Mirror rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_traffic_mirror_filter_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_traffic_mirror_filter_rule)
        """

    async def modify_traffic_mirror_session(
        self, **kwargs: Unpack[ModifyTrafficMirrorSessionRequestRequestTypeDef]
    ) -> ModifyTrafficMirrorSessionResultTypeDef:
        """
        Modifies a Traffic Mirror session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_traffic_mirror_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_traffic_mirror_session)
        """

    async def modify_transit_gateway(
        self, **kwargs: Unpack[ModifyTransitGatewayRequestRequestTypeDef]
    ) -> ModifyTransitGatewayResultTypeDef:
        """
        Modifies the specified transit gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_transit_gateway.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_transit_gateway)
        """

    async def modify_transit_gateway_prefix_list_reference(
        self, **kwargs: Unpack[ModifyTransitGatewayPrefixListReferenceRequestRequestTypeDef]
    ) -> ModifyTransitGatewayPrefixListReferenceResultTypeDef:
        """
        Modifies a reference (route) to a prefix list in a specified transit gateway
        route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_transit_gateway_prefix_list_reference.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_transit_gateway_prefix_list_reference)
        """

    async def modify_transit_gateway_vpc_attachment(
        self, **kwargs: Unpack[ModifyTransitGatewayVpcAttachmentRequestRequestTypeDef]
    ) -> ModifyTransitGatewayVpcAttachmentResultTypeDef:
        """
        Modifies the specified VPC attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_transit_gateway_vpc_attachment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_transit_gateway_vpc_attachment)
        """

    async def modify_verified_access_endpoint(
        self, **kwargs: Unpack[ModifyVerifiedAccessEndpointRequestRequestTypeDef]
    ) -> ModifyVerifiedAccessEndpointResultTypeDef:
        """
        Modifies the configuration of the specified Amazon Web Services Verified Access
        endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_verified_access_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_verified_access_endpoint)
        """

    async def modify_verified_access_endpoint_policy(
        self, **kwargs: Unpack[ModifyVerifiedAccessEndpointPolicyRequestRequestTypeDef]
    ) -> ModifyVerifiedAccessEndpointPolicyResultTypeDef:
        """
        Modifies the specified Amazon Web Services Verified Access endpoint policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_verified_access_endpoint_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_verified_access_endpoint_policy)
        """

    async def modify_verified_access_group(
        self, **kwargs: Unpack[ModifyVerifiedAccessGroupRequestRequestTypeDef]
    ) -> ModifyVerifiedAccessGroupResultTypeDef:
        """
        Modifies the specified Amazon Web Services Verified Access group configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_verified_access_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_verified_access_group)
        """

    async def modify_verified_access_group_policy(
        self, **kwargs: Unpack[ModifyVerifiedAccessGroupPolicyRequestRequestTypeDef]
    ) -> ModifyVerifiedAccessGroupPolicyResultTypeDef:
        """
        Modifies the specified Amazon Web Services Verified Access group policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_verified_access_group_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_verified_access_group_policy)
        """

    async def modify_verified_access_instance(
        self, **kwargs: Unpack[ModifyVerifiedAccessInstanceRequestRequestTypeDef]
    ) -> ModifyVerifiedAccessInstanceResultTypeDef:
        """
        Modifies the configuration of the specified Amazon Web Services Verified Access
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_verified_access_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_verified_access_instance)
        """

    async def modify_verified_access_instance_logging_configuration(
        self,
        **kwargs: Unpack[ModifyVerifiedAccessInstanceLoggingConfigurationRequestRequestTypeDef],
    ) -> ModifyVerifiedAccessInstanceLoggingConfigurationResultTypeDef:
        """
        Modifies the logging configuration for the specified Amazon Web Services
        Verified Access instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_verified_access_instance_logging_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_verified_access_instance_logging_configuration)
        """

    async def modify_verified_access_trust_provider(
        self, **kwargs: Unpack[ModifyVerifiedAccessTrustProviderRequestRequestTypeDef]
    ) -> ModifyVerifiedAccessTrustProviderResultTypeDef:
        """
        Modifies the configuration of the specified Amazon Web Services Verified Access
        trust provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_verified_access_trust_provider.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_verified_access_trust_provider)
        """

    async def modify_volume(
        self, **kwargs: Unpack[ModifyVolumeRequestRequestTypeDef]
    ) -> ModifyVolumeResultTypeDef:
        """
        You can modify several parameters of an existing EBS volume, including volume
        size, volume type, and IOPS capacity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_volume)
        """

    async def modify_volume_attribute(
        self, **kwargs: Unpack[ModifyVolumeAttributeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies a volume attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_volume_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_volume_attribute)
        """

    async def modify_vpc_attribute(
        self, **kwargs: Unpack[ModifyVpcAttributeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies the specified attribute of the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_vpc_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_vpc_attribute)
        """

    async def modify_vpc_endpoint(
        self, **kwargs: Unpack[ModifyVpcEndpointRequestRequestTypeDef]
    ) -> ModifyVpcEndpointResultTypeDef:
        """
        Modifies attributes of a specified VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_vpc_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_vpc_endpoint)
        """

    async def modify_vpc_endpoint_connection_notification(
        self, **kwargs: Unpack[ModifyVpcEndpointConnectionNotificationRequestRequestTypeDef]
    ) -> ModifyVpcEndpointConnectionNotificationResultTypeDef:
        """
        Modifies a connection notification for VPC endpoint or VPC endpoint service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_vpc_endpoint_connection_notification.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_vpc_endpoint_connection_notification)
        """

    async def modify_vpc_endpoint_service_configuration(
        self, **kwargs: Unpack[ModifyVpcEndpointServiceConfigurationRequestRequestTypeDef]
    ) -> ModifyVpcEndpointServiceConfigurationResultTypeDef:
        """
        Modifies the attributes of your VPC endpoint service configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_vpc_endpoint_service_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_vpc_endpoint_service_configuration)
        """

    async def modify_vpc_endpoint_service_payer_responsibility(
        self, **kwargs: Unpack[ModifyVpcEndpointServicePayerResponsibilityRequestRequestTypeDef]
    ) -> ModifyVpcEndpointServicePayerResponsibilityResultTypeDef:
        """
        Modifies the payer responsibility for your VPC endpoint service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_vpc_endpoint_service_payer_responsibility.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_vpc_endpoint_service_payer_responsibility)
        """

    async def modify_vpc_endpoint_service_permissions(
        self, **kwargs: Unpack[ModifyVpcEndpointServicePermissionsRequestRequestTypeDef]
    ) -> ModifyVpcEndpointServicePermissionsResultTypeDef:
        """
        Modifies the permissions for your VPC endpoint service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_vpc_endpoint_service_permissions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_vpc_endpoint_service_permissions)
        """

    async def modify_vpc_peering_connection_options(
        self, **kwargs: Unpack[ModifyVpcPeeringConnectionOptionsRequestRequestTypeDef]
    ) -> ModifyVpcPeeringConnectionOptionsResultTypeDef:
        """
        Modifies the VPC peering connection options on one side of a VPC peering
        connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_vpc_peering_connection_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_vpc_peering_connection_options)
        """

    async def modify_vpc_tenancy(
        self, **kwargs: Unpack[ModifyVpcTenancyRequestRequestTypeDef]
    ) -> ModifyVpcTenancyResultTypeDef:
        """
        Modifies the instance tenancy attribute of the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_vpc_tenancy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_vpc_tenancy)
        """

    async def modify_vpn_connection(
        self, **kwargs: Unpack[ModifyVpnConnectionRequestRequestTypeDef]
    ) -> ModifyVpnConnectionResultTypeDef:
        """
        Modifies the customer gateway or the target gateway of an Amazon Web Services
        Site-to-Site VPN connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_vpn_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_vpn_connection)
        """

    async def modify_vpn_connection_options(
        self, **kwargs: Unpack[ModifyVpnConnectionOptionsRequestRequestTypeDef]
    ) -> ModifyVpnConnectionOptionsResultTypeDef:
        """
        Modifies the connection options for your Site-to-Site VPN connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_vpn_connection_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_vpn_connection_options)
        """

    async def modify_vpn_tunnel_certificate(
        self, **kwargs: Unpack[ModifyVpnTunnelCertificateRequestRequestTypeDef]
    ) -> ModifyVpnTunnelCertificateResultTypeDef:
        """
        Modifies the VPN tunnel endpoint certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_vpn_tunnel_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_vpn_tunnel_certificate)
        """

    async def modify_vpn_tunnel_options(
        self, **kwargs: Unpack[ModifyVpnTunnelOptionsRequestRequestTypeDef]
    ) -> ModifyVpnTunnelOptionsResultTypeDef:
        """
        Modifies the options for a VPN tunnel in an Amazon Web Services Site-to-Site
        VPN connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/modify_vpn_tunnel_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#modify_vpn_tunnel_options)
        """

    async def monitor_instances(
        self, **kwargs: Unpack[MonitorInstancesRequestRequestTypeDef]
    ) -> MonitorInstancesResultTypeDef:
        """
        Enables detailed monitoring for a running instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/monitor_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#monitor_instances)
        """

    async def move_address_to_vpc(
        self, **kwargs: Unpack[MoveAddressToVpcRequestRequestTypeDef]
    ) -> MoveAddressToVpcResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/move_address_to_vpc.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#move_address_to_vpc)
        """

    async def move_byoip_cidr_to_ipam(
        self, **kwargs: Unpack[MoveByoipCidrToIpamRequestRequestTypeDef]
    ) -> MoveByoipCidrToIpamResultTypeDef:
        """
        Move a BYOIPv4 CIDR to IPAM from a public IPv4 pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/move_byoip_cidr_to_ipam.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#move_byoip_cidr_to_ipam)
        """

    async def move_capacity_reservation_instances(
        self, **kwargs: Unpack[MoveCapacityReservationInstancesRequestRequestTypeDef]
    ) -> MoveCapacityReservationInstancesResultTypeDef:
        """
        Move available capacity from a source Capacity Reservation to a destination
        Capacity Reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/move_capacity_reservation_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#move_capacity_reservation_instances)
        """

    async def provision_byoip_cidr(
        self, **kwargs: Unpack[ProvisionByoipCidrRequestRequestTypeDef]
    ) -> ProvisionByoipCidrResultTypeDef:
        """
        Provisions an IPv4 or IPv6 address range for use with your Amazon Web Services
        resources through bring your own IP addresses (BYOIP) and creates a
        corresponding address pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/provision_byoip_cidr.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#provision_byoip_cidr)
        """

    async def provision_ipam_byoasn(
        self, **kwargs: Unpack[ProvisionIpamByoasnRequestRequestTypeDef]
    ) -> ProvisionIpamByoasnResultTypeDef:
        """
        Provisions your Autonomous System Number (ASN) for use in your Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/provision_ipam_byoasn.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#provision_ipam_byoasn)
        """

    async def provision_ipam_pool_cidr(
        self, **kwargs: Unpack[ProvisionIpamPoolCidrRequestRequestTypeDef]
    ) -> ProvisionIpamPoolCidrResultTypeDef:
        """
        Provision a CIDR to an IPAM pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/provision_ipam_pool_cidr.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#provision_ipam_pool_cidr)
        """

    async def provision_public_ipv4_pool_cidr(
        self, **kwargs: Unpack[ProvisionPublicIpv4PoolCidrRequestRequestTypeDef]
    ) -> ProvisionPublicIpv4PoolCidrResultTypeDef:
        """
        Provision a CIDR to a public IPv4 pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/provision_public_ipv4_pool_cidr.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#provision_public_ipv4_pool_cidr)
        """

    async def purchase_capacity_block(
        self, **kwargs: Unpack[PurchaseCapacityBlockRequestRequestTypeDef]
    ) -> PurchaseCapacityBlockResultTypeDef:
        """
        Purchase the Capacity Block for use with your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/purchase_capacity_block.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#purchase_capacity_block)
        """

    async def purchase_host_reservation(
        self, **kwargs: Unpack[PurchaseHostReservationRequestRequestTypeDef]
    ) -> PurchaseHostReservationResultTypeDef:
        """
        Purchase a reservation with configurations that match those of your Dedicated
        Host.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/purchase_host_reservation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#purchase_host_reservation)
        """

    async def purchase_reserved_instances_offering(
        self, **kwargs: Unpack[PurchaseReservedInstancesOfferingRequestRequestTypeDef]
    ) -> PurchaseReservedInstancesOfferingResultTypeDef:
        """
        Purchases a Reserved Instance for use with your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/purchase_reserved_instances_offering.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#purchase_reserved_instances_offering)
        """

    async def purchase_scheduled_instances(
        self, **kwargs: Unpack[PurchaseScheduledInstancesRequestRequestTypeDef]
    ) -> PurchaseScheduledInstancesResultTypeDef:
        """
        You can no longer purchase Scheduled Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/purchase_scheduled_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#purchase_scheduled_instances)
        """

    async def reboot_instances(
        self, **kwargs: Unpack[RebootInstancesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Requests a reboot of the specified instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/reboot_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#reboot_instances)
        """

    async def register_image(
        self, **kwargs: Unpack[RegisterImageRequestRequestTypeDef]
    ) -> RegisterImageResultTypeDef:
        """
        Registers an AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/register_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#register_image)
        """

    async def register_instance_event_notification_attributes(
        self, **kwargs: Unpack[RegisterInstanceEventNotificationAttributesRequestRequestTypeDef]
    ) -> RegisterInstanceEventNotificationAttributesResultTypeDef:
        """
        Registers a set of tag keys to include in scheduled event notifications for
        your resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/register_instance_event_notification_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#register_instance_event_notification_attributes)
        """

    async def register_transit_gateway_multicast_group_members(
        self, **kwargs: Unpack[RegisterTransitGatewayMulticastGroupMembersRequestRequestTypeDef]
    ) -> RegisterTransitGatewayMulticastGroupMembersResultTypeDef:
        """
        Registers members (network interfaces) with the transit gateway multicast group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/register_transit_gateway_multicast_group_members.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#register_transit_gateway_multicast_group_members)
        """

    async def register_transit_gateway_multicast_group_sources(
        self, **kwargs: Unpack[RegisterTransitGatewayMulticastGroupSourcesRequestRequestTypeDef]
    ) -> RegisterTransitGatewayMulticastGroupSourcesResultTypeDef:
        """
        Registers sources (network interfaces) with the specified transit gateway
        multicast group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/register_transit_gateway_multicast_group_sources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#register_transit_gateway_multicast_group_sources)
        """

    async def reject_transit_gateway_multicast_domain_associations(
        self, **kwargs: Unpack[RejectTransitGatewayMulticastDomainAssociationsRequestRequestTypeDef]
    ) -> RejectTransitGatewayMulticastDomainAssociationsResultTypeDef:
        """
        Rejects a request to associate cross-account subnets with a transit gateway
        multicast domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/reject_transit_gateway_multicast_domain_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#reject_transit_gateway_multicast_domain_associations)
        """

    async def reject_transit_gateway_peering_attachment(
        self, **kwargs: Unpack[RejectTransitGatewayPeeringAttachmentRequestRequestTypeDef]
    ) -> RejectTransitGatewayPeeringAttachmentResultTypeDef:
        """
        Rejects a transit gateway peering attachment request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/reject_transit_gateway_peering_attachment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#reject_transit_gateway_peering_attachment)
        """

    async def reject_transit_gateway_vpc_attachment(
        self, **kwargs: Unpack[RejectTransitGatewayVpcAttachmentRequestRequestTypeDef]
    ) -> RejectTransitGatewayVpcAttachmentResultTypeDef:
        """
        Rejects a request to attach a VPC to a transit gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/reject_transit_gateway_vpc_attachment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#reject_transit_gateway_vpc_attachment)
        """

    async def reject_vpc_endpoint_connections(
        self, **kwargs: Unpack[RejectVpcEndpointConnectionsRequestRequestTypeDef]
    ) -> RejectVpcEndpointConnectionsResultTypeDef:
        """
        Rejects VPC endpoint connection requests to your VPC endpoint service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/reject_vpc_endpoint_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#reject_vpc_endpoint_connections)
        """

    async def reject_vpc_peering_connection(
        self, **kwargs: Unpack[RejectVpcPeeringConnectionRequestRequestTypeDef]
    ) -> RejectVpcPeeringConnectionResultTypeDef:
        """
        Rejects a VPC peering connection request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/reject_vpc_peering_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#reject_vpc_peering_connection)
        """

    async def release_address(
        self, **kwargs: Unpack[ReleaseAddressRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Releases the specified Elastic IP address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/release_address.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#release_address)
        """

    async def release_hosts(
        self, **kwargs: Unpack[ReleaseHostsRequestRequestTypeDef]
    ) -> ReleaseHostsResultTypeDef:
        """
        When you no longer want to use an On-Demand Dedicated Host it can be released.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/release_hosts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#release_hosts)
        """

    async def release_ipam_pool_allocation(
        self, **kwargs: Unpack[ReleaseIpamPoolAllocationRequestRequestTypeDef]
    ) -> ReleaseIpamPoolAllocationResultTypeDef:
        """
        Release an allocation within an IPAM pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/release_ipam_pool_allocation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#release_ipam_pool_allocation)
        """

    async def replace_iam_instance_profile_association(
        self, **kwargs: Unpack[ReplaceIamInstanceProfileAssociationRequestRequestTypeDef]
    ) -> ReplaceIamInstanceProfileAssociationResultTypeDef:
        """
        Replaces an IAM instance profile for the specified running instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/replace_iam_instance_profile_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#replace_iam_instance_profile_association)
        """

    async def replace_network_acl_association(
        self, **kwargs: Unpack[ReplaceNetworkAclAssociationRequestRequestTypeDef]
    ) -> ReplaceNetworkAclAssociationResultTypeDef:
        """
        Changes which network ACL a subnet is associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/replace_network_acl_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#replace_network_acl_association)
        """

    async def replace_network_acl_entry(
        self, **kwargs: Unpack[ReplaceNetworkAclEntryRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Replaces an entry (rule) in a network ACL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/replace_network_acl_entry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#replace_network_acl_entry)
        """

    async def replace_route(
        self, **kwargs: Unpack[ReplaceRouteRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Replaces an existing route within a route table in a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/replace_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#replace_route)
        """

    async def replace_route_table_association(
        self, **kwargs: Unpack[ReplaceRouteTableAssociationRequestRequestTypeDef]
    ) -> ReplaceRouteTableAssociationResultTypeDef:
        """
        Changes the route table associated with a given subnet, internet gateway, or
        virtual private gateway in a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/replace_route_table_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#replace_route_table_association)
        """

    async def replace_transit_gateway_route(
        self, **kwargs: Unpack[ReplaceTransitGatewayRouteRequestRequestTypeDef]
    ) -> ReplaceTransitGatewayRouteResultTypeDef:
        """
        Replaces the specified route in the specified transit gateway route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/replace_transit_gateway_route.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#replace_transit_gateway_route)
        """

    async def replace_vpn_tunnel(
        self, **kwargs: Unpack[ReplaceVpnTunnelRequestRequestTypeDef]
    ) -> ReplaceVpnTunnelResultTypeDef:
        """
        Trigger replacement of specified VPN tunnel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/replace_vpn_tunnel.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#replace_vpn_tunnel)
        """

    async def report_instance_status(
        self, **kwargs: Unpack[ReportInstanceStatusRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Submits feedback about the status of an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/report_instance_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#report_instance_status)
        """

    async def request_spot_fleet(
        self, **kwargs: Unpack[RequestSpotFleetRequestRequestTypeDef]
    ) -> RequestSpotFleetResponseTypeDef:
        """
        Creates a Spot Fleet request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/request_spot_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#request_spot_fleet)
        """

    async def request_spot_instances(
        self, **kwargs: Unpack[RequestSpotInstancesRequestRequestTypeDef]
    ) -> RequestSpotInstancesResultTypeDef:
        """
        Creates a Spot Instance request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/request_spot_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#request_spot_instances)
        """

    async def reset_address_attribute(
        self, **kwargs: Unpack[ResetAddressAttributeRequestRequestTypeDef]
    ) -> ResetAddressAttributeResultTypeDef:
        """
        Resets the attribute of the specified IP address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/reset_address_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#reset_address_attribute)
        """

    async def reset_ebs_default_kms_key_id(
        self, **kwargs: Unpack[ResetEbsDefaultKmsKeyIdRequestRequestTypeDef]
    ) -> ResetEbsDefaultKmsKeyIdResultTypeDef:
        """
        Resets the default KMS key for EBS encryption for your account in this Region
        to the Amazon Web Services managed KMS key for EBS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/reset_ebs_default_kms_key_id.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#reset_ebs_default_kms_key_id)
        """

    async def reset_fpga_image_attribute(
        self, **kwargs: Unpack[ResetFpgaImageAttributeRequestRequestTypeDef]
    ) -> ResetFpgaImageAttributeResultTypeDef:
        """
        Resets the specified attribute of the specified Amazon FPGA Image (AFI) to its
        default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/reset_fpga_image_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#reset_fpga_image_attribute)
        """

    async def reset_image_attribute(
        self, **kwargs: Unpack[ResetImageAttributeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Resets an attribute of an AMI to its default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/reset_image_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#reset_image_attribute)
        """

    async def reset_instance_attribute(
        self, **kwargs: Unpack[ResetInstanceAttributeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Resets an attribute of an instance to its default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/reset_instance_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#reset_instance_attribute)
        """

    async def reset_network_interface_attribute(
        self, **kwargs: Unpack[ResetNetworkInterfaceAttributeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Resets a network interface attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/reset_network_interface_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#reset_network_interface_attribute)
        """

    async def reset_snapshot_attribute(
        self, **kwargs: Unpack[ResetSnapshotAttributeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Resets permission settings for the specified snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/reset_snapshot_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#reset_snapshot_attribute)
        """

    async def restore_address_to_classic(
        self, **kwargs: Unpack[RestoreAddressToClassicRequestRequestTypeDef]
    ) -> RestoreAddressToClassicResultTypeDef:
        """
        This action is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/restore_address_to_classic.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#restore_address_to_classic)
        """

    async def restore_image_from_recycle_bin(
        self, **kwargs: Unpack[RestoreImageFromRecycleBinRequestRequestTypeDef]
    ) -> RestoreImageFromRecycleBinResultTypeDef:
        """
        Restores an AMI from the Recycle Bin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/restore_image_from_recycle_bin.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#restore_image_from_recycle_bin)
        """

    async def restore_managed_prefix_list_version(
        self, **kwargs: Unpack[RestoreManagedPrefixListVersionRequestRequestTypeDef]
    ) -> RestoreManagedPrefixListVersionResultTypeDef:
        """
        Restores the entries from a previous version of a managed prefix list to a new
        version of the prefix list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/restore_managed_prefix_list_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#restore_managed_prefix_list_version)
        """

    async def restore_snapshot_from_recycle_bin(
        self, **kwargs: Unpack[RestoreSnapshotFromRecycleBinRequestRequestTypeDef]
    ) -> RestoreSnapshotFromRecycleBinResultTypeDef:
        """
        Restores a snapshot from the Recycle Bin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/restore_snapshot_from_recycle_bin.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#restore_snapshot_from_recycle_bin)
        """

    async def restore_snapshot_tier(
        self, **kwargs: Unpack[RestoreSnapshotTierRequestRequestTypeDef]
    ) -> RestoreSnapshotTierResultTypeDef:
        """
        Restores an archived Amazon EBS snapshot for use temporarily or permanently, or
        modifies the restore period or restore type for a snapshot that was previously
        temporarily restored.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/restore_snapshot_tier.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#restore_snapshot_tier)
        """

    async def revoke_client_vpn_ingress(
        self, **kwargs: Unpack[RevokeClientVpnIngressRequestRequestTypeDef]
    ) -> RevokeClientVpnIngressResultTypeDef:
        """
        Removes an ingress authorization rule from a Client VPN endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/revoke_client_vpn_ingress.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#revoke_client_vpn_ingress)
        """

    async def revoke_security_group_egress(
        self, **kwargs: Unpack[RevokeSecurityGroupEgressRequestRequestTypeDef]
    ) -> RevokeSecurityGroupEgressResultTypeDef:
        """
        Removes the specified outbound (egress) rules from the specified security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/revoke_security_group_egress.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#revoke_security_group_egress)
        """

    async def revoke_security_group_ingress(
        self, **kwargs: Unpack[RevokeSecurityGroupIngressRequestRequestTypeDef]
    ) -> RevokeSecurityGroupIngressResultTypeDef:
        """
        Removes the specified inbound (ingress) rules from a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/revoke_security_group_ingress.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#revoke_security_group_ingress)
        """

    async def run_instances(
        self, **kwargs: Unpack[RunInstancesRequestRequestTypeDef]
    ) -> ReservationResponseTypeDef:
        """
        Launches the specified number of instances using an AMI for which you have
        permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/run_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#run_instances)
        """

    async def run_scheduled_instances(
        self, **kwargs: Unpack[RunScheduledInstancesRequestRequestTypeDef]
    ) -> RunScheduledInstancesResultTypeDef:
        """
        Launches the specified Scheduled Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/run_scheduled_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#run_scheduled_instances)
        """

    async def search_local_gateway_routes(
        self, **kwargs: Unpack[SearchLocalGatewayRoutesRequestRequestTypeDef]
    ) -> SearchLocalGatewayRoutesResultTypeDef:
        """
        Searches for routes in the specified local gateway route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/search_local_gateway_routes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#search_local_gateway_routes)
        """

    async def search_transit_gateway_multicast_groups(
        self, **kwargs: Unpack[SearchTransitGatewayMulticastGroupsRequestRequestTypeDef]
    ) -> SearchTransitGatewayMulticastGroupsResultTypeDef:
        """
        Searches one or more transit gateway multicast groups and returns the group
        membership information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/search_transit_gateway_multicast_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#search_transit_gateway_multicast_groups)
        """

    async def search_transit_gateway_routes(
        self, **kwargs: Unpack[SearchTransitGatewayRoutesRequestRequestTypeDef]
    ) -> SearchTransitGatewayRoutesResultTypeDef:
        """
        Searches for routes in the specified transit gateway route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/search_transit_gateway_routes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#search_transit_gateway_routes)
        """

    async def send_diagnostic_interrupt(
        self, **kwargs: Unpack[SendDiagnosticInterruptRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sends a diagnostic interrupt to the specified Amazon EC2 instance to trigger a
        <i>kernel panic</i> (on Linux instances), or a <i>blue screen</i>/<i>stop
        error</i> (on Windows instances).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/send_diagnostic_interrupt.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#send_diagnostic_interrupt)
        """

    async def start_instances(
        self, **kwargs: Unpack[StartInstancesRequestRequestTypeDef]
    ) -> StartInstancesResultTypeDef:
        """
        Starts an Amazon EBS-backed instance that you've previously stopped.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/start_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#start_instances)
        """

    async def start_network_insights_access_scope_analysis(
        self, **kwargs: Unpack[StartNetworkInsightsAccessScopeAnalysisRequestRequestTypeDef]
    ) -> StartNetworkInsightsAccessScopeAnalysisResultTypeDef:
        """
        Starts analyzing the specified Network Access Scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/start_network_insights_access_scope_analysis.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#start_network_insights_access_scope_analysis)
        """

    async def start_network_insights_analysis(
        self, **kwargs: Unpack[StartNetworkInsightsAnalysisRequestRequestTypeDef]
    ) -> StartNetworkInsightsAnalysisResultTypeDef:
        """
        Starts analyzing the specified path.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/start_network_insights_analysis.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#start_network_insights_analysis)
        """

    async def start_vpc_endpoint_service_private_dns_verification(
        self, **kwargs: Unpack[StartVpcEndpointServicePrivateDnsVerificationRequestRequestTypeDef]
    ) -> StartVpcEndpointServicePrivateDnsVerificationResultTypeDef:
        """
        Initiates the verification process to prove that the service provider owns the
        private DNS name domain for the endpoint service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/start_vpc_endpoint_service_private_dns_verification.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#start_vpc_endpoint_service_private_dns_verification)
        """

    async def stop_instances(
        self, **kwargs: Unpack[StopInstancesRequestRequestTypeDef]
    ) -> StopInstancesResultTypeDef:
        """
        Stops an Amazon EBS-backed instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/stop_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#stop_instances)
        """

    async def terminate_client_vpn_connections(
        self, **kwargs: Unpack[TerminateClientVpnConnectionsRequestRequestTypeDef]
    ) -> TerminateClientVpnConnectionsResultTypeDef:
        """
        Terminates active Client VPN endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/terminate_client_vpn_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#terminate_client_vpn_connections)
        """

    async def terminate_instances(
        self, **kwargs: Unpack[TerminateInstancesRequestRequestTypeDef]
    ) -> TerminateInstancesResultTypeDef:
        """
        Shuts down the specified instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/terminate_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#terminate_instances)
        """

    async def unassign_ipv6_addresses(
        self, **kwargs: Unpack[UnassignIpv6AddressesRequestRequestTypeDef]
    ) -> UnassignIpv6AddressesResultTypeDef:
        """
        Unassigns one or more IPv6 addresses IPv4 Prefix Delegation prefixes from a
        network interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/unassign_ipv6_addresses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#unassign_ipv6_addresses)
        """

    async def unassign_private_ip_addresses(
        self, **kwargs: Unpack[UnassignPrivateIpAddressesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Unassigns one or more secondary private IP addresses, or IPv4 Prefix Delegation
        prefixes from a network interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/unassign_private_ip_addresses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#unassign_private_ip_addresses)
        """

    async def unassign_private_nat_gateway_address(
        self, **kwargs: Unpack[UnassignPrivateNatGatewayAddressRequestRequestTypeDef]
    ) -> UnassignPrivateNatGatewayAddressResultTypeDef:
        """
        Unassigns secondary private IPv4 addresses from a private NAT gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/unassign_private_nat_gateway_address.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#unassign_private_nat_gateway_address)
        """

    async def unlock_snapshot(
        self, **kwargs: Unpack[UnlockSnapshotRequestRequestTypeDef]
    ) -> UnlockSnapshotResultTypeDef:
        """
        Unlocks a snapshot that is locked in governance mode or that is locked in
        compliance mode but still in the cooling-off period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/unlock_snapshot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#unlock_snapshot)
        """

    async def unmonitor_instances(
        self, **kwargs: Unpack[UnmonitorInstancesRequestRequestTypeDef]
    ) -> UnmonitorInstancesResultTypeDef:
        """
        Disables detailed monitoring for a running instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/unmonitor_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#unmonitor_instances)
        """

    async def update_security_group_rule_descriptions_egress(
        self, **kwargs: Unpack[UpdateSecurityGroupRuleDescriptionsEgressRequestRequestTypeDef]
    ) -> UpdateSecurityGroupRuleDescriptionsEgressResultTypeDef:
        """
        Updates the description of an egress (outbound) security group rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/update_security_group_rule_descriptions_egress.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#update_security_group_rule_descriptions_egress)
        """

    async def update_security_group_rule_descriptions_ingress(
        self, **kwargs: Unpack[UpdateSecurityGroupRuleDescriptionsIngressRequestRequestTypeDef]
    ) -> UpdateSecurityGroupRuleDescriptionsIngressResultTypeDef:
        """
        Updates the description of an ingress (inbound) security group rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/update_security_group_rule_descriptions_ingress.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#update_security_group_rule_descriptions_ingress)
        """

    async def withdraw_byoip_cidr(
        self, **kwargs: Unpack[WithdrawByoipCidrRequestRequestTypeDef]
    ) -> WithdrawByoipCidrResultTypeDef:
        """
        Stops advertising an address range that is provisioned as an address pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/withdraw_byoip_cidr.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#withdraw_byoip_cidr)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_address_transfers"]
    ) -> DescribeAddressTransfersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_addresses_attribute"]
    ) -> DescribeAddressesAttributePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_aws_network_performance_metric_subscriptions"]
    ) -> DescribeAwsNetworkPerformanceMetricSubscriptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_byoip_cidrs"]
    ) -> DescribeByoipCidrsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_capacity_block_offerings"]
    ) -> DescribeCapacityBlockOfferingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_capacity_reservation_fleets"]
    ) -> DescribeCapacityReservationFleetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_capacity_reservations"]
    ) -> DescribeCapacityReservationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_carrier_gateways"]
    ) -> DescribeCarrierGatewaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_classic_link_instances"]
    ) -> DescribeClassicLinkInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_client_vpn_authorization_rules"]
    ) -> DescribeClientVpnAuthorizationRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_client_vpn_connections"]
    ) -> DescribeClientVpnConnectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_client_vpn_endpoints"]
    ) -> DescribeClientVpnEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_client_vpn_routes"]
    ) -> DescribeClientVpnRoutesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_client_vpn_target_networks"]
    ) -> DescribeClientVpnTargetNetworksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_coip_pools"]
    ) -> DescribeCoipPoolsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_dhcp_options"]
    ) -> DescribeDhcpOptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_egress_only_internet_gateways"]
    ) -> DescribeEgressOnlyInternetGatewaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_export_image_tasks"]
    ) -> DescribeExportImageTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_fast_launch_images"]
    ) -> DescribeFastLaunchImagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_fast_snapshot_restores"]
    ) -> DescribeFastSnapshotRestoresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_fleets"]) -> DescribeFleetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_flow_logs"]
    ) -> DescribeFlowLogsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_fpga_images"]
    ) -> DescribeFpgaImagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_host_reservation_offerings"]
    ) -> DescribeHostReservationOfferingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_host_reservations"]
    ) -> DescribeHostReservationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_hosts"]) -> DescribeHostsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_iam_instance_profile_associations"]
    ) -> DescribeIamInstanceProfileAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_images"]) -> DescribeImagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_import_image_tasks"]
    ) -> DescribeImportImageTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_import_snapshot_tasks"]
    ) -> DescribeImportSnapshotTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_connect_endpoints"]
    ) -> DescribeInstanceConnectEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_credit_specifications"]
    ) -> DescribeInstanceCreditSpecificationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_event_windows"]
    ) -> DescribeInstanceEventWindowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_status"]
    ) -> DescribeInstanceStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_topology"]
    ) -> DescribeInstanceTopologyPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_type_offerings"]
    ) -> DescribeInstanceTypeOfferingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_types"]
    ) -> DescribeInstanceTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instances"]
    ) -> DescribeInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_internet_gateways"]
    ) -> DescribeInternetGatewaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_ipam_pools"]
    ) -> DescribeIpamPoolsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_ipam_resource_discoveries"]
    ) -> DescribeIpamResourceDiscoveriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_ipam_resource_discovery_associations"]
    ) -> DescribeIpamResourceDiscoveryAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_ipam_scopes"]
    ) -> DescribeIpamScopesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_ipams"]) -> DescribeIpamsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_ipv6_pools"]
    ) -> DescribeIpv6PoolsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_launch_template_versions"]
    ) -> DescribeLaunchTemplateVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_launch_templates"]
    ) -> DescribeLaunchTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self,
        operation_name: Literal[
            "describe_local_gateway_route_table_virtual_interface_group_associations"
        ],
    ) -> DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_local_gateway_route_table_vpc_associations"]
    ) -> DescribeLocalGatewayRouteTableVpcAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_local_gateway_route_tables"]
    ) -> DescribeLocalGatewayRouteTablesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_local_gateway_virtual_interface_groups"]
    ) -> DescribeLocalGatewayVirtualInterfaceGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_local_gateway_virtual_interfaces"]
    ) -> DescribeLocalGatewayVirtualInterfacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_local_gateways"]
    ) -> DescribeLocalGatewaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_mac_hosts"]
    ) -> DescribeMacHostsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_managed_prefix_lists"]
    ) -> DescribeManagedPrefixListsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_moving_addresses"]
    ) -> DescribeMovingAddressesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_nat_gateways"]
    ) -> DescribeNatGatewaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_network_acls"]
    ) -> DescribeNetworkAclsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_network_insights_access_scope_analyses"]
    ) -> DescribeNetworkInsightsAccessScopeAnalysesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_network_insights_access_scopes"]
    ) -> DescribeNetworkInsightsAccessScopesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_network_insights_analyses"]
    ) -> DescribeNetworkInsightsAnalysesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_network_insights_paths"]
    ) -> DescribeNetworkInsightsPathsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_network_interface_permissions"]
    ) -> DescribeNetworkInterfacePermissionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_network_interfaces"]
    ) -> DescribeNetworkInterfacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_prefix_lists"]
    ) -> DescribePrefixListsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_principal_id_format"]
    ) -> DescribePrincipalIdFormatPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_public_ipv4_pools"]
    ) -> DescribePublicIpv4PoolsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_replace_root_volume_tasks"]
    ) -> DescribeReplaceRootVolumeTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_instances_modifications"]
    ) -> DescribeReservedInstancesModificationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_instances_offerings"]
    ) -> DescribeReservedInstancesOfferingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_route_tables"]
    ) -> DescribeRouteTablesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scheduled_instance_availability"]
    ) -> DescribeScheduledInstanceAvailabilityPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scheduled_instances"]
    ) -> DescribeScheduledInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_security_group_rules"]
    ) -> DescribeSecurityGroupRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_security_groups"]
    ) -> DescribeSecurityGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_snapshot_tier_status"]
    ) -> DescribeSnapshotTierStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_snapshots"]
    ) -> DescribeSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_spot_fleet_instances"]
    ) -> DescribeSpotFleetInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_spot_fleet_requests"]
    ) -> DescribeSpotFleetRequestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_spot_instance_requests"]
    ) -> DescribeSpotInstanceRequestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_spot_price_history"]
    ) -> DescribeSpotPriceHistoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_stale_security_groups"]
    ) -> DescribeStaleSecurityGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_store_image_tasks"]
    ) -> DescribeStoreImageTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_subnets"]
    ) -> DescribeSubnetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_tags"]) -> DescribeTagsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_traffic_mirror_filters"]
    ) -> DescribeTrafficMirrorFiltersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_traffic_mirror_sessions"]
    ) -> DescribeTrafficMirrorSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_traffic_mirror_targets"]
    ) -> DescribeTrafficMirrorTargetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_transit_gateway_attachments"]
    ) -> DescribeTransitGatewayAttachmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_transit_gateway_connect_peers"]
    ) -> DescribeTransitGatewayConnectPeersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_transit_gateway_connects"]
    ) -> DescribeTransitGatewayConnectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_transit_gateway_multicast_domains"]
    ) -> DescribeTransitGatewayMulticastDomainsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_transit_gateway_peering_attachments"]
    ) -> DescribeTransitGatewayPeeringAttachmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_transit_gateway_policy_tables"]
    ) -> DescribeTransitGatewayPolicyTablesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_transit_gateway_route_table_announcements"]
    ) -> DescribeTransitGatewayRouteTableAnnouncementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_transit_gateway_route_tables"]
    ) -> DescribeTransitGatewayRouteTablesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_transit_gateway_vpc_attachments"]
    ) -> DescribeTransitGatewayVpcAttachmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_transit_gateways"]
    ) -> DescribeTransitGatewaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_trunk_interface_associations"]
    ) -> DescribeTrunkInterfaceAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_verified_access_endpoints"]
    ) -> DescribeVerifiedAccessEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_verified_access_groups"]
    ) -> DescribeVerifiedAccessGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_verified_access_instance_logging_configurations"]
    ) -> DescribeVerifiedAccessInstanceLoggingConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_verified_access_instances"]
    ) -> DescribeVerifiedAccessInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_verified_access_trust_providers"]
    ) -> DescribeVerifiedAccessTrustProvidersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_volume_status"]
    ) -> DescribeVolumeStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_volumes_modifications"]
    ) -> DescribeVolumesModificationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_volumes"]
    ) -> DescribeVolumesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_vpc_classic_link_dns_support"]
    ) -> DescribeVpcClassicLinkDnsSupportPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_vpc_endpoint_connection_notifications"]
    ) -> DescribeVpcEndpointConnectionNotificationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_vpc_endpoint_connections"]
    ) -> DescribeVpcEndpointConnectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_vpc_endpoint_service_configurations"]
    ) -> DescribeVpcEndpointServiceConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_vpc_endpoint_service_permissions"]
    ) -> DescribeVpcEndpointServicePermissionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_vpc_endpoint_services"]
    ) -> DescribeVpcEndpointServicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_vpc_endpoints"]
    ) -> DescribeVpcEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_vpc_peering_connections"]
    ) -> DescribeVpcPeeringConnectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_vpcs"]) -> DescribeVpcsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_associated_ipv6_pool_cidrs"]
    ) -> GetAssociatedIpv6PoolCidrsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_aws_network_performance_data"]
    ) -> GetAwsNetworkPerformanceDataPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_groups_for_capacity_reservation"]
    ) -> GetGroupsForCapacityReservationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_instance_types_from_instance_requirements"]
    ) -> GetInstanceTypesFromInstanceRequirementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_ipam_address_history"]
    ) -> GetIpamAddressHistoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_ipam_discovered_accounts"]
    ) -> GetIpamDiscoveredAccountsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_ipam_discovered_resource_cidrs"]
    ) -> GetIpamDiscoveredResourceCidrsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_ipam_pool_allocations"]
    ) -> GetIpamPoolAllocationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_ipam_pool_cidrs"]
    ) -> GetIpamPoolCidrsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_ipam_resource_cidrs"]
    ) -> GetIpamResourceCidrsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_managed_prefix_list_associations"]
    ) -> GetManagedPrefixListAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_managed_prefix_list_entries"]
    ) -> GetManagedPrefixListEntriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_network_insights_access_scope_analysis_findings"]
    ) -> GetNetworkInsightsAccessScopeAnalysisFindingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_security_groups_for_vpc"]
    ) -> GetSecurityGroupsForVpcPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_spot_placement_scores"]
    ) -> GetSpotPlacementScoresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_transit_gateway_attachment_propagations"]
    ) -> GetTransitGatewayAttachmentPropagationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_transit_gateway_multicast_domain_associations"]
    ) -> GetTransitGatewayMulticastDomainAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_transit_gateway_policy_table_associations"]
    ) -> GetTransitGatewayPolicyTableAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_transit_gateway_prefix_list_references"]
    ) -> GetTransitGatewayPrefixListReferencesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_transit_gateway_route_table_associations"]
    ) -> GetTransitGatewayRouteTableAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_transit_gateway_route_table_propagations"]
    ) -> GetTransitGatewayRouteTablePropagationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_vpn_connection_device_types"]
    ) -> GetVpnConnectionDeviceTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_images_in_recycle_bin"]
    ) -> ListImagesInRecycleBinPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_snapshots_in_recycle_bin"]
    ) -> ListSnapshotsInRecycleBinPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_local_gateway_routes"]
    ) -> SearchLocalGatewayRoutesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_transit_gateway_multicast_groups"]
    ) -> SearchTransitGatewayMulticastGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["bundle_task_complete"]) -> BundleTaskCompleteWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["conversion_task_cancelled"]
    ) -> ConversionTaskCancelledWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["conversion_task_completed"]
    ) -> ConversionTaskCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["conversion_task_deleted"]
    ) -> ConversionTaskDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["customer_gateway_available"]
    ) -> CustomerGatewayAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["export_task_cancelled"]
    ) -> ExportTaskCancelledWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["export_task_completed"]
    ) -> ExportTaskCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["image_available"]) -> ImageAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["image_exists"]) -> ImageExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["instance_exists"]) -> InstanceExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["instance_running"]) -> InstanceRunningWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["instance_status_ok"]) -> InstanceStatusOkWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["instance_stopped"]) -> InstanceStoppedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["instance_terminated"]) -> InstanceTerminatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["internet_gateway_exists"]
    ) -> InternetGatewayExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["key_pair_exists"]) -> KeyPairExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["nat_gateway_available"]
    ) -> NatGatewayAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["nat_gateway_deleted"]) -> NatGatewayDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["network_interface_available"]
    ) -> NetworkInterfaceAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["password_data_available"]
    ) -> PasswordDataAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["security_group_exists"]
    ) -> SecurityGroupExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["snapshot_completed"]) -> SnapshotCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["snapshot_imported"]) -> SnapshotImportedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["spot_instance_request_fulfilled"]
    ) -> SpotInstanceRequestFulfilledWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["store_image_task_complete"]
    ) -> StoreImageTaskCompleteWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["subnet_available"]) -> SubnetAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["system_status_ok"]) -> SystemStatusOkWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["volume_available"]) -> VolumeAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["volume_deleted"]) -> VolumeDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["volume_in_use"]) -> VolumeInUseWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["vpc_available"]) -> VpcAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["vpc_exists"]) -> VpcExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["vpc_peering_connection_deleted"]
    ) -> VpcPeeringConnectionDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["vpc_peering_connection_exists"]
    ) -> VpcPeeringConnectionExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["vpn_connection_available"]
    ) -> VpnConnectionAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["vpn_connection_deleted"]
    ) -> VpnConnectionDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/#get_waiter)
        """

    async def __aenter__(self) -> "EC2Client":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/client/)
        """
