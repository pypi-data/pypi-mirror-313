"""
Type annotations for secretsmanager service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_secretsmanager.client import SecretsManagerClient

    session = get_session()
    async with session.create_client("secretsmanager") as client:
        client: SecretsManagerClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListSecretsPaginator
from .type_defs import (
    BatchGetSecretValueRequestRequestTypeDef,
    BatchGetSecretValueResponseTypeDef,
    CancelRotateSecretRequestRequestTypeDef,
    CancelRotateSecretResponseTypeDef,
    CreateSecretRequestRequestTypeDef,
    CreateSecretResponseTypeDef,
    DeleteResourcePolicyRequestRequestTypeDef,
    DeleteResourcePolicyResponseTypeDef,
    DeleteSecretRequestRequestTypeDef,
    DeleteSecretResponseTypeDef,
    DescribeSecretRequestRequestTypeDef,
    DescribeSecretResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetRandomPasswordRequestRequestTypeDef,
    GetRandomPasswordResponseTypeDef,
    GetResourcePolicyRequestRequestTypeDef,
    GetResourcePolicyResponseTypeDef,
    GetSecretValueRequestRequestTypeDef,
    GetSecretValueResponseTypeDef,
    ListSecretsRequestRequestTypeDef,
    ListSecretsResponseTypeDef,
    ListSecretVersionIdsRequestRequestTypeDef,
    ListSecretVersionIdsResponseTypeDef,
    PutResourcePolicyRequestRequestTypeDef,
    PutResourcePolicyResponseTypeDef,
    PutSecretValueRequestRequestTypeDef,
    PutSecretValueResponseTypeDef,
    RemoveRegionsFromReplicationRequestRequestTypeDef,
    RemoveRegionsFromReplicationResponseTypeDef,
    ReplicateSecretToRegionsRequestRequestTypeDef,
    ReplicateSecretToRegionsResponseTypeDef,
    RestoreSecretRequestRequestTypeDef,
    RestoreSecretResponseTypeDef,
    RotateSecretRequestRequestTypeDef,
    RotateSecretResponseTypeDef,
    StopReplicationToReplicaRequestRequestTypeDef,
    StopReplicationToReplicaResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateSecretRequestRequestTypeDef,
    UpdateSecretResponseTypeDef,
    UpdateSecretVersionStageRequestRequestTypeDef,
    UpdateSecretVersionStageResponseTypeDef,
    ValidateResourcePolicyRequestRequestTypeDef,
    ValidateResourcePolicyResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("SecretsManagerClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    DecryptionFailure: Type[BotocoreClientError]
    EncryptionFailure: Type[BotocoreClientError]
    InternalServiceError: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MalformedPolicyDocumentException: Type[BotocoreClientError]
    PreconditionNotMetException: Type[BotocoreClientError]
    PublicPolicyException: Type[BotocoreClientError]
    ResourceExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]

class SecretsManagerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SecretsManagerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#close)
        """

    async def batch_get_secret_value(
        self, **kwargs: Unpack[BatchGetSecretValueRequestRequestTypeDef]
    ) -> BatchGetSecretValueResponseTypeDef:
        """
        Retrieves the contents of the encrypted fields <code>SecretString</code> or
        <code>SecretBinary</code> for up to 20 secrets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/batch_get_secret_value.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#batch_get_secret_value)
        """

    async def cancel_rotate_secret(
        self, **kwargs: Unpack[CancelRotateSecretRequestRequestTypeDef]
    ) -> CancelRotateSecretResponseTypeDef:
        """
        Turns off automatic rotation, and if a rotation is currently in progress,
        cancels the rotation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/cancel_rotate_secret.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#cancel_rotate_secret)
        """

    async def create_secret(
        self, **kwargs: Unpack[CreateSecretRequestRequestTypeDef]
    ) -> CreateSecretResponseTypeDef:
        """
        Creates a new secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/create_secret.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#create_secret)
        """

    async def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestRequestTypeDef]
    ) -> DeleteResourcePolicyResponseTypeDef:
        """
        Deletes the resource-based permission policy attached to the secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/delete_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#delete_resource_policy)
        """

    async def delete_secret(
        self, **kwargs: Unpack[DeleteSecretRequestRequestTypeDef]
    ) -> DeleteSecretResponseTypeDef:
        """
        Deletes a secret and all of its versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/delete_secret.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#delete_secret)
        """

    async def describe_secret(
        self, **kwargs: Unpack[DescribeSecretRequestRequestTypeDef]
    ) -> DescribeSecretResponseTypeDef:
        """
        Retrieves the details of a secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/describe_secret.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#describe_secret)
        """

    async def get_random_password(
        self, **kwargs: Unpack[GetRandomPasswordRequestRequestTypeDef]
    ) -> GetRandomPasswordResponseTypeDef:
        """
        Generates a random password.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/get_random_password.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#get_random_password)
        """

    async def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyRequestRequestTypeDef]
    ) -> GetResourcePolicyResponseTypeDef:
        """
        Retrieves the JSON text of the resource-based policy document attached to the
        secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/get_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#get_resource_policy)
        """

    async def get_secret_value(
        self, **kwargs: Unpack[GetSecretValueRequestRequestTypeDef]
    ) -> GetSecretValueResponseTypeDef:
        """
        Retrieves the contents of the encrypted fields <code>SecretString</code> or
        <code>SecretBinary</code> from the specified version of a secret, whichever
        contains content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/get_secret_value.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#get_secret_value)
        """

    async def list_secret_version_ids(
        self, **kwargs: Unpack[ListSecretVersionIdsRequestRequestTypeDef]
    ) -> ListSecretVersionIdsResponseTypeDef:
        """
        Lists the versions of a secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/list_secret_version_ids.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#list_secret_version_ids)
        """

    async def list_secrets(
        self, **kwargs: Unpack[ListSecretsRequestRequestTypeDef]
    ) -> ListSecretsResponseTypeDef:
        """
        Lists the secrets that are stored by Secrets Manager in the Amazon Web Services
        account, not including secrets that are marked for deletion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/list_secrets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#list_secrets)
        """

    async def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestRequestTypeDef]
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Attaches a resource-based permission policy to a secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/put_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#put_resource_policy)
        """

    async def put_secret_value(
        self, **kwargs: Unpack[PutSecretValueRequestRequestTypeDef]
    ) -> PutSecretValueResponseTypeDef:
        """
        Creates a new version with a new encrypted secret value and attaches it to the
        secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/put_secret_value.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#put_secret_value)
        """

    async def remove_regions_from_replication(
        self, **kwargs: Unpack[RemoveRegionsFromReplicationRequestRequestTypeDef]
    ) -> RemoveRegionsFromReplicationResponseTypeDef:
        """
        For a secret that is replicated to other Regions, deletes the secret replicas
        from the Regions you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/remove_regions_from_replication.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#remove_regions_from_replication)
        """

    async def replicate_secret_to_regions(
        self, **kwargs: Unpack[ReplicateSecretToRegionsRequestRequestTypeDef]
    ) -> ReplicateSecretToRegionsResponseTypeDef:
        """
        Replicates the secret to a new Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/replicate_secret_to_regions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#replicate_secret_to_regions)
        """

    async def restore_secret(
        self, **kwargs: Unpack[RestoreSecretRequestRequestTypeDef]
    ) -> RestoreSecretResponseTypeDef:
        """
        Cancels the scheduled deletion of a secret by removing the
        <code>DeletedDate</code> time stamp.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/restore_secret.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#restore_secret)
        """

    async def rotate_secret(
        self, **kwargs: Unpack[RotateSecretRequestRequestTypeDef]
    ) -> RotateSecretResponseTypeDef:
        """
        Configures and starts the asynchronous process of rotating the secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/rotate_secret.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#rotate_secret)
        """

    async def stop_replication_to_replica(
        self, **kwargs: Unpack[StopReplicationToReplicaRequestRequestTypeDef]
    ) -> StopReplicationToReplicaResponseTypeDef:
        """
        Removes the link between the replica secret and the primary secret and promotes
        the replica to a primary secret in the replica Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/stop_replication_to_replica.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#stop_replication_to_replica)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches tags to a secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes specific tags from a secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#untag_resource)
        """

    async def update_secret(
        self, **kwargs: Unpack[UpdateSecretRequestRequestTypeDef]
    ) -> UpdateSecretResponseTypeDef:
        """
        Modifies the details of a secret, including metadata and the secret value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/update_secret.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#update_secret)
        """

    async def update_secret_version_stage(
        self, **kwargs: Unpack[UpdateSecretVersionStageRequestRequestTypeDef]
    ) -> UpdateSecretVersionStageResponseTypeDef:
        """
        Modifies the staging labels attached to a version of a secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/update_secret_version_stage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#update_secret_version_stage)
        """

    async def validate_resource_policy(
        self, **kwargs: Unpack[ValidateResourcePolicyRequestRequestTypeDef]
    ) -> ValidateResourcePolicyResponseTypeDef:
        """
        Validates that a resource policy does not grant a wide range of principals
        access to your secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/validate_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#validate_resource_policy)
        """

    def get_paginator(self, operation_name: Literal["list_secrets"]) -> ListSecretsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#get_paginator)
        """

    async def __aenter__(self) -> "SecretsManagerClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/)
        """
