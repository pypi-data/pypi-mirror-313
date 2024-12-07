"""
Type annotations for datapipeline service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_datapipeline.client import DataPipelineClient
    from types_aiobotocore_datapipeline.paginator import (
        DescribeObjectsPaginator,
        ListPipelinesPaginator,
        QueryObjectsPaginator,
    )

    session = get_session()
    with session.create_client("datapipeline") as client:
        client: DataPipelineClient

        describe_objects_paginator: DescribeObjectsPaginator = client.get_paginator("describe_objects")
        list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
        query_objects_paginator: QueryObjectsPaginator = client.get_paginator("query_objects")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeObjectsInputDescribeObjectsPaginateTypeDef,
    DescribeObjectsOutputTypeDef,
    ListPipelinesInputListPipelinesPaginateTypeDef,
    ListPipelinesOutputTypeDef,
    QueryObjectsInputQueryObjectsPaginateTypeDef,
    QueryObjectsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("DescribeObjectsPaginator", "ListPipelinesPaginator", "QueryObjectsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeObjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/DescribeObjects.html#DataPipeline.Paginator.DescribeObjects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators/#describeobjectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeObjectsInputDescribeObjectsPaginateTypeDef]
    ) -> AsyncIterator[DescribeObjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/DescribeObjects.html#DataPipeline.Paginator.DescribeObjects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators/#describeobjectspaginator)
        """

class ListPipelinesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/ListPipelines.html#DataPipeline.Paginator.ListPipelines)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators/#listpipelinespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPipelinesInputListPipelinesPaginateTypeDef]
    ) -> AsyncIterator[ListPipelinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/ListPipelines.html#DataPipeline.Paginator.ListPipelines.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators/#listpipelinespaginator)
        """

class QueryObjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/QueryObjects.html#DataPipeline.Paginator.QueryObjects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators/#queryobjectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[QueryObjectsInputQueryObjectsPaginateTypeDef]
    ) -> AsyncIterator[QueryObjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datapipeline/paginator/QueryObjects.html#DataPipeline.Paginator.QueryObjects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datapipeline/paginators/#queryobjectspaginator)
        """
