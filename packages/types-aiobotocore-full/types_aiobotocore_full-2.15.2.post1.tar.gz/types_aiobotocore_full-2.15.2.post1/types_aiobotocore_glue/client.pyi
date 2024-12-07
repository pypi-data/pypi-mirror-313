"""
Type annotations for glue service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_glue.client import GlueClient

    session = get_session()
    async with session.create_client("glue") as client:
        client: GlueClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    GetClassifiersPaginator,
    GetConnectionsPaginator,
    GetCrawlerMetricsPaginator,
    GetCrawlersPaginator,
    GetDatabasesPaginator,
    GetDevEndpointsPaginator,
    GetJobRunsPaginator,
    GetJobsPaginator,
    GetPartitionIndexesPaginator,
    GetPartitionsPaginator,
    GetResourcePoliciesPaginator,
    GetSecurityConfigurationsPaginator,
    GetTablesPaginator,
    GetTableVersionsPaginator,
    GetTriggersPaginator,
    GetUserDefinedFunctionsPaginator,
    GetWorkflowRunsPaginator,
    ListBlueprintsPaginator,
    ListJobsPaginator,
    ListRegistriesPaginator,
    ListSchemasPaginator,
    ListSchemaVersionsPaginator,
    ListTableOptimizerRunsPaginator,
    ListTriggersPaginator,
    ListUsageProfilesPaginator,
    ListWorkflowsPaginator,
)
from .type_defs import (
    BatchCreatePartitionRequestRequestTypeDef,
    BatchCreatePartitionResponseTypeDef,
    BatchDeleteConnectionRequestRequestTypeDef,
    BatchDeleteConnectionResponseTypeDef,
    BatchDeletePartitionRequestRequestTypeDef,
    BatchDeletePartitionResponseTypeDef,
    BatchDeleteTableRequestRequestTypeDef,
    BatchDeleteTableResponseTypeDef,
    BatchDeleteTableVersionRequestRequestTypeDef,
    BatchDeleteTableVersionResponseTypeDef,
    BatchGetBlueprintsRequestRequestTypeDef,
    BatchGetBlueprintsResponseTypeDef,
    BatchGetCrawlersRequestRequestTypeDef,
    BatchGetCrawlersResponseTypeDef,
    BatchGetCustomEntityTypesRequestRequestTypeDef,
    BatchGetCustomEntityTypesResponseTypeDef,
    BatchGetDataQualityResultRequestRequestTypeDef,
    BatchGetDataQualityResultResponseTypeDef,
    BatchGetDevEndpointsRequestRequestTypeDef,
    BatchGetDevEndpointsResponseTypeDef,
    BatchGetJobsRequestRequestTypeDef,
    BatchGetJobsResponseTypeDef,
    BatchGetPartitionRequestRequestTypeDef,
    BatchGetPartitionResponseTypeDef,
    BatchGetTableOptimizerRequestRequestTypeDef,
    BatchGetTableOptimizerResponseTypeDef,
    BatchGetTriggersRequestRequestTypeDef,
    BatchGetTriggersResponseTypeDef,
    BatchGetWorkflowsRequestRequestTypeDef,
    BatchGetWorkflowsResponseTypeDef,
    BatchPutDataQualityStatisticAnnotationRequestRequestTypeDef,
    BatchPutDataQualityStatisticAnnotationResponseTypeDef,
    BatchStopJobRunRequestRequestTypeDef,
    BatchStopJobRunResponseTypeDef,
    BatchUpdatePartitionRequestRequestTypeDef,
    BatchUpdatePartitionResponseTypeDef,
    CancelDataQualityRuleRecommendationRunRequestRequestTypeDef,
    CancelDataQualityRulesetEvaluationRunRequestRequestTypeDef,
    CancelMLTaskRunRequestRequestTypeDef,
    CancelMLTaskRunResponseTypeDef,
    CancelStatementRequestRequestTypeDef,
    CheckSchemaVersionValidityInputRequestTypeDef,
    CheckSchemaVersionValidityResponseTypeDef,
    CreateBlueprintRequestRequestTypeDef,
    CreateBlueprintResponseTypeDef,
    CreateClassifierRequestRequestTypeDef,
    CreateConnectionRequestRequestTypeDef,
    CreateConnectionResponseTypeDef,
    CreateCrawlerRequestRequestTypeDef,
    CreateCustomEntityTypeRequestRequestTypeDef,
    CreateCustomEntityTypeResponseTypeDef,
    CreateDatabaseRequestRequestTypeDef,
    CreateDataQualityRulesetRequestRequestTypeDef,
    CreateDataQualityRulesetResponseTypeDef,
    CreateDevEndpointRequestRequestTypeDef,
    CreateDevEndpointResponseTypeDef,
    CreateJobRequestRequestTypeDef,
    CreateJobResponseTypeDef,
    CreateMLTransformRequestRequestTypeDef,
    CreateMLTransformResponseTypeDef,
    CreatePartitionIndexRequestRequestTypeDef,
    CreatePartitionRequestRequestTypeDef,
    CreateRegistryInputRequestTypeDef,
    CreateRegistryResponseTypeDef,
    CreateSchemaInputRequestTypeDef,
    CreateSchemaResponseTypeDef,
    CreateScriptRequestRequestTypeDef,
    CreateScriptResponseTypeDef,
    CreateSecurityConfigurationRequestRequestTypeDef,
    CreateSecurityConfigurationResponseTypeDef,
    CreateSessionRequestRequestTypeDef,
    CreateSessionResponseTypeDef,
    CreateTableOptimizerRequestRequestTypeDef,
    CreateTableRequestRequestTypeDef,
    CreateTriggerRequestRequestTypeDef,
    CreateTriggerResponseTypeDef,
    CreateUsageProfileRequestRequestTypeDef,
    CreateUsageProfileResponseTypeDef,
    CreateUserDefinedFunctionRequestRequestTypeDef,
    CreateWorkflowRequestRequestTypeDef,
    CreateWorkflowResponseTypeDef,
    DeleteBlueprintRequestRequestTypeDef,
    DeleteBlueprintResponseTypeDef,
    DeleteClassifierRequestRequestTypeDef,
    DeleteColumnStatisticsForPartitionRequestRequestTypeDef,
    DeleteColumnStatisticsForTableRequestRequestTypeDef,
    DeleteConnectionRequestRequestTypeDef,
    DeleteCrawlerRequestRequestTypeDef,
    DeleteCustomEntityTypeRequestRequestTypeDef,
    DeleteCustomEntityTypeResponseTypeDef,
    DeleteDatabaseRequestRequestTypeDef,
    DeleteDataQualityRulesetRequestRequestTypeDef,
    DeleteDevEndpointRequestRequestTypeDef,
    DeleteJobRequestRequestTypeDef,
    DeleteJobResponseTypeDef,
    DeleteMLTransformRequestRequestTypeDef,
    DeleteMLTransformResponseTypeDef,
    DeletePartitionIndexRequestRequestTypeDef,
    DeletePartitionRequestRequestTypeDef,
    DeleteRegistryInputRequestTypeDef,
    DeleteRegistryResponseTypeDef,
    DeleteResourcePolicyRequestRequestTypeDef,
    DeleteSchemaInputRequestTypeDef,
    DeleteSchemaResponseTypeDef,
    DeleteSchemaVersionsInputRequestTypeDef,
    DeleteSchemaVersionsResponseTypeDef,
    DeleteSecurityConfigurationRequestRequestTypeDef,
    DeleteSessionRequestRequestTypeDef,
    DeleteSessionResponseTypeDef,
    DeleteTableOptimizerRequestRequestTypeDef,
    DeleteTableRequestRequestTypeDef,
    DeleteTableVersionRequestRequestTypeDef,
    DeleteTriggerRequestRequestTypeDef,
    DeleteTriggerResponseTypeDef,
    DeleteUsageProfileRequestRequestTypeDef,
    DeleteUserDefinedFunctionRequestRequestTypeDef,
    DeleteWorkflowRequestRequestTypeDef,
    DeleteWorkflowResponseTypeDef,
    GetBlueprintRequestRequestTypeDef,
    GetBlueprintResponseTypeDef,
    GetBlueprintRunRequestRequestTypeDef,
    GetBlueprintRunResponseTypeDef,
    GetBlueprintRunsRequestRequestTypeDef,
    GetBlueprintRunsResponseTypeDef,
    GetCatalogImportStatusRequestRequestTypeDef,
    GetCatalogImportStatusResponseTypeDef,
    GetClassifierRequestRequestTypeDef,
    GetClassifierResponseTypeDef,
    GetClassifiersRequestRequestTypeDef,
    GetClassifiersResponseTypeDef,
    GetColumnStatisticsForPartitionRequestRequestTypeDef,
    GetColumnStatisticsForPartitionResponseTypeDef,
    GetColumnStatisticsForTableRequestRequestTypeDef,
    GetColumnStatisticsForTableResponseTypeDef,
    GetColumnStatisticsTaskRunRequestRequestTypeDef,
    GetColumnStatisticsTaskRunResponseTypeDef,
    GetColumnStatisticsTaskRunsRequestRequestTypeDef,
    GetColumnStatisticsTaskRunsResponseTypeDef,
    GetConnectionRequestRequestTypeDef,
    GetConnectionResponseTypeDef,
    GetConnectionsRequestRequestTypeDef,
    GetConnectionsResponseTypeDef,
    GetCrawlerMetricsRequestRequestTypeDef,
    GetCrawlerMetricsResponseTypeDef,
    GetCrawlerRequestRequestTypeDef,
    GetCrawlerResponseTypeDef,
    GetCrawlersRequestRequestTypeDef,
    GetCrawlersResponseTypeDef,
    GetCustomEntityTypeRequestRequestTypeDef,
    GetCustomEntityTypeResponseTypeDef,
    GetDatabaseRequestRequestTypeDef,
    GetDatabaseResponseTypeDef,
    GetDatabasesRequestRequestTypeDef,
    GetDatabasesResponseTypeDef,
    GetDataCatalogEncryptionSettingsRequestRequestTypeDef,
    GetDataCatalogEncryptionSettingsResponseTypeDef,
    GetDataflowGraphRequestRequestTypeDef,
    GetDataflowGraphResponseTypeDef,
    GetDataQualityModelRequestRequestTypeDef,
    GetDataQualityModelResponseTypeDef,
    GetDataQualityModelResultRequestRequestTypeDef,
    GetDataQualityModelResultResponseTypeDef,
    GetDataQualityResultRequestRequestTypeDef,
    GetDataQualityResultResponseTypeDef,
    GetDataQualityRuleRecommendationRunRequestRequestTypeDef,
    GetDataQualityRuleRecommendationRunResponseTypeDef,
    GetDataQualityRulesetEvaluationRunRequestRequestTypeDef,
    GetDataQualityRulesetEvaluationRunResponseTypeDef,
    GetDataQualityRulesetRequestRequestTypeDef,
    GetDataQualityRulesetResponseTypeDef,
    GetDevEndpointRequestRequestTypeDef,
    GetDevEndpointResponseTypeDef,
    GetDevEndpointsRequestRequestTypeDef,
    GetDevEndpointsResponseTypeDef,
    GetJobBookmarkRequestRequestTypeDef,
    GetJobBookmarkResponseTypeDef,
    GetJobRequestRequestTypeDef,
    GetJobResponseTypeDef,
    GetJobRunRequestRequestTypeDef,
    GetJobRunResponseTypeDef,
    GetJobRunsRequestRequestTypeDef,
    GetJobRunsResponseTypeDef,
    GetJobsRequestRequestTypeDef,
    GetJobsResponseTypeDef,
    GetMappingRequestRequestTypeDef,
    GetMappingResponseTypeDef,
    GetMLTaskRunRequestRequestTypeDef,
    GetMLTaskRunResponseTypeDef,
    GetMLTaskRunsRequestRequestTypeDef,
    GetMLTaskRunsResponseTypeDef,
    GetMLTransformRequestRequestTypeDef,
    GetMLTransformResponseTypeDef,
    GetMLTransformsRequestRequestTypeDef,
    GetMLTransformsResponseTypeDef,
    GetPartitionIndexesRequestRequestTypeDef,
    GetPartitionIndexesResponseTypeDef,
    GetPartitionRequestRequestTypeDef,
    GetPartitionResponseTypeDef,
    GetPartitionsRequestRequestTypeDef,
    GetPartitionsResponseTypeDef,
    GetPlanRequestRequestTypeDef,
    GetPlanResponseTypeDef,
    GetRegistryInputRequestTypeDef,
    GetRegistryResponseTypeDef,
    GetResourcePoliciesRequestRequestTypeDef,
    GetResourcePoliciesResponseTypeDef,
    GetResourcePolicyRequestRequestTypeDef,
    GetResourcePolicyResponseTypeDef,
    GetSchemaByDefinitionInputRequestTypeDef,
    GetSchemaByDefinitionResponseTypeDef,
    GetSchemaInputRequestTypeDef,
    GetSchemaResponseTypeDef,
    GetSchemaVersionInputRequestTypeDef,
    GetSchemaVersionResponseTypeDef,
    GetSchemaVersionsDiffInputRequestTypeDef,
    GetSchemaVersionsDiffResponseTypeDef,
    GetSecurityConfigurationRequestRequestTypeDef,
    GetSecurityConfigurationResponseTypeDef,
    GetSecurityConfigurationsRequestRequestTypeDef,
    GetSecurityConfigurationsResponseTypeDef,
    GetSessionRequestRequestTypeDef,
    GetSessionResponseTypeDef,
    GetStatementRequestRequestTypeDef,
    GetStatementResponseTypeDef,
    GetTableOptimizerRequestRequestTypeDef,
    GetTableOptimizerResponseTypeDef,
    GetTableRequestRequestTypeDef,
    GetTableResponseTypeDef,
    GetTablesRequestRequestTypeDef,
    GetTablesResponseTypeDef,
    GetTableVersionRequestRequestTypeDef,
    GetTableVersionResponseTypeDef,
    GetTableVersionsRequestRequestTypeDef,
    GetTableVersionsResponseTypeDef,
    GetTagsRequestRequestTypeDef,
    GetTagsResponseTypeDef,
    GetTriggerRequestRequestTypeDef,
    GetTriggerResponseTypeDef,
    GetTriggersRequestRequestTypeDef,
    GetTriggersResponseTypeDef,
    GetUnfilteredPartitionMetadataRequestRequestTypeDef,
    GetUnfilteredPartitionMetadataResponseTypeDef,
    GetUnfilteredPartitionsMetadataRequestRequestTypeDef,
    GetUnfilteredPartitionsMetadataResponseTypeDef,
    GetUnfilteredTableMetadataRequestRequestTypeDef,
    GetUnfilteredTableMetadataResponseTypeDef,
    GetUsageProfileRequestRequestTypeDef,
    GetUsageProfileResponseTypeDef,
    GetUserDefinedFunctionRequestRequestTypeDef,
    GetUserDefinedFunctionResponseTypeDef,
    GetUserDefinedFunctionsRequestRequestTypeDef,
    GetUserDefinedFunctionsResponseTypeDef,
    GetWorkflowRequestRequestTypeDef,
    GetWorkflowResponseTypeDef,
    GetWorkflowRunPropertiesRequestRequestTypeDef,
    GetWorkflowRunPropertiesResponseTypeDef,
    GetWorkflowRunRequestRequestTypeDef,
    GetWorkflowRunResponseTypeDef,
    GetWorkflowRunsRequestRequestTypeDef,
    GetWorkflowRunsResponseTypeDef,
    ImportCatalogToGlueRequestRequestTypeDef,
    ListBlueprintsRequestRequestTypeDef,
    ListBlueprintsResponseTypeDef,
    ListColumnStatisticsTaskRunsRequestRequestTypeDef,
    ListColumnStatisticsTaskRunsResponseTypeDef,
    ListCrawlersRequestRequestTypeDef,
    ListCrawlersResponseTypeDef,
    ListCrawlsRequestRequestTypeDef,
    ListCrawlsResponseTypeDef,
    ListCustomEntityTypesRequestRequestTypeDef,
    ListCustomEntityTypesResponseTypeDef,
    ListDataQualityResultsRequestRequestTypeDef,
    ListDataQualityResultsResponseTypeDef,
    ListDataQualityRuleRecommendationRunsRequestRequestTypeDef,
    ListDataQualityRuleRecommendationRunsResponseTypeDef,
    ListDataQualityRulesetEvaluationRunsRequestRequestTypeDef,
    ListDataQualityRulesetEvaluationRunsResponseTypeDef,
    ListDataQualityRulesetsRequestRequestTypeDef,
    ListDataQualityRulesetsResponseTypeDef,
    ListDataQualityStatisticAnnotationsRequestRequestTypeDef,
    ListDataQualityStatisticAnnotationsResponseTypeDef,
    ListDataQualityStatisticsRequestRequestTypeDef,
    ListDataQualityStatisticsResponseTypeDef,
    ListDevEndpointsRequestRequestTypeDef,
    ListDevEndpointsResponseTypeDef,
    ListJobsRequestRequestTypeDef,
    ListJobsResponseTypeDef,
    ListMLTransformsRequestRequestTypeDef,
    ListMLTransformsResponseTypeDef,
    ListRegistriesInputRequestTypeDef,
    ListRegistriesResponseTypeDef,
    ListSchemasInputRequestTypeDef,
    ListSchemasResponseTypeDef,
    ListSchemaVersionsInputRequestTypeDef,
    ListSchemaVersionsResponseTypeDef,
    ListSessionsRequestRequestTypeDef,
    ListSessionsResponseTypeDef,
    ListStatementsRequestRequestTypeDef,
    ListStatementsResponseTypeDef,
    ListTableOptimizerRunsRequestRequestTypeDef,
    ListTableOptimizerRunsResponseTypeDef,
    ListTriggersRequestRequestTypeDef,
    ListTriggersResponseTypeDef,
    ListUsageProfilesRequestRequestTypeDef,
    ListUsageProfilesResponseTypeDef,
    ListWorkflowsRequestRequestTypeDef,
    ListWorkflowsResponseTypeDef,
    PutDataCatalogEncryptionSettingsRequestRequestTypeDef,
    PutDataQualityProfileAnnotationRequestRequestTypeDef,
    PutResourcePolicyRequestRequestTypeDef,
    PutResourcePolicyResponseTypeDef,
    PutSchemaVersionMetadataInputRequestTypeDef,
    PutSchemaVersionMetadataResponseTypeDef,
    PutWorkflowRunPropertiesRequestRequestTypeDef,
    QuerySchemaVersionMetadataInputRequestTypeDef,
    QuerySchemaVersionMetadataResponseTypeDef,
    RegisterSchemaVersionInputRequestTypeDef,
    RegisterSchemaVersionResponseTypeDef,
    RemoveSchemaVersionMetadataInputRequestTypeDef,
    RemoveSchemaVersionMetadataResponseTypeDef,
    ResetJobBookmarkRequestRequestTypeDef,
    ResetJobBookmarkResponseTypeDef,
    ResumeWorkflowRunRequestRequestTypeDef,
    ResumeWorkflowRunResponseTypeDef,
    RunStatementRequestRequestTypeDef,
    RunStatementResponseTypeDef,
    SearchTablesRequestRequestTypeDef,
    SearchTablesResponseTypeDef,
    StartBlueprintRunRequestRequestTypeDef,
    StartBlueprintRunResponseTypeDef,
    StartColumnStatisticsTaskRunRequestRequestTypeDef,
    StartColumnStatisticsTaskRunResponseTypeDef,
    StartCrawlerRequestRequestTypeDef,
    StartCrawlerScheduleRequestRequestTypeDef,
    StartDataQualityRuleRecommendationRunRequestRequestTypeDef,
    StartDataQualityRuleRecommendationRunResponseTypeDef,
    StartDataQualityRulesetEvaluationRunRequestRequestTypeDef,
    StartDataQualityRulesetEvaluationRunResponseTypeDef,
    StartExportLabelsTaskRunRequestRequestTypeDef,
    StartExportLabelsTaskRunResponseTypeDef,
    StartImportLabelsTaskRunRequestRequestTypeDef,
    StartImportLabelsTaskRunResponseTypeDef,
    StartJobRunRequestRequestTypeDef,
    StartJobRunResponseTypeDef,
    StartMLEvaluationTaskRunRequestRequestTypeDef,
    StartMLEvaluationTaskRunResponseTypeDef,
    StartMLLabelingSetGenerationTaskRunRequestRequestTypeDef,
    StartMLLabelingSetGenerationTaskRunResponseTypeDef,
    StartTriggerRequestRequestTypeDef,
    StartTriggerResponseTypeDef,
    StartWorkflowRunRequestRequestTypeDef,
    StartWorkflowRunResponseTypeDef,
    StopColumnStatisticsTaskRunRequestRequestTypeDef,
    StopCrawlerRequestRequestTypeDef,
    StopCrawlerScheduleRequestRequestTypeDef,
    StopSessionRequestRequestTypeDef,
    StopSessionResponseTypeDef,
    StopTriggerRequestRequestTypeDef,
    StopTriggerResponseTypeDef,
    StopWorkflowRunRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    TestConnectionRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateBlueprintRequestRequestTypeDef,
    UpdateBlueprintResponseTypeDef,
    UpdateClassifierRequestRequestTypeDef,
    UpdateColumnStatisticsForPartitionRequestRequestTypeDef,
    UpdateColumnStatisticsForPartitionResponseTypeDef,
    UpdateColumnStatisticsForTableRequestRequestTypeDef,
    UpdateColumnStatisticsForTableResponseTypeDef,
    UpdateConnectionRequestRequestTypeDef,
    UpdateCrawlerRequestRequestTypeDef,
    UpdateCrawlerScheduleRequestRequestTypeDef,
    UpdateDatabaseRequestRequestTypeDef,
    UpdateDataQualityRulesetRequestRequestTypeDef,
    UpdateDataQualityRulesetResponseTypeDef,
    UpdateDevEndpointRequestRequestTypeDef,
    UpdateJobFromSourceControlRequestRequestTypeDef,
    UpdateJobFromSourceControlResponseTypeDef,
    UpdateJobRequestRequestTypeDef,
    UpdateJobResponseTypeDef,
    UpdateMLTransformRequestRequestTypeDef,
    UpdateMLTransformResponseTypeDef,
    UpdatePartitionRequestRequestTypeDef,
    UpdateRegistryInputRequestTypeDef,
    UpdateRegistryResponseTypeDef,
    UpdateSchemaInputRequestTypeDef,
    UpdateSchemaResponseTypeDef,
    UpdateSourceControlFromJobRequestRequestTypeDef,
    UpdateSourceControlFromJobResponseTypeDef,
    UpdateTableOptimizerRequestRequestTypeDef,
    UpdateTableRequestRequestTypeDef,
    UpdateTriggerRequestRequestTypeDef,
    UpdateTriggerResponseTypeDef,
    UpdateUsageProfileRequestRequestTypeDef,
    UpdateUsageProfileResponseTypeDef,
    UpdateUserDefinedFunctionRequestRequestTypeDef,
    UpdateWorkflowRequestRequestTypeDef,
    UpdateWorkflowResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("GlueClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AlreadyExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ColumnStatisticsTaskNotRunningException: Type[BotocoreClientError]
    ColumnStatisticsTaskRunningException: Type[BotocoreClientError]
    ColumnStatisticsTaskStoppingException: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConcurrentRunsExceededException: Type[BotocoreClientError]
    ConditionCheckFailureException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    CrawlerNotRunningException: Type[BotocoreClientError]
    CrawlerRunningException: Type[BotocoreClientError]
    CrawlerStoppingException: Type[BotocoreClientError]
    EntityNotFoundException: Type[BotocoreClientError]
    FederatedResourceAlreadyExistsException: Type[BotocoreClientError]
    FederationSourceException: Type[BotocoreClientError]
    FederationSourceRetryableException: Type[BotocoreClientError]
    GlueEncryptionException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    IllegalBlueprintStateException: Type[BotocoreClientError]
    IllegalSessionStateException: Type[BotocoreClientError]
    IllegalWorkflowStateException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    MLTransformNotReadyException: Type[BotocoreClientError]
    NoScheduleException: Type[BotocoreClientError]
    OperationNotSupportedException: Type[BotocoreClientError]
    OperationTimeoutException: Type[BotocoreClientError]
    PermissionTypeMismatchException: Type[BotocoreClientError]
    ResourceNotReadyException: Type[BotocoreClientError]
    ResourceNumberLimitExceededException: Type[BotocoreClientError]
    SchedulerNotRunningException: Type[BotocoreClientError]
    SchedulerRunningException: Type[BotocoreClientError]
    SchedulerTransitioningException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]
    VersionMismatchException: Type[BotocoreClientError]

class GlueClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GlueClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#close)
        """

    async def batch_create_partition(
        self, **kwargs: Unpack[BatchCreatePartitionRequestRequestTypeDef]
    ) -> BatchCreatePartitionResponseTypeDef:
        """
        Creates one or more partitions in a batch operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_create_partition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_create_partition)
        """

    async def batch_delete_connection(
        self, **kwargs: Unpack[BatchDeleteConnectionRequestRequestTypeDef]
    ) -> BatchDeleteConnectionResponseTypeDef:
        """
        Deletes a list of connection definitions from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_delete_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_delete_connection)
        """

    async def batch_delete_partition(
        self, **kwargs: Unpack[BatchDeletePartitionRequestRequestTypeDef]
    ) -> BatchDeletePartitionResponseTypeDef:
        """
        Deletes one or more partitions in a batch operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_delete_partition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_delete_partition)
        """

    async def batch_delete_table(
        self, **kwargs: Unpack[BatchDeleteTableRequestRequestTypeDef]
    ) -> BatchDeleteTableResponseTypeDef:
        """
        Deletes multiple tables at once.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_delete_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_delete_table)
        """

    async def batch_delete_table_version(
        self, **kwargs: Unpack[BatchDeleteTableVersionRequestRequestTypeDef]
    ) -> BatchDeleteTableVersionResponseTypeDef:
        """
        Deletes a specified batch of versions of a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_delete_table_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_delete_table_version)
        """

    async def batch_get_blueprints(
        self, **kwargs: Unpack[BatchGetBlueprintsRequestRequestTypeDef]
    ) -> BatchGetBlueprintsResponseTypeDef:
        """
        Retrieves information about a list of blueprints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_get_blueprints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_blueprints)
        """

    async def batch_get_crawlers(
        self, **kwargs: Unpack[BatchGetCrawlersRequestRequestTypeDef]
    ) -> BatchGetCrawlersResponseTypeDef:
        """
        Returns a list of resource metadata for a given list of crawler names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_get_crawlers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_crawlers)
        """

    async def batch_get_custom_entity_types(
        self, **kwargs: Unpack[BatchGetCustomEntityTypesRequestRequestTypeDef]
    ) -> BatchGetCustomEntityTypesResponseTypeDef:
        """
        Retrieves the details for the custom patterns specified by a list of names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_get_custom_entity_types.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_custom_entity_types)
        """

    async def batch_get_data_quality_result(
        self, **kwargs: Unpack[BatchGetDataQualityResultRequestRequestTypeDef]
    ) -> BatchGetDataQualityResultResponseTypeDef:
        """
        Retrieves a list of data quality results for the specified result IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_get_data_quality_result.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_data_quality_result)
        """

    async def batch_get_dev_endpoints(
        self, **kwargs: Unpack[BatchGetDevEndpointsRequestRequestTypeDef]
    ) -> BatchGetDevEndpointsResponseTypeDef:
        """
        Returns a list of resource metadata for a given list of development endpoint
        names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_get_dev_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_dev_endpoints)
        """

    async def batch_get_jobs(
        self, **kwargs: Unpack[BatchGetJobsRequestRequestTypeDef]
    ) -> BatchGetJobsResponseTypeDef:
        """
        Returns a list of resource metadata for a given list of job names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_get_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_jobs)
        """

    async def batch_get_partition(
        self, **kwargs: Unpack[BatchGetPartitionRequestRequestTypeDef]
    ) -> BatchGetPartitionResponseTypeDef:
        """
        Retrieves partitions in a batch request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_get_partition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_partition)
        """

    async def batch_get_table_optimizer(
        self, **kwargs: Unpack[BatchGetTableOptimizerRequestRequestTypeDef]
    ) -> BatchGetTableOptimizerResponseTypeDef:
        """
        Returns the configuration for the specified table optimizers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_get_table_optimizer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_table_optimizer)
        """

    async def batch_get_triggers(
        self, **kwargs: Unpack[BatchGetTriggersRequestRequestTypeDef]
    ) -> BatchGetTriggersResponseTypeDef:
        """
        Returns a list of resource metadata for a given list of trigger names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_get_triggers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_triggers)
        """

    async def batch_get_workflows(
        self, **kwargs: Unpack[BatchGetWorkflowsRequestRequestTypeDef]
    ) -> BatchGetWorkflowsResponseTypeDef:
        """
        Returns a list of resource metadata for a given list of workflow names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_get_workflows.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_workflows)
        """

    async def batch_put_data_quality_statistic_annotation(
        self, **kwargs: Unpack[BatchPutDataQualityStatisticAnnotationRequestRequestTypeDef]
    ) -> BatchPutDataQualityStatisticAnnotationResponseTypeDef:
        """
        Annotate datapoints over time for a specific data quality statistic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_put_data_quality_statistic_annotation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_put_data_quality_statistic_annotation)
        """

    async def batch_stop_job_run(
        self, **kwargs: Unpack[BatchStopJobRunRequestRequestTypeDef]
    ) -> BatchStopJobRunResponseTypeDef:
        """
        Stops one or more job runs for a specified job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_stop_job_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_stop_job_run)
        """

    async def batch_update_partition(
        self, **kwargs: Unpack[BatchUpdatePartitionRequestRequestTypeDef]
    ) -> BatchUpdatePartitionResponseTypeDef:
        """
        Updates one or more partitions in a batch operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/batch_update_partition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_update_partition)
        """

    async def cancel_data_quality_rule_recommendation_run(
        self, **kwargs: Unpack[CancelDataQualityRuleRecommendationRunRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels the specified recommendation run that was being used to generate rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/cancel_data_quality_rule_recommendation_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#cancel_data_quality_rule_recommendation_run)
        """

    async def cancel_data_quality_ruleset_evaluation_run(
        self, **kwargs: Unpack[CancelDataQualityRulesetEvaluationRunRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels a run where a ruleset is being evaluated against a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/cancel_data_quality_ruleset_evaluation_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#cancel_data_quality_ruleset_evaluation_run)
        """

    async def cancel_ml_task_run(
        self, **kwargs: Unpack[CancelMLTaskRunRequestRequestTypeDef]
    ) -> CancelMLTaskRunResponseTypeDef:
        """
        Cancels (stops) a task run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/cancel_ml_task_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#cancel_ml_task_run)
        """

    async def cancel_statement(
        self, **kwargs: Unpack[CancelStatementRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels the statement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/cancel_statement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#cancel_statement)
        """

    async def check_schema_version_validity(
        self, **kwargs: Unpack[CheckSchemaVersionValidityInputRequestTypeDef]
    ) -> CheckSchemaVersionValidityResponseTypeDef:
        """
        Validates the supplied schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/check_schema_version_validity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#check_schema_version_validity)
        """

    async def create_blueprint(
        self, **kwargs: Unpack[CreateBlueprintRequestRequestTypeDef]
    ) -> CreateBlueprintResponseTypeDef:
        """
        Registers a blueprint with Glue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_blueprint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_blueprint)
        """

    async def create_classifier(
        self, **kwargs: Unpack[CreateClassifierRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a classifier in the user's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_classifier.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_classifier)
        """

    async def create_connection(
        self, **kwargs: Unpack[CreateConnectionRequestRequestTypeDef]
    ) -> CreateConnectionResponseTypeDef:
        """
        Creates a connection definition in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_connection)
        """

    async def create_crawler(
        self, **kwargs: Unpack[CreateCrawlerRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a new crawler with specified targets, role, configuration, and optional
        schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_crawler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_crawler)
        """

    async def create_custom_entity_type(
        self, **kwargs: Unpack[CreateCustomEntityTypeRequestRequestTypeDef]
    ) -> CreateCustomEntityTypeResponseTypeDef:
        """
        Creates a custom pattern that is used to detect sensitive data across the
        columns and rows of your structured data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_custom_entity_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_custom_entity_type)
        """

    async def create_data_quality_ruleset(
        self, **kwargs: Unpack[CreateDataQualityRulesetRequestRequestTypeDef]
    ) -> CreateDataQualityRulesetResponseTypeDef:
        """
        Creates a data quality ruleset with DQDL rules applied to a specified Glue
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_data_quality_ruleset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_data_quality_ruleset)
        """

    async def create_database(
        self, **kwargs: Unpack[CreateDatabaseRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a new database in a Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_database.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_database)
        """

    async def create_dev_endpoint(
        self, **kwargs: Unpack[CreateDevEndpointRequestRequestTypeDef]
    ) -> CreateDevEndpointResponseTypeDef:
        """
        Creates a new development endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_dev_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_dev_endpoint)
        """

    async def create_job(
        self, **kwargs: Unpack[CreateJobRequestRequestTypeDef]
    ) -> CreateJobResponseTypeDef:
        """
        Creates a new job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_job)
        """

    async def create_ml_transform(
        self, **kwargs: Unpack[CreateMLTransformRequestRequestTypeDef]
    ) -> CreateMLTransformResponseTypeDef:
        """
        Creates an Glue machine learning transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_ml_transform.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_ml_transform)
        """

    async def create_partition(
        self, **kwargs: Unpack[CreatePartitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a new partition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_partition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_partition)
        """

    async def create_partition_index(
        self, **kwargs: Unpack[CreatePartitionIndexRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a specified partition index in an existing table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_partition_index.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_partition_index)
        """

    async def create_registry(
        self, **kwargs: Unpack[CreateRegistryInputRequestTypeDef]
    ) -> CreateRegistryResponseTypeDef:
        """
        Creates a new registry which may be used to hold a collection of schemas.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_registry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_registry)
        """

    async def create_schema(
        self, **kwargs: Unpack[CreateSchemaInputRequestTypeDef]
    ) -> CreateSchemaResponseTypeDef:
        """
        Creates a new schema set and registers the schema definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_schema.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_schema)
        """

    async def create_script(
        self, **kwargs: Unpack[CreateScriptRequestRequestTypeDef]
    ) -> CreateScriptResponseTypeDef:
        """
        Transforms a directed acyclic graph (DAG) into code.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_script.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_script)
        """

    async def create_security_configuration(
        self, **kwargs: Unpack[CreateSecurityConfigurationRequestRequestTypeDef]
    ) -> CreateSecurityConfigurationResponseTypeDef:
        """
        Creates a new security configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_security_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_security_configuration)
        """

    async def create_session(
        self, **kwargs: Unpack[CreateSessionRequestRequestTypeDef]
    ) -> CreateSessionResponseTypeDef:
        """
        Creates a new session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_session)
        """

    async def create_table(
        self, **kwargs: Unpack[CreateTableRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a new table definition in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_table)
        """

    async def create_table_optimizer(
        self, **kwargs: Unpack[CreateTableOptimizerRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a new table optimizer for a specific function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_table_optimizer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_table_optimizer)
        """

    async def create_trigger(
        self, **kwargs: Unpack[CreateTriggerRequestRequestTypeDef]
    ) -> CreateTriggerResponseTypeDef:
        """
        Creates a new trigger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_trigger.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_trigger)
        """

    async def create_usage_profile(
        self, **kwargs: Unpack[CreateUsageProfileRequestRequestTypeDef]
    ) -> CreateUsageProfileResponseTypeDef:
        """
        Creates an Glue usage profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_usage_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_usage_profile)
        """

    async def create_user_defined_function(
        self, **kwargs: Unpack[CreateUserDefinedFunctionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a new function definition in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_user_defined_function.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_user_defined_function)
        """

    async def create_workflow(
        self, **kwargs: Unpack[CreateWorkflowRequestRequestTypeDef]
    ) -> CreateWorkflowResponseTypeDef:
        """
        Creates a new workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/create_workflow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_workflow)
        """

    async def delete_blueprint(
        self, **kwargs: Unpack[DeleteBlueprintRequestRequestTypeDef]
    ) -> DeleteBlueprintResponseTypeDef:
        """
        Deletes an existing blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_blueprint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_blueprint)
        """

    async def delete_classifier(
        self, **kwargs: Unpack[DeleteClassifierRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a classifier from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_classifier.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_classifier)
        """

    async def delete_column_statistics_for_partition(
        self, **kwargs: Unpack[DeleteColumnStatisticsForPartitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete the partition column statistics of a column.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_column_statistics_for_partition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_column_statistics_for_partition)
        """

    async def delete_column_statistics_for_table(
        self, **kwargs: Unpack[DeleteColumnStatisticsForTableRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Retrieves table statistics of columns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_column_statistics_for_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_column_statistics_for_table)
        """

    async def delete_connection(
        self, **kwargs: Unpack[DeleteConnectionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a connection from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_connection)
        """

    async def delete_crawler(
        self, **kwargs: Unpack[DeleteCrawlerRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a specified crawler from the Glue Data Catalog, unless the crawler
        state is <code>RUNNING</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_crawler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_crawler)
        """

    async def delete_custom_entity_type(
        self, **kwargs: Unpack[DeleteCustomEntityTypeRequestRequestTypeDef]
    ) -> DeleteCustomEntityTypeResponseTypeDef:
        """
        Deletes a custom pattern by specifying its name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_custom_entity_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_custom_entity_type)
        """

    async def delete_data_quality_ruleset(
        self, **kwargs: Unpack[DeleteDataQualityRulesetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a data quality ruleset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_data_quality_ruleset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_data_quality_ruleset)
        """

    async def delete_database(
        self, **kwargs: Unpack[DeleteDatabaseRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a specified database from a Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_database.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_database)
        """

    async def delete_dev_endpoint(
        self, **kwargs: Unpack[DeleteDevEndpointRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specified development endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_dev_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_dev_endpoint)
        """

    async def delete_job(
        self, **kwargs: Unpack[DeleteJobRequestRequestTypeDef]
    ) -> DeleteJobResponseTypeDef:
        """
        Deletes a specified job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_job)
        """

    async def delete_ml_transform(
        self, **kwargs: Unpack[DeleteMLTransformRequestRequestTypeDef]
    ) -> DeleteMLTransformResponseTypeDef:
        """
        Deletes an Glue machine learning transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_ml_transform.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_ml_transform)
        """

    async def delete_partition(
        self, **kwargs: Unpack[DeletePartitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specified partition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_partition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_partition)
        """

    async def delete_partition_index(
        self, **kwargs: Unpack[DeletePartitionIndexRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specified partition index from an existing table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_partition_index.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_partition_index)
        """

    async def delete_registry(
        self, **kwargs: Unpack[DeleteRegistryInputRequestTypeDef]
    ) -> DeleteRegistryResponseTypeDef:
        """
        Delete the entire registry including schema and all of its versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_registry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_registry)
        """

    async def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_resource_policy)
        """

    async def delete_schema(
        self, **kwargs: Unpack[DeleteSchemaInputRequestTypeDef]
    ) -> DeleteSchemaResponseTypeDef:
        """
        Deletes the entire schema set, including the schema set and all of its versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_schema.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_schema)
        """

    async def delete_schema_versions(
        self, **kwargs: Unpack[DeleteSchemaVersionsInputRequestTypeDef]
    ) -> DeleteSchemaVersionsResponseTypeDef:
        """
        Remove versions from the specified schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_schema_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_schema_versions)
        """

    async def delete_security_configuration(
        self, **kwargs: Unpack[DeleteSecurityConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specified security configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_security_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_security_configuration)
        """

    async def delete_session(
        self, **kwargs: Unpack[DeleteSessionRequestRequestTypeDef]
    ) -> DeleteSessionResponseTypeDef:
        """
        Deletes the session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_session)
        """

    async def delete_table(
        self, **kwargs: Unpack[DeleteTableRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a table definition from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_table)
        """

    async def delete_table_optimizer(
        self, **kwargs: Unpack[DeleteTableOptimizerRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an optimizer and all associated metadata for a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_table_optimizer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_table_optimizer)
        """

    async def delete_table_version(
        self, **kwargs: Unpack[DeleteTableVersionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specified version of a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_table_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_table_version)
        """

    async def delete_trigger(
        self, **kwargs: Unpack[DeleteTriggerRequestRequestTypeDef]
    ) -> DeleteTriggerResponseTypeDef:
        """
        Deletes a specified trigger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_trigger.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_trigger)
        """

    async def delete_usage_profile(
        self, **kwargs: Unpack[DeleteUsageProfileRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the Glue specified usage profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_usage_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_usage_profile)
        """

    async def delete_user_defined_function(
        self, **kwargs: Unpack[DeleteUserDefinedFunctionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an existing function definition from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_user_defined_function.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_user_defined_function)
        """

    async def delete_workflow(
        self, **kwargs: Unpack[DeleteWorkflowRequestRequestTypeDef]
    ) -> DeleteWorkflowResponseTypeDef:
        """
        Deletes a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/delete_workflow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_workflow)
        """

    async def get_blueprint(
        self, **kwargs: Unpack[GetBlueprintRequestRequestTypeDef]
    ) -> GetBlueprintResponseTypeDef:
        """
        Retrieves the details of a blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_blueprint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_blueprint)
        """

    async def get_blueprint_run(
        self, **kwargs: Unpack[GetBlueprintRunRequestRequestTypeDef]
    ) -> GetBlueprintRunResponseTypeDef:
        """
        Retrieves the details of a blueprint run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_blueprint_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_blueprint_run)
        """

    async def get_blueprint_runs(
        self, **kwargs: Unpack[GetBlueprintRunsRequestRequestTypeDef]
    ) -> GetBlueprintRunsResponseTypeDef:
        """
        Retrieves the details of blueprint runs for a specified blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_blueprint_runs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_blueprint_runs)
        """

    async def get_catalog_import_status(
        self, **kwargs: Unpack[GetCatalogImportStatusRequestRequestTypeDef]
    ) -> GetCatalogImportStatusResponseTypeDef:
        """
        Retrieves the status of a migration operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_catalog_import_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_catalog_import_status)
        """

    async def get_classifier(
        self, **kwargs: Unpack[GetClassifierRequestRequestTypeDef]
    ) -> GetClassifierResponseTypeDef:
        """
        Retrieve a classifier by name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_classifier.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_classifier)
        """

    async def get_classifiers(
        self, **kwargs: Unpack[GetClassifiersRequestRequestTypeDef]
    ) -> GetClassifiersResponseTypeDef:
        """
        Lists all classifier objects in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_classifiers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_classifiers)
        """

    async def get_column_statistics_for_partition(
        self, **kwargs: Unpack[GetColumnStatisticsForPartitionRequestRequestTypeDef]
    ) -> GetColumnStatisticsForPartitionResponseTypeDef:
        """
        Retrieves partition statistics of columns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_column_statistics_for_partition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_column_statistics_for_partition)
        """

    async def get_column_statistics_for_table(
        self, **kwargs: Unpack[GetColumnStatisticsForTableRequestRequestTypeDef]
    ) -> GetColumnStatisticsForTableResponseTypeDef:
        """
        Retrieves table statistics of columns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_column_statistics_for_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_column_statistics_for_table)
        """

    async def get_column_statistics_task_run(
        self, **kwargs: Unpack[GetColumnStatisticsTaskRunRequestRequestTypeDef]
    ) -> GetColumnStatisticsTaskRunResponseTypeDef:
        """
        Get the associated metadata/information for a task run, given a task run ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_column_statistics_task_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_column_statistics_task_run)
        """

    async def get_column_statistics_task_runs(
        self, **kwargs: Unpack[GetColumnStatisticsTaskRunsRequestRequestTypeDef]
    ) -> GetColumnStatisticsTaskRunsResponseTypeDef:
        """
        Retrieves information about all runs associated with the specified table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_column_statistics_task_runs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_column_statistics_task_runs)
        """

    async def get_connection(
        self, **kwargs: Unpack[GetConnectionRequestRequestTypeDef]
    ) -> GetConnectionResponseTypeDef:
        """
        Retrieves a connection definition from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_connection)
        """

    async def get_connections(
        self, **kwargs: Unpack[GetConnectionsRequestRequestTypeDef]
    ) -> GetConnectionsResponseTypeDef:
        """
        Retrieves a list of connection definitions from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_connections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_connections)
        """

    async def get_crawler(
        self, **kwargs: Unpack[GetCrawlerRequestRequestTypeDef]
    ) -> GetCrawlerResponseTypeDef:
        """
        Retrieves metadata for a specified crawler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_crawler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_crawler)
        """

    async def get_crawler_metrics(
        self, **kwargs: Unpack[GetCrawlerMetricsRequestRequestTypeDef]
    ) -> GetCrawlerMetricsResponseTypeDef:
        """
        Retrieves metrics about specified crawlers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_crawler_metrics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_crawler_metrics)
        """

    async def get_crawlers(
        self, **kwargs: Unpack[GetCrawlersRequestRequestTypeDef]
    ) -> GetCrawlersResponseTypeDef:
        """
        Retrieves metadata for all crawlers defined in the customer account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_crawlers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_crawlers)
        """

    async def get_custom_entity_type(
        self, **kwargs: Unpack[GetCustomEntityTypeRequestRequestTypeDef]
    ) -> GetCustomEntityTypeResponseTypeDef:
        """
        Retrieves the details of a custom pattern by specifying its name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_custom_entity_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_custom_entity_type)
        """

    async def get_data_catalog_encryption_settings(
        self, **kwargs: Unpack[GetDataCatalogEncryptionSettingsRequestRequestTypeDef]
    ) -> GetDataCatalogEncryptionSettingsResponseTypeDef:
        """
        Retrieves the security configuration for a specified catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_data_catalog_encryption_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_data_catalog_encryption_settings)
        """

    async def get_data_quality_model(
        self, **kwargs: Unpack[GetDataQualityModelRequestRequestTypeDef]
    ) -> GetDataQualityModelResponseTypeDef:
        """
        Retrieve the training status of the model along with more information
        (CompletedOn, StartedOn, FailureReason).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_data_quality_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_data_quality_model)
        """

    async def get_data_quality_model_result(
        self, **kwargs: Unpack[GetDataQualityModelResultRequestRequestTypeDef]
    ) -> GetDataQualityModelResultResponseTypeDef:
        """
        Retrieve a statistic's predictions for a given Profile ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_data_quality_model_result.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_data_quality_model_result)
        """

    async def get_data_quality_result(
        self, **kwargs: Unpack[GetDataQualityResultRequestRequestTypeDef]
    ) -> GetDataQualityResultResponseTypeDef:
        """
        Retrieves the result of a data quality rule evaluation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_data_quality_result.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_data_quality_result)
        """

    async def get_data_quality_rule_recommendation_run(
        self, **kwargs: Unpack[GetDataQualityRuleRecommendationRunRequestRequestTypeDef]
    ) -> GetDataQualityRuleRecommendationRunResponseTypeDef:
        """
        Gets the specified recommendation run that was used to generate rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_data_quality_rule_recommendation_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_data_quality_rule_recommendation_run)
        """

    async def get_data_quality_ruleset(
        self, **kwargs: Unpack[GetDataQualityRulesetRequestRequestTypeDef]
    ) -> GetDataQualityRulesetResponseTypeDef:
        """
        Returns an existing ruleset by identifier or name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_data_quality_ruleset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_data_quality_ruleset)
        """

    async def get_data_quality_ruleset_evaluation_run(
        self, **kwargs: Unpack[GetDataQualityRulesetEvaluationRunRequestRequestTypeDef]
    ) -> GetDataQualityRulesetEvaluationRunResponseTypeDef:
        """
        Retrieves a specific run where a ruleset is evaluated against a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_data_quality_ruleset_evaluation_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_data_quality_ruleset_evaluation_run)
        """

    async def get_database(
        self, **kwargs: Unpack[GetDatabaseRequestRequestTypeDef]
    ) -> GetDatabaseResponseTypeDef:
        """
        Retrieves the definition of a specified database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_database.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_database)
        """

    async def get_databases(
        self, **kwargs: Unpack[GetDatabasesRequestRequestTypeDef]
    ) -> GetDatabasesResponseTypeDef:
        """
        Retrieves all databases defined in a given Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_databases.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_databases)
        """

    async def get_dataflow_graph(
        self, **kwargs: Unpack[GetDataflowGraphRequestRequestTypeDef]
    ) -> GetDataflowGraphResponseTypeDef:
        """
        Transforms a Python script into a directed acyclic graph (DAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_dataflow_graph.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_dataflow_graph)
        """

    async def get_dev_endpoint(
        self, **kwargs: Unpack[GetDevEndpointRequestRequestTypeDef]
    ) -> GetDevEndpointResponseTypeDef:
        """
        Retrieves information about a specified development endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_dev_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_dev_endpoint)
        """

    async def get_dev_endpoints(
        self, **kwargs: Unpack[GetDevEndpointsRequestRequestTypeDef]
    ) -> GetDevEndpointsResponseTypeDef:
        """
        Retrieves all the development endpoints in this Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_dev_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_dev_endpoints)
        """

    async def get_job(self, **kwargs: Unpack[GetJobRequestRequestTypeDef]) -> GetJobResponseTypeDef:
        """
        Retrieves an existing job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_job)
        """

    async def get_job_bookmark(
        self, **kwargs: Unpack[GetJobBookmarkRequestRequestTypeDef]
    ) -> GetJobBookmarkResponseTypeDef:
        """
        Returns information on a job bookmark entry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_job_bookmark.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_job_bookmark)
        """

    async def get_job_run(
        self, **kwargs: Unpack[GetJobRunRequestRequestTypeDef]
    ) -> GetJobRunResponseTypeDef:
        """
        Retrieves the metadata for a given job run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_job_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_job_run)
        """

    async def get_job_runs(
        self, **kwargs: Unpack[GetJobRunsRequestRequestTypeDef]
    ) -> GetJobRunsResponseTypeDef:
        """
        Retrieves metadata for all runs of a given job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_job_runs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_job_runs)
        """

    async def get_jobs(
        self, **kwargs: Unpack[GetJobsRequestRequestTypeDef]
    ) -> GetJobsResponseTypeDef:
        """
        Retrieves all current job definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_jobs)
        """

    async def get_ml_task_run(
        self, **kwargs: Unpack[GetMLTaskRunRequestRequestTypeDef]
    ) -> GetMLTaskRunResponseTypeDef:
        """
        Gets details for a specific task run on a machine learning transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_ml_task_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_ml_task_run)
        """

    async def get_ml_task_runs(
        self, **kwargs: Unpack[GetMLTaskRunsRequestRequestTypeDef]
    ) -> GetMLTaskRunsResponseTypeDef:
        """
        Gets a list of runs for a machine learning transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_ml_task_runs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_ml_task_runs)
        """

    async def get_ml_transform(
        self, **kwargs: Unpack[GetMLTransformRequestRequestTypeDef]
    ) -> GetMLTransformResponseTypeDef:
        """
        Gets an Glue machine learning transform artifact and all its corresponding
        metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_ml_transform.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_ml_transform)
        """

    async def get_ml_transforms(
        self, **kwargs: Unpack[GetMLTransformsRequestRequestTypeDef]
    ) -> GetMLTransformsResponseTypeDef:
        """
        Gets a sortable, filterable list of existing Glue machine learning transforms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_ml_transforms.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_ml_transforms)
        """

    async def get_mapping(
        self, **kwargs: Unpack[GetMappingRequestRequestTypeDef]
    ) -> GetMappingResponseTypeDef:
        """
        Creates mappings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_mapping.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_mapping)
        """

    async def get_partition(
        self, **kwargs: Unpack[GetPartitionRequestRequestTypeDef]
    ) -> GetPartitionResponseTypeDef:
        """
        Retrieves information about a specified partition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_partition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_partition)
        """

    async def get_partition_indexes(
        self, **kwargs: Unpack[GetPartitionIndexesRequestRequestTypeDef]
    ) -> GetPartitionIndexesResponseTypeDef:
        """
        Retrieves the partition indexes associated with a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_partition_indexes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_partition_indexes)
        """

    async def get_partitions(
        self, **kwargs: Unpack[GetPartitionsRequestRequestTypeDef]
    ) -> GetPartitionsResponseTypeDef:
        """
        Retrieves information about the partitions in a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_partitions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_partitions)
        """

    async def get_plan(
        self, **kwargs: Unpack[GetPlanRequestRequestTypeDef]
    ) -> GetPlanResponseTypeDef:
        """
        Gets code to perform a specified mapping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_plan.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_plan)
        """

    async def get_registry(
        self, **kwargs: Unpack[GetRegistryInputRequestTypeDef]
    ) -> GetRegistryResponseTypeDef:
        """
        Describes the specified registry in detail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_registry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_registry)
        """

    async def get_resource_policies(
        self, **kwargs: Unpack[GetResourcePoliciesRequestRequestTypeDef]
    ) -> GetResourcePoliciesResponseTypeDef:
        """
        Retrieves the resource policies set on individual resources by Resource Access
        Manager during cross-account permission grants.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_resource_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_resource_policies)
        """

    async def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyRequestRequestTypeDef]
    ) -> GetResourcePolicyResponseTypeDef:
        """
        Retrieves a specified resource policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_resource_policy)
        """

    async def get_schema(
        self, **kwargs: Unpack[GetSchemaInputRequestTypeDef]
    ) -> GetSchemaResponseTypeDef:
        """
        Describes the specified schema in detail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_schema.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_schema)
        """

    async def get_schema_by_definition(
        self, **kwargs: Unpack[GetSchemaByDefinitionInputRequestTypeDef]
    ) -> GetSchemaByDefinitionResponseTypeDef:
        """
        Retrieves a schema by the <code>SchemaDefinition</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_schema_by_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_schema_by_definition)
        """

    async def get_schema_version(
        self, **kwargs: Unpack[GetSchemaVersionInputRequestTypeDef]
    ) -> GetSchemaVersionResponseTypeDef:
        """
        Get the specified schema by its unique ID assigned when a version of the schema
        is created or registered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_schema_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_schema_version)
        """

    async def get_schema_versions_diff(
        self, **kwargs: Unpack[GetSchemaVersionsDiffInputRequestTypeDef]
    ) -> GetSchemaVersionsDiffResponseTypeDef:
        """
        Fetches the schema version difference in the specified difference type between
        two stored schema versions in the Schema Registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_schema_versions_diff.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_schema_versions_diff)
        """

    async def get_security_configuration(
        self, **kwargs: Unpack[GetSecurityConfigurationRequestRequestTypeDef]
    ) -> GetSecurityConfigurationResponseTypeDef:
        """
        Retrieves a specified security configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_security_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_security_configuration)
        """

    async def get_security_configurations(
        self, **kwargs: Unpack[GetSecurityConfigurationsRequestRequestTypeDef]
    ) -> GetSecurityConfigurationsResponseTypeDef:
        """
        Retrieves a list of all security configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_security_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_security_configurations)
        """

    async def get_session(
        self, **kwargs: Unpack[GetSessionRequestRequestTypeDef]
    ) -> GetSessionResponseTypeDef:
        """
        Retrieves the session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_session)
        """

    async def get_statement(
        self, **kwargs: Unpack[GetStatementRequestRequestTypeDef]
    ) -> GetStatementResponseTypeDef:
        """
        Retrieves the statement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_statement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_statement)
        """

    async def get_table(
        self, **kwargs: Unpack[GetTableRequestRequestTypeDef]
    ) -> GetTableResponseTypeDef:
        """
        Retrieves the <code>Table</code> definition in a Data Catalog for a specified
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_table)
        """

    async def get_table_optimizer(
        self, **kwargs: Unpack[GetTableOptimizerRequestRequestTypeDef]
    ) -> GetTableOptimizerResponseTypeDef:
        """
        Returns the configuration of all optimizers associated with a specified table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_table_optimizer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_table_optimizer)
        """

    async def get_table_version(
        self, **kwargs: Unpack[GetTableVersionRequestRequestTypeDef]
    ) -> GetTableVersionResponseTypeDef:
        """
        Retrieves a specified version of a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_table_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_table_version)
        """

    async def get_table_versions(
        self, **kwargs: Unpack[GetTableVersionsRequestRequestTypeDef]
    ) -> GetTableVersionsResponseTypeDef:
        """
        Retrieves a list of strings that identify available versions of a specified
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_table_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_table_versions)
        """

    async def get_tables(
        self, **kwargs: Unpack[GetTablesRequestRequestTypeDef]
    ) -> GetTablesResponseTypeDef:
        """
        Retrieves the definitions of some or all of the tables in a given
        <code>Database</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_tables.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_tables)
        """

    async def get_tags(
        self, **kwargs: Unpack[GetTagsRequestRequestTypeDef]
    ) -> GetTagsResponseTypeDef:
        """
        Retrieves a list of tags associated with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_tags)
        """

    async def get_trigger(
        self, **kwargs: Unpack[GetTriggerRequestRequestTypeDef]
    ) -> GetTriggerResponseTypeDef:
        """
        Retrieves the definition of a trigger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_trigger.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_trigger)
        """

    async def get_triggers(
        self, **kwargs: Unpack[GetTriggersRequestRequestTypeDef]
    ) -> GetTriggersResponseTypeDef:
        """
        Gets all the triggers associated with a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_triggers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_triggers)
        """

    async def get_unfiltered_partition_metadata(
        self, **kwargs: Unpack[GetUnfilteredPartitionMetadataRequestRequestTypeDef]
    ) -> GetUnfilteredPartitionMetadataResponseTypeDef:
        """
        Retrieves partition metadata from the Data Catalog that contains unfiltered
        metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_unfiltered_partition_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_unfiltered_partition_metadata)
        """

    async def get_unfiltered_partitions_metadata(
        self, **kwargs: Unpack[GetUnfilteredPartitionsMetadataRequestRequestTypeDef]
    ) -> GetUnfilteredPartitionsMetadataResponseTypeDef:
        """
        Retrieves partition metadata from the Data Catalog that contains unfiltered
        metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_unfiltered_partitions_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_unfiltered_partitions_metadata)
        """

    async def get_unfiltered_table_metadata(
        self, **kwargs: Unpack[GetUnfilteredTableMetadataRequestRequestTypeDef]
    ) -> GetUnfilteredTableMetadataResponseTypeDef:
        """
        Allows a third-party analytical engine to retrieve unfiltered table metadata
        from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_unfiltered_table_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_unfiltered_table_metadata)
        """

    async def get_usage_profile(
        self, **kwargs: Unpack[GetUsageProfileRequestRequestTypeDef]
    ) -> GetUsageProfileResponseTypeDef:
        """
        Retrieves information about the specified Glue usage profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_usage_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_usage_profile)
        """

    async def get_user_defined_function(
        self, **kwargs: Unpack[GetUserDefinedFunctionRequestRequestTypeDef]
    ) -> GetUserDefinedFunctionResponseTypeDef:
        """
        Retrieves a specified function definition from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_user_defined_function.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_user_defined_function)
        """

    async def get_user_defined_functions(
        self, **kwargs: Unpack[GetUserDefinedFunctionsRequestRequestTypeDef]
    ) -> GetUserDefinedFunctionsResponseTypeDef:
        """
        Retrieves multiple function definitions from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_user_defined_functions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_user_defined_functions)
        """

    async def get_workflow(
        self, **kwargs: Unpack[GetWorkflowRequestRequestTypeDef]
    ) -> GetWorkflowResponseTypeDef:
        """
        Retrieves resource metadata for a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_workflow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_workflow)
        """

    async def get_workflow_run(
        self, **kwargs: Unpack[GetWorkflowRunRequestRequestTypeDef]
    ) -> GetWorkflowRunResponseTypeDef:
        """
        Retrieves the metadata for a given workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_workflow_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_workflow_run)
        """

    async def get_workflow_run_properties(
        self, **kwargs: Unpack[GetWorkflowRunPropertiesRequestRequestTypeDef]
    ) -> GetWorkflowRunPropertiesResponseTypeDef:
        """
        Retrieves the workflow run properties which were set during the run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_workflow_run_properties.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_workflow_run_properties)
        """

    async def get_workflow_runs(
        self, **kwargs: Unpack[GetWorkflowRunsRequestRequestTypeDef]
    ) -> GetWorkflowRunsResponseTypeDef:
        """
        Retrieves metadata for all runs of a given workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_workflow_runs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_workflow_runs)
        """

    async def import_catalog_to_glue(
        self, **kwargs: Unpack[ImportCatalogToGlueRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Imports an existing Amazon Athena Data Catalog to Glue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/import_catalog_to_glue.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#import_catalog_to_glue)
        """

    async def list_blueprints(
        self, **kwargs: Unpack[ListBlueprintsRequestRequestTypeDef]
    ) -> ListBlueprintsResponseTypeDef:
        """
        Lists all the blueprint names in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_blueprints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_blueprints)
        """

    async def list_column_statistics_task_runs(
        self, **kwargs: Unpack[ListColumnStatisticsTaskRunsRequestRequestTypeDef]
    ) -> ListColumnStatisticsTaskRunsResponseTypeDef:
        """
        List all task runs for a particular account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_column_statistics_task_runs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_column_statistics_task_runs)
        """

    async def list_crawlers(
        self, **kwargs: Unpack[ListCrawlersRequestRequestTypeDef]
    ) -> ListCrawlersResponseTypeDef:
        """
        Retrieves the names of all crawler resources in this Amazon Web Services
        account, or the resources with the specified tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_crawlers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_crawlers)
        """

    async def list_crawls(
        self, **kwargs: Unpack[ListCrawlsRequestRequestTypeDef]
    ) -> ListCrawlsResponseTypeDef:
        """
        Returns all the crawls of a specified crawler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_crawls.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_crawls)
        """

    async def list_custom_entity_types(
        self, **kwargs: Unpack[ListCustomEntityTypesRequestRequestTypeDef]
    ) -> ListCustomEntityTypesResponseTypeDef:
        """
        Lists all the custom patterns that have been created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_custom_entity_types.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_custom_entity_types)
        """

    async def list_data_quality_results(
        self, **kwargs: Unpack[ListDataQualityResultsRequestRequestTypeDef]
    ) -> ListDataQualityResultsResponseTypeDef:
        """
        Returns all data quality execution results for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_data_quality_results.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_data_quality_results)
        """

    async def list_data_quality_rule_recommendation_runs(
        self, **kwargs: Unpack[ListDataQualityRuleRecommendationRunsRequestRequestTypeDef]
    ) -> ListDataQualityRuleRecommendationRunsResponseTypeDef:
        """
        Lists the recommendation runs meeting the filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_data_quality_rule_recommendation_runs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_data_quality_rule_recommendation_runs)
        """

    async def list_data_quality_ruleset_evaluation_runs(
        self, **kwargs: Unpack[ListDataQualityRulesetEvaluationRunsRequestRequestTypeDef]
    ) -> ListDataQualityRulesetEvaluationRunsResponseTypeDef:
        """
        Lists all the runs meeting the filter criteria, where a ruleset is evaluated
        against a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_data_quality_ruleset_evaluation_runs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_data_quality_ruleset_evaluation_runs)
        """

    async def list_data_quality_rulesets(
        self, **kwargs: Unpack[ListDataQualityRulesetsRequestRequestTypeDef]
    ) -> ListDataQualityRulesetsResponseTypeDef:
        """
        Returns a paginated list of rulesets for the specified list of Glue tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_data_quality_rulesets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_data_quality_rulesets)
        """

    async def list_data_quality_statistic_annotations(
        self, **kwargs: Unpack[ListDataQualityStatisticAnnotationsRequestRequestTypeDef]
    ) -> ListDataQualityStatisticAnnotationsResponseTypeDef:
        """
        Retrieve annotations for a data quality statistic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_data_quality_statistic_annotations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_data_quality_statistic_annotations)
        """

    async def list_data_quality_statistics(
        self, **kwargs: Unpack[ListDataQualityStatisticsRequestRequestTypeDef]
    ) -> ListDataQualityStatisticsResponseTypeDef:
        """
        Retrieves a list of data quality statistics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_data_quality_statistics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_data_quality_statistics)
        """

    async def list_dev_endpoints(
        self, **kwargs: Unpack[ListDevEndpointsRequestRequestTypeDef]
    ) -> ListDevEndpointsResponseTypeDef:
        """
        Retrieves the names of all <code>DevEndpoint</code> resources in this Amazon
        Web Services account, or the resources with the specified tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_dev_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_dev_endpoints)
        """

    async def list_jobs(
        self, **kwargs: Unpack[ListJobsRequestRequestTypeDef]
    ) -> ListJobsResponseTypeDef:
        """
        Retrieves the names of all job resources in this Amazon Web Services account,
        or the resources with the specified tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_jobs)
        """

    async def list_ml_transforms(
        self, **kwargs: Unpack[ListMLTransformsRequestRequestTypeDef]
    ) -> ListMLTransformsResponseTypeDef:
        """
        Retrieves a sortable, filterable list of existing Glue machine learning
        transforms in this Amazon Web Services account, or the resources with the
        specified tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_ml_transforms.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_ml_transforms)
        """

    async def list_registries(
        self, **kwargs: Unpack[ListRegistriesInputRequestTypeDef]
    ) -> ListRegistriesResponseTypeDef:
        """
        Returns a list of registries that you have created, with minimal registry
        information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_registries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_registries)
        """

    async def list_schema_versions(
        self, **kwargs: Unpack[ListSchemaVersionsInputRequestTypeDef]
    ) -> ListSchemaVersionsResponseTypeDef:
        """
        Returns a list of schema versions that you have created, with minimal
        information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_schema_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_schema_versions)
        """

    async def list_schemas(
        self, **kwargs: Unpack[ListSchemasInputRequestTypeDef]
    ) -> ListSchemasResponseTypeDef:
        """
        Returns a list of schemas with minimal details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_schemas.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_schemas)
        """

    async def list_sessions(
        self, **kwargs: Unpack[ListSessionsRequestRequestTypeDef]
    ) -> ListSessionsResponseTypeDef:
        """
        Retrieve a list of sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_sessions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_sessions)
        """

    async def list_statements(
        self, **kwargs: Unpack[ListStatementsRequestRequestTypeDef]
    ) -> ListStatementsResponseTypeDef:
        """
        Lists statements for the session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_statements.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_statements)
        """

    async def list_table_optimizer_runs(
        self, **kwargs: Unpack[ListTableOptimizerRunsRequestRequestTypeDef]
    ) -> ListTableOptimizerRunsResponseTypeDef:
        """
        Lists the history of previous optimizer runs for a specific table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_table_optimizer_runs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_table_optimizer_runs)
        """

    async def list_triggers(
        self, **kwargs: Unpack[ListTriggersRequestRequestTypeDef]
    ) -> ListTriggersResponseTypeDef:
        """
        Retrieves the names of all trigger resources in this Amazon Web Services
        account, or the resources with the specified tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_triggers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_triggers)
        """

    async def list_usage_profiles(
        self, **kwargs: Unpack[ListUsageProfilesRequestRequestTypeDef]
    ) -> ListUsageProfilesResponseTypeDef:
        """
        List all the Glue usage profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_usage_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_usage_profiles)
        """

    async def list_workflows(
        self, **kwargs: Unpack[ListWorkflowsRequestRequestTypeDef]
    ) -> ListWorkflowsResponseTypeDef:
        """
        Lists names of workflows created in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/list_workflows.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_workflows)
        """

    async def put_data_catalog_encryption_settings(
        self, **kwargs: Unpack[PutDataCatalogEncryptionSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets the security configuration for a specified catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/put_data_catalog_encryption_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#put_data_catalog_encryption_settings)
        """

    async def put_data_quality_profile_annotation(
        self, **kwargs: Unpack[PutDataQualityProfileAnnotationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Annotate all datapoints for a Profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/put_data_quality_profile_annotation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#put_data_quality_profile_annotation)
        """

    async def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestRequestTypeDef]
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Sets the Data Catalog resource policy for access control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/put_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#put_resource_policy)
        """

    async def put_schema_version_metadata(
        self, **kwargs: Unpack[PutSchemaVersionMetadataInputRequestTypeDef]
    ) -> PutSchemaVersionMetadataResponseTypeDef:
        """
        Puts the metadata key value pair for a specified schema version ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/put_schema_version_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#put_schema_version_metadata)
        """

    async def put_workflow_run_properties(
        self, **kwargs: Unpack[PutWorkflowRunPropertiesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Puts the specified workflow run properties for the given workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/put_workflow_run_properties.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#put_workflow_run_properties)
        """

    async def query_schema_version_metadata(
        self, **kwargs: Unpack[QuerySchemaVersionMetadataInputRequestTypeDef]
    ) -> QuerySchemaVersionMetadataResponseTypeDef:
        """
        Queries for the schema version metadata information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/query_schema_version_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#query_schema_version_metadata)
        """

    async def register_schema_version(
        self, **kwargs: Unpack[RegisterSchemaVersionInputRequestTypeDef]
    ) -> RegisterSchemaVersionResponseTypeDef:
        """
        Adds a new version to the existing schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/register_schema_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#register_schema_version)
        """

    async def remove_schema_version_metadata(
        self, **kwargs: Unpack[RemoveSchemaVersionMetadataInputRequestTypeDef]
    ) -> RemoveSchemaVersionMetadataResponseTypeDef:
        """
        Removes a key value pair from the schema version metadata for the specified
        schema version ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/remove_schema_version_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#remove_schema_version_metadata)
        """

    async def reset_job_bookmark(
        self, **kwargs: Unpack[ResetJobBookmarkRequestRequestTypeDef]
    ) -> ResetJobBookmarkResponseTypeDef:
        """
        Resets a bookmark entry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/reset_job_bookmark.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#reset_job_bookmark)
        """

    async def resume_workflow_run(
        self, **kwargs: Unpack[ResumeWorkflowRunRequestRequestTypeDef]
    ) -> ResumeWorkflowRunResponseTypeDef:
        """
        Restarts selected nodes of a previous partially completed workflow run and
        resumes the workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/resume_workflow_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#resume_workflow_run)
        """

    async def run_statement(
        self, **kwargs: Unpack[RunStatementRequestRequestTypeDef]
    ) -> RunStatementResponseTypeDef:
        """
        Executes the statement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/run_statement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#run_statement)
        """

    async def search_tables(
        self, **kwargs: Unpack[SearchTablesRequestRequestTypeDef]
    ) -> SearchTablesResponseTypeDef:
        """
        Searches a set of tables based on properties in the table metadata as well as
        on the parent database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/search_tables.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#search_tables)
        """

    async def start_blueprint_run(
        self, **kwargs: Unpack[StartBlueprintRunRequestRequestTypeDef]
    ) -> StartBlueprintRunResponseTypeDef:
        """
        Starts a new run of the specified blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/start_blueprint_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_blueprint_run)
        """

    async def start_column_statistics_task_run(
        self, **kwargs: Unpack[StartColumnStatisticsTaskRunRequestRequestTypeDef]
    ) -> StartColumnStatisticsTaskRunResponseTypeDef:
        """
        Starts a column statistics task run, for a specified table and columns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/start_column_statistics_task_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_column_statistics_task_run)
        """

    async def start_crawler(
        self, **kwargs: Unpack[StartCrawlerRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts a crawl using the specified crawler, regardless of what is scheduled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/start_crawler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_crawler)
        """

    async def start_crawler_schedule(
        self, **kwargs: Unpack[StartCrawlerScheduleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Changes the schedule state of the specified crawler to <code>SCHEDULED</code>,
        unless the crawler is already running or the schedule state is already
        <code>SCHEDULED</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/start_crawler_schedule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_crawler_schedule)
        """

    async def start_data_quality_rule_recommendation_run(
        self, **kwargs: Unpack[StartDataQualityRuleRecommendationRunRequestRequestTypeDef]
    ) -> StartDataQualityRuleRecommendationRunResponseTypeDef:
        """
        Starts a recommendation run that is used to generate rules when you don't know
        what rules to write.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/start_data_quality_rule_recommendation_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_data_quality_rule_recommendation_run)
        """

    async def start_data_quality_ruleset_evaluation_run(
        self, **kwargs: Unpack[StartDataQualityRulesetEvaluationRunRequestRequestTypeDef]
    ) -> StartDataQualityRulesetEvaluationRunResponseTypeDef:
        """
        Once you have a ruleset definition (either recommended or your own), you call
        this operation to evaluate the ruleset against a data source (Glue table).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/start_data_quality_ruleset_evaluation_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_data_quality_ruleset_evaluation_run)
        """

    async def start_export_labels_task_run(
        self, **kwargs: Unpack[StartExportLabelsTaskRunRequestRequestTypeDef]
    ) -> StartExportLabelsTaskRunResponseTypeDef:
        """
        Begins an asynchronous task to export all labeled data for a particular
        transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/start_export_labels_task_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_export_labels_task_run)
        """

    async def start_import_labels_task_run(
        self, **kwargs: Unpack[StartImportLabelsTaskRunRequestRequestTypeDef]
    ) -> StartImportLabelsTaskRunResponseTypeDef:
        """
        Enables you to provide additional labels (examples of truth) to be used to
        teach the machine learning transform and improve its quality.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/start_import_labels_task_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_import_labels_task_run)
        """

    async def start_job_run(
        self, **kwargs: Unpack[StartJobRunRequestRequestTypeDef]
    ) -> StartJobRunResponseTypeDef:
        """
        Starts a job run using a job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/start_job_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_job_run)
        """

    async def start_ml_evaluation_task_run(
        self, **kwargs: Unpack[StartMLEvaluationTaskRunRequestRequestTypeDef]
    ) -> StartMLEvaluationTaskRunResponseTypeDef:
        """
        Starts a task to estimate the quality of the transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/start_ml_evaluation_task_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_ml_evaluation_task_run)
        """

    async def start_ml_labeling_set_generation_task_run(
        self, **kwargs: Unpack[StartMLLabelingSetGenerationTaskRunRequestRequestTypeDef]
    ) -> StartMLLabelingSetGenerationTaskRunResponseTypeDef:
        """
        Starts the active learning workflow for your machine learning transform to
        improve the transform's quality by generating label sets and adding labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/start_ml_labeling_set_generation_task_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_ml_labeling_set_generation_task_run)
        """

    async def start_trigger(
        self, **kwargs: Unpack[StartTriggerRequestRequestTypeDef]
    ) -> StartTriggerResponseTypeDef:
        """
        Starts an existing trigger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/start_trigger.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_trigger)
        """

    async def start_workflow_run(
        self, **kwargs: Unpack[StartWorkflowRunRequestRequestTypeDef]
    ) -> StartWorkflowRunResponseTypeDef:
        """
        Starts a new run of the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/start_workflow_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_workflow_run)
        """

    async def stop_column_statistics_task_run(
        self, **kwargs: Unpack[StopColumnStatisticsTaskRunRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops a task run for the specified table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/stop_column_statistics_task_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#stop_column_statistics_task_run)
        """

    async def stop_crawler(
        self, **kwargs: Unpack[StopCrawlerRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        If the specified crawler is running, stops the crawl.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/stop_crawler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#stop_crawler)
        """

    async def stop_crawler_schedule(
        self, **kwargs: Unpack[StopCrawlerScheduleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets the schedule state of the specified crawler to <code>NOT_SCHEDULED</code>,
        but does not stop the crawler if it is already running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/stop_crawler_schedule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#stop_crawler_schedule)
        """

    async def stop_session(
        self, **kwargs: Unpack[StopSessionRequestRequestTypeDef]
    ) -> StopSessionResponseTypeDef:
        """
        Stops the session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/stop_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#stop_session)
        """

    async def stop_trigger(
        self, **kwargs: Unpack[StopTriggerRequestRequestTypeDef]
    ) -> StopTriggerResponseTypeDef:
        """
        Stops a specified trigger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/stop_trigger.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#stop_trigger)
        """

    async def stop_workflow_run(
        self, **kwargs: Unpack[StopWorkflowRunRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops the execution of the specified workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/stop_workflow_run.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#stop_workflow_run)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#tag_resource)
        """

    async def test_connection(
        self, **kwargs: Unpack[TestConnectionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Tests a connection to a service to validate the service credentials that you
        provide.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/test_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#test_connection)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#untag_resource)
        """

    async def update_blueprint(
        self, **kwargs: Unpack[UpdateBlueprintRequestRequestTypeDef]
    ) -> UpdateBlueprintResponseTypeDef:
        """
        Updates a registered blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_blueprint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_blueprint)
        """

    async def update_classifier(
        self, **kwargs: Unpack[UpdateClassifierRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Modifies an existing classifier (a <code>GrokClassifier</code>, an
        <code>XMLClassifier</code>, a <code>JsonClassifier</code>, or a
        <code>CsvClassifier</code>, depending on which field is present).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_classifier.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_classifier)
        """

    async def update_column_statistics_for_partition(
        self, **kwargs: Unpack[UpdateColumnStatisticsForPartitionRequestRequestTypeDef]
    ) -> UpdateColumnStatisticsForPartitionResponseTypeDef:
        """
        Creates or updates partition statistics of columns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_column_statistics_for_partition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_column_statistics_for_partition)
        """

    async def update_column_statistics_for_table(
        self, **kwargs: Unpack[UpdateColumnStatisticsForTableRequestRequestTypeDef]
    ) -> UpdateColumnStatisticsForTableResponseTypeDef:
        """
        Creates or updates table statistics of columns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_column_statistics_for_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_column_statistics_for_table)
        """

    async def update_connection(
        self, **kwargs: Unpack[UpdateConnectionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a connection definition in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_connection)
        """

    async def update_crawler(
        self, **kwargs: Unpack[UpdateCrawlerRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a crawler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_crawler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_crawler)
        """

    async def update_crawler_schedule(
        self, **kwargs: Unpack[UpdateCrawlerScheduleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the schedule of a crawler using a <code>cron</code> expression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_crawler_schedule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_crawler_schedule)
        """

    async def update_data_quality_ruleset(
        self, **kwargs: Unpack[UpdateDataQualityRulesetRequestRequestTypeDef]
    ) -> UpdateDataQualityRulesetResponseTypeDef:
        """
        Updates the specified data quality ruleset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_data_quality_ruleset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_data_quality_ruleset)
        """

    async def update_database(
        self, **kwargs: Unpack[UpdateDatabaseRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an existing database definition in a Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_database.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_database)
        """

    async def update_dev_endpoint(
        self, **kwargs: Unpack[UpdateDevEndpointRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a specified development endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_dev_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_dev_endpoint)
        """

    async def update_job(
        self, **kwargs: Unpack[UpdateJobRequestRequestTypeDef]
    ) -> UpdateJobResponseTypeDef:
        """
        Updates an existing job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_job)
        """

    async def update_job_from_source_control(
        self, **kwargs: Unpack[UpdateJobFromSourceControlRequestRequestTypeDef]
    ) -> UpdateJobFromSourceControlResponseTypeDef:
        """
        Synchronizes a job from the source control repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_job_from_source_control.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_job_from_source_control)
        """

    async def update_ml_transform(
        self, **kwargs: Unpack[UpdateMLTransformRequestRequestTypeDef]
    ) -> UpdateMLTransformResponseTypeDef:
        """
        Updates an existing machine learning transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_ml_transform.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_ml_transform)
        """

    async def update_partition(
        self, **kwargs: Unpack[UpdatePartitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a partition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_partition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_partition)
        """

    async def update_registry(
        self, **kwargs: Unpack[UpdateRegistryInputRequestTypeDef]
    ) -> UpdateRegistryResponseTypeDef:
        """
        Updates an existing registry which is used to hold a collection of schemas.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_registry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_registry)
        """

    async def update_schema(
        self, **kwargs: Unpack[UpdateSchemaInputRequestTypeDef]
    ) -> UpdateSchemaResponseTypeDef:
        """
        Updates the description, compatibility setting, or version checkpoint for a
        schema set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_schema.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_schema)
        """

    async def update_source_control_from_job(
        self, **kwargs: Unpack[UpdateSourceControlFromJobRequestRequestTypeDef]
    ) -> UpdateSourceControlFromJobResponseTypeDef:
        """
        Synchronizes a job to the source control repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_source_control_from_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_source_control_from_job)
        """

    async def update_table(
        self, **kwargs: Unpack[UpdateTableRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a metadata table in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_table.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_table)
        """

    async def update_table_optimizer(
        self, **kwargs: Unpack[UpdateTableOptimizerRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the configuration for an existing table optimizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_table_optimizer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_table_optimizer)
        """

    async def update_trigger(
        self, **kwargs: Unpack[UpdateTriggerRequestRequestTypeDef]
    ) -> UpdateTriggerResponseTypeDef:
        """
        Updates a trigger definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_trigger.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_trigger)
        """

    async def update_usage_profile(
        self, **kwargs: Unpack[UpdateUsageProfileRequestRequestTypeDef]
    ) -> UpdateUsageProfileResponseTypeDef:
        """
        Update an Glue usage profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_usage_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_usage_profile)
        """

    async def update_user_defined_function(
        self, **kwargs: Unpack[UpdateUserDefinedFunctionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an existing function definition in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_user_defined_function.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_user_defined_function)
        """

    async def update_workflow(
        self, **kwargs: Unpack[UpdateWorkflowRequestRequestTypeDef]
    ) -> UpdateWorkflowResponseTypeDef:
        """
        Updates an existing workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_workflow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_workflow)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_classifiers"]) -> GetClassifiersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_connections"]) -> GetConnectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_crawler_metrics"]
    ) -> GetCrawlerMetricsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_crawlers"]) -> GetCrawlersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_databases"]) -> GetDatabasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_dev_endpoints"]
    ) -> GetDevEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_job_runs"]) -> GetJobRunsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_jobs"]) -> GetJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_partition_indexes"]
    ) -> GetPartitionIndexesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_partitions"]) -> GetPartitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_policies"]
    ) -> GetResourcePoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_security_configurations"]
    ) -> GetSecurityConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_table_versions"]
    ) -> GetTableVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_tables"]) -> GetTablesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_triggers"]) -> GetTriggersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_user_defined_functions"]
    ) -> GetUserDefinedFunctionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_workflow_runs"]
    ) -> GetWorkflowRunsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_blueprints"]) -> ListBlueprintsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_registries"]) -> ListRegistriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_schema_versions"]
    ) -> ListSchemaVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_schemas"]) -> ListSchemasPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_table_optimizer_runs"]
    ) -> ListTableOptimizerRunsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_triggers"]) -> ListTriggersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_usage_profiles"]
    ) -> ListUsageProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workflows"]) -> ListWorkflowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    async def __aenter__(self) -> "GlueClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/)
        """
