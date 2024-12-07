"""
Type annotations for ivs service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/type_defs/)

Usage::

    ```python
    from types_aiobotocore_ivs.type_defs import AudioConfigurationTypeDef

    data: AudioConfigurationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ChannelLatencyModeType,
    ChannelTypeType,
    RecordingConfigurationStateType,
    RecordingModeType,
    RenditionConfigurationRenditionSelectionType,
    RenditionConfigurationRenditionType,
    StreamHealthType,
    StreamStateType,
    ThumbnailConfigurationResolutionType,
    ThumbnailConfigurationStorageType,
    TranscodePresetType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AudioConfigurationTypeDef",
    "BatchErrorTypeDef",
    "BatchGetChannelRequestRequestTypeDef",
    "BatchGetChannelResponseTypeDef",
    "BatchGetStreamKeyRequestRequestTypeDef",
    "BatchGetStreamKeyResponseTypeDef",
    "BatchStartViewerSessionRevocationErrorTypeDef",
    "BatchStartViewerSessionRevocationRequestRequestTypeDef",
    "BatchStartViewerSessionRevocationResponseTypeDef",
    "BatchStartViewerSessionRevocationViewerSessionTypeDef",
    "ChannelSummaryTypeDef",
    "ChannelTypeDef",
    "CreateChannelRequestRequestTypeDef",
    "CreateChannelResponseTypeDef",
    "CreatePlaybackRestrictionPolicyRequestRequestTypeDef",
    "CreatePlaybackRestrictionPolicyResponseTypeDef",
    "CreateRecordingConfigurationRequestRequestTypeDef",
    "CreateRecordingConfigurationResponseTypeDef",
    "CreateStreamKeyRequestRequestTypeDef",
    "CreateStreamKeyResponseTypeDef",
    "DeleteChannelRequestRequestTypeDef",
    "DeletePlaybackKeyPairRequestRequestTypeDef",
    "DeletePlaybackRestrictionPolicyRequestRequestTypeDef",
    "DeleteRecordingConfigurationRequestRequestTypeDef",
    "DeleteStreamKeyRequestRequestTypeDef",
    "DestinationConfigurationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetChannelRequestRequestTypeDef",
    "GetChannelResponseTypeDef",
    "GetPlaybackKeyPairRequestRequestTypeDef",
    "GetPlaybackKeyPairResponseTypeDef",
    "GetPlaybackRestrictionPolicyRequestRequestTypeDef",
    "GetPlaybackRestrictionPolicyResponseTypeDef",
    "GetRecordingConfigurationRequestRequestTypeDef",
    "GetRecordingConfigurationResponseTypeDef",
    "GetStreamKeyRequestRequestTypeDef",
    "GetStreamKeyResponseTypeDef",
    "GetStreamRequestRequestTypeDef",
    "GetStreamResponseTypeDef",
    "GetStreamSessionRequestRequestTypeDef",
    "GetStreamSessionResponseTypeDef",
    "ImportPlaybackKeyPairRequestRequestTypeDef",
    "ImportPlaybackKeyPairResponseTypeDef",
    "IngestConfigurationTypeDef",
    "ListChannelsRequestListChannelsPaginateTypeDef",
    "ListChannelsRequestRequestTypeDef",
    "ListChannelsResponseTypeDef",
    "ListPlaybackKeyPairsRequestListPlaybackKeyPairsPaginateTypeDef",
    "ListPlaybackKeyPairsRequestRequestTypeDef",
    "ListPlaybackKeyPairsResponseTypeDef",
    "ListPlaybackRestrictionPoliciesRequestRequestTypeDef",
    "ListPlaybackRestrictionPoliciesResponseTypeDef",
    "ListRecordingConfigurationsRequestListRecordingConfigurationsPaginateTypeDef",
    "ListRecordingConfigurationsRequestRequestTypeDef",
    "ListRecordingConfigurationsResponseTypeDef",
    "ListStreamKeysRequestListStreamKeysPaginateTypeDef",
    "ListStreamKeysRequestRequestTypeDef",
    "ListStreamKeysResponseTypeDef",
    "ListStreamSessionsRequestRequestTypeDef",
    "ListStreamSessionsResponseTypeDef",
    "ListStreamsRequestListStreamsPaginateTypeDef",
    "ListStreamsRequestRequestTypeDef",
    "ListStreamsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PlaybackKeyPairSummaryTypeDef",
    "PlaybackKeyPairTypeDef",
    "PlaybackRestrictionPolicySummaryTypeDef",
    "PlaybackRestrictionPolicyTypeDef",
    "PutMetadataRequestRequestTypeDef",
    "RecordingConfigurationSummaryTypeDef",
    "RecordingConfigurationTypeDef",
    "RenditionConfigurationOutputTypeDef",
    "RenditionConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "S3DestinationConfigurationTypeDef",
    "SrtTypeDef",
    "StartViewerSessionRevocationRequestRequestTypeDef",
    "StopStreamRequestRequestTypeDef",
    "StreamEventTypeDef",
    "StreamFiltersTypeDef",
    "StreamKeySummaryTypeDef",
    "StreamKeyTypeDef",
    "StreamSessionSummaryTypeDef",
    "StreamSessionTypeDef",
    "StreamSummaryTypeDef",
    "StreamTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ThumbnailConfigurationOutputTypeDef",
    "ThumbnailConfigurationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateChannelRequestRequestTypeDef",
    "UpdateChannelResponseTypeDef",
    "UpdatePlaybackRestrictionPolicyRequestRequestTypeDef",
    "UpdatePlaybackRestrictionPolicyResponseTypeDef",
    "VideoConfigurationTypeDef",
)


class AudioConfigurationTypeDef(TypedDict):
    codec: NotRequired[str]
    targetBitrate: NotRequired[int]
    sampleRate: NotRequired[int]
    channels: NotRequired[int]


class BatchErrorTypeDef(TypedDict):
    arn: NotRequired[str]
    code: NotRequired[str]
    message: NotRequired[str]


class BatchGetChannelRequestRequestTypeDef(TypedDict):
    arns: Sequence[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class BatchGetStreamKeyRequestRequestTypeDef(TypedDict):
    arns: Sequence[str]


class StreamKeyTypeDef(TypedDict):
    arn: NotRequired[str]
    value: NotRequired[str]
    channelArn: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class BatchStartViewerSessionRevocationErrorTypeDef(TypedDict):
    channelArn: str
    viewerId: str
    code: NotRequired[str]
    message: NotRequired[str]


class BatchStartViewerSessionRevocationViewerSessionTypeDef(TypedDict):
    channelArn: str
    viewerId: str
    viewerSessionVersionsLessThanOrEqualTo: NotRequired[int]


ChannelSummaryTypeDef = TypedDict(
    "ChannelSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "latencyMode": NotRequired[ChannelLatencyModeType],
        "authorized": NotRequired[bool],
        "recordingConfigurationArn": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "insecureIngest": NotRequired[bool],
        "type": NotRequired[ChannelTypeType],
        "preset": NotRequired[TranscodePresetType],
        "playbackRestrictionPolicyArn": NotRequired[str],
    },
)


class SrtTypeDef(TypedDict):
    endpoint: NotRequired[str]
    passphrase: NotRequired[str]


CreateChannelRequestRequestTypeDef = TypedDict(
    "CreateChannelRequestRequestTypeDef",
    {
        "name": NotRequired[str],
        "latencyMode": NotRequired[ChannelLatencyModeType],
        "type": NotRequired[ChannelTypeType],
        "authorized": NotRequired[bool],
        "recordingConfigurationArn": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
        "insecureIngest": NotRequired[bool],
        "preset": NotRequired[TranscodePresetType],
        "playbackRestrictionPolicyArn": NotRequired[str],
    },
)


class CreatePlaybackRestrictionPolicyRequestRequestTypeDef(TypedDict):
    allowedCountries: NotRequired[Sequence[str]]
    allowedOrigins: NotRequired[Sequence[str]]
    enableStrictOriginEnforcement: NotRequired[bool]
    name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class PlaybackRestrictionPolicyTypeDef(TypedDict):
    arn: str
    allowedCountries: List[str]
    allowedOrigins: List[str]
    enableStrictOriginEnforcement: NotRequired[bool]
    name: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class RenditionConfigurationTypeDef(TypedDict):
    renditionSelection: NotRequired[RenditionConfigurationRenditionSelectionType]
    renditions: NotRequired[Sequence[RenditionConfigurationRenditionType]]


class ThumbnailConfigurationTypeDef(TypedDict):
    recordingMode: NotRequired[RecordingModeType]
    targetIntervalSeconds: NotRequired[int]
    resolution: NotRequired[ThumbnailConfigurationResolutionType]
    storage: NotRequired[Sequence[ThumbnailConfigurationStorageType]]


class CreateStreamKeyRequestRequestTypeDef(TypedDict):
    channelArn: str
    tags: NotRequired[Mapping[str, str]]


class DeleteChannelRequestRequestTypeDef(TypedDict):
    arn: str


class DeletePlaybackKeyPairRequestRequestTypeDef(TypedDict):
    arn: str


class DeletePlaybackRestrictionPolicyRequestRequestTypeDef(TypedDict):
    arn: str


class DeleteRecordingConfigurationRequestRequestTypeDef(TypedDict):
    arn: str


class DeleteStreamKeyRequestRequestTypeDef(TypedDict):
    arn: str


class S3DestinationConfigurationTypeDef(TypedDict):
    bucketName: str


class GetChannelRequestRequestTypeDef(TypedDict):
    arn: str


class GetPlaybackKeyPairRequestRequestTypeDef(TypedDict):
    arn: str


class PlaybackKeyPairTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    fingerprint: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class GetPlaybackRestrictionPolicyRequestRequestTypeDef(TypedDict):
    arn: str


class GetRecordingConfigurationRequestRequestTypeDef(TypedDict):
    arn: str


class GetStreamKeyRequestRequestTypeDef(TypedDict):
    arn: str


class GetStreamRequestRequestTypeDef(TypedDict):
    channelArn: str


class StreamTypeDef(TypedDict):
    channelArn: NotRequired[str]
    streamId: NotRequired[str]
    playbackUrl: NotRequired[str]
    startTime: NotRequired[datetime]
    state: NotRequired[StreamStateType]
    health: NotRequired[StreamHealthType]
    viewerCount: NotRequired[int]


class GetStreamSessionRequestRequestTypeDef(TypedDict):
    channelArn: str
    streamId: NotRequired[str]


class ImportPlaybackKeyPairRequestRequestTypeDef(TypedDict):
    publicKeyMaterial: str
    name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class VideoConfigurationTypeDef(TypedDict):
    avcProfile: NotRequired[str]
    avcLevel: NotRequired[str]
    codec: NotRequired[str]
    encoder: NotRequired[str]
    targetBitrate: NotRequired[int]
    targetFramerate: NotRequired[int]
    videoHeight: NotRequired[int]
    videoWidth: NotRequired[int]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListChannelsRequestRequestTypeDef(TypedDict):
    filterByName: NotRequired[str]
    filterByRecordingConfigurationArn: NotRequired[str]
    filterByPlaybackRestrictionPolicyArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListPlaybackKeyPairsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class PlaybackKeyPairSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class ListPlaybackRestrictionPoliciesRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class PlaybackRestrictionPolicySummaryTypeDef(TypedDict):
    arn: str
    allowedCountries: List[str]
    allowedOrigins: List[str]
    enableStrictOriginEnforcement: NotRequired[bool]
    name: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class ListRecordingConfigurationsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListStreamKeysRequestRequestTypeDef(TypedDict):
    channelArn: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class StreamKeySummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    channelArn: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class ListStreamSessionsRequestRequestTypeDef(TypedDict):
    channelArn: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class StreamSessionSummaryTypeDef(TypedDict):
    streamId: NotRequired[str]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    hasErrorEvent: NotRequired[bool]


class StreamFiltersTypeDef(TypedDict):
    health: NotRequired[StreamHealthType]


class StreamSummaryTypeDef(TypedDict):
    channelArn: NotRequired[str]
    streamId: NotRequired[str]
    state: NotRequired[StreamStateType]
    health: NotRequired[StreamHealthType]
    viewerCount: NotRequired[int]
    startTime: NotRequired[datetime]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class PutMetadataRequestRequestTypeDef(TypedDict):
    channelArn: str
    metadata: str


class RenditionConfigurationOutputTypeDef(TypedDict):
    renditionSelection: NotRequired[RenditionConfigurationRenditionSelectionType]
    renditions: NotRequired[List[RenditionConfigurationRenditionType]]


class ThumbnailConfigurationOutputTypeDef(TypedDict):
    recordingMode: NotRequired[RecordingModeType]
    targetIntervalSeconds: NotRequired[int]
    resolution: NotRequired[ThumbnailConfigurationResolutionType]
    storage: NotRequired[List[ThumbnailConfigurationStorageType]]


class StartViewerSessionRevocationRequestRequestTypeDef(TypedDict):
    channelArn: str
    viewerId: str
    viewerSessionVersionsLessThanOrEqualTo: NotRequired[int]


class StopStreamRequestRequestTypeDef(TypedDict):
    channelArn: str


StreamEventTypeDef = TypedDict(
    "StreamEventTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "eventTime": NotRequired[datetime],
    },
)


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


UpdateChannelRequestRequestTypeDef = TypedDict(
    "UpdateChannelRequestRequestTypeDef",
    {
        "arn": str,
        "name": NotRequired[str],
        "latencyMode": NotRequired[ChannelLatencyModeType],
        "type": NotRequired[ChannelTypeType],
        "authorized": NotRequired[bool],
        "recordingConfigurationArn": NotRequired[str],
        "insecureIngest": NotRequired[bool],
        "preset": NotRequired[TranscodePresetType],
        "playbackRestrictionPolicyArn": NotRequired[str],
    },
)


class UpdatePlaybackRestrictionPolicyRequestRequestTypeDef(TypedDict):
    arn: str
    allowedCountries: NotRequired[Sequence[str]]
    allowedOrigins: NotRequired[Sequence[str]]
    enableStrictOriginEnforcement: NotRequired[bool]
    name: NotRequired[str]


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetStreamKeyResponseTypeDef(TypedDict):
    streamKeys: List[StreamKeyTypeDef]
    errors: List[BatchErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateStreamKeyResponseTypeDef(TypedDict):
    streamKey: StreamKeyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetStreamKeyResponseTypeDef(TypedDict):
    streamKey: StreamKeyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class BatchStartViewerSessionRevocationResponseTypeDef(TypedDict):
    errors: List[BatchStartViewerSessionRevocationErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchStartViewerSessionRevocationRequestRequestTypeDef(TypedDict):
    viewerSessions: Sequence[BatchStartViewerSessionRevocationViewerSessionTypeDef]


class ListChannelsResponseTypeDef(TypedDict):
    channels: List[ChannelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


ChannelTypeDef = TypedDict(
    "ChannelTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "latencyMode": NotRequired[ChannelLatencyModeType],
        "type": NotRequired[ChannelTypeType],
        "recordingConfigurationArn": NotRequired[str],
        "ingestEndpoint": NotRequired[str],
        "playbackUrl": NotRequired[str],
        "authorized": NotRequired[bool],
        "tags": NotRequired[Dict[str, str]],
        "insecureIngest": NotRequired[bool],
        "preset": NotRequired[TranscodePresetType],
        "srt": NotRequired[SrtTypeDef],
        "playbackRestrictionPolicyArn": NotRequired[str],
    },
)


class CreatePlaybackRestrictionPolicyResponseTypeDef(TypedDict):
    playbackRestrictionPolicy: PlaybackRestrictionPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetPlaybackRestrictionPolicyResponseTypeDef(TypedDict):
    playbackRestrictionPolicy: PlaybackRestrictionPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePlaybackRestrictionPolicyResponseTypeDef(TypedDict):
    playbackRestrictionPolicy: PlaybackRestrictionPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DestinationConfigurationTypeDef(TypedDict):
    s3: NotRequired[S3DestinationConfigurationTypeDef]


class GetPlaybackKeyPairResponseTypeDef(TypedDict):
    keyPair: PlaybackKeyPairTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ImportPlaybackKeyPairResponseTypeDef(TypedDict):
    keyPair: PlaybackKeyPairTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetStreamResponseTypeDef(TypedDict):
    stream: StreamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class IngestConfigurationTypeDef(TypedDict):
    video: NotRequired[VideoConfigurationTypeDef]
    audio: NotRequired[AudioConfigurationTypeDef]


class ListChannelsRequestListChannelsPaginateTypeDef(TypedDict):
    filterByName: NotRequired[str]
    filterByRecordingConfigurationArn: NotRequired[str]
    filterByPlaybackRestrictionPolicyArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPlaybackKeyPairsRequestListPlaybackKeyPairsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRecordingConfigurationsRequestListRecordingConfigurationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStreamKeysRequestListStreamKeysPaginateTypeDef(TypedDict):
    channelArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPlaybackKeyPairsResponseTypeDef(TypedDict):
    keyPairs: List[PlaybackKeyPairSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPlaybackRestrictionPoliciesResponseTypeDef(TypedDict):
    playbackRestrictionPolicies: List[PlaybackRestrictionPolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListStreamKeysResponseTypeDef(TypedDict):
    streamKeys: List[StreamKeySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListStreamSessionsResponseTypeDef(TypedDict):
    streamSessions: List[StreamSessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListStreamsRequestListStreamsPaginateTypeDef(TypedDict):
    filterBy: NotRequired[StreamFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStreamsRequestRequestTypeDef(TypedDict):
    filterBy: NotRequired[StreamFiltersTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListStreamsResponseTypeDef(TypedDict):
    streams: List[StreamSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class BatchGetChannelResponseTypeDef(TypedDict):
    channels: List[ChannelTypeDef]
    errors: List[BatchErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateChannelResponseTypeDef(TypedDict):
    channel: ChannelTypeDef
    streamKey: StreamKeyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetChannelResponseTypeDef(TypedDict):
    channel: ChannelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateChannelResponseTypeDef(TypedDict):
    channel: ChannelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRecordingConfigurationRequestRequestTypeDef(TypedDict):
    destinationConfiguration: DestinationConfigurationTypeDef
    name: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    thumbnailConfiguration: NotRequired[ThumbnailConfigurationTypeDef]
    recordingReconnectWindowSeconds: NotRequired[int]
    renditionConfiguration: NotRequired[RenditionConfigurationTypeDef]


class RecordingConfigurationSummaryTypeDef(TypedDict):
    arn: str
    destinationConfiguration: DestinationConfigurationTypeDef
    state: RecordingConfigurationStateType
    name: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class RecordingConfigurationTypeDef(TypedDict):
    arn: str
    destinationConfiguration: DestinationConfigurationTypeDef
    state: RecordingConfigurationStateType
    name: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    thumbnailConfiguration: NotRequired[ThumbnailConfigurationOutputTypeDef]
    recordingReconnectWindowSeconds: NotRequired[int]
    renditionConfiguration: NotRequired[RenditionConfigurationOutputTypeDef]


class ListRecordingConfigurationsResponseTypeDef(TypedDict):
    recordingConfigurations: List[RecordingConfigurationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateRecordingConfigurationResponseTypeDef(TypedDict):
    recordingConfiguration: RecordingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetRecordingConfigurationResponseTypeDef(TypedDict):
    recordingConfiguration: RecordingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StreamSessionTypeDef(TypedDict):
    streamId: NotRequired[str]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    channel: NotRequired[ChannelTypeDef]
    ingestConfiguration: NotRequired[IngestConfigurationTypeDef]
    recordingConfiguration: NotRequired[RecordingConfigurationTypeDef]
    truncatedEvents: NotRequired[List[StreamEventTypeDef]]


class GetStreamSessionResponseTypeDef(TypedDict):
    streamSession: StreamSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
