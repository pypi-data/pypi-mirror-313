"""
Type annotations for cleanroomsml service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/type_defs/)

Usage::

    ```python
    from types_aiobotocore_cleanroomsml.type_defs import S3ConfigMapTypeDef

    data: S3ConfigMapTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AudienceExportJobStatusType,
    AudienceGenerationJobStatusType,
    AudienceModelStatusType,
    AudienceSizeTypeType,
    ColumnTypeType,
    PolicyExistenceConditionType,
    SharedAudienceMetricsType,
    TagOnCreatePolicyType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AudienceDestinationTypeDef",
    "AudienceExportJobSummaryTypeDef",
    "AudienceGenerationJobDataSourceOutputTypeDef",
    "AudienceGenerationJobDataSourceTypeDef",
    "AudienceGenerationJobSummaryTypeDef",
    "AudienceModelSummaryTypeDef",
    "AudienceQualityMetricsTypeDef",
    "AudienceSizeConfigOutputTypeDef",
    "AudienceSizeConfigTypeDef",
    "AudienceSizeTypeDef",
    "ColumnSchemaOutputTypeDef",
    "ColumnSchemaTypeDef",
    "ColumnSchemaUnionTypeDef",
    "ConfiguredAudienceModelOutputConfigTypeDef",
    "ConfiguredAudienceModelSummaryTypeDef",
    "CreateAudienceModelRequestRequestTypeDef",
    "CreateAudienceModelResponseTypeDef",
    "CreateConfiguredAudienceModelRequestRequestTypeDef",
    "CreateConfiguredAudienceModelResponseTypeDef",
    "CreateTrainingDatasetRequestRequestTypeDef",
    "CreateTrainingDatasetResponseTypeDef",
    "DataSourceTypeDef",
    "DatasetInputConfigOutputTypeDef",
    "DatasetInputConfigTypeDef",
    "DatasetInputConfigUnionTypeDef",
    "DatasetOutputTypeDef",
    "DatasetTypeDef",
    "DatasetUnionTypeDef",
    "DeleteAudienceGenerationJobRequestRequestTypeDef",
    "DeleteAudienceModelRequestRequestTypeDef",
    "DeleteConfiguredAudienceModelPolicyRequestRequestTypeDef",
    "DeleteConfiguredAudienceModelRequestRequestTypeDef",
    "DeleteTrainingDatasetRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetAudienceGenerationJobRequestRequestTypeDef",
    "GetAudienceGenerationJobResponseTypeDef",
    "GetAudienceModelRequestRequestTypeDef",
    "GetAudienceModelResponseTypeDef",
    "GetConfiguredAudienceModelPolicyRequestRequestTypeDef",
    "GetConfiguredAudienceModelPolicyResponseTypeDef",
    "GetConfiguredAudienceModelRequestRequestTypeDef",
    "GetConfiguredAudienceModelResponseTypeDef",
    "GetTrainingDatasetRequestRequestTypeDef",
    "GetTrainingDatasetResponseTypeDef",
    "GlueDataSourceTypeDef",
    "ListAudienceExportJobsRequestListAudienceExportJobsPaginateTypeDef",
    "ListAudienceExportJobsRequestRequestTypeDef",
    "ListAudienceExportJobsResponseTypeDef",
    "ListAudienceGenerationJobsRequestListAudienceGenerationJobsPaginateTypeDef",
    "ListAudienceGenerationJobsRequestRequestTypeDef",
    "ListAudienceGenerationJobsResponseTypeDef",
    "ListAudienceModelsRequestListAudienceModelsPaginateTypeDef",
    "ListAudienceModelsRequestRequestTypeDef",
    "ListAudienceModelsResponseTypeDef",
    "ListConfiguredAudienceModelsRequestListConfiguredAudienceModelsPaginateTypeDef",
    "ListConfiguredAudienceModelsRequestRequestTypeDef",
    "ListConfiguredAudienceModelsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTrainingDatasetsRequestListTrainingDatasetsPaginateTypeDef",
    "ListTrainingDatasetsRequestRequestTypeDef",
    "ListTrainingDatasetsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ProtectedQuerySQLParametersOutputTypeDef",
    "ProtectedQuerySQLParametersTypeDef",
    "ProtectedQuerySQLParametersUnionTypeDef",
    "PutConfiguredAudienceModelPolicyRequestRequestTypeDef",
    "PutConfiguredAudienceModelPolicyResponseTypeDef",
    "RelevanceMetricTypeDef",
    "ResponseMetadataTypeDef",
    "S3ConfigMapTypeDef",
    "StartAudienceExportJobRequestRequestTypeDef",
    "StartAudienceGenerationJobRequestRequestTypeDef",
    "StartAudienceGenerationJobResponseTypeDef",
    "StatusDetailsTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampTypeDef",
    "TrainingDatasetSummaryTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateConfiguredAudienceModelRequestRequestTypeDef",
    "UpdateConfiguredAudienceModelResponseTypeDef",
)

class S3ConfigMapTypeDef(TypedDict):
    s3Uri: str

AudienceSizeTypeDef = TypedDict(
    "AudienceSizeTypeDef",
    {
        "type": AudienceSizeTypeType,
        "value": int,
    },
)

class StatusDetailsTypeDef(TypedDict):
    statusCode: NotRequired[str]
    message: NotRequired[str]

class ProtectedQuerySQLParametersOutputTypeDef(TypedDict):
    queryString: NotRequired[str]
    analysisTemplateArn: NotRequired[str]
    parameters: NotRequired[Dict[str, str]]

class AudienceGenerationJobSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    audienceGenerationJobArn: str
    name: str
    status: AudienceGenerationJobStatusType
    configuredAudienceModelArn: str
    description: NotRequired[str]
    collaborationId: NotRequired[str]
    startedBy: NotRequired[str]

class AudienceModelSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    audienceModelArn: str
    name: str
    trainingDatasetArn: str
    status: AudienceModelStatusType
    description: NotRequired[str]

class AudienceSizeConfigOutputTypeDef(TypedDict):
    audienceSizeType: AudienceSizeTypeType
    audienceSizeBins: List[int]

class AudienceSizeConfigTypeDef(TypedDict):
    audienceSizeType: AudienceSizeTypeType
    audienceSizeBins: Sequence[int]

class ColumnSchemaOutputTypeDef(TypedDict):
    columnName: str
    columnTypes: List[ColumnTypeType]

class ColumnSchemaTypeDef(TypedDict):
    columnName: str
    columnTypes: Sequence[ColumnTypeType]

TimestampTypeDef = Union[datetime, str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class GlueDataSourceTypeDef(TypedDict):
    tableName: str
    databaseName: str
    catalogId: NotRequired[str]

class DeleteAudienceGenerationJobRequestRequestTypeDef(TypedDict):
    audienceGenerationJobArn: str

class DeleteAudienceModelRequestRequestTypeDef(TypedDict):
    audienceModelArn: str

class DeleteConfiguredAudienceModelPolicyRequestRequestTypeDef(TypedDict):
    configuredAudienceModelArn: str

class DeleteConfiguredAudienceModelRequestRequestTypeDef(TypedDict):
    configuredAudienceModelArn: str

class DeleteTrainingDatasetRequestRequestTypeDef(TypedDict):
    trainingDatasetArn: str

class GetAudienceGenerationJobRequestRequestTypeDef(TypedDict):
    audienceGenerationJobArn: str

class GetAudienceModelRequestRequestTypeDef(TypedDict):
    audienceModelArn: str

class GetConfiguredAudienceModelPolicyRequestRequestTypeDef(TypedDict):
    configuredAudienceModelArn: str

class GetConfiguredAudienceModelRequestRequestTypeDef(TypedDict):
    configuredAudienceModelArn: str

class GetTrainingDatasetRequestRequestTypeDef(TypedDict):
    trainingDatasetArn: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAudienceExportJobsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    audienceGenerationJobArn: NotRequired[str]

class ListAudienceGenerationJobsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    configuredAudienceModelArn: NotRequired[str]
    collaborationId: NotRequired[str]

class ListAudienceModelsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListConfiguredAudienceModelsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class ListTrainingDatasetsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class TrainingDatasetSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    trainingDatasetArn: str
    name: str
    status: Literal["ACTIVE"]
    description: NotRequired[str]

class ProtectedQuerySQLParametersTypeDef(TypedDict):
    queryString: NotRequired[str]
    analysisTemplateArn: NotRequired[str]
    parameters: NotRequired[Mapping[str, str]]

class PutConfiguredAudienceModelPolicyRequestRequestTypeDef(TypedDict):
    configuredAudienceModelArn: str
    configuredAudienceModelPolicy: str
    previousPolicyHash: NotRequired[str]
    policyExistenceCondition: NotRequired[PolicyExistenceConditionType]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class AudienceDestinationTypeDef(TypedDict):
    s3Destination: S3ConfigMapTypeDef

class RelevanceMetricTypeDef(TypedDict):
    audienceSize: AudienceSizeTypeDef
    score: NotRequired[float]

class StartAudienceExportJobRequestRequestTypeDef(TypedDict):
    name: str
    audienceGenerationJobArn: str
    audienceSize: AudienceSizeTypeDef
    description: NotRequired[str]

class AudienceExportJobSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    name: str
    audienceGenerationJobArn: str
    audienceSize: AudienceSizeTypeDef
    status: AudienceExportJobStatusType
    description: NotRequired[str]
    statusDetails: NotRequired[StatusDetailsTypeDef]
    outputLocation: NotRequired[str]

class AudienceGenerationJobDataSourceOutputTypeDef(TypedDict):
    roleArn: str
    dataSource: NotRequired[S3ConfigMapTypeDef]
    sqlParameters: NotRequired[ProtectedQuerySQLParametersOutputTypeDef]

ColumnSchemaUnionTypeDef = Union[ColumnSchemaTypeDef, ColumnSchemaOutputTypeDef]

class CreateAudienceModelRequestRequestTypeDef(TypedDict):
    name: str
    trainingDatasetArn: str
    trainingDataStartTime: NotRequired[TimestampTypeDef]
    trainingDataEndTime: NotRequired[TimestampTypeDef]
    kmsKeyArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    description: NotRequired[str]

class CreateAudienceModelResponseTypeDef(TypedDict):
    audienceModelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateConfiguredAudienceModelResponseTypeDef(TypedDict):
    configuredAudienceModelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTrainingDatasetResponseTypeDef(TypedDict):
    trainingDatasetArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetAudienceModelResponseTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    trainingDataStartTime: datetime
    trainingDataEndTime: datetime
    audienceModelArn: str
    name: str
    trainingDatasetArn: str
    status: AudienceModelStatusType
    statusDetails: StatusDetailsTypeDef
    kmsKeyArn: str
    tags: Dict[str, str]
    description: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetConfiguredAudienceModelPolicyResponseTypeDef(TypedDict):
    configuredAudienceModelArn: str
    configuredAudienceModelPolicy: str
    policyHash: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAudienceGenerationJobsResponseTypeDef(TypedDict):
    audienceGenerationJobs: List[AudienceGenerationJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAudienceModelsResponseTypeDef(TypedDict):
    audienceModels: List[AudienceModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PutConfiguredAudienceModelPolicyResponseTypeDef(TypedDict):
    configuredAudienceModelPolicy: str
    policyHash: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartAudienceGenerationJobResponseTypeDef(TypedDict):
    audienceGenerationJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConfiguredAudienceModelResponseTypeDef(TypedDict):
    configuredAudienceModelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DataSourceTypeDef(TypedDict):
    glueDataSource: GlueDataSourceTypeDef

class ListAudienceExportJobsRequestListAudienceExportJobsPaginateTypeDef(TypedDict):
    audienceGenerationJobArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAudienceGenerationJobsRequestListAudienceGenerationJobsPaginateTypeDef(TypedDict):
    configuredAudienceModelArn: NotRequired[str]
    collaborationId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAudienceModelsRequestListAudienceModelsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConfiguredAudienceModelsRequestListConfiguredAudienceModelsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTrainingDatasetsRequestListTrainingDatasetsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTrainingDatasetsResponseTypeDef(TypedDict):
    trainingDatasets: List[TrainingDatasetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

ProtectedQuerySQLParametersUnionTypeDef = Union[
    ProtectedQuerySQLParametersTypeDef, ProtectedQuerySQLParametersOutputTypeDef
]

class ConfiguredAudienceModelOutputConfigTypeDef(TypedDict):
    destination: AudienceDestinationTypeDef
    roleArn: str

class AudienceQualityMetricsTypeDef(TypedDict):
    relevanceMetrics: List[RelevanceMetricTypeDef]
    recallMetric: NotRequired[float]

class ListAudienceExportJobsResponseTypeDef(TypedDict):
    audienceExportJobs: List[AudienceExportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DatasetInputConfigOutputTypeDef(TypedDict):
    schema: List[ColumnSchemaOutputTypeDef]
    dataSource: DataSourceTypeDef

class DatasetInputConfigTypeDef(TypedDict):
    schema: Sequence[ColumnSchemaUnionTypeDef]
    dataSource: DataSourceTypeDef

class AudienceGenerationJobDataSourceTypeDef(TypedDict):
    roleArn: str
    dataSource: NotRequired[S3ConfigMapTypeDef]
    sqlParameters: NotRequired[ProtectedQuerySQLParametersUnionTypeDef]

class ConfiguredAudienceModelSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    name: str
    audienceModelArn: str
    outputConfig: ConfiguredAudienceModelOutputConfigTypeDef
    configuredAudienceModelArn: str
    status: Literal["ACTIVE"]
    description: NotRequired[str]

class CreateConfiguredAudienceModelRequestRequestTypeDef(TypedDict):
    name: str
    audienceModelArn: str
    outputConfig: ConfiguredAudienceModelOutputConfigTypeDef
    sharedAudienceMetrics: Sequence[SharedAudienceMetricsType]
    description: NotRequired[str]
    minMatchingSeedSize: NotRequired[int]
    audienceSizeConfig: NotRequired[AudienceSizeConfigTypeDef]
    tags: NotRequired[Mapping[str, str]]
    childResourceTagOnCreatePolicy: NotRequired[TagOnCreatePolicyType]

class GetConfiguredAudienceModelResponseTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    configuredAudienceModelArn: str
    name: str
    audienceModelArn: str
    outputConfig: ConfiguredAudienceModelOutputConfigTypeDef
    description: str
    status: Literal["ACTIVE"]
    sharedAudienceMetrics: List[SharedAudienceMetricsType]
    minMatchingSeedSize: int
    audienceSizeConfig: AudienceSizeConfigOutputTypeDef
    tags: Dict[str, str]
    childResourceTagOnCreatePolicy: TagOnCreatePolicyType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConfiguredAudienceModelRequestRequestTypeDef(TypedDict):
    configuredAudienceModelArn: str
    outputConfig: NotRequired[ConfiguredAudienceModelOutputConfigTypeDef]
    audienceModelArn: NotRequired[str]
    sharedAudienceMetrics: NotRequired[Sequence[SharedAudienceMetricsType]]
    minMatchingSeedSize: NotRequired[int]
    audienceSizeConfig: NotRequired[AudienceSizeConfigTypeDef]
    description: NotRequired[str]

class GetAudienceGenerationJobResponseTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    audienceGenerationJobArn: str
    name: str
    description: str
    status: AudienceGenerationJobStatusType
    statusDetails: StatusDetailsTypeDef
    configuredAudienceModelArn: str
    seedAudience: AudienceGenerationJobDataSourceOutputTypeDef
    includeSeedInOutput: bool
    collaborationId: str
    metrics: AudienceQualityMetricsTypeDef
    startedBy: str
    tags: Dict[str, str]
    protectedQueryIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

DatasetOutputTypeDef = TypedDict(
    "DatasetOutputTypeDef",
    {
        "type": Literal["INTERACTIONS"],
        "inputConfig": DatasetInputConfigOutputTypeDef,
    },
)
DatasetInputConfigUnionTypeDef = Union[DatasetInputConfigTypeDef, DatasetInputConfigOutputTypeDef]

class StartAudienceGenerationJobRequestRequestTypeDef(TypedDict):
    name: str
    configuredAudienceModelArn: str
    seedAudience: AudienceGenerationJobDataSourceTypeDef
    includeSeedInOutput: NotRequired[bool]
    collaborationId: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class ListConfiguredAudienceModelsResponseTypeDef(TypedDict):
    configuredAudienceModels: List[ConfiguredAudienceModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetTrainingDatasetResponseTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    trainingDatasetArn: str
    name: str
    trainingData: List[DatasetOutputTypeDef]
    status: Literal["ACTIVE"]
    roleArn: str
    tags: Dict[str, str]
    description: str
    ResponseMetadata: ResponseMetadataTypeDef

DatasetTypeDef = TypedDict(
    "DatasetTypeDef",
    {
        "type": Literal["INTERACTIONS"],
        "inputConfig": DatasetInputConfigUnionTypeDef,
    },
)
DatasetUnionTypeDef = Union[DatasetTypeDef, DatasetOutputTypeDef]

class CreateTrainingDatasetRequestRequestTypeDef(TypedDict):
    name: str
    roleArn: str
    trainingData: Sequence[DatasetUnionTypeDef]
    tags: NotRequired[Mapping[str, str]]
    description: NotRequired[str]
