"""
Main interface for bedrock-agent-runtime service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_bedrock_agent_runtime import (
        AgentsforBedrockRuntimeClient,
        Client,
        GetAgentMemoryPaginator,
        RetrievePaginator,
    )

    session = get_session()
    async with session.create_client("bedrock-agent-runtime") as client:
        client: AgentsforBedrockRuntimeClient
        ...


    get_agent_memory_paginator: GetAgentMemoryPaginator = client.get_paginator("get_agent_memory")
    retrieve_paginator: RetrievePaginator = client.get_paginator("retrieve")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import AgentsforBedrockRuntimeClient
from .paginator import GetAgentMemoryPaginator, RetrievePaginator

Client = AgentsforBedrockRuntimeClient

__all__ = (
    "AgentsforBedrockRuntimeClient",
    "Client",
    "GetAgentMemoryPaginator",
    "RetrievePaginator",
)
