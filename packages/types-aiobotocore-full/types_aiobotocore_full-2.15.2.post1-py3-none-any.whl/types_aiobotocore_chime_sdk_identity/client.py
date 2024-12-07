"""
Type annotations for chime-sdk-identity service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chime_sdk_identity.client import ChimeSDKIdentityClient

    session = get_session()
    async with session.create_client("chime-sdk-identity") as client:
        client: ChimeSDKIdentityClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    CreateAppInstanceAdminRequestRequestTypeDef,
    CreateAppInstanceAdminResponseTypeDef,
    CreateAppInstanceBotRequestRequestTypeDef,
    CreateAppInstanceBotResponseTypeDef,
    CreateAppInstanceRequestRequestTypeDef,
    CreateAppInstanceResponseTypeDef,
    CreateAppInstanceUserRequestRequestTypeDef,
    CreateAppInstanceUserResponseTypeDef,
    DeleteAppInstanceAdminRequestRequestTypeDef,
    DeleteAppInstanceBotRequestRequestTypeDef,
    DeleteAppInstanceRequestRequestTypeDef,
    DeleteAppInstanceUserRequestRequestTypeDef,
    DeregisterAppInstanceUserEndpointRequestRequestTypeDef,
    DescribeAppInstanceAdminRequestRequestTypeDef,
    DescribeAppInstanceAdminResponseTypeDef,
    DescribeAppInstanceBotRequestRequestTypeDef,
    DescribeAppInstanceBotResponseTypeDef,
    DescribeAppInstanceRequestRequestTypeDef,
    DescribeAppInstanceResponseTypeDef,
    DescribeAppInstanceUserEndpointRequestRequestTypeDef,
    DescribeAppInstanceUserEndpointResponseTypeDef,
    DescribeAppInstanceUserRequestRequestTypeDef,
    DescribeAppInstanceUserResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAppInstanceRetentionSettingsRequestRequestTypeDef,
    GetAppInstanceRetentionSettingsResponseTypeDef,
    ListAppInstanceAdminsRequestRequestTypeDef,
    ListAppInstanceAdminsResponseTypeDef,
    ListAppInstanceBotsRequestRequestTypeDef,
    ListAppInstanceBotsResponseTypeDef,
    ListAppInstancesRequestRequestTypeDef,
    ListAppInstancesResponseTypeDef,
    ListAppInstanceUserEndpointsRequestRequestTypeDef,
    ListAppInstanceUserEndpointsResponseTypeDef,
    ListAppInstanceUsersRequestRequestTypeDef,
    ListAppInstanceUsersResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutAppInstanceRetentionSettingsRequestRequestTypeDef,
    PutAppInstanceRetentionSettingsResponseTypeDef,
    PutAppInstanceUserExpirationSettingsRequestRequestTypeDef,
    PutAppInstanceUserExpirationSettingsResponseTypeDef,
    RegisterAppInstanceUserEndpointRequestRequestTypeDef,
    RegisterAppInstanceUserEndpointResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAppInstanceBotRequestRequestTypeDef,
    UpdateAppInstanceBotResponseTypeDef,
    UpdateAppInstanceRequestRequestTypeDef,
    UpdateAppInstanceResponseTypeDef,
    UpdateAppInstanceUserEndpointRequestRequestTypeDef,
    UpdateAppInstanceUserEndpointResponseTypeDef,
    UpdateAppInstanceUserRequestRequestTypeDef,
    UpdateAppInstanceUserResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ChimeSDKIdentityClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottledClientException: Type[BotocoreClientError]
    UnauthorizedClientException: Type[BotocoreClientError]


class ChimeSDKIdentityClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChimeSDKIdentityClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#close)
        """

    async def create_app_instance(
        self, **kwargs: Unpack[CreateAppInstanceRequestRequestTypeDef]
    ) -> CreateAppInstanceResponseTypeDef:
        """
        Creates an Amazon Chime SDK messaging <code>AppInstance</code> under an AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/create_app_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#create_app_instance)
        """

    async def create_app_instance_admin(
        self, **kwargs: Unpack[CreateAppInstanceAdminRequestRequestTypeDef]
    ) -> CreateAppInstanceAdminResponseTypeDef:
        """
        Promotes an <code>AppInstanceUser</code> or <code>AppInstanceBot</code> to an
        <code>AppInstanceAdmin</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/create_app_instance_admin.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#create_app_instance_admin)
        """

    async def create_app_instance_bot(
        self, **kwargs: Unpack[CreateAppInstanceBotRequestRequestTypeDef]
    ) -> CreateAppInstanceBotResponseTypeDef:
        """
        Creates a bot under an Amazon Chime <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/create_app_instance_bot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#create_app_instance_bot)
        """

    async def create_app_instance_user(
        self, **kwargs: Unpack[CreateAppInstanceUserRequestRequestTypeDef]
    ) -> CreateAppInstanceUserResponseTypeDef:
        """
        Creates a user under an Amazon Chime <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/create_app_instance_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#create_app_instance_user)
        """

    async def delete_app_instance(
        self, **kwargs: Unpack[DeleteAppInstanceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an <code>AppInstance</code> and all associated data asynchronously.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/delete_app_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#delete_app_instance)
        """

    async def delete_app_instance_admin(
        self, **kwargs: Unpack[DeleteAppInstanceAdminRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Demotes an <code>AppInstanceAdmin</code> to an <code>AppInstanceUser</code> or
        <code>AppInstanceBot</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/delete_app_instance_admin.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#delete_app_instance_admin)
        """

    async def delete_app_instance_bot(
        self, **kwargs: Unpack[DeleteAppInstanceBotRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an <code>AppInstanceBot</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/delete_app_instance_bot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#delete_app_instance_bot)
        """

    async def delete_app_instance_user(
        self, **kwargs: Unpack[DeleteAppInstanceUserRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/delete_app_instance_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#delete_app_instance_user)
        """

    async def deregister_app_instance_user_endpoint(
        self, **kwargs: Unpack[DeregisterAppInstanceUserEndpointRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters an <code>AppInstanceUserEndpoint</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/deregister_app_instance_user_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#deregister_app_instance_user_endpoint)
        """

    async def describe_app_instance(
        self, **kwargs: Unpack[DescribeAppInstanceRequestRequestTypeDef]
    ) -> DescribeAppInstanceResponseTypeDef:
        """
        Returns the full details of an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/describe_app_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#describe_app_instance)
        """

    async def describe_app_instance_admin(
        self, **kwargs: Unpack[DescribeAppInstanceAdminRequestRequestTypeDef]
    ) -> DescribeAppInstanceAdminResponseTypeDef:
        """
        Returns the full details of an <code>AppInstanceAdmin</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/describe_app_instance_admin.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#describe_app_instance_admin)
        """

    async def describe_app_instance_bot(
        self, **kwargs: Unpack[DescribeAppInstanceBotRequestRequestTypeDef]
    ) -> DescribeAppInstanceBotResponseTypeDef:
        """
        The <code>AppInstanceBot's</code> information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/describe_app_instance_bot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#describe_app_instance_bot)
        """

    async def describe_app_instance_user(
        self, **kwargs: Unpack[DescribeAppInstanceUserRequestRequestTypeDef]
    ) -> DescribeAppInstanceUserResponseTypeDef:
        """
        Returns the full details of an <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/describe_app_instance_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#describe_app_instance_user)
        """

    async def describe_app_instance_user_endpoint(
        self, **kwargs: Unpack[DescribeAppInstanceUserEndpointRequestRequestTypeDef]
    ) -> DescribeAppInstanceUserEndpointResponseTypeDef:
        """
        Returns the full details of an <code>AppInstanceUserEndpoint</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/describe_app_instance_user_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#describe_app_instance_user_endpoint)
        """

    async def get_app_instance_retention_settings(
        self, **kwargs: Unpack[GetAppInstanceRetentionSettingsRequestRequestTypeDef]
    ) -> GetAppInstanceRetentionSettingsResponseTypeDef:
        """
        Gets the retention settings for an <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/get_app_instance_retention_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#get_app_instance_retention_settings)
        """

    async def list_app_instance_admins(
        self, **kwargs: Unpack[ListAppInstanceAdminsRequestRequestTypeDef]
    ) -> ListAppInstanceAdminsResponseTypeDef:
        """
        Returns a list of the administrators in the <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/list_app_instance_admins.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#list_app_instance_admins)
        """

    async def list_app_instance_bots(
        self, **kwargs: Unpack[ListAppInstanceBotsRequestRequestTypeDef]
    ) -> ListAppInstanceBotsResponseTypeDef:
        """
        Lists all <code>AppInstanceBots</code> created under a single
        <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/list_app_instance_bots.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#list_app_instance_bots)
        """

    async def list_app_instance_user_endpoints(
        self, **kwargs: Unpack[ListAppInstanceUserEndpointsRequestRequestTypeDef]
    ) -> ListAppInstanceUserEndpointsResponseTypeDef:
        """
        Lists all the <code>AppInstanceUserEndpoints</code> created under a single
        <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/list_app_instance_user_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#list_app_instance_user_endpoints)
        """

    async def list_app_instance_users(
        self, **kwargs: Unpack[ListAppInstanceUsersRequestRequestTypeDef]
    ) -> ListAppInstanceUsersResponseTypeDef:
        """
        List all <code>AppInstanceUsers</code> created under a single
        <code>AppInstance</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/list_app_instance_users.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#list_app_instance_users)
        """

    async def list_app_instances(
        self, **kwargs: Unpack[ListAppInstancesRequestRequestTypeDef]
    ) -> ListAppInstancesResponseTypeDef:
        """
        Lists all Amazon Chime <code>AppInstance</code>s created under a single AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/list_app_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#list_app_instances)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags applied to an Amazon Chime SDK identity resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#list_tags_for_resource)
        """

    async def put_app_instance_retention_settings(
        self, **kwargs: Unpack[PutAppInstanceRetentionSettingsRequestRequestTypeDef]
    ) -> PutAppInstanceRetentionSettingsResponseTypeDef:
        """
        Sets the amount of time in days that a given <code>AppInstance</code> retains
        data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/put_app_instance_retention_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#put_app_instance_retention_settings)
        """

    async def put_app_instance_user_expiration_settings(
        self, **kwargs: Unpack[PutAppInstanceUserExpirationSettingsRequestRequestTypeDef]
    ) -> PutAppInstanceUserExpirationSettingsResponseTypeDef:
        """
        Sets the number of days before the <code>AppInstanceUser</code> is
        automatically deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/put_app_instance_user_expiration_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#put_app_instance_user_expiration_settings)
        """

    async def register_app_instance_user_endpoint(
        self, **kwargs: Unpack[RegisterAppInstanceUserEndpointRequestRequestTypeDef]
    ) -> RegisterAppInstanceUserEndpointResponseTypeDef:
        """
        Registers an endpoint under an Amazon Chime <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/register_app_instance_user_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#register_app_instance_user_endpoint)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Applies the specified tags to the specified Amazon Chime SDK identity resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified tags from the specified Amazon Chime SDK identity
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#untag_resource)
        """

    async def update_app_instance(
        self, **kwargs: Unpack[UpdateAppInstanceRequestRequestTypeDef]
    ) -> UpdateAppInstanceResponseTypeDef:
        """
        Updates <code>AppInstance</code> metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/update_app_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#update_app_instance)
        """

    async def update_app_instance_bot(
        self, **kwargs: Unpack[UpdateAppInstanceBotRequestRequestTypeDef]
    ) -> UpdateAppInstanceBotResponseTypeDef:
        """
        Updates the name and metadata of an <code>AppInstanceBot</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/update_app_instance_bot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#update_app_instance_bot)
        """

    async def update_app_instance_user(
        self, **kwargs: Unpack[UpdateAppInstanceUserRequestRequestTypeDef]
    ) -> UpdateAppInstanceUserResponseTypeDef:
        """
        Updates the details of an <code>AppInstanceUser</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/update_app_instance_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#update_app_instance_user)
        """

    async def update_app_instance_user_endpoint(
        self, **kwargs: Unpack[UpdateAppInstanceUserEndpointRequestRequestTypeDef]
    ) -> UpdateAppInstanceUserEndpointResponseTypeDef:
        """
        Updates the details of an <code>AppInstanceUserEndpoint</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity/client/update_app_instance_user_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#update_app_instance_user_endpoint)
        """

    async def __aenter__(self) -> "ChimeSDKIdentityClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/)
        """
