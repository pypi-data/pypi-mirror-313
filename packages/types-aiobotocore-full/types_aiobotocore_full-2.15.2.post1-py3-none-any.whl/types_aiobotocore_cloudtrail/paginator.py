"""
Type annotations for cloudtrail service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudtrail.client import CloudTrailClient
    from types_aiobotocore_cloudtrail.paginator import (
        ListImportFailuresPaginator,
        ListImportsPaginator,
        ListPublicKeysPaginator,
        ListTagsPaginator,
        ListTrailsPaginator,
        LookupEventsPaginator,
    )

    session = get_session()
    with session.create_client("cloudtrail") as client:
        client: CloudTrailClient

        list_import_failures_paginator: ListImportFailuresPaginator = client.get_paginator("list_import_failures")
        list_imports_paginator: ListImportsPaginator = client.get_paginator("list_imports")
        list_public_keys_paginator: ListPublicKeysPaginator = client.get_paginator("list_public_keys")
        list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
        list_trails_paginator: ListTrailsPaginator = client.get_paginator("list_trails")
        lookup_events_paginator: LookupEventsPaginator = client.get_paginator("lookup_events")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListImportFailuresRequestListImportFailuresPaginateTypeDef,
    ListImportFailuresResponseTypeDef,
    ListImportsRequestListImportsPaginateTypeDef,
    ListImportsResponseTypeDef,
    ListPublicKeysRequestListPublicKeysPaginateTypeDef,
    ListPublicKeysResponseTypeDef,
    ListTagsRequestListTagsPaginateTypeDef,
    ListTagsResponseTypeDef,
    ListTrailsRequestListTrailsPaginateTypeDef,
    ListTrailsResponseTypeDef,
    LookupEventsRequestLookupEventsPaginateTypeDef,
    LookupEventsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListImportFailuresPaginator",
    "ListImportsPaginator",
    "ListPublicKeysPaginator",
    "ListTagsPaginator",
    "ListTrailsPaginator",
    "LookupEventsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListImportFailuresPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListImportFailures.html#CloudTrail.Paginator.ListImportFailures)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listimportfailurespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListImportFailuresRequestListImportFailuresPaginateTypeDef]
    ) -> AsyncIterator[ListImportFailuresResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListImportFailures.html#CloudTrail.Paginator.ListImportFailures.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listimportfailurespaginator)
        """


class ListImportsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListImports.html#CloudTrail.Paginator.ListImports)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listimportspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListImportsRequestListImportsPaginateTypeDef]
    ) -> AsyncIterator[ListImportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListImports.html#CloudTrail.Paginator.ListImports.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listimportspaginator)
        """


class ListPublicKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListPublicKeys.html#CloudTrail.Paginator.ListPublicKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listpublickeyspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPublicKeysRequestListPublicKeysPaginateTypeDef]
    ) -> AsyncIterator[ListPublicKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListPublicKeys.html#CloudTrail.Paginator.ListPublicKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listpublickeyspaginator)
        """


class ListTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListTags.html#CloudTrail.Paginator.ListTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listtagspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTagsRequestListTagsPaginateTypeDef]
    ) -> AsyncIterator[ListTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListTags.html#CloudTrail.Paginator.ListTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listtagspaginator)
        """


class ListTrailsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListTrails.html#CloudTrail.Paginator.ListTrails)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listtrailspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTrailsRequestListTrailsPaginateTypeDef]
    ) -> AsyncIterator[ListTrailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/ListTrails.html#CloudTrail.Paginator.ListTrails.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#listtrailspaginator)
        """


class LookupEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/LookupEvents.html#CloudTrail.Paginator.LookupEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#lookupeventspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[LookupEventsRequestLookupEventsPaginateTypeDef]
    ) -> AsyncIterator[LookupEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/paginator/LookupEvents.html#CloudTrail.Paginator.LookupEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail/paginators/#lookupeventspaginator)
        """
