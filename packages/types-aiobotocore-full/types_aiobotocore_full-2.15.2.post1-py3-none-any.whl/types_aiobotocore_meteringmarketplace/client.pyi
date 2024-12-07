"""
Type annotations for meteringmarketplace service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_meteringmarketplace/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_meteringmarketplace.client import MarketplaceMeteringClient

    session = get_session()
    async with session.create_client("meteringmarketplace") as client:
        client: MarketplaceMeteringClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    BatchMeterUsageRequestRequestTypeDef,
    BatchMeterUsageResultTypeDef,
    MeterUsageRequestRequestTypeDef,
    MeterUsageResultTypeDef,
    RegisterUsageRequestRequestTypeDef,
    RegisterUsageResultTypeDef,
    ResolveCustomerRequestRequestTypeDef,
    ResolveCustomerResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("MarketplaceMeteringClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    CustomerNotEntitledException: Type[BotocoreClientError]
    DisabledApiException: Type[BotocoreClientError]
    DuplicateRequestException: Type[BotocoreClientError]
    ExpiredTokenException: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidCustomerIdentifierException: Type[BotocoreClientError]
    InvalidEndpointRegionException: Type[BotocoreClientError]
    InvalidProductCodeException: Type[BotocoreClientError]
    InvalidPublicKeyVersionException: Type[BotocoreClientError]
    InvalidRegionException: Type[BotocoreClientError]
    InvalidTagException: Type[BotocoreClientError]
    InvalidTokenException: Type[BotocoreClientError]
    InvalidUsageAllocationsException: Type[BotocoreClientError]
    InvalidUsageDimensionException: Type[BotocoreClientError]
    PlatformNotSupportedException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TimestampOutOfBoundsException: Type[BotocoreClientError]

class MarketplaceMeteringClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace.html#MarketplaceMetering.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_meteringmarketplace/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MarketplaceMeteringClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace.html#MarketplaceMetering.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_meteringmarketplace/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_meteringmarketplace/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_meteringmarketplace/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_meteringmarketplace/client/#close)
        """

    async def batch_meter_usage(
        self, **kwargs: Unpack[BatchMeterUsageRequestRequestTypeDef]
    ) -> BatchMeterUsageResultTypeDef:
        """
        <code>BatchMeterUsage</code> is called from a SaaS application listed on AWS
        Marketplace to post metering records for a set of customers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace/client/batch_meter_usage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_meteringmarketplace/client/#batch_meter_usage)
        """

    async def meter_usage(
        self, **kwargs: Unpack[MeterUsageRequestRequestTypeDef]
    ) -> MeterUsageResultTypeDef:
        """
        API to emit metering records.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace/client/meter_usage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_meteringmarketplace/client/#meter_usage)
        """

    async def register_usage(
        self, **kwargs: Unpack[RegisterUsageRequestRequestTypeDef]
    ) -> RegisterUsageResultTypeDef:
        """
        Paid container software products sold through AWS Marketplace must integrate
        with the AWS Marketplace Metering Service and call the
        <code>RegisterUsage</code> operation for software entitlement and metering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace/client/register_usage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_meteringmarketplace/client/#register_usage)
        """

    async def resolve_customer(
        self, **kwargs: Unpack[ResolveCustomerRequestRequestTypeDef]
    ) -> ResolveCustomerResultTypeDef:
        """
        <code>ResolveCustomer</code> is called by a SaaS application during the
        registration process.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace/client/resolve_customer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_meteringmarketplace/client/#resolve_customer)
        """

    async def __aenter__(self) -> "MarketplaceMeteringClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace.html#MarketplaceMetering.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_meteringmarketplace/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace.html#MarketplaceMetering.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_meteringmarketplace/client/)
        """
