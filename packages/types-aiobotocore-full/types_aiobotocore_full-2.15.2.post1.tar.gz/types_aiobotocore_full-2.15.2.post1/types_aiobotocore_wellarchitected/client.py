"""
Type annotations for wellarchitected service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_wellarchitected.client import WellArchitectedClient

    session = get_session()
    async with session.create_client("wellarchitected") as client:
        client: WellArchitectedClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    AssociateLensesInputRequestTypeDef,
    AssociateProfilesInputRequestTypeDef,
    CreateLensShareInputRequestTypeDef,
    CreateLensShareOutputTypeDef,
    CreateLensVersionInputRequestTypeDef,
    CreateLensVersionOutputTypeDef,
    CreateMilestoneInputRequestTypeDef,
    CreateMilestoneOutputTypeDef,
    CreateProfileInputRequestTypeDef,
    CreateProfileOutputTypeDef,
    CreateProfileShareInputRequestTypeDef,
    CreateProfileShareOutputTypeDef,
    CreateReviewTemplateInputRequestTypeDef,
    CreateReviewTemplateOutputTypeDef,
    CreateTemplateShareInputRequestTypeDef,
    CreateTemplateShareOutputTypeDef,
    CreateWorkloadInputRequestTypeDef,
    CreateWorkloadOutputTypeDef,
    CreateWorkloadShareInputRequestTypeDef,
    CreateWorkloadShareOutputTypeDef,
    DeleteLensInputRequestTypeDef,
    DeleteLensShareInputRequestTypeDef,
    DeleteProfileInputRequestTypeDef,
    DeleteProfileShareInputRequestTypeDef,
    DeleteReviewTemplateInputRequestTypeDef,
    DeleteTemplateShareInputRequestTypeDef,
    DeleteWorkloadInputRequestTypeDef,
    DeleteWorkloadShareInputRequestTypeDef,
    DisassociateLensesInputRequestTypeDef,
    DisassociateProfilesInputRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportLensInputRequestTypeDef,
    ExportLensOutputTypeDef,
    GetAnswerInputRequestTypeDef,
    GetAnswerOutputTypeDef,
    GetConsolidatedReportInputRequestTypeDef,
    GetConsolidatedReportOutputTypeDef,
    GetGlobalSettingsOutputTypeDef,
    GetLensInputRequestTypeDef,
    GetLensOutputTypeDef,
    GetLensReviewInputRequestTypeDef,
    GetLensReviewOutputTypeDef,
    GetLensReviewReportInputRequestTypeDef,
    GetLensReviewReportOutputTypeDef,
    GetLensVersionDifferenceInputRequestTypeDef,
    GetLensVersionDifferenceOutputTypeDef,
    GetMilestoneInputRequestTypeDef,
    GetMilestoneOutputTypeDef,
    GetProfileInputRequestTypeDef,
    GetProfileOutputTypeDef,
    GetProfileTemplateOutputTypeDef,
    GetReviewTemplateAnswerInputRequestTypeDef,
    GetReviewTemplateAnswerOutputTypeDef,
    GetReviewTemplateInputRequestTypeDef,
    GetReviewTemplateLensReviewInputRequestTypeDef,
    GetReviewTemplateLensReviewOutputTypeDef,
    GetReviewTemplateOutputTypeDef,
    GetWorkloadInputRequestTypeDef,
    GetWorkloadOutputTypeDef,
    ImportLensInputRequestTypeDef,
    ImportLensOutputTypeDef,
    ListAnswersInputRequestTypeDef,
    ListAnswersOutputTypeDef,
    ListCheckDetailsInputRequestTypeDef,
    ListCheckDetailsOutputTypeDef,
    ListCheckSummariesInputRequestTypeDef,
    ListCheckSummariesOutputTypeDef,
    ListLensesInputRequestTypeDef,
    ListLensesOutputTypeDef,
    ListLensReviewImprovementsInputRequestTypeDef,
    ListLensReviewImprovementsOutputTypeDef,
    ListLensReviewsInputRequestTypeDef,
    ListLensReviewsOutputTypeDef,
    ListLensSharesInputRequestTypeDef,
    ListLensSharesOutputTypeDef,
    ListMilestonesInputRequestTypeDef,
    ListMilestonesOutputTypeDef,
    ListNotificationsInputRequestTypeDef,
    ListNotificationsOutputTypeDef,
    ListProfileNotificationsInputRequestTypeDef,
    ListProfileNotificationsOutputTypeDef,
    ListProfileSharesInputRequestTypeDef,
    ListProfileSharesOutputTypeDef,
    ListProfilesInputRequestTypeDef,
    ListProfilesOutputTypeDef,
    ListReviewTemplateAnswersInputRequestTypeDef,
    ListReviewTemplateAnswersOutputTypeDef,
    ListReviewTemplatesInputRequestTypeDef,
    ListReviewTemplatesOutputTypeDef,
    ListShareInvitationsInputRequestTypeDef,
    ListShareInvitationsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTemplateSharesInputRequestTypeDef,
    ListTemplateSharesOutputTypeDef,
    ListWorkloadSharesInputRequestTypeDef,
    ListWorkloadSharesOutputTypeDef,
    ListWorkloadsInputRequestTypeDef,
    ListWorkloadsOutputTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateAnswerInputRequestTypeDef,
    UpdateAnswerOutputTypeDef,
    UpdateGlobalSettingsInputRequestTypeDef,
    UpdateIntegrationInputRequestTypeDef,
    UpdateLensReviewInputRequestTypeDef,
    UpdateLensReviewOutputTypeDef,
    UpdateProfileInputRequestTypeDef,
    UpdateProfileOutputTypeDef,
    UpdateReviewTemplateAnswerInputRequestTypeDef,
    UpdateReviewTemplateAnswerOutputTypeDef,
    UpdateReviewTemplateInputRequestTypeDef,
    UpdateReviewTemplateLensReviewInputRequestTypeDef,
    UpdateReviewTemplateLensReviewOutputTypeDef,
    UpdateReviewTemplateOutputTypeDef,
    UpdateShareInvitationInputRequestTypeDef,
    UpdateShareInvitationOutputTypeDef,
    UpdateWorkloadInputRequestTypeDef,
    UpdateWorkloadOutputTypeDef,
    UpdateWorkloadShareInputRequestTypeDef,
    UpdateWorkloadShareOutputTypeDef,
    UpgradeLensReviewInputRequestTypeDef,
    UpgradeProfileVersionInputRequestTypeDef,
    UpgradeReviewTemplateLensReviewInputRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("WellArchitectedClient",)


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
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class WellArchitectedClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WellArchitectedClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#close)
        """

    async def associate_lenses(
        self, **kwargs: Unpack[AssociateLensesInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associate a lens to a workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/associate_lenses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#associate_lenses)
        """

    async def associate_profiles(
        self, **kwargs: Unpack[AssociateProfilesInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associate a profile with a workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/associate_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#associate_profiles)
        """

    async def create_lens_share(
        self, **kwargs: Unpack[CreateLensShareInputRequestTypeDef]
    ) -> CreateLensShareOutputTypeDef:
        """
        Create a lens share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/create_lens_share.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_lens_share)
        """

    async def create_lens_version(
        self, **kwargs: Unpack[CreateLensVersionInputRequestTypeDef]
    ) -> CreateLensVersionOutputTypeDef:
        """
        Create a new lens version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/create_lens_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_lens_version)
        """

    async def create_milestone(
        self, **kwargs: Unpack[CreateMilestoneInputRequestTypeDef]
    ) -> CreateMilestoneOutputTypeDef:
        """
        Create a milestone for an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/create_milestone.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_milestone)
        """

    async def create_profile(
        self, **kwargs: Unpack[CreateProfileInputRequestTypeDef]
    ) -> CreateProfileOutputTypeDef:
        """
        Create a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/create_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_profile)
        """

    async def create_profile_share(
        self, **kwargs: Unpack[CreateProfileShareInputRequestTypeDef]
    ) -> CreateProfileShareOutputTypeDef:
        """
        Create a profile share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/create_profile_share.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_profile_share)
        """

    async def create_review_template(
        self, **kwargs: Unpack[CreateReviewTemplateInputRequestTypeDef]
    ) -> CreateReviewTemplateOutputTypeDef:
        """
        Create a review template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/create_review_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_review_template)
        """

    async def create_template_share(
        self, **kwargs: Unpack[CreateTemplateShareInputRequestTypeDef]
    ) -> CreateTemplateShareOutputTypeDef:
        """
        Create a review template share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/create_template_share.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_template_share)
        """

    async def create_workload(
        self, **kwargs: Unpack[CreateWorkloadInputRequestTypeDef]
    ) -> CreateWorkloadOutputTypeDef:
        """
        Create a new workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/create_workload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_workload)
        """

    async def create_workload_share(
        self, **kwargs: Unpack[CreateWorkloadShareInputRequestTypeDef]
    ) -> CreateWorkloadShareOutputTypeDef:
        """
        Create a workload share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/create_workload_share.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#create_workload_share)
        """

    async def delete_lens(
        self, **kwargs: Unpack[DeleteLensInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete an existing lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/delete_lens.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#delete_lens)
        """

    async def delete_lens_share(
        self, **kwargs: Unpack[DeleteLensShareInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a lens share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/delete_lens_share.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#delete_lens_share)
        """

    async def delete_profile(
        self, **kwargs: Unpack[DeleteProfileInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/delete_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#delete_profile)
        """

    async def delete_profile_share(
        self, **kwargs: Unpack[DeleteProfileShareInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a profile share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/delete_profile_share.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#delete_profile_share)
        """

    async def delete_review_template(
        self, **kwargs: Unpack[DeleteReviewTemplateInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a review template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/delete_review_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#delete_review_template)
        """

    async def delete_template_share(
        self, **kwargs: Unpack[DeleteTemplateShareInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a review template share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/delete_template_share.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#delete_template_share)
        """

    async def delete_workload(
        self, **kwargs: Unpack[DeleteWorkloadInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/delete_workload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#delete_workload)
        """

    async def delete_workload_share(
        self, **kwargs: Unpack[DeleteWorkloadShareInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a workload share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/delete_workload_share.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#delete_workload_share)
        """

    async def disassociate_lenses(
        self, **kwargs: Unpack[DisassociateLensesInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociate a lens from a workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/disassociate_lenses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#disassociate_lenses)
        """

    async def disassociate_profiles(
        self, **kwargs: Unpack[DisassociateProfilesInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociate a profile from a workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/disassociate_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#disassociate_profiles)
        """

    async def export_lens(
        self, **kwargs: Unpack[ExportLensInputRequestTypeDef]
    ) -> ExportLensOutputTypeDef:
        """
        Export an existing lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/export_lens.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#export_lens)
        """

    async def get_answer(
        self, **kwargs: Unpack[GetAnswerInputRequestTypeDef]
    ) -> GetAnswerOutputTypeDef:
        """
        Get the answer to a specific question in a workload review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/get_answer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_answer)
        """

    async def get_consolidated_report(
        self, **kwargs: Unpack[GetConsolidatedReportInputRequestTypeDef]
    ) -> GetConsolidatedReportOutputTypeDef:
        """
        Get a consolidated report of your workloads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/get_consolidated_report.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_consolidated_report)
        """

    async def get_global_settings(self) -> GetGlobalSettingsOutputTypeDef:
        """
        Global settings for all workloads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/get_global_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_global_settings)
        """

    async def get_lens(self, **kwargs: Unpack[GetLensInputRequestTypeDef]) -> GetLensOutputTypeDef:
        """
        Get an existing lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/get_lens.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_lens)
        """

    async def get_lens_review(
        self, **kwargs: Unpack[GetLensReviewInputRequestTypeDef]
    ) -> GetLensReviewOutputTypeDef:
        """
        Get lens review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/get_lens_review.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_lens_review)
        """

    async def get_lens_review_report(
        self, **kwargs: Unpack[GetLensReviewReportInputRequestTypeDef]
    ) -> GetLensReviewReportOutputTypeDef:
        """
        Get lens review report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/get_lens_review_report.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_lens_review_report)
        """

    async def get_lens_version_difference(
        self, **kwargs: Unpack[GetLensVersionDifferenceInputRequestTypeDef]
    ) -> GetLensVersionDifferenceOutputTypeDef:
        """
        Get lens version differences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/get_lens_version_difference.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_lens_version_difference)
        """

    async def get_milestone(
        self, **kwargs: Unpack[GetMilestoneInputRequestTypeDef]
    ) -> GetMilestoneOutputTypeDef:
        """
        Get a milestone for an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/get_milestone.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_milestone)
        """

    async def get_profile(
        self, **kwargs: Unpack[GetProfileInputRequestTypeDef]
    ) -> GetProfileOutputTypeDef:
        """
        Get profile information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/get_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_profile)
        """

    async def get_profile_template(self) -> GetProfileTemplateOutputTypeDef:
        """
        Get profile template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/get_profile_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_profile_template)
        """

    async def get_review_template(
        self, **kwargs: Unpack[GetReviewTemplateInputRequestTypeDef]
    ) -> GetReviewTemplateOutputTypeDef:
        """
        Get review template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/get_review_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_review_template)
        """

    async def get_review_template_answer(
        self, **kwargs: Unpack[GetReviewTemplateAnswerInputRequestTypeDef]
    ) -> GetReviewTemplateAnswerOutputTypeDef:
        """
        Get review template answer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/get_review_template_answer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_review_template_answer)
        """

    async def get_review_template_lens_review(
        self, **kwargs: Unpack[GetReviewTemplateLensReviewInputRequestTypeDef]
    ) -> GetReviewTemplateLensReviewOutputTypeDef:
        """
        Get a lens review associated with a review template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/get_review_template_lens_review.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_review_template_lens_review)
        """

    async def get_workload(
        self, **kwargs: Unpack[GetWorkloadInputRequestTypeDef]
    ) -> GetWorkloadOutputTypeDef:
        """
        Get an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/get_workload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#get_workload)
        """

    async def import_lens(
        self, **kwargs: Unpack[ImportLensInputRequestTypeDef]
    ) -> ImportLensOutputTypeDef:
        """
        Import a new custom lens or update an existing custom lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/import_lens.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#import_lens)
        """

    async def list_answers(
        self, **kwargs: Unpack[ListAnswersInputRequestTypeDef]
    ) -> ListAnswersOutputTypeDef:
        """
        List of answers for a particular workload and lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_answers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_answers)
        """

    async def list_check_details(
        self, **kwargs: Unpack[ListCheckDetailsInputRequestTypeDef]
    ) -> ListCheckDetailsOutputTypeDef:
        """
        List of Trusted Advisor check details by account related to the workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_check_details.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_check_details)
        """

    async def list_check_summaries(
        self, **kwargs: Unpack[ListCheckSummariesInputRequestTypeDef]
    ) -> ListCheckSummariesOutputTypeDef:
        """
        List of Trusted Advisor checks summarized for all accounts related to the
        workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_check_summaries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_check_summaries)
        """

    async def list_lens_review_improvements(
        self, **kwargs: Unpack[ListLensReviewImprovementsInputRequestTypeDef]
    ) -> ListLensReviewImprovementsOutputTypeDef:
        """
        List the improvements of a particular lens review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_lens_review_improvements.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_lens_review_improvements)
        """

    async def list_lens_reviews(
        self, **kwargs: Unpack[ListLensReviewsInputRequestTypeDef]
    ) -> ListLensReviewsOutputTypeDef:
        """
        List lens reviews for a particular workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_lens_reviews.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_lens_reviews)
        """

    async def list_lens_shares(
        self, **kwargs: Unpack[ListLensSharesInputRequestTypeDef]
    ) -> ListLensSharesOutputTypeDef:
        """
        List the lens shares associated with the lens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_lens_shares.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_lens_shares)
        """

    async def list_lenses(
        self, **kwargs: Unpack[ListLensesInputRequestTypeDef]
    ) -> ListLensesOutputTypeDef:
        """
        List the available lenses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_lenses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_lenses)
        """

    async def list_milestones(
        self, **kwargs: Unpack[ListMilestonesInputRequestTypeDef]
    ) -> ListMilestonesOutputTypeDef:
        """
        List all milestones for an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_milestones.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_milestones)
        """

    async def list_notifications(
        self, **kwargs: Unpack[ListNotificationsInputRequestTypeDef]
    ) -> ListNotificationsOutputTypeDef:
        """
        List lens notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_notifications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_notifications)
        """

    async def list_profile_notifications(
        self, **kwargs: Unpack[ListProfileNotificationsInputRequestTypeDef]
    ) -> ListProfileNotificationsOutputTypeDef:
        """
        List profile notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_profile_notifications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_profile_notifications)
        """

    async def list_profile_shares(
        self, **kwargs: Unpack[ListProfileSharesInputRequestTypeDef]
    ) -> ListProfileSharesOutputTypeDef:
        """
        List profile shares.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_profile_shares.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_profile_shares)
        """

    async def list_profiles(
        self, **kwargs: Unpack[ListProfilesInputRequestTypeDef]
    ) -> ListProfilesOutputTypeDef:
        """
        List profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_profiles)
        """

    async def list_review_template_answers(
        self, **kwargs: Unpack[ListReviewTemplateAnswersInputRequestTypeDef]
    ) -> ListReviewTemplateAnswersOutputTypeDef:
        """
        List the answers of a review template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_review_template_answers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_review_template_answers)
        """

    async def list_review_templates(
        self, **kwargs: Unpack[ListReviewTemplatesInputRequestTypeDef]
    ) -> ListReviewTemplatesOutputTypeDef:
        """
        List review templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_review_templates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_review_templates)
        """

    async def list_share_invitations(
        self, **kwargs: Unpack[ListShareInvitationsInputRequestTypeDef]
    ) -> ListShareInvitationsOutputTypeDef:
        """
        List the share invitations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_share_invitations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_share_invitations)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        List the tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_tags_for_resource)
        """

    async def list_template_shares(
        self, **kwargs: Unpack[ListTemplateSharesInputRequestTypeDef]
    ) -> ListTemplateSharesOutputTypeDef:
        """
        List review template shares.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_template_shares.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_template_shares)
        """

    async def list_workload_shares(
        self, **kwargs: Unpack[ListWorkloadSharesInputRequestTypeDef]
    ) -> ListWorkloadSharesOutputTypeDef:
        """
        List the workload shares associated with the workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_workload_shares.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_workload_shares)
        """

    async def list_workloads(
        self, **kwargs: Unpack[ListWorkloadsInputRequestTypeDef]
    ) -> ListWorkloadsOutputTypeDef:
        """
        Paginated list of workloads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/list_workloads.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#list_workloads)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds one or more tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#untag_resource)
        """

    async def update_answer(
        self, **kwargs: Unpack[UpdateAnswerInputRequestTypeDef]
    ) -> UpdateAnswerOutputTypeDef:
        """
        Update the answer to a specific question in a workload review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/update_answer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_answer)
        """

    async def update_global_settings(
        self, **kwargs: Unpack[UpdateGlobalSettingsInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Update whether the Amazon Web Services account is opted into organization
        sharing and discovery integration features.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/update_global_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_global_settings)
        """

    async def update_integration(
        self, **kwargs: Unpack[UpdateIntegrationInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Update integration features.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/update_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_integration)
        """

    async def update_lens_review(
        self, **kwargs: Unpack[UpdateLensReviewInputRequestTypeDef]
    ) -> UpdateLensReviewOutputTypeDef:
        """
        Update lens review for a particular workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/update_lens_review.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_lens_review)
        """

    async def update_profile(
        self, **kwargs: Unpack[UpdateProfileInputRequestTypeDef]
    ) -> UpdateProfileOutputTypeDef:
        """
        Update a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/update_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_profile)
        """

    async def update_review_template(
        self, **kwargs: Unpack[UpdateReviewTemplateInputRequestTypeDef]
    ) -> UpdateReviewTemplateOutputTypeDef:
        """
        Update a review template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/update_review_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_review_template)
        """

    async def update_review_template_answer(
        self, **kwargs: Unpack[UpdateReviewTemplateAnswerInputRequestTypeDef]
    ) -> UpdateReviewTemplateAnswerOutputTypeDef:
        """
        Update a review template answer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/update_review_template_answer.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_review_template_answer)
        """

    async def update_review_template_lens_review(
        self, **kwargs: Unpack[UpdateReviewTemplateLensReviewInputRequestTypeDef]
    ) -> UpdateReviewTemplateLensReviewOutputTypeDef:
        """
        Update a lens review associated with a review template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/update_review_template_lens_review.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_review_template_lens_review)
        """

    async def update_share_invitation(
        self, **kwargs: Unpack[UpdateShareInvitationInputRequestTypeDef]
    ) -> UpdateShareInvitationOutputTypeDef:
        """
        Update a workload or custom lens share invitation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/update_share_invitation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_share_invitation)
        """

    async def update_workload(
        self, **kwargs: Unpack[UpdateWorkloadInputRequestTypeDef]
    ) -> UpdateWorkloadOutputTypeDef:
        """
        Update an existing workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/update_workload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_workload)
        """

    async def update_workload_share(
        self, **kwargs: Unpack[UpdateWorkloadShareInputRequestTypeDef]
    ) -> UpdateWorkloadShareOutputTypeDef:
        """
        Update a workload share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/update_workload_share.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#update_workload_share)
        """

    async def upgrade_lens_review(
        self, **kwargs: Unpack[UpgradeLensReviewInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Upgrade lens review for a particular workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/upgrade_lens_review.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#upgrade_lens_review)
        """

    async def upgrade_profile_version(
        self, **kwargs: Unpack[UpgradeProfileVersionInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Upgrade a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/upgrade_profile_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#upgrade_profile_version)
        """

    async def upgrade_review_template_lens_review(
        self, **kwargs: Unpack[UpgradeReviewTemplateLensReviewInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Upgrade the lens review of a review template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/client/upgrade_review_template_lens_review.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/#upgrade_review_template_lens_review)
        """

    async def __aenter__(self) -> "WellArchitectedClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected.html#WellArchitected.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/client/)
        """
