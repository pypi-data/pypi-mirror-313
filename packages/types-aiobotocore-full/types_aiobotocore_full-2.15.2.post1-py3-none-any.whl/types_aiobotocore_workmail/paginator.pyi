"""
Type annotations for workmail service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_workmail.client import WorkMailClient
    from types_aiobotocore_workmail.paginator import (
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

    session = get_session()
    with session.create_client("workmail") as client:
        client: WorkMailClient

        list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
        list_availability_configurations_paginator: ListAvailabilityConfigurationsPaginator = client.get_paginator("list_availability_configurations")
        list_group_members_paginator: ListGroupMembersPaginator = client.get_paginator("list_group_members")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        list_mailbox_permissions_paginator: ListMailboxPermissionsPaginator = client.get_paginator("list_mailbox_permissions")
        list_organizations_paginator: ListOrganizationsPaginator = client.get_paginator("list_organizations")
        list_resource_delegates_paginator: ListResourceDelegatesPaginator = client.get_paginator("list_resource_delegates")
        list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAliasesRequestListAliasesPaginateTypeDef,
    ListAliasesResponseTypeDef,
    ListAvailabilityConfigurationsRequestListAvailabilityConfigurationsPaginateTypeDef,
    ListAvailabilityConfigurationsResponseTypeDef,
    ListGroupMembersRequestListGroupMembersPaginateTypeDef,
    ListGroupMembersResponseTypeDef,
    ListGroupsRequestListGroupsPaginateTypeDef,
    ListGroupsResponseTypeDef,
    ListMailboxPermissionsRequestListMailboxPermissionsPaginateTypeDef,
    ListMailboxPermissionsResponseTypeDef,
    ListOrganizationsRequestListOrganizationsPaginateTypeDef,
    ListOrganizationsResponseTypeDef,
    ListResourceDelegatesRequestListResourceDelegatesPaginateTypeDef,
    ListResourceDelegatesResponseTypeDef,
    ListResourcesRequestListResourcesPaginateTypeDef,
    ListResourcesResponseTypeDef,
    ListUsersRequestListUsersPaginateTypeDef,
    ListUsersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAliasesPaginator",
    "ListAvailabilityConfigurationsPaginator",
    "ListGroupMembersPaginator",
    "ListGroupsPaginator",
    "ListMailboxPermissionsPaginator",
    "ListOrganizationsPaginator",
    "ListResourceDelegatesPaginator",
    "ListResourcesPaginator",
    "ListUsersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAliasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListAliases.html#WorkMail.Paginator.ListAliases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listaliasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAliasesRequestListAliasesPaginateTypeDef]
    ) -> AsyncIterator[ListAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListAliases.html#WorkMail.Paginator.ListAliases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listaliasespaginator)
        """

class ListAvailabilityConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListAvailabilityConfigurations.html#WorkMail.Paginator.ListAvailabilityConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listavailabilityconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAvailabilityConfigurationsRequestListAvailabilityConfigurationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAvailabilityConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListAvailabilityConfigurations.html#WorkMail.Paginator.ListAvailabilityConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listavailabilityconfigurationspaginator)
        """

class ListGroupMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListGroupMembers.html#WorkMail.Paginator.ListGroupMembers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listgroupmemberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroupMembersRequestListGroupMembersPaginateTypeDef]
    ) -> AsyncIterator[ListGroupMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListGroupMembers.html#WorkMail.Paginator.ListGroupMembers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listgroupmemberspaginator)
        """

class ListGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListGroups.html#WorkMail.Paginator.ListGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroupsRequestListGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListGroups.html#WorkMail.Paginator.ListGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listgroupspaginator)
        """

class ListMailboxPermissionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListMailboxPermissions.html#WorkMail.Paginator.ListMailboxPermissions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listmailboxpermissionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMailboxPermissionsRequestListMailboxPermissionsPaginateTypeDef]
    ) -> AsyncIterator[ListMailboxPermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListMailboxPermissions.html#WorkMail.Paginator.ListMailboxPermissions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listmailboxpermissionspaginator)
        """

class ListOrganizationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListOrganizations.html#WorkMail.Paginator.ListOrganizations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listorganizationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListOrganizationsRequestListOrganizationsPaginateTypeDef]
    ) -> AsyncIterator[ListOrganizationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListOrganizations.html#WorkMail.Paginator.ListOrganizations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listorganizationspaginator)
        """

class ListResourceDelegatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListResourceDelegates.html#WorkMail.Paginator.ListResourceDelegates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listresourcedelegatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListResourceDelegatesRequestListResourceDelegatesPaginateTypeDef]
    ) -> AsyncIterator[ListResourceDelegatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListResourceDelegates.html#WorkMail.Paginator.ListResourceDelegates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listresourcedelegatespaginator)
        """

class ListResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListResources.html#WorkMail.Paginator.ListResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListResourcesRequestListResourcesPaginateTypeDef]
    ) -> AsyncIterator[ListResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListResources.html#WorkMail.Paginator.ListResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listresourcespaginator)
        """

class ListUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListUsers.html#WorkMail.Paginator.ListUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listuserspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUsersRequestListUsersPaginateTypeDef]
    ) -> AsyncIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workmail/paginator/ListUsers.html#WorkMail.Paginator.ListUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmail/paginators/#listuserspaginator)
        """
