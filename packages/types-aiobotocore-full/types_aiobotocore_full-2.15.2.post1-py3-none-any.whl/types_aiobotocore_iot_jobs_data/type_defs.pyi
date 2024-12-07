"""
Type annotations for iot-jobs-data service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_jobs_data/type_defs/)

Usage::

    ```python
    from types_aiobotocore_iot_jobs_data.type_defs import DescribeJobExecutionRequestRequestTypeDef

    data: DescribeJobExecutionRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Mapping

from .literals import JobExecutionStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "DescribeJobExecutionRequestRequestTypeDef",
    "DescribeJobExecutionResponseTypeDef",
    "GetPendingJobExecutionsRequestRequestTypeDef",
    "GetPendingJobExecutionsResponseTypeDef",
    "JobExecutionStateTypeDef",
    "JobExecutionSummaryTypeDef",
    "JobExecutionTypeDef",
    "ResponseMetadataTypeDef",
    "StartNextPendingJobExecutionRequestRequestTypeDef",
    "StartNextPendingJobExecutionResponseTypeDef",
    "UpdateJobExecutionRequestRequestTypeDef",
    "UpdateJobExecutionResponseTypeDef",
)

class DescribeJobExecutionRequestRequestTypeDef(TypedDict):
    jobId: str
    thingName: str
    includeJobDocument: NotRequired[bool]
    executionNumber: NotRequired[int]

class JobExecutionTypeDef(TypedDict):
    jobId: NotRequired[str]
    thingName: NotRequired[str]
    status: NotRequired[JobExecutionStatusType]
    statusDetails: NotRequired[Dict[str, str]]
    queuedAt: NotRequired[int]
    startedAt: NotRequired[int]
    lastUpdatedAt: NotRequired[int]
    approximateSecondsBeforeTimedOut: NotRequired[int]
    versionNumber: NotRequired[int]
    executionNumber: NotRequired[int]
    jobDocument: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class GetPendingJobExecutionsRequestRequestTypeDef(TypedDict):
    thingName: str

class JobExecutionSummaryTypeDef(TypedDict):
    jobId: NotRequired[str]
    queuedAt: NotRequired[int]
    startedAt: NotRequired[int]
    lastUpdatedAt: NotRequired[int]
    versionNumber: NotRequired[int]
    executionNumber: NotRequired[int]

class JobExecutionStateTypeDef(TypedDict):
    status: NotRequired[JobExecutionStatusType]
    statusDetails: NotRequired[Dict[str, str]]
    versionNumber: NotRequired[int]

class StartNextPendingJobExecutionRequestRequestTypeDef(TypedDict):
    thingName: str
    statusDetails: NotRequired[Mapping[str, str]]
    stepTimeoutInMinutes: NotRequired[int]

class UpdateJobExecutionRequestRequestTypeDef(TypedDict):
    jobId: str
    thingName: str
    status: JobExecutionStatusType
    statusDetails: NotRequired[Mapping[str, str]]
    stepTimeoutInMinutes: NotRequired[int]
    expectedVersion: NotRequired[int]
    includeJobExecutionState: NotRequired[bool]
    includeJobDocument: NotRequired[bool]
    executionNumber: NotRequired[int]

class DescribeJobExecutionResponseTypeDef(TypedDict):
    execution: JobExecutionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartNextPendingJobExecutionResponseTypeDef(TypedDict):
    execution: JobExecutionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetPendingJobExecutionsResponseTypeDef(TypedDict):
    inProgressJobs: List[JobExecutionSummaryTypeDef]
    queuedJobs: List[JobExecutionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateJobExecutionResponseTypeDef(TypedDict):
    executionState: JobExecutionStateTypeDef
    jobDocument: str
    ResponseMetadata: ResponseMetadataTypeDef
