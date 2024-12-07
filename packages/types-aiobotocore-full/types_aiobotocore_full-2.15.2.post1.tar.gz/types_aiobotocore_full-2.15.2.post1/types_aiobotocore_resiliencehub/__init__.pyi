"""
Main interface for resiliencehub service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_resiliencehub import (
        Client,
        ListAppAssessmentResourceDriftsPaginator,
        ListResourceGroupingRecommendationsPaginator,
        ResilienceHubClient,
    )

    session = get_session()
    async with session.create_client("resiliencehub") as client:
        client: ResilienceHubClient
        ...


    list_app_assessment_resource_drifts_paginator: ListAppAssessmentResourceDriftsPaginator = client.get_paginator("list_app_assessment_resource_drifts")
    list_resource_grouping_recommendations_paginator: ListResourceGroupingRecommendationsPaginator = client.get_paginator("list_resource_grouping_recommendations")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ResilienceHubClient
from .paginator import (
    ListAppAssessmentResourceDriftsPaginator,
    ListResourceGroupingRecommendationsPaginator,
)

Client = ResilienceHubClient

__all__ = (
    "Client",
    "ListAppAssessmentResourceDriftsPaginator",
    "ListResourceGroupingRecommendationsPaginator",
    "ResilienceHubClient",
)
