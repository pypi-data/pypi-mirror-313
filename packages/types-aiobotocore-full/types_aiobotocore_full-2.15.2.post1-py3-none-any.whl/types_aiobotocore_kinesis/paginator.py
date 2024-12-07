"""
Type annotations for kinesis service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_kinesis.client import KinesisClient
    from types_aiobotocore_kinesis.paginator import (
        DescribeStreamPaginator,
        ListShardsPaginator,
        ListStreamConsumersPaginator,
        ListStreamsPaginator,
    )

    session = get_session()
    with session.create_client("kinesis") as client:
        client: KinesisClient

        describe_stream_paginator: DescribeStreamPaginator = client.get_paginator("describe_stream")
        list_shards_paginator: ListShardsPaginator = client.get_paginator("list_shards")
        list_stream_consumers_paginator: ListStreamConsumersPaginator = client.get_paginator("list_stream_consumers")
        list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeStreamInputDescribeStreamPaginateTypeDef,
    DescribeStreamOutputTypeDef,
    ListShardsInputListShardsPaginateTypeDef,
    ListShardsOutputTypeDef,
    ListStreamConsumersInputListStreamConsumersPaginateTypeDef,
    ListStreamConsumersOutputTypeDef,
    ListStreamsInputListStreamsPaginateTypeDef,
    ListStreamsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeStreamPaginator",
    "ListShardsPaginator",
    "ListStreamConsumersPaginator",
    "ListStreamsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeStreamPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/paginator/DescribeStream.html#Kinesis.Paginator.DescribeStream)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/#describestreampaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeStreamInputDescribeStreamPaginateTypeDef]
    ) -> AsyncIterator[DescribeStreamOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/paginator/DescribeStream.html#Kinesis.Paginator.DescribeStream.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/#describestreampaginator)
        """


class ListShardsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/paginator/ListShards.html#Kinesis.Paginator.ListShards)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/#listshardspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListShardsInputListShardsPaginateTypeDef]
    ) -> AsyncIterator[ListShardsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/paginator/ListShards.html#Kinesis.Paginator.ListShards.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/#listshardspaginator)
        """


class ListStreamConsumersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/paginator/ListStreamConsumers.html#Kinesis.Paginator.ListStreamConsumers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/#liststreamconsumerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStreamConsumersInputListStreamConsumersPaginateTypeDef]
    ) -> AsyncIterator[ListStreamConsumersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/paginator/ListStreamConsumers.html#Kinesis.Paginator.ListStreamConsumers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/#liststreamconsumerspaginator)
        """


class ListStreamsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/paginator/ListStreams.html#Kinesis.Paginator.ListStreams)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/#liststreamspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStreamsInputListStreamsPaginateTypeDef]
    ) -> AsyncIterator[ListStreamsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/paginator/ListStreams.html#Kinesis.Paginator.ListStreams.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/paginators/#liststreamspaginator)
        """
