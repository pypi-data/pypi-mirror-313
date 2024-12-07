"""
Type annotations for taxsettings service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_taxsettings.client import TaxSettingsClient
    from types_aiobotocore_taxsettings.paginator import (
        ListTaxRegistrationsPaginator,
    )

    session = get_session()
    with session.create_client("taxsettings") as client:
        client: TaxSettingsClient

        list_tax_registrations_paginator: ListTaxRegistrationsPaginator = client.get_paginator("list_tax_registrations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListTaxRegistrationsRequestListTaxRegistrationsPaginateTypeDef,
    ListTaxRegistrationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListTaxRegistrationsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListTaxRegistrationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/paginator/ListTaxRegistrations.html#TaxSettings.Paginator.ListTaxRegistrations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/#listtaxregistrationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTaxRegistrationsRequestListTaxRegistrationsPaginateTypeDef]
    ) -> AsyncIterator[ListTaxRegistrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/paginator/ListTaxRegistrations.html#TaxSettings.Paginator.ListTaxRegistrations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/#listtaxregistrationspaginator)
        """
