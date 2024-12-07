"""
Type annotations for kinesis service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesis.client import KinesisClient

    session = get_session()
    async with session.create_client("kinesis") as client:
        client: KinesisClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    DescribeStreamPaginator,
    ListShardsPaginator,
    ListStreamConsumersPaginator,
    ListStreamsPaginator,
)
from .type_defs import (
    AddTagsToStreamInputRequestTypeDef,
    CreateStreamInputRequestTypeDef,
    DecreaseStreamRetentionPeriodInputRequestTypeDef,
    DeleteResourcePolicyInputRequestTypeDef,
    DeleteStreamInputRequestTypeDef,
    DeregisterStreamConsumerInputRequestTypeDef,
    DescribeLimitsOutputTypeDef,
    DescribeStreamConsumerInputRequestTypeDef,
    DescribeStreamConsumerOutputTypeDef,
    DescribeStreamInputRequestTypeDef,
    DescribeStreamOutputTypeDef,
    DescribeStreamSummaryInputRequestTypeDef,
    DescribeStreamSummaryOutputTypeDef,
    DisableEnhancedMonitoringInputRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableEnhancedMonitoringInputRequestTypeDef,
    EnhancedMonitoringOutputTypeDef,
    GetRecordsInputRequestTypeDef,
    GetRecordsOutputTypeDef,
    GetResourcePolicyInputRequestTypeDef,
    GetResourcePolicyOutputTypeDef,
    GetShardIteratorInputRequestTypeDef,
    GetShardIteratorOutputTypeDef,
    IncreaseStreamRetentionPeriodInputRequestTypeDef,
    ListShardsInputRequestTypeDef,
    ListShardsOutputTypeDef,
    ListStreamConsumersInputRequestTypeDef,
    ListStreamConsumersOutputTypeDef,
    ListStreamsInputRequestTypeDef,
    ListStreamsOutputTypeDef,
    ListTagsForStreamInputRequestTypeDef,
    ListTagsForStreamOutputTypeDef,
    MergeShardsInputRequestTypeDef,
    PutRecordInputRequestTypeDef,
    PutRecordOutputTypeDef,
    PutRecordsInputRequestTypeDef,
    PutRecordsOutputTypeDef,
    PutResourcePolicyInputRequestTypeDef,
    RegisterStreamConsumerInputRequestTypeDef,
    RegisterStreamConsumerOutputTypeDef,
    RemoveTagsFromStreamInputRequestTypeDef,
    SplitShardInputRequestTypeDef,
    StartStreamEncryptionInputRequestTypeDef,
    StopStreamEncryptionInputRequestTypeDef,
    SubscribeToShardInputRequestTypeDef,
    SubscribeToShardOutputTypeDef,
    UpdateShardCountInputRequestTypeDef,
    UpdateShardCountOutputTypeDef,
    UpdateStreamModeInputRequestTypeDef,
)
from .waiter import StreamExistsWaiter, StreamNotExistsWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("KinesisClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ExpiredIteratorException: Type[BotocoreClientError]
    ExpiredNextTokenException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    KMSAccessDeniedException: Type[BotocoreClientError]
    KMSDisabledException: Type[BotocoreClientError]
    KMSInvalidStateException: Type[BotocoreClientError]
    KMSNotFoundException: Type[BotocoreClientError]
    KMSOptInRequired: Type[BotocoreClientError]
    KMSThrottlingException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ProvisionedThroughputExceededException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class KinesisClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KinesisClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#close)
        """

    async def add_tags_to_stream(
        self, **kwargs: Unpack[AddTagsToStreamInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates tags for the specified Kinesis data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/add_tags_to_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#add_tags_to_stream)
        """

    async def create_stream(
        self, **kwargs: Unpack[CreateStreamInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a Kinesis data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/create_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#create_stream)
        """

    async def decrease_stream_retention_period(
        self, **kwargs: Unpack[DecreaseStreamRetentionPeriodInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Decreases the Kinesis data stream's retention period, which is the length of
        time data records are accessible after they are added to the stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/decrease_stream_retention_period.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#decrease_stream_retention_period)
        """

    async def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a policy for the specified data stream or consumer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/delete_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#delete_resource_policy)
        """

    async def delete_stream(
        self, **kwargs: Unpack[DeleteStreamInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Kinesis data stream and all its shards and data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/delete_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#delete_stream)
        """

    async def deregister_stream_consumer(
        self, **kwargs: Unpack[DeregisterStreamConsumerInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        To deregister a consumer, provide its ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/deregister_stream_consumer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#deregister_stream_consumer)
        """

    async def describe_limits(self) -> DescribeLimitsOutputTypeDef:
        """
        Describes the shard limits and usage for the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/describe_limits.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#describe_limits)
        """

    async def describe_stream(
        self, **kwargs: Unpack[DescribeStreamInputRequestTypeDef]
    ) -> DescribeStreamOutputTypeDef:
        """
        Describes the specified Kinesis data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/describe_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#describe_stream)
        """

    async def describe_stream_consumer(
        self, **kwargs: Unpack[DescribeStreamConsumerInputRequestTypeDef]
    ) -> DescribeStreamConsumerOutputTypeDef:
        """
        To get the description of a registered consumer, provide the ARN of the
        consumer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/describe_stream_consumer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#describe_stream_consumer)
        """

    async def describe_stream_summary(
        self, **kwargs: Unpack[DescribeStreamSummaryInputRequestTypeDef]
    ) -> DescribeStreamSummaryOutputTypeDef:
        """
        Provides a summarized description of the specified Kinesis data stream without
        the shard list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/describe_stream_summary.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#describe_stream_summary)
        """

    async def disable_enhanced_monitoring(
        self, **kwargs: Unpack[DisableEnhancedMonitoringInputRequestTypeDef]
    ) -> EnhancedMonitoringOutputTypeDef:
        """
        Disables enhanced monitoring.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/disable_enhanced_monitoring.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#disable_enhanced_monitoring)
        """

    async def enable_enhanced_monitoring(
        self, **kwargs: Unpack[EnableEnhancedMonitoringInputRequestTypeDef]
    ) -> EnhancedMonitoringOutputTypeDef:
        """
        Enables enhanced Kinesis data stream monitoring for shard-level metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/enable_enhanced_monitoring.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#enable_enhanced_monitoring)
        """

    async def get_records(
        self, **kwargs: Unpack[GetRecordsInputRequestTypeDef]
    ) -> GetRecordsOutputTypeDef:
        """
        Gets data records from a Kinesis data stream's shard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_records.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#get_records)
        """

    async def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyInputRequestTypeDef]
    ) -> GetResourcePolicyOutputTypeDef:
        """
        Returns a policy attached to the specified data stream or consumer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#get_resource_policy)
        """

    async def get_shard_iterator(
        self, **kwargs: Unpack[GetShardIteratorInputRequestTypeDef]
    ) -> GetShardIteratorOutputTypeDef:
        """
        Gets an Amazon Kinesis shard iterator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_shard_iterator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#get_shard_iterator)
        """

    async def increase_stream_retention_period(
        self, **kwargs: Unpack[IncreaseStreamRetentionPeriodInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Increases the Kinesis data stream's retention period, which is the length of
        time data records are accessible after they are added to the stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/increase_stream_retention_period.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#increase_stream_retention_period)
        """

    async def list_shards(
        self, **kwargs: Unpack[ListShardsInputRequestTypeDef]
    ) -> ListShardsOutputTypeDef:
        """
        Lists the shards in a stream and provides information about each shard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/list_shards.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#list_shards)
        """

    async def list_stream_consumers(
        self, **kwargs: Unpack[ListStreamConsumersInputRequestTypeDef]
    ) -> ListStreamConsumersOutputTypeDef:
        """
        Lists the consumers registered to receive data from a stream using enhanced
        fan-out, and provides information about each consumer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/list_stream_consumers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#list_stream_consumers)
        """

    async def list_streams(
        self, **kwargs: Unpack[ListStreamsInputRequestTypeDef]
    ) -> ListStreamsOutputTypeDef:
        """
        Lists your Kinesis data streams.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/list_streams.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#list_streams)
        """

    async def list_tags_for_stream(
        self, **kwargs: Unpack[ListTagsForStreamInputRequestTypeDef]
    ) -> ListTagsForStreamOutputTypeDef:
        """
        Lists the tags for the specified Kinesis data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/list_tags_for_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#list_tags_for_stream)
        """

    async def merge_shards(
        self, **kwargs: Unpack[MergeShardsInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Merges two adjacent shards in a Kinesis data stream and combines them into a
        single shard to reduce the stream's capacity to ingest and transport data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/merge_shards.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#merge_shards)
        """

    async def put_record(
        self, **kwargs: Unpack[PutRecordInputRequestTypeDef]
    ) -> PutRecordOutputTypeDef:
        """
        Writes a single data record into an Amazon Kinesis data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/put_record.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#put_record)
        """

    async def put_records(
        self, **kwargs: Unpack[PutRecordsInputRequestTypeDef]
    ) -> PutRecordsOutputTypeDef:
        """
        Writes multiple data records into a Kinesis data stream in a single call (also
        referred to as a <code>PutRecords</code> request).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/put_records.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#put_records)
        """

    async def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches a resource-based policy to a data stream or registered consumer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/put_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#put_resource_policy)
        """

    async def register_stream_consumer(
        self, **kwargs: Unpack[RegisterStreamConsumerInputRequestTypeDef]
    ) -> RegisterStreamConsumerOutputTypeDef:
        """
        Registers a consumer with a Kinesis data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/register_stream_consumer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#register_stream_consumer)
        """

    async def remove_tags_from_stream(
        self, **kwargs: Unpack[RemoveTagsFromStreamInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags from the specified Kinesis data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/remove_tags_from_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#remove_tags_from_stream)
        """

    async def split_shard(
        self, **kwargs: Unpack[SplitShardInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Splits a shard into two new shards in the Kinesis data stream, to increase the
        stream's capacity to ingest and transport data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/split_shard.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#split_shard)
        """

    async def start_stream_encryption(
        self, **kwargs: Unpack[StartStreamEncryptionInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables or updates server-side encryption using an Amazon Web Services KMS key
        for a specified stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/start_stream_encryption.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#start_stream_encryption)
        """

    async def stop_stream_encryption(
        self, **kwargs: Unpack[StopStreamEncryptionInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disables server-side encryption for a specified stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/stop_stream_encryption.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#stop_stream_encryption)
        """

    async def subscribe_to_shard(
        self, **kwargs: Unpack[SubscribeToShardInputRequestTypeDef]
    ) -> SubscribeToShardOutputTypeDef:
        """
        This operation establishes an HTTP/2 connection between the consumer you
        specify in the <code>ConsumerARN</code> parameter and the shard you specify in
        the <code>ShardId</code> parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/subscribe_to_shard.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#subscribe_to_shard)
        """

    async def update_shard_count(
        self, **kwargs: Unpack[UpdateShardCountInputRequestTypeDef]
    ) -> UpdateShardCountOutputTypeDef:
        """
        Updates the shard count of the specified stream to the specified number of
        shards.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/update_shard_count.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#update_shard_count)
        """

    async def update_stream_mode(
        self, **kwargs: Unpack[UpdateStreamModeInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the capacity mode of the data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/update_stream_mode.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#update_stream_mode)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_stream"]) -> DescribeStreamPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_shards"]) -> ListShardsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_stream_consumers"]
    ) -> ListStreamConsumersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_streams"]) -> ListStreamsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["stream_exists"]) -> StreamExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["stream_not_exists"]) -> StreamNotExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/#get_waiter)
        """

    async def __aenter__(self) -> "KinesisClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/client/)
        """
