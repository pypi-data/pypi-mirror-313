"""
Main interface for bedrock-agent-runtime service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_bedrock_agent_runtime import (
        AgentsforBedrockRuntimeClient,
        Client,
        GetAgentMemoryPaginator,
        RerankPaginator,
        RetrievePaginator,
    )

    session = Session()
    client: AgentsforBedrockRuntimeClient = session.client("bedrock-agent-runtime")

    get_agent_memory_paginator: GetAgentMemoryPaginator = client.get_paginator("get_agent_memory")
    rerank_paginator: RerankPaginator = client.get_paginator("rerank")
    retrieve_paginator: RetrievePaginator = client.get_paginator("retrieve")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import AgentsforBedrockRuntimeClient
from .paginator import GetAgentMemoryPaginator, RerankPaginator, RetrievePaginator

Client = AgentsforBedrockRuntimeClient


__all__ = (
    "AgentsforBedrockRuntimeClient",
    "Client",
    "GetAgentMemoryPaginator",
    "RerankPaginator",
    "RetrievePaginator",
)
