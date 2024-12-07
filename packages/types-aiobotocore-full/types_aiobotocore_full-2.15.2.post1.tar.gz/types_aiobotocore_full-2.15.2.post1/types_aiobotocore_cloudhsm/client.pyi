"""
Type annotations for cloudhsm service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudhsm.client import CloudHSMClient

    session = get_session()
    async with session.create_client("cloudhsm") as client:
        client: CloudHSMClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListHapgsPaginator, ListHsmsPaginator, ListLunaClientsPaginator
from .type_defs import (
    AddTagsToResourceRequestRequestTypeDef,
    AddTagsToResourceResponseTypeDef,
    CreateHapgRequestRequestTypeDef,
    CreateHapgResponseTypeDef,
    CreateHsmRequestRequestTypeDef,
    CreateHsmResponseTypeDef,
    CreateLunaClientRequestRequestTypeDef,
    CreateLunaClientResponseTypeDef,
    DeleteHapgRequestRequestTypeDef,
    DeleteHapgResponseTypeDef,
    DeleteHsmRequestRequestTypeDef,
    DeleteHsmResponseTypeDef,
    DeleteLunaClientRequestRequestTypeDef,
    DeleteLunaClientResponseTypeDef,
    DescribeHapgRequestRequestTypeDef,
    DescribeHapgResponseTypeDef,
    DescribeHsmRequestRequestTypeDef,
    DescribeHsmResponseTypeDef,
    DescribeLunaClientRequestRequestTypeDef,
    DescribeLunaClientResponseTypeDef,
    GetConfigRequestRequestTypeDef,
    GetConfigResponseTypeDef,
    ListAvailableZonesResponseTypeDef,
    ListHapgsRequestRequestTypeDef,
    ListHapgsResponseTypeDef,
    ListHsmsRequestRequestTypeDef,
    ListHsmsResponseTypeDef,
    ListLunaClientsRequestRequestTypeDef,
    ListLunaClientsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ModifyHapgRequestRequestTypeDef,
    ModifyHapgResponseTypeDef,
    ModifyHsmRequestRequestTypeDef,
    ModifyHsmResponseTypeDef,
    ModifyLunaClientRequestRequestTypeDef,
    ModifyLunaClientResponseTypeDef,
    RemoveTagsFromResourceRequestRequestTypeDef,
    RemoveTagsFromResourceResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("CloudHSMClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    CloudHsmInternalException: Type[BotocoreClientError]
    CloudHsmServiceException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]

class CloudHSMClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudHSMClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#close)
        """

    async def add_tags_to_resource(
        self, **kwargs: Unpack[AddTagsToResourceRequestRequestTypeDef]
    ) -> AddTagsToResourceResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/add_tags_to_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#add_tags_to_resource)
        """

    async def create_hapg(
        self, **kwargs: Unpack[CreateHapgRequestRequestTypeDef]
    ) -> CreateHapgResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/create_hapg.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#create_hapg)
        """

    async def create_hsm(
        self, **kwargs: Unpack[CreateHsmRequestRequestTypeDef]
    ) -> CreateHsmResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/create_hsm.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#create_hsm)
        """

    async def create_luna_client(
        self, **kwargs: Unpack[CreateLunaClientRequestRequestTypeDef]
    ) -> CreateLunaClientResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/create_luna_client.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#create_luna_client)
        """

    async def delete_hapg(
        self, **kwargs: Unpack[DeleteHapgRequestRequestTypeDef]
    ) -> DeleteHapgResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/delete_hapg.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#delete_hapg)
        """

    async def delete_hsm(
        self, **kwargs: Unpack[DeleteHsmRequestRequestTypeDef]
    ) -> DeleteHsmResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/delete_hsm.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#delete_hsm)
        """

    async def delete_luna_client(
        self, **kwargs: Unpack[DeleteLunaClientRequestRequestTypeDef]
    ) -> DeleteLunaClientResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/delete_luna_client.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#delete_luna_client)
        """

    async def describe_hapg(
        self, **kwargs: Unpack[DescribeHapgRequestRequestTypeDef]
    ) -> DescribeHapgResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/describe_hapg.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#describe_hapg)
        """

    async def describe_hsm(
        self, **kwargs: Unpack[DescribeHsmRequestRequestTypeDef]
    ) -> DescribeHsmResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/describe_hsm.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#describe_hsm)
        """

    async def describe_luna_client(
        self, **kwargs: Unpack[DescribeLunaClientRequestRequestTypeDef]
    ) -> DescribeLunaClientResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/describe_luna_client.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#describe_luna_client)
        """

    async def get_config(
        self, **kwargs: Unpack[GetConfigRequestRequestTypeDef]
    ) -> GetConfigResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/get_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#get_config)
        """

    async def list_available_zones(self) -> ListAvailableZonesResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/list_available_zones.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#list_available_zones)
        """

    async def list_hapgs(
        self, **kwargs: Unpack[ListHapgsRequestRequestTypeDef]
    ) -> ListHapgsResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/list_hapgs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#list_hapgs)
        """

    async def list_hsms(
        self, **kwargs: Unpack[ListHsmsRequestRequestTypeDef]
    ) -> ListHsmsResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/list_hsms.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#list_hsms)
        """

    async def list_luna_clients(
        self, **kwargs: Unpack[ListLunaClientsRequestRequestTypeDef]
    ) -> ListLunaClientsResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/list_luna_clients.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#list_luna_clients)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#list_tags_for_resource)
        """

    async def modify_hapg(
        self, **kwargs: Unpack[ModifyHapgRequestRequestTypeDef]
    ) -> ModifyHapgResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/modify_hapg.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#modify_hapg)
        """

    async def modify_hsm(
        self, **kwargs: Unpack[ModifyHsmRequestRequestTypeDef]
    ) -> ModifyHsmResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/modify_hsm.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#modify_hsm)
        """

    async def modify_luna_client(
        self, **kwargs: Unpack[ModifyLunaClientRequestRequestTypeDef]
    ) -> ModifyLunaClientResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/modify_luna_client.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#modify_luna_client)
        """

    async def remove_tags_from_resource(
        self, **kwargs: Unpack[RemoveTagsFromResourceRequestRequestTypeDef]
    ) -> RemoveTagsFromResourceResponseTypeDef:
        """
        This is documentation for <b>AWS CloudHSM Classic</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/remove_tags_from_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#remove_tags_from_resource)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_hapgs"]) -> ListHapgsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_hsms"]) -> ListHsmsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_luna_clients"]
    ) -> ListLunaClientsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#get_paginator)
        """

    async def __aenter__(self) -> "CloudHSMClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/)
        """
