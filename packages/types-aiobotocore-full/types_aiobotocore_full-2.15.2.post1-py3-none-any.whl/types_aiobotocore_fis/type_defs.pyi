"""
Type annotations for fis service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/type_defs/)

Usage::

    ```python
    from types_aiobotocore_fis.type_defs import ActionParameterTypeDef

    data: ActionParameterTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AccountTargetingType,
    ActionsModeType,
    EmptyTargetResolutionModeType,
    ExperimentActionStatusType,
    ExperimentStatusType,
    SafetyLeverStatusInputType,
    SafetyLeverStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ActionParameterTypeDef",
    "ActionSummaryTypeDef",
    "ActionTargetTypeDef",
    "ActionTypeDef",
    "CreateExperimentTemplateActionInputTypeDef",
    "CreateExperimentTemplateExperimentOptionsInputTypeDef",
    "CreateExperimentTemplateLogConfigurationInputTypeDef",
    "CreateExperimentTemplateRequestRequestTypeDef",
    "CreateExperimentTemplateResponseTypeDef",
    "CreateExperimentTemplateStopConditionInputTypeDef",
    "CreateExperimentTemplateTargetInputTypeDef",
    "CreateTargetAccountConfigurationRequestRequestTypeDef",
    "CreateTargetAccountConfigurationResponseTypeDef",
    "DeleteExperimentTemplateRequestRequestTypeDef",
    "DeleteExperimentTemplateResponseTypeDef",
    "DeleteTargetAccountConfigurationRequestRequestTypeDef",
    "DeleteTargetAccountConfigurationResponseTypeDef",
    "ExperimentActionStateTypeDef",
    "ExperimentActionTypeDef",
    "ExperimentCloudWatchLogsLogConfigurationTypeDef",
    "ExperimentErrorTypeDef",
    "ExperimentLogConfigurationTypeDef",
    "ExperimentOptionsTypeDef",
    "ExperimentS3LogConfigurationTypeDef",
    "ExperimentStateTypeDef",
    "ExperimentStopConditionTypeDef",
    "ExperimentSummaryTypeDef",
    "ExperimentTargetAccountConfigurationSummaryTypeDef",
    "ExperimentTargetAccountConfigurationTypeDef",
    "ExperimentTargetFilterTypeDef",
    "ExperimentTargetTypeDef",
    "ExperimentTemplateActionTypeDef",
    "ExperimentTemplateCloudWatchLogsLogConfigurationInputTypeDef",
    "ExperimentTemplateCloudWatchLogsLogConfigurationTypeDef",
    "ExperimentTemplateExperimentOptionsTypeDef",
    "ExperimentTemplateLogConfigurationTypeDef",
    "ExperimentTemplateS3LogConfigurationInputTypeDef",
    "ExperimentTemplateS3LogConfigurationTypeDef",
    "ExperimentTemplateStopConditionTypeDef",
    "ExperimentTemplateSummaryTypeDef",
    "ExperimentTemplateTargetFilterTypeDef",
    "ExperimentTemplateTargetInputFilterTypeDef",
    "ExperimentTemplateTargetTypeDef",
    "ExperimentTemplateTypeDef",
    "ExperimentTypeDef",
    "GetActionRequestRequestTypeDef",
    "GetActionResponseTypeDef",
    "GetExperimentRequestRequestTypeDef",
    "GetExperimentResponseTypeDef",
    "GetExperimentTargetAccountConfigurationRequestRequestTypeDef",
    "GetExperimentTargetAccountConfigurationResponseTypeDef",
    "GetExperimentTemplateRequestRequestTypeDef",
    "GetExperimentTemplateResponseTypeDef",
    "GetSafetyLeverRequestRequestTypeDef",
    "GetSafetyLeverResponseTypeDef",
    "GetTargetAccountConfigurationRequestRequestTypeDef",
    "GetTargetAccountConfigurationResponseTypeDef",
    "GetTargetResourceTypeRequestRequestTypeDef",
    "GetTargetResourceTypeResponseTypeDef",
    "ListActionsRequestRequestTypeDef",
    "ListActionsResponseTypeDef",
    "ListExperimentResolvedTargetsRequestRequestTypeDef",
    "ListExperimentResolvedTargetsResponseTypeDef",
    "ListExperimentTargetAccountConfigurationsRequestRequestTypeDef",
    "ListExperimentTargetAccountConfigurationsResponseTypeDef",
    "ListExperimentTemplatesRequestRequestTypeDef",
    "ListExperimentTemplatesResponseTypeDef",
    "ListExperimentsRequestRequestTypeDef",
    "ListExperimentsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTargetAccountConfigurationsRequestRequestTypeDef",
    "ListTargetAccountConfigurationsResponseTypeDef",
    "ListTargetResourceTypesRequestRequestTypeDef",
    "ListTargetResourceTypesResponseTypeDef",
    "ResolvedTargetTypeDef",
    "ResponseMetadataTypeDef",
    "SafetyLeverStateTypeDef",
    "SafetyLeverTypeDef",
    "StartExperimentExperimentOptionsInputTypeDef",
    "StartExperimentRequestRequestTypeDef",
    "StartExperimentResponseTypeDef",
    "StopExperimentRequestRequestTypeDef",
    "StopExperimentResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TargetAccountConfigurationSummaryTypeDef",
    "TargetAccountConfigurationTypeDef",
    "TargetResourceTypeParameterTypeDef",
    "TargetResourceTypeSummaryTypeDef",
    "TargetResourceTypeTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateExperimentTemplateActionInputItemTypeDef",
    "UpdateExperimentTemplateExperimentOptionsInputTypeDef",
    "UpdateExperimentTemplateLogConfigurationInputTypeDef",
    "UpdateExperimentTemplateRequestRequestTypeDef",
    "UpdateExperimentTemplateResponseTypeDef",
    "UpdateExperimentTemplateStopConditionInputTypeDef",
    "UpdateExperimentTemplateTargetInputTypeDef",
    "UpdateSafetyLeverStateInputTypeDef",
    "UpdateSafetyLeverStateRequestRequestTypeDef",
    "UpdateSafetyLeverStateResponseTypeDef",
    "UpdateTargetAccountConfigurationRequestRequestTypeDef",
    "UpdateTargetAccountConfigurationResponseTypeDef",
)

class ActionParameterTypeDef(TypedDict):
    description: NotRequired[str]
    required: NotRequired[bool]

class ActionTargetTypeDef(TypedDict):
    resourceType: NotRequired[str]

class CreateExperimentTemplateActionInputTypeDef(TypedDict):
    actionId: str
    description: NotRequired[str]
    parameters: NotRequired[Mapping[str, str]]
    targets: NotRequired[Mapping[str, str]]
    startAfter: NotRequired[Sequence[str]]

class CreateExperimentTemplateExperimentOptionsInputTypeDef(TypedDict):
    accountTargeting: NotRequired[AccountTargetingType]
    emptyTargetResolutionMode: NotRequired[EmptyTargetResolutionModeType]

class ExperimentTemplateCloudWatchLogsLogConfigurationInputTypeDef(TypedDict):
    logGroupArn: str

class ExperimentTemplateS3LogConfigurationInputTypeDef(TypedDict):
    bucketName: str
    prefix: NotRequired[str]

class CreateExperimentTemplateStopConditionInputTypeDef(TypedDict):
    source: str
    value: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ExperimentTemplateTargetInputFilterTypeDef(TypedDict):
    path: str
    values: Sequence[str]

class CreateTargetAccountConfigurationRequestRequestTypeDef(TypedDict):
    experimentTemplateId: str
    accountId: str
    roleArn: str
    clientToken: NotRequired[str]
    description: NotRequired[str]

class TargetAccountConfigurationTypeDef(TypedDict):
    roleArn: NotRequired[str]
    accountId: NotRequired[str]
    description: NotRequired[str]

DeleteExperimentTemplateRequestRequestTypeDef = TypedDict(
    "DeleteExperimentTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)

class DeleteTargetAccountConfigurationRequestRequestTypeDef(TypedDict):
    experimentTemplateId: str
    accountId: str

class ExperimentActionStateTypeDef(TypedDict):
    status: NotRequired[ExperimentActionStatusType]
    reason: NotRequired[str]

class ExperimentCloudWatchLogsLogConfigurationTypeDef(TypedDict):
    logGroupArn: NotRequired[str]

class ExperimentErrorTypeDef(TypedDict):
    accountId: NotRequired[str]
    code: NotRequired[str]
    location: NotRequired[str]

class ExperimentS3LogConfigurationTypeDef(TypedDict):
    bucketName: NotRequired[str]
    prefix: NotRequired[str]

class ExperimentOptionsTypeDef(TypedDict):
    accountTargeting: NotRequired[AccountTargetingType]
    emptyTargetResolutionMode: NotRequired[EmptyTargetResolutionModeType]
    actionsMode: NotRequired[ActionsModeType]

class ExperimentStopConditionTypeDef(TypedDict):
    source: NotRequired[str]
    value: NotRequired[str]

class ExperimentTargetAccountConfigurationSummaryTypeDef(TypedDict):
    roleArn: NotRequired[str]
    accountId: NotRequired[str]
    description: NotRequired[str]

class ExperimentTargetAccountConfigurationTypeDef(TypedDict):
    roleArn: NotRequired[str]
    accountId: NotRequired[str]
    description: NotRequired[str]

class ExperimentTargetFilterTypeDef(TypedDict):
    path: NotRequired[str]
    values: NotRequired[List[str]]

class ExperimentTemplateActionTypeDef(TypedDict):
    actionId: NotRequired[str]
    description: NotRequired[str]
    parameters: NotRequired[Dict[str, str]]
    targets: NotRequired[Dict[str, str]]
    startAfter: NotRequired[List[str]]

class ExperimentTemplateCloudWatchLogsLogConfigurationTypeDef(TypedDict):
    logGroupArn: NotRequired[str]

class ExperimentTemplateExperimentOptionsTypeDef(TypedDict):
    accountTargeting: NotRequired[AccountTargetingType]
    emptyTargetResolutionMode: NotRequired[EmptyTargetResolutionModeType]

class ExperimentTemplateS3LogConfigurationTypeDef(TypedDict):
    bucketName: NotRequired[str]
    prefix: NotRequired[str]

class ExperimentTemplateStopConditionTypeDef(TypedDict):
    source: NotRequired[str]
    value: NotRequired[str]

ExperimentTemplateSummaryTypeDef = TypedDict(
    "ExperimentTemplateSummaryTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "description": NotRequired[str],
        "creationTime": NotRequired[datetime],
        "lastUpdateTime": NotRequired[datetime],
        "tags": NotRequired[Dict[str, str]],
    },
)

class ExperimentTemplateTargetFilterTypeDef(TypedDict):
    path: NotRequired[str]
    values: NotRequired[List[str]]

GetActionRequestRequestTypeDef = TypedDict(
    "GetActionRequestRequestTypeDef",
    {
        "id": str,
    },
)
GetExperimentRequestRequestTypeDef = TypedDict(
    "GetExperimentRequestRequestTypeDef",
    {
        "id": str,
    },
)

class GetExperimentTargetAccountConfigurationRequestRequestTypeDef(TypedDict):
    experimentId: str
    accountId: str

GetExperimentTemplateRequestRequestTypeDef = TypedDict(
    "GetExperimentTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)
GetSafetyLeverRequestRequestTypeDef = TypedDict(
    "GetSafetyLeverRequestRequestTypeDef",
    {
        "id": str,
    },
)

class GetTargetAccountConfigurationRequestRequestTypeDef(TypedDict):
    experimentTemplateId: str
    accountId: str

class GetTargetResourceTypeRequestRequestTypeDef(TypedDict):
    resourceType: str

class ListActionsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListExperimentResolvedTargetsRequestRequestTypeDef(TypedDict):
    experimentId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    targetName: NotRequired[str]

class ResolvedTargetTypeDef(TypedDict):
    resourceType: NotRequired[str]
    targetName: NotRequired[str]
    targetInformation: NotRequired[Dict[str, str]]

class ListExperimentTargetAccountConfigurationsRequestRequestTypeDef(TypedDict):
    experimentId: str
    nextToken: NotRequired[str]

class ListExperimentTemplatesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListExperimentsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    experimentTemplateId: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class ListTargetAccountConfigurationsRequestRequestTypeDef(TypedDict):
    experimentTemplateId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class TargetAccountConfigurationSummaryTypeDef(TypedDict):
    roleArn: NotRequired[str]
    accountId: NotRequired[str]
    description: NotRequired[str]

class ListTargetResourceTypesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class TargetResourceTypeSummaryTypeDef(TypedDict):
    resourceType: NotRequired[str]
    description: NotRequired[str]

class SafetyLeverStateTypeDef(TypedDict):
    status: NotRequired[SafetyLeverStatusType]
    reason: NotRequired[str]

class StartExperimentExperimentOptionsInputTypeDef(TypedDict):
    actionsMode: NotRequired[ActionsModeType]

StopExperimentRequestRequestTypeDef = TypedDict(
    "StopExperimentRequestRequestTypeDef",
    {
        "id": str,
    },
)

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class TargetResourceTypeParameterTypeDef(TypedDict):
    description: NotRequired[str]
    required: NotRequired[bool]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: NotRequired[Sequence[str]]

class UpdateExperimentTemplateActionInputItemTypeDef(TypedDict):
    actionId: NotRequired[str]
    description: NotRequired[str]
    parameters: NotRequired[Mapping[str, str]]
    targets: NotRequired[Mapping[str, str]]
    startAfter: NotRequired[Sequence[str]]

class UpdateExperimentTemplateExperimentOptionsInputTypeDef(TypedDict):
    emptyTargetResolutionMode: NotRequired[EmptyTargetResolutionModeType]

class UpdateExperimentTemplateStopConditionInputTypeDef(TypedDict):
    source: str
    value: NotRequired[str]

class UpdateSafetyLeverStateInputTypeDef(TypedDict):
    status: SafetyLeverStatusInputType
    reason: str

class UpdateTargetAccountConfigurationRequestRequestTypeDef(TypedDict):
    experimentTemplateId: str
    accountId: str
    roleArn: NotRequired[str]
    description: NotRequired[str]

ActionSummaryTypeDef = TypedDict(
    "ActionSummaryTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "description": NotRequired[str],
        "targets": NotRequired[Dict[str, ActionTargetTypeDef]],
        "tags": NotRequired[Dict[str, str]],
    },
)
ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "description": NotRequired[str],
        "parameters": NotRequired[Dict[str, ActionParameterTypeDef]],
        "targets": NotRequired[Dict[str, ActionTargetTypeDef]],
        "tags": NotRequired[Dict[str, str]],
    },
)

class CreateExperimentTemplateLogConfigurationInputTypeDef(TypedDict):
    logSchemaVersion: int
    cloudWatchLogsConfiguration: NotRequired[
        ExperimentTemplateCloudWatchLogsLogConfigurationInputTypeDef
    ]
    s3Configuration: NotRequired[ExperimentTemplateS3LogConfigurationInputTypeDef]

class UpdateExperimentTemplateLogConfigurationInputTypeDef(TypedDict):
    cloudWatchLogsConfiguration: NotRequired[
        ExperimentTemplateCloudWatchLogsLogConfigurationInputTypeDef
    ]
    s3Configuration: NotRequired[ExperimentTemplateS3LogConfigurationInputTypeDef]
    logSchemaVersion: NotRequired[int]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateExperimentTemplateTargetInputTypeDef(TypedDict):
    resourceType: str
    selectionMode: str
    resourceArns: NotRequired[Sequence[str]]
    resourceTags: NotRequired[Mapping[str, str]]
    filters: NotRequired[Sequence[ExperimentTemplateTargetInputFilterTypeDef]]
    parameters: NotRequired[Mapping[str, str]]

class UpdateExperimentTemplateTargetInputTypeDef(TypedDict):
    resourceType: str
    selectionMode: str
    resourceArns: NotRequired[Sequence[str]]
    resourceTags: NotRequired[Mapping[str, str]]
    filters: NotRequired[Sequence[ExperimentTemplateTargetInputFilterTypeDef]]
    parameters: NotRequired[Mapping[str, str]]

class CreateTargetAccountConfigurationResponseTypeDef(TypedDict):
    targetAccountConfiguration: TargetAccountConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteTargetAccountConfigurationResponseTypeDef(TypedDict):
    targetAccountConfiguration: TargetAccountConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetTargetAccountConfigurationResponseTypeDef(TypedDict):
    targetAccountConfiguration: TargetAccountConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTargetAccountConfigurationResponseTypeDef(TypedDict):
    targetAccountConfiguration: TargetAccountConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExperimentActionTypeDef(TypedDict):
    actionId: NotRequired[str]
    description: NotRequired[str]
    parameters: NotRequired[Dict[str, str]]
    targets: NotRequired[Dict[str, str]]
    startAfter: NotRequired[List[str]]
    state: NotRequired[ExperimentActionStateTypeDef]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]

class ExperimentStateTypeDef(TypedDict):
    status: NotRequired[ExperimentStatusType]
    reason: NotRequired[str]
    error: NotRequired[ExperimentErrorTypeDef]

class ExperimentLogConfigurationTypeDef(TypedDict):
    cloudWatchLogsConfiguration: NotRequired[ExperimentCloudWatchLogsLogConfigurationTypeDef]
    s3Configuration: NotRequired[ExperimentS3LogConfigurationTypeDef]
    logSchemaVersion: NotRequired[int]

class ListExperimentTargetAccountConfigurationsResponseTypeDef(TypedDict):
    targetAccountConfigurations: List[ExperimentTargetAccountConfigurationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetExperimentTargetAccountConfigurationResponseTypeDef(TypedDict):
    targetAccountConfiguration: ExperimentTargetAccountConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExperimentTargetTypeDef(TypedDict):
    resourceType: NotRequired[str]
    resourceArns: NotRequired[List[str]]
    resourceTags: NotRequired[Dict[str, str]]
    filters: NotRequired[List[ExperimentTargetFilterTypeDef]]
    selectionMode: NotRequired[str]
    parameters: NotRequired[Dict[str, str]]

class ExperimentTemplateLogConfigurationTypeDef(TypedDict):
    cloudWatchLogsConfiguration: NotRequired[
        ExperimentTemplateCloudWatchLogsLogConfigurationTypeDef
    ]
    s3Configuration: NotRequired[ExperimentTemplateS3LogConfigurationTypeDef]
    logSchemaVersion: NotRequired[int]

class ListExperimentTemplatesResponseTypeDef(TypedDict):
    experimentTemplates: List[ExperimentTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ExperimentTemplateTargetTypeDef(TypedDict):
    resourceType: NotRequired[str]
    resourceArns: NotRequired[List[str]]
    resourceTags: NotRequired[Dict[str, str]]
    filters: NotRequired[List[ExperimentTemplateTargetFilterTypeDef]]
    selectionMode: NotRequired[str]
    parameters: NotRequired[Dict[str, str]]

class ListExperimentResolvedTargetsResponseTypeDef(TypedDict):
    resolvedTargets: List[ResolvedTargetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTargetAccountConfigurationsResponseTypeDef(TypedDict):
    targetAccountConfigurations: List[TargetAccountConfigurationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTargetResourceTypesResponseTypeDef(TypedDict):
    targetResourceTypes: List[TargetResourceTypeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

SafetyLeverTypeDef = TypedDict(
    "SafetyLeverTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "state": NotRequired[SafetyLeverStateTypeDef],
    },
)

class StartExperimentRequestRequestTypeDef(TypedDict):
    clientToken: str
    experimentTemplateId: str
    experimentOptions: NotRequired[StartExperimentExperimentOptionsInputTypeDef]
    tags: NotRequired[Mapping[str, str]]

class TargetResourceTypeTypeDef(TypedDict):
    resourceType: NotRequired[str]
    description: NotRequired[str]
    parameters: NotRequired[Dict[str, TargetResourceTypeParameterTypeDef]]

UpdateSafetyLeverStateRequestRequestTypeDef = TypedDict(
    "UpdateSafetyLeverStateRequestRequestTypeDef",
    {
        "id": str,
        "state": UpdateSafetyLeverStateInputTypeDef,
    },
)

class ListActionsResponseTypeDef(TypedDict):
    actions: List[ActionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetActionResponseTypeDef(TypedDict):
    action: ActionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateExperimentTemplateRequestRequestTypeDef(TypedDict):
    clientToken: str
    description: str
    stopConditions: Sequence[CreateExperimentTemplateStopConditionInputTypeDef]
    actions: Mapping[str, CreateExperimentTemplateActionInputTypeDef]
    roleArn: str
    targets: NotRequired[Mapping[str, CreateExperimentTemplateTargetInputTypeDef]]
    tags: NotRequired[Mapping[str, str]]
    logConfiguration: NotRequired[CreateExperimentTemplateLogConfigurationInputTypeDef]
    experimentOptions: NotRequired[CreateExperimentTemplateExperimentOptionsInputTypeDef]

UpdateExperimentTemplateRequestRequestTypeDef = TypedDict(
    "UpdateExperimentTemplateRequestRequestTypeDef",
    {
        "id": str,
        "description": NotRequired[str],
        "stopConditions": NotRequired[Sequence[UpdateExperimentTemplateStopConditionInputTypeDef]],
        "targets": NotRequired[Mapping[str, UpdateExperimentTemplateTargetInputTypeDef]],
        "actions": NotRequired[Mapping[str, UpdateExperimentTemplateActionInputItemTypeDef]],
        "roleArn": NotRequired[str],
        "logConfiguration": NotRequired[UpdateExperimentTemplateLogConfigurationInputTypeDef],
        "experimentOptions": NotRequired[UpdateExperimentTemplateExperimentOptionsInputTypeDef],
    },
)
ExperimentSummaryTypeDef = TypedDict(
    "ExperimentSummaryTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "experimentTemplateId": NotRequired[str],
        "state": NotRequired[ExperimentStateTypeDef],
        "creationTime": NotRequired[datetime],
        "tags": NotRequired[Dict[str, str]],
        "experimentOptions": NotRequired[ExperimentOptionsTypeDef],
    },
)
ExperimentTypeDef = TypedDict(
    "ExperimentTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "experimentTemplateId": NotRequired[str],
        "roleArn": NotRequired[str],
        "state": NotRequired[ExperimentStateTypeDef],
        "targets": NotRequired[Dict[str, ExperimentTargetTypeDef]],
        "actions": NotRequired[Dict[str, ExperimentActionTypeDef]],
        "stopConditions": NotRequired[List[ExperimentStopConditionTypeDef]],
        "creationTime": NotRequired[datetime],
        "startTime": NotRequired[datetime],
        "endTime": NotRequired[datetime],
        "tags": NotRequired[Dict[str, str]],
        "logConfiguration": NotRequired[ExperimentLogConfigurationTypeDef],
        "experimentOptions": NotRequired[ExperimentOptionsTypeDef],
        "targetAccountConfigurationsCount": NotRequired[int],
    },
)
ExperimentTemplateTypeDef = TypedDict(
    "ExperimentTemplateTypeDef",
    {
        "id": NotRequired[str],
        "arn": NotRequired[str],
        "description": NotRequired[str],
        "targets": NotRequired[Dict[str, ExperimentTemplateTargetTypeDef]],
        "actions": NotRequired[Dict[str, ExperimentTemplateActionTypeDef]],
        "stopConditions": NotRequired[List[ExperimentTemplateStopConditionTypeDef]],
        "creationTime": NotRequired[datetime],
        "lastUpdateTime": NotRequired[datetime],
        "roleArn": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "logConfiguration": NotRequired[ExperimentTemplateLogConfigurationTypeDef],
        "experimentOptions": NotRequired[ExperimentTemplateExperimentOptionsTypeDef],
        "targetAccountConfigurationsCount": NotRequired[int],
    },
)

class GetSafetyLeverResponseTypeDef(TypedDict):
    safetyLever: SafetyLeverTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSafetyLeverStateResponseTypeDef(TypedDict):
    safetyLever: SafetyLeverTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetTargetResourceTypeResponseTypeDef(TypedDict):
    targetResourceType: TargetResourceTypeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListExperimentsResponseTypeDef(TypedDict):
    experiments: List[ExperimentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetExperimentResponseTypeDef(TypedDict):
    experiment: ExperimentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartExperimentResponseTypeDef(TypedDict):
    experiment: ExperimentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StopExperimentResponseTypeDef(TypedDict):
    experiment: ExperimentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateExperimentTemplateResponseTypeDef(TypedDict):
    experimentTemplate: ExperimentTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteExperimentTemplateResponseTypeDef(TypedDict):
    experimentTemplate: ExperimentTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetExperimentTemplateResponseTypeDef(TypedDict):
    experimentTemplate: ExperimentTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateExperimentTemplateResponseTypeDef(TypedDict):
    experimentTemplate: ExperimentTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
