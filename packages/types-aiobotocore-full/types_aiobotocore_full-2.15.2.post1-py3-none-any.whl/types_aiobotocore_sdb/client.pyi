"""
Type annotations for sdb service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sdb.client import SimpleDBClient

    session = get_session()
    async with session.create_client("sdb") as client:
        client: SimpleDBClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListDomainsPaginator, SelectPaginator
from .type_defs import (
    BatchDeleteAttributesRequestRequestTypeDef,
    BatchPutAttributesRequestRequestTypeDef,
    CreateDomainRequestRequestTypeDef,
    DeleteAttributesRequestRequestTypeDef,
    DeleteDomainRequestRequestTypeDef,
    DomainMetadataRequestRequestTypeDef,
    DomainMetadataResultTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAttributesRequestRequestTypeDef,
    GetAttributesResultTypeDef,
    ListDomainsRequestRequestTypeDef,
    ListDomainsResultTypeDef,
    PutAttributesRequestRequestTypeDef,
    SelectRequestRequestTypeDef,
    SelectResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("SimpleDBClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AttributeDoesNotExist: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DuplicateItemName: Type[BotocoreClientError]
    InvalidNextToken: Type[BotocoreClientError]
    InvalidNumberPredicates: Type[BotocoreClientError]
    InvalidNumberValueTests: Type[BotocoreClientError]
    InvalidParameterValue: Type[BotocoreClientError]
    InvalidQueryExpression: Type[BotocoreClientError]
    MissingParameter: Type[BotocoreClientError]
    NoSuchDomain: Type[BotocoreClientError]
    NumberDomainAttributesExceeded: Type[BotocoreClientError]
    NumberDomainBytesExceeded: Type[BotocoreClientError]
    NumberDomainsExceeded: Type[BotocoreClientError]
    NumberItemAttributesExceeded: Type[BotocoreClientError]
    NumberSubmittedAttributesExceeded: Type[BotocoreClientError]
    NumberSubmittedItemsExceeded: Type[BotocoreClientError]
    RequestTimeout: Type[BotocoreClientError]
    TooManyRequestedAttributes: Type[BotocoreClientError]

class SimpleDBClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb.html#SimpleDB.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SimpleDBClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb.html#SimpleDB.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/#close)
        """

    async def batch_delete_attributes(
        self, **kwargs: Unpack[BatchDeleteAttributesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Performs multiple DeleteAttributes operations in a single call, which reduces
        round trips and latencies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/client/batch_delete_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/#batch_delete_attributes)
        """

    async def batch_put_attributes(
        self, **kwargs: Unpack[BatchPutAttributesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        The <code>BatchPutAttributes</code> operation creates or replaces attributes
        within one or more items.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/client/batch_put_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/#batch_put_attributes)
        """

    async def create_domain(
        self, **kwargs: Unpack[CreateDomainRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        The <code>CreateDomain</code> operation creates a new domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/client/create_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/#create_domain)
        """

    async def delete_attributes(
        self, **kwargs: Unpack[DeleteAttributesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes one or more attributes associated with an item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/client/delete_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/#delete_attributes)
        """

    async def delete_domain(
        self, **kwargs: Unpack[DeleteDomainRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        The <code>DeleteDomain</code> operation deletes a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/client/delete_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/#delete_domain)
        """

    async def domain_metadata(
        self, **kwargs: Unpack[DomainMetadataRequestRequestTypeDef]
    ) -> DomainMetadataResultTypeDef:
        """
        Returns information about the domain, including when the domain was created,
        the number of items and attributes in the domain, and the size of the attribute
        names and values.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/client/domain_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/#domain_metadata)
        """

    async def get_attributes(
        self, **kwargs: Unpack[GetAttributesRequestRequestTypeDef]
    ) -> GetAttributesResultTypeDef:
        """
        Returns all of the attributes associated with the specified item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/client/get_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/#get_attributes)
        """

    async def list_domains(
        self, **kwargs: Unpack[ListDomainsRequestRequestTypeDef]
    ) -> ListDomainsResultTypeDef:
        """
        The <code>ListDomains</code> operation lists all domains associated with the
        Access Key ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/client/list_domains.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/#list_domains)
        """

    async def put_attributes(
        self, **kwargs: Unpack[PutAttributesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        The PutAttributes operation creates or replaces attributes in an item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/client/put_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/#put_attributes)
        """

    async def select(self, **kwargs: Unpack[SelectRequestRequestTypeDef]) -> SelectResultTypeDef:
        """
        The <code>Select</code> operation returns a set of attributes for
        <code>ItemNames</code> that match the select expression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/client/select.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/#select)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_domains"]) -> ListDomainsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["select"]) -> SelectPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/#get_paginator)
        """

    async def __aenter__(self) -> "SimpleDBClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb.html#SimpleDB.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb.html#SimpleDB.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/client/)
        """
