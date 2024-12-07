"""
Type annotations for tnb service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_tnb.client import TelcoNetworkBuilderClient
    from types_aiobotocore_tnb.paginator import (
        ListSolFunctionInstancesPaginator,
        ListSolFunctionPackagesPaginator,
        ListSolNetworkInstancesPaginator,
        ListSolNetworkOperationsPaginator,
        ListSolNetworkPackagesPaginator,
    )

    session = get_session()
    with session.create_client("tnb") as client:
        client: TelcoNetworkBuilderClient

        list_sol_function_instances_paginator: ListSolFunctionInstancesPaginator = client.get_paginator("list_sol_function_instances")
        list_sol_function_packages_paginator: ListSolFunctionPackagesPaginator = client.get_paginator("list_sol_function_packages")
        list_sol_network_instances_paginator: ListSolNetworkInstancesPaginator = client.get_paginator("list_sol_network_instances")
        list_sol_network_operations_paginator: ListSolNetworkOperationsPaginator = client.get_paginator("list_sol_network_operations")
        list_sol_network_packages_paginator: ListSolNetworkPackagesPaginator = client.get_paginator("list_sol_network_packages")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListSolFunctionInstancesInputListSolFunctionInstancesPaginateTypeDef,
    ListSolFunctionInstancesOutputTypeDef,
    ListSolFunctionPackagesInputListSolFunctionPackagesPaginateTypeDef,
    ListSolFunctionPackagesOutputTypeDef,
    ListSolNetworkInstancesInputListSolNetworkInstancesPaginateTypeDef,
    ListSolNetworkInstancesOutputTypeDef,
    ListSolNetworkOperationsInputListSolNetworkOperationsPaginateTypeDef,
    ListSolNetworkOperationsOutputTypeDef,
    ListSolNetworkPackagesInputListSolNetworkPackagesPaginateTypeDef,
    ListSolNetworkPackagesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListSolFunctionInstancesPaginator",
    "ListSolFunctionPackagesPaginator",
    "ListSolNetworkInstancesPaginator",
    "ListSolNetworkOperationsPaginator",
    "ListSolNetworkPackagesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListSolFunctionInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolFunctionInstances.html#TelcoNetworkBuilder.Paginator.ListSolFunctionInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolfunctioninstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSolFunctionInstancesInputListSolFunctionInstancesPaginateTypeDef]
    ) -> AsyncIterator[ListSolFunctionInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolFunctionInstances.html#TelcoNetworkBuilder.Paginator.ListSolFunctionInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolfunctioninstancespaginator)
        """


class ListSolFunctionPackagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolFunctionPackages.html#TelcoNetworkBuilder.Paginator.ListSolFunctionPackages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolfunctionpackagespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSolFunctionPackagesInputListSolFunctionPackagesPaginateTypeDef]
    ) -> AsyncIterator[ListSolFunctionPackagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolFunctionPackages.html#TelcoNetworkBuilder.Paginator.ListSolFunctionPackages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolfunctionpackagespaginator)
        """


class ListSolNetworkInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkInstances.html#TelcoNetworkBuilder.Paginator.ListSolNetworkInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolnetworkinstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSolNetworkInstancesInputListSolNetworkInstancesPaginateTypeDef]
    ) -> AsyncIterator[ListSolNetworkInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkInstances.html#TelcoNetworkBuilder.Paginator.ListSolNetworkInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolnetworkinstancespaginator)
        """


class ListSolNetworkOperationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkOperations.html#TelcoNetworkBuilder.Paginator.ListSolNetworkOperations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolnetworkoperationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSolNetworkOperationsInputListSolNetworkOperationsPaginateTypeDef]
    ) -> AsyncIterator[ListSolNetworkOperationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkOperations.html#TelcoNetworkBuilder.Paginator.ListSolNetworkOperations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolnetworkoperationspaginator)
        """


class ListSolNetworkPackagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkPackages.html#TelcoNetworkBuilder.Paginator.ListSolNetworkPackages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolnetworkpackagespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSolNetworkPackagesInputListSolNetworkPackagesPaginateTypeDef]
    ) -> AsyncIterator[ListSolNetworkPackagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/paginator/ListSolNetworkPackages.html#TelcoNetworkBuilder.Paginator.ListSolNetworkPackages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/paginators/#listsolnetworkpackagespaginator)
        """
