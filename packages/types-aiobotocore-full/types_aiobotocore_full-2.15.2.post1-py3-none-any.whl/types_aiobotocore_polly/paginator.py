"""
Type annotations for polly service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_polly.client import PollyClient
    from types_aiobotocore_polly.paginator import (
        DescribeVoicesPaginator,
        ListLexiconsPaginator,
        ListSpeechSynthesisTasksPaginator,
    )

    session = get_session()
    with session.create_client("polly") as client:
        client: PollyClient

        describe_voices_paginator: DescribeVoicesPaginator = client.get_paginator("describe_voices")
        list_lexicons_paginator: ListLexiconsPaginator = client.get_paginator("list_lexicons")
        list_speech_synthesis_tasks_paginator: ListSpeechSynthesisTasksPaginator = client.get_paginator("list_speech_synthesis_tasks")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeVoicesInputDescribeVoicesPaginateTypeDef,
    DescribeVoicesOutputTypeDef,
    ListLexiconsInputListLexiconsPaginateTypeDef,
    ListLexiconsOutputTypeDef,
    ListSpeechSynthesisTasksInputListSpeechSynthesisTasksPaginateTypeDef,
    ListSpeechSynthesisTasksOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DescribeVoicesPaginator", "ListLexiconsPaginator", "ListSpeechSynthesisTasksPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeVoicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/DescribeVoices.html#Polly.Paginator.DescribeVoices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/paginators/#describevoicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeVoicesInputDescribeVoicesPaginateTypeDef]
    ) -> AsyncIterator[DescribeVoicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/DescribeVoices.html#Polly.Paginator.DescribeVoices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/paginators/#describevoicespaginator)
        """


class ListLexiconsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/ListLexicons.html#Polly.Paginator.ListLexicons)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/paginators/#listlexiconspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLexiconsInputListLexiconsPaginateTypeDef]
    ) -> AsyncIterator[ListLexiconsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/ListLexicons.html#Polly.Paginator.ListLexicons.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/paginators/#listlexiconspaginator)
        """


class ListSpeechSynthesisTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/ListSpeechSynthesisTasks.html#Polly.Paginator.ListSpeechSynthesisTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/paginators/#listspeechsynthesistaskspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSpeechSynthesisTasksInputListSpeechSynthesisTasksPaginateTypeDef]
    ) -> AsyncIterator[ListSpeechSynthesisTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/ListSpeechSynthesisTasks.html#Polly.Paginator.ListSpeechSynthesisTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/paginators/#listspeechsynthesistaskspaginator)
        """
