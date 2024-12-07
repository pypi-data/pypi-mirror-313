"""
Type annotations for kinesisvideo service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesisvideo.client import KinesisVideoClient

    session = get_session()
    async with session.create_client("kinesisvideo") as client:
        client: KinesisVideoClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    DescribeMappedResourceConfigurationPaginator,
    ListEdgeAgentConfigurationsPaginator,
    ListSignalingChannelsPaginator,
    ListStreamsPaginator,
)
from .type_defs import (
    CreateSignalingChannelInputRequestTypeDef,
    CreateSignalingChannelOutputTypeDef,
    CreateStreamInputRequestTypeDef,
    CreateStreamOutputTypeDef,
    DeleteEdgeConfigurationInputRequestTypeDef,
    DeleteSignalingChannelInputRequestTypeDef,
    DeleteStreamInputRequestTypeDef,
    DescribeEdgeConfigurationInputRequestTypeDef,
    DescribeEdgeConfigurationOutputTypeDef,
    DescribeImageGenerationConfigurationInputRequestTypeDef,
    DescribeImageGenerationConfigurationOutputTypeDef,
    DescribeMappedResourceConfigurationInputRequestTypeDef,
    DescribeMappedResourceConfigurationOutputTypeDef,
    DescribeMediaStorageConfigurationInputRequestTypeDef,
    DescribeMediaStorageConfigurationOutputTypeDef,
    DescribeNotificationConfigurationInputRequestTypeDef,
    DescribeNotificationConfigurationOutputTypeDef,
    DescribeSignalingChannelInputRequestTypeDef,
    DescribeSignalingChannelOutputTypeDef,
    DescribeStreamInputRequestTypeDef,
    DescribeStreamOutputTypeDef,
    GetDataEndpointInputRequestTypeDef,
    GetDataEndpointOutputTypeDef,
    GetSignalingChannelEndpointInputRequestTypeDef,
    GetSignalingChannelEndpointOutputTypeDef,
    ListEdgeAgentConfigurationsInputRequestTypeDef,
    ListEdgeAgentConfigurationsOutputTypeDef,
    ListSignalingChannelsInputRequestTypeDef,
    ListSignalingChannelsOutputTypeDef,
    ListStreamsInputRequestTypeDef,
    ListStreamsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTagsForStreamInputRequestTypeDef,
    ListTagsForStreamOutputTypeDef,
    StartEdgeConfigurationUpdateInputRequestTypeDef,
    StartEdgeConfigurationUpdateOutputTypeDef,
    TagResourceInputRequestTypeDef,
    TagStreamInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UntagStreamInputRequestTypeDef,
    UpdateDataRetentionInputRequestTypeDef,
    UpdateImageGenerationConfigurationInputRequestTypeDef,
    UpdateMediaStorageConfigurationInputRequestTypeDef,
    UpdateNotificationConfigurationInputRequestTypeDef,
    UpdateSignalingChannelInputRequestTypeDef,
    UpdateStreamInputRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("KinesisVideoClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AccountChannelLimitExceededException: Type[BotocoreClientError]
    AccountStreamLimitExceededException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientLimitExceededException: Type[BotocoreClientError]
    DeviceStreamLimitExceededException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidDeviceException: Type[BotocoreClientError]
    InvalidResourceFormatException: Type[BotocoreClientError]
    NoDataRetentionException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    StreamEdgeConfigurationNotFoundException: Type[BotocoreClientError]
    TagsPerResourceExceededLimitException: Type[BotocoreClientError]
    VersionMismatchException: Type[BotocoreClientError]


class KinesisVideoClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KinesisVideoClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#close)
        """

    async def create_signaling_channel(
        self, **kwargs: Unpack[CreateSignalingChannelInputRequestTypeDef]
    ) -> CreateSignalingChannelOutputTypeDef:
        """
        Creates a signaling channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/create_signaling_channel.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#create_signaling_channel)
        """

    async def create_stream(
        self, **kwargs: Unpack[CreateStreamInputRequestTypeDef]
    ) -> CreateStreamOutputTypeDef:
        """
        Creates a new Kinesis video stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/create_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#create_stream)
        """

    async def delete_edge_configuration(
        self, **kwargs: Unpack[DeleteEdgeConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        An asynchronous API that deletes a stream's existing edge configuration, as
        well as the corresponding media from the Edge Agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/delete_edge_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#delete_edge_configuration)
        """

    async def delete_signaling_channel(
        self, **kwargs: Unpack[DeleteSignalingChannelInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specified signaling channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/delete_signaling_channel.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#delete_signaling_channel)
        """

    async def delete_stream(
        self, **kwargs: Unpack[DeleteStreamInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Kinesis video stream and the data contained in the stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/delete_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#delete_stream)
        """

    async def describe_edge_configuration(
        self, **kwargs: Unpack[DescribeEdgeConfigurationInputRequestTypeDef]
    ) -> DescribeEdgeConfigurationOutputTypeDef:
        """
        Describes a stream's edge configuration that was set using the
        <code>StartEdgeConfigurationUpdate</code> API and the latest status of the edge
        agent's recorder and uploader jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/describe_edge_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#describe_edge_configuration)
        """

    async def describe_image_generation_configuration(
        self, **kwargs: Unpack[DescribeImageGenerationConfigurationInputRequestTypeDef]
    ) -> DescribeImageGenerationConfigurationOutputTypeDef:
        """
        Gets the <code>ImageGenerationConfiguration</code> for a given Kinesis video
        stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/describe_image_generation_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#describe_image_generation_configuration)
        """

    async def describe_mapped_resource_configuration(
        self, **kwargs: Unpack[DescribeMappedResourceConfigurationInputRequestTypeDef]
    ) -> DescribeMappedResourceConfigurationOutputTypeDef:
        """
        Returns the most current information about the stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/describe_mapped_resource_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#describe_mapped_resource_configuration)
        """

    async def describe_media_storage_configuration(
        self, **kwargs: Unpack[DescribeMediaStorageConfigurationInputRequestTypeDef]
    ) -> DescribeMediaStorageConfigurationOutputTypeDef:
        """
        Returns the most current information about the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/describe_media_storage_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#describe_media_storage_configuration)
        """

    async def describe_notification_configuration(
        self, **kwargs: Unpack[DescribeNotificationConfigurationInputRequestTypeDef]
    ) -> DescribeNotificationConfigurationOutputTypeDef:
        """
        Gets the <code>NotificationConfiguration</code> for a given Kinesis video
        stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/describe_notification_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#describe_notification_configuration)
        """

    async def describe_signaling_channel(
        self, **kwargs: Unpack[DescribeSignalingChannelInputRequestTypeDef]
    ) -> DescribeSignalingChannelOutputTypeDef:
        """
        Returns the most current information about the signaling channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/describe_signaling_channel.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#describe_signaling_channel)
        """

    async def describe_stream(
        self, **kwargs: Unpack[DescribeStreamInputRequestTypeDef]
    ) -> DescribeStreamOutputTypeDef:
        """
        Returns the most current information about the specified stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/describe_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#describe_stream)
        """

    async def get_data_endpoint(
        self, **kwargs: Unpack[GetDataEndpointInputRequestTypeDef]
    ) -> GetDataEndpointOutputTypeDef:
        """
        Gets an endpoint for a specified stream for either reading or writing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/get_data_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#get_data_endpoint)
        """

    async def get_signaling_channel_endpoint(
        self, **kwargs: Unpack[GetSignalingChannelEndpointInputRequestTypeDef]
    ) -> GetSignalingChannelEndpointOutputTypeDef:
        """
        Provides an endpoint for the specified signaling channel to send and receive
        messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/get_signaling_channel_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#get_signaling_channel_endpoint)
        """

    async def list_edge_agent_configurations(
        self, **kwargs: Unpack[ListEdgeAgentConfigurationsInputRequestTypeDef]
    ) -> ListEdgeAgentConfigurationsOutputTypeDef:
        """
        Returns an array of edge configurations associated with the specified Edge
        Agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/list_edge_agent_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#list_edge_agent_configurations)
        """

    async def list_signaling_channels(
        self, **kwargs: Unpack[ListSignalingChannelsInputRequestTypeDef]
    ) -> ListSignalingChannelsOutputTypeDef:
        """
        Returns an array of <code>ChannelInfo</code> objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/list_signaling_channels.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#list_signaling_channels)
        """

    async def list_streams(
        self, **kwargs: Unpack[ListStreamsInputRequestTypeDef]
    ) -> ListStreamsOutputTypeDef:
        """
        Returns an array of <code>StreamInfo</code> objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/list_streams.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#list_streams)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Returns a list of tags associated with the specified signaling channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#list_tags_for_resource)
        """

    async def list_tags_for_stream(
        self, **kwargs: Unpack[ListTagsForStreamInputRequestTypeDef]
    ) -> ListTagsForStreamOutputTypeDef:
        """
        Returns a list of tags associated with the specified stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/list_tags_for_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#list_tags_for_stream)
        """

    async def start_edge_configuration_update(
        self, **kwargs: Unpack[StartEdgeConfigurationUpdateInputRequestTypeDef]
    ) -> StartEdgeConfigurationUpdateOutputTypeDef:
        """
        An asynchronous API that updates a stream's existing edge configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/start_edge_configuration_update.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#start_edge_configuration_update)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds one or more tags to a signaling channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#tag_resource)
        """

    async def tag_stream(self, **kwargs: Unpack[TagStreamInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to a stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/tag_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#tag_stream)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from a signaling channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#untag_resource)
        """

    async def untag_stream(
        self, **kwargs: Unpack[UntagStreamInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from a stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/untag_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#untag_stream)
        """

    async def update_data_retention(
        self, **kwargs: Unpack[UpdateDataRetentionInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Increases or decreases the stream's data retention period by the value that you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/update_data_retention.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#update_data_retention)
        """

    async def update_image_generation_configuration(
        self, **kwargs: Unpack[UpdateImageGenerationConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the <code>StreamInfo</code> and
        <code>ImageProcessingConfiguration</code> fields.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/update_image_generation_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#update_image_generation_configuration)
        """

    async def update_media_storage_configuration(
        self, **kwargs: Unpack[UpdateMediaStorageConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a <code>SignalingChannel</code> to a stream to store the media.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/update_media_storage_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#update_media_storage_configuration)
        """

    async def update_notification_configuration(
        self, **kwargs: Unpack[UpdateNotificationConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the notification information for a stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/update_notification_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#update_notification_configuration)
        """

    async def update_signaling_channel(
        self, **kwargs: Unpack[UpdateSignalingChannelInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the existing signaling channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/update_signaling_channel.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#update_signaling_channel)
        """

    async def update_stream(
        self, **kwargs: Unpack[UpdateStreamInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates stream metadata, such as the device name and media type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/update_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#update_stream)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_mapped_resource_configuration"]
    ) -> DescribeMappedResourceConfigurationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_edge_agent_configurations"]
    ) -> ListEdgeAgentConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_signaling_channels"]
    ) -> ListSignalingChannelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_streams"]) -> ListStreamsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/#get_paginator)
        """

    async def __aenter__(self) -> "KinesisVideoClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo.html#KinesisVideo.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/client/)
        """
