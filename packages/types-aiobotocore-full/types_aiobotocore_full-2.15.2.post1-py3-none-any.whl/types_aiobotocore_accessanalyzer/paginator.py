"""
Type annotations for accessanalyzer service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_accessanalyzer.client import AccessAnalyzerClient
    from types_aiobotocore_accessanalyzer.paginator import (
        GetFindingRecommendationPaginator,
        GetFindingV2Paginator,
        ListAccessPreviewFindingsPaginator,
        ListAccessPreviewsPaginator,
        ListAnalyzedResourcesPaginator,
        ListAnalyzersPaginator,
        ListArchiveRulesPaginator,
        ListFindingsPaginator,
        ListFindingsV2Paginator,
        ListPolicyGenerationsPaginator,
        ValidatePolicyPaginator,
    )

    session = get_session()
    with session.create_client("accessanalyzer") as client:
        client: AccessAnalyzerClient

        get_finding_recommendation_paginator: GetFindingRecommendationPaginator = client.get_paginator("get_finding_recommendation")
        get_finding_v2_paginator: GetFindingV2Paginator = client.get_paginator("get_finding_v2")
        list_access_preview_findings_paginator: ListAccessPreviewFindingsPaginator = client.get_paginator("list_access_preview_findings")
        list_access_previews_paginator: ListAccessPreviewsPaginator = client.get_paginator("list_access_previews")
        list_analyzed_resources_paginator: ListAnalyzedResourcesPaginator = client.get_paginator("list_analyzed_resources")
        list_analyzers_paginator: ListAnalyzersPaginator = client.get_paginator("list_analyzers")
        list_archive_rules_paginator: ListArchiveRulesPaginator = client.get_paginator("list_archive_rules")
        list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
        list_findings_v2_paginator: ListFindingsV2Paginator = client.get_paginator("list_findings_v2")
        list_policy_generations_paginator: ListPolicyGenerationsPaginator = client.get_paginator("list_policy_generations")
        validate_policy_paginator: ValidatePolicyPaginator = client.get_paginator("validate_policy")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetFindingRecommendationRequestGetFindingRecommendationPaginateTypeDef,
    GetFindingRecommendationResponseTypeDef,
    GetFindingV2RequestGetFindingV2PaginateTypeDef,
    GetFindingV2ResponseTypeDef,
    ListAccessPreviewFindingsRequestListAccessPreviewFindingsPaginateTypeDef,
    ListAccessPreviewFindingsResponseTypeDef,
    ListAccessPreviewsRequestListAccessPreviewsPaginateTypeDef,
    ListAccessPreviewsResponseTypeDef,
    ListAnalyzedResourcesRequestListAnalyzedResourcesPaginateTypeDef,
    ListAnalyzedResourcesResponseTypeDef,
    ListAnalyzersRequestListAnalyzersPaginateTypeDef,
    ListAnalyzersResponseTypeDef,
    ListArchiveRulesRequestListArchiveRulesPaginateTypeDef,
    ListArchiveRulesResponseTypeDef,
    ListFindingsRequestListFindingsPaginateTypeDef,
    ListFindingsResponseTypeDef,
    ListFindingsV2RequestListFindingsV2PaginateTypeDef,
    ListFindingsV2ResponseTypeDef,
    ListPolicyGenerationsRequestListPolicyGenerationsPaginateTypeDef,
    ListPolicyGenerationsResponseTypeDef,
    ValidatePolicyRequestValidatePolicyPaginateTypeDef,
    ValidatePolicyResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetFindingRecommendationPaginator",
    "GetFindingV2Paginator",
    "ListAccessPreviewFindingsPaginator",
    "ListAccessPreviewsPaginator",
    "ListAnalyzedResourcesPaginator",
    "ListAnalyzersPaginator",
    "ListArchiveRulesPaginator",
    "ListFindingsPaginator",
    "ListFindingsV2Paginator",
    "ListPolicyGenerationsPaginator",
    "ValidatePolicyPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetFindingRecommendationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/GetFindingRecommendation.html#AccessAnalyzer.Paginator.GetFindingRecommendation)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#getfindingrecommendationpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[GetFindingRecommendationRequestGetFindingRecommendationPaginateTypeDef],
    ) -> AsyncIterator[GetFindingRecommendationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/GetFindingRecommendation.html#AccessAnalyzer.Paginator.GetFindingRecommendation.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#getfindingrecommendationpaginator)
        """


