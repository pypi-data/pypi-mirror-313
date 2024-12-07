"""
Type annotations for iam service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iam.client import IAMClient
    from types_aiobotocore_iam.paginator import (
        GetAccountAuthorizationDetailsPaginator,
        GetGroupPaginator,
        ListAccessKeysPaginator,
        ListAccountAliasesPaginator,
        ListAttachedGroupPoliciesPaginator,
        ListAttachedRolePoliciesPaginator,
        ListAttachedUserPoliciesPaginator,
        ListEntitiesForPolicyPaginator,
        ListGroupPoliciesPaginator,
        ListGroupsForUserPaginator,
        ListGroupsPaginator,
        ListInstanceProfileTagsPaginator,
        ListInstanceProfilesForRolePaginator,
        ListInstanceProfilesPaginator,
        ListMFADeviceTagsPaginator,
        ListMFADevicesPaginator,
        ListOpenIDConnectProviderTagsPaginator,
        ListPoliciesPaginator,
        ListPolicyTagsPaginator,
        ListPolicyVersionsPaginator,
        ListRolePoliciesPaginator,
        ListRoleTagsPaginator,
        ListRolesPaginator,
        ListSAMLProviderTagsPaginator,
        ListSSHPublicKeysPaginator,
        ListServerCertificateTagsPaginator,
        ListServerCertificatesPaginator,
        ListSigningCertificatesPaginator,
        ListUserPoliciesPaginator,
        ListUserTagsPaginator,
        ListUsersPaginator,
        ListVirtualMFADevicesPaginator,
        SimulateCustomPolicyPaginator,
        SimulatePrincipalPolicyPaginator,
    )

    session = get_session()
    with session.create_client("iam") as client:
        client: IAMClient

        get_account_authorization_details_paginator: GetAccountAuthorizationDetailsPaginator = client.get_paginator("get_account_authorization_details")
        get_group_paginator: GetGroupPaginator = client.get_paginator("get_group")
        list_access_keys_paginator: ListAccessKeysPaginator = client.get_paginator("list_access_keys")
        list_account_aliases_paginator: ListAccountAliasesPaginator = client.get_paginator("list_account_aliases")
        list_attached_group_policies_paginator: ListAttachedGroupPoliciesPaginator = client.get_paginator("list_attached_group_policies")
        list_attached_role_policies_paginator: ListAttachedRolePoliciesPaginator = client.get_paginator("list_attached_role_policies")
        list_attached_user_policies_paginator: ListAttachedUserPoliciesPaginator = client.get_paginator("list_attached_user_policies")
        list_entities_for_policy_paginator: ListEntitiesForPolicyPaginator = client.get_paginator("list_entities_for_policy")
        list_group_policies_paginator: ListGroupPoliciesPaginator = client.get_paginator("list_group_policies")
        list_groups_for_user_paginator: ListGroupsForUserPaginator = client.get_paginator("list_groups_for_user")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        list_instance_profile_tags_paginator: ListInstanceProfileTagsPaginator = client.get_paginator("list_instance_profile_tags")
        list_instance_profiles_for_role_paginator: ListInstanceProfilesForRolePaginator = client.get_paginator("list_instance_profiles_for_role")
        list_instance_profiles_paginator: ListInstanceProfilesPaginator = client.get_paginator("list_instance_profiles")
        list_mfa_device_tags_paginator: ListMFADeviceTagsPaginator = client.get_paginator("list_mfa_device_tags")
        list_mfa_devices_paginator: ListMFADevicesPaginator = client.get_paginator("list_mfa_devices")
        list_open_id_connect_provider_tags_paginator: ListOpenIDConnectProviderTagsPaginator = client.get_paginator("list_open_id_connect_provider_tags")
        list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
        list_policy_tags_paginator: ListPolicyTagsPaginator = client.get_paginator("list_policy_tags")
        list_policy_versions_paginator: ListPolicyVersionsPaginator = client.get_paginator("list_policy_versions")
        list_role_policies_paginator: ListRolePoliciesPaginator = client.get_paginator("list_role_policies")
        list_role_tags_paginator: ListRoleTagsPaginator = client.get_paginator("list_role_tags")
        list_roles_paginator: ListRolesPaginator = client.get_paginator("list_roles")
        list_saml_provider_tags_paginator: ListSAMLProviderTagsPaginator = client.get_paginator("list_saml_provider_tags")
        list_ssh_public_keys_paginator: ListSSHPublicKeysPaginator = client.get_paginator("list_ssh_public_keys")
        list_server_certificate_tags_paginator: ListServerCertificateTagsPaginator = client.get_paginator("list_server_certificate_tags")
        list_server_certificates_paginator: ListServerCertificatesPaginator = client.get_paginator("list_server_certificates")
        list_signing_certificates_paginator: ListSigningCertificatesPaginator = client.get_paginator("list_signing_certificates")
        list_user_policies_paginator: ListUserPoliciesPaginator = client.get_paginator("list_user_policies")
        list_user_tags_paginator: ListUserTagsPaginator = client.get_paginator("list_user_tags")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
        list_virtual_mfa_devices_paginator: ListVirtualMFADevicesPaginator = client.get_paginator("list_virtual_mfa_devices")
        simulate_custom_policy_paginator: SimulateCustomPolicyPaginator = client.get_paginator("simulate_custom_policy")
        simulate_principal_policy_paginator: SimulatePrincipalPolicyPaginator = client.get_paginator("simulate_principal_policy")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetAccountAuthorizationDetailsRequestGetAccountAuthorizationDetailsPaginateTypeDef,
    GetAccountAuthorizationDetailsResponseTypeDef,
    GetGroupRequestGetGroupPaginateTypeDef,
    GetGroupResponseTypeDef,
    ListAccessKeysRequestListAccessKeysPaginateTypeDef,
    ListAccessKeysResponseTypeDef,
    ListAccountAliasesRequestListAccountAliasesPaginateTypeDef,
    ListAccountAliasesResponseTypeDef,
    ListAttachedGroupPoliciesRequestListAttachedGroupPoliciesPaginateTypeDef,
    ListAttachedGroupPoliciesResponseTypeDef,
    ListAttachedRolePoliciesRequestListAttachedRolePoliciesPaginateTypeDef,
    ListAttachedRolePoliciesResponseTypeDef,
    ListAttachedUserPoliciesRequestListAttachedUserPoliciesPaginateTypeDef,
    ListAttachedUserPoliciesResponseTypeDef,
    ListEntitiesForPolicyRequestListEntitiesForPolicyPaginateTypeDef,
    ListEntitiesForPolicyResponseTypeDef,
    ListGroupPoliciesRequestListGroupPoliciesPaginateTypeDef,
    ListGroupPoliciesResponseTypeDef,
    ListGroupsForUserRequestListGroupsForUserPaginateTypeDef,
    ListGroupsForUserResponseTypeDef,
    ListGroupsRequestListGroupsPaginateTypeDef,
    ListGroupsResponseTypeDef,
    ListInstanceProfilesForRoleRequestListInstanceProfilesForRolePaginateTypeDef,
    ListInstanceProfilesForRoleResponseTypeDef,
    ListInstanceProfilesRequestListInstanceProfilesPaginateTypeDef,
    ListInstanceProfilesResponseTypeDef,
    ListInstanceProfileTagsRequestListInstanceProfileTagsPaginateTypeDef,
    ListInstanceProfileTagsResponseTypeDef,
    ListMFADevicesRequestListMFADevicesPaginateTypeDef,
    ListMFADevicesResponseTypeDef,
    ListMFADeviceTagsRequestListMFADeviceTagsPaginateTypeDef,
    ListMFADeviceTagsResponseTypeDef,
    ListOpenIDConnectProviderTagsRequestListOpenIDConnectProviderTagsPaginateTypeDef,
    ListOpenIDConnectProviderTagsResponseTypeDef,
    ListPoliciesRequestListPoliciesPaginateTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyTagsRequestListPolicyTagsPaginateTypeDef,
    ListPolicyTagsResponseTypeDef,
    ListPolicyVersionsRequestListPolicyVersionsPaginateTypeDef,
    ListPolicyVersionsResponseTypeDef,
    ListRolePoliciesRequestListRolePoliciesPaginateTypeDef,
    ListRolePoliciesResponseTypeDef,
    ListRolesRequestListRolesPaginateTypeDef,
    ListRolesResponseTypeDef,
    ListRoleTagsRequestListRoleTagsPaginateTypeDef,
    ListRoleTagsResponseTypeDef,
    ListSAMLProviderTagsRequestListSAMLProviderTagsPaginateTypeDef,
    ListSAMLProviderTagsResponseTypeDef,
    ListServerCertificatesRequestListServerCertificatesPaginateTypeDef,
    ListServerCertificatesResponseTypeDef,
    ListServerCertificateTagsRequestListServerCertificateTagsPaginateTypeDef,
    ListServerCertificateTagsResponseTypeDef,
    ListSigningCertificatesRequestListSigningCertificatesPaginateTypeDef,
    ListSigningCertificatesResponseTypeDef,
    ListSSHPublicKeysRequestListSSHPublicKeysPaginateTypeDef,
    ListSSHPublicKeysResponseTypeDef,
    ListUserPoliciesRequestListUserPoliciesPaginateTypeDef,
    ListUserPoliciesResponseTypeDef,
    ListUsersRequestListUsersPaginateTypeDef,
    ListUsersResponseTypeDef,
    ListUserTagsRequestListUserTagsPaginateTypeDef,
    ListUserTagsResponseTypeDef,
    ListVirtualMFADevicesRequestListVirtualMFADevicesPaginateTypeDef,
    ListVirtualMFADevicesResponseTypeDef,
    SimulateCustomPolicyRequestSimulateCustomPolicyPaginateTypeDef,
    SimulatePolicyResponseTypeDef,
    SimulatePrincipalPolicyRequestSimulatePrincipalPolicyPaginateTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetAccountAuthorizationDetailsPaginator",
    "GetGroupPaginator",
    "ListAccessKeysPaginator",
    "ListAccountAliasesPaginator",
    "ListAttachedGroupPoliciesPaginator",
    "ListAttachedRolePoliciesPaginator",
    "ListAttachedUserPoliciesPaginator",
    "ListEntitiesForPolicyPaginator",
    "ListGroupPoliciesPaginator",
    "ListGroupsForUserPaginator",
    "ListGroupsPaginator",
    "ListInstanceProfileTagsPaginator",
    "ListInstanceProfilesForRolePaginator",
    "ListInstanceProfilesPaginator",
    "ListMFADeviceTagsPaginator",
    "ListMFADevicesPaginator",
    "ListOpenIDConnectProviderTagsPaginator",
    "ListPoliciesPaginator",
    "ListPolicyTagsPaginator",
    "ListPolicyVersionsPaginator",
    "ListRolePoliciesPaginator",
    "ListRoleTagsPaginator",
    "ListRolesPaginator",
    "ListSAMLProviderTagsPaginator",
    "ListSSHPublicKeysPaginator",
    "ListServerCertificateTagsPaginator",
    "ListServerCertificatesPaginator",
    "ListSigningCertificatesPaginator",
    "ListUserPoliciesPaginator",
    "ListUserTagsPaginator",
    "ListUsersPaginator",
    "ListVirtualMFADevicesPaginator",
    "SimulateCustomPolicyPaginator",
    "SimulatePrincipalPolicyPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetAccountAuthorizationDetailsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/GetAccountAuthorizationDetails.html#IAM.Paginator.GetAccountAuthorizationDetails)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#getaccountauthorizationdetailspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetAccountAuthorizationDetailsRequestGetAccountAuthorizationDetailsPaginateTypeDef
        ],
    ) -> AsyncIterator[GetAccountAuthorizationDetailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/GetAccountAuthorizationDetails.html#IAM.Paginator.GetAccountAuthorizationDetails.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#getaccountauthorizationdetailspaginator)
        """

class GetGroupPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/GetGroup.html#IAM.Paginator.GetGroup)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#getgrouppaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetGroupRequestGetGroupPaginateTypeDef]
    ) -> AsyncIterator[GetGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/GetGroup.html#IAM.Paginator.GetGroup.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#getgrouppaginator)
        """

class ListAccessKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAccessKeys.html#IAM.Paginator.ListAccessKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listaccesskeyspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccessKeysRequestListAccessKeysPaginateTypeDef]
    ) -> AsyncIterator[ListAccessKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAccessKeys.html#IAM.Paginator.ListAccessKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listaccesskeyspaginator)
        """

class ListAccountAliasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAccountAliases.html#IAM.Paginator.ListAccountAliases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listaccountaliasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccountAliasesRequestListAccountAliasesPaginateTypeDef]
    ) -> AsyncIterator[ListAccountAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAccountAliases.html#IAM.Paginator.ListAccountAliases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listaccountaliasespaginator)
        """

class ListAttachedGroupPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedGroupPolicies.html#IAM.Paginator.ListAttachedGroupPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattachedgrouppoliciespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListAttachedGroupPoliciesRequestListAttachedGroupPoliciesPaginateTypeDef],
    ) -> AsyncIterator[ListAttachedGroupPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedGroupPolicies.html#IAM.Paginator.ListAttachedGroupPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattachedgrouppoliciespaginator)
        """

class ListAttachedRolePoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedRolePolicies.html#IAM.Paginator.ListAttachedRolePolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattachedrolepoliciespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListAttachedRolePoliciesRequestListAttachedRolePoliciesPaginateTypeDef],
    ) -> AsyncIterator[ListAttachedRolePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedRolePolicies.html#IAM.Paginator.ListAttachedRolePolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattachedrolepoliciespaginator)
        """

class ListAttachedUserPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedUserPolicies.html#IAM.Paginator.ListAttachedUserPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattacheduserpoliciespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListAttachedUserPoliciesRequestListAttachedUserPoliciesPaginateTypeDef],
    ) -> AsyncIterator[ListAttachedUserPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListAttachedUserPolicies.html#IAM.Paginator.ListAttachedUserPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattacheduserpoliciespaginator)
        """

class ListEntitiesForPolicyPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListEntitiesForPolicy.html#IAM.Paginator.ListEntitiesForPolicy)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listentitiesforpolicypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEntitiesForPolicyRequestListEntitiesForPolicyPaginateTypeDef]
    ) -> AsyncIterator[ListEntitiesForPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListEntitiesForPolicy.html#IAM.Paginator.ListEntitiesForPolicy.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listentitiesforpolicypaginator)
        """

class ListGroupPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroupPolicies.html#IAM.Paginator.ListGroupPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgrouppoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroupPoliciesRequestListGroupPoliciesPaginateTypeDef]
    ) -> AsyncIterator[ListGroupPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroupPolicies.html#IAM.Paginator.ListGroupPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgrouppoliciespaginator)
        """

class ListGroupsForUserPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroupsForUser.html#IAM.Paginator.ListGroupsForUser)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgroupsforuserpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroupsForUserRequestListGroupsForUserPaginateTypeDef]
    ) -> AsyncIterator[ListGroupsForUserResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroupsForUser.html#IAM.Paginator.ListGroupsForUser.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgroupsforuserpaginator)
        """

class ListGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroups.html#IAM.Paginator.ListGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroupsRequestListGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListGroups.html#IAM.Paginator.ListGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgroupspaginator)
        """

class ListInstanceProfileTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfileTags.html#IAM.Paginator.ListInstanceProfileTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listinstanceprofiletagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInstanceProfileTagsRequestListInstanceProfileTagsPaginateTypeDef]
    ) -> AsyncIterator[ListInstanceProfileTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfileTags.html#IAM.Paginator.ListInstanceProfileTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listinstanceprofiletagspaginator)
        """

class ListInstanceProfilesForRolePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfilesForRole.html#IAM.Paginator.ListInstanceProfilesForRole)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listinstanceprofilesforrolepaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListInstanceProfilesForRoleRequestListInstanceProfilesForRolePaginateTypeDef
        ],
    ) -> AsyncIterator[ListInstanceProfilesForRoleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfilesForRole.html#IAM.Paginator.ListInstanceProfilesForRole.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listinstanceprofilesforrolepaginator)
        """

class ListInstanceProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfiles.html#IAM.Paginator.ListInstanceProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listinstanceprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInstanceProfilesRequestListInstanceProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListInstanceProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListInstanceProfiles.html#IAM.Paginator.ListInstanceProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listinstanceprofilespaginator)
        """

class ListMFADeviceTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListMFADeviceTags.html#IAM.Paginator.ListMFADeviceTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listmfadevicetagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMFADeviceTagsRequestListMFADeviceTagsPaginateTypeDef]
    ) -> AsyncIterator[ListMFADeviceTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListMFADeviceTags.html#IAM.Paginator.ListMFADeviceTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listmfadevicetagspaginator)
        """

class ListMFADevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListMFADevices.html#IAM.Paginator.ListMFADevices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listmfadevicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMFADevicesRequestListMFADevicesPaginateTypeDef]
    ) -> AsyncIterator[ListMFADevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListMFADevices.html#IAM.Paginator.ListMFADevices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listmfadevicespaginator)
        """

class ListOpenIDConnectProviderTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListOpenIDConnectProviderTags.html#IAM.Paginator.ListOpenIDConnectProviderTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listopenidconnectprovidertagspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListOpenIDConnectProviderTagsRequestListOpenIDConnectProviderTagsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListOpenIDConnectProviderTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListOpenIDConnectProviderTags.html#IAM.Paginator.ListOpenIDConnectProviderTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listopenidconnectprovidertagspaginator)
        """

class ListPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicies.html#IAM.Paginator.ListPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPoliciesRequestListPoliciesPaginateTypeDef]
    ) -> AsyncIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicies.html#IAM.Paginator.ListPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listpoliciespaginator)
        """

class ListPolicyTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicyTags.html#IAM.Paginator.ListPolicyTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listpolicytagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPolicyTagsRequestListPolicyTagsPaginateTypeDef]
    ) -> AsyncIterator[ListPolicyTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicyTags.html#IAM.Paginator.ListPolicyTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listpolicytagspaginator)
        """

class ListPolicyVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicyVersions.html#IAM.Paginator.ListPolicyVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listpolicyversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPolicyVersionsRequestListPolicyVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListPolicyVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListPolicyVersions.html#IAM.Paginator.ListPolicyVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listpolicyversionspaginator)
        """

class ListRolePoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRolePolicies.html#IAM.Paginator.ListRolePolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listrolepoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRolePoliciesRequestListRolePoliciesPaginateTypeDef]
    ) -> AsyncIterator[ListRolePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRolePolicies.html#IAM.Paginator.ListRolePolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listrolepoliciespaginator)
        """

class ListRoleTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRoleTags.html#IAM.Paginator.ListRoleTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listroletagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRoleTagsRequestListRoleTagsPaginateTypeDef]
    ) -> AsyncIterator[ListRoleTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRoleTags.html#IAM.Paginator.ListRoleTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listroletagspaginator)
        """

class ListRolesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRoles.html#IAM.Paginator.ListRoles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listrolespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRolesRequestListRolesPaginateTypeDef]
    ) -> AsyncIterator[ListRolesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListRoles.html#IAM.Paginator.ListRoles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listrolespaginator)
        """

class ListSAMLProviderTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSAMLProviderTags.html#IAM.Paginator.ListSAMLProviderTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listsamlprovidertagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSAMLProviderTagsRequestListSAMLProviderTagsPaginateTypeDef]
    ) -> AsyncIterator[ListSAMLProviderTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSAMLProviderTags.html#IAM.Paginator.ListSAMLProviderTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listsamlprovidertagspaginator)
        """

class ListSSHPublicKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSSHPublicKeys.html#IAM.Paginator.ListSSHPublicKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listsshpublickeyspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSSHPublicKeysRequestListSSHPublicKeysPaginateTypeDef]
    ) -> AsyncIterator[ListSSHPublicKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSSHPublicKeys.html#IAM.Paginator.ListSSHPublicKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listsshpublickeyspaginator)
        """

class ListServerCertificateTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListServerCertificateTags.html#IAM.Paginator.ListServerCertificateTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listservercertificatetagspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListServerCertificateTagsRequestListServerCertificateTagsPaginateTypeDef],
    ) -> AsyncIterator[ListServerCertificateTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListServerCertificateTags.html#IAM.Paginator.ListServerCertificateTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listservercertificatetagspaginator)
        """

class ListServerCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListServerCertificates.html#IAM.Paginator.ListServerCertificates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listservercertificatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListServerCertificatesRequestListServerCertificatesPaginateTypeDef]
    ) -> AsyncIterator[ListServerCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListServerCertificates.html#IAM.Paginator.ListServerCertificates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listservercertificatespaginator)
        """

class ListSigningCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSigningCertificates.html#IAM.Paginator.ListSigningCertificates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listsigningcertificatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSigningCertificatesRequestListSigningCertificatesPaginateTypeDef]
    ) -> AsyncIterator[ListSigningCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListSigningCertificates.html#IAM.Paginator.ListSigningCertificates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listsigningcertificatespaginator)
        """

class ListUserPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUserPolicies.html#IAM.Paginator.ListUserPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listuserpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUserPoliciesRequestListUserPoliciesPaginateTypeDef]
    ) -> AsyncIterator[ListUserPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUserPolicies.html#IAM.Paginator.ListUserPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listuserpoliciespaginator)
        """

class ListUserTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUserTags.html#IAM.Paginator.ListUserTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listusertagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUserTagsRequestListUserTagsPaginateTypeDef]
    ) -> AsyncIterator[ListUserTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUserTags.html#IAM.Paginator.ListUserTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listusertagspaginator)
        """

class ListUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUsers.html#IAM.Paginator.ListUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listuserspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUsersRequestListUsersPaginateTypeDef]
    ) -> AsyncIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListUsers.html#IAM.Paginator.ListUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listuserspaginator)
        """

class ListVirtualMFADevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListVirtualMFADevices.html#IAM.Paginator.ListVirtualMFADevices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listvirtualmfadevicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListVirtualMFADevicesRequestListVirtualMFADevicesPaginateTypeDef]
    ) -> AsyncIterator[ListVirtualMFADevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/ListVirtualMFADevices.html#IAM.Paginator.ListVirtualMFADevices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listvirtualmfadevicespaginator)
        """

class SimulateCustomPolicyPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/SimulateCustomPolicy.html#IAM.Paginator.SimulateCustomPolicy)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#simulatecustompolicypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SimulateCustomPolicyRequestSimulateCustomPolicyPaginateTypeDef]
    ) -> AsyncIterator[SimulatePolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/SimulateCustomPolicy.html#IAM.Paginator.SimulateCustomPolicy.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#simulatecustompolicypaginator)
        """

class SimulatePrincipalPolicyPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/SimulatePrincipalPolicy.html#IAM.Paginator.SimulatePrincipalPolicy)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#simulateprincipalpolicypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SimulatePrincipalPolicyRequestSimulatePrincipalPolicyPaginateTypeDef]
    ) -> AsyncIterator[SimulatePolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/paginator/SimulatePrincipalPolicy.html#IAM.Paginator.SimulatePrincipalPolicy.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#simulateprincipalpolicypaginator)
        """
