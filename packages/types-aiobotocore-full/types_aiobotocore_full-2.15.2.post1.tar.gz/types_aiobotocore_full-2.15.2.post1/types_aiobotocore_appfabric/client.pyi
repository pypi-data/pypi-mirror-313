"""
Type annotations for appfabric service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_appfabric.client import AppFabricClient

    session = get_session()
    async with session.create_client("appfabric") as client:
        client: AppFabricClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListAppAuthorizationsPaginator,
    ListAppBundlesPaginator,
    ListIngestionDestinationsPaginator,
    ListIngestionsPaginator,
)
from .type_defs import (
    BatchGetUserAccessTasksRequestRequestTypeDef,
    BatchGetUserAccessTasksResponseTypeDef,
    ConnectAppAuthorizationRequestRequestTypeDef,
    ConnectAppAuthorizationResponseTypeDef,
    CreateAppAuthorizationRequestRequestTypeDef,
    CreateAppAuthorizationResponseTypeDef,
    CreateAppBundleRequestRequestTypeDef,
    CreateAppBundleResponseTypeDef,
    CreateIngestionDestinationRequestRequestTypeDef,
    CreateIngestionDestinationResponseTypeDef,
    CreateIngestionRequestRequestTypeDef,
    CreateIngestionResponseTypeDef,
    DeleteAppAuthorizationRequestRequestTypeDef,
    DeleteAppBundleRequestRequestTypeDef,
    DeleteIngestionDestinationRequestRequestTypeDef,
    DeleteIngestionRequestRequestTypeDef,
    GetAppAuthorizationRequestRequestTypeDef,
    GetAppAuthorizationResponseTypeDef,
    GetAppBundleRequestRequestTypeDef,
    GetAppBundleResponseTypeDef,
    GetIngestionDestinationRequestRequestTypeDef,
    GetIngestionDestinationResponseTypeDef,
    GetIngestionRequestRequestTypeDef,
    GetIngestionResponseTypeDef,
    ListAppAuthorizationsRequestRequestTypeDef,
    ListAppAuthorizationsResponseTypeDef,
    ListAppBundlesRequestRequestTypeDef,
    ListAppBundlesResponseTypeDef,
    ListIngestionDestinationsRequestRequestTypeDef,
    ListIngestionDestinationsResponseTypeDef,
    ListIngestionsRequestRequestTypeDef,
    ListIngestionsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartIngestionRequestRequestTypeDef,
    StartUserAccessTasksRequestRequestTypeDef,
    StartUserAccessTasksResponseTypeDef,
    StopIngestionRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAppAuthorizationRequestRequestTypeDef,
    UpdateAppAuthorizationResponseTypeDef,
    UpdateIngestionDestinationRequestRequestTypeDef,
    UpdateIngestionDestinationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("AppFabricClient",)

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

class AppFabricClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric.html#AppFabric.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppFabricClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric.html#AppFabric.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#close)
        """

    async def batch_get_user_access_tasks(
        self, **kwargs: Unpack[BatchGetUserAccessTasksRequestRequestTypeDef]
    ) -> BatchGetUserAccessTasksResponseTypeDef:
        """
        Gets user access details in a batch request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/batch_get_user_access_tasks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#batch_get_user_access_tasks)
        """

    async def connect_app_authorization(
        self, **kwargs: Unpack[ConnectAppAuthorizationRequestRequestTypeDef]
    ) -> ConnectAppAuthorizationResponseTypeDef:
        """
        Establishes a connection between Amazon Web Services AppFabric and an
        application, which allows AppFabric to call the APIs of the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/connect_app_authorization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#connect_app_authorization)
        """

    async def create_app_authorization(
        self, **kwargs: Unpack[CreateAppAuthorizationRequestRequestTypeDef]
    ) -> CreateAppAuthorizationResponseTypeDef:
        """
        Creates an app authorization within an app bundle, which allows AppFabric to
        connect to an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/create_app_authorization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#create_app_authorization)
        """

    async def create_app_bundle(
        self, **kwargs: Unpack[CreateAppBundleRequestRequestTypeDef]
    ) -> CreateAppBundleResponseTypeDef:
        """
        Creates an app bundle to collect data from an application using AppFabric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/create_app_bundle.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#create_app_bundle)
        """

    async def create_ingestion(
        self, **kwargs: Unpack[CreateIngestionRequestRequestTypeDef]
    ) -> CreateIngestionResponseTypeDef:
        """
        Creates a data ingestion for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/create_ingestion.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#create_ingestion)
        """

    async def create_ingestion_destination(
        self, **kwargs: Unpack[CreateIngestionDestinationRequestRequestTypeDef]
    ) -> CreateIngestionDestinationResponseTypeDef:
        """
        Creates an ingestion destination, which specifies how an application's ingested
        data is processed by Amazon Web Services AppFabric and where it's delivered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/create_ingestion_destination.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#create_ingestion_destination)
        """

    async def delete_app_authorization(
        self, **kwargs: Unpack[DeleteAppAuthorizationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an app authorization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/delete_app_authorization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#delete_app_authorization)
        """

    async def delete_app_bundle(
        self, **kwargs: Unpack[DeleteAppBundleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an app bundle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/delete_app_bundle.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#delete_app_bundle)
        """

    async def delete_ingestion(
        self, **kwargs: Unpack[DeleteIngestionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an ingestion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/delete_ingestion.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#delete_ingestion)
        """

    async def delete_ingestion_destination(
        self, **kwargs: Unpack[DeleteIngestionDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an ingestion destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/delete_ingestion_destination.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#delete_ingestion_destination)
        """

    async def get_app_authorization(
        self, **kwargs: Unpack[GetAppAuthorizationRequestRequestTypeDef]
    ) -> GetAppAuthorizationResponseTypeDef:
        """
        Returns information about an app authorization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/get_app_authorization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#get_app_authorization)
        """

    async def get_app_bundle(
        self, **kwargs: Unpack[GetAppBundleRequestRequestTypeDef]
    ) -> GetAppBundleResponseTypeDef:
        """
        Returns information about an app bundle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/get_app_bundle.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#get_app_bundle)
        """

    async def get_ingestion(
        self, **kwargs: Unpack[GetIngestionRequestRequestTypeDef]
    ) -> GetIngestionResponseTypeDef:
        """
        Returns information about an ingestion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/get_ingestion.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#get_ingestion)
        """

    async def get_ingestion_destination(
        self, **kwargs: Unpack[GetIngestionDestinationRequestRequestTypeDef]
    ) -> GetIngestionDestinationResponseTypeDef:
        """
        Returns information about an ingestion destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/get_ingestion_destination.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#get_ingestion_destination)
        """

    async def list_app_authorizations(
        self, **kwargs: Unpack[ListAppAuthorizationsRequestRequestTypeDef]
    ) -> ListAppAuthorizationsResponseTypeDef:
        """
        Returns a list of all app authorizations configured for an app bundle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/list_app_authorizations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#list_app_authorizations)
        """

    async def list_app_bundles(
        self, **kwargs: Unpack[ListAppBundlesRequestRequestTypeDef]
    ) -> ListAppBundlesResponseTypeDef:
        """
        Returns a list of app bundles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/list_app_bundles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#list_app_bundles)
        """

    async def list_ingestion_destinations(
        self, **kwargs: Unpack[ListIngestionDestinationsRequestRequestTypeDef]
    ) -> ListIngestionDestinationsResponseTypeDef:
        """
        Returns a list of all ingestion destinations configured for an ingestion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/list_ingestion_destinations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#list_ingestion_destinations)
        """

    async def list_ingestions(
        self, **kwargs: Unpack[ListIngestionsRequestRequestTypeDef]
    ) -> ListIngestionsResponseTypeDef:
        """
        Returns a list of all ingestions configured for an app bundle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/list_ingestions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#list_ingestions)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#list_tags_for_resource)
        """

    async def start_ingestion(
        self, **kwargs: Unpack[StartIngestionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts (enables) an ingestion, which collects data from an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/start_ingestion.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#start_ingestion)
        """

    async def start_user_access_tasks(
        self, **kwargs: Unpack[StartUserAccessTasksRequestRequestTypeDef]
    ) -> StartUserAccessTasksResponseTypeDef:
        """
        Starts the tasks to search user access status for a specific email address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/start_user_access_tasks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#start_user_access_tasks)
        """

    async def stop_ingestion(
        self, **kwargs: Unpack[StopIngestionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops (disables) an ingestion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/stop_ingestion.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#stop_ingestion)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag or tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#untag_resource)
        """

    async def update_app_authorization(
        self, **kwargs: Unpack[UpdateAppAuthorizationRequestRequestTypeDef]
    ) -> UpdateAppAuthorizationResponseTypeDef:
        """
        Updates an app authorization within an app bundle, which allows AppFabric to
        connect to an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/update_app_authorization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#update_app_authorization)
        """

    async def update_ingestion_destination(
        self, **kwargs: Unpack[UpdateIngestionDestinationRequestRequestTypeDef]
    ) -> UpdateIngestionDestinationResponseTypeDef:
        """
        Updates an ingestion destination, which specifies how an application's ingested
        data is processed by Amazon Web Services AppFabric and where it's delivered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/update_ingestion_destination.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#update_ingestion_destination)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_app_authorizations"]
    ) -> ListAppAuthorizationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_app_bundles"]) -> ListAppBundlesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ingestion_destinations"]
    ) -> ListIngestionDestinationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_ingestions"]) -> ListIngestionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/#get_paginator)
        """

    async def __aenter__(self) -> "AppFabricClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric.html#AppFabric.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric.html#AppFabric.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appfabric/client/)
        """
