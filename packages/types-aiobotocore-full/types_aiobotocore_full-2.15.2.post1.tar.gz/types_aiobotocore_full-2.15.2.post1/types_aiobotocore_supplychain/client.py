"""
Type annotations for supplychain service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_supplychain.client import SupplyChainClient

    session = get_session()
    async with session.create_client("supplychain") as client:
        client: SupplyChainClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListDataIntegrationFlowsPaginator, ListDataLakeDatasetsPaginator
from .type_defs import (
    CreateBillOfMaterialsImportJobRequestRequestTypeDef,
    CreateBillOfMaterialsImportJobResponseTypeDef,
    CreateDataIntegrationFlowRequestRequestTypeDef,
    CreateDataIntegrationFlowResponseTypeDef,
    CreateDataLakeDatasetRequestRequestTypeDef,
    CreateDataLakeDatasetResponseTypeDef,
    DeleteDataIntegrationFlowRequestRequestTypeDef,
    DeleteDataIntegrationFlowResponseTypeDef,
    DeleteDataLakeDatasetRequestRequestTypeDef,
    DeleteDataLakeDatasetResponseTypeDef,
    GetBillOfMaterialsImportJobRequestRequestTypeDef,
    GetBillOfMaterialsImportJobResponseTypeDef,
    GetDataIntegrationFlowRequestRequestTypeDef,
    GetDataIntegrationFlowResponseTypeDef,
    GetDataLakeDatasetRequestRequestTypeDef,
    GetDataLakeDatasetResponseTypeDef,
    ListDataIntegrationFlowsRequestRequestTypeDef,
    ListDataIntegrationFlowsResponseTypeDef,
    ListDataLakeDatasetsRequestRequestTypeDef,
    ListDataLakeDatasetsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    SendDataIntegrationEventRequestRequestTypeDef,
    SendDataIntegrationEventResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDataIntegrationFlowRequestRequestTypeDef,
    UpdateDataIntegrationFlowResponseTypeDef,
    UpdateDataLakeDatasetRequestRequestTypeDef,
    UpdateDataLakeDatasetResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("SupplyChainClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class SupplyChainClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SupplyChainClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#close)
        """

    async def create_bill_of_materials_import_job(
        self, **kwargs: Unpack[CreateBillOfMaterialsImportJobRequestRequestTypeDef]
    ) -> CreateBillOfMaterialsImportJobResponseTypeDef:
        """
        CreateBillOfMaterialsImportJob creates an import job for the Product Bill Of
        Materials (BOM) entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/create_bill_of_materials_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#create_bill_of_materials_import_job)
        """

    async def create_data_integration_flow(
        self, **kwargs: Unpack[CreateDataIntegrationFlowRequestRequestTypeDef]
    ) -> CreateDataIntegrationFlowResponseTypeDef:
        """
        Create DataIntegrationFlow to map one or more different sources to one target
        using the SQL transformation query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/create_data_integration_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#create_data_integration_flow)
        """

    async def create_data_lake_dataset(
        self, **kwargs: Unpack[CreateDataLakeDatasetRequestRequestTypeDef]
    ) -> CreateDataLakeDatasetResponseTypeDef:
        """
        Create a data lake dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/create_data_lake_dataset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#create_data_lake_dataset)
        """

    async def delete_data_integration_flow(
        self, **kwargs: Unpack[DeleteDataIntegrationFlowRequestRequestTypeDef]
    ) -> DeleteDataIntegrationFlowResponseTypeDef:
        """
        Delete the DataIntegrationFlow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/delete_data_integration_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#delete_data_integration_flow)
        """

    async def delete_data_lake_dataset(
        self, **kwargs: Unpack[DeleteDataLakeDatasetRequestRequestTypeDef]
    ) -> DeleteDataLakeDatasetResponseTypeDef:
        """
        Delete a data lake dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/delete_data_lake_dataset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#delete_data_lake_dataset)
        """

    async def get_bill_of_materials_import_job(
        self, **kwargs: Unpack[GetBillOfMaterialsImportJobRequestRequestTypeDef]
    ) -> GetBillOfMaterialsImportJobResponseTypeDef:
        """
        Get status and details of a BillOfMaterialsImportJob.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_bill_of_materials_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_bill_of_materials_import_job)
        """

    async def get_data_integration_flow(
        self, **kwargs: Unpack[GetDataIntegrationFlowRequestRequestTypeDef]
    ) -> GetDataIntegrationFlowResponseTypeDef:
        """
        View the DataIntegrationFlow details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_data_integration_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_data_integration_flow)
        """

    async def get_data_lake_dataset(
        self, **kwargs: Unpack[GetDataLakeDatasetRequestRequestTypeDef]
    ) -> GetDataLakeDatasetResponseTypeDef:
        """
        Get a data lake dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_data_lake_dataset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_data_lake_dataset)
        """

    async def list_data_integration_flows(
        self, **kwargs: Unpack[ListDataIntegrationFlowsRequestRequestTypeDef]
    ) -> ListDataIntegrationFlowsResponseTypeDef:
        """
        Lists all the DataIntegrationFlows in a paginated way.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/list_data_integration_flows.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#list_data_integration_flows)
        """

    async def list_data_lake_datasets(
        self, **kwargs: Unpack[ListDataLakeDatasetsRequestRequestTypeDef]
    ) -> ListDataLakeDatasetsResponseTypeDef:
        """
        List the data lake datasets for a specific instance and name space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/list_data_lake_datasets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#list_data_lake_datasets)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List all the tags for an Amazon Web ServicesSupply Chain resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#list_tags_for_resource)
        """

    async def send_data_integration_event(
        self, **kwargs: Unpack[SendDataIntegrationEventRequestRequestTypeDef]
    ) -> SendDataIntegrationEventResponseTypeDef:
        """
        Send the transactional data payload for the event with real-time data for
        analysis or monitoring.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/send_data_integration_event.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#send_data_integration_event)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Create tags for an Amazon Web Services Supply chain resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete tags for an Amazon Web Services Supply chain resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#untag_resource)
        """

    async def update_data_integration_flow(
        self, **kwargs: Unpack[UpdateDataIntegrationFlowRequestRequestTypeDef]
    ) -> UpdateDataIntegrationFlowResponseTypeDef:
        """
        Update the DataIntegrationFlow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/update_data_integration_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#update_data_integration_flow)
        """

    async def update_data_lake_dataset(
        self, **kwargs: Unpack[UpdateDataLakeDatasetRequestRequestTypeDef]
    ) -> UpdateDataLakeDatasetResponseTypeDef:
        """
        Update a data lake dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/update_data_lake_dataset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#update_data_lake_dataset)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_integration_flows"]
    ) -> ListDataIntegrationFlowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_lake_datasets"]
    ) -> ListDataLakeDatasetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_paginator)
        """

    async def __aenter__(self) -> "SupplyChainClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/)
        """
