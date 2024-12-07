"""
Type annotations for sagemaker-a2i-runtime service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_a2i_runtime/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sagemaker_a2i_runtime.client import AugmentedAIRuntimeClient
    from types_aiobotocore_sagemaker_a2i_runtime.paginator import (
        ListHumanLoopsPaginator,
    )

    session = get_session()
    with session.create_client("sagemaker-a2i-runtime") as client:
        client: AugmentedAIRuntimeClient

        list_human_loops_paginator: ListHumanLoopsPaginator = client.get_paginator("list_human_loops")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListHumanLoopsRequestListHumanLoopsPaginateTypeDef,
    ListHumanLoopsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListHumanLoopsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListHumanLoopsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime/paginator/ListHumanLoops.html#AugmentedAIRuntime.Paginator.ListHumanLoops)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_a2i_runtime/paginators/#listhumanloopspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListHumanLoopsRequestListHumanLoopsPaginateTypeDef]
    ) -> AsyncIterator[ListHumanLoopsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime/paginator/ListHumanLoops.html#AugmentedAIRuntime.Paginator.ListHumanLoops.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_a2i_runtime/paginators/#listhumanloopspaginator)
        """
