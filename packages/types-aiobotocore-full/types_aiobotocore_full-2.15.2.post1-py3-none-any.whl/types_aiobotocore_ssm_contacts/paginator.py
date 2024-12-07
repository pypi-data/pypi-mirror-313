"""
Type annotations for ssm-contacts service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ssm_contacts.client import SSMContactsClient
    from types_aiobotocore_ssm_contacts.paginator import (
        ListContactChannelsPaginator,
        ListContactsPaginator,
        ListEngagementsPaginator,
        ListPageReceiptsPaginator,
        ListPageResolutionsPaginator,
        ListPagesByContactPaginator,
        ListPagesByEngagementPaginator,
        ListPreviewRotationShiftsPaginator,
        ListRotationOverridesPaginator,
        ListRotationShiftsPaginator,
        ListRotationsPaginator,
    )

    session = get_session()
    with session.create_client("ssm-contacts") as client:
        client: SSMContactsClient

        list_contact_channels_paginator: ListContactChannelsPaginator = client.get_paginator("list_contact_channels")
        list_contacts_paginator: ListContactsPaginator = client.get_paginator("list_contacts")
        list_engagements_paginator: ListEngagementsPaginator = client.get_paginator("list_engagements")
        list_page_receipts_paginator: ListPageReceiptsPaginator = client.get_paginator("list_page_receipts")
        list_page_resolutions_paginator: ListPageResolutionsPaginator = client.get_paginator("list_page_resolutions")
        list_pages_by_contact_paginator: ListPagesByContactPaginator = client.get_paginator("list_pages_by_contact")
        list_pages_by_engagement_paginator: ListPagesByEngagementPaginator = client.get_paginator("list_pages_by_engagement")
        list_preview_rotation_shifts_paginator: ListPreviewRotationShiftsPaginator = client.get_paginator("list_preview_rotation_shifts")
        list_rotation_overrides_paginator: ListRotationOverridesPaginator = client.get_paginator("list_rotation_overrides")
        list_rotation_shifts_paginator: ListRotationShiftsPaginator = client.get_paginator("list_rotation_shifts")
        list_rotations_paginator: ListRotationsPaginator = client.get_paginator("list_rotations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListContactChannelsRequestListContactChannelsPaginateTypeDef,
    ListContactChannelsResultTypeDef,
    ListContactsRequestListContactsPaginateTypeDef,
    ListContactsResultTypeDef,
    ListEngagementsRequestListEngagementsPaginateTypeDef,
    ListEngagementsResultTypeDef,
    ListPageReceiptsRequestListPageReceiptsPaginateTypeDef,
    ListPageReceiptsResultTypeDef,
    ListPageResolutionsRequestListPageResolutionsPaginateTypeDef,
    ListPageResolutionsResultTypeDef,
    ListPagesByContactRequestListPagesByContactPaginateTypeDef,
    ListPagesByContactResultTypeDef,
    ListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef,
    ListPagesByEngagementResultTypeDef,
    ListPreviewRotationShiftsRequestListPreviewRotationShiftsPaginateTypeDef,
    ListPreviewRotationShiftsResultTypeDef,
    ListRotationOverridesRequestListRotationOverridesPaginateTypeDef,
    ListRotationOverridesResultTypeDef,
    ListRotationShiftsRequestListRotationShiftsPaginateTypeDef,
    ListRotationShiftsResultTypeDef,
    ListRotationsRequestListRotationsPaginateTypeDef,
    ListRotationsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListContactChannelsPaginator",
    "ListContactsPaginator",
    "ListEngagementsPaginator",
    "ListPageReceiptsPaginator",
    "ListPageResolutionsPaginator",
    "ListPagesByContactPaginator",
    "ListPagesByEngagementPaginator",
    "ListPreviewRotationShiftsPaginator",
    "ListRotationOverridesPaginator",
    "ListRotationShiftsPaginator",
    "ListRotationsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListContactChannelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListContactChannels.html#SSMContacts.Paginator.ListContactChannels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listcontactchannelspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListContactChannelsRequestListContactChannelsPaginateTypeDef]
    ) -> AsyncIterator[ListContactChannelsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListContactChannels.html#SSMContacts.Paginator.ListContactChannels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listcontactchannelspaginator)
        """


class ListContactsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListContacts.html#SSMContacts.Paginator.ListContacts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listcontactspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListContactsRequestListContactsPaginateTypeDef]
    ) -> AsyncIterator[ListContactsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListContacts.html#SSMContacts.Paginator.ListContacts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listcontactspaginator)
        """


class ListEngagementsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListEngagements.html#SSMContacts.Paginator.ListEngagements)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listengagementspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEngagementsRequestListEngagementsPaginateTypeDef]
    ) -> AsyncIterator[ListEngagementsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListEngagements.html#SSMContacts.Paginator.ListEngagements.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listengagementspaginator)
        """


class ListPageReceiptsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListPageReceipts.html#SSMContacts.Paginator.ListPageReceipts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listpagereceiptspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPageReceiptsRequestListPageReceiptsPaginateTypeDef]
    ) -> AsyncIterator[ListPageReceiptsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListPageReceipts.html#SSMContacts.Paginator.ListPageReceipts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listpagereceiptspaginator)
        """


class ListPageResolutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListPageResolutions.html#SSMContacts.Paginator.ListPageResolutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listpageresolutionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPageResolutionsRequestListPageResolutionsPaginateTypeDef]
    ) -> AsyncIterator[ListPageResolutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListPageResolutions.html#SSMContacts.Paginator.ListPageResolutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listpageresolutionspaginator)
        """


class ListPagesByContactPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListPagesByContact.html#SSMContacts.Paginator.ListPagesByContact)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listpagesbycontactpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPagesByContactRequestListPagesByContactPaginateTypeDef]
    ) -> AsyncIterator[ListPagesByContactResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListPagesByContact.html#SSMContacts.Paginator.ListPagesByContact.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listpagesbycontactpaginator)
        """


class ListPagesByEngagementPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListPagesByEngagement.html#SSMContacts.Paginator.ListPagesByEngagement)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listpagesbyengagementpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef]
    ) -> AsyncIterator[ListPagesByEngagementResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListPagesByEngagement.html#SSMContacts.Paginator.ListPagesByEngagement.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listpagesbyengagementpaginator)
        """


class ListPreviewRotationShiftsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListPreviewRotationShifts.html#SSMContacts.Paginator.ListPreviewRotationShifts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listpreviewrotationshiftspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListPreviewRotationShiftsRequestListPreviewRotationShiftsPaginateTypeDef],
    ) -> AsyncIterator[ListPreviewRotationShiftsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListPreviewRotationShifts.html#SSMContacts.Paginator.ListPreviewRotationShifts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listpreviewrotationshiftspaginator)
        """


class ListRotationOverridesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListRotationOverrides.html#SSMContacts.Paginator.ListRotationOverrides)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listrotationoverridespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRotationOverridesRequestListRotationOverridesPaginateTypeDef]
    ) -> AsyncIterator[ListRotationOverridesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListRotationOverrides.html#SSMContacts.Paginator.ListRotationOverrides.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listrotationoverridespaginator)
        """


class ListRotationShiftsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListRotationShifts.html#SSMContacts.Paginator.ListRotationShifts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listrotationshiftspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRotationShiftsRequestListRotationShiftsPaginateTypeDef]
    ) -> AsyncIterator[ListRotationShiftsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListRotationShifts.html#SSMContacts.Paginator.ListRotationShifts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listrotationshiftspaginator)
        """


class ListRotationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListRotations.html#SSMContacts.Paginator.ListRotations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listrotationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRotationsRequestListRotationsPaginateTypeDef]
    ) -> AsyncIterator[ListRotationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts/paginator/ListRotations.html#SSMContacts.Paginator.ListRotations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listrotationspaginator)
        """
