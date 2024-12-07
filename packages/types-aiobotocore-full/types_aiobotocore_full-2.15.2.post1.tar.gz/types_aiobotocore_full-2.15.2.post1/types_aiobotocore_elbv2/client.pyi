"""
Type annotations for elbv2 service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_elbv2.client import ElasticLoadBalancingv2Client

    session = get_session()
    async with session.create_client("elbv2") as client:
        client: ElasticLoadBalancingv2Client
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    DescribeAccountLimitsPaginator,
    DescribeListenerCertificatesPaginator,
    DescribeListenersPaginator,
    DescribeLoadBalancersPaginator,
    DescribeRulesPaginator,
    DescribeSSLPoliciesPaginator,
    DescribeTargetGroupsPaginator,
)
from .type_defs import (
    AddListenerCertificatesInputRequestTypeDef,
    AddListenerCertificatesOutputTypeDef,
    AddTagsInputRequestTypeDef,
    AddTrustStoreRevocationsInputRequestTypeDef,
    AddTrustStoreRevocationsOutputTypeDef,
    CreateListenerInputRequestTypeDef,
    CreateListenerOutputTypeDef,
    CreateLoadBalancerInputRequestTypeDef,
    CreateLoadBalancerOutputTypeDef,
    CreateRuleInputRequestTypeDef,
    CreateRuleOutputTypeDef,
    CreateTargetGroupInputRequestTypeDef,
    CreateTargetGroupOutputTypeDef,
    CreateTrustStoreInputRequestTypeDef,
    CreateTrustStoreOutputTypeDef,
    DeleteListenerInputRequestTypeDef,
    DeleteLoadBalancerInputRequestTypeDef,
    DeleteRuleInputRequestTypeDef,
    DeleteSharedTrustStoreAssociationInputRequestTypeDef,
    DeleteTargetGroupInputRequestTypeDef,
    DeleteTrustStoreInputRequestTypeDef,
    DeregisterTargetsInputRequestTypeDef,
    DescribeAccountLimitsInputRequestTypeDef,
    DescribeAccountLimitsOutputTypeDef,
    DescribeListenerAttributesInputRequestTypeDef,
    DescribeListenerAttributesOutputTypeDef,
    DescribeListenerCertificatesInputRequestTypeDef,
    DescribeListenerCertificatesOutputTypeDef,
    DescribeListenersInputRequestTypeDef,
    DescribeListenersOutputTypeDef,
    DescribeLoadBalancerAttributesInputRequestTypeDef,
    DescribeLoadBalancerAttributesOutputTypeDef,
    DescribeLoadBalancersInputRequestTypeDef,
    DescribeLoadBalancersOutputTypeDef,
    DescribeRulesInputRequestTypeDef,
    DescribeRulesOutputTypeDef,
    DescribeSSLPoliciesInputRequestTypeDef,
    DescribeSSLPoliciesOutputTypeDef,
    DescribeTagsInputRequestTypeDef,
    DescribeTagsOutputTypeDef,
    DescribeTargetGroupAttributesInputRequestTypeDef,
    DescribeTargetGroupAttributesOutputTypeDef,
    DescribeTargetGroupsInputRequestTypeDef,
    DescribeTargetGroupsOutputTypeDef,
    DescribeTargetHealthInputRequestTypeDef,
    DescribeTargetHealthOutputTypeDef,
    DescribeTrustStoreAssociationsInputRequestTypeDef,
    DescribeTrustStoreAssociationsOutputTypeDef,
    DescribeTrustStoreRevocationsInputRequestTypeDef,
    DescribeTrustStoreRevocationsOutputTypeDef,
    DescribeTrustStoresInputRequestTypeDef,
    DescribeTrustStoresOutputTypeDef,
    GetResourcePolicyInputRequestTypeDef,
    GetResourcePolicyOutputTypeDef,
    GetTrustStoreCaCertificatesBundleInputRequestTypeDef,
    GetTrustStoreCaCertificatesBundleOutputTypeDef,
    GetTrustStoreRevocationContentInputRequestTypeDef,
    GetTrustStoreRevocationContentOutputTypeDef,
    ModifyListenerAttributesInputRequestTypeDef,
    ModifyListenerAttributesOutputTypeDef,
    ModifyListenerInputRequestTypeDef,
    ModifyListenerOutputTypeDef,
    ModifyLoadBalancerAttributesInputRequestTypeDef,
    ModifyLoadBalancerAttributesOutputTypeDef,
    ModifyRuleInputRequestTypeDef,
    ModifyRuleOutputTypeDef,
    ModifyTargetGroupAttributesInputRequestTypeDef,
    ModifyTargetGroupAttributesOutputTypeDef,
    ModifyTargetGroupInputRequestTypeDef,
    ModifyTargetGroupOutputTypeDef,
    ModifyTrustStoreInputRequestTypeDef,
    ModifyTrustStoreOutputTypeDef,
    RegisterTargetsInputRequestTypeDef,
    RemoveListenerCertificatesInputRequestTypeDef,
    RemoveTagsInputRequestTypeDef,
    RemoveTrustStoreRevocationsInputRequestTypeDef,
    SetIpAddressTypeInputRequestTypeDef,
    SetIpAddressTypeOutputTypeDef,
    SetRulePrioritiesInputRequestTypeDef,
    SetRulePrioritiesOutputTypeDef,
    SetSecurityGroupsInputRequestTypeDef,
    SetSecurityGroupsOutputTypeDef,
    SetSubnetsInputRequestTypeDef,
    SetSubnetsOutputTypeDef,
)
from .waiter import (
    LoadBalancerAvailableWaiter,
    LoadBalancerExistsWaiter,
    LoadBalancersDeletedWaiter,
    TargetDeregisteredWaiter,
    TargetInServiceWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ElasticLoadBalancingv2Client",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ALPNPolicyNotSupportedException: Type[BotocoreClientError]
    AllocationIdNotFoundException: Type[BotocoreClientError]
    AvailabilityZoneNotSupportedException: Type[BotocoreClientError]
    CaCertificatesBundleNotFoundException: Type[BotocoreClientError]
    CertificateNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DeleteAssociationSameAccountException: Type[BotocoreClientError]
    DuplicateListenerException: Type[BotocoreClientError]
    DuplicateLoadBalancerNameException: Type[BotocoreClientError]
    DuplicateTagKeysException: Type[BotocoreClientError]
    DuplicateTargetGroupNameException: Type[BotocoreClientError]
    DuplicateTrustStoreNameException: Type[BotocoreClientError]
    HealthUnavailableException: Type[BotocoreClientError]
    IncompatibleProtocolsException: Type[BotocoreClientError]
    InvalidCaCertificatesBundleException: Type[BotocoreClientError]
    InvalidConfigurationRequestException: Type[BotocoreClientError]
    InvalidLoadBalancerActionException: Type[BotocoreClientError]
    InvalidRevocationContentException: Type[BotocoreClientError]
    InvalidSchemeException: Type[BotocoreClientError]
    InvalidSecurityGroupException: Type[BotocoreClientError]
    InvalidSubnetException: Type[BotocoreClientError]
    InvalidTargetException: Type[BotocoreClientError]
    ListenerNotFoundException: Type[BotocoreClientError]
    LoadBalancerNotFoundException: Type[BotocoreClientError]
    OperationNotPermittedException: Type[BotocoreClientError]
    PriorityInUseException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    RevocationContentNotFoundException: Type[BotocoreClientError]
    RevocationIdNotFoundException: Type[BotocoreClientError]
    RuleNotFoundException: Type[BotocoreClientError]
    SSLPolicyNotFoundException: Type[BotocoreClientError]
    SubnetNotFoundException: Type[BotocoreClientError]
    TargetGroupAssociationLimitException: Type[BotocoreClientError]
    TargetGroupNotFoundException: Type[BotocoreClientError]
    TooManyActionsException: Type[BotocoreClientError]
    TooManyCertificatesException: Type[BotocoreClientError]
    TooManyListenersException: Type[BotocoreClientError]
    TooManyLoadBalancersException: Type[BotocoreClientError]
    TooManyRegistrationsForTargetIdException: Type[BotocoreClientError]
    TooManyRulesException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    TooManyTargetGroupsException: Type[BotocoreClientError]
    TooManyTargetsException: Type[BotocoreClientError]
    TooManyTrustStoreRevocationEntriesException: Type[BotocoreClientError]
    TooManyTrustStoresException: Type[BotocoreClientError]
    TooManyUniqueTargetGroupsPerLoadBalancerException: Type[BotocoreClientError]
    TrustStoreAssociationNotFoundException: Type[BotocoreClientError]
    TrustStoreInUseException: Type[BotocoreClientError]
    TrustStoreNotFoundException: Type[BotocoreClientError]
    TrustStoreNotReadyException: Type[BotocoreClientError]
    UnsupportedProtocolException: Type[BotocoreClientError]

class ElasticLoadBalancingv2Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElasticLoadBalancingv2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#close)
        """

    async def add_listener_certificates(
        self, **kwargs: Unpack[AddListenerCertificatesInputRequestTypeDef]
    ) -> AddListenerCertificatesOutputTypeDef:
        """
        Adds the specified SSL server certificate to the certificate list for the
        specified HTTPS or TLS listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/add_listener_certificates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#add_listener_certificates)
        """

    async def add_tags(self, **kwargs: Unpack[AddTagsInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified Elastic Load Balancing resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/add_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#add_tags)
        """

    async def add_trust_store_revocations(
        self, **kwargs: Unpack[AddTrustStoreRevocationsInputRequestTypeDef]
    ) -> AddTrustStoreRevocationsOutputTypeDef:
        """
        Adds the specified revocation file to the specified trust store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/add_trust_store_revocations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#add_trust_store_revocations)
        """

    async def create_listener(
        self, **kwargs: Unpack[CreateListenerInputRequestTypeDef]
    ) -> CreateListenerOutputTypeDef:
        """
        Creates a listener for the specified Application Load Balancer, Network Load
        Balancer, or Gateway Load Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/create_listener.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#create_listener)
        """

    async def create_load_balancer(
        self, **kwargs: Unpack[CreateLoadBalancerInputRequestTypeDef]
    ) -> CreateLoadBalancerOutputTypeDef:
        """
        Creates an Application Load Balancer, Network Load Balancer, or Gateway Load
        Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/create_load_balancer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#create_load_balancer)
        """

    async def create_rule(
        self, **kwargs: Unpack[CreateRuleInputRequestTypeDef]
    ) -> CreateRuleOutputTypeDef:
        """
        Creates a rule for the specified listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/create_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#create_rule)
        """

    async def create_target_group(
        self, **kwargs: Unpack[CreateTargetGroupInputRequestTypeDef]
    ) -> CreateTargetGroupOutputTypeDef:
        """
        Creates a target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/create_target_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#create_target_group)
        """

    async def create_trust_store(
        self, **kwargs: Unpack[CreateTrustStoreInputRequestTypeDef]
    ) -> CreateTrustStoreOutputTypeDef:
        """
        Creates a trust store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/create_trust_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#create_trust_store)
        """

    async def delete_listener(
        self, **kwargs: Unpack[DeleteListenerInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/delete_listener.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#delete_listener)
        """

    async def delete_load_balancer(
        self, **kwargs: Unpack[DeleteLoadBalancerInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified Application Load Balancer, Network Load Balancer, or
        Gateway Load Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/delete_load_balancer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#delete_load_balancer)
        """

    async def delete_rule(self, **kwargs: Unpack[DeleteRuleInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/delete_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#delete_rule)
        """

    async def delete_shared_trust_store_association(
        self, **kwargs: Unpack[DeleteSharedTrustStoreAssociationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a shared trust store association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/delete_shared_trust_store_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#delete_shared_trust_store_association)
        """

    async def delete_target_group(
        self, **kwargs: Unpack[DeleteTargetGroupInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/delete_target_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#delete_target_group)
        """

    async def delete_trust_store(
        self, **kwargs: Unpack[DeleteTrustStoreInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a trust store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/delete_trust_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#delete_trust_store)
        """

    async def deregister_targets(
        self, **kwargs: Unpack[DeregisterTargetsInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deregisters the specified targets from the specified target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/deregister_targets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#deregister_targets)
        """

    async def describe_account_limits(
        self, **kwargs: Unpack[DescribeAccountLimitsInputRequestTypeDef]
    ) -> DescribeAccountLimitsOutputTypeDef:
        """
        Describes the current Elastic Load Balancing resource limits for your Amazon
        Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_account_limits.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_account_limits)
        """

    async def describe_listener_attributes(
        self, **kwargs: Unpack[DescribeListenerAttributesInputRequestTypeDef]
    ) -> DescribeListenerAttributesOutputTypeDef:
        """
        Describes the attributes for the specified listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_listener_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_listener_attributes)
        """

    async def describe_listener_certificates(
        self, **kwargs: Unpack[DescribeListenerCertificatesInputRequestTypeDef]
    ) -> DescribeListenerCertificatesOutputTypeDef:
        """
        Describes the default certificate and the certificate list for the specified
        HTTPS or TLS listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_listener_certificates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_listener_certificates)
        """

    async def describe_listeners(
        self, **kwargs: Unpack[DescribeListenersInputRequestTypeDef]
    ) -> DescribeListenersOutputTypeDef:
        """
        Describes the specified listeners or the listeners for the specified
        Application Load Balancer, Network Load Balancer, or Gateway Load Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_listeners.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_listeners)
        """

    async def describe_load_balancer_attributes(
        self, **kwargs: Unpack[DescribeLoadBalancerAttributesInputRequestTypeDef]
    ) -> DescribeLoadBalancerAttributesOutputTypeDef:
        """
        Describes the attributes for the specified Application Load Balancer, Network
        Load Balancer, or Gateway Load Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_load_balancer_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_load_balancer_attributes)
        """

    async def describe_load_balancers(
        self, **kwargs: Unpack[DescribeLoadBalancersInputRequestTypeDef]
    ) -> DescribeLoadBalancersOutputTypeDef:
        """
        Describes the specified load balancers or all of your load balancers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_load_balancers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_load_balancers)
        """

    async def describe_rules(
        self, **kwargs: Unpack[DescribeRulesInputRequestTypeDef]
    ) -> DescribeRulesOutputTypeDef:
        """
        Describes the specified rules or the rules for the specified listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_rules.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_rules)
        """

    async def describe_ssl_policies(
        self, **kwargs: Unpack[DescribeSSLPoliciesInputRequestTypeDef]
    ) -> DescribeSSLPoliciesOutputTypeDef:
        """
        Describes the specified policies or all policies used for SSL negotiation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_ssl_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_ssl_policies)
        """

    async def describe_tags(
        self, **kwargs: Unpack[DescribeTagsInputRequestTypeDef]
    ) -> DescribeTagsOutputTypeDef:
        """
        Describes the tags for the specified Elastic Load Balancing resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_tags)
        """

    async def describe_target_group_attributes(
        self, **kwargs: Unpack[DescribeTargetGroupAttributesInputRequestTypeDef]
    ) -> DescribeTargetGroupAttributesOutputTypeDef:
        """
        Describes the attributes for the specified target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_target_group_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_target_group_attributes)
        """

    async def describe_target_groups(
        self, **kwargs: Unpack[DescribeTargetGroupsInputRequestTypeDef]
    ) -> DescribeTargetGroupsOutputTypeDef:
        """
        Describes the specified target groups or all of your target groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_target_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_target_groups)
        """

    async def describe_target_health(
        self, **kwargs: Unpack[DescribeTargetHealthInputRequestTypeDef]
    ) -> DescribeTargetHealthOutputTypeDef:
        """
        Describes the health of the specified targets or all of your targets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_target_health.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_target_health)
        """

    async def describe_trust_store_associations(
        self, **kwargs: Unpack[DescribeTrustStoreAssociationsInputRequestTypeDef]
    ) -> DescribeTrustStoreAssociationsOutputTypeDef:
        """
        Describes all resources associated with the specified trust store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_trust_store_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_trust_store_associations)
        """

    async def describe_trust_store_revocations(
        self, **kwargs: Unpack[DescribeTrustStoreRevocationsInputRequestTypeDef]
    ) -> DescribeTrustStoreRevocationsOutputTypeDef:
        """
        Describes the revocation files in use by the specified trust store or
        revocation files.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_trust_store_revocations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_trust_store_revocations)
        """

    async def describe_trust_stores(
        self, **kwargs: Unpack[DescribeTrustStoresInputRequestTypeDef]
    ) -> DescribeTrustStoresOutputTypeDef:
        """
        Describes all trust stores for the specified account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_trust_stores.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_trust_stores)
        """

    async def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyInputRequestTypeDef]
    ) -> GetResourcePolicyOutputTypeDef:
        """
        Retrieves the resource policy for a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/get_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_resource_policy)
        """

    async def get_trust_store_ca_certificates_bundle(
        self, **kwargs: Unpack[GetTrustStoreCaCertificatesBundleInputRequestTypeDef]
    ) -> GetTrustStoreCaCertificatesBundleOutputTypeDef:
        """
        Retrieves the ca certificate bundle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/get_trust_store_ca_certificates_bundle.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_trust_store_ca_certificates_bundle)
        """

    async def get_trust_store_revocation_content(
        self, **kwargs: Unpack[GetTrustStoreRevocationContentInputRequestTypeDef]
    ) -> GetTrustStoreRevocationContentOutputTypeDef:
        """
        Retrieves the specified revocation file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/get_trust_store_revocation_content.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_trust_store_revocation_content)
        """

    async def modify_listener(
        self, **kwargs: Unpack[ModifyListenerInputRequestTypeDef]
    ) -> ModifyListenerOutputTypeDef:
        """
        Replaces the specified properties of the specified listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/modify_listener.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#modify_listener)
        """

    async def modify_listener_attributes(
        self, **kwargs: Unpack[ModifyListenerAttributesInputRequestTypeDef]
    ) -> ModifyListenerAttributesOutputTypeDef:
        """
        Modifies the specified attributes of the specified listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/modify_listener_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#modify_listener_attributes)
        """

    async def modify_load_balancer_attributes(
        self, **kwargs: Unpack[ModifyLoadBalancerAttributesInputRequestTypeDef]
    ) -> ModifyLoadBalancerAttributesOutputTypeDef:
        """
        Modifies the specified attributes of the specified Application Load Balancer,
        Network Load Balancer, or Gateway Load Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/modify_load_balancer_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#modify_load_balancer_attributes)
        """

    async def modify_rule(
        self, **kwargs: Unpack[ModifyRuleInputRequestTypeDef]
    ) -> ModifyRuleOutputTypeDef:
        """
        Replaces the specified properties of the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/modify_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#modify_rule)
        """

    async def modify_target_group(
        self, **kwargs: Unpack[ModifyTargetGroupInputRequestTypeDef]
    ) -> ModifyTargetGroupOutputTypeDef:
        """
        Modifies the health checks used when evaluating the health state of the targets
        in the specified target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/modify_target_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#modify_target_group)
        """

    async def modify_target_group_attributes(
        self, **kwargs: Unpack[ModifyTargetGroupAttributesInputRequestTypeDef]
    ) -> ModifyTargetGroupAttributesOutputTypeDef:
        """
        Modifies the specified attributes of the specified target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/modify_target_group_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#modify_target_group_attributes)
        """

    async def modify_trust_store(
        self, **kwargs: Unpack[ModifyTrustStoreInputRequestTypeDef]
    ) -> ModifyTrustStoreOutputTypeDef:
        """
        Update the ca certificate bundle for the specified trust store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/modify_trust_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#modify_trust_store)
        """

    async def register_targets(
        self, **kwargs: Unpack[RegisterTargetsInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Registers the specified targets with the specified target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/register_targets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#register_targets)
        """

    async def remove_listener_certificates(
        self, **kwargs: Unpack[RemoveListenerCertificatesInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified certificate from the certificate list for the specified
        HTTPS or TLS listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/remove_listener_certificates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#remove_listener_certificates)
        """

    async def remove_tags(self, **kwargs: Unpack[RemoveTagsInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified Elastic Load Balancing resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/remove_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#remove_tags)
        """

    async def remove_trust_store_revocations(
        self, **kwargs: Unpack[RemoveTrustStoreRevocationsInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified revocation file from the specified trust store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/remove_trust_store_revocations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#remove_trust_store_revocations)
        """

    async def set_ip_address_type(
        self, **kwargs: Unpack[SetIpAddressTypeInputRequestTypeDef]
    ) -> SetIpAddressTypeOutputTypeDef:
        """
        Sets the type of IP addresses used by the subnets of the specified load
        balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/set_ip_address_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#set_ip_address_type)
        """

    async def set_rule_priorities(
        self, **kwargs: Unpack[SetRulePrioritiesInputRequestTypeDef]
    ) -> SetRulePrioritiesOutputTypeDef:
        """
        Sets the priorities of the specified rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/set_rule_priorities.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#set_rule_priorities)
        """

    async def set_security_groups(
        self, **kwargs: Unpack[SetSecurityGroupsInputRequestTypeDef]
    ) -> SetSecurityGroupsOutputTypeDef:
        """
        Associates the specified security groups with the specified Application Load
        Balancer or Network Load Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/set_security_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#set_security_groups)
        """

    async def set_subnets(
        self, **kwargs: Unpack[SetSubnetsInputRequestTypeDef]
    ) -> SetSubnetsOutputTypeDef:
        """
        Enables the Availability Zones for the specified public subnets for the
        specified Application Load Balancer, Network Load Balancer or Gateway Load
        Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/set_subnets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#set_subnets)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_account_limits"]
    ) -> DescribeAccountLimitsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_listener_certificates"]
    ) -> DescribeListenerCertificatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_listeners"]
    ) -> DescribeListenersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_load_balancers"]
    ) -> DescribeLoadBalancersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_rules"]) -> DescribeRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_ssl_policies"]
    ) -> DescribeSSLPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_target_groups"]
    ) -> DescribeTargetGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["load_balancer_available"]
    ) -> LoadBalancerAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["load_balancer_exists"]) -> LoadBalancerExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["load_balancers_deleted"]
    ) -> LoadBalancersDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["target_deregistered"]) -> TargetDeregisteredWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["target_in_service"]) -> TargetInServiceWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_waiter)
        """

    async def __aenter__(self) -> "ElasticLoadBalancingv2Client":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/)
        """
