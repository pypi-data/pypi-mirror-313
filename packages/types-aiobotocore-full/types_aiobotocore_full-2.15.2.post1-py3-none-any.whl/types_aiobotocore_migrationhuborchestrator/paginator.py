"""
Type annotations for migrationhuborchestrator service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_migrationhuborchestrator.client import MigrationHubOrchestratorClient
    from types_aiobotocore_migrationhuborchestrator.paginator import (
        ListPluginsPaginator,
        ListTemplateStepGroupsPaginator,
        ListTemplateStepsPaginator,
        ListTemplatesPaginator,
        ListWorkflowStepGroupsPaginator,
        ListWorkflowStepsPaginator,
        ListWorkflowsPaginator,
    )

    session = get_session()
    with session.create_client("migrationhuborchestrator") as client:
        client: MigrationHubOrchestratorClient

        list_plugins_paginator: ListPluginsPaginator = client.get_paginator("list_plugins")
        list_template_step_groups_paginator: ListTemplateStepGroupsPaginator = client.get_paginator("list_template_step_groups")
        list_template_steps_paginator: ListTemplateStepsPaginator = client.get_paginator("list_template_steps")
        list_templates_paginator: ListTemplatesPaginator = client.get_paginator("list_templates")
        list_workflow_step_groups_paginator: ListWorkflowStepGroupsPaginator = client.get_paginator("list_workflow_step_groups")
        list_workflow_steps_paginator: ListWorkflowStepsPaginator = client.get_paginator("list_workflow_steps")
        list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListMigrationWorkflowsRequestListWorkflowsPaginateTypeDef,
    ListMigrationWorkflowsResponseTypeDef,
    ListMigrationWorkflowTemplatesRequestListTemplatesPaginateTypeDef,
    ListMigrationWorkflowTemplatesResponseTypeDef,
    ListPluginsRequestListPluginsPaginateTypeDef,
    ListPluginsResponseTypeDef,
    ListTemplateStepGroupsRequestListTemplateStepGroupsPaginateTypeDef,
    ListTemplateStepGroupsResponseTypeDef,
    ListTemplateStepsRequestListTemplateStepsPaginateTypeDef,
    ListTemplateStepsResponseTypeDef,
    ListWorkflowStepGroupsRequestListWorkflowStepGroupsPaginateTypeDef,
    ListWorkflowStepGroupsResponseTypeDef,
    ListWorkflowStepsRequestListWorkflowStepsPaginateTypeDef,
    ListWorkflowStepsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListPluginsPaginator",
    "ListTemplateStepGroupsPaginator",
    "ListTemplateStepsPaginator",
    "ListTemplatesPaginator",
    "ListWorkflowStepGroupsPaginator",
    "ListWorkflowStepsPaginator",
    "ListWorkflowsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListPluginsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListPlugins.html#MigrationHubOrchestrator.Paginator.ListPlugins)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listpluginspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPluginsRequestListPluginsPaginateTypeDef]
    ) -> AsyncIterator[ListPluginsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListPlugins.html#MigrationHubOrchestrator.Paginator.ListPlugins.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listpluginspaginator)
        """


class ListTemplateStepGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplateStepGroups.html#MigrationHubOrchestrator.Paginator.ListTemplateStepGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listtemplatestepgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTemplateStepGroupsRequestListTemplateStepGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListTemplateStepGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplateStepGroups.html#MigrationHubOrchestrator.Paginator.ListTemplateStepGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listtemplatestepgroupspaginator)
        """


class ListTemplateStepsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplateSteps.html#MigrationHubOrchestrator.Paginator.ListTemplateSteps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listtemplatestepspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTemplateStepsRequestListTemplateStepsPaginateTypeDef]
    ) -> AsyncIterator[ListTemplateStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplateSteps.html#MigrationHubOrchestrator.Paginator.ListTemplateSteps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listtemplatestepspaginator)
        """


class ListTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplates.html#MigrationHubOrchestrator.Paginator.ListTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listtemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMigrationWorkflowTemplatesRequestListTemplatesPaginateTypeDef]
    ) -> AsyncIterator[ListMigrationWorkflowTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplates.html#MigrationHubOrchestrator.Paginator.ListTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listtemplatespaginator)
        """


class ListWorkflowStepGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflowStepGroups.html#MigrationHubOrchestrator.Paginator.ListWorkflowStepGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listworkflowstepgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorkflowStepGroupsRequestListWorkflowStepGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListWorkflowStepGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflowStepGroups.html#MigrationHubOrchestrator.Paginator.ListWorkflowStepGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listworkflowstepgroupspaginator)
        """


class ListWorkflowStepsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflowSteps.html#MigrationHubOrchestrator.Paginator.ListWorkflowSteps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listworkflowstepspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListWorkflowStepsRequestListWorkflowStepsPaginateTypeDef]
    ) -> AsyncIterator[ListWorkflowStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflowSteps.html#MigrationHubOrchestrator.Paginator.ListWorkflowSteps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listworkflowstepspaginator)
        """


class ListWorkflowsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflows.html#MigrationHubOrchestrator.Paginator.ListWorkflows)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listworkflowspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMigrationWorkflowsRequestListWorkflowsPaginateTypeDef]
    ) -> AsyncIterator[ListMigrationWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflows.html#MigrationHubOrchestrator.Paginator.ListWorkflows.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listworkflowspaginator)
        """
