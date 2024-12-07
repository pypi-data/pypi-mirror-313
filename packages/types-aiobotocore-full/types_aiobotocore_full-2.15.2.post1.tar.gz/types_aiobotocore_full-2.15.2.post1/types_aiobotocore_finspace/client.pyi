"""
Type annotations for finspace service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_finspace.client import FinspaceClient

    session = get_session()
    async with session.create_client("finspace") as client:
        client: FinspaceClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListKxEnvironmentsPaginator
from .type_defs import (
    CreateEnvironmentRequestRequestTypeDef,
    CreateEnvironmentResponseTypeDef,
    CreateKxChangesetRequestRequestTypeDef,
    CreateKxChangesetResponseTypeDef,
    CreateKxClusterRequestRequestTypeDef,
    CreateKxClusterResponseTypeDef,
    CreateKxDatabaseRequestRequestTypeDef,
    CreateKxDatabaseResponseTypeDef,
    CreateKxDataviewRequestRequestTypeDef,
    CreateKxDataviewResponseTypeDef,
    CreateKxEnvironmentRequestRequestTypeDef,
    CreateKxEnvironmentResponseTypeDef,
    CreateKxScalingGroupRequestRequestTypeDef,
    CreateKxScalingGroupResponseTypeDef,
    CreateKxUserRequestRequestTypeDef,
    CreateKxUserResponseTypeDef,
    CreateKxVolumeRequestRequestTypeDef,
    CreateKxVolumeResponseTypeDef,
    DeleteEnvironmentRequestRequestTypeDef,
    DeleteKxClusterNodeRequestRequestTypeDef,
    DeleteKxClusterRequestRequestTypeDef,
    DeleteKxDatabaseRequestRequestTypeDef,
    DeleteKxDataviewRequestRequestTypeDef,
    DeleteKxEnvironmentRequestRequestTypeDef,
    DeleteKxScalingGroupRequestRequestTypeDef,
    DeleteKxUserRequestRequestTypeDef,
    DeleteKxVolumeRequestRequestTypeDef,
    GetEnvironmentRequestRequestTypeDef,
    GetEnvironmentResponseTypeDef,
    GetKxChangesetRequestRequestTypeDef,
    GetKxChangesetResponseTypeDef,
    GetKxClusterRequestRequestTypeDef,
    GetKxClusterResponseTypeDef,
    GetKxConnectionStringRequestRequestTypeDef,
    GetKxConnectionStringResponseTypeDef,
    GetKxDatabaseRequestRequestTypeDef,
    GetKxDatabaseResponseTypeDef,
    GetKxDataviewRequestRequestTypeDef,
    GetKxDataviewResponseTypeDef,
    GetKxEnvironmentRequestRequestTypeDef,
    GetKxEnvironmentResponseTypeDef,
    GetKxScalingGroupRequestRequestTypeDef,
    GetKxScalingGroupResponseTypeDef,
    GetKxUserRequestRequestTypeDef,
    GetKxUserResponseTypeDef,
    GetKxVolumeRequestRequestTypeDef,
    GetKxVolumeResponseTypeDef,
    ListEnvironmentsRequestRequestTypeDef,
    ListEnvironmentsResponseTypeDef,
    ListKxChangesetsRequestRequestTypeDef,
    ListKxChangesetsResponseTypeDef,
    ListKxClusterNodesRequestRequestTypeDef,
    ListKxClusterNodesResponseTypeDef,
    ListKxClustersRequestRequestTypeDef,
    ListKxClustersResponseTypeDef,
    ListKxDatabasesRequestRequestTypeDef,
    ListKxDatabasesResponseTypeDef,
    ListKxDataviewsRequestRequestTypeDef,
    ListKxDataviewsResponseTypeDef,
    ListKxEnvironmentsRequestRequestTypeDef,
    ListKxEnvironmentsResponseTypeDef,
    ListKxScalingGroupsRequestRequestTypeDef,
    ListKxScalingGroupsResponseTypeDef,
    ListKxUsersRequestRequestTypeDef,
    ListKxUsersResponseTypeDef,
    ListKxVolumesRequestRequestTypeDef,
    ListKxVolumesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateEnvironmentRequestRequestTypeDef,
    UpdateEnvironmentResponseTypeDef,
    UpdateKxClusterCodeConfigurationRequestRequestTypeDef,
    UpdateKxClusterDatabasesRequestRequestTypeDef,
    UpdateKxDatabaseRequestRequestTypeDef,
    UpdateKxDatabaseResponseTypeDef,
    UpdateKxDataviewRequestRequestTypeDef,
    UpdateKxDataviewResponseTypeDef,
    UpdateKxEnvironmentNetworkRequestRequestTypeDef,
    UpdateKxEnvironmentNetworkResponseTypeDef,
    UpdateKxEnvironmentRequestRequestTypeDef,
    UpdateKxEnvironmentResponseTypeDef,
    UpdateKxUserRequestRequestTypeDef,
    UpdateKxUserResponseTypeDef,
    UpdateKxVolumeRequestRequestTypeDef,
    UpdateKxVolumeResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("FinspaceClient",)

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
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class FinspaceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        FinspaceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#close)
        """

    async def create_environment(
        self, **kwargs: Unpack[CreateEnvironmentRequestRequestTypeDef]
    ) -> CreateEnvironmentResponseTypeDef:
        """
        Create a new FinSpace environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/create_environment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#create_environment)
        """

    async def create_kx_changeset(
        self, **kwargs: Unpack[CreateKxChangesetRequestRequestTypeDef]
    ) -> CreateKxChangesetResponseTypeDef:
        """
        Creates a changeset for a kdb database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/create_kx_changeset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#create_kx_changeset)
        """

    async def create_kx_cluster(
        self, **kwargs: Unpack[CreateKxClusterRequestRequestTypeDef]
    ) -> CreateKxClusterResponseTypeDef:
        """
        Creates a new kdb cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/create_kx_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#create_kx_cluster)
        """

    async def create_kx_database(
        self, **kwargs: Unpack[CreateKxDatabaseRequestRequestTypeDef]
    ) -> CreateKxDatabaseResponseTypeDef:
        """
        Creates a new kdb database in the environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/create_kx_database.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#create_kx_database)
        """

    async def create_kx_dataview(
        self, **kwargs: Unpack[CreateKxDataviewRequestRequestTypeDef]
    ) -> CreateKxDataviewResponseTypeDef:
        """
        Creates a snapshot of kdb database with tiered storage capabilities and a
        pre-warmed cache, ready for mounting on kdb clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/create_kx_dataview.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#create_kx_dataview)
        """

    async def create_kx_environment(
        self, **kwargs: Unpack[CreateKxEnvironmentRequestRequestTypeDef]
    ) -> CreateKxEnvironmentResponseTypeDef:
        """
        Creates a managed kdb environment for the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/create_kx_environment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#create_kx_environment)
        """

    async def create_kx_scaling_group(
        self, **kwargs: Unpack[CreateKxScalingGroupRequestRequestTypeDef]
    ) -> CreateKxScalingGroupResponseTypeDef:
        """
        Creates a new scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/create_kx_scaling_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#create_kx_scaling_group)
        """

    async def create_kx_user(
        self, **kwargs: Unpack[CreateKxUserRequestRequestTypeDef]
    ) -> CreateKxUserResponseTypeDef:
        """
        Creates a user in FinSpace kdb environment with an associated IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/create_kx_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#create_kx_user)
        """

    async def create_kx_volume(
        self, **kwargs: Unpack[CreateKxVolumeRequestRequestTypeDef]
    ) -> CreateKxVolumeResponseTypeDef:
        """
        Creates a new volume with a specific amount of throughput and storage capacity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/create_kx_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#create_kx_volume)
        """

    async def delete_environment(
        self, **kwargs: Unpack[DeleteEnvironmentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete an FinSpace environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/delete_environment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#delete_environment)
        """

    async def delete_kx_cluster(
        self, **kwargs: Unpack[DeleteKxClusterRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a kdb cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/delete_kx_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#delete_kx_cluster)
        """

    async def delete_kx_cluster_node(
        self, **kwargs: Unpack[DeleteKxClusterNodeRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified nodes from a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/delete_kx_cluster_node.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#delete_kx_cluster_node)
        """

    async def delete_kx_database(
        self, **kwargs: Unpack[DeleteKxDatabaseRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified database and all of its associated data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/delete_kx_database.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#delete_kx_database)
        """

    async def delete_kx_dataview(
        self, **kwargs: Unpack[DeleteKxDataviewRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified dataview.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/delete_kx_dataview.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#delete_kx_dataview)
        """

    async def delete_kx_environment(
        self, **kwargs: Unpack[DeleteKxEnvironmentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the kdb environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/delete_kx_environment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#delete_kx_environment)
        """

    async def delete_kx_scaling_group(
        self, **kwargs: Unpack[DeleteKxScalingGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/delete_kx_scaling_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#delete_kx_scaling_group)
        """

    async def delete_kx_user(
        self, **kwargs: Unpack[DeleteKxUserRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a user in the specified kdb environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/delete_kx_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#delete_kx_user)
        """

    async def delete_kx_volume(
        self, **kwargs: Unpack[DeleteKxVolumeRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/delete_kx_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#delete_kx_volume)
        """

    async def get_environment(
        self, **kwargs: Unpack[GetEnvironmentRequestRequestTypeDef]
    ) -> GetEnvironmentResponseTypeDef:
        """
        Returns the FinSpace environment object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/get_environment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#get_environment)
        """

    async def get_kx_changeset(
        self, **kwargs: Unpack[GetKxChangesetRequestRequestTypeDef]
    ) -> GetKxChangesetResponseTypeDef:
        """
        Returns information about a kdb changeset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/get_kx_changeset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#get_kx_changeset)
        """

    async def get_kx_cluster(
        self, **kwargs: Unpack[GetKxClusterRequestRequestTypeDef]
    ) -> GetKxClusterResponseTypeDef:
        """
        Retrieves information about a kdb cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/get_kx_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#get_kx_cluster)
        """

    async def get_kx_connection_string(
        self, **kwargs: Unpack[GetKxConnectionStringRequestRequestTypeDef]
    ) -> GetKxConnectionStringResponseTypeDef:
        """
        Retrieves a connection string for a user to connect to a kdb cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/get_kx_connection_string.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#get_kx_connection_string)
        """

    async def get_kx_database(
        self, **kwargs: Unpack[GetKxDatabaseRequestRequestTypeDef]
    ) -> GetKxDatabaseResponseTypeDef:
        """
        Returns database information for the specified environment ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/get_kx_database.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#get_kx_database)
        """

    async def get_kx_dataview(
        self, **kwargs: Unpack[GetKxDataviewRequestRequestTypeDef]
    ) -> GetKxDataviewResponseTypeDef:
        """
        Retrieves details of the dataview.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/get_kx_dataview.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#get_kx_dataview)
        """

    async def get_kx_environment(
        self, **kwargs: Unpack[GetKxEnvironmentRequestRequestTypeDef]
    ) -> GetKxEnvironmentResponseTypeDef:
        """
        Retrieves all the information for the specified kdb environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/get_kx_environment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#get_kx_environment)
        """

    async def get_kx_scaling_group(
        self, **kwargs: Unpack[GetKxScalingGroupRequestRequestTypeDef]
    ) -> GetKxScalingGroupResponseTypeDef:
        """
        Retrieves details of a scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/get_kx_scaling_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#get_kx_scaling_group)
        """

    async def get_kx_user(
        self, **kwargs: Unpack[GetKxUserRequestRequestTypeDef]
    ) -> GetKxUserResponseTypeDef:
        """
        Retrieves information about the specified kdb user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/get_kx_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#get_kx_user)
        """

    async def get_kx_volume(
        self, **kwargs: Unpack[GetKxVolumeRequestRequestTypeDef]
    ) -> GetKxVolumeResponseTypeDef:
        """
        Retrieves the information about the volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/get_kx_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#get_kx_volume)
        """

    async def list_environments(
        self, **kwargs: Unpack[ListEnvironmentsRequestRequestTypeDef]
    ) -> ListEnvironmentsResponseTypeDef:
        """
        A list of all of your FinSpace environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/list_environments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#list_environments)
        """

    async def list_kx_changesets(
        self, **kwargs: Unpack[ListKxChangesetsRequestRequestTypeDef]
    ) -> ListKxChangesetsResponseTypeDef:
        """
        Returns a list of all the changesets for a database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/list_kx_changesets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#list_kx_changesets)
        """

    async def list_kx_cluster_nodes(
        self, **kwargs: Unpack[ListKxClusterNodesRequestRequestTypeDef]
    ) -> ListKxClusterNodesResponseTypeDef:
        """
        Lists all the nodes in a kdb cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/list_kx_cluster_nodes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#list_kx_cluster_nodes)
        """

    async def list_kx_clusters(
        self, **kwargs: Unpack[ListKxClustersRequestRequestTypeDef]
    ) -> ListKxClustersResponseTypeDef:
        """
        Returns a list of clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/list_kx_clusters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#list_kx_clusters)
        """

    async def list_kx_databases(
        self, **kwargs: Unpack[ListKxDatabasesRequestRequestTypeDef]
    ) -> ListKxDatabasesResponseTypeDef:
        """
        Returns a list of all the databases in the kdb environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/list_kx_databases.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#list_kx_databases)
        """

    async def list_kx_dataviews(
        self, **kwargs: Unpack[ListKxDataviewsRequestRequestTypeDef]
    ) -> ListKxDataviewsResponseTypeDef:
        """
        Returns a list of all the dataviews in the database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/list_kx_dataviews.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#list_kx_dataviews)
        """

    async def list_kx_environments(
        self, **kwargs: Unpack[ListKxEnvironmentsRequestRequestTypeDef]
    ) -> ListKxEnvironmentsResponseTypeDef:
        """
        Returns a list of kdb environments created in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/list_kx_environments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#list_kx_environments)
        """

    async def list_kx_scaling_groups(
        self, **kwargs: Unpack[ListKxScalingGroupsRequestRequestTypeDef]
    ) -> ListKxScalingGroupsResponseTypeDef:
        """
        Returns a list of scaling groups in a kdb environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/list_kx_scaling_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#list_kx_scaling_groups)
        """

    async def list_kx_users(
        self, **kwargs: Unpack[ListKxUsersRequestRequestTypeDef]
    ) -> ListKxUsersResponseTypeDef:
        """
        Lists all the users in a kdb environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/list_kx_users.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#list_kx_users)
        """

    async def list_kx_volumes(
        self, **kwargs: Unpack[ListKxVolumesRequestRequestTypeDef]
    ) -> ListKxVolumesResponseTypeDef:
        """
        Lists all the volumes in a kdb environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/list_kx_volumes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#list_kx_volumes)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        A list of all tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#list_tags_for_resource)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds metadata tags to a FinSpace resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes metadata tags from a FinSpace resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#untag_resource)
        """

    async def update_environment(
        self, **kwargs: Unpack[UpdateEnvironmentRequestRequestTypeDef]
    ) -> UpdateEnvironmentResponseTypeDef:
        """
        Update your FinSpace environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/update_environment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#update_environment)
        """

    async def update_kx_cluster_code_configuration(
        self, **kwargs: Unpack[UpdateKxClusterCodeConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Allows you to update code configuration on a running cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/update_kx_cluster_code_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#update_kx_cluster_code_configuration)
        """

    async def update_kx_cluster_databases(
        self, **kwargs: Unpack[UpdateKxClusterDatabasesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the databases mounted on a kdb cluster, which includes the
        <code>changesetId</code> and all the dbPaths to be cached.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/update_kx_cluster_databases.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#update_kx_cluster_databases)
        """

    async def update_kx_database(
        self, **kwargs: Unpack[UpdateKxDatabaseRequestRequestTypeDef]
    ) -> UpdateKxDatabaseResponseTypeDef:
        """
        Updates information for the given kdb database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/update_kx_database.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#update_kx_database)
        """

    async def update_kx_dataview(
        self, **kwargs: Unpack[UpdateKxDataviewRequestRequestTypeDef]
    ) -> UpdateKxDataviewResponseTypeDef:
        """
        Updates the specified dataview.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/update_kx_dataview.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#update_kx_dataview)
        """

    async def update_kx_environment(
        self, **kwargs: Unpack[UpdateKxEnvironmentRequestRequestTypeDef]
    ) -> UpdateKxEnvironmentResponseTypeDef:
        """
        Updates information for the given kdb environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/update_kx_environment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#update_kx_environment)
        """

    async def update_kx_environment_network(
        self, **kwargs: Unpack[UpdateKxEnvironmentNetworkRequestRequestTypeDef]
    ) -> UpdateKxEnvironmentNetworkResponseTypeDef:
        """
        Updates environment network to connect to your internal network by using a
        transit gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/update_kx_environment_network.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#update_kx_environment_network)
        """

    async def update_kx_user(
        self, **kwargs: Unpack[UpdateKxUserRequestRequestTypeDef]
    ) -> UpdateKxUserResponseTypeDef:
        """
        Updates the user details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/update_kx_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#update_kx_user)
        """

    async def update_kx_volume(
        self, **kwargs: Unpack[UpdateKxVolumeRequestRequestTypeDef]
    ) -> UpdateKxVolumeResponseTypeDef:
        """
        Updates the throughput or capacity of a volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/update_kx_volume.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#update_kx_volume)
        """

    def get_paginator(
        self, operation_name: Literal["list_kx_environments"]
    ) -> ListKxEnvironmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/#get_paginator)
        """

    async def __aenter__(self) -> "FinspaceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/client/)
        """
