"""
Type annotations for workmail service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_workmail.client import WorkMailClient

    session = get_session()
    async with session.create_client("workmail") as client:
        client: WorkMailClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListAliasesPaginator,
    ListAvailabilityConfigurationsPaginator,
    ListGroupMembersPaginator,
    ListGroupsPaginator,
    ListMailboxPermissionsPaginator,
    ListOrganizationsPaginator,
    ListResourceDelegatesPaginator,
    ListResourcesPaginator,
    ListUsersPaginator,
)
from .type_defs import (
    AssociateDelegateToResourceRequestRequestTypeDef,
    AssociateMemberToGroupRequestRequestTypeDef,
    AssumeImpersonationRoleRequestRequestTypeDef,
    AssumeImpersonationRoleResponseTypeDef,
    CancelMailboxExportJobRequestRequestTypeDef,
    CreateAliasRequestRequestTypeDef,
    CreateAvailabilityConfigurationRequestRequestTypeDef,
    CreateGroupRequestRequestTypeDef,
    CreateGroupResponseTypeDef,
    CreateImpersonationRoleRequestRequestTypeDef,
    CreateImpersonationRoleResponseTypeDef,
    CreateMobileDeviceAccessRuleRequestRequestTypeDef,
    CreateMobileDeviceAccessRuleResponseTypeDef,
    CreateOrganizationRequestRequestTypeDef,
    CreateOrganizationResponseTypeDef,
    CreateResourceRequestRequestTypeDef,
    CreateResourceResponseTypeDef,
    CreateUserRequestRequestTypeDef,
    CreateUserResponseTypeDef,
    DeleteAccessControlRuleRequestRequestTypeDef,
    DeleteAliasRequestRequestTypeDef,
    DeleteAvailabilityConfigurationRequestRequestTypeDef,
    DeleteEmailMonitoringConfigurationRequestRequestTypeDef,
    DeleteGroupRequestRequestTypeDef,
    DeleteImpersonationRoleRequestRequestTypeDef,
    DeleteMailboxPermissionsRequestRequestTypeDef,
    DeleteMobileDeviceAccessOverrideRequestRequestTypeDef,
    DeleteMobileDeviceAccessRuleRequestRequestTypeDef,
    DeleteOrganizationRequestRequestTypeDef,
    DeleteOrganizationResponseTypeDef,
    DeleteResourceRequestRequestTypeDef,
    DeleteRetentionPolicyRequestRequestTypeDef,
    DeleteUserRequestRequestTypeDef,
    DeregisterFromWorkMailRequestRequestTypeDef,
    DeregisterMailDomainRequestRequestTypeDef,
    DescribeEmailMonitoringConfigurationRequestRequestTypeDef,
    DescribeEmailMonitoringConfigurationResponseTypeDef,
    DescribeEntityRequestRequestTypeDef,
    DescribeEntityResponseTypeDef,
    DescribeGroupRequestRequestTypeDef,
    DescribeGroupResponseTypeDef,
    DescribeInboundDmarcSettingsRequestRequestTypeDef,
    DescribeInboundDmarcSettingsResponseTypeDef,
    DescribeMailboxExportJobRequestRequestTypeDef,
    DescribeMailboxExportJobResponseTypeDef,
    DescribeOrganizationRequestRequestTypeDef,
    DescribeOrganizationResponseTypeDef,
    DescribeResourceRequestRequestTypeDef,
    DescribeResourceResponseTypeDef,
    DescribeUserRequestRequestTypeDef,
    DescribeUserResponseTypeDef,
    DisassociateDelegateFromResourceRequestRequestTypeDef,
    DisassociateMemberFromGroupRequestRequestTypeDef,
    GetAccessControlEffectRequestRequestTypeDef,
    GetAccessControlEffectResponseTypeDef,
    GetDefaultRetentionPolicyRequestRequestTypeDef,
    GetDefaultRetentionPolicyResponseTypeDef,
    GetImpersonationRoleEffectRequestRequestTypeDef,
    GetImpersonationRoleEffectResponseTypeDef,
    GetImpersonationRoleRequestRequestTypeDef,
    GetImpersonationRoleResponseTypeDef,
    GetMailboxDetailsRequestRequestTypeDef,
    GetMailboxDetailsResponseTypeDef,
    GetMailDomainRequestRequestTypeDef,
    GetMailDomainResponseTypeDef,
    GetMobileDeviceAccessEffectRequestRequestTypeDef,
    GetMobileDeviceAccessEffectResponseTypeDef,
    GetMobileDeviceAccessOverrideRequestRequestTypeDef,
    GetMobileDeviceAccessOverrideResponseTypeDef,
    ListAccessControlRulesRequestRequestTypeDef,
    ListAccessControlRulesResponseTypeDef,
    ListAliasesRequestRequestTypeDef,
    ListAliasesResponseTypeDef,
    ListAvailabilityConfigurationsRequestRequestTypeDef,
    ListAvailabilityConfigurationsResponseTypeDef,
    ListGroupMembersRequestRequestTypeDef,
    ListGroupMembersResponseTypeDef,
    ListGroupsForEntityRequestRequestTypeDef,
    ListGroupsForEntityResponseTypeDef,
    ListGroupsRequestRequestTypeDef,
    ListGroupsResponseTypeDef,
    ListImpersonationRolesRequestRequestTypeDef,
    ListImpersonationRolesResponseTypeDef,
    ListMailboxExportJobsRequestRequestTypeDef,
    ListMailboxExportJobsResponseTypeDef,
    ListMailboxPermissionsRequestRequestTypeDef,
    ListMailboxPermissionsResponseTypeDef,
    ListMailDomainsRequestRequestTypeDef,
    ListMailDomainsResponseTypeDef,
    ListMobileDeviceAccessOverridesRequestRequestTypeDef,
    ListMobileDeviceAccessOverridesResponseTypeDef,
    ListMobileDeviceAccessRulesRequestRequestTypeDef,
    ListMobileDeviceAccessRulesResponseTypeDef,
    ListOrganizationsRequestRequestTypeDef,
    ListOrganizationsResponseTypeDef,
    ListResourceDelegatesRequestRequestTypeDef,
    ListResourceDelegatesResponseTypeDef,
    ListResourcesRequestRequestTypeDef,
    ListResourcesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUsersRequestRequestTypeDef,
    ListUsersResponseTypeDef,
    PutAccessControlRuleRequestRequestTypeDef,
    PutEmailMonitoringConfigurationRequestRequestTypeDef,
    PutInboundDmarcSettingsRequestRequestTypeDef,
    PutMailboxPermissionsRequestRequestTypeDef,
    PutMobileDeviceAccessOverrideRequestRequestTypeDef,
    PutRetentionPolicyRequestRequestTypeDef,
    RegisterMailDomainRequestRequestTypeDef,
    RegisterToWorkMailRequestRequestTypeDef,
    ResetPasswordRequestRequestTypeDef,
    StartMailboxExportJobRequestRequestTypeDef,
    StartMailboxExportJobResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    TestAvailabilityConfigurationRequestRequestTypeDef,
    TestAvailabilityConfigurationResponseTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAvailabilityConfigurationRequestRequestTypeDef,
    UpdateDefaultMailDomainRequestRequestTypeDef,
    UpdateGroupRequestRequestTypeDef,
    UpdateImpersonationRoleRequestRequestTypeDef,
    UpdateMailboxQuotaRequestRequestTypeDef,
    UpdateMobileDeviceAccessRuleRequestRequestTypeDef,
    UpdatePrimaryEmailAddressRequestRequestTypeDef,
    UpdateResourceRequestRequestTypeDef,
    UpdateUserRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("WorkMailClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    DirectoryInUseException: Type[BotocoreClientError]
    DirectoryServiceAuthenticationFailedException: Type[BotocoreClientError]
    DirectoryUnavailableException: Type[BotocoreClientError]
    EmailAddressInUseException: Type[BotocoreClientError]
    EntityAlreadyRegisteredException: Type[BotocoreClientError]
    EntityNotFoundException: Type[BotocoreClientError]
    EntityStateException: Type[BotocoreClientError]
    InvalidConfigurationException: Type[BotocoreClientError]
    InvalidCustomSesConfigurationException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidPasswordException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MailDomainInUseException: Type[BotocoreClientError]
    MailDomainNotFoundException: Type[BotocoreClientError]
    MailDomainStateException: Type[BotocoreClientError]
    NameAvailabilityException: Type[BotocoreClientError]
    OrganizationNotFoundException: Type[BotocoreClientError]
    OrganizationStateException: Type[BotocoreClientError]
    ReservedNameException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]


class WorkMailClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WorkMailClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#close)
        """

    async def associate_delegate_to_resource(
        self, **kwargs: Unpack[AssociateDelegateToResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds a member (user or group) to the resource's set of delegates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/associate_delegate_to_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#associate_delegate_to_resource)
        """

    async def associate_member_to_group(
        self, **kwargs: Unpack[AssociateMemberToGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds a member (user or group) to the group's set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/associate_member_to_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#associate_member_to_group)
        """

    async def assume_impersonation_role(
        self, **kwargs: Unpack[AssumeImpersonationRoleRequestRequestTypeDef]
    ) -> AssumeImpersonationRoleResponseTypeDef:
        """
        Assumes an impersonation role for the given WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/assume_impersonation_role.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#assume_impersonation_role)
        """

    async def cancel_mailbox_export_job(
        self, **kwargs: Unpack[CancelMailboxExportJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels a mailbox export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/cancel_mailbox_export_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#cancel_mailbox_export_job)
        """

    async def create_alias(
        self, **kwargs: Unpack[CreateAliasRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds an alias to the set of a given member (user or group) of WorkMail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/create_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#create_alias)
        """

    async def create_availability_configuration(
        self, **kwargs: Unpack[CreateAvailabilityConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates an <code>AvailabilityConfiguration</code> for the given WorkMail
        organization and domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/create_availability_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#create_availability_configuration)
        """

    async def create_group(
        self, **kwargs: Unpack[CreateGroupRequestRequestTypeDef]
    ) -> CreateGroupResponseTypeDef:
        """
        Creates a group that can be used in WorkMail by calling the
        <a>RegisterToWorkMail</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/create_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#create_group)
        """

    async def create_impersonation_role(
        self, **kwargs: Unpack[CreateImpersonationRoleRequestRequestTypeDef]
    ) -> CreateImpersonationRoleResponseTypeDef:
        """
        Creates an impersonation role for the given WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/create_impersonation_role.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#create_impersonation_role)
        """

    async def create_mobile_device_access_rule(
        self, **kwargs: Unpack[CreateMobileDeviceAccessRuleRequestRequestTypeDef]
    ) -> CreateMobileDeviceAccessRuleResponseTypeDef:
        """
        Creates a new mobile device access rule for the specified WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/create_mobile_device_access_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#create_mobile_device_access_rule)
        """

    async def create_organization(
        self, **kwargs: Unpack[CreateOrganizationRequestRequestTypeDef]
    ) -> CreateOrganizationResponseTypeDef:
        """
        Creates a new WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/create_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#create_organization)
        """

    async def create_resource(
        self, **kwargs: Unpack[CreateResourceRequestRequestTypeDef]
    ) -> CreateResourceResponseTypeDef:
        """
        Creates a new WorkMail resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/create_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#create_resource)
        """

    async def create_user(
        self, **kwargs: Unpack[CreateUserRequestRequestTypeDef]
    ) -> CreateUserResponseTypeDef:
        """
        Creates a user who can be used in WorkMail by calling the
        <a>RegisterToWorkMail</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/create_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#create_user)
        """

    async def delete_access_control_rule(
        self, **kwargs: Unpack[DeleteAccessControlRuleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an access control rule for the specified WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/delete_access_control_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_access_control_rule)
        """

    async def delete_alias(
        self, **kwargs: Unpack[DeleteAliasRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove one or more specified aliases from a set of aliases for a given user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/delete_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_alias)
        """

    async def delete_availability_configuration(
        self, **kwargs: Unpack[DeleteAvailabilityConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the <code>AvailabilityConfiguration</code> for the given WorkMail
        organization and domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/delete_availability_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_availability_configuration)
        """

    async def delete_email_monitoring_configuration(
        self, **kwargs: Unpack[DeleteEmailMonitoringConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the email monitoring configuration for a specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/delete_email_monitoring_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_email_monitoring_configuration)
        """

    async def delete_group(
        self, **kwargs: Unpack[DeleteGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a group from WorkMail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/delete_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_group)
        """

    async def delete_impersonation_role(
        self, **kwargs: Unpack[DeleteImpersonationRoleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an impersonation role for the given WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/delete_impersonation_role.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_impersonation_role)
        """

    async def delete_mailbox_permissions(
        self, **kwargs: Unpack[DeleteMailboxPermissionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes permissions granted to a member (user or group).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/delete_mailbox_permissions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_mailbox_permissions)
        """

    async def delete_mobile_device_access_override(
        self, **kwargs: Unpack[DeleteMobileDeviceAccessOverrideRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the mobile device access override for the given WorkMail organization,
        user, and device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/delete_mobile_device_access_override.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_mobile_device_access_override)
        """

    async def delete_mobile_device_access_rule(
        self, **kwargs: Unpack[DeleteMobileDeviceAccessRuleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a mobile device access rule for the specified WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/delete_mobile_device_access_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_mobile_device_access_rule)
        """

    async def delete_organization(
        self, **kwargs: Unpack[DeleteOrganizationRequestRequestTypeDef]
    ) -> DeleteOrganizationResponseTypeDef:
        """
        Deletes an WorkMail organization and all underlying AWS resources managed by
        WorkMail as part of the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/delete_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_organization)
        """

    async def delete_resource(
        self, **kwargs: Unpack[DeleteResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/delete_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_resource)
        """

    async def delete_retention_policy(
        self, **kwargs: Unpack[DeleteRetentionPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified retention policy from the specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/delete_retention_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_retention_policy)
        """

    async def delete_user(
        self, **kwargs: Unpack[DeleteUserRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a user from WorkMail and all subsequent systems.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/delete_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#delete_user)
        """

    async def deregister_from_work_mail(
        self, **kwargs: Unpack[DeregisterFromWorkMailRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Mark a user, group, or resource as no longer used in WorkMail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/deregister_from_work_mail.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#deregister_from_work_mail)
        """

    async def deregister_mail_domain(
        self, **kwargs: Unpack[DeregisterMailDomainRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a domain from WorkMail, stops email routing to WorkMail, and removes
        the authorization allowing WorkMail use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/deregister_mail_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#deregister_mail_domain)
        """

    async def describe_email_monitoring_configuration(
        self, **kwargs: Unpack[DescribeEmailMonitoringConfigurationRequestRequestTypeDef]
    ) -> DescribeEmailMonitoringConfigurationResponseTypeDef:
        """
        Describes the current email monitoring configuration for a specified
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/describe_email_monitoring_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#describe_email_monitoring_configuration)
        """

    async def describe_entity(
        self, **kwargs: Unpack[DescribeEntityRequestRequestTypeDef]
    ) -> DescribeEntityResponseTypeDef:
        """
        Returns basic details about an entity in WorkMail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/describe_entity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#describe_entity)
        """

    async def describe_group(
        self, **kwargs: Unpack[DescribeGroupRequestRequestTypeDef]
    ) -> DescribeGroupResponseTypeDef:
        """
        Returns the data available for the group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/describe_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#describe_group)
        """

    async def describe_inbound_dmarc_settings(
        self, **kwargs: Unpack[DescribeInboundDmarcSettingsRequestRequestTypeDef]
    ) -> DescribeInboundDmarcSettingsResponseTypeDef:
        """
        Lists the settings in a DMARC policy for a specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/describe_inbound_dmarc_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#describe_inbound_dmarc_settings)
        """

    async def describe_mailbox_export_job(
        self, **kwargs: Unpack[DescribeMailboxExportJobRequestRequestTypeDef]
    ) -> DescribeMailboxExportJobResponseTypeDef:
        """
        Describes the current status of a mailbox export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/describe_mailbox_export_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#describe_mailbox_export_job)
        """

    async def describe_organization(
        self, **kwargs: Unpack[DescribeOrganizationRequestRequestTypeDef]
    ) -> DescribeOrganizationResponseTypeDef:
        """
        Provides more information regarding a given organization based on its
        identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/describe_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#describe_organization)
        """

    async def describe_resource(
        self, **kwargs: Unpack[DescribeResourceRequestRequestTypeDef]
    ) -> DescribeResourceResponseTypeDef:
        """
        Returns the data available for the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/describe_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#describe_resource)
        """

    async def describe_user(
        self, **kwargs: Unpack[DescribeUserRequestRequestTypeDef]
    ) -> DescribeUserResponseTypeDef:
        """
        Provides information regarding the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/describe_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#describe_user)
        """

    async def disassociate_delegate_from_resource(
        self, **kwargs: Unpack[DisassociateDelegateFromResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a member from the resource's set of delegates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/disassociate_delegate_from_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#disassociate_delegate_from_resource)
        """

    async def disassociate_member_from_group(
        self, **kwargs: Unpack[DisassociateMemberFromGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a member from a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/disassociate_member_from_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#disassociate_member_from_group)
        """

    async def get_access_control_effect(
        self, **kwargs: Unpack[GetAccessControlEffectRequestRequestTypeDef]
    ) -> GetAccessControlEffectResponseTypeDef:
        """
        Gets the effects of an organization's access control rules as they apply to a
        specified IPv4 address, access protocol action, and user ID or impersonation
        role ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_access_control_effect.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_access_control_effect)
        """

    async def get_default_retention_policy(
        self, **kwargs: Unpack[GetDefaultRetentionPolicyRequestRequestTypeDef]
    ) -> GetDefaultRetentionPolicyResponseTypeDef:
        """
        Gets the default retention policy details for the specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_default_retention_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_default_retention_policy)
        """

    async def get_impersonation_role(
        self, **kwargs: Unpack[GetImpersonationRoleRequestRequestTypeDef]
    ) -> GetImpersonationRoleResponseTypeDef:
        """
        Gets the impersonation role details for the given WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_impersonation_role.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_impersonation_role)
        """

    async def get_impersonation_role_effect(
        self, **kwargs: Unpack[GetImpersonationRoleEffectRequestRequestTypeDef]
    ) -> GetImpersonationRoleEffectResponseTypeDef:
        """
        Tests whether the given impersonation role can impersonate a target user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_impersonation_role_effect.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_impersonation_role_effect)
        """

    async def get_mail_domain(
        self, **kwargs: Unpack[GetMailDomainRequestRequestTypeDef]
    ) -> GetMailDomainResponseTypeDef:
        """
        Gets details for a mail domain, including domain records required to configure
        your domain with recommended security.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_mail_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_mail_domain)
        """

    async def get_mailbox_details(
        self, **kwargs: Unpack[GetMailboxDetailsRequestRequestTypeDef]
    ) -> GetMailboxDetailsResponseTypeDef:
        """
        Requests a user's mailbox details for a specified organization and user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_mailbox_details.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_mailbox_details)
        """

    async def get_mobile_device_access_effect(
        self, **kwargs: Unpack[GetMobileDeviceAccessEffectRequestRequestTypeDef]
    ) -> GetMobileDeviceAccessEffectResponseTypeDef:
        """
        Simulates the effect of the mobile device access rules for the given attributes
        of a sample access event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_mobile_device_access_effect.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_mobile_device_access_effect)
        """

    async def get_mobile_device_access_override(
        self, **kwargs: Unpack[GetMobileDeviceAccessOverrideRequestRequestTypeDef]
    ) -> GetMobileDeviceAccessOverrideResponseTypeDef:
        """
        Gets the mobile device access override for the given WorkMail organization,
        user, and device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_mobile_device_access_override.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_mobile_device_access_override)
        """

    async def list_access_control_rules(
        self, **kwargs: Unpack[ListAccessControlRulesRequestRequestTypeDef]
    ) -> ListAccessControlRulesResponseTypeDef:
        """
        Lists the access control rules for the specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_access_control_rules.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_access_control_rules)
        """

    async def list_aliases(
        self, **kwargs: Unpack[ListAliasesRequestRequestTypeDef]
    ) -> ListAliasesResponseTypeDef:
        """
        Creates a paginated call to list the aliases associated with a given entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_aliases.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_aliases)
        """

    async def list_availability_configurations(
        self, **kwargs: Unpack[ListAvailabilityConfigurationsRequestRequestTypeDef]
    ) -> ListAvailabilityConfigurationsResponseTypeDef:
        """
        List all the <code>AvailabilityConfiguration</code>'s for the given WorkMail
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_availability_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_availability_configurations)
        """

    async def list_group_members(
        self, **kwargs: Unpack[ListGroupMembersRequestRequestTypeDef]
    ) -> ListGroupMembersResponseTypeDef:
        """
        Returns an overview of the members of a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_group_members.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_group_members)
        """

    async def list_groups(
        self, **kwargs: Unpack[ListGroupsRequestRequestTypeDef]
    ) -> ListGroupsResponseTypeDef:
        """
        Returns summaries of the organization's groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_groups)
        """

    async def list_groups_for_entity(
        self, **kwargs: Unpack[ListGroupsForEntityRequestRequestTypeDef]
    ) -> ListGroupsForEntityResponseTypeDef:
        """
        Returns all the groups to which an entity belongs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_groups_for_entity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_groups_for_entity)
        """

    async def list_impersonation_roles(
        self, **kwargs: Unpack[ListImpersonationRolesRequestRequestTypeDef]
    ) -> ListImpersonationRolesResponseTypeDef:
        """
        Lists all the impersonation roles for the given WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_impersonation_roles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_impersonation_roles)
        """

    async def list_mail_domains(
        self, **kwargs: Unpack[ListMailDomainsRequestRequestTypeDef]
    ) -> ListMailDomainsResponseTypeDef:
        """
        Lists the mail domains in a given WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_mail_domains.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_mail_domains)
        """

    async def list_mailbox_export_jobs(
        self, **kwargs: Unpack[ListMailboxExportJobsRequestRequestTypeDef]
    ) -> ListMailboxExportJobsResponseTypeDef:
        """
        Lists the mailbox export jobs started for the specified organization within the
        last seven days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_mailbox_export_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_mailbox_export_jobs)
        """

    async def list_mailbox_permissions(
        self, **kwargs: Unpack[ListMailboxPermissionsRequestRequestTypeDef]
    ) -> ListMailboxPermissionsResponseTypeDef:
        """
        Lists the mailbox permissions associated with a user, group, or resource
        mailbox.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_mailbox_permissions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_mailbox_permissions)
        """

    async def list_mobile_device_access_overrides(
        self, **kwargs: Unpack[ListMobileDeviceAccessOverridesRequestRequestTypeDef]
    ) -> ListMobileDeviceAccessOverridesResponseTypeDef:
        """
        Lists all the mobile device access overrides for any given combination of
        WorkMail organization, user, or device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_mobile_device_access_overrides.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_mobile_device_access_overrides)
        """

    async def list_mobile_device_access_rules(
        self, **kwargs: Unpack[ListMobileDeviceAccessRulesRequestRequestTypeDef]
    ) -> ListMobileDeviceAccessRulesResponseTypeDef:
        """
        Lists the mobile device access rules for the specified WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_mobile_device_access_rules.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_mobile_device_access_rules)
        """

    async def list_organizations(
        self, **kwargs: Unpack[ListOrganizationsRequestRequestTypeDef]
    ) -> ListOrganizationsResponseTypeDef:
        """
        Returns summaries of the customer's organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_organizations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_organizations)
        """

    async def list_resource_delegates(
        self, **kwargs: Unpack[ListResourceDelegatesRequestRequestTypeDef]
    ) -> ListResourceDelegatesResponseTypeDef:
        """
        Lists the delegates associated with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_resource_delegates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_resource_delegates)
        """

    async def list_resources(
        self, **kwargs: Unpack[ListResourcesRequestRequestTypeDef]
    ) -> ListResourcesResponseTypeDef:
        """
        Returns summaries of the organization's resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_resources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_resources)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags applied to an WorkMail organization resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_tags_for_resource)
        """

    async def list_users(
        self, **kwargs: Unpack[ListUsersRequestRequestTypeDef]
    ) -> ListUsersResponseTypeDef:
        """
        Returns summaries of the organization's users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/list_users.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#list_users)
        """

    async def put_access_control_rule(
        self, **kwargs: Unpack[PutAccessControlRuleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds a new access control rule for the specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/put_access_control_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#put_access_control_rule)
        """

    async def put_email_monitoring_configuration(
        self, **kwargs: Unpack[PutEmailMonitoringConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates the email monitoring configuration for a specified
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/put_email_monitoring_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#put_email_monitoring_configuration)
        """

    async def put_inbound_dmarc_settings(
        self, **kwargs: Unpack[PutInboundDmarcSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enables or disables a DMARC policy for a given organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/put_inbound_dmarc_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#put_inbound_dmarc_settings)
        """

    async def put_mailbox_permissions(
        self, **kwargs: Unpack[PutMailboxPermissionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets permissions for a user, group, or resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/put_mailbox_permissions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#put_mailbox_permissions)
        """

    async def put_mobile_device_access_override(
        self, **kwargs: Unpack[PutMobileDeviceAccessOverrideRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates a mobile device access override for the given WorkMail
        organization, user, and device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/put_mobile_device_access_override.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#put_mobile_device_access_override)
        """

    async def put_retention_policy(
        self, **kwargs: Unpack[PutRetentionPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Puts a retention policy to the specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/put_retention_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#put_retention_policy)
        """

    async def register_mail_domain(
        self, **kwargs: Unpack[RegisterMailDomainRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Registers a new domain in WorkMail and SES, and configures it for use by
        WorkMail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/register_mail_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#register_mail_domain)
        """

    async def register_to_work_mail(
        self, **kwargs: Unpack[RegisterToWorkMailRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Registers an existing and disabled user, group, or resource for WorkMail use by
        associating a mailbox and calendaring capabilities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/register_to_work_mail.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#register_to_work_mail)
        """

    async def reset_password(
        self, **kwargs: Unpack[ResetPasswordRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Allows the administrator to reset the password for a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/reset_password.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#reset_password)
        """

    async def start_mailbox_export_job(
        self, **kwargs: Unpack[StartMailboxExportJobRequestRequestTypeDef]
    ) -> StartMailboxExportJobResponseTypeDef:
        """
        Starts a mailbox export job to export MIME-format email messages and calendar
        items from the specified mailbox to the specified Amazon Simple Storage Service
        (Amazon S3) bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/start_mailbox_export_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#start_mailbox_export_job)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Applies the specified tags to the specified WorkMailorganization resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#tag_resource)
        """

    async def test_availability_configuration(
        self, **kwargs: Unpack[TestAvailabilityConfigurationRequestRequestTypeDef]
    ) -> TestAvailabilityConfigurationResponseTypeDef:
        """
        Performs a test on an availability provider to ensure that access is allowed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/test_availability_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#test_availability_configuration)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Untags the specified tags from the specified WorkMail organization resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#untag_resource)
        """

    async def update_availability_configuration(
        self, **kwargs: Unpack[UpdateAvailabilityConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an existing <code>AvailabilityConfiguration</code> for the given
        WorkMail organization and domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/update_availability_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_availability_configuration)
        """

    async def update_default_mail_domain(
        self, **kwargs: Unpack[UpdateDefaultMailDomainRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the default mail domain for an organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/update_default_mail_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_default_mail_domain)
        """

    async def update_group(
        self, **kwargs: Unpack[UpdateGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates attibutes in a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/update_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_group)
        """

    async def update_impersonation_role(
        self, **kwargs: Unpack[UpdateImpersonationRoleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an impersonation role for the given WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/update_impersonation_role.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_impersonation_role)
        """

    async def update_mailbox_quota(
        self, **kwargs: Unpack[UpdateMailboxQuotaRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a user's current mailbox quota for a specified organization and user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/update_mailbox_quota.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_mailbox_quota)
        """

    async def update_mobile_device_access_rule(
        self, **kwargs: Unpack[UpdateMobileDeviceAccessRuleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a mobile device access rule for the specified WorkMail organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/update_mobile_device_access_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_mobile_device_access_rule)
        """

    async def update_primary_email_address(
        self, **kwargs: Unpack[UpdatePrimaryEmailAddressRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the primary email for a user, group, or resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/update_primary_email_address.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_primary_email_address)
        """

    async def update_resource(
        self, **kwargs: Unpack[UpdateResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates data for the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/update_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_resource)
        """

    async def update_user(
        self, **kwargs: Unpack[UpdateUserRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates data for the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/update_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#update_user)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_aliases"]) -> ListAliasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_availability_configurations"]
    ) -> ListAvailabilityConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_members"]
    ) -> ListGroupMembersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_mailbox_permissions"]
    ) -> ListMailboxPermissionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_organizations"]
    ) -> ListOrganizationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_delegates"]
    ) -> ListResourceDelegatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_resources"]) -> ListResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/#get_paginator)
        """

    async def __aenter__(self) -> "WorkMailClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail.html#WorkMail.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/client/)
        """
