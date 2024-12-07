"""
Type annotations for opensearchserverless service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_opensearchserverless.client import OpenSearchServiceServerlessClient

    session = get_session()
    async with session.create_client("opensearchserverless") as client:
        client: OpenSearchServiceServerlessClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    BatchGetCollectionRequestRequestTypeDef,
    BatchGetCollectionResponseTypeDef,
    BatchGetEffectiveLifecyclePolicyRequestRequestTypeDef,
    BatchGetEffectiveLifecyclePolicyResponseTypeDef,
    BatchGetLifecyclePolicyRequestRequestTypeDef,
    BatchGetLifecyclePolicyResponseTypeDef,
    BatchGetVpcEndpointRequestRequestTypeDef,
    BatchGetVpcEndpointResponseTypeDef,
    CreateAccessPolicyRequestRequestTypeDef,
    CreateAccessPolicyResponseTypeDef,
    CreateCollectionRequestRequestTypeDef,
    CreateCollectionResponseTypeDef,
    CreateLifecyclePolicyRequestRequestTypeDef,
    CreateLifecyclePolicyResponseTypeDef,
    CreateSecurityConfigRequestRequestTypeDef,
    CreateSecurityConfigResponseTypeDef,
    CreateSecurityPolicyRequestRequestTypeDef,
    CreateSecurityPolicyResponseTypeDef,
    CreateVpcEndpointRequestRequestTypeDef,
    CreateVpcEndpointResponseTypeDef,
    DeleteAccessPolicyRequestRequestTypeDef,
    DeleteCollectionRequestRequestTypeDef,
    DeleteCollectionResponseTypeDef,
    DeleteLifecyclePolicyRequestRequestTypeDef,
    DeleteSecurityConfigRequestRequestTypeDef,
    DeleteSecurityPolicyRequestRequestTypeDef,
    DeleteVpcEndpointRequestRequestTypeDef,
    DeleteVpcEndpointResponseTypeDef,
    GetAccessPolicyRequestRequestTypeDef,
    GetAccessPolicyResponseTypeDef,
    GetAccountSettingsResponseTypeDef,
    GetPoliciesStatsResponseTypeDef,
    GetSecurityConfigRequestRequestTypeDef,
    GetSecurityConfigResponseTypeDef,
    GetSecurityPolicyRequestRequestTypeDef,
    GetSecurityPolicyResponseTypeDef,
    ListAccessPoliciesRequestRequestTypeDef,
    ListAccessPoliciesResponseTypeDef,
    ListCollectionsRequestRequestTypeDef,
    ListCollectionsResponseTypeDef,
    ListLifecyclePoliciesRequestRequestTypeDef,
    ListLifecyclePoliciesResponseTypeDef,
    ListSecurityConfigsRequestRequestTypeDef,
    ListSecurityConfigsResponseTypeDef,
    ListSecurityPoliciesRequestRequestTypeDef,
    ListSecurityPoliciesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVpcEndpointsRequestRequestTypeDef,
    ListVpcEndpointsResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAccessPolicyRequestRequestTypeDef,
    UpdateAccessPolicyResponseTypeDef,
    UpdateAccountSettingsRequestRequestTypeDef,
    UpdateAccountSettingsResponseTypeDef,
    UpdateCollectionRequestRequestTypeDef,
    UpdateCollectionResponseTypeDef,
    UpdateLifecyclePolicyRequestRequestTypeDef,
    UpdateLifecyclePolicyResponseTypeDef,
    UpdateSecurityConfigRequestRequestTypeDef,
    UpdateSecurityConfigResponseTypeDef,
    UpdateSecurityPolicyRequestRequestTypeDef,
    UpdateSecurityPolicyResponseTypeDef,
    UpdateVpcEndpointRequestRequestTypeDef,
    UpdateVpcEndpointResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("OpenSearchServiceServerlessClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    OcuLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class OpenSearchServiceServerlessClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OpenSearchServiceServerlessClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#close)
        """

    async def batch_get_collection(
        self, **kwargs: Unpack[BatchGetCollectionRequestRequestTypeDef]
    ) -> BatchGetCollectionResponseTypeDef:
        """
        Returns attributes for one or more collections, including the collection
        endpoint and the OpenSearch Dashboards endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/batch_get_collection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#batch_get_collection)
        """

    async def batch_get_effective_lifecycle_policy(
        self, **kwargs: Unpack[BatchGetEffectiveLifecyclePolicyRequestRequestTypeDef]
    ) -> BatchGetEffectiveLifecyclePolicyResponseTypeDef:
        """
        Returns a list of successful and failed retrievals for the OpenSearch
        Serverless indexes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/batch_get_effective_lifecycle_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#batch_get_effective_lifecycle_policy)
        """

    async def batch_get_lifecycle_policy(
        self, **kwargs: Unpack[BatchGetLifecyclePolicyRequestRequestTypeDef]
    ) -> BatchGetLifecyclePolicyResponseTypeDef:
        """
        Returns one or more configured OpenSearch Serverless lifecycle policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/batch_get_lifecycle_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#batch_get_lifecycle_policy)
        """

    async def batch_get_vpc_endpoint(
        self, **kwargs: Unpack[BatchGetVpcEndpointRequestRequestTypeDef]
    ) -> BatchGetVpcEndpointResponseTypeDef:
        """
        Returns attributes for one or more VPC endpoints associated with the current
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/batch_get_vpc_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#batch_get_vpc_endpoint)
        """

    async def create_access_policy(
        self, **kwargs: Unpack[CreateAccessPolicyRequestRequestTypeDef]
    ) -> CreateAccessPolicyResponseTypeDef:
        """
        Creates a data access policy for OpenSearch Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/create_access_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#create_access_policy)
        """

    async def create_collection(
        self, **kwargs: Unpack[CreateCollectionRequestRequestTypeDef]
    ) -> CreateCollectionResponseTypeDef:
        """
        Creates a new OpenSearch Serverless collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/create_collection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#create_collection)
        """

    async def create_lifecycle_policy(
        self, **kwargs: Unpack[CreateLifecyclePolicyRequestRequestTypeDef]
    ) -> CreateLifecyclePolicyResponseTypeDef:
        """
        Creates a lifecyle policy to be applied to OpenSearch Serverless indexes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/create_lifecycle_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#create_lifecycle_policy)
        """

    async def create_security_config(
        self, **kwargs: Unpack[CreateSecurityConfigRequestRequestTypeDef]
    ) -> CreateSecurityConfigResponseTypeDef:
        """
        Specifies a security configuration for OpenSearch Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/create_security_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#create_security_config)
        """

    async def create_security_policy(
        self, **kwargs: Unpack[CreateSecurityPolicyRequestRequestTypeDef]
    ) -> CreateSecurityPolicyResponseTypeDef:
        """
        Creates a security policy to be used by one or more OpenSearch Serverless
        collections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/create_security_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#create_security_policy)
        """

    async def create_vpc_endpoint(
        self, **kwargs: Unpack[CreateVpcEndpointRequestRequestTypeDef]
    ) -> CreateVpcEndpointResponseTypeDef:
        """
        Creates an OpenSearch Serverless-managed interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/create_vpc_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#create_vpc_endpoint)
        """

    async def delete_access_policy(
        self, **kwargs: Unpack[DeleteAccessPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an OpenSearch Serverless access policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/delete_access_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#delete_access_policy)
        """

    async def delete_collection(
        self, **kwargs: Unpack[DeleteCollectionRequestRequestTypeDef]
    ) -> DeleteCollectionResponseTypeDef:
        """
        Deletes an OpenSearch Serverless collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/delete_collection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#delete_collection)
        """

    async def delete_lifecycle_policy(
        self, **kwargs: Unpack[DeleteLifecyclePolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an OpenSearch Serverless lifecycle policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/delete_lifecycle_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#delete_lifecycle_policy)
        """

    async def delete_security_config(
        self, **kwargs: Unpack[DeleteSecurityConfigRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a security configuration for OpenSearch Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/delete_security_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#delete_security_config)
        """

    async def delete_security_policy(
        self, **kwargs: Unpack[DeleteSecurityPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an OpenSearch Serverless security policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/delete_security_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#delete_security_policy)
        """

    async def delete_vpc_endpoint(
        self, **kwargs: Unpack[DeleteVpcEndpointRequestRequestTypeDef]
    ) -> DeleteVpcEndpointResponseTypeDef:
        """
        Deletes an OpenSearch Serverless-managed interface endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/delete_vpc_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#delete_vpc_endpoint)
        """

    async def get_access_policy(
        self, **kwargs: Unpack[GetAccessPolicyRequestRequestTypeDef]
    ) -> GetAccessPolicyResponseTypeDef:
        """
        Returns an OpenSearch Serverless access policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/get_access_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#get_access_policy)
        """

    async def get_account_settings(self) -> GetAccountSettingsResponseTypeDef:
        """
        Returns account-level settings related to OpenSearch Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/get_account_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#get_account_settings)
        """

    async def get_policies_stats(self) -> GetPoliciesStatsResponseTypeDef:
        """
        Returns statistical information about your OpenSearch Serverless access
        policies, security configurations, and security policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/get_policies_stats.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#get_policies_stats)
        """

    async def get_security_config(
        self, **kwargs: Unpack[GetSecurityConfigRequestRequestTypeDef]
    ) -> GetSecurityConfigResponseTypeDef:
        """
        Returns information about an OpenSearch Serverless security configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/get_security_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#get_security_config)
        """

    async def get_security_policy(
        self, **kwargs: Unpack[GetSecurityPolicyRequestRequestTypeDef]
    ) -> GetSecurityPolicyResponseTypeDef:
        """
        Returns information about a configured OpenSearch Serverless security policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/get_security_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#get_security_policy)
        """

    async def list_access_policies(
        self, **kwargs: Unpack[ListAccessPoliciesRequestRequestTypeDef]
    ) -> ListAccessPoliciesResponseTypeDef:
        """
        Returns information about a list of OpenSearch Serverless access policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/list_access_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#list_access_policies)
        """

    async def list_collections(
        self, **kwargs: Unpack[ListCollectionsRequestRequestTypeDef]
    ) -> ListCollectionsResponseTypeDef:
        """
        Lists all OpenSearch Serverless collections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/list_collections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#list_collections)
        """

    async def list_lifecycle_policies(
        self, **kwargs: Unpack[ListLifecyclePoliciesRequestRequestTypeDef]
    ) -> ListLifecyclePoliciesResponseTypeDef:
        """
        Returns a list of OpenSearch Serverless lifecycle policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/list_lifecycle_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#list_lifecycle_policies)
        """

    async def list_security_configs(
        self, **kwargs: Unpack[ListSecurityConfigsRequestRequestTypeDef]
    ) -> ListSecurityConfigsResponseTypeDef:
        """
        Returns information about configured OpenSearch Serverless security
        configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/list_security_configs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#list_security_configs)
        """

    async def list_security_policies(
        self, **kwargs: Unpack[ListSecurityPoliciesRequestRequestTypeDef]
    ) -> ListSecurityPoliciesResponseTypeDef:
        """
        Returns information about configured OpenSearch Serverless security policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/list_security_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#list_security_policies)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns the tags for an OpenSearch Serverless resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#list_tags_for_resource)
        """

    async def list_vpc_endpoints(
        self, **kwargs: Unpack[ListVpcEndpointsRequestRequestTypeDef]
    ) -> ListVpcEndpointsResponseTypeDef:
        """
        Returns the OpenSearch Serverless-managed interface VPC endpoints associated
        with the current account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/list_vpc_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#list_vpc_endpoints)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates tags with an OpenSearch Serverless resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag or set of tags from an OpenSearch Serverless resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#untag_resource)
        """

    async def update_access_policy(
        self, **kwargs: Unpack[UpdateAccessPolicyRequestRequestTypeDef]
    ) -> UpdateAccessPolicyResponseTypeDef:
        """
        Updates an OpenSearch Serverless access policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/update_access_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#update_access_policy)
        """

    async def update_account_settings(
        self, **kwargs: Unpack[UpdateAccountSettingsRequestRequestTypeDef]
    ) -> UpdateAccountSettingsResponseTypeDef:
        """
        Update the OpenSearch Serverless settings for the current Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/update_account_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#update_account_settings)
        """

    async def update_collection(
        self, **kwargs: Unpack[UpdateCollectionRequestRequestTypeDef]
    ) -> UpdateCollectionResponseTypeDef:
        """
        Updates an OpenSearch Serverless collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/update_collection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#update_collection)
        """

    async def update_lifecycle_policy(
        self, **kwargs: Unpack[UpdateLifecyclePolicyRequestRequestTypeDef]
    ) -> UpdateLifecyclePolicyResponseTypeDef:
        """
        Updates an OpenSearch Serverless access policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/update_lifecycle_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#update_lifecycle_policy)
        """

    async def update_security_config(
        self, **kwargs: Unpack[UpdateSecurityConfigRequestRequestTypeDef]
    ) -> UpdateSecurityConfigResponseTypeDef:
        """
        Updates a security configuration for OpenSearch Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/update_security_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#update_security_config)
        """

    async def update_security_policy(
        self, **kwargs: Unpack[UpdateSecurityPolicyRequestRequestTypeDef]
    ) -> UpdateSecurityPolicyResponseTypeDef:
        """
        Updates an OpenSearch Serverless security policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/update_security_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#update_security_policy)
        """

    async def update_vpc_endpoint(
        self, **kwargs: Unpack[UpdateVpcEndpointRequestRequestTypeDef]
    ) -> UpdateVpcEndpointResponseTypeDef:
        """
        Updates an OpenSearch Serverless-managed interface endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/update_vpc_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/#update_vpc_endpoint)
        """

    async def __aenter__(self) -> "OpenSearchServiceServerlessClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/client/)
        """
