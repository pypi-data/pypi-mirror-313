"""
Type annotations for cognito-identity service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cognito_identity.client import CognitoIdentityClient

    session = get_session()
    async with session.create_client("cognito-identity") as client:
        client: CognitoIdentityClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListIdentityPoolsPaginator
from .type_defs import (
    CreateIdentityPoolInputRequestTypeDef,
    DeleteIdentitiesInputRequestTypeDef,
    DeleteIdentitiesResponseTypeDef,
    DeleteIdentityPoolInputRequestTypeDef,
    DescribeIdentityInputRequestTypeDef,
    DescribeIdentityPoolInputRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCredentialsForIdentityInputRequestTypeDef,
    GetCredentialsForIdentityResponseTypeDef,
    GetIdentityPoolRolesInputRequestTypeDef,
    GetIdentityPoolRolesResponseTypeDef,
    GetIdInputRequestTypeDef,
    GetIdResponseTypeDef,
    GetOpenIdTokenForDeveloperIdentityInputRequestTypeDef,
    GetOpenIdTokenForDeveloperIdentityResponseTypeDef,
    GetOpenIdTokenInputRequestTypeDef,
    GetOpenIdTokenResponseTypeDef,
    GetPrincipalTagAttributeMapInputRequestTypeDef,
    GetPrincipalTagAttributeMapResponseTypeDef,
    IdentityDescriptionResponseTypeDef,
    IdentityPoolRequestTypeDef,
    IdentityPoolTypeDef,
    ListIdentitiesInputRequestTypeDef,
    ListIdentitiesResponseTypeDef,
    ListIdentityPoolsInputRequestTypeDef,
    ListIdentityPoolsResponseTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    LookupDeveloperIdentityInputRequestTypeDef,
    LookupDeveloperIdentityResponseTypeDef,
    MergeDeveloperIdentitiesInputRequestTypeDef,
    MergeDeveloperIdentitiesResponseTypeDef,
    SetIdentityPoolRolesInputRequestTypeDef,
    SetPrincipalTagAttributeMapInputRequestTypeDef,
    SetPrincipalTagAttributeMapResponseTypeDef,
    TagResourceInputRequestTypeDef,
    UnlinkDeveloperIdentityInputRequestTypeDef,
    UnlinkIdentityInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("CognitoIdentityClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    DeveloperUserAlreadyRegisteredException: Type[BotocoreClientError]
    ExternalServiceException: Type[BotocoreClientError]
    InternalErrorException: Type[BotocoreClientError]
    InvalidIdentityPoolConfigurationException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class CognitoIdentityClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CognitoIdentityClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#close)
        """

    async def create_identity_pool(
        self, **kwargs: Unpack[CreateIdentityPoolInputRequestTypeDef]
    ) -> IdentityPoolTypeDef:
        """
        Creates a new identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/create_identity_pool.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#create_identity_pool)
        """

    async def delete_identities(
        self, **kwargs: Unpack[DeleteIdentitiesInputRequestTypeDef]
    ) -> DeleteIdentitiesResponseTypeDef:
        """
        Deletes identities from an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/delete_identities.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#delete_identities)
        """

    async def delete_identity_pool(
        self, **kwargs: Unpack[DeleteIdentityPoolInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/delete_identity_pool.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#delete_identity_pool)
        """

    async def describe_identity(
        self, **kwargs: Unpack[DescribeIdentityInputRequestTypeDef]
    ) -> IdentityDescriptionResponseTypeDef:
        """
        Returns metadata related to the given identity, including when the identity was
        created and any associated linked logins.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/describe_identity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#describe_identity)
        """

    async def describe_identity_pool(
        self, **kwargs: Unpack[DescribeIdentityPoolInputRequestTypeDef]
    ) -> IdentityPoolTypeDef:
        """
        Gets details about a particular identity pool, including the pool name, ID
        description, creation date, and current number of users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/describe_identity_pool.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#describe_identity_pool)
        """

    async def get_credentials_for_identity(
        self, **kwargs: Unpack[GetCredentialsForIdentityInputRequestTypeDef]
    ) -> GetCredentialsForIdentityResponseTypeDef:
        """
        Returns credentials for the provided identity ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/get_credentials_for_identity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#get_credentials_for_identity)
        """

    async def get_id(self, **kwargs: Unpack[GetIdInputRequestTypeDef]) -> GetIdResponseTypeDef:
        """
        Generates (or retrieves) a Cognito ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/get_id.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#get_id)
        """

    async def get_identity_pool_roles(
        self, **kwargs: Unpack[GetIdentityPoolRolesInputRequestTypeDef]
    ) -> GetIdentityPoolRolesResponseTypeDef:
        """
        Gets the roles for an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/get_identity_pool_roles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#get_identity_pool_roles)
        """

    async def get_open_id_token(
        self, **kwargs: Unpack[GetOpenIdTokenInputRequestTypeDef]
    ) -> GetOpenIdTokenResponseTypeDef:
        """
        Gets an OpenID token, using a known Cognito ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/get_open_id_token.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#get_open_id_token)
        """

    async def get_open_id_token_for_developer_identity(
        self, **kwargs: Unpack[GetOpenIdTokenForDeveloperIdentityInputRequestTypeDef]
    ) -> GetOpenIdTokenForDeveloperIdentityResponseTypeDef:
        """
        Registers (or retrieves) a Cognito <code>IdentityId</code> and an OpenID
        Connect token for a user authenticated by your backend authentication process.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/get_open_id_token_for_developer_identity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#get_open_id_token_for_developer_identity)
        """

    async def get_principal_tag_attribute_map(
        self, **kwargs: Unpack[GetPrincipalTagAttributeMapInputRequestTypeDef]
    ) -> GetPrincipalTagAttributeMapResponseTypeDef:
        """
        Use <code>GetPrincipalTagAttributeMap</code> to list all mappings between
        <code>PrincipalTags</code> and user attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/get_principal_tag_attribute_map.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#get_principal_tag_attribute_map)
        """

    async def list_identities(
        self, **kwargs: Unpack[ListIdentitiesInputRequestTypeDef]
    ) -> ListIdentitiesResponseTypeDef:
        """
        Lists the identities in an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/list_identities.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#list_identities)
        """

    async def list_identity_pools(
        self, **kwargs: Unpack[ListIdentityPoolsInputRequestTypeDef]
    ) -> ListIdentityPoolsResponseTypeDef:
        """
        Lists all of the Cognito identity pools registered for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/list_identity_pools.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#list_identity_pools)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags that are assigned to an Amazon Cognito identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#list_tags_for_resource)
        """

    async def lookup_developer_identity(
        self, **kwargs: Unpack[LookupDeveloperIdentityInputRequestTypeDef]
    ) -> LookupDeveloperIdentityResponseTypeDef:
        """
        Retrieves the <code>IdentityID</code> associated with a
        <code>DeveloperUserIdentifier</code> or the list of
        <code>DeveloperUserIdentifier</code> values associated with an
        <code>IdentityId</code> for an existing identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/lookup_developer_identity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#lookup_developer_identity)
        """

    async def merge_developer_identities(
        self, **kwargs: Unpack[MergeDeveloperIdentitiesInputRequestTypeDef]
    ) -> MergeDeveloperIdentitiesResponseTypeDef:
        """
        Merges two users having different <code>IdentityId</code>s, existing in the
        same identity pool, and identified by the same developer provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/merge_developer_identities.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#merge_developer_identities)
        """

    async def set_identity_pool_roles(
        self, **kwargs: Unpack[SetIdentityPoolRolesInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the roles for an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/set_identity_pool_roles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#set_identity_pool_roles)
        """

    async def set_principal_tag_attribute_map(
        self, **kwargs: Unpack[SetPrincipalTagAttributeMapInputRequestTypeDef]
    ) -> SetPrincipalTagAttributeMapResponseTypeDef:
        """
        You can use this operation to use default (username and clientID) attribute or
        custom attribute mappings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/set_principal_tag_attribute_map.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#set_principal_tag_attribute_map)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Assigns a set of tags to the specified Amazon Cognito identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#tag_resource)
        """

    async def unlink_developer_identity(
        self, **kwargs: Unpack[UnlinkDeveloperIdentityInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Unlinks a <code>DeveloperUserIdentifier</code> from an existing identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/unlink_developer_identity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#unlink_developer_identity)
        """

    async def unlink_identity(
        self, **kwargs: Unpack[UnlinkIdentityInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Unlinks a federated identity from an existing account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/unlink_identity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#unlink_identity)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified Amazon Cognito identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#untag_resource)
        """

    async def update_identity_pool(
        self, **kwargs: Unpack[IdentityPoolRequestTypeDef]
    ) -> IdentityPoolTypeDef:
        """
        Updates an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/update_identity_pool.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#update_identity_pool)
        """

    def get_paginator(
        self, operation_name: Literal["list_identity_pools"]
    ) -> ListIdentityPoolsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#get_paginator)
        """

    async def __aenter__(self) -> "CognitoIdentityClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/)
        """
