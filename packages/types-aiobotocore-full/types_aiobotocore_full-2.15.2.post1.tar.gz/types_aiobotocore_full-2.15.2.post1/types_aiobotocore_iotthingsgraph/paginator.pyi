"""
Type annotations for iotthingsgraph service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iotthingsgraph.client import IoTThingsGraphClient
    from types_aiobotocore_iotthingsgraph.paginator import (
        GetFlowTemplateRevisionsPaginator,
        GetSystemTemplateRevisionsPaginator,
        ListFlowExecutionMessagesPaginator,
        ListTagsForResourcePaginator,
        SearchEntitiesPaginator,
        SearchFlowExecutionsPaginator,
        SearchFlowTemplatesPaginator,
        SearchSystemInstancesPaginator,
        SearchSystemTemplatesPaginator,
        SearchThingsPaginator,
    )

    session = get_session()
    with session.create_client("iotthingsgraph") as client:
        client: IoTThingsGraphClient

        get_flow_template_revisions_paginator: GetFlowTemplateRevisionsPaginator = client.get_paginator("get_flow_template_revisions")
        get_system_template_revisions_paginator: GetSystemTemplateRevisionsPaginator = client.get_paginator("get_system_template_revisions")
        list_flow_execution_messages_paginator: ListFlowExecutionMessagesPaginator = client.get_paginator("list_flow_execution_messages")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        search_entities_paginator: SearchEntitiesPaginator = client.get_paginator("search_entities")
        search_flow_executions_paginator: SearchFlowExecutionsPaginator = client.get_paginator("search_flow_executions")
        search_flow_templates_paginator: SearchFlowTemplatesPaginator = client.get_paginator("search_flow_templates")
        search_system_instances_paginator: SearchSystemInstancesPaginator = client.get_paginator("search_system_instances")
        search_system_templates_paginator: SearchSystemTemplatesPaginator = client.get_paginator("search_system_templates")
        search_things_paginator: SearchThingsPaginator = client.get_paginator("search_things")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetFlowTemplateRevisionsRequestGetFlowTemplateRevisionsPaginateTypeDef,
    GetFlowTemplateRevisionsResponseTypeDef,
    GetSystemTemplateRevisionsRequestGetSystemTemplateRevisionsPaginateTypeDef,
    GetSystemTemplateRevisionsResponseTypeDef,
    ListFlowExecutionMessagesRequestListFlowExecutionMessagesPaginateTypeDef,
    ListFlowExecutionMessagesResponseTypeDef,
    ListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    SearchEntitiesRequestSearchEntitiesPaginateTypeDef,
    SearchEntitiesResponseTypeDef,
    SearchFlowExecutionsRequestSearchFlowExecutionsPaginateTypeDef,
    SearchFlowExecutionsResponseTypeDef,
    SearchFlowTemplatesRequestSearchFlowTemplatesPaginateTypeDef,
    SearchFlowTemplatesResponseTypeDef,
    SearchSystemInstancesRequestSearchSystemInstancesPaginateTypeDef,
    SearchSystemInstancesResponseTypeDef,
    SearchSystemTemplatesRequestSearchSystemTemplatesPaginateTypeDef,
    SearchSystemTemplatesResponseTypeDef,
    SearchThingsRequestSearchThingsPaginateTypeDef,
    SearchThingsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetFlowTemplateRevisionsPaginator",
    "GetSystemTemplateRevisionsPaginator",
    "ListFlowExecutionMessagesPaginator",
    "ListTagsForResourcePaginator",
    "SearchEntitiesPaginator",
    "SearchFlowExecutionsPaginator",
    "SearchFlowTemplatesPaginator",
    "SearchSystemInstancesPaginator",
    "SearchSystemTemplatesPaginator",
    "SearchThingsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetFlowTemplateRevisionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/GetFlowTemplateRevisions.html#IoTThingsGraph.Paginator.GetFlowTemplateRevisions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#getflowtemplaterevisionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[GetFlowTemplateRevisionsRequestGetFlowTemplateRevisionsPaginateTypeDef],
    ) -> AsyncIterator[GetFlowTemplateRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/GetFlowTemplateRevisions.html#IoTThingsGraph.Paginator.GetFlowTemplateRevisions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#getflowtemplaterevisionspaginator)
        """

class GetSystemTemplateRevisionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/GetSystemTemplateRevisions.html#IoTThingsGraph.Paginator.GetSystemTemplateRevisions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#getsystemtemplaterevisionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetSystemTemplateRevisionsRequestGetSystemTemplateRevisionsPaginateTypeDef
        ],
    ) -> AsyncIterator[GetSystemTemplateRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/GetSystemTemplateRevisions.html#IoTThingsGraph.Paginator.GetSystemTemplateRevisions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#getsystemtemplaterevisionspaginator)
        """

class ListFlowExecutionMessagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/ListFlowExecutionMessages.html#IoTThingsGraph.Paginator.ListFlowExecutionMessages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#listflowexecutionmessagespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListFlowExecutionMessagesRequestListFlowExecutionMessagesPaginateTypeDef],
    ) -> AsyncIterator[ListFlowExecutionMessagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/ListFlowExecutionMessages.html#IoTThingsGraph.Paginator.ListFlowExecutionMessages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#listflowexecutionmessagespaginator)
        """

class ListTagsForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/ListTagsForResource.html#IoTThingsGraph.Paginator.ListTagsForResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#listtagsforresourcepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> AsyncIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/ListTagsForResource.html#IoTThingsGraph.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#listtagsforresourcepaginator)
        """

class SearchEntitiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchEntities.html#IoTThingsGraph.Paginator.SearchEntities)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchentitiespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchEntitiesRequestSearchEntitiesPaginateTypeDef]
    ) -> AsyncIterator[SearchEntitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchEntities.html#IoTThingsGraph.Paginator.SearchEntities.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchentitiespaginator)
        """

class SearchFlowExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchFlowExecutions.html#IoTThingsGraph.Paginator.SearchFlowExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchflowexecutionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchFlowExecutionsRequestSearchFlowExecutionsPaginateTypeDef]
    ) -> AsyncIterator[SearchFlowExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchFlowExecutions.html#IoTThingsGraph.Paginator.SearchFlowExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchflowexecutionspaginator)
        """

class SearchFlowTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchFlowTemplates.html#IoTThingsGraph.Paginator.SearchFlowTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchflowtemplatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchFlowTemplatesRequestSearchFlowTemplatesPaginateTypeDef]
    ) -> AsyncIterator[SearchFlowTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchFlowTemplates.html#IoTThingsGraph.Paginator.SearchFlowTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchflowtemplatespaginator)
        """

class SearchSystemInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchSystemInstances.html#IoTThingsGraph.Paginator.SearchSystemInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchsysteminstancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchSystemInstancesRequestSearchSystemInstancesPaginateTypeDef]
    ) -> AsyncIterator[SearchSystemInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchSystemInstances.html#IoTThingsGraph.Paginator.SearchSystemInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchsysteminstancespaginator)
        """

class SearchSystemTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchSystemTemplates.html#IoTThingsGraph.Paginator.SearchSystemTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchsystemtemplatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchSystemTemplatesRequestSearchSystemTemplatesPaginateTypeDef]
    ) -> AsyncIterator[SearchSystemTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchSystemTemplates.html#IoTThingsGraph.Paginator.SearchSystemTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchsystemtemplatespaginator)
        """

class SearchThingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchThings.html#IoTThingsGraph.Paginator.SearchThings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchthingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchThingsRequestSearchThingsPaginateTypeDef]
    ) -> AsyncIterator[SearchThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchThings.html#IoTThingsGraph.Paginator.SearchThings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchthingspaginator)
        """
