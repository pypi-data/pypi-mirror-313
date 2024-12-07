"""
Type annotations for logs service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_logs.client import CloudWatchLogsClient

    session = get_session()
    async with session.create_client("logs") as client:
        client: CloudWatchLogsClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    DescribeConfigurationTemplatesPaginator,
    DescribeDeliveriesPaginator,
    DescribeDeliveryDestinationsPaginator,
    DescribeDeliverySourcesPaginator,
    DescribeDestinationsPaginator,
    DescribeExportTasksPaginator,
    DescribeLogGroupsPaginator,
    DescribeLogStreamsPaginator,
    DescribeMetricFiltersPaginator,
    DescribeQueriesPaginator,
    DescribeResourcePoliciesPaginator,
    DescribeSubscriptionFiltersPaginator,
    FilterLogEventsPaginator,
    ListAnomaliesPaginator,
    ListLogAnomalyDetectorsPaginator,
)
from .type_defs import (
    AssociateKmsKeyRequestRequestTypeDef,
    CancelExportTaskRequestRequestTypeDef,
    CreateDeliveryRequestRequestTypeDef,
    CreateDeliveryResponseTypeDef,
    CreateExportTaskRequestRequestTypeDef,
    CreateExportTaskResponseTypeDef,
    CreateLogAnomalyDetectorRequestRequestTypeDef,
    CreateLogAnomalyDetectorResponseTypeDef,
    CreateLogGroupRequestRequestTypeDef,
    CreateLogStreamRequestRequestTypeDef,
    DeleteAccountPolicyRequestRequestTypeDef,
    DeleteDataProtectionPolicyRequestRequestTypeDef,
    DeleteDeliveryDestinationPolicyRequestRequestTypeDef,
    DeleteDeliveryDestinationRequestRequestTypeDef,
    DeleteDeliveryRequestRequestTypeDef,
    DeleteDeliverySourceRequestRequestTypeDef,
    DeleteDestinationRequestRequestTypeDef,
    DeleteLogAnomalyDetectorRequestRequestTypeDef,
    DeleteLogGroupRequestRequestTypeDef,
    DeleteLogStreamRequestRequestTypeDef,
    DeleteMetricFilterRequestRequestTypeDef,
    DeleteQueryDefinitionRequestRequestTypeDef,
    DeleteQueryDefinitionResponseTypeDef,
    DeleteResourcePolicyRequestRequestTypeDef,
    DeleteRetentionPolicyRequestRequestTypeDef,
    DeleteSubscriptionFilterRequestRequestTypeDef,
    DescribeAccountPoliciesRequestRequestTypeDef,
    DescribeAccountPoliciesResponseTypeDef,
    DescribeConfigurationTemplatesRequestRequestTypeDef,
    DescribeConfigurationTemplatesResponseTypeDef,
    DescribeDeliveriesRequestRequestTypeDef,
    DescribeDeliveriesResponseTypeDef,
    DescribeDeliveryDestinationsRequestRequestTypeDef,
    DescribeDeliveryDestinationsResponseTypeDef,
    DescribeDeliverySourcesRequestRequestTypeDef,
    DescribeDeliverySourcesResponseTypeDef,
    DescribeDestinationsRequestRequestTypeDef,
    DescribeDestinationsResponseTypeDef,
    DescribeExportTasksRequestRequestTypeDef,
    DescribeExportTasksResponseTypeDef,
    DescribeLogGroupsRequestRequestTypeDef,
    DescribeLogGroupsResponseTypeDef,
    DescribeLogStreamsRequestRequestTypeDef,
    DescribeLogStreamsResponseTypeDef,
    DescribeMetricFiltersRequestRequestTypeDef,
    DescribeMetricFiltersResponseTypeDef,
    DescribeQueriesRequestRequestTypeDef,
    DescribeQueriesResponseTypeDef,
    DescribeQueryDefinitionsRequestRequestTypeDef,
    DescribeQueryDefinitionsResponseTypeDef,
    DescribeResourcePoliciesRequestRequestTypeDef,
    DescribeResourcePoliciesResponseTypeDef,
    DescribeSubscriptionFiltersRequestRequestTypeDef,
    DescribeSubscriptionFiltersResponseTypeDef,
    DisassociateKmsKeyRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    FilterLogEventsRequestRequestTypeDef,
    FilterLogEventsResponseTypeDef,
    GetDataProtectionPolicyRequestRequestTypeDef,
    GetDataProtectionPolicyResponseTypeDef,
    GetDeliveryDestinationPolicyRequestRequestTypeDef,
    GetDeliveryDestinationPolicyResponseTypeDef,
    GetDeliveryDestinationRequestRequestTypeDef,
    GetDeliveryDestinationResponseTypeDef,
    GetDeliveryRequestRequestTypeDef,
    GetDeliveryResponseTypeDef,
    GetDeliverySourceRequestRequestTypeDef,
    GetDeliverySourceResponseTypeDef,
    GetLogAnomalyDetectorRequestRequestTypeDef,
    GetLogAnomalyDetectorResponseTypeDef,
    GetLogEventsRequestRequestTypeDef,
    GetLogEventsResponseTypeDef,
    GetLogGroupFieldsRequestRequestTypeDef,
    GetLogGroupFieldsResponseTypeDef,
    GetLogRecordRequestRequestTypeDef,
    GetLogRecordResponseTypeDef,
    GetQueryResultsRequestRequestTypeDef,
    GetQueryResultsResponseTypeDef,
    ListAnomaliesRequestRequestTypeDef,
    ListAnomaliesResponseTypeDef,
    ListLogAnomalyDetectorsRequestRequestTypeDef,
    ListLogAnomalyDetectorsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTagsLogGroupRequestRequestTypeDef,
    ListTagsLogGroupResponseTypeDef,
    PutAccountPolicyRequestRequestTypeDef,
    PutAccountPolicyResponseTypeDef,
    PutDataProtectionPolicyRequestRequestTypeDef,
    PutDataProtectionPolicyResponseTypeDef,
    PutDeliveryDestinationPolicyRequestRequestTypeDef,
    PutDeliveryDestinationPolicyResponseTypeDef,
    PutDeliveryDestinationRequestRequestTypeDef,
    PutDeliveryDestinationResponseTypeDef,
    PutDeliverySourceRequestRequestTypeDef,
    PutDeliverySourceResponseTypeDef,
    PutDestinationPolicyRequestRequestTypeDef,
    PutDestinationRequestRequestTypeDef,
    PutDestinationResponseTypeDef,
    PutLogEventsRequestRequestTypeDef,
    PutLogEventsResponseTypeDef,
    PutMetricFilterRequestRequestTypeDef,
    PutQueryDefinitionRequestRequestTypeDef,
    PutQueryDefinitionResponseTypeDef,
    PutResourcePolicyRequestRequestTypeDef,
    PutResourcePolicyResponseTypeDef,
    PutRetentionPolicyRequestRequestTypeDef,
    PutSubscriptionFilterRequestRequestTypeDef,
    StartLiveTailRequestRequestTypeDef,
    StartLiveTailResponseTypeDef,
    StartQueryRequestRequestTypeDef,
    StartQueryResponseTypeDef,
    StopQueryRequestRequestTypeDef,
    StopQueryResponseTypeDef,
    TagLogGroupRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    TestMetricFilterRequestRequestTypeDef,
    TestMetricFilterResponseTypeDef,
    UntagLogGroupRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAnomalyRequestRequestTypeDef,
    UpdateDeliveryConfigurationRequestRequestTypeDef,
    UpdateLogAnomalyDetectorRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("CloudWatchLogsClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DataAlreadyAcceptedException: Type[BotocoreClientError]
    InvalidOperationException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidSequenceTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MalformedQueryException: Type[BotocoreClientError]
    OperationAbortedException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    SessionStreamingException: Type[BotocoreClientError]
    SessionTimeoutException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnrecognizedClientException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CloudWatchLogsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchLogsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#close)
        """

    async def associate_kms_key(
        self, **kwargs: Unpack[AssociateKmsKeyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates the specified KMS key with either one log group in the account, or
        with all stored CloudWatch Logs query insights results in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/associate_kms_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#associate_kms_key)
        """

    async def cancel_export_task(
        self, **kwargs: Unpack[CancelExportTaskRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels the specified export task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/cancel_export_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#cancel_export_task)
        """

    async def create_delivery(
        self, **kwargs: Unpack[CreateDeliveryRequestRequestTypeDef]
    ) -> CreateDeliveryResponseTypeDef:
        """
        Creates a <i>delivery</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/create_delivery.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#create_delivery)
        """

    async def create_export_task(
        self, **kwargs: Unpack[CreateExportTaskRequestRequestTypeDef]
    ) -> CreateExportTaskResponseTypeDef:
        """
        Creates an export task so that you can efficiently export data from a log group
        to an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/create_export_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#create_export_task)
        """

    async def create_log_anomaly_detector(
        self, **kwargs: Unpack[CreateLogAnomalyDetectorRequestRequestTypeDef]
    ) -> CreateLogAnomalyDetectorResponseTypeDef:
        """
        Creates an <i>anomaly detector</i> that regularly scans one or more log groups
        and look for patterns and anomalies in the logs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/create_log_anomaly_detector.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#create_log_anomaly_detector)
        """

    async def create_log_group(
        self, **kwargs: Unpack[CreateLogGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a log group with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/create_log_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#create_log_group)
        """

    async def create_log_stream(
        self, **kwargs: Unpack[CreateLogStreamRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a log stream for the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/create_log_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#create_log_stream)
        """

    async def delete_account_policy(
        self, **kwargs: Unpack[DeleteAccountPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a CloudWatch Logs account policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_account_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_account_policy)
        """

    async def delete_data_protection_policy(
        self, **kwargs: Unpack[DeleteDataProtectionPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the data protection policy from the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_data_protection_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_data_protection_policy)
        """

    async def delete_delivery(
        self, **kwargs: Unpack[DeleteDeliveryRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes s <i>delivery</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_delivery.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_delivery)
        """

    async def delete_delivery_destination(
        self, **kwargs: Unpack[DeleteDeliveryDestinationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a <i>delivery destination</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_delivery_destination.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_delivery_destination)
        """

    async def delete_delivery_destination_policy(
        self, **kwargs: Unpack[DeleteDeliveryDestinationPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a delivery destination policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_delivery_destination_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_delivery_destination_policy)
        """

    async def delete_delivery_source(
        self, **kwargs: Unpack[DeleteDeliverySourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a <i>delivery source</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_delivery_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_delivery_source)
        """

    async def delete_destination(
        self, **kwargs: Unpack[DeleteDestinationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified destination, and eventually disables all the subscription
        filters that publish to it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_destination.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_destination)
        """

    async def delete_log_anomaly_detector(
        self, **kwargs: Unpack[DeleteLogAnomalyDetectorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified CloudWatch Logs anomaly detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_log_anomaly_detector.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_log_anomaly_detector)
        """

    async def delete_log_group(
        self, **kwargs: Unpack[DeleteLogGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified log group and permanently deletes all the archived log
        events associated with the log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_log_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_log_group)
        """

    async def delete_log_stream(
        self, **kwargs: Unpack[DeleteLogStreamRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified log stream and permanently deletes all the archived log
        events associated with the log stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_log_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_log_stream)
        """

    async def delete_metric_filter(
        self, **kwargs: Unpack[DeleteMetricFilterRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified metric filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_metric_filter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_metric_filter)
        """

    async def delete_query_definition(
        self, **kwargs: Unpack[DeleteQueryDefinitionRequestRequestTypeDef]
    ) -> DeleteQueryDefinitionResponseTypeDef:
        """
        Deletes a saved CloudWatch Logs Insights query definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_query_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_query_definition)
        """

    async def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a resource policy from this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_resource_policy)
        """

    async def delete_retention_policy(
        self, **kwargs: Unpack[DeleteRetentionPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified retention policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_retention_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_retention_policy)
        """

    async def delete_subscription_filter(
        self, **kwargs: Unpack[DeleteSubscriptionFilterRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified subscription filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_subscription_filter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_subscription_filter)
        """

    async def describe_account_policies(
        self, **kwargs: Unpack[DescribeAccountPoliciesRequestRequestTypeDef]
    ) -> DescribeAccountPoliciesResponseTypeDef:
        """
        Returns a list of all CloudWatch Logs account policies in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_account_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_account_policies)
        """

    async def describe_configuration_templates(
        self, **kwargs: Unpack[DescribeConfigurationTemplatesRequestRequestTypeDef]
    ) -> DescribeConfigurationTemplatesResponseTypeDef:
        """
        Use this operation to return the valid and default values that are used when
        creating delivery sources, delivery destinations, and deliveries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_configuration_templates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_configuration_templates)
        """

    async def describe_deliveries(
        self, **kwargs: Unpack[DescribeDeliveriesRequestRequestTypeDef]
    ) -> DescribeDeliveriesResponseTypeDef:
        """
        Retrieves a list of the deliveries that have been created in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_deliveries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_deliveries)
        """

    async def describe_delivery_destinations(
        self, **kwargs: Unpack[DescribeDeliveryDestinationsRequestRequestTypeDef]
    ) -> DescribeDeliveryDestinationsResponseTypeDef:
        """
        Retrieves a list of the delivery destinations that have been created in the
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_delivery_destinations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_delivery_destinations)
        """

    async def describe_delivery_sources(
        self, **kwargs: Unpack[DescribeDeliverySourcesRequestRequestTypeDef]
    ) -> DescribeDeliverySourcesResponseTypeDef:
        """
        Retrieves a list of the delivery sources that have been created in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_delivery_sources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_delivery_sources)
        """

    async def describe_destinations(
        self, **kwargs: Unpack[DescribeDestinationsRequestRequestTypeDef]
    ) -> DescribeDestinationsResponseTypeDef:
        """
        Lists all your destinations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_destinations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_destinations)
        """

    async def describe_export_tasks(
        self, **kwargs: Unpack[DescribeExportTasksRequestRequestTypeDef]
    ) -> DescribeExportTasksResponseTypeDef:
        """
        Lists the specified export tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_export_tasks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_export_tasks)
        """

    async def describe_log_groups(
        self, **kwargs: Unpack[DescribeLogGroupsRequestRequestTypeDef]
    ) -> DescribeLogGroupsResponseTypeDef:
        """
        Lists the specified log groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_log_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_log_groups)
        """

    async def describe_log_streams(
        self, **kwargs: Unpack[DescribeLogStreamsRequestRequestTypeDef]
    ) -> DescribeLogStreamsResponseTypeDef:
        """
        Lists the log streams for the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_log_streams.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_log_streams)
        """

    async def describe_metric_filters(
        self, **kwargs: Unpack[DescribeMetricFiltersRequestRequestTypeDef]
    ) -> DescribeMetricFiltersResponseTypeDef:
        """
        Lists the specified metric filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_metric_filters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_metric_filters)
        """

    async def describe_queries(
        self, **kwargs: Unpack[DescribeQueriesRequestRequestTypeDef]
    ) -> DescribeQueriesResponseTypeDef:
        """
        Returns a list of CloudWatch Logs Insights queries that are scheduled, running,
        or have been run recently in this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_queries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_queries)
        """

    async def describe_query_definitions(
        self, **kwargs: Unpack[DescribeQueryDefinitionsRequestRequestTypeDef]
    ) -> DescribeQueryDefinitionsResponseTypeDef:
        """
        This operation returns a paginated list of your saved CloudWatch Logs Insights
        query definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_query_definitions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_query_definitions)
        """

    async def describe_resource_policies(
        self, **kwargs: Unpack[DescribeResourcePoliciesRequestRequestTypeDef]
    ) -> DescribeResourcePoliciesResponseTypeDef:
        """
        Lists the resource policies in this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_resource_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_resource_policies)
        """

    async def describe_subscription_filters(
        self, **kwargs: Unpack[DescribeSubscriptionFiltersRequestRequestTypeDef]
    ) -> DescribeSubscriptionFiltersResponseTypeDef:
        """
        Lists the subscription filters for the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_subscription_filters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_subscription_filters)
        """

    async def disassociate_kms_key(
        self, **kwargs: Unpack[DisassociateKmsKeyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates the specified KMS key from the specified log group or from all
        CloudWatch Logs Insights query results in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/disassociate_kms_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#disassociate_kms_key)
        """

    async def filter_log_events(
        self, **kwargs: Unpack[FilterLogEventsRequestRequestTypeDef]
    ) -> FilterLogEventsResponseTypeDef:
        """
        Lists log events from the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/filter_log_events.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#filter_log_events)
        """

    async def get_data_protection_policy(
        self, **kwargs: Unpack[GetDataProtectionPolicyRequestRequestTypeDef]
    ) -> GetDataProtectionPolicyResponseTypeDef:
        """
        Returns information about a log group data protection policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_data_protection_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_data_protection_policy)
        """

    async def get_delivery(
        self, **kwargs: Unpack[GetDeliveryRequestRequestTypeDef]
    ) -> GetDeliveryResponseTypeDef:
        """
        Returns complete information about one logical <i>delivery</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_delivery.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_delivery)
        """

    async def get_delivery_destination(
        self, **kwargs: Unpack[GetDeliveryDestinationRequestRequestTypeDef]
    ) -> GetDeliveryDestinationResponseTypeDef:
        """
        Retrieves complete information about one delivery destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_delivery_destination.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_delivery_destination)
        """

    async def get_delivery_destination_policy(
        self, **kwargs: Unpack[GetDeliveryDestinationPolicyRequestRequestTypeDef]
    ) -> GetDeliveryDestinationPolicyResponseTypeDef:
        """
        Retrieves the delivery destination policy assigned to the delivery destination
        that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_delivery_destination_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_delivery_destination_policy)
        """

    async def get_delivery_source(
        self, **kwargs: Unpack[GetDeliverySourceRequestRequestTypeDef]
    ) -> GetDeliverySourceResponseTypeDef:
        """
        Retrieves complete information about one delivery source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_delivery_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_delivery_source)
        """

    async def get_log_anomaly_detector(
        self, **kwargs: Unpack[GetLogAnomalyDetectorRequestRequestTypeDef]
    ) -> GetLogAnomalyDetectorResponseTypeDef:
        """
        Retrieves information about the log anomaly detector that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_log_anomaly_detector.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_log_anomaly_detector)
        """

    async def get_log_events(
        self, **kwargs: Unpack[GetLogEventsRequestRequestTypeDef]
    ) -> GetLogEventsResponseTypeDef:
        """
        Lists log events from the specified log stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_log_events.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_log_events)
        """

    async def get_log_group_fields(
        self, **kwargs: Unpack[GetLogGroupFieldsRequestRequestTypeDef]
    ) -> GetLogGroupFieldsResponseTypeDef:
        """
        Returns a list of the fields that are included in log events in the specified
        log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_log_group_fields.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_log_group_fields)
        """

    async def get_log_record(
        self, **kwargs: Unpack[GetLogRecordRequestRequestTypeDef]
    ) -> GetLogRecordResponseTypeDef:
        """
        Retrieves all of the fields and values of a single log event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_log_record.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_log_record)
        """

    async def get_query_results(
        self, **kwargs: Unpack[GetQueryResultsRequestRequestTypeDef]
    ) -> GetQueryResultsResponseTypeDef:
        """
        Returns the results from the specified query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_query_results.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_query_results)
        """

    async def list_anomalies(
        self, **kwargs: Unpack[ListAnomaliesRequestRequestTypeDef]
    ) -> ListAnomaliesResponseTypeDef:
        """
        Returns a list of anomalies that log anomaly detectors have found.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/list_anomalies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#list_anomalies)
        """

    async def list_log_anomaly_detectors(
        self, **kwargs: Unpack[ListLogAnomalyDetectorsRequestRequestTypeDef]
    ) -> ListLogAnomalyDetectorsResponseTypeDef:
        """
        Retrieves a list of the log anomaly detectors in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/list_log_anomaly_detectors.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#list_log_anomaly_detectors)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Displays the tags associated with a CloudWatch Logs resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#list_tags_for_resource)
        """

    async def list_tags_log_group(
        self, **kwargs: Unpack[ListTagsLogGroupRequestRequestTypeDef]
    ) -> ListTagsLogGroupResponseTypeDef:
        """
        The ListTagsLogGroup operation is on the path to deprecation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/list_tags_log_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#list_tags_log_group)
        """

    async def put_account_policy(
        self, **kwargs: Unpack[PutAccountPolicyRequestRequestTypeDef]
    ) -> PutAccountPolicyResponseTypeDef:
        """
        Creates an account-level data protection policy or subscription filter policy
        that applies to all log groups or a subset of log groups in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_account_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_account_policy)
        """

    async def put_data_protection_policy(
        self, **kwargs: Unpack[PutDataProtectionPolicyRequestRequestTypeDef]
    ) -> PutDataProtectionPolicyResponseTypeDef:
        """
        Creates a data protection policy for the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_data_protection_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_data_protection_policy)
        """

    async def put_delivery_destination(
        self, **kwargs: Unpack[PutDeliveryDestinationRequestRequestTypeDef]
    ) -> PutDeliveryDestinationResponseTypeDef:
        """
        Creates or updates a logical <i>delivery destination</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_delivery_destination.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_delivery_destination)
        """

    async def put_delivery_destination_policy(
        self, **kwargs: Unpack[PutDeliveryDestinationPolicyRequestRequestTypeDef]
    ) -> PutDeliveryDestinationPolicyResponseTypeDef:
        """
        Creates and assigns an IAM policy that grants permissions to CloudWatch Logs to
        deliver logs cross-account to a specified destination in this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_delivery_destination_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_delivery_destination_policy)
        """

    async def put_delivery_source(
        self, **kwargs: Unpack[PutDeliverySourceRequestRequestTypeDef]
    ) -> PutDeliverySourceResponseTypeDef:
        """
        Creates or updates a logical <i>delivery source</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_delivery_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_delivery_source)
        """

    async def put_destination(
        self, **kwargs: Unpack[PutDestinationRequestRequestTypeDef]
    ) -> PutDestinationResponseTypeDef:
        """
        Creates or updates a destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_destination.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_destination)
        """

    async def put_destination_policy(
        self, **kwargs: Unpack[PutDestinationPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates an access policy associated with an existing destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_destination_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_destination_policy)
        """

    async def put_log_events(
        self, **kwargs: Unpack[PutLogEventsRequestRequestTypeDef]
    ) -> PutLogEventsResponseTypeDef:
        """
        Uploads a batch of log events to the specified log stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_log_events.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_log_events)
        """

    async def put_metric_filter(
        self, **kwargs: Unpack[PutMetricFilterRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates a metric filter and associates it with the specified log
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_metric_filter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_metric_filter)
        """

    async def put_query_definition(
        self, **kwargs: Unpack[PutQueryDefinitionRequestRequestTypeDef]
    ) -> PutQueryDefinitionResponseTypeDef:
        """
        Creates or updates a query definition for CloudWatch Logs Insights.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_query_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_query_definition)
        """

    async def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestRequestTypeDef]
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Creates or updates a resource policy allowing other Amazon Web Services
        services to put log events to this account, such as Amazon Route 53.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_resource_policy)
        """

    async def put_retention_policy(
        self, **kwargs: Unpack[PutRetentionPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the retention of the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_retention_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_retention_policy)
        """

    async def put_subscription_filter(
        self, **kwargs: Unpack[PutSubscriptionFilterRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates a subscription filter and associates it with the specified
        log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_subscription_filter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_subscription_filter)
        """

    async def start_live_tail(
        self, **kwargs: Unpack[StartLiveTailRequestRequestTypeDef]
    ) -> StartLiveTailResponseTypeDef:
        """
        Starts a Live Tail streaming session for one or more log groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/start_live_tail.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#start_live_tail)
        """

    async def start_query(
        self, **kwargs: Unpack[StartQueryRequestRequestTypeDef]
    ) -> StartQueryResponseTypeDef:
        """
        Schedules a query of a log group using CloudWatch Logs Insights.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/start_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#start_query)
        """

    async def stop_query(
        self, **kwargs: Unpack[StopQueryRequestRequestTypeDef]
    ) -> StopQueryResponseTypeDef:
        """
        Stops a CloudWatch Logs Insights query that is in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/stop_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#stop_query)
        """

    async def tag_log_group(
        self, **kwargs: Unpack[TagLogGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        The TagLogGroup operation is on the path to deprecation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/tag_log_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#tag_log_group)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assigns one or more tags (key-value pairs) to the specified CloudWatch Logs
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#tag_resource)
        """

    async def test_metric_filter(
        self, **kwargs: Unpack[TestMetricFilterRequestRequestTypeDef]
    ) -> TestMetricFilterResponseTypeDef:
        """
        Tests the filter pattern of a metric filter against a sample of log event
        messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/test_metric_filter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#test_metric_filter)
        """

    async def untag_log_group(
        self, **kwargs: Unpack[UntagLogGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        The UntagLogGroup operation is on the path to deprecation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/untag_log_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#untag_log_group)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#untag_resource)
        """

    async def update_anomaly(
        self, **kwargs: Unpack[UpdateAnomalyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Use this operation to <i>suppress</i> anomaly detection for a specified anomaly
        or pattern.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/update_anomaly.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#update_anomaly)
        """

    async def update_delivery_configuration(
        self, **kwargs: Unpack[UpdateDeliveryConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Use this operation to update the configuration of a <a
        href="https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_Delivery.html">delivery</a>
        to change either the S3 path pattern or the format of the delivered logs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/update_delivery_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#update_delivery_configuration)
        """

    async def update_log_anomaly_detector(
        self, **kwargs: Unpack[UpdateLogAnomalyDetectorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an existing log anomaly detector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/update_log_anomaly_detector.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#update_log_anomaly_detector)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_configuration_templates"]
    ) -> DescribeConfigurationTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_deliveries"]
    ) -> DescribeDeliveriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_delivery_destinations"]
    ) -> DescribeDeliveryDestinationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_delivery_sources"]
    ) -> DescribeDeliverySourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_destinations"]
    ) -> DescribeDestinationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_export_tasks"]
    ) -> DescribeExportTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_log_groups"]
    ) -> DescribeLogGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_log_streams"]
    ) -> DescribeLogStreamsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_metric_filters"]
    ) -> DescribeMetricFiltersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_queries"]
    ) -> DescribeQueriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_resource_policies"]
    ) -> DescribeResourcePoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_subscription_filters"]
    ) -> DescribeSubscriptionFiltersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["filter_log_events"]
    ) -> FilterLogEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_anomalies"]) -> ListAnomaliesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_log_anomaly_detectors"]
    ) -> ListLogAnomalyDetectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    async def __aenter__(self) -> "CloudWatchLogsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/)
        """
