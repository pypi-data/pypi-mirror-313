"""
Type annotations for workdocs service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_workdocs.client import WorkDocsClient
    from types_aiobotocore_workdocs.paginator import (
        DescribeActivitiesPaginator,
        DescribeCommentsPaginator,
        DescribeDocumentVersionsPaginator,
        DescribeFolderContentsPaginator,
        DescribeGroupsPaginator,
        DescribeNotificationSubscriptionsPaginator,
        DescribeResourcePermissionsPaginator,
        DescribeRootFoldersPaginator,
        DescribeUsersPaginator,
        SearchResourcesPaginator,
    )

    session = get_session()
    with session.create_client("workdocs") as client:
        client: WorkDocsClient

        describe_activities_paginator: DescribeActivitiesPaginator = client.get_paginator("describe_activities")
        describe_comments_paginator: DescribeCommentsPaginator = client.get_paginator("describe_comments")
        describe_document_versions_paginator: DescribeDocumentVersionsPaginator = client.get_paginator("describe_document_versions")
        describe_folder_contents_paginator: DescribeFolderContentsPaginator = client.get_paginator("describe_folder_contents")
        describe_groups_paginator: DescribeGroupsPaginator = client.get_paginator("describe_groups")
        describe_notification_subscriptions_paginator: DescribeNotificationSubscriptionsPaginator = client.get_paginator("describe_notification_subscriptions")
        describe_resource_permissions_paginator: DescribeResourcePermissionsPaginator = client.get_paginator("describe_resource_permissions")
        describe_root_folders_paginator: DescribeRootFoldersPaginator = client.get_paginator("describe_root_folders")
        describe_users_paginator: DescribeUsersPaginator = client.get_paginator("describe_users")
        search_resources_paginator: SearchResourcesPaginator = client.get_paginator("search_resources")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeActivitiesRequestDescribeActivitiesPaginateTypeDef,
    DescribeActivitiesResponseTypeDef,
    DescribeCommentsRequestDescribeCommentsPaginateTypeDef,
    DescribeCommentsResponseTypeDef,
    DescribeDocumentVersionsRequestDescribeDocumentVersionsPaginateTypeDef,
    DescribeDocumentVersionsResponseTypeDef,
    DescribeFolderContentsRequestDescribeFolderContentsPaginateTypeDef,
    DescribeFolderContentsResponseTypeDef,
    DescribeGroupsRequestDescribeGroupsPaginateTypeDef,
    DescribeGroupsResponseTypeDef,
    DescribeNotificationSubscriptionsRequestDescribeNotificationSubscriptionsPaginateTypeDef,
    DescribeNotificationSubscriptionsResponseTypeDef,
    DescribeResourcePermissionsRequestDescribeResourcePermissionsPaginateTypeDef,
    DescribeResourcePermissionsResponseTypeDef,
    DescribeRootFoldersRequestDescribeRootFoldersPaginateTypeDef,
    DescribeRootFoldersResponseTypeDef,
    DescribeUsersRequestDescribeUsersPaginateTypeDef,
    DescribeUsersResponseTypeDef,
    SearchResourcesRequestSearchResourcesPaginateTypeDef,
    SearchResourcesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeActivitiesPaginator",
    "DescribeCommentsPaginator",
    "DescribeDocumentVersionsPaginator",
    "DescribeFolderContentsPaginator",
    "DescribeGroupsPaginator",
    "DescribeNotificationSubscriptionsPaginator",
    "DescribeResourcePermissionsPaginator",
    "DescribeRootFoldersPaginator",
    "DescribeUsersPaginator",
    "SearchResourcesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeActivitiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeActivities.html#WorkDocs.Paginator.DescribeActivities)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeactivitiespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeActivitiesRequestDescribeActivitiesPaginateTypeDef]
    ) -> AsyncIterator[DescribeActivitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeActivities.html#WorkDocs.Paginator.DescribeActivities.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeactivitiespaginator)
        """

class DescribeCommentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeComments.html#WorkDocs.Paginator.DescribeComments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describecommentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeCommentsRequestDescribeCommentsPaginateTypeDef]
    ) -> AsyncIterator[DescribeCommentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeComments.html#WorkDocs.Paginator.DescribeComments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describecommentspaginator)
        """

class DescribeDocumentVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeDocumentVersions.html#WorkDocs.Paginator.DescribeDocumentVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describedocumentversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[DescribeDocumentVersionsRequestDescribeDocumentVersionsPaginateTypeDef],
    ) -> AsyncIterator[DescribeDocumentVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeDocumentVersions.html#WorkDocs.Paginator.DescribeDocumentVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describedocumentversionspaginator)
        """

class DescribeFolderContentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeFolderContents.html#WorkDocs.Paginator.DescribeFolderContents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describefoldercontentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeFolderContentsRequestDescribeFolderContentsPaginateTypeDef]
    ) -> AsyncIterator[DescribeFolderContentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeFolderContents.html#WorkDocs.Paginator.DescribeFolderContents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describefoldercontentspaginator)
        """

class DescribeGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeGroups.html#WorkDocs.Paginator.DescribeGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describegroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeGroupsRequestDescribeGroupsPaginateTypeDef]
    ) -> AsyncIterator[DescribeGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeGroups.html#WorkDocs.Paginator.DescribeGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describegroupspaginator)
        """

class DescribeNotificationSubscriptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeNotificationSubscriptions.html#WorkDocs.Paginator.DescribeNotificationSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describenotificationsubscriptionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeNotificationSubscriptionsRequestDescribeNotificationSubscriptionsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeNotificationSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeNotificationSubscriptions.html#WorkDocs.Paginator.DescribeNotificationSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describenotificationsubscriptionspaginator)
        """

class DescribeResourcePermissionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeResourcePermissions.html#WorkDocs.Paginator.DescribeResourcePermissions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeresourcepermissionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            DescribeResourcePermissionsRequestDescribeResourcePermissionsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeResourcePermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeResourcePermissions.html#WorkDocs.Paginator.DescribeResourcePermissions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeresourcepermissionspaginator)
        """

class DescribeRootFoldersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeRootFolders.html#WorkDocs.Paginator.DescribeRootFolders)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describerootfolderspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeRootFoldersRequestDescribeRootFoldersPaginateTypeDef]
    ) -> AsyncIterator[DescribeRootFoldersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeRootFolders.html#WorkDocs.Paginator.DescribeRootFolders.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describerootfolderspaginator)
        """

class DescribeUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeUsers.html#WorkDocs.Paginator.DescribeUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeuserspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeUsersRequestDescribeUsersPaginateTypeDef]
    ) -> AsyncIterator[DescribeUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeUsers.html#WorkDocs.Paginator.DescribeUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeuserspaginator)
        """

class SearchResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/SearchResources.html#WorkDocs.Paginator.SearchResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#searchresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchResourcesRequestSearchResourcesPaginateTypeDef]
    ) -> AsyncIterator[SearchResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/SearchResources.html#WorkDocs.Paginator.SearchResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#searchresourcespaginator)
        """
