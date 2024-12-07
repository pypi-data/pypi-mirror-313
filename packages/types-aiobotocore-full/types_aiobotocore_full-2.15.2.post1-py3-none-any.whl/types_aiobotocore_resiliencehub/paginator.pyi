"""
Type annotations for resiliencehub service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_resiliencehub.client import ResilienceHubClient
    from types_aiobotocore_resiliencehub.paginator import (
        ListAppAssessmentResourceDriftsPaginator,
        ListResourceGroupingRecommendationsPaginator,
    )

    session = get_session()
    with session.create_client("resiliencehub") as client:
        client: ResilienceHubClient

        list_app_assessment_resource_drifts_paginator: ListAppAssessmentResourceDriftsPaginator = client.get_paginator("list_app_assessment_resource_drifts")
        list_resource_grouping_recommendations_paginator: ListResourceGroupingRecommendationsPaginator = client.get_paginator("list_resource_grouping_recommendations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAppAssessmentResourceDriftsRequestListAppAssessmentResourceDriftsPaginateTypeDef,
    ListAppAssessmentResourceDriftsResponseTypeDef,
    ListResourceGroupingRecommendationsRequestListResourceGroupingRecommendationsPaginateTypeDef,
    ListResourceGroupingRecommendationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAppAssessmentResourceDriftsPaginator",
    "ListResourceGroupingRecommendationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAppAssessmentResourceDriftsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/paginator/ListAppAssessmentResourceDrifts.html#ResilienceHub.Paginator.ListAppAssessmentResourceDrifts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/paginators/#listappassessmentresourcedriftspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAppAssessmentResourceDriftsRequestListAppAssessmentResourceDriftsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAppAssessmentResourceDriftsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/paginator/ListAppAssessmentResourceDrifts.html#ResilienceHub.Paginator.ListAppAssessmentResourceDrifts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/paginators/#listappassessmentresourcedriftspaginator)
        """

class ListResourceGroupingRecommendationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/paginator/ListResourceGroupingRecommendations.html#ResilienceHub.Paginator.ListResourceGroupingRecommendations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/paginators/#listresourcegroupingrecommendationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListResourceGroupingRecommendationsRequestListResourceGroupingRecommendationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListResourceGroupingRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/paginator/ListResourceGroupingRecommendations.html#ResilienceHub.Paginator.ListResourceGroupingRecommendations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/paginators/#listresourcegroupingrecommendationspaginator)
        """
