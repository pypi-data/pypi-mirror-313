"""
Type annotations for s3control service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_s3control.client import S3ControlClient
    from types_aiobotocore_s3control.paginator import (
        ListAccessPointsForObjectLambdaPaginator,
        ListCallerAccessGrantsPaginator,
    )

    session = get_session()
    with session.create_client("s3control") as client:
        client: S3ControlClient

        list_access_points_for_object_lambda_paginator: ListAccessPointsForObjectLambdaPaginator = client.get_paginator("list_access_points_for_object_lambda")
        list_caller_access_grants_paginator: ListCallerAccessGrantsPaginator = client.get_paginator("list_caller_access_grants")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAccessPointsForObjectLambdaRequestListAccessPointsForObjectLambdaPaginateTypeDef,
    ListAccessPointsForObjectLambdaResultTypeDef,
    ListCallerAccessGrantsRequestListCallerAccessGrantsPaginateTypeDef,
    ListCallerAccessGrantsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListAccessPointsForObjectLambdaPaginator", "ListCallerAccessGrantsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAccessPointsForObjectLambdaPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/paginator/ListAccessPointsForObjectLambda.html#S3Control.Paginator.ListAccessPointsForObjectLambda)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/paginators/#listaccesspointsforobjectlambdapaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAccessPointsForObjectLambdaRequestListAccessPointsForObjectLambdaPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAccessPointsForObjectLambdaResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/paginator/ListAccessPointsForObjectLambda.html#S3Control.Paginator.ListAccessPointsForObjectLambda.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/paginators/#listaccesspointsforobjectlambdapaginator)
        """

class ListCallerAccessGrantsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/paginator/ListCallerAccessGrants.html#S3Control.Paginator.ListCallerAccessGrants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/paginators/#listcalleraccessgrantspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCallerAccessGrantsRequestListCallerAccessGrantsPaginateTypeDef]
    ) -> AsyncIterator[ListCallerAccessGrantsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/paginator/ListCallerAccessGrants.html#S3Control.Paginator.ListCallerAccessGrants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/paginators/#listcalleraccessgrantspaginator)
        """
