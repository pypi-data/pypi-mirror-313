"""
Type annotations for route53 service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_route53.client import Route53Client

    session = get_session()
    async with session.create_client("route53") as client:
        client: Route53Client
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListCidrBlocksPaginator,
    ListCidrCollectionsPaginator,
    ListCidrLocationsPaginator,
    ListHealthChecksPaginator,
    ListHostedZonesPaginator,
    ListQueryLoggingConfigsPaginator,
    ListResourceRecordSetsPaginator,
    ListVPCAssociationAuthorizationsPaginator,
)
from .type_defs import (
    ActivateKeySigningKeyRequestRequestTypeDef,
    ActivateKeySigningKeyResponseTypeDef,
    AssociateVPCWithHostedZoneRequestRequestTypeDef,
    AssociateVPCWithHostedZoneResponseTypeDef,
    ChangeCidrCollectionRequestRequestTypeDef,
    ChangeCidrCollectionResponseTypeDef,
    ChangeResourceRecordSetsRequestRequestTypeDef,
    ChangeResourceRecordSetsResponseTypeDef,
    ChangeTagsForResourceRequestRequestTypeDef,
    CreateCidrCollectionRequestRequestTypeDef,
    CreateCidrCollectionResponseTypeDef,
    CreateHealthCheckRequestRequestTypeDef,
    CreateHealthCheckResponseTypeDef,
    CreateHostedZoneRequestRequestTypeDef,
    CreateHostedZoneResponseTypeDef,
    CreateKeySigningKeyRequestRequestTypeDef,
    CreateKeySigningKeyResponseTypeDef,
    CreateQueryLoggingConfigRequestRequestTypeDef,
    CreateQueryLoggingConfigResponseTypeDef,
    CreateReusableDelegationSetRequestRequestTypeDef,
    CreateReusableDelegationSetResponseTypeDef,
    CreateTrafficPolicyInstanceRequestRequestTypeDef,
    CreateTrafficPolicyInstanceResponseTypeDef,
    CreateTrafficPolicyRequestRequestTypeDef,
    CreateTrafficPolicyResponseTypeDef,
    CreateTrafficPolicyVersionRequestRequestTypeDef,
    CreateTrafficPolicyVersionResponseTypeDef,
    CreateVPCAssociationAuthorizationRequestRequestTypeDef,
    CreateVPCAssociationAuthorizationResponseTypeDef,
    DeactivateKeySigningKeyRequestRequestTypeDef,
    DeactivateKeySigningKeyResponseTypeDef,
    DeleteCidrCollectionRequestRequestTypeDef,
    DeleteHealthCheckRequestRequestTypeDef,
    DeleteHostedZoneRequestRequestTypeDef,
    DeleteHostedZoneResponseTypeDef,
    DeleteKeySigningKeyRequestRequestTypeDef,
    DeleteKeySigningKeyResponseTypeDef,
    DeleteQueryLoggingConfigRequestRequestTypeDef,
    DeleteReusableDelegationSetRequestRequestTypeDef,
    DeleteTrafficPolicyInstanceRequestRequestTypeDef,
    DeleteTrafficPolicyRequestRequestTypeDef,
    DeleteVPCAssociationAuthorizationRequestRequestTypeDef,
    DisableHostedZoneDNSSECRequestRequestTypeDef,
    DisableHostedZoneDNSSECResponseTypeDef,
    DisassociateVPCFromHostedZoneRequestRequestTypeDef,
    DisassociateVPCFromHostedZoneResponseTypeDef,
    EnableHostedZoneDNSSECRequestRequestTypeDef,
    EnableHostedZoneDNSSECResponseTypeDef,
    GetAccountLimitRequestRequestTypeDef,
    GetAccountLimitResponseTypeDef,
    GetChangeRequestRequestTypeDef,
    GetChangeResponseTypeDef,
    GetCheckerIpRangesResponseTypeDef,
    GetDNSSECRequestRequestTypeDef,
    GetDNSSECResponseTypeDef,
    GetGeoLocationRequestRequestTypeDef,
    GetGeoLocationResponseTypeDef,
    GetHealthCheckCountResponseTypeDef,
    GetHealthCheckLastFailureReasonRequestRequestTypeDef,
    GetHealthCheckLastFailureReasonResponseTypeDef,
    GetHealthCheckRequestRequestTypeDef,
    GetHealthCheckResponseTypeDef,
    GetHealthCheckStatusRequestRequestTypeDef,
    GetHealthCheckStatusResponseTypeDef,
    GetHostedZoneCountResponseTypeDef,
    GetHostedZoneLimitRequestRequestTypeDef,
    GetHostedZoneLimitResponseTypeDef,
    GetHostedZoneRequestRequestTypeDef,
    GetHostedZoneResponseTypeDef,
    GetQueryLoggingConfigRequestRequestTypeDef,
    GetQueryLoggingConfigResponseTypeDef,
    GetReusableDelegationSetLimitRequestRequestTypeDef,
    GetReusableDelegationSetLimitResponseTypeDef,
    GetReusableDelegationSetRequestRequestTypeDef,
    GetReusableDelegationSetResponseTypeDef,
    GetTrafficPolicyInstanceCountResponseTypeDef,
    GetTrafficPolicyInstanceRequestRequestTypeDef,
    GetTrafficPolicyInstanceResponseTypeDef,
    GetTrafficPolicyRequestRequestTypeDef,
    GetTrafficPolicyResponseTypeDef,
    ListCidrBlocksRequestRequestTypeDef,
    ListCidrBlocksResponseTypeDef,
    ListCidrCollectionsRequestRequestTypeDef,
    ListCidrCollectionsResponseTypeDef,
    ListCidrLocationsRequestRequestTypeDef,
    ListCidrLocationsResponseTypeDef,
    ListGeoLocationsRequestRequestTypeDef,
    ListGeoLocationsResponseTypeDef,
    ListHealthChecksRequestRequestTypeDef,
    ListHealthChecksResponseTypeDef,
    ListHostedZonesByNameRequestRequestTypeDef,
    ListHostedZonesByNameResponseTypeDef,
    ListHostedZonesByVPCRequestRequestTypeDef,
    ListHostedZonesByVPCResponseTypeDef,
    ListHostedZonesRequestRequestTypeDef,
    ListHostedZonesResponseTypeDef,
    ListQueryLoggingConfigsRequestRequestTypeDef,
    ListQueryLoggingConfigsResponseTypeDef,
    ListResourceRecordSetsRequestRequestTypeDef,
    ListResourceRecordSetsResponseTypeDef,
    ListReusableDelegationSetsRequestRequestTypeDef,
    ListReusableDelegationSetsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTagsForResourcesRequestRequestTypeDef,
    ListTagsForResourcesResponseTypeDef,
    ListTrafficPoliciesRequestRequestTypeDef,
    ListTrafficPoliciesResponseTypeDef,
    ListTrafficPolicyInstancesByHostedZoneRequestRequestTypeDef,
    ListTrafficPolicyInstancesByHostedZoneResponseTypeDef,
    ListTrafficPolicyInstancesByPolicyRequestRequestTypeDef,
    ListTrafficPolicyInstancesByPolicyResponseTypeDef,
    ListTrafficPolicyInstancesRequestRequestTypeDef,
    ListTrafficPolicyInstancesResponseTypeDef,
    ListTrafficPolicyVersionsRequestRequestTypeDef,
    ListTrafficPolicyVersionsResponseTypeDef,
    ListVPCAssociationAuthorizationsRequestRequestTypeDef,
    ListVPCAssociationAuthorizationsResponseTypeDef,
    TestDNSAnswerRequestRequestTypeDef,
    TestDNSAnswerResponseTypeDef,
    UpdateHealthCheckRequestRequestTypeDef,
    UpdateHealthCheckResponseTypeDef,
    UpdateHostedZoneCommentRequestRequestTypeDef,
    UpdateHostedZoneCommentResponseTypeDef,
    UpdateTrafficPolicyCommentRequestRequestTypeDef,
    UpdateTrafficPolicyCommentResponseTypeDef,
    UpdateTrafficPolicyInstanceRequestRequestTypeDef,
    UpdateTrafficPolicyInstanceResponseTypeDef,
)
from .waiter import ResourceRecordSetsChangedWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("Route53Client",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    CidrBlockInUseException: Type[BotocoreClientError]
    CidrCollectionAlreadyExistsException: Type[BotocoreClientError]
    CidrCollectionInUseException: Type[BotocoreClientError]
    CidrCollectionVersionMismatchException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModification: Type[BotocoreClientError]
    ConflictingDomainExists: Type[BotocoreClientError]
    ConflictingTypes: Type[BotocoreClientError]
    DNSSECNotFound: Type[BotocoreClientError]
    DelegationSetAlreadyCreated: Type[BotocoreClientError]
    DelegationSetAlreadyReusable: Type[BotocoreClientError]
    DelegationSetInUse: Type[BotocoreClientError]
    DelegationSetNotAvailable: Type[BotocoreClientError]
    DelegationSetNotReusable: Type[BotocoreClientError]
    HealthCheckAlreadyExists: Type[BotocoreClientError]
    HealthCheckInUse: Type[BotocoreClientError]
    HealthCheckVersionMismatch: Type[BotocoreClientError]
    HostedZoneAlreadyExists: Type[BotocoreClientError]
    HostedZoneNotEmpty: Type[BotocoreClientError]
    HostedZoneNotFound: Type[BotocoreClientError]
    HostedZoneNotPrivate: Type[BotocoreClientError]
    HostedZonePartiallyDelegated: Type[BotocoreClientError]
    IncompatibleVersion: Type[BotocoreClientError]
    InsufficientCloudWatchLogsResourcePolicy: Type[BotocoreClientError]
    InvalidArgument: Type[BotocoreClientError]
    InvalidChangeBatch: Type[BotocoreClientError]
    InvalidDomainName: Type[BotocoreClientError]
    InvalidInput: Type[BotocoreClientError]
    InvalidKMSArn: Type[BotocoreClientError]
    InvalidKeySigningKeyName: Type[BotocoreClientError]
    InvalidKeySigningKeyStatus: Type[BotocoreClientError]
    InvalidPaginationToken: Type[BotocoreClientError]
    InvalidSigningStatus: Type[BotocoreClientError]
    InvalidTrafficPolicyDocument: Type[BotocoreClientError]
    InvalidVPCId: Type[BotocoreClientError]
    KeySigningKeyAlreadyExists: Type[BotocoreClientError]
    KeySigningKeyInParentDSRecord: Type[BotocoreClientError]
    KeySigningKeyInUse: Type[BotocoreClientError]
    KeySigningKeyWithActiveStatusNotFound: Type[BotocoreClientError]
    LastVPCAssociation: Type[BotocoreClientError]
    LimitsExceeded: Type[BotocoreClientError]
    NoSuchChange: Type[BotocoreClientError]
    NoSuchCidrCollectionException: Type[BotocoreClientError]
    NoSuchCidrLocationException: Type[BotocoreClientError]
    NoSuchCloudWatchLogsLogGroup: Type[BotocoreClientError]
    NoSuchDelegationSet: Type[BotocoreClientError]
    NoSuchGeoLocation: Type[BotocoreClientError]
    NoSuchHealthCheck: Type[BotocoreClientError]
    NoSuchHostedZone: Type[BotocoreClientError]
    NoSuchKeySigningKey: Type[BotocoreClientError]
    NoSuchQueryLoggingConfig: Type[BotocoreClientError]
    NoSuchTrafficPolicy: Type[BotocoreClientError]
    NoSuchTrafficPolicyInstance: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]
    PriorRequestNotComplete: Type[BotocoreClientError]
    PublicZoneVPCAssociation: Type[BotocoreClientError]
    QueryLoggingConfigAlreadyExists: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyHealthChecks: Type[BotocoreClientError]
    TooManyHostedZones: Type[BotocoreClientError]
    TooManyKeySigningKeys: Type[BotocoreClientError]
    TooManyTrafficPolicies: Type[BotocoreClientError]
    TooManyTrafficPolicyInstances: Type[BotocoreClientError]
    TooManyTrafficPolicyVersionsForCurrentPolicy: Type[BotocoreClientError]
    TooManyVPCAssociationAuthorizations: Type[BotocoreClientError]
    TrafficPolicyAlreadyExists: Type[BotocoreClientError]
    TrafficPolicyInUse: Type[BotocoreClientError]
    TrafficPolicyInstanceAlreadyExists: Type[BotocoreClientError]
    VPCAssociationAuthorizationNotFound: Type[BotocoreClientError]
    VPCAssociationNotFound: Type[BotocoreClientError]

class Route53Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Route53Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#close)
        """

    async def activate_key_signing_key(
        self, **kwargs: Unpack[ActivateKeySigningKeyRequestRequestTypeDef]
    ) -> ActivateKeySigningKeyResponseTypeDef:
        """
        Activates a key-signing key (KSK) so that it can be used for signing by DNSSEC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/activate_key_signing_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#activate_key_signing_key)
        """

    async def associate_vpc_with_hosted_zone(
        self, **kwargs: Unpack[AssociateVPCWithHostedZoneRequestRequestTypeDef]
    ) -> AssociateVPCWithHostedZoneResponseTypeDef:
        """
        Associates an Amazon VPC with a private hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/associate_vpc_with_hosted_zone.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#associate_vpc_with_hosted_zone)
        """

    async def change_cidr_collection(
        self, **kwargs: Unpack[ChangeCidrCollectionRequestRequestTypeDef]
    ) -> ChangeCidrCollectionResponseTypeDef:
        """
        Creates, changes, or deletes CIDR blocks within a collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/change_cidr_collection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#change_cidr_collection)
        """

    async def change_resource_record_sets(
        self, **kwargs: Unpack[ChangeResourceRecordSetsRequestRequestTypeDef]
    ) -> ChangeResourceRecordSetsResponseTypeDef:
        """
        Creates, changes, or deletes a resource record set, which contains
        authoritative DNS information for a specified domain name or subdomain name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/change_resource_record_sets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#change_resource_record_sets)
        """

    async def change_tags_for_resource(
        self, **kwargs: Unpack[ChangeTagsForResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds, edits, or deletes tags for a health check or a hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/change_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#change_tags_for_resource)
        """

    async def create_cidr_collection(
        self, **kwargs: Unpack[CreateCidrCollectionRequestRequestTypeDef]
    ) -> CreateCidrCollectionResponseTypeDef:
        """
        Creates a CIDR collection in the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/create_cidr_collection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_cidr_collection)
        """

    async def create_health_check(
        self, **kwargs: Unpack[CreateHealthCheckRequestRequestTypeDef]
    ) -> CreateHealthCheckResponseTypeDef:
        """
        Creates a new health check.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/create_health_check.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_health_check)
        """

    async def create_hosted_zone(
        self, **kwargs: Unpack[CreateHostedZoneRequestRequestTypeDef]
    ) -> CreateHostedZoneResponseTypeDef:
        """
        Creates a new public or private hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/create_hosted_zone.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_hosted_zone)
        """

    async def create_key_signing_key(
        self, **kwargs: Unpack[CreateKeySigningKeyRequestRequestTypeDef]
    ) -> CreateKeySigningKeyResponseTypeDef:
        """
        Creates a new key-signing key (KSK) associated with a hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/create_key_signing_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_key_signing_key)
        """

    async def create_query_logging_config(
        self, **kwargs: Unpack[CreateQueryLoggingConfigRequestRequestTypeDef]
    ) -> CreateQueryLoggingConfigResponseTypeDef:
        """
        Creates a configuration for DNS query logging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/create_query_logging_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_query_logging_config)
        """

    async def create_reusable_delegation_set(
        self, **kwargs: Unpack[CreateReusableDelegationSetRequestRequestTypeDef]
    ) -> CreateReusableDelegationSetResponseTypeDef:
        """
        Creates a delegation set (a group of four name servers) that can be reused by
        multiple hosted zones that were created by the same Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/create_reusable_delegation_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_reusable_delegation_set)
        """

    async def create_traffic_policy(
        self, **kwargs: Unpack[CreateTrafficPolicyRequestRequestTypeDef]
    ) -> CreateTrafficPolicyResponseTypeDef:
        """
        Creates a traffic policy, which you use to create multiple DNS resource record
        sets for one domain name (such as example.com) or one subdomain name (such as
        www.example.com).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/create_traffic_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_traffic_policy)
        """

    async def create_traffic_policy_instance(
        self, **kwargs: Unpack[CreateTrafficPolicyInstanceRequestRequestTypeDef]
    ) -> CreateTrafficPolicyInstanceResponseTypeDef:
        """
        Creates resource record sets in a specified hosted zone based on the settings
        in a specified traffic policy version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/create_traffic_policy_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_traffic_policy_instance)
        """

    async def create_traffic_policy_version(
        self, **kwargs: Unpack[CreateTrafficPolicyVersionRequestRequestTypeDef]
    ) -> CreateTrafficPolicyVersionResponseTypeDef:
        """
        Creates a new version of an existing traffic policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/create_traffic_policy_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_traffic_policy_version)
        """

    async def create_vpc_association_authorization(
        self, **kwargs: Unpack[CreateVPCAssociationAuthorizationRequestRequestTypeDef]
    ) -> CreateVPCAssociationAuthorizationResponseTypeDef:
        """
        Authorizes the Amazon Web Services account that created a specified VPC to
        submit an <code>AssociateVPCWithHostedZone</code> request to associate the VPC
        with a specified hosted zone that was created by a different account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/create_vpc_association_authorization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_vpc_association_authorization)
        """

    async def deactivate_key_signing_key(
        self, **kwargs: Unpack[DeactivateKeySigningKeyRequestRequestTypeDef]
    ) -> DeactivateKeySigningKeyResponseTypeDef:
        """
        Deactivates a key-signing key (KSK) so that it will not be used for signing by
        DNSSEC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/deactivate_key_signing_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#deactivate_key_signing_key)
        """

    async def delete_cidr_collection(
        self, **kwargs: Unpack[DeleteCidrCollectionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a CIDR collection in the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/delete_cidr_collection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_cidr_collection)
        """

    async def delete_health_check(
        self, **kwargs: Unpack[DeleteHealthCheckRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a health check.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/delete_health_check.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_health_check)
        """

    async def delete_hosted_zone(
        self, **kwargs: Unpack[DeleteHostedZoneRequestRequestTypeDef]
    ) -> DeleteHostedZoneResponseTypeDef:
        """
        Deletes a hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/delete_hosted_zone.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_hosted_zone)
        """

    async def delete_key_signing_key(
        self, **kwargs: Unpack[DeleteKeySigningKeyRequestRequestTypeDef]
    ) -> DeleteKeySigningKeyResponseTypeDef:
        """
        Deletes a key-signing key (KSK).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/delete_key_signing_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_key_signing_key)
        """

    async def delete_query_logging_config(
        self, **kwargs: Unpack[DeleteQueryLoggingConfigRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a configuration for DNS query logging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/delete_query_logging_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_query_logging_config)
        """

    async def delete_reusable_delegation_set(
        self, **kwargs: Unpack[DeleteReusableDelegationSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a reusable delegation set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/delete_reusable_delegation_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_reusable_delegation_set)
        """

    async def delete_traffic_policy(
        self, **kwargs: Unpack[DeleteTrafficPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a traffic policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/delete_traffic_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_traffic_policy)
        """

    async def delete_traffic_policy_instance(
        self, **kwargs: Unpack[DeleteTrafficPolicyInstanceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a traffic policy instance and all of the resource record sets that
        Amazon Route 53 created when you created the instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/delete_traffic_policy_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_traffic_policy_instance)
        """

    async def delete_vpc_association_authorization(
        self, **kwargs: Unpack[DeleteVPCAssociationAuthorizationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes authorization to submit an <code>AssociateVPCWithHostedZone</code>
        request to associate a specified VPC with a hosted zone that was created by a
        different account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/delete_vpc_association_authorization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_vpc_association_authorization)
        """

    async def disable_hosted_zone_dnssec(
        self, **kwargs: Unpack[DisableHostedZoneDNSSECRequestRequestTypeDef]
    ) -> DisableHostedZoneDNSSECResponseTypeDef:
        """
        Disables DNSSEC signing in a specific hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/disable_hosted_zone_dnssec.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#disable_hosted_zone_dnssec)
        """

    async def disassociate_vpc_from_hosted_zone(
        self, **kwargs: Unpack[DisassociateVPCFromHostedZoneRequestRequestTypeDef]
    ) -> DisassociateVPCFromHostedZoneResponseTypeDef:
        """
        Disassociates an Amazon Virtual Private Cloud (Amazon VPC) from an Amazon Route
        53 private hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/disassociate_vpc_from_hosted_zone.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#disassociate_vpc_from_hosted_zone)
        """

    async def enable_hosted_zone_dnssec(
        self, **kwargs: Unpack[EnableHostedZoneDNSSECRequestRequestTypeDef]
    ) -> EnableHostedZoneDNSSECResponseTypeDef:
        """
        Enables DNSSEC signing in a specific hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/enable_hosted_zone_dnssec.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#enable_hosted_zone_dnssec)
        """

    async def get_account_limit(
        self, **kwargs: Unpack[GetAccountLimitRequestRequestTypeDef]
    ) -> GetAccountLimitResponseTypeDef:
        """
        Gets the specified limit for the current account, for example, the maximum
        number of health checks that you can create using the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_account_limit.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_account_limit)
        """

    async def get_change(
        self, **kwargs: Unpack[GetChangeRequestRequestTypeDef]
    ) -> GetChangeResponseTypeDef:
        """
        Returns the current status of a change batch request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_change.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_change)
        """

    async def get_checker_ip_ranges(self) -> GetCheckerIpRangesResponseTypeDef:
        """
        Route 53 does not perform authorization for this API because it retrieves
        information that is already available to the public.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_checker_ip_ranges.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_checker_ip_ranges)
        """

    async def get_dnssec(
        self, **kwargs: Unpack[GetDNSSECRequestRequestTypeDef]
    ) -> GetDNSSECResponseTypeDef:
        """
        Returns information about DNSSEC for a specific hosted zone, including the
        key-signing keys (KSKs) in the hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_dnssec.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_dnssec)
        """

    async def get_geo_location(
        self, **kwargs: Unpack[GetGeoLocationRequestRequestTypeDef]
    ) -> GetGeoLocationResponseTypeDef:
        """
        Gets information about whether a specified geographic location is supported for
        Amazon Route 53 geolocation resource record sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_geo_location.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_geo_location)
        """

    async def get_health_check(
        self, **kwargs: Unpack[GetHealthCheckRequestRequestTypeDef]
    ) -> GetHealthCheckResponseTypeDef:
        """
        Gets information about a specified health check.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_health_check.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_health_check)
        """

    async def get_health_check_count(self) -> GetHealthCheckCountResponseTypeDef:
        """
        Retrieves the number of health checks that are associated with the current
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_health_check_count.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_health_check_count)
        """

    async def get_health_check_last_failure_reason(
        self, **kwargs: Unpack[GetHealthCheckLastFailureReasonRequestRequestTypeDef]
    ) -> GetHealthCheckLastFailureReasonResponseTypeDef:
        """
        Gets the reason that a specified health check failed most recently.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_health_check_last_failure_reason.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_health_check_last_failure_reason)
        """

    async def get_health_check_status(
        self, **kwargs: Unpack[GetHealthCheckStatusRequestRequestTypeDef]
    ) -> GetHealthCheckStatusResponseTypeDef:
        """
        Gets status of a specified health check.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_health_check_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_health_check_status)
        """

    async def get_hosted_zone(
        self, **kwargs: Unpack[GetHostedZoneRequestRequestTypeDef]
    ) -> GetHostedZoneResponseTypeDef:
        """
        Gets information about a specified hosted zone including the four name servers
        assigned to the hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_hosted_zone.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_hosted_zone)
        """

    async def get_hosted_zone_count(self) -> GetHostedZoneCountResponseTypeDef:
        """
        Retrieves the number of hosted zones that are associated with the current
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_hosted_zone_count.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_hosted_zone_count)
        """

    async def get_hosted_zone_limit(
        self, **kwargs: Unpack[GetHostedZoneLimitRequestRequestTypeDef]
    ) -> GetHostedZoneLimitResponseTypeDef:
        """
        Gets the specified limit for a specified hosted zone, for example, the maximum
        number of records that you can create in the hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_hosted_zone_limit.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_hosted_zone_limit)
        """

    async def get_query_logging_config(
        self, **kwargs: Unpack[GetQueryLoggingConfigRequestRequestTypeDef]
    ) -> GetQueryLoggingConfigResponseTypeDef:
        """
        Gets information about a specified configuration for DNS query logging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_query_logging_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_query_logging_config)
        """

    async def get_reusable_delegation_set(
        self, **kwargs: Unpack[GetReusableDelegationSetRequestRequestTypeDef]
    ) -> GetReusableDelegationSetResponseTypeDef:
        """
        Retrieves information about a specified reusable delegation set, including the
        four name servers that are assigned to the delegation set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_reusable_delegation_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_reusable_delegation_set)
        """

    async def get_reusable_delegation_set_limit(
        self, **kwargs: Unpack[GetReusableDelegationSetLimitRequestRequestTypeDef]
    ) -> GetReusableDelegationSetLimitResponseTypeDef:
        """
        Gets the maximum number of hosted zones that you can associate with the
        specified reusable delegation set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_reusable_delegation_set_limit.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_reusable_delegation_set_limit)
        """

    async def get_traffic_policy(
        self, **kwargs: Unpack[GetTrafficPolicyRequestRequestTypeDef]
    ) -> GetTrafficPolicyResponseTypeDef:
        """
        Gets information about a specific traffic policy version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_traffic_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_traffic_policy)
        """

    async def get_traffic_policy_instance(
        self, **kwargs: Unpack[GetTrafficPolicyInstanceRequestRequestTypeDef]
    ) -> GetTrafficPolicyInstanceResponseTypeDef:
        """
        Gets information about a specified traffic policy instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_traffic_policy_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_traffic_policy_instance)
        """

    async def get_traffic_policy_instance_count(
        self,
    ) -> GetTrafficPolicyInstanceCountResponseTypeDef:
        """
        Gets the number of traffic policy instances that are associated with the
        current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_traffic_policy_instance_count.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_traffic_policy_instance_count)
        """

    async def list_cidr_blocks(
        self, **kwargs: Unpack[ListCidrBlocksRequestRequestTypeDef]
    ) -> ListCidrBlocksResponseTypeDef:
        """
        Returns a paginated list of location objects and their CIDR blocks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_cidr_blocks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_cidr_blocks)
        """

    async def list_cidr_collections(
        self, **kwargs: Unpack[ListCidrCollectionsRequestRequestTypeDef]
    ) -> ListCidrCollectionsResponseTypeDef:
        """
        Returns a paginated list of CIDR collections in the Amazon Web Services account
        (metadata only).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_cidr_collections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_cidr_collections)
        """

    async def list_cidr_locations(
        self, **kwargs: Unpack[ListCidrLocationsRequestRequestTypeDef]
    ) -> ListCidrLocationsResponseTypeDef:
        """
        Returns a paginated list of CIDR locations for the given collection (metadata
        only, does not include CIDR blocks).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_cidr_locations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_cidr_locations)
        """

    async def list_geo_locations(
        self, **kwargs: Unpack[ListGeoLocationsRequestRequestTypeDef]
    ) -> ListGeoLocationsResponseTypeDef:
        """
        Retrieves a list of supported geographic locations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_geo_locations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_geo_locations)
        """

    async def list_health_checks(
        self, **kwargs: Unpack[ListHealthChecksRequestRequestTypeDef]
    ) -> ListHealthChecksResponseTypeDef:
        """
        Retrieve a list of the health checks that are associated with the current
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_health_checks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_health_checks)
        """

    async def list_hosted_zones(
        self, **kwargs: Unpack[ListHostedZonesRequestRequestTypeDef]
    ) -> ListHostedZonesResponseTypeDef:
        """
        Retrieves a list of the public and private hosted zones that are associated
        with the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_hosted_zones.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_hosted_zones)
        """

    async def list_hosted_zones_by_name(
        self, **kwargs: Unpack[ListHostedZonesByNameRequestRequestTypeDef]
    ) -> ListHostedZonesByNameResponseTypeDef:
        """
        Retrieves a list of your hosted zones in lexicographic order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_hosted_zones_by_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_hosted_zones_by_name)
        """

    async def list_hosted_zones_by_vpc(
        self, **kwargs: Unpack[ListHostedZonesByVPCRequestRequestTypeDef]
    ) -> ListHostedZonesByVPCResponseTypeDef:
        """
        Lists all the private hosted zones that a specified VPC is associated with,
        regardless of which Amazon Web Services account or Amazon Web Services service
        owns the hosted zones.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_hosted_zones_by_vpc.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_hosted_zones_by_vpc)
        """

    async def list_query_logging_configs(
        self, **kwargs: Unpack[ListQueryLoggingConfigsRequestRequestTypeDef]
    ) -> ListQueryLoggingConfigsResponseTypeDef:
        """
        Lists the configurations for DNS query logging that are associated with the
        current Amazon Web Services account or the configuration that is associated
        with a specified hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_query_logging_configs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_query_logging_configs)
        """

    async def list_resource_record_sets(
        self, **kwargs: Unpack[ListResourceRecordSetsRequestRequestTypeDef]
    ) -> ListResourceRecordSetsResponseTypeDef:
        """
        Lists the resource record sets in a specified hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_resource_record_sets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_resource_record_sets)
        """

    async def list_reusable_delegation_sets(
        self, **kwargs: Unpack[ListReusableDelegationSetsRequestRequestTypeDef]
    ) -> ListReusableDelegationSetsResponseTypeDef:
        """
        Retrieves a list of the reusable delegation sets that are associated with the
        current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_reusable_delegation_sets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_reusable_delegation_sets)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for one health check or hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_tags_for_resource)
        """

    async def list_tags_for_resources(
        self, **kwargs: Unpack[ListTagsForResourcesRequestRequestTypeDef]
    ) -> ListTagsForResourcesResponseTypeDef:
        """
        Lists tags for up to 10 health checks or hosted zones.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_tags_for_resources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_tags_for_resources)
        """

    async def list_traffic_policies(
        self, **kwargs: Unpack[ListTrafficPoliciesRequestRequestTypeDef]
    ) -> ListTrafficPoliciesResponseTypeDef:
        """
        Gets information about the latest version for every traffic policy that is
        associated with the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_traffic_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_traffic_policies)
        """

    async def list_traffic_policy_instances(
        self, **kwargs: Unpack[ListTrafficPolicyInstancesRequestRequestTypeDef]
    ) -> ListTrafficPolicyInstancesResponseTypeDef:
        """
        Gets information about the traffic policy instances that you created by using
        the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_traffic_policy_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_traffic_policy_instances)
        """

    async def list_traffic_policy_instances_by_hosted_zone(
        self, **kwargs: Unpack[ListTrafficPolicyInstancesByHostedZoneRequestRequestTypeDef]
    ) -> ListTrafficPolicyInstancesByHostedZoneResponseTypeDef:
        """
        Gets information about the traffic policy instances that you created in a
        specified hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_traffic_policy_instances_by_hosted_zone.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_traffic_policy_instances_by_hosted_zone)
        """

    async def list_traffic_policy_instances_by_policy(
        self, **kwargs: Unpack[ListTrafficPolicyInstancesByPolicyRequestRequestTypeDef]
    ) -> ListTrafficPolicyInstancesByPolicyResponseTypeDef:
        """
        Gets information about the traffic policy instances that you created by using a
        specify traffic policy version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_traffic_policy_instances_by_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_traffic_policy_instances_by_policy)
        """

    async def list_traffic_policy_versions(
        self, **kwargs: Unpack[ListTrafficPolicyVersionsRequestRequestTypeDef]
    ) -> ListTrafficPolicyVersionsResponseTypeDef:
        """
        Gets information about all of the versions for a specified traffic policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_traffic_policy_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_traffic_policy_versions)
        """

    async def list_vpc_association_authorizations(
        self, **kwargs: Unpack[ListVPCAssociationAuthorizationsRequestRequestTypeDef]
    ) -> ListVPCAssociationAuthorizationsResponseTypeDef:
        """
        Gets a list of the VPCs that were created by other accounts and that can be
        associated with a specified hosted zone because you've submitted one or more
        <code>CreateVPCAssociationAuthorization</code> requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/list_vpc_association_authorizations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_vpc_association_authorizations)
        """

    async def test_dns_answer(
        self, **kwargs: Unpack[TestDNSAnswerRequestRequestTypeDef]
    ) -> TestDNSAnswerResponseTypeDef:
        """
        Gets the value that Amazon Route 53 returns in response to a DNS request for a
        specified record name and type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/test_dns_answer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#test_dns_answer)
        """

    async def update_health_check(
        self, **kwargs: Unpack[UpdateHealthCheckRequestRequestTypeDef]
    ) -> UpdateHealthCheckResponseTypeDef:
        """
        Updates an existing health check.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/update_health_check.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#update_health_check)
        """

    async def update_hosted_zone_comment(
        self, **kwargs: Unpack[UpdateHostedZoneCommentRequestRequestTypeDef]
    ) -> UpdateHostedZoneCommentResponseTypeDef:
        """
        Updates the comment for a specified hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/update_hosted_zone_comment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#update_hosted_zone_comment)
        """

    async def update_traffic_policy_comment(
        self, **kwargs: Unpack[UpdateTrafficPolicyCommentRequestRequestTypeDef]
    ) -> UpdateTrafficPolicyCommentResponseTypeDef:
        """
        Updates the comment for a specified traffic policy version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/update_traffic_policy_comment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#update_traffic_policy_comment)
        """

    async def update_traffic_policy_instance(
        self, **kwargs: Unpack[UpdateTrafficPolicyInstanceRequestRequestTypeDef]
    ) -> UpdateTrafficPolicyInstanceResponseTypeDef:
        """
        After you submit a <code>UpdateTrafficPolicyInstance</code> request, there's a
        brief delay while Route 53 creates the resource record sets that are specified
        in the traffic policy definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/update_traffic_policy_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#update_traffic_policy_instance)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_cidr_blocks"]) -> ListCidrBlocksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cidr_collections"]
    ) -> ListCidrCollectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cidr_locations"]
    ) -> ListCidrLocationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_health_checks"]
    ) -> ListHealthChecksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_hosted_zones"]
    ) -> ListHostedZonesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_query_logging_configs"]
    ) -> ListQueryLoggingConfigsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_record_sets"]
    ) -> ListResourceRecordSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_vpc_association_authorizations"]
    ) -> ListVPCAssociationAuthorizationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_paginator)
        """

    def get_waiter(
        self, waiter_name: Literal["resource_record_sets_changed"]
    ) -> ResourceRecordSetsChangedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_waiter)
        """

    async def __aenter__(self) -> "Route53Client":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/)
        """