class GetFindingV2Paginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/GetFindingV2.html#AccessAnalyzer.Paginator.GetFindingV2)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#getfindingv2paginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetFindingV2RequestGetFindingV2PaginateTypeDef]
    ) -> AsyncIterator[GetFindingV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/GetFindingV2.html#AccessAnalyzer.Paginator.GetFindingV2.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#getfindingv2paginator)
        """


class ListAccessPreviewFindingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ListAccessPreviewFindings.html#AccessAnalyzer.Paginator.ListAccessPreviewFindings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listaccesspreviewfindingspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListAccessPreviewFindingsRequestListAccessPreviewFindingsPaginateTypeDef],
    ) -> AsyncIterator[ListAccessPreviewFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ListAccessPreviewFindings.html#AccessAnalyzer.Paginator.ListAccessPreviewFindings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listaccesspreviewfindingspaginator)
        """


class ListAccessPreviewsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ListAccessPreviews.html#AccessAnalyzer.Paginator.ListAccessPreviews)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listaccesspreviewspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAccessPreviewsRequestListAccessPreviewsPaginateTypeDef]
    ) -> AsyncIterator[ListAccessPreviewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ListAccessPreviews.html#AccessAnalyzer.Paginator.ListAccessPreviews.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listaccesspreviewspaginator)
        """


class ListAnalyzedResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ListAnalyzedResources.html#AccessAnalyzer.Paginator.ListAnalyzedResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listanalyzedresourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAnalyzedResourcesRequestListAnalyzedResourcesPaginateTypeDef]
    ) -> AsyncIterator[ListAnalyzedResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ListAnalyzedResources.html#AccessAnalyzer.Paginator.ListAnalyzedResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listanalyzedresourcespaginator)
        """


class ListAnalyzersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ListAnalyzers.html#AccessAnalyzer.Paginator.ListAnalyzers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listanalyzerspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAnalyzersRequestListAnalyzersPaginateTypeDef]
    ) -> AsyncIterator[ListAnalyzersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ListAnalyzers.html#AccessAnalyzer.Paginator.ListAnalyzers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listanalyzerspaginator)
        """


class ListArchiveRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ListArchiveRules.html#AccessAnalyzer.Paginator.ListArchiveRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listarchiverulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListArchiveRulesRequestListArchiveRulesPaginateTypeDef]
    ) -> AsyncIterator[ListArchiveRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ListArchiveRules.html#AccessAnalyzer.Paginator.ListArchiveRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listarchiverulespaginator)
        """


class ListFindingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ListFindings.html#AccessAnalyzer.Paginator.ListFindings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listfindingspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFindingsRequestListFindingsPaginateTypeDef]
    ) -> AsyncIterator[ListFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ListFindings.html#AccessAnalyzer.Paginator.ListFindings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listfindingspaginator)
        """


class ListFindingsV2Paginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ListFindingsV2.html#AccessAnalyzer.Paginator.ListFindingsV2)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listfindingsv2paginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFindingsV2RequestListFindingsV2PaginateTypeDef]
    ) -> AsyncIterator[ListFindingsV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ListFindingsV2.html#AccessAnalyzer.Paginator.ListFindingsV2.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listfindingsv2paginator)
        """


class ListPolicyGenerationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ListPolicyGenerations.html#AccessAnalyzer.Paginator.ListPolicyGenerations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listpolicygenerationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPolicyGenerationsRequestListPolicyGenerationsPaginateTypeDef]
    ) -> AsyncIterator[ListPolicyGenerationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ListPolicyGenerations.html#AccessAnalyzer.Paginator.ListPolicyGenerations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listpolicygenerationspaginator)
        """


class ValidatePolicyPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ValidatePolicy.html#AccessAnalyzer.Paginator.ValidatePolicy)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#validatepolicypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ValidatePolicyRequestValidatePolicyPaginateTypeDef]
    ) -> AsyncIterator[ValidatePolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/paginator/ValidatePolicy.html#AccessAnalyzer.Paginator.ValidatePolicy.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#validatepolicypaginator)
        """
