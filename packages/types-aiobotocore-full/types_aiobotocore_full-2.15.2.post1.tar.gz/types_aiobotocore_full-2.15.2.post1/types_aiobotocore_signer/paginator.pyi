"""
Type annotations for signer service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_signer.client import SignerClient
    from types_aiobotocore_signer.paginator import (
        ListSigningJobsPaginator,
        ListSigningPlatformsPaginator,
        ListSigningProfilesPaginator,
    )

    session = get_session()
    with session.create_client("signer") as client:
        client: SignerClient

        list_signing_jobs_paginator: ListSigningJobsPaginator = client.get_paginator("list_signing_jobs")
        list_signing_platforms_paginator: ListSigningPlatformsPaginator = client.get_paginator("list_signing_platforms")
        list_signing_profiles_paginator: ListSigningProfilesPaginator = client.get_paginator("list_signing_profiles")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListSigningJobsRequestListSigningJobsPaginateTypeDef,
    ListSigningJobsResponseTypeDef,
    ListSigningPlatformsRequestListSigningPlatformsPaginateTypeDef,
    ListSigningPlatformsResponseTypeDef,
    ListSigningProfilesRequestListSigningProfilesPaginateTypeDef,
    ListSigningProfilesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListSigningJobsPaginator",
    "ListSigningPlatformsPaginator",
    "ListSigningProfilesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListSigningJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningJobs.html#Signer.Paginator.ListSigningJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/paginators/#listsigningjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSigningJobsRequestListSigningJobsPaginateTypeDef]
    ) -> AsyncIterator[ListSigningJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningJobs.html#Signer.Paginator.ListSigningJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/paginators/#listsigningjobspaginator)
        """

class ListSigningPlatformsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningPlatforms.html#Signer.Paginator.ListSigningPlatforms)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/paginators/#listsigningplatformspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSigningPlatformsRequestListSigningPlatformsPaginateTypeDef]
    ) -> AsyncIterator[ListSigningPlatformsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningPlatforms.html#Signer.Paginator.ListSigningPlatforms.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/paginators/#listsigningplatformspaginator)
        """

class ListSigningProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningProfiles.html#Signer.Paginator.ListSigningProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/paginators/#listsigningprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSigningProfilesRequestListSigningProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListSigningProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningProfiles.html#Signer.Paginator.ListSigningProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/paginators/#listsigningprofilespaginator)
        """
