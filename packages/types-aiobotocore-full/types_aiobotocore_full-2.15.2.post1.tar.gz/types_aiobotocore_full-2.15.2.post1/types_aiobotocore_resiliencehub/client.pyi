"""
Type annotations for resiliencehub service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_resiliencehub.client import ResilienceHubClient

    session = get_session()
    async with session.create_client("resiliencehub") as client:
        client: ResilienceHubClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListAppAssessmentResourceDriftsPaginator,
    ListResourceGroupingRecommendationsPaginator,
)
from .type_defs import (
    AcceptResourceGroupingRecommendationsRequestRequestTypeDef,
    AcceptResourceGroupingRecommendationsResponseTypeDef,
    AddDraftAppVersionResourceMappingsRequestRequestTypeDef,
    AddDraftAppVersionResourceMappingsResponseTypeDef,
    BatchUpdateRecommendationStatusRequestRequestTypeDef,
    BatchUpdateRecommendationStatusResponseTypeDef,
    CreateAppRequestRequestTypeDef,
    CreateAppResponseTypeDef,
    CreateAppVersionAppComponentRequestRequestTypeDef,
    CreateAppVersionAppComponentResponseTypeDef,
    CreateAppVersionResourceRequestRequestTypeDef,
    CreateAppVersionResourceResponseTypeDef,
    CreateRecommendationTemplateRequestRequestTypeDef,
    CreateRecommendationTemplateResponseTypeDef,
    CreateResiliencyPolicyRequestRequestTypeDef,
    CreateResiliencyPolicyResponseTypeDef,
    DeleteAppAssessmentRequestRequestTypeDef,
    DeleteAppAssessmentResponseTypeDef,
    DeleteAppInputSourceRequestRequestTypeDef,
    DeleteAppInputSourceResponseTypeDef,
    DeleteAppRequestRequestTypeDef,
    DeleteAppResponseTypeDef,
    DeleteAppVersionAppComponentRequestRequestTypeDef,
    DeleteAppVersionAppComponentResponseTypeDef,
    DeleteAppVersionResourceRequestRequestTypeDef,
    DeleteAppVersionResourceResponseTypeDef,
    DeleteRecommendationTemplateRequestRequestTypeDef,
    DeleteRecommendationTemplateResponseTypeDef,
    DeleteResiliencyPolicyRequestRequestTypeDef,
    DeleteResiliencyPolicyResponseTypeDef,
    DescribeAppAssessmentRequestRequestTypeDef,
    DescribeAppAssessmentResponseTypeDef,
    DescribeAppRequestRequestTypeDef,
    DescribeAppResponseTypeDef,
    DescribeAppVersionAppComponentRequestRequestTypeDef,
    DescribeAppVersionAppComponentResponseTypeDef,
    DescribeAppVersionRequestRequestTypeDef,
    DescribeAppVersionResourceRequestRequestTypeDef,
    DescribeAppVersionResourceResponseTypeDef,
    DescribeAppVersionResourcesResolutionStatusRequestRequestTypeDef,
    DescribeAppVersionResourcesResolutionStatusResponseTypeDef,
    DescribeAppVersionResponseTypeDef,
    DescribeAppVersionTemplateRequestRequestTypeDef,
    DescribeAppVersionTemplateResponseTypeDef,
    DescribeDraftAppVersionResourcesImportStatusRequestRequestTypeDef,
    DescribeDraftAppVersionResourcesImportStatusResponseTypeDef,
    DescribeResiliencyPolicyRequestRequestTypeDef,
    DescribeResiliencyPolicyResponseTypeDef,
    DescribeResourceGroupingRecommendationTaskRequestRequestTypeDef,
    DescribeResourceGroupingRecommendationTaskResponseTypeDef,
    ImportResourcesToDraftAppVersionRequestRequestTypeDef,
    ImportResourcesToDraftAppVersionResponseTypeDef,
    ListAlarmRecommendationsRequestRequestTypeDef,
    ListAlarmRecommendationsResponseTypeDef,
    ListAppAssessmentComplianceDriftsRequestRequestTypeDef,
    ListAppAssessmentComplianceDriftsResponseTypeDef,
    ListAppAssessmentResourceDriftsRequestRequestTypeDef,
    ListAppAssessmentResourceDriftsResponseTypeDef,
    ListAppAssessmentsRequestRequestTypeDef,
    ListAppAssessmentsResponseTypeDef,
    ListAppComponentCompliancesRequestRequestTypeDef,
    ListAppComponentCompliancesResponseTypeDef,
    ListAppComponentRecommendationsRequestRequestTypeDef,
    ListAppComponentRecommendationsResponseTypeDef,
    ListAppInputSourcesRequestRequestTypeDef,
    ListAppInputSourcesResponseTypeDef,
    ListAppsRequestRequestTypeDef,
    ListAppsResponseTypeDef,
    ListAppVersionAppComponentsRequestRequestTypeDef,
    ListAppVersionAppComponentsResponseTypeDef,
    ListAppVersionResourceMappingsRequestRequestTypeDef,
    ListAppVersionResourceMappingsResponseTypeDef,
    ListAppVersionResourcesRequestRequestTypeDef,
    ListAppVersionResourcesResponseTypeDef,
    ListAppVersionsRequestRequestTypeDef,
    ListAppVersionsResponseTypeDef,
    ListRecommendationTemplatesRequestRequestTypeDef,
    ListRecommendationTemplatesResponseTypeDef,
    ListResiliencyPoliciesRequestRequestTypeDef,
    ListResiliencyPoliciesResponseTypeDef,
    ListResourceGroupingRecommendationsRequestRequestTypeDef,
    ListResourceGroupingRecommendationsResponseTypeDef,
    ListSopRecommendationsRequestRequestTypeDef,
    ListSopRecommendationsResponseTypeDef,
    ListSuggestedResiliencyPoliciesRequestRequestTypeDef,
    ListSuggestedResiliencyPoliciesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTestRecommendationsRequestRequestTypeDef,
    ListTestRecommendationsResponseTypeDef,
    ListUnsupportedAppVersionResourcesRequestRequestTypeDef,
    ListUnsupportedAppVersionResourcesResponseTypeDef,
    PublishAppVersionRequestRequestTypeDef,
    PublishAppVersionResponseTypeDef,
    PutDraftAppVersionTemplateRequestRequestTypeDef,
    PutDraftAppVersionTemplateResponseTypeDef,
    RejectResourceGroupingRecommendationsRequestRequestTypeDef,
    RejectResourceGroupingRecommendationsResponseTypeDef,
    RemoveDraftAppVersionResourceMappingsRequestRequestTypeDef,
    RemoveDraftAppVersionResourceMappingsResponseTypeDef,
    ResolveAppVersionResourcesRequestRequestTypeDef,
    ResolveAppVersionResourcesResponseTypeDef,
    StartAppAssessmentRequestRequestTypeDef,
    StartAppAssessmentResponseTypeDef,
    StartResourceGroupingRecommendationTaskRequestRequestTypeDef,
    StartResourceGroupingRecommendationTaskResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAppRequestRequestTypeDef,
    UpdateAppResponseTypeDef,
    UpdateAppVersionAppComponentRequestRequestTypeDef,
    UpdateAppVersionAppComponentResponseTypeDef,
    UpdateAppVersionRequestRequestTypeDef,
    UpdateAppVersionResourceRequestRequestTypeDef,
    UpdateAppVersionResourceResponseTypeDef,
    UpdateAppVersionResponseTypeDef,
    UpdateResiliencyPolicyRequestRequestTypeDef,
    UpdateResiliencyPolicyResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ResilienceHubClient",)

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

class ResilienceHubClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ResilienceHubClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#close)
        """

    async def accept_resource_grouping_recommendations(
        self, **kwargs: Unpack[AcceptResourceGroupingRecommendationsRequestRequestTypeDef]
    ) -> AcceptResourceGroupingRecommendationsResponseTypeDef:
        """
        Accepts the resource grouping recommendations suggested by Resilience Hub for
        your application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/accept_resource_grouping_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#accept_resource_grouping_recommendations)
        """

    async def add_draft_app_version_resource_mappings(
        self, **kwargs: Unpack[AddDraftAppVersionResourceMappingsRequestRequestTypeDef]
    ) -> AddDraftAppVersionResourceMappingsResponseTypeDef:
        """
        Adds the source of resource-maps to the draft version of an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/add_draft_app_version_resource_mappings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#add_draft_app_version_resource_mappings)
        """

    async def batch_update_recommendation_status(
        self, **kwargs: Unpack[BatchUpdateRecommendationStatusRequestRequestTypeDef]
    ) -> BatchUpdateRecommendationStatusResponseTypeDef:
        """
        Enables you to include or exclude one or more operational recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/batch_update_recommendation_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#batch_update_recommendation_status)
        """

    async def create_app(
        self, **kwargs: Unpack[CreateAppRequestRequestTypeDef]
    ) -> CreateAppResponseTypeDef:
        """
        Creates an Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/create_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#create_app)
        """

    async def create_app_version_app_component(
        self, **kwargs: Unpack[CreateAppVersionAppComponentRequestRequestTypeDef]
    ) -> CreateAppVersionAppComponentResponseTypeDef:
        """
        Creates a new Application Component in the Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/create_app_version_app_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#create_app_version_app_component)
        """

    async def create_app_version_resource(
        self, **kwargs: Unpack[CreateAppVersionResourceRequestRequestTypeDef]
    ) -> CreateAppVersionResourceResponseTypeDef:
        """
        Adds a resource to the Resilience Hub application and assigns it to the
        specified Application Components.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/create_app_version_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#create_app_version_resource)
        """

    async def create_recommendation_template(
        self, **kwargs: Unpack[CreateRecommendationTemplateRequestRequestTypeDef]
    ) -> CreateRecommendationTemplateResponseTypeDef:
        """
        Creates a new recommendation template for the Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/create_recommendation_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#create_recommendation_template)
        """

    async def create_resiliency_policy(
        self, **kwargs: Unpack[CreateResiliencyPolicyRequestRequestTypeDef]
    ) -> CreateResiliencyPolicyResponseTypeDef:
        """
        Creates a resiliency policy for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/create_resiliency_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#create_resiliency_policy)
        """

    async def delete_app(
        self, **kwargs: Unpack[DeleteAppRequestRequestTypeDef]
    ) -> DeleteAppResponseTypeDef:
        """
        Deletes an Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/delete_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#delete_app)
        """

    async def delete_app_assessment(
        self, **kwargs: Unpack[DeleteAppAssessmentRequestRequestTypeDef]
    ) -> DeleteAppAssessmentResponseTypeDef:
        """
        Deletes an Resilience Hub application assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/delete_app_assessment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#delete_app_assessment)
        """

    async def delete_app_input_source(
        self, **kwargs: Unpack[DeleteAppInputSourceRequestRequestTypeDef]
    ) -> DeleteAppInputSourceResponseTypeDef:
        """
        Deletes the input source and all of its imported resources from the Resilience
        Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/delete_app_input_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#delete_app_input_source)
        """

    async def delete_app_version_app_component(
        self, **kwargs: Unpack[DeleteAppVersionAppComponentRequestRequestTypeDef]
    ) -> DeleteAppVersionAppComponentResponseTypeDef:
        """
        Deletes an Application Component from the Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/delete_app_version_app_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#delete_app_version_app_component)
        """

    async def delete_app_version_resource(
        self, **kwargs: Unpack[DeleteAppVersionResourceRequestRequestTypeDef]
    ) -> DeleteAppVersionResourceResponseTypeDef:
        """
        Deletes a resource from the Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/delete_app_version_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#delete_app_version_resource)
        """

    async def delete_recommendation_template(
        self, **kwargs: Unpack[DeleteRecommendationTemplateRequestRequestTypeDef]
    ) -> DeleteRecommendationTemplateResponseTypeDef:
        """
        Deletes a recommendation template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/delete_recommendation_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#delete_recommendation_template)
        """

    async def delete_resiliency_policy(
        self, **kwargs: Unpack[DeleteResiliencyPolicyRequestRequestTypeDef]
    ) -> DeleteResiliencyPolicyResponseTypeDef:
        """
        Deletes a resiliency policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/delete_resiliency_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#delete_resiliency_policy)
        """

    async def describe_app(
        self, **kwargs: Unpack[DescribeAppRequestRequestTypeDef]
    ) -> DescribeAppResponseTypeDef:
        """
        Describes an Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/describe_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#describe_app)
        """

    async def describe_app_assessment(
        self, **kwargs: Unpack[DescribeAppAssessmentRequestRequestTypeDef]
    ) -> DescribeAppAssessmentResponseTypeDef:
        """
        Describes an assessment for an Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/describe_app_assessment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#describe_app_assessment)
        """

    async def describe_app_version(
        self, **kwargs: Unpack[DescribeAppVersionRequestRequestTypeDef]
    ) -> DescribeAppVersionResponseTypeDef:
        """
        Describes the Resilience Hub application version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/describe_app_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#describe_app_version)
        """

    async def describe_app_version_app_component(
        self, **kwargs: Unpack[DescribeAppVersionAppComponentRequestRequestTypeDef]
    ) -> DescribeAppVersionAppComponentResponseTypeDef:
        """
        Describes an Application Component in the Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/describe_app_version_app_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#describe_app_version_app_component)
        """

    async def describe_app_version_resource(
        self, **kwargs: Unpack[DescribeAppVersionResourceRequestRequestTypeDef]
    ) -> DescribeAppVersionResourceResponseTypeDef:
        """
        Describes a resource of the Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/describe_app_version_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#describe_app_version_resource)
        """

    async def describe_app_version_resources_resolution_status(
        self, **kwargs: Unpack[DescribeAppVersionResourcesResolutionStatusRequestRequestTypeDef]
    ) -> DescribeAppVersionResourcesResolutionStatusResponseTypeDef:
        """
        Returns the resolution status for the specified resolution identifier for an
        application version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/describe_app_version_resources_resolution_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#describe_app_version_resources_resolution_status)
        """

    async def describe_app_version_template(
        self, **kwargs: Unpack[DescribeAppVersionTemplateRequestRequestTypeDef]
    ) -> DescribeAppVersionTemplateResponseTypeDef:
        """
        Describes details about an Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/describe_app_version_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#describe_app_version_template)
        """

    async def describe_draft_app_version_resources_import_status(
        self, **kwargs: Unpack[DescribeDraftAppVersionResourcesImportStatusRequestRequestTypeDef]
    ) -> DescribeDraftAppVersionResourcesImportStatusResponseTypeDef:
        """
        Describes the status of importing resources to an application version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/describe_draft_app_version_resources_import_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#describe_draft_app_version_resources_import_status)
        """

    async def describe_resiliency_policy(
        self, **kwargs: Unpack[DescribeResiliencyPolicyRequestRequestTypeDef]
    ) -> DescribeResiliencyPolicyResponseTypeDef:
        """
        Describes a specified resiliency policy for an Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/describe_resiliency_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#describe_resiliency_policy)
        """

    async def describe_resource_grouping_recommendation_task(
        self, **kwargs: Unpack[DescribeResourceGroupingRecommendationTaskRequestRequestTypeDef]
    ) -> DescribeResourceGroupingRecommendationTaskResponseTypeDef:
        """
        Describes the resource grouping recommendation tasks run by Resilience Hub for
        your application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/describe_resource_grouping_recommendation_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#describe_resource_grouping_recommendation_task)
        """

    async def import_resources_to_draft_app_version(
        self, **kwargs: Unpack[ImportResourcesToDraftAppVersionRequestRequestTypeDef]
    ) -> ImportResourcesToDraftAppVersionResponseTypeDef:
        """
        Imports resources to Resilience Hub application draft version from different
        input sources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/import_resources_to_draft_app_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#import_resources_to_draft_app_version)
        """

    async def list_alarm_recommendations(
        self, **kwargs: Unpack[ListAlarmRecommendationsRequestRequestTypeDef]
    ) -> ListAlarmRecommendationsResponseTypeDef:
        """
        Lists the alarm recommendations for an Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_alarm_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_alarm_recommendations)
        """

    async def list_app_assessment_compliance_drifts(
        self, **kwargs: Unpack[ListAppAssessmentComplianceDriftsRequestRequestTypeDef]
    ) -> ListAppAssessmentComplianceDriftsResponseTypeDef:
        """
        List of compliance drifts that were detected while running an assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_app_assessment_compliance_drifts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_app_assessment_compliance_drifts)
        """

    async def list_app_assessment_resource_drifts(
        self, **kwargs: Unpack[ListAppAssessmentResourceDriftsRequestRequestTypeDef]
    ) -> ListAppAssessmentResourceDriftsResponseTypeDef:
        """
        Indicates the list of resource drifts that were detected while running an
        assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_app_assessment_resource_drifts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_app_assessment_resource_drifts)
        """

    async def list_app_assessments(
        self, **kwargs: Unpack[ListAppAssessmentsRequestRequestTypeDef]
    ) -> ListAppAssessmentsResponseTypeDef:
        """
        Lists the assessments for an Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_app_assessments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_app_assessments)
        """

    async def list_app_component_compliances(
        self, **kwargs: Unpack[ListAppComponentCompliancesRequestRequestTypeDef]
    ) -> ListAppComponentCompliancesResponseTypeDef:
        """
        Lists the compliances for an Resilience Hub Application Component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_app_component_compliances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_app_component_compliances)
        """

    async def list_app_component_recommendations(
        self, **kwargs: Unpack[ListAppComponentRecommendationsRequestRequestTypeDef]
    ) -> ListAppComponentRecommendationsResponseTypeDef:
        """
        Lists the recommendations for an Resilience Hub Application Component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_app_component_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_app_component_recommendations)
        """

    async def list_app_input_sources(
        self, **kwargs: Unpack[ListAppInputSourcesRequestRequestTypeDef]
    ) -> ListAppInputSourcesResponseTypeDef:
        """
        Lists all the input sources of the Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_app_input_sources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_app_input_sources)
        """

    async def list_app_version_app_components(
        self, **kwargs: Unpack[ListAppVersionAppComponentsRequestRequestTypeDef]
    ) -> ListAppVersionAppComponentsResponseTypeDef:
        """
        Lists all the Application Components in the Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_app_version_app_components.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_app_version_app_components)
        """

    async def list_app_version_resource_mappings(
        self, **kwargs: Unpack[ListAppVersionResourceMappingsRequestRequestTypeDef]
    ) -> ListAppVersionResourceMappingsResponseTypeDef:
        """
        Lists how the resources in an application version are mapped/sourced from.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_app_version_resource_mappings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_app_version_resource_mappings)
        """

    async def list_app_version_resources(
        self, **kwargs: Unpack[ListAppVersionResourcesRequestRequestTypeDef]
    ) -> ListAppVersionResourcesResponseTypeDef:
        """
        Lists all the resources in an Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_app_version_resources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_app_version_resources)
        """

    async def list_app_versions(
        self, **kwargs: Unpack[ListAppVersionsRequestRequestTypeDef]
    ) -> ListAppVersionsResponseTypeDef:
        """
        Lists the different versions for the Resilience Hub applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_app_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_app_versions)
        """

    async def list_apps(
        self, **kwargs: Unpack[ListAppsRequestRequestTypeDef]
    ) -> ListAppsResponseTypeDef:
        """
        Lists your Resilience Hub applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_apps.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_apps)
        """

    async def list_recommendation_templates(
        self, **kwargs: Unpack[ListRecommendationTemplatesRequestRequestTypeDef]
    ) -> ListRecommendationTemplatesResponseTypeDef:
        """
        Lists the recommendation templates for the Resilience Hub applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_recommendation_templates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_recommendation_templates)
        """

    async def list_resiliency_policies(
        self, **kwargs: Unpack[ListResiliencyPoliciesRequestRequestTypeDef]
    ) -> ListResiliencyPoliciesResponseTypeDef:
        """
        Lists the resiliency policies for the Resilience Hub applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_resiliency_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_resiliency_policies)
        """

    async def list_resource_grouping_recommendations(
        self, **kwargs: Unpack[ListResourceGroupingRecommendationsRequestRequestTypeDef]
    ) -> ListResourceGroupingRecommendationsResponseTypeDef:
        """
        Lists the resource grouping recommendations suggested by Resilience Hub for
        your application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_resource_grouping_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_resource_grouping_recommendations)
        """

    async def list_sop_recommendations(
        self, **kwargs: Unpack[ListSopRecommendationsRequestRequestTypeDef]
    ) -> ListSopRecommendationsResponseTypeDef:
        """
        Lists the standard operating procedure (SOP) recommendations for the Resilience
        Hub applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_sop_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_sop_recommendations)
        """

    async def list_suggested_resiliency_policies(
        self, **kwargs: Unpack[ListSuggestedResiliencyPoliciesRequestRequestTypeDef]
    ) -> ListSuggestedResiliencyPoliciesResponseTypeDef:
        """
        Lists the suggested resiliency policies for the Resilience Hub applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_suggested_resiliency_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_suggested_resiliency_policies)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for your resources in your Resilience Hub applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_tags_for_resource)
        """

    async def list_test_recommendations(
        self, **kwargs: Unpack[ListTestRecommendationsRequestRequestTypeDef]
    ) -> ListTestRecommendationsResponseTypeDef:
        """
        Lists the test recommendations for the Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_test_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_test_recommendations)
        """

    async def list_unsupported_app_version_resources(
        self, **kwargs: Unpack[ListUnsupportedAppVersionResourcesRequestRequestTypeDef]
    ) -> ListUnsupportedAppVersionResourcesResponseTypeDef:
        """
        Lists the resources that are not currently supported in Resilience Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/list_unsupported_app_version_resources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#list_unsupported_app_version_resources)
        """

    async def publish_app_version(
        self, **kwargs: Unpack[PublishAppVersionRequestRequestTypeDef]
    ) -> PublishAppVersionResponseTypeDef:
        """
        Publishes a new version of a specific Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/publish_app_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#publish_app_version)
        """

    async def put_draft_app_version_template(
        self, **kwargs: Unpack[PutDraftAppVersionTemplateRequestRequestTypeDef]
    ) -> PutDraftAppVersionTemplateResponseTypeDef:
        """
        Adds or updates the app template for an Resilience Hub application draft
        version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/put_draft_app_version_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#put_draft_app_version_template)
        """

    async def reject_resource_grouping_recommendations(
        self, **kwargs: Unpack[RejectResourceGroupingRecommendationsRequestRequestTypeDef]
    ) -> RejectResourceGroupingRecommendationsResponseTypeDef:
        """
        Rejects resource grouping recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/reject_resource_grouping_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#reject_resource_grouping_recommendations)
        """

    async def remove_draft_app_version_resource_mappings(
        self, **kwargs: Unpack[RemoveDraftAppVersionResourceMappingsRequestRequestTypeDef]
    ) -> RemoveDraftAppVersionResourceMappingsResponseTypeDef:
        """
        Removes resource mappings from a draft application version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/remove_draft_app_version_resource_mappings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#remove_draft_app_version_resource_mappings)
        """

    async def resolve_app_version_resources(
        self, **kwargs: Unpack[ResolveAppVersionResourcesRequestRequestTypeDef]
    ) -> ResolveAppVersionResourcesResponseTypeDef:
        """
        Resolves the resources for an application version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/resolve_app_version_resources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#resolve_app_version_resources)
        """

    async def start_app_assessment(
        self, **kwargs: Unpack[StartAppAssessmentRequestRequestTypeDef]
    ) -> StartAppAssessmentResponseTypeDef:
        """
        Creates a new application assessment for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/start_app_assessment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#start_app_assessment)
        """

    async def start_resource_grouping_recommendation_task(
        self, **kwargs: Unpack[StartResourceGroupingRecommendationTaskRequestRequestTypeDef]
    ) -> StartResourceGroupingRecommendationTaskResponseTypeDef:
        """
        Starts grouping recommendation task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/start_resource_grouping_recommendation_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#start_resource_grouping_recommendation_task)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Applies one or more tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#untag_resource)
        """

    async def update_app(
        self, **kwargs: Unpack[UpdateAppRequestRequestTypeDef]
    ) -> UpdateAppResponseTypeDef:
        """
        Updates an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/update_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#update_app)
        """

    async def update_app_version(
        self, **kwargs: Unpack[UpdateAppVersionRequestRequestTypeDef]
    ) -> UpdateAppVersionResponseTypeDef:
        """
        Updates the Resilience Hub application version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/update_app_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#update_app_version)
        """

    async def update_app_version_app_component(
        self, **kwargs: Unpack[UpdateAppVersionAppComponentRequestRequestTypeDef]
    ) -> UpdateAppVersionAppComponentResponseTypeDef:
        """
        Updates an existing Application Component in the Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/update_app_version_app_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#update_app_version_app_component)
        """

    async def update_app_version_resource(
        self, **kwargs: Unpack[UpdateAppVersionResourceRequestRequestTypeDef]
    ) -> UpdateAppVersionResourceResponseTypeDef:
        """
        Updates the resource details in the Resilience Hub application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/update_app_version_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#update_app_version_resource)
        """

    async def update_resiliency_policy(
        self, **kwargs: Unpack[UpdateResiliencyPolicyRequestRequestTypeDef]
    ) -> UpdateResiliencyPolicyResponseTypeDef:
        """
        Updates a resiliency policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/update_resiliency_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#update_resiliency_policy)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_app_assessment_resource_drifts"]
    ) -> ListAppAssessmentResourceDriftsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_grouping_recommendations"]
    ) -> ListResourceGroupingRecommendationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/#get_paginator)
        """

    async def __aenter__(self) -> "ResilienceHubClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehub.html#ResilienceHub.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehub/client/)
        """
