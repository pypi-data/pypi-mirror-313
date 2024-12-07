"""
Type annotations for compute-optimizer service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_compute_optimizer.client import ComputeOptimizerClient

    session = get_session()
    async with session.create_client("compute-optimizer") as client:
        client: ComputeOptimizerClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    DescribeRecommendationExportJobsPaginator,
    GetEnrollmentStatusesForOrganizationPaginator,
    GetLambdaFunctionRecommendationsPaginator,
    GetRecommendationPreferencesPaginator,
    GetRecommendationSummariesPaginator,
)
from .type_defs import (
    DeleteRecommendationPreferencesRequestRequestTypeDef,
    DescribeRecommendationExportJobsRequestRequestTypeDef,
    DescribeRecommendationExportJobsResponseTypeDef,
    ExportAutoScalingGroupRecommendationsRequestRequestTypeDef,
    ExportAutoScalingGroupRecommendationsResponseTypeDef,
    ExportEBSVolumeRecommendationsRequestRequestTypeDef,
    ExportEBSVolumeRecommendationsResponseTypeDef,
    ExportEC2InstanceRecommendationsRequestRequestTypeDef,
    ExportEC2InstanceRecommendationsResponseTypeDef,
    ExportECSServiceRecommendationsRequestRequestTypeDef,
    ExportECSServiceRecommendationsResponseTypeDef,
    ExportLambdaFunctionRecommendationsRequestRequestTypeDef,
    ExportLambdaFunctionRecommendationsResponseTypeDef,
    ExportLicenseRecommendationsRequestRequestTypeDef,
    ExportLicenseRecommendationsResponseTypeDef,
    ExportRDSDatabaseRecommendationsRequestRequestTypeDef,
    ExportRDSDatabaseRecommendationsResponseTypeDef,
    GetAutoScalingGroupRecommendationsRequestRequestTypeDef,
    GetAutoScalingGroupRecommendationsResponseTypeDef,
    GetEBSVolumeRecommendationsRequestRequestTypeDef,
    GetEBSVolumeRecommendationsResponseTypeDef,
    GetEC2InstanceRecommendationsRequestRequestTypeDef,
    GetEC2InstanceRecommendationsResponseTypeDef,
    GetEC2RecommendationProjectedMetricsRequestRequestTypeDef,
    GetEC2RecommendationProjectedMetricsResponseTypeDef,
    GetECSServiceRecommendationProjectedMetricsRequestRequestTypeDef,
    GetECSServiceRecommendationProjectedMetricsResponseTypeDef,
    GetECSServiceRecommendationsRequestRequestTypeDef,
    GetECSServiceRecommendationsResponseTypeDef,
    GetEffectiveRecommendationPreferencesRequestRequestTypeDef,
    GetEffectiveRecommendationPreferencesResponseTypeDef,
    GetEnrollmentStatusesForOrganizationRequestRequestTypeDef,
    GetEnrollmentStatusesForOrganizationResponseTypeDef,
    GetEnrollmentStatusResponseTypeDef,
    GetLambdaFunctionRecommendationsRequestRequestTypeDef,
    GetLambdaFunctionRecommendationsResponseTypeDef,
    GetLicenseRecommendationsRequestRequestTypeDef,
    GetLicenseRecommendationsResponseTypeDef,
    GetRDSDatabaseRecommendationProjectedMetricsRequestRequestTypeDef,
    GetRDSDatabaseRecommendationProjectedMetricsResponseTypeDef,
    GetRDSDatabaseRecommendationsRequestRequestTypeDef,
    GetRDSDatabaseRecommendationsResponseTypeDef,
    GetRecommendationPreferencesRequestRequestTypeDef,
    GetRecommendationPreferencesResponseTypeDef,
    GetRecommendationSummariesRequestRequestTypeDef,
    GetRecommendationSummariesResponseTypeDef,
    PutRecommendationPreferencesRequestRequestTypeDef,
    UpdateEnrollmentStatusRequestRequestTypeDef,
    UpdateEnrollmentStatusResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ComputeOptimizerClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MissingAuthenticationToken: Type[BotocoreClientError]
    OptInRequiredException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]

class ComputeOptimizerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ComputeOptimizerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#close)
        """

    async def delete_recommendation_preferences(
        self, **kwargs: Unpack[DeleteRecommendationPreferencesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a recommendation preference, such as enhanced infrastructure metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/delete_recommendation_preferences.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#delete_recommendation_preferences)
        """

    async def describe_recommendation_export_jobs(
        self, **kwargs: Unpack[DescribeRecommendationExportJobsRequestRequestTypeDef]
    ) -> DescribeRecommendationExportJobsResponseTypeDef:
        """
        Describes recommendation export jobs created in the last seven days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/describe_recommendation_export_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#describe_recommendation_export_jobs)
        """

    async def export_auto_scaling_group_recommendations(
        self, **kwargs: Unpack[ExportAutoScalingGroupRecommendationsRequestRequestTypeDef]
    ) -> ExportAutoScalingGroupRecommendationsResponseTypeDef:
        """
        Exports optimization recommendations for Auto Scaling groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/export_auto_scaling_group_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#export_auto_scaling_group_recommendations)
        """

    async def export_ebs_volume_recommendations(
        self, **kwargs: Unpack[ExportEBSVolumeRecommendationsRequestRequestTypeDef]
    ) -> ExportEBSVolumeRecommendationsResponseTypeDef:
        """
        Exports optimization recommendations for Amazon EBS volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/export_ebs_volume_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#export_ebs_volume_recommendations)
        """

    async def export_ec2_instance_recommendations(
        self, **kwargs: Unpack[ExportEC2InstanceRecommendationsRequestRequestTypeDef]
    ) -> ExportEC2InstanceRecommendationsResponseTypeDef:
        """
        Exports optimization recommendations for Amazon EC2 instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/export_ec2_instance_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#export_ec2_instance_recommendations)
        """

    async def export_ecs_service_recommendations(
        self, **kwargs: Unpack[ExportECSServiceRecommendationsRequestRequestTypeDef]
    ) -> ExportECSServiceRecommendationsResponseTypeDef:
        """
        Exports optimization recommendations for Amazon ECS services on Fargate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/export_ecs_service_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#export_ecs_service_recommendations)
        """

    async def export_lambda_function_recommendations(
        self, **kwargs: Unpack[ExportLambdaFunctionRecommendationsRequestRequestTypeDef]
    ) -> ExportLambdaFunctionRecommendationsResponseTypeDef:
        """
        Exports optimization recommendations for Lambda functions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/export_lambda_function_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#export_lambda_function_recommendations)
        """

    async def export_license_recommendations(
        self, **kwargs: Unpack[ExportLicenseRecommendationsRequestRequestTypeDef]
    ) -> ExportLicenseRecommendationsResponseTypeDef:
        """
        Export optimization recommendations for your licenses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/export_license_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#export_license_recommendations)
        """

    async def export_rds_database_recommendations(
        self, **kwargs: Unpack[ExportRDSDatabaseRecommendationsRequestRequestTypeDef]
    ) -> ExportRDSDatabaseRecommendationsResponseTypeDef:
        """
        Export optimization recommendations for your Amazon Relational Database Service
        (Amazon RDS).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/export_rds_database_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#export_rds_database_recommendations)
        """

    async def get_auto_scaling_group_recommendations(
        self, **kwargs: Unpack[GetAutoScalingGroupRecommendationsRequestRequestTypeDef]
    ) -> GetAutoScalingGroupRecommendationsResponseTypeDef:
        """
        Returns Auto Scaling group recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_auto_scaling_group_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_auto_scaling_group_recommendations)
        """

    async def get_ebs_volume_recommendations(
        self, **kwargs: Unpack[GetEBSVolumeRecommendationsRequestRequestTypeDef]
    ) -> GetEBSVolumeRecommendationsResponseTypeDef:
        """
        Returns Amazon Elastic Block Store (Amazon EBS) volume recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_ebs_volume_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_ebs_volume_recommendations)
        """

    async def get_ec2_instance_recommendations(
        self, **kwargs: Unpack[GetEC2InstanceRecommendationsRequestRequestTypeDef]
    ) -> GetEC2InstanceRecommendationsResponseTypeDef:
        """
        Returns Amazon EC2 instance recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_ec2_instance_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_ec2_instance_recommendations)
        """

    async def get_ec2_recommendation_projected_metrics(
        self, **kwargs: Unpack[GetEC2RecommendationProjectedMetricsRequestRequestTypeDef]
    ) -> GetEC2RecommendationProjectedMetricsResponseTypeDef:
        """
        Returns the projected utilization metrics of Amazon EC2 instance
        recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_ec2_recommendation_projected_metrics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_ec2_recommendation_projected_metrics)
        """

    async def get_ecs_service_recommendation_projected_metrics(
        self, **kwargs: Unpack[GetECSServiceRecommendationProjectedMetricsRequestRequestTypeDef]
    ) -> GetECSServiceRecommendationProjectedMetricsResponseTypeDef:
        """
        Returns the projected metrics of Amazon ECS service recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_ecs_service_recommendation_projected_metrics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_ecs_service_recommendation_projected_metrics)
        """

    async def get_ecs_service_recommendations(
        self, **kwargs: Unpack[GetECSServiceRecommendationsRequestRequestTypeDef]
    ) -> GetECSServiceRecommendationsResponseTypeDef:
        """
        Returns Amazon ECS service recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_ecs_service_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_ecs_service_recommendations)
        """

    async def get_effective_recommendation_preferences(
        self, **kwargs: Unpack[GetEffectiveRecommendationPreferencesRequestRequestTypeDef]
    ) -> GetEffectiveRecommendationPreferencesResponseTypeDef:
        """
        Returns the recommendation preferences that are in effect for a given resource,
        such as enhanced infrastructure metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_effective_recommendation_preferences.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_effective_recommendation_preferences)
        """

    async def get_enrollment_status(self) -> GetEnrollmentStatusResponseTypeDef:
        """
        Returns the enrollment (opt in) status of an account to the Compute Optimizer
        service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_enrollment_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_enrollment_status)
        """

    async def get_enrollment_statuses_for_organization(
        self, **kwargs: Unpack[GetEnrollmentStatusesForOrganizationRequestRequestTypeDef]
    ) -> GetEnrollmentStatusesForOrganizationResponseTypeDef:
        """
        Returns the Compute Optimizer enrollment (opt-in) status of organization member
        accounts, if your account is an organization management account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_enrollment_statuses_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_enrollment_statuses_for_organization)
        """

    async def get_lambda_function_recommendations(
        self, **kwargs: Unpack[GetLambdaFunctionRecommendationsRequestRequestTypeDef]
    ) -> GetLambdaFunctionRecommendationsResponseTypeDef:
        """
        Returns Lambda function recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_lambda_function_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_lambda_function_recommendations)
        """

    async def get_license_recommendations(
        self, **kwargs: Unpack[GetLicenseRecommendationsRequestRequestTypeDef]
    ) -> GetLicenseRecommendationsResponseTypeDef:
        """
        Returns license recommendations for Amazon EC2 instances that run on a specific
        license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_license_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_license_recommendations)
        """

    async def get_rds_database_recommendation_projected_metrics(
        self, **kwargs: Unpack[GetRDSDatabaseRecommendationProjectedMetricsRequestRequestTypeDef]
    ) -> GetRDSDatabaseRecommendationProjectedMetricsResponseTypeDef:
        """
        Returns the projected metrics of Amazon RDS recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_rds_database_recommendation_projected_metrics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_rds_database_recommendation_projected_metrics)
        """

    async def get_rds_database_recommendations(
        self, **kwargs: Unpack[GetRDSDatabaseRecommendationsRequestRequestTypeDef]
    ) -> GetRDSDatabaseRecommendationsResponseTypeDef:
        """
        Returns Amazon RDS recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_rds_database_recommendations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_rds_database_recommendations)
        """

    async def get_recommendation_preferences(
        self, **kwargs: Unpack[GetRecommendationPreferencesRequestRequestTypeDef]
    ) -> GetRecommendationPreferencesResponseTypeDef:
        """
        Returns existing recommendation preferences, such as enhanced infrastructure
        metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_recommendation_preferences.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_recommendation_preferences)
        """

    async def get_recommendation_summaries(
        self, **kwargs: Unpack[GetRecommendationSummariesRequestRequestTypeDef]
    ) -> GetRecommendationSummariesResponseTypeDef:
        """
        Returns the optimization findings for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_recommendation_summaries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_recommendation_summaries)
        """

    async def put_recommendation_preferences(
        self, **kwargs: Unpack[PutRecommendationPreferencesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a new recommendation preference or updates an existing recommendation
        preference, such as enhanced infrastructure metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/put_recommendation_preferences.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#put_recommendation_preferences)
        """

    async def update_enrollment_status(
        self, **kwargs: Unpack[UpdateEnrollmentStatusRequestRequestTypeDef]
    ) -> UpdateEnrollmentStatusResponseTypeDef:
        """
        Updates the enrollment (opt in and opt out) status of an account to the Compute
        Optimizer service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/update_enrollment_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#update_enrollment_status)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_recommendation_export_jobs"]
    ) -> DescribeRecommendationExportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_enrollment_statuses_for_organization"]
    ) -> GetEnrollmentStatusesForOrganizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_lambda_function_recommendations"]
    ) -> GetLambdaFunctionRecommendationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_recommendation_preferences"]
    ) -> GetRecommendationPreferencesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_recommendation_summaries"]
    ) -> GetRecommendationSummariesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/#get_paginator)
        """

    async def __aenter__(self) -> "ComputeOptimizerClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/client/)
        """
