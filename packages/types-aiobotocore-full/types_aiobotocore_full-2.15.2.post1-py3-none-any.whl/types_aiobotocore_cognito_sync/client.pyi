"""
Type annotations for cognito-sync service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cognito_sync.client import CognitoSyncClient

    session = get_session()
    async with session.create_client("cognito-sync") as client:
        client: CognitoSyncClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    BulkPublishRequestRequestTypeDef,
    BulkPublishResponseTypeDef,
    DeleteDatasetRequestRequestTypeDef,
    DeleteDatasetResponseTypeDef,
    DescribeDatasetRequestRequestTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeIdentityPoolUsageRequestRequestTypeDef,
    DescribeIdentityPoolUsageResponseTypeDef,
    DescribeIdentityUsageRequestRequestTypeDef,
    DescribeIdentityUsageResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetBulkPublishDetailsRequestRequestTypeDef,
    GetBulkPublishDetailsResponseTypeDef,
    GetCognitoEventsRequestRequestTypeDef,
    GetCognitoEventsResponseTypeDef,
    GetIdentityPoolConfigurationRequestRequestTypeDef,
    GetIdentityPoolConfigurationResponseTypeDef,
    ListDatasetsRequestRequestTypeDef,
    ListDatasetsResponseTypeDef,
    ListIdentityPoolUsageRequestRequestTypeDef,
    ListIdentityPoolUsageResponseTypeDef,
    ListRecordsRequestRequestTypeDef,
    ListRecordsResponseTypeDef,
    RegisterDeviceRequestRequestTypeDef,
    RegisterDeviceResponseTypeDef,
    SetCognitoEventsRequestRequestTypeDef,
    SetIdentityPoolConfigurationRequestRequestTypeDef,
    SetIdentityPoolConfigurationResponseTypeDef,
    SubscribeToDatasetRequestRequestTypeDef,
    UnsubscribeFromDatasetRequestRequestTypeDef,
    UpdateRecordsRequestRequestTypeDef,
    UpdateRecordsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("CognitoSyncClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AlreadyStreamedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    DuplicateRequestException: Type[BotocoreClientError]
    InternalErrorException: Type[BotocoreClientError]
    InvalidConfigurationException: Type[BotocoreClientError]
    InvalidLambdaFunctionOutputException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LambdaThrottledException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]

class CognitoSyncClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CognitoSyncClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#close)
        """

    async def bulk_publish(
        self, **kwargs: Unpack[BulkPublishRequestRequestTypeDef]
    ) -> BulkPublishResponseTypeDef:
        """
        Initiates a bulk publish of all existing datasets for an Identity Pool to the
        configured stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/bulk_publish.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#bulk_publish)
        """

    async def delete_dataset(
        self, **kwargs: Unpack[DeleteDatasetRequestRequestTypeDef]
    ) -> DeleteDatasetResponseTypeDef:
        """
        Deletes the specific dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/delete_dataset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#delete_dataset)
        """

    async def describe_dataset(
        self, **kwargs: Unpack[DescribeDatasetRequestRequestTypeDef]
    ) -> DescribeDatasetResponseTypeDef:
        """
        Gets meta data about a dataset by identity and dataset name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/describe_dataset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#describe_dataset)
        """

    async def describe_identity_pool_usage(
        self, **kwargs: Unpack[DescribeIdentityPoolUsageRequestRequestTypeDef]
    ) -> DescribeIdentityPoolUsageResponseTypeDef:
        """
        Gets usage details (for example, data storage) about a particular identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/describe_identity_pool_usage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#describe_identity_pool_usage)
        """

    async def describe_identity_usage(
        self, **kwargs: Unpack[DescribeIdentityUsageRequestRequestTypeDef]
    ) -> DescribeIdentityUsageResponseTypeDef:
        """
        Gets usage information for an identity, including number of datasets and data
        usage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/describe_identity_usage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#describe_identity_usage)
        """

    async def get_bulk_publish_details(
        self, **kwargs: Unpack[GetBulkPublishDetailsRequestRequestTypeDef]
    ) -> GetBulkPublishDetailsResponseTypeDef:
        """
        Get the status of the last BulkPublish operation for an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/get_bulk_publish_details.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#get_bulk_publish_details)
        """

    async def get_cognito_events(
        self, **kwargs: Unpack[GetCognitoEventsRequestRequestTypeDef]
    ) -> GetCognitoEventsResponseTypeDef:
        """
        Gets the events and the corresponding Lambda functions associated with an
        identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/get_cognito_events.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#get_cognito_events)
        """

    async def get_identity_pool_configuration(
        self, **kwargs: Unpack[GetIdentityPoolConfigurationRequestRequestTypeDef]
    ) -> GetIdentityPoolConfigurationResponseTypeDef:
        """
        Gets the configuration settings of an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/get_identity_pool_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#get_identity_pool_configuration)
        """

    async def list_datasets(
        self, **kwargs: Unpack[ListDatasetsRequestRequestTypeDef]
    ) -> ListDatasetsResponseTypeDef:
        """
        Lists datasets for an identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/list_datasets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#list_datasets)
        """

    async def list_identity_pool_usage(
        self, **kwargs: Unpack[ListIdentityPoolUsageRequestRequestTypeDef]
    ) -> ListIdentityPoolUsageResponseTypeDef:
        """
        Gets a list of identity pools registered with Cognito.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/list_identity_pool_usage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#list_identity_pool_usage)
        """

    async def list_records(
        self, **kwargs: Unpack[ListRecordsRequestRequestTypeDef]
    ) -> ListRecordsResponseTypeDef:
        """
        Gets paginated records, optionally changed after a particular sync count for a
        dataset and identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/list_records.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#list_records)
        """

    async def register_device(
        self, **kwargs: Unpack[RegisterDeviceRequestRequestTypeDef]
    ) -> RegisterDeviceResponseTypeDef:
        """
        Registers a device to receive push sync notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/register_device.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#register_device)
        """

    async def set_cognito_events(
        self, **kwargs: Unpack[SetCognitoEventsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the AWS Lambda function for a given event type for an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/set_cognito_events.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#set_cognito_events)
        """

    async def set_identity_pool_configuration(
        self, **kwargs: Unpack[SetIdentityPoolConfigurationRequestRequestTypeDef]
    ) -> SetIdentityPoolConfigurationResponseTypeDef:
        """
        Sets the necessary configuration for push sync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/set_identity_pool_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#set_identity_pool_configuration)
        """

    async def subscribe_to_dataset(
        self, **kwargs: Unpack[SubscribeToDatasetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Subscribes to receive notifications when a dataset is modified by another
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/subscribe_to_dataset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#subscribe_to_dataset)
        """

    async def unsubscribe_from_dataset(
        self, **kwargs: Unpack[UnsubscribeFromDatasetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Unsubscribes from receiving notifications when a dataset is modified by another
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/unsubscribe_from_dataset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#unsubscribe_from_dataset)
        """

    async def update_records(
        self, **kwargs: Unpack[UpdateRecordsRequestRequestTypeDef]
    ) -> UpdateRecordsResponseTypeDef:
        """
        Posts updates to records and adds and deletes records for a dataset and user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/update_records.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#update_records)
        """

    async def __aenter__(self) -> "CognitoSyncClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/)
        """
