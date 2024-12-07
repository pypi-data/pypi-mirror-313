"""
Type annotations for cloudformation service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudformation.client import CloudFormationClient
    from types_aiobotocore_cloudformation.paginator import (
        DescribeAccountLimitsPaginator,
        DescribeChangeSetPaginator,
        DescribeStackEventsPaginator,
        DescribeStacksPaginator,
        ListChangeSetsPaginator,
        ListExportsPaginator,
        ListGeneratedTemplatesPaginator,
        ListImportsPaginator,
        ListResourceScanRelatedResourcesPaginator,
        ListResourceScanResourcesPaginator,
        ListResourceScansPaginator,
        ListStackInstancesPaginator,
        ListStackResourcesPaginator,
        ListStackSetOperationResultsPaginator,
        ListStackSetOperationsPaginator,
        ListStackSetsPaginator,
        ListStacksPaginator,
        ListTypesPaginator,
    )

    session = get_session()
    with session.create_client("cloudformation") as client:
        client: CloudFormationClient

        describe_account_limits_paginator: DescribeAccountLimitsPaginator = client.get_paginator("describe_account_limits")
        describe_change_set_paginator: DescribeChangeSetPaginator = client.get_paginator("describe_change_set")
        describe_stack_events_paginator: DescribeStackEventsPaginator = client.get_paginator("describe_stack_events")
        describe_stacks_paginator: DescribeStacksPaginator = client.get_paginator("describe_stacks")
        list_change_sets_paginator: ListChangeSetsPaginator = client.get_paginator("list_change_sets")
        list_exports_paginator: ListExportsPaginator = client.get_paginator("list_exports")
        list_generated_templates_paginator: ListGeneratedTemplatesPaginator = client.get_paginator("list_generated_templates")
        list_imports_paginator: ListImportsPaginator = client.get_paginator("list_imports")
        list_resource_scan_related_resources_paginator: ListResourceScanRelatedResourcesPaginator = client.get_paginator("list_resource_scan_related_resources")
        list_resource_scan_resources_paginator: ListResourceScanResourcesPaginator = client.get_paginator("list_resource_scan_resources")
        list_resource_scans_paginator: ListResourceScansPaginator = client.get_paginator("list_resource_scans")
        list_stack_instances_paginator: ListStackInstancesPaginator = client.get_paginator("list_stack_instances")
        list_stack_resources_paginator: ListStackResourcesPaginator = client.get_paginator("list_stack_resources")
        list_stack_set_operation_results_paginator: ListStackSetOperationResultsPaginator = client.get_paginator("list_stack_set_operation_results")
        list_stack_set_operations_paginator: ListStackSetOperationsPaginator = client.get_paginator("list_stack_set_operations")
        list_stack_sets_paginator: ListStackSetsPaginator = client.get_paginator("list_stack_sets")
        list_stacks_paginator: ListStacksPaginator = client.get_paginator("list_stacks")
        list_types_paginator: ListTypesPaginator = client.get_paginator("list_types")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeAccountLimitsInputDescribeAccountLimitsPaginateTypeDef,
    DescribeAccountLimitsOutputTypeDef,
    DescribeChangeSetInputDescribeChangeSetPaginateTypeDef,
    DescribeChangeSetOutputTypeDef,
    DescribeStackEventsInputDescribeStackEventsPaginateTypeDef,
    DescribeStackEventsOutputTypeDef,
    DescribeStacksInputDescribeStacksPaginateTypeDef,
    DescribeStacksOutputTypeDef,
    ListChangeSetsInputListChangeSetsPaginateTypeDef,
    ListChangeSetsOutputTypeDef,
    ListExportsInputListExportsPaginateTypeDef,
    ListExportsOutputTypeDef,
    ListGeneratedTemplatesInputListGeneratedTemplatesPaginateTypeDef,
    ListGeneratedTemplatesOutputTypeDef,
    ListImportsInputListImportsPaginateTypeDef,
    ListImportsOutputTypeDef,
    ListResourceScanRelatedResourcesInputListResourceScanRelatedResourcesPaginateTypeDef,
    ListResourceScanRelatedResourcesOutputTypeDef,
    ListResourceScanResourcesInputListResourceScanResourcesPaginateTypeDef,
    ListResourceScanResourcesOutputTypeDef,
    ListResourceScansInputListResourceScansPaginateTypeDef,
    ListResourceScansOutputTypeDef,
    ListStackInstancesInputListStackInstancesPaginateTypeDef,
    ListStackInstancesOutputTypeDef,
    ListStackResourcesInputListStackResourcesPaginateTypeDef,
    ListStackResourcesOutputTypeDef,
    ListStackSetOperationResultsInputListStackSetOperationResultsPaginateTypeDef,
    ListStackSetOperationResultsOutputTypeDef,
    ListStackSetOperationsInputListStackSetOperationsPaginateTypeDef,
    ListStackSetOperationsOutputTypeDef,
    ListStackSetsInputListStackSetsPaginateTypeDef,
    ListStackSetsOutputTypeDef,
    ListStacksInputListStacksPaginateTypeDef,
    ListStacksOutputTypeDef,
    ListTypesInputListTypesPaginateTypeDef,
    ListTypesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeAccountLimitsPaginator",
    "DescribeChangeSetPaginator",
    "DescribeStackEventsPaginator",
    "DescribeStacksPaginator",
    "ListChangeSetsPaginator",
    "ListExportsPaginator",
    "ListGeneratedTemplatesPaginator",
    "ListImportsPaginator",
    "ListResourceScanRelatedResourcesPaginator",
    "ListResourceScanResourcesPaginator",
    "ListResourceScansPaginator",
    "ListStackInstancesPaginator",
    "ListStackResourcesPaginator",
    "ListStackSetOperationResultsPaginator",
    "ListStackSetOperationsPaginator",
    "ListStackSetsPaginator",
    "ListStacksPaginator",
    "ListTypesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeAccountLimitsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeAccountLimits.html#CloudFormation.Paginator.DescribeAccountLimits)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#describeaccountlimitspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeAccountLimitsInputDescribeAccountLimitsPaginateTypeDef]
    ) -> AsyncIterator[DescribeAccountLimitsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeAccountLimits.html#CloudFormation.Paginator.DescribeAccountLimits.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#describeaccountlimitspaginator)
        """


class DescribeChangeSetPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeChangeSet.html#CloudFormation.Paginator.DescribeChangeSet)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#describechangesetpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeChangeSetInputDescribeChangeSetPaginateTypeDef]
    ) -> AsyncIterator[DescribeChangeSetOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeChangeSet.html#CloudFormation.Paginator.DescribeChangeSet.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#describechangesetpaginator)
        """


class DescribeStackEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeStackEvents.html#CloudFormation.Paginator.DescribeStackEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#describestackeventspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeStackEventsInputDescribeStackEventsPaginateTypeDef]
    ) -> AsyncIterator[DescribeStackEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeStackEvents.html#CloudFormation.Paginator.DescribeStackEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#describestackeventspaginator)
        """


class DescribeStacksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeStacks.html#CloudFormation.Paginator.DescribeStacks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#describestackspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeStacksInputDescribeStacksPaginateTypeDef]
    ) -> AsyncIterator[DescribeStacksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeStacks.html#CloudFormation.Paginator.DescribeStacks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#describestackspaginator)
        """


class ListChangeSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListChangeSets.html#CloudFormation.Paginator.ListChangeSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listchangesetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListChangeSetsInputListChangeSetsPaginateTypeDef]
    ) -> AsyncIterator[ListChangeSetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListChangeSets.html#CloudFormation.Paginator.ListChangeSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listchangesetspaginator)
        """


class ListExportsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListExports.html#CloudFormation.Paginator.ListExports)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listexportspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListExportsInputListExportsPaginateTypeDef]
    ) -> AsyncIterator[ListExportsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListExports.html#CloudFormation.Paginator.ListExports.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listexportspaginator)
        """


class ListGeneratedTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListGeneratedTemplates.html#CloudFormation.Paginator.ListGeneratedTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listgeneratedtemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListGeneratedTemplatesInputListGeneratedTemplatesPaginateTypeDef]
    ) -> AsyncIterator[ListGeneratedTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListGeneratedTemplates.html#CloudFormation.Paginator.ListGeneratedTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listgeneratedtemplatespaginator)
        """


class ListImportsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListImports.html#CloudFormation.Paginator.ListImports)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listimportspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListImportsInputListImportsPaginateTypeDef]
    ) -> AsyncIterator[ListImportsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListImports.html#CloudFormation.Paginator.ListImports.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listimportspaginator)
        """


class ListResourceScanRelatedResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScanRelatedResources.html#CloudFormation.Paginator.ListResourceScanRelatedResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listresourcescanrelatedresourcespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResourceScanRelatedResourcesInputListResourceScanRelatedResourcesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListResourceScanRelatedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScanRelatedResources.html#CloudFormation.Paginator.ListResourceScanRelatedResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listresourcescanrelatedresourcespaginator)
        """


class ListResourceScanResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScanResources.html#CloudFormation.Paginator.ListResourceScanResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listresourcescanresourcespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListResourceScanResourcesInputListResourceScanResourcesPaginateTypeDef],
    ) -> AsyncIterator[ListResourceScanResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScanResources.html#CloudFormation.Paginator.ListResourceScanResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listresourcescanresourcespaginator)
        """


class ListResourceScansPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScans.html#CloudFormation.Paginator.ListResourceScans)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listresourcescanspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResourceScansInputListResourceScansPaginateTypeDef]
    ) -> AsyncIterator[ListResourceScansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScans.html#CloudFormation.Paginator.ListResourceScans.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listresourcescanspaginator)
        """


class ListStackInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackInstances.html#CloudFormation.Paginator.ListStackInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststackinstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStackInstancesInputListStackInstancesPaginateTypeDef]
    ) -> AsyncIterator[ListStackInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackInstances.html#CloudFormation.Paginator.ListStackInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststackinstancespaginator)
        """


class ListStackResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackResources.html#CloudFormation.Paginator.ListStackResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststackresourcespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStackResourcesInputListStackResourcesPaginateTypeDef]
    ) -> AsyncIterator[ListStackResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackResources.html#CloudFormation.Paginator.ListStackResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststackresourcespaginator)
        """


class ListStackSetOperationResultsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSetOperationResults.html#CloudFormation.Paginator.ListStackSetOperationResults)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststacksetoperationresultspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListStackSetOperationResultsInputListStackSetOperationResultsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListStackSetOperationResultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSetOperationResults.html#CloudFormation.Paginator.ListStackSetOperationResults.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststacksetoperationresultspaginator)
        """


class ListStackSetOperationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSetOperations.html#CloudFormation.Paginator.ListStackSetOperations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststacksetoperationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStackSetOperationsInputListStackSetOperationsPaginateTypeDef]
    ) -> AsyncIterator[ListStackSetOperationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSetOperations.html#CloudFormation.Paginator.ListStackSetOperations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststacksetoperationspaginator)
        """


class ListStackSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSets.html#CloudFormation.Paginator.ListStackSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststacksetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStackSetsInputListStackSetsPaginateTypeDef]
    ) -> AsyncIterator[ListStackSetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSets.html#CloudFormation.Paginator.ListStackSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststacksetspaginator)
        """


class ListStacksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStacks.html#CloudFormation.Paginator.ListStacks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststackspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStacksInputListStacksPaginateTypeDef]
    ) -> AsyncIterator[ListStacksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStacks.html#CloudFormation.Paginator.ListStacks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststackspaginator)
        """


class ListTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListTypes.html#CloudFormation.Paginator.ListTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listtypespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTypesInputListTypesPaginateTypeDef]
    ) -> AsyncIterator[ListTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListTypes.html#CloudFormation.Paginator.ListTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listtypespaginator)
        """
