"""
Type annotations for athena service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_athena.client import AthenaClient

    session = get_session()
    async with session.create_client("athena") as client:
        client: AthenaClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    GetQueryResultsPaginator,
    ListDatabasesPaginator,
    ListDataCatalogsPaginator,
    ListNamedQueriesPaginator,
    ListQueryExecutionsPaginator,
    ListTableMetadataPaginator,
    ListTagsForResourcePaginator,
)
from .type_defs import (
    BatchGetNamedQueryInputRequestTypeDef,
    BatchGetNamedQueryOutputTypeDef,
    BatchGetPreparedStatementInputRequestTypeDef,
    BatchGetPreparedStatementOutputTypeDef,
    BatchGetQueryExecutionInputRequestTypeDef,
    BatchGetQueryExecutionOutputTypeDef,
    CancelCapacityReservationInputRequestTypeDef,
    CreateCapacityReservationInputRequestTypeDef,
    CreateDataCatalogInputRequestTypeDef,
    CreateDataCatalogOutputTypeDef,
    CreateNamedQueryInputRequestTypeDef,
    CreateNamedQueryOutputTypeDef,
    CreateNotebookInputRequestTypeDef,
    CreateNotebookOutputTypeDef,
    CreatePreparedStatementInputRequestTypeDef,
    CreatePresignedNotebookUrlRequestRequestTypeDef,
    CreatePresignedNotebookUrlResponseTypeDef,
    CreateWorkGroupInputRequestTypeDef,
    DeleteCapacityReservationInputRequestTypeDef,
    DeleteDataCatalogInputRequestTypeDef,
    DeleteDataCatalogOutputTypeDef,
    DeleteNamedQueryInputRequestTypeDef,
    DeleteNotebookInputRequestTypeDef,
    DeletePreparedStatementInputRequestTypeDef,
    DeleteWorkGroupInputRequestTypeDef,
    ExportNotebookInputRequestTypeDef,
    ExportNotebookOutputTypeDef,
    GetCalculationExecutionCodeRequestRequestTypeDef,
    GetCalculationExecutionCodeResponseTypeDef,
    GetCalculationExecutionRequestRequestTypeDef,
    GetCalculationExecutionResponseTypeDef,
    GetCalculationExecutionStatusRequestRequestTypeDef,
    GetCalculationExecutionStatusResponseTypeDef,
    GetCapacityAssignmentConfigurationInputRequestTypeDef,
    GetCapacityAssignmentConfigurationOutputTypeDef,
    GetCapacityReservationInputRequestTypeDef,
    GetCapacityReservationOutputTypeDef,
    GetDatabaseInputRequestTypeDef,
    GetDatabaseOutputTypeDef,
    GetDataCatalogInputRequestTypeDef,
    GetDataCatalogOutputTypeDef,
    GetNamedQueryInputRequestTypeDef,
    GetNamedQueryOutputTypeDef,
    GetNotebookMetadataInputRequestTypeDef,
    GetNotebookMetadataOutputTypeDef,
    GetPreparedStatementInputRequestTypeDef,
    GetPreparedStatementOutputTypeDef,
    GetQueryExecutionInputRequestTypeDef,
    GetQueryExecutionOutputTypeDef,
    GetQueryResultsInputRequestTypeDef,
    GetQueryResultsOutputTypeDef,
    GetQueryRuntimeStatisticsInputRequestTypeDef,
    GetQueryRuntimeStatisticsOutputTypeDef,
    GetSessionRequestRequestTypeDef,
    GetSessionResponseTypeDef,
    GetSessionStatusRequestRequestTypeDef,
    GetSessionStatusResponseTypeDef,
    GetTableMetadataInputRequestTypeDef,
    GetTableMetadataOutputTypeDef,
    GetWorkGroupInputRequestTypeDef,
    GetWorkGroupOutputTypeDef,
    ImportNotebookInputRequestTypeDef,
    ImportNotebookOutputTypeDef,
    ListApplicationDPUSizesInputRequestTypeDef,
    ListApplicationDPUSizesOutputTypeDef,
    ListCalculationExecutionsRequestRequestTypeDef,
    ListCalculationExecutionsResponseTypeDef,
    ListCapacityReservationsInputRequestTypeDef,
    ListCapacityReservationsOutputTypeDef,
    ListDatabasesInputRequestTypeDef,
    ListDatabasesOutputTypeDef,
    ListDataCatalogsInputRequestTypeDef,
    ListDataCatalogsOutputTypeDef,
    ListEngineVersionsInputRequestTypeDef,
    ListEngineVersionsOutputTypeDef,
    ListExecutorsRequestRequestTypeDef,
    ListExecutorsResponseTypeDef,
    ListNamedQueriesInputRequestTypeDef,
    ListNamedQueriesOutputTypeDef,
    ListNotebookMetadataInputRequestTypeDef,
    ListNotebookMetadataOutputTypeDef,
    ListNotebookSessionsRequestRequestTypeDef,
    ListNotebookSessionsResponseTypeDef,
    ListPreparedStatementsInputRequestTypeDef,
    ListPreparedStatementsOutputTypeDef,
    ListQueryExecutionsInputRequestTypeDef,
    ListQueryExecutionsOutputTypeDef,
    ListSessionsRequestRequestTypeDef,
    ListSessionsResponseTypeDef,
    ListTableMetadataInputRequestTypeDef,
    ListTableMetadataOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListWorkGroupsInputRequestTypeDef,
    ListWorkGroupsOutputTypeDef,
    PutCapacityAssignmentConfigurationInputRequestTypeDef,
    StartCalculationExecutionRequestRequestTypeDef,
    StartCalculationExecutionResponseTypeDef,
    StartQueryExecutionInputRequestTypeDef,
    StartQueryExecutionOutputTypeDef,
    StartSessionRequestRequestTypeDef,
    StartSessionResponseTypeDef,
    StopCalculationExecutionRequestRequestTypeDef,
    StopCalculationExecutionResponseTypeDef,
    StopQueryExecutionInputRequestTypeDef,
    TagResourceInputRequestTypeDef,
    TerminateSessionRequestRequestTypeDef,
    TerminateSessionResponseTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateCapacityReservationInputRequestTypeDef,
    UpdateDataCatalogInputRequestTypeDef,
    UpdateNamedQueryInputRequestTypeDef,
    UpdateNotebookInputRequestTypeDef,
    UpdateNotebookMetadataInputRequestTypeDef,
    UpdatePreparedStatementInputRequestTypeDef,
    UpdateWorkGroupInputRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("AthenaClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    MetadataException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    SessionAlreadyExistsException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class AthenaClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AthenaClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#close)
        """

    async def batch_get_named_query(
        self, **kwargs: Unpack[BatchGetNamedQueryInputRequestTypeDef]
    ) -> BatchGetNamedQueryOutputTypeDef:
        """
        Returns the details of a single named query or a list of up to 50 queries,
        which you provide as an array of query ID strings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/batch_get_named_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#batch_get_named_query)
        """

    async def batch_get_prepared_statement(
        self, **kwargs: Unpack[BatchGetPreparedStatementInputRequestTypeDef]
    ) -> BatchGetPreparedStatementOutputTypeDef:
        """
        Returns the details of a single prepared statement or a list of up to 256
        prepared statements for the array of prepared statement names that you provide.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/batch_get_prepared_statement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#batch_get_prepared_statement)
        """

    async def batch_get_query_execution(
        self, **kwargs: Unpack[BatchGetQueryExecutionInputRequestTypeDef]
    ) -> BatchGetQueryExecutionOutputTypeDef:
        """
        Returns the details of a single query execution or a list of up to 50 query
        executions, which you provide as an array of query execution ID strings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/batch_get_query_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#batch_get_query_execution)
        """

    async def cancel_capacity_reservation(
        self, **kwargs: Unpack[CancelCapacityReservationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels the capacity reservation with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/cancel_capacity_reservation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#cancel_capacity_reservation)
        """

    async def create_capacity_reservation(
        self, **kwargs: Unpack[CreateCapacityReservationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a capacity reservation with the specified name and number of requested
        data processing units.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/create_capacity_reservation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#create_capacity_reservation)
        """

    async def create_data_catalog(
        self, **kwargs: Unpack[CreateDataCatalogInputRequestTypeDef]
    ) -> CreateDataCatalogOutputTypeDef:
        """
        Creates (registers) a data catalog with the specified name and properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/create_data_catalog.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#create_data_catalog)
        """

    async def create_named_query(
        self, **kwargs: Unpack[CreateNamedQueryInputRequestTypeDef]
    ) -> CreateNamedQueryOutputTypeDef:
        """
        Creates a named query in the specified workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/create_named_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#create_named_query)
        """

    async def create_notebook(
        self, **kwargs: Unpack[CreateNotebookInputRequestTypeDef]
    ) -> CreateNotebookOutputTypeDef:
        """
        Creates an empty <code>ipynb</code> file in the specified Apache Spark enabled
        workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/create_notebook.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#create_notebook)
        """

    async def create_prepared_statement(
        self, **kwargs: Unpack[CreatePreparedStatementInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a prepared statement for use with SQL queries in Athena.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/create_prepared_statement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#create_prepared_statement)
        """

    async def create_presigned_notebook_url(
        self, **kwargs: Unpack[CreatePresignedNotebookUrlRequestRequestTypeDef]
    ) -> CreatePresignedNotebookUrlResponseTypeDef:
        """
        Gets an authentication token and the URL at which the notebook can be accessed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/create_presigned_notebook_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#create_presigned_notebook_url)
        """

    async def create_work_group(
        self, **kwargs: Unpack[CreateWorkGroupInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a workgroup with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/create_work_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#create_work_group)
        """

    async def delete_capacity_reservation(
        self, **kwargs: Unpack[DeleteCapacityReservationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a cancelled capacity reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/delete_capacity_reservation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#delete_capacity_reservation)
        """

    async def delete_data_catalog(
        self, **kwargs: Unpack[DeleteDataCatalogInputRequestTypeDef]
    ) -> DeleteDataCatalogOutputTypeDef:
        """
        Deletes a data catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/delete_data_catalog.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#delete_data_catalog)
        """

    async def delete_named_query(
        self, **kwargs: Unpack[DeleteNamedQueryInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the named query if you have access to the workgroup in which the query
        was saved.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/delete_named_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#delete_named_query)
        """

    async def delete_notebook(
        self, **kwargs: Unpack[DeleteNotebookInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified notebook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/delete_notebook.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#delete_notebook)
        """

    async def delete_prepared_statement(
        self, **kwargs: Unpack[DeletePreparedStatementInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the prepared statement with the specified name from the specified
        workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/delete_prepared_statement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#delete_prepared_statement)
        """

    async def delete_work_group(
        self, **kwargs: Unpack[DeleteWorkGroupInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the workgroup with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/delete_work_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#delete_work_group)
        """

    async def export_notebook(
        self, **kwargs: Unpack[ExportNotebookInputRequestTypeDef]
    ) -> ExportNotebookOutputTypeDef:
        """
        Exports the specified notebook and its metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/export_notebook.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#export_notebook)
        """

    async def get_calculation_execution(
        self, **kwargs: Unpack[GetCalculationExecutionRequestRequestTypeDef]
    ) -> GetCalculationExecutionResponseTypeDef:
        """
        Describes a previously submitted calculation execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_calculation_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_calculation_execution)
        """

    async def get_calculation_execution_code(
        self, **kwargs: Unpack[GetCalculationExecutionCodeRequestRequestTypeDef]
    ) -> GetCalculationExecutionCodeResponseTypeDef:
        """
        Retrieves the unencrypted code that was executed for the calculation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_calculation_execution_code.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_calculation_execution_code)
        """

    async def get_calculation_execution_status(
        self, **kwargs: Unpack[GetCalculationExecutionStatusRequestRequestTypeDef]
    ) -> GetCalculationExecutionStatusResponseTypeDef:
        """
        Gets the status of a current calculation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_calculation_execution_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_calculation_execution_status)
        """

    async def get_capacity_assignment_configuration(
        self, **kwargs: Unpack[GetCapacityAssignmentConfigurationInputRequestTypeDef]
    ) -> GetCapacityAssignmentConfigurationOutputTypeDef:
        """
        Gets the capacity assignment configuration for a capacity reservation, if one
        exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_capacity_assignment_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_capacity_assignment_configuration)
        """

    async def get_capacity_reservation(
        self, **kwargs: Unpack[GetCapacityReservationInputRequestTypeDef]
    ) -> GetCapacityReservationOutputTypeDef:
        """
        Returns information about the capacity reservation with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_capacity_reservation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_capacity_reservation)
        """

    async def get_data_catalog(
        self, **kwargs: Unpack[GetDataCatalogInputRequestTypeDef]
    ) -> GetDataCatalogOutputTypeDef:
        """
        Returns the specified data catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_data_catalog.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_data_catalog)
        """

    async def get_database(
        self, **kwargs: Unpack[GetDatabaseInputRequestTypeDef]
    ) -> GetDatabaseOutputTypeDef:
        """
        Returns a database object for the specified database and data catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_database.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_database)
        """

    async def get_named_query(
        self, **kwargs: Unpack[GetNamedQueryInputRequestTypeDef]
    ) -> GetNamedQueryOutputTypeDef:
        """
        Returns information about a single query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_named_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_named_query)
        """

    async def get_notebook_metadata(
        self, **kwargs: Unpack[GetNotebookMetadataInputRequestTypeDef]
    ) -> GetNotebookMetadataOutputTypeDef:
        """
        Retrieves notebook metadata for the specified notebook ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_notebook_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_notebook_metadata)
        """

    async def get_prepared_statement(
        self, **kwargs: Unpack[GetPreparedStatementInputRequestTypeDef]
    ) -> GetPreparedStatementOutputTypeDef:
        """
        Retrieves the prepared statement with the specified name from the specified
        workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_prepared_statement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_prepared_statement)
        """

    async def get_query_execution(
        self, **kwargs: Unpack[GetQueryExecutionInputRequestTypeDef]
    ) -> GetQueryExecutionOutputTypeDef:
        """
        Returns information about a single execution of a query if you have access to
        the workgroup in which the query ran.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_query_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_query_execution)
        """

    async def get_query_results(
        self, **kwargs: Unpack[GetQueryResultsInputRequestTypeDef]
    ) -> GetQueryResultsOutputTypeDef:
        """
        Streams the results of a single query execution specified by
        <code>QueryExecutionId</code> from the Athena query results location in Amazon
        S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_query_results.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_query_results)
        """

    async def get_query_runtime_statistics(
        self, **kwargs: Unpack[GetQueryRuntimeStatisticsInputRequestTypeDef]
    ) -> GetQueryRuntimeStatisticsOutputTypeDef:
        """
        Returns query execution runtime statistics related to a single execution of a
        query if you have access to the workgroup in which the query ran.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_query_runtime_statistics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_query_runtime_statistics)
        """

    async def get_session(
        self, **kwargs: Unpack[GetSessionRequestRequestTypeDef]
    ) -> GetSessionResponseTypeDef:
        """
        Gets the full details of a previously created session, including the session
        status and configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_session)
        """

    async def get_session_status(
        self, **kwargs: Unpack[GetSessionStatusRequestRequestTypeDef]
    ) -> GetSessionStatusResponseTypeDef:
        """
        Gets the current status of a session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_session_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_session_status)
        """

    async def get_table_metadata(
        self, **kwargs: Unpack[GetTableMetadataInputRequestTypeDef]
    ) -> GetTableMetadataOutputTypeDef:
        """
        Returns table metadata for the specified catalog, database, and table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_table_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_table_metadata)
        """

    async def get_work_group(
        self, **kwargs: Unpack[GetWorkGroupInputRequestTypeDef]
    ) -> GetWorkGroupOutputTypeDef:
        """
        Returns information about the workgroup with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_work_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_work_group)
        """

    async def import_notebook(
        self, **kwargs: Unpack[ImportNotebookInputRequestTypeDef]
    ) -> ImportNotebookOutputTypeDef:
        """
        Imports a single <code>ipynb</code> file to a Spark enabled workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/import_notebook.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#import_notebook)
        """

    async def list_application_dpu_sizes(
        self, **kwargs: Unpack[ListApplicationDPUSizesInputRequestTypeDef]
    ) -> ListApplicationDPUSizesOutputTypeDef:
        """
        Returns the supported DPU sizes for the supported application runtimes (for
        example, <code>Athena notebook version 1</code>).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/list_application_dpu_sizes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#list_application_dpu_sizes)
        """

    async def list_calculation_executions(
        self, **kwargs: Unpack[ListCalculationExecutionsRequestRequestTypeDef]
    ) -> ListCalculationExecutionsResponseTypeDef:
        """
        Lists the calculations that have been submitted to a session in descending
        order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/list_calculation_executions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#list_calculation_executions)
        """

    async def list_capacity_reservations(
        self, **kwargs: Unpack[ListCapacityReservationsInputRequestTypeDef]
    ) -> ListCapacityReservationsOutputTypeDef:
        """
        Lists the capacity reservations for the current account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/list_capacity_reservations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#list_capacity_reservations)
        """

    async def list_data_catalogs(
        self, **kwargs: Unpack[ListDataCatalogsInputRequestTypeDef]
    ) -> ListDataCatalogsOutputTypeDef:
        """
        Lists the data catalogs in the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/list_data_catalogs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#list_data_catalogs)
        """

    async def list_databases(
        self, **kwargs: Unpack[ListDatabasesInputRequestTypeDef]
    ) -> ListDatabasesOutputTypeDef:
        """
        Lists the databases in the specified data catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/list_databases.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#list_databases)
        """

    async def list_engine_versions(
        self, **kwargs: Unpack[ListEngineVersionsInputRequestTypeDef]
    ) -> ListEngineVersionsOutputTypeDef:
        """
        Returns a list of engine versions that are available to choose from, including
        the Auto option.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/list_engine_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#list_engine_versions)
        """

    async def list_executors(
        self, **kwargs: Unpack[ListExecutorsRequestRequestTypeDef]
    ) -> ListExecutorsResponseTypeDef:
        """
        Lists, in descending order, the executors that joined a session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/list_executors.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#list_executors)
        """

    async def list_named_queries(
        self, **kwargs: Unpack[ListNamedQueriesInputRequestTypeDef]
    ) -> ListNamedQueriesOutputTypeDef:
        """
        Provides a list of available query IDs only for queries saved in the specified
        workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/list_named_queries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#list_named_queries)
        """

    async def list_notebook_metadata(
        self, **kwargs: Unpack[ListNotebookMetadataInputRequestTypeDef]
    ) -> ListNotebookMetadataOutputTypeDef:
        """
        Displays the notebook files for the specified workgroup in paginated format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/list_notebook_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#list_notebook_metadata)
        """

    async def list_notebook_sessions(
        self, **kwargs: Unpack[ListNotebookSessionsRequestRequestTypeDef]
    ) -> ListNotebookSessionsResponseTypeDef:
        """
        Lists, in descending order, the sessions that have been created in a notebook
        that are in an active state like <code>CREATING</code>, <code>CREATED</code>,
        <code>IDLE</code> or <code>BUSY</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/list_notebook_sessions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#list_notebook_sessions)
        """

    async def list_prepared_statements(
        self, **kwargs: Unpack[ListPreparedStatementsInputRequestTypeDef]
    ) -> ListPreparedStatementsOutputTypeDef:
        """
        Lists the prepared statements in the specified workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/list_prepared_statements.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#list_prepared_statements)
        """

    async def list_query_executions(
        self, **kwargs: Unpack[ListQueryExecutionsInputRequestTypeDef]
    ) -> ListQueryExecutionsOutputTypeDef:
        """
        Provides a list of available query execution IDs for the queries in the
        specified workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/list_query_executions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#list_query_executions)
        """

    async def list_sessions(
        self, **kwargs: Unpack[ListSessionsRequestRequestTypeDef]
    ) -> ListSessionsResponseTypeDef:
        """
        Lists the sessions in a workgroup that are in an active state like
        <code>CREATING</code>, <code>CREATED</code>, <code>IDLE</code>, or
        <code>BUSY</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/list_sessions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#list_sessions)
        """

    async def list_table_metadata(
        self, **kwargs: Unpack[ListTableMetadataInputRequestTypeDef]
    ) -> ListTableMetadataOutputTypeDef:
        """
        Lists the metadata for the tables in the specified data catalog database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/list_table_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#list_table_metadata)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags associated with an Athena resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#list_tags_for_resource)
        """

    async def list_work_groups(
        self, **kwargs: Unpack[ListWorkGroupsInputRequestTypeDef]
    ) -> ListWorkGroupsOutputTypeDef:
        """
        Lists available workgroups for the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/list_work_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#list_work_groups)
        """

    async def put_capacity_assignment_configuration(
        self, **kwargs: Unpack[PutCapacityAssignmentConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Puts a new capacity assignment configuration for a specified capacity
        reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/put_capacity_assignment_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#put_capacity_assignment_configuration)
        """

    async def start_calculation_execution(
        self, **kwargs: Unpack[StartCalculationExecutionRequestRequestTypeDef]
    ) -> StartCalculationExecutionResponseTypeDef:
        """
        Submits calculations for execution within a session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/start_calculation_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#start_calculation_execution)
        """

    async def start_query_execution(
        self, **kwargs: Unpack[StartQueryExecutionInputRequestTypeDef]
    ) -> StartQueryExecutionOutputTypeDef:
        """
        Runs the SQL query statements contained in the <code>Query</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/start_query_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#start_query_execution)
        """

    async def start_session(
        self, **kwargs: Unpack[StartSessionRequestRequestTypeDef]
    ) -> StartSessionResponseTypeDef:
        """
        Creates a session for running calculations within a workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/start_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#start_session)
        """

    async def stop_calculation_execution(
        self, **kwargs: Unpack[StopCalculationExecutionRequestRequestTypeDef]
    ) -> StopCalculationExecutionResponseTypeDef:
        """
        Requests the cancellation of a calculation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/stop_calculation_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#stop_calculation_execution)
        """

    async def stop_query_execution(
        self, **kwargs: Unpack[StopQueryExecutionInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops a query execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/stop_query_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#stop_query_execution)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds one or more tags to an Athena resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#tag_resource)
        """

    async def terminate_session(
        self, **kwargs: Unpack[TerminateSessionRequestRequestTypeDef]
    ) -> TerminateSessionResponseTypeDef:
        """
        Terminates an active session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/terminate_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#terminate_session)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from an Athena resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#untag_resource)
        """

    async def update_capacity_reservation(
        self, **kwargs: Unpack[UpdateCapacityReservationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the number of requested data processing units for the capacity
        reservation with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/update_capacity_reservation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#update_capacity_reservation)
        """

    async def update_data_catalog(
        self, **kwargs: Unpack[UpdateDataCatalogInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the data catalog that has the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/update_data_catalog.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#update_data_catalog)
        """

    async def update_named_query(
        self, **kwargs: Unpack[UpdateNamedQueryInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a <a>NamedQuery</a> object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/update_named_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#update_named_query)
        """

    async def update_notebook(
        self, **kwargs: Unpack[UpdateNotebookInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the contents of a Spark notebook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/update_notebook.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#update_notebook)
        """

    async def update_notebook_metadata(
        self, **kwargs: Unpack[UpdateNotebookMetadataInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the metadata for a notebook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/update_notebook_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#update_notebook_metadata)
        """

    async def update_prepared_statement(
        self, **kwargs: Unpack[UpdatePreparedStatementInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a prepared statement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/update_prepared_statement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#update_prepared_statement)
        """

    async def update_work_group(
        self, **kwargs: Unpack[UpdateWorkGroupInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the workgroup with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/update_work_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#update_work_group)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_query_results"]
    ) -> GetQueryResultsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_catalogs"]
    ) -> ListDataCatalogsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_databases"]) -> ListDatabasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_named_queries"]
    ) -> ListNamedQueriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_query_executions"]
    ) -> ListQueryExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_table_metadata"]
    ) -> ListTableMetadataPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/#get_paginator)
        """

    async def __aenter__(self) -> "AthenaClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_athena/client/)
        """
