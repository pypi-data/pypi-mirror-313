"""
Type annotations for mediapackagev2 service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackagev2/type_defs/)

Usage::

    ```python
    from types_aiobotocore_mediapackagev2.type_defs import ChannelGroupListConfigurationTypeDef

    data: ChannelGroupListConfigurationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AdMarkerDashType,
    CmafEncryptionMethodType,
    ContainerTypeType,
    DashDrmSignalingType,
    DashPeriodTriggerType,
    DashUtcTimingModeType,
    DrmSystemType,
    EndpointErrorConditionType,
    InputTypeType,
    PresetSpeke20AudioType,
    PresetSpeke20VideoType,
    ScteFilterType,
    TsEncryptionMethodType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ChannelGroupListConfigurationTypeDef",
    "ChannelListConfigurationTypeDef",
    "CreateChannelGroupRequestRequestTypeDef",
    "CreateChannelGroupResponseTypeDef",
    "CreateChannelRequestRequestTypeDef",
    "CreateChannelResponseTypeDef",
    "CreateDashManifestConfigurationTypeDef",
    "CreateHlsManifestConfigurationTypeDef",
    "CreateLowLatencyHlsManifestConfigurationTypeDef",
    "CreateOriginEndpointRequestRequestTypeDef",
    "CreateOriginEndpointResponseTypeDef",
    "DashUtcTimingTypeDef",
    "DeleteChannelGroupRequestRequestTypeDef",
    "DeleteChannelPolicyRequestRequestTypeDef",
    "DeleteChannelRequestRequestTypeDef",
    "DeleteOriginEndpointPolicyRequestRequestTypeDef",
    "DeleteOriginEndpointRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionContractConfigurationTypeDef",
    "EncryptionMethodTypeDef",
    "EncryptionOutputTypeDef",
    "EncryptionTypeDef",
    "EncryptionUnionTypeDef",
    "FilterConfigurationOutputTypeDef",
    "FilterConfigurationTypeDef",
    "FilterConfigurationUnionTypeDef",
    "ForceEndpointErrorConfigurationOutputTypeDef",
    "ForceEndpointErrorConfigurationTypeDef",
    "GetChannelGroupRequestRequestTypeDef",
    "GetChannelGroupResponseTypeDef",
    "GetChannelPolicyRequestRequestTypeDef",
    "GetChannelPolicyResponseTypeDef",
    "GetChannelRequestRequestTypeDef",
    "GetChannelResponseTypeDef",
    "GetDashManifestConfigurationTypeDef",
    "GetHlsManifestConfigurationTypeDef",
    "GetLowLatencyHlsManifestConfigurationTypeDef",
    "GetOriginEndpointPolicyRequestRequestTypeDef",
    "GetOriginEndpointPolicyResponseTypeDef",
    "GetOriginEndpointRequestRequestTypeDef",
    "GetOriginEndpointResponseTypeDef",
    "IngestEndpointTypeDef",
    "ListChannelGroupsRequestListChannelGroupsPaginateTypeDef",
    "ListChannelGroupsRequestRequestTypeDef",
    "ListChannelGroupsResponseTypeDef",
    "ListChannelsRequestListChannelsPaginateTypeDef",
    "ListChannelsRequestRequestTypeDef",
    "ListChannelsResponseTypeDef",
    "ListDashManifestConfigurationTypeDef",
    "ListHlsManifestConfigurationTypeDef",
    "ListLowLatencyHlsManifestConfigurationTypeDef",
    "ListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef",
    "ListOriginEndpointsRequestRequestTypeDef",
    "ListOriginEndpointsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "OriginEndpointListConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PutChannelPolicyRequestRequestTypeDef",
    "PutOriginEndpointPolicyRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ScteDashTypeDef",
    "ScteHlsTypeDef",
    "ScteOutputTypeDef",
    "ScteTypeDef",
    "ScteUnionTypeDef",
    "SegmentOutputTypeDef",
    "SegmentTypeDef",
    "SpekeKeyProviderOutputTypeDef",
    "SpekeKeyProviderTypeDef",
    "SpekeKeyProviderUnionTypeDef",
    "StartTagTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateChannelGroupRequestRequestTypeDef",
    "UpdateChannelGroupResponseTypeDef",
    "UpdateChannelRequestRequestTypeDef",
    "UpdateChannelResponseTypeDef",
    "UpdateOriginEndpointRequestRequestTypeDef",
    "UpdateOriginEndpointResponseTypeDef",
)


class ChannelGroupListConfigurationTypeDef(TypedDict):
    ChannelGroupName: str
    Arn: str
    CreatedAt: datetime
    ModifiedAt: datetime
    Description: NotRequired[str]


class ChannelListConfigurationTypeDef(TypedDict):
    Arn: str
    ChannelName: str
    ChannelGroupName: str
    CreatedAt: datetime
    ModifiedAt: datetime
    Description: NotRequired[str]
    InputType: NotRequired[InputTypeType]


class CreateChannelGroupRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateChannelRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str
    ClientToken: NotRequired[str]
    InputType: NotRequired[InputTypeType]
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class IngestEndpointTypeDef(TypedDict):
    Id: NotRequired[str]
    Url: NotRequired[str]


class DashUtcTimingTypeDef(TypedDict):
    TimingMode: NotRequired[DashUtcTimingModeType]
    TimingSource: NotRequired[str]


class ScteDashTypeDef(TypedDict):
    AdMarkerDash: NotRequired[AdMarkerDashType]


class ScteHlsTypeDef(TypedDict):
    AdMarkerHls: NotRequired[Literal["DATERANGE"]]


class StartTagTypeDef(TypedDict):
    TimeOffset: float
    Precise: NotRequired[bool]


class ForceEndpointErrorConfigurationTypeDef(TypedDict):
    EndpointErrorConditions: NotRequired[Sequence[EndpointErrorConditionType]]


class ForceEndpointErrorConfigurationOutputTypeDef(TypedDict):
    EndpointErrorConditions: NotRequired[List[EndpointErrorConditionType]]


class DeleteChannelGroupRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str


class DeleteChannelPolicyRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str


class DeleteChannelRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str


class DeleteOriginEndpointPolicyRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str
    OriginEndpointName: str


class DeleteOriginEndpointRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str
    OriginEndpointName: str


class EncryptionContractConfigurationTypeDef(TypedDict):
    PresetSpeke20Audio: PresetSpeke20AudioType
    PresetSpeke20Video: PresetSpeke20VideoType


class EncryptionMethodTypeDef(TypedDict):
    TsEncryptionMethod: NotRequired[TsEncryptionMethodType]
    CmafEncryptionMethod: NotRequired[CmafEncryptionMethodType]


class FilterConfigurationOutputTypeDef(TypedDict):
    ManifestFilter: NotRequired[str]
    Start: NotRequired[datetime]
    End: NotRequired[datetime]
    TimeDelaySeconds: NotRequired[int]
    ClipStartTime: NotRequired[datetime]


TimestampTypeDef = Union[datetime, str]


class GetChannelGroupRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str


class GetChannelPolicyRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str


class GetChannelRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str


class GetOriginEndpointPolicyRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str
    OriginEndpointName: str


class GetOriginEndpointRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str
    OriginEndpointName: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListChannelGroupsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListChannelsRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListDashManifestConfigurationTypeDef(TypedDict):
    ManifestName: str
    Url: NotRequired[str]


class ListHlsManifestConfigurationTypeDef(TypedDict):
    ManifestName: str
    ChildManifestName: NotRequired[str]
    Url: NotRequired[str]


class ListLowLatencyHlsManifestConfigurationTypeDef(TypedDict):
    ManifestName: str
    ChildManifestName: NotRequired[str]
    Url: NotRequired[str]


class ListOriginEndpointsRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class PutChannelPolicyRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str
    Policy: str


class PutOriginEndpointPolicyRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str
    OriginEndpointName: str
    Policy: str


class ScteOutputTypeDef(TypedDict):
    ScteFilter: NotRequired[List[ScteFilterType]]


class ScteTypeDef(TypedDict):
    ScteFilter: NotRequired[Sequence[ScteFilterType]]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateChannelGroupRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ETag: NotRequired[str]
    Description: NotRequired[str]


class UpdateChannelRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str
    ETag: NotRequired[str]
    Description: NotRequired[str]


class CreateChannelGroupResponseTypeDef(TypedDict):
    ChannelGroupName: str
    Arn: str
    EgressDomain: str
    CreatedAt: datetime
    ModifiedAt: datetime
    ETag: str
    Description: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetChannelGroupResponseTypeDef(TypedDict):
    ChannelGroupName: str
    Arn: str
    EgressDomain: str
    CreatedAt: datetime
    ModifiedAt: datetime
    Description: str
    ETag: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetChannelPolicyResponseTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetOriginEndpointPolicyResponseTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str
    OriginEndpointName: str
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListChannelGroupsResponseTypeDef(TypedDict):
    Items: List[ChannelGroupListConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListChannelsResponseTypeDef(TypedDict):
    Items: List[ChannelListConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateChannelGroupResponseTypeDef(TypedDict):
    ChannelGroupName: str
    Arn: str
    EgressDomain: str
    CreatedAt: datetime
    ModifiedAt: datetime
    Description: str
    ETag: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateChannelResponseTypeDef(TypedDict):
    Arn: str
    ChannelName: str
    ChannelGroupName: str
    CreatedAt: datetime
    ModifiedAt: datetime
    Description: str
    IngestEndpoints: List[IngestEndpointTypeDef]
    InputType: InputTypeType
    ETag: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetChannelResponseTypeDef(TypedDict):
    Arn: str
    ChannelName: str
    ChannelGroupName: str
    CreatedAt: datetime
    ModifiedAt: datetime
    Description: str
    IngestEndpoints: List[IngestEndpointTypeDef]
    InputType: InputTypeType
    ETag: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateChannelResponseTypeDef(TypedDict):
    Arn: str
    ChannelName: str
    ChannelGroupName: str
    CreatedAt: datetime
    ModifiedAt: datetime
    Description: str
    IngestEndpoints: List[IngestEndpointTypeDef]
    InputType: InputTypeType
    ETag: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class SpekeKeyProviderOutputTypeDef(TypedDict):
    EncryptionContractConfiguration: EncryptionContractConfigurationTypeDef
    ResourceId: str
    DrmSystems: List[DrmSystemType]
    RoleArn: str
    Url: str


class SpekeKeyProviderTypeDef(TypedDict):
    EncryptionContractConfiguration: EncryptionContractConfigurationTypeDef
    ResourceId: str
    DrmSystems: Sequence[DrmSystemType]
    RoleArn: str
    Url: str


class GetDashManifestConfigurationTypeDef(TypedDict):
    ManifestName: str
    Url: str
    ManifestWindowSeconds: NotRequired[int]
    FilterConfiguration: NotRequired[FilterConfigurationOutputTypeDef]
    MinUpdatePeriodSeconds: NotRequired[int]
    MinBufferTimeSeconds: NotRequired[int]
    SuggestedPresentationDelaySeconds: NotRequired[int]
    SegmentTemplateFormat: NotRequired[Literal["NUMBER_WITH_TIMELINE"]]
    PeriodTriggers: NotRequired[List[DashPeriodTriggerType]]
    ScteDash: NotRequired[ScteDashTypeDef]
    DrmSignaling: NotRequired[DashDrmSignalingType]
    UtcTiming: NotRequired[DashUtcTimingTypeDef]


class GetHlsManifestConfigurationTypeDef(TypedDict):
    ManifestName: str
    Url: str
    ChildManifestName: NotRequired[str]
    ManifestWindowSeconds: NotRequired[int]
    ProgramDateTimeIntervalSeconds: NotRequired[int]
    ScteHls: NotRequired[ScteHlsTypeDef]
    FilterConfiguration: NotRequired[FilterConfigurationOutputTypeDef]
    StartTag: NotRequired[StartTagTypeDef]


class GetLowLatencyHlsManifestConfigurationTypeDef(TypedDict):
    ManifestName: str
    Url: str
    ChildManifestName: NotRequired[str]
    ManifestWindowSeconds: NotRequired[int]
    ProgramDateTimeIntervalSeconds: NotRequired[int]
    ScteHls: NotRequired[ScteHlsTypeDef]
    FilterConfiguration: NotRequired[FilterConfigurationOutputTypeDef]
    StartTag: NotRequired[StartTagTypeDef]


class FilterConfigurationTypeDef(TypedDict):
    ManifestFilter: NotRequired[str]
    Start: NotRequired[TimestampTypeDef]
    End: NotRequired[TimestampTypeDef]
    TimeDelaySeconds: NotRequired[int]
    ClipStartTime: NotRequired[TimestampTypeDef]


class ListChannelGroupsRequestListChannelGroupsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListChannelsRequestListChannelsPaginateTypeDef(TypedDict):
    ChannelGroupName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOriginEndpointsRequestListOriginEndpointsPaginateTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class OriginEndpointListConfigurationTypeDef(TypedDict):
    Arn: str
    ChannelGroupName: str
    ChannelName: str
    OriginEndpointName: str
    ContainerType: ContainerTypeType
    Description: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    ModifiedAt: NotRequired[datetime]
    HlsManifests: NotRequired[List[ListHlsManifestConfigurationTypeDef]]
    LowLatencyHlsManifests: NotRequired[List[ListLowLatencyHlsManifestConfigurationTypeDef]]
    DashManifests: NotRequired[List[ListDashManifestConfigurationTypeDef]]
    ForceEndpointErrorConfiguration: NotRequired[ForceEndpointErrorConfigurationOutputTypeDef]


ScteUnionTypeDef = Union[ScteTypeDef, ScteOutputTypeDef]


class EncryptionOutputTypeDef(TypedDict):
    EncryptionMethod: EncryptionMethodTypeDef
    SpekeKeyProvider: SpekeKeyProviderOutputTypeDef
    ConstantInitializationVector: NotRequired[str]
    KeyRotationIntervalSeconds: NotRequired[int]


SpekeKeyProviderUnionTypeDef = Union[SpekeKeyProviderTypeDef, SpekeKeyProviderOutputTypeDef]
FilterConfigurationUnionTypeDef = Union[
    FilterConfigurationTypeDef, FilterConfigurationOutputTypeDef
]


class ListOriginEndpointsResponseTypeDef(TypedDict):
    Items: List[OriginEndpointListConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SegmentOutputTypeDef(TypedDict):
    SegmentDurationSeconds: NotRequired[int]
    SegmentName: NotRequired[str]
    TsUseAudioRenditionGroup: NotRequired[bool]
    IncludeIframeOnlyStreams: NotRequired[bool]
    TsIncludeDvbSubtitles: NotRequired[bool]
    Scte: NotRequired[ScteOutputTypeDef]
    Encryption: NotRequired[EncryptionOutputTypeDef]


class EncryptionTypeDef(TypedDict):
    EncryptionMethod: EncryptionMethodTypeDef
    SpekeKeyProvider: SpekeKeyProviderUnionTypeDef
    ConstantInitializationVector: NotRequired[str]
    KeyRotationIntervalSeconds: NotRequired[int]


class CreateDashManifestConfigurationTypeDef(TypedDict):
    ManifestName: str
    ManifestWindowSeconds: NotRequired[int]
    FilterConfiguration: NotRequired[FilterConfigurationUnionTypeDef]
    MinUpdatePeriodSeconds: NotRequired[int]
    MinBufferTimeSeconds: NotRequired[int]
    SuggestedPresentationDelaySeconds: NotRequired[int]
    SegmentTemplateFormat: NotRequired[Literal["NUMBER_WITH_TIMELINE"]]
    PeriodTriggers: NotRequired[Sequence[DashPeriodTriggerType]]
    ScteDash: NotRequired[ScteDashTypeDef]
    DrmSignaling: NotRequired[DashDrmSignalingType]
    UtcTiming: NotRequired[DashUtcTimingTypeDef]


class CreateHlsManifestConfigurationTypeDef(TypedDict):
    ManifestName: str
    ChildManifestName: NotRequired[str]
    ScteHls: NotRequired[ScteHlsTypeDef]
    StartTag: NotRequired[StartTagTypeDef]
    ManifestWindowSeconds: NotRequired[int]
    ProgramDateTimeIntervalSeconds: NotRequired[int]
    FilterConfiguration: NotRequired[FilterConfigurationUnionTypeDef]


class CreateLowLatencyHlsManifestConfigurationTypeDef(TypedDict):
    ManifestName: str
    ChildManifestName: NotRequired[str]
    ScteHls: NotRequired[ScteHlsTypeDef]
    StartTag: NotRequired[StartTagTypeDef]
    ManifestWindowSeconds: NotRequired[int]
    ProgramDateTimeIntervalSeconds: NotRequired[int]
    FilterConfiguration: NotRequired[FilterConfigurationUnionTypeDef]


class CreateOriginEndpointResponseTypeDef(TypedDict):
    Arn: str
    ChannelGroupName: str
    ChannelName: str
    OriginEndpointName: str
    ContainerType: ContainerTypeType
    Segment: SegmentOutputTypeDef
    CreatedAt: datetime
    ModifiedAt: datetime
    Description: str
    StartoverWindowSeconds: int
    HlsManifests: List[GetHlsManifestConfigurationTypeDef]
    LowLatencyHlsManifests: List[GetLowLatencyHlsManifestConfigurationTypeDef]
    DashManifests: List[GetDashManifestConfigurationTypeDef]
    ForceEndpointErrorConfiguration: ForceEndpointErrorConfigurationOutputTypeDef
    ETag: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetOriginEndpointResponseTypeDef(TypedDict):
    Arn: str
    ChannelGroupName: str
    ChannelName: str
    OriginEndpointName: str
    ContainerType: ContainerTypeType
    Segment: SegmentOutputTypeDef
    CreatedAt: datetime
    ModifiedAt: datetime
    Description: str
    StartoverWindowSeconds: int
    HlsManifests: List[GetHlsManifestConfigurationTypeDef]
    LowLatencyHlsManifests: List[GetLowLatencyHlsManifestConfigurationTypeDef]
    DashManifests: List[GetDashManifestConfigurationTypeDef]
    ForceEndpointErrorConfiguration: ForceEndpointErrorConfigurationOutputTypeDef
    ETag: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateOriginEndpointResponseTypeDef(TypedDict):
    Arn: str
    ChannelGroupName: str
    ChannelName: str
    OriginEndpointName: str
    ContainerType: ContainerTypeType
    Segment: SegmentOutputTypeDef
    CreatedAt: datetime
    ModifiedAt: datetime
    Description: str
    StartoverWindowSeconds: int
    HlsManifests: List[GetHlsManifestConfigurationTypeDef]
    LowLatencyHlsManifests: List[GetLowLatencyHlsManifestConfigurationTypeDef]
    ForceEndpointErrorConfiguration: ForceEndpointErrorConfigurationOutputTypeDef
    ETag: str
    Tags: Dict[str, str]
    DashManifests: List[GetDashManifestConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


EncryptionUnionTypeDef = Union[EncryptionTypeDef, EncryptionOutputTypeDef]


class SegmentTypeDef(TypedDict):
    SegmentDurationSeconds: NotRequired[int]
    SegmentName: NotRequired[str]
    TsUseAudioRenditionGroup: NotRequired[bool]
    IncludeIframeOnlyStreams: NotRequired[bool]
    TsIncludeDvbSubtitles: NotRequired[bool]
    Scte: NotRequired[ScteUnionTypeDef]
    Encryption: NotRequired[EncryptionUnionTypeDef]


class CreateOriginEndpointRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str
    OriginEndpointName: str
    ContainerType: ContainerTypeType
    Segment: NotRequired[SegmentTypeDef]
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    StartoverWindowSeconds: NotRequired[int]
    HlsManifests: NotRequired[Sequence[CreateHlsManifestConfigurationTypeDef]]
    LowLatencyHlsManifests: NotRequired[Sequence[CreateLowLatencyHlsManifestConfigurationTypeDef]]
    DashManifests: NotRequired[Sequence[CreateDashManifestConfigurationTypeDef]]
    ForceEndpointErrorConfiguration: NotRequired[ForceEndpointErrorConfigurationTypeDef]
    Tags: NotRequired[Mapping[str, str]]


class UpdateOriginEndpointRequestRequestTypeDef(TypedDict):
    ChannelGroupName: str
    ChannelName: str
    OriginEndpointName: str
    ContainerType: ContainerTypeType
    Segment: NotRequired[SegmentTypeDef]
    Description: NotRequired[str]
    StartoverWindowSeconds: NotRequired[int]
    HlsManifests: NotRequired[Sequence[CreateHlsManifestConfigurationTypeDef]]
    LowLatencyHlsManifests: NotRequired[Sequence[CreateLowLatencyHlsManifestConfigurationTypeDef]]
    DashManifests: NotRequired[Sequence[CreateDashManifestConfigurationTypeDef]]
    ForceEndpointErrorConfiguration: NotRequired[ForceEndpointErrorConfigurationTypeDef]
    ETag: NotRequired[str]
