"""
Type annotations for rds-data service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds_data/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_rds_data.client import RDSDataServiceClient

    session = get_session()
    async with session.create_client("rds-data") as client:
        client: RDSDataServiceClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    BatchExecuteStatementRequestRequestTypeDef,
    BatchExecuteStatementResponseTypeDef,
    BeginTransactionRequestRequestTypeDef,
    BeginTransactionResponseTypeDef,
    CommitTransactionRequestRequestTypeDef,
    CommitTransactionResponseTypeDef,
    ExecuteSqlRequestRequestTypeDef,
    ExecuteSqlResponseTypeDef,
    ExecuteStatementRequestRequestTypeDef,
    ExecuteStatementResponseTypeDef,
    RollbackTransactionRequestRequestTypeDef,
    RollbackTransactionResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("RDSDataServiceClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DatabaseErrorException: Type[BotocoreClientError]
    DatabaseNotFoundException: Type[BotocoreClientError]
    DatabaseUnavailableException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    HttpEndpointNotEnabledException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    InvalidSecretException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    SecretsErrorException: Type[BotocoreClientError]
    ServiceUnavailableError: Type[BotocoreClientError]
    StatementTimeoutException: Type[BotocoreClientError]
    TransactionNotFoundException: Type[BotocoreClientError]
    UnsupportedResultException: Type[BotocoreClientError]

class RDSDataServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data.html#RDSDataService.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds_data/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RDSDataServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data.html#RDSDataService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds_data/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds_data/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds_data/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds_data/client/#close)
        """

    async def batch_execute_statement(
        self, **kwargs: Unpack[BatchExecuteStatementRequestRequestTypeDef]
    ) -> BatchExecuteStatementResponseTypeDef:
        """
        Runs a batch SQL statement over an array of data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/batch_execute_statement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds_data/client/#batch_execute_statement)
        """

    async def begin_transaction(
        self, **kwargs: Unpack[BeginTransactionRequestRequestTypeDef]
    ) -> BeginTransactionResponseTypeDef:
        """
        Starts a SQL transaction.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/begin_transaction.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds_data/client/#begin_transaction)
        """

    async def commit_transaction(
        self, **kwargs: Unpack[CommitTransactionRequestRequestTypeDef]
    ) -> CommitTransactionResponseTypeDef:
        """
        Ends a SQL transaction started with the <code>BeginTransaction</code> operation
        and commits the changes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/commit_transaction.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds_data/client/#commit_transaction)
        """

    async def execute_sql(
        self, **kwargs: Unpack[ExecuteSqlRequestRequestTypeDef]
    ) -> ExecuteSqlResponseTypeDef:
        """
        Runs one or more SQL statements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/execute_sql.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds_data/client/#execute_sql)
        """

    async def execute_statement(
        self, **kwargs: Unpack[ExecuteStatementRequestRequestTypeDef]
    ) -> ExecuteStatementResponseTypeDef:
        """
        Runs a SQL statement against a database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/execute_statement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds_data/client/#execute_statement)
        """

    async def rollback_transaction(
        self, **kwargs: Unpack[RollbackTransactionRequestRequestTypeDef]
    ) -> RollbackTransactionResponseTypeDef:
        """
        Performs a rollback of a transaction.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/rollback_transaction.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds_data/client/#rollback_transaction)
        """

    async def __aenter__(self) -> "RDSDataServiceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data.html#RDSDataService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds_data/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data.html#RDSDataService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds_data/client/)
        """
