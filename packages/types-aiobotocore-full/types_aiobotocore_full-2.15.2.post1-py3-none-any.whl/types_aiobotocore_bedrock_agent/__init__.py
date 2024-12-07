"""
Main interface for bedrock-agent service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_bedrock_agent import (
        AgentsforBedrockClient,
        Client,
        ListAgentActionGroupsPaginator,
        ListAgentAliasesPaginator,
        ListAgentKnowledgeBasesPaginator,
        ListAgentVersionsPaginator,
        ListAgentsPaginator,
        ListDataSourcesPaginator,
        ListFlowAliasesPaginator,
        ListFlowVersionsPaginator,
        ListFlowsPaginator,
        ListIngestionJobsPaginator,
        ListKnowledgeBasesPaginator,
        ListPromptsPaginator,
    )

    session = get_session()
    async with session.create_client("bedrock-agent") as client:
        client: AgentsforBedrockClient
        ...


    list_agent_action_groups_paginator: ListAgentActionGroupsPaginator = client.get_paginator("list_agent_action_groups")
    list_agent_aliases_paginator: ListAgentAliasesPaginator = client.get_paginator("list_agent_aliases")
    list_agent_knowledge_bases_paginator: ListAgentKnowledgeBasesPaginator = client.get_paginator("list_agent_knowledge_bases")
    list_agent_versions_paginator: ListAgentVersionsPaginator = client.get_paginator("list_agent_versions")
    list_agents_paginator: ListAgentsPaginator = client.get_paginator("list_agents")
    list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
    list_flow_aliases_paginator: ListFlowAliasesPaginator = client.get_paginator("list_flow_aliases")
    list_flow_versions_paginator: ListFlowVersionsPaginator = client.get_paginator("list_flow_versions")
    list_flows_paginator: ListFlowsPaginator = client.get_paginator("list_flows")
    list_ingestion_jobs_paginator: ListIngestionJobsPaginator = client.get_paginator("list_ingestion_jobs")
    list_knowledge_bases_paginator: ListKnowledgeBasesPaginator = client.get_paginator("list_knowledge_bases")
    list_prompts_paginator: ListPromptsPaginator = client.get_paginator("list_prompts")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import AgentsforBedrockClient
from .paginator import (
    ListAgentActionGroupsPaginator,
    ListAgentAliasesPaginator,
    ListAgentKnowledgeBasesPaginator,
    ListAgentsPaginator,
    ListAgentVersionsPaginator,
    ListDataSourcesPaginator,
    ListFlowAliasesPaginator,
    ListFlowsPaginator,
    ListFlowVersionsPaginator,
    ListIngestionJobsPaginator,
    ListKnowledgeBasesPaginator,
    ListPromptsPaginator,
)

Client = AgentsforBedrockClient


__all__ = (
    "AgentsforBedrockClient",
    "Client",
    "ListAgentActionGroupsPaginator",
    "ListAgentAliasesPaginator",
    "ListAgentKnowledgeBasesPaginator",
    "ListAgentVersionsPaginator",
    "ListAgentsPaginator",
    "ListDataSourcesPaginator",
    "ListFlowAliasesPaginator",
    "ListFlowVersionsPaginator",
    "ListFlowsPaginator",
    "ListIngestionJobsPaginator",
    "ListKnowledgeBasesPaginator",
    "ListPromptsPaginator",
)
