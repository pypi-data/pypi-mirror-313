"""
Type annotations for backup-gateway service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_backup_gateway.client import BackupGatewayClient
    from types_aiobotocore_backup_gateway.paginator import (
        ListGatewaysPaginator,
        ListHypervisorsPaginator,
        ListVirtualMachinesPaginator,
    )

    session = get_session()
    with session.create_client("backup-gateway") as client:
        client: BackupGatewayClient

        list_gateways_paginator: ListGatewaysPaginator = client.get_paginator("list_gateways")
        list_hypervisors_paginator: ListHypervisorsPaginator = client.get_paginator("list_hypervisors")
        list_virtual_machines_paginator: ListVirtualMachinesPaginator = client.get_paginator("list_virtual_machines")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListGatewaysInputListGatewaysPaginateTypeDef,
    ListGatewaysOutputTypeDef,
    ListHypervisorsInputListHypervisorsPaginateTypeDef,
    ListHypervisorsOutputTypeDef,
    ListVirtualMachinesInputListVirtualMachinesPaginateTypeDef,
    ListVirtualMachinesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListGatewaysPaginator", "ListHypervisorsPaginator", "ListVirtualMachinesPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListGatewaysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListGateways.html#BackupGateway.Paginator.ListGateways)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/paginators/#listgatewayspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGatewaysInputListGatewaysPaginateTypeDef]
    ) -> AsyncIterator[ListGatewaysOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListGateways.html#BackupGateway.Paginator.ListGateways.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/paginators/#listgatewayspaginator)
        """

class ListHypervisorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListHypervisors.html#BackupGateway.Paginator.ListHypervisors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/paginators/#listhypervisorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListHypervisorsInputListHypervisorsPaginateTypeDef]
    ) -> AsyncIterator[ListHypervisorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListHypervisors.html#BackupGateway.Paginator.ListHypervisors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/paginators/#listhypervisorspaginator)
        """

class ListVirtualMachinesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListVirtualMachines.html#BackupGateway.Paginator.ListVirtualMachines)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/paginators/#listvirtualmachinespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListVirtualMachinesInputListVirtualMachinesPaginateTypeDef]
    ) -> AsyncIterator[ListVirtualMachinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway/paginator/ListVirtualMachines.html#BackupGateway.Paginator.ListVirtualMachines.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/paginators/#listvirtualmachinespaginator)
        """
