"""
Type annotations for bedrock-agent-runtime service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bedrock_agent_runtime.client import AgentsforBedrockRuntimeClient
    from types_aiobotocore_bedrock_agent_runtime.paginator import (
        GetAgentMemoryPaginator,
        RetrievePaginator,
    )

    session = get_session()
    with session.create_client("bedrock-agent-runtime") as client:
        client: AgentsforBedrockRuntimeClient

        get_agent_memory_paginator: GetAgentMemoryPaginator = client.get_paginator("get_agent_memory")
        retrieve_paginator: RetrievePaginator = client.get_paginator("retrieve")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetAgentMemoryRequestGetAgentMemoryPaginateTypeDef,
    GetAgentMemoryResponseTypeDef,
    RetrieveRequestRetrievePaginateTypeDef,
    RetrieveResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("GetAgentMemoryPaginator", "RetrievePaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetAgentMemoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/GetAgentMemory.html#AgentsforBedrockRuntime.Paginator.GetAgentMemory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#getagentmemorypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetAgentMemoryRequestGetAgentMemoryPaginateTypeDef]
    ) -> AsyncIterator[GetAgentMemoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/GetAgentMemory.html#AgentsforBedrockRuntime.Paginator.GetAgentMemory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#getagentmemorypaginator)
        """

class RetrievePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Retrieve.html#AgentsforBedrockRuntime.Paginator.Retrieve)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#retrievepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[RetrieveRequestRetrievePaginateTypeDef]
    ) -> AsyncIterator[RetrieveResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Retrieve.html#AgentsforBedrockRuntime.Paginator.Retrieve.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#retrievepaginator)
        """
