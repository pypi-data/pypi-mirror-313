"""
Type annotations for connect service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_connect.client import ConnectClient
    from types_aiobotocore_connect.paginator import (
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
        ListEvaluationFormVersionsPaginator,
        ListEvaluationFormsPaginator,
        ListFlowAssociationsPaginator,
        ListHoursOfOperationsPaginator,
        ListInstanceAttributesPaginator,
        ListInstanceStorageConfigsPaginator,
        ListInstancesPaginator,
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
        ListTrafficDistributionGroupUsersPaginator,
        ListTrafficDistributionGroupsPaginator,
        ListUseCasesPaginator,
        ListUserHierarchyGroupsPaginator,
        ListUserProficienciesPaginator,
        ListUsersPaginator,
        ListViewVersionsPaginator,
        ListViewsPaginator,
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

    session = get_session()
    with session.create_client("connect") as client:
        client: ConnectClient

        get_metric_data_paginator: GetMetricDataPaginator = client.get_paginator("get_metric_data")
        list_agent_statuses_paginator: ListAgentStatusesPaginator = client.get_paginator("list_agent_statuses")
        list_approved_origins_paginator: ListApprovedOriginsPaginator = client.get_paginator("list_approved_origins")
        list_authentication_profiles_paginator: ListAuthenticationProfilesPaginator = client.get_paginator("list_authentication_profiles")
        list_bots_paginator: ListBotsPaginator = client.get_paginator("list_bots")
        list_contact_evaluations_paginator: ListContactEvaluationsPaginator = client.get_paginator("list_contact_evaluations")
        list_contact_flow_modules_paginator: ListContactFlowModulesPaginator = client.get_paginator("list_contact_flow_modules")
        list_contact_flows_paginator: ListContactFlowsPaginator = client.get_paginator("list_contact_flows")
        list_contact_references_paginator: ListContactReferencesPaginator = client.get_paginator("list_contact_references")
        list_default_vocabularies_paginator: ListDefaultVocabulariesPaginator = client.get_paginator("list_default_vocabularies")
        list_evaluation_form_versions_paginator: ListEvaluationFormVersionsPaginator = client.get_paginator("list_evaluation_form_versions")
        list_evaluation_forms_paginator: ListEvaluationFormsPaginator = client.get_paginator("list_evaluation_forms")
        list_flow_associations_paginator: ListFlowAssociationsPaginator = client.get_paginator("list_flow_associations")
        list_hours_of_operations_paginator: ListHoursOfOperationsPaginator = client.get_paginator("list_hours_of_operations")
        list_instance_attributes_paginator: ListInstanceAttributesPaginator = client.get_paginator("list_instance_attributes")
        list_instance_storage_configs_paginator: ListInstanceStorageConfigsPaginator = client.get_paginator("list_instance_storage_configs")
        list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
        list_integration_associations_paginator: ListIntegrationAssociationsPaginator = client.get_paginator("list_integration_associations")
        list_lambda_functions_paginator: ListLambdaFunctionsPaginator = client.get_paginator("list_lambda_functions")
        list_lex_bots_paginator: ListLexBotsPaginator = client.get_paginator("list_lex_bots")
        list_phone_numbers_paginator: ListPhoneNumbersPaginator = client.get_paginator("list_phone_numbers")
        list_phone_numbers_v2_paginator: ListPhoneNumbersV2Paginator = client.get_paginator("list_phone_numbers_v2")
        list_predefined_attributes_paginator: ListPredefinedAttributesPaginator = client.get_paginator("list_predefined_attributes")
        list_prompts_paginator: ListPromptsPaginator = client.get_paginator("list_prompts")
        list_queue_quick_connects_paginator: ListQueueQuickConnectsPaginator = client.get_paginator("list_queue_quick_connects")
        list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
        list_quick_connects_paginator: ListQuickConnectsPaginator = client.get_paginator("list_quick_connects")
        list_routing_profile_queues_paginator: ListRoutingProfileQueuesPaginator = client.get_paginator("list_routing_profile_queues")
        list_routing_profiles_paginator: ListRoutingProfilesPaginator = client.get_paginator("list_routing_profiles")
        list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
        list_security_keys_paginator: ListSecurityKeysPaginator = client.get_paginator("list_security_keys")
        list_security_profile_applications_paginator: ListSecurityProfileApplicationsPaginator = client.get_paginator("list_security_profile_applications")
        list_security_profile_permissions_paginator: ListSecurityProfilePermissionsPaginator = client.get_paginator("list_security_profile_permissions")
        list_security_profiles_paginator: ListSecurityProfilesPaginator = client.get_paginator("list_security_profiles")
        list_task_templates_paginator: ListTaskTemplatesPaginator = client.get_paginator("list_task_templates")
        list_traffic_distribution_group_users_paginator: ListTrafficDistributionGroupUsersPaginator = client.get_paginator("list_traffic_distribution_group_users")
        list_traffic_distribution_groups_paginator: ListTrafficDistributionGroupsPaginator = client.get_paginator("list_traffic_distribution_groups")
        list_use_cases_paginator: ListUseCasesPaginator = client.get_paginator("list_use_cases")
        list_user_hierarchy_groups_paginator: ListUserHierarchyGroupsPaginator = client.get_paginator("list_user_hierarchy_groups")
        list_user_proficiencies_paginator: ListUserProficienciesPaginator = client.get_paginator("list_user_proficiencies")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
        list_view_versions_paginator: ListViewVersionsPaginator = client.get_paginator("list_view_versions")
        list_views_paginator: ListViewsPaginator = client.get_paginator("list_views")
        search_agent_statuses_paginator: SearchAgentStatusesPaginator = client.get_paginator("search_agent_statuses")
        search_available_phone_numbers_paginator: SearchAvailablePhoneNumbersPaginator = client.get_paginator("search_available_phone_numbers")
        search_contact_flow_modules_paginator: SearchContactFlowModulesPaginator = client.get_paginator("search_contact_flow_modules")
        search_contact_flows_paginator: SearchContactFlowsPaginator = client.get_paginator("search_contact_flows")
        search_contacts_paginator: SearchContactsPaginator = client.get_paginator("search_contacts")
        search_hours_of_operations_paginator: SearchHoursOfOperationsPaginator = client.get_paginator("search_hours_of_operations")
        search_predefined_attributes_paginator: SearchPredefinedAttributesPaginator = client.get_paginator("search_predefined_attributes")
        search_prompts_paginator: SearchPromptsPaginator = client.get_paginator("search_prompts")
        search_queues_paginator: SearchQueuesPaginator = client.get_paginator("search_queues")
        search_quick_connects_paginator: SearchQuickConnectsPaginator = client.get_paginator("search_quick_connects")
        search_resource_tags_paginator: SearchResourceTagsPaginator = client.get_paginator("search_resource_tags")
        search_routing_profiles_paginator: SearchRoutingProfilesPaginator = client.get_paginator("search_routing_profiles")
        search_security_profiles_paginator: SearchSecurityProfilesPaginator = client.get_paginator("search_security_profiles")
        search_user_hierarchy_groups_paginator: SearchUserHierarchyGroupsPaginator = client.get_paginator("search_user_hierarchy_groups")
        search_users_paginator: SearchUsersPaginator = client.get_paginator("search_users")
        search_vocabularies_paginator: SearchVocabulariesPaginator = client.get_paginator("search_vocabularies")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetMetricDataRequestGetMetricDataPaginateTypeDef,
    GetMetricDataResponseTypeDef,
    ListAgentStatusRequestListAgentStatusesPaginateTypeDef,
    ListAgentStatusResponseTypeDef,
    ListApprovedOriginsRequestListApprovedOriginsPaginateTypeDef,
    ListApprovedOriginsResponseTypeDef,
    ListAuthenticationProfilesRequestListAuthenticationProfilesPaginateTypeDef,
    ListAuthenticationProfilesResponseTypeDef,
    ListBotsRequestListBotsPaginateTypeDef,
    ListBotsResponseTypeDef,
    ListContactEvaluationsRequestListContactEvaluationsPaginateTypeDef,
    ListContactEvaluationsResponseTypeDef,
    ListContactFlowModulesRequestListContactFlowModulesPaginateTypeDef,
    ListContactFlowModulesResponseTypeDef,
    ListContactFlowsRequestListContactFlowsPaginateTypeDef,
    ListContactFlowsResponseTypeDef,
    ListContactReferencesRequestListContactReferencesPaginateTypeDef,
    ListContactReferencesResponseTypeDef,
    ListDefaultVocabulariesRequestListDefaultVocabulariesPaginateTypeDef,
    ListDefaultVocabulariesResponseTypeDef,
    ListEvaluationFormsRequestListEvaluationFormsPaginateTypeDef,
    ListEvaluationFormsResponseTypeDef,
    ListEvaluationFormVersionsRequestListEvaluationFormVersionsPaginateTypeDef,
    ListEvaluationFormVersionsResponseTypeDef,
    ListFlowAssociationsRequestListFlowAssociationsPaginateTypeDef,
    ListFlowAssociationsResponseTypeDef,
    ListHoursOfOperationsRequestListHoursOfOperationsPaginateTypeDef,
    ListHoursOfOperationsResponseTypeDef,
    ListInstanceAttributesRequestListInstanceAttributesPaginateTypeDef,
    ListInstanceAttributesResponseTypeDef,
    ListInstancesRequestListInstancesPaginateTypeDef,
    ListInstancesResponseTypeDef,
    ListInstanceStorageConfigsRequestListInstanceStorageConfigsPaginateTypeDef,
    ListInstanceStorageConfigsResponseTypeDef,
    ListIntegrationAssociationsRequestListIntegrationAssociationsPaginateTypeDef,
    ListIntegrationAssociationsResponseTypeDef,
    ListLambdaFunctionsRequestListLambdaFunctionsPaginateTypeDef,
    ListLambdaFunctionsResponseTypeDef,
    ListLexBotsRequestListLexBotsPaginateTypeDef,
    ListLexBotsResponseTypeDef,
    ListPhoneNumbersRequestListPhoneNumbersPaginateTypeDef,
    ListPhoneNumbersResponseTypeDef,
    ListPhoneNumbersV2RequestListPhoneNumbersV2PaginateTypeDef,
    ListPhoneNumbersV2ResponseTypeDef,
    ListPredefinedAttributesRequestListPredefinedAttributesPaginateTypeDef,
    ListPredefinedAttributesResponseTypeDef,
    ListPromptsRequestListPromptsPaginateTypeDef,
    ListPromptsResponseTypeDef,
    ListQueueQuickConnectsRequestListQueueQuickConnectsPaginateTypeDef,
    ListQueueQuickConnectsResponseTypeDef,
    ListQueuesRequestListQueuesPaginateTypeDef,
    ListQueuesResponseTypeDef,
    ListQuickConnectsRequestListQuickConnectsPaginateTypeDef,
    ListQuickConnectsResponseTypeDef,
    ListRoutingProfileQueuesRequestListRoutingProfileQueuesPaginateTypeDef,
    ListRoutingProfileQueuesResponseTypeDef,
    ListRoutingProfilesRequestListRoutingProfilesPaginateTypeDef,
    ListRoutingProfilesResponseTypeDef,
    ListRulesRequestListRulesPaginateTypeDef,
    ListRulesResponseTypeDef,
    ListSecurityKeysRequestListSecurityKeysPaginateTypeDef,
    ListSecurityKeysResponseTypeDef,
    ListSecurityProfileApplicationsRequestListSecurityProfileApplicationsPaginateTypeDef,
    ListSecurityProfileApplicationsResponseTypeDef,
    ListSecurityProfilePermissionsRequestListSecurityProfilePermissionsPaginateTypeDef,
    ListSecurityProfilePermissionsResponseTypeDef,
    ListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef,
    ListSecurityProfilesResponseTypeDef,
    ListTaskTemplatesRequestListTaskTemplatesPaginateTypeDef,
    ListTaskTemplatesResponseTypeDef,
    ListTrafficDistributionGroupsRequestListTrafficDistributionGroupsPaginateTypeDef,
    ListTrafficDistributionGroupsResponseTypeDef,
    ListTrafficDistributionGroupUsersRequestListTrafficDistributionGroupUsersPaginateTypeDef,
    ListTrafficDistributionGroupUsersResponseTypeDef,
    ListUseCasesRequestListUseCasesPaginateTypeDef,
    ListUseCasesResponseTypeDef,
    ListUserHierarchyGroupsRequestListUserHierarchyGroupsPaginateTypeDef,
    ListUserHierarchyGroupsResponseTypeDef,
    ListUserProficienciesRequestListUserProficienciesPaginateTypeDef,
    ListUserProficienciesResponseTypeDef,
    ListUsersRequestListUsersPaginateTypeDef,
    ListUsersResponseTypeDef,
    ListViewsRequestListViewsPaginateTypeDef,
    ListViewsResponseTypeDef,
    ListViewVersionsRequestListViewVersionsPaginateTypeDef,
    ListViewVersionsResponseTypeDef,
    SearchAgentStatusesRequestSearchAgentStatusesPaginateTypeDef,
    SearchAgentStatusesResponseTypeDef,
    SearchAvailablePhoneNumbersRequestSearchAvailablePhoneNumbersPaginateTypeDef,
    SearchAvailablePhoneNumbersResponseTypeDef,
    SearchContactFlowModulesRequestSearchContactFlowModulesPaginateTypeDef,
    SearchContactFlowModulesResponseTypeDef,
    SearchContactFlowsRequestSearchContactFlowsPaginateTypeDef,
    SearchContactFlowsResponseTypeDef,
    SearchContactsRequestSearchContactsPaginateTypeDef,
    SearchContactsResponseTypeDef,
    SearchHoursOfOperationsRequestSearchHoursOfOperationsPaginateTypeDef,
    SearchHoursOfOperationsResponseTypeDef,
    SearchPredefinedAttributesRequestSearchPredefinedAttributesPaginateTypeDef,
    SearchPredefinedAttributesResponseTypeDef,
    SearchPromptsRequestSearchPromptsPaginateTypeDef,
    SearchPromptsResponseTypeDef,
    SearchQueuesRequestSearchQueuesPaginateTypeDef,
    SearchQueuesResponseTypeDef,
    SearchQuickConnectsRequestSearchQuickConnectsPaginateTypeDef,
    SearchQuickConnectsResponseTypeDef,
    SearchResourceTagsRequestSearchResourceTagsPaginateTypeDef,
    SearchResourceTagsResponseTypeDef,
    SearchRoutingProfilesRequestSearchRoutingProfilesPaginateTypeDef,
    SearchRoutingProfilesResponseTypeDef,
    SearchSecurityProfilesRequestSearchSecurityProfilesPaginateTypeDef,
    SearchSecurityProfilesResponseTypeDef,
    SearchUserHierarchyGroupsRequestSearchUserHierarchyGroupsPaginateTypeDef,
    SearchUserHierarchyGroupsResponseTypeDef,
    SearchUsersRequestSearchUsersPaginateTypeDef,
    SearchUsersResponseTypeDef,
    SearchVocabulariesRequestSearchVocabulariesPaginateTypeDef,
    SearchVocabulariesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetMetricDataPaginator",
    "ListAgentStatusesPaginator",
    "ListApprovedOriginsPaginator",
    "ListAuthenticationProfilesPaginator",
    "ListBotsPaginator",
    "ListContactEvaluationsPaginator",
    "ListContactFlowModulesPaginator",
    "ListContactFlowsPaginator",
    "ListContactReferencesPaginator",
    "ListDefaultVocabulariesPaginator",
    "ListEvaluationFormVersionsPaginator",
    "ListEvaluationFormsPaginator",
    "ListFlowAssociationsPaginator",
    "ListHoursOfOperationsPaginator",
    "ListInstanceAttributesPaginator",
    "ListInstanceStorageConfigsPaginator",
    "ListInstancesPaginator",
    "ListIntegrationAssociationsPaginator",
    "ListLambdaFunctionsPaginator",
    "ListLexBotsPaginator",
    "ListPhoneNumbersPaginator",
    "ListPhoneNumbersV2Paginator",
    "ListPredefinedAttributesPaginator",
    "ListPromptsPaginator",
    "ListQueueQuickConnectsPaginator",
    "ListQueuesPaginator",
    "ListQuickConnectsPaginator",
    "ListRoutingProfileQueuesPaginator",
    "ListRoutingProfilesPaginator",
    "ListRulesPaginator",
    "ListSecurityKeysPaginator",
    "ListSecurityProfileApplicationsPaginator",
    "ListSecurityProfilePermissionsPaginator",
    "ListSecurityProfilesPaginator",
    "ListTaskTemplatesPaginator",
    "ListTrafficDistributionGroupUsersPaginator",
    "ListTrafficDistributionGroupsPaginator",
    "ListUseCasesPaginator",
    "ListUserHierarchyGroupsPaginator",
    "ListUserProficienciesPaginator",
    "ListUsersPaginator",
    "ListViewVersionsPaginator",
    "ListViewsPaginator",
    "SearchAgentStatusesPaginator",
    "SearchAvailablePhoneNumbersPaginator",
    "SearchContactFlowModulesPaginator",
    "SearchContactFlowsPaginator",
    "SearchContactsPaginator",
    "SearchHoursOfOperationsPaginator",
    "SearchPredefinedAttributesPaginator",
    "SearchPromptsPaginator",
    "SearchQueuesPaginator",
    "SearchQuickConnectsPaginator",
    "SearchResourceTagsPaginator",
    "SearchRoutingProfilesPaginator",
    "SearchSecurityProfilesPaginator",
    "SearchUserHierarchyGroupsPaginator",
    "SearchUsersPaginator",
    "SearchVocabulariesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetMetricDataPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/GetMetricData.html#Connect.Paginator.GetMetricData)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#getmetricdatapaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetMetricDataRequestGetMetricDataPaginateTypeDef]
    ) -> AsyncIterator[GetMetricDataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/GetMetricData.html#Connect.Paginator.GetMetricData.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#getmetricdatapaginator)
        """

class ListAgentStatusesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListAgentStatuses.html#Connect.Paginator.ListAgentStatuses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listagentstatusespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAgentStatusRequestListAgentStatusesPaginateTypeDef]
    ) -> AsyncIterator[ListAgentStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListAgentStatuses.html#Connect.Paginator.ListAgentStatuses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listagentstatusespaginator)
        """

class ListApprovedOriginsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListApprovedOrigins.html#Connect.Paginator.ListApprovedOrigins)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listapprovedoriginspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListApprovedOriginsRequestListApprovedOriginsPaginateTypeDef]
    ) -> AsyncIterator[ListApprovedOriginsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListApprovedOrigins.html#Connect.Paginator.ListApprovedOrigins.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listapprovedoriginspaginator)
        """

class ListAuthenticationProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListAuthenticationProfiles.html#Connect.Paginator.ListAuthenticationProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listauthenticationprofilespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAuthenticationProfilesRequestListAuthenticationProfilesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListAuthenticationProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListAuthenticationProfiles.html#Connect.Paginator.ListAuthenticationProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listauthenticationprofilespaginator)
        """

class ListBotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListBots.html#Connect.Paginator.ListBots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listbotspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBotsRequestListBotsPaginateTypeDef]
    ) -> AsyncIterator[ListBotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListBots.html#Connect.Paginator.ListBots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listbotspaginator)
        """

class ListContactEvaluationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactEvaluations.html#Connect.Paginator.ListContactEvaluations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactevaluationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListContactEvaluationsRequestListContactEvaluationsPaginateTypeDef]
    ) -> AsyncIterator[ListContactEvaluationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactEvaluations.html#Connect.Paginator.ListContactEvaluations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactevaluationspaginator)
        """

class ListContactFlowModulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactFlowModules.html#Connect.Paginator.ListContactFlowModules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactflowmodulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListContactFlowModulesRequestListContactFlowModulesPaginateTypeDef]
    ) -> AsyncIterator[ListContactFlowModulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactFlowModules.html#Connect.Paginator.ListContactFlowModules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactflowmodulespaginator)
        """

class ListContactFlowsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactFlows.html#Connect.Paginator.ListContactFlows)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactflowspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListContactFlowsRequestListContactFlowsPaginateTypeDef]
    ) -> AsyncIterator[ListContactFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactFlows.html#Connect.Paginator.ListContactFlows.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactflowspaginator)
        """

class ListContactReferencesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactReferences.html#Connect.Paginator.ListContactReferences)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactreferencespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListContactReferencesRequestListContactReferencesPaginateTypeDef]
    ) -> AsyncIterator[ListContactReferencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactReferences.html#Connect.Paginator.ListContactReferences.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactreferencespaginator)
        """

class ListDefaultVocabulariesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListDefaultVocabularies.html#Connect.Paginator.ListDefaultVocabularies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listdefaultvocabulariespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDefaultVocabulariesRequestListDefaultVocabulariesPaginateTypeDef]
    ) -> AsyncIterator[ListDefaultVocabulariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListDefaultVocabularies.html#Connect.Paginator.ListDefaultVocabularies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listdefaultvocabulariespaginator)
        """

class ListEvaluationFormVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListEvaluationFormVersions.html#Connect.Paginator.ListEvaluationFormVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listevaluationformversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListEvaluationFormVersionsRequestListEvaluationFormVersionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListEvaluationFormVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListEvaluationFormVersions.html#Connect.Paginator.ListEvaluationFormVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listevaluationformversionspaginator)
        """

class ListEvaluationFormsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListEvaluationForms.html#Connect.Paginator.ListEvaluationForms)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listevaluationformspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEvaluationFormsRequestListEvaluationFormsPaginateTypeDef]
    ) -> AsyncIterator[ListEvaluationFormsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListEvaluationForms.html#Connect.Paginator.ListEvaluationForms.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listevaluationformspaginator)
        """

class ListFlowAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListFlowAssociations.html#Connect.Paginator.ListFlowAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listflowassociationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFlowAssociationsRequestListFlowAssociationsPaginateTypeDef]
    ) -> AsyncIterator[ListFlowAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListFlowAssociations.html#Connect.Paginator.ListFlowAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listflowassociationspaginator)
        """

class ListHoursOfOperationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListHoursOfOperations.html#Connect.Paginator.ListHoursOfOperations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listhoursofoperationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListHoursOfOperationsRequestListHoursOfOperationsPaginateTypeDef]
    ) -> AsyncIterator[ListHoursOfOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListHoursOfOperations.html#Connect.Paginator.ListHoursOfOperations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listhoursofoperationspaginator)
        """

class ListInstanceAttributesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstanceAttributes.html#Connect.Paginator.ListInstanceAttributes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listinstanceattributespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInstanceAttributesRequestListInstanceAttributesPaginateTypeDef]
    ) -> AsyncIterator[ListInstanceAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstanceAttributes.html#Connect.Paginator.ListInstanceAttributes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listinstanceattributespaginator)
        """

class ListInstanceStorageConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstanceStorageConfigs.html#Connect.Paginator.ListInstanceStorageConfigs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listinstancestorageconfigspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListInstanceStorageConfigsRequestListInstanceStorageConfigsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListInstanceStorageConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstanceStorageConfigs.html#Connect.Paginator.ListInstanceStorageConfigs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listinstancestorageconfigspaginator)
        """

class ListInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstances.html#Connect.Paginator.ListInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listinstancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInstancesRequestListInstancesPaginateTypeDef]
    ) -> AsyncIterator[ListInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstances.html#Connect.Paginator.ListInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listinstancespaginator)
        """

class ListIntegrationAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListIntegrationAssociations.html#Connect.Paginator.ListIntegrationAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listintegrationassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListIntegrationAssociationsRequestListIntegrationAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListIntegrationAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListIntegrationAssociations.html#Connect.Paginator.ListIntegrationAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listintegrationassociationspaginator)
        """

class ListLambdaFunctionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListLambdaFunctions.html#Connect.Paginator.ListLambdaFunctions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listlambdafunctionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLambdaFunctionsRequestListLambdaFunctionsPaginateTypeDef]
    ) -> AsyncIterator[ListLambdaFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListLambdaFunctions.html#Connect.Paginator.ListLambdaFunctions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listlambdafunctionspaginator)
        """

class ListLexBotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListLexBots.html#Connect.Paginator.ListLexBots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listlexbotspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLexBotsRequestListLexBotsPaginateTypeDef]
    ) -> AsyncIterator[ListLexBotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListLexBots.html#Connect.Paginator.ListLexBots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listlexbotspaginator)
        """

class ListPhoneNumbersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPhoneNumbers.html#Connect.Paginator.ListPhoneNumbers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listphonenumberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPhoneNumbersRequestListPhoneNumbersPaginateTypeDef]
    ) -> AsyncIterator[ListPhoneNumbersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPhoneNumbers.html#Connect.Paginator.ListPhoneNumbers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listphonenumberspaginator)
        """

class ListPhoneNumbersV2Paginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPhoneNumbersV2.html#Connect.Paginator.ListPhoneNumbersV2)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listphonenumbersv2paginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPhoneNumbersV2RequestListPhoneNumbersV2PaginateTypeDef]
    ) -> AsyncIterator[ListPhoneNumbersV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPhoneNumbersV2.html#Connect.Paginator.ListPhoneNumbersV2.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listphonenumbersv2paginator)
        """

class ListPredefinedAttributesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPredefinedAttributes.html#Connect.Paginator.ListPredefinedAttributes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listpredefinedattributespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListPredefinedAttributesRequestListPredefinedAttributesPaginateTypeDef],
    ) -> AsyncIterator[ListPredefinedAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPredefinedAttributes.html#Connect.Paginator.ListPredefinedAttributes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listpredefinedattributespaginator)
        """

class ListPromptsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPrompts.html#Connect.Paginator.ListPrompts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listpromptspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPromptsRequestListPromptsPaginateTypeDef]
    ) -> AsyncIterator[ListPromptsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPrompts.html#Connect.Paginator.ListPrompts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listpromptspaginator)
        """

class ListQueueQuickConnectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQueueQuickConnects.html#Connect.Paginator.ListQueueQuickConnects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listqueuequickconnectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListQueueQuickConnectsRequestListQueueQuickConnectsPaginateTypeDef]
    ) -> AsyncIterator[ListQueueQuickConnectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQueueQuickConnects.html#Connect.Paginator.ListQueueQuickConnects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listqueuequickconnectspaginator)
        """

class ListQueuesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQueues.html#Connect.Paginator.ListQueues)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listqueuespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListQueuesRequestListQueuesPaginateTypeDef]
    ) -> AsyncIterator[ListQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQueues.html#Connect.Paginator.ListQueues.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listqueuespaginator)
        """

class ListQuickConnectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQuickConnects.html#Connect.Paginator.ListQuickConnects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listquickconnectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListQuickConnectsRequestListQuickConnectsPaginateTypeDef]
    ) -> AsyncIterator[ListQuickConnectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQuickConnects.html#Connect.Paginator.ListQuickConnects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listquickconnectspaginator)
        """

class ListRoutingProfileQueuesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRoutingProfileQueues.html#Connect.Paginator.ListRoutingProfileQueues)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listroutingprofilequeuespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListRoutingProfileQueuesRequestListRoutingProfileQueuesPaginateTypeDef],
    ) -> AsyncIterator[ListRoutingProfileQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRoutingProfileQueues.html#Connect.Paginator.ListRoutingProfileQueues.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listroutingprofilequeuespaginator)
        """

class ListRoutingProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRoutingProfiles.html#Connect.Paginator.ListRoutingProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listroutingprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRoutingProfilesRequestListRoutingProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListRoutingProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRoutingProfiles.html#Connect.Paginator.ListRoutingProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listroutingprofilespaginator)
        """

class ListRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRules.html#Connect.Paginator.ListRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listrulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRulesRequestListRulesPaginateTypeDef]
    ) -> AsyncIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRules.html#Connect.Paginator.ListRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listrulespaginator)
        """

class ListSecurityKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityKeys.html#Connect.Paginator.ListSecurityKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listsecuritykeyspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSecurityKeysRequestListSecurityKeysPaginateTypeDef]
    ) -> AsyncIterator[ListSecurityKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityKeys.html#Connect.Paginator.ListSecurityKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listsecuritykeyspaginator)
        """

class ListSecurityProfileApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfileApplications.html#Connect.Paginator.ListSecurityProfileApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listsecurityprofileapplicationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListSecurityProfileApplicationsRequestListSecurityProfileApplicationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListSecurityProfileApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfileApplications.html#Connect.Paginator.ListSecurityProfileApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listsecurityprofileapplicationspaginator)
        """

class ListSecurityProfilePermissionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfilePermissions.html#Connect.Paginator.ListSecurityProfilePermissions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listsecurityprofilepermissionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListSecurityProfilePermissionsRequestListSecurityProfilePermissionsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListSecurityProfilePermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfilePermissions.html#Connect.Paginator.ListSecurityProfilePermissions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listsecurityprofilepermissionspaginator)
        """

class ListSecurityProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfiles.html#Connect.Paginator.ListSecurityProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listsecurityprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListSecurityProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfiles.html#Connect.Paginator.ListSecurityProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listsecurityprofilespaginator)
        """

class ListTaskTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTaskTemplates.html#Connect.Paginator.ListTaskTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listtasktemplatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTaskTemplatesRequestListTaskTemplatesPaginateTypeDef]
    ) -> AsyncIterator[ListTaskTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTaskTemplates.html#Connect.Paginator.ListTaskTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listtasktemplatespaginator)
        """

class ListTrafficDistributionGroupUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTrafficDistributionGroupUsers.html#Connect.Paginator.ListTrafficDistributionGroupUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listtrafficdistributiongroupuserspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListTrafficDistributionGroupUsersRequestListTrafficDistributionGroupUsersPaginateTypeDef
        ],
    ) -> AsyncIterator[ListTrafficDistributionGroupUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTrafficDistributionGroupUsers.html#Connect.Paginator.ListTrafficDistributionGroupUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listtrafficdistributiongroupuserspaginator)
        """

class ListTrafficDistributionGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTrafficDistributionGroups.html#Connect.Paginator.ListTrafficDistributionGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listtrafficdistributiongroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListTrafficDistributionGroupsRequestListTrafficDistributionGroupsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListTrafficDistributionGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTrafficDistributionGroups.html#Connect.Paginator.ListTrafficDistributionGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listtrafficdistributiongroupspaginator)
        """

class ListUseCasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUseCases.html#Connect.Paginator.ListUseCases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listusecasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUseCasesRequestListUseCasesPaginateTypeDef]
    ) -> AsyncIterator[ListUseCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUseCases.html#Connect.Paginator.ListUseCases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listusecasespaginator)
        """

class ListUserHierarchyGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUserHierarchyGroups.html#Connect.Paginator.ListUserHierarchyGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listuserhierarchygroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUserHierarchyGroupsRequestListUserHierarchyGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListUserHierarchyGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUserHierarchyGroups.html#Connect.Paginator.ListUserHierarchyGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listuserhierarchygroupspaginator)
        """

class ListUserProficienciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUserProficiencies.html#Connect.Paginator.ListUserProficiencies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listuserproficienciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUserProficienciesRequestListUserProficienciesPaginateTypeDef]
    ) -> AsyncIterator[ListUserProficienciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUserProficiencies.html#Connect.Paginator.ListUserProficiencies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listuserproficienciespaginator)
        """

class ListUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUsers.html#Connect.Paginator.ListUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listuserspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUsersRequestListUsersPaginateTypeDef]
    ) -> AsyncIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUsers.html#Connect.Paginator.ListUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listuserspaginator)
        """

class ListViewVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListViewVersions.html#Connect.Paginator.ListViewVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listviewversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListViewVersionsRequestListViewVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListViewVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListViewVersions.html#Connect.Paginator.ListViewVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listviewversionspaginator)
        """

class ListViewsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListViews.html#Connect.Paginator.ListViews)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listviewspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListViewsRequestListViewsPaginateTypeDef]
    ) -> AsyncIterator[ListViewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListViews.html#Connect.Paginator.ListViews.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listviewspaginator)
        """

class SearchAgentStatusesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchAgentStatuses.html#Connect.Paginator.SearchAgentStatuses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchagentstatusespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchAgentStatusesRequestSearchAgentStatusesPaginateTypeDef]
    ) -> AsyncIterator[SearchAgentStatusesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchAgentStatuses.html#Connect.Paginator.SearchAgentStatuses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchagentstatusespaginator)
        """

class SearchAvailablePhoneNumbersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchAvailablePhoneNumbers.html#Connect.Paginator.SearchAvailablePhoneNumbers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchavailablephonenumberspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            SearchAvailablePhoneNumbersRequestSearchAvailablePhoneNumbersPaginateTypeDef
        ],
    ) -> AsyncIterator[SearchAvailablePhoneNumbersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchAvailablePhoneNumbers.html#Connect.Paginator.SearchAvailablePhoneNumbers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchavailablephonenumberspaginator)
        """

class SearchContactFlowModulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContactFlowModules.html#Connect.Paginator.SearchContactFlowModules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchcontactflowmodulespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[SearchContactFlowModulesRequestSearchContactFlowModulesPaginateTypeDef],
    ) -> AsyncIterator[SearchContactFlowModulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContactFlowModules.html#Connect.Paginator.SearchContactFlowModules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchcontactflowmodulespaginator)
        """

class SearchContactFlowsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContactFlows.html#Connect.Paginator.SearchContactFlows)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchcontactflowspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchContactFlowsRequestSearchContactFlowsPaginateTypeDef]
    ) -> AsyncIterator[SearchContactFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContactFlows.html#Connect.Paginator.SearchContactFlows.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchcontactflowspaginator)
        """

class SearchContactsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContacts.html#Connect.Paginator.SearchContacts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchcontactspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchContactsRequestSearchContactsPaginateTypeDef]
    ) -> AsyncIterator[SearchContactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContacts.html#Connect.Paginator.SearchContacts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchcontactspaginator)
        """

class SearchHoursOfOperationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchHoursOfOperations.html#Connect.Paginator.SearchHoursOfOperations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchhoursofoperationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchHoursOfOperationsRequestSearchHoursOfOperationsPaginateTypeDef]
    ) -> AsyncIterator[SearchHoursOfOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchHoursOfOperations.html#Connect.Paginator.SearchHoursOfOperations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchhoursofoperationspaginator)
        """

class SearchPredefinedAttributesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchPredefinedAttributes.html#Connect.Paginator.SearchPredefinedAttributes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchpredefinedattributespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            SearchPredefinedAttributesRequestSearchPredefinedAttributesPaginateTypeDef
        ],
    ) -> AsyncIterator[SearchPredefinedAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchPredefinedAttributes.html#Connect.Paginator.SearchPredefinedAttributes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchpredefinedattributespaginator)
        """

class SearchPromptsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchPrompts.html#Connect.Paginator.SearchPrompts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchpromptspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchPromptsRequestSearchPromptsPaginateTypeDef]
    ) -> AsyncIterator[SearchPromptsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchPrompts.html#Connect.Paginator.SearchPrompts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchpromptspaginator)
        """

class SearchQueuesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchQueues.html#Connect.Paginator.SearchQueues)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchqueuespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchQueuesRequestSearchQueuesPaginateTypeDef]
    ) -> AsyncIterator[SearchQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchQueues.html#Connect.Paginator.SearchQueues.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchqueuespaginator)
        """

class SearchQuickConnectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchQuickConnects.html#Connect.Paginator.SearchQuickConnects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchquickconnectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchQuickConnectsRequestSearchQuickConnectsPaginateTypeDef]
    ) -> AsyncIterator[SearchQuickConnectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchQuickConnects.html#Connect.Paginator.SearchQuickConnects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchquickconnectspaginator)
        """

class SearchResourceTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchResourceTags.html#Connect.Paginator.SearchResourceTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchresourcetagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchResourceTagsRequestSearchResourceTagsPaginateTypeDef]
    ) -> AsyncIterator[SearchResourceTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchResourceTags.html#Connect.Paginator.SearchResourceTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchresourcetagspaginator)
        """

class SearchRoutingProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchRoutingProfiles.html#Connect.Paginator.SearchRoutingProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchroutingprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchRoutingProfilesRequestSearchRoutingProfilesPaginateTypeDef]
    ) -> AsyncIterator[SearchRoutingProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchRoutingProfiles.html#Connect.Paginator.SearchRoutingProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchroutingprofilespaginator)
        """

class SearchSecurityProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchSecurityProfiles.html#Connect.Paginator.SearchSecurityProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchsecurityprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchSecurityProfilesRequestSearchSecurityProfilesPaginateTypeDef]
    ) -> AsyncIterator[SearchSecurityProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchSecurityProfiles.html#Connect.Paginator.SearchSecurityProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchsecurityprofilespaginator)
        """

class SearchUserHierarchyGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchUserHierarchyGroups.html#Connect.Paginator.SearchUserHierarchyGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchuserhierarchygroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[SearchUserHierarchyGroupsRequestSearchUserHierarchyGroupsPaginateTypeDef],
    ) -> AsyncIterator[SearchUserHierarchyGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchUserHierarchyGroups.html#Connect.Paginator.SearchUserHierarchyGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchuserhierarchygroupspaginator)
        """

class SearchUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchUsers.html#Connect.Paginator.SearchUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchuserspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchUsersRequestSearchUsersPaginateTypeDef]
    ) -> AsyncIterator[SearchUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchUsers.html#Connect.Paginator.SearchUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchuserspaginator)
        """

class SearchVocabulariesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchVocabularies.html#Connect.Paginator.SearchVocabularies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchvocabulariespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchVocabulariesRequestSearchVocabulariesPaginateTypeDef]
    ) -> AsyncIterator[SearchVocabulariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchVocabularies.html#Connect.Paginator.SearchVocabularies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchvocabulariespaginator)
        """
