"""
Type annotations for evidently service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_evidently.client import CloudWatchEvidentlyClient
    from types_aiobotocore_evidently.paginator import (
        ListExperimentsPaginator,
        ListFeaturesPaginator,
        ListLaunchesPaginator,
        ListProjectsPaginator,
        ListSegmentReferencesPaginator,
        ListSegmentsPaginator,
    )

    session = get_session()
    with session.create_client("evidently") as client:
        client: CloudWatchEvidentlyClient

        list_experiments_paginator: ListExperimentsPaginator = client.get_paginator("list_experiments")
        list_features_paginator: ListFeaturesPaginator = client.get_paginator("list_features")
        list_launches_paginator: ListLaunchesPaginator = client.get_paginator("list_launches")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
        list_segment_references_paginator: ListSegmentReferencesPaginator = client.get_paginator("list_segment_references")
        list_segments_paginator: ListSegmentsPaginator = client.get_paginator("list_segments")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListExperimentsRequestListExperimentsPaginateTypeDef,
    ListExperimentsResponseTypeDef,
    ListFeaturesRequestListFeaturesPaginateTypeDef,
    ListFeaturesResponseTypeDef,
    ListLaunchesRequestListLaunchesPaginateTypeDef,
    ListLaunchesResponseTypeDef,
    ListProjectsRequestListProjectsPaginateTypeDef,
    ListProjectsResponseTypeDef,
    ListSegmentReferencesRequestListSegmentReferencesPaginateTypeDef,
    ListSegmentReferencesResponseTypeDef,
    ListSegmentsRequestListSegmentsPaginateTypeDef,
    ListSegmentsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListExperimentsPaginator",
    "ListFeaturesPaginator",
    "ListLaunchesPaginator",
    "ListProjectsPaginator",
    "ListSegmentReferencesPaginator",
    "ListSegmentsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListExperimentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListExperiments.html#CloudWatchEvidently.Paginator.ListExperiments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listexperimentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListExperimentsRequestListExperimentsPaginateTypeDef]
    ) -> AsyncIterator[ListExperimentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListExperiments.html#CloudWatchEvidently.Paginator.ListExperiments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listexperimentspaginator)
        """


class ListFeaturesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListFeatures.html#CloudWatchEvidently.Paginator.ListFeatures)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listfeaturespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFeaturesRequestListFeaturesPaginateTypeDef]
    ) -> AsyncIterator[ListFeaturesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListFeatures.html#CloudWatchEvidently.Paginator.ListFeatures.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listfeaturespaginator)
        """


class ListLaunchesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListLaunches.html#CloudWatchEvidently.Paginator.ListLaunches)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listlaunchespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListLaunchesRequestListLaunchesPaginateTypeDef]
    ) -> AsyncIterator[ListLaunchesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListLaunches.html#CloudWatchEvidently.Paginator.ListLaunches.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listlaunchespaginator)
        """


class ListProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListProjects.html#CloudWatchEvidently.Paginator.ListProjects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listprojectspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListProjectsRequestListProjectsPaginateTypeDef]
    ) -> AsyncIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListProjects.html#CloudWatchEvidently.Paginator.ListProjects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listprojectspaginator)
        """


class ListSegmentReferencesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListSegmentReferences.html#CloudWatchEvidently.Paginator.ListSegmentReferences)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listsegmentreferencespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSegmentReferencesRequestListSegmentReferencesPaginateTypeDef]
    ) -> AsyncIterator[ListSegmentReferencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListSegmentReferences.html#CloudWatchEvidently.Paginator.ListSegmentReferences.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listsegmentreferencespaginator)
        """


class ListSegmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListSegments.html#CloudWatchEvidently.Paginator.ListSegments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listsegmentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSegmentsRequestListSegmentsPaginateTypeDef]
    ) -> AsyncIterator[ListSegmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently/paginator/ListSegments.html#CloudWatchEvidently.Paginator.ListSegments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evidently/paginators/#listsegmentspaginator)
        """
