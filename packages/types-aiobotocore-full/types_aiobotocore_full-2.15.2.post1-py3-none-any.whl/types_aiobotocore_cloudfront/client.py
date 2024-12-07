"""
Type annotations for cloudfront service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudfront.client import CloudFrontClient

    session = get_session()
    async with session.create_client("cloudfront") as client:
        client: CloudFrontClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListCloudFrontOriginAccessIdentitiesPaginator,
    ListDistributionsPaginator,
    ListInvalidationsPaginator,
    ListKeyValueStoresPaginator,
    ListStreamingDistributionsPaginator,
)
from .type_defs import (
    AssociateAliasRequestRequestTypeDef,
    CopyDistributionRequestRequestTypeDef,
    CopyDistributionResultTypeDef,
    CreateCachePolicyRequestRequestTypeDef,
    CreateCachePolicyResultTypeDef,
    CreateCloudFrontOriginAccessIdentityRequestRequestTypeDef,
    CreateCloudFrontOriginAccessIdentityResultTypeDef,
    CreateContinuousDeploymentPolicyRequestRequestTypeDef,
    CreateContinuousDeploymentPolicyResultTypeDef,
    CreateDistributionRequestRequestTypeDef,
    CreateDistributionResultTypeDef,
    CreateDistributionWithTagsRequestRequestTypeDef,
    CreateDistributionWithTagsResultTypeDef,
    CreateFieldLevelEncryptionConfigRequestRequestTypeDef,
    CreateFieldLevelEncryptionConfigResultTypeDef,
    CreateFieldLevelEncryptionProfileRequestRequestTypeDef,
    CreateFieldLevelEncryptionProfileResultTypeDef,
    CreateFunctionRequestRequestTypeDef,
    CreateFunctionResultTypeDef,
    CreateInvalidationRequestRequestTypeDef,
    CreateInvalidationResultTypeDef,
    CreateKeyGroupRequestRequestTypeDef,
    CreateKeyGroupResultTypeDef,
    CreateKeyValueStoreRequestRequestTypeDef,
    CreateKeyValueStoreResultTypeDef,
    CreateMonitoringSubscriptionRequestRequestTypeDef,
    CreateMonitoringSubscriptionResultTypeDef,
    CreateOriginAccessControlRequestRequestTypeDef,
    CreateOriginAccessControlResultTypeDef,
    CreateOriginRequestPolicyRequestRequestTypeDef,
    CreateOriginRequestPolicyResultTypeDef,
    CreatePublicKeyRequestRequestTypeDef,
    CreatePublicKeyResultTypeDef,
    CreateRealtimeLogConfigRequestRequestTypeDef,
    CreateRealtimeLogConfigResultTypeDef,
    CreateResponseHeadersPolicyRequestRequestTypeDef,
    CreateResponseHeadersPolicyResultTypeDef,
    CreateStreamingDistributionRequestRequestTypeDef,
    CreateStreamingDistributionResultTypeDef,
    CreateStreamingDistributionWithTagsRequestRequestTypeDef,
    CreateStreamingDistributionWithTagsResultTypeDef,
    DeleteCachePolicyRequestRequestTypeDef,
    DeleteCloudFrontOriginAccessIdentityRequestRequestTypeDef,
    DeleteContinuousDeploymentPolicyRequestRequestTypeDef,
    DeleteDistributionRequestRequestTypeDef,
    DeleteFieldLevelEncryptionConfigRequestRequestTypeDef,
    DeleteFieldLevelEncryptionProfileRequestRequestTypeDef,
    DeleteFunctionRequestRequestTypeDef,
    DeleteKeyGroupRequestRequestTypeDef,
    DeleteKeyValueStoreRequestRequestTypeDef,
    DeleteMonitoringSubscriptionRequestRequestTypeDef,
    DeleteOriginAccessControlRequestRequestTypeDef,
    DeleteOriginRequestPolicyRequestRequestTypeDef,
    DeletePublicKeyRequestRequestTypeDef,
    DeleteRealtimeLogConfigRequestRequestTypeDef,
    DeleteResponseHeadersPolicyRequestRequestTypeDef,
    DeleteStreamingDistributionRequestRequestTypeDef,
    DescribeFunctionRequestRequestTypeDef,
    DescribeFunctionResultTypeDef,
    DescribeKeyValueStoreRequestRequestTypeDef,
    DescribeKeyValueStoreResultTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCachePolicyConfigRequestRequestTypeDef,
    GetCachePolicyConfigResultTypeDef,
    GetCachePolicyRequestRequestTypeDef,
    GetCachePolicyResultTypeDef,
    GetCloudFrontOriginAccessIdentityConfigRequestRequestTypeDef,
    GetCloudFrontOriginAccessIdentityConfigResultTypeDef,
    GetCloudFrontOriginAccessIdentityRequestRequestTypeDef,
    GetCloudFrontOriginAccessIdentityResultTypeDef,
    GetContinuousDeploymentPolicyConfigRequestRequestTypeDef,
    GetContinuousDeploymentPolicyConfigResultTypeDef,
    GetContinuousDeploymentPolicyRequestRequestTypeDef,
    GetContinuousDeploymentPolicyResultTypeDef,
    GetDistributionConfigRequestRequestTypeDef,
    GetDistributionConfigResultTypeDef,
    GetDistributionRequestRequestTypeDef,
    GetDistributionResultTypeDef,
    GetFieldLevelEncryptionConfigRequestRequestTypeDef,
    GetFieldLevelEncryptionConfigResultTypeDef,
    GetFieldLevelEncryptionProfileConfigRequestRequestTypeDef,
    GetFieldLevelEncryptionProfileConfigResultTypeDef,
    GetFieldLevelEncryptionProfileRequestRequestTypeDef,
    GetFieldLevelEncryptionProfileResultTypeDef,
    GetFieldLevelEncryptionRequestRequestTypeDef,
    GetFieldLevelEncryptionResultTypeDef,
    GetFunctionRequestRequestTypeDef,
    GetFunctionResultTypeDef,
    GetInvalidationRequestRequestTypeDef,
    GetInvalidationResultTypeDef,
    GetKeyGroupConfigRequestRequestTypeDef,
    GetKeyGroupConfigResultTypeDef,
    GetKeyGroupRequestRequestTypeDef,
    GetKeyGroupResultTypeDef,
    GetMonitoringSubscriptionRequestRequestTypeDef,
    GetMonitoringSubscriptionResultTypeDef,
    GetOriginAccessControlConfigRequestRequestTypeDef,
    GetOriginAccessControlConfigResultTypeDef,
    GetOriginAccessControlRequestRequestTypeDef,
    GetOriginAccessControlResultTypeDef,
    GetOriginRequestPolicyConfigRequestRequestTypeDef,
    GetOriginRequestPolicyConfigResultTypeDef,
    GetOriginRequestPolicyRequestRequestTypeDef,
    GetOriginRequestPolicyResultTypeDef,
    GetPublicKeyConfigRequestRequestTypeDef,
    GetPublicKeyConfigResultTypeDef,
    GetPublicKeyRequestRequestTypeDef,
    GetPublicKeyResultTypeDef,
    GetRealtimeLogConfigRequestRequestTypeDef,
    GetRealtimeLogConfigResultTypeDef,
    GetResponseHeadersPolicyConfigRequestRequestTypeDef,
    GetResponseHeadersPolicyConfigResultTypeDef,
    GetResponseHeadersPolicyRequestRequestTypeDef,
    GetResponseHeadersPolicyResultTypeDef,
    GetStreamingDistributionConfigRequestRequestTypeDef,
    GetStreamingDistributionConfigResultTypeDef,
    GetStreamingDistributionRequestRequestTypeDef,
    GetStreamingDistributionResultTypeDef,
    ListCachePoliciesRequestRequestTypeDef,
    ListCachePoliciesResultTypeDef,
    ListCloudFrontOriginAccessIdentitiesRequestRequestTypeDef,
    ListCloudFrontOriginAccessIdentitiesResultTypeDef,
    ListConflictingAliasesRequestRequestTypeDef,
    ListConflictingAliasesResultTypeDef,
    ListContinuousDeploymentPoliciesRequestRequestTypeDef,
    ListContinuousDeploymentPoliciesResultTypeDef,
    ListDistributionsByCachePolicyIdRequestRequestTypeDef,
    ListDistributionsByCachePolicyIdResultTypeDef,
    ListDistributionsByKeyGroupRequestRequestTypeDef,
    ListDistributionsByKeyGroupResultTypeDef,
    ListDistributionsByOriginRequestPolicyIdRequestRequestTypeDef,
    ListDistributionsByOriginRequestPolicyIdResultTypeDef,
    ListDistributionsByRealtimeLogConfigRequestRequestTypeDef,
    ListDistributionsByRealtimeLogConfigResultTypeDef,
    ListDistributionsByResponseHeadersPolicyIdRequestRequestTypeDef,
    ListDistributionsByResponseHeadersPolicyIdResultTypeDef,
    ListDistributionsByWebACLIdRequestRequestTypeDef,
    ListDistributionsByWebACLIdResultTypeDef,
    ListDistributionsRequestRequestTypeDef,
    ListDistributionsResultTypeDef,
    ListFieldLevelEncryptionConfigsRequestRequestTypeDef,
    ListFieldLevelEncryptionConfigsResultTypeDef,
    ListFieldLevelEncryptionProfilesRequestRequestTypeDef,
    ListFieldLevelEncryptionProfilesResultTypeDef,
    ListFunctionsRequestRequestTypeDef,
    ListFunctionsResultTypeDef,
    ListInvalidationsRequestRequestTypeDef,
    ListInvalidationsResultTypeDef,
    ListKeyGroupsRequestRequestTypeDef,
    ListKeyGroupsResultTypeDef,
    ListKeyValueStoresRequestRequestTypeDef,
    ListKeyValueStoresResultTypeDef,
    ListOriginAccessControlsRequestRequestTypeDef,
    ListOriginAccessControlsResultTypeDef,
    ListOriginRequestPoliciesRequestRequestTypeDef,
    ListOriginRequestPoliciesResultTypeDef,
    ListPublicKeysRequestRequestTypeDef,
    ListPublicKeysResultTypeDef,
    ListRealtimeLogConfigsRequestRequestTypeDef,
    ListRealtimeLogConfigsResultTypeDef,
    ListResponseHeadersPoliciesRequestRequestTypeDef,
    ListResponseHeadersPoliciesResultTypeDef,
    ListStreamingDistributionsRequestRequestTypeDef,
    ListStreamingDistributionsResultTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResultTypeDef,
    PublishFunctionRequestRequestTypeDef,
    PublishFunctionResultTypeDef,
    TagResourceRequestRequestTypeDef,
    TestFunctionRequestRequestTypeDef,
    TestFunctionResultTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateCachePolicyRequestRequestTypeDef,
    UpdateCachePolicyResultTypeDef,
    UpdateCloudFrontOriginAccessIdentityRequestRequestTypeDef,
    UpdateCloudFrontOriginAccessIdentityResultTypeDef,
    UpdateContinuousDeploymentPolicyRequestRequestTypeDef,
    UpdateContinuousDeploymentPolicyResultTypeDef,
    UpdateDistributionRequestRequestTypeDef,
    UpdateDistributionResultTypeDef,
    UpdateDistributionWithStagingConfigRequestRequestTypeDef,
    UpdateDistributionWithStagingConfigResultTypeDef,
    UpdateFieldLevelEncryptionConfigRequestRequestTypeDef,
    UpdateFieldLevelEncryptionConfigResultTypeDef,
    UpdateFieldLevelEncryptionProfileRequestRequestTypeDef,
    UpdateFieldLevelEncryptionProfileResultTypeDef,
    UpdateFunctionRequestRequestTypeDef,
    UpdateFunctionResultTypeDef,
    UpdateKeyGroupRequestRequestTypeDef,
    UpdateKeyGroupResultTypeDef,
    UpdateKeyValueStoreRequestRequestTypeDef,
    UpdateKeyValueStoreResultTypeDef,
    UpdateOriginAccessControlRequestRequestTypeDef,
    UpdateOriginAccessControlResultTypeDef,
    UpdateOriginRequestPolicyRequestRequestTypeDef,
    UpdateOriginRequestPolicyResultTypeDef,
    UpdatePublicKeyRequestRequestTypeDef,
    UpdatePublicKeyResultTypeDef,
    UpdateRealtimeLogConfigRequestRequestTypeDef,
    UpdateRealtimeLogConfigResultTypeDef,
    UpdateResponseHeadersPolicyRequestRequestTypeDef,
    UpdateResponseHeadersPolicyResultTypeDef,
    UpdateStreamingDistributionRequestRequestTypeDef,
    UpdateStreamingDistributionResultTypeDef,
)
from .waiter import (
    DistributionDeployedWaiter,
    InvalidationCompletedWaiter,
    StreamingDistributionDeployedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("CloudFrontClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDenied: Type[BotocoreClientError]
    BatchTooLarge: Type[BotocoreClientError]
    CNAMEAlreadyExists: Type[BotocoreClientError]
    CachePolicyAlreadyExists: Type[BotocoreClientError]
    CachePolicyInUse: Type[BotocoreClientError]
    CannotChangeImmutablePublicKeyFields: Type[BotocoreClientError]
    CannotDeleteEntityWhileInUse: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    CloudFrontOriginAccessIdentityAlreadyExists: Type[BotocoreClientError]
    CloudFrontOriginAccessIdentityInUse: Type[BotocoreClientError]
    ContinuousDeploymentPolicyAlreadyExists: Type[BotocoreClientError]
    ContinuousDeploymentPolicyInUse: Type[BotocoreClientError]
    DistributionAlreadyExists: Type[BotocoreClientError]
    DistributionNotDisabled: Type[BotocoreClientError]
    EntityAlreadyExists: Type[BotocoreClientError]
    EntityLimitExceeded: Type[BotocoreClientError]
    EntityNotFound: Type[BotocoreClientError]
    EntitySizeLimitExceeded: Type[BotocoreClientError]
    FieldLevelEncryptionConfigAlreadyExists: Type[BotocoreClientError]
    FieldLevelEncryptionConfigInUse: Type[BotocoreClientError]
    FieldLevelEncryptionProfileAlreadyExists: Type[BotocoreClientError]
    FieldLevelEncryptionProfileInUse: Type[BotocoreClientError]
    FieldLevelEncryptionProfileSizeExceeded: Type[BotocoreClientError]
    FunctionAlreadyExists: Type[BotocoreClientError]
    FunctionInUse: Type[BotocoreClientError]
    FunctionSizeLimitExceeded: Type[BotocoreClientError]
    IllegalDelete: Type[BotocoreClientError]
    IllegalFieldLevelEncryptionConfigAssociationWithCacheBehavior: Type[BotocoreClientError]
    IllegalOriginAccessConfiguration: Type[BotocoreClientError]
    IllegalUpdate: Type[BotocoreClientError]
    InconsistentQuantities: Type[BotocoreClientError]
    InvalidArgument: Type[BotocoreClientError]
    InvalidDefaultRootObject: Type[BotocoreClientError]
    InvalidDomainNameForOriginAccessControl: Type[BotocoreClientError]
    InvalidErrorCode: Type[BotocoreClientError]
    InvalidForwardCookies: Type[BotocoreClientError]
    InvalidFunctionAssociation: Type[BotocoreClientError]
    InvalidGeoRestrictionParameter: Type[BotocoreClientError]
    InvalidHeadersForS3Origin: Type[BotocoreClientError]
    InvalidIfMatchVersion: Type[BotocoreClientError]
    InvalidLambdaFunctionAssociation: Type[BotocoreClientError]
    InvalidLocationCode: Type[BotocoreClientError]
    InvalidMinimumProtocolVersion: Type[BotocoreClientError]
    InvalidOrigin: Type[BotocoreClientError]
    InvalidOriginAccessControl: Type[BotocoreClientError]
    InvalidOriginAccessIdentity: Type[BotocoreClientError]
    InvalidOriginKeepaliveTimeout: Type[BotocoreClientError]
    InvalidOriginReadTimeout: Type[BotocoreClientError]
    InvalidProtocolSettings: Type[BotocoreClientError]
    InvalidQueryStringParameters: Type[BotocoreClientError]
    InvalidRelativePath: Type[BotocoreClientError]
    InvalidRequiredProtocol: Type[BotocoreClientError]
    InvalidResponseCode: Type[BotocoreClientError]
    InvalidTTLOrder: Type[BotocoreClientError]
    InvalidTagging: Type[BotocoreClientError]
    InvalidViewerCertificate: Type[BotocoreClientError]
    InvalidWebACLId: Type[BotocoreClientError]
    KeyGroupAlreadyExists: Type[BotocoreClientError]
    MissingBody: Type[BotocoreClientError]
    MonitoringSubscriptionAlreadyExists: Type[BotocoreClientError]
    NoSuchCachePolicy: Type[BotocoreClientError]
    NoSuchCloudFrontOriginAccessIdentity: Type[BotocoreClientError]
    NoSuchContinuousDeploymentPolicy: Type[BotocoreClientError]
    NoSuchDistribution: Type[BotocoreClientError]
    NoSuchFieldLevelEncryptionConfig: Type[BotocoreClientError]
    NoSuchFieldLevelEncryptionProfile: Type[BotocoreClientError]
    NoSuchFunctionExists: Type[BotocoreClientError]
    NoSuchInvalidation: Type[BotocoreClientError]
    NoSuchMonitoringSubscription: Type[BotocoreClientError]
    NoSuchOrigin: Type[BotocoreClientError]
    NoSuchOriginAccessControl: Type[BotocoreClientError]
    NoSuchOriginRequestPolicy: Type[BotocoreClientError]
    NoSuchPublicKey: Type[BotocoreClientError]
    NoSuchRealtimeLogConfig: Type[BotocoreClientError]
    NoSuchResource: Type[BotocoreClientError]
    NoSuchResponseHeadersPolicy: Type[BotocoreClientError]
    NoSuchStreamingDistribution: Type[BotocoreClientError]
    OriginAccessControlAlreadyExists: Type[BotocoreClientError]
    OriginAccessControlInUse: Type[BotocoreClientError]
    OriginRequestPolicyAlreadyExists: Type[BotocoreClientError]
    OriginRequestPolicyInUse: Type[BotocoreClientError]
    PreconditionFailed: Type[BotocoreClientError]
    PublicKeyAlreadyExists: Type[BotocoreClientError]
    PublicKeyInUse: Type[BotocoreClientError]
    QueryArgProfileEmpty: Type[BotocoreClientError]
    RealtimeLogConfigAlreadyExists: Type[BotocoreClientError]
    RealtimeLogConfigInUse: Type[BotocoreClientError]
    RealtimeLogConfigOwnerMismatch: Type[BotocoreClientError]
    ResourceInUse: Type[BotocoreClientError]
    ResponseHeadersPolicyAlreadyExists: Type[BotocoreClientError]
    ResponseHeadersPolicyInUse: Type[BotocoreClientError]
    StagingDistributionInUse: Type[BotocoreClientError]
    StreamingDistributionAlreadyExists: Type[BotocoreClientError]
    StreamingDistributionNotDisabled: Type[BotocoreClientError]
    TestFunctionFailed: Type[BotocoreClientError]
    TooLongCSPInResponseHeadersPolicy: Type[BotocoreClientError]
    TooManyCacheBehaviors: Type[BotocoreClientError]
    TooManyCachePolicies: Type[BotocoreClientError]
    TooManyCertificates: Type[BotocoreClientError]
    TooManyCloudFrontOriginAccessIdentities: Type[BotocoreClientError]
    TooManyContinuousDeploymentPolicies: Type[BotocoreClientError]
    TooManyCookieNamesInWhiteList: Type[BotocoreClientError]
    TooManyCookiesInCachePolicy: Type[BotocoreClientError]
    TooManyCookiesInOriginRequestPolicy: Type[BotocoreClientError]
    TooManyCustomHeadersInResponseHeadersPolicy: Type[BotocoreClientError]
    TooManyDistributionCNAMEs: Type[BotocoreClientError]
    TooManyDistributions: Type[BotocoreClientError]
    TooManyDistributionsAssociatedToCachePolicy: Type[BotocoreClientError]
    TooManyDistributionsAssociatedToFieldLevelEncryptionConfig: Type[BotocoreClientError]
    TooManyDistributionsAssociatedToKeyGroup: Type[BotocoreClientError]
    TooManyDistributionsAssociatedToOriginAccessControl: Type[BotocoreClientError]
    TooManyDistributionsAssociatedToOriginRequestPolicy: Type[BotocoreClientError]
    TooManyDistributionsAssociatedToResponseHeadersPolicy: Type[BotocoreClientError]
    TooManyDistributionsWithFunctionAssociations: Type[BotocoreClientError]
    TooManyDistributionsWithLambdaAssociations: Type[BotocoreClientError]
    TooManyDistributionsWithSingleFunctionARN: Type[BotocoreClientError]
    TooManyFieldLevelEncryptionConfigs: Type[BotocoreClientError]
    TooManyFieldLevelEncryptionContentTypeProfiles: Type[BotocoreClientError]
    TooManyFieldLevelEncryptionEncryptionEntities: Type[BotocoreClientError]
    TooManyFieldLevelEncryptionFieldPatterns: Type[BotocoreClientError]
    TooManyFieldLevelEncryptionProfiles: Type[BotocoreClientError]
    TooManyFieldLevelEncryptionQueryArgProfiles: Type[BotocoreClientError]
    TooManyFunctionAssociations: Type[BotocoreClientError]
    TooManyFunctions: Type[BotocoreClientError]
    TooManyHeadersInCachePolicy: Type[BotocoreClientError]
    TooManyHeadersInForwardedValues: Type[BotocoreClientError]
    TooManyHeadersInOriginRequestPolicy: Type[BotocoreClientError]
    TooManyInvalidationsInProgress: Type[BotocoreClientError]
    TooManyKeyGroups: Type[BotocoreClientError]
    TooManyKeyGroupsAssociatedToDistribution: Type[BotocoreClientError]
    TooManyLambdaFunctionAssociations: Type[BotocoreClientError]
    TooManyOriginAccessControls: Type[BotocoreClientError]
    TooManyOriginCustomHeaders: Type[BotocoreClientError]
    TooManyOriginGroupsPerDistribution: Type[BotocoreClientError]
    TooManyOriginRequestPolicies: Type[BotocoreClientError]
    TooManyOrigins: Type[BotocoreClientError]
    TooManyPublicKeys: Type[BotocoreClientError]
    TooManyPublicKeysInKeyGroup: Type[BotocoreClientError]
    TooManyQueryStringParameters: Type[BotocoreClientError]
    TooManyQueryStringsInCachePolicy: Type[BotocoreClientError]
    TooManyQueryStringsInOriginRequestPolicy: Type[BotocoreClientError]
    TooManyRealtimeLogConfigs: Type[BotocoreClientError]
    TooManyRemoveHeadersInResponseHeadersPolicy: Type[BotocoreClientError]
    TooManyResponseHeadersPolicies: Type[BotocoreClientError]
    TooManyStreamingDistributionCNAMEs: Type[BotocoreClientError]
    TooManyStreamingDistributions: Type[BotocoreClientError]
    TooManyTrustedSigners: Type[BotocoreClientError]
    TrustedKeyGroupDoesNotExist: Type[BotocoreClientError]
    TrustedSignerDoesNotExist: Type[BotocoreClientError]
    UnsupportedOperation: Type[BotocoreClientError]


class CloudFrontClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#CloudFront.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudFrontClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#CloudFront.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#close)
        """

    async def associate_alias(
        self, **kwargs: Unpack[AssociateAliasRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates an alias (also known as a CNAME or an alternate domain name) with a
        CloudFront distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/associate_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#associate_alias)
        """

    async def copy_distribution(
        self, **kwargs: Unpack[CopyDistributionRequestRequestTypeDef]
    ) -> CopyDistributionResultTypeDef:
        """
        Creates a staging distribution using the configuration of the provided primary
        distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/copy_distribution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#copy_distribution)
        """

    async def create_cache_policy(
        self, **kwargs: Unpack[CreateCachePolicyRequestRequestTypeDef]
    ) -> CreateCachePolicyResultTypeDef:
        """
        Creates a cache policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_cache_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_cache_policy)
        """

    async def create_cloud_front_origin_access_identity(
        self, **kwargs: Unpack[CreateCloudFrontOriginAccessIdentityRequestRequestTypeDef]
    ) -> CreateCloudFrontOriginAccessIdentityResultTypeDef:
        """
        Creates a new origin access identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_cloud_front_origin_access_identity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_cloud_front_origin_access_identity)
        """

    async def create_continuous_deployment_policy(
        self, **kwargs: Unpack[CreateContinuousDeploymentPolicyRequestRequestTypeDef]
    ) -> CreateContinuousDeploymentPolicyResultTypeDef:
        """
        Creates a continuous deployment policy that distributes traffic for a custom
        domain name to two different CloudFront distributions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_continuous_deployment_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_continuous_deployment_policy)
        """

    async def create_distribution(
        self, **kwargs: Unpack[CreateDistributionRequestRequestTypeDef]
    ) -> CreateDistributionResultTypeDef:
        """
        Creates a CloudFront distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_distribution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_distribution)
        """

    async def create_distribution_with_tags(
        self, **kwargs: Unpack[CreateDistributionWithTagsRequestRequestTypeDef]
    ) -> CreateDistributionWithTagsResultTypeDef:
        """
        Create a new distribution with tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_distribution_with_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_distribution_with_tags)
        """

    async def create_field_level_encryption_config(
        self, **kwargs: Unpack[CreateFieldLevelEncryptionConfigRequestRequestTypeDef]
    ) -> CreateFieldLevelEncryptionConfigResultTypeDef:
        """
        Create a new field-level encryption configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_field_level_encryption_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_field_level_encryption_config)
        """

    async def create_field_level_encryption_profile(
        self, **kwargs: Unpack[CreateFieldLevelEncryptionProfileRequestRequestTypeDef]
    ) -> CreateFieldLevelEncryptionProfileResultTypeDef:
        """
        Create a field-level encryption profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_field_level_encryption_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_field_level_encryption_profile)
        """

    async def create_function(
        self, **kwargs: Unpack[CreateFunctionRequestRequestTypeDef]
    ) -> CreateFunctionResultTypeDef:
        """
        Creates a CloudFront function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_function.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_function)
        """

    async def create_invalidation(
        self, **kwargs: Unpack[CreateInvalidationRequestRequestTypeDef]
    ) -> CreateInvalidationResultTypeDef:
        """
        Create a new invalidation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_invalidation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_invalidation)
        """

    async def create_key_group(
        self, **kwargs: Unpack[CreateKeyGroupRequestRequestTypeDef]
    ) -> CreateKeyGroupResultTypeDef:
        """
        Creates a key group that you can use with <a
        href="https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html">CloudFront
        signed URLs and signed cookies</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_key_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_key_group)
        """

    async def create_key_value_store(
        self, **kwargs: Unpack[CreateKeyValueStoreRequestRequestTypeDef]
    ) -> CreateKeyValueStoreResultTypeDef:
        """
        Specifies the key value store resource to add to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_key_value_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_key_value_store)
        """

    async def create_monitoring_subscription(
        self, **kwargs: Unpack[CreateMonitoringSubscriptionRequestRequestTypeDef]
    ) -> CreateMonitoringSubscriptionResultTypeDef:
        """
        Enables additional CloudWatch metrics for the specified CloudFront distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_monitoring_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_monitoring_subscription)
        """

    async def create_origin_access_control(
        self, **kwargs: Unpack[CreateOriginAccessControlRequestRequestTypeDef]
    ) -> CreateOriginAccessControlResultTypeDef:
        """
        Creates a new origin access control in CloudFront.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_origin_access_control.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_origin_access_control)
        """

    async def create_origin_request_policy(
        self, **kwargs: Unpack[CreateOriginRequestPolicyRequestRequestTypeDef]
    ) -> CreateOriginRequestPolicyResultTypeDef:
        """
        Creates an origin request policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_origin_request_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_origin_request_policy)
        """

    async def create_public_key(
        self, **kwargs: Unpack[CreatePublicKeyRequestRequestTypeDef]
    ) -> CreatePublicKeyResultTypeDef:
        """
        Uploads a public key to CloudFront that you can use with <a
        href="https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html">signed
        URLs and signed cookies</a>, or with <a
        href="https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/field-level-encryption....

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_public_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_public_key)
        """

    async def create_realtime_log_config(
        self, **kwargs: Unpack[CreateRealtimeLogConfigRequestRequestTypeDef]
    ) -> CreateRealtimeLogConfigResultTypeDef:
        """
        Creates a real-time log configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_realtime_log_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_realtime_log_config)
        """

    async def create_response_headers_policy(
        self, **kwargs: Unpack[CreateResponseHeadersPolicyRequestRequestTypeDef]
    ) -> CreateResponseHeadersPolicyResultTypeDef:
        """
        Creates a response headers policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_response_headers_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_response_headers_policy)
        """

    async def create_streaming_distribution(
        self, **kwargs: Unpack[CreateStreamingDistributionRequestRequestTypeDef]
    ) -> CreateStreamingDistributionResultTypeDef:
        """
        This API is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_streaming_distribution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_streaming_distribution)
        """

    async def create_streaming_distribution_with_tags(
        self, **kwargs: Unpack[CreateStreamingDistributionWithTagsRequestRequestTypeDef]
    ) -> CreateStreamingDistributionWithTagsResultTypeDef:
        """
        This API is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_streaming_distribution_with_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#create_streaming_distribution_with_tags)
        """

    async def delete_cache_policy(
        self, **kwargs: Unpack[DeleteCachePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a cache policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/delete_cache_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#delete_cache_policy)
        """

    async def delete_cloud_front_origin_access_identity(
        self, **kwargs: Unpack[DeleteCloudFrontOriginAccessIdentityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete an origin access identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/delete_cloud_front_origin_access_identity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#delete_cloud_front_origin_access_identity)
        """

    async def delete_continuous_deployment_policy(
        self, **kwargs: Unpack[DeleteContinuousDeploymentPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a continuous deployment policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/delete_continuous_deployment_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#delete_continuous_deployment_policy)
        """

    async def delete_distribution(
        self, **kwargs: Unpack[DeleteDistributionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/delete_distribution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#delete_distribution)
        """

    async def delete_field_level_encryption_config(
        self, **kwargs: Unpack[DeleteFieldLevelEncryptionConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove a field-level encryption configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/delete_field_level_encryption_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#delete_field_level_encryption_config)
        """

    async def delete_field_level_encryption_profile(
        self, **kwargs: Unpack[DeleteFieldLevelEncryptionProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove a field-level encryption profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/delete_field_level_encryption_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#delete_field_level_encryption_profile)
        """

    async def delete_function(
        self, **kwargs: Unpack[DeleteFunctionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a CloudFront function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/delete_function.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#delete_function)
        """

    async def delete_key_group(
        self, **kwargs: Unpack[DeleteKeyGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a key group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/delete_key_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#delete_key_group)
        """

    async def delete_key_value_store(
        self, **kwargs: Unpack[DeleteKeyValueStoreRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specifies the key value store to delete.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/delete_key_value_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#delete_key_value_store)
        """

    async def delete_monitoring_subscription(
        self, **kwargs: Unpack[DeleteMonitoringSubscriptionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disables additional CloudWatch metrics for the specified CloudFront
        distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/delete_monitoring_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#delete_monitoring_subscription)
        """

    async def delete_origin_access_control(
        self, **kwargs: Unpack[DeleteOriginAccessControlRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a CloudFront origin access control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/delete_origin_access_control.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#delete_origin_access_control)
        """

    async def delete_origin_request_policy(
        self, **kwargs: Unpack[DeleteOriginRequestPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an origin request policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/delete_origin_request_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#delete_origin_request_policy)
        """

    async def delete_public_key(
        self, **kwargs: Unpack[DeletePublicKeyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove a public key you previously added to CloudFront.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/delete_public_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#delete_public_key)
        """

    async def delete_realtime_log_config(
        self, **kwargs: Unpack[DeleteRealtimeLogConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a real-time log configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/delete_realtime_log_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#delete_realtime_log_config)
        """

    async def delete_response_headers_policy(
        self, **kwargs: Unpack[DeleteResponseHeadersPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a response headers policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/delete_response_headers_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#delete_response_headers_policy)
        """

    async def delete_streaming_distribution(
        self, **kwargs: Unpack[DeleteStreamingDistributionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a streaming distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/delete_streaming_distribution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#delete_streaming_distribution)
        """

    async def describe_function(
        self, **kwargs: Unpack[DescribeFunctionRequestRequestTypeDef]
    ) -> DescribeFunctionResultTypeDef:
        """
        Gets configuration information and metadata about a CloudFront function, but
        not the function's code.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/describe_function.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#describe_function)
        """

    async def describe_key_value_store(
        self, **kwargs: Unpack[DescribeKeyValueStoreRequestRequestTypeDef]
    ) -> DescribeKeyValueStoreResultTypeDef:
        """
        Specifies the key value store and its configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/describe_key_value_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#describe_key_value_store)
        """

    async def get_cache_policy(
        self, **kwargs: Unpack[GetCachePolicyRequestRequestTypeDef]
    ) -> GetCachePolicyResultTypeDef:
        """
        Gets a cache policy, including the following metadata:.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_cache_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_cache_policy)
        """

    async def get_cache_policy_config(
        self, **kwargs: Unpack[GetCachePolicyConfigRequestRequestTypeDef]
    ) -> GetCachePolicyConfigResultTypeDef:
        """
        Gets a cache policy configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_cache_policy_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_cache_policy_config)
        """

    async def get_cloud_front_origin_access_identity(
        self, **kwargs: Unpack[GetCloudFrontOriginAccessIdentityRequestRequestTypeDef]
    ) -> GetCloudFrontOriginAccessIdentityResultTypeDef:
        """
        Get the information about an origin access identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_cloud_front_origin_access_identity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_cloud_front_origin_access_identity)
        """

    async def get_cloud_front_origin_access_identity_config(
        self, **kwargs: Unpack[GetCloudFrontOriginAccessIdentityConfigRequestRequestTypeDef]
    ) -> GetCloudFrontOriginAccessIdentityConfigResultTypeDef:
        """
        Get the configuration information about an origin access identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_cloud_front_origin_access_identity_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_cloud_front_origin_access_identity_config)
        """

    async def get_continuous_deployment_policy(
        self, **kwargs: Unpack[GetContinuousDeploymentPolicyRequestRequestTypeDef]
    ) -> GetContinuousDeploymentPolicyResultTypeDef:
        """
        Gets a continuous deployment policy, including metadata (the policy's
        identifier and the date and time when the policy was last modified).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_continuous_deployment_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_continuous_deployment_policy)
        """

    async def get_continuous_deployment_policy_config(
        self, **kwargs: Unpack[GetContinuousDeploymentPolicyConfigRequestRequestTypeDef]
    ) -> GetContinuousDeploymentPolicyConfigResultTypeDef:
        """
        Gets configuration information about a continuous deployment policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_continuous_deployment_policy_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_continuous_deployment_policy_config)
        """

    async def get_distribution(
        self, **kwargs: Unpack[GetDistributionRequestRequestTypeDef]
    ) -> GetDistributionResultTypeDef:
        """
        Get the information about a distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_distribution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_distribution)
        """

    async def get_distribution_config(
        self, **kwargs: Unpack[GetDistributionConfigRequestRequestTypeDef]
    ) -> GetDistributionConfigResultTypeDef:
        """
        Get the configuration information about a distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_distribution_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_distribution_config)
        """

    async def get_field_level_encryption(
        self, **kwargs: Unpack[GetFieldLevelEncryptionRequestRequestTypeDef]
    ) -> GetFieldLevelEncryptionResultTypeDef:
        """
        Get the field-level encryption configuration information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_field_level_encryption.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_field_level_encryption)
        """

    async def get_field_level_encryption_config(
        self, **kwargs: Unpack[GetFieldLevelEncryptionConfigRequestRequestTypeDef]
    ) -> GetFieldLevelEncryptionConfigResultTypeDef:
        """
        Get the field-level encryption configuration information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_field_level_encryption_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_field_level_encryption_config)
        """

    async def get_field_level_encryption_profile(
        self, **kwargs: Unpack[GetFieldLevelEncryptionProfileRequestRequestTypeDef]
    ) -> GetFieldLevelEncryptionProfileResultTypeDef:
        """
        Get the field-level encryption profile information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_field_level_encryption_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_field_level_encryption_profile)
        """

    async def get_field_level_encryption_profile_config(
        self, **kwargs: Unpack[GetFieldLevelEncryptionProfileConfigRequestRequestTypeDef]
    ) -> GetFieldLevelEncryptionProfileConfigResultTypeDef:
        """
        Get the field-level encryption profile configuration information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_field_level_encryption_profile_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_field_level_encryption_profile_config)
        """

    async def get_function(
        self, **kwargs: Unpack[GetFunctionRequestRequestTypeDef]
    ) -> GetFunctionResultTypeDef:
        """
        Gets the code of a CloudFront function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_function.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_function)
        """

    async def get_invalidation(
        self, **kwargs: Unpack[GetInvalidationRequestRequestTypeDef]
    ) -> GetInvalidationResultTypeDef:
        """
        Get the information about an invalidation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_invalidation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_invalidation)
        """

    async def get_key_group(
        self, **kwargs: Unpack[GetKeyGroupRequestRequestTypeDef]
    ) -> GetKeyGroupResultTypeDef:
        """
        Gets a key group, including the date and time when the key group was last
        modified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_key_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_key_group)
        """

    async def get_key_group_config(
        self, **kwargs: Unpack[GetKeyGroupConfigRequestRequestTypeDef]
    ) -> GetKeyGroupConfigResultTypeDef:
        """
        Gets a key group configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_key_group_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_key_group_config)
        """

    async def get_monitoring_subscription(
        self, **kwargs: Unpack[GetMonitoringSubscriptionRequestRequestTypeDef]
    ) -> GetMonitoringSubscriptionResultTypeDef:
        """
        Gets information about whether additional CloudWatch metrics are enabled for
        the specified CloudFront distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_monitoring_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_monitoring_subscription)
        """

    async def get_origin_access_control(
        self, **kwargs: Unpack[GetOriginAccessControlRequestRequestTypeDef]
    ) -> GetOriginAccessControlResultTypeDef:
        """
        Gets a CloudFront origin access control, including its unique identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_origin_access_control.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_origin_access_control)
        """

    async def get_origin_access_control_config(
        self, **kwargs: Unpack[GetOriginAccessControlConfigRequestRequestTypeDef]
    ) -> GetOriginAccessControlConfigResultTypeDef:
        """
        Gets a CloudFront origin access control configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_origin_access_control_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_origin_access_control_config)
        """

    async def get_origin_request_policy(
        self, **kwargs: Unpack[GetOriginRequestPolicyRequestRequestTypeDef]
    ) -> GetOriginRequestPolicyResultTypeDef:
        """
        Gets an origin request policy, including the following metadata:.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_origin_request_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_origin_request_policy)
        """

    async def get_origin_request_policy_config(
        self, **kwargs: Unpack[GetOriginRequestPolicyConfigRequestRequestTypeDef]
    ) -> GetOriginRequestPolicyConfigResultTypeDef:
        """
        Gets an origin request policy configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_origin_request_policy_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_origin_request_policy_config)
        """

    async def get_public_key(
        self, **kwargs: Unpack[GetPublicKeyRequestRequestTypeDef]
    ) -> GetPublicKeyResultTypeDef:
        """
        Gets a public key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_public_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_public_key)
        """

    async def get_public_key_config(
        self, **kwargs: Unpack[GetPublicKeyConfigRequestRequestTypeDef]
    ) -> GetPublicKeyConfigResultTypeDef:
        """
        Gets a public key configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_public_key_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_public_key_config)
        """

    async def get_realtime_log_config(
        self, **kwargs: Unpack[GetRealtimeLogConfigRequestRequestTypeDef]
    ) -> GetRealtimeLogConfigResultTypeDef:
        """
        Gets a real-time log configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_realtime_log_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_realtime_log_config)
        """

    async def get_response_headers_policy(
        self, **kwargs: Unpack[GetResponseHeadersPolicyRequestRequestTypeDef]
    ) -> GetResponseHeadersPolicyResultTypeDef:
        """
        Gets a response headers policy, including metadata (the policy's identifier and
        the date and time when the policy was last modified).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_response_headers_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_response_headers_policy)
        """

    async def get_response_headers_policy_config(
        self, **kwargs: Unpack[GetResponseHeadersPolicyConfigRequestRequestTypeDef]
    ) -> GetResponseHeadersPolicyConfigResultTypeDef:
        """
        Gets a response headers policy configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_response_headers_policy_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_response_headers_policy_config)
        """

    async def get_streaming_distribution(
        self, **kwargs: Unpack[GetStreamingDistributionRequestRequestTypeDef]
    ) -> GetStreamingDistributionResultTypeDef:
        """
        Gets information about a specified RTMP distribution, including the
        distribution configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_streaming_distribution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_streaming_distribution)
        """

    async def get_streaming_distribution_config(
        self, **kwargs: Unpack[GetStreamingDistributionConfigRequestRequestTypeDef]
    ) -> GetStreamingDistributionConfigResultTypeDef:
        """
        Get the configuration information about a streaming distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_streaming_distribution_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_streaming_distribution_config)
        """

    async def list_cache_policies(
        self, **kwargs: Unpack[ListCachePoliciesRequestRequestTypeDef]
    ) -> ListCachePoliciesResultTypeDef:
        """
        Gets a list of cache policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_cache_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_cache_policies)
        """

    async def list_cloud_front_origin_access_identities(
        self, **kwargs: Unpack[ListCloudFrontOriginAccessIdentitiesRequestRequestTypeDef]
    ) -> ListCloudFrontOriginAccessIdentitiesResultTypeDef:
        """
        Lists origin access identities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_cloud_front_origin_access_identities.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_cloud_front_origin_access_identities)
        """

    async def list_conflicting_aliases(
        self, **kwargs: Unpack[ListConflictingAliasesRequestRequestTypeDef]
    ) -> ListConflictingAliasesResultTypeDef:
        """
        Gets a list of aliases (also called CNAMEs or alternate domain names) that
        conflict or overlap with the provided alias, and the associated CloudFront
        distributions and Amazon Web Services accounts for each conflicting alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_conflicting_aliases.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_conflicting_aliases)
        """

    async def list_continuous_deployment_policies(
        self, **kwargs: Unpack[ListContinuousDeploymentPoliciesRequestRequestTypeDef]
    ) -> ListContinuousDeploymentPoliciesResultTypeDef:
        """
        Gets a list of the continuous deployment policies in your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_continuous_deployment_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_continuous_deployment_policies)
        """

    async def list_distributions(
        self, **kwargs: Unpack[ListDistributionsRequestRequestTypeDef]
    ) -> ListDistributionsResultTypeDef:
        """
        List CloudFront distributions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_distributions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_distributions)
        """

    async def list_distributions_by_cache_policy_id(
        self, **kwargs: Unpack[ListDistributionsByCachePolicyIdRequestRequestTypeDef]
    ) -> ListDistributionsByCachePolicyIdResultTypeDef:
        """
        Gets a list of distribution IDs for distributions that have a cache behavior
        that's associated with the specified cache policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_distributions_by_cache_policy_id.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_distributions_by_cache_policy_id)
        """

    async def list_distributions_by_key_group(
        self, **kwargs: Unpack[ListDistributionsByKeyGroupRequestRequestTypeDef]
    ) -> ListDistributionsByKeyGroupResultTypeDef:
        """
        Gets a list of distribution IDs for distributions that have a cache behavior
        that references the specified key group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_distributions_by_key_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_distributions_by_key_group)
        """

    async def list_distributions_by_origin_request_policy_id(
        self, **kwargs: Unpack[ListDistributionsByOriginRequestPolicyIdRequestRequestTypeDef]
    ) -> ListDistributionsByOriginRequestPolicyIdResultTypeDef:
        """
        Gets a list of distribution IDs for distributions that have a cache behavior
        that's associated with the specified origin request policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_distributions_by_origin_request_policy_id.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_distributions_by_origin_request_policy_id)
        """

    async def list_distributions_by_realtime_log_config(
        self, **kwargs: Unpack[ListDistributionsByRealtimeLogConfigRequestRequestTypeDef]
    ) -> ListDistributionsByRealtimeLogConfigResultTypeDef:
        """
        Gets a list of distributions that have a cache behavior that's associated with
        the specified real-time log configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_distributions_by_realtime_log_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_distributions_by_realtime_log_config)
        """

    async def list_distributions_by_response_headers_policy_id(
        self, **kwargs: Unpack[ListDistributionsByResponseHeadersPolicyIdRequestRequestTypeDef]
    ) -> ListDistributionsByResponseHeadersPolicyIdResultTypeDef:
        """
        Gets a list of distribution IDs for distributions that have a cache behavior
        that's associated with the specified response headers policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_distributions_by_response_headers_policy_id.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_distributions_by_response_headers_policy_id)
        """

    async def list_distributions_by_web_acl_id(
        self, **kwargs: Unpack[ListDistributionsByWebACLIdRequestRequestTypeDef]
    ) -> ListDistributionsByWebACLIdResultTypeDef:
        """
        List the distributions that are associated with a specified WAF web ACL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_distributions_by_web_acl_id.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_distributions_by_web_acl_id)
        """

    async def list_field_level_encryption_configs(
        self, **kwargs: Unpack[ListFieldLevelEncryptionConfigsRequestRequestTypeDef]
    ) -> ListFieldLevelEncryptionConfigsResultTypeDef:
        """
        List all field-level encryption configurations that have been created in
        CloudFront for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_field_level_encryption_configs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_field_level_encryption_configs)
        """

    async def list_field_level_encryption_profiles(
        self, **kwargs: Unpack[ListFieldLevelEncryptionProfilesRequestRequestTypeDef]
    ) -> ListFieldLevelEncryptionProfilesResultTypeDef:
        """
        Request a list of field-level encryption profiles that have been created in
        CloudFront for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_field_level_encryption_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_field_level_encryption_profiles)
        """

    async def list_functions(
        self, **kwargs: Unpack[ListFunctionsRequestRequestTypeDef]
    ) -> ListFunctionsResultTypeDef:
        """
        Gets a list of all CloudFront functions in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_functions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_functions)
        """

    async def list_invalidations(
        self, **kwargs: Unpack[ListInvalidationsRequestRequestTypeDef]
    ) -> ListInvalidationsResultTypeDef:
        """
        Lists invalidation batches.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_invalidations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_invalidations)
        """

    async def list_key_groups(
        self, **kwargs: Unpack[ListKeyGroupsRequestRequestTypeDef]
    ) -> ListKeyGroupsResultTypeDef:
        """
        Gets a list of key groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_key_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_key_groups)
        """

    async def list_key_value_stores(
        self, **kwargs: Unpack[ListKeyValueStoresRequestRequestTypeDef]
    ) -> ListKeyValueStoresResultTypeDef:
        """
        Specifies the key value stores to list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_key_value_stores.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_key_value_stores)
        """

    async def list_origin_access_controls(
        self, **kwargs: Unpack[ListOriginAccessControlsRequestRequestTypeDef]
    ) -> ListOriginAccessControlsResultTypeDef:
        """
        Gets the list of CloudFront origin access controls in this Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_origin_access_controls.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_origin_access_controls)
        """

    async def list_origin_request_policies(
        self, **kwargs: Unpack[ListOriginRequestPoliciesRequestRequestTypeDef]
    ) -> ListOriginRequestPoliciesResultTypeDef:
        """
        Gets a list of origin request policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_origin_request_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_origin_request_policies)
        """

    async def list_public_keys(
        self, **kwargs: Unpack[ListPublicKeysRequestRequestTypeDef]
    ) -> ListPublicKeysResultTypeDef:
        """
        List all public keys that have been added to CloudFront for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_public_keys.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_public_keys)
        """

    async def list_realtime_log_configs(
        self, **kwargs: Unpack[ListRealtimeLogConfigsRequestRequestTypeDef]
    ) -> ListRealtimeLogConfigsResultTypeDef:
        """
        Gets a list of real-time log configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_realtime_log_configs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_realtime_log_configs)
        """

    async def list_response_headers_policies(
        self, **kwargs: Unpack[ListResponseHeadersPoliciesRequestRequestTypeDef]
    ) -> ListResponseHeadersPoliciesResultTypeDef:
        """
        Gets a list of response headers policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_response_headers_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_response_headers_policies)
        """

    async def list_streaming_distributions(
        self, **kwargs: Unpack[ListStreamingDistributionsRequestRequestTypeDef]
    ) -> ListStreamingDistributionsResultTypeDef:
        """
        List streaming distributions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_streaming_distributions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_streaming_distributions)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResultTypeDef:
        """
        List tags for a CloudFront resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#list_tags_for_resource)
        """

    async def publish_function(
        self, **kwargs: Unpack[PublishFunctionRequestRequestTypeDef]
    ) -> PublishFunctionResultTypeDef:
        """
        Publishes a CloudFront function by copying the function code from the
        <code>DEVELOPMENT</code> stage to <code>LIVE</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/publish_function.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#publish_function)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Add tags to a CloudFront resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#tag_resource)
        """

    async def test_function(
        self, **kwargs: Unpack[TestFunctionRequestRequestTypeDef]
    ) -> TestFunctionResultTypeDef:
        """
        Tests a CloudFront function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/test_function.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#test_function)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove tags from a CloudFront resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#untag_resource)
        """

    async def update_cache_policy(
        self, **kwargs: Unpack[UpdateCachePolicyRequestRequestTypeDef]
    ) -> UpdateCachePolicyResultTypeDef:
        """
        Updates a cache policy configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_cache_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#update_cache_policy)
        """

    async def update_cloud_front_origin_access_identity(
        self, **kwargs: Unpack[UpdateCloudFrontOriginAccessIdentityRequestRequestTypeDef]
    ) -> UpdateCloudFrontOriginAccessIdentityResultTypeDef:
        """
        Update an origin access identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_cloud_front_origin_access_identity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#update_cloud_front_origin_access_identity)
        """

    async def update_continuous_deployment_policy(
        self, **kwargs: Unpack[UpdateContinuousDeploymentPolicyRequestRequestTypeDef]
    ) -> UpdateContinuousDeploymentPolicyResultTypeDef:
        """
        Updates a continuous deployment policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_continuous_deployment_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#update_continuous_deployment_policy)
        """

    async def update_distribution(
        self, **kwargs: Unpack[UpdateDistributionRequestRequestTypeDef]
    ) -> UpdateDistributionResultTypeDef:
        """
        Updates the configuration for a CloudFront distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_distribution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#update_distribution)
        """

    async def update_distribution_with_staging_config(
        self, **kwargs: Unpack[UpdateDistributionWithStagingConfigRequestRequestTypeDef]
    ) -> UpdateDistributionWithStagingConfigResultTypeDef:
        """
        Copies the staging distribution's configuration to its corresponding primary
        distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_distribution_with_staging_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#update_distribution_with_staging_config)
        """

    async def update_field_level_encryption_config(
        self, **kwargs: Unpack[UpdateFieldLevelEncryptionConfigRequestRequestTypeDef]
    ) -> UpdateFieldLevelEncryptionConfigResultTypeDef:
        """
        Update a field-level encryption configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_field_level_encryption_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#update_field_level_encryption_config)
        """

    async def update_field_level_encryption_profile(
        self, **kwargs: Unpack[UpdateFieldLevelEncryptionProfileRequestRequestTypeDef]
    ) -> UpdateFieldLevelEncryptionProfileResultTypeDef:
        """
        Update a field-level encryption profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_field_level_encryption_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#update_field_level_encryption_profile)
        """

    async def update_function(
        self, **kwargs: Unpack[UpdateFunctionRequestRequestTypeDef]
    ) -> UpdateFunctionResultTypeDef:
        """
        Updates a CloudFront function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_function.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#update_function)
        """

    async def update_key_group(
        self, **kwargs: Unpack[UpdateKeyGroupRequestRequestTypeDef]
    ) -> UpdateKeyGroupResultTypeDef:
        """
        Updates a key group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_key_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#update_key_group)
        """

    async def update_key_value_store(
        self, **kwargs: Unpack[UpdateKeyValueStoreRequestRequestTypeDef]
    ) -> UpdateKeyValueStoreResultTypeDef:
        """
        Specifies the key value store to update.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_key_value_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#update_key_value_store)
        """

    async def update_origin_access_control(
        self, **kwargs: Unpack[UpdateOriginAccessControlRequestRequestTypeDef]
    ) -> UpdateOriginAccessControlResultTypeDef:
        """
        Updates a CloudFront origin access control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_origin_access_control.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#update_origin_access_control)
        """

    async def update_origin_request_policy(
        self, **kwargs: Unpack[UpdateOriginRequestPolicyRequestRequestTypeDef]
    ) -> UpdateOriginRequestPolicyResultTypeDef:
        """
        Updates an origin request policy configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_origin_request_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#update_origin_request_policy)
        """

    async def update_public_key(
        self, **kwargs: Unpack[UpdatePublicKeyRequestRequestTypeDef]
    ) -> UpdatePublicKeyResultTypeDef:
        """
        Update public key information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_public_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#update_public_key)
        """

    async def update_realtime_log_config(
        self, **kwargs: Unpack[UpdateRealtimeLogConfigRequestRequestTypeDef]
    ) -> UpdateRealtimeLogConfigResultTypeDef:
        """
        Updates a real-time log configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_realtime_log_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#update_realtime_log_config)
        """

    async def update_response_headers_policy(
        self, **kwargs: Unpack[UpdateResponseHeadersPolicyRequestRequestTypeDef]
    ) -> UpdateResponseHeadersPolicyResultTypeDef:
        """
        Updates a response headers policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_response_headers_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#update_response_headers_policy)
        """

    async def update_streaming_distribution(
        self, **kwargs: Unpack[UpdateStreamingDistributionRequestRequestTypeDef]
    ) -> UpdateStreamingDistributionResultTypeDef:
        """
        Update a streaming distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/update_streaming_distribution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#update_streaming_distribution)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cloud_front_origin_access_identities"]
    ) -> ListCloudFrontOriginAccessIdentitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_distributions"]
    ) -> ListDistributionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_invalidations"]
    ) -> ListInvalidationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_key_value_stores"]
    ) -> ListKeyValueStoresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_streaming_distributions"]
    ) -> ListStreamingDistributionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["distribution_deployed"]
    ) -> DistributionDeployedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["invalidation_completed"]
    ) -> InvalidationCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["streaming_distribution_deployed"]
    ) -> StreamingDistributionDeployedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/#get_waiter)
        """

    async def __aenter__(self) -> "CloudFrontClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#CloudFront.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#CloudFront.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/client/)
        """
