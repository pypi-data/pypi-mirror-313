"""
Type annotations for kinesis-video-archived-media service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_kinesis_video_archived_media.client import KinesisVideoArchivedMediaClient
    from types_aiobotocore_kinesis_video_archived_media.paginator import (
        GetImagesPaginator,
        ListFragmentsPaginator,
    )

    session = get_session()
    with session.create_client("kinesis-video-archived-media") as client:
        client: KinesisVideoArchivedMediaClient

        get_images_paginator: GetImagesPaginator = client.get_paginator("get_images")
        list_fragments_paginator: ListFragmentsPaginator = client.get_paginator("list_fragments")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetImagesInputGetImagesPaginateTypeDef,
    GetImagesOutputTypeDef,
    ListFragmentsInputListFragmentsPaginateTypeDef,
    ListFragmentsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("GetImagesPaginator", "ListFragmentsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetImagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/paginator/GetImages.html#KinesisVideoArchivedMedia.Paginator.GetImages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/paginators/#getimagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetImagesInputGetImagesPaginateTypeDef]
    ) -> AsyncIterator[GetImagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/paginator/GetImages.html#KinesisVideoArchivedMedia.Paginator.GetImages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/paginators/#getimagespaginator)
        """

class ListFragmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/paginator/ListFragments.html#KinesisVideoArchivedMedia.Paginator.ListFragments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/paginators/#listfragmentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFragmentsInputListFragmentsPaginateTypeDef]
    ) -> AsyncIterator[ListFragmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media/paginator/ListFragments.html#KinesisVideoArchivedMedia.Paginator.ListFragments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/paginators/#listfragmentspaginator)
        """
