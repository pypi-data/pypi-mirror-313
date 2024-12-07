"""
Type annotations for codedeploy service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codedeploy.client import CodeDeployClient
    from types_aiobotocore_codedeploy.paginator import (
        ListApplicationRevisionsPaginator,
        ListApplicationsPaginator,
        ListDeploymentConfigsPaginator,
        ListDeploymentGroupsPaginator,
        ListDeploymentInstancesPaginator,
        ListDeploymentTargetsPaginator,
        ListDeploymentsPaginator,
        ListGitHubAccountTokenNamesPaginator,
        ListOnPremisesInstancesPaginator,
    )

    session = get_session()
    with session.create_client("codedeploy") as client:
        client: CodeDeployClient

        list_application_revisions_paginator: ListApplicationRevisionsPaginator = client.get_paginator("list_application_revisions")
        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
        list_deployment_configs_paginator: ListDeploymentConfigsPaginator = client.get_paginator("list_deployment_configs")
        list_deployment_groups_paginator: ListDeploymentGroupsPaginator = client.get_paginator("list_deployment_groups")
        list_deployment_instances_paginator: ListDeploymentInstancesPaginator = client.get_paginator("list_deployment_instances")
        list_deployment_targets_paginator: ListDeploymentTargetsPaginator = client.get_paginator("list_deployment_targets")
        list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
        list_git_hub_account_token_names_paginator: ListGitHubAccountTokenNamesPaginator = client.get_paginator("list_git_hub_account_token_names")
        list_on_premises_instances_paginator: ListOnPremisesInstancesPaginator = client.get_paginator("list_on_premises_instances")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListApplicationRevisionsInputListApplicationRevisionsPaginateTypeDef,
    ListApplicationRevisionsOutputTypeDef,
    ListApplicationsInputListApplicationsPaginateTypeDef,
    ListApplicationsOutputTypeDef,
    ListDeploymentConfigsInputListDeploymentConfigsPaginateTypeDef,
    ListDeploymentConfigsOutputTypeDef,
    ListDeploymentGroupsInputListDeploymentGroupsPaginateTypeDef,
    ListDeploymentGroupsOutputTypeDef,
    ListDeploymentInstancesInputListDeploymentInstancesPaginateTypeDef,
    ListDeploymentInstancesOutputTypeDef,
    ListDeploymentsInputListDeploymentsPaginateTypeDef,
    ListDeploymentsOutputTypeDef,
    ListDeploymentTargetsInputListDeploymentTargetsPaginateTypeDef,
    ListDeploymentTargetsOutputTypeDef,
    ListGitHubAccountTokenNamesInputListGitHubAccountTokenNamesPaginateTypeDef,
    ListGitHubAccountTokenNamesOutputTypeDef,
    ListOnPremisesInstancesInputListOnPremisesInstancesPaginateTypeDef,
    ListOnPremisesInstancesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListApplicationRevisionsPaginator",
    "ListApplicationsPaginator",
    "ListDeploymentConfigsPaginator",
    "ListDeploymentGroupsPaginator",
    "ListDeploymentInstancesPaginator",
    "ListDeploymentTargetsPaginator",
    "ListDeploymentsPaginator",
    "ListGitHubAccountTokenNamesPaginator",
    "ListOnPremisesInstancesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListApplicationRevisionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListApplicationRevisions.html#CodeDeploy.Paginator.ListApplicationRevisions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listapplicationrevisionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListApplicationRevisionsInputListApplicationRevisionsPaginateTypeDef]
    ) -> AsyncIterator[ListApplicationRevisionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListApplicationRevisions.html#CodeDeploy.Paginator.ListApplicationRevisions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listapplicationrevisionspaginator)
        """


class ListApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListApplications.html#CodeDeploy.Paginator.ListApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listapplicationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListApplicationsInputListApplicationsPaginateTypeDef]
    ) -> AsyncIterator[ListApplicationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListApplications.html#CodeDeploy.Paginator.ListApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listapplicationspaginator)
        """


class ListDeploymentConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentConfigs.html#CodeDeploy.Paginator.ListDeploymentConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymentconfigspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeploymentConfigsInputListDeploymentConfigsPaginateTypeDef]
    ) -> AsyncIterator[ListDeploymentConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentConfigs.html#CodeDeploy.Paginator.ListDeploymentConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymentconfigspaginator)
        """


class ListDeploymentGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentGroups.html#CodeDeploy.Paginator.ListDeploymentGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymentgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeploymentGroupsInputListDeploymentGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListDeploymentGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentGroups.html#CodeDeploy.Paginator.ListDeploymentGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymentgroupspaginator)
        """


class ListDeploymentInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentInstances.html#CodeDeploy.Paginator.ListDeploymentInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymentinstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeploymentInstancesInputListDeploymentInstancesPaginateTypeDef]
    ) -> AsyncIterator[ListDeploymentInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentInstances.html#CodeDeploy.Paginator.ListDeploymentInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymentinstancespaginator)
        """


class ListDeploymentTargetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentTargets.html#CodeDeploy.Paginator.ListDeploymentTargets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymenttargetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeploymentTargetsInputListDeploymentTargetsPaginateTypeDef]
    ) -> AsyncIterator[ListDeploymentTargetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeploymentTargets.html#CodeDeploy.Paginator.ListDeploymentTargets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymenttargetspaginator)
        """


class ListDeploymentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeployments.html#CodeDeploy.Paginator.ListDeployments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeploymentsInputListDeploymentsPaginateTypeDef]
    ) -> AsyncIterator[ListDeploymentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListDeployments.html#CodeDeploy.Paginator.ListDeployments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listdeploymentspaginator)
        """


class ListGitHubAccountTokenNamesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListGitHubAccountTokenNames.html#CodeDeploy.Paginator.ListGitHubAccountTokenNames)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listgithubaccounttokennamespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListGitHubAccountTokenNamesInputListGitHubAccountTokenNamesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListGitHubAccountTokenNamesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListGitHubAccountTokenNames.html#CodeDeploy.Paginator.ListGitHubAccountTokenNames.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listgithubaccounttokennamespaginator)
        """


class ListOnPremisesInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListOnPremisesInstances.html#CodeDeploy.Paginator.ListOnPremisesInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listonpremisesinstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOnPremisesInstancesInputListOnPremisesInstancesPaginateTypeDef]
    ) -> AsyncIterator[ListOnPremisesInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/paginator/ListOnPremisesInstances.html#CodeDeploy.Paginator.ListOnPremisesInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/paginators/#listonpremisesinstancespaginator)
        """
