"""
Type annotations for workspaces-web service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_workspaces_web.client import WorkSpacesWebClient

    session = get_session()
    async with session.create_client("workspaces-web") as client:
        client: WorkSpacesWebClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListSessionsPaginator
from .type_defs import (
    AssociateBrowserSettingsRequestRequestTypeDef,
    AssociateBrowserSettingsResponseTypeDef,
    AssociateIpAccessSettingsRequestRequestTypeDef,
    AssociateIpAccessSettingsResponseTypeDef,
    AssociateNetworkSettingsRequestRequestTypeDef,
    AssociateNetworkSettingsResponseTypeDef,
    AssociateTrustStoreRequestRequestTypeDef,
    AssociateTrustStoreResponseTypeDef,
    AssociateUserAccessLoggingSettingsRequestRequestTypeDef,
    AssociateUserAccessLoggingSettingsResponseTypeDef,
    AssociateUserSettingsRequestRequestTypeDef,
    AssociateUserSettingsResponseTypeDef,
    CreateBrowserSettingsRequestRequestTypeDef,
    CreateBrowserSettingsResponseTypeDef,
    CreateIdentityProviderRequestRequestTypeDef,
    CreateIdentityProviderResponseTypeDef,
    CreateIpAccessSettingsRequestRequestTypeDef,
    CreateIpAccessSettingsResponseTypeDef,
    CreateNetworkSettingsRequestRequestTypeDef,
    CreateNetworkSettingsResponseTypeDef,
    CreatePortalRequestRequestTypeDef,
    CreatePortalResponseTypeDef,
    CreateTrustStoreRequestRequestTypeDef,
    CreateTrustStoreResponseTypeDef,
    CreateUserAccessLoggingSettingsRequestRequestTypeDef,
    CreateUserAccessLoggingSettingsResponseTypeDef,
    CreateUserSettingsRequestRequestTypeDef,
    CreateUserSettingsResponseTypeDef,
    DeleteBrowserSettingsRequestRequestTypeDef,
    DeleteIdentityProviderRequestRequestTypeDef,
    DeleteIpAccessSettingsRequestRequestTypeDef,
    DeleteNetworkSettingsRequestRequestTypeDef,
    DeletePortalRequestRequestTypeDef,
    DeleteTrustStoreRequestRequestTypeDef,
    DeleteUserAccessLoggingSettingsRequestRequestTypeDef,
    DeleteUserSettingsRequestRequestTypeDef,
    DisassociateBrowserSettingsRequestRequestTypeDef,
    DisassociateIpAccessSettingsRequestRequestTypeDef,
    DisassociateNetworkSettingsRequestRequestTypeDef,
    DisassociateTrustStoreRequestRequestTypeDef,
    DisassociateUserAccessLoggingSettingsRequestRequestTypeDef,
    DisassociateUserSettingsRequestRequestTypeDef,
    ExpireSessionRequestRequestTypeDef,
    GetBrowserSettingsRequestRequestTypeDef,
    GetBrowserSettingsResponseTypeDef,
    GetIdentityProviderRequestRequestTypeDef,
    GetIdentityProviderResponseTypeDef,
    GetIpAccessSettingsRequestRequestTypeDef,
    GetIpAccessSettingsResponseTypeDef,
    GetNetworkSettingsRequestRequestTypeDef,
    GetNetworkSettingsResponseTypeDef,
    GetPortalRequestRequestTypeDef,
    GetPortalResponseTypeDef,
    GetPortalServiceProviderMetadataRequestRequestTypeDef,
    GetPortalServiceProviderMetadataResponseTypeDef,
    GetSessionRequestRequestTypeDef,
    GetSessionResponseTypeDef,
    GetTrustStoreCertificateRequestRequestTypeDef,
    GetTrustStoreCertificateResponseTypeDef,
    GetTrustStoreRequestRequestTypeDef,
    GetTrustStoreResponseTypeDef,
    GetUserAccessLoggingSettingsRequestRequestTypeDef,
    GetUserAccessLoggingSettingsResponseTypeDef,
    GetUserSettingsRequestRequestTypeDef,
    GetUserSettingsResponseTypeDef,
    ListBrowserSettingsRequestRequestTypeDef,
    ListBrowserSettingsResponseTypeDef,
    ListIdentityProvidersRequestRequestTypeDef,
    ListIdentityProvidersResponseTypeDef,
    ListIpAccessSettingsRequestRequestTypeDef,
    ListIpAccessSettingsResponseTypeDef,
    ListNetworkSettingsRequestRequestTypeDef,
    ListNetworkSettingsResponseTypeDef,
    ListPortalsRequestRequestTypeDef,
    ListPortalsResponseTypeDef,
    ListSessionsRequestRequestTypeDef,
    ListSessionsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTrustStoreCertificatesRequestRequestTypeDef,
    ListTrustStoreCertificatesResponseTypeDef,
    ListTrustStoresRequestRequestTypeDef,
    ListTrustStoresResponseTypeDef,
    ListUserAccessLoggingSettingsRequestRequestTypeDef,
    ListUserAccessLoggingSettingsResponseTypeDef,
    ListUserSettingsRequestRequestTypeDef,
    ListUserSettingsResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateBrowserSettingsRequestRequestTypeDef,
    UpdateBrowserSettingsResponseTypeDef,
    UpdateIdentityProviderRequestRequestTypeDef,
    UpdateIdentityProviderResponseTypeDef,
    UpdateIpAccessSettingsRequestRequestTypeDef,
    UpdateIpAccessSettingsResponseTypeDef,
    UpdateNetworkSettingsRequestRequestTypeDef,
    UpdateNetworkSettingsResponseTypeDef,
    UpdatePortalRequestRequestTypeDef,
    UpdatePortalResponseTypeDef,
    UpdateTrustStoreRequestRequestTypeDef,
    UpdateTrustStoreResponseTypeDef,
    UpdateUserAccessLoggingSettingsRequestRequestTypeDef,
    UpdateUserAccessLoggingSettingsResponseTypeDef,
    UpdateUserSettingsRequestRequestTypeDef,
    UpdateUserSettingsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("WorkSpacesWebClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class WorkSpacesWebClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web.html#WorkSpacesWeb.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WorkSpacesWebClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web.html#WorkSpacesWeb.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#close)
        """

    async def associate_browser_settings(
        self, **kwargs: Unpack[AssociateBrowserSettingsRequestRequestTypeDef]
    ) -> AssociateBrowserSettingsResponseTypeDef:
        """
        Associates a browser settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_browser_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#associate_browser_settings)
        """

    async def associate_ip_access_settings(
        self, **kwargs: Unpack[AssociateIpAccessSettingsRequestRequestTypeDef]
    ) -> AssociateIpAccessSettingsResponseTypeDef:
        """
        Associates an IP access settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_ip_access_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#associate_ip_access_settings)
        """

    async def associate_network_settings(
        self, **kwargs: Unpack[AssociateNetworkSettingsRequestRequestTypeDef]
    ) -> AssociateNetworkSettingsResponseTypeDef:
        """
        Associates a network settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_network_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#associate_network_settings)
        """

    async def associate_trust_store(
        self, **kwargs: Unpack[AssociateTrustStoreRequestRequestTypeDef]
    ) -> AssociateTrustStoreResponseTypeDef:
        """
        Associates a trust store with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_trust_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#associate_trust_store)
        """

    async def associate_user_access_logging_settings(
        self, **kwargs: Unpack[AssociateUserAccessLoggingSettingsRequestRequestTypeDef]
    ) -> AssociateUserAccessLoggingSettingsResponseTypeDef:
        """
        Associates a user access logging settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_user_access_logging_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#associate_user_access_logging_settings)
        """

    async def associate_user_settings(
        self, **kwargs: Unpack[AssociateUserSettingsRequestRequestTypeDef]
    ) -> AssociateUserSettingsResponseTypeDef:
        """
        Associates a user settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_user_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#associate_user_settings)
        """

    async def create_browser_settings(
        self, **kwargs: Unpack[CreateBrowserSettingsRequestRequestTypeDef]
    ) -> CreateBrowserSettingsResponseTypeDef:
        """
        Creates a browser settings resource that can be associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_browser_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_browser_settings)
        """

    async def create_identity_provider(
        self, **kwargs: Unpack[CreateIdentityProviderRequestRequestTypeDef]
    ) -> CreateIdentityProviderResponseTypeDef:
        """
        Creates an identity provider resource that is then associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_identity_provider.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_identity_provider)
        """

    async def create_ip_access_settings(
        self, **kwargs: Unpack[CreateIpAccessSettingsRequestRequestTypeDef]
    ) -> CreateIpAccessSettingsResponseTypeDef:
        """
        Creates an IP access settings resource that can be associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_ip_access_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_ip_access_settings)
        """

    async def create_network_settings(
        self, **kwargs: Unpack[CreateNetworkSettingsRequestRequestTypeDef]
    ) -> CreateNetworkSettingsResponseTypeDef:
        """
        Creates a network settings resource that can be associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_network_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_network_settings)
        """

    async def create_portal(
        self, **kwargs: Unpack[CreatePortalRequestRequestTypeDef]
    ) -> CreatePortalResponseTypeDef:
        """
        Creates a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_portal.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_portal)
        """

    async def create_trust_store(
        self, **kwargs: Unpack[CreateTrustStoreRequestRequestTypeDef]
    ) -> CreateTrustStoreResponseTypeDef:
        """
        Creates a trust store that can be associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_trust_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_trust_store)
        """

    async def create_user_access_logging_settings(
        self, **kwargs: Unpack[CreateUserAccessLoggingSettingsRequestRequestTypeDef]
    ) -> CreateUserAccessLoggingSettingsResponseTypeDef:
        """
        Creates a user access logging settings resource that can be associated with a
        web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_user_access_logging_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_user_access_logging_settings)
        """

    async def create_user_settings(
        self, **kwargs: Unpack[CreateUserSettingsRequestRequestTypeDef]
    ) -> CreateUserSettingsResponseTypeDef:
        """
        Creates a user settings resource that can be associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_user_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_user_settings)
        """

    async def delete_browser_settings(
        self, **kwargs: Unpack[DeleteBrowserSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes browser settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_browser_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_browser_settings)
        """

    async def delete_identity_provider(
        self, **kwargs: Unpack[DeleteIdentityProviderRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_identity_provider.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_identity_provider)
        """

    async def delete_ip_access_settings(
        self, **kwargs: Unpack[DeleteIpAccessSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes IP access settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_ip_access_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_ip_access_settings)
        """

    async def delete_network_settings(
        self, **kwargs: Unpack[DeleteNetworkSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes network settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_network_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_network_settings)
        """

    async def delete_portal(
        self, **kwargs: Unpack[DeletePortalRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_portal.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_portal)
        """

    async def delete_trust_store(
        self, **kwargs: Unpack[DeleteTrustStoreRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the trust store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_trust_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_trust_store)
        """

    async def delete_user_access_logging_settings(
        self, **kwargs: Unpack[DeleteUserAccessLoggingSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes user access logging settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_user_access_logging_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_user_access_logging_settings)
        """

    async def delete_user_settings(
        self, **kwargs: Unpack[DeleteUserSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes user settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_user_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_user_settings)
        """

    async def disassociate_browser_settings(
        self, **kwargs: Unpack[DisassociateBrowserSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates browser settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_browser_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#disassociate_browser_settings)
        """

    async def disassociate_ip_access_settings(
        self, **kwargs: Unpack[DisassociateIpAccessSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates IP access settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_ip_access_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#disassociate_ip_access_settings)
        """

    async def disassociate_network_settings(
        self, **kwargs: Unpack[DisassociateNetworkSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates network settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_network_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#disassociate_network_settings)
        """

    async def disassociate_trust_store(
        self, **kwargs: Unpack[DisassociateTrustStoreRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a trust store from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_trust_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#disassociate_trust_store)
        """

    async def disassociate_user_access_logging_settings(
        self, **kwargs: Unpack[DisassociateUserAccessLoggingSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates user access logging settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_user_access_logging_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#disassociate_user_access_logging_settings)
        """

    async def disassociate_user_settings(
        self, **kwargs: Unpack[DisassociateUserSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates user settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_user_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#disassociate_user_settings)
        """

    async def expire_session(
        self, **kwargs: Unpack[ExpireSessionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Expires an active secure browser session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/expire_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#expire_session)
        """

    async def get_browser_settings(
        self, **kwargs: Unpack[GetBrowserSettingsRequestRequestTypeDef]
    ) -> GetBrowserSettingsResponseTypeDef:
        """
        Gets browser settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_browser_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_browser_settings)
        """

    async def get_identity_provider(
        self, **kwargs: Unpack[GetIdentityProviderRequestRequestTypeDef]
    ) -> GetIdentityProviderResponseTypeDef:
        """
        Gets the identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_identity_provider.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_identity_provider)
        """

    async def get_ip_access_settings(
        self, **kwargs: Unpack[GetIpAccessSettingsRequestRequestTypeDef]
    ) -> GetIpAccessSettingsResponseTypeDef:
        """
        Gets the IP access settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_ip_access_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_ip_access_settings)
        """

    async def get_network_settings(
        self, **kwargs: Unpack[GetNetworkSettingsRequestRequestTypeDef]
    ) -> GetNetworkSettingsResponseTypeDef:
        """
        Gets the network settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_network_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_network_settings)
        """

    async def get_portal(
        self, **kwargs: Unpack[GetPortalRequestRequestTypeDef]
    ) -> GetPortalResponseTypeDef:
        """
        Gets the web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_portal.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_portal)
        """

    async def get_portal_service_provider_metadata(
        self, **kwargs: Unpack[GetPortalServiceProviderMetadataRequestRequestTypeDef]
    ) -> GetPortalServiceProviderMetadataResponseTypeDef:
        """
        Gets the service provider metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_portal_service_provider_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_portal_service_provider_metadata)
        """

    async def get_session(
        self, **kwargs: Unpack[GetSessionRequestRequestTypeDef]
    ) -> GetSessionResponseTypeDef:
        """
        Gets information for a secure browser session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_session)
        """

    async def get_trust_store(
        self, **kwargs: Unpack[GetTrustStoreRequestRequestTypeDef]
    ) -> GetTrustStoreResponseTypeDef:
        """
        Gets the trust store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_trust_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_trust_store)
        """

    async def get_trust_store_certificate(
        self, **kwargs: Unpack[GetTrustStoreCertificateRequestRequestTypeDef]
    ) -> GetTrustStoreCertificateResponseTypeDef:
        """
        Gets the trust store certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_trust_store_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_trust_store_certificate)
        """

    async def get_user_access_logging_settings(
        self, **kwargs: Unpack[GetUserAccessLoggingSettingsRequestRequestTypeDef]
    ) -> GetUserAccessLoggingSettingsResponseTypeDef:
        """
        Gets user access logging settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_user_access_logging_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_user_access_logging_settings)
        """

    async def get_user_settings(
        self, **kwargs: Unpack[GetUserSettingsRequestRequestTypeDef]
    ) -> GetUserSettingsResponseTypeDef:
        """
        Gets user settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_user_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_user_settings)
        """

    async def list_browser_settings(
        self, **kwargs: Unpack[ListBrowserSettingsRequestRequestTypeDef]
    ) -> ListBrowserSettingsResponseTypeDef:
        """
        Retrieves a list of browser settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_browser_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_browser_settings)
        """

    async def list_identity_providers(
        self, **kwargs: Unpack[ListIdentityProvidersRequestRequestTypeDef]
    ) -> ListIdentityProvidersResponseTypeDef:
        """
        Retrieves a list of identity providers for a specific web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_identity_providers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_identity_providers)
        """

    async def list_ip_access_settings(
        self, **kwargs: Unpack[ListIpAccessSettingsRequestRequestTypeDef]
    ) -> ListIpAccessSettingsResponseTypeDef:
        """
        Retrieves a list of IP access settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_ip_access_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_ip_access_settings)
        """

    async def list_network_settings(
        self, **kwargs: Unpack[ListNetworkSettingsRequestRequestTypeDef]
    ) -> ListNetworkSettingsResponseTypeDef:
        """
        Retrieves a list of network settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_network_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_network_settings)
        """

    async def list_portals(
        self, **kwargs: Unpack[ListPortalsRequestRequestTypeDef]
    ) -> ListPortalsResponseTypeDef:
        """
        Retrieves a list or web portals.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_portals.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_portals)
        """

    async def list_sessions(
        self, **kwargs: Unpack[ListSessionsRequestRequestTypeDef]
    ) -> ListSessionsResponseTypeDef:
        """
        Lists information for multiple secure browser sessions from a specific portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_sessions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_sessions)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves a list of tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_tags_for_resource)
        """

    async def list_trust_store_certificates(
        self, **kwargs: Unpack[ListTrustStoreCertificatesRequestRequestTypeDef]
    ) -> ListTrustStoreCertificatesResponseTypeDef:
        """
        Retrieves a list of trust store certificates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_trust_store_certificates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_trust_store_certificates)
        """

    async def list_trust_stores(
        self, **kwargs: Unpack[ListTrustStoresRequestRequestTypeDef]
    ) -> ListTrustStoresResponseTypeDef:
        """
        Retrieves a list of trust stores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_trust_stores.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_trust_stores)
        """

    async def list_user_access_logging_settings(
        self, **kwargs: Unpack[ListUserAccessLoggingSettingsRequestRequestTypeDef]
    ) -> ListUserAccessLoggingSettingsResponseTypeDef:
        """
        Retrieves a list of user access logging settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_user_access_logging_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_user_access_logging_settings)
        """

    async def list_user_settings(
        self, **kwargs: Unpack[ListUserSettingsRequestRequestTypeDef]
    ) -> ListUserSettingsResponseTypeDef:
        """
        Retrieves a list of user settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_user_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_user_settings)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds or overwrites one or more tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#untag_resource)
        """

    async def update_browser_settings(
        self, **kwargs: Unpack[UpdateBrowserSettingsRequestRequestTypeDef]
    ) -> UpdateBrowserSettingsResponseTypeDef:
        """
        Updates browser settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_browser_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_browser_settings)
        """

    async def update_identity_provider(
        self, **kwargs: Unpack[UpdateIdentityProviderRequestRequestTypeDef]
    ) -> UpdateIdentityProviderResponseTypeDef:
        """
        Updates the identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_identity_provider.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_identity_provider)
        """

    async def update_ip_access_settings(
        self, **kwargs: Unpack[UpdateIpAccessSettingsRequestRequestTypeDef]
    ) -> UpdateIpAccessSettingsResponseTypeDef:
        """
        Updates IP access settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_ip_access_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_ip_access_settings)
        """

    async def update_network_settings(
        self, **kwargs: Unpack[UpdateNetworkSettingsRequestRequestTypeDef]
    ) -> UpdateNetworkSettingsResponseTypeDef:
        """
        Updates network settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_network_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_network_settings)
        """

    async def update_portal(
        self, **kwargs: Unpack[UpdatePortalRequestRequestTypeDef]
    ) -> UpdatePortalResponseTypeDef:
        """
        Updates a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_portal.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_portal)
        """

    async def update_trust_store(
        self, **kwargs: Unpack[UpdateTrustStoreRequestRequestTypeDef]
    ) -> UpdateTrustStoreResponseTypeDef:
        """
        Updates the trust store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_trust_store.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_trust_store)
        """

    async def update_user_access_logging_settings(
        self, **kwargs: Unpack[UpdateUserAccessLoggingSettingsRequestRequestTypeDef]
    ) -> UpdateUserAccessLoggingSettingsResponseTypeDef:
        """
        Updates the user access logging settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_user_access_logging_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_user_access_logging_settings)
        """

    async def update_user_settings(
        self, **kwargs: Unpack[UpdateUserSettingsRequestRequestTypeDef]
    ) -> UpdateUserSettingsResponseTypeDef:
        """
        Updates the user settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_user_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_user_settings)
        """

    def get_paginator(self, operation_name: Literal["list_sessions"]) -> ListSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_paginator)
        """

    async def __aenter__(self) -> "WorkSpacesWebClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web.html#WorkSpacesWeb.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web.html#WorkSpacesWeb.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/)
        """
