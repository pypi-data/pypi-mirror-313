"""
Type annotations for entityresolution service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_entityresolution.client import EntityResolutionClient
    from types_aiobotocore_entityresolution.paginator import (
        ListIdMappingJobsPaginator,
        ListIdMappingWorkflowsPaginator,
        ListIdNamespacesPaginator,
        ListMatchingJobsPaginator,
        ListMatchingWorkflowsPaginator,
        ListProviderServicesPaginator,
        ListSchemaMappingsPaginator,
    )

    session = get_session()
    with session.create_client("entityresolution") as client:
        client: EntityResolutionClient

        list_id_mapping_jobs_paginator: ListIdMappingJobsPaginator = client.get_paginator("list_id_mapping_jobs")
        list_id_mapping_workflows_paginator: ListIdMappingWorkflowsPaginator = client.get_paginator("list_id_mapping_workflows")
        list_id_namespaces_paginator: ListIdNamespacesPaginator = client.get_paginator("list_id_namespaces")
        list_matching_jobs_paginator: ListMatchingJobsPaginator = client.get_paginator("list_matching_jobs")
        list_matching_workflows_paginator: ListMatchingWorkflowsPaginator = client.get_paginator("list_matching_workflows")
        list_provider_services_paginator: ListProviderServicesPaginator = client.get_paginator("list_provider_services")
        list_schema_mappings_paginator: ListSchemaMappingsPaginator = client.get_paginator("list_schema_mappings")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListIdMappingJobsInputListIdMappingJobsPaginateTypeDef,
    ListIdMappingJobsOutputTypeDef,
    ListIdMappingWorkflowsInputListIdMappingWorkflowsPaginateTypeDef,
    ListIdMappingWorkflowsOutputTypeDef,
    ListIdNamespacesInputListIdNamespacesPaginateTypeDef,
    ListIdNamespacesOutputTypeDef,
    ListMatchingJobsInputListMatchingJobsPaginateTypeDef,
    ListMatchingJobsOutputTypeDef,
    ListMatchingWorkflowsInputListMatchingWorkflowsPaginateTypeDef,
    ListMatchingWorkflowsOutputTypeDef,
    ListProviderServicesInputListProviderServicesPaginateTypeDef,
    ListProviderServicesOutputTypeDef,
    ListSchemaMappingsInputListSchemaMappingsPaginateTypeDef,
    ListSchemaMappingsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListIdMappingJobsPaginator",
    "ListIdMappingWorkflowsPaginator",
    "ListIdNamespacesPaginator",
    "ListMatchingJobsPaginator",
    "ListMatchingWorkflowsPaginator",
    "ListProviderServicesPaginator",
    "ListSchemaMappingsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListIdMappingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdMappingJobs.html#EntityResolution.Paginator.ListIdMappingJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listidmappingjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIdMappingJobsInputListIdMappingJobsPaginateTypeDef]
    ) -> AsyncIterator[ListIdMappingJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdMappingJobs.html#EntityResolution.Paginator.ListIdMappingJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listidmappingjobspaginator)
        """

class ListIdMappingWorkflowsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdMappingWorkflows.html#EntityResolution.Paginator.ListIdMappingWorkflows)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listidmappingworkflowspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIdMappingWorkflowsInputListIdMappingWorkflowsPaginateTypeDef]
    ) -> AsyncIterator[ListIdMappingWorkflowsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdMappingWorkflows.html#EntityResolution.Paginator.ListIdMappingWorkflows.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listidmappingworkflowspaginator)
        """

class ListIdNamespacesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdNamespaces.html#EntityResolution.Paginator.ListIdNamespaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listidnamespacespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIdNamespacesInputListIdNamespacesPaginateTypeDef]
    ) -> AsyncIterator[ListIdNamespacesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdNamespaces.html#EntityResolution.Paginator.ListIdNamespaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listidnamespacespaginator)
        """

class ListMatchingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListMatchingJobs.html#EntityResolution.Paginator.ListMatchingJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listmatchingjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMatchingJobsInputListMatchingJobsPaginateTypeDef]
    ) -> AsyncIterator[ListMatchingJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListMatchingJobs.html#EntityResolution.Paginator.ListMatchingJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listmatchingjobspaginator)
        """

class ListMatchingWorkflowsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListMatchingWorkflows.html#EntityResolution.Paginator.ListMatchingWorkflows)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listmatchingworkflowspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMatchingWorkflowsInputListMatchingWorkflowsPaginateTypeDef]
    ) -> AsyncIterator[ListMatchingWorkflowsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListMatchingWorkflows.html#EntityResolution.Paginator.ListMatchingWorkflows.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listmatchingworkflowspaginator)
        """

class ListProviderServicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListProviderServices.html#EntityResolution.Paginator.ListProviderServices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listproviderservicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProviderServicesInputListProviderServicesPaginateTypeDef]
    ) -> AsyncIterator[ListProviderServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListProviderServices.html#EntityResolution.Paginator.ListProviderServices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listproviderservicespaginator)
        """

class ListSchemaMappingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListSchemaMappings.html#EntityResolution.Paginator.ListSchemaMappings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listschemamappingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSchemaMappingsInputListSchemaMappingsPaginateTypeDef]
    ) -> AsyncIterator[ListSchemaMappingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListSchemaMappings.html#EntityResolution.Paginator.ListSchemaMappings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listschemamappingspaginator)
        """
