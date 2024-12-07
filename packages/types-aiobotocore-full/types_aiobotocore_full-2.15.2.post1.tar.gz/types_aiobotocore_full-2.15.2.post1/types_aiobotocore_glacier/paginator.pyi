"""
Type annotations for glacier service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_glacier.client import GlacierClient
    from types_aiobotocore_glacier.paginator import (
        ListJobsPaginator,
        ListMultipartUploadsPaginator,
        ListPartsPaginator,
        ListVaultsPaginator,
    )

    session = get_session()
    with session.create_client("glacier") as client:
        client: GlacierClient

        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_multipart_uploads_paginator: ListMultipartUploadsPaginator = client.get_paginator("list_multipart_uploads")
        list_parts_paginator: ListPartsPaginator = client.get_paginator("list_parts")
        list_vaults_paginator: ListVaultsPaginator = client.get_paginator("list_vaults")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListJobsInputListJobsPaginateTypeDef,
    ListJobsOutputTypeDef,
    ListMultipartUploadsInputListMultipartUploadsPaginateTypeDef,
    ListMultipartUploadsOutputTypeDef,
    ListPartsInputListPartsPaginateTypeDef,
    ListPartsOutputTypeDef,
    ListVaultsInputListVaultsPaginateTypeDef,
    ListVaultsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListJobsPaginator",
    "ListMultipartUploadsPaginator",
    "ListPartsPaginator",
    "ListVaultsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListJobs.html#Glacier.Paginator.ListJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/#listjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsInputListJobsPaginateTypeDef]
    ) -> AsyncIterator[ListJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListJobs.html#Glacier.Paginator.ListJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/#listjobspaginator)
        """

class ListMultipartUploadsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListMultipartUploads.html#Glacier.Paginator.ListMultipartUploads)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/#listmultipartuploadspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMultipartUploadsInputListMultipartUploadsPaginateTypeDef]
    ) -> AsyncIterator[ListMultipartUploadsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListMultipartUploads.html#Glacier.Paginator.ListMultipartUploads.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/#listmultipartuploadspaginator)
        """

class ListPartsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListParts.html#Glacier.Paginator.ListParts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/#listpartspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPartsInputListPartsPaginateTypeDef]
    ) -> AsyncIterator[ListPartsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListParts.html#Glacier.Paginator.ListParts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/#listpartspaginator)
        """

class ListVaultsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListVaults.html#Glacier.Paginator.ListVaults)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/#listvaultspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListVaultsInputListVaultsPaginateTypeDef]
    ) -> AsyncIterator[ListVaultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListVaults.html#Glacier.Paginator.ListVaults.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/#listvaultspaginator)
        """
