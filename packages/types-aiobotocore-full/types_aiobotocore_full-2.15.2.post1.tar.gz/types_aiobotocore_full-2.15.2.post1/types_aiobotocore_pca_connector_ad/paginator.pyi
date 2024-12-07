"""
Type annotations for pca-connector-ad service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_ad/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_pca_connector_ad.client import PcaConnectorAdClient
    from types_aiobotocore_pca_connector_ad.paginator import (
        ListConnectorsPaginator,
        ListDirectoryRegistrationsPaginator,
        ListServicePrincipalNamesPaginator,
        ListTemplateGroupAccessControlEntriesPaginator,
        ListTemplatesPaginator,
    )

    session = get_session()
    with session.create_client("pca-connector-ad") as client:
        client: PcaConnectorAdClient

        list_connectors_paginator: ListConnectorsPaginator = client.get_paginator("list_connectors")
        list_directory_registrations_paginator: ListDirectoryRegistrationsPaginator = client.get_paginator("list_directory_registrations")
        list_service_principal_names_paginator: ListServicePrincipalNamesPaginator = client.get_paginator("list_service_principal_names")
        list_template_group_access_control_entries_paginator: ListTemplateGroupAccessControlEntriesPaginator = client.get_paginator("list_template_group_access_control_entries")
        list_templates_paginator: ListTemplatesPaginator = client.get_paginator("list_templates")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListConnectorsRequestListConnectorsPaginateTypeDef,
    ListConnectorsResponseTypeDef,
    ListDirectoryRegistrationsRequestListDirectoryRegistrationsPaginateTypeDef,
    ListDirectoryRegistrationsResponseTypeDef,
    ListServicePrincipalNamesRequestListServicePrincipalNamesPaginateTypeDef,
    ListServicePrincipalNamesResponseTypeDef,
    ListTemplateGroupAccessControlEntriesRequestListTemplateGroupAccessControlEntriesPaginateTypeDef,
    ListTemplateGroupAccessControlEntriesResponseTypeDef,
    ListTemplatesRequestListTemplatesPaginateTypeDef,
    ListTemplatesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListConnectorsPaginator",
    "ListDirectoryRegistrationsPaginator",
    "ListServicePrincipalNamesPaginator",
    "ListTemplateGroupAccessControlEntriesPaginator",
    "ListTemplatesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListConnectorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListConnectors.html#PcaConnectorAd.Paginator.ListConnectors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_ad/paginators/#listconnectorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListConnectorsRequestListConnectorsPaginateTypeDef]
    ) -> AsyncIterator[ListConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListConnectors.html#PcaConnectorAd.Paginator.ListConnectors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_ad/paginators/#listconnectorspaginator)
        """

class ListDirectoryRegistrationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListDirectoryRegistrations.html#PcaConnectorAd.Paginator.ListDirectoryRegistrations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_ad/paginators/#listdirectoryregistrationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListDirectoryRegistrationsRequestListDirectoryRegistrationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListDirectoryRegistrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListDirectoryRegistrations.html#PcaConnectorAd.Paginator.ListDirectoryRegistrations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_ad/paginators/#listdirectoryregistrationspaginator)
        """

class ListServicePrincipalNamesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListServicePrincipalNames.html#PcaConnectorAd.Paginator.ListServicePrincipalNames)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_ad/paginators/#listserviceprincipalnamespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListServicePrincipalNamesRequestListServicePrincipalNamesPaginateTypeDef],
    ) -> AsyncIterator[ListServicePrincipalNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListServicePrincipalNames.html#PcaConnectorAd.Paginator.ListServicePrincipalNames.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_ad/paginators/#listserviceprincipalnamespaginator)
        """

class ListTemplateGroupAccessControlEntriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListTemplateGroupAccessControlEntries.html#PcaConnectorAd.Paginator.ListTemplateGroupAccessControlEntries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_ad/paginators/#listtemplategroupaccesscontrolentriespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListTemplateGroupAccessControlEntriesRequestListTemplateGroupAccessControlEntriesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListTemplateGroupAccessControlEntriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListTemplateGroupAccessControlEntries.html#PcaConnectorAd.Paginator.ListTemplateGroupAccessControlEntries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_ad/paginators/#listtemplategroupaccesscontrolentriespaginator)
        """

class ListTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListTemplates.html#PcaConnectorAd.Paginator.ListTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_ad/paginators/#listtemplatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTemplatesRequestListTemplatesPaginateTypeDef]
    ) -> AsyncIterator[ListTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-ad/paginator/ListTemplates.html#PcaConnectorAd.Paginator.ListTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_ad/paginators/#listtemplatespaginator)
        """
