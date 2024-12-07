"""
Type annotations for ssm-sap service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ssm_sap.client import SsmSapClient
    from types_aiobotocore_ssm_sap.paginator import (
        ListApplicationsPaginator,
        ListComponentsPaginator,
        ListDatabasesPaginator,
        ListOperationEventsPaginator,
        ListOperationsPaginator,
    )

    session = get_session()
    with session.create_client("ssm-sap") as client:
        client: SsmSapClient

        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
        list_components_paginator: ListComponentsPaginator = client.get_paginator("list_components")
        list_databases_paginator: ListDatabasesPaginator = client.get_paginator("list_databases")
        list_operation_events_paginator: ListOperationEventsPaginator = client.get_paginator("list_operation_events")
        list_operations_paginator: ListOperationsPaginator = client.get_paginator("list_operations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListApplicationsInputListApplicationsPaginateTypeDef,
    ListApplicationsOutputTypeDef,
    ListComponentsInputListComponentsPaginateTypeDef,
    ListComponentsOutputTypeDef,
    ListDatabasesInputListDatabasesPaginateTypeDef,
    ListDatabasesOutputTypeDef,
    ListOperationEventsInputListOperationEventsPaginateTypeDef,
    ListOperationEventsOutputTypeDef,
    ListOperationsInputListOperationsPaginateTypeDef,
    ListOperationsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListApplicationsPaginator",
    "ListComponentsPaginator",
    "ListDatabasesPaginator",
    "ListOperationEventsPaginator",
    "ListOperationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListApplications.html#SsmSap.Paginator.ListApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/paginators/#listapplicationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListApplicationsInputListApplicationsPaginateTypeDef]
    ) -> AsyncIterator[ListApplicationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListApplications.html#SsmSap.Paginator.ListApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/paginators/#listapplicationspaginator)
        """

class ListComponentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListComponents.html#SsmSap.Paginator.ListComponents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/paginators/#listcomponentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListComponentsInputListComponentsPaginateTypeDef]
    ) -> AsyncIterator[ListComponentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListComponents.html#SsmSap.Paginator.ListComponents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/paginators/#listcomponentspaginator)
        """

class ListDatabasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListDatabases.html#SsmSap.Paginator.ListDatabases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/paginators/#listdatabasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDatabasesInputListDatabasesPaginateTypeDef]
    ) -> AsyncIterator[ListDatabasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListDatabases.html#SsmSap.Paginator.ListDatabases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/paginators/#listdatabasespaginator)
        """

class ListOperationEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListOperationEvents.html#SsmSap.Paginator.ListOperationEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/paginators/#listoperationeventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListOperationEventsInputListOperationEventsPaginateTypeDef]
    ) -> AsyncIterator[ListOperationEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListOperationEvents.html#SsmSap.Paginator.ListOperationEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/paginators/#listoperationeventspaginator)
        """

class ListOperationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListOperations.html#SsmSap.Paginator.ListOperations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/paginators/#listoperationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListOperationsInputListOperationsPaginateTypeDef]
    ) -> AsyncIterator[ListOperationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/paginator/ListOperations.html#SsmSap.Paginator.ListOperations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/paginators/#listoperationspaginator)
        """
