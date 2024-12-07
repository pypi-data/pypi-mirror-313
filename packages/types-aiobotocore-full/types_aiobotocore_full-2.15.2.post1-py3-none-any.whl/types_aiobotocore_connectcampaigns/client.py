"""
Type annotations for connectcampaigns service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_connectcampaigns.client import ConnectCampaignServiceClient

    session = get_session()
    async with session.create_client("connectcampaigns") as client:
        client: ConnectCampaignServiceClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListCampaignsPaginator
from .type_defs import (
    CreateCampaignRequestRequestTypeDef,
    CreateCampaignResponseTypeDef,
    DeleteCampaignRequestRequestTypeDef,
    DeleteConnectInstanceConfigRequestRequestTypeDef,
    DeleteInstanceOnboardingJobRequestRequestTypeDef,
    DescribeCampaignRequestRequestTypeDef,
    DescribeCampaignResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCampaignStateBatchRequestRequestTypeDef,
    GetCampaignStateBatchResponseTypeDef,
    GetCampaignStateRequestRequestTypeDef,
    GetCampaignStateResponseTypeDef,
    GetConnectInstanceConfigRequestRequestTypeDef,
    GetConnectInstanceConfigResponseTypeDef,
    GetInstanceOnboardingJobStatusRequestRequestTypeDef,
    GetInstanceOnboardingJobStatusResponseTypeDef,
    ListCampaignsRequestRequestTypeDef,
    ListCampaignsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PauseCampaignRequestRequestTypeDef,
    PutDialRequestBatchRequestRequestTypeDef,
    PutDialRequestBatchResponseTypeDef,
    ResumeCampaignRequestRequestTypeDef,
    StartCampaignRequestRequestTypeDef,
    StartInstanceOnboardingJobRequestRequestTypeDef,
    StartInstanceOnboardingJobResponseTypeDef,
    StopCampaignRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateCampaignDialerConfigRequestRequestTypeDef,
    UpdateCampaignNameRequestRequestTypeDef,
    UpdateCampaignOutboundCallConfigRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ConnectCampaignServiceClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidCampaignStateException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ConnectCampaignServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ConnectCampaignServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#close)
        """

    async def create_campaign(
        self, **kwargs: Unpack[CreateCampaignRequestRequestTypeDef]
    ) -> CreateCampaignResponseTypeDef:
        """
        Creates a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/create_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#create_campaign)
        """

    async def delete_campaign(
        self, **kwargs: Unpack[DeleteCampaignRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a campaign from the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/delete_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#delete_campaign)
        """

    async def delete_connect_instance_config(
        self, **kwargs: Unpack[DeleteConnectInstanceConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a connect instance config from the specified AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/delete_connect_instance_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#delete_connect_instance_config)
        """

    async def delete_instance_onboarding_job(
        self, **kwargs: Unpack[DeleteInstanceOnboardingJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete the Connect Campaigns onboarding job for the specified Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/delete_instance_onboarding_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#delete_instance_onboarding_job)
        """

    async def describe_campaign(
        self, **kwargs: Unpack[DescribeCampaignRequestRequestTypeDef]
    ) -> DescribeCampaignResponseTypeDef:
        """
        Describes the specific campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/describe_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#describe_campaign)
        """

    async def get_campaign_state(
        self, **kwargs: Unpack[GetCampaignStateRequestRequestTypeDef]
    ) -> GetCampaignStateResponseTypeDef:
        """
        Get state of a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/get_campaign_state.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#get_campaign_state)
        """

    async def get_campaign_state_batch(
        self, **kwargs: Unpack[GetCampaignStateBatchRequestRequestTypeDef]
    ) -> GetCampaignStateBatchResponseTypeDef:
        """
        Get state of campaigns for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/get_campaign_state_batch.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#get_campaign_state_batch)
        """

    async def get_connect_instance_config(
        self, **kwargs: Unpack[GetConnectInstanceConfigRequestRequestTypeDef]
    ) -> GetConnectInstanceConfigResponseTypeDef:
        """
        Get the specific Connect instance config.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/get_connect_instance_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#get_connect_instance_config)
        """

    async def get_instance_onboarding_job_status(
        self, **kwargs: Unpack[GetInstanceOnboardingJobStatusRequestRequestTypeDef]
    ) -> GetInstanceOnboardingJobStatusResponseTypeDef:
        """
        Get the specific instance onboarding job status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/get_instance_onboarding_job_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#get_instance_onboarding_job_status)
        """

    async def list_campaigns(
        self, **kwargs: Unpack[ListCampaignsRequestRequestTypeDef]
    ) -> ListCampaignsResponseTypeDef:
        """
        Provides summary information about the campaigns under the specified Amazon
        Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/list_campaigns.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#list_campaigns)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#list_tags_for_resource)
        """

    async def pause_campaign(
        self, **kwargs: Unpack[PauseCampaignRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Pauses a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/pause_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#pause_campaign)
        """

    async def put_dial_request_batch(
        self, **kwargs: Unpack[PutDialRequestBatchRequestRequestTypeDef]
    ) -> PutDialRequestBatchResponseTypeDef:
        """
        Creates dials requests for the specified campaign Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/put_dial_request_batch.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#put_dial_request_batch)
        """

    async def resume_campaign(
        self, **kwargs: Unpack[ResumeCampaignRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/resume_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#resume_campaign)
        """

    async def start_campaign(
        self, **kwargs: Unpack[StartCampaignRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/start_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#start_campaign)
        """

    async def start_instance_onboarding_job(
        self, **kwargs: Unpack[StartInstanceOnboardingJobRequestRequestTypeDef]
    ) -> StartInstanceOnboardingJobResponseTypeDef:
        """
        Onboard the specific Amazon Connect instance to Connect Campaigns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/start_instance_onboarding_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#start_instance_onboarding_job)
        """

    async def stop_campaign(
        self, **kwargs: Unpack[StopCampaignRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a campaign for the specified Amazon Connect account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/stop_campaign.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#stop_campaign)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Tag a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Untag a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#untag_resource)
        """

    async def update_campaign_dialer_config(
        self, **kwargs: Unpack[UpdateCampaignDialerConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the dialer config of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/update_campaign_dialer_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#update_campaign_dialer_config)
        """

    async def update_campaign_name(
        self, **kwargs: Unpack[UpdateCampaignNameRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the name of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/update_campaign_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#update_campaign_name)
        """

    async def update_campaign_outbound_call_config(
        self, **kwargs: Unpack[UpdateCampaignOutboundCallConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the outbound call config of a campaign.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/update_campaign_outbound_call_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#update_campaign_outbound_call_config)
        """

    def get_paginator(self, operation_name: Literal["list_campaigns"]) -> ListCampaignsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/#get_paginator)
        """

    async def __aenter__(self) -> "ConnectCampaignServiceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaigns.html#ConnectCampaignService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaigns/client/)
        """
