"""
Type annotations for databrew service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_databrew.client import GlueDataBrewClient
    from types_aiobotocore_databrew.paginator import (
        ListDatasetsPaginator,
        ListJobRunsPaginator,
        ListJobsPaginator,
        ListProjectsPaginator,
        ListRecipeVersionsPaginator,
        ListRecipesPaginator,
        ListRulesetsPaginator,
        ListSchedulesPaginator,
    )

    session = get_session()
    with session.create_client("databrew") as client:
        client: GlueDataBrewClient

        list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
        list_job_runs_paginator: ListJobRunsPaginator = client.get_paginator("list_job_runs")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
        list_recipe_versions_paginator: ListRecipeVersionsPaginator = client.get_paginator("list_recipe_versions")
        list_recipes_paginator: ListRecipesPaginator = client.get_paginator("list_recipes")
        list_rulesets_paginator: ListRulesetsPaginator = client.get_paginator("list_rulesets")
        list_schedules_paginator: ListSchedulesPaginator = client.get_paginator("list_schedules")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListDatasetsRequestListDatasetsPaginateTypeDef,
    ListDatasetsResponseTypeDef,
    ListJobRunsRequestListJobRunsPaginateTypeDef,
    ListJobRunsResponseTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListProjectsRequestListProjectsPaginateTypeDef,
    ListProjectsResponseTypeDef,
    ListRecipesRequestListRecipesPaginateTypeDef,
    ListRecipesResponseTypeDef,
    ListRecipeVersionsRequestListRecipeVersionsPaginateTypeDef,
    ListRecipeVersionsResponseTypeDef,
    ListRulesetsRequestListRulesetsPaginateTypeDef,
    ListRulesetsResponseTypeDef,
    ListSchedulesRequestListSchedulesPaginateTypeDef,
    ListSchedulesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDatasetsPaginator",
    "ListJobRunsPaginator",
    "ListJobsPaginator",
    "ListProjectsPaginator",
    "ListRecipeVersionsPaginator",
    "ListRecipesPaginator",
    "ListRulesetsPaginator",
    "ListSchedulesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDatasetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListDatasets.html#GlueDataBrew.Paginator.ListDatasets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listdatasetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDatasetsRequestListDatasetsPaginateTypeDef]
    ) -> AsyncIterator[ListDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListDatasets.html#GlueDataBrew.Paginator.ListDatasets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listdatasetspaginator)
        """

class ListJobRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListJobRuns.html#GlueDataBrew.Paginator.ListJobRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listjobrunspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobRunsRequestListJobRunsPaginateTypeDef]
    ) -> AsyncIterator[ListJobRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListJobRuns.html#GlueDataBrew.Paginator.ListJobRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listjobrunspaginator)
        """

class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListJobs.html#GlueDataBrew.Paginator.ListJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> AsyncIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListJobs.html#GlueDataBrew.Paginator.ListJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listjobspaginator)
        """

class ListProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListProjects.html#GlueDataBrew.Paginator.ListProjects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listprojectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProjectsRequestListProjectsPaginateTypeDef]
    ) -> AsyncIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListProjects.html#GlueDataBrew.Paginator.ListProjects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listprojectspaginator)
        """

class ListRecipeVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListRecipeVersions.html#GlueDataBrew.Paginator.ListRecipeVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listrecipeversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRecipeVersionsRequestListRecipeVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListRecipeVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListRecipeVersions.html#GlueDataBrew.Paginator.ListRecipeVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listrecipeversionspaginator)
        """

class ListRecipesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListRecipes.html#GlueDataBrew.Paginator.ListRecipes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listrecipespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRecipesRequestListRecipesPaginateTypeDef]
    ) -> AsyncIterator[ListRecipesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListRecipes.html#GlueDataBrew.Paginator.ListRecipes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listrecipespaginator)
        """

class ListRulesetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListRulesets.html#GlueDataBrew.Paginator.ListRulesets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listrulesetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRulesetsRequestListRulesetsPaginateTypeDef]
    ) -> AsyncIterator[ListRulesetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListRulesets.html#GlueDataBrew.Paginator.ListRulesets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listrulesetspaginator)
        """

class ListSchedulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListSchedules.html#GlueDataBrew.Paginator.ListSchedules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listschedulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSchedulesRequestListSchedulesPaginateTypeDef]
    ) -> AsyncIterator[ListSchedulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListSchedules.html#GlueDataBrew.Paginator.ListSchedules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listschedulespaginator)
        """
