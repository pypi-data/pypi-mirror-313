"""
Type annotations for nimble service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/type_defs/)

Usage::

    ```python
    from types_aiobotocore_nimble.type_defs import AcceptEulasRequestRequestTypeDef

    data: AcceptEulasRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AutomaticTerminationModeType,
    LaunchProfilePlatformType,
    LaunchProfileStateType,
    LaunchProfileStatusCodeType,
    LaunchProfileValidationStateType,
    LaunchProfileValidationStatusCodeType,
    LaunchProfileValidationTypeType,
    SessionBackupModeType,
    SessionPersistenceModeType,
    StreamingClipboardModeType,
    StreamingImageStateType,
    StreamingImageStatusCodeType,
    StreamingInstanceTypeType,
    StreamingSessionStateType,
    StreamingSessionStatusCodeType,
    StreamingSessionStreamStateType,
    StreamingSessionStreamStatusCodeType,
    StudioComponentInitializationScriptRunContextType,
    StudioComponentStateType,
    StudioComponentStatusCodeType,
    StudioComponentSubtypeType,
    StudioComponentTypeType,
    StudioEncryptionConfigurationKeyTypeType,
    StudioStateType,
    StudioStatusCodeType,
    VolumeRetentionModeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AcceptEulasRequestRequestTypeDef",
    "AcceptEulasResponseTypeDef",
    "ActiveDirectoryComputerAttributeTypeDef",
    "ActiveDirectoryConfigurationOutputTypeDef",
    "ActiveDirectoryConfigurationTypeDef",
    "ActiveDirectoryConfigurationUnionTypeDef",
    "ComputeFarmConfigurationTypeDef",
    "CreateLaunchProfileRequestRequestTypeDef",
    "CreateLaunchProfileResponseTypeDef",
    "CreateStreamingImageRequestRequestTypeDef",
    "CreateStreamingImageResponseTypeDef",
    "CreateStreamingSessionRequestRequestTypeDef",
    "CreateStreamingSessionResponseTypeDef",
    "CreateStreamingSessionStreamRequestRequestTypeDef",
    "CreateStreamingSessionStreamResponseTypeDef",
    "CreateStudioComponentRequestRequestTypeDef",
    "CreateStudioComponentResponseTypeDef",
    "CreateStudioRequestRequestTypeDef",
    "CreateStudioResponseTypeDef",
    "DeleteLaunchProfileMemberRequestRequestTypeDef",
    "DeleteLaunchProfileRequestRequestTypeDef",
    "DeleteLaunchProfileResponseTypeDef",
    "DeleteStreamingImageRequestRequestTypeDef",
    "DeleteStreamingImageResponseTypeDef",
    "DeleteStreamingSessionRequestRequestTypeDef",
    "DeleteStreamingSessionResponseTypeDef",
    "DeleteStudioComponentRequestRequestTypeDef",
    "DeleteStudioComponentResponseTypeDef",
    "DeleteStudioMemberRequestRequestTypeDef",
    "DeleteStudioRequestRequestTypeDef",
    "DeleteStudioResponseTypeDef",
    "EulaAcceptanceTypeDef",
    "EulaTypeDef",
    "GetEulaRequestRequestTypeDef",
    "GetEulaResponseTypeDef",
    "GetLaunchProfileDetailsRequestRequestTypeDef",
    "GetLaunchProfileDetailsResponseTypeDef",
    "GetLaunchProfileInitializationRequestRequestTypeDef",
    "GetLaunchProfileInitializationResponseTypeDef",
    "GetLaunchProfileMemberRequestRequestTypeDef",
    "GetLaunchProfileMemberResponseTypeDef",
    "GetLaunchProfileRequestLaunchProfileDeletedWaitTypeDef",
    "GetLaunchProfileRequestLaunchProfileReadyWaitTypeDef",
    "GetLaunchProfileRequestRequestTypeDef",
    "GetLaunchProfileResponseTypeDef",
    "GetStreamingImageRequestRequestTypeDef",
    "GetStreamingImageRequestStreamingImageDeletedWaitTypeDef",
    "GetStreamingImageRequestStreamingImageReadyWaitTypeDef",
    "GetStreamingImageResponseTypeDef",
    "GetStreamingSessionBackupRequestRequestTypeDef",
    "GetStreamingSessionBackupResponseTypeDef",
    "GetStreamingSessionRequestRequestTypeDef",
    "GetStreamingSessionRequestStreamingSessionDeletedWaitTypeDef",
    "GetStreamingSessionRequestStreamingSessionReadyWaitTypeDef",
    "GetStreamingSessionRequestStreamingSessionStoppedWaitTypeDef",
    "GetStreamingSessionResponseTypeDef",
    "GetStreamingSessionStreamRequestRequestTypeDef",
    "GetStreamingSessionStreamRequestStreamingSessionStreamReadyWaitTypeDef",
    "GetStreamingSessionStreamResponseTypeDef",
    "GetStudioComponentRequestRequestTypeDef",
    "GetStudioComponentRequestStudioComponentDeletedWaitTypeDef",
    "GetStudioComponentRequestStudioComponentReadyWaitTypeDef",
    "GetStudioComponentResponseTypeDef",
    "GetStudioMemberRequestRequestTypeDef",
    "GetStudioMemberResponseTypeDef",
    "GetStudioRequestRequestTypeDef",
    "GetStudioRequestStudioDeletedWaitTypeDef",
    "GetStudioRequestStudioReadyWaitTypeDef",
    "GetStudioResponseTypeDef",
    "LaunchProfileInitializationActiveDirectoryTypeDef",
    "LaunchProfileInitializationScriptTypeDef",
    "LaunchProfileInitializationTypeDef",
    "LaunchProfileMembershipTypeDef",
    "LaunchProfileTypeDef",
    "LicenseServiceConfigurationTypeDef",
    "ListEulaAcceptancesRequestListEulaAcceptancesPaginateTypeDef",
    "ListEulaAcceptancesRequestRequestTypeDef",
    "ListEulaAcceptancesResponseTypeDef",
    "ListEulasRequestListEulasPaginateTypeDef",
    "ListEulasRequestRequestTypeDef",
    "ListEulasResponseTypeDef",
    "ListLaunchProfileMembersRequestListLaunchProfileMembersPaginateTypeDef",
    "ListLaunchProfileMembersRequestRequestTypeDef",
    "ListLaunchProfileMembersResponseTypeDef",
    "ListLaunchProfilesRequestListLaunchProfilesPaginateTypeDef",
    "ListLaunchProfilesRequestRequestTypeDef",
    "ListLaunchProfilesResponseTypeDef",
    "ListStreamingImagesRequestListStreamingImagesPaginateTypeDef",
    "ListStreamingImagesRequestRequestTypeDef",
    "ListStreamingImagesResponseTypeDef",
    "ListStreamingSessionBackupsRequestListStreamingSessionBackupsPaginateTypeDef",
    "ListStreamingSessionBackupsRequestRequestTypeDef",
    "ListStreamingSessionBackupsResponseTypeDef",
    "ListStreamingSessionsRequestListStreamingSessionsPaginateTypeDef",
    "ListStreamingSessionsRequestRequestTypeDef",
    "ListStreamingSessionsResponseTypeDef",
    "ListStudioComponentsRequestListStudioComponentsPaginateTypeDef",
    "ListStudioComponentsRequestRequestTypeDef",
    "ListStudioComponentsResponseTypeDef",
    "ListStudioMembersRequestListStudioMembersPaginateTypeDef",
    "ListStudioMembersRequestRequestTypeDef",
    "ListStudioMembersResponseTypeDef",
    "ListStudiosRequestListStudiosPaginateTypeDef",
    "ListStudiosRequestRequestTypeDef",
    "ListStudiosResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NewLaunchProfileMemberTypeDef",
    "NewStudioMemberTypeDef",
    "PaginatorConfigTypeDef",
    "PutLaunchProfileMembersRequestRequestTypeDef",
    "PutStudioMembersRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ScriptParameterKeyValueTypeDef",
    "SharedFileSystemConfigurationTypeDef",
    "StartStreamingSessionRequestRequestTypeDef",
    "StartStreamingSessionResponseTypeDef",
    "StartStudioSSOConfigurationRepairRequestRequestTypeDef",
    "StartStudioSSOConfigurationRepairResponseTypeDef",
    "StopStreamingSessionRequestRequestTypeDef",
    "StopStreamingSessionResponseTypeDef",
    "StreamConfigurationCreateTypeDef",
    "StreamConfigurationSessionBackupTypeDef",
    "StreamConfigurationSessionStorageOutputTypeDef",
    "StreamConfigurationSessionStorageTypeDef",
    "StreamConfigurationSessionStorageUnionTypeDef",
    "StreamConfigurationTypeDef",
    "StreamingImageEncryptionConfigurationTypeDef",
    "StreamingImageTypeDef",
    "StreamingSessionBackupTypeDef",
    "StreamingSessionStorageRootTypeDef",
    "StreamingSessionStreamTypeDef",
    "StreamingSessionTypeDef",
    "StudioComponentConfigurationOutputTypeDef",
    "StudioComponentConfigurationTypeDef",
    "StudioComponentInitializationScriptTypeDef",
    "StudioComponentSummaryTypeDef",
    "StudioComponentTypeDef",
    "StudioEncryptionConfigurationTypeDef",
    "StudioMembershipTypeDef",
    "StudioTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateLaunchProfileMemberRequestRequestTypeDef",
    "UpdateLaunchProfileMemberResponseTypeDef",
    "UpdateLaunchProfileRequestRequestTypeDef",
    "UpdateLaunchProfileResponseTypeDef",
    "UpdateStreamingImageRequestRequestTypeDef",
    "UpdateStreamingImageResponseTypeDef",
    "UpdateStudioComponentRequestRequestTypeDef",
    "UpdateStudioComponentResponseTypeDef",
    "UpdateStudioRequestRequestTypeDef",
    "UpdateStudioResponseTypeDef",
    "ValidationResultTypeDef",
    "VolumeConfigurationTypeDef",
    "WaiterConfigTypeDef",
)

class AcceptEulasRequestRequestTypeDef(TypedDict):
    studioId: str
    clientToken: NotRequired[str]
    eulaIds: NotRequired[Sequence[str]]

class EulaAcceptanceTypeDef(TypedDict):
    acceptedAt: NotRequired[datetime]
    acceptedBy: NotRequired[str]
    accepteeId: NotRequired[str]
    eulaAcceptanceId: NotRequired[str]
    eulaId: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ActiveDirectoryComputerAttributeTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[str]

class ComputeFarmConfigurationTypeDef(TypedDict):
    activeDirectoryUser: NotRequired[str]
    endpoint: NotRequired[str]

class CreateStreamingImageRequestRequestTypeDef(TypedDict):
    ec2ImageId: str
    name: str
    studioId: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class CreateStreamingSessionRequestRequestTypeDef(TypedDict):
    launchProfileId: str
    studioId: str
    clientToken: NotRequired[str]
    ec2InstanceType: NotRequired[StreamingInstanceTypeType]
    ownedBy: NotRequired[str]
    streamingImageId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class CreateStreamingSessionStreamRequestRequestTypeDef(TypedDict):
    sessionId: str
    studioId: str
    clientToken: NotRequired[str]
    expirationInSeconds: NotRequired[int]

class StreamingSessionStreamTypeDef(TypedDict):
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    expiresAt: NotRequired[datetime]
    ownedBy: NotRequired[str]
    state: NotRequired[StreamingSessionStreamStateType]
    statusCode: NotRequired[StreamingSessionStreamStatusCodeType]
    streamId: NotRequired[str]
    url: NotRequired[str]

class ScriptParameterKeyValueTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]

class StudioComponentInitializationScriptTypeDef(TypedDict):
    launchProfileProtocolVersion: NotRequired[str]
    platform: NotRequired[LaunchProfilePlatformType]
    runContext: NotRequired[StudioComponentInitializationScriptRunContextType]
    script: NotRequired[str]

class StudioEncryptionConfigurationTypeDef(TypedDict):
    keyType: StudioEncryptionConfigurationKeyTypeType
    keyArn: NotRequired[str]

class DeleteLaunchProfileMemberRequestRequestTypeDef(TypedDict):
    launchProfileId: str
    principalId: str
    studioId: str
    clientToken: NotRequired[str]

class DeleteLaunchProfileRequestRequestTypeDef(TypedDict):
    launchProfileId: str
    studioId: str
    clientToken: NotRequired[str]

class DeleteStreamingImageRequestRequestTypeDef(TypedDict):
    streamingImageId: str
    studioId: str
    clientToken: NotRequired[str]

class DeleteStreamingSessionRequestRequestTypeDef(TypedDict):
    sessionId: str
    studioId: str
    clientToken: NotRequired[str]

class DeleteStudioComponentRequestRequestTypeDef(TypedDict):
    studioComponentId: str
    studioId: str
    clientToken: NotRequired[str]

class DeleteStudioMemberRequestRequestTypeDef(TypedDict):
    principalId: str
    studioId: str
    clientToken: NotRequired[str]

class DeleteStudioRequestRequestTypeDef(TypedDict):
    studioId: str
    clientToken: NotRequired[str]

class EulaTypeDef(TypedDict):
    content: NotRequired[str]
    createdAt: NotRequired[datetime]
    eulaId: NotRequired[str]
    name: NotRequired[str]
    updatedAt: NotRequired[datetime]

class GetEulaRequestRequestTypeDef(TypedDict):
    eulaId: str

class GetLaunchProfileDetailsRequestRequestTypeDef(TypedDict):
    launchProfileId: str
    studioId: str

StudioComponentSummaryTypeDef = TypedDict(
    "StudioComponentSummaryTypeDef",
    {
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "description": NotRequired[str],
        "name": NotRequired[str],
        "studioComponentId": NotRequired[str],
        "subtype": NotRequired[StudioComponentSubtypeType],
        "type": NotRequired[StudioComponentTypeType],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)

class GetLaunchProfileInitializationRequestRequestTypeDef(TypedDict):
    launchProfileId: str
    launchProfileProtocolVersions: Sequence[str]
    launchPurpose: str
    platform: str
    studioId: str

class GetLaunchProfileMemberRequestRequestTypeDef(TypedDict):
    launchProfileId: str
    principalId: str
    studioId: str

class LaunchProfileMembershipTypeDef(TypedDict):
    identityStoreId: NotRequired[str]
    persona: NotRequired[Literal["USER"]]
    principalId: NotRequired[str]
    sid: NotRequired[str]

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class GetLaunchProfileRequestRequestTypeDef(TypedDict):
    launchProfileId: str
    studioId: str

class GetStreamingImageRequestRequestTypeDef(TypedDict):
    streamingImageId: str
    studioId: str

class GetStreamingSessionBackupRequestRequestTypeDef(TypedDict):
    backupId: str
    studioId: str

class StreamingSessionBackupTypeDef(TypedDict):
    arn: NotRequired[str]
    backupId: NotRequired[str]
    createdAt: NotRequired[datetime]
    launchProfileId: NotRequired[str]
    ownedBy: NotRequired[str]
    sessionId: NotRequired[str]
    state: NotRequired[StreamingSessionStateType]
    statusCode: NotRequired[StreamingSessionStatusCodeType]
    statusMessage: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

class GetStreamingSessionRequestRequestTypeDef(TypedDict):
    sessionId: str
    studioId: str

class GetStreamingSessionStreamRequestRequestTypeDef(TypedDict):
    sessionId: str
    streamId: str
    studioId: str

class GetStudioComponentRequestRequestTypeDef(TypedDict):
    studioComponentId: str
    studioId: str

class GetStudioMemberRequestRequestTypeDef(TypedDict):
    principalId: str
    studioId: str

class StudioMembershipTypeDef(TypedDict):
    identityStoreId: NotRequired[str]
    persona: NotRequired[Literal["ADMINISTRATOR"]]
    principalId: NotRequired[str]
    sid: NotRequired[str]

class GetStudioRequestRequestTypeDef(TypedDict):
    studioId: str

class LaunchProfileInitializationScriptTypeDef(TypedDict):
    runtimeRoleArn: NotRequired[str]
    script: NotRequired[str]
    secureInitializationRoleArn: NotRequired[str]
    studioComponentId: NotRequired[str]
    studioComponentName: NotRequired[str]

ValidationResultTypeDef = TypedDict(
    "ValidationResultTypeDef",
    {
        "state": LaunchProfileValidationStateType,
        "statusCode": LaunchProfileValidationStatusCodeType,
        "statusMessage": str,
        "type": LaunchProfileValidationTypeType,
    },
)

class LicenseServiceConfigurationTypeDef(TypedDict):
    endpoint: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListEulaAcceptancesRequestRequestTypeDef(TypedDict):
    studioId: str
    eulaIds: NotRequired[Sequence[str]]
    nextToken: NotRequired[str]

class ListEulasRequestRequestTypeDef(TypedDict):
    eulaIds: NotRequired[Sequence[str]]
    nextToken: NotRequired[str]

class ListLaunchProfileMembersRequestRequestTypeDef(TypedDict):
    launchProfileId: str
    studioId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListLaunchProfilesRequestRequestTypeDef(TypedDict):
    studioId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    principalId: NotRequired[str]
    states: NotRequired[Sequence[LaunchProfileStateType]]

class ListStreamingImagesRequestRequestTypeDef(TypedDict):
    studioId: str
    nextToken: NotRequired[str]
    owner: NotRequired[str]

class ListStreamingSessionBackupsRequestRequestTypeDef(TypedDict):
    studioId: str
    nextToken: NotRequired[str]
    ownedBy: NotRequired[str]

class ListStreamingSessionsRequestRequestTypeDef(TypedDict):
    studioId: str
    createdBy: NotRequired[str]
    nextToken: NotRequired[str]
    ownedBy: NotRequired[str]
    sessionIds: NotRequired[str]

ListStudioComponentsRequestRequestTypeDef = TypedDict(
    "ListStudioComponentsRequestRequestTypeDef",
    {
        "studioId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "states": NotRequired[Sequence[StudioComponentStateType]],
        "types": NotRequired[Sequence[StudioComponentTypeType]],
    },
)

class ListStudioMembersRequestRequestTypeDef(TypedDict):
    studioId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListStudiosRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class NewLaunchProfileMemberTypeDef(TypedDict):
    persona: Literal["USER"]
    principalId: str

class NewStudioMemberTypeDef(TypedDict):
    persona: Literal["ADMINISTRATOR"]
    principalId: str

class SharedFileSystemConfigurationTypeDef(TypedDict):
    endpoint: NotRequired[str]
    fileSystemId: NotRequired[str]
    linuxMountPoint: NotRequired[str]
    shareName: NotRequired[str]
    windowsMountDrive: NotRequired[str]

class StartStreamingSessionRequestRequestTypeDef(TypedDict):
    sessionId: str
    studioId: str
    backupId: NotRequired[str]
    clientToken: NotRequired[str]

class StartStudioSSOConfigurationRepairRequestRequestTypeDef(TypedDict):
    studioId: str
    clientToken: NotRequired[str]

class StopStreamingSessionRequestRequestTypeDef(TypedDict):
    sessionId: str
    studioId: str
    clientToken: NotRequired[str]
    volumeRetentionMode: NotRequired[VolumeRetentionModeType]

class StreamConfigurationSessionBackupTypeDef(TypedDict):
    maxBackupsToRetain: NotRequired[int]
    mode: NotRequired[SessionBackupModeType]

class VolumeConfigurationTypeDef(TypedDict):
    iops: NotRequired[int]
    size: NotRequired[int]
    throughput: NotRequired[int]

class StreamingSessionStorageRootTypeDef(TypedDict):
    linux: NotRequired[str]
    windows: NotRequired[str]

class StreamingImageEncryptionConfigurationTypeDef(TypedDict):
    keyType: Literal["CUSTOMER_MANAGED_KEY"]
    keyArn: NotRequired[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: NotRequired[Mapping[str, str]]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateLaunchProfileMemberRequestRequestTypeDef(TypedDict):
    launchProfileId: str
    persona: Literal["USER"]
    principalId: str
    studioId: str
    clientToken: NotRequired[str]

class UpdateStreamingImageRequestRequestTypeDef(TypedDict):
    streamingImageId: str
    studioId: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    name: NotRequired[str]

class UpdateStudioRequestRequestTypeDef(TypedDict):
    studioId: str
    adminRoleArn: NotRequired[str]
    clientToken: NotRequired[str]
    displayName: NotRequired[str]
    userRoleArn: NotRequired[str]

class AcceptEulasResponseTypeDef(TypedDict):
    eulaAcceptances: List[EulaAcceptanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListEulaAcceptancesResponseTypeDef(TypedDict):
    eulaAcceptances: List[EulaAcceptanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ActiveDirectoryConfigurationOutputTypeDef(TypedDict):
    computerAttributes: NotRequired[List[ActiveDirectoryComputerAttributeTypeDef]]
    directoryId: NotRequired[str]
    organizationalUnitDistinguishedName: NotRequired[str]

class ActiveDirectoryConfigurationTypeDef(TypedDict):
    computerAttributes: NotRequired[Sequence[ActiveDirectoryComputerAttributeTypeDef]]
    directoryId: NotRequired[str]
    organizationalUnitDistinguishedName: NotRequired[str]

class LaunchProfileInitializationActiveDirectoryTypeDef(TypedDict):
    computerAttributes: NotRequired[List[ActiveDirectoryComputerAttributeTypeDef]]
    directoryId: NotRequired[str]
    directoryName: NotRequired[str]
    dnsIpAddresses: NotRequired[List[str]]
    organizationalUnitDistinguishedName: NotRequired[str]
    studioComponentId: NotRequired[str]
    studioComponentName: NotRequired[str]

class CreateStreamingSessionStreamResponseTypeDef(TypedDict):
    stream: StreamingSessionStreamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetStreamingSessionStreamResponseTypeDef(TypedDict):
    stream: StreamingSessionStreamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateStudioRequestRequestTypeDef(TypedDict):
    adminRoleArn: str
    displayName: str
    studioName: str
    userRoleArn: str
    clientToken: NotRequired[str]
    studioEncryptionConfiguration: NotRequired[StudioEncryptionConfigurationTypeDef]
    tags: NotRequired[Mapping[str, str]]

class StudioTypeDef(TypedDict):
    adminRoleArn: NotRequired[str]
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    displayName: NotRequired[str]
    homeRegion: NotRequired[str]
    ssoClientId: NotRequired[str]
    state: NotRequired[StudioStateType]
    statusCode: NotRequired[StudioStatusCodeType]
    statusMessage: NotRequired[str]
    studioEncryptionConfiguration: NotRequired[StudioEncryptionConfigurationTypeDef]
    studioId: NotRequired[str]
    studioName: NotRequired[str]
    studioUrl: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    updatedAt: NotRequired[datetime]
    userRoleArn: NotRequired[str]

class GetEulaResponseTypeDef(TypedDict):
    eula: EulaTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListEulasResponseTypeDef(TypedDict):
    eulas: List[EulaTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetLaunchProfileMemberResponseTypeDef(TypedDict):
    member: LaunchProfileMembershipTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListLaunchProfileMembersResponseTypeDef(TypedDict):
    members: List[LaunchProfileMembershipTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateLaunchProfileMemberResponseTypeDef(TypedDict):
    member: LaunchProfileMembershipTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetLaunchProfileRequestLaunchProfileDeletedWaitTypeDef(TypedDict):
    launchProfileId: str
    studioId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetLaunchProfileRequestLaunchProfileReadyWaitTypeDef(TypedDict):
    launchProfileId: str
    studioId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetStreamingImageRequestStreamingImageDeletedWaitTypeDef(TypedDict):
    streamingImageId: str
    studioId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetStreamingImageRequestStreamingImageReadyWaitTypeDef(TypedDict):
    streamingImageId: str
    studioId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetStreamingSessionRequestStreamingSessionDeletedWaitTypeDef(TypedDict):
    sessionId: str
    studioId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetStreamingSessionRequestStreamingSessionReadyWaitTypeDef(TypedDict):
    sessionId: str
    studioId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetStreamingSessionRequestStreamingSessionStoppedWaitTypeDef(TypedDict):
    sessionId: str
    studioId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetStreamingSessionStreamRequestStreamingSessionStreamReadyWaitTypeDef(TypedDict):
    sessionId: str
    streamId: str
    studioId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetStudioComponentRequestStudioComponentDeletedWaitTypeDef(TypedDict):
    studioComponentId: str
    studioId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetStudioComponentRequestStudioComponentReadyWaitTypeDef(TypedDict):
    studioComponentId: str
    studioId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetStudioRequestStudioDeletedWaitTypeDef(TypedDict):
    studioId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetStudioRequestStudioReadyWaitTypeDef(TypedDict):
    studioId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetStreamingSessionBackupResponseTypeDef(TypedDict):
    streamingSessionBackup: StreamingSessionBackupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListStreamingSessionBackupsResponseTypeDef(TypedDict):
    streamingSessionBackups: List[StreamingSessionBackupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetStudioMemberResponseTypeDef(TypedDict):
    member: StudioMembershipTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListStudioMembersResponseTypeDef(TypedDict):
    members: List[StudioMembershipTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListEulaAcceptancesRequestListEulaAcceptancesPaginateTypeDef(TypedDict):
    studioId: str
    eulaIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEulasRequestListEulasPaginateTypeDef(TypedDict):
    eulaIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLaunchProfileMembersRequestListLaunchProfileMembersPaginateTypeDef(TypedDict):
    launchProfileId: str
    studioId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLaunchProfilesRequestListLaunchProfilesPaginateTypeDef(TypedDict):
    studioId: str
    principalId: NotRequired[str]
    states: NotRequired[Sequence[LaunchProfileStateType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStreamingImagesRequestListStreamingImagesPaginateTypeDef(TypedDict):
    studioId: str
    owner: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStreamingSessionBackupsRequestListStreamingSessionBackupsPaginateTypeDef(TypedDict):
    studioId: str
    ownedBy: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStreamingSessionsRequestListStreamingSessionsPaginateTypeDef(TypedDict):
    studioId: str
    createdBy: NotRequired[str]
    ownedBy: NotRequired[str]
    sessionIds: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListStudioComponentsRequestListStudioComponentsPaginateTypeDef = TypedDict(
    "ListStudioComponentsRequestListStudioComponentsPaginateTypeDef",
    {
        "studioId": str,
        "states": NotRequired[Sequence[StudioComponentStateType]],
        "types": NotRequired[Sequence[StudioComponentTypeType]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListStudioMembersRequestListStudioMembersPaginateTypeDef(TypedDict):
    studioId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStudiosRequestListStudiosPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class PutLaunchProfileMembersRequestRequestTypeDef(TypedDict):
    identityStoreId: str
    launchProfileId: str
    members: Sequence[NewLaunchProfileMemberTypeDef]
    studioId: str
    clientToken: NotRequired[str]

class PutStudioMembersRequestRequestTypeDef(TypedDict):
    identityStoreId: str
    members: Sequence[NewStudioMemberTypeDef]
    studioId: str
    clientToken: NotRequired[str]

class StreamingSessionTypeDef(TypedDict):
    arn: NotRequired[str]
    automaticTerminationMode: NotRequired[AutomaticTerminationModeType]
    backupMode: NotRequired[SessionBackupModeType]
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    ec2InstanceType: NotRequired[str]
    launchProfileId: NotRequired[str]
    maxBackupsToRetain: NotRequired[int]
    ownedBy: NotRequired[str]
    sessionId: NotRequired[str]
    sessionPersistenceMode: NotRequired[SessionPersistenceModeType]
    startedAt: NotRequired[datetime]
    startedBy: NotRequired[str]
    startedFromBackupId: NotRequired[str]
    state: NotRequired[StreamingSessionStateType]
    statusCode: NotRequired[StreamingSessionStatusCodeType]
    statusMessage: NotRequired[str]
    stopAt: NotRequired[datetime]
    stoppedAt: NotRequired[datetime]
    stoppedBy: NotRequired[str]
    streamingImageId: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    terminateAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]
    volumeConfiguration: NotRequired[VolumeConfigurationTypeDef]
    volumeRetentionMode: NotRequired[VolumeRetentionModeType]

class StreamConfigurationSessionStorageOutputTypeDef(TypedDict):
    mode: List[Literal["UPLOAD"]]
    root: NotRequired[StreamingSessionStorageRootTypeDef]

class StreamConfigurationSessionStorageTypeDef(TypedDict):
    mode: Sequence[Literal["UPLOAD"]]
    root: NotRequired[StreamingSessionStorageRootTypeDef]

class StreamingImageTypeDef(TypedDict):
    arn: NotRequired[str]
    description: NotRequired[str]
    ec2ImageId: NotRequired[str]
    encryptionConfiguration: NotRequired[StreamingImageEncryptionConfigurationTypeDef]
    eulaIds: NotRequired[List[str]]
    name: NotRequired[str]
    owner: NotRequired[str]
    platform: NotRequired[str]
    state: NotRequired[StreamingImageStateType]
    statusCode: NotRequired[StreamingImageStatusCodeType]
    statusMessage: NotRequired[str]
    streamingImageId: NotRequired[str]
    tags: NotRequired[Dict[str, str]]

class StudioComponentConfigurationOutputTypeDef(TypedDict):
    activeDirectoryConfiguration: NotRequired[ActiveDirectoryConfigurationOutputTypeDef]
    computeFarmConfiguration: NotRequired[ComputeFarmConfigurationTypeDef]
    licenseServiceConfiguration: NotRequired[LicenseServiceConfigurationTypeDef]
    sharedFileSystemConfiguration: NotRequired[SharedFileSystemConfigurationTypeDef]

ActiveDirectoryConfigurationUnionTypeDef = Union[
    ActiveDirectoryConfigurationTypeDef, ActiveDirectoryConfigurationOutputTypeDef
]

class LaunchProfileInitializationTypeDef(TypedDict):
    activeDirectory: NotRequired[LaunchProfileInitializationActiveDirectoryTypeDef]
    ec2SecurityGroupIds: NotRequired[List[str]]
    launchProfileId: NotRequired[str]
    launchProfileProtocolVersion: NotRequired[str]
    launchPurpose: NotRequired[str]
    name: NotRequired[str]
    platform: NotRequired[LaunchProfilePlatformType]
    systemInitializationScripts: NotRequired[List[LaunchProfileInitializationScriptTypeDef]]
    userInitializationScripts: NotRequired[List[LaunchProfileInitializationScriptTypeDef]]

class CreateStudioResponseTypeDef(TypedDict):
    studio: StudioTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteStudioResponseTypeDef(TypedDict):
    studio: StudioTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetStudioResponseTypeDef(TypedDict):
    studio: StudioTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListStudiosResponseTypeDef(TypedDict):
    studios: List[StudioTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class StartStudioSSOConfigurationRepairResponseTypeDef(TypedDict):
    studio: StudioTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateStudioResponseTypeDef(TypedDict):
    studio: StudioTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateStreamingSessionResponseTypeDef(TypedDict):
    session: StreamingSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteStreamingSessionResponseTypeDef(TypedDict):
    session: StreamingSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetStreamingSessionResponseTypeDef(TypedDict):
    session: StreamingSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListStreamingSessionsResponseTypeDef(TypedDict):
    sessions: List[StreamingSessionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class StartStreamingSessionResponseTypeDef(TypedDict):
    session: StreamingSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StopStreamingSessionResponseTypeDef(TypedDict):
    session: StreamingSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StreamConfigurationTypeDef(TypedDict):
    clipboardMode: StreamingClipboardModeType
    ec2InstanceTypes: List[StreamingInstanceTypeType]
    streamingImageIds: List[str]
    automaticTerminationMode: NotRequired[AutomaticTerminationModeType]
    maxSessionLengthInMinutes: NotRequired[int]
    maxStoppedSessionLengthInMinutes: NotRequired[int]
    sessionBackup: NotRequired[StreamConfigurationSessionBackupTypeDef]
    sessionPersistenceMode: NotRequired[SessionPersistenceModeType]
    sessionStorage: NotRequired[StreamConfigurationSessionStorageOutputTypeDef]
    volumeConfiguration: NotRequired[VolumeConfigurationTypeDef]

StreamConfigurationSessionStorageUnionTypeDef = Union[
    StreamConfigurationSessionStorageTypeDef, StreamConfigurationSessionStorageOutputTypeDef
]

class CreateStreamingImageResponseTypeDef(TypedDict):
    streamingImage: StreamingImageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteStreamingImageResponseTypeDef(TypedDict):
    streamingImage: StreamingImageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetStreamingImageResponseTypeDef(TypedDict):
    streamingImage: StreamingImageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListStreamingImagesResponseTypeDef(TypedDict):
    streamingImages: List[StreamingImageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateStreamingImageResponseTypeDef(TypedDict):
    streamingImage: StreamingImageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

StudioComponentTypeDef = TypedDict(
    "StudioComponentTypeDef",
    {
        "arn": NotRequired[str],
        "configuration": NotRequired[StudioComponentConfigurationOutputTypeDef],
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "description": NotRequired[str],
        "ec2SecurityGroupIds": NotRequired[List[str]],
        "initializationScripts": NotRequired[List[StudioComponentInitializationScriptTypeDef]],
        "name": NotRequired[str],
        "runtimeRoleArn": NotRequired[str],
        "scriptParameters": NotRequired[List[ScriptParameterKeyValueTypeDef]],
        "secureInitializationRoleArn": NotRequired[str],
        "state": NotRequired[StudioComponentStateType],
        "statusCode": NotRequired[StudioComponentStatusCodeType],
        "statusMessage": NotRequired[str],
        "studioComponentId": NotRequired[str],
        "subtype": NotRequired[StudioComponentSubtypeType],
        "tags": NotRequired[Dict[str, str]],
        "type": NotRequired[StudioComponentTypeType],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)

class StudioComponentConfigurationTypeDef(TypedDict):
    activeDirectoryConfiguration: NotRequired[ActiveDirectoryConfigurationUnionTypeDef]
    computeFarmConfiguration: NotRequired[ComputeFarmConfigurationTypeDef]
    licenseServiceConfiguration: NotRequired[LicenseServiceConfigurationTypeDef]
    sharedFileSystemConfiguration: NotRequired[SharedFileSystemConfigurationTypeDef]

class GetLaunchProfileInitializationResponseTypeDef(TypedDict):
    launchProfileInitialization: LaunchProfileInitializationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class LaunchProfileTypeDef(TypedDict):
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    description: NotRequired[str]
    ec2SubnetIds: NotRequired[List[str]]
    launchProfileId: NotRequired[str]
    launchProfileProtocolVersions: NotRequired[List[str]]
    name: NotRequired[str]
    state: NotRequired[LaunchProfileStateType]
    statusCode: NotRequired[LaunchProfileStatusCodeType]
    statusMessage: NotRequired[str]
    streamConfiguration: NotRequired[StreamConfigurationTypeDef]
    studioComponentIds: NotRequired[List[str]]
    tags: NotRequired[Dict[str, str]]
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]
    validationResults: NotRequired[List[ValidationResultTypeDef]]

class StreamConfigurationCreateTypeDef(TypedDict):
    clipboardMode: StreamingClipboardModeType
    ec2InstanceTypes: Sequence[StreamingInstanceTypeType]
    streamingImageIds: Sequence[str]
    automaticTerminationMode: NotRequired[AutomaticTerminationModeType]
    maxSessionLengthInMinutes: NotRequired[int]
    maxStoppedSessionLengthInMinutes: NotRequired[int]
    sessionBackup: NotRequired[StreamConfigurationSessionBackupTypeDef]
    sessionPersistenceMode: NotRequired[SessionPersistenceModeType]
    sessionStorage: NotRequired[StreamConfigurationSessionStorageUnionTypeDef]
    volumeConfiguration: NotRequired[VolumeConfigurationTypeDef]

class CreateStudioComponentResponseTypeDef(TypedDict):
    studioComponent: StudioComponentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteStudioComponentResponseTypeDef(TypedDict):
    studioComponent: StudioComponentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetStudioComponentResponseTypeDef(TypedDict):
    studioComponent: StudioComponentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListStudioComponentsResponseTypeDef(TypedDict):
    studioComponents: List[StudioComponentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateStudioComponentResponseTypeDef(TypedDict):
    studioComponent: StudioComponentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

CreateStudioComponentRequestRequestTypeDef = TypedDict(
    "CreateStudioComponentRequestRequestTypeDef",
    {
        "name": str,
        "studioId": str,
        "type": StudioComponentTypeType,
        "clientToken": NotRequired[str],
        "configuration": NotRequired[StudioComponentConfigurationTypeDef],
        "description": NotRequired[str],
        "ec2SecurityGroupIds": NotRequired[Sequence[str]],
        "initializationScripts": NotRequired[Sequence[StudioComponentInitializationScriptTypeDef]],
        "runtimeRoleArn": NotRequired[str],
        "scriptParameters": NotRequired[Sequence[ScriptParameterKeyValueTypeDef]],
        "secureInitializationRoleArn": NotRequired[str],
        "subtype": NotRequired[StudioComponentSubtypeType],
        "tags": NotRequired[Mapping[str, str]],
    },
)
UpdateStudioComponentRequestRequestTypeDef = TypedDict(
    "UpdateStudioComponentRequestRequestTypeDef",
    {
        "studioComponentId": str,
        "studioId": str,
        "clientToken": NotRequired[str],
        "configuration": NotRequired[StudioComponentConfigurationTypeDef],
        "description": NotRequired[str],
        "ec2SecurityGroupIds": NotRequired[Sequence[str]],
        "initializationScripts": NotRequired[Sequence[StudioComponentInitializationScriptTypeDef]],
        "name": NotRequired[str],
        "runtimeRoleArn": NotRequired[str],
        "scriptParameters": NotRequired[Sequence[ScriptParameterKeyValueTypeDef]],
        "secureInitializationRoleArn": NotRequired[str],
        "subtype": NotRequired[StudioComponentSubtypeType],
        "type": NotRequired[StudioComponentTypeType],
    },
)

class CreateLaunchProfileResponseTypeDef(TypedDict):
    launchProfile: LaunchProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteLaunchProfileResponseTypeDef(TypedDict):
    launchProfile: LaunchProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetLaunchProfileDetailsResponseTypeDef(TypedDict):
    launchProfile: LaunchProfileTypeDef
    streamingImages: List[StreamingImageTypeDef]
    studioComponentSummaries: List[StudioComponentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetLaunchProfileResponseTypeDef(TypedDict):
    launchProfile: LaunchProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListLaunchProfilesResponseTypeDef(TypedDict):
    launchProfiles: List[LaunchProfileTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateLaunchProfileResponseTypeDef(TypedDict):
    launchProfile: LaunchProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLaunchProfileRequestRequestTypeDef(TypedDict):
    ec2SubnetIds: Sequence[str]
    launchProfileProtocolVersions: Sequence[str]
    name: str
    streamConfiguration: StreamConfigurationCreateTypeDef
    studioComponentIds: Sequence[str]
    studioId: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class UpdateLaunchProfileRequestRequestTypeDef(TypedDict):
    launchProfileId: str
    studioId: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    launchProfileProtocolVersions: NotRequired[Sequence[str]]
    name: NotRequired[str]
    streamConfiguration: NotRequired[StreamConfigurationCreateTypeDef]
    studioComponentIds: NotRequired[Sequence[str]]
