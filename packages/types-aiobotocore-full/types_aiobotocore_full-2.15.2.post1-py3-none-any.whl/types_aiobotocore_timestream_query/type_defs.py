"""
Type annotations for timestream-query service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_query/type_defs/)

Usage::

    ```python
    from types_aiobotocore_timestream_query.type_defs import CancelQueryRequestRequestTypeDef

    data: CancelQueryRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Sequence, Union

from .literals import (
    MeasureValueTypeType,
    QueryPricingModelType,
    S3EncryptionOptionType,
    ScalarMeasureValueTypeType,
    ScalarTypeType,
    ScheduledQueryRunStatusType,
    ScheduledQueryStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "CancelQueryRequestRequestTypeDef",
    "CancelQueryResponseTypeDef",
    "ColumnInfoPaginatorTypeDef",
    "ColumnInfoTypeDef",
    "CreateScheduledQueryRequestRequestTypeDef",
    "CreateScheduledQueryResponseTypeDef",
    "DatumPaginatorTypeDef",
    "DatumTypeDef",
    "DeleteScheduledQueryRequestRequestTypeDef",
    "DescribeAccountSettingsResponseTypeDef",
    "DescribeEndpointsResponseTypeDef",
    "DescribeScheduledQueryRequestRequestTypeDef",
    "DescribeScheduledQueryResponseTypeDef",
    "DimensionMappingTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointTypeDef",
    "ErrorReportConfigurationTypeDef",
    "ErrorReportLocationTypeDef",
    "ExecuteScheduledQueryRequestRequestTypeDef",
    "ExecutionStatsTypeDef",
    "ListScheduledQueriesRequestListScheduledQueriesPaginateTypeDef",
    "ListScheduledQueriesRequestRequestTypeDef",
    "ListScheduledQueriesResponseTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MixedMeasureMappingOutputTypeDef",
    "MixedMeasureMappingTypeDef",
    "MixedMeasureMappingUnionTypeDef",
    "MultiMeasureAttributeMappingTypeDef",
    "MultiMeasureMappingsOutputTypeDef",
    "MultiMeasureMappingsTypeDef",
    "MultiMeasureMappingsUnionTypeDef",
    "NotificationConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterMappingTypeDef",
    "PrepareQueryRequestRequestTypeDef",
    "PrepareQueryResponseTypeDef",
    "QueryRequestQueryPaginateTypeDef",
    "QueryRequestRequestTypeDef",
    "QueryResponsePaginatorTypeDef",
    "QueryResponseTypeDef",
    "QueryStatusTypeDef",
    "ResponseMetadataTypeDef",
    "RowPaginatorTypeDef",
    "RowTypeDef",
    "S3ConfigurationTypeDef",
    "S3ReportLocationTypeDef",
    "ScheduleConfigurationTypeDef",
    "ScheduledQueryDescriptionTypeDef",
    "ScheduledQueryRunSummaryTypeDef",
    "ScheduledQueryTypeDef",
    "SelectColumnTypeDef",
    "SnsConfigurationTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TargetConfigurationOutputTypeDef",
    "TargetConfigurationTypeDef",
    "TargetDestinationTypeDef",
    "TimeSeriesDataPointPaginatorTypeDef",
    "TimeSeriesDataPointTypeDef",
    "TimestampTypeDef",
    "TimestreamConfigurationOutputTypeDef",
    "TimestreamConfigurationTypeDef",
    "TimestreamConfigurationUnionTypeDef",
    "TimestreamDestinationTypeDef",
    "TypePaginatorTypeDef",
    "TypeTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccountSettingsRequestRequestTypeDef",
    "UpdateAccountSettingsResponseTypeDef",
    "UpdateScheduledQueryRequestRequestTypeDef",
)


class CancelQueryRequestRequestTypeDef(TypedDict):
    QueryId: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class TypePaginatorTypeDef(TypedDict):
    ScalarType: NotRequired[ScalarTypeType]
    ArrayColumnInfo: NotRequired[Dict[str, Any]]
    TimeSeriesMeasureValueColumnInfo: NotRequired[Dict[str, Any]]
    RowColumnInfo: NotRequired[List[Dict[str, Any]]]


ColumnInfoTypeDef = TypedDict(
    "ColumnInfoTypeDef",
    {
        "Type": Dict[str, Any],
        "Name": NotRequired[str],
    },
)


class ScheduleConfigurationTypeDef(TypedDict):
    ScheduleExpression: str


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class TimeSeriesDataPointPaginatorTypeDef(TypedDict):
    Time: str
    Value: Dict[str, Any]


class TimeSeriesDataPointTypeDef(TypedDict):
    Time: str
    Value: Dict[str, Any]


class DeleteScheduledQueryRequestRequestTypeDef(TypedDict):
    ScheduledQueryArn: str


class EndpointTypeDef(TypedDict):
    Address: str
    CachePeriodInMinutes: int


class DescribeScheduledQueryRequestRequestTypeDef(TypedDict):
    ScheduledQueryArn: str


class DimensionMappingTypeDef(TypedDict):
    Name: str
    DimensionValueType: Literal["VARCHAR"]


class S3ConfigurationTypeDef(TypedDict):
    BucketName: str
    ObjectKeyPrefix: NotRequired[str]
    EncryptionOption: NotRequired[S3EncryptionOptionType]


class S3ReportLocationTypeDef(TypedDict):
    BucketName: NotRequired[str]
    ObjectKey: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class ExecutionStatsTypeDef(TypedDict):
    ExecutionTimeInMillis: NotRequired[int]
    DataWrites: NotRequired[int]
    BytesMetered: NotRequired[int]
    CumulativeBytesScanned: NotRequired[int]
    RecordsIngested: NotRequired[int]
    QueryResultRows: NotRequired[int]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListScheduledQueriesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class MultiMeasureAttributeMappingTypeDef(TypedDict):
    SourceColumn: str
    MeasureValueType: ScalarMeasureValueTypeType
    TargetMultiMeasureAttributeName: NotRequired[str]


class SnsConfigurationTypeDef(TypedDict):
    TopicArn: str


class PrepareQueryRequestRequestTypeDef(TypedDict):
    QueryString: str
    ValidateOnly: NotRequired[bool]


class QueryRequestRequestTypeDef(TypedDict):
    QueryString: str
    ClientToken: NotRequired[str]
    NextToken: NotRequired[str]
    MaxRows: NotRequired[int]


class QueryStatusTypeDef(TypedDict):
    ProgressPercentage: NotRequired[float]
    CumulativeBytesScanned: NotRequired[int]
    CumulativeBytesMetered: NotRequired[int]


class TimestreamDestinationTypeDef(TypedDict):
    DatabaseName: NotRequired[str]
    TableName: NotRequired[str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


class UpdateAccountSettingsRequestRequestTypeDef(TypedDict):
    MaxQueryTCU: NotRequired[int]
    QueryPricingModel: NotRequired[QueryPricingModelType]


class UpdateScheduledQueryRequestRequestTypeDef(TypedDict):
    ScheduledQueryArn: str
    State: ScheduledQueryStateType


class CancelQueryResponseTypeDef(TypedDict):
    CancellationMessage: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateScheduledQueryResponseTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAccountSettingsResponseTypeDef(TypedDict):
    MaxQueryTCU: int
    QueryPricingModel: QueryPricingModelType
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAccountSettingsResponseTypeDef(TypedDict):
    MaxQueryTCU: int
    QueryPricingModel: QueryPricingModelType
    ResponseMetadata: ResponseMetadataTypeDef


ColumnInfoPaginatorTypeDef = TypedDict(
    "ColumnInfoPaginatorTypeDef",
    {
        "Type": TypePaginatorTypeDef,
        "Name": NotRequired[str],
    },
)


class TypeTypeDef(TypedDict):
    ScalarType: NotRequired[ScalarTypeType]
    ArrayColumnInfo: NotRequired[Dict[str, Any]]
    TimeSeriesMeasureValueColumnInfo: NotRequired[Dict[str, Any]]
    RowColumnInfo: NotRequired[List[ColumnInfoTypeDef]]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


class DatumPaginatorTypeDef(TypedDict):
    ScalarValue: NotRequired[str]
    TimeSeriesValue: NotRequired[List[TimeSeriesDataPointPaginatorTypeDef]]
    ArrayValue: NotRequired[List[Dict[str, Any]]]
    RowValue: NotRequired[Dict[str, Any]]
    NullValue: NotRequired[bool]


class DatumTypeDef(TypedDict):
    ScalarValue: NotRequired[str]
    TimeSeriesValue: NotRequired[List[TimeSeriesDataPointTypeDef]]
    ArrayValue: NotRequired[List[Dict[str, Any]]]
    RowValue: NotRequired[Dict[str, Any]]
    NullValue: NotRequired[bool]


class DescribeEndpointsResponseTypeDef(TypedDict):
    Endpoints: List[EndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ErrorReportConfigurationTypeDef(TypedDict):
    S3Configuration: S3ConfigurationTypeDef


class ErrorReportLocationTypeDef(TypedDict):
    S3ReportLocation: NotRequired[S3ReportLocationTypeDef]


class ExecuteScheduledQueryRequestRequestTypeDef(TypedDict):
    ScheduledQueryArn: str
    InvocationTime: TimestampTypeDef
    ClientToken: NotRequired[str]


class ListScheduledQueriesRequestListScheduledQueriesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(TypedDict):
    ResourceARN: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class QueryRequestQueryPaginateTypeDef(TypedDict):
    QueryString: str
    ClientToken: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class MixedMeasureMappingOutputTypeDef(TypedDict):
    MeasureValueType: MeasureValueTypeType
    MeasureName: NotRequired[str]
    SourceColumn: NotRequired[str]
    TargetMeasureName: NotRequired[str]
    MultiMeasureAttributeMappings: NotRequired[List[MultiMeasureAttributeMappingTypeDef]]


class MixedMeasureMappingTypeDef(TypedDict):
    MeasureValueType: MeasureValueTypeType
    MeasureName: NotRequired[str]
    SourceColumn: NotRequired[str]
    TargetMeasureName: NotRequired[str]
    MultiMeasureAttributeMappings: NotRequired[Sequence[MultiMeasureAttributeMappingTypeDef]]


class MultiMeasureMappingsOutputTypeDef(TypedDict):
    MultiMeasureAttributeMappings: List[MultiMeasureAttributeMappingTypeDef]
    TargetMultiMeasureName: NotRequired[str]


class MultiMeasureMappingsTypeDef(TypedDict):
    MultiMeasureAttributeMappings: Sequence[MultiMeasureAttributeMappingTypeDef]
    TargetMultiMeasureName: NotRequired[str]


class NotificationConfigurationTypeDef(TypedDict):
    SnsConfiguration: SnsConfigurationTypeDef


class TargetDestinationTypeDef(TypedDict):
    TimestreamDestination: NotRequired[TimestreamDestinationTypeDef]


ParameterMappingTypeDef = TypedDict(
    "ParameterMappingTypeDef",
    {
        "Name": str,
        "Type": TypeTypeDef,
    },
)
SelectColumnTypeDef = TypedDict(
    "SelectColumnTypeDef",
    {
        "Name": NotRequired[str],
        "Type": NotRequired[TypeTypeDef],
        "DatabaseName": NotRequired[str],
        "TableName": NotRequired[str],
        "Aliased": NotRequired[bool],
    },
)


class RowPaginatorTypeDef(TypedDict):
    Data: List[DatumPaginatorTypeDef]


class RowTypeDef(TypedDict):
    Data: List[DatumTypeDef]


class ScheduledQueryRunSummaryTypeDef(TypedDict):
    InvocationTime: NotRequired[datetime]
    TriggerTime: NotRequired[datetime]
    RunStatus: NotRequired[ScheduledQueryRunStatusType]
    ExecutionStats: NotRequired[ExecutionStatsTypeDef]
    ErrorReportLocation: NotRequired[ErrorReportLocationTypeDef]
    FailureReason: NotRequired[str]


MixedMeasureMappingUnionTypeDef = Union[
    MixedMeasureMappingTypeDef, MixedMeasureMappingOutputTypeDef
]


class TimestreamConfigurationOutputTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    TimeColumn: str
    DimensionMappings: List[DimensionMappingTypeDef]
    MultiMeasureMappings: NotRequired[MultiMeasureMappingsOutputTypeDef]
    MixedMeasureMappings: NotRequired[List[MixedMeasureMappingOutputTypeDef]]
    MeasureNameColumn: NotRequired[str]


MultiMeasureMappingsUnionTypeDef = Union[
    MultiMeasureMappingsTypeDef, MultiMeasureMappingsOutputTypeDef
]


class ScheduledQueryTypeDef(TypedDict):
    Arn: str
    Name: str
    State: ScheduledQueryStateType
    CreationTime: NotRequired[datetime]
    PreviousInvocationTime: NotRequired[datetime]
    NextInvocationTime: NotRequired[datetime]
    ErrorReportConfiguration: NotRequired[ErrorReportConfigurationTypeDef]
    TargetDestination: NotRequired[TargetDestinationTypeDef]
    LastRunStatus: NotRequired[ScheduledQueryRunStatusType]


class PrepareQueryResponseTypeDef(TypedDict):
    QueryString: str
    Columns: List[SelectColumnTypeDef]
    Parameters: List[ParameterMappingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class QueryResponsePaginatorTypeDef(TypedDict):
    QueryId: str
    Rows: List[RowPaginatorTypeDef]
    ColumnInfo: List[ColumnInfoPaginatorTypeDef]
    QueryStatus: QueryStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class QueryResponseTypeDef(TypedDict):
    QueryId: str
    Rows: List[RowTypeDef]
    ColumnInfo: List[ColumnInfoTypeDef]
    QueryStatus: QueryStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TargetConfigurationOutputTypeDef(TypedDict):
    TimestreamConfiguration: TimestreamConfigurationOutputTypeDef


class TimestreamConfigurationTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    TimeColumn: str
    DimensionMappings: Sequence[DimensionMappingTypeDef]
    MultiMeasureMappings: NotRequired[MultiMeasureMappingsUnionTypeDef]
    MixedMeasureMappings: NotRequired[Sequence[MixedMeasureMappingUnionTypeDef]]
    MeasureNameColumn: NotRequired[str]


class ListScheduledQueriesResponseTypeDef(TypedDict):
    ScheduledQueries: List[ScheduledQueryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ScheduledQueryDescriptionTypeDef(TypedDict):
    Arn: str
    Name: str
    QueryString: str
    State: ScheduledQueryStateType
    ScheduleConfiguration: ScheduleConfigurationTypeDef
    NotificationConfiguration: NotificationConfigurationTypeDef
    CreationTime: NotRequired[datetime]
    PreviousInvocationTime: NotRequired[datetime]
    NextInvocationTime: NotRequired[datetime]
    TargetConfiguration: NotRequired[TargetConfigurationOutputTypeDef]
    ScheduledQueryExecutionRoleArn: NotRequired[str]
    KmsKeyId: NotRequired[str]
    ErrorReportConfiguration: NotRequired[ErrorReportConfigurationTypeDef]
    LastRunSummary: NotRequired[ScheduledQueryRunSummaryTypeDef]
    RecentlyFailedRuns: NotRequired[List[ScheduledQueryRunSummaryTypeDef]]


TimestreamConfigurationUnionTypeDef = Union[
    TimestreamConfigurationTypeDef, TimestreamConfigurationOutputTypeDef
]


class DescribeScheduledQueryResponseTypeDef(TypedDict):
    ScheduledQuery: ScheduledQueryDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TargetConfigurationTypeDef(TypedDict):
    TimestreamConfiguration: TimestreamConfigurationUnionTypeDef


class CreateScheduledQueryRequestRequestTypeDef(TypedDict):
    Name: str
    QueryString: str
    ScheduleConfiguration: ScheduleConfigurationTypeDef
    NotificationConfiguration: NotificationConfigurationTypeDef
    ScheduledQueryExecutionRoleArn: str
    ErrorReportConfiguration: ErrorReportConfigurationTypeDef
    TargetConfiguration: NotRequired[TargetConfigurationTypeDef]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    KmsKeyId: NotRequired[str]
