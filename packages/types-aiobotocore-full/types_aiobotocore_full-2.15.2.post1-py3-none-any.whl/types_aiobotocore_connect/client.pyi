"""
Type annotations for connect service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_connect.client import ConnectClient

    session = get_session()
    async with session.create_client("connect") as client:
        client: ConnectClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    GetMetricDataPaginator,
    ListAgentStatusesPaginator,
    ListApprovedOriginsPaginator,
    ListAuthenticationProfilesPaginator,
    ListBotsPaginator,
    ListContactEvaluationsPaginator,
    ListContactFlowModulesPaginator,
    ListContactFlowsPaginator,
    ListContactReferencesPaginator,
    ListDefaultVocabulariesPaginator,
    ListEvaluationFormsPaginator,
    ListEvaluationFormVersionsPaginator,
    ListFlowAssociationsPaginator,
    ListHoursOfOperationsPaginator,
    ListInstanceAttributesPaginator,
    ListInstancesPaginator,
    ListInstanceStorageConfigsPaginator,
    ListIntegrationAssociationsPaginator,
    ListLambdaFunctionsPaginator,
    ListLexBotsPaginator,
    ListPhoneNumbersPaginator,
    ListPhoneNumbersV2Paginator,
    ListPredefinedAttributesPaginator,
    ListPromptsPaginator,
    ListQueueQuickConnectsPaginator,
    ListQueuesPaginator,
    ListQuickConnectsPaginator,
    ListRoutingProfileQueuesPaginator,
    ListRoutingProfilesPaginator,
    ListRulesPaginator,
    ListSecurityKeysPaginator,
    ListSecurityProfileApplicationsPaginator,
    ListSecurityProfilePermissionsPaginator,
    ListSecurityProfilesPaginator,
    ListTaskTemplatesPaginator,
    ListTrafficDistributionGroupsPaginator,
    ListTrafficDistributionGroupUsersPaginator,
    ListUseCasesPaginator,
    ListUserHierarchyGroupsPaginator,
    ListUserProficienciesPaginator,
    ListUsersPaginator,
    ListViewsPaginator,
    ListViewVersionsPaginator,
    SearchAgentStatusesPaginator,
    SearchAvailablePhoneNumbersPaginator,
    SearchContactFlowModulesPaginator,
    SearchContactFlowsPaginator,
    SearchContactsPaginator,
    SearchHoursOfOperationsPaginator,
    SearchPredefinedAttributesPaginator,
    SearchPromptsPaginator,
    SearchQueuesPaginator,
    SearchQuickConnectsPaginator,
    SearchResourceTagsPaginator,
    SearchRoutingProfilesPaginator,
    SearchSecurityProfilesPaginator,
    SearchUserHierarchyGroupsPaginator,
    SearchUsersPaginator,
    SearchVocabulariesPaginator,
)
from .type_defs import (
    ActivateEvaluationFormRequestRequestTypeDef,
    ActivateEvaluationFormResponseTypeDef,
    AssociateAnalyticsDataSetRequestRequestTypeDef,
    AssociateAnalyticsDataSetResponseTypeDef,
    AssociateApprovedOriginRequestRequestTypeDef,
    AssociateBotRequestRequestTypeDef,
    AssociateDefaultVocabularyRequestRequestTypeDef,
    AssociateFlowRequestRequestTypeDef,
    AssociateInstanceStorageConfigRequestRequestTypeDef,
    AssociateInstanceStorageConfigResponseTypeDef,
    AssociateLambdaFunctionRequestRequestTypeDef,
    AssociateLexBotRequestRequestTypeDef,
    AssociatePhoneNumberContactFlowRequestRequestTypeDef,
    AssociateQueueQuickConnectsRequestRequestTypeDef,
    AssociateRoutingProfileQueuesRequestRequestTypeDef,
    AssociateSecurityKeyRequestRequestTypeDef,
    AssociateSecurityKeyResponseTypeDef,
    AssociateTrafficDistributionGroupUserRequestRequestTypeDef,
    AssociateUserProficienciesRequestRequestTypeDef,
    BatchAssociateAnalyticsDataSetRequestRequestTypeDef,
    BatchAssociateAnalyticsDataSetResponseTypeDef,
    BatchDisassociateAnalyticsDataSetRequestRequestTypeDef,
    BatchDisassociateAnalyticsDataSetResponseTypeDef,
    BatchGetAttachedFileMetadataRequestRequestTypeDef,
    BatchGetAttachedFileMetadataResponseTypeDef,
    BatchGetFlowAssociationRequestRequestTypeDef,
    BatchGetFlowAssociationResponseTypeDef,
    BatchPutContactRequestRequestTypeDef,
    BatchPutContactResponseTypeDef,
    ClaimPhoneNumberRequestRequestTypeDef,
    ClaimPhoneNumberResponseTypeDef,
    CompleteAttachedFileUploadRequestRequestTypeDef,
    CreateAgentStatusRequestRequestTypeDef,
    CreateAgentStatusResponseTypeDef,
    CreateContactFlowModuleRequestRequestTypeDef,
    CreateContactFlowModuleResponseTypeDef,
    CreateContactFlowRequestRequestTypeDef,
    CreateContactFlowResponseTypeDef,
    CreateEvaluationFormRequestRequestTypeDef,
    CreateEvaluationFormResponseTypeDef,
    CreateHoursOfOperationRequestRequestTypeDef,
    CreateHoursOfOperationResponseTypeDef,
    CreateInstanceRequestRequestTypeDef,
    CreateInstanceResponseTypeDef,
    CreateIntegrationAssociationRequestRequestTypeDef,
    CreateIntegrationAssociationResponseTypeDef,
    CreateParticipantRequestRequestTypeDef,
    CreateParticipantResponseTypeDef,
    CreatePersistentContactAssociationRequestRequestTypeDef,
    CreatePersistentContactAssociationResponseTypeDef,
    CreatePredefinedAttributeRequestRequestTypeDef,
    CreatePromptRequestRequestTypeDef,
    CreatePromptResponseTypeDef,
    CreateQueueRequestRequestTypeDef,
    CreateQueueResponseTypeDef,
    CreateQuickConnectRequestRequestTypeDef,
    CreateQuickConnectResponseTypeDef,
    CreateRoutingProfileRequestRequestTypeDef,
    CreateRoutingProfileResponseTypeDef,
    CreateRuleRequestRequestTypeDef,
    CreateRuleResponseTypeDef,
    CreateSecurityProfileRequestRequestTypeDef,
    CreateSecurityProfileResponseTypeDef,
    CreateTaskTemplateRequestRequestTypeDef,
    CreateTaskTemplateResponseTypeDef,
    CreateTrafficDistributionGroupRequestRequestTypeDef,
    CreateTrafficDistributionGroupResponseTypeDef,
    CreateUseCaseRequestRequestTypeDef,
    CreateUseCaseResponseTypeDef,
    CreateUserHierarchyGroupRequestRequestTypeDef,
    CreateUserHierarchyGroupResponseTypeDef,
    CreateUserRequestRequestTypeDef,
    CreateUserResponseTypeDef,
    CreateViewRequestRequestTypeDef,
    CreateViewResponseTypeDef,
    CreateViewVersionRequestRequestTypeDef,
    CreateViewVersionResponseTypeDef,
    CreateVocabularyRequestRequestTypeDef,
    CreateVocabularyResponseTypeDef,
    DeactivateEvaluationFormRequestRequestTypeDef,
    DeactivateEvaluationFormResponseTypeDef,
    DeleteAttachedFileRequestRequestTypeDef,
    DeleteContactEvaluationRequestRequestTypeDef,
    DeleteContactFlowModuleRequestRequestTypeDef,
    DeleteContactFlowRequestRequestTypeDef,
    DeleteEvaluationFormRequestRequestTypeDef,
    DeleteHoursOfOperationRequestRequestTypeDef,
    DeleteInstanceRequestRequestTypeDef,
    DeleteIntegrationAssociationRequestRequestTypeDef,
    DeletePredefinedAttributeRequestRequestTypeDef,
    DeletePromptRequestRequestTypeDef,
    DeleteQueueRequestRequestTypeDef,
    DeleteQuickConnectRequestRequestTypeDef,
    DeleteRoutingProfileRequestRequestTypeDef,
    DeleteRuleRequestRequestTypeDef,
    DeleteSecurityProfileRequestRequestTypeDef,
    DeleteTaskTemplateRequestRequestTypeDef,
    DeleteTrafficDistributionGroupRequestRequestTypeDef,
    DeleteUseCaseRequestRequestTypeDef,
    DeleteUserHierarchyGroupRequestRequestTypeDef,
    DeleteUserRequestRequestTypeDef,
    DeleteViewRequestRequestTypeDef,
    DeleteViewVersionRequestRequestTypeDef,
    DeleteVocabularyRequestRequestTypeDef,
    DeleteVocabularyResponseTypeDef,
    DescribeAgentStatusRequestRequestTypeDef,
    DescribeAgentStatusResponseTypeDef,
    DescribeAuthenticationProfileRequestRequestTypeDef,
    DescribeAuthenticationProfileResponseTypeDef,
    DescribeContactEvaluationRequestRequestTypeDef,
    DescribeContactEvaluationResponseTypeDef,
    DescribeContactFlowModuleRequestRequestTypeDef,
    DescribeContactFlowModuleResponseTypeDef,
    DescribeContactFlowRequestRequestTypeDef,
    DescribeContactFlowResponseTypeDef,
    DescribeContactRequestRequestTypeDef,
    DescribeContactResponseTypeDef,
    DescribeEvaluationFormRequestRequestTypeDef,
    DescribeEvaluationFormResponseTypeDef,
    DescribeHoursOfOperationRequestRequestTypeDef,
    DescribeHoursOfOperationResponseTypeDef,
    DescribeInstanceAttributeRequestRequestTypeDef,
    DescribeInstanceAttributeResponseTypeDef,
    DescribeInstanceRequestRequestTypeDef,
    DescribeInstanceResponseTypeDef,
    DescribeInstanceStorageConfigRequestRequestTypeDef,
    DescribeInstanceStorageConfigResponseTypeDef,
    DescribePhoneNumberRequestRequestTypeDef,
    DescribePhoneNumberResponseTypeDef,
    DescribePredefinedAttributeRequestRequestTypeDef,
    DescribePredefinedAttributeResponseTypeDef,
    DescribePromptRequestRequestTypeDef,
    DescribePromptResponseTypeDef,
    DescribeQueueRequestRequestTypeDef,
    DescribeQueueResponseTypeDef,
    DescribeQuickConnectRequestRequestTypeDef,
    DescribeQuickConnectResponseTypeDef,
    DescribeRoutingProfileRequestRequestTypeDef,
    DescribeRoutingProfileResponseTypeDef,
    DescribeRuleRequestRequestTypeDef,
    DescribeRuleResponseTypeDef,
    DescribeSecurityProfileRequestRequestTypeDef,
    DescribeSecurityProfileResponseTypeDef,
    DescribeTrafficDistributionGroupRequestRequestTypeDef,
    DescribeTrafficDistributionGroupResponseTypeDef,
    DescribeUserHierarchyGroupRequestRequestTypeDef,
    DescribeUserHierarchyGroupResponseTypeDef,
    DescribeUserHierarchyStructureRequestRequestTypeDef,
    DescribeUserHierarchyStructureResponseTypeDef,
    DescribeUserRequestRequestTypeDef,
    DescribeUserResponseTypeDef,
    DescribeViewRequestRequestTypeDef,
    DescribeViewResponseTypeDef,
    DescribeVocabularyRequestRequestTypeDef,
    DescribeVocabularyResponseTypeDef,
    DisassociateAnalyticsDataSetRequestRequestTypeDef,
    DisassociateApprovedOriginRequestRequestTypeDef,
    DisassociateBotRequestRequestTypeDef,
    DisassociateFlowRequestRequestTypeDef,
    DisassociateInstanceStorageConfigRequestRequestTypeDef,
    DisassociateLambdaFunctionRequestRequestTypeDef,
    DisassociateLexBotRequestRequestTypeDef,
    DisassociatePhoneNumberContactFlowRequestRequestTypeDef,
    DisassociateQueueQuickConnectsRequestRequestTypeDef,
    DisassociateRoutingProfileQueuesRequestRequestTypeDef,
    DisassociateSecurityKeyRequestRequestTypeDef,
    DisassociateTrafficDistributionGroupUserRequestRequestTypeDef,
    DisassociateUserProficienciesRequestRequestTypeDef,
    DismissUserContactRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAttachedFileRequestRequestTypeDef,
    GetAttachedFileResponseTypeDef,
    GetContactAttributesRequestRequestTypeDef,
    GetContactAttributesResponseTypeDef,
    GetCurrentMetricDataRequestRequestTypeDef,
    GetCurrentMetricDataResponseTypeDef,
    GetCurrentUserDataRequestRequestTypeDef,
    GetCurrentUserDataResponseTypeDef,
    GetFederationTokenRequestRequestTypeDef,
    GetFederationTokenResponseTypeDef,
    GetFlowAssociationRequestRequestTypeDef,
    GetFlowAssociationResponseTypeDef,
    GetMetricDataRequestRequestTypeDef,
    GetMetricDataResponseTypeDef,
    GetMetricDataV2RequestRequestTypeDef,
    GetMetricDataV2ResponseTypeDef,
    GetPromptFileRequestRequestTypeDef,
    GetPromptFileResponseTypeDef,
    GetTaskTemplateRequestRequestTypeDef,
    GetTaskTemplateResponseTypeDef,
    GetTrafficDistributionRequestRequestTypeDef,
    GetTrafficDistributionResponseTypeDef,
    ImportPhoneNumberRequestRequestTypeDef,
    ImportPhoneNumberResponseTypeDef,
    ListAgentStatusRequestRequestTypeDef,
    ListAgentStatusResponseTypeDef,
    ListAnalyticsDataAssociationsRequestRequestTypeDef,
    ListAnalyticsDataAssociationsResponseTypeDef,
    ListApprovedOriginsRequestRequestTypeDef,
    ListApprovedOriginsResponseTypeDef,
    ListAuthenticationProfilesRequestRequestTypeDef,
    ListAuthenticationProfilesResponseTypeDef,
    ListBotsRequestRequestTypeDef,
    ListBotsResponseTypeDef,
    ListContactEvaluationsRequestRequestTypeDef,
    ListContactEvaluationsResponseTypeDef,
    ListContactFlowModulesRequestRequestTypeDef,
    ListContactFlowModulesResponseTypeDef,
    ListContactFlowsRequestRequestTypeDef,
    ListContactFlowsResponseTypeDef,
    ListContactReferencesRequestRequestTypeDef,
    ListContactReferencesResponseTypeDef,
    ListDefaultVocabulariesRequestRequestTypeDef,
    ListDefaultVocabulariesResponseTypeDef,
    ListEvaluationFormsRequestRequestTypeDef,
    ListEvaluationFormsResponseTypeDef,
    ListEvaluationFormVersionsRequestRequestTypeDef,
    ListEvaluationFormVersionsResponseTypeDef,
    ListFlowAssociationsRequestRequestTypeDef,
    ListFlowAssociationsResponseTypeDef,
    ListHoursOfOperationsRequestRequestTypeDef,
    ListHoursOfOperationsResponseTypeDef,
    ListInstanceAttributesRequestRequestTypeDef,
    ListInstanceAttributesResponseTypeDef,
    ListInstancesRequestRequestTypeDef,
    ListInstancesResponseTypeDef,
    ListInstanceStorageConfigsRequestRequestTypeDef,
    ListInstanceStorageConfigsResponseTypeDef,
    ListIntegrationAssociationsRequestRequestTypeDef,
    ListIntegrationAssociationsResponseTypeDef,
    ListLambdaFunctionsRequestRequestTypeDef,
    ListLambdaFunctionsResponseTypeDef,
    ListLexBotsRequestRequestTypeDef,
    ListLexBotsResponseTypeDef,
    ListPhoneNumbersRequestRequestTypeDef,
    ListPhoneNumbersResponseTypeDef,
    ListPhoneNumbersV2RequestRequestTypeDef,
    ListPhoneNumbersV2ResponseTypeDef,
    ListPredefinedAttributesRequestRequestTypeDef,
    ListPredefinedAttributesResponseTypeDef,
    ListPromptsRequestRequestTypeDef,
    ListPromptsResponseTypeDef,
    ListQueueQuickConnectsRequestRequestTypeDef,
    ListQueueQuickConnectsResponseTypeDef,
    ListQueuesRequestRequestTypeDef,
    ListQueuesResponseTypeDef,
    ListQuickConnectsRequestRequestTypeDef,
    ListQuickConnectsResponseTypeDef,
    ListRealtimeContactAnalysisSegmentsV2RequestRequestTypeDef,
    ListRealtimeContactAnalysisSegmentsV2ResponseTypeDef,
    ListRoutingProfileQueuesRequestRequestTypeDef,
    ListRoutingProfileQueuesResponseTypeDef,
    ListRoutingProfilesRequestRequestTypeDef,
    ListRoutingProfilesResponseTypeDef,
    ListRulesRequestRequestTypeDef,
    ListRulesResponseTypeDef,
    ListSecurityKeysRequestRequestTypeDef,
    ListSecurityKeysResponseTypeDef,
    ListSecurityProfileApplicationsRequestRequestTypeDef,
    ListSecurityProfileApplicationsResponseTypeDef,
    ListSecurityProfilePermissionsRequestRequestTypeDef,
    ListSecurityProfilePermissionsResponseTypeDef,
    ListSecurityProfilesRequestRequestTypeDef,
    ListSecurityProfilesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTaskTemplatesRequestRequestTypeDef,
    ListTaskTemplatesResponseTypeDef,
    ListTrafficDistributionGroupsRequestRequestTypeDef,
    ListTrafficDistributionGroupsResponseTypeDef,
    ListTrafficDistributionGroupUsersRequestRequestTypeDef,
    ListTrafficDistributionGroupUsersResponseTypeDef,
    ListUseCasesRequestRequestTypeDef,
    ListUseCasesResponseTypeDef,
    ListUserHierarchyGroupsRequestRequestTypeDef,
    ListUserHierarchyGroupsResponseTypeDef,
    ListUserProficienciesRequestRequestTypeDef,
    ListUserProficienciesResponseTypeDef,
    ListUsersRequestRequestTypeDef,
    ListUsersResponseTypeDef,
    ListViewsRequestRequestTypeDef,
    ListViewsResponseTypeDef,
    ListViewVersionsRequestRequestTypeDef,
    ListViewVersionsResponseTypeDef,
    MonitorContactRequestRequestTypeDef,
    MonitorContactResponseTypeDef,
    PauseContactRequestRequestTypeDef,
    PutUserStatusRequestRequestTypeDef,
    ReleasePhoneNumberRequestRequestTypeDef,
    ReplicateInstanceRequestRequestTypeDef,
    ReplicateInstanceResponseTypeDef,
    ResumeContactRecordingRequestRequestTypeDef,
    ResumeContactRequestRequestTypeDef,
    SearchAgentStatusesRequestRequestTypeDef,
    SearchAgentStatusesResponseTypeDef,
    SearchAvailablePhoneNumbersRequestRequestTypeDef,
    SearchAvailablePhoneNumbersResponseTypeDef,
    SearchContactFlowModulesRequestRequestTypeDef,
    SearchContactFlowModulesResponseTypeDef,
    SearchContactFlowsRequestRequestTypeDef,
    SearchContactFlowsResponseTypeDef,
    SearchContactsRequestRequestTypeDef,
    SearchContactsResponseTypeDef,
    SearchHoursOfOperationsRequestRequestTypeDef,
    SearchHoursOfOperationsResponseTypeDef,
    SearchPredefinedAttributesRequestRequestTypeDef,
    SearchPredefinedAttributesResponseTypeDef,
    SearchPromptsRequestRequestTypeDef,
    SearchPromptsResponseTypeDef,
    SearchQueuesRequestRequestTypeDef,
    SearchQueuesResponseTypeDef,
    SearchQuickConnectsRequestRequestTypeDef,
    SearchQuickConnectsResponseTypeDef,
    SearchResourceTagsRequestRequestTypeDef,
    SearchResourceTagsResponseTypeDef,
    SearchRoutingProfilesRequestRequestTypeDef,
    SearchRoutingProfilesResponseTypeDef,
    SearchSecurityProfilesRequestRequestTypeDef,
    SearchSecurityProfilesResponseTypeDef,
    SearchUserHierarchyGroupsRequestRequestTypeDef,
    SearchUserHierarchyGroupsResponseTypeDef,
    SearchUsersRequestRequestTypeDef,
    SearchUsersResponseTypeDef,
    SearchVocabulariesRequestRequestTypeDef,
    SearchVocabulariesResponseTypeDef,
    SendChatIntegrationEventRequestRequestTypeDef,
    SendChatIntegrationEventResponseTypeDef,
    StartAttachedFileUploadRequestRequestTypeDef,
    StartAttachedFileUploadResponseTypeDef,
    StartChatContactRequestRequestTypeDef,
    StartChatContactResponseTypeDef,
    StartContactEvaluationRequestRequestTypeDef,
    StartContactEvaluationResponseTypeDef,
    StartContactRecordingRequestRequestTypeDef,
    StartContactStreamingRequestRequestTypeDef,
    StartContactStreamingResponseTypeDef,
    StartOutboundChatContactRequestRequestTypeDef,
    StartOutboundChatContactResponseTypeDef,
    StartOutboundVoiceContactRequestRequestTypeDef,
    StartOutboundVoiceContactResponseTypeDef,
    StartTaskContactRequestRequestTypeDef,
    StartTaskContactResponseTypeDef,
    StartWebRTCContactRequestRequestTypeDef,
    StartWebRTCContactResponseTypeDef,
    StopContactRecordingRequestRequestTypeDef,
    StopContactRequestRequestTypeDef,
    StopContactStreamingRequestRequestTypeDef,
    SubmitContactEvaluationRequestRequestTypeDef,
    SubmitContactEvaluationResponseTypeDef,
    SuspendContactRecordingRequestRequestTypeDef,
    TagContactRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    TransferContactRequestRequestTypeDef,
    TransferContactResponseTypeDef,
    UntagContactRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAgentStatusRequestRequestTypeDef,
    UpdateAuthenticationProfileRequestRequestTypeDef,
    UpdateContactAttributesRequestRequestTypeDef,
    UpdateContactEvaluationRequestRequestTypeDef,
    UpdateContactEvaluationResponseTypeDef,
    UpdateContactFlowContentRequestRequestTypeDef,
    UpdateContactFlowMetadataRequestRequestTypeDef,
    UpdateContactFlowModuleContentRequestRequestTypeDef,
    UpdateContactFlowModuleMetadataRequestRequestTypeDef,
    UpdateContactFlowNameRequestRequestTypeDef,
    UpdateContactRequestRequestTypeDef,
    UpdateContactRoutingDataRequestRequestTypeDef,
    UpdateContactScheduleRequestRequestTypeDef,
    UpdateEvaluationFormRequestRequestTypeDef,
    UpdateEvaluationFormResponseTypeDef,
    UpdateHoursOfOperationRequestRequestTypeDef,
    UpdateInstanceAttributeRequestRequestTypeDef,
    UpdateInstanceStorageConfigRequestRequestTypeDef,
    UpdateParticipantRoleConfigRequestRequestTypeDef,
    UpdatePhoneNumberMetadataRequestRequestTypeDef,
    UpdatePhoneNumberRequestRequestTypeDef,
    UpdatePhoneNumberResponseTypeDef,
    UpdatePredefinedAttributeRequestRequestTypeDef,
    UpdatePromptRequestRequestTypeDef,
    UpdatePromptResponseTypeDef,
    UpdateQueueHoursOfOperationRequestRequestTypeDef,
    UpdateQueueMaxContactsRequestRequestTypeDef,
    UpdateQueueNameRequestRequestTypeDef,
    UpdateQueueOutboundCallerConfigRequestRequestTypeDef,
    UpdateQueueStatusRequestRequestTypeDef,
    UpdateQuickConnectConfigRequestRequestTypeDef,
    UpdateQuickConnectNameRequestRequestTypeDef,
    UpdateRoutingProfileAgentAvailabilityTimerRequestRequestTypeDef,
    UpdateRoutingProfileConcurrencyRequestRequestTypeDef,
    UpdateRoutingProfileDefaultOutboundQueueRequestRequestTypeDef,
    UpdateRoutingProfileNameRequestRequestTypeDef,
    UpdateRoutingProfileQueuesRequestRequestTypeDef,
    UpdateRuleRequestRequestTypeDef,
    UpdateSecurityProfileRequestRequestTypeDef,
    UpdateTaskTemplateRequestRequestTypeDef,
    UpdateTaskTemplateResponseTypeDef,
    UpdateTrafficDistributionRequestRequestTypeDef,
    UpdateUserHierarchyGroupNameRequestRequestTypeDef,
    UpdateUserHierarchyRequestRequestTypeDef,
    UpdateUserHierarchyStructureRequestRequestTypeDef,
    UpdateUserIdentityInfoRequestRequestTypeDef,
    UpdateUserPhoneConfigRequestRequestTypeDef,
    UpdateUserProficienciesRequestRequestTypeDef,
    UpdateUserRoutingProfileRequestRequestTypeDef,
    UpdateUserSecurityProfilesRequestRequestTypeDef,
    UpdateViewContentRequestRequestTypeDef,
    UpdateViewContentResponseTypeDef,
    UpdateViewMetadataRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ConnectClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ContactFlowNotPublishedException: Type[BotocoreClientError]
    ContactNotFoundException: Type[BotocoreClientError]
    DestinationNotAllowedException: Type[BotocoreClientError]
    DuplicateResourceException: Type[BotocoreClientError]
    IdempotencyException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidContactFlowException: Type[BotocoreClientError]
    InvalidContactFlowModuleException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MaximumResultReturnedException: Type[BotocoreClientError]
    OutboundContactNotPermittedException: Type[BotocoreClientError]
    OutputTypeNotFoundException: Type[BotocoreClientError]
    PropertyValidationException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceNotReadyException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UserNotFoundException: Type[BotocoreClientError]

class ConnectClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ConnectClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#close)
        """

    async def activate_evaluation_form(
        self, **kwargs: Unpack[ActivateEvaluationFormRequestRequestTypeDef]
    ) -> ActivateEvaluationFormResponseTypeDef:
        """
        Activates an evaluation form in the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/activate_evaluation_form.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#activate_evaluation_form)
        """

    async def associate_analytics_data_set(
        self, **kwargs: Unpack[AssociateAnalyticsDataSetRequestRequestTypeDef]
    ) -> AssociateAnalyticsDataSetResponseTypeDef:
        """
        Associates the specified dataset for a Amazon Connect instance with the target
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/associate_analytics_data_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#associate_analytics_data_set)
        """

    async def associate_approved_origin(
        self, **kwargs: Unpack[AssociateApprovedOriginRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/associate_approved_origin.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#associate_approved_origin)
        """

    async def associate_bot(
        self, **kwargs: Unpack[AssociateBotRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/associate_bot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#associate_bot)
        """

    async def associate_default_vocabulary(
        self, **kwargs: Unpack[AssociateDefaultVocabularyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates an existing vocabulary as the default.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/associate_default_vocabulary.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#associate_default_vocabulary)
        """

    async def associate_flow(
        self, **kwargs: Unpack[AssociateFlowRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a connect resource to a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/associate_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#associate_flow)
        """

    async def associate_instance_storage_config(
        self, **kwargs: Unpack[AssociateInstanceStorageConfigRequestRequestTypeDef]
    ) -> AssociateInstanceStorageConfigResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/associate_instance_storage_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#associate_instance_storage_config)
        """

    async def associate_lambda_function(
        self, **kwargs: Unpack[AssociateLambdaFunctionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/associate_lambda_function.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#associate_lambda_function)
        """

    async def associate_lex_bot(
        self, **kwargs: Unpack[AssociateLexBotRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/associate_lex_bot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#associate_lex_bot)
        """

    async def associate_phone_number_contact_flow(
        self, **kwargs: Unpack[AssociatePhoneNumberContactFlowRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates a flow with a phone number claimed to your Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/associate_phone_number_contact_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#associate_phone_number_contact_flow)
        """

    async def associate_queue_quick_connects(
        self, **kwargs: Unpack[AssociateQueueQuickConnectsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/associate_queue_quick_connects.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#associate_queue_quick_connects)
        """

    async def associate_routing_profile_queues(
        self, **kwargs: Unpack[AssociateRoutingProfileQueuesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates a set of queues with a routing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/associate_routing_profile_queues.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#associate_routing_profile_queues)
        """

    async def associate_security_key(
        self, **kwargs: Unpack[AssociateSecurityKeyRequestRequestTypeDef]
    ) -> AssociateSecurityKeyResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/associate_security_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#associate_security_key)
        """

    async def associate_traffic_distribution_group_user(
        self, **kwargs: Unpack[AssociateTrafficDistributionGroupUserRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates an agent with a traffic distribution group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/associate_traffic_distribution_group_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#associate_traffic_distribution_group_user)
        """

    async def associate_user_proficiencies(
        self, **kwargs: Unpack[AssociateUserProficienciesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        &gt;Associates a set of proficiencies with a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/associate_user_proficiencies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#associate_user_proficiencies)
        """

    async def batch_associate_analytics_data_set(
        self, **kwargs: Unpack[BatchAssociateAnalyticsDataSetRequestRequestTypeDef]
    ) -> BatchAssociateAnalyticsDataSetResponseTypeDef:
        """
        Associates a list of analytics datasets for a given Amazon Connect instance to
        a target account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/batch_associate_analytics_data_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#batch_associate_analytics_data_set)
        """

    async def batch_disassociate_analytics_data_set(
        self, **kwargs: Unpack[BatchDisassociateAnalyticsDataSetRequestRequestTypeDef]
    ) -> BatchDisassociateAnalyticsDataSetResponseTypeDef:
        """
        Removes a list of analytics datasets associated with a given Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/batch_disassociate_analytics_data_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#batch_disassociate_analytics_data_set)
        """

    async def batch_get_attached_file_metadata(
        self, **kwargs: Unpack[BatchGetAttachedFileMetadataRequestRequestTypeDef]
    ) -> BatchGetAttachedFileMetadataResponseTypeDef:
        """
        Allows you to retrieve metadata about multiple attached files on an associated
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/batch_get_attached_file_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#batch_get_attached_file_metadata)
        """

    async def batch_get_flow_association(
        self, **kwargs: Unpack[BatchGetFlowAssociationRequestRequestTypeDef]
    ) -> BatchGetFlowAssociationResponseTypeDef:
        """
        Retrieve the flow associations for the given resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/batch_get_flow_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#batch_get_flow_association)
        """

    async def batch_put_contact(
        self, **kwargs: Unpack[BatchPutContactRequestRequestTypeDef]
    ) -> BatchPutContactResponseTypeDef:
        """
        Only the Amazon Connect outbound campaigns service principal is allowed to
        assume a role in your account and call this API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/batch_put_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#batch_put_contact)
        """

    async def claim_phone_number(
        self, **kwargs: Unpack[ClaimPhoneNumberRequestRequestTypeDef]
    ) -> ClaimPhoneNumberResponseTypeDef:
        """
        Claims an available phone number to your Amazon Connect instance or traffic
        distribution group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/claim_phone_number.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#claim_phone_number)
        """

    async def complete_attached_file_upload(
        self, **kwargs: Unpack[CompleteAttachedFileUploadRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Allows you to confirm that the attached file has been uploaded using the
        pre-signed URL provided in the StartAttachedFileUpload API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/complete_attached_file_upload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#complete_attached_file_upload)
        """

    async def create_agent_status(
        self, **kwargs: Unpack[CreateAgentStatusRequestRequestTypeDef]
    ) -> CreateAgentStatusResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_agent_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_agent_status)
        """

    async def create_contact_flow(
        self, **kwargs: Unpack[CreateContactFlowRequestRequestTypeDef]
    ) -> CreateContactFlowResponseTypeDef:
        """
        Creates a flow for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_contact_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_contact_flow)
        """

    async def create_contact_flow_module(
        self, **kwargs: Unpack[CreateContactFlowModuleRequestRequestTypeDef]
    ) -> CreateContactFlowModuleResponseTypeDef:
        """
        Creates a flow module for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_contact_flow_module.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_contact_flow_module)
        """

    async def create_evaluation_form(
        self, **kwargs: Unpack[CreateEvaluationFormRequestRequestTypeDef]
    ) -> CreateEvaluationFormResponseTypeDef:
        """
        Creates an evaluation form in the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_evaluation_form.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_evaluation_form)
        """

    async def create_hours_of_operation(
        self, **kwargs: Unpack[CreateHoursOfOperationRequestRequestTypeDef]
    ) -> CreateHoursOfOperationResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_hours_of_operation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_hours_of_operation)
        """

    async def create_instance(
        self, **kwargs: Unpack[CreateInstanceRequestRequestTypeDef]
    ) -> CreateInstanceResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_instance)
        """

    async def create_integration_association(
        self, **kwargs: Unpack[CreateIntegrationAssociationRequestRequestTypeDef]
    ) -> CreateIntegrationAssociationResponseTypeDef:
        """
        Creates an Amazon Web Services resource association with an Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_integration_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_integration_association)
        """

    async def create_participant(
        self, **kwargs: Unpack[CreateParticipantRequestRequestTypeDef]
    ) -> CreateParticipantResponseTypeDef:
        """
        Adds a new participant into an on-going chat contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_participant.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_participant)
        """

    async def create_persistent_contact_association(
        self, **kwargs: Unpack[CreatePersistentContactAssociationRequestRequestTypeDef]
    ) -> CreatePersistentContactAssociationResponseTypeDef:
        """
        Enables rehydration of chats for the lifespan of a contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_persistent_contact_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_persistent_contact_association)
        """

    async def create_predefined_attribute(
        self, **kwargs: Unpack[CreatePredefinedAttributeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a new predefined attribute for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_predefined_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_predefined_attribute)
        """

    async def create_prompt(
        self, **kwargs: Unpack[CreatePromptRequestRequestTypeDef]
    ) -> CreatePromptResponseTypeDef:
        """
        Creates a prompt.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_prompt.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_prompt)
        """

    async def create_queue(
        self, **kwargs: Unpack[CreateQueueRequestRequestTypeDef]
    ) -> CreateQueueResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_queue.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_queue)
        """

    async def create_quick_connect(
        self, **kwargs: Unpack[CreateQuickConnectRequestRequestTypeDef]
    ) -> CreateQuickConnectResponseTypeDef:
        """
        Creates a quick connect for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_quick_connect.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_quick_connect)
        """

    async def create_routing_profile(
        self, **kwargs: Unpack[CreateRoutingProfileRequestRequestTypeDef]
    ) -> CreateRoutingProfileResponseTypeDef:
        """
        Creates a new routing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_routing_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_routing_profile)
        """

    async def create_rule(
        self, **kwargs: Unpack[CreateRuleRequestRequestTypeDef]
    ) -> CreateRuleResponseTypeDef:
        """
        Creates a rule for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_rule)
        """

    async def create_security_profile(
        self, **kwargs: Unpack[CreateSecurityProfileRequestRequestTypeDef]
    ) -> CreateSecurityProfileResponseTypeDef:
        """
        Creates a security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_security_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_security_profile)
        """

    async def create_task_template(
        self, **kwargs: Unpack[CreateTaskTemplateRequestRequestTypeDef]
    ) -> CreateTaskTemplateResponseTypeDef:
        """
        Creates a new task template in the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_task_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_task_template)
        """

    async def create_traffic_distribution_group(
        self, **kwargs: Unpack[CreateTrafficDistributionGroupRequestRequestTypeDef]
    ) -> CreateTrafficDistributionGroupResponseTypeDef:
        """
        Creates a traffic distribution group given an Amazon Connect instance that has
        been replicated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_traffic_distribution_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_traffic_distribution_group)
        """

    async def create_use_case(
        self, **kwargs: Unpack[CreateUseCaseRequestRequestTypeDef]
    ) -> CreateUseCaseResponseTypeDef:
        """
        Creates a use case for an integration association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_use_case.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_use_case)
        """

    async def create_user(
        self, **kwargs: Unpack[CreateUserRequestRequestTypeDef]
    ) -> CreateUserResponseTypeDef:
        """
        Creates a user account for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_user)
        """

    async def create_user_hierarchy_group(
        self, **kwargs: Unpack[CreateUserHierarchyGroupRequestRequestTypeDef]
    ) -> CreateUserHierarchyGroupResponseTypeDef:
        """
        Creates a new user hierarchy group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_user_hierarchy_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_user_hierarchy_group)
        """

    async def create_view(
        self, **kwargs: Unpack[CreateViewRequestRequestTypeDef]
    ) -> CreateViewResponseTypeDef:
        """
        Creates a new view with the possible status of <code>SAVED</code> or
        <code>PUBLISHED</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_view.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_view)
        """

    async def create_view_version(
        self, **kwargs: Unpack[CreateViewVersionRequestRequestTypeDef]
    ) -> CreateViewVersionResponseTypeDef:
        """
        Publishes a new version of the view identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_view_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_view_version)
        """

    async def create_vocabulary(
        self, **kwargs: Unpack[CreateVocabularyRequestRequestTypeDef]
    ) -> CreateVocabularyResponseTypeDef:
        """
        Creates a custom vocabulary associated with your Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/create_vocabulary.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#create_vocabulary)
        """

    async def deactivate_evaluation_form(
        self, **kwargs: Unpack[DeactivateEvaluationFormRequestRequestTypeDef]
    ) -> DeactivateEvaluationFormResponseTypeDef:
        """
        Deactivates an evaluation form in the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/deactivate_evaluation_form.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#deactivate_evaluation_form)
        """

    async def delete_attached_file(
        self, **kwargs: Unpack[DeleteAttachedFileRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an attached file along with the underlying S3 Object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_attached_file.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_attached_file)
        """

    async def delete_contact_evaluation(
        self, **kwargs: Unpack[DeleteContactEvaluationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a contact evaluation in the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_contact_evaluation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_contact_evaluation)
        """

    async def delete_contact_flow(
        self, **kwargs: Unpack[DeleteContactFlowRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a flow for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_contact_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_contact_flow)
        """

    async def delete_contact_flow_module(
        self, **kwargs: Unpack[DeleteContactFlowModuleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified flow module.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_contact_flow_module.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_contact_flow_module)
        """

    async def delete_evaluation_form(
        self, **kwargs: Unpack[DeleteEvaluationFormRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an evaluation form in the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_evaluation_form.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_evaluation_form)
        """

    async def delete_hours_of_operation(
        self, **kwargs: Unpack[DeleteHoursOfOperationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_hours_of_operation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_hours_of_operation)
        """

    async def delete_instance(
        self, **kwargs: Unpack[DeleteInstanceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_instance)
        """

    async def delete_integration_association(
        self, **kwargs: Unpack[DeleteIntegrationAssociationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Web Services resource association from an Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_integration_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_integration_association)
        """

    async def delete_predefined_attribute(
        self, **kwargs: Unpack[DeletePredefinedAttributeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a predefined attribute from the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_predefined_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_predefined_attribute)
        """

    async def delete_prompt(
        self, **kwargs: Unpack[DeletePromptRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a prompt.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_prompt.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_prompt)
        """

    async def delete_queue(
        self, **kwargs: Unpack[DeleteQueueRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_queue.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_queue)
        """

    async def delete_quick_connect(
        self, **kwargs: Unpack[DeleteQuickConnectRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a quick connect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_quick_connect.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_quick_connect)
        """

    async def delete_routing_profile(
        self, **kwargs: Unpack[DeleteRoutingProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a routing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_routing_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_routing_profile)
        """

    async def delete_rule(
        self, **kwargs: Unpack[DeleteRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a rule for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_rule)
        """

    async def delete_security_profile(
        self, **kwargs: Unpack[DeleteSecurityProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_security_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_security_profile)
        """

    async def delete_task_template(
        self, **kwargs: Unpack[DeleteTaskTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the task template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_task_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_task_template)
        """

    async def delete_traffic_distribution_group(
        self, **kwargs: Unpack[DeleteTrafficDistributionGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a traffic distribution group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_traffic_distribution_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_traffic_distribution_group)
        """

    async def delete_use_case(
        self, **kwargs: Unpack[DeleteUseCaseRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a use case from an integration association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_use_case.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_use_case)
        """

    async def delete_user(
        self, **kwargs: Unpack[DeleteUserRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a user account from the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_user)
        """

    async def delete_user_hierarchy_group(
        self, **kwargs: Unpack[DeleteUserHierarchyGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an existing user hierarchy group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_user_hierarchy_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_user_hierarchy_group)
        """

    async def delete_view(
        self, **kwargs: Unpack[DeleteViewRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the view entirely.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_view.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_view)
        """

    async def delete_view_version(
        self, **kwargs: Unpack[DeleteViewVersionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the particular version specified in <code>ViewVersion</code> identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_view_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_view_version)
        """

    async def delete_vocabulary(
        self, **kwargs: Unpack[DeleteVocabularyRequestRequestTypeDef]
    ) -> DeleteVocabularyResponseTypeDef:
        """
        Deletes the vocabulary that has the given identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/delete_vocabulary.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#delete_vocabulary)
        """

    async def describe_agent_status(
        self, **kwargs: Unpack[DescribeAgentStatusRequestRequestTypeDef]
    ) -> DescribeAgentStatusResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_agent_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_agent_status)
        """

    async def describe_authentication_profile(
        self, **kwargs: Unpack[DescribeAuthenticationProfileRequestRequestTypeDef]
    ) -> DescribeAuthenticationProfileResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_authentication_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_authentication_profile)
        """

    async def describe_contact(
        self, **kwargs: Unpack[DescribeContactRequestRequestTypeDef]
    ) -> DescribeContactResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_contact)
        """

    async def describe_contact_evaluation(
        self, **kwargs: Unpack[DescribeContactEvaluationRequestRequestTypeDef]
    ) -> DescribeContactEvaluationResponseTypeDef:
        """
        Describes a contact evaluation in the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_contact_evaluation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_contact_evaluation)
        """

    async def describe_contact_flow(
        self, **kwargs: Unpack[DescribeContactFlowRequestRequestTypeDef]
    ) -> DescribeContactFlowResponseTypeDef:
        """
        Describes the specified flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_contact_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_contact_flow)
        """

    async def describe_contact_flow_module(
        self, **kwargs: Unpack[DescribeContactFlowModuleRequestRequestTypeDef]
    ) -> DescribeContactFlowModuleResponseTypeDef:
        """
        Describes the specified flow module.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_contact_flow_module.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_contact_flow_module)
        """

    async def describe_evaluation_form(
        self, **kwargs: Unpack[DescribeEvaluationFormRequestRequestTypeDef]
    ) -> DescribeEvaluationFormResponseTypeDef:
        """
        Describes an evaluation form in the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_evaluation_form.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_evaluation_form)
        """

    async def describe_hours_of_operation(
        self, **kwargs: Unpack[DescribeHoursOfOperationRequestRequestTypeDef]
    ) -> DescribeHoursOfOperationResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_hours_of_operation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_hours_of_operation)
        """

    async def describe_instance(
        self, **kwargs: Unpack[DescribeInstanceRequestRequestTypeDef]
    ) -> DescribeInstanceResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_instance)
        """

    async def describe_instance_attribute(
        self, **kwargs: Unpack[DescribeInstanceAttributeRequestRequestTypeDef]
    ) -> DescribeInstanceAttributeResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_instance_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_instance_attribute)
        """

    async def describe_instance_storage_config(
        self, **kwargs: Unpack[DescribeInstanceStorageConfigRequestRequestTypeDef]
    ) -> DescribeInstanceStorageConfigResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_instance_storage_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_instance_storage_config)
        """

    async def describe_phone_number(
        self, **kwargs: Unpack[DescribePhoneNumberRequestRequestTypeDef]
    ) -> DescribePhoneNumberResponseTypeDef:
        """
        Gets details and status of a phone number that's claimed to your Amazon Connect
        instance or traffic distribution group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_phone_number.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_phone_number)
        """

    async def describe_predefined_attribute(
        self, **kwargs: Unpack[DescribePredefinedAttributeRequestRequestTypeDef]
    ) -> DescribePredefinedAttributeResponseTypeDef:
        """
        Describes a predefined attribute for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_predefined_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_predefined_attribute)
        """

    async def describe_prompt(
        self, **kwargs: Unpack[DescribePromptRequestRequestTypeDef]
    ) -> DescribePromptResponseTypeDef:
        """
        Describes the prompt.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_prompt.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_prompt)
        """

    async def describe_queue(
        self, **kwargs: Unpack[DescribeQueueRequestRequestTypeDef]
    ) -> DescribeQueueResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_queue.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_queue)
        """

    async def describe_quick_connect(
        self, **kwargs: Unpack[DescribeQuickConnectRequestRequestTypeDef]
    ) -> DescribeQuickConnectResponseTypeDef:
        """
        Describes the quick connect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_quick_connect.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_quick_connect)
        """

    async def describe_routing_profile(
        self, **kwargs: Unpack[DescribeRoutingProfileRequestRequestTypeDef]
    ) -> DescribeRoutingProfileResponseTypeDef:
        """
        Describes the specified routing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_routing_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_routing_profile)
        """

    async def describe_rule(
        self, **kwargs: Unpack[DescribeRuleRequestRequestTypeDef]
    ) -> DescribeRuleResponseTypeDef:
        """
        Describes a rule for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_rule)
        """

    async def describe_security_profile(
        self, **kwargs: Unpack[DescribeSecurityProfileRequestRequestTypeDef]
    ) -> DescribeSecurityProfileResponseTypeDef:
        """
        Gets basic information about the security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_security_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_security_profile)
        """

    async def describe_traffic_distribution_group(
        self, **kwargs: Unpack[DescribeTrafficDistributionGroupRequestRequestTypeDef]
    ) -> DescribeTrafficDistributionGroupResponseTypeDef:
        """
        Gets details and status of a traffic distribution group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_traffic_distribution_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_traffic_distribution_group)
        """

    async def describe_user(
        self, **kwargs: Unpack[DescribeUserRequestRequestTypeDef]
    ) -> DescribeUserResponseTypeDef:
        """
        Describes the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_user)
        """

    async def describe_user_hierarchy_group(
        self, **kwargs: Unpack[DescribeUserHierarchyGroupRequestRequestTypeDef]
    ) -> DescribeUserHierarchyGroupResponseTypeDef:
        """
        Describes the specified hierarchy group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_user_hierarchy_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_user_hierarchy_group)
        """

    async def describe_user_hierarchy_structure(
        self, **kwargs: Unpack[DescribeUserHierarchyStructureRequestRequestTypeDef]
    ) -> DescribeUserHierarchyStructureResponseTypeDef:
        """
        Describes the hierarchy structure of the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_user_hierarchy_structure.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_user_hierarchy_structure)
        """

    async def describe_view(
        self, **kwargs: Unpack[DescribeViewRequestRequestTypeDef]
    ) -> DescribeViewResponseTypeDef:
        """
        Retrieves the view for the specified Amazon Connect instance and view
        identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_view.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_view)
        """

    async def describe_vocabulary(
        self, **kwargs: Unpack[DescribeVocabularyRequestRequestTypeDef]
    ) -> DescribeVocabularyResponseTypeDef:
        """
        Describes the specified vocabulary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_vocabulary.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#describe_vocabulary)
        """

    async def disassociate_analytics_data_set(
        self, **kwargs: Unpack[DisassociateAnalyticsDataSetRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the dataset ID associated with a given Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/disassociate_analytics_data_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#disassociate_analytics_data_set)
        """

    async def disassociate_approved_origin(
        self, **kwargs: Unpack[DisassociateApprovedOriginRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/disassociate_approved_origin.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#disassociate_approved_origin)
        """

    async def disassociate_bot(
        self, **kwargs: Unpack[DisassociateBotRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/disassociate_bot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#disassociate_bot)
        """

    async def disassociate_flow(
        self, **kwargs: Unpack[DisassociateFlowRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a connect resource from a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/disassociate_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#disassociate_flow)
        """

    async def disassociate_instance_storage_config(
        self, **kwargs: Unpack[DisassociateInstanceStorageConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/disassociate_instance_storage_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#disassociate_instance_storage_config)
        """

    async def disassociate_lambda_function(
        self, **kwargs: Unpack[DisassociateLambdaFunctionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/disassociate_lambda_function.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#disassociate_lambda_function)
        """

    async def disassociate_lex_bot(
        self, **kwargs: Unpack[DisassociateLexBotRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/disassociate_lex_bot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#disassociate_lex_bot)
        """

    async def disassociate_phone_number_contact_flow(
        self, **kwargs: Unpack[DisassociatePhoneNumberContactFlowRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the flow association from a phone number claimed to your Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/disassociate_phone_number_contact_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#disassociate_phone_number_contact_flow)
        """

    async def disassociate_queue_quick_connects(
        self, **kwargs: Unpack[DisassociateQueueQuickConnectsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/disassociate_queue_quick_connects.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#disassociate_queue_quick_connects)
        """

    async def disassociate_routing_profile_queues(
        self, **kwargs: Unpack[DisassociateRoutingProfileQueuesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates a set of queues from a routing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/disassociate_routing_profile_queues.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#disassociate_routing_profile_queues)
        """

    async def disassociate_security_key(
        self, **kwargs: Unpack[DisassociateSecurityKeyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/disassociate_security_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#disassociate_security_key)
        """

    async def disassociate_traffic_distribution_group_user(
        self, **kwargs: Unpack[DisassociateTrafficDistributionGroupUserRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates an agent from a traffic distribution group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/disassociate_traffic_distribution_group_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#disassociate_traffic_distribution_group_user)
        """

    async def disassociate_user_proficiencies(
        self, **kwargs: Unpack[DisassociateUserProficienciesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates a set of proficiencies from a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/disassociate_user_proficiencies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#disassociate_user_proficiencies)
        """

    async def dismiss_user_contact(
        self, **kwargs: Unpack[DismissUserContactRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Dismisses contacts from an agent's CCP and returns the agent to an available
        state, which allows the agent to receive a new routed contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/dismiss_user_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#dismiss_user_contact)
        """

    async def get_attached_file(
        self, **kwargs: Unpack[GetAttachedFileRequestRequestTypeDef]
    ) -> GetAttachedFileResponseTypeDef:
        """
        Provides a pre-signed URL for download of an approved attached file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_attached_file.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_attached_file)
        """

    async def get_contact_attributes(
        self, **kwargs: Unpack[GetContactAttributesRequestRequestTypeDef]
    ) -> GetContactAttributesResponseTypeDef:
        """
        Retrieves the contact attributes for the specified contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_contact_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_contact_attributes)
        """

    async def get_current_metric_data(
        self, **kwargs: Unpack[GetCurrentMetricDataRequestRequestTypeDef]
    ) -> GetCurrentMetricDataResponseTypeDef:
        """
        Gets the real-time metric data from the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_current_metric_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_current_metric_data)
        """

    async def get_current_user_data(
        self, **kwargs: Unpack[GetCurrentUserDataRequestRequestTypeDef]
    ) -> GetCurrentUserDataResponseTypeDef:
        """
        Gets the real-time active user data from the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_current_user_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_current_user_data)
        """

    async def get_federation_token(
        self, **kwargs: Unpack[GetFederationTokenRequestRequestTypeDef]
    ) -> GetFederationTokenResponseTypeDef:
        """
        Supports SAML sign-in for Amazon Connect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_federation_token.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_federation_token)
        """

    async def get_flow_association(
        self, **kwargs: Unpack[GetFlowAssociationRequestRequestTypeDef]
    ) -> GetFlowAssociationResponseTypeDef:
        """
        Retrieves the flow associated for a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_flow_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_flow_association)
        """

    async def get_metric_data(
        self, **kwargs: Unpack[GetMetricDataRequestRequestTypeDef]
    ) -> GetMetricDataResponseTypeDef:
        """
        Gets historical metric data from the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_metric_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_metric_data)
        """

    async def get_metric_data_v2(
        self, **kwargs: Unpack[GetMetricDataV2RequestRequestTypeDef]
    ) -> GetMetricDataV2ResponseTypeDef:
        """
        Gets metric data from the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_metric_data_v2.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_metric_data_v2)
        """

    async def get_prompt_file(
        self, **kwargs: Unpack[GetPromptFileRequestRequestTypeDef]
    ) -> GetPromptFileResponseTypeDef:
        """
        Gets the prompt file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_prompt_file.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_prompt_file)
        """

    async def get_task_template(
        self, **kwargs: Unpack[GetTaskTemplateRequestRequestTypeDef]
    ) -> GetTaskTemplateResponseTypeDef:
        """
        Gets details about a specific task template in the specified Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_task_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_task_template)
        """

    async def get_traffic_distribution(
        self, **kwargs: Unpack[GetTrafficDistributionRequestRequestTypeDef]
    ) -> GetTrafficDistributionResponseTypeDef:
        """
        Retrieves the current traffic distribution for a given traffic distribution
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_traffic_distribution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_traffic_distribution)
        """

    async def import_phone_number(
        self, **kwargs: Unpack[ImportPhoneNumberRequestRequestTypeDef]
    ) -> ImportPhoneNumberResponseTypeDef:
        """
        Imports a claimed phone number from an external service, such as Amazon
        Pinpoint, into an Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/import_phone_number.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#import_phone_number)
        """

    async def list_agent_statuses(
        self, **kwargs: Unpack[ListAgentStatusRequestRequestTypeDef]
    ) -> ListAgentStatusResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_agent_statuses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_agent_statuses)
        """

    async def list_analytics_data_associations(
        self, **kwargs: Unpack[ListAnalyticsDataAssociationsRequestRequestTypeDef]
    ) -> ListAnalyticsDataAssociationsResponseTypeDef:
        """
        Lists the association status of requested dataset ID for a given Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_analytics_data_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_analytics_data_associations)
        """

    async def list_approved_origins(
        self, **kwargs: Unpack[ListApprovedOriginsRequestRequestTypeDef]
    ) -> ListApprovedOriginsResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_approved_origins.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_approved_origins)
        """

    async def list_authentication_profiles(
        self, **kwargs: Unpack[ListAuthenticationProfilesRequestRequestTypeDef]
    ) -> ListAuthenticationProfilesResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_authentication_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_authentication_profiles)
        """

    async def list_bots(
        self, **kwargs: Unpack[ListBotsRequestRequestTypeDef]
    ) -> ListBotsResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_bots.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_bots)
        """

    async def list_contact_evaluations(
        self, **kwargs: Unpack[ListContactEvaluationsRequestRequestTypeDef]
    ) -> ListContactEvaluationsResponseTypeDef:
        """
        Lists contact evaluations in the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_contact_evaluations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_contact_evaluations)
        """

    async def list_contact_flow_modules(
        self, **kwargs: Unpack[ListContactFlowModulesRequestRequestTypeDef]
    ) -> ListContactFlowModulesResponseTypeDef:
        """
        Provides information about the flow modules for the specified Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_contact_flow_modules.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_contact_flow_modules)
        """

    async def list_contact_flows(
        self, **kwargs: Unpack[ListContactFlowsRequestRequestTypeDef]
    ) -> ListContactFlowsResponseTypeDef:
        """
        Provides information about the flows for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_contact_flows.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_contact_flows)
        """

    async def list_contact_references(
        self, **kwargs: Unpack[ListContactReferencesRequestRequestTypeDef]
    ) -> ListContactReferencesResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_contact_references.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_contact_references)
        """

    async def list_default_vocabularies(
        self, **kwargs: Unpack[ListDefaultVocabulariesRequestRequestTypeDef]
    ) -> ListDefaultVocabulariesResponseTypeDef:
        """
        Lists the default vocabularies for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_default_vocabularies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_default_vocabularies)
        """

    async def list_evaluation_form_versions(
        self, **kwargs: Unpack[ListEvaluationFormVersionsRequestRequestTypeDef]
    ) -> ListEvaluationFormVersionsResponseTypeDef:
        """
        Lists versions of an evaluation form in the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_evaluation_form_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_evaluation_form_versions)
        """

    async def list_evaluation_forms(
        self, **kwargs: Unpack[ListEvaluationFormsRequestRequestTypeDef]
    ) -> ListEvaluationFormsResponseTypeDef:
        """
        Lists evaluation forms in the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_evaluation_forms.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_evaluation_forms)
        """

    async def list_flow_associations(
        self, **kwargs: Unpack[ListFlowAssociationsRequestRequestTypeDef]
    ) -> ListFlowAssociationsResponseTypeDef:
        """
        List the flow association based on the filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_flow_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_flow_associations)
        """

    async def list_hours_of_operations(
        self, **kwargs: Unpack[ListHoursOfOperationsRequestRequestTypeDef]
    ) -> ListHoursOfOperationsResponseTypeDef:
        """
        Provides information about the hours of operation for the specified Amazon
        Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_hours_of_operations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_hours_of_operations)
        """

    async def list_instance_attributes(
        self, **kwargs: Unpack[ListInstanceAttributesRequestRequestTypeDef]
    ) -> ListInstanceAttributesResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_instance_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_instance_attributes)
        """

    async def list_instance_storage_configs(
        self, **kwargs: Unpack[ListInstanceStorageConfigsRequestRequestTypeDef]
    ) -> ListInstanceStorageConfigsResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_instance_storage_configs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_instance_storage_configs)
        """

    async def list_instances(
        self, **kwargs: Unpack[ListInstancesRequestRequestTypeDef]
    ) -> ListInstancesResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_instances)
        """

    async def list_integration_associations(
        self, **kwargs: Unpack[ListIntegrationAssociationsRequestRequestTypeDef]
    ) -> ListIntegrationAssociationsResponseTypeDef:
        """
        Provides summary information about the Amazon Web Services resource
        associations for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_integration_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_integration_associations)
        """

    async def list_lambda_functions(
        self, **kwargs: Unpack[ListLambdaFunctionsRequestRequestTypeDef]
    ) -> ListLambdaFunctionsResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_lambda_functions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_lambda_functions)
        """

    async def list_lex_bots(
        self, **kwargs: Unpack[ListLexBotsRequestRequestTypeDef]
    ) -> ListLexBotsResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_lex_bots.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_lex_bots)
        """

    async def list_phone_numbers(
        self, **kwargs: Unpack[ListPhoneNumbersRequestRequestTypeDef]
    ) -> ListPhoneNumbersResponseTypeDef:
        """
        Provides information about the phone numbers for the specified Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_phone_numbers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_phone_numbers)
        """

    async def list_phone_numbers_v2(
        self, **kwargs: Unpack[ListPhoneNumbersV2RequestRequestTypeDef]
    ) -> ListPhoneNumbersV2ResponseTypeDef:
        """
        Lists phone numbers claimed to your Amazon Connect instance or traffic
        distribution group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_phone_numbers_v2.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_phone_numbers_v2)
        """

    async def list_predefined_attributes(
        self, **kwargs: Unpack[ListPredefinedAttributesRequestRequestTypeDef]
    ) -> ListPredefinedAttributesResponseTypeDef:
        """
        Lists predefined attributes for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_predefined_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_predefined_attributes)
        """

    async def list_prompts(
        self, **kwargs: Unpack[ListPromptsRequestRequestTypeDef]
    ) -> ListPromptsResponseTypeDef:
        """
        Provides information about the prompts for the specified Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_prompts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_prompts)
        """

    async def list_queue_quick_connects(
        self, **kwargs: Unpack[ListQueueQuickConnectsRequestRequestTypeDef]
    ) -> ListQueueQuickConnectsResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_queue_quick_connects.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_queue_quick_connects)
        """

    async def list_queues(
        self, **kwargs: Unpack[ListQueuesRequestRequestTypeDef]
    ) -> ListQueuesResponseTypeDef:
        """
        Provides information about the queues for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_queues.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_queues)
        """

    async def list_quick_connects(
        self, **kwargs: Unpack[ListQuickConnectsRequestRequestTypeDef]
    ) -> ListQuickConnectsResponseTypeDef:
        """
        Provides information about the quick connects for the specified Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_quick_connects.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_quick_connects)
        """

    async def list_realtime_contact_analysis_segments_v2(
        self, **kwargs: Unpack[ListRealtimeContactAnalysisSegmentsV2RequestRequestTypeDef]
    ) -> ListRealtimeContactAnalysisSegmentsV2ResponseTypeDef:
        """
        Provides a list of analysis segments for a real-time analysis session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_realtime_contact_analysis_segments_v2.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_realtime_contact_analysis_segments_v2)
        """

    async def list_routing_profile_queues(
        self, **kwargs: Unpack[ListRoutingProfileQueuesRequestRequestTypeDef]
    ) -> ListRoutingProfileQueuesResponseTypeDef:
        """
        Lists the queues associated with a routing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_routing_profile_queues.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_routing_profile_queues)
        """

    async def list_routing_profiles(
        self, **kwargs: Unpack[ListRoutingProfilesRequestRequestTypeDef]
    ) -> ListRoutingProfilesResponseTypeDef:
        """
        Provides summary information about the routing profiles for the specified
        Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_routing_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_routing_profiles)
        """

    async def list_rules(
        self, **kwargs: Unpack[ListRulesRequestRequestTypeDef]
    ) -> ListRulesResponseTypeDef:
        """
        List all rules for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_rules.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_rules)
        """

    async def list_security_keys(
        self, **kwargs: Unpack[ListSecurityKeysRequestRequestTypeDef]
    ) -> ListSecurityKeysResponseTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_security_keys.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_security_keys)
        """

    async def list_security_profile_applications(
        self, **kwargs: Unpack[ListSecurityProfileApplicationsRequestRequestTypeDef]
    ) -> ListSecurityProfileApplicationsResponseTypeDef:
        """
        Returns a list of third-party applications in a specific security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_security_profile_applications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_security_profile_applications)
        """

    async def list_security_profile_permissions(
        self, **kwargs: Unpack[ListSecurityProfilePermissionsRequestRequestTypeDef]
    ) -> ListSecurityProfilePermissionsResponseTypeDef:
        """
        Lists the permissions granted to a security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_security_profile_permissions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_security_profile_permissions)
        """

    async def list_security_profiles(
        self, **kwargs: Unpack[ListSecurityProfilesRequestRequestTypeDef]
    ) -> ListSecurityProfilesResponseTypeDef:
        """
        Provides summary information about the security profiles for the specified
        Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_security_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_security_profiles)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_tags_for_resource)
        """

    async def list_task_templates(
        self, **kwargs: Unpack[ListTaskTemplatesRequestRequestTypeDef]
    ) -> ListTaskTemplatesResponseTypeDef:
        """
        Lists task templates for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_task_templates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_task_templates)
        """

    async def list_traffic_distribution_group_users(
        self, **kwargs: Unpack[ListTrafficDistributionGroupUsersRequestRequestTypeDef]
    ) -> ListTrafficDistributionGroupUsersResponseTypeDef:
        """
        Lists traffic distribution group users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_traffic_distribution_group_users.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_traffic_distribution_group_users)
        """

    async def list_traffic_distribution_groups(
        self, **kwargs: Unpack[ListTrafficDistributionGroupsRequestRequestTypeDef]
    ) -> ListTrafficDistributionGroupsResponseTypeDef:
        """
        Lists traffic distribution groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_traffic_distribution_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_traffic_distribution_groups)
        """

    async def list_use_cases(
        self, **kwargs: Unpack[ListUseCasesRequestRequestTypeDef]
    ) -> ListUseCasesResponseTypeDef:
        """
        Lists the use cases for the integration association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_use_cases.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_use_cases)
        """

    async def list_user_hierarchy_groups(
        self, **kwargs: Unpack[ListUserHierarchyGroupsRequestRequestTypeDef]
    ) -> ListUserHierarchyGroupsResponseTypeDef:
        """
        Provides summary information about the hierarchy groups for the specified
        Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_user_hierarchy_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_user_hierarchy_groups)
        """

    async def list_user_proficiencies(
        self, **kwargs: Unpack[ListUserProficienciesRequestRequestTypeDef]
    ) -> ListUserProficienciesResponseTypeDef:
        """
        Lists proficiencies associated with a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_user_proficiencies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_user_proficiencies)
        """

    async def list_users(
        self, **kwargs: Unpack[ListUsersRequestRequestTypeDef]
    ) -> ListUsersResponseTypeDef:
        """
        Provides summary information about the users for the specified Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_users.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_users)
        """

    async def list_view_versions(
        self, **kwargs: Unpack[ListViewVersionsRequestRequestTypeDef]
    ) -> ListViewVersionsResponseTypeDef:
        """
        Returns all the available versions for the specified Amazon Connect instance
        and view identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_view_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_view_versions)
        """

    async def list_views(
        self, **kwargs: Unpack[ListViewsRequestRequestTypeDef]
    ) -> ListViewsResponseTypeDef:
        """
        Returns views in the given instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/list_views.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#list_views)
        """

    async def monitor_contact(
        self, **kwargs: Unpack[MonitorContactRequestRequestTypeDef]
    ) -> MonitorContactResponseTypeDef:
        """
        Initiates silent monitoring of a contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/monitor_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#monitor_contact)
        """

    async def pause_contact(
        self, **kwargs: Unpack[PauseContactRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Allows pausing an ongoing task contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/pause_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#pause_contact)
        """

    async def put_user_status(
        self, **kwargs: Unpack[PutUserStatusRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Changes the current status of a user or agent in Amazon Connect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/put_user_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#put_user_status)
        """

    async def release_phone_number(
        self, **kwargs: Unpack[ReleasePhoneNumberRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Releases a phone number previously claimed to an Amazon Connect instance or
        traffic distribution group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/release_phone_number.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#release_phone_number)
        """

    async def replicate_instance(
        self, **kwargs: Unpack[ReplicateInstanceRequestRequestTypeDef]
    ) -> ReplicateInstanceResponseTypeDef:
        """
        Replicates an Amazon Connect instance in the specified Amazon Web Services
        Region and copies configuration information for Amazon Connect resources across
        Amazon Web Services Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/replicate_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#replicate_instance)
        """

    async def resume_contact(
        self, **kwargs: Unpack[ResumeContactRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Allows resuming a task contact in a paused state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/resume_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#resume_contact)
        """

    async def resume_contact_recording(
        self, **kwargs: Unpack[ResumeContactRecordingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        When a contact is being recorded, and the recording has been suspended using
        SuspendContactRecording, this API resumes recording whatever recording is
        selected in the flow configuration: call, screen, or both.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/resume_contact_recording.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#resume_contact_recording)
        """

    async def search_agent_statuses(
        self, **kwargs: Unpack[SearchAgentStatusesRequestRequestTypeDef]
    ) -> SearchAgentStatusesResponseTypeDef:
        """
        Searches AgentStatuses in an Amazon Connect instance, with optional filtering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/search_agent_statuses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#search_agent_statuses)
        """

    async def search_available_phone_numbers(
        self, **kwargs: Unpack[SearchAvailablePhoneNumbersRequestRequestTypeDef]
    ) -> SearchAvailablePhoneNumbersResponseTypeDef:
        """
        Searches for available phone numbers that you can claim to your Amazon Connect
        instance or traffic distribution group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/search_available_phone_numbers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#search_available_phone_numbers)
        """

    async def search_contact_flow_modules(
        self, **kwargs: Unpack[SearchContactFlowModulesRequestRequestTypeDef]
    ) -> SearchContactFlowModulesResponseTypeDef:
        """
        Searches the flow modules in an Amazon Connect instance, with optional
        filtering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/search_contact_flow_modules.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#search_contact_flow_modules)
        """

    async def search_contact_flows(
        self, **kwargs: Unpack[SearchContactFlowsRequestRequestTypeDef]
    ) -> SearchContactFlowsResponseTypeDef:
        """
        Searches the contact flows in an Amazon Connect instance, with optional
        filtering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/search_contact_flows.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#search_contact_flows)
        """

    async def search_contacts(
        self, **kwargs: Unpack[SearchContactsRequestRequestTypeDef]
    ) -> SearchContactsResponseTypeDef:
        """
        Searches contacts in an Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/search_contacts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#search_contacts)
        """

    async def search_hours_of_operations(
        self, **kwargs: Unpack[SearchHoursOfOperationsRequestRequestTypeDef]
    ) -> SearchHoursOfOperationsResponseTypeDef:
        """
        Searches the hours of operation in an Amazon Connect instance, with optional
        filtering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/search_hours_of_operations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#search_hours_of_operations)
        """

    async def search_predefined_attributes(
        self, **kwargs: Unpack[SearchPredefinedAttributesRequestRequestTypeDef]
    ) -> SearchPredefinedAttributesResponseTypeDef:
        """
        Searches predefined attributes that meet certain criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/search_predefined_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#search_predefined_attributes)
        """

    async def search_prompts(
        self, **kwargs: Unpack[SearchPromptsRequestRequestTypeDef]
    ) -> SearchPromptsResponseTypeDef:
        """
        Searches prompts in an Amazon Connect instance, with optional filtering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/search_prompts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#search_prompts)
        """

    async def search_queues(
        self, **kwargs: Unpack[SearchQueuesRequestRequestTypeDef]
    ) -> SearchQueuesResponseTypeDef:
        """
        Searches queues in an Amazon Connect instance, with optional filtering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/search_queues.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#search_queues)
        """

    async def search_quick_connects(
        self, **kwargs: Unpack[SearchQuickConnectsRequestRequestTypeDef]
    ) -> SearchQuickConnectsResponseTypeDef:
        """
        Searches quick connects in an Amazon Connect instance, with optional filtering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/search_quick_connects.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#search_quick_connects)
        """

    async def search_resource_tags(
        self, **kwargs: Unpack[SearchResourceTagsRequestRequestTypeDef]
    ) -> SearchResourceTagsResponseTypeDef:
        """
        Searches tags used in an Amazon Connect instance using optional search criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/search_resource_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#search_resource_tags)
        """

    async def search_routing_profiles(
        self, **kwargs: Unpack[SearchRoutingProfilesRequestRequestTypeDef]
    ) -> SearchRoutingProfilesResponseTypeDef:
        """
        Searches routing profiles in an Amazon Connect instance, with optional
        filtering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/search_routing_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#search_routing_profiles)
        """

    async def search_security_profiles(
        self, **kwargs: Unpack[SearchSecurityProfilesRequestRequestTypeDef]
    ) -> SearchSecurityProfilesResponseTypeDef:
        """
        Searches security profiles in an Amazon Connect instance, with optional
        filtering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/search_security_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#search_security_profiles)
        """

    async def search_user_hierarchy_groups(
        self, **kwargs: Unpack[SearchUserHierarchyGroupsRequestRequestTypeDef]
    ) -> SearchUserHierarchyGroupsResponseTypeDef:
        """
        Searches UserHierarchyGroups in an Amazon Connect instance, with optional
        filtering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/search_user_hierarchy_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#search_user_hierarchy_groups)
        """

    async def search_users(
        self, **kwargs: Unpack[SearchUsersRequestRequestTypeDef]
    ) -> SearchUsersResponseTypeDef:
        """
        Searches users in an Amazon Connect instance, with optional filtering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/search_users.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#search_users)
        """

    async def search_vocabularies(
        self, **kwargs: Unpack[SearchVocabulariesRequestRequestTypeDef]
    ) -> SearchVocabulariesResponseTypeDef:
        """
        Searches for vocabularies within a specific Amazon Connect instance using
        <code>State</code>, <code>NameStartsWith</code>, and <code>LanguageCode</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/search_vocabularies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#search_vocabularies)
        """

    async def send_chat_integration_event(
        self, **kwargs: Unpack[SendChatIntegrationEventRequestRequestTypeDef]
    ) -> SendChatIntegrationEventResponseTypeDef:
        """
        Processes chat integration events from Amazon Web Services or external
        integrations to Amazon Connect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/send_chat_integration_event.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#send_chat_integration_event)
        """

    async def start_attached_file_upload(
        self, **kwargs: Unpack[StartAttachedFileUploadRequestRequestTypeDef]
    ) -> StartAttachedFileUploadResponseTypeDef:
        """
        Provides a pre-signed Amazon S3 URL in response for uploading your content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/start_attached_file_upload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#start_attached_file_upload)
        """

    async def start_chat_contact(
        self, **kwargs: Unpack[StartChatContactRequestRequestTypeDef]
    ) -> StartChatContactResponseTypeDef:
        """
        Initiates a flow to start a new chat for the customer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/start_chat_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#start_chat_contact)
        """

    async def start_contact_evaluation(
        self, **kwargs: Unpack[StartContactEvaluationRequestRequestTypeDef]
    ) -> StartContactEvaluationResponseTypeDef:
        """
        Starts an empty evaluation in the specified Amazon Connect instance, using the
        given evaluation form for the particular contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/start_contact_evaluation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#start_contact_evaluation)
        """

    async def start_contact_recording(
        self, **kwargs: Unpack[StartContactRecordingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts recording the contact:.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/start_contact_recording.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#start_contact_recording)
        """

    async def start_contact_streaming(
        self, **kwargs: Unpack[StartContactStreamingRequestRequestTypeDef]
    ) -> StartContactStreamingResponseTypeDef:
        """
        Initiates real-time message streaming for a new chat contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/start_contact_streaming.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#start_contact_streaming)
        """

    async def start_outbound_chat_contact(
        self, **kwargs: Unpack[StartOutboundChatContactRequestRequestTypeDef]
    ) -> StartOutboundChatContactResponseTypeDef:
        """
        Initiates a new outbound SMS contact to a customer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/start_outbound_chat_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#start_outbound_chat_contact)
        """

    async def start_outbound_voice_contact(
        self, **kwargs: Unpack[StartOutboundVoiceContactRequestRequestTypeDef]
    ) -> StartOutboundVoiceContactResponseTypeDef:
        """
        Places an outbound call to a contact, and then initiates the flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/start_outbound_voice_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#start_outbound_voice_contact)
        """

    async def start_task_contact(
        self, **kwargs: Unpack[StartTaskContactRequestRequestTypeDef]
    ) -> StartTaskContactResponseTypeDef:
        """
        Initiates a flow to start a new task contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/start_task_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#start_task_contact)
        """

    async def start_web_rtc_contact(
        self, **kwargs: Unpack[StartWebRTCContactRequestRequestTypeDef]
    ) -> StartWebRTCContactResponseTypeDef:
        """
        Places an inbound in-app, web, or video call to a contact, and then initiates
        the flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/start_web_rtc_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#start_web_rtc_contact)
        """

    async def stop_contact(
        self, **kwargs: Unpack[StopContactRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Ends the specified contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/stop_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#stop_contact)
        """

    async def stop_contact_recording(
        self, **kwargs: Unpack[StopContactRecordingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops recording a call when a contact is being recorded.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/stop_contact_recording.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#stop_contact_recording)
        """

    async def stop_contact_streaming(
        self, **kwargs: Unpack[StopContactStreamingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Ends message streaming on a specified contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/stop_contact_streaming.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#stop_contact_streaming)
        """

    async def submit_contact_evaluation(
        self, **kwargs: Unpack[SubmitContactEvaluationRequestRequestTypeDef]
    ) -> SubmitContactEvaluationResponseTypeDef:
        """
        Submits a contact evaluation in the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/submit_contact_evaluation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#submit_contact_evaluation)
        """

    async def suspend_contact_recording(
        self, **kwargs: Unpack[SuspendContactRecordingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        When a contact is being recorded, this API suspends recording whatever is
        selected in the flow configuration: call, screen, or both.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/suspend_contact_recording.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#suspend_contact_recording)
        """

    async def tag_contact(
        self, **kwargs: Unpack[TagContactRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds the specified tags to the contact resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/tag_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#tag_contact)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds the specified tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#tag_resource)
        """

    async def transfer_contact(
        self, **kwargs: Unpack[TransferContactRequestRequestTypeDef]
    ) -> TransferContactResponseTypeDef:
        """
        Transfers contacts from one agent or queue to another agent or queue at any
        point after a contact is created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/transfer_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#transfer_contact)
        """

    async def untag_contact(
        self, **kwargs: Unpack[UntagContactRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified tags from the contact resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/untag_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#untag_contact)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#untag_resource)
        """

    async def update_agent_status(
        self, **kwargs: Unpack[UpdateAgentStatusRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_agent_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_agent_status)
        """

    async def update_authentication_profile(
        self, **kwargs: Unpack[UpdateAuthenticationProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_authentication_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_authentication_profile)
        """

    async def update_contact(
        self, **kwargs: Unpack[UpdateContactRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_contact)
        """

    async def update_contact_attributes(
        self, **kwargs: Unpack[UpdateContactAttributesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates user-defined contact attributes associated with the
        specified contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_contact_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_contact_attributes)
        """

    async def update_contact_evaluation(
        self, **kwargs: Unpack[UpdateContactEvaluationRequestRequestTypeDef]
    ) -> UpdateContactEvaluationResponseTypeDef:
        """
        Updates details about a contact evaluation in the specified Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_contact_evaluation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_contact_evaluation)
        """

    async def update_contact_flow_content(
        self, **kwargs: Unpack[UpdateContactFlowContentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the specified flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_contact_flow_content.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_contact_flow_content)
        """

    async def update_contact_flow_metadata(
        self, **kwargs: Unpack[UpdateContactFlowMetadataRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates metadata about specified flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_contact_flow_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_contact_flow_metadata)
        """

    async def update_contact_flow_module_content(
        self, **kwargs: Unpack[UpdateContactFlowModuleContentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates specified flow module for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_contact_flow_module_content.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_contact_flow_module_content)
        """

    async def update_contact_flow_module_metadata(
        self, **kwargs: Unpack[UpdateContactFlowModuleMetadataRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates metadata about specified flow module.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_contact_flow_module_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_contact_flow_module_metadata)
        """

    async def update_contact_flow_name(
        self, **kwargs: Unpack[UpdateContactFlowNameRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        The name of the flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_contact_flow_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_contact_flow_name)
        """

    async def update_contact_routing_data(
        self, **kwargs: Unpack[UpdateContactRoutingDataRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates routing priority and age on the contact (<b>QueuePriority</b> and
        <b>QueueTimeAdjustmentInSeconds</b>).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_contact_routing_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_contact_routing_data)
        """

    async def update_contact_schedule(
        self, **kwargs: Unpack[UpdateContactScheduleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the scheduled time of a task contact that is already scheduled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_contact_schedule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_contact_schedule)
        """

    async def update_evaluation_form(
        self, **kwargs: Unpack[UpdateEvaluationFormRequestRequestTypeDef]
    ) -> UpdateEvaluationFormResponseTypeDef:
        """
        Updates details about a specific evaluation form version in the specified
        Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_evaluation_form.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_evaluation_form)
        """

    async def update_hours_of_operation(
        self, **kwargs: Unpack[UpdateHoursOfOperationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_hours_of_operation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_hours_of_operation)
        """

    async def update_instance_attribute(
        self, **kwargs: Unpack[UpdateInstanceAttributeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_instance_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_instance_attribute)
        """

    async def update_instance_storage_config(
        self, **kwargs: Unpack[UpdateInstanceStorageConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_instance_storage_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_instance_storage_config)
        """

    async def update_participant_role_config(
        self, **kwargs: Unpack[UpdateParticipantRoleConfigRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates timeouts for when human chat participants are to be considered idle,
        and when agents are automatically disconnected from a chat due to idleness.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_participant_role_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_participant_role_config)
        """

    async def update_phone_number(
        self, **kwargs: Unpack[UpdatePhoneNumberRequestRequestTypeDef]
    ) -> UpdatePhoneNumberResponseTypeDef:
        """
        Updates your claimed phone number from its current Amazon Connect instance or
        traffic distribution group to another Amazon Connect instance or traffic
        distribution group in the same Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_phone_number.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_phone_number)
        """

    async def update_phone_number_metadata(
        self, **kwargs: Unpack[UpdatePhoneNumberMetadataRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a phone number's metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_phone_number_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_phone_number_metadata)
        """

    async def update_predefined_attribute(
        self, **kwargs: Unpack[UpdatePredefinedAttributeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a predefined attribute for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_predefined_attribute.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_predefined_attribute)
        """

    async def update_prompt(
        self, **kwargs: Unpack[UpdatePromptRequestRequestTypeDef]
    ) -> UpdatePromptResponseTypeDef:
        """
        Updates a prompt.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_prompt.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_prompt)
        """

    async def update_queue_hours_of_operation(
        self, **kwargs: Unpack[UpdateQueueHoursOfOperationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_queue_hours_of_operation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_queue_hours_of_operation)
        """

    async def update_queue_max_contacts(
        self, **kwargs: Unpack[UpdateQueueMaxContactsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_queue_max_contacts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_queue_max_contacts)
        """

    async def update_queue_name(
        self, **kwargs: Unpack[UpdateQueueNameRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_queue_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_queue_name)
        """

    async def update_queue_outbound_caller_config(
        self, **kwargs: Unpack[UpdateQueueOutboundCallerConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_queue_outbound_caller_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_queue_outbound_caller_config)
        """

    async def update_queue_status(
        self, **kwargs: Unpack[UpdateQueueStatusRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This API is in preview release for Amazon Connect and is subject to change.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_queue_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_queue_status)
        """

    async def update_quick_connect_config(
        self, **kwargs: Unpack[UpdateQuickConnectConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the configuration settings for the specified quick connect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_quick_connect_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_quick_connect_config)
        """

    async def update_quick_connect_name(
        self, **kwargs: Unpack[UpdateQuickConnectNameRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the name and description of a quick connect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_quick_connect_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_quick_connect_name)
        """

    async def update_routing_profile_agent_availability_timer(
        self, **kwargs: Unpack[UpdateRoutingProfileAgentAvailabilityTimerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Whether agents with this routing profile will have their routing order
        calculated based on <i>time since their last inbound contact</i> or <i>longest
        idle time</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_routing_profile_agent_availability_timer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_routing_profile_agent_availability_timer)
        """

    async def update_routing_profile_concurrency(
        self, **kwargs: Unpack[UpdateRoutingProfileConcurrencyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the channels that agents can handle in the Contact Control Panel (CCP)
        for a routing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_routing_profile_concurrency.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_routing_profile_concurrency)
        """

    async def update_routing_profile_default_outbound_queue(
        self, **kwargs: Unpack[UpdateRoutingProfileDefaultOutboundQueueRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the default outbound queue of a routing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_routing_profile_default_outbound_queue.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_routing_profile_default_outbound_queue)
        """

    async def update_routing_profile_name(
        self, **kwargs: Unpack[UpdateRoutingProfileNameRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the name and description of a routing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_routing_profile_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_routing_profile_name)
        """

    async def update_routing_profile_queues(
        self, **kwargs: Unpack[UpdateRoutingProfileQueuesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the properties associated with a set of queues for a routing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_routing_profile_queues.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_routing_profile_queues)
        """

    async def update_rule(
        self, **kwargs: Unpack[UpdateRuleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a rule for the specified Amazon Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_rule)
        """

    async def update_security_profile(
        self, **kwargs: Unpack[UpdateSecurityProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_security_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_security_profile)
        """

    async def update_task_template(
        self, **kwargs: Unpack[UpdateTaskTemplateRequestRequestTypeDef]
    ) -> UpdateTaskTemplateResponseTypeDef:
        """
        Updates details about a specific task template in the specified Amazon Connect
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_task_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_task_template)
        """

    async def update_traffic_distribution(
        self, **kwargs: Unpack[UpdateTrafficDistributionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the traffic distribution for a given traffic distribution group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_traffic_distribution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_traffic_distribution)
        """

    async def update_user_hierarchy(
        self, **kwargs: Unpack[UpdateUserHierarchyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assigns the specified hierarchy group to the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_user_hierarchy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_user_hierarchy)
        """

    async def update_user_hierarchy_group_name(
        self, **kwargs: Unpack[UpdateUserHierarchyGroupNameRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the name of the user hierarchy group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_user_hierarchy_group_name.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_user_hierarchy_group_name)
        """

    async def update_user_hierarchy_structure(
        self, **kwargs: Unpack[UpdateUserHierarchyStructureRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the user hierarchy structure: add, remove, and rename user hierarchy
        levels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_user_hierarchy_structure.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_user_hierarchy_structure)
        """

    async def update_user_identity_info(
        self, **kwargs: Unpack[UpdateUserIdentityInfoRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the identity information for the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_user_identity_info.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_user_identity_info)
        """

    async def update_user_phone_config(
        self, **kwargs: Unpack[UpdateUserPhoneConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the phone configuration settings for the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_user_phone_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_user_phone_config)
        """

    async def update_user_proficiencies(
        self, **kwargs: Unpack[UpdateUserProficienciesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the properties associated with the proficiencies of a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_user_proficiencies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_user_proficiencies)
        """

    async def update_user_routing_profile(
        self, **kwargs: Unpack[UpdateUserRoutingProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assigns the specified routing profile to the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_user_routing_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_user_routing_profile)
        """

    async def update_user_security_profiles(
        self, **kwargs: Unpack[UpdateUserSecurityProfilesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assigns the specified security profiles to the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_user_security_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_user_security_profiles)
        """

    async def update_view_content(
        self, **kwargs: Unpack[UpdateViewContentRequestRequestTypeDef]
    ) -> UpdateViewContentResponseTypeDef:
        """
        Updates the view content of the given view identifier in the specified Amazon
        Connect instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_view_content.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_view_content)
        """

    async def update_view_metadata(
        self, **kwargs: Unpack[UpdateViewMetadataRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the view metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/update_view_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#update_view_metadata)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_metric_data"]) -> GetMetricDataPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_agent_statuses"]
    ) -> ListAgentStatusesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_approved_origins"]
    ) -> ListApprovedOriginsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_authentication_profiles"]
    ) -> ListAuthenticationProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_bots"]) -> ListBotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_contact_evaluations"]
    ) -> ListContactEvaluationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_contact_flow_modules"]
    ) -> ListContactFlowModulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_contact_flows"]
    ) -> ListContactFlowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_contact_references"]
    ) -> ListContactReferencesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_default_vocabularies"]
    ) -> ListDefaultVocabulariesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_evaluation_form_versions"]
    ) -> ListEvaluationFormVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_evaluation_forms"]
    ) -> ListEvaluationFormsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_flow_associations"]
    ) -> ListFlowAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_hours_of_operations"]
    ) -> ListHoursOfOperationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_instance_attributes"]
    ) -> ListInstanceAttributesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_instance_storage_configs"]
    ) -> ListInstanceStorageConfigsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_instances"]) -> ListInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_integration_associations"]
    ) -> ListIntegrationAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_lambda_functions"]
    ) -> ListLambdaFunctionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_lex_bots"]) -> ListLexBotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_phone_numbers"]
    ) -> ListPhoneNumbersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_phone_numbers_v2"]
    ) -> ListPhoneNumbersV2Paginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_predefined_attributes"]
    ) -> ListPredefinedAttributesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_prompts"]) -> ListPromptsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_queue_quick_connects"]
    ) -> ListQueueQuickConnectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_queues"]) -> ListQueuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_quick_connects"]
    ) -> ListQuickConnectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_routing_profile_queues"]
    ) -> ListRoutingProfileQueuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_routing_profiles"]
    ) -> ListRoutingProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_rules"]) -> ListRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_security_keys"]
    ) -> ListSecurityKeysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_security_profile_applications"]
    ) -> ListSecurityProfileApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_security_profile_permissions"]
    ) -> ListSecurityProfilePermissionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_security_profiles"]
    ) -> ListSecurityProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_task_templates"]
    ) -> ListTaskTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_traffic_distribution_group_users"]
    ) -> ListTrafficDistributionGroupUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_traffic_distribution_groups"]
    ) -> ListTrafficDistributionGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_use_cases"]) -> ListUseCasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_user_hierarchy_groups"]
    ) -> ListUserHierarchyGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_user_proficiencies"]
    ) -> ListUserProficienciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_view_versions"]
    ) -> ListViewVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_views"]) -> ListViewsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_agent_statuses"]
    ) -> SearchAgentStatusesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_available_phone_numbers"]
    ) -> SearchAvailablePhoneNumbersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_contact_flow_modules"]
    ) -> SearchContactFlowModulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_contact_flows"]
    ) -> SearchContactFlowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_contacts"]) -> SearchContactsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_hours_of_operations"]
    ) -> SearchHoursOfOperationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_predefined_attributes"]
    ) -> SearchPredefinedAttributesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_prompts"]) -> SearchPromptsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_queues"]) -> SearchQueuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_quick_connects"]
    ) -> SearchQuickConnectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_resource_tags"]
    ) -> SearchResourceTagsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_routing_profiles"]
    ) -> SearchRoutingProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_security_profiles"]
    ) -> SearchSecurityProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_user_hierarchy_groups"]
    ) -> SearchUserHierarchyGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_users"]) -> SearchUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_vocabularies"]
    ) -> SearchVocabulariesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/#get_paginator)
        """

    async def __aenter__(self) -> "ConnectClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/client/)
        """
