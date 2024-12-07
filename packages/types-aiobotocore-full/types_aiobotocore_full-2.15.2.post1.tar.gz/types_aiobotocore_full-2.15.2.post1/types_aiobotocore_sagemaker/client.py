"""
Type annotations for sagemaker service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sagemaker.client import SageMakerClient

    session = get_session()
    async with session.create_client("sagemaker") as client:
        client: SageMakerClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
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
    ListImagesPaginator,
    ListImageVersionsPaginator,
    ListInferenceComponentsPaginator,
    ListInferenceExperimentsPaginator,
    ListInferenceRecommendationsJobsPaginator,
    ListInferenceRecommendationsJobStepsPaginator,
    ListLabelingJobsForWorkteamPaginator,
    ListLabelingJobsPaginator,
    ListLineageGroupsPaginator,
    ListMlflowTrackingServersPaginator,
    ListModelBiasJobDefinitionsPaginator,
    ListModelCardExportJobsPaginator,
    ListModelCardsPaginator,
    ListModelCardVersionsPaginator,
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
    ListPipelineExecutionsPaginator,
    ListPipelineExecutionStepsPaginator,
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
from .type_defs import (
    AddAssociationRequestRequestTypeDef,
    AddAssociationResponseTypeDef,
    AddTagsInputRequestTypeDef,
    AddTagsOutputTypeDef,
    AssociateTrialComponentRequestRequestTypeDef,
    AssociateTrialComponentResponseTypeDef,
    BatchDescribeModelPackageInputRequestTypeDef,
    BatchDescribeModelPackageOutputTypeDef,
    CreateActionRequestRequestTypeDef,
    CreateActionResponseTypeDef,
    CreateAlgorithmInputRequestTypeDef,
    CreateAlgorithmOutputTypeDef,
    CreateAppImageConfigRequestRequestTypeDef,
    CreateAppImageConfigResponseTypeDef,
    CreateAppRequestRequestTypeDef,
    CreateAppResponseTypeDef,
    CreateArtifactRequestRequestTypeDef,
    CreateArtifactResponseTypeDef,
    CreateAutoMLJobRequestRequestTypeDef,
    CreateAutoMLJobResponseTypeDef,
    CreateAutoMLJobV2RequestRequestTypeDef,
    CreateAutoMLJobV2ResponseTypeDef,
    CreateClusterRequestRequestTypeDef,
    CreateClusterResponseTypeDef,
    CreateCodeRepositoryInputRequestTypeDef,
    CreateCodeRepositoryOutputTypeDef,
    CreateCompilationJobRequestRequestTypeDef,
    CreateCompilationJobResponseTypeDef,
    CreateContextRequestRequestTypeDef,
    CreateContextResponseTypeDef,
    CreateDataQualityJobDefinitionRequestRequestTypeDef,
    CreateDataQualityJobDefinitionResponseTypeDef,
    CreateDeviceFleetRequestRequestTypeDef,
    CreateDomainRequestRequestTypeDef,
    CreateDomainResponseTypeDef,
    CreateEdgeDeploymentPlanRequestRequestTypeDef,
    CreateEdgeDeploymentPlanResponseTypeDef,
    CreateEdgeDeploymentStageRequestRequestTypeDef,
    CreateEdgePackagingJobRequestRequestTypeDef,
    CreateEndpointConfigInputRequestTypeDef,
    CreateEndpointConfigOutputTypeDef,
    CreateEndpointInputRequestTypeDef,
    CreateEndpointOutputTypeDef,
    CreateExperimentRequestRequestTypeDef,
    CreateExperimentResponseTypeDef,
    CreateFeatureGroupRequestRequestTypeDef,
    CreateFeatureGroupResponseTypeDef,
    CreateFlowDefinitionRequestRequestTypeDef,
    CreateFlowDefinitionResponseTypeDef,
    CreateHubContentReferenceRequestRequestTypeDef,
    CreateHubContentReferenceResponseTypeDef,
    CreateHubRequestRequestTypeDef,
    CreateHubResponseTypeDef,
    CreateHumanTaskUiRequestRequestTypeDef,
    CreateHumanTaskUiResponseTypeDef,
    CreateHyperParameterTuningJobRequestRequestTypeDef,
    CreateHyperParameterTuningJobResponseTypeDef,
    CreateImageRequestRequestTypeDef,
    CreateImageResponseTypeDef,
    CreateImageVersionRequestRequestTypeDef,
    CreateImageVersionResponseTypeDef,
    CreateInferenceComponentInputRequestTypeDef,
    CreateInferenceComponentOutputTypeDef,
    CreateInferenceExperimentRequestRequestTypeDef,
    CreateInferenceExperimentResponseTypeDef,
    CreateInferenceRecommendationsJobRequestRequestTypeDef,
    CreateInferenceRecommendationsJobResponseTypeDef,
    CreateLabelingJobRequestRequestTypeDef,
    CreateLabelingJobResponseTypeDef,
    CreateMlflowTrackingServerRequestRequestTypeDef,
    CreateMlflowTrackingServerResponseTypeDef,
    CreateModelBiasJobDefinitionRequestRequestTypeDef,
    CreateModelBiasJobDefinitionResponseTypeDef,
    CreateModelCardExportJobRequestRequestTypeDef,
    CreateModelCardExportJobResponseTypeDef,
    CreateModelCardRequestRequestTypeDef,
    CreateModelCardResponseTypeDef,
    CreateModelExplainabilityJobDefinitionRequestRequestTypeDef,
    CreateModelExplainabilityJobDefinitionResponseTypeDef,
    CreateModelInputRequestTypeDef,
    CreateModelOutputTypeDef,
    CreateModelPackageGroupInputRequestTypeDef,
    CreateModelPackageGroupOutputTypeDef,
    CreateModelPackageInputRequestTypeDef,
    CreateModelPackageOutputTypeDef,
    CreateModelQualityJobDefinitionRequestRequestTypeDef,
    CreateModelQualityJobDefinitionResponseTypeDef,
    CreateMonitoringScheduleRequestRequestTypeDef,
    CreateMonitoringScheduleResponseTypeDef,
    CreateNotebookInstanceInputRequestTypeDef,
    CreateNotebookInstanceLifecycleConfigInputRequestTypeDef,
    CreateNotebookInstanceLifecycleConfigOutputTypeDef,
    CreateNotebookInstanceOutputTypeDef,
    CreateOptimizationJobRequestRequestTypeDef,
    CreateOptimizationJobResponseTypeDef,
    CreatePipelineRequestRequestTypeDef,
    CreatePipelineResponseTypeDef,
    CreatePresignedDomainUrlRequestRequestTypeDef,
    CreatePresignedDomainUrlResponseTypeDef,
    CreatePresignedMlflowTrackingServerUrlRequestRequestTypeDef,
    CreatePresignedMlflowTrackingServerUrlResponseTypeDef,
    CreatePresignedNotebookInstanceUrlInputRequestTypeDef,
    CreatePresignedNotebookInstanceUrlOutputTypeDef,
    CreateProcessingJobRequestRequestTypeDef,
    CreateProcessingJobResponseTypeDef,
    CreateProjectInputRequestTypeDef,
    CreateProjectOutputTypeDef,
    CreateSpaceRequestRequestTypeDef,
    CreateSpaceResponseTypeDef,
    CreateStudioLifecycleConfigRequestRequestTypeDef,
    CreateStudioLifecycleConfigResponseTypeDef,
    CreateTrainingJobRequestRequestTypeDef,
    CreateTrainingJobResponseTypeDef,
    CreateTransformJobRequestRequestTypeDef,
    CreateTransformJobResponseTypeDef,
    CreateTrialComponentRequestRequestTypeDef,
    CreateTrialComponentResponseTypeDef,
    CreateTrialRequestRequestTypeDef,
    CreateTrialResponseTypeDef,
    CreateUserProfileRequestRequestTypeDef,
    CreateUserProfileResponseTypeDef,
    CreateWorkforceRequestRequestTypeDef,
    CreateWorkforceResponseTypeDef,
    CreateWorkteamRequestRequestTypeDef,
    CreateWorkteamResponseTypeDef,
    DeleteActionRequestRequestTypeDef,
    DeleteActionResponseTypeDef,
    DeleteAlgorithmInputRequestTypeDef,
    DeleteAppImageConfigRequestRequestTypeDef,
    DeleteAppRequestRequestTypeDef,
    DeleteArtifactRequestRequestTypeDef,
    DeleteArtifactResponseTypeDef,
    DeleteAssociationRequestRequestTypeDef,
    DeleteAssociationResponseTypeDef,
    DeleteClusterRequestRequestTypeDef,
    DeleteClusterResponseTypeDef,
    DeleteCodeRepositoryInputRequestTypeDef,
    DeleteCompilationJobRequestRequestTypeDef,
    DeleteContextRequestRequestTypeDef,
    DeleteContextResponseTypeDef,
    DeleteDataQualityJobDefinitionRequestRequestTypeDef,
    DeleteDeviceFleetRequestRequestTypeDef,
    DeleteDomainRequestRequestTypeDef,
    DeleteEdgeDeploymentPlanRequestRequestTypeDef,
    DeleteEdgeDeploymentStageRequestRequestTypeDef,
    DeleteEndpointConfigInputRequestTypeDef,
    DeleteEndpointInputRequestTypeDef,
    DeleteExperimentRequestRequestTypeDef,
    DeleteExperimentResponseTypeDef,
    DeleteFeatureGroupRequestRequestTypeDef,
    DeleteFlowDefinitionRequestRequestTypeDef,
    DeleteHubContentReferenceRequestRequestTypeDef,
    DeleteHubContentRequestRequestTypeDef,
    DeleteHubRequestRequestTypeDef,
    DeleteHumanTaskUiRequestRequestTypeDef,
    DeleteHyperParameterTuningJobRequestRequestTypeDef,
    DeleteImageRequestRequestTypeDef,
    DeleteImageVersionRequestRequestTypeDef,
    DeleteInferenceComponentInputRequestTypeDef,
    DeleteInferenceExperimentRequestRequestTypeDef,
    DeleteInferenceExperimentResponseTypeDef,
    DeleteMlflowTrackingServerRequestRequestTypeDef,
    DeleteMlflowTrackingServerResponseTypeDef,
    DeleteModelBiasJobDefinitionRequestRequestTypeDef,
    DeleteModelCardRequestRequestTypeDef,
    DeleteModelExplainabilityJobDefinitionRequestRequestTypeDef,
    DeleteModelInputRequestTypeDef,
    DeleteModelPackageGroupInputRequestTypeDef,
    DeleteModelPackageGroupPolicyInputRequestTypeDef,
    DeleteModelPackageInputRequestTypeDef,
    DeleteModelQualityJobDefinitionRequestRequestTypeDef,
    DeleteMonitoringScheduleRequestRequestTypeDef,
    DeleteNotebookInstanceInputRequestTypeDef,
    DeleteNotebookInstanceLifecycleConfigInputRequestTypeDef,
    DeleteOptimizationJobRequestRequestTypeDef,
    DeletePipelineRequestRequestTypeDef,
    DeletePipelineResponseTypeDef,
    DeleteProjectInputRequestTypeDef,
    DeleteSpaceRequestRequestTypeDef,
    DeleteStudioLifecycleConfigRequestRequestTypeDef,
    DeleteTagsInputRequestTypeDef,
    DeleteTrialComponentRequestRequestTypeDef,
    DeleteTrialComponentResponseTypeDef,
    DeleteTrialRequestRequestTypeDef,
    DeleteTrialResponseTypeDef,
    DeleteUserProfileRequestRequestTypeDef,
    DeleteWorkforceRequestRequestTypeDef,
    DeleteWorkteamRequestRequestTypeDef,
    DeleteWorkteamResponseTypeDef,
    DeregisterDevicesRequestRequestTypeDef,
    DescribeActionRequestRequestTypeDef,
    DescribeActionResponseTypeDef,
    DescribeAlgorithmInputRequestTypeDef,
    DescribeAlgorithmOutputTypeDef,
    DescribeAppImageConfigRequestRequestTypeDef,
    DescribeAppImageConfigResponseTypeDef,
    DescribeAppRequestRequestTypeDef,
    DescribeAppResponseTypeDef,
    DescribeArtifactRequestRequestTypeDef,
    DescribeArtifactResponseTypeDef,
    DescribeAutoMLJobRequestRequestTypeDef,
    DescribeAutoMLJobResponseTypeDef,
    DescribeAutoMLJobV2RequestRequestTypeDef,
    DescribeAutoMLJobV2ResponseTypeDef,
    DescribeClusterNodeRequestRequestTypeDef,
    DescribeClusterNodeResponseTypeDef,
    DescribeClusterRequestRequestTypeDef,
    DescribeClusterResponseTypeDef,
    DescribeCodeRepositoryInputRequestTypeDef,
    DescribeCodeRepositoryOutputTypeDef,
    DescribeCompilationJobRequestRequestTypeDef,
    DescribeCompilationJobResponseTypeDef,
    DescribeContextRequestRequestTypeDef,
    DescribeContextResponseTypeDef,
    DescribeDataQualityJobDefinitionRequestRequestTypeDef,
    DescribeDataQualityJobDefinitionResponseTypeDef,
    DescribeDeviceFleetRequestRequestTypeDef,
    DescribeDeviceFleetResponseTypeDef,
    DescribeDeviceRequestRequestTypeDef,
    DescribeDeviceResponseTypeDef,
    DescribeDomainRequestRequestTypeDef,
    DescribeDomainResponseTypeDef,
    DescribeEdgeDeploymentPlanRequestRequestTypeDef,
    DescribeEdgeDeploymentPlanResponseTypeDef,
    DescribeEdgePackagingJobRequestRequestTypeDef,
    DescribeEdgePackagingJobResponseTypeDef,
    DescribeEndpointConfigInputRequestTypeDef,
    DescribeEndpointConfigOutputTypeDef,
    DescribeEndpointInputRequestTypeDef,
    DescribeEndpointOutputTypeDef,
    DescribeExperimentRequestRequestTypeDef,
    DescribeExperimentResponseTypeDef,
    DescribeFeatureGroupRequestRequestTypeDef,
    DescribeFeatureGroupResponseTypeDef,
    DescribeFeatureMetadataRequestRequestTypeDef,
    DescribeFeatureMetadataResponseTypeDef,
    DescribeFlowDefinitionRequestRequestTypeDef,
    DescribeFlowDefinitionResponseTypeDef,
    DescribeHubContentRequestRequestTypeDef,
    DescribeHubContentResponseTypeDef,
    DescribeHubRequestRequestTypeDef,
    DescribeHubResponseTypeDef,
    DescribeHumanTaskUiRequestRequestTypeDef,
    DescribeHumanTaskUiResponseTypeDef,
    DescribeHyperParameterTuningJobRequestRequestTypeDef,
    DescribeHyperParameterTuningJobResponseTypeDef,
    DescribeImageRequestRequestTypeDef,
    DescribeImageResponseTypeDef,
    DescribeImageVersionRequestRequestTypeDef,
    DescribeImageVersionResponseTypeDef,
    DescribeInferenceComponentInputRequestTypeDef,
    DescribeInferenceComponentOutputTypeDef,
    DescribeInferenceExperimentRequestRequestTypeDef,
    DescribeInferenceExperimentResponseTypeDef,
    DescribeInferenceRecommendationsJobRequestRequestTypeDef,
    DescribeInferenceRecommendationsJobResponseTypeDef,
    DescribeLabelingJobRequestRequestTypeDef,
    DescribeLabelingJobResponseTypeDef,
    DescribeLineageGroupRequestRequestTypeDef,
    DescribeLineageGroupResponseTypeDef,
    DescribeMlflowTrackingServerRequestRequestTypeDef,
    DescribeMlflowTrackingServerResponseTypeDef,
    DescribeModelBiasJobDefinitionRequestRequestTypeDef,
    DescribeModelBiasJobDefinitionResponseTypeDef,
    DescribeModelCardExportJobRequestRequestTypeDef,
    DescribeModelCardExportJobResponseTypeDef,
    DescribeModelCardRequestRequestTypeDef,
    DescribeModelCardResponseTypeDef,
    DescribeModelExplainabilityJobDefinitionRequestRequestTypeDef,
    DescribeModelExplainabilityJobDefinitionResponseTypeDef,
    DescribeModelInputRequestTypeDef,
    DescribeModelOutputTypeDef,
    DescribeModelPackageGroupInputRequestTypeDef,
    DescribeModelPackageGroupOutputTypeDef,
    DescribeModelPackageInputRequestTypeDef,
    DescribeModelPackageOutputTypeDef,
    DescribeModelQualityJobDefinitionRequestRequestTypeDef,
    DescribeModelQualityJobDefinitionResponseTypeDef,
    DescribeMonitoringScheduleRequestRequestTypeDef,
    DescribeMonitoringScheduleResponseTypeDef,
    DescribeNotebookInstanceInputRequestTypeDef,
    DescribeNotebookInstanceLifecycleConfigInputRequestTypeDef,
    DescribeNotebookInstanceLifecycleConfigOutputTypeDef,
    DescribeNotebookInstanceOutputTypeDef,
    DescribeOptimizationJobRequestRequestTypeDef,
    DescribeOptimizationJobResponseTypeDef,
    DescribePipelineDefinitionForExecutionRequestRequestTypeDef,
    DescribePipelineDefinitionForExecutionResponseTypeDef,
    DescribePipelineExecutionRequestRequestTypeDef,
    DescribePipelineExecutionResponseTypeDef,
    DescribePipelineRequestRequestTypeDef,
    DescribePipelineResponseTypeDef,
    DescribeProcessingJobRequestRequestTypeDef,
    DescribeProcessingJobResponseTypeDef,
    DescribeProjectInputRequestTypeDef,
    DescribeProjectOutputTypeDef,
    DescribeSpaceRequestRequestTypeDef,
    DescribeSpaceResponseTypeDef,
    DescribeStudioLifecycleConfigRequestRequestTypeDef,
    DescribeStudioLifecycleConfigResponseTypeDef,
    DescribeSubscribedWorkteamRequestRequestTypeDef,
    DescribeSubscribedWorkteamResponseTypeDef,
    DescribeTrainingJobRequestRequestTypeDef,
    DescribeTrainingJobResponseTypeDef,
    DescribeTransformJobRequestRequestTypeDef,
    DescribeTransformJobResponseTypeDef,
    DescribeTrialComponentRequestRequestTypeDef,
    DescribeTrialComponentResponseTypeDef,
    DescribeTrialRequestRequestTypeDef,
    DescribeTrialResponseTypeDef,
    DescribeUserProfileRequestRequestTypeDef,
    DescribeUserProfileResponseTypeDef,
    DescribeWorkforceRequestRequestTypeDef,
    DescribeWorkforceResponseTypeDef,
    DescribeWorkteamRequestRequestTypeDef,
    DescribeWorkteamResponseTypeDef,
    DisassociateTrialComponentRequestRequestTypeDef,
    DisassociateTrialComponentResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetDeviceFleetReportRequestRequestTypeDef,
    GetDeviceFleetReportResponseTypeDef,
    GetLineageGroupPolicyRequestRequestTypeDef,
    GetLineageGroupPolicyResponseTypeDef,
    GetModelPackageGroupPolicyInputRequestTypeDef,
    GetModelPackageGroupPolicyOutputTypeDef,
    GetSagemakerServicecatalogPortfolioStatusOutputTypeDef,
    GetScalingConfigurationRecommendationRequestRequestTypeDef,
    GetScalingConfigurationRecommendationResponseTypeDef,
    GetSearchSuggestionsRequestRequestTypeDef,
    GetSearchSuggestionsResponseTypeDef,
    ImportHubContentRequestRequestTypeDef,
    ImportHubContentResponseTypeDef,
    ListActionsRequestRequestTypeDef,
    ListActionsResponseTypeDef,
    ListAlgorithmsInputRequestTypeDef,
    ListAlgorithmsOutputTypeDef,
    ListAliasesRequestRequestTypeDef,
    ListAliasesResponseTypeDef,
    ListAppImageConfigsRequestRequestTypeDef,
    ListAppImageConfigsResponseTypeDef,
    ListAppsRequestRequestTypeDef,
    ListAppsResponseTypeDef,
    ListArtifactsRequestRequestTypeDef,
    ListArtifactsResponseTypeDef,
    ListAssociationsRequestRequestTypeDef,
    ListAssociationsResponseTypeDef,
    ListAutoMLJobsRequestRequestTypeDef,
    ListAutoMLJobsResponseTypeDef,
    ListCandidatesForAutoMLJobRequestRequestTypeDef,
    ListCandidatesForAutoMLJobResponseTypeDef,
    ListClusterNodesRequestRequestTypeDef,
    ListClusterNodesResponseTypeDef,
    ListClustersRequestRequestTypeDef,
    ListClustersResponseTypeDef,
    ListCodeRepositoriesInputRequestTypeDef,
    ListCodeRepositoriesOutputTypeDef,
    ListCompilationJobsRequestRequestTypeDef,
    ListCompilationJobsResponseTypeDef,
    ListContextsRequestRequestTypeDef,
    ListContextsResponseTypeDef,
    ListDataQualityJobDefinitionsRequestRequestTypeDef,
    ListDataQualityJobDefinitionsResponseTypeDef,
    ListDeviceFleetsRequestRequestTypeDef,
    ListDeviceFleetsResponseTypeDef,
    ListDevicesRequestRequestTypeDef,
    ListDevicesResponseTypeDef,
    ListDomainsRequestRequestTypeDef,
    ListDomainsResponseTypeDef,
    ListEdgeDeploymentPlansRequestRequestTypeDef,
    ListEdgeDeploymentPlansResponseTypeDef,
    ListEdgePackagingJobsRequestRequestTypeDef,
    ListEdgePackagingJobsResponseTypeDef,
    ListEndpointConfigsInputRequestTypeDef,
    ListEndpointConfigsOutputTypeDef,
    ListEndpointsInputRequestTypeDef,
    ListEndpointsOutputTypeDef,
    ListExperimentsRequestRequestTypeDef,
    ListExperimentsResponseTypeDef,
    ListFeatureGroupsRequestRequestTypeDef,
    ListFeatureGroupsResponseTypeDef,
    ListFlowDefinitionsRequestRequestTypeDef,
    ListFlowDefinitionsResponseTypeDef,
    ListHubContentsRequestRequestTypeDef,
    ListHubContentsResponseTypeDef,
    ListHubContentVersionsRequestRequestTypeDef,
    ListHubContentVersionsResponseTypeDef,
    ListHubsRequestRequestTypeDef,
    ListHubsResponseTypeDef,
    ListHumanTaskUisRequestRequestTypeDef,
    ListHumanTaskUisResponseTypeDef,
    ListHyperParameterTuningJobsRequestRequestTypeDef,
    ListHyperParameterTuningJobsResponseTypeDef,
    ListImagesRequestRequestTypeDef,
    ListImagesResponseTypeDef,
    ListImageVersionsRequestRequestTypeDef,
    ListImageVersionsResponseTypeDef,
    ListInferenceComponentsInputRequestTypeDef,
    ListInferenceComponentsOutputTypeDef,
    ListInferenceExperimentsRequestRequestTypeDef,
    ListInferenceExperimentsResponseTypeDef,
    ListInferenceRecommendationsJobsRequestRequestTypeDef,
    ListInferenceRecommendationsJobsResponseTypeDef,
    ListInferenceRecommendationsJobStepsRequestRequestTypeDef,
    ListInferenceRecommendationsJobStepsResponseTypeDef,
    ListLabelingJobsForWorkteamRequestRequestTypeDef,
    ListLabelingJobsForWorkteamResponseTypeDef,
    ListLabelingJobsRequestRequestTypeDef,
    ListLabelingJobsResponseTypeDef,
    ListLineageGroupsRequestRequestTypeDef,
    ListLineageGroupsResponseTypeDef,
    ListMlflowTrackingServersRequestRequestTypeDef,
    ListMlflowTrackingServersResponseTypeDef,
    ListModelBiasJobDefinitionsRequestRequestTypeDef,
    ListModelBiasJobDefinitionsResponseTypeDef,
    ListModelCardExportJobsRequestRequestTypeDef,
    ListModelCardExportJobsResponseTypeDef,
    ListModelCardsRequestRequestTypeDef,
    ListModelCardsResponseTypeDef,
    ListModelCardVersionsRequestRequestTypeDef,
    ListModelCardVersionsResponseTypeDef,
    ListModelExplainabilityJobDefinitionsRequestRequestTypeDef,
    ListModelExplainabilityJobDefinitionsResponseTypeDef,
    ListModelMetadataRequestRequestTypeDef,
    ListModelMetadataResponseTypeDef,
    ListModelPackageGroupsInputRequestTypeDef,
    ListModelPackageGroupsOutputTypeDef,
    ListModelPackagesInputRequestTypeDef,
    ListModelPackagesOutputTypeDef,
    ListModelQualityJobDefinitionsRequestRequestTypeDef,
    ListModelQualityJobDefinitionsResponseTypeDef,
    ListModelsInputRequestTypeDef,
    ListModelsOutputTypeDef,
    ListMonitoringAlertHistoryRequestRequestTypeDef,
    ListMonitoringAlertHistoryResponseTypeDef,
    ListMonitoringAlertsRequestRequestTypeDef,
    ListMonitoringAlertsResponseTypeDef,
    ListMonitoringExecutionsRequestRequestTypeDef,
    ListMonitoringExecutionsResponseTypeDef,
    ListMonitoringSchedulesRequestRequestTypeDef,
    ListMonitoringSchedulesResponseTypeDef,
    ListNotebookInstanceLifecycleConfigsInputRequestTypeDef,
    ListNotebookInstanceLifecycleConfigsOutputTypeDef,
    ListNotebookInstancesInputRequestTypeDef,
    ListNotebookInstancesOutputTypeDef,
    ListOptimizationJobsRequestRequestTypeDef,
    ListOptimizationJobsResponseTypeDef,
    ListPipelineExecutionsRequestRequestTypeDef,
    ListPipelineExecutionsResponseTypeDef,
    ListPipelineExecutionStepsRequestRequestTypeDef,
    ListPipelineExecutionStepsResponseTypeDef,
    ListPipelineParametersForExecutionRequestRequestTypeDef,
    ListPipelineParametersForExecutionResponseTypeDef,
    ListPipelinesRequestRequestTypeDef,
    ListPipelinesResponseTypeDef,
    ListProcessingJobsRequestRequestTypeDef,
    ListProcessingJobsResponseTypeDef,
    ListProjectsInputRequestTypeDef,
    ListProjectsOutputTypeDef,
    ListResourceCatalogsRequestRequestTypeDef,
    ListResourceCatalogsResponseTypeDef,
    ListSpacesRequestRequestTypeDef,
    ListSpacesResponseTypeDef,
    ListStageDevicesRequestRequestTypeDef,
    ListStageDevicesResponseTypeDef,
    ListStudioLifecycleConfigsRequestRequestTypeDef,
    ListStudioLifecycleConfigsResponseTypeDef,
    ListSubscribedWorkteamsRequestRequestTypeDef,
    ListSubscribedWorkteamsResponseTypeDef,
    ListTagsInputRequestTypeDef,
    ListTagsOutputTypeDef,
    ListTrainingJobsForHyperParameterTuningJobRequestRequestTypeDef,
    ListTrainingJobsForHyperParameterTuningJobResponseTypeDef,
    ListTrainingJobsRequestRequestTypeDef,
    ListTrainingJobsResponseTypeDef,
    ListTransformJobsRequestRequestTypeDef,
    ListTransformJobsResponseTypeDef,
    ListTrialComponentsRequestRequestTypeDef,
    ListTrialComponentsResponseTypeDef,
    ListTrialsRequestRequestTypeDef,
    ListTrialsResponseTypeDef,
    ListUserProfilesRequestRequestTypeDef,
    ListUserProfilesResponseTypeDef,
    ListWorkforcesRequestRequestTypeDef,
    ListWorkforcesResponseTypeDef,
    ListWorkteamsRequestRequestTypeDef,
    ListWorkteamsResponseTypeDef,
    PutModelPackageGroupPolicyInputRequestTypeDef,
    PutModelPackageGroupPolicyOutputTypeDef,
    QueryLineageRequestRequestTypeDef,
    QueryLineageResponseTypeDef,
    RegisterDevicesRequestRequestTypeDef,
    RenderUiTemplateRequestRequestTypeDef,
    RenderUiTemplateResponseTypeDef,
    RetryPipelineExecutionRequestRequestTypeDef,
    RetryPipelineExecutionResponseTypeDef,
    SearchRequestRequestTypeDef,
    SearchResponseTypeDef,
    SendPipelineExecutionStepFailureRequestRequestTypeDef,
    SendPipelineExecutionStepFailureResponseTypeDef,
    SendPipelineExecutionStepSuccessRequestRequestTypeDef,
    SendPipelineExecutionStepSuccessResponseTypeDef,
    StartEdgeDeploymentStageRequestRequestTypeDef,
    StartInferenceExperimentRequestRequestTypeDef,
    StartInferenceExperimentResponseTypeDef,
    StartMlflowTrackingServerRequestRequestTypeDef,
    StartMlflowTrackingServerResponseTypeDef,
    StartMonitoringScheduleRequestRequestTypeDef,
    StartNotebookInstanceInputRequestTypeDef,
    StartPipelineExecutionRequestRequestTypeDef,
    StartPipelineExecutionResponseTypeDef,
    StopAutoMLJobRequestRequestTypeDef,
    StopCompilationJobRequestRequestTypeDef,
    StopEdgeDeploymentStageRequestRequestTypeDef,
    StopEdgePackagingJobRequestRequestTypeDef,
    StopHyperParameterTuningJobRequestRequestTypeDef,
    StopInferenceExperimentRequestRequestTypeDef,
    StopInferenceExperimentResponseTypeDef,
    StopInferenceRecommendationsJobRequestRequestTypeDef,
    StopLabelingJobRequestRequestTypeDef,
    StopMlflowTrackingServerRequestRequestTypeDef,
    StopMlflowTrackingServerResponseTypeDef,
    StopMonitoringScheduleRequestRequestTypeDef,
    StopNotebookInstanceInputRequestTypeDef,
    StopOptimizationJobRequestRequestTypeDef,
    StopPipelineExecutionRequestRequestTypeDef,
    StopPipelineExecutionResponseTypeDef,
    StopProcessingJobRequestRequestTypeDef,
    StopTrainingJobRequestRequestTypeDef,
    StopTransformJobRequestRequestTypeDef,
    UpdateActionRequestRequestTypeDef,
    UpdateActionResponseTypeDef,
    UpdateAppImageConfigRequestRequestTypeDef,
    UpdateAppImageConfigResponseTypeDef,
    UpdateArtifactRequestRequestTypeDef,
    UpdateArtifactResponseTypeDef,
    UpdateClusterRequestRequestTypeDef,
    UpdateClusterResponseTypeDef,
    UpdateClusterSoftwareRequestRequestTypeDef,
    UpdateClusterSoftwareResponseTypeDef,
    UpdateCodeRepositoryInputRequestTypeDef,
    UpdateCodeRepositoryOutputTypeDef,
    UpdateContextRequestRequestTypeDef,
    UpdateContextResponseTypeDef,
    UpdateDeviceFleetRequestRequestTypeDef,
    UpdateDevicesRequestRequestTypeDef,
    UpdateDomainRequestRequestTypeDef,
    UpdateDomainResponseTypeDef,
    UpdateEndpointInputRequestTypeDef,
    UpdateEndpointOutputTypeDef,
    UpdateEndpointWeightsAndCapacitiesInputRequestTypeDef,
    UpdateEndpointWeightsAndCapacitiesOutputTypeDef,
    UpdateExperimentRequestRequestTypeDef,
    UpdateExperimentResponseTypeDef,
    UpdateFeatureGroupRequestRequestTypeDef,
    UpdateFeatureGroupResponseTypeDef,
    UpdateFeatureMetadataRequestRequestTypeDef,
    UpdateHubRequestRequestTypeDef,
    UpdateHubResponseTypeDef,
    UpdateImageRequestRequestTypeDef,
    UpdateImageResponseTypeDef,
    UpdateImageVersionRequestRequestTypeDef,
    UpdateImageVersionResponseTypeDef,
    UpdateInferenceComponentInputRequestTypeDef,
    UpdateInferenceComponentOutputTypeDef,
    UpdateInferenceComponentRuntimeConfigInputRequestTypeDef,
    UpdateInferenceComponentRuntimeConfigOutputTypeDef,
    UpdateInferenceExperimentRequestRequestTypeDef,
    UpdateInferenceExperimentResponseTypeDef,
    UpdateMlflowTrackingServerRequestRequestTypeDef,
    UpdateMlflowTrackingServerResponseTypeDef,
    UpdateModelCardRequestRequestTypeDef,
    UpdateModelCardResponseTypeDef,
    UpdateModelPackageInputRequestTypeDef,
    UpdateModelPackageOutputTypeDef,
    UpdateMonitoringAlertRequestRequestTypeDef,
    UpdateMonitoringAlertResponseTypeDef,
    UpdateMonitoringScheduleRequestRequestTypeDef,
    UpdateMonitoringScheduleResponseTypeDef,
    UpdateNotebookInstanceInputRequestTypeDef,
    UpdateNotebookInstanceLifecycleConfigInputRequestTypeDef,
    UpdatePipelineExecutionRequestRequestTypeDef,
    UpdatePipelineExecutionResponseTypeDef,
    UpdatePipelineRequestRequestTypeDef,
    UpdatePipelineResponseTypeDef,
    UpdateProjectInputRequestTypeDef,
    UpdateProjectOutputTypeDef,
    UpdateSpaceRequestRequestTypeDef,
    UpdateSpaceResponseTypeDef,
    UpdateTrainingJobRequestRequestTypeDef,
    UpdateTrainingJobResponseTypeDef,
    UpdateTrialComponentRequestRequestTypeDef,
    UpdateTrialComponentResponseTypeDef,
    UpdateTrialRequestRequestTypeDef,
    UpdateTrialResponseTypeDef,
    UpdateUserProfileRequestRequestTypeDef,
    UpdateUserProfileResponseTypeDef,
    UpdateWorkforceRequestRequestTypeDef,
    UpdateWorkforceResponseTypeDef,
    UpdateWorkteamRequestRequestTypeDef,
    UpdateWorkteamResponseTypeDef,
)
from .waiter import (
    EndpointDeletedWaiter,
    EndpointInServiceWaiter,
    ImageCreatedWaiter,
    ImageDeletedWaiter,
    ImageUpdatedWaiter,
    ImageVersionCreatedWaiter,
    ImageVersionDeletedWaiter,
    NotebookInstanceDeletedWaiter,
    NotebookInstanceInServiceWaiter,
    NotebookInstanceStoppedWaiter,
    ProcessingJobCompletedOrStoppedWaiter,
    TrainingJobCompletedOrStoppedWaiter,
    TransformJobCompletedOrStoppedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("SageMakerClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ResourceInUse: Type[BotocoreClientError]
    ResourceLimitExceeded: Type[BotocoreClientError]
    ResourceNotFound: Type[BotocoreClientError]


class SageMakerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SageMakerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#close)
        """

    async def add_association(
        self, **kwargs: Unpack[AddAssociationRequestRequestTypeDef]
    ) -> AddAssociationResponseTypeDef:
        """
        Creates an <i>association</i> between the source and the destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/add_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#add_association)
        """

    async def add_tags(self, **kwargs: Unpack[AddTagsInputRequestTypeDef]) -> AddTagsOutputTypeDef:
        """
        Adds or overwrites one or more tags for the specified SageMaker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/add_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#add_tags)
        """

    async def associate_trial_component(
        self, **kwargs: Unpack[AssociateTrialComponentRequestRequestTypeDef]
    ) -> AssociateTrialComponentResponseTypeDef:
        """
        Associates a trial component with a trial.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/associate_trial_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#associate_trial_component)
        """

    async def batch_describe_model_package(
        self, **kwargs: Unpack[BatchDescribeModelPackageInputRequestTypeDef]
    ) -> BatchDescribeModelPackageOutputTypeDef:
        """
        This action batch describes a list of versioned model packages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/batch_describe_model_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#batch_describe_model_package)
        """

    async def create_action(
        self, **kwargs: Unpack[CreateActionRequestRequestTypeDef]
    ) -> CreateActionResponseTypeDef:
        """
        Creates an <i>action</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_action)
        """

    async def create_algorithm(
        self, **kwargs: Unpack[CreateAlgorithmInputRequestTypeDef]
    ) -> CreateAlgorithmOutputTypeDef:
        """
        Create a machine learning algorithm that you can use in SageMaker and list in
        the Amazon Web Services Marketplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_algorithm.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_algorithm)
        """

    async def create_app(
        self, **kwargs: Unpack[CreateAppRequestRequestTypeDef]
    ) -> CreateAppResponseTypeDef:
        """
        Creates a running app for the specified UserProfile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_app)
        """

    async def create_app_image_config(
        self, **kwargs: Unpack[CreateAppImageConfigRequestRequestTypeDef]
    ) -> CreateAppImageConfigResponseTypeDef:
        """
        Creates a configuration for running a SageMaker image as a KernelGateway app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_app_image_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_app_image_config)
        """

    async def create_artifact(
        self, **kwargs: Unpack[CreateArtifactRequestRequestTypeDef]
    ) -> CreateArtifactResponseTypeDef:
        """
        Creates an <i>artifact</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_artifact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_artifact)
        """

    async def create_auto_ml_job(
        self, **kwargs: Unpack[CreateAutoMLJobRequestRequestTypeDef]
    ) -> CreateAutoMLJobResponseTypeDef:
        """
        Creates an Autopilot job also referred to as Autopilot experiment or AutoML job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_auto_ml_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_auto_ml_job)
        """

    async def create_auto_ml_job_v2(
        self, **kwargs: Unpack[CreateAutoMLJobV2RequestRequestTypeDef]
    ) -> CreateAutoMLJobV2ResponseTypeDef:
        """
        Creates an Autopilot job also referred to as Autopilot experiment or AutoML job
        V2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_auto_ml_job_v2.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_auto_ml_job_v2)
        """

    async def create_cluster(
        self, **kwargs: Unpack[CreateClusterRequestRequestTypeDef]
    ) -> CreateClusterResponseTypeDef:
        """
        Creates a SageMaker HyperPod cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_cluster)
        """

    async def create_code_repository(
        self, **kwargs: Unpack[CreateCodeRepositoryInputRequestTypeDef]
    ) -> CreateCodeRepositoryOutputTypeDef:
        """
        Creates a Git repository as a resource in your SageMaker account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_code_repository.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_code_repository)
        """

    async def create_compilation_job(
        self, **kwargs: Unpack[CreateCompilationJobRequestRequestTypeDef]
    ) -> CreateCompilationJobResponseTypeDef:
        """
        Starts a model compilation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_compilation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_compilation_job)
        """

    async def create_context(
        self, **kwargs: Unpack[CreateContextRequestRequestTypeDef]
    ) -> CreateContextResponseTypeDef:
        """
        Creates a <i>context</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_context.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_context)
        """

    async def create_data_quality_job_definition(
        self, **kwargs: Unpack[CreateDataQualityJobDefinitionRequestRequestTypeDef]
    ) -> CreateDataQualityJobDefinitionResponseTypeDef:
        """
        Creates a definition for a job that monitors data quality and drift.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_data_quality_job_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_data_quality_job_definition)
        """

    async def create_device_fleet(
        self, **kwargs: Unpack[CreateDeviceFleetRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a device fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_device_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_device_fleet)
        """

    async def create_domain(
        self, **kwargs: Unpack[CreateDomainRequestRequestTypeDef]
    ) -> CreateDomainResponseTypeDef:
        """
        Creates a <code>Domain</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_domain)
        """

    async def create_edge_deployment_plan(
        self, **kwargs: Unpack[CreateEdgeDeploymentPlanRequestRequestTypeDef]
    ) -> CreateEdgeDeploymentPlanResponseTypeDef:
        """
        Creates an edge deployment plan, consisting of multiple stages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_edge_deployment_plan.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_edge_deployment_plan)
        """

    async def create_edge_deployment_stage(
        self, **kwargs: Unpack[CreateEdgeDeploymentStageRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a new stage in an existing edge deployment plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_edge_deployment_stage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_edge_deployment_stage)
        """

    async def create_edge_packaging_job(
        self, **kwargs: Unpack[CreateEdgePackagingJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a SageMaker Edge Manager model packaging job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_edge_packaging_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_edge_packaging_job)
        """

    async def create_endpoint(
        self, **kwargs: Unpack[CreateEndpointInputRequestTypeDef]
    ) -> CreateEndpointOutputTypeDef:
        """
        Creates an endpoint using the endpoint configuration specified in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_endpoint)
        """

    async def create_endpoint_config(
        self, **kwargs: Unpack[CreateEndpointConfigInputRequestTypeDef]
    ) -> CreateEndpointConfigOutputTypeDef:
        """
        Creates an endpoint configuration that SageMaker hosting services uses to
        deploy models.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_endpoint_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_endpoint_config)
        """

    async def create_experiment(
        self, **kwargs: Unpack[CreateExperimentRequestRequestTypeDef]
    ) -> CreateExperimentResponseTypeDef:
        """
        Creates a SageMaker <i>experiment</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_experiment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_experiment)
        """

    async def create_feature_group(
        self, **kwargs: Unpack[CreateFeatureGroupRequestRequestTypeDef]
    ) -> CreateFeatureGroupResponseTypeDef:
        """
        Create a new <code>FeatureGroup</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_feature_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_feature_group)
        """

    async def create_flow_definition(
        self, **kwargs: Unpack[CreateFlowDefinitionRequestRequestTypeDef]
    ) -> CreateFlowDefinitionResponseTypeDef:
        """
        Creates a flow definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_flow_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_flow_definition)
        """

    async def create_hub(
        self, **kwargs: Unpack[CreateHubRequestRequestTypeDef]
    ) -> CreateHubResponseTypeDef:
        """
        Create a hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_hub.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_hub)
        """

    async def create_hub_content_reference(
        self, **kwargs: Unpack[CreateHubContentReferenceRequestRequestTypeDef]
    ) -> CreateHubContentReferenceResponseTypeDef:
        """
        Create a hub content reference in order to add a model in the JumpStart public
        hub to a private hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_hub_content_reference.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_hub_content_reference)
        """

    async def create_human_task_ui(
        self, **kwargs: Unpack[CreateHumanTaskUiRequestRequestTypeDef]
    ) -> CreateHumanTaskUiResponseTypeDef:
        """
        Defines the settings you will use for the human review workflow user interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_human_task_ui.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_human_task_ui)
        """

    async def create_hyper_parameter_tuning_job(
        self, **kwargs: Unpack[CreateHyperParameterTuningJobRequestRequestTypeDef]
    ) -> CreateHyperParameterTuningJobResponseTypeDef:
        """
        Starts a hyperparameter tuning job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_hyper_parameter_tuning_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_hyper_parameter_tuning_job)
        """

    async def create_image(
        self, **kwargs: Unpack[CreateImageRequestRequestTypeDef]
    ) -> CreateImageResponseTypeDef:
        """
        Creates a custom SageMaker image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_image)
        """

    async def create_image_version(
        self, **kwargs: Unpack[CreateImageVersionRequestRequestTypeDef]
    ) -> CreateImageVersionResponseTypeDef:
        """
        Creates a version of the SageMaker image specified by <code>ImageName</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_image_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_image_version)
        """

    async def create_inference_component(
        self, **kwargs: Unpack[CreateInferenceComponentInputRequestTypeDef]
    ) -> CreateInferenceComponentOutputTypeDef:
        """
        Creates an inference component, which is a SageMaker hosting object that you
        can use to deploy a model to an endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_inference_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_inference_component)
        """

    async def create_inference_experiment(
        self, **kwargs: Unpack[CreateInferenceExperimentRequestRequestTypeDef]
    ) -> CreateInferenceExperimentResponseTypeDef:
        """
        Creates an inference experiment using the configurations specified in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_inference_experiment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_inference_experiment)
        """

    async def create_inference_recommendations_job(
        self, **kwargs: Unpack[CreateInferenceRecommendationsJobRequestRequestTypeDef]
    ) -> CreateInferenceRecommendationsJobResponseTypeDef:
        """
        Starts a recommendation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_inference_recommendations_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_inference_recommendations_job)
        """

    async def create_labeling_job(
        self, **kwargs: Unpack[CreateLabelingJobRequestRequestTypeDef]
    ) -> CreateLabelingJobResponseTypeDef:
        """
        Creates a job that uses workers to label the data objects in your input dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_labeling_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_labeling_job)
        """

    async def create_mlflow_tracking_server(
        self, **kwargs: Unpack[CreateMlflowTrackingServerRequestRequestTypeDef]
    ) -> CreateMlflowTrackingServerResponseTypeDef:
        """
        Creates an MLflow Tracking Server using a general purpose Amazon S3 bucket as
        the artifact store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_mlflow_tracking_server.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_mlflow_tracking_server)
        """

    async def create_model(
        self, **kwargs: Unpack[CreateModelInputRequestTypeDef]
    ) -> CreateModelOutputTypeDef:
        """
        Creates a model in SageMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_model)
        """

    async def create_model_bias_job_definition(
        self, **kwargs: Unpack[CreateModelBiasJobDefinitionRequestRequestTypeDef]
    ) -> CreateModelBiasJobDefinitionResponseTypeDef:
        """
        Creates the definition for a model bias job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_model_bias_job_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_model_bias_job_definition)
        """

    async def create_model_card(
        self, **kwargs: Unpack[CreateModelCardRequestRequestTypeDef]
    ) -> CreateModelCardResponseTypeDef:
        """
        Creates an Amazon SageMaker Model Card.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_model_card.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_model_card)
        """

    async def create_model_card_export_job(
        self, **kwargs: Unpack[CreateModelCardExportJobRequestRequestTypeDef]
    ) -> CreateModelCardExportJobResponseTypeDef:
        """
        Creates an Amazon SageMaker Model Card export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_model_card_export_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_model_card_export_job)
        """

    async def create_model_explainability_job_definition(
        self, **kwargs: Unpack[CreateModelExplainabilityJobDefinitionRequestRequestTypeDef]
    ) -> CreateModelExplainabilityJobDefinitionResponseTypeDef:
        """
        Creates the definition for a model explainability job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_model_explainability_job_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_model_explainability_job_definition)
        """

    async def create_model_package(
        self, **kwargs: Unpack[CreateModelPackageInputRequestTypeDef]
    ) -> CreateModelPackageOutputTypeDef:
        """
        Creates a model package that you can use to create SageMaker models or list on
        Amazon Web Services Marketplace, or a versioned model that is part of a model
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_model_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_model_package)
        """

    async def create_model_package_group(
        self, **kwargs: Unpack[CreateModelPackageGroupInputRequestTypeDef]
    ) -> CreateModelPackageGroupOutputTypeDef:
        """
        Creates a model group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_model_package_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_model_package_group)
        """

    async def create_model_quality_job_definition(
        self, **kwargs: Unpack[CreateModelQualityJobDefinitionRequestRequestTypeDef]
    ) -> CreateModelQualityJobDefinitionResponseTypeDef:
        """
        Creates a definition for a job that monitors model quality and drift.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_model_quality_job_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_model_quality_job_definition)
        """

    async def create_monitoring_schedule(
        self, **kwargs: Unpack[CreateMonitoringScheduleRequestRequestTypeDef]
    ) -> CreateMonitoringScheduleResponseTypeDef:
        """
        Creates a schedule that regularly starts Amazon SageMaker Processing Jobs to
        monitor the data captured for an Amazon SageMaker Endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_monitoring_schedule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_monitoring_schedule)
        """

    async def create_notebook_instance(
        self, **kwargs: Unpack[CreateNotebookInstanceInputRequestTypeDef]
    ) -> CreateNotebookInstanceOutputTypeDef:
        """
        Creates an SageMaker notebook instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_notebook_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_notebook_instance)
        """

    async def create_notebook_instance_lifecycle_config(
        self, **kwargs: Unpack[CreateNotebookInstanceLifecycleConfigInputRequestTypeDef]
    ) -> CreateNotebookInstanceLifecycleConfigOutputTypeDef:
        """
        Creates a lifecycle configuration that you can associate with a notebook
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_notebook_instance_lifecycle_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_notebook_instance_lifecycle_config)
        """

    async def create_optimization_job(
        self, **kwargs: Unpack[CreateOptimizationJobRequestRequestTypeDef]
    ) -> CreateOptimizationJobResponseTypeDef:
        """
        Creates a job that optimizes a model for inference performance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_optimization_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_optimization_job)
        """

    async def create_pipeline(
        self, **kwargs: Unpack[CreatePipelineRequestRequestTypeDef]
    ) -> CreatePipelineResponseTypeDef:
        """
        Creates a pipeline using a JSON pipeline definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_pipeline)
        """

    async def create_presigned_domain_url(
        self, **kwargs: Unpack[CreatePresignedDomainUrlRequestRequestTypeDef]
    ) -> CreatePresignedDomainUrlResponseTypeDef:
        """
        Creates a URL for a specified UserProfile in a Domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_presigned_domain_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_presigned_domain_url)
        """

    async def create_presigned_mlflow_tracking_server_url(
        self, **kwargs: Unpack[CreatePresignedMlflowTrackingServerUrlRequestRequestTypeDef]
    ) -> CreatePresignedMlflowTrackingServerUrlResponseTypeDef:
        """
        Returns a presigned URL that you can use to connect to the MLflow UI attached
        to your tracking server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_presigned_mlflow_tracking_server_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_presigned_mlflow_tracking_server_url)
        """

    async def create_presigned_notebook_instance_url(
        self, **kwargs: Unpack[CreatePresignedNotebookInstanceUrlInputRequestTypeDef]
    ) -> CreatePresignedNotebookInstanceUrlOutputTypeDef:
        """
        Returns a URL that you can use to connect to the Jupyter server from a notebook
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_presigned_notebook_instance_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_presigned_notebook_instance_url)
        """

    async def create_processing_job(
        self, **kwargs: Unpack[CreateProcessingJobRequestRequestTypeDef]
    ) -> CreateProcessingJobResponseTypeDef:
        """
        Creates a processing job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_processing_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_processing_job)
        """

    async def create_project(
        self, **kwargs: Unpack[CreateProjectInputRequestTypeDef]
    ) -> CreateProjectOutputTypeDef:
        """
        Creates a machine learning (ML) project that can contain one or more templates
        that set up an ML pipeline from training to deploying an approved model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_project.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_project)
        """

    async def create_space(
        self, **kwargs: Unpack[CreateSpaceRequestRequestTypeDef]
    ) -> CreateSpaceResponseTypeDef:
        """
        Creates a private space or a space used for real time collaboration in a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_space.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_space)
        """

    async def create_studio_lifecycle_config(
        self, **kwargs: Unpack[CreateStudioLifecycleConfigRequestRequestTypeDef]
    ) -> CreateStudioLifecycleConfigResponseTypeDef:
        """
        Creates a new Amazon SageMaker Studio Lifecycle Configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_studio_lifecycle_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_studio_lifecycle_config)
        """

    async def create_training_job(
        self, **kwargs: Unpack[CreateTrainingJobRequestRequestTypeDef]
    ) -> CreateTrainingJobResponseTypeDef:
        """
        Starts a model training job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_training_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_training_job)
        """

    async def create_transform_job(
        self, **kwargs: Unpack[CreateTransformJobRequestRequestTypeDef]
    ) -> CreateTransformJobResponseTypeDef:
        """
        Starts a transform job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_transform_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_transform_job)
        """

    async def create_trial(
        self, **kwargs: Unpack[CreateTrialRequestRequestTypeDef]
    ) -> CreateTrialResponseTypeDef:
        """
        Creates an SageMaker <i>trial</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_trial.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_trial)
        """

    async def create_trial_component(
        self, **kwargs: Unpack[CreateTrialComponentRequestRequestTypeDef]
    ) -> CreateTrialComponentResponseTypeDef:
        """
        Creates a <i>trial component</i>, which is a stage of a machine learning
        <i>trial</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_trial_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_trial_component)
        """

    async def create_user_profile(
        self, **kwargs: Unpack[CreateUserProfileRequestRequestTypeDef]
    ) -> CreateUserProfileResponseTypeDef:
        """
        Creates a user profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_user_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_user_profile)
        """

    async def create_workforce(
        self, **kwargs: Unpack[CreateWorkforceRequestRequestTypeDef]
    ) -> CreateWorkforceResponseTypeDef:
        """
        Use this operation to create a workforce.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_workforce.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_workforce)
        """

    async def create_workteam(
        self, **kwargs: Unpack[CreateWorkteamRequestRequestTypeDef]
    ) -> CreateWorkteamResponseTypeDef:
        """
        Creates a new work team for labeling your data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_workteam.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#create_workteam)
        """

    async def delete_action(
        self, **kwargs: Unpack[DeleteActionRequestRequestTypeDef]
    ) -> DeleteActionResponseTypeDef:
        """
        Deletes an action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_action)
        """

    async def delete_algorithm(
        self, **kwargs: Unpack[DeleteAlgorithmInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified algorithm from your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_algorithm.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_algorithm)
        """

    async def delete_app(
        self, **kwargs: Unpack[DeleteAppRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used to stop and delete an app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_app)
        """

    async def delete_app_image_config(
        self, **kwargs: Unpack[DeleteAppImageConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an AppImageConfig.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_app_image_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_app_image_config)
        """

    async def delete_artifact(
        self, **kwargs: Unpack[DeleteArtifactRequestRequestTypeDef]
    ) -> DeleteArtifactResponseTypeDef:
        """
        Deletes an artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_artifact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_artifact)
        """

    async def delete_association(
        self, **kwargs: Unpack[DeleteAssociationRequestRequestTypeDef]
    ) -> DeleteAssociationResponseTypeDef:
        """
        Deletes an association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_association)
        """

    async def delete_cluster(
        self, **kwargs: Unpack[DeleteClusterRequestRequestTypeDef]
    ) -> DeleteClusterResponseTypeDef:
        """
        Delete a SageMaker HyperPod cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_cluster)
        """

    async def delete_code_repository(
        self, **kwargs: Unpack[DeleteCodeRepositoryInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Git repository from your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_code_repository.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_code_repository)
        """

    async def delete_compilation_job(
        self, **kwargs: Unpack[DeleteCompilationJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified compilation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_compilation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_compilation_job)
        """

    async def delete_context(
        self, **kwargs: Unpack[DeleteContextRequestRequestTypeDef]
    ) -> DeleteContextResponseTypeDef:
        """
        Deletes an context.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_context.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_context)
        """

    async def delete_data_quality_job_definition(
        self, **kwargs: Unpack[DeleteDataQualityJobDefinitionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a data quality monitoring job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_data_quality_job_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_data_quality_job_definition)
        """

    async def delete_device_fleet(
        self, **kwargs: Unpack[DeleteDeviceFleetRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_device_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_device_fleet)
        """

    async def delete_domain(
        self, **kwargs: Unpack[DeleteDomainRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used to delete a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_domain)
        """

    async def delete_edge_deployment_plan(
        self, **kwargs: Unpack[DeleteEdgeDeploymentPlanRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an edge deployment plan if (and only if) all the stages in the plan are
        inactive or there are no stages in the plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_edge_deployment_plan.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_edge_deployment_plan)
        """

    async def delete_edge_deployment_stage(
        self, **kwargs: Unpack[DeleteEdgeDeploymentStageRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a stage in an edge deployment plan if (and only if) the stage is
        inactive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_edge_deployment_stage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_edge_deployment_stage)
        """

    async def delete_endpoint(
        self, **kwargs: Unpack[DeleteEndpointInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_endpoint)
        """

    async def delete_endpoint_config(
        self, **kwargs: Unpack[DeleteEndpointConfigInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an endpoint configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_endpoint_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_endpoint_config)
        """

    async def delete_experiment(
        self, **kwargs: Unpack[DeleteExperimentRequestRequestTypeDef]
    ) -> DeleteExperimentResponseTypeDef:
        """
        Deletes an SageMaker experiment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_experiment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_experiment)
        """

    async def delete_feature_group(
        self, **kwargs: Unpack[DeleteFeatureGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete the <code>FeatureGroup</code> and any data that was written to the
        <code>OnlineStore</code> of the <code>FeatureGroup</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_feature_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_feature_group)
        """

    async def delete_flow_definition(
        self, **kwargs: Unpack[DeleteFlowDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified flow definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_flow_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_flow_definition)
        """

    async def delete_hub(
        self, **kwargs: Unpack[DeleteHubRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_hub.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_hub)
        """

    async def delete_hub_content(
        self, **kwargs: Unpack[DeleteHubContentRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete the contents of a hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_hub_content.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_hub_content)
        """

    async def delete_hub_content_reference(
        self, **kwargs: Unpack[DeleteHubContentReferenceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a hub content reference in order to remove a model from a private hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_hub_content_reference.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_hub_content_reference)
        """

    async def delete_human_task_ui(
        self, **kwargs: Unpack[DeleteHumanTaskUiRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Use this operation to delete a human task user interface (worker task template).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_human_task_ui.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_human_task_ui)
        """

    async def delete_hyper_parameter_tuning_job(
        self, **kwargs: Unpack[DeleteHyperParameterTuningJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a hyperparameter tuning job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_hyper_parameter_tuning_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_hyper_parameter_tuning_job)
        """

    async def delete_image(
        self, **kwargs: Unpack[DeleteImageRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a SageMaker image and all versions of the image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_image)
        """

    async def delete_image_version(
        self, **kwargs: Unpack[DeleteImageVersionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a version of a SageMaker image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_image_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_image_version)
        """

    async def delete_inference_component(
        self, **kwargs: Unpack[DeleteInferenceComponentInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an inference component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_inference_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_inference_component)
        """

    async def delete_inference_experiment(
        self, **kwargs: Unpack[DeleteInferenceExperimentRequestRequestTypeDef]
    ) -> DeleteInferenceExperimentResponseTypeDef:
        """
        Deletes an inference experiment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_inference_experiment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_inference_experiment)
        """

    async def delete_mlflow_tracking_server(
        self, **kwargs: Unpack[DeleteMlflowTrackingServerRequestRequestTypeDef]
    ) -> DeleteMlflowTrackingServerResponseTypeDef:
        """
        Deletes an MLflow Tracking Server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_mlflow_tracking_server.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_mlflow_tracking_server)
        """

    async def delete_model(
        self, **kwargs: Unpack[DeleteModelInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_model)
        """

    async def delete_model_bias_job_definition(
        self, **kwargs: Unpack[DeleteModelBiasJobDefinitionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon SageMaker model bias job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_model_bias_job_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_model_bias_job_definition)
        """

    async def delete_model_card(
        self, **kwargs: Unpack[DeleteModelCardRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon SageMaker Model Card.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_model_card.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_model_card)
        """

    async def delete_model_explainability_job_definition(
        self, **kwargs: Unpack[DeleteModelExplainabilityJobDefinitionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon SageMaker model explainability job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_model_explainability_job_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_model_explainability_job_definition)
        """

    async def delete_model_package(
        self, **kwargs: Unpack[DeleteModelPackageInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a model package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_model_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_model_package)
        """

    async def delete_model_package_group(
        self, **kwargs: Unpack[DeleteModelPackageGroupInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified model group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_model_package_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_model_package_group)
        """

    async def delete_model_package_group_policy(
        self, **kwargs: Unpack[DeleteModelPackageGroupPolicyInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a model group resource policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_model_package_group_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_model_package_group_policy)
        """

    async def delete_model_quality_job_definition(
        self, **kwargs: Unpack[DeleteModelQualityJobDefinitionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the secified model quality monitoring job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_model_quality_job_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_model_quality_job_definition)
        """

    async def delete_monitoring_schedule(
        self, **kwargs: Unpack[DeleteMonitoringScheduleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a monitoring schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_monitoring_schedule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_monitoring_schedule)
        """

    async def delete_notebook_instance(
        self, **kwargs: Unpack[DeleteNotebookInstanceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an SageMaker notebook instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_notebook_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_notebook_instance)
        """

    async def delete_notebook_instance_lifecycle_config(
        self, **kwargs: Unpack[DeleteNotebookInstanceLifecycleConfigInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a notebook instance lifecycle configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_notebook_instance_lifecycle_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_notebook_instance_lifecycle_config)
        """

    async def delete_optimization_job(
        self, **kwargs: Unpack[DeleteOptimizationJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an optimization job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_optimization_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_optimization_job)
        """

    async def delete_pipeline(
        self, **kwargs: Unpack[DeletePipelineRequestRequestTypeDef]
    ) -> DeletePipelineResponseTypeDef:
        """
        Deletes a pipeline if there are no running instances of the pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_pipeline)
        """

    async def delete_project(
        self, **kwargs: Unpack[DeleteProjectInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete the specified project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_project.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_project)
        """

    async def delete_space(
        self, **kwargs: Unpack[DeleteSpaceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used to delete a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_space.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_space)
        """

    async def delete_studio_lifecycle_config(
        self, **kwargs: Unpack[DeleteStudioLifecycleConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the Amazon SageMaker Studio Lifecycle Configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_studio_lifecycle_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_studio_lifecycle_config)
        """

    async def delete_tags(self, **kwargs: Unpack[DeleteTagsInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified tags from an SageMaker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_tags)
        """

    async def delete_trial(
        self, **kwargs: Unpack[DeleteTrialRequestRequestTypeDef]
    ) -> DeleteTrialResponseTypeDef:
        """
        Deletes the specified trial.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_trial.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_trial)
        """

    async def delete_trial_component(
        self, **kwargs: Unpack[DeleteTrialComponentRequestRequestTypeDef]
    ) -> DeleteTrialComponentResponseTypeDef:
        """
        Deletes the specified trial component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_trial_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_trial_component)
        """

    async def delete_user_profile(
        self, **kwargs: Unpack[DeleteUserProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a user profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_user_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_user_profile)
        """

    async def delete_workforce(
        self, **kwargs: Unpack[DeleteWorkforceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Use this operation to delete a workforce.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_workforce.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_workforce)
        """

    async def delete_workteam(
        self, **kwargs: Unpack[DeleteWorkteamRequestRequestTypeDef]
    ) -> DeleteWorkteamResponseTypeDef:
        """
        Deletes an existing work team.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/delete_workteam.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#delete_workteam)
        """

    async def deregister_devices(
        self, **kwargs: Unpack[DeregisterDevicesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters the specified devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/deregister_devices.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#deregister_devices)
        """

    async def describe_action(
        self, **kwargs: Unpack[DescribeActionRequestRequestTypeDef]
    ) -> DescribeActionResponseTypeDef:
        """
        Describes an action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_action)
        """

    async def describe_algorithm(
        self, **kwargs: Unpack[DescribeAlgorithmInputRequestTypeDef]
    ) -> DescribeAlgorithmOutputTypeDef:
        """
        Returns a description of the specified algorithm that is in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_algorithm.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_algorithm)
        """

    async def describe_app(
        self, **kwargs: Unpack[DescribeAppRequestRequestTypeDef]
    ) -> DescribeAppResponseTypeDef:
        """
        Describes the app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_app.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_app)
        """

    async def describe_app_image_config(
        self, **kwargs: Unpack[DescribeAppImageConfigRequestRequestTypeDef]
    ) -> DescribeAppImageConfigResponseTypeDef:
        """
        Describes an AppImageConfig.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_app_image_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_app_image_config)
        """

    async def describe_artifact(
        self, **kwargs: Unpack[DescribeArtifactRequestRequestTypeDef]
    ) -> DescribeArtifactResponseTypeDef:
        """
        Describes an artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_artifact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_artifact)
        """

    async def describe_auto_ml_job(
        self, **kwargs: Unpack[DescribeAutoMLJobRequestRequestTypeDef]
    ) -> DescribeAutoMLJobResponseTypeDef:
        """
        Returns information about an AutoML job created by calling <a
        href="https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateAutoMLJob.html">CreateAutoMLJob</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_auto_ml_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_auto_ml_job)
        """

    async def describe_auto_ml_job_v2(
        self, **kwargs: Unpack[DescribeAutoMLJobV2RequestRequestTypeDef]
    ) -> DescribeAutoMLJobV2ResponseTypeDef:
        """
        Returns information about an AutoML job created by calling <a
        href="https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateAutoMLJobV2.html">CreateAutoMLJobV2</a>
        or <a
        href="https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateAutoMLJob.html">CreateAutoMLJob</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_auto_ml_job_v2.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_auto_ml_job_v2)
        """

    async def describe_cluster(
        self, **kwargs: Unpack[DescribeClusterRequestRequestTypeDef]
    ) -> DescribeClusterResponseTypeDef:
        """
        Retrieves information of a SageMaker HyperPod cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_cluster)
        """

    async def describe_cluster_node(
        self, **kwargs: Unpack[DescribeClusterNodeRequestRequestTypeDef]
    ) -> DescribeClusterNodeResponseTypeDef:
        """
        Retrieves information of a node (also called a <i>instance</i> interchangeably)
        of a SageMaker HyperPod cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_cluster_node.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_cluster_node)
        """

    async def describe_code_repository(
        self, **kwargs: Unpack[DescribeCodeRepositoryInputRequestTypeDef]
    ) -> DescribeCodeRepositoryOutputTypeDef:
        """
        Gets details about the specified Git repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_code_repository.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_code_repository)
        """

    async def describe_compilation_job(
        self, **kwargs: Unpack[DescribeCompilationJobRequestRequestTypeDef]
    ) -> DescribeCompilationJobResponseTypeDef:
        """
        Returns information about a model compilation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_compilation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_compilation_job)
        """

    async def describe_context(
        self, **kwargs: Unpack[DescribeContextRequestRequestTypeDef]
    ) -> DescribeContextResponseTypeDef:
        """
        Describes a context.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_context.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_context)
        """

    async def describe_data_quality_job_definition(
        self, **kwargs: Unpack[DescribeDataQualityJobDefinitionRequestRequestTypeDef]
    ) -> DescribeDataQualityJobDefinitionResponseTypeDef:
        """
        Gets the details of a data quality monitoring job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_data_quality_job_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_data_quality_job_definition)
        """

    async def describe_device(
        self, **kwargs: Unpack[DescribeDeviceRequestRequestTypeDef]
    ) -> DescribeDeviceResponseTypeDef:
        """
        Describes the device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_device.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_device)
        """

    async def describe_device_fleet(
        self, **kwargs: Unpack[DescribeDeviceFleetRequestRequestTypeDef]
    ) -> DescribeDeviceFleetResponseTypeDef:
        """
        A description of the fleet the device belongs to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_device_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_device_fleet)
        """

    async def describe_domain(
        self, **kwargs: Unpack[DescribeDomainRequestRequestTypeDef]
    ) -> DescribeDomainResponseTypeDef:
        """
        The description of the domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_domain)
        """

    async def describe_edge_deployment_plan(
        self, **kwargs: Unpack[DescribeEdgeDeploymentPlanRequestRequestTypeDef]
    ) -> DescribeEdgeDeploymentPlanResponseTypeDef:
        """
        Describes an edge deployment plan with deployment status per stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_edge_deployment_plan.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_edge_deployment_plan)
        """

    async def describe_edge_packaging_job(
        self, **kwargs: Unpack[DescribeEdgePackagingJobRequestRequestTypeDef]
    ) -> DescribeEdgePackagingJobResponseTypeDef:
        """
        A description of edge packaging jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_edge_packaging_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_edge_packaging_job)
        """

    async def describe_endpoint(
        self, **kwargs: Unpack[DescribeEndpointInputRequestTypeDef]
    ) -> DescribeEndpointOutputTypeDef:
        """
        Returns the description of an endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_endpoint)
        """

    async def describe_endpoint_config(
        self, **kwargs: Unpack[DescribeEndpointConfigInputRequestTypeDef]
    ) -> DescribeEndpointConfigOutputTypeDef:
        """
        Returns the description of an endpoint configuration created using the
        <code>CreateEndpointConfig</code> API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_endpoint_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_endpoint_config)
        """

    async def describe_experiment(
        self, **kwargs: Unpack[DescribeExperimentRequestRequestTypeDef]
    ) -> DescribeExperimentResponseTypeDef:
        """
        Provides a list of an experiment's properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_experiment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_experiment)
        """

    async def describe_feature_group(
        self, **kwargs: Unpack[DescribeFeatureGroupRequestRequestTypeDef]
    ) -> DescribeFeatureGroupResponseTypeDef:
        """
        Use this operation to describe a <code>FeatureGroup</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_feature_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_feature_group)
        """

    async def describe_feature_metadata(
        self, **kwargs: Unpack[DescribeFeatureMetadataRequestRequestTypeDef]
    ) -> DescribeFeatureMetadataResponseTypeDef:
        """
        Shows the metadata for a feature within a feature group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_feature_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_feature_metadata)
        """

    async def describe_flow_definition(
        self, **kwargs: Unpack[DescribeFlowDefinitionRequestRequestTypeDef]
    ) -> DescribeFlowDefinitionResponseTypeDef:
        """
        Returns information about the specified flow definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_flow_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_flow_definition)
        """

    async def describe_hub(
        self, **kwargs: Unpack[DescribeHubRequestRequestTypeDef]
    ) -> DescribeHubResponseTypeDef:
        """
        Describes a hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_hub.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_hub)
        """

    async def describe_hub_content(
        self, **kwargs: Unpack[DescribeHubContentRequestRequestTypeDef]
    ) -> DescribeHubContentResponseTypeDef:
        """
        Describe the content of a hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_hub_content.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_hub_content)
        """

    async def describe_human_task_ui(
        self, **kwargs: Unpack[DescribeHumanTaskUiRequestRequestTypeDef]
    ) -> DescribeHumanTaskUiResponseTypeDef:
        """
        Returns information about the requested human task user interface (worker task
        template).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_human_task_ui.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_human_task_ui)
        """

    async def describe_hyper_parameter_tuning_job(
        self, **kwargs: Unpack[DescribeHyperParameterTuningJobRequestRequestTypeDef]
    ) -> DescribeHyperParameterTuningJobResponseTypeDef:
        """
        Returns a description of a hyperparameter tuning job, depending on the fields
        selected.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_hyper_parameter_tuning_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_hyper_parameter_tuning_job)
        """

    async def describe_image(
        self, **kwargs: Unpack[DescribeImageRequestRequestTypeDef]
    ) -> DescribeImageResponseTypeDef:
        """
        Describes a SageMaker image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_image)
        """

    async def describe_image_version(
        self, **kwargs: Unpack[DescribeImageVersionRequestRequestTypeDef]
    ) -> DescribeImageVersionResponseTypeDef:
        """
        Describes a version of a SageMaker image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_image_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_image_version)
        """

    async def describe_inference_component(
        self, **kwargs: Unpack[DescribeInferenceComponentInputRequestTypeDef]
    ) -> DescribeInferenceComponentOutputTypeDef:
        """
        Returns information about an inference component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_inference_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_inference_component)
        """

    async def describe_inference_experiment(
        self, **kwargs: Unpack[DescribeInferenceExperimentRequestRequestTypeDef]
    ) -> DescribeInferenceExperimentResponseTypeDef:
        """
        Returns details about an inference experiment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_inference_experiment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_inference_experiment)
        """

    async def describe_inference_recommendations_job(
        self, **kwargs: Unpack[DescribeInferenceRecommendationsJobRequestRequestTypeDef]
    ) -> DescribeInferenceRecommendationsJobResponseTypeDef:
        """
        Provides the results of the Inference Recommender job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_inference_recommendations_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_inference_recommendations_job)
        """

    async def describe_labeling_job(
        self, **kwargs: Unpack[DescribeLabelingJobRequestRequestTypeDef]
    ) -> DescribeLabelingJobResponseTypeDef:
        """
        Gets information about a labeling job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_labeling_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_labeling_job)
        """

    async def describe_lineage_group(
        self, **kwargs: Unpack[DescribeLineageGroupRequestRequestTypeDef]
    ) -> DescribeLineageGroupResponseTypeDef:
        """
        Provides a list of properties for the requested lineage group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_lineage_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_lineage_group)
        """

    async def describe_mlflow_tracking_server(
        self, **kwargs: Unpack[DescribeMlflowTrackingServerRequestRequestTypeDef]
    ) -> DescribeMlflowTrackingServerResponseTypeDef:
        """
        Returns information about an MLflow Tracking Server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_mlflow_tracking_server.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_mlflow_tracking_server)
        """

    async def describe_model(
        self, **kwargs: Unpack[DescribeModelInputRequestTypeDef]
    ) -> DescribeModelOutputTypeDef:
        """
        Describes a model that you created using the <code>CreateModel</code> API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_model)
        """

    async def describe_model_bias_job_definition(
        self, **kwargs: Unpack[DescribeModelBiasJobDefinitionRequestRequestTypeDef]
    ) -> DescribeModelBiasJobDefinitionResponseTypeDef:
        """
        Returns a description of a model bias job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_model_bias_job_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_model_bias_job_definition)
        """

    async def describe_model_card(
        self, **kwargs: Unpack[DescribeModelCardRequestRequestTypeDef]
    ) -> DescribeModelCardResponseTypeDef:
        """
        Describes the content, creation time, and security configuration of an Amazon
        SageMaker Model Card.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_model_card.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_model_card)
        """

    async def describe_model_card_export_job(
        self, **kwargs: Unpack[DescribeModelCardExportJobRequestRequestTypeDef]
    ) -> DescribeModelCardExportJobResponseTypeDef:
        """
        Describes an Amazon SageMaker Model Card export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_model_card_export_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_model_card_export_job)
        """

    async def describe_model_explainability_job_definition(
        self, **kwargs: Unpack[DescribeModelExplainabilityJobDefinitionRequestRequestTypeDef]
    ) -> DescribeModelExplainabilityJobDefinitionResponseTypeDef:
        """
        Returns a description of a model explainability job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_model_explainability_job_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_model_explainability_job_definition)
        """

    async def describe_model_package(
        self, **kwargs: Unpack[DescribeModelPackageInputRequestTypeDef]
    ) -> DescribeModelPackageOutputTypeDef:
        """
        Returns a description of the specified model package, which is used to create
        SageMaker models or list them on Amazon Web Services Marketplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_model_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_model_package)
        """

    async def describe_model_package_group(
        self, **kwargs: Unpack[DescribeModelPackageGroupInputRequestTypeDef]
    ) -> DescribeModelPackageGroupOutputTypeDef:
        """
        Gets a description for the specified model group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_model_package_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_model_package_group)
        """

    async def describe_model_quality_job_definition(
        self, **kwargs: Unpack[DescribeModelQualityJobDefinitionRequestRequestTypeDef]
    ) -> DescribeModelQualityJobDefinitionResponseTypeDef:
        """
        Returns a description of a model quality job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_model_quality_job_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_model_quality_job_definition)
        """

    async def describe_monitoring_schedule(
        self, **kwargs: Unpack[DescribeMonitoringScheduleRequestRequestTypeDef]
    ) -> DescribeMonitoringScheduleResponseTypeDef:
        """
        Describes the schedule for a monitoring job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_monitoring_schedule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_monitoring_schedule)
        """

    async def describe_notebook_instance(
        self, **kwargs: Unpack[DescribeNotebookInstanceInputRequestTypeDef]
    ) -> DescribeNotebookInstanceOutputTypeDef:
        """
        Returns information about a notebook instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_notebook_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_notebook_instance)
        """

    async def describe_notebook_instance_lifecycle_config(
        self, **kwargs: Unpack[DescribeNotebookInstanceLifecycleConfigInputRequestTypeDef]
    ) -> DescribeNotebookInstanceLifecycleConfigOutputTypeDef:
        """
        Returns a description of a notebook instance lifecycle configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_notebook_instance_lifecycle_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_notebook_instance_lifecycle_config)
        """

    async def describe_optimization_job(
        self, **kwargs: Unpack[DescribeOptimizationJobRequestRequestTypeDef]
    ) -> DescribeOptimizationJobResponseTypeDef:
        """
        Provides the properties of the specified optimization job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_optimization_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_optimization_job)
        """

    async def describe_pipeline(
        self, **kwargs: Unpack[DescribePipelineRequestRequestTypeDef]
    ) -> DescribePipelineResponseTypeDef:
        """
        Describes the details of a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_pipeline)
        """

    async def describe_pipeline_definition_for_execution(
        self, **kwargs: Unpack[DescribePipelineDefinitionForExecutionRequestRequestTypeDef]
    ) -> DescribePipelineDefinitionForExecutionResponseTypeDef:
        """
        Describes the details of an execution's pipeline definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_pipeline_definition_for_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_pipeline_definition_for_execution)
        """

    async def describe_pipeline_execution(
        self, **kwargs: Unpack[DescribePipelineExecutionRequestRequestTypeDef]
    ) -> DescribePipelineExecutionResponseTypeDef:
        """
        Describes the details of a pipeline execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_pipeline_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_pipeline_execution)
        """

    async def describe_processing_job(
        self, **kwargs: Unpack[DescribeProcessingJobRequestRequestTypeDef]
    ) -> DescribeProcessingJobResponseTypeDef:
        """
        Returns a description of a processing job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_processing_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_processing_job)
        """

    async def describe_project(
        self, **kwargs: Unpack[DescribeProjectInputRequestTypeDef]
    ) -> DescribeProjectOutputTypeDef:
        """
        Describes the details of a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_project.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_project)
        """

    async def describe_space(
        self, **kwargs: Unpack[DescribeSpaceRequestRequestTypeDef]
    ) -> DescribeSpaceResponseTypeDef:
        """
        Describes the space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_space.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_space)
        """

    async def describe_studio_lifecycle_config(
        self, **kwargs: Unpack[DescribeStudioLifecycleConfigRequestRequestTypeDef]
    ) -> DescribeStudioLifecycleConfigResponseTypeDef:
        """
        Describes the Amazon SageMaker Studio Lifecycle Configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_studio_lifecycle_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_studio_lifecycle_config)
        """

    async def describe_subscribed_workteam(
        self, **kwargs: Unpack[DescribeSubscribedWorkteamRequestRequestTypeDef]
    ) -> DescribeSubscribedWorkteamResponseTypeDef:
        """
        Gets information about a work team provided by a vendor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_subscribed_workteam.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_subscribed_workteam)
        """

    async def describe_training_job(
        self, **kwargs: Unpack[DescribeTrainingJobRequestRequestTypeDef]
    ) -> DescribeTrainingJobResponseTypeDef:
        """
        Returns information about a training job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_training_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_training_job)
        """

    async def describe_transform_job(
        self, **kwargs: Unpack[DescribeTransformJobRequestRequestTypeDef]
    ) -> DescribeTransformJobResponseTypeDef:
        """
        Returns information about a transform job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_transform_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_transform_job)
        """

    async def describe_trial(
        self, **kwargs: Unpack[DescribeTrialRequestRequestTypeDef]
    ) -> DescribeTrialResponseTypeDef:
        """
        Provides a list of a trial's properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_trial.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_trial)
        """

    async def describe_trial_component(
        self, **kwargs: Unpack[DescribeTrialComponentRequestRequestTypeDef]
    ) -> DescribeTrialComponentResponseTypeDef:
        """
        Provides a list of a trials component's properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_trial_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_trial_component)
        """

    async def describe_user_profile(
        self, **kwargs: Unpack[DescribeUserProfileRequestRequestTypeDef]
    ) -> DescribeUserProfileResponseTypeDef:
        """
        Describes a user profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_user_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_user_profile)
        """

    async def describe_workforce(
        self, **kwargs: Unpack[DescribeWorkforceRequestRequestTypeDef]
    ) -> DescribeWorkforceResponseTypeDef:
        """
        Lists private workforce information, including workforce name, Amazon Resource
        Name (ARN), and, if applicable, allowed IP address ranges (<a
        href="https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html">CIDRs</a>).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_workforce.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_workforce)
        """

    async def describe_workteam(
        self, **kwargs: Unpack[DescribeWorkteamRequestRequestTypeDef]
    ) -> DescribeWorkteamResponseTypeDef:
        """
        Gets information about a specific work team.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/describe_workteam.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#describe_workteam)
        """

    async def disable_sagemaker_servicecatalog_portfolio(self) -> Dict[str, Any]:
        """
        Disables using Service Catalog in SageMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/disable_sagemaker_servicecatalog_portfolio.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#disable_sagemaker_servicecatalog_portfolio)
        """

    async def disassociate_trial_component(
        self, **kwargs: Unpack[DisassociateTrialComponentRequestRequestTypeDef]
    ) -> DisassociateTrialComponentResponseTypeDef:
        """
        Disassociates a trial component from a trial.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/disassociate_trial_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#disassociate_trial_component)
        """

    async def enable_sagemaker_servicecatalog_portfolio(self) -> Dict[str, Any]:
        """
        Enables using Service Catalog in SageMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/enable_sagemaker_servicecatalog_portfolio.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#enable_sagemaker_servicecatalog_portfolio)
        """

    async def get_device_fleet_report(
        self, **kwargs: Unpack[GetDeviceFleetReportRequestRequestTypeDef]
    ) -> GetDeviceFleetReportResponseTypeDef:
        """
        Describes a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_device_fleet_report.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_device_fleet_report)
        """

    async def get_lineage_group_policy(
        self, **kwargs: Unpack[GetLineageGroupPolicyRequestRequestTypeDef]
    ) -> GetLineageGroupPolicyResponseTypeDef:
        """
        The resource policy for the lineage group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_lineage_group_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_lineage_group_policy)
        """

    async def get_model_package_group_policy(
        self, **kwargs: Unpack[GetModelPackageGroupPolicyInputRequestTypeDef]
    ) -> GetModelPackageGroupPolicyOutputTypeDef:
        """
        Gets a resource policy that manages access for a model group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_model_package_group_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_model_package_group_policy)
        """

    async def get_sagemaker_servicecatalog_portfolio_status(
        self,
    ) -> GetSagemakerServicecatalogPortfolioStatusOutputTypeDef:
        """
        Gets the status of Service Catalog in SageMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_sagemaker_servicecatalog_portfolio_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_sagemaker_servicecatalog_portfolio_status)
        """

    async def get_scaling_configuration_recommendation(
        self, **kwargs: Unpack[GetScalingConfigurationRecommendationRequestRequestTypeDef]
    ) -> GetScalingConfigurationRecommendationResponseTypeDef:
        """
        Starts an Amazon SageMaker Inference Recommender autoscaling recommendation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_scaling_configuration_recommendation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_scaling_configuration_recommendation)
        """

    async def get_search_suggestions(
        self, **kwargs: Unpack[GetSearchSuggestionsRequestRequestTypeDef]
    ) -> GetSearchSuggestionsResponseTypeDef:
        """
        An auto-complete API for the search functionality in the SageMaker console.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_search_suggestions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_search_suggestions)
        """

    async def import_hub_content(
        self, **kwargs: Unpack[ImportHubContentRequestRequestTypeDef]
    ) -> ImportHubContentResponseTypeDef:
        """
        Import hub content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/import_hub_content.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#import_hub_content)
        """

    async def list_actions(
        self, **kwargs: Unpack[ListActionsRequestRequestTypeDef]
    ) -> ListActionsResponseTypeDef:
        """
        Lists the actions in your account and their properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_actions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_actions)
        """

    async def list_algorithms(
        self, **kwargs: Unpack[ListAlgorithmsInputRequestTypeDef]
    ) -> ListAlgorithmsOutputTypeDef:
        """
        Lists the machine learning algorithms that have been created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_algorithms.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_algorithms)
        """

    async def list_aliases(
        self, **kwargs: Unpack[ListAliasesRequestRequestTypeDef]
    ) -> ListAliasesResponseTypeDef:
        """
        Lists the aliases of a specified image or image version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_aliases.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_aliases)
        """

    async def list_app_image_configs(
        self, **kwargs: Unpack[ListAppImageConfigsRequestRequestTypeDef]
    ) -> ListAppImageConfigsResponseTypeDef:
        """
        Lists the AppImageConfigs in your account and their properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_app_image_configs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_app_image_configs)
        """

    async def list_apps(
        self, **kwargs: Unpack[ListAppsRequestRequestTypeDef]
    ) -> ListAppsResponseTypeDef:
        """
        Lists apps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_apps.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_apps)
        """

    async def list_artifacts(
        self, **kwargs: Unpack[ListArtifactsRequestRequestTypeDef]
    ) -> ListArtifactsResponseTypeDef:
        """
        Lists the artifacts in your account and their properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_artifacts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_artifacts)
        """

    async def list_associations(
        self, **kwargs: Unpack[ListAssociationsRequestRequestTypeDef]
    ) -> ListAssociationsResponseTypeDef:
        """
        Lists the associations in your account and their properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_associations)
        """

    async def list_auto_ml_jobs(
        self, **kwargs: Unpack[ListAutoMLJobsRequestRequestTypeDef]
    ) -> ListAutoMLJobsResponseTypeDef:
        """
        Request a list of jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_auto_ml_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_auto_ml_jobs)
        """

    async def list_candidates_for_auto_ml_job(
        self, **kwargs: Unpack[ListCandidatesForAutoMLJobRequestRequestTypeDef]
    ) -> ListCandidatesForAutoMLJobResponseTypeDef:
        """
        List the candidates created for the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_candidates_for_auto_ml_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_candidates_for_auto_ml_job)
        """

    async def list_cluster_nodes(
        self, **kwargs: Unpack[ListClusterNodesRequestRequestTypeDef]
    ) -> ListClusterNodesResponseTypeDef:
        """
        Retrieves the list of instances (also called <i>nodes</i> interchangeably) in a
        SageMaker HyperPod cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_cluster_nodes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_cluster_nodes)
        """

    async def list_clusters(
        self, **kwargs: Unpack[ListClustersRequestRequestTypeDef]
    ) -> ListClustersResponseTypeDef:
        """
        Retrieves the list of SageMaker HyperPod clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_clusters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_clusters)
        """

    async def list_code_repositories(
        self, **kwargs: Unpack[ListCodeRepositoriesInputRequestTypeDef]
    ) -> ListCodeRepositoriesOutputTypeDef:
        """
        Gets a list of the Git repositories in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_code_repositories.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_code_repositories)
        """

    async def list_compilation_jobs(
        self, **kwargs: Unpack[ListCompilationJobsRequestRequestTypeDef]
    ) -> ListCompilationJobsResponseTypeDef:
        """
        Lists model compilation jobs that satisfy various filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_compilation_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_compilation_jobs)
        """

    async def list_contexts(
        self, **kwargs: Unpack[ListContextsRequestRequestTypeDef]
    ) -> ListContextsResponseTypeDef:
        """
        Lists the contexts in your account and their properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_contexts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_contexts)
        """

    async def list_data_quality_job_definitions(
        self, **kwargs: Unpack[ListDataQualityJobDefinitionsRequestRequestTypeDef]
    ) -> ListDataQualityJobDefinitionsResponseTypeDef:
        """
        Lists the data quality job definitions in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_data_quality_job_definitions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_data_quality_job_definitions)
        """

    async def list_device_fleets(
        self, **kwargs: Unpack[ListDeviceFleetsRequestRequestTypeDef]
    ) -> ListDeviceFleetsResponseTypeDef:
        """
        Returns a list of devices in the fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_device_fleets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_device_fleets)
        """

    async def list_devices(
        self, **kwargs: Unpack[ListDevicesRequestRequestTypeDef]
    ) -> ListDevicesResponseTypeDef:
        """
        A list of devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_devices.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_devices)
        """

    async def list_domains(
        self, **kwargs: Unpack[ListDomainsRequestRequestTypeDef]
    ) -> ListDomainsResponseTypeDef:
        """
        Lists the domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_domains.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_domains)
        """

    async def list_edge_deployment_plans(
        self, **kwargs: Unpack[ListEdgeDeploymentPlansRequestRequestTypeDef]
    ) -> ListEdgeDeploymentPlansResponseTypeDef:
        """
        Lists all edge deployment plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_edge_deployment_plans.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_edge_deployment_plans)
        """

    async def list_edge_packaging_jobs(
        self, **kwargs: Unpack[ListEdgePackagingJobsRequestRequestTypeDef]
    ) -> ListEdgePackagingJobsResponseTypeDef:
        """
        Returns a list of edge packaging jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_edge_packaging_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_edge_packaging_jobs)
        """

    async def list_endpoint_configs(
        self, **kwargs: Unpack[ListEndpointConfigsInputRequestTypeDef]
    ) -> ListEndpointConfigsOutputTypeDef:
        """
        Lists endpoint configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_endpoint_configs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_endpoint_configs)
        """

    async def list_endpoints(
        self, **kwargs: Unpack[ListEndpointsInputRequestTypeDef]
    ) -> ListEndpointsOutputTypeDef:
        """
        Lists endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_endpoints)
        """

    async def list_experiments(
        self, **kwargs: Unpack[ListExperimentsRequestRequestTypeDef]
    ) -> ListExperimentsResponseTypeDef:
        """
        Lists all the experiments in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_experiments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_experiments)
        """

    async def list_feature_groups(
        self, **kwargs: Unpack[ListFeatureGroupsRequestRequestTypeDef]
    ) -> ListFeatureGroupsResponseTypeDef:
        """
        List <code>FeatureGroup</code>s based on given filter and order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_feature_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_feature_groups)
        """

    async def list_flow_definitions(
        self, **kwargs: Unpack[ListFlowDefinitionsRequestRequestTypeDef]
    ) -> ListFlowDefinitionsResponseTypeDef:
        """
        Returns information about the flow definitions in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_flow_definitions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_flow_definitions)
        """

    async def list_hub_content_versions(
        self, **kwargs: Unpack[ListHubContentVersionsRequestRequestTypeDef]
    ) -> ListHubContentVersionsResponseTypeDef:
        """
        List hub content versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_hub_content_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_hub_content_versions)
        """

    async def list_hub_contents(
        self, **kwargs: Unpack[ListHubContentsRequestRequestTypeDef]
    ) -> ListHubContentsResponseTypeDef:
        """
        List the contents of a hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_hub_contents.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_hub_contents)
        """

    async def list_hubs(
        self, **kwargs: Unpack[ListHubsRequestRequestTypeDef]
    ) -> ListHubsResponseTypeDef:
        """
        List all existing hubs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_hubs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_hubs)
        """

    async def list_human_task_uis(
        self, **kwargs: Unpack[ListHumanTaskUisRequestRequestTypeDef]
    ) -> ListHumanTaskUisResponseTypeDef:
        """
        Returns information about the human task user interfaces in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_human_task_uis.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_human_task_uis)
        """

    async def list_hyper_parameter_tuning_jobs(
        self, **kwargs: Unpack[ListHyperParameterTuningJobsRequestRequestTypeDef]
    ) -> ListHyperParameterTuningJobsResponseTypeDef:
        """
        Gets a list of <a
        href="https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_HyperParameterTuningJobSummary.html">HyperParameterTuningJobSummary</a>
        objects that describe the hyperparameter tuning jobs launched in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_hyper_parameter_tuning_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_hyper_parameter_tuning_jobs)
        """

    async def list_image_versions(
        self, **kwargs: Unpack[ListImageVersionsRequestRequestTypeDef]
    ) -> ListImageVersionsResponseTypeDef:
        """
        Lists the versions of a specified image and their properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_image_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_image_versions)
        """

    async def list_images(
        self, **kwargs: Unpack[ListImagesRequestRequestTypeDef]
    ) -> ListImagesResponseTypeDef:
        """
        Lists the images in your account and their properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_images.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_images)
        """

    async def list_inference_components(
        self, **kwargs: Unpack[ListInferenceComponentsInputRequestTypeDef]
    ) -> ListInferenceComponentsOutputTypeDef:
        """
        Lists the inference components in your account and their properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_inference_components.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_inference_components)
        """

    async def list_inference_experiments(
        self, **kwargs: Unpack[ListInferenceExperimentsRequestRequestTypeDef]
    ) -> ListInferenceExperimentsResponseTypeDef:
        """
        Returns the list of all inference experiments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_inference_experiments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_inference_experiments)
        """

    async def list_inference_recommendations_job_steps(
        self, **kwargs: Unpack[ListInferenceRecommendationsJobStepsRequestRequestTypeDef]
    ) -> ListInferenceRecommendationsJobStepsResponseTypeDef:
        """
        Returns a list of the subtasks for an Inference Recommender job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_inference_recommendations_job_steps.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_inference_recommendations_job_steps)
        """

    async def list_inference_recommendations_jobs(
        self, **kwargs: Unpack[ListInferenceRecommendationsJobsRequestRequestTypeDef]
    ) -> ListInferenceRecommendationsJobsResponseTypeDef:
        """
        Lists recommendation jobs that satisfy various filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_inference_recommendations_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_inference_recommendations_jobs)
        """

    async def list_labeling_jobs(
        self, **kwargs: Unpack[ListLabelingJobsRequestRequestTypeDef]
    ) -> ListLabelingJobsResponseTypeDef:
        """
        Gets a list of labeling jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_labeling_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_labeling_jobs)
        """

    async def list_labeling_jobs_for_workteam(
        self, **kwargs: Unpack[ListLabelingJobsForWorkteamRequestRequestTypeDef]
    ) -> ListLabelingJobsForWorkteamResponseTypeDef:
        """
        Gets a list of labeling jobs assigned to a specified work team.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_labeling_jobs_for_workteam.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_labeling_jobs_for_workteam)
        """

    async def list_lineage_groups(
        self, **kwargs: Unpack[ListLineageGroupsRequestRequestTypeDef]
    ) -> ListLineageGroupsResponseTypeDef:
        """
        A list of lineage groups shared with your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_lineage_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_lineage_groups)
        """

    async def list_mlflow_tracking_servers(
        self, **kwargs: Unpack[ListMlflowTrackingServersRequestRequestTypeDef]
    ) -> ListMlflowTrackingServersResponseTypeDef:
        """
        Lists all MLflow Tracking Servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_mlflow_tracking_servers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_mlflow_tracking_servers)
        """

    async def list_model_bias_job_definitions(
        self, **kwargs: Unpack[ListModelBiasJobDefinitionsRequestRequestTypeDef]
    ) -> ListModelBiasJobDefinitionsResponseTypeDef:
        """
        Lists model bias jobs definitions that satisfy various filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_model_bias_job_definitions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_model_bias_job_definitions)
        """

    async def list_model_card_export_jobs(
        self, **kwargs: Unpack[ListModelCardExportJobsRequestRequestTypeDef]
    ) -> ListModelCardExportJobsResponseTypeDef:
        """
        List the export jobs for the Amazon SageMaker Model Card.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_model_card_export_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_model_card_export_jobs)
        """

    async def list_model_card_versions(
        self, **kwargs: Unpack[ListModelCardVersionsRequestRequestTypeDef]
    ) -> ListModelCardVersionsResponseTypeDef:
        """
        List existing versions of an Amazon SageMaker Model Card.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_model_card_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_model_card_versions)
        """

    async def list_model_cards(
        self, **kwargs: Unpack[ListModelCardsRequestRequestTypeDef]
    ) -> ListModelCardsResponseTypeDef:
        """
        List existing model cards.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_model_cards.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_model_cards)
        """

    async def list_model_explainability_job_definitions(
        self, **kwargs: Unpack[ListModelExplainabilityJobDefinitionsRequestRequestTypeDef]
    ) -> ListModelExplainabilityJobDefinitionsResponseTypeDef:
        """
        Lists model explainability job definitions that satisfy various filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_model_explainability_job_definitions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_model_explainability_job_definitions)
        """

    async def list_model_metadata(
        self, **kwargs: Unpack[ListModelMetadataRequestRequestTypeDef]
    ) -> ListModelMetadataResponseTypeDef:
        """
        Lists the domain, framework, task, and model name of standard machine learning
        models found in common model zoos.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_model_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_model_metadata)
        """

    async def list_model_package_groups(
        self, **kwargs: Unpack[ListModelPackageGroupsInputRequestTypeDef]
    ) -> ListModelPackageGroupsOutputTypeDef:
        """
        Gets a list of the model groups in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_model_package_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_model_package_groups)
        """

    async def list_model_packages(
        self, **kwargs: Unpack[ListModelPackagesInputRequestTypeDef]
    ) -> ListModelPackagesOutputTypeDef:
        """
        Lists the model packages that have been created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_model_packages.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_model_packages)
        """

    async def list_model_quality_job_definitions(
        self, **kwargs: Unpack[ListModelQualityJobDefinitionsRequestRequestTypeDef]
    ) -> ListModelQualityJobDefinitionsResponseTypeDef:
        """
        Gets a list of model quality monitoring job definitions in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_model_quality_job_definitions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_model_quality_job_definitions)
        """

    async def list_models(
        self, **kwargs: Unpack[ListModelsInputRequestTypeDef]
    ) -> ListModelsOutputTypeDef:
        """
        Lists models created with the <code>CreateModel</code> API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_models.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_models)
        """

    async def list_monitoring_alert_history(
        self, **kwargs: Unpack[ListMonitoringAlertHistoryRequestRequestTypeDef]
    ) -> ListMonitoringAlertHistoryResponseTypeDef:
        """
        Gets a list of past alerts in a model monitoring schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_monitoring_alert_history.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_monitoring_alert_history)
        """

    async def list_monitoring_alerts(
        self, **kwargs: Unpack[ListMonitoringAlertsRequestRequestTypeDef]
    ) -> ListMonitoringAlertsResponseTypeDef:
        """
        Gets the alerts for a single monitoring schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_monitoring_alerts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_monitoring_alerts)
        """

    async def list_monitoring_executions(
        self, **kwargs: Unpack[ListMonitoringExecutionsRequestRequestTypeDef]
    ) -> ListMonitoringExecutionsResponseTypeDef:
        """
        Returns list of all monitoring job executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_monitoring_executions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_monitoring_executions)
        """

    async def list_monitoring_schedules(
        self, **kwargs: Unpack[ListMonitoringSchedulesRequestRequestTypeDef]
    ) -> ListMonitoringSchedulesResponseTypeDef:
        """
        Returns list of all monitoring schedules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_monitoring_schedules.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_monitoring_schedules)
        """

    async def list_notebook_instance_lifecycle_configs(
        self, **kwargs: Unpack[ListNotebookInstanceLifecycleConfigsInputRequestTypeDef]
    ) -> ListNotebookInstanceLifecycleConfigsOutputTypeDef:
        """
        Lists notebook instance lifestyle configurations created with the <a
        href="https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateNotebookInstanceLifecycleConfig.html">CreateNotebookInstanceLifecycleConfig</a>
        API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_notebook_instance_lifecycle_configs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_notebook_instance_lifecycle_configs)
        """

    async def list_notebook_instances(
        self, **kwargs: Unpack[ListNotebookInstancesInputRequestTypeDef]
    ) -> ListNotebookInstancesOutputTypeDef:
        """
        Returns a list of the SageMaker notebook instances in the requester's account
        in an Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_notebook_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_notebook_instances)
        """

    async def list_optimization_jobs(
        self, **kwargs: Unpack[ListOptimizationJobsRequestRequestTypeDef]
    ) -> ListOptimizationJobsResponseTypeDef:
        """
        Lists the optimization jobs in your account and their properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_optimization_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_optimization_jobs)
        """

    async def list_pipeline_execution_steps(
        self, **kwargs: Unpack[ListPipelineExecutionStepsRequestRequestTypeDef]
    ) -> ListPipelineExecutionStepsResponseTypeDef:
        """
        Gets a list of <code>PipeLineExecutionStep</code> objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_pipeline_execution_steps.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_pipeline_execution_steps)
        """

    async def list_pipeline_executions(
        self, **kwargs: Unpack[ListPipelineExecutionsRequestRequestTypeDef]
    ) -> ListPipelineExecutionsResponseTypeDef:
        """
        Gets a list of the pipeline executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_pipeline_executions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_pipeline_executions)
        """

    async def list_pipeline_parameters_for_execution(
        self, **kwargs: Unpack[ListPipelineParametersForExecutionRequestRequestTypeDef]
    ) -> ListPipelineParametersForExecutionResponseTypeDef:
        """
        Gets a list of parameters for a pipeline execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_pipeline_parameters_for_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_pipeline_parameters_for_execution)
        """

    async def list_pipelines(
        self, **kwargs: Unpack[ListPipelinesRequestRequestTypeDef]
    ) -> ListPipelinesResponseTypeDef:
        """
        Gets a list of pipelines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_pipelines.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_pipelines)
        """

    async def list_processing_jobs(
        self, **kwargs: Unpack[ListProcessingJobsRequestRequestTypeDef]
    ) -> ListProcessingJobsResponseTypeDef:
        """
        Lists processing jobs that satisfy various filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_processing_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_processing_jobs)
        """

    async def list_projects(
        self, **kwargs: Unpack[ListProjectsInputRequestTypeDef]
    ) -> ListProjectsOutputTypeDef:
        """
        Gets a list of the projects in an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_projects.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_projects)
        """

    async def list_resource_catalogs(
        self, **kwargs: Unpack[ListResourceCatalogsRequestRequestTypeDef]
    ) -> ListResourceCatalogsResponseTypeDef:
        """
        Lists Amazon SageMaker Catalogs based on given filters and orders.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_resource_catalogs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_resource_catalogs)
        """

    async def list_spaces(
        self, **kwargs: Unpack[ListSpacesRequestRequestTypeDef]
    ) -> ListSpacesResponseTypeDef:
        """
        Lists spaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_spaces.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_spaces)
        """

    async def list_stage_devices(
        self, **kwargs: Unpack[ListStageDevicesRequestRequestTypeDef]
    ) -> ListStageDevicesResponseTypeDef:
        """
        Lists devices allocated to the stage, containing detailed device information
        and deployment status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_stage_devices.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_stage_devices)
        """

    async def list_studio_lifecycle_configs(
        self, **kwargs: Unpack[ListStudioLifecycleConfigsRequestRequestTypeDef]
    ) -> ListStudioLifecycleConfigsResponseTypeDef:
        """
        Lists the Amazon SageMaker Studio Lifecycle Configurations in your Amazon Web
        Services Account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_studio_lifecycle_configs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_studio_lifecycle_configs)
        """

    async def list_subscribed_workteams(
        self, **kwargs: Unpack[ListSubscribedWorkteamsRequestRequestTypeDef]
    ) -> ListSubscribedWorkteamsResponseTypeDef:
        """
        Gets a list of the work teams that you are subscribed to in the Amazon Web
        Services Marketplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_subscribed_workteams.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_subscribed_workteams)
        """

    async def list_tags(
        self, **kwargs: Unpack[ListTagsInputRequestTypeDef]
    ) -> ListTagsOutputTypeDef:
        """
        Returns the tags for the specified SageMaker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_tags)
        """

    async def list_training_jobs(
        self, **kwargs: Unpack[ListTrainingJobsRequestRequestTypeDef]
    ) -> ListTrainingJobsResponseTypeDef:
        """
        Lists training jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_training_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_training_jobs)
        """

    async def list_training_jobs_for_hyper_parameter_tuning_job(
        self, **kwargs: Unpack[ListTrainingJobsForHyperParameterTuningJobRequestRequestTypeDef]
    ) -> ListTrainingJobsForHyperParameterTuningJobResponseTypeDef:
        """
        Gets a list of <a
        href="https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_TrainingJobSummary.html">TrainingJobSummary</a>
        objects that describe the training jobs that a hyperparameter tuning job
        launched.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_training_jobs_for_hyper_parameter_tuning_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_training_jobs_for_hyper_parameter_tuning_job)
        """

    async def list_transform_jobs(
        self, **kwargs: Unpack[ListTransformJobsRequestRequestTypeDef]
    ) -> ListTransformJobsResponseTypeDef:
        """
        Lists transform jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_transform_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_transform_jobs)
        """

    async def list_trial_components(
        self, **kwargs: Unpack[ListTrialComponentsRequestRequestTypeDef]
    ) -> ListTrialComponentsResponseTypeDef:
        """
        Lists the trial components in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_trial_components.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_trial_components)
        """

    async def list_trials(
        self, **kwargs: Unpack[ListTrialsRequestRequestTypeDef]
    ) -> ListTrialsResponseTypeDef:
        """
        Lists the trials in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_trials.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_trials)
        """

    async def list_user_profiles(
        self, **kwargs: Unpack[ListUserProfilesRequestRequestTypeDef]
    ) -> ListUserProfilesResponseTypeDef:
        """
        Lists user profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_user_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_user_profiles)
        """

    async def list_workforces(
        self, **kwargs: Unpack[ListWorkforcesRequestRequestTypeDef]
    ) -> ListWorkforcesResponseTypeDef:
        """
        Use this operation to list all private and vendor workforces in an Amazon Web
        Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_workforces.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_workforces)
        """

    async def list_workteams(
        self, **kwargs: Unpack[ListWorkteamsRequestRequestTypeDef]
    ) -> ListWorkteamsResponseTypeDef:
        """
        Gets a list of private work teams that you have defined in a region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/list_workteams.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#list_workteams)
        """

    async def put_model_package_group_policy(
        self, **kwargs: Unpack[PutModelPackageGroupPolicyInputRequestTypeDef]
    ) -> PutModelPackageGroupPolicyOutputTypeDef:
        """
        Adds a resouce policy to control access to a model group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/put_model_package_group_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#put_model_package_group_policy)
        """

    async def query_lineage(
        self, **kwargs: Unpack[QueryLineageRequestRequestTypeDef]
    ) -> QueryLineageResponseTypeDef:
        """
        Use this action to inspect your lineage and discover relationships between
        entities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/query_lineage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#query_lineage)
        """

    async def register_devices(
        self, **kwargs: Unpack[RegisterDevicesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Register devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/register_devices.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#register_devices)
        """

    async def render_ui_template(
        self, **kwargs: Unpack[RenderUiTemplateRequestRequestTypeDef]
    ) -> RenderUiTemplateResponseTypeDef:
        """
        Renders the UI template so that you can preview the worker's experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/render_ui_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#render_ui_template)
        """

    async def retry_pipeline_execution(
        self, **kwargs: Unpack[RetryPipelineExecutionRequestRequestTypeDef]
    ) -> RetryPipelineExecutionResponseTypeDef:
        """
        Retry the execution of the pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/retry_pipeline_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#retry_pipeline_execution)
        """

    async def search(self, **kwargs: Unpack[SearchRequestRequestTypeDef]) -> SearchResponseTypeDef:
        """
        Finds SageMaker resources that match a search query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/search.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#search)
        """

    async def send_pipeline_execution_step_failure(
        self, **kwargs: Unpack[SendPipelineExecutionStepFailureRequestRequestTypeDef]
    ) -> SendPipelineExecutionStepFailureResponseTypeDef:
        """
        Notifies the pipeline that the execution of a callback step failed, along with
        a message describing why.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/send_pipeline_execution_step_failure.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#send_pipeline_execution_step_failure)
        """

    async def send_pipeline_execution_step_success(
        self, **kwargs: Unpack[SendPipelineExecutionStepSuccessRequestRequestTypeDef]
    ) -> SendPipelineExecutionStepSuccessResponseTypeDef:
        """
        Notifies the pipeline that the execution of a callback step succeeded and
        provides a list of the step's output parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/send_pipeline_execution_step_success.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#send_pipeline_execution_step_success)
        """

    async def start_edge_deployment_stage(
        self, **kwargs: Unpack[StartEdgeDeploymentStageRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a stage in an edge deployment plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/start_edge_deployment_stage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#start_edge_deployment_stage)
        """

    async def start_inference_experiment(
        self, **kwargs: Unpack[StartInferenceExperimentRequestRequestTypeDef]
    ) -> StartInferenceExperimentResponseTypeDef:
        """
        Starts an inference experiment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/start_inference_experiment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#start_inference_experiment)
        """

    async def start_mlflow_tracking_server(
        self, **kwargs: Unpack[StartMlflowTrackingServerRequestRequestTypeDef]
    ) -> StartMlflowTrackingServerResponseTypeDef:
        """
        Programmatically start an MLflow Tracking Server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/start_mlflow_tracking_server.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#start_mlflow_tracking_server)
        """

    async def start_monitoring_schedule(
        self, **kwargs: Unpack[StartMonitoringScheduleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a previously stopped monitoring schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/start_monitoring_schedule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#start_monitoring_schedule)
        """

    async def start_notebook_instance(
        self, **kwargs: Unpack[StartNotebookInstanceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Launches an ML compute instance with the latest version of the libraries and
        attaches your ML storage volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/start_notebook_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#start_notebook_instance)
        """

    async def start_pipeline_execution(
        self, **kwargs: Unpack[StartPipelineExecutionRequestRequestTypeDef]
    ) -> StartPipelineExecutionResponseTypeDef:
        """
        Starts a pipeline execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/start_pipeline_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#start_pipeline_execution)
        """

    async def stop_auto_ml_job(
        self, **kwargs: Unpack[StopAutoMLJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        A method for forcing a running job to shut down.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/stop_auto_ml_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#stop_auto_ml_job)
        """

    async def stop_compilation_job(
        self, **kwargs: Unpack[StopCompilationJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a model compilation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/stop_compilation_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#stop_compilation_job)
        """

    async def stop_edge_deployment_stage(
        self, **kwargs: Unpack[StopEdgeDeploymentStageRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a stage in an edge deployment plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/stop_edge_deployment_stage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#stop_edge_deployment_stage)
        """

    async def stop_edge_packaging_job(
        self, **kwargs: Unpack[StopEdgePackagingJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Request to stop an edge packaging job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/stop_edge_packaging_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#stop_edge_packaging_job)
        """

    async def stop_hyper_parameter_tuning_job(
        self, **kwargs: Unpack[StopHyperParameterTuningJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a running hyperparameter tuning job and all running training jobs that
        the tuning job launched.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/stop_hyper_parameter_tuning_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#stop_hyper_parameter_tuning_job)
        """

    async def stop_inference_experiment(
        self, **kwargs: Unpack[StopInferenceExperimentRequestRequestTypeDef]
    ) -> StopInferenceExperimentResponseTypeDef:
        """
        Stops an inference experiment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/stop_inference_experiment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#stop_inference_experiment)
        """

    async def stop_inference_recommendations_job(
        self, **kwargs: Unpack[StopInferenceRecommendationsJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops an Inference Recommender job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/stop_inference_recommendations_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#stop_inference_recommendations_job)
        """

    async def stop_labeling_job(
        self, **kwargs: Unpack[StopLabelingJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a running labeling job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/stop_labeling_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#stop_labeling_job)
        """

    async def stop_mlflow_tracking_server(
        self, **kwargs: Unpack[StopMlflowTrackingServerRequestRequestTypeDef]
    ) -> StopMlflowTrackingServerResponseTypeDef:
        """
        Programmatically stop an MLflow Tracking Server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/stop_mlflow_tracking_server.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#stop_mlflow_tracking_server)
        """

    async def stop_monitoring_schedule(
        self, **kwargs: Unpack[StopMonitoringScheduleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a previously started monitoring schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/stop_monitoring_schedule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#stop_monitoring_schedule)
        """

    async def stop_notebook_instance(
        self, **kwargs: Unpack[StopNotebookInstanceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Terminates the ML compute instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/stop_notebook_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#stop_notebook_instance)
        """

    async def stop_optimization_job(
        self, **kwargs: Unpack[StopOptimizationJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Ends a running inference optimization job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/stop_optimization_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#stop_optimization_job)
        """

    async def stop_pipeline_execution(
        self, **kwargs: Unpack[StopPipelineExecutionRequestRequestTypeDef]
    ) -> StopPipelineExecutionResponseTypeDef:
        """
        Stops a pipeline execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/stop_pipeline_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#stop_pipeline_execution)
        """

    async def stop_processing_job(
        self, **kwargs: Unpack[StopProcessingJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a processing job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/stop_processing_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#stop_processing_job)
        """

    async def stop_training_job(
        self, **kwargs: Unpack[StopTrainingJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a training job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/stop_training_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#stop_training_job)
        """

    async def stop_transform_job(
        self, **kwargs: Unpack[StopTransformJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a batch transform job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/stop_transform_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#stop_transform_job)
        """

    async def update_action(
        self, **kwargs: Unpack[UpdateActionRequestRequestTypeDef]
    ) -> UpdateActionResponseTypeDef:
        """
        Updates an action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_action)
        """

    async def update_app_image_config(
        self, **kwargs: Unpack[UpdateAppImageConfigRequestRequestTypeDef]
    ) -> UpdateAppImageConfigResponseTypeDef:
        """
        Updates the properties of an AppImageConfig.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_app_image_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_app_image_config)
        """

    async def update_artifact(
        self, **kwargs: Unpack[UpdateArtifactRequestRequestTypeDef]
    ) -> UpdateArtifactResponseTypeDef:
        """
        Updates an artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_artifact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_artifact)
        """

    async def update_cluster(
        self, **kwargs: Unpack[UpdateClusterRequestRequestTypeDef]
    ) -> UpdateClusterResponseTypeDef:
        """
        Updates a SageMaker HyperPod cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_cluster.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_cluster)
        """

    async def update_cluster_software(
        self, **kwargs: Unpack[UpdateClusterSoftwareRequestRequestTypeDef]
    ) -> UpdateClusterSoftwareResponseTypeDef:
        """
        Updates the platform software of a SageMaker HyperPod cluster for security
        patching.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_cluster_software.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_cluster_software)
        """

    async def update_code_repository(
        self, **kwargs: Unpack[UpdateCodeRepositoryInputRequestTypeDef]
    ) -> UpdateCodeRepositoryOutputTypeDef:
        """
        Updates the specified Git repository with the specified values.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_code_repository.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_code_repository)
        """

    async def update_context(
        self, **kwargs: Unpack[UpdateContextRequestRequestTypeDef]
    ) -> UpdateContextResponseTypeDef:
        """
        Updates a context.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_context.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_context)
        """

    async def update_device_fleet(
        self, **kwargs: Unpack[UpdateDeviceFleetRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a fleet of devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_device_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_device_fleet)
        """

    async def update_devices(
        self, **kwargs: Unpack[UpdateDevicesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates one or more devices in a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_devices.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_devices)
        """

    async def update_domain(
        self, **kwargs: Unpack[UpdateDomainRequestRequestTypeDef]
    ) -> UpdateDomainResponseTypeDef:
        """
        Updates the default settings for new user profiles in the domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_domain)
        """

    async def update_endpoint(
        self, **kwargs: Unpack[UpdateEndpointInputRequestTypeDef]
    ) -> UpdateEndpointOutputTypeDef:
        """
        Deploys the <code>EndpointConfig</code> specified in the request to a new fleet
        of instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_endpoint)
        """

    async def update_endpoint_weights_and_capacities(
        self, **kwargs: Unpack[UpdateEndpointWeightsAndCapacitiesInputRequestTypeDef]
    ) -> UpdateEndpointWeightsAndCapacitiesOutputTypeDef:
        """
        Updates variant weight of one or more variants associated with an existing
        endpoint, or capacity of one variant associated with an existing endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_endpoint_weights_and_capacities.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_endpoint_weights_and_capacities)
        """

    async def update_experiment(
        self, **kwargs: Unpack[UpdateExperimentRequestRequestTypeDef]
    ) -> UpdateExperimentResponseTypeDef:
        """
        Adds, updates, or removes the description of an experiment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_experiment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_experiment)
        """

    async def update_feature_group(
        self, **kwargs: Unpack[UpdateFeatureGroupRequestRequestTypeDef]
    ) -> UpdateFeatureGroupResponseTypeDef:
        """
        Updates the feature group by either adding features or updating the online
        store configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_feature_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_feature_group)
        """

    async def update_feature_metadata(
        self, **kwargs: Unpack[UpdateFeatureMetadataRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the description and parameters of the feature group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_feature_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_feature_metadata)
        """

    async def update_hub(
        self, **kwargs: Unpack[UpdateHubRequestRequestTypeDef]
    ) -> UpdateHubResponseTypeDef:
        """
        Update a hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_hub.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_hub)
        """

    async def update_image(
        self, **kwargs: Unpack[UpdateImageRequestRequestTypeDef]
    ) -> UpdateImageResponseTypeDef:
        """
        Updates the properties of a SageMaker image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_image)
        """

    async def update_image_version(
        self, **kwargs: Unpack[UpdateImageVersionRequestRequestTypeDef]
    ) -> UpdateImageVersionResponseTypeDef:
        """
        Updates the properties of a SageMaker image version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_image_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_image_version)
        """

    async def update_inference_component(
        self, **kwargs: Unpack[UpdateInferenceComponentInputRequestTypeDef]
    ) -> UpdateInferenceComponentOutputTypeDef:
        """
        Updates an inference component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_inference_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_inference_component)
        """

    async def update_inference_component_runtime_config(
        self, **kwargs: Unpack[UpdateInferenceComponentRuntimeConfigInputRequestTypeDef]
    ) -> UpdateInferenceComponentRuntimeConfigOutputTypeDef:
        """
        Runtime settings for a model that is deployed with an inference component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_inference_component_runtime_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_inference_component_runtime_config)
        """

    async def update_inference_experiment(
        self, **kwargs: Unpack[UpdateInferenceExperimentRequestRequestTypeDef]
    ) -> UpdateInferenceExperimentResponseTypeDef:
        """
        Updates an inference experiment that you created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_inference_experiment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_inference_experiment)
        """

    async def update_mlflow_tracking_server(
        self, **kwargs: Unpack[UpdateMlflowTrackingServerRequestRequestTypeDef]
    ) -> UpdateMlflowTrackingServerResponseTypeDef:
        """
        Updates properties of an existing MLflow Tracking Server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_mlflow_tracking_server.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_mlflow_tracking_server)
        """

    async def update_model_card(
        self, **kwargs: Unpack[UpdateModelCardRequestRequestTypeDef]
    ) -> UpdateModelCardResponseTypeDef:
        """
        Update an Amazon SageMaker Model Card.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_model_card.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_model_card)
        """

    async def update_model_package(
        self, **kwargs: Unpack[UpdateModelPackageInputRequestTypeDef]
    ) -> UpdateModelPackageOutputTypeDef:
        """
        Updates a versioned model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_model_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_model_package)
        """

    async def update_monitoring_alert(
        self, **kwargs: Unpack[UpdateMonitoringAlertRequestRequestTypeDef]
    ) -> UpdateMonitoringAlertResponseTypeDef:
        """
        Update the parameters of a model monitor alert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_monitoring_alert.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_monitoring_alert)
        """

    async def update_monitoring_schedule(
        self, **kwargs: Unpack[UpdateMonitoringScheduleRequestRequestTypeDef]
    ) -> UpdateMonitoringScheduleResponseTypeDef:
        """
        Updates a previously created schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_monitoring_schedule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_monitoring_schedule)
        """

    async def update_notebook_instance(
        self, **kwargs: Unpack[UpdateNotebookInstanceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a notebook instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_notebook_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_notebook_instance)
        """

    async def update_notebook_instance_lifecycle_config(
        self, **kwargs: Unpack[UpdateNotebookInstanceLifecycleConfigInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a notebook instance lifecycle configuration created with the <a
        href="https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateNotebookInstanceLifecycleConfig.html">CreateNotebookInstanceLifecycleConfig</a>
        API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_notebook_instance_lifecycle_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_notebook_instance_lifecycle_config)
        """

    async def update_pipeline(
        self, **kwargs: Unpack[UpdatePipelineRequestRequestTypeDef]
    ) -> UpdatePipelineResponseTypeDef:
        """
        Updates a pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_pipeline)
        """

    async def update_pipeline_execution(
        self, **kwargs: Unpack[UpdatePipelineExecutionRequestRequestTypeDef]
    ) -> UpdatePipelineExecutionResponseTypeDef:
        """
        Updates a pipeline execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_pipeline_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_pipeline_execution)
        """

    async def update_project(
        self, **kwargs: Unpack[UpdateProjectInputRequestTypeDef]
    ) -> UpdateProjectOutputTypeDef:
        """
        Updates a machine learning (ML) project that is created from a template that
        sets up an ML pipeline from training to deploying an approved model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_project.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_project)
        """

    async def update_space(
        self, **kwargs: Unpack[UpdateSpaceRequestRequestTypeDef]
    ) -> UpdateSpaceResponseTypeDef:
        """
        Updates the settings of a space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_space.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_space)
        """

    async def update_training_job(
        self, **kwargs: Unpack[UpdateTrainingJobRequestRequestTypeDef]
    ) -> UpdateTrainingJobResponseTypeDef:
        """
        Update a model training job to request a new Debugger profiling configuration
        or to change warm pool retention length.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_training_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_training_job)
        """

    async def update_trial(
        self, **kwargs: Unpack[UpdateTrialRequestRequestTypeDef]
    ) -> UpdateTrialResponseTypeDef:
        """
        Updates the display name of a trial.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_trial.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_trial)
        """

    async def update_trial_component(
        self, **kwargs: Unpack[UpdateTrialComponentRequestRequestTypeDef]
    ) -> UpdateTrialComponentResponseTypeDef:
        """
        Updates one or more properties of a trial component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_trial_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_trial_component)
        """

    async def update_user_profile(
        self, **kwargs: Unpack[UpdateUserProfileRequestRequestTypeDef]
    ) -> UpdateUserProfileResponseTypeDef:
        """
        Updates a user profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_user_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_user_profile)
        """

    async def update_workforce(
        self, **kwargs: Unpack[UpdateWorkforceRequestRequestTypeDef]
    ) -> UpdateWorkforceResponseTypeDef:
        """
        Use this operation to update your workforce.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_workforce.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_workforce)
        """

    async def update_workteam(
        self, **kwargs: Unpack[UpdateWorkteamRequestRequestTypeDef]
    ) -> UpdateWorkteamResponseTypeDef:
        """
        Updates an existing work team with new member definitions or description.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/update_workteam.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#update_workteam)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_actions"]) -> ListActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_algorithms"]) -> ListAlgorithmsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_aliases"]) -> ListAliasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_app_image_configs"]
    ) -> ListAppImageConfigsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_apps"]) -> ListAppsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_artifacts"]) -> ListArtifactsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_associations"]
    ) -> ListAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_auto_ml_jobs"]
    ) -> ListAutoMLJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_candidates_for_auto_ml_job"]
    ) -> ListCandidatesForAutoMLJobPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cluster_nodes"]
    ) -> ListClusterNodesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_clusters"]) -> ListClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_code_repositories"]
    ) -> ListCodeRepositoriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_compilation_jobs"]
    ) -> ListCompilationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_contexts"]) -> ListContextsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_quality_job_definitions"]
    ) -> ListDataQualityJobDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_fleets"]
    ) -> ListDeviceFleetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_devices"]) -> ListDevicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_domains"]) -> ListDomainsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_edge_deployment_plans"]
    ) -> ListEdgeDeploymentPlansPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_edge_packaging_jobs"]
    ) -> ListEdgePackagingJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_endpoint_configs"]
    ) -> ListEndpointConfigsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_endpoints"]) -> ListEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_experiments"]
    ) -> ListExperimentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_feature_groups"]
    ) -> ListFeatureGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_flow_definitions"]
    ) -> ListFlowDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_human_task_uis"]
    ) -> ListHumanTaskUisPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_hyper_parameter_tuning_jobs"]
    ) -> ListHyperParameterTuningJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_image_versions"]
    ) -> ListImageVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_images"]) -> ListImagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_inference_components"]
    ) -> ListInferenceComponentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_inference_experiments"]
    ) -> ListInferenceExperimentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_inference_recommendations_job_steps"]
    ) -> ListInferenceRecommendationsJobStepsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_inference_recommendations_jobs"]
    ) -> ListInferenceRecommendationsJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_labeling_jobs_for_workteam"]
    ) -> ListLabelingJobsForWorkteamPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_labeling_jobs"]
    ) -> ListLabelingJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_lineage_groups"]
    ) -> ListLineageGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_mlflow_tracking_servers"]
    ) -> ListMlflowTrackingServersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_bias_job_definitions"]
    ) -> ListModelBiasJobDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_card_export_jobs"]
    ) -> ListModelCardExportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_card_versions"]
    ) -> ListModelCardVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_model_cards"]) -> ListModelCardsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_explainability_job_definitions"]
    ) -> ListModelExplainabilityJobDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_metadata"]
    ) -> ListModelMetadataPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_package_groups"]
    ) -> ListModelPackageGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_packages"]
    ) -> ListModelPackagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_quality_job_definitions"]
    ) -> ListModelQualityJobDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_models"]) -> ListModelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_monitoring_alert_history"]
    ) -> ListMonitoringAlertHistoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_monitoring_alerts"]
    ) -> ListMonitoringAlertsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_monitoring_executions"]
    ) -> ListMonitoringExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_monitoring_schedules"]
    ) -> ListMonitoringSchedulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_notebook_instance_lifecycle_configs"]
    ) -> ListNotebookInstanceLifecycleConfigsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_notebook_instances"]
    ) -> ListNotebookInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_optimization_jobs"]
    ) -> ListOptimizationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pipeline_execution_steps"]
    ) -> ListPipelineExecutionStepsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pipeline_executions"]
    ) -> ListPipelineExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pipeline_parameters_for_execution"]
    ) -> ListPipelineParametersForExecutionPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_pipelines"]) -> ListPipelinesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_processing_jobs"]
    ) -> ListProcessingJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_catalogs"]
    ) -> ListResourceCatalogsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_spaces"]) -> ListSpacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_stage_devices"]
    ) -> ListStageDevicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_studio_lifecycle_configs"]
    ) -> ListStudioLifecycleConfigsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_subscribed_workteams"]
    ) -> ListSubscribedWorkteamsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tags"]) -> ListTagsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_training_jobs_for_hyper_parameter_tuning_job"]
    ) -> ListTrainingJobsForHyperParameterTuningJobPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_training_jobs"]
    ) -> ListTrainingJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_transform_jobs"]
    ) -> ListTransformJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_trial_components"]
    ) -> ListTrialComponentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_trials"]) -> ListTrialsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_user_profiles"]
    ) -> ListUserProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workforces"]) -> ListWorkforcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workteams"]) -> ListWorkteamsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search"]) -> SearchPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["endpoint_deleted"]) -> EndpointDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["endpoint_in_service"]) -> EndpointInServiceWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["image_created"]) -> ImageCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["image_deleted"]) -> ImageDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["image_updated"]) -> ImageUpdatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["image_version_created"]
    ) -> ImageVersionCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["image_version_deleted"]
    ) -> ImageVersionDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["notebook_instance_deleted"]
    ) -> NotebookInstanceDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["notebook_instance_in_service"]
    ) -> NotebookInstanceInServiceWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["notebook_instance_stopped"]
    ) -> NotebookInstanceStoppedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["processing_job_completed_or_stopped"]
    ) -> ProcessingJobCompletedOrStoppedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["training_job_completed_or_stopped"]
    ) -> TrainingJobCompletedOrStoppedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["transform_job_completed_or_stopped"]
    ) -> TransformJobCompletedOrStoppedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/#get_waiter)
        """

    async def __aenter__(self) -> "SageMakerClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/client/)
        """
