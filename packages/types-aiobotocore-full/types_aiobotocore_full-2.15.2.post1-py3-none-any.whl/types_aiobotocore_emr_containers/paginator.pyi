"""
Type annotations for emr-containers service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_emr_containers.client import EMRContainersClient
    from types_aiobotocore_emr_containers.paginator import (
        ListJobRunsPaginator,
        ListJobTemplatesPaginator,
        ListManagedEndpointsPaginator,
        ListSecurityConfigurationsPaginator,
        ListVirtualClustersPaginator,
    )

    session = get_session()
    with session.create_client("emr-containers") as client:
        client: EMRContainersClient

        list_job_runs_paginator: ListJobRunsPaginator = client.get_paginator("list_job_runs")
        list_job_templates_paginator: ListJobTemplatesPaginator = client.get_paginator("list_job_templates")
        list_managed_endpoints_paginator: ListManagedEndpointsPaginator = client.get_paginator("list_managed_endpoints")
        list_security_configurations_paginator: ListSecurityConfigurationsPaginator = client.get_paginator("list_security_configurations")
        list_virtual_clusters_paginator: ListVirtualClustersPaginator = client.get_paginator("list_virtual_clusters")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListJobRunsRequestListJobRunsPaginateTypeDef,
    ListJobRunsResponsePaginatorTypeDef,
    ListJobTemplatesRequestListJobTemplatesPaginateTypeDef,
    ListJobTemplatesResponsePaginatorTypeDef,
    ListManagedEndpointsRequestListManagedEndpointsPaginateTypeDef,
    ListManagedEndpointsResponsePaginatorTypeDef,
    ListSecurityConfigurationsRequestListSecurityConfigurationsPaginateTypeDef,
    ListSecurityConfigurationsResponseTypeDef,
    ListVirtualClustersRequestListVirtualClustersPaginateTypeDef,
    ListVirtualClustersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListJobRunsPaginator",
    "ListJobTemplatesPaginator",
    "ListManagedEndpointsPaginator",
    "ListSecurityConfigurationsPaginator",
    "ListVirtualClustersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListJobRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListJobRuns.html#EMRContainers.Paginator.ListJobRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listjobrunspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobRunsRequestListJobRunsPaginateTypeDef]
    ) -> AsyncIterator[ListJobRunsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListJobRuns.html#EMRContainers.Paginator.ListJobRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listjobrunspaginator)
        """

class ListJobTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListJobTemplates.html#EMRContainers.Paginator.ListJobTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listjobtemplatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobTemplatesRequestListJobTemplatesPaginateTypeDef]
    ) -> AsyncIterator[ListJobTemplatesResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListJobTemplates.html#EMRContainers.Paginator.ListJobTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listjobtemplatespaginator)
        """

class ListManagedEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListManagedEndpoints.html#EMRContainers.Paginator.ListManagedEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listmanagedendpointspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListManagedEndpointsRequestListManagedEndpointsPaginateTypeDef]
    ) -> AsyncIterator[ListManagedEndpointsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListManagedEndpoints.html#EMRContainers.Paginator.ListManagedEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listmanagedendpointspaginator)
        """

class ListSecurityConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListSecurityConfigurations.html#EMRContainers.Paginator.ListSecurityConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listsecurityconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListSecurityConfigurationsRequestListSecurityConfigurationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListSecurityConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListSecurityConfigurations.html#EMRContainers.Paginator.ListSecurityConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listsecurityconfigurationspaginator)
        """

class ListVirtualClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListVirtualClusters.html#EMRContainers.Paginator.ListVirtualClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listvirtualclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListVirtualClustersRequestListVirtualClustersPaginateTypeDef]
    ) -> AsyncIterator[ListVirtualClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListVirtualClusters.html#EMRContainers.Paginator.ListVirtualClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listvirtualclusterspaginator)
        """
