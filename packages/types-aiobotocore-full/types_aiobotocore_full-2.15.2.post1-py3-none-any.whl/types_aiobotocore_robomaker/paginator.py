"""
Type annotations for robomaker service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_robomaker.client import RoboMakerClient
    from types_aiobotocore_robomaker.paginator import (
        ListDeploymentJobsPaginator,
        ListFleetsPaginator,
        ListRobotApplicationsPaginator,
        ListRobotsPaginator,
        ListSimulationApplicationsPaginator,
        ListSimulationJobBatchesPaginator,
        ListSimulationJobsPaginator,
        ListWorldExportJobsPaginator,
        ListWorldGenerationJobsPaginator,
        ListWorldTemplatesPaginator,
        ListWorldsPaginator,
    )

    session = get_session()
    with session.create_client("robomaker") as client:
        client: RoboMakerClient

        list_deployment_jobs_paginator: ListDeploymentJobsPaginator = client.get_paginator("list_deployment_jobs")
        list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
        list_robot_applications_paginator: ListRobotApplicationsPaginator = client.get_paginator("list_robot_applications")
        list_robots_paginator: ListRobotsPaginator = client.get_paginator("list_robots")
        list_simulation_applications_paginator: ListSimulationApplicationsPaginator = client.get_paginator("list_simulation_applications")
        list_simulation_job_batches_paginator: ListSimulationJobBatchesPaginator = client.get_paginator("list_simulation_job_batches")
        list_simulation_jobs_paginator: ListSimulationJobsPaginator = client.get_paginator("list_simulation_jobs")
        list_world_export_jobs_paginator: ListWorldExportJobsPaginator = client.get_paginator("list_world_export_jobs")
        list_world_generation_jobs_paginator: ListWorldGenerationJobsPaginator = client.get_paginator("list_world_generation_jobs")
        list_world_templates_paginator: ListWorldTemplatesPaginator = client.get_paginator("list_world_templates")
        list_worlds_paginator: ListWorldsPaginator = client.get_paginator("list_worlds")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListDeploymentJobsRequestListDeploymentJobsPaginateTypeDef,
    ListDeploymentJobsResponseTypeDef,
    ListFleetsRequestListFleetsPaginateTypeDef,
    ListFleetsResponseTypeDef,
    ListRobotApplicationsRequestListRobotApplicationsPaginateTypeDef,
    ListRobotApplicationsResponseTypeDef,
    ListRobotsRequestListRobotsPaginateTypeDef,
    ListRobotsResponseTypeDef,
    ListSimulationApplicationsRequestListSimulationApplicationsPaginateTypeDef,
    ListSimulationApplicationsResponseTypeDef,
    ListSimulationJobBatchesRequestListSimulationJobBatchesPaginateTypeDef,
    ListSimulationJobBatchesResponseTypeDef,
    ListSimulationJobsRequestListSimulationJobsPaginateTypeDef,
    ListSimulationJobsResponseTypeDef,
    ListWorldExportJobsRequestListWorldExportJobsPaginateTypeDef,
    ListWorldExportJobsResponseTypeDef,
    ListWorldGenerationJobsRequestListWorldGenerationJobsPaginateTypeDef,
    ListWorldGenerationJobsResponseTypeDef,
    ListWorldsRequestListWorldsPaginateTypeDef,
    ListWorldsResponseTypeDef,
    ListWorldTemplatesRequestListWorldTemplatesPaginateTypeDef,
    ListWorldTemplatesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListDeploymentJobsPaginator",
    "ListFleetsPaginator",
    "ListRobotApplicationsPaginator",
    "ListRobotsPaginator",
    "ListSimulationApplicationsPaginator",
    "ListSimulationJobBatchesPaginator",
    "ListSimulationJobsPaginator",
    "ListWorldExportJobsPaginator",
    "ListWorldGenerationJobsPaginator",
    "ListWorldTemplatesPaginator",
    "ListWorldsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDeploymentJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListDeploymentJobs.html#RoboMaker.Paginator.ListDeploymentJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listdeploymentjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeploymentJobsRequestListDeploymentJobsPaginateTypeDef]
    ) -> AsyncIterator[ListDeploymentJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListDeploymentJobs.html#RoboMaker.Paginator.ListDeploymentJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listdeploymentjobspaginator)
        """


class ListFleetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListFleets.html#RoboMaker.Paginator.ListFleets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listfleetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListFleetsRequestListFleetsPaginateTypeDef]
    ) -> AsyncIterator[ListFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListFleets.html#RoboMaker.Paginator.ListFleets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listfleetspaginator)
        """


class ListRobotApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListRobotApplications.html#RoboMaker.Paginator.ListRobotApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listrobotapplicationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRobotApplicationsRequestListRobotApplicationsPaginateTypeDef]
    ) -> AsyncIterator[ListRobotApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListRobotApplications.html#RoboMaker.Paginator.ListRobotApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listrobotapplicationspaginator)
        """


class ListRobotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListRobots.html#RoboMaker.Paginator.ListRobots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listrobotspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRobotsRequestListRobotsPaginateTypeDef]
    ) -> AsyncIterator[ListRobotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListRobots.html#RoboMaker.Paginator.ListRobots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listrobotspaginator)
        """


class ListSimulationApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationApplications.html#RoboMaker.Paginator.ListSimulationApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listsimulationapplicationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListSimulationApplicationsRequestListSimulationApplicationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListSimulationApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationApplications.html#RoboMaker.Paginator.ListSimulationApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listsimulationapplicationspaginator)
        """


class ListSimulationJobBatchesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationJobBatches.html#RoboMaker.Paginator.ListSimulationJobBatches)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listsimulationjobbatchespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListSimulationJobBatchesRequestListSimulationJobBatchesPaginateTypeDef],
    ) -> AsyncIterator[ListSimulationJobBatchesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationJobBatches.html#RoboMaker.Paginator.ListSimulationJobBatches.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listsimulationjobbatchespaginator)
        """


class ListSimulationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationJobs.html#RoboMaker.Paginator.ListSimulationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listsimulationjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSimulationJobsRequestListSimulationJobsPaginateTypeDef]
    ) -> AsyncIterator[ListSimulationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationJobs.html#RoboMaker.Paginator.ListSimulationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listsimulationjobspaginator)
        """


class ListWorldExportJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldExportJobs.html#RoboMaker.Paginator.ListWorldExportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listworldexportjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorldExportJobsRequestListWorldExportJobsPaginateTypeDef]
    ) -> AsyncIterator[ListWorldExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldExportJobs.html#RoboMaker.Paginator.ListWorldExportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listworldexportjobspaginator)
        """


class ListWorldGenerationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldGenerationJobs.html#RoboMaker.Paginator.ListWorldGenerationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listworldgenerationjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorldGenerationJobsRequestListWorldGenerationJobsPaginateTypeDef]
    ) -> AsyncIterator[ListWorldGenerationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldGenerationJobs.html#RoboMaker.Paginator.ListWorldGenerationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listworldgenerationjobspaginator)
        """


class ListWorldTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldTemplates.html#RoboMaker.Paginator.ListWorldTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listworldtemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorldTemplatesRequestListWorldTemplatesPaginateTypeDef]
    ) -> AsyncIterator[ListWorldTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldTemplates.html#RoboMaker.Paginator.ListWorldTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listworldtemplatespaginator)
        """


class ListWorldsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorlds.html#RoboMaker.Paginator.ListWorlds)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listworldspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorldsRequestListWorldsPaginateTypeDef]
    ) -> AsyncIterator[ListWorldsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorlds.html#RoboMaker.Paginator.ListWorlds.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listworldspaginator)
        """
