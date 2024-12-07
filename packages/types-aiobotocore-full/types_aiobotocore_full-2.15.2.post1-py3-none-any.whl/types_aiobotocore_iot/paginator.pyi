"""
Type annotations for iot service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iot.client import IoTClient
    from types_aiobotocore_iot.paginator import (
        GetBehaviorModelTrainingSummariesPaginator,
        ListActiveViolationsPaginator,
        ListAttachedPoliciesPaginator,
        ListAuditFindingsPaginator,
        ListAuditMitigationActionsExecutionsPaginator,
        ListAuditMitigationActionsTasksPaginator,
        ListAuditSuppressionsPaginator,
        ListAuditTasksPaginator,
        ListAuthorizersPaginator,
        ListBillingGroupsPaginator,
        ListCACertificatesPaginator,
        ListCertificatesByCAPaginator,
        ListCertificatesPaginator,
        ListCustomMetricsPaginator,
        ListDetectMitigationActionsExecutionsPaginator,
        ListDetectMitigationActionsTasksPaginator,
        ListDimensionsPaginator,
        ListDomainConfigurationsPaginator,
        ListFleetMetricsPaginator,
        ListIndicesPaginator,
        ListJobExecutionsForJobPaginator,
        ListJobExecutionsForThingPaginator,
        ListJobTemplatesPaginator,
        ListJobsPaginator,
        ListManagedJobTemplatesPaginator,
        ListMetricValuesPaginator,
        ListMitigationActionsPaginator,
        ListOTAUpdatesPaginator,
        ListOutgoingCertificatesPaginator,
        ListPackageVersionsPaginator,
        ListPackagesPaginator,
        ListPoliciesPaginator,
        ListPolicyPrincipalsPaginator,
        ListPrincipalPoliciesPaginator,
        ListPrincipalThingsPaginator,
        ListProvisioningTemplateVersionsPaginator,
        ListProvisioningTemplatesPaginator,
        ListRelatedResourcesForAuditFindingPaginator,
        ListRoleAliasesPaginator,
        ListSbomValidationResultsPaginator,
        ListScheduledAuditsPaginator,
        ListSecurityProfilesForTargetPaginator,
        ListSecurityProfilesPaginator,
        ListStreamsPaginator,
        ListTagsForResourcePaginator,
        ListTargetsForPolicyPaginator,
        ListTargetsForSecurityProfilePaginator,
        ListThingGroupsForThingPaginator,
        ListThingGroupsPaginator,
        ListThingPrincipalsPaginator,
        ListThingRegistrationTaskReportsPaginator,
        ListThingRegistrationTasksPaginator,
        ListThingTypesPaginator,
        ListThingsInBillingGroupPaginator,
        ListThingsInThingGroupPaginator,
        ListThingsPaginator,
        ListTopicRuleDestinationsPaginator,
        ListTopicRulesPaginator,
        ListV2LoggingLevelsPaginator,
        ListViolationEventsPaginator,
    )

    session = get_session()
    with session.create_client("iot") as client:
        client: IoTClient

        get_behavior_model_training_summaries_paginator: GetBehaviorModelTrainingSummariesPaginator = client.get_paginator("get_behavior_model_training_summaries")
        list_active_violations_paginator: ListActiveViolationsPaginator = client.get_paginator("list_active_violations")
        list_attached_policies_paginator: ListAttachedPoliciesPaginator = client.get_paginator("list_attached_policies")
        list_audit_findings_paginator: ListAuditFindingsPaginator = client.get_paginator("list_audit_findings")
        list_audit_mitigation_actions_executions_paginator: ListAuditMitigationActionsExecutionsPaginator = client.get_paginator("list_audit_mitigation_actions_executions")
        list_audit_mitigation_actions_tasks_paginator: ListAuditMitigationActionsTasksPaginator = client.get_paginator("list_audit_mitigation_actions_tasks")
        list_audit_suppressions_paginator: ListAuditSuppressionsPaginator = client.get_paginator("list_audit_suppressions")
        list_audit_tasks_paginator: ListAuditTasksPaginator = client.get_paginator("list_audit_tasks")
        list_authorizers_paginator: ListAuthorizersPaginator = client.get_paginator("list_authorizers")
        list_billing_groups_paginator: ListBillingGroupsPaginator = client.get_paginator("list_billing_groups")
        list_ca_certificates_paginator: ListCACertificatesPaginator = client.get_paginator("list_ca_certificates")
        list_certificates_by_ca_paginator: ListCertificatesByCAPaginator = client.get_paginator("list_certificates_by_ca")
        list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
        list_custom_metrics_paginator: ListCustomMetricsPaginator = client.get_paginator("list_custom_metrics")
        list_detect_mitigation_actions_executions_paginator: ListDetectMitigationActionsExecutionsPaginator = client.get_paginator("list_detect_mitigation_actions_executions")
        list_detect_mitigation_actions_tasks_paginator: ListDetectMitigationActionsTasksPaginator = client.get_paginator("list_detect_mitigation_actions_tasks")
        list_dimensions_paginator: ListDimensionsPaginator = client.get_paginator("list_dimensions")
        list_domain_configurations_paginator: ListDomainConfigurationsPaginator = client.get_paginator("list_domain_configurations")
        list_fleet_metrics_paginator: ListFleetMetricsPaginator = client.get_paginator("list_fleet_metrics")
        list_indices_paginator: ListIndicesPaginator = client.get_paginator("list_indices")
        list_job_executions_for_job_paginator: ListJobExecutionsForJobPaginator = client.get_paginator("list_job_executions_for_job")
        list_job_executions_for_thing_paginator: ListJobExecutionsForThingPaginator = client.get_paginator("list_job_executions_for_thing")
        list_job_templates_paginator: ListJobTemplatesPaginator = client.get_paginator("list_job_templates")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_managed_job_templates_paginator: ListManagedJobTemplatesPaginator = client.get_paginator("list_managed_job_templates")
        list_metric_values_paginator: ListMetricValuesPaginator = client.get_paginator("list_metric_values")
        list_mitigation_actions_paginator: ListMitigationActionsPaginator = client.get_paginator("list_mitigation_actions")
        list_ota_updates_paginator: ListOTAUpdatesPaginator = client.get_paginator("list_ota_updates")
        list_outgoing_certificates_paginator: ListOutgoingCertificatesPaginator = client.get_paginator("list_outgoing_certificates")
        list_package_versions_paginator: ListPackageVersionsPaginator = client.get_paginator("list_package_versions")
        list_packages_paginator: ListPackagesPaginator = client.get_paginator("list_packages")
        list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
        list_policy_principals_paginator: ListPolicyPrincipalsPaginator = client.get_paginator("list_policy_principals")
        list_principal_policies_paginator: ListPrincipalPoliciesPaginator = client.get_paginator("list_principal_policies")
        list_principal_things_paginator: ListPrincipalThingsPaginator = client.get_paginator("list_principal_things")
        list_provisioning_template_versions_paginator: ListProvisioningTemplateVersionsPaginator = client.get_paginator("list_provisioning_template_versions")
        list_provisioning_templates_paginator: ListProvisioningTemplatesPaginator = client.get_paginator("list_provisioning_templates")
        list_related_resources_for_audit_finding_paginator: ListRelatedResourcesForAuditFindingPaginator = client.get_paginator("list_related_resources_for_audit_finding")
        list_role_aliases_paginator: ListRoleAliasesPaginator = client.get_paginator("list_role_aliases")
        list_sbom_validation_results_paginator: ListSbomValidationResultsPaginator = client.get_paginator("list_sbom_validation_results")
        list_scheduled_audits_paginator: ListScheduledAuditsPaginator = client.get_paginator("list_scheduled_audits")
        list_security_profiles_for_target_paginator: ListSecurityProfilesForTargetPaginator = client.get_paginator("list_security_profiles_for_target")
        list_security_profiles_paginator: ListSecurityProfilesPaginator = client.get_paginator("list_security_profiles")
        list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        list_targets_for_policy_paginator: ListTargetsForPolicyPaginator = client.get_paginator("list_targets_for_policy")
        list_targets_for_security_profile_paginator: ListTargetsForSecurityProfilePaginator = client.get_paginator("list_targets_for_security_profile")
        list_thing_groups_for_thing_paginator: ListThingGroupsForThingPaginator = client.get_paginator("list_thing_groups_for_thing")
        list_thing_groups_paginator: ListThingGroupsPaginator = client.get_paginator("list_thing_groups")
        list_thing_principals_paginator: ListThingPrincipalsPaginator = client.get_paginator("list_thing_principals")
        list_thing_registration_task_reports_paginator: ListThingRegistrationTaskReportsPaginator = client.get_paginator("list_thing_registration_task_reports")
        list_thing_registration_tasks_paginator: ListThingRegistrationTasksPaginator = client.get_paginator("list_thing_registration_tasks")
        list_thing_types_paginator: ListThingTypesPaginator = client.get_paginator("list_thing_types")
        list_things_in_billing_group_paginator: ListThingsInBillingGroupPaginator = client.get_paginator("list_things_in_billing_group")
        list_things_in_thing_group_paginator: ListThingsInThingGroupPaginator = client.get_paginator("list_things_in_thing_group")
        list_things_paginator: ListThingsPaginator = client.get_paginator("list_things")
        list_topic_rule_destinations_paginator: ListTopicRuleDestinationsPaginator = client.get_paginator("list_topic_rule_destinations")
        list_topic_rules_paginator: ListTopicRulesPaginator = client.get_paginator("list_topic_rules")
        list_v2_logging_levels_paginator: ListV2LoggingLevelsPaginator = client.get_paginator("list_v2_logging_levels")
        list_violation_events_paginator: ListViolationEventsPaginator = client.get_paginator("list_violation_events")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetBehaviorModelTrainingSummariesRequestGetBehaviorModelTrainingSummariesPaginateTypeDef,
    GetBehaviorModelTrainingSummariesResponseTypeDef,
    ListActiveViolationsRequestListActiveViolationsPaginateTypeDef,
    ListActiveViolationsResponseTypeDef,
    ListAttachedPoliciesRequestListAttachedPoliciesPaginateTypeDef,
    ListAttachedPoliciesResponseTypeDef,
    ListAuditFindingsRequestListAuditFindingsPaginateTypeDef,
    ListAuditFindingsResponseTypeDef,
    ListAuditMitigationActionsExecutionsRequestListAuditMitigationActionsExecutionsPaginateTypeDef,
    ListAuditMitigationActionsExecutionsResponseTypeDef,
    ListAuditMitigationActionsTasksRequestListAuditMitigationActionsTasksPaginateTypeDef,
    ListAuditMitigationActionsTasksResponseTypeDef,
    ListAuditSuppressionsRequestListAuditSuppressionsPaginateTypeDef,
    ListAuditSuppressionsResponseTypeDef,
    ListAuditTasksRequestListAuditTasksPaginateTypeDef,
    ListAuditTasksResponseTypeDef,
    ListAuthorizersRequestListAuthorizersPaginateTypeDef,
    ListAuthorizersResponseTypeDef,
    ListBillingGroupsRequestListBillingGroupsPaginateTypeDef,
    ListBillingGroupsResponseTypeDef,
    ListCACertificatesRequestListCACertificatesPaginateTypeDef,
    ListCACertificatesResponseTypeDef,
    ListCertificatesByCARequestListCertificatesByCAPaginateTypeDef,
    ListCertificatesByCAResponseTypeDef,
    ListCertificatesRequestListCertificatesPaginateTypeDef,
    ListCertificatesResponseTypeDef,
    ListCustomMetricsRequestListCustomMetricsPaginateTypeDef,
    ListCustomMetricsResponseTypeDef,
    ListDetectMitigationActionsExecutionsRequestListDetectMitigationActionsExecutionsPaginateTypeDef,
    ListDetectMitigationActionsExecutionsResponseTypeDef,
    ListDetectMitigationActionsTasksRequestListDetectMitigationActionsTasksPaginateTypeDef,
    ListDetectMitigationActionsTasksResponseTypeDef,
    ListDimensionsRequestListDimensionsPaginateTypeDef,
    ListDimensionsResponseTypeDef,
    ListDomainConfigurationsRequestListDomainConfigurationsPaginateTypeDef,
    ListDomainConfigurationsResponseTypeDef,
    ListFleetMetricsRequestListFleetMetricsPaginateTypeDef,
    ListFleetMetricsResponseTypeDef,
    ListIndicesRequestListIndicesPaginateTypeDef,
    ListIndicesResponseTypeDef,
    ListJobExecutionsForJobRequestListJobExecutionsForJobPaginateTypeDef,
    ListJobExecutionsForJobResponseTypeDef,
    ListJobExecutionsForThingRequestListJobExecutionsForThingPaginateTypeDef,
    ListJobExecutionsForThingResponseTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListJobTemplatesRequestListJobTemplatesPaginateTypeDef,
    ListJobTemplatesResponseTypeDef,
    ListManagedJobTemplatesRequestListManagedJobTemplatesPaginateTypeDef,
    ListManagedJobTemplatesResponseTypeDef,
    ListMetricValuesRequestListMetricValuesPaginateTypeDef,
    ListMetricValuesResponseTypeDef,
    ListMitigationActionsRequestListMitigationActionsPaginateTypeDef,
    ListMitigationActionsResponseTypeDef,
    ListOTAUpdatesRequestListOTAUpdatesPaginateTypeDef,
    ListOTAUpdatesResponseTypeDef,
    ListOutgoingCertificatesRequestListOutgoingCertificatesPaginateTypeDef,
    ListOutgoingCertificatesResponseTypeDef,
    ListPackagesRequestListPackagesPaginateTypeDef,
    ListPackagesResponseTypeDef,
    ListPackageVersionsRequestListPackageVersionsPaginateTypeDef,
    ListPackageVersionsResponseTypeDef,
    ListPoliciesRequestListPoliciesPaginateTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyPrincipalsRequestListPolicyPrincipalsPaginateTypeDef,
    ListPolicyPrincipalsResponseTypeDef,
    ListPrincipalPoliciesRequestListPrincipalPoliciesPaginateTypeDef,
    ListPrincipalPoliciesResponseTypeDef,
    ListPrincipalThingsRequestListPrincipalThingsPaginateTypeDef,
    ListPrincipalThingsResponseTypeDef,
    ListProvisioningTemplatesRequestListProvisioningTemplatesPaginateTypeDef,
    ListProvisioningTemplatesResponseTypeDef,
    ListProvisioningTemplateVersionsRequestListProvisioningTemplateVersionsPaginateTypeDef,
    ListProvisioningTemplateVersionsResponseTypeDef,
    ListRelatedResourcesForAuditFindingRequestListRelatedResourcesForAuditFindingPaginateTypeDef,
    ListRelatedResourcesForAuditFindingResponseTypeDef,
    ListRoleAliasesRequestListRoleAliasesPaginateTypeDef,
    ListRoleAliasesResponseTypeDef,
    ListSbomValidationResultsRequestListSbomValidationResultsPaginateTypeDef,
    ListSbomValidationResultsResponseTypeDef,
    ListScheduledAuditsRequestListScheduledAuditsPaginateTypeDef,
    ListScheduledAuditsResponseTypeDef,
    ListSecurityProfilesForTargetRequestListSecurityProfilesForTargetPaginateTypeDef,
    ListSecurityProfilesForTargetResponseTypeDef,
    ListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef,
    ListSecurityProfilesResponseTypeDef,
    ListStreamsRequestListStreamsPaginateTypeDef,
    ListStreamsResponseTypeDef,
    ListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef,
    ListTargetsForPolicyResponseTypeDef,
    ListTargetsForSecurityProfileRequestListTargetsForSecurityProfilePaginateTypeDef,
    ListTargetsForSecurityProfileResponseTypeDef,
    ListThingGroupsForThingRequestListThingGroupsForThingPaginateTypeDef,
    ListThingGroupsForThingResponseTypeDef,
    ListThingGroupsRequestListThingGroupsPaginateTypeDef,
    ListThingGroupsResponseTypeDef,
    ListThingPrincipalsRequestListThingPrincipalsPaginateTypeDef,
    ListThingPrincipalsResponseTypeDef,
    ListThingRegistrationTaskReportsRequestListThingRegistrationTaskReportsPaginateTypeDef,
    ListThingRegistrationTaskReportsResponseTypeDef,
    ListThingRegistrationTasksRequestListThingRegistrationTasksPaginateTypeDef,
    ListThingRegistrationTasksResponseTypeDef,
    ListThingsInBillingGroupRequestListThingsInBillingGroupPaginateTypeDef,
    ListThingsInBillingGroupResponseTypeDef,
    ListThingsInThingGroupRequestListThingsInThingGroupPaginateTypeDef,
    ListThingsInThingGroupResponseTypeDef,
    ListThingsRequestListThingsPaginateTypeDef,
    ListThingsResponseTypeDef,
    ListThingTypesRequestListThingTypesPaginateTypeDef,
    ListThingTypesResponseTypeDef,
    ListTopicRuleDestinationsRequestListTopicRuleDestinationsPaginateTypeDef,
    ListTopicRuleDestinationsResponseTypeDef,
    ListTopicRulesRequestListTopicRulesPaginateTypeDef,
    ListTopicRulesResponseTypeDef,
    ListV2LoggingLevelsRequestListV2LoggingLevelsPaginateTypeDef,
    ListV2LoggingLevelsResponseTypeDef,
    ListViolationEventsRequestListViolationEventsPaginateTypeDef,
    ListViolationEventsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetBehaviorModelTrainingSummariesPaginator",
    "ListActiveViolationsPaginator",
    "ListAttachedPoliciesPaginator",
    "ListAuditFindingsPaginator",
    "ListAuditMitigationActionsExecutionsPaginator",
    "ListAuditMitigationActionsTasksPaginator",
    "ListAuditSuppressionsPaginator",
    "ListAuditTasksPaginator",
    "ListAuthorizersPaginator",
    "ListBillingGroupsPaginator",
    "ListCACertificatesPaginator",
    "ListCertificatesByCAPaginator",
    "ListCertificatesPaginator",
    "ListCustomMetricsPaginator",
    "ListDetectMitigationActionsExecutionsPaginator",
    "ListDetectMitigationActionsTasksPaginator",
    "ListDimensionsPaginator",
    "ListDomainConfigurationsPaginator",
    "ListFleetMetricsPaginator",
    "ListIndicesPaginator",
    "ListJobExecutionsForJobPaginator",
    "ListJobExecutionsForThingPaginator",
    "ListJobTemplatesPaginator",
    "ListJobsPaginator",
    "ListManagedJobTemplatesPaginator",
    "ListMetricValuesPaginator",
    "ListMitigationActionsPaginator",
    "ListOTAUpdatesPaginator",
    "ListOutgoingCertificatesPaginator",
    "ListPackageVersionsPaginator",
    "ListPackagesPaginator",
    "ListPoliciesPaginator",
    "ListPolicyPrincipalsPaginator",
    "ListPrincipalPoliciesPaginator",
    "ListPrincipalThingsPaginator",
    "ListProvisioningTemplateVersionsPaginator",
    "ListProvisioningTemplatesPaginator",
    "ListRelatedResourcesForAuditFindingPaginator",
    "ListRoleAliasesPaginator",
    "ListSbomValidationResultsPaginator",
    "ListScheduledAuditsPaginator",
    "ListSecurityProfilesForTargetPaginator",
    "ListSecurityProfilesPaginator",
    "ListStreamsPaginator",
    "ListTagsForResourcePaginator",
    "ListTargetsForPolicyPaginator",
    "ListTargetsForSecurityProfilePaginator",
    "ListThingGroupsForThingPaginator",
    "ListThingGroupsPaginator",
    "ListThingPrincipalsPaginator",
    "ListThingRegistrationTaskReportsPaginator",
    "ListThingRegistrationTasksPaginator",
    "ListThingTypesPaginator",
    "ListThingsInBillingGroupPaginator",
    "ListThingsInThingGroupPaginator",
    "ListThingsPaginator",
    "ListTopicRuleDestinationsPaginator",
    "ListTopicRulesPaginator",
    "ListV2LoggingLevelsPaginator",
    "ListViolationEventsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetBehaviorModelTrainingSummariesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/GetBehaviorModelTrainingSummaries.html#IoT.Paginator.GetBehaviorModelTrainingSummaries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#getbehaviormodeltrainingsummariespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetBehaviorModelTrainingSummariesRequestGetBehaviorModelTrainingSummariesPaginateTypeDef
        ],
    ) -> AsyncIterator[GetBehaviorModelTrainingSummariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/GetBehaviorModelTrainingSummaries.html#IoT.Paginator.GetBehaviorModelTrainingSummaries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#getbehaviormodeltrainingsummariespaginator)
        """

class ListActiveViolationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListActiveViolations.html#IoT.Paginator.ListActiveViolations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listactiveviolationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListActiveViolationsRequestListActiveViolationsPaginateTypeDef]
    ) -> AsyncIterator[ListActiveViolationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListActiveViolations.html#IoT.Paginator.ListActiveViolations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listactiveviolationspaginator)
        """

class ListAttachedPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAttachedPolicies.html#IoT.Paginator.ListAttachedPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listattachedpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAttachedPoliciesRequestListAttachedPoliciesPaginateTypeDef]
    ) -> AsyncIterator[ListAttachedPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAttachedPolicies.html#IoT.Paginator.ListAttachedPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listattachedpoliciespaginator)
        """

class ListAuditFindingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditFindings.html#IoT.Paginator.ListAuditFindings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauditfindingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAuditFindingsRequestListAuditFindingsPaginateTypeDef]
    ) -> AsyncIterator[ListAuditFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditFindings.html#IoT.Paginator.ListAuditFindings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauditfindingspaginator)
        """

class ListAuditMitigationActionsExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditMitigationActionsExecutions.html#IoT.Paginator.ListAuditMitigationActionsExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauditmitigationactionsexecutionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAuditMitigationActionsExecutionsRequestListAuditMitigationActionsExecutionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAuditMitigationActionsExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditMitigationActionsExecutions.html#IoT.Paginator.ListAuditMitigationActionsExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauditmitigationactionsexecutionspaginator)
        """

class ListAuditMitigationActionsTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditMitigationActionsTasks.html#IoT.Paginator.ListAuditMitigationActionsTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauditmitigationactionstaskspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAuditMitigationActionsTasksRequestListAuditMitigationActionsTasksPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAuditMitigationActionsTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditMitigationActionsTasks.html#IoT.Paginator.ListAuditMitigationActionsTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauditmitigationactionstaskspaginator)
        """

class ListAuditSuppressionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditSuppressions.html#IoT.Paginator.ListAuditSuppressions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauditsuppressionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAuditSuppressionsRequestListAuditSuppressionsPaginateTypeDef]
    ) -> AsyncIterator[ListAuditSuppressionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditSuppressions.html#IoT.Paginator.ListAuditSuppressions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauditsuppressionspaginator)
        """

class ListAuditTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditTasks.html#IoT.Paginator.ListAuditTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listaudittaskspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAuditTasksRequestListAuditTasksPaginateTypeDef]
    ) -> AsyncIterator[ListAuditTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditTasks.html#IoT.Paginator.ListAuditTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listaudittaskspaginator)
        """

class ListAuthorizersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuthorizers.html#IoT.Paginator.ListAuthorizers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauthorizerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAuthorizersRequestListAuthorizersPaginateTypeDef]
    ) -> AsyncIterator[ListAuthorizersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuthorizers.html#IoT.Paginator.ListAuthorizers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauthorizerspaginator)
        """

class ListBillingGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListBillingGroups.html#IoT.Paginator.ListBillingGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listbillinggroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBillingGroupsRequestListBillingGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListBillingGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListBillingGroups.html#IoT.Paginator.ListBillingGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listbillinggroupspaginator)
        """

class ListCACertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCACertificates.html#IoT.Paginator.ListCACertificates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcacertificatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCACertificatesRequestListCACertificatesPaginateTypeDef]
    ) -> AsyncIterator[ListCACertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCACertificates.html#IoT.Paginator.ListCACertificates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcacertificatespaginator)
        """

class ListCertificatesByCAPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCertificatesByCA.html#IoT.Paginator.ListCertificatesByCA)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcertificatesbycapaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCertificatesByCARequestListCertificatesByCAPaginateTypeDef]
    ) -> AsyncIterator[ListCertificatesByCAResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCertificatesByCA.html#IoT.Paginator.ListCertificatesByCA.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcertificatesbycapaginator)
        """

class ListCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCertificates.html#IoT.Paginator.ListCertificates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcertificatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCertificatesRequestListCertificatesPaginateTypeDef]
    ) -> AsyncIterator[ListCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCertificates.html#IoT.Paginator.ListCertificates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcertificatespaginator)
        """

class ListCustomMetricsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCustomMetrics.html#IoT.Paginator.ListCustomMetrics)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcustommetricspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCustomMetricsRequestListCustomMetricsPaginateTypeDef]
    ) -> AsyncIterator[ListCustomMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCustomMetrics.html#IoT.Paginator.ListCustomMetrics.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcustommetricspaginator)
        """

class ListDetectMitigationActionsExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDetectMitigationActionsExecutions.html#IoT.Paginator.ListDetectMitigationActionsExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listdetectmitigationactionsexecutionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListDetectMitigationActionsExecutionsRequestListDetectMitigationActionsExecutionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListDetectMitigationActionsExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDetectMitigationActionsExecutions.html#IoT.Paginator.ListDetectMitigationActionsExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listdetectmitigationactionsexecutionspaginator)
        """

class ListDetectMitigationActionsTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDetectMitigationActionsTasks.html#IoT.Paginator.ListDetectMitigationActionsTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listdetectmitigationactionstaskspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListDetectMitigationActionsTasksRequestListDetectMitigationActionsTasksPaginateTypeDef
        ],
    ) -> AsyncIterator[ListDetectMitigationActionsTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDetectMitigationActionsTasks.html#IoT.Paginator.ListDetectMitigationActionsTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listdetectmitigationactionstaskspaginator)
        """

class ListDimensionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDimensions.html#IoT.Paginator.ListDimensions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listdimensionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDimensionsRequestListDimensionsPaginateTypeDef]
    ) -> AsyncIterator[ListDimensionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDimensions.html#IoT.Paginator.ListDimensions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listdimensionspaginator)
        """

class ListDomainConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDomainConfigurations.html#IoT.Paginator.ListDomainConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listdomainconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListDomainConfigurationsRequestListDomainConfigurationsPaginateTypeDef],
    ) -> AsyncIterator[ListDomainConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDomainConfigurations.html#IoT.Paginator.ListDomainConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listdomainconfigurationspaginator)
        """

class ListFleetMetricsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListFleetMetrics.html#IoT.Paginator.ListFleetMetrics)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listfleetmetricspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFleetMetricsRequestListFleetMetricsPaginateTypeDef]
    ) -> AsyncIterator[ListFleetMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListFleetMetrics.html#IoT.Paginator.ListFleetMetrics.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listfleetmetricspaginator)
        """

class ListIndicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListIndices.html#IoT.Paginator.ListIndices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listindicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIndicesRequestListIndicesPaginateTypeDef]
    ) -> AsyncIterator[ListIndicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListIndices.html#IoT.Paginator.ListIndices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listindicespaginator)
        """

class ListJobExecutionsForJobPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobExecutionsForJob.html#IoT.Paginator.ListJobExecutionsForJob)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listjobexecutionsforjobpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobExecutionsForJobRequestListJobExecutionsForJobPaginateTypeDef]
    ) -> AsyncIterator[ListJobExecutionsForJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobExecutionsForJob.html#IoT.Paginator.ListJobExecutionsForJob.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listjobexecutionsforjobpaginator)
        """

class ListJobExecutionsForThingPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobExecutionsForThing.html#IoT.Paginator.ListJobExecutionsForThing)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listjobexecutionsforthingpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListJobExecutionsForThingRequestListJobExecutionsForThingPaginateTypeDef],
    ) -> AsyncIterator[ListJobExecutionsForThingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobExecutionsForThing.html#IoT.Paginator.ListJobExecutionsForThing.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listjobexecutionsforthingpaginator)
        """

class ListJobTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobTemplates.html#IoT.Paginator.ListJobTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listjobtemplatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobTemplatesRequestListJobTemplatesPaginateTypeDef]
    ) -> AsyncIterator[ListJobTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobTemplates.html#IoT.Paginator.ListJobTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listjobtemplatespaginator)
        """

class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobs.html#IoT.Paginator.ListJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> AsyncIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobs.html#IoT.Paginator.ListJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listjobspaginator)
        """

class ListManagedJobTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListManagedJobTemplates.html#IoT.Paginator.ListManagedJobTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listmanagedjobtemplatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListManagedJobTemplatesRequestListManagedJobTemplatesPaginateTypeDef]
    ) -> AsyncIterator[ListManagedJobTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListManagedJobTemplates.html#IoT.Paginator.ListManagedJobTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listmanagedjobtemplatespaginator)
        """

class ListMetricValuesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListMetricValues.html#IoT.Paginator.ListMetricValues)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listmetricvaluespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMetricValuesRequestListMetricValuesPaginateTypeDef]
    ) -> AsyncIterator[ListMetricValuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListMetricValues.html#IoT.Paginator.ListMetricValues.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listmetricvaluespaginator)
        """

class ListMitigationActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListMitigationActions.html#IoT.Paginator.ListMitigationActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listmitigationactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMitigationActionsRequestListMitigationActionsPaginateTypeDef]
    ) -> AsyncIterator[ListMitigationActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListMitigationActions.html#IoT.Paginator.ListMitigationActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listmitigationactionspaginator)
        """

class ListOTAUpdatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListOTAUpdates.html#IoT.Paginator.ListOTAUpdates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listotaupdatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListOTAUpdatesRequestListOTAUpdatesPaginateTypeDef]
    ) -> AsyncIterator[ListOTAUpdatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListOTAUpdates.html#IoT.Paginator.ListOTAUpdates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listotaupdatespaginator)
        """

class ListOutgoingCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListOutgoingCertificates.html#IoT.Paginator.ListOutgoingCertificates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listoutgoingcertificatespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListOutgoingCertificatesRequestListOutgoingCertificatesPaginateTypeDef],
    ) -> AsyncIterator[ListOutgoingCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListOutgoingCertificates.html#IoT.Paginator.ListOutgoingCertificates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listoutgoingcertificatespaginator)
        """

class ListPackageVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPackageVersions.html#IoT.Paginator.ListPackageVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listpackageversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPackageVersionsRequestListPackageVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListPackageVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPackageVersions.html#IoT.Paginator.ListPackageVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listpackageversionspaginator)
        """

class ListPackagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPackages.html#IoT.Paginator.ListPackages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listpackagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPackagesRequestListPackagesPaginateTypeDef]
    ) -> AsyncIterator[ListPackagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPackages.html#IoT.Paginator.ListPackages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listpackagespaginator)
        """

class ListPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPolicies.html#IoT.Paginator.ListPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPoliciesRequestListPoliciesPaginateTypeDef]
    ) -> AsyncIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPolicies.html#IoT.Paginator.ListPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listpoliciespaginator)
        """

class ListPolicyPrincipalsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPolicyPrincipals.html#IoT.Paginator.ListPolicyPrincipals)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listpolicyprincipalspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPolicyPrincipalsRequestListPolicyPrincipalsPaginateTypeDef]
    ) -> AsyncIterator[ListPolicyPrincipalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPolicyPrincipals.html#IoT.Paginator.ListPolicyPrincipals.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listpolicyprincipalspaginator)
        """

class ListPrincipalPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPrincipalPolicies.html#IoT.Paginator.ListPrincipalPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprincipalpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPrincipalPoliciesRequestListPrincipalPoliciesPaginateTypeDef]
    ) -> AsyncIterator[ListPrincipalPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPrincipalPolicies.html#IoT.Paginator.ListPrincipalPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprincipalpoliciespaginator)
        """

class ListPrincipalThingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPrincipalThings.html#IoT.Paginator.ListPrincipalThings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprincipalthingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPrincipalThingsRequestListPrincipalThingsPaginateTypeDef]
    ) -> AsyncIterator[ListPrincipalThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPrincipalThings.html#IoT.Paginator.ListPrincipalThings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprincipalthingspaginator)
        """

class ListProvisioningTemplateVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListProvisioningTemplateVersions.html#IoT.Paginator.ListProvisioningTemplateVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprovisioningtemplateversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListProvisioningTemplateVersionsRequestListProvisioningTemplateVersionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListProvisioningTemplateVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListProvisioningTemplateVersions.html#IoT.Paginator.ListProvisioningTemplateVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprovisioningtemplateversionspaginator)
        """

class ListProvisioningTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListProvisioningTemplates.html#IoT.Paginator.ListProvisioningTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprovisioningtemplatespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListProvisioningTemplatesRequestListProvisioningTemplatesPaginateTypeDef],
    ) -> AsyncIterator[ListProvisioningTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListProvisioningTemplates.html#IoT.Paginator.ListProvisioningTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprovisioningtemplatespaginator)
        """

class ListRelatedResourcesForAuditFindingPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListRelatedResourcesForAuditFinding.html#IoT.Paginator.ListRelatedResourcesForAuditFinding)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listrelatedresourcesforauditfindingpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListRelatedResourcesForAuditFindingRequestListRelatedResourcesForAuditFindingPaginateTypeDef
        ],
    ) -> AsyncIterator[ListRelatedResourcesForAuditFindingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListRelatedResourcesForAuditFinding.html#IoT.Paginator.ListRelatedResourcesForAuditFinding.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listrelatedresourcesforauditfindingpaginator)
        """

class ListRoleAliasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListRoleAliases.html#IoT.Paginator.ListRoleAliases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listrolealiasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRoleAliasesRequestListRoleAliasesPaginateTypeDef]
    ) -> AsyncIterator[ListRoleAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListRoleAliases.html#IoT.Paginator.ListRoleAliases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listrolealiasespaginator)
        """

class ListSbomValidationResultsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSbomValidationResults.html#IoT.Paginator.ListSbomValidationResults)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listsbomvalidationresultspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListSbomValidationResultsRequestListSbomValidationResultsPaginateTypeDef],
    ) -> AsyncIterator[ListSbomValidationResultsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSbomValidationResults.html#IoT.Paginator.ListSbomValidationResults.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listsbomvalidationresultspaginator)
        """

class ListScheduledAuditsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListScheduledAudits.html#IoT.Paginator.ListScheduledAudits)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listscheduledauditspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListScheduledAuditsRequestListScheduledAuditsPaginateTypeDef]
    ) -> AsyncIterator[ListScheduledAuditsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListScheduledAudits.html#IoT.Paginator.ListScheduledAudits.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listscheduledauditspaginator)
        """

class ListSecurityProfilesForTargetPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSecurityProfilesForTarget.html#IoT.Paginator.ListSecurityProfilesForTarget)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listsecurityprofilesfortargetpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListSecurityProfilesForTargetRequestListSecurityProfilesForTargetPaginateTypeDef
        ],
    ) -> AsyncIterator[ListSecurityProfilesForTargetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSecurityProfilesForTarget.html#IoT.Paginator.ListSecurityProfilesForTarget.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listsecurityprofilesfortargetpaginator)
        """

class ListSecurityProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSecurityProfiles.html#IoT.Paginator.ListSecurityProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listsecurityprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListSecurityProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSecurityProfiles.html#IoT.Paginator.ListSecurityProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listsecurityprofilespaginator)
        """

class ListStreamsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListStreams.html#IoT.Paginator.ListStreams)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#liststreamspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStreamsRequestListStreamsPaginateTypeDef]
    ) -> AsyncIterator[ListStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListStreams.html#IoT.Paginator.ListStreams.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#liststreamspaginator)
        """

class ListTagsForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTagsForResource.html#IoT.Paginator.ListTagsForResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtagsforresourcepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsForResourceRequestListTagsForResourcePaginateTypeDef]
    ) -> AsyncIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTagsForResource.html#IoT.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtagsforresourcepaginator)
        """

class ListTargetsForPolicyPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTargetsForPolicy.html#IoT.Paginator.ListTargetsForPolicy)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtargetsforpolicypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTargetsForPolicyRequestListTargetsForPolicyPaginateTypeDef]
    ) -> AsyncIterator[ListTargetsForPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTargetsForPolicy.html#IoT.Paginator.ListTargetsForPolicy.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtargetsforpolicypaginator)
        """

class ListTargetsForSecurityProfilePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTargetsForSecurityProfile.html#IoT.Paginator.ListTargetsForSecurityProfile)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtargetsforsecurityprofilepaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListTargetsForSecurityProfileRequestListTargetsForSecurityProfilePaginateTypeDef
        ],
    ) -> AsyncIterator[ListTargetsForSecurityProfileResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTargetsForSecurityProfile.html#IoT.Paginator.ListTargetsForSecurityProfile.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtargetsforsecurityprofilepaginator)
        """

class ListThingGroupsForThingPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingGroupsForThing.html#IoT.Paginator.ListThingGroupsForThing)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthinggroupsforthingpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListThingGroupsForThingRequestListThingGroupsForThingPaginateTypeDef]
    ) -> AsyncIterator[ListThingGroupsForThingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingGroupsForThing.html#IoT.Paginator.ListThingGroupsForThing.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthinggroupsforthingpaginator)
        """

class ListThingGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingGroups.html#IoT.Paginator.ListThingGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthinggroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListThingGroupsRequestListThingGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListThingGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingGroups.html#IoT.Paginator.ListThingGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthinggroupspaginator)
        """

class ListThingPrincipalsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingPrincipals.html#IoT.Paginator.ListThingPrincipals)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingprincipalspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListThingPrincipalsRequestListThingPrincipalsPaginateTypeDef]
    ) -> AsyncIterator[ListThingPrincipalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingPrincipals.html#IoT.Paginator.ListThingPrincipals.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingprincipalspaginator)
        """

class ListThingRegistrationTaskReportsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingRegistrationTaskReports.html#IoT.Paginator.ListThingRegistrationTaskReports)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingregistrationtaskreportspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListThingRegistrationTaskReportsRequestListThingRegistrationTaskReportsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListThingRegistrationTaskReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingRegistrationTaskReports.html#IoT.Paginator.ListThingRegistrationTaskReports.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingregistrationtaskreportspaginator)
        """

class ListThingRegistrationTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingRegistrationTasks.html#IoT.Paginator.ListThingRegistrationTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingregistrationtaskspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListThingRegistrationTasksRequestListThingRegistrationTasksPaginateTypeDef
        ],
    ) -> AsyncIterator[ListThingRegistrationTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingRegistrationTasks.html#IoT.Paginator.ListThingRegistrationTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingregistrationtaskspaginator)
        """

class ListThingTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingTypes.html#IoT.Paginator.ListThingTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingtypespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListThingTypesRequestListThingTypesPaginateTypeDef]
    ) -> AsyncIterator[ListThingTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingTypes.html#IoT.Paginator.ListThingTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingtypespaginator)
        """

class ListThingsInBillingGroupPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingsInBillingGroup.html#IoT.Paginator.ListThingsInBillingGroup)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingsinbillinggrouppaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListThingsInBillingGroupRequestListThingsInBillingGroupPaginateTypeDef],
    ) -> AsyncIterator[ListThingsInBillingGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingsInBillingGroup.html#IoT.Paginator.ListThingsInBillingGroup.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingsinbillinggrouppaginator)
        """

class ListThingsInThingGroupPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingsInThingGroup.html#IoT.Paginator.ListThingsInThingGroup)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingsinthinggrouppaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListThingsInThingGroupRequestListThingsInThingGroupPaginateTypeDef]
    ) -> AsyncIterator[ListThingsInThingGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingsInThingGroup.html#IoT.Paginator.ListThingsInThingGroup.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingsinthinggrouppaginator)
        """

class ListThingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThings.html#IoT.Paginator.ListThings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListThingsRequestListThingsPaginateTypeDef]
    ) -> AsyncIterator[ListThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThings.html#IoT.Paginator.ListThings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingspaginator)
        """

class ListTopicRuleDestinationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTopicRuleDestinations.html#IoT.Paginator.ListTopicRuleDestinations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtopicruledestinationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListTopicRuleDestinationsRequestListTopicRuleDestinationsPaginateTypeDef],
    ) -> AsyncIterator[ListTopicRuleDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTopicRuleDestinations.html#IoT.Paginator.ListTopicRuleDestinations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtopicruledestinationspaginator)
        """

class ListTopicRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTopicRules.html#IoT.Paginator.ListTopicRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtopicrulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTopicRulesRequestListTopicRulesPaginateTypeDef]
    ) -> AsyncIterator[ListTopicRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTopicRules.html#IoT.Paginator.ListTopicRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtopicrulespaginator)
        """

class ListV2LoggingLevelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListV2LoggingLevels.html#IoT.Paginator.ListV2LoggingLevels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listv2logginglevelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListV2LoggingLevelsRequestListV2LoggingLevelsPaginateTypeDef]
    ) -> AsyncIterator[ListV2LoggingLevelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListV2LoggingLevels.html#IoT.Paginator.ListV2LoggingLevels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listv2logginglevelspaginator)
        """

class ListViolationEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListViolationEvents.html#IoT.Paginator.ListViolationEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listviolationeventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListViolationEventsRequestListViolationEventsPaginateTypeDef]
    ) -> AsyncIterator[ListViolationEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListViolationEvents.html#IoT.Paginator.ListViolationEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listviolationeventspaginator)
        """
