"""
Type annotations for sagemaker service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sagemaker.client import SageMakerClient
    from types_aiobotocore_sagemaker.paginator import (
        ListActionsPaginator,
        ListAlgorithmsPaginator,
        ListAliasesPaginator,
        ListAppImageConfigsPaginator,
        ListAppsPaginator,
        ListArtifactsPaginator,
        ListAssociationsPaginator,
        ListAutoMLJobsPaginator,
        ListCandidatesForAutoMLJobPaginator,
        ListClusterNodesPaginator,
        ListClustersPaginator,
        ListCodeRepositoriesPaginator,
        ListCompilationJobsPaginator,
        ListContextsPaginator,
        ListDataQualityJobDefinitionsPaginator,
        ListDeviceFleetsPaginator,
        ListDevicesPaginator,
        ListDomainsPaginator,
        ListEdgeDeploymentPlansPaginator,
        ListEdgePackagingJobsPaginator,
        ListEndpointConfigsPaginator,
        ListEndpointsPaginator,
        ListExperimentsPaginator,
        ListFeatureGroupsPaginator,
        ListFlowDefinitionsPaginator,
        ListHumanTaskUisPaginator,
        ListHyperParameterTuningJobsPaginator,
        ListImageVersionsPaginator,
        ListImagesPaginator,
        ListInferenceComponentsPaginator,
        ListInferenceExperimentsPaginator,
        ListInferenceRecommendationsJobStepsPaginator,
        ListInferenceRecommendationsJobsPaginator,
        ListLabelingJobsForWorkteamPaginator,
        ListLabelingJobsPaginator,
        ListLineageGroupsPaginator,
        ListMlflowTrackingServersPaginator,
        ListModelBiasJobDefinitionsPaginator,
        ListModelCardExportJobsPaginator,
        ListModelCardVersionsPaginator,
        ListModelCardsPaginator,
        ListModelExplainabilityJobDefinitionsPaginator,
        ListModelMetadataPaginator,
        ListModelPackageGroupsPaginator,
        ListModelPackagesPaginator,
        ListModelQualityJobDefinitionsPaginator,
        ListModelsPaginator,
        ListMonitoringAlertHistoryPaginator,
        ListMonitoringAlertsPaginator,
        ListMonitoringExecutionsPaginator,
        ListMonitoringSchedulesPaginator,
        ListNotebookInstanceLifecycleConfigsPaginator,
        ListNotebookInstancesPaginator,
        ListOptimizationJobsPaginator,
        ListPipelineExecutionStepsPaginator,
        ListPipelineExecutionsPaginator,
        ListPipelineParametersForExecutionPaginator,
        ListPipelinesPaginator,
        ListProcessingJobsPaginator,
        ListResourceCatalogsPaginator,
        ListSpacesPaginator,
        ListStageDevicesPaginator,
        ListStudioLifecycleConfigsPaginator,
        ListSubscribedWorkteamsPaginator,
        ListTagsPaginator,
        ListTrainingJobsForHyperParameterTuningJobPaginator,
        ListTrainingJobsPaginator,
        ListTransformJobsPaginator,
        ListTrialComponentsPaginator,
        ListTrialsPaginator,
        ListUserProfilesPaginator,
        ListWorkforcesPaginator,
        ListWorkteamsPaginator,
        SearchPaginator,
    )

    session = get_session()
    with session.create_client("sagemaker") as client:
        client: SageMakerClient

        list_actions_paginator: ListActionsPaginator = client.get_paginator("list_actions")
        list_algorithms_paginator: ListAlgorithmsPaginator = client.get_paginator("list_algorithms")
        list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
        list_app_image_configs_paginator: ListAppImageConfigsPaginator = client.get_paginator("list_app_image_configs")
        list_apps_paginator: ListAppsPaginator = client.get_paginator("list_apps")
        list_artifacts_paginator: ListArtifactsPaginator = client.get_paginator("list_artifacts")
        list_associations_paginator: ListAssociationsPaginator = client.get_paginator("list_associations")
        list_auto_ml_jobs_paginator: ListAutoMLJobsPaginator = client.get_paginator("list_auto_ml_jobs")
        list_candidates_for_auto_ml_job_paginator: ListCandidatesForAutoMLJobPaginator = client.get_paginator("list_candidates_for_auto_ml_job")
        list_cluster_nodes_paginator: ListClusterNodesPaginator = client.get_paginator("list_cluster_nodes")
        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
        list_code_repositories_paginator: ListCodeRepositoriesPaginator = client.get_paginator("list_code_repositories")
        list_compilation_jobs_paginator: ListCompilationJobsPaginator = client.get_paginator("list_compilation_jobs")
        list_contexts_paginator: ListContextsPaginator = client.get_paginator("list_contexts")
        list_data_quality_job_definitions_paginator: ListDataQualityJobDefinitionsPaginator = client.get_paginator("list_data_quality_job_definitions")
        list_device_fleets_paginator: ListDeviceFleetsPaginator = client.get_paginator("list_device_fleets")
        list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_edge_deployment_plans_paginator: ListEdgeDeploymentPlansPaginator = client.get_paginator("list_edge_deployment_plans")
        list_edge_packaging_jobs_paginator: ListEdgePackagingJobsPaginator = client.get_paginator("list_edge_packaging_jobs")
        list_endpoint_configs_paginator: ListEndpointConfigsPaginator = client.get_paginator("list_endpoint_configs")
        list_endpoints_paginator: ListEndpointsPaginator = client.get_paginator("list_endpoints")
        list_experiments_paginator: ListExperimentsPaginator = client.get_paginator("list_experiments")
        list_feature_groups_paginator: ListFeatureGroupsPaginator = client.get_paginator("list_feature_groups")
        list_flow_definitions_paginator: ListFlowDefinitionsPaginator = client.get_paginator("list_flow_definitions")
        list_human_task_uis_paginator: ListHumanTaskUisPaginator = client.get_paginator("list_human_task_uis")
        list_hyper_parameter_tuning_jobs_paginator: ListHyperParameterTuningJobsPaginator = client.get_paginator("list_hyper_parameter_tuning_jobs")
        list_image_versions_paginator: ListImageVersionsPaginator = client.get_paginator("list_image_versions")
        list_images_paginator: ListImagesPaginator = client.get_paginator("list_images")
        list_inference_components_paginator: ListInferenceComponentsPaginator = client.get_paginator("list_inference_components")
        list_inference_experiments_paginator: ListInferenceExperimentsPaginator = client.get_paginator("list_inference_experiments")
        list_inference_recommendations_job_steps_paginator: ListInferenceRecommendationsJobStepsPaginator = client.get_paginator("list_inference_recommendations_job_steps")
        list_inference_recommendations_jobs_paginator: ListInferenceRecommendationsJobsPaginator = client.get_paginator("list_inference_recommendations_jobs")
        list_labeling_jobs_for_workteam_paginator: ListLabelingJobsForWorkteamPaginator = client.get_paginator("list_labeling_jobs_for_workteam")
        list_labeling_jobs_paginator: ListLabelingJobsPaginator = client.get_paginator("list_labeling_jobs")
        list_lineage_groups_paginator: ListLineageGroupsPaginator = client.get_paginator("list_lineage_groups")
        list_mlflow_tracking_servers_paginator: ListMlflowTrackingServersPaginator = client.get_paginator("list_mlflow_tracking_servers")
        list_model_bias_job_definitions_paginator: ListModelBiasJobDefinitionsPaginator = client.get_paginator("list_model_bias_job_definitions")
        list_model_card_export_jobs_paginator: ListModelCardExportJobsPaginator = client.get_paginator("list_model_card_export_jobs")
        list_model_card_versions_paginator: ListModelCardVersionsPaginator = client.get_paginator("list_model_card_versions")
        list_model_cards_paginator: ListModelCardsPaginator = client.get_paginator("list_model_cards")
        list_model_explainability_job_definitions_paginator: ListModelExplainabilityJobDefinitionsPaginator = client.get_paginator("list_model_explainability_job_definitions")
        list_model_metadata_paginator: ListModelMetadataPaginator = client.get_paginator("list_model_metadata")
        list_model_package_groups_paginator: ListModelPackageGroupsPaginator = client.get_paginator("list_model_package_groups")
        list_model_packages_paginator: ListModelPackagesPaginator = client.get_paginator("list_model_packages")
        list_model_quality_job_definitions_paginator: ListModelQualityJobDefinitionsPaginator = client.get_paginator("list_model_quality_job_definitions")
        list_models_paginator: ListModelsPaginator = client.get_paginator("list_models")
        list_monitoring_alert_history_paginator: ListMonitoringAlertHistoryPaginator = client.get_paginator("list_monitoring_alert_history")
        list_monitoring_alerts_paginator: ListMonitoringAlertsPaginator = client.get_paginator("list_monitoring_alerts")
        list_monitoring_executions_paginator: ListMonitoringExecutionsPaginator = client.get_paginator("list_monitoring_executions")
        list_monitoring_schedules_paginator: ListMonitoringSchedulesPaginator = client.get_paginator("list_monitoring_schedules")
        list_notebook_instance_lifecycle_configs_paginator: ListNotebookInstanceLifecycleConfigsPaginator = client.get_paginator("list_notebook_instance_lifecycle_configs")
        list_notebook_instances_paginator: ListNotebookInstancesPaginator = client.get_paginator("list_notebook_instances")
        list_optimization_jobs_paginator: ListOptimizationJobsPaginator = client.get_paginator("list_optimization_jobs")
        list_pipeline_execution_steps_paginator: ListPipelineExecutionStepsPaginator = client.get_paginator("list_pipeline_execution_steps")
        list_pipeline_executions_paginator: ListPipelineExecutionsPaginator = client.get_paginator("list_pipeline_executions")
        list_pipeline_parameters_for_execution_paginator: ListPipelineParametersForExecutionPaginator = client.get_paginator("list_pipeline_parameters_for_execution")
        list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
        list_processing_jobs_paginator: ListProcessingJobsPaginator = client.get_paginator("list_processing_jobs")
        list_resource_catalogs_paginator: ListResourceCatalogsPaginator = client.get_paginator("list_resource_catalogs")
        list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
        list_stage_devices_paginator: ListStageDevicesPaginator = client.get_paginator("list_stage_devices")
        list_studio_lifecycle_configs_paginator: ListStudioLifecycleConfigsPaginator = client.get_paginator("list_studio_lifecycle_configs")
        list_subscribed_workteams_paginator: ListSubscribedWorkteamsPaginator = client.get_paginator("list_subscribed_workteams")
        list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
        list_training_jobs_for_hyper_parameter_tuning_job_paginator: ListTrainingJobsForHyperParameterTuningJobPaginator = client.get_paginator("list_training_jobs_for_hyper_parameter_tuning_job")
        list_training_jobs_paginator: ListTrainingJobsPaginator = client.get_paginator("list_training_jobs")
        list_transform_jobs_paginator: ListTransformJobsPaginator = client.get_paginator("list_transform_jobs")
        list_trial_components_paginator: ListTrialComponentsPaginator = client.get_paginator("list_trial_components")
        list_trials_paginator: ListTrialsPaginator = client.get_paginator("list_trials")
        list_user_profiles_paginator: ListUserProfilesPaginator = client.get_paginator("list_user_profiles")
        list_workforces_paginator: ListWorkforcesPaginator = client.get_paginator("list_workforces")
        list_workteams_paginator: ListWorkteamsPaginator = client.get_paginator("list_workteams")
        search_paginator: SearchPaginator = client.get_paginator("search")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListActionsRequestListActionsPaginateTypeDef,
    ListActionsResponseTypeDef,
    ListAlgorithmsInputListAlgorithmsPaginateTypeDef,
    ListAlgorithmsOutputTypeDef,
    ListAliasesRequestListAliasesPaginateTypeDef,
    ListAliasesResponseTypeDef,
    ListAppImageConfigsRequestListAppImageConfigsPaginateTypeDef,
    ListAppImageConfigsResponseTypeDef,
    ListAppsRequestListAppsPaginateTypeDef,
    ListAppsResponseTypeDef,
    ListArtifactsRequestListArtifactsPaginateTypeDef,
    ListArtifactsResponseTypeDef,
    ListAssociationsRequestListAssociationsPaginateTypeDef,
    ListAssociationsResponseTypeDef,
    ListAutoMLJobsRequestListAutoMLJobsPaginateTypeDef,
    ListAutoMLJobsResponseTypeDef,
    ListCandidatesForAutoMLJobRequestListCandidatesForAutoMLJobPaginateTypeDef,
    ListCandidatesForAutoMLJobResponseTypeDef,
    ListClusterNodesRequestListClusterNodesPaginateTypeDef,
    ListClusterNodesResponseTypeDef,
    ListClustersRequestListClustersPaginateTypeDef,
    ListClustersResponseTypeDef,
    ListCodeRepositoriesInputListCodeRepositoriesPaginateTypeDef,
    ListCodeRepositoriesOutputTypeDef,
    ListCompilationJobsRequestListCompilationJobsPaginateTypeDef,
    ListCompilationJobsResponseTypeDef,
    ListContextsRequestListContextsPaginateTypeDef,
    ListContextsResponseTypeDef,
    ListDataQualityJobDefinitionsRequestListDataQualityJobDefinitionsPaginateTypeDef,
    ListDataQualityJobDefinitionsResponseTypeDef,
    ListDeviceFleetsRequestListDeviceFleetsPaginateTypeDef,
    ListDeviceFleetsResponseTypeDef,
    ListDevicesRequestListDevicesPaginateTypeDef,
    ListDevicesResponseTypeDef,
    ListDomainsRequestListDomainsPaginateTypeDef,
    ListDomainsResponseTypeDef,
    ListEdgeDeploymentPlansRequestListEdgeDeploymentPlansPaginateTypeDef,
    ListEdgeDeploymentPlansResponseTypeDef,
    ListEdgePackagingJobsRequestListEdgePackagingJobsPaginateTypeDef,
    ListEdgePackagingJobsResponseTypeDef,
    ListEndpointConfigsInputListEndpointConfigsPaginateTypeDef,
    ListEndpointConfigsOutputTypeDef,
    ListEndpointsInputListEndpointsPaginateTypeDef,
    ListEndpointsOutputTypeDef,
    ListExperimentsRequestListExperimentsPaginateTypeDef,
    ListExperimentsResponseTypeDef,
    ListFeatureGroupsRequestListFeatureGroupsPaginateTypeDef,
    ListFeatureGroupsResponseTypeDef,
    ListFlowDefinitionsRequestListFlowDefinitionsPaginateTypeDef,
    ListFlowDefinitionsResponseTypeDef,
    ListHumanTaskUisRequestListHumanTaskUisPaginateTypeDef,
    ListHumanTaskUisResponseTypeDef,
    ListHyperParameterTuningJobsRequestListHyperParameterTuningJobsPaginateTypeDef,
    ListHyperParameterTuningJobsResponseTypeDef,
    ListImagesRequestListImagesPaginateTypeDef,
    ListImagesResponseTypeDef,
    ListImageVersionsRequestListImageVersionsPaginateTypeDef,
    ListImageVersionsResponseTypeDef,
    ListInferenceComponentsInputListInferenceComponentsPaginateTypeDef,
    ListInferenceComponentsOutputTypeDef,
    ListInferenceExperimentsRequestListInferenceExperimentsPaginateTypeDef,
    ListInferenceExperimentsResponseTypeDef,
    ListInferenceRecommendationsJobsRequestListInferenceRecommendationsJobsPaginateTypeDef,
    ListInferenceRecommendationsJobsResponseTypeDef,
    ListInferenceRecommendationsJobStepsRequestListInferenceRecommendationsJobStepsPaginateTypeDef,
    ListInferenceRecommendationsJobStepsResponseTypeDef,
    ListLabelingJobsForWorkteamRequestListLabelingJobsForWorkteamPaginateTypeDef,
    ListLabelingJobsForWorkteamResponseTypeDef,
    ListLabelingJobsRequestListLabelingJobsPaginateTypeDef,
    ListLabelingJobsResponseTypeDef,
    ListLineageGroupsRequestListLineageGroupsPaginateTypeDef,
    ListLineageGroupsResponseTypeDef,
    ListMlflowTrackingServersRequestListMlflowTrackingServersPaginateTypeDef,
    ListMlflowTrackingServersResponseTypeDef,
    ListModelBiasJobDefinitionsRequestListModelBiasJobDefinitionsPaginateTypeDef,
    ListModelBiasJobDefinitionsResponseTypeDef,
    ListModelCardExportJobsRequestListModelCardExportJobsPaginateTypeDef,
    ListModelCardExportJobsResponseTypeDef,
    ListModelCardsRequestListModelCardsPaginateTypeDef,
    ListModelCardsResponseTypeDef,
    ListModelCardVersionsRequestListModelCardVersionsPaginateTypeDef,
    ListModelCardVersionsResponseTypeDef,
    ListModelExplainabilityJobDefinitionsRequestListModelExplainabilityJobDefinitionsPaginateTypeDef,
    ListModelExplainabilityJobDefinitionsResponseTypeDef,
    ListModelMetadataRequestListModelMetadataPaginateTypeDef,
    ListModelMetadataResponseTypeDef,
    ListModelPackageGroupsInputListModelPackageGroupsPaginateTypeDef,
    ListModelPackageGroupsOutputTypeDef,
    ListModelPackagesInputListModelPackagesPaginateTypeDef,
    ListModelPackagesOutputTypeDef,
    ListModelQualityJobDefinitionsRequestListModelQualityJobDefinitionsPaginateTypeDef,
    ListModelQualityJobDefinitionsResponseTypeDef,
    ListModelsInputListModelsPaginateTypeDef,
    ListModelsOutputTypeDef,
    ListMonitoringAlertHistoryRequestListMonitoringAlertHistoryPaginateTypeDef,
    ListMonitoringAlertHistoryResponseTypeDef,
    ListMonitoringAlertsRequestListMonitoringAlertsPaginateTypeDef,
    ListMonitoringAlertsResponseTypeDef,
    ListMonitoringExecutionsRequestListMonitoringExecutionsPaginateTypeDef,
    ListMonitoringExecutionsResponseTypeDef,
    ListMonitoringSchedulesRequestListMonitoringSchedulesPaginateTypeDef,
    ListMonitoringSchedulesResponseTypeDef,
    ListNotebookInstanceLifecycleConfigsInputListNotebookInstanceLifecycleConfigsPaginateTypeDef,
    ListNotebookInstanceLifecycleConfigsOutputTypeDef,
    ListNotebookInstancesInputListNotebookInstancesPaginateTypeDef,
    ListNotebookInstancesOutputTypeDef,
    ListOptimizationJobsRequestListOptimizationJobsPaginateTypeDef,
    ListOptimizationJobsResponseTypeDef,
    ListPipelineExecutionsRequestListPipelineExecutionsPaginateTypeDef,
    ListPipelineExecutionsResponseTypeDef,
    ListPipelineExecutionStepsRequestListPipelineExecutionStepsPaginateTypeDef,
    ListPipelineExecutionStepsResponseTypeDef,
    ListPipelineParametersForExecutionRequestListPipelineParametersForExecutionPaginateTypeDef,
    ListPipelineParametersForExecutionResponseTypeDef,
    ListPipelinesRequestListPipelinesPaginateTypeDef,
    ListPipelinesResponseTypeDef,
    ListProcessingJobsRequestListProcessingJobsPaginateTypeDef,
    ListProcessingJobsResponseTypeDef,
    ListResourceCatalogsRequestListResourceCatalogsPaginateTypeDef,
    ListResourceCatalogsResponseTypeDef,
    ListSpacesRequestListSpacesPaginateTypeDef,
    ListSpacesResponseTypeDef,
    ListStageDevicesRequestListStageDevicesPaginateTypeDef,
    ListStageDevicesResponseTypeDef,
    ListStudioLifecycleConfigsRequestListStudioLifecycleConfigsPaginateTypeDef,
    ListStudioLifecycleConfigsResponseTypeDef,
    ListSubscribedWorkteamsRequestListSubscribedWorkteamsPaginateTypeDef,
    ListSubscribedWorkteamsResponseTypeDef,
    ListTagsInputListTagsPaginateTypeDef,
    ListTagsOutputTypeDef,
    ListTrainingJobsForHyperParameterTuningJobRequestListTrainingJobsForHyperParameterTuningJobPaginateTypeDef,
    ListTrainingJobsForHyperParameterTuningJobResponseTypeDef,
    ListTrainingJobsRequestListTrainingJobsPaginateTypeDef,
    ListTrainingJobsResponseTypeDef,
    ListTransformJobsRequestListTransformJobsPaginateTypeDef,
    ListTransformJobsResponseTypeDef,
    ListTrialComponentsRequestListTrialComponentsPaginateTypeDef,
    ListTrialComponentsResponseTypeDef,
    ListTrialsRequestListTrialsPaginateTypeDef,
    ListTrialsResponseTypeDef,
    ListUserProfilesRequestListUserProfilesPaginateTypeDef,
    ListUserProfilesResponseTypeDef,
    ListWorkforcesRequestListWorkforcesPaginateTypeDef,
    ListWorkforcesResponseTypeDef,
    ListWorkteamsRequestListWorkteamsPaginateTypeDef,
    ListWorkteamsResponseTypeDef,
    SearchRequestSearchPaginateTypeDef,
    SearchResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListActionsPaginator",
    "ListAlgorithmsPaginator",
    "ListAliasesPaginator",
    "ListAppImageConfigsPaginator",
    "ListAppsPaginator",
    "ListArtifactsPaginator",
    "ListAssociationsPaginator",
    "ListAutoMLJobsPaginator",
    "ListCandidatesForAutoMLJobPaginator",
    "ListClusterNodesPaginator",
    "ListClustersPaginator",
    "ListCodeRepositoriesPaginator",
    "ListCompilationJobsPaginator",
    "ListContextsPaginator",
    "ListDataQualityJobDefinitionsPaginator",
    "ListDeviceFleetsPaginator",
    "ListDevicesPaginator",
    "ListDomainsPaginator",
    "ListEdgeDeploymentPlansPaginator",
    "ListEdgePackagingJobsPaginator",
    "ListEndpointConfigsPaginator",
    "ListEndpointsPaginator",
    "ListExperimentsPaginator",
    "ListFeatureGroupsPaginator",
    "ListFlowDefinitionsPaginator",
    "ListHumanTaskUisPaginator",
    "ListHyperParameterTuningJobsPaginator",
    "ListImageVersionsPaginator",
    "ListImagesPaginator",
    "ListInferenceComponentsPaginator",
    "ListInferenceExperimentsPaginator",
    "ListInferenceRecommendationsJobStepsPaginator",
    "ListInferenceRecommendationsJobsPaginator",
    "ListLabelingJobsForWorkteamPaginator",
    "ListLabelingJobsPaginator",
    "ListLineageGroupsPaginator",
    "ListMlflowTrackingServersPaginator",
    "ListModelBiasJobDefinitionsPaginator",
    "ListModelCardExportJobsPaginator",
    "ListModelCardVersionsPaginator",
    "ListModelCardsPaginator",
    "ListModelExplainabilityJobDefinitionsPaginator",
    "ListModelMetadataPaginator",
    "ListModelPackageGroupsPaginator",
    "ListModelPackagesPaginator",
    "ListModelQualityJobDefinitionsPaginator",
    "ListModelsPaginator",
    "ListMonitoringAlertHistoryPaginator",
    "ListMonitoringAlertsPaginator",
    "ListMonitoringExecutionsPaginator",
    "ListMonitoringSchedulesPaginator",
    "ListNotebookInstanceLifecycleConfigsPaginator",
    "ListNotebookInstancesPaginator",
    "ListOptimizationJobsPaginator",
    "ListPipelineExecutionStepsPaginator",
    "ListPipelineExecutionsPaginator",
    "ListPipelineParametersForExecutionPaginator",
    "ListPipelinesPaginator",
    "ListProcessingJobsPaginator",
    "ListResourceCatalogsPaginator",
    "ListSpacesPaginator",
    "ListStageDevicesPaginator",
    "ListStudioLifecycleConfigsPaginator",
    "ListSubscribedWorkteamsPaginator",
    "ListTagsPaginator",
    "ListTrainingJobsForHyperParameterTuningJobPaginator",
    "ListTrainingJobsPaginator",
    "ListTransformJobsPaginator",
    "ListTrialComponentsPaginator",
    "ListTrialsPaginator",
    "ListUserProfilesPaginator",
    "ListWorkforcesPaginator",
    "ListWorkteamsPaginator",
    "SearchPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListActions.html#SageMaker.Paginator.ListActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListActionsRequestListActionsPaginateTypeDef]
    ) -> AsyncIterator[ListActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListActions.html#SageMaker.Paginator.ListActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listactionspaginator)
        """

class ListAlgorithmsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAlgorithms.html#SageMaker.Paginator.ListAlgorithms)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listalgorithmspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAlgorithmsInputListAlgorithmsPaginateTypeDef]
    ) -> AsyncIterator[ListAlgorithmsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAlgorithms.html#SageMaker.Paginator.ListAlgorithms.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listalgorithmspaginator)
        """

class ListAliasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAliases.html#SageMaker.Paginator.ListAliases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listaliasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAliasesRequestListAliasesPaginateTypeDef]
    ) -> AsyncIterator[ListAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAliases.html#SageMaker.Paginator.ListAliases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listaliasespaginator)
        """

class ListAppImageConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAppImageConfigs.html#SageMaker.Paginator.ListAppImageConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listappimageconfigspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAppImageConfigsRequestListAppImageConfigsPaginateTypeDef]
    ) -> AsyncIterator[ListAppImageConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAppImageConfigs.html#SageMaker.Paginator.ListAppImageConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listappimageconfigspaginator)
        """

class ListAppsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListApps.html#SageMaker.Paginator.ListApps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listappspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAppsRequestListAppsPaginateTypeDef]
    ) -> AsyncIterator[ListAppsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListApps.html#SageMaker.Paginator.ListApps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listappspaginator)
        """

class ListArtifactsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListArtifacts.html#SageMaker.Paginator.ListArtifacts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listartifactspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListArtifactsRequestListArtifactsPaginateTypeDef]
    ) -> AsyncIterator[ListArtifactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListArtifacts.html#SageMaker.Paginator.ListArtifacts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listartifactspaginator)
        """

class ListAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAssociations.html#SageMaker.Paginator.ListAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listassociationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAssociationsRequestListAssociationsPaginateTypeDef]
    ) -> AsyncIterator[ListAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAssociations.html#SageMaker.Paginator.ListAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listassociationspaginator)
        """

class ListAutoMLJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAutoMLJobs.html#SageMaker.Paginator.ListAutoMLJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listautomljobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAutoMLJobsRequestListAutoMLJobsPaginateTypeDef]
    ) -> AsyncIterator[ListAutoMLJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAutoMLJobs.html#SageMaker.Paginator.ListAutoMLJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listautomljobspaginator)
        """

class ListCandidatesForAutoMLJobPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCandidatesForAutoMLJob.html#SageMaker.Paginator.ListCandidatesForAutoMLJob)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcandidatesforautomljobpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCandidatesForAutoMLJobRequestListCandidatesForAutoMLJobPaginateTypeDef
        ],
    ) -> AsyncIterator[ListCandidatesForAutoMLJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCandidatesForAutoMLJob.html#SageMaker.Paginator.ListCandidatesForAutoMLJob.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcandidatesforautomljobpaginator)
        """

class ListClusterNodesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusterNodes.html#SageMaker.Paginator.ListClusterNodes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listclusternodespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListClusterNodesRequestListClusterNodesPaginateTypeDef]
    ) -> AsyncIterator[ListClusterNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusterNodes.html#SageMaker.Paginator.ListClusterNodes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listclusternodespaginator)
        """

class ListClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusters.html#SageMaker.Paginator.ListClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListClustersRequestListClustersPaginateTypeDef]
    ) -> AsyncIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusters.html#SageMaker.Paginator.ListClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listclusterspaginator)
        """

class ListCodeRepositoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCodeRepositories.html#SageMaker.Paginator.ListCodeRepositories)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcoderepositoriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCodeRepositoriesInputListCodeRepositoriesPaginateTypeDef]
    ) -> AsyncIterator[ListCodeRepositoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCodeRepositories.html#SageMaker.Paginator.ListCodeRepositories.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcoderepositoriespaginator)
        """

class ListCompilationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCompilationJobs.html#SageMaker.Paginator.ListCompilationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcompilationjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCompilationJobsRequestListCompilationJobsPaginateTypeDef]
    ) -> AsyncIterator[ListCompilationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCompilationJobs.html#SageMaker.Paginator.ListCompilationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcompilationjobspaginator)
        """

class ListContextsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListContexts.html#SageMaker.Paginator.ListContexts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcontextspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListContextsRequestListContextsPaginateTypeDef]
    ) -> AsyncIterator[ListContextsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListContexts.html#SageMaker.Paginator.ListContexts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcontextspaginator)
        """

class ListDataQualityJobDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDataQualityJobDefinitions.html#SageMaker.Paginator.ListDataQualityJobDefinitions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdataqualityjobdefinitionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListDataQualityJobDefinitionsRequestListDataQualityJobDefinitionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListDataQualityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDataQualityJobDefinitions.html#SageMaker.Paginator.ListDataQualityJobDefinitions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdataqualityjobdefinitionspaginator)
        """

class ListDeviceFleetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDeviceFleets.html#SageMaker.Paginator.ListDeviceFleets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdevicefleetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDeviceFleetsRequestListDeviceFleetsPaginateTypeDef]
    ) -> AsyncIterator[ListDeviceFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDeviceFleets.html#SageMaker.Paginator.ListDeviceFleets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdevicefleetspaginator)
        """

class ListDevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDevices.html#SageMaker.Paginator.ListDevices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdevicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDevicesRequestListDevicesPaginateTypeDef]
    ) -> AsyncIterator[ListDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDevices.html#SageMaker.Paginator.ListDevices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdevicespaginator)
        """

class ListDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDomains.html#SageMaker.Paginator.ListDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdomainspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDomainsRequestListDomainsPaginateTypeDef]
    ) -> AsyncIterator[ListDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDomains.html#SageMaker.Paginator.ListDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdomainspaginator)
        """

class ListEdgeDeploymentPlansPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEdgeDeploymentPlans.html#SageMaker.Paginator.ListEdgeDeploymentPlans)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listedgedeploymentplanspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEdgeDeploymentPlansRequestListEdgeDeploymentPlansPaginateTypeDef]
    ) -> AsyncIterator[ListEdgeDeploymentPlansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEdgeDeploymentPlans.html#SageMaker.Paginator.ListEdgeDeploymentPlans.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listedgedeploymentplanspaginator)
        """

class ListEdgePackagingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEdgePackagingJobs.html#SageMaker.Paginator.ListEdgePackagingJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listedgepackagingjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEdgePackagingJobsRequestListEdgePackagingJobsPaginateTypeDef]
    ) -> AsyncIterator[ListEdgePackagingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEdgePackagingJobs.html#SageMaker.Paginator.ListEdgePackagingJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listedgepackagingjobspaginator)
        """

class ListEndpointConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEndpointConfigs.html#SageMaker.Paginator.ListEndpointConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listendpointconfigspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEndpointConfigsInputListEndpointConfigsPaginateTypeDef]
    ) -> AsyncIterator[ListEndpointConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEndpointConfigs.html#SageMaker.Paginator.ListEndpointConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listendpointconfigspaginator)
        """

class ListEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEndpoints.html#SageMaker.Paginator.ListEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listendpointspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEndpointsInputListEndpointsPaginateTypeDef]
    ) -> AsyncIterator[ListEndpointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEndpoints.html#SageMaker.Paginator.ListEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listendpointspaginator)
        """

class ListExperimentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListExperiments.html#SageMaker.Paginator.ListExperiments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listexperimentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListExperimentsRequestListExperimentsPaginateTypeDef]
    ) -> AsyncIterator[ListExperimentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListExperiments.html#SageMaker.Paginator.ListExperiments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listexperimentspaginator)
        """

class ListFeatureGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListFeatureGroups.html#SageMaker.Paginator.ListFeatureGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listfeaturegroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFeatureGroupsRequestListFeatureGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListFeatureGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListFeatureGroups.html#SageMaker.Paginator.ListFeatureGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listfeaturegroupspaginator)
        """

class ListFlowDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListFlowDefinitions.html#SageMaker.Paginator.ListFlowDefinitions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listflowdefinitionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFlowDefinitionsRequestListFlowDefinitionsPaginateTypeDef]
    ) -> AsyncIterator[ListFlowDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListFlowDefinitions.html#SageMaker.Paginator.ListFlowDefinitions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listflowdefinitionspaginator)
        """

class ListHumanTaskUisPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListHumanTaskUis.html#SageMaker.Paginator.ListHumanTaskUis)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listhumantaskuispaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListHumanTaskUisRequestListHumanTaskUisPaginateTypeDef]
    ) -> AsyncIterator[ListHumanTaskUisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListHumanTaskUis.html#SageMaker.Paginator.ListHumanTaskUis.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listhumantaskuispaginator)
        """

class ListHyperParameterTuningJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListHyperParameterTuningJobs.html#SageMaker.Paginator.ListHyperParameterTuningJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listhyperparametertuningjobspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListHyperParameterTuningJobsRequestListHyperParameterTuningJobsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListHyperParameterTuningJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListHyperParameterTuningJobs.html#SageMaker.Paginator.ListHyperParameterTuningJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listhyperparametertuningjobspaginator)
        """

class ListImageVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListImageVersions.html#SageMaker.Paginator.ListImageVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listimageversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListImageVersionsRequestListImageVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListImageVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListImageVersions.html#SageMaker.Paginator.ListImageVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listimageversionspaginator)
        """

class ListImagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListImages.html#SageMaker.Paginator.ListImages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listimagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListImagesRequestListImagesPaginateTypeDef]
    ) -> AsyncIterator[ListImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListImages.html#SageMaker.Paginator.ListImages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listimagespaginator)
        """

class ListInferenceComponentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceComponents.html#SageMaker.Paginator.ListInferenceComponents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencecomponentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInferenceComponentsInputListInferenceComponentsPaginateTypeDef]
    ) -> AsyncIterator[ListInferenceComponentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceComponents.html#SageMaker.Paginator.ListInferenceComponents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencecomponentspaginator)
        """

class ListInferenceExperimentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceExperiments.html#SageMaker.Paginator.ListInferenceExperiments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferenceexperimentspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListInferenceExperimentsRequestListInferenceExperimentsPaginateTypeDef],
    ) -> AsyncIterator[ListInferenceExperimentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceExperiments.html#SageMaker.Paginator.ListInferenceExperiments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferenceexperimentspaginator)
        """

class ListInferenceRecommendationsJobStepsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceRecommendationsJobSteps.html#SageMaker.Paginator.ListInferenceRecommendationsJobSteps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencerecommendationsjobstepspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListInferenceRecommendationsJobStepsRequestListInferenceRecommendationsJobStepsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListInferenceRecommendationsJobStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceRecommendationsJobSteps.html#SageMaker.Paginator.ListInferenceRecommendationsJobSteps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencerecommendationsjobstepspaginator)
        """

class ListInferenceRecommendationsJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceRecommendationsJobs.html#SageMaker.Paginator.ListInferenceRecommendationsJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencerecommendationsjobspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListInferenceRecommendationsJobsRequestListInferenceRecommendationsJobsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListInferenceRecommendationsJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceRecommendationsJobs.html#SageMaker.Paginator.ListInferenceRecommendationsJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencerecommendationsjobspaginator)
        """

class ListLabelingJobsForWorkteamPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLabelingJobsForWorkteam.html#SageMaker.Paginator.ListLabelingJobsForWorkteam)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlabelingjobsforworkteampaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListLabelingJobsForWorkteamRequestListLabelingJobsForWorkteamPaginateTypeDef
        ],
    ) -> AsyncIterator[ListLabelingJobsForWorkteamResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLabelingJobsForWorkteam.html#SageMaker.Paginator.ListLabelingJobsForWorkteam.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlabelingjobsforworkteampaginator)
        """

class ListLabelingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLabelingJobs.html#SageMaker.Paginator.ListLabelingJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlabelingjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLabelingJobsRequestListLabelingJobsPaginateTypeDef]
    ) -> AsyncIterator[ListLabelingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLabelingJobs.html#SageMaker.Paginator.ListLabelingJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlabelingjobspaginator)
        """

class ListLineageGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLineageGroups.html#SageMaker.Paginator.ListLineageGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlineagegroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLineageGroupsRequestListLineageGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListLineageGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLineageGroups.html#SageMaker.Paginator.ListLineageGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlineagegroupspaginator)
        """

class ListMlflowTrackingServersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMlflowTrackingServers.html#SageMaker.Paginator.ListMlflowTrackingServers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmlflowtrackingserverspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListMlflowTrackingServersRequestListMlflowTrackingServersPaginateTypeDef],
    ) -> AsyncIterator[ListMlflowTrackingServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMlflowTrackingServers.html#SageMaker.Paginator.ListMlflowTrackingServers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmlflowtrackingserverspaginator)
        """

class ListModelBiasJobDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelBiasJobDefinitions.html#SageMaker.Paginator.ListModelBiasJobDefinitions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelbiasjobdefinitionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListModelBiasJobDefinitionsRequestListModelBiasJobDefinitionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListModelBiasJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelBiasJobDefinitions.html#SageMaker.Paginator.ListModelBiasJobDefinitions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelbiasjobdefinitionspaginator)
        """

class ListModelCardExportJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCardExportJobs.html#SageMaker.Paginator.ListModelCardExportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardexportjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListModelCardExportJobsRequestListModelCardExportJobsPaginateTypeDef]
    ) -> AsyncIterator[ListModelCardExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCardExportJobs.html#SageMaker.Paginator.ListModelCardExportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardexportjobspaginator)
        """

class ListModelCardVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCardVersions.html#SageMaker.Paginator.ListModelCardVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListModelCardVersionsRequestListModelCardVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListModelCardVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCardVersions.html#SageMaker.Paginator.ListModelCardVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardversionspaginator)
        """

class ListModelCardsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCards.html#SageMaker.Paginator.ListModelCards)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListModelCardsRequestListModelCardsPaginateTypeDef]
    ) -> AsyncIterator[ListModelCardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCards.html#SageMaker.Paginator.ListModelCards.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardspaginator)
        """

class ListModelExplainabilityJobDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelExplainabilityJobDefinitions.html#SageMaker.Paginator.ListModelExplainabilityJobDefinitions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelexplainabilityjobdefinitionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListModelExplainabilityJobDefinitionsRequestListModelExplainabilityJobDefinitionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListModelExplainabilityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelExplainabilityJobDefinitions.html#SageMaker.Paginator.ListModelExplainabilityJobDefinitions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelexplainabilityjobdefinitionspaginator)
        """

class ListModelMetadataPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelMetadata.html#SageMaker.Paginator.ListModelMetadata)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelmetadatapaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListModelMetadataRequestListModelMetadataPaginateTypeDef]
    ) -> AsyncIterator[ListModelMetadataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelMetadata.html#SageMaker.Paginator.ListModelMetadata.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelmetadatapaginator)
        """

class ListModelPackageGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelPackageGroups.html#SageMaker.Paginator.ListModelPackageGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelpackagegroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListModelPackageGroupsInputListModelPackageGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListModelPackageGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelPackageGroups.html#SageMaker.Paginator.ListModelPackageGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelpackagegroupspaginator)
        """

class ListModelPackagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelPackages.html#SageMaker.Paginator.ListModelPackages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelpackagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListModelPackagesInputListModelPackagesPaginateTypeDef]
    ) -> AsyncIterator[ListModelPackagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelPackages.html#SageMaker.Paginator.ListModelPackages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelpackagespaginator)
        """

class ListModelQualityJobDefinitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelQualityJobDefinitions.html#SageMaker.Paginator.ListModelQualityJobDefinitions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelqualityjobdefinitionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListModelQualityJobDefinitionsRequestListModelQualityJobDefinitionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListModelQualityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelQualityJobDefinitions.html#SageMaker.Paginator.ListModelQualityJobDefinitions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelqualityjobdefinitionspaginator)
        """

class ListModelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModels.html#SageMaker.Paginator.ListModels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListModelsInputListModelsPaginateTypeDef]
    ) -> AsyncIterator[ListModelsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModels.html#SageMaker.Paginator.ListModels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelspaginator)
        """

class ListMonitoringAlertHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringAlertHistory.html#SageMaker.Paginator.ListMonitoringAlertHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringalerthistorypaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListMonitoringAlertHistoryRequestListMonitoringAlertHistoryPaginateTypeDef
        ],
    ) -> AsyncIterator[ListMonitoringAlertHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringAlertHistory.html#SageMaker.Paginator.ListMonitoringAlertHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringalerthistorypaginator)
        """

class ListMonitoringAlertsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringAlerts.html#SageMaker.Paginator.ListMonitoringAlerts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringalertspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMonitoringAlertsRequestListMonitoringAlertsPaginateTypeDef]
    ) -> AsyncIterator[ListMonitoringAlertsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringAlerts.html#SageMaker.Paginator.ListMonitoringAlerts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringalertspaginator)
        """

class ListMonitoringExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringExecutions.html#SageMaker.Paginator.ListMonitoringExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringexecutionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListMonitoringExecutionsRequestListMonitoringExecutionsPaginateTypeDef],
    ) -> AsyncIterator[ListMonitoringExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringExecutions.html#SageMaker.Paginator.ListMonitoringExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringexecutionspaginator)
        """

class ListMonitoringSchedulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringSchedules.html#SageMaker.Paginator.ListMonitoringSchedules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringschedulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMonitoringSchedulesRequestListMonitoringSchedulesPaginateTypeDef]
    ) -> AsyncIterator[ListMonitoringSchedulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringSchedules.html#SageMaker.Paginator.ListMonitoringSchedules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringschedulespaginator)
        """

class ListNotebookInstanceLifecycleConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListNotebookInstanceLifecycleConfigs.html#SageMaker.Paginator.ListNotebookInstanceLifecycleConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listnotebookinstancelifecycleconfigspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListNotebookInstanceLifecycleConfigsInputListNotebookInstanceLifecycleConfigsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListNotebookInstanceLifecycleConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListNotebookInstanceLifecycleConfigs.html#SageMaker.Paginator.ListNotebookInstanceLifecycleConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listnotebookinstancelifecycleconfigspaginator)
        """

class ListNotebookInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListNotebookInstances.html#SageMaker.Paginator.ListNotebookInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listnotebookinstancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListNotebookInstancesInputListNotebookInstancesPaginateTypeDef]
    ) -> AsyncIterator[ListNotebookInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListNotebookInstances.html#SageMaker.Paginator.ListNotebookInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listnotebookinstancespaginator)
        """

class ListOptimizationJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListOptimizationJobs.html#SageMaker.Paginator.ListOptimizationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listoptimizationjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListOptimizationJobsRequestListOptimizationJobsPaginateTypeDef]
    ) -> AsyncIterator[ListOptimizationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListOptimizationJobs.html#SageMaker.Paginator.ListOptimizationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listoptimizationjobspaginator)
        """

class ListPipelineExecutionStepsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineExecutionSteps.html#SageMaker.Paginator.ListPipelineExecutionSteps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineexecutionstepspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListPipelineExecutionStepsRequestListPipelineExecutionStepsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListPipelineExecutionStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineExecutionSteps.html#SageMaker.Paginator.ListPipelineExecutionSteps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineexecutionstepspaginator)
        """

class ListPipelineExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineExecutions.html#SageMaker.Paginator.ListPipelineExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineexecutionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPipelineExecutionsRequestListPipelineExecutionsPaginateTypeDef]
    ) -> AsyncIterator[ListPipelineExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineExecutions.html#SageMaker.Paginator.ListPipelineExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineexecutionspaginator)
        """

class ListPipelineParametersForExecutionPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineParametersForExecution.html#SageMaker.Paginator.ListPipelineParametersForExecution)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineparametersforexecutionpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListPipelineParametersForExecutionRequestListPipelineParametersForExecutionPaginateTypeDef
        ],
    ) -> AsyncIterator[ListPipelineParametersForExecutionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineParametersForExecution.html#SageMaker.Paginator.ListPipelineParametersForExecution.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineparametersforexecutionpaginator)
        """

class ListPipelinesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelines.html#SageMaker.Paginator.ListPipelines)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelinespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPipelinesRequestListPipelinesPaginateTypeDef]
    ) -> AsyncIterator[ListPipelinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelines.html#SageMaker.Paginator.ListPipelines.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelinespaginator)
        """

class ListProcessingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListProcessingJobs.html#SageMaker.Paginator.ListProcessingJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listprocessingjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProcessingJobsRequestListProcessingJobsPaginateTypeDef]
    ) -> AsyncIterator[ListProcessingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListProcessingJobs.html#SageMaker.Paginator.ListProcessingJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listprocessingjobspaginator)
        """

class ListResourceCatalogsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListResourceCatalogs.html#SageMaker.Paginator.ListResourceCatalogs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listresourcecatalogspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListResourceCatalogsRequestListResourceCatalogsPaginateTypeDef]
    ) -> AsyncIterator[ListResourceCatalogsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListResourceCatalogs.html#SageMaker.Paginator.ListResourceCatalogs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listresourcecatalogspaginator)
        """

class ListSpacesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListSpaces.html#SageMaker.Paginator.ListSpaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listspacespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSpacesRequestListSpacesPaginateTypeDef]
    ) -> AsyncIterator[ListSpacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListSpaces.html#SageMaker.Paginator.ListSpaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listspacespaginator)
        """

class ListStageDevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListStageDevices.html#SageMaker.Paginator.ListStageDevices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#liststagedevicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStageDevicesRequestListStageDevicesPaginateTypeDef]
    ) -> AsyncIterator[ListStageDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListStageDevices.html#SageMaker.Paginator.ListStageDevices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#liststagedevicespaginator)
        """

class ListStudioLifecycleConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListStudioLifecycleConfigs.html#SageMaker.Paginator.ListStudioLifecycleConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#liststudiolifecycleconfigspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListStudioLifecycleConfigsRequestListStudioLifecycleConfigsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListStudioLifecycleConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListStudioLifecycleConfigs.html#SageMaker.Paginator.ListStudioLifecycleConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#liststudiolifecycleconfigspaginator)
        """

class ListSubscribedWorkteamsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListSubscribedWorkteams.html#SageMaker.Paginator.ListSubscribedWorkteams)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listsubscribedworkteamspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSubscribedWorkteamsRequestListSubscribedWorkteamsPaginateTypeDef]
    ) -> AsyncIterator[ListSubscribedWorkteamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListSubscribedWorkteams.html#SageMaker.Paginator.ListSubscribedWorkteams.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listsubscribedworkteamspaginator)
        """

class ListTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTags.html#SageMaker.Paginator.ListTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsInputListTagsPaginateTypeDef]
    ) -> AsyncIterator[ListTagsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTags.html#SageMaker.Paginator.ListTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtagspaginator)
        """

class ListTrainingJobsForHyperParameterTuningJobPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingJobsForHyperParameterTuningJob.html#SageMaker.Paginator.ListTrainingJobsForHyperParameterTuningJob)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrainingjobsforhyperparametertuningjobpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListTrainingJobsForHyperParameterTuningJobRequestListTrainingJobsForHyperParameterTuningJobPaginateTypeDef
        ],
    ) -> AsyncIterator[ListTrainingJobsForHyperParameterTuningJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingJobsForHyperParameterTuningJob.html#SageMaker.Paginator.ListTrainingJobsForHyperParameterTuningJob.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrainingjobsforhyperparametertuningjobpaginator)
        """

class ListTrainingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingJobs.html#SageMaker.Paginator.ListTrainingJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrainingjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTrainingJobsRequestListTrainingJobsPaginateTypeDef]
    ) -> AsyncIterator[ListTrainingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingJobs.html#SageMaker.Paginator.ListTrainingJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrainingjobspaginator)
        """

class ListTransformJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTransformJobs.html#SageMaker.Paginator.ListTransformJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtransformjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTransformJobsRequestListTransformJobsPaginateTypeDef]
    ) -> AsyncIterator[ListTransformJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTransformJobs.html#SageMaker.Paginator.ListTransformJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtransformjobspaginator)
        """

class ListTrialComponentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrialComponents.html#SageMaker.Paginator.ListTrialComponents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrialcomponentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTrialComponentsRequestListTrialComponentsPaginateTypeDef]
    ) -> AsyncIterator[ListTrialComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrialComponents.html#SageMaker.Paginator.ListTrialComponents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrialcomponentspaginator)
        """

class ListTrialsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrials.html#SageMaker.Paginator.ListTrials)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrialspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTrialsRequestListTrialsPaginateTypeDef]
    ) -> AsyncIterator[ListTrialsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrials.html#SageMaker.Paginator.ListTrials.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrialspaginator)
        """

class ListUserProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListUserProfiles.html#SageMaker.Paginator.ListUserProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listuserprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUserProfilesRequestListUserProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListUserProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListUserProfiles.html#SageMaker.Paginator.ListUserProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listuserprofilespaginator)
        """

class ListWorkforcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListWorkforces.html#SageMaker.Paginator.ListWorkforces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listworkforcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListWorkforcesRequestListWorkforcesPaginateTypeDef]
    ) -> AsyncIterator[ListWorkforcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListWorkforces.html#SageMaker.Paginator.ListWorkforces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listworkforcespaginator)
        """

class ListWorkteamsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListWorkteams.html#SageMaker.Paginator.ListWorkteams)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listworkteamspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListWorkteamsRequestListWorkteamsPaginateTypeDef]
    ) -> AsyncIterator[ListWorkteamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListWorkteams.html#SageMaker.Paginator.ListWorkteams.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listworkteamspaginator)
        """

class SearchPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/Search.html#SageMaker.Paginator.Search)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#searchpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchRequestSearchPaginateTypeDef]
    ) -> AsyncIterator[SearchResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/Search.html#SageMaker.Paginator.Search.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#searchpaginator)
        """
