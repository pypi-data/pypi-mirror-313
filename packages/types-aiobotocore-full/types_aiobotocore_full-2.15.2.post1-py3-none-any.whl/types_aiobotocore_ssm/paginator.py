"""
Type annotations for ssm service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ssm.client import SSMClient
    from types_aiobotocore_ssm.paginator import (
        DescribeActivationsPaginator,
        DescribeAssociationExecutionTargetsPaginator,
        DescribeAssociationExecutionsPaginator,
        DescribeAutomationExecutionsPaginator,
        DescribeAutomationStepExecutionsPaginator,
        DescribeAvailablePatchesPaginator,
        DescribeEffectiveInstanceAssociationsPaginator,
        DescribeEffectivePatchesForPatchBaselinePaginator,
        DescribeInstanceAssociationsStatusPaginator,
        DescribeInstanceInformationPaginator,
        DescribeInstancePatchStatesForPatchGroupPaginator,
        DescribeInstancePatchStatesPaginator,
        DescribeInstancePatchesPaginator,
        DescribeInstancePropertiesPaginator,
        DescribeInventoryDeletionsPaginator,
        DescribeMaintenanceWindowExecutionTaskInvocationsPaginator,
        DescribeMaintenanceWindowExecutionTasksPaginator,
        DescribeMaintenanceWindowExecutionsPaginator,
        DescribeMaintenanceWindowSchedulePaginator,
        DescribeMaintenanceWindowTargetsPaginator,
        DescribeMaintenanceWindowTasksPaginator,
        DescribeMaintenanceWindowsForTargetPaginator,
        DescribeMaintenanceWindowsPaginator,
        DescribeOpsItemsPaginator,
        DescribeParametersPaginator,
        DescribePatchBaselinesPaginator,
        DescribePatchGroupsPaginator,
        DescribePatchPropertiesPaginator,
        DescribeSessionsPaginator,
        GetInventoryPaginator,
        GetInventorySchemaPaginator,
        GetOpsSummaryPaginator,
        GetParameterHistoryPaginator,
        GetParametersByPathPaginator,
        GetResourcePoliciesPaginator,
        ListAssociationVersionsPaginator,
        ListAssociationsPaginator,
        ListCommandInvocationsPaginator,
        ListCommandsPaginator,
        ListComplianceItemsPaginator,
        ListComplianceSummariesPaginator,
        ListDocumentVersionsPaginator,
        ListDocumentsPaginator,
        ListOpsItemEventsPaginator,
        ListOpsItemRelatedItemsPaginator,
        ListOpsMetadataPaginator,
        ListResourceComplianceSummariesPaginator,
        ListResourceDataSyncPaginator,
    )

    session = get_session()
    with session.create_client("ssm") as client:
        client: SSMClient

        describe_activations_paginator: DescribeActivationsPaginator = client.get_paginator("describe_activations")
        describe_association_execution_targets_paginator: DescribeAssociationExecutionTargetsPaginator = client.get_paginator("describe_association_execution_targets")
        describe_association_executions_paginator: DescribeAssociationExecutionsPaginator = client.get_paginator("describe_association_executions")
        describe_automation_executions_paginator: DescribeAutomationExecutionsPaginator = client.get_paginator("describe_automation_executions")
        describe_automation_step_executions_paginator: DescribeAutomationStepExecutionsPaginator = client.get_paginator("describe_automation_step_executions")
        describe_available_patches_paginator: DescribeAvailablePatchesPaginator = client.get_paginator("describe_available_patches")
        describe_effective_instance_associations_paginator: DescribeEffectiveInstanceAssociationsPaginator = client.get_paginator("describe_effective_instance_associations")
        describe_effective_patches_for_patch_baseline_paginator: DescribeEffectivePatchesForPatchBaselinePaginator = client.get_paginator("describe_effective_patches_for_patch_baseline")
        describe_instance_associations_status_paginator: DescribeInstanceAssociationsStatusPaginator = client.get_paginator("describe_instance_associations_status")
        describe_instance_information_paginator: DescribeInstanceInformationPaginator = client.get_paginator("describe_instance_information")
        describe_instance_patch_states_for_patch_group_paginator: DescribeInstancePatchStatesForPatchGroupPaginator = client.get_paginator("describe_instance_patch_states_for_patch_group")
        describe_instance_patch_states_paginator: DescribeInstancePatchStatesPaginator = client.get_paginator("describe_instance_patch_states")
        describe_instance_patches_paginator: DescribeInstancePatchesPaginator = client.get_paginator("describe_instance_patches")
        describe_instance_properties_paginator: DescribeInstancePropertiesPaginator = client.get_paginator("describe_instance_properties")
        describe_inventory_deletions_paginator: DescribeInventoryDeletionsPaginator = client.get_paginator("describe_inventory_deletions")
        describe_maintenance_window_execution_task_invocations_paginator: DescribeMaintenanceWindowExecutionTaskInvocationsPaginator = client.get_paginator("describe_maintenance_window_execution_task_invocations")
        describe_maintenance_window_execution_tasks_paginator: DescribeMaintenanceWindowExecutionTasksPaginator = client.get_paginator("describe_maintenance_window_execution_tasks")
        describe_maintenance_window_executions_paginator: DescribeMaintenanceWindowExecutionsPaginator = client.get_paginator("describe_maintenance_window_executions")
        describe_maintenance_window_schedule_paginator: DescribeMaintenanceWindowSchedulePaginator = client.get_paginator("describe_maintenance_window_schedule")
        describe_maintenance_window_targets_paginator: DescribeMaintenanceWindowTargetsPaginator = client.get_paginator("describe_maintenance_window_targets")
        describe_maintenance_window_tasks_paginator: DescribeMaintenanceWindowTasksPaginator = client.get_paginator("describe_maintenance_window_tasks")
        describe_maintenance_windows_for_target_paginator: DescribeMaintenanceWindowsForTargetPaginator = client.get_paginator("describe_maintenance_windows_for_target")
        describe_maintenance_windows_paginator: DescribeMaintenanceWindowsPaginator = client.get_paginator("describe_maintenance_windows")
        describe_ops_items_paginator: DescribeOpsItemsPaginator = client.get_paginator("describe_ops_items")
        describe_parameters_paginator: DescribeParametersPaginator = client.get_paginator("describe_parameters")
        describe_patch_baselines_paginator: DescribePatchBaselinesPaginator = client.get_paginator("describe_patch_baselines")
        describe_patch_groups_paginator: DescribePatchGroupsPaginator = client.get_paginator("describe_patch_groups")
        describe_patch_properties_paginator: DescribePatchPropertiesPaginator = client.get_paginator("describe_patch_properties")
        describe_sessions_paginator: DescribeSessionsPaginator = client.get_paginator("describe_sessions")
        get_inventory_paginator: GetInventoryPaginator = client.get_paginator("get_inventory")
        get_inventory_schema_paginator: GetInventorySchemaPaginator = client.get_paginator("get_inventory_schema")
        get_ops_summary_paginator: GetOpsSummaryPaginator = client.get_paginator("get_ops_summary")
        get_parameter_history_paginator: GetParameterHistoryPaginator = client.get_paginator("get_parameter_history")
        get_parameters_by_path_paginator: GetParametersByPathPaginator = client.get_paginator("get_parameters_by_path")
        get_resource_policies_paginator: GetResourcePoliciesPaginator = client.get_paginator("get_resource_policies")
        list_association_versions_paginator: ListAssociationVersionsPaginator = client.get_paginator("list_association_versions")
        list_associations_paginator: ListAssociationsPaginator = client.get_paginator("list_associations")
        list_command_invocations_paginator: ListCommandInvocationsPaginator = client.get_paginator("list_command_invocations")
        list_commands_paginator: ListCommandsPaginator = client.get_paginator("list_commands")
        list_compliance_items_paginator: ListComplianceItemsPaginator = client.get_paginator("list_compliance_items")
        list_compliance_summaries_paginator: ListComplianceSummariesPaginator = client.get_paginator("list_compliance_summaries")
        list_document_versions_paginator: ListDocumentVersionsPaginator = client.get_paginator("list_document_versions")
        list_documents_paginator: ListDocumentsPaginator = client.get_paginator("list_documents")
        list_ops_item_events_paginator: ListOpsItemEventsPaginator = client.get_paginator("list_ops_item_events")
        list_ops_item_related_items_paginator: ListOpsItemRelatedItemsPaginator = client.get_paginator("list_ops_item_related_items")
        list_ops_metadata_paginator: ListOpsMetadataPaginator = client.get_paginator("list_ops_metadata")
        list_resource_compliance_summaries_paginator: ListResourceComplianceSummariesPaginator = client.get_paginator("list_resource_compliance_summaries")
        list_resource_data_sync_paginator: ListResourceDataSyncPaginator = client.get_paginator("list_resource_data_sync")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeActivationsRequestDescribeActivationsPaginateTypeDef,
    DescribeActivationsResultTypeDef,
    DescribeAssociationExecutionsRequestDescribeAssociationExecutionsPaginateTypeDef,
    DescribeAssociationExecutionsResultTypeDef,
    DescribeAssociationExecutionTargetsRequestDescribeAssociationExecutionTargetsPaginateTypeDef,
    DescribeAssociationExecutionTargetsResultTypeDef,
    DescribeAutomationExecutionsRequestDescribeAutomationExecutionsPaginateTypeDef,
    DescribeAutomationExecutionsResultTypeDef,
    DescribeAutomationStepExecutionsRequestDescribeAutomationStepExecutionsPaginateTypeDef,
    DescribeAutomationStepExecutionsResultTypeDef,
    DescribeAvailablePatchesRequestDescribeAvailablePatchesPaginateTypeDef,
    DescribeAvailablePatchesResultTypeDef,
    DescribeEffectiveInstanceAssociationsRequestDescribeEffectiveInstanceAssociationsPaginateTypeDef,
    DescribeEffectiveInstanceAssociationsResultTypeDef,
    DescribeEffectivePatchesForPatchBaselineRequestDescribeEffectivePatchesForPatchBaselinePaginateTypeDef,
    DescribeEffectivePatchesForPatchBaselineResultTypeDef,
    DescribeInstanceAssociationsStatusRequestDescribeInstanceAssociationsStatusPaginateTypeDef,
    DescribeInstanceAssociationsStatusResultTypeDef,
    DescribeInstanceInformationRequestDescribeInstanceInformationPaginateTypeDef,
    DescribeInstanceInformationResultTypeDef,
    DescribeInstancePatchesRequestDescribeInstancePatchesPaginateTypeDef,
    DescribeInstancePatchesResultTypeDef,
    DescribeInstancePatchStatesForPatchGroupRequestDescribeInstancePatchStatesForPatchGroupPaginateTypeDef,
    DescribeInstancePatchStatesForPatchGroupResultTypeDef,
    DescribeInstancePatchStatesRequestDescribeInstancePatchStatesPaginateTypeDef,
    DescribeInstancePatchStatesResultTypeDef,
    DescribeInstancePropertiesRequestDescribeInstancePropertiesPaginateTypeDef,
    DescribeInstancePropertiesResultTypeDef,
    DescribeInventoryDeletionsRequestDescribeInventoryDeletionsPaginateTypeDef,
    DescribeInventoryDeletionsResultTypeDef,
    DescribeMaintenanceWindowExecutionsRequestDescribeMaintenanceWindowExecutionsPaginateTypeDef,
    DescribeMaintenanceWindowExecutionsResultTypeDef,
    DescribeMaintenanceWindowExecutionTaskInvocationsRequestDescribeMaintenanceWindowExecutionTaskInvocationsPaginateTypeDef,
    DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef,
    DescribeMaintenanceWindowExecutionTasksRequestDescribeMaintenanceWindowExecutionTasksPaginateTypeDef,
    DescribeMaintenanceWindowExecutionTasksResultTypeDef,
    DescribeMaintenanceWindowScheduleRequestDescribeMaintenanceWindowSchedulePaginateTypeDef,
    DescribeMaintenanceWindowScheduleResultTypeDef,
    DescribeMaintenanceWindowsForTargetRequestDescribeMaintenanceWindowsForTargetPaginateTypeDef,
    DescribeMaintenanceWindowsForTargetResultTypeDef,
    DescribeMaintenanceWindowsRequestDescribeMaintenanceWindowsPaginateTypeDef,
    DescribeMaintenanceWindowsResultTypeDef,
    DescribeMaintenanceWindowTargetsRequestDescribeMaintenanceWindowTargetsPaginateTypeDef,
    DescribeMaintenanceWindowTargetsResultTypeDef,
    DescribeMaintenanceWindowTasksRequestDescribeMaintenanceWindowTasksPaginateTypeDef,
    DescribeMaintenanceWindowTasksResultTypeDef,
    DescribeOpsItemsRequestDescribeOpsItemsPaginateTypeDef,
    DescribeOpsItemsResponseTypeDef,
    DescribeParametersRequestDescribeParametersPaginateTypeDef,
    DescribeParametersResultTypeDef,
    DescribePatchBaselinesRequestDescribePatchBaselinesPaginateTypeDef,
    DescribePatchBaselinesResultTypeDef,
    DescribePatchGroupsRequestDescribePatchGroupsPaginateTypeDef,
    DescribePatchGroupsResultTypeDef,
    DescribePatchPropertiesRequestDescribePatchPropertiesPaginateTypeDef,
    DescribePatchPropertiesResultTypeDef,
    DescribeSessionsRequestDescribeSessionsPaginateTypeDef,
    DescribeSessionsResponseTypeDef,
    GetInventoryRequestGetInventoryPaginateTypeDef,
    GetInventoryResultTypeDef,
    GetInventorySchemaRequestGetInventorySchemaPaginateTypeDef,
    GetInventorySchemaResultTypeDef,
    GetOpsSummaryRequestGetOpsSummaryPaginateTypeDef,
    GetOpsSummaryResultTypeDef,
    GetParameterHistoryRequestGetParameterHistoryPaginateTypeDef,
    GetParameterHistoryResultTypeDef,
    GetParametersByPathRequestGetParametersByPathPaginateTypeDef,
    GetParametersByPathResultTypeDef,
    GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef,
    GetResourcePoliciesResponseTypeDef,
    ListAssociationsRequestListAssociationsPaginateTypeDef,
    ListAssociationsResultTypeDef,
    ListAssociationVersionsRequestListAssociationVersionsPaginateTypeDef,
    ListAssociationVersionsResultTypeDef,
    ListCommandInvocationsRequestListCommandInvocationsPaginateTypeDef,
    ListCommandInvocationsResultTypeDef,
    ListCommandsRequestListCommandsPaginateTypeDef,
    ListCommandsResultTypeDef,
    ListComplianceItemsRequestListComplianceItemsPaginateTypeDef,
    ListComplianceItemsResultTypeDef,
    ListComplianceSummariesRequestListComplianceSummariesPaginateTypeDef,
    ListComplianceSummariesResultTypeDef,
    ListDocumentsRequestListDocumentsPaginateTypeDef,
    ListDocumentsResultTypeDef,
    ListDocumentVersionsRequestListDocumentVersionsPaginateTypeDef,
    ListDocumentVersionsResultTypeDef,
    ListOpsItemEventsRequestListOpsItemEventsPaginateTypeDef,
    ListOpsItemEventsResponseTypeDef,
    ListOpsItemRelatedItemsRequestListOpsItemRelatedItemsPaginateTypeDef,
    ListOpsItemRelatedItemsResponseTypeDef,
    ListOpsMetadataRequestListOpsMetadataPaginateTypeDef,
    ListOpsMetadataResultTypeDef,
    ListResourceComplianceSummariesRequestListResourceComplianceSummariesPaginateTypeDef,
    ListResourceComplianceSummariesResultTypeDef,
    ListResourceDataSyncRequestListResourceDataSyncPaginateTypeDef,
    ListResourceDataSyncResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeActivationsPaginator",
    "DescribeAssociationExecutionTargetsPaginator",
    "DescribeAssociationExecutionsPaginator",
    "DescribeAutomationExecutionsPaginator",
    "DescribeAutomationStepExecutionsPaginator",
    "DescribeAvailablePatchesPaginator",
    "DescribeEffectiveInstanceAssociationsPaginator",
    "DescribeEffectivePatchesForPatchBaselinePaginator",
    "DescribeInstanceAssociationsStatusPaginator",
    "DescribeInstanceInformationPaginator",
    "DescribeInstancePatchStatesForPatchGroupPaginator",
    "DescribeInstancePatchStatesPaginator",
    "DescribeInstancePatchesPaginator",
    "DescribeInstancePropertiesPaginator",
    "DescribeInventoryDeletionsPaginator",
    "DescribeMaintenanceWindowExecutionTaskInvocationsPaginator",
    "DescribeMaintenanceWindowExecutionTasksPaginator",
    "DescribeMaintenanceWindowExecutionsPaginator",
    "DescribeMaintenanceWindowSchedulePaginator",
    "DescribeMaintenanceWindowTargetsPaginator",
    "DescribeMaintenanceWindowTasksPaginator",
    "DescribeMaintenanceWindowsForTargetPaginator",
    "DescribeMaintenanceWindowsPaginator",
    "DescribeOpsItemsPaginator",
    "DescribeParametersPaginator",
    "DescribePatchBaselinesPaginator",
    "DescribePatchGroupsPaginator",
    "DescribePatchPropertiesPaginator",
    "DescribeSessionsPaginator",
    "GetInventoryPaginator",
    "GetInventorySchemaPaginator",
    "GetOpsSummaryPaginator",
    "GetParameterHistoryPaginator",
    "GetParametersByPathPaginator",
    "GetResourcePoliciesPaginator",
    "ListAssociationVersionsPaginator",
    "ListAssociationsPaginator",
    "ListCommandInvocationsPaginator",
    "ListCommandsPaginator",
    "ListComplianceItemsPaginator",
    "ListComplianceSummariesPaginator",
    "ListDocumentVersionsPaginator",
    "ListDocumentsPaginator",
    "ListOpsItemEventsPaginator",
    "ListOpsItemRelatedItemsPaginator",
    "ListOpsMetadataPaginator",
    "ListResourceComplianceSummariesPaginator",
    "ListResourceDataSyncPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeActivationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeActivations.html#SSM.Paginator.DescribeActivations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeactivationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeActivationsRequestDescribeActivationsPaginateTypeDef]
    ) -> AsyncIterator[DescribeActivationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeActivations.html#SSM.Paginator.DescribeActivations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeactivationspaginator)
        """


class DescribeAssociationExecutionTargetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAssociationExecutionTargets.html#SSM.Paginator.DescribeAssociationExecutionTargets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeassociationexecutiontargetspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAssociationExecutionTargetsRequestDescribeAssociationExecutionTargetsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeAssociationExecutionTargetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAssociationExecutionTargets.html#SSM.Paginator.DescribeAssociationExecutionTargets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeassociationexecutiontargetspaginator)
        """


class DescribeAssociationExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAssociationExecutions.html#SSM.Paginator.DescribeAssociationExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeassociationexecutionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAssociationExecutionsRequestDescribeAssociationExecutionsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeAssociationExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAssociationExecutions.html#SSM.Paginator.DescribeAssociationExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeassociationexecutionspaginator)
        """


class DescribeAutomationExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAutomationExecutions.html#SSM.Paginator.DescribeAutomationExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeautomationexecutionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAutomationExecutionsRequestDescribeAutomationExecutionsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeAutomationExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAutomationExecutions.html#SSM.Paginator.DescribeAutomationExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeautomationexecutionspaginator)
        """


class DescribeAutomationStepExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAutomationStepExecutions.html#SSM.Paginator.DescribeAutomationStepExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeautomationstepexecutionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAutomationStepExecutionsRequestDescribeAutomationStepExecutionsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeAutomationStepExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAutomationStepExecutions.html#SSM.Paginator.DescribeAutomationStepExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeautomationstepexecutionspaginator)
        """


class DescribeAvailablePatchesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAvailablePatches.html#SSM.Paginator.DescribeAvailablePatches)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeavailablepatchespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeAvailablePatchesRequestDescribeAvailablePatchesPaginateTypeDef],
    ) -> AsyncIterator[DescribeAvailablePatchesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAvailablePatches.html#SSM.Paginator.DescribeAvailablePatches.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeavailablepatchespaginator)
        """


class DescribeEffectiveInstanceAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeEffectiveInstanceAssociations.html#SSM.Paginator.DescribeEffectiveInstanceAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeeffectiveinstanceassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEffectiveInstanceAssociationsRequestDescribeEffectiveInstanceAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeEffectiveInstanceAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeEffectiveInstanceAssociations.html#SSM.Paginator.DescribeEffectiveInstanceAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeeffectiveinstanceassociationspaginator)
        """


class DescribeEffectivePatchesForPatchBaselinePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeEffectivePatchesForPatchBaseline.html#SSM.Paginator.DescribeEffectivePatchesForPatchBaseline)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeeffectivepatchesforpatchbaselinepaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEffectivePatchesForPatchBaselineRequestDescribeEffectivePatchesForPatchBaselinePaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeEffectivePatchesForPatchBaselineResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeEffectivePatchesForPatchBaseline.html#SSM.Paginator.DescribeEffectivePatchesForPatchBaseline.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeeffectivepatchesforpatchbaselinepaginator)
        """


class DescribeInstanceAssociationsStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceAssociationsStatus.html#SSM.Paginator.DescribeInstanceAssociationsStatus)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstanceassociationsstatuspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInstanceAssociationsStatusRequestDescribeInstanceAssociationsStatusPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeInstanceAssociationsStatusResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceAssociationsStatus.html#SSM.Paginator.DescribeInstanceAssociationsStatus.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstanceassociationsstatuspaginator)
        """


class DescribeInstanceInformationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceInformation.html#SSM.Paginator.DescribeInstanceInformation)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstanceinformationpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInstanceInformationRequestDescribeInstanceInformationPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeInstanceInformationResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceInformation.html#SSM.Paginator.DescribeInstanceInformation.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstanceinformationpaginator)
        """


class DescribeInstancePatchStatesForPatchGroupPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatchStatesForPatchGroup.html#SSM.Paginator.DescribeInstancePatchStatesForPatchGroup)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstancepatchstatesforpatchgrouppaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInstancePatchStatesForPatchGroupRequestDescribeInstancePatchStatesForPatchGroupPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeInstancePatchStatesForPatchGroupResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatchStatesForPatchGroup.html#SSM.Paginator.DescribeInstancePatchStatesForPatchGroup.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstancepatchstatesforpatchgrouppaginator)
        """


class DescribeInstancePatchStatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatchStates.html#SSM.Paginator.DescribeInstancePatchStates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstancepatchstatespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInstancePatchStatesRequestDescribeInstancePatchStatesPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeInstancePatchStatesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatchStates.html#SSM.Paginator.DescribeInstancePatchStates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstancepatchstatespaginator)
        """


class DescribeInstancePatchesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatches.html#SSM.Paginator.DescribeInstancePatches)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstancepatchespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeInstancePatchesRequestDescribeInstancePatchesPaginateTypeDef]
    ) -> AsyncIterator[DescribeInstancePatchesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatches.html#SSM.Paginator.DescribeInstancePatches.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstancepatchespaginator)
        """


class DescribeInstancePropertiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceProperties.html#SSM.Paginator.DescribeInstanceProperties)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstancepropertiespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInstancePropertiesRequestDescribeInstancePropertiesPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeInstancePropertiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceProperties.html#SSM.Paginator.DescribeInstanceProperties.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstancepropertiespaginator)
        """


class DescribeInventoryDeletionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInventoryDeletions.html#SSM.Paginator.DescribeInventoryDeletions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinventorydeletionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeInventoryDeletionsRequestDescribeInventoryDeletionsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeInventoryDeletionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInventoryDeletions.html#SSM.Paginator.DescribeInventoryDeletions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinventorydeletionspaginator)
        """


class DescribeMaintenanceWindowExecutionTaskInvocationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutionTaskInvocations.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTaskInvocations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowexecutiontaskinvocationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMaintenanceWindowExecutionTaskInvocationsRequestDescribeMaintenanceWindowExecutionTaskInvocationsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutionTaskInvocations.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTaskInvocations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowexecutiontaskinvocationspaginator)
        """


class DescribeMaintenanceWindowExecutionTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutionTasks.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowexecutiontaskspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMaintenanceWindowExecutionTasksRequestDescribeMaintenanceWindowExecutionTasksPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeMaintenanceWindowExecutionTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutionTasks.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowexecutiontaskspaginator)
        """


class DescribeMaintenanceWindowExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutions.html#SSM.Paginator.DescribeMaintenanceWindowExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowexecutionspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMaintenanceWindowExecutionsRequestDescribeMaintenanceWindowExecutionsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeMaintenanceWindowExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutions.html#SSM.Paginator.DescribeMaintenanceWindowExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowexecutionspaginator)
        """


class DescribeMaintenanceWindowSchedulePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowSchedule.html#SSM.Paginator.DescribeMaintenanceWindowSchedule)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowschedulepaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMaintenanceWindowScheduleRequestDescribeMaintenanceWindowSchedulePaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeMaintenanceWindowScheduleResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowSchedule.html#SSM.Paginator.DescribeMaintenanceWindowSchedule.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowschedulepaginator)
        """


class DescribeMaintenanceWindowTargetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowTargets.html#SSM.Paginator.DescribeMaintenanceWindowTargets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowtargetspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMaintenanceWindowTargetsRequestDescribeMaintenanceWindowTargetsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeMaintenanceWindowTargetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowTargets.html#SSM.Paginator.DescribeMaintenanceWindowTargets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowtargetspaginator)
        """


class DescribeMaintenanceWindowTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowTasks.html#SSM.Paginator.DescribeMaintenanceWindowTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowtaskspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMaintenanceWindowTasksRequestDescribeMaintenanceWindowTasksPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeMaintenanceWindowTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowTasks.html#SSM.Paginator.DescribeMaintenanceWindowTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowtaskspaginator)
        """


class DescribeMaintenanceWindowsForTargetPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowsForTarget.html#SSM.Paginator.DescribeMaintenanceWindowsForTarget)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowsfortargetpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMaintenanceWindowsForTargetRequestDescribeMaintenanceWindowsForTargetPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeMaintenanceWindowsForTargetResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowsForTarget.html#SSM.Paginator.DescribeMaintenanceWindowsForTarget.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowsfortargetpaginator)
        """


class DescribeMaintenanceWindowsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindows.html#SSM.Paginator.DescribeMaintenanceWindows)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeMaintenanceWindowsRequestDescribeMaintenanceWindowsPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeMaintenanceWindowsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindows.html#SSM.Paginator.DescribeMaintenanceWindows.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowspaginator)
        """


class DescribeOpsItemsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeOpsItems.html#SSM.Paginator.DescribeOpsItems)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeopsitemspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeOpsItemsRequestDescribeOpsItemsPaginateTypeDef]
    ) -> AsyncIterator[DescribeOpsItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeOpsItems.html#SSM.Paginator.DescribeOpsItems.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeopsitemspaginator)
        """


class DescribeParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeParameters.html#SSM.Paginator.DescribeParameters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeparameterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeParametersRequestDescribeParametersPaginateTypeDef]
    ) -> AsyncIterator[DescribeParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeParameters.html#SSM.Paginator.DescribeParameters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeparameterspaginator)
        """


class DescribePatchBaselinesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchBaselines.html#SSM.Paginator.DescribePatchBaselines)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describepatchbaselinespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribePatchBaselinesRequestDescribePatchBaselinesPaginateTypeDef]
    ) -> AsyncIterator[DescribePatchBaselinesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchBaselines.html#SSM.Paginator.DescribePatchBaselines.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describepatchbaselinespaginator)
        """


class DescribePatchGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchGroups.html#SSM.Paginator.DescribePatchGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describepatchgroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribePatchGroupsRequestDescribePatchGroupsPaginateTypeDef]
    ) -> AsyncIterator[DescribePatchGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchGroups.html#SSM.Paginator.DescribePatchGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describepatchgroupspaginator)
        """


class DescribePatchPropertiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchProperties.html#SSM.Paginator.DescribePatchProperties)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describepatchpropertiespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribePatchPropertiesRequestDescribePatchPropertiesPaginateTypeDef]
    ) -> AsyncIterator[DescribePatchPropertiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchProperties.html#SSM.Paginator.DescribePatchProperties.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describepatchpropertiespaginator)
        """


class DescribeSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeSessions.html#SSM.Paginator.DescribeSessions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describesessionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeSessionsRequestDescribeSessionsPaginateTypeDef]
    ) -> AsyncIterator[DescribeSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeSessions.html#SSM.Paginator.DescribeSessions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describesessionspaginator)
        """


class GetInventoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetInventory.html#SSM.Paginator.GetInventory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getinventorypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetInventoryRequestGetInventoryPaginateTypeDef]
    ) -> AsyncIterator[GetInventoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetInventory.html#SSM.Paginator.GetInventory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getinventorypaginator)
        """


class GetInventorySchemaPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetInventorySchema.html#SSM.Paginator.GetInventorySchema)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getinventoryschemapaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetInventorySchemaRequestGetInventorySchemaPaginateTypeDef]
    ) -> AsyncIterator[GetInventorySchemaResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetInventorySchema.html#SSM.Paginator.GetInventorySchema.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getinventoryschemapaginator)
        """


class GetOpsSummaryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetOpsSummary.html#SSM.Paginator.GetOpsSummary)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getopssummarypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetOpsSummaryRequestGetOpsSummaryPaginateTypeDef]
    ) -> AsyncIterator[GetOpsSummaryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetOpsSummary.html#SSM.Paginator.GetOpsSummary.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getopssummarypaginator)
        """


class GetParameterHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetParameterHistory.html#SSM.Paginator.GetParameterHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getparameterhistorypaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetParameterHistoryRequestGetParameterHistoryPaginateTypeDef]
    ) -> AsyncIterator[GetParameterHistoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetParameterHistory.html#SSM.Paginator.GetParameterHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getparameterhistorypaginator)
        """


class GetParametersByPathPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetParametersByPath.html#SSM.Paginator.GetParametersByPath)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getparametersbypathpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetParametersByPathRequestGetParametersByPathPaginateTypeDef]
    ) -> AsyncIterator[GetParametersByPathResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetParametersByPath.html#SSM.Paginator.GetParametersByPath.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getparametersbypathpaginator)
        """


class GetResourcePoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetResourcePolicies.html#SSM.Paginator.GetResourcePolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getresourcepoliciespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef]
    ) -> AsyncIterator[GetResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetResourcePolicies.html#SSM.Paginator.GetResourcePolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getresourcepoliciespaginator)
        """


class ListAssociationVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListAssociationVersions.html#SSM.Paginator.ListAssociationVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listassociationversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssociationVersionsRequestListAssociationVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListAssociationVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListAssociationVersions.html#SSM.Paginator.ListAssociationVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listassociationversionspaginator)
        """


class ListAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListAssociations.html#SSM.Paginator.ListAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listassociationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAssociationsRequestListAssociationsPaginateTypeDef]
    ) -> AsyncIterator[ListAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListAssociations.html#SSM.Paginator.ListAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listassociationspaginator)
        """


class ListCommandInvocationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListCommandInvocations.html#SSM.Paginator.ListCommandInvocations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listcommandinvocationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCommandInvocationsRequestListCommandInvocationsPaginateTypeDef]
    ) -> AsyncIterator[ListCommandInvocationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListCommandInvocations.html#SSM.Paginator.ListCommandInvocations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listcommandinvocationspaginator)
        """


class ListCommandsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListCommands.html#SSM.Paginator.ListCommands)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listcommandspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCommandsRequestListCommandsPaginateTypeDef]
    ) -> AsyncIterator[ListCommandsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListCommands.html#SSM.Paginator.ListCommands.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listcommandspaginator)
        """


class ListComplianceItemsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListComplianceItems.html#SSM.Paginator.ListComplianceItems)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listcomplianceitemspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListComplianceItemsRequestListComplianceItemsPaginateTypeDef]
    ) -> AsyncIterator[ListComplianceItemsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListComplianceItems.html#SSM.Paginator.ListComplianceItems.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listcomplianceitemspaginator)
        """


class ListComplianceSummariesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListComplianceSummaries.html#SSM.Paginator.ListComplianceSummaries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listcompliancesummariespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListComplianceSummariesRequestListComplianceSummariesPaginateTypeDef]
    ) -> AsyncIterator[ListComplianceSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListComplianceSummaries.html#SSM.Paginator.ListComplianceSummaries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listcompliancesummariespaginator)
        """


class ListDocumentVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListDocumentVersions.html#SSM.Paginator.ListDocumentVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listdocumentversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDocumentVersionsRequestListDocumentVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListDocumentVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListDocumentVersions.html#SSM.Paginator.ListDocumentVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listdocumentversionspaginator)
        """


class ListDocumentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListDocuments.html#SSM.Paginator.ListDocuments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listdocumentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDocumentsRequestListDocumentsPaginateTypeDef]
    ) -> AsyncIterator[ListDocumentsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListDocuments.html#SSM.Paginator.ListDocuments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listdocumentspaginator)
        """


class ListOpsItemEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsItemEvents.html#SSM.Paginator.ListOpsItemEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listopsitemeventspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOpsItemEventsRequestListOpsItemEventsPaginateTypeDef]
    ) -> AsyncIterator[ListOpsItemEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsItemEvents.html#SSM.Paginator.ListOpsItemEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listopsitemeventspaginator)
        """


class ListOpsItemRelatedItemsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsItemRelatedItems.html#SSM.Paginator.ListOpsItemRelatedItems)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listopsitemrelateditemspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOpsItemRelatedItemsRequestListOpsItemRelatedItemsPaginateTypeDef]
    ) -> AsyncIterator[ListOpsItemRelatedItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsItemRelatedItems.html#SSM.Paginator.ListOpsItemRelatedItems.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listopsitemrelateditemspaginator)
        """


class ListOpsMetadataPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsMetadata.html#SSM.Paginator.ListOpsMetadata)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listopsmetadatapaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOpsMetadataRequestListOpsMetadataPaginateTypeDef]
    ) -> AsyncIterator[ListOpsMetadataResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsMetadata.html#SSM.Paginator.ListOpsMetadata.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listopsmetadatapaginator)
        """


class ListResourceComplianceSummariesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListResourceComplianceSummaries.html#SSM.Paginator.ListResourceComplianceSummaries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listresourcecompliancesummariespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListResourceComplianceSummariesRequestListResourceComplianceSummariesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListResourceComplianceSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListResourceComplianceSummaries.html#SSM.Paginator.ListResourceComplianceSummaries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listresourcecompliancesummariespaginator)
        """


class ListResourceDataSyncPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListResourceDataSync.html#SSM.Paginator.ListResourceDataSync)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listresourcedatasyncpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListResourceDataSyncRequestListResourceDataSyncPaginateTypeDef]
    ) -> AsyncIterator[ListResourceDataSyncResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListResourceDataSync.html#SSM.Paginator.ListResourceDataSync.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listresourcedatasyncpaginator)
        """
