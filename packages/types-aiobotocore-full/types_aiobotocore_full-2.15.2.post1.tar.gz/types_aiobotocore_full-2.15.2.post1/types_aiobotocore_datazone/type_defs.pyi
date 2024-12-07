"""
Type annotations for datazone service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datazone/type_defs/)

Usage::

    ```python
    from types_aiobotocore_datazone.type_defs import AcceptChoiceTypeDef

    data: AcceptChoiceTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from aiobotocore.response import StreamingBody

from .literals import (
    AcceptRuleBehaviorType,
    AuthTypeType,
    ChangeActionType,
    ConfigurableActionTypeAuthorizationType,
    DataAssetActivityStatusType,
    DataProductStatusType,
    DataSourceErrorTypeType,
    DataSourceRunStatusType,
    DataSourceRunTypeType,
    DataSourceStatusType,
    DeploymentStatusType,
    DeploymentTypeType,
    DomainStatusType,
    EdgeDirectionType,
    EnableSettingType,
    EntityTypeType,
    EnvironmentStatusType,
    FilterExpressionTypeType,
    FilterStatusType,
    FormTypeStatusType,
    GlossaryStatusType,
    GlossaryTermStatusType,
    GroupProfileStatusType,
    GroupSearchTypeType,
    InventorySearchScopeType,
    ListingStatusType,
    ManagedPolicyTypeType,
    MetadataGenerationRunStatusType,
    NotificationRoleType,
    NotificationTypeType,
    ProjectDesignationType,
    ProjectStatusType,
    RejectRuleBehaviorType,
    SearchOutputAdditionalAttributeType,
    SelfGrantStatusType,
    SortKeyType,
    SortOrderType,
    SubscriptionGrantOverallStatusType,
    SubscriptionGrantStatusType,
    SubscriptionRequestStatusType,
    SubscriptionStatusType,
    TargetEntityTypeType,
    TaskStatusType,
    TimeSeriesEntityTypeType,
    TimezoneType,
    TypesSearchScopeType,
    UserAssignmentType,
    UserDesignationType,
    UserProfileStatusType,
    UserProfileTypeType,
    UserSearchTypeType,
    UserTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AcceptChoiceTypeDef",
    "AcceptPredictionsInputRequestTypeDef",
    "AcceptPredictionsOutputTypeDef",
    "AcceptRuleTypeDef",
    "AcceptSubscriptionRequestInputRequestTypeDef",
    "AcceptSubscriptionRequestOutputTypeDef",
    "AcceptedAssetScopeTypeDef",
    "ActionParametersTypeDef",
    "AddEntityOwnerInputRequestTypeDef",
    "AddPolicyGrantInputRequestTypeDef",
    "AddToProjectMemberPoolPolicyGrantDetailTypeDef",
    "AssetFilterConfigurationOutputTypeDef",
    "AssetFilterConfigurationTypeDef",
    "AssetFilterSummaryTypeDef",
    "AssetInDataProductListingItemTypeDef",
    "AssetItemAdditionalAttributesTypeDef",
    "AssetItemTypeDef",
    "AssetListingDetailsTypeDef",
    "AssetListingItemAdditionalAttributesTypeDef",
    "AssetListingItemTypeDef",
    "AssetListingTypeDef",
    "AssetRevisionTypeDef",
    "AssetScopeTypeDef",
    "AssetTargetNameMapTypeDef",
    "AssetTypeItemTypeDef",
    "AssociateEnvironmentRoleInputRequestTypeDef",
    "AwsConsoleLinkParametersTypeDef",
    "BlobTypeDef",
    "BusinessNameGenerationConfigurationTypeDef",
    "CancelMetadataGenerationRunInputRequestTypeDef",
    "CancelSubscriptionInputRequestTypeDef",
    "CancelSubscriptionOutputTypeDef",
    "CloudFormationPropertiesTypeDef",
    "ColumnFilterConfigurationOutputTypeDef",
    "ColumnFilterConfigurationTypeDef",
    "ColumnFilterConfigurationUnionTypeDef",
    "ConfigurableActionParameterTypeDef",
    "ConfigurableEnvironmentActionTypeDef",
    "CreateAssetFilterInputRequestTypeDef",
    "CreateAssetFilterOutputTypeDef",
    "CreateAssetInputRequestTypeDef",
    "CreateAssetOutputTypeDef",
    "CreateAssetRevisionInputRequestTypeDef",
    "CreateAssetRevisionOutputTypeDef",
    "CreateAssetTypeInputRequestTypeDef",
    "CreateAssetTypeOutputTypeDef",
    "CreateAssetTypePolicyGrantDetailTypeDef",
    "CreateDataProductInputRequestTypeDef",
    "CreateDataProductOutputTypeDef",
    "CreateDataProductRevisionInputRequestTypeDef",
    "CreateDataProductRevisionOutputTypeDef",
    "CreateDataSourceInputRequestTypeDef",
    "CreateDataSourceOutputTypeDef",
    "CreateDomainInputRequestTypeDef",
    "CreateDomainOutputTypeDef",
    "CreateDomainUnitInputRequestTypeDef",
    "CreateDomainUnitOutputTypeDef",
    "CreateDomainUnitPolicyGrantDetailTypeDef",
    "CreateEnvironmentActionInputRequestTypeDef",
    "CreateEnvironmentActionOutputTypeDef",
    "CreateEnvironmentInputRequestTypeDef",
    "CreateEnvironmentOutputTypeDef",
    "CreateEnvironmentProfileInputRequestTypeDef",
    "CreateEnvironmentProfileOutputTypeDef",
    "CreateEnvironmentProfilePolicyGrantDetailTypeDef",
    "CreateFormTypeInputRequestTypeDef",
    "CreateFormTypeOutputTypeDef",
    "CreateFormTypePolicyGrantDetailTypeDef",
    "CreateGlossaryInputRequestTypeDef",
    "CreateGlossaryOutputTypeDef",
    "CreateGlossaryPolicyGrantDetailTypeDef",
    "CreateGlossaryTermInputRequestTypeDef",
    "CreateGlossaryTermOutputTypeDef",
    "CreateGroupProfileInputRequestTypeDef",
    "CreateGroupProfileOutputTypeDef",
    "CreateListingChangeSetInputRequestTypeDef",
    "CreateListingChangeSetOutputTypeDef",
    "CreateProjectInputRequestTypeDef",
    "CreateProjectMembershipInputRequestTypeDef",
    "CreateProjectOutputTypeDef",
    "CreateProjectPolicyGrantDetailTypeDef",
    "CreateSubscriptionGrantInputRequestTypeDef",
    "CreateSubscriptionGrantOutputTypeDef",
    "CreateSubscriptionRequestInputRequestTypeDef",
    "CreateSubscriptionRequestOutputTypeDef",
    "CreateSubscriptionTargetInputRequestTypeDef",
    "CreateSubscriptionTargetOutputTypeDef",
    "CreateUserProfileInputRequestTypeDef",
    "CreateUserProfileOutputTypeDef",
    "CustomParameterTypeDef",
    "DataProductItemOutputTypeDef",
    "DataProductItemTypeDef",
    "DataProductItemUnionTypeDef",
    "DataProductListingItemAdditionalAttributesTypeDef",
    "DataProductListingItemTypeDef",
    "DataProductListingTypeDef",
    "DataProductResultItemTypeDef",
    "DataProductRevisionTypeDef",
    "DataSourceConfigurationInputTypeDef",
    "DataSourceConfigurationOutputTypeDef",
    "DataSourceErrorMessageTypeDef",
    "DataSourceRunActivityTypeDef",
    "DataSourceRunSummaryTypeDef",
    "DataSourceSummaryTypeDef",
    "DeleteAssetFilterInputRequestTypeDef",
    "DeleteAssetInputRequestTypeDef",
    "DeleteAssetTypeInputRequestTypeDef",
    "DeleteDataProductInputRequestTypeDef",
    "DeleteDataSourceInputRequestTypeDef",
    "DeleteDataSourceOutputTypeDef",
    "DeleteDomainInputRequestTypeDef",
    "DeleteDomainOutputTypeDef",
    "DeleteDomainUnitInputRequestTypeDef",
    "DeleteEnvironmentActionInputRequestTypeDef",
    "DeleteEnvironmentBlueprintConfigurationInputRequestTypeDef",
    "DeleteEnvironmentInputRequestTypeDef",
    "DeleteEnvironmentProfileInputRequestTypeDef",
    "DeleteFormTypeInputRequestTypeDef",
    "DeleteGlossaryInputRequestTypeDef",
    "DeleteGlossaryTermInputRequestTypeDef",
    "DeleteListingInputRequestTypeDef",
    "DeleteProjectInputRequestTypeDef",
    "DeleteProjectMembershipInputRequestTypeDef",
    "DeleteSubscriptionGrantInputRequestTypeDef",
    "DeleteSubscriptionGrantOutputTypeDef",
    "DeleteSubscriptionRequestInputRequestTypeDef",
    "DeleteSubscriptionTargetInputRequestTypeDef",
    "DeleteTimeSeriesDataPointsInputRequestTypeDef",
    "DeploymentPropertiesTypeDef",
    "DeploymentTypeDef",
    "DetailedGlossaryTermTypeDef",
    "DisassociateEnvironmentRoleInputRequestTypeDef",
    "DomainSummaryTypeDef",
    "DomainUnitFilterForProjectTypeDef",
    "DomainUnitGrantFilterOutputTypeDef",
    "DomainUnitGrantFilterTypeDef",
    "DomainUnitGrantFilterUnionTypeDef",
    "DomainUnitGroupPropertiesTypeDef",
    "DomainUnitOwnerPropertiesTypeDef",
    "DomainUnitPolicyGrantPrincipalOutputTypeDef",
    "DomainUnitPolicyGrantPrincipalTypeDef",
    "DomainUnitPolicyGrantPrincipalUnionTypeDef",
    "DomainUnitSummaryTypeDef",
    "DomainUnitUserPropertiesTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnvironmentActionSummaryTypeDef",
    "EnvironmentBlueprintConfigurationItemTypeDef",
    "EnvironmentBlueprintSummaryTypeDef",
    "EnvironmentErrorTypeDef",
    "EnvironmentParameterTypeDef",
    "EnvironmentProfileSummaryTypeDef",
    "EnvironmentSummaryTypeDef",
    "EqualToExpressionTypeDef",
    "FailureCauseTypeDef",
    "FilterClausePaginatorTypeDef",
    "FilterClauseTypeDef",
    "FilterExpressionTypeDef",
    "FilterTypeDef",
    "FormEntryInputTypeDef",
    "FormEntryOutputTypeDef",
    "FormInputTypeDef",
    "FormOutputTypeDef",
    "FormTypeDataTypeDef",
    "GetAssetFilterInputRequestTypeDef",
    "GetAssetFilterOutputTypeDef",
    "GetAssetInputRequestTypeDef",
    "GetAssetOutputTypeDef",
    "GetAssetTypeInputRequestTypeDef",
    "GetAssetTypeOutputTypeDef",
    "GetDataProductInputRequestTypeDef",
    "GetDataProductOutputTypeDef",
    "GetDataSourceInputRequestTypeDef",
    "GetDataSourceOutputTypeDef",
    "GetDataSourceRunInputRequestTypeDef",
    "GetDataSourceRunOutputTypeDef",
    "GetDomainInputRequestTypeDef",
    "GetDomainOutputTypeDef",
    "GetDomainUnitInputRequestTypeDef",
    "GetDomainUnitOutputTypeDef",
    "GetEnvironmentActionInputRequestTypeDef",
    "GetEnvironmentActionOutputTypeDef",
    "GetEnvironmentBlueprintConfigurationInputRequestTypeDef",
    "GetEnvironmentBlueprintConfigurationOutputTypeDef",
    "GetEnvironmentBlueprintInputRequestTypeDef",
    "GetEnvironmentBlueprintOutputTypeDef",
    "GetEnvironmentCredentialsInputRequestTypeDef",
    "GetEnvironmentCredentialsOutputTypeDef",
    "GetEnvironmentInputRequestTypeDef",
    "GetEnvironmentOutputTypeDef",
    "GetEnvironmentProfileInputRequestTypeDef",
    "GetEnvironmentProfileOutputTypeDef",
    "GetFormTypeInputRequestTypeDef",
    "GetFormTypeOutputTypeDef",
    "GetGlossaryInputRequestTypeDef",
    "GetGlossaryOutputTypeDef",
    "GetGlossaryTermInputRequestTypeDef",
    "GetGlossaryTermOutputTypeDef",
    "GetGroupProfileInputRequestTypeDef",
    "GetGroupProfileOutputTypeDef",
    "GetIamPortalLoginUrlInputRequestTypeDef",
    "GetIamPortalLoginUrlOutputTypeDef",
    "GetLineageNodeInputRequestTypeDef",
    "GetLineageNodeOutputTypeDef",
    "GetListingInputRequestTypeDef",
    "GetListingOutputTypeDef",
    "GetMetadataGenerationRunInputRequestTypeDef",
    "GetMetadataGenerationRunOutputTypeDef",
    "GetProjectInputRequestTypeDef",
    "GetProjectOutputTypeDef",
    "GetSubscriptionGrantInputRequestTypeDef",
    "GetSubscriptionGrantOutputTypeDef",
    "GetSubscriptionInputRequestTypeDef",
    "GetSubscriptionOutputTypeDef",
    "GetSubscriptionRequestDetailsInputRequestTypeDef",
    "GetSubscriptionRequestDetailsOutputTypeDef",
    "GetSubscriptionTargetInputRequestTypeDef",
    "GetSubscriptionTargetOutputTypeDef",
    "GetTimeSeriesDataPointInputRequestTypeDef",
    "GetTimeSeriesDataPointOutputTypeDef",
    "GetUserProfileInputRequestTypeDef",
    "GetUserProfileOutputTypeDef",
    "GlossaryItemTypeDef",
    "GlossaryTermItemTypeDef",
    "GlueRunConfigurationInputTypeDef",
    "GlueRunConfigurationOutputTypeDef",
    "GlueSelfGrantStatusOutputTypeDef",
    "GrantedEntityInputTypeDef",
    "GrantedEntityTypeDef",
    "GreaterThanExpressionTypeDef",
    "GreaterThanOrEqualToExpressionTypeDef",
    "GroupDetailsTypeDef",
    "GroupPolicyGrantPrincipalTypeDef",
    "GroupProfileSummaryTypeDef",
    "IamUserProfileDetailsTypeDef",
    "ImportTypeDef",
    "InExpressionOutputTypeDef",
    "InExpressionTypeDef",
    "InExpressionUnionTypeDef",
    "IsNotNullExpressionTypeDef",
    "IsNullExpressionTypeDef",
    "LakeFormationConfigurationOutputTypeDef",
    "LakeFormationConfigurationTypeDef",
    "LakeFormationConfigurationUnionTypeDef",
    "LessThanExpressionTypeDef",
    "LessThanOrEqualToExpressionTypeDef",
    "LikeExpressionTypeDef",
    "LineageNodeReferenceTypeDef",
    "LineageNodeSummaryTypeDef",
    "LineageNodeTypeItemTypeDef",
    "ListAssetFiltersInputListAssetFiltersPaginateTypeDef",
    "ListAssetFiltersInputRequestTypeDef",
    "ListAssetFiltersOutputTypeDef",
    "ListAssetRevisionsInputListAssetRevisionsPaginateTypeDef",
    "ListAssetRevisionsInputRequestTypeDef",
    "ListAssetRevisionsOutputTypeDef",
    "ListDataProductRevisionsInputListDataProductRevisionsPaginateTypeDef",
    "ListDataProductRevisionsInputRequestTypeDef",
    "ListDataProductRevisionsOutputTypeDef",
    "ListDataSourceRunActivitiesInputListDataSourceRunActivitiesPaginateTypeDef",
    "ListDataSourceRunActivitiesInputRequestTypeDef",
    "ListDataSourceRunActivitiesOutputTypeDef",
    "ListDataSourceRunsInputListDataSourceRunsPaginateTypeDef",
    "ListDataSourceRunsInputRequestTypeDef",
    "ListDataSourceRunsOutputTypeDef",
    "ListDataSourcesInputListDataSourcesPaginateTypeDef",
    "ListDataSourcesInputRequestTypeDef",
    "ListDataSourcesOutputTypeDef",
    "ListDomainUnitsForParentInputListDomainUnitsForParentPaginateTypeDef",
    "ListDomainUnitsForParentInputRequestTypeDef",
    "ListDomainUnitsForParentOutputTypeDef",
    "ListDomainsInputListDomainsPaginateTypeDef",
    "ListDomainsInputRequestTypeDef",
    "ListDomainsOutputTypeDef",
    "ListEntityOwnersInputListEntityOwnersPaginateTypeDef",
    "ListEntityOwnersInputRequestTypeDef",
    "ListEntityOwnersOutputTypeDef",
    "ListEnvironmentActionsInputListEnvironmentActionsPaginateTypeDef",
    "ListEnvironmentActionsInputRequestTypeDef",
    "ListEnvironmentActionsOutputTypeDef",
    "ListEnvironmentBlueprintConfigurationsInputListEnvironmentBlueprintConfigurationsPaginateTypeDef",
    "ListEnvironmentBlueprintConfigurationsInputRequestTypeDef",
    "ListEnvironmentBlueprintConfigurationsOutputTypeDef",
    "ListEnvironmentBlueprintsInputListEnvironmentBlueprintsPaginateTypeDef",
    "ListEnvironmentBlueprintsInputRequestTypeDef",
    "ListEnvironmentBlueprintsOutputTypeDef",
    "ListEnvironmentProfilesInputListEnvironmentProfilesPaginateTypeDef",
    "ListEnvironmentProfilesInputRequestTypeDef",
    "ListEnvironmentProfilesOutputTypeDef",
    "ListEnvironmentsInputListEnvironmentsPaginateTypeDef",
    "ListEnvironmentsInputRequestTypeDef",
    "ListEnvironmentsOutputTypeDef",
    "ListLineageNodeHistoryInputListLineageNodeHistoryPaginateTypeDef",
    "ListLineageNodeHistoryInputRequestTypeDef",
    "ListLineageNodeHistoryOutputTypeDef",
    "ListMetadataGenerationRunsInputListMetadataGenerationRunsPaginateTypeDef",
    "ListMetadataGenerationRunsInputRequestTypeDef",
    "ListMetadataGenerationRunsOutputTypeDef",
    "ListNotificationsInputListNotificationsPaginateTypeDef",
    "ListNotificationsInputRequestTypeDef",
    "ListNotificationsOutputTypeDef",
    "ListPolicyGrantsInputListPolicyGrantsPaginateTypeDef",
    "ListPolicyGrantsInputRequestTypeDef",
    "ListPolicyGrantsOutputTypeDef",
    "ListProjectMembershipsInputListProjectMembershipsPaginateTypeDef",
    "ListProjectMembershipsInputRequestTypeDef",
    "ListProjectMembershipsOutputTypeDef",
    "ListProjectsInputListProjectsPaginateTypeDef",
    "ListProjectsInputRequestTypeDef",
    "ListProjectsOutputTypeDef",
    "ListSubscriptionGrantsInputListSubscriptionGrantsPaginateTypeDef",
    "ListSubscriptionGrantsInputRequestTypeDef",
    "ListSubscriptionGrantsOutputTypeDef",
    "ListSubscriptionRequestsInputListSubscriptionRequestsPaginateTypeDef",
    "ListSubscriptionRequestsInputRequestTypeDef",
    "ListSubscriptionRequestsOutputTypeDef",
    "ListSubscriptionTargetsInputListSubscriptionTargetsPaginateTypeDef",
    "ListSubscriptionTargetsInputRequestTypeDef",
    "ListSubscriptionTargetsOutputTypeDef",
    "ListSubscriptionsInputListSubscriptionsPaginateTypeDef",
    "ListSubscriptionsInputRequestTypeDef",
    "ListSubscriptionsOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTimeSeriesDataPointsInputListTimeSeriesDataPointsPaginateTypeDef",
    "ListTimeSeriesDataPointsInputRequestTypeDef",
    "ListTimeSeriesDataPointsOutputTypeDef",
    "ListingItemTypeDef",
    "ListingRevisionInputTypeDef",
    "ListingRevisionTypeDef",
    "ListingSummaryItemTypeDef",
    "ListingSummaryTypeDef",
    "MemberDetailsTypeDef",
    "MemberTypeDef",
    "MetadataGenerationRunItemTypeDef",
    "MetadataGenerationRunTargetTypeDef",
    "ModelTypeDef",
    "NotEqualToExpressionTypeDef",
    "NotInExpressionOutputTypeDef",
    "NotInExpressionTypeDef",
    "NotInExpressionUnionTypeDef",
    "NotLikeExpressionTypeDef",
    "NotificationOutputTypeDef",
    "NotificationResourceTypeDef",
    "OverrideDomainUnitOwnersPolicyGrantDetailTypeDef",
    "OverrideProjectOwnersPolicyGrantDetailTypeDef",
    "OwnerGroupPropertiesOutputTypeDef",
    "OwnerGroupPropertiesTypeDef",
    "OwnerPropertiesOutputTypeDef",
    "OwnerPropertiesTypeDef",
    "OwnerUserPropertiesOutputTypeDef",
    "OwnerUserPropertiesTypeDef",
    "PaginatorConfigTypeDef",
    "PolicyGrantDetailOutputTypeDef",
    "PolicyGrantDetailTypeDef",
    "PolicyGrantMemberTypeDef",
    "PolicyGrantPrincipalOutputTypeDef",
    "PolicyGrantPrincipalTypeDef",
    "PostLineageEventInputRequestTypeDef",
    "PostTimeSeriesDataPointsInputRequestTypeDef",
    "PostTimeSeriesDataPointsOutputTypeDef",
    "PredictionConfigurationTypeDef",
    "ProjectDeletionErrorTypeDef",
    "ProjectGrantFilterTypeDef",
    "ProjectMemberTypeDef",
    "ProjectPolicyGrantPrincipalTypeDef",
    "ProjectSummaryTypeDef",
    "ProvisioningConfigurationOutputTypeDef",
    "ProvisioningConfigurationTypeDef",
    "ProvisioningConfigurationUnionTypeDef",
    "ProvisioningPropertiesTypeDef",
    "PutEnvironmentBlueprintConfigurationInputRequestTypeDef",
    "PutEnvironmentBlueprintConfigurationOutputTypeDef",
    "RecommendationConfigurationTypeDef",
    "RedshiftClusterStorageTypeDef",
    "RedshiftCredentialConfigurationTypeDef",
    "RedshiftRunConfigurationInputTypeDef",
    "RedshiftRunConfigurationOutputTypeDef",
    "RedshiftSelfGrantStatusOutputTypeDef",
    "RedshiftServerlessStorageTypeDef",
    "RedshiftStorageTypeDef",
    "RejectChoiceTypeDef",
    "RejectPredictionsInputRequestTypeDef",
    "RejectPredictionsOutputTypeDef",
    "RejectRuleTypeDef",
    "RejectSubscriptionRequestInputRequestTypeDef",
    "RejectSubscriptionRequestOutputTypeDef",
    "RelationalFilterConfigurationOutputTypeDef",
    "RelationalFilterConfigurationTypeDef",
    "RelationalFilterConfigurationUnionTypeDef",
    "RemoveEntityOwnerInputRequestTypeDef",
    "RemovePolicyGrantInputRequestTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "RevokeSubscriptionInputRequestTypeDef",
    "RevokeSubscriptionOutputTypeDef",
    "RowFilterConfigurationOutputTypeDef",
    "RowFilterConfigurationTypeDef",
    "RowFilterConfigurationUnionTypeDef",
    "RowFilterExpressionOutputTypeDef",
    "RowFilterExpressionTypeDef",
    "RowFilterExpressionUnionTypeDef",
    "RowFilterOutputTypeDef",
    "RowFilterTypeDef",
    "RowFilterUnionTypeDef",
    "RunStatisticsForAssetsTypeDef",
    "ScheduleConfigurationTypeDef",
    "SearchGroupProfilesInputRequestTypeDef",
    "SearchGroupProfilesInputSearchGroupProfilesPaginateTypeDef",
    "SearchGroupProfilesOutputTypeDef",
    "SearchInItemTypeDef",
    "SearchInputRequestTypeDef",
    "SearchInputSearchPaginateTypeDef",
    "SearchInventoryResultItemTypeDef",
    "SearchListingsInputRequestTypeDef",
    "SearchListingsInputSearchListingsPaginateTypeDef",
    "SearchListingsOutputTypeDef",
    "SearchOutputTypeDef",
    "SearchResultItemTypeDef",
    "SearchSortTypeDef",
    "SearchTypesInputRequestTypeDef",
    "SearchTypesInputSearchTypesPaginateTypeDef",
    "SearchTypesOutputTypeDef",
    "SearchTypesResultItemTypeDef",
    "SearchUserProfilesInputRequestTypeDef",
    "SearchUserProfilesInputSearchUserProfilesPaginateTypeDef",
    "SearchUserProfilesOutputTypeDef",
    "SelfGrantStatusDetailTypeDef",
    "SelfGrantStatusOutputTypeDef",
    "SingleSignOnTypeDef",
    "SsoUserProfileDetailsTypeDef",
    "StartDataSourceRunInputRequestTypeDef",
    "StartDataSourceRunOutputTypeDef",
    "StartMetadataGenerationRunInputRequestTypeDef",
    "StartMetadataGenerationRunOutputTypeDef",
    "SubscribedAssetListingTypeDef",
    "SubscribedAssetTypeDef",
    "SubscribedListingInputTypeDef",
    "SubscribedListingItemTypeDef",
    "SubscribedListingTypeDef",
    "SubscribedPrincipalInputTypeDef",
    "SubscribedPrincipalTypeDef",
    "SubscribedProductListingTypeDef",
    "SubscribedProjectInputTypeDef",
    "SubscribedProjectTypeDef",
    "SubscriptionGrantSummaryTypeDef",
    "SubscriptionRequestSummaryTypeDef",
    "SubscriptionSummaryTypeDef",
    "SubscriptionTargetFormTypeDef",
    "SubscriptionTargetSummaryTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TermRelationsOutputTypeDef",
    "TermRelationsTypeDef",
    "TimeSeriesDataPointFormInputTypeDef",
    "TimeSeriesDataPointFormOutputTypeDef",
    "TimeSeriesDataPointSummaryFormOutputTypeDef",
    "TimestampTypeDef",
    "TopicTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAssetFilterInputRequestTypeDef",
    "UpdateAssetFilterOutputTypeDef",
    "UpdateDataSourceInputRequestTypeDef",
    "UpdateDataSourceOutputTypeDef",
    "UpdateDomainInputRequestTypeDef",
    "UpdateDomainOutputTypeDef",
    "UpdateDomainUnitInputRequestTypeDef",
    "UpdateDomainUnitOutputTypeDef",
    "UpdateEnvironmentActionInputRequestTypeDef",
    "UpdateEnvironmentActionOutputTypeDef",
    "UpdateEnvironmentInputRequestTypeDef",
    "UpdateEnvironmentOutputTypeDef",
    "UpdateEnvironmentProfileInputRequestTypeDef",
    "UpdateEnvironmentProfileOutputTypeDef",
    "UpdateGlossaryInputRequestTypeDef",
    "UpdateGlossaryOutputTypeDef",
    "UpdateGlossaryTermInputRequestTypeDef",
    "UpdateGlossaryTermOutputTypeDef",
    "UpdateGroupProfileInputRequestTypeDef",
    "UpdateGroupProfileOutputTypeDef",
    "UpdateProjectInputRequestTypeDef",
    "UpdateProjectOutputTypeDef",
    "UpdateSubscriptionGrantStatusInputRequestTypeDef",
    "UpdateSubscriptionGrantStatusOutputTypeDef",
    "UpdateSubscriptionRequestInputRequestTypeDef",
    "UpdateSubscriptionRequestOutputTypeDef",
    "UpdateSubscriptionTargetInputRequestTypeDef",
    "UpdateSubscriptionTargetOutputTypeDef",
    "UpdateUserProfileInputRequestTypeDef",
    "UpdateUserProfileOutputTypeDef",
    "UserDetailsTypeDef",
    "UserPolicyGrantPrincipalOutputTypeDef",
    "UserPolicyGrantPrincipalTypeDef",
    "UserPolicyGrantPrincipalUnionTypeDef",
    "UserProfileDetailsTypeDef",
    "UserProfileSummaryTypeDef",
)

class AcceptChoiceTypeDef(TypedDict):
    predictionTarget: str
    editedValue: NotRequired[str]
    predictionChoice: NotRequired[int]

class AcceptRuleTypeDef(TypedDict):
    rule: NotRequired[AcceptRuleBehaviorType]
    threshold: NotRequired[float]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AcceptedAssetScopeTypeDef(TypedDict):
    assetId: str
    filterIds: Sequence[str]

class AwsConsoleLinkParametersTypeDef(TypedDict):
    uri: NotRequired[str]

class AddToProjectMemberPoolPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]

class ColumnFilterConfigurationOutputTypeDef(TypedDict):
    includedColumnNames: NotRequired[List[str]]

AssetFilterSummaryTypeDef = TypedDict(
    "AssetFilterSummaryTypeDef",
    {
        "assetId": str,
        "domainId": str,
        "id": str,
        "name": str,
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "effectiveColumnNames": NotRequired[List[str]],
        "effectiveRowFilter": NotRequired[str],
        "errorMessage": NotRequired[str],
        "status": NotRequired[FilterStatusType],
    },
)

class AssetInDataProductListingItemTypeDef(TypedDict):
    entityId: NotRequired[str]
    entityRevision: NotRequired[str]
    entityType: NotRequired[str]

class FormOutputTypeDef(TypedDict):
    formName: str
    content: NotRequired[str]
    typeName: NotRequired[str]
    typeRevision: NotRequired[str]

TimeSeriesDataPointSummaryFormOutputTypeDef = TypedDict(
    "TimeSeriesDataPointSummaryFormOutputTypeDef",
    {
        "formName": str,
        "timestamp": datetime,
        "typeIdentifier": str,
        "contentSummary": NotRequired[str],
        "id": NotRequired[str],
        "typeRevision": NotRequired[str],
    },
)

class AssetListingDetailsTypeDef(TypedDict):
    listingId: str
    listingStatus: ListingStatusType

class DetailedGlossaryTermTypeDef(TypedDict):
    name: NotRequired[str]
    shortDescription: NotRequired[str]

AssetRevisionTypeDef = TypedDict(
    "AssetRevisionTypeDef",
    {
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "domainId": NotRequired[str],
        "id": NotRequired[str],
        "revision": NotRequired[str],
    },
)

class AssetScopeTypeDef(TypedDict):
    assetId: str
    filterIds: List[str]
    status: str
    errorMessage: NotRequired[str]

class AssetTargetNameMapTypeDef(TypedDict):
    assetId: str
    targetName: str

class FormEntryOutputTypeDef(TypedDict):
    typeName: str
    typeRevision: str
    required: NotRequired[bool]

class AssociateEnvironmentRoleInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    environmentRoleArn: str

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class BusinessNameGenerationConfigurationTypeDef(TypedDict):
    enabled: NotRequired[bool]

class CancelMetadataGenerationRunInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class CancelSubscriptionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class CloudFormationPropertiesTypeDef(TypedDict):
    templateUrl: str

class ColumnFilterConfigurationTypeDef(TypedDict):
    includedColumnNames: NotRequired[Sequence[str]]

class ConfigurableActionParameterTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]

class FormInputTypeDef(TypedDict):
    formName: str
    content: NotRequired[str]
    typeIdentifier: NotRequired[str]
    typeRevision: NotRequired[str]

class FormEntryInputTypeDef(TypedDict):
    typeIdentifier: str
    typeRevision: str
    required: NotRequired[bool]

class CreateAssetTypePolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]

class DataProductItemOutputTypeDef(TypedDict):
    identifier: str
    itemType: Literal["ASSET"]
    glossaryTerms: NotRequired[List[str]]
    revision: NotRequired[str]

class DataProductItemTypeDef(TypedDict):
    identifier: str
    itemType: Literal["ASSET"]
    glossaryTerms: NotRequired[Sequence[str]]
    revision: NotRequired[str]

class RecommendationConfigurationTypeDef(TypedDict):
    enableBusinessNameGeneration: NotRequired[bool]

class ScheduleConfigurationTypeDef(TypedDict):
    schedule: NotRequired[str]
    timezone: NotRequired[TimezoneType]

class DataSourceErrorMessageTypeDef(TypedDict):
    errorType: DataSourceErrorTypeType
    errorDetail: NotRequired[str]

SingleSignOnTypeDef = TypedDict(
    "SingleSignOnTypeDef",
    {
        "type": NotRequired[AuthTypeType],
        "userAssignment": NotRequired[UserAssignmentType],
    },
)

class CreateDomainUnitInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    parentDomainUnitIdentifier: str
    clientToken: NotRequired[str]
    description: NotRequired[str]

class CreateDomainUnitPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]

class EnvironmentParameterTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[str]

class CustomParameterTypeDef(TypedDict):
    fieldType: str
    keyName: str
    defaultValue: NotRequired[str]
    description: NotRequired[str]
    isEditable: NotRequired[bool]
    isOptional: NotRequired[bool]

class DeploymentPropertiesTypeDef(TypedDict):
    endTimeoutMinutes: NotRequired[int]
    startTimeoutMinutes: NotRequired[int]

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "type": str,
        "value": str,
        "name": NotRequired[str],
        "provider": NotRequired[str],
    },
)

class CreateEnvironmentProfilePolicyGrantDetailTypeDef(TypedDict):
    domainUnitId: NotRequired[str]

class ModelTypeDef(TypedDict):
    smithy: NotRequired[str]

class CreateFormTypePolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]

class CreateGlossaryInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    owningProjectIdentifier: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    status: NotRequired[GlossaryStatusType]

class CreateGlossaryPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]

class TermRelationsTypeDef(TypedDict):
    classifies: NotRequired[Sequence[str]]
    isA: NotRequired[Sequence[str]]

class TermRelationsOutputTypeDef(TypedDict):
    classifies: NotRequired[List[str]]
    isA: NotRequired[List[str]]

class CreateGroupProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    groupIdentifier: str
    clientToken: NotRequired[str]

class CreateListingChangeSetInputRequestTypeDef(TypedDict):
    action: ChangeActionType
    domainIdentifier: str
    entityIdentifier: str
    entityType: EntityTypeType
    clientToken: NotRequired[str]
    entityRevision: NotRequired[str]

class CreateProjectInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    description: NotRequired[str]
    domainUnitId: NotRequired[str]
    glossaryTerms: NotRequired[Sequence[str]]

class MemberTypeDef(TypedDict):
    groupIdentifier: NotRequired[str]
    userIdentifier: NotRequired[str]

class ProjectDeletionErrorTypeDef(TypedDict):
    code: NotRequired[str]
    message: NotRequired[str]

class CreateProjectPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]

class SubscribedListingInputTypeDef(TypedDict):
    identifier: str

class SubscriptionTargetFormTypeDef(TypedDict):
    content: str
    formName: str

class CreateUserProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    userIdentifier: str
    clientToken: NotRequired[str]
    userType: NotRequired[UserTypeType]

class DataProductListingItemAdditionalAttributesTypeDef(TypedDict):
    forms: NotRequired[str]

DataProductResultItemTypeDef = TypedDict(
    "DataProductResultItemTypeDef",
    {
        "domainId": str,
        "id": str,
        "name": str,
        "owningProjectId": str,
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "description": NotRequired[str],
        "firstRevisionCreatedAt": NotRequired[datetime],
        "firstRevisionCreatedBy": NotRequired[str],
        "glossaryTerms": NotRequired[List[str]],
    },
)
DataProductRevisionTypeDef = TypedDict(
    "DataProductRevisionTypeDef",
    {
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "domainId": NotRequired[str],
        "id": NotRequired[str],
        "revision": NotRequired[str],
    },
)

class RunStatisticsForAssetsTypeDef(TypedDict):
    added: NotRequired[int]
    failed: NotRequired[int]
    skipped: NotRequired[int]
    unchanged: NotRequired[int]
    updated: NotRequired[int]

class DeleteAssetFilterInputRequestTypeDef(TypedDict):
    assetIdentifier: str
    domainIdentifier: str
    identifier: str

class DeleteAssetInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteAssetTypeInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteDataProductInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteDataSourceInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    clientToken: NotRequired[str]
    retainPermissionsOnRevokeFailure: NotRequired[bool]

class DeleteDomainInputRequestTypeDef(TypedDict):
    identifier: str
    clientToken: NotRequired[str]
    skipDeletionCheck: NotRequired[bool]

class DeleteDomainUnitInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteEnvironmentActionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str

class DeleteEnvironmentBlueprintConfigurationInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentBlueprintIdentifier: str

class DeleteEnvironmentInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteEnvironmentProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteFormTypeInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    formTypeIdentifier: str

class DeleteGlossaryInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteGlossaryTermInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteListingInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteProjectInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    skipDeletionCheck: NotRequired[bool]

class DeleteSubscriptionGrantInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteSubscriptionRequestInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class DeleteSubscriptionTargetInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str

class DeleteTimeSeriesDataPointsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TimeSeriesEntityTypeType
    formName: str
    clientToken: NotRequired[str]

class EnvironmentErrorTypeDef(TypedDict):
    message: str
    code: NotRequired[str]

class DisassociateEnvironmentRoleInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    environmentRoleArn: str

DomainSummaryTypeDef = TypedDict(
    "DomainSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "id": str,
        "managedAccountId": str,
        "name": str,
        "status": DomainStatusType,
        "description": NotRequired[str],
        "lastUpdatedAt": NotRequired[datetime],
        "portalUrl": NotRequired[str],
    },
)

class DomainUnitFilterForProjectTypeDef(TypedDict):
    domainUnit: str
    includeChildDomainUnits: NotRequired[bool]

class DomainUnitGrantFilterOutputTypeDef(TypedDict):
    allDomainUnitsGrantFilter: NotRequired[Dict[str, Any]]

class DomainUnitGrantFilterTypeDef(TypedDict):
    allDomainUnitsGrantFilter: NotRequired[Mapping[str, Any]]

class DomainUnitGroupPropertiesTypeDef(TypedDict):
    groupId: NotRequired[str]

class DomainUnitUserPropertiesTypeDef(TypedDict):
    userId: NotRequired[str]

DomainUnitSummaryTypeDef = TypedDict(
    "DomainUnitSummaryTypeDef",
    {
        "id": str,
        "name": str,
    },
)
EnvironmentProfileSummaryTypeDef = TypedDict(
    "EnvironmentProfileSummaryTypeDef",
    {
        "createdBy": str,
        "domainId": str,
        "environmentBlueprintId": str,
        "id": str,
        "name": str,
        "awsAccountId": NotRequired[str],
        "awsAccountRegion": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "projectId": NotRequired[str],
        "updatedAt": NotRequired[datetime],
    },
)
EnvironmentSummaryTypeDef = TypedDict(
    "EnvironmentSummaryTypeDef",
    {
        "createdBy": str,
        "domainId": str,
        "name": str,
        "projectId": str,
        "provider": str,
        "awsAccountId": NotRequired[str],
        "awsAccountRegion": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "environmentProfileId": NotRequired[str],
        "id": NotRequired[str],
        "status": NotRequired[EnvironmentStatusType],
        "updatedAt": NotRequired[datetime],
    },
)

class EqualToExpressionTypeDef(TypedDict):
    columnName: str
    value: str

class FailureCauseTypeDef(TypedDict):
    message: NotRequired[str]

class FilterTypeDef(TypedDict):
    attribute: str
    value: str

FilterExpressionTypeDef = TypedDict(
    "FilterExpressionTypeDef",
    {
        "expression": str,
        "type": FilterExpressionTypeType,
    },
)

class ImportTypeDef(TypedDict):
    name: str
    revision: str

class GetAssetFilterInputRequestTypeDef(TypedDict):
    assetIdentifier: str
    domainIdentifier: str
    identifier: str

class GetAssetInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    revision: NotRequired[str]

class GetAssetTypeInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    revision: NotRequired[str]

class GetDataProductInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    revision: NotRequired[str]

class GetDataSourceInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetDataSourceRunInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetDomainInputRequestTypeDef(TypedDict):
    identifier: str

class GetDomainUnitInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetEnvironmentActionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str

class GetEnvironmentBlueprintConfigurationInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentBlueprintIdentifier: str

class GetEnvironmentBlueprintInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetEnvironmentCredentialsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str

class GetEnvironmentInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetEnvironmentProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetFormTypeInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    formTypeIdentifier: str
    revision: NotRequired[str]

class GetGlossaryInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetGlossaryTermInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetGroupProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    groupIdentifier: str

class GetIamPortalLoginUrlInputRequestTypeDef(TypedDict):
    domainIdentifier: str

TimestampTypeDef = Union[datetime, str]
LineageNodeReferenceTypeDef = TypedDict(
    "LineageNodeReferenceTypeDef",
    {
        "eventTimestamp": NotRequired[datetime],
        "id": NotRequired[str],
    },
)

class GetListingInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    listingRevision: NotRequired[str]

class GetMetadataGenerationRunInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

MetadataGenerationRunTargetTypeDef = TypedDict(
    "MetadataGenerationRunTargetTypeDef",
    {
        "identifier": str,
        "type": Literal["ASSET"],
        "revision": NotRequired[str],
    },
)

class GetProjectInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetSubscriptionGrantInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetSubscriptionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetSubscriptionRequestDetailsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str

class GetSubscriptionTargetInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str

class GetTimeSeriesDataPointInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TimeSeriesEntityTypeType
    formName: str
    identifier: str

TimeSeriesDataPointFormOutputTypeDef = TypedDict(
    "TimeSeriesDataPointFormOutputTypeDef",
    {
        "formName": str,
        "timestamp": datetime,
        "typeIdentifier": str,
        "content": NotRequired[str],
        "id": NotRequired[str],
        "typeRevision": NotRequired[str],
    },
)
GetUserProfileInputRequestTypeDef = TypedDict(
    "GetUserProfileInputRequestTypeDef",
    {
        "domainIdentifier": str,
        "userIdentifier": str,
        "type": NotRequired[UserProfileTypeType],
    },
)
GlossaryItemTypeDef = TypedDict(
    "GlossaryItemTypeDef",
    {
        "domainId": str,
        "id": str,
        "name": str,
        "owningProjectId": str,
        "status": GlossaryStatusType,
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "description": NotRequired[str],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)

class SelfGrantStatusDetailTypeDef(TypedDict):
    databaseName: str
    status: SelfGrantStatusType
    failureCause: NotRequired[str]
    schemaName: NotRequired[str]

class ListingRevisionInputTypeDef(TypedDict):
    identifier: str
    revision: str

ListingRevisionTypeDef = TypedDict(
    "ListingRevisionTypeDef",
    {
        "id": str,
        "revision": str,
    },
)

class GreaterThanExpressionTypeDef(TypedDict):
    columnName: str
    value: str

class GreaterThanOrEqualToExpressionTypeDef(TypedDict):
    columnName: str
    value: str

class GroupDetailsTypeDef(TypedDict):
    groupId: str

class GroupPolicyGrantPrincipalTypeDef(TypedDict):
    groupIdentifier: NotRequired[str]

GroupProfileSummaryTypeDef = TypedDict(
    "GroupProfileSummaryTypeDef",
    {
        "domainId": NotRequired[str],
        "groupName": NotRequired[str],
        "id": NotRequired[str],
        "status": NotRequired[GroupProfileStatusType],
    },
)

class IamUserProfileDetailsTypeDef(TypedDict):
    arn: NotRequired[str]

class InExpressionOutputTypeDef(TypedDict):
    columnName: str
    values: List[str]

class InExpressionTypeDef(TypedDict):
    columnName: str
    values: Sequence[str]

class IsNotNullExpressionTypeDef(TypedDict):
    columnName: str

class IsNullExpressionTypeDef(TypedDict):
    columnName: str

class LakeFormationConfigurationOutputTypeDef(TypedDict):
    locationRegistrationExcludeS3Locations: NotRequired[List[str]]
    locationRegistrationRole: NotRequired[str]

class LakeFormationConfigurationTypeDef(TypedDict):
    locationRegistrationExcludeS3Locations: NotRequired[Sequence[str]]
    locationRegistrationRole: NotRequired[str]

class LessThanExpressionTypeDef(TypedDict):
    columnName: str
    value: str

class LessThanOrEqualToExpressionTypeDef(TypedDict):
    columnName: str
    value: str

class LikeExpressionTypeDef(TypedDict):
    columnName: str
    value: str

LineageNodeSummaryTypeDef = TypedDict(
    "LineageNodeSummaryTypeDef",
    {
        "domainId": str,
        "id": str,
        "typeName": str,
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "description": NotRequired[str],
        "eventTimestamp": NotRequired[datetime],
        "name": NotRequired[str],
        "sourceIdentifier": NotRequired[str],
        "typeRevision": NotRequired[str],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAssetFiltersInputRequestTypeDef(TypedDict):
    assetIdentifier: str
    domainIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[FilterStatusType]

class ListAssetRevisionsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListDataProductRevisionsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListDataSourceRunActivitiesInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[DataAssetActivityStatusType]

class ListDataSourceRunsInputRequestTypeDef(TypedDict):
    dataSourceIdentifier: str
    domainIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[DataSourceRunStatusType]

ListDataSourcesInputRequestTypeDef = TypedDict(
    "ListDataSourcesInputRequestTypeDef",
    {
        "domainIdentifier": str,
        "projectIdentifier": str,
        "environmentIdentifier": NotRequired[str],
        "maxResults": NotRequired[int],
        "name": NotRequired[str],
        "nextToken": NotRequired[str],
        "status": NotRequired[DataSourceStatusType],
        "type": NotRequired[str],
    },
)

class ListDomainUnitsForParentInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    parentDomainUnitIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListDomainsInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[DomainStatusType]

class ListEntityOwnersInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: Literal["DOMAIN_UNIT"]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListEnvironmentActionsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListEnvironmentBlueprintConfigurationsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListEnvironmentBlueprintsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    managed: NotRequired[bool]
    maxResults: NotRequired[int]
    name: NotRequired[str]
    nextToken: NotRequired[str]

class ListEnvironmentProfilesInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    awsAccountId: NotRequired[str]
    awsAccountRegion: NotRequired[str]
    environmentBlueprintIdentifier: NotRequired[str]
    maxResults: NotRequired[int]
    name: NotRequired[str]
    nextToken: NotRequired[str]
    projectIdentifier: NotRequired[str]

class ListEnvironmentsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    projectIdentifier: str
    awsAccountId: NotRequired[str]
    awsAccountRegion: NotRequired[str]
    environmentBlueprintIdentifier: NotRequired[str]
    environmentProfileIdentifier: NotRequired[str]
    maxResults: NotRequired[int]
    name: NotRequired[str]
    nextToken: NotRequired[str]
    provider: NotRequired[str]
    status: NotRequired[EnvironmentStatusType]

ListMetadataGenerationRunsInputRequestTypeDef = TypedDict(
    "ListMetadataGenerationRunsInputRequestTypeDef",
    {
        "domainIdentifier": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "status": NotRequired[MetadataGenerationRunStatusType],
        "type": NotRequired[Literal["BUSINESS_DESCRIPTIONS"]],
    },
)

class ListPolicyGrantsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TargetEntityTypeType
    policyType: ManagedPolicyTypeType
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListProjectMembershipsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    projectIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["NAME"]]
    sortOrder: NotRequired[SortOrderType]

class ListProjectsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    groupIdentifier: NotRequired[str]
    maxResults: NotRequired[int]
    name: NotRequired[str]
    nextToken: NotRequired[str]
    userIdentifier: NotRequired[str]

class ListSubscriptionGrantsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    owningProjectId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    subscribedListingId: NotRequired[str]
    subscriptionId: NotRequired[str]
    subscriptionTargetId: NotRequired[str]

class ListSubscriptionRequestsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    approverProjectId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    owningProjectId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    status: NotRequired[SubscriptionRequestStatusType]
    subscribedListingId: NotRequired[str]

class ListSubscriptionTargetsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]

class ListSubscriptionsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    approverProjectId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    owningProjectId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    status: NotRequired[SubscriptionStatusType]
    subscribedListingId: NotRequired[str]
    subscriptionRequestIdentifier: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class UserDetailsTypeDef(TypedDict):
    userId: str

class NotEqualToExpressionTypeDef(TypedDict):
    columnName: str
    value: str

class NotInExpressionOutputTypeDef(TypedDict):
    columnName: str
    values: List[str]

class NotInExpressionTypeDef(TypedDict):
    columnName: str
    values: Sequence[str]

class NotLikeExpressionTypeDef(TypedDict):
    columnName: str
    value: str

NotificationResourceTypeDef = TypedDict(
    "NotificationResourceTypeDef",
    {
        "id": str,
        "type": Literal["PROJECT"],
        "name": NotRequired[str],
    },
)

class OverrideDomainUnitOwnersPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]

class OverrideProjectOwnersPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]

class OwnerGroupPropertiesOutputTypeDef(TypedDict):
    groupId: NotRequired[str]

class OwnerGroupPropertiesTypeDef(TypedDict):
    groupIdentifier: str

class OwnerUserPropertiesOutputTypeDef(TypedDict):
    userId: NotRequired[str]

class OwnerUserPropertiesTypeDef(TypedDict):
    userIdentifier: str

class UserPolicyGrantPrincipalOutputTypeDef(TypedDict):
    allUsersGrantFilter: NotRequired[Dict[str, Any]]
    userIdentifier: NotRequired[str]

class RedshiftClusterStorageTypeDef(TypedDict):
    clusterName: str

class RedshiftCredentialConfigurationTypeDef(TypedDict):
    secretManagerArn: str

class RedshiftServerlessStorageTypeDef(TypedDict):
    workgroupName: str

class RejectChoiceTypeDef(TypedDict):
    predictionTarget: str
    predictionChoices: NotRequired[Sequence[int]]

class RejectRuleTypeDef(TypedDict):
    rule: NotRequired[RejectRuleBehaviorType]
    threshold: NotRequired[float]

class RejectSubscriptionRequestInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    decisionComment: NotRequired[str]

class RevokeSubscriptionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    retainPermissions: NotRequired[bool]

class SearchGroupProfilesInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    groupType: GroupSearchTypeType
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    searchText: NotRequired[str]

class SearchInItemTypeDef(TypedDict):
    attribute: str

class SearchSortTypeDef(TypedDict):
    attribute: str
    order: NotRequired[SortOrderType]

class SearchUserProfilesInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    userType: UserSearchTypeType
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    searchText: NotRequired[str]

class SsoUserProfileDetailsTypeDef(TypedDict):
    firstName: NotRequired[str]
    lastName: NotRequired[str]
    username: NotRequired[str]

class StartDataSourceRunInputRequestTypeDef(TypedDict):
    dataSourceIdentifier: str
    domainIdentifier: str
    clientToken: NotRequired[str]

class SubscribedProjectInputTypeDef(TypedDict):
    identifier: NotRequired[str]

SubscribedProjectTypeDef = TypedDict(
    "SubscribedProjectTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateDomainUnitInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    description: NotRequired[str]
    name: NotRequired[str]

class UpdateEnvironmentInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    description: NotRequired[str]
    glossaryTerms: NotRequired[Sequence[str]]
    name: NotRequired[str]

class UpdateGlossaryInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    name: NotRequired[str]
    status: NotRequired[GlossaryStatusType]

class UpdateGroupProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    groupIdentifier: str
    status: GroupProfileStatusType

class UpdateProjectInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    description: NotRequired[str]
    glossaryTerms: NotRequired[Sequence[str]]
    name: NotRequired[str]

class UpdateSubscriptionRequestInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    requestReason: str

UpdateUserProfileInputRequestTypeDef = TypedDict(
    "UpdateUserProfileInputRequestTypeDef",
    {
        "domainIdentifier": str,
        "status": UserProfileStatusType,
        "userIdentifier": str,
        "type": NotRequired[UserProfileTypeType],
    },
)

class UserPolicyGrantPrincipalTypeDef(TypedDict):
    allUsersGrantFilter: NotRequired[Mapping[str, Any]]
    userIdentifier: NotRequired[str]

class AcceptPredictionsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    acceptChoices: NotRequired[Sequence[AcceptChoiceTypeDef]]
    acceptRule: NotRequired[AcceptRuleTypeDef]
    clientToken: NotRequired[str]
    revision: NotRequired[str]

class AcceptPredictionsOutputTypeDef(TypedDict):
    assetId: str
    domainId: str
    revision: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFormTypeOutputTypeDef(TypedDict):
    description: str
    domainId: str
    name: str
    originDomainId: str
    originProjectId: str
    owningProjectId: str
    revision: str
    ResponseMetadata: ResponseMetadataTypeDef

CreateGlossaryOutputTypeDef = TypedDict(
    "CreateGlossaryOutputTypeDef",
    {
        "description": str,
        "domainId": str,
        "id": str,
        "name": str,
        "owningProjectId": str,
        "status": GlossaryStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateGroupProfileOutputTypeDef = TypedDict(
    "CreateGroupProfileOutputTypeDef",
    {
        "domainId": str,
        "groupName": str,
        "id": str,
        "status": GroupProfileStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateListingChangeSetOutputTypeDef(TypedDict):
    listingId: str
    listingRevision: str
    status: ListingStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDomainOutputTypeDef(TypedDict):
    status: DomainStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetEnvironmentCredentialsOutputTypeDef(TypedDict):
    accessKeyId: str
    expiration: datetime
    secretAccessKey: str
    sessionToken: str
    ResponseMetadata: ResponseMetadataTypeDef

GetGlossaryOutputTypeDef = TypedDict(
    "GetGlossaryOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "id": str,
        "name": str,
        "owningProjectId": str,
        "status": GlossaryStatusType,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetGroupProfileOutputTypeDef = TypedDict(
    "GetGroupProfileOutputTypeDef",
    {
        "domainId": str,
        "groupName": str,
        "id": str,
        "status": GroupProfileStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class GetIamPortalLoginUrlOutputTypeDef(TypedDict):
    authCodeUrl: str
    userProfileId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class RejectPredictionsOutputTypeDef(TypedDict):
    assetId: str
    assetRevision: str
    domainId: str
    ResponseMetadata: ResponseMetadataTypeDef

StartMetadataGenerationRunOutputTypeDef = TypedDict(
    "StartMetadataGenerationRunOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "id": str,
        "owningProjectId": str,
        "status": MetadataGenerationRunStatusType,
        "type": Literal["BUSINESS_DESCRIPTIONS"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateGlossaryOutputTypeDef = TypedDict(
    "UpdateGlossaryOutputTypeDef",
    {
        "description": str,
        "domainId": str,
        "id": str,
        "name": str,
        "owningProjectId": str,
        "status": GlossaryStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateGroupProfileOutputTypeDef = TypedDict(
    "UpdateGroupProfileOutputTypeDef",
    {
        "domainId": str,
        "groupName": str,
        "id": str,
        "status": GroupProfileStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class AcceptSubscriptionRequestInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    assetScopes: NotRequired[Sequence[AcceptedAssetScopeTypeDef]]
    decisionComment: NotRequired[str]

class ActionParametersTypeDef(TypedDict):
    awsConsoleLink: NotRequired[AwsConsoleLinkParametersTypeDef]

class ListAssetFiltersOutputTypeDef(TypedDict):
    items: List[AssetFilterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class AssetItemAdditionalAttributesTypeDef(TypedDict):
    formsOutput: NotRequired[List[FormOutputTypeDef]]
    latestTimeSeriesDataPointFormsOutput: NotRequired[
        List[TimeSeriesDataPointSummaryFormOutputTypeDef]
    ]
    readOnlyFormsOutput: NotRequired[List[FormOutputTypeDef]]

class AssetListingItemAdditionalAttributesTypeDef(TypedDict):
    forms: NotRequired[str]
    latestTimeSeriesDataPointForms: NotRequired[List[TimeSeriesDataPointSummaryFormOutputTypeDef]]

class ListTimeSeriesDataPointsOutputTypeDef(TypedDict):
    items: List[TimeSeriesDataPointSummaryFormOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

GetAssetOutputTypeDef = TypedDict(
    "GetAssetOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "externalIdentifier": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "formsOutput": List[FormOutputTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "latestTimeSeriesDataPointFormsOutput": List[TimeSeriesDataPointSummaryFormOutputTypeDef],
        "listing": AssetListingDetailsTypeDef,
        "name": str,
        "owningProjectId": str,
        "readOnlyFormsOutput": List[FormOutputTypeDef],
        "revision": str,
        "typeIdentifier": str,
        "typeRevision": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class AssetListingTypeDef(TypedDict):
    assetId: NotRequired[str]
    assetRevision: NotRequired[str]
    assetType: NotRequired[str]
    createdAt: NotRequired[datetime]
    forms: NotRequired[str]
    glossaryTerms: NotRequired[List[DetailedGlossaryTermTypeDef]]
    latestTimeSeriesDataPointForms: NotRequired[List[TimeSeriesDataPointSummaryFormOutputTypeDef]]
    owningProjectId: NotRequired[str]

class ListingSummaryItemTypeDef(TypedDict):
    glossaryTerms: NotRequired[List[DetailedGlossaryTermTypeDef]]
    listingId: NotRequired[str]
    listingRevision: NotRequired[str]

class ListingSummaryTypeDef(TypedDict):
    glossaryTerms: NotRequired[List[DetailedGlossaryTermTypeDef]]
    listingId: NotRequired[str]
    listingRevision: NotRequired[str]

class SubscribedProductListingTypeDef(TypedDict):
    assetListings: NotRequired[List[AssetInDataProductListingItemTypeDef]]
    description: NotRequired[str]
    entityId: NotRequired[str]
    entityRevision: NotRequired[str]
    glossaryTerms: NotRequired[List[DetailedGlossaryTermTypeDef]]
    name: NotRequired[str]

class ListAssetRevisionsOutputTypeDef(TypedDict):
    items: List[AssetRevisionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SubscribedAssetListingTypeDef(TypedDict):
    assetScope: NotRequired[AssetScopeTypeDef]
    entityId: NotRequired[str]
    entityRevision: NotRequired[str]
    entityType: NotRequired[str]
    forms: NotRequired[str]
    glossaryTerms: NotRequired[List[DetailedGlossaryTermTypeDef]]

class AssetTypeItemTypeDef(TypedDict):
    domainId: str
    formsOutput: Dict[str, FormEntryOutputTypeDef]
    name: str
    owningProjectId: str
    revision: str
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    description: NotRequired[str]
    originDomainId: NotRequired[str]
    originProjectId: NotRequired[str]
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]

class CreateAssetTypeOutputTypeDef(TypedDict):
    createdAt: datetime
    createdBy: str
    description: str
    domainId: str
    formsOutput: Dict[str, FormEntryOutputTypeDef]
    name: str
    originDomainId: str
    originProjectId: str
    owningProjectId: str
    revision: str
    updatedAt: datetime
    updatedBy: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetAssetTypeOutputTypeDef(TypedDict):
    createdAt: datetime
    createdBy: str
    description: str
    domainId: str
    formsOutput: Dict[str, FormEntryOutputTypeDef]
    name: str
    originDomainId: str
    originProjectId: str
    owningProjectId: str
    revision: str
    updatedAt: datetime
    updatedBy: str
    ResponseMetadata: ResponseMetadataTypeDef

class LineageNodeTypeItemTypeDef(TypedDict):
    domainId: str
    formsOutput: Dict[str, FormEntryOutputTypeDef]
    revision: str
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    description: NotRequired[str]
    name: NotRequired[str]
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]

class PostLineageEventInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    event: BlobTypeDef
    clientToken: NotRequired[str]

class PredictionConfigurationTypeDef(TypedDict):
    businessNameGeneration: NotRequired[BusinessNameGenerationConfigurationTypeDef]

class ProvisioningPropertiesTypeDef(TypedDict):
    cloudFormation: NotRequired[CloudFormationPropertiesTypeDef]

ColumnFilterConfigurationUnionTypeDef = Union[
    ColumnFilterConfigurationTypeDef, ColumnFilterConfigurationOutputTypeDef
]
ConfigurableEnvironmentActionTypeDef = TypedDict(
    "ConfigurableEnvironmentActionTypeDef",
    {
        "parameters": List[ConfigurableActionParameterTypeDef],
        "type": str,
        "auth": NotRequired[ConfigurableActionTypeAuthorizationType],
    },
)

class CreateAssetTypeInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    formsInput: Mapping[str, FormEntryInputTypeDef]
    name: str
    owningProjectIdentifier: str
    description: NotRequired[str]

CreateDataProductOutputTypeDef = TypedDict(
    "CreateDataProductOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "formsOutput": List[FormOutputTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "items": List[DataProductItemOutputTypeDef],
        "name": str,
        "owningProjectId": str,
        "revision": str,
        "status": DataProductStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateDataProductRevisionOutputTypeDef = TypedDict(
    "CreateDataProductRevisionOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "formsOutput": List[FormOutputTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "items": List[DataProductItemOutputTypeDef],
        "name": str,
        "owningProjectId": str,
        "revision": str,
        "status": DataProductStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDataProductOutputTypeDef = TypedDict(
    "GetDataProductOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "formsOutput": List[FormOutputTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "items": List[DataProductItemOutputTypeDef],
        "name": str,
        "owningProjectId": str,
        "revision": str,
        "status": DataProductStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateDataProductRevisionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    formsInput: NotRequired[Sequence[FormInputTypeDef]]
    glossaryTerms: NotRequired[Sequence[str]]
    items: NotRequired[Sequence[DataProductItemTypeDef]]

DataProductItemUnionTypeDef = Union[DataProductItemTypeDef, DataProductItemOutputTypeDef]

class DataSourceRunActivityTypeDef(TypedDict):
    createdAt: datetime
    dataAssetStatus: DataAssetActivityStatusType
    dataSourceRunId: str
    database: str
    projectId: str
    technicalName: str
    updatedAt: datetime
    dataAssetId: NotRequired[str]
    errorMessage: NotRequired[DataSourceErrorMessageTypeDef]
    technicalDescription: NotRequired[str]

DataSourceSummaryTypeDef = TypedDict(
    "DataSourceSummaryTypeDef",
    {
        "dataSourceId": str,
        "domainId": str,
        "environmentId": str,
        "name": str,
        "status": DataSourceStatusType,
        "type": str,
        "createdAt": NotRequired[datetime],
        "enableSetting": NotRequired[EnableSettingType],
        "lastRunAssetCount": NotRequired[int],
        "lastRunAt": NotRequired[datetime],
        "lastRunErrorMessage": NotRequired[DataSourceErrorMessageTypeDef],
        "lastRunStatus": NotRequired[DataSourceRunStatusType],
        "schedule": NotRequired[ScheduleConfigurationTypeDef],
        "updatedAt": NotRequired[datetime],
    },
)

class CreateDomainInputRequestTypeDef(TypedDict):
    domainExecutionRole: str
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    kmsKeyIdentifier: NotRequired[str]
    singleSignOn: NotRequired[SingleSignOnTypeDef]
    tags: NotRequired[Mapping[str, str]]

CreateDomainOutputTypeDef = TypedDict(
    "CreateDomainOutputTypeDef",
    {
        "arn": str,
        "description": str,
        "domainExecutionRole": str,
        "id": str,
        "kmsKeyIdentifier": str,
        "name": str,
        "portalUrl": str,
        "rootDomainUnitId": str,
        "singleSignOn": SingleSignOnTypeDef,
        "status": DomainStatusType,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDomainOutputTypeDef = TypedDict(
    "GetDomainOutputTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "description": str,
        "domainExecutionRole": str,
        "id": str,
        "kmsKeyIdentifier": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "portalUrl": str,
        "rootDomainUnitId": str,
        "singleSignOn": SingleSignOnTypeDef,
        "status": DomainStatusType,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class UpdateDomainInputRequestTypeDef(TypedDict):
    identifier: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    domainExecutionRole: NotRequired[str]
    name: NotRequired[str]
    singleSignOn: NotRequired[SingleSignOnTypeDef]

UpdateDomainOutputTypeDef = TypedDict(
    "UpdateDomainOutputTypeDef",
    {
        "description": str,
        "domainExecutionRole": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "rootDomainUnitId": str,
        "singleSignOn": SingleSignOnTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateEnvironmentInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentProfileIdentifier: str
    name: str
    projectIdentifier: str
    description: NotRequired[str]
    environmentAccountIdentifier: NotRequired[str]
    environmentAccountRegion: NotRequired[str]
    environmentBlueprintIdentifier: NotRequired[str]
    glossaryTerms: NotRequired[Sequence[str]]
    userParameters: NotRequired[Sequence[EnvironmentParameterTypeDef]]

class CreateEnvironmentProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentBlueprintIdentifier: str
    name: str
    projectIdentifier: str
    awsAccountId: NotRequired[str]
    awsAccountRegion: NotRequired[str]
    description: NotRequired[str]
    userParameters: NotRequired[Sequence[EnvironmentParameterTypeDef]]

class UpdateEnvironmentProfileInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    awsAccountId: NotRequired[str]
    awsAccountRegion: NotRequired[str]
    description: NotRequired[str]
    name: NotRequired[str]
    userParameters: NotRequired[Sequence[EnvironmentParameterTypeDef]]

CreateEnvironmentProfileOutputTypeDef = TypedDict(
    "CreateEnvironmentProfileOutputTypeDef",
    {
        "awsAccountId": str,
        "awsAccountRegion": str,
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "environmentBlueprintId": str,
        "id": str,
        "name": str,
        "projectId": str,
        "updatedAt": datetime,
        "userParameters": List[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetEnvironmentProfileOutputTypeDef = TypedDict(
    "GetEnvironmentProfileOutputTypeDef",
    {
        "awsAccountId": str,
        "awsAccountRegion": str,
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "environmentBlueprintId": str,
        "id": str,
        "name": str,
        "projectId": str,
        "updatedAt": datetime,
        "userParameters": List[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateEnvironmentProfileOutputTypeDef = TypedDict(
    "UpdateEnvironmentProfileOutputTypeDef",
    {
        "awsAccountId": str,
        "awsAccountRegion": str,
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "environmentBlueprintId": str,
        "id": str,
        "name": str,
        "projectId": str,
        "updatedAt": datetime,
        "userParameters": List[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateFormTypeInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    model: ModelTypeDef
    name: str
    owningProjectIdentifier: str
    description: NotRequired[str]
    status: NotRequired[FormTypeStatusType]

class CreateGlossaryTermInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    glossaryIdentifier: str
    name: str
    clientToken: NotRequired[str]
    longDescription: NotRequired[str]
    shortDescription: NotRequired[str]
    status: NotRequired[GlossaryTermStatusType]
    termRelations: NotRequired[TermRelationsTypeDef]

class UpdateGlossaryTermInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    glossaryIdentifier: NotRequired[str]
    longDescription: NotRequired[str]
    name: NotRequired[str]
    shortDescription: NotRequired[str]
    status: NotRequired[GlossaryTermStatusType]
    termRelations: NotRequired[TermRelationsTypeDef]

CreateGlossaryTermOutputTypeDef = TypedDict(
    "CreateGlossaryTermOutputTypeDef",
    {
        "domainId": str,
        "glossaryId": str,
        "id": str,
        "longDescription": str,
        "name": str,
        "shortDescription": str,
        "status": GlossaryTermStatusType,
        "termRelations": TermRelationsOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetGlossaryTermOutputTypeDef = TypedDict(
    "GetGlossaryTermOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "glossaryId": str,
        "id": str,
        "longDescription": str,
        "name": str,
        "shortDescription": str,
        "status": GlossaryTermStatusType,
        "termRelations": TermRelationsOutputTypeDef,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GlossaryTermItemTypeDef = TypedDict(
    "GlossaryTermItemTypeDef",
    {
        "domainId": str,
        "glossaryId": str,
        "id": str,
        "name": str,
        "status": GlossaryTermStatusType,
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "longDescription": NotRequired[str],
        "shortDescription": NotRequired[str],
        "termRelations": NotRequired[TermRelationsOutputTypeDef],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)
UpdateGlossaryTermOutputTypeDef = TypedDict(
    "UpdateGlossaryTermOutputTypeDef",
    {
        "domainId": str,
        "glossaryId": str,
        "id": str,
        "longDescription": str,
        "name": str,
        "shortDescription": str,
        "status": GlossaryTermStatusType,
        "termRelations": TermRelationsOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateProjectMembershipInputRequestTypeDef(TypedDict):
    designation: UserDesignationType
    domainIdentifier: str
    member: MemberTypeDef
    projectIdentifier: str

class DeleteProjectMembershipInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    member: MemberTypeDef
    projectIdentifier: str

CreateProjectOutputTypeDef = TypedDict(
    "CreateProjectOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "domainUnitId": str,
        "failureReasons": List[ProjectDeletionErrorTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "projectStatus": ProjectStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetProjectOutputTypeDef = TypedDict(
    "GetProjectOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "domainUnitId": str,
        "failureReasons": List[ProjectDeletionErrorTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "projectStatus": ProjectStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ProjectSummaryTypeDef = TypedDict(
    "ProjectSummaryTypeDef",
    {
        "createdBy": str,
        "domainId": str,
        "id": str,
        "name": str,
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "domainUnitId": NotRequired[str],
        "failureReasons": NotRequired[List[ProjectDeletionErrorTypeDef]],
        "projectStatus": NotRequired[ProjectStatusType],
        "updatedAt": NotRequired[datetime],
    },
)
UpdateProjectOutputTypeDef = TypedDict(
    "UpdateProjectOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "domainUnitId": str,
        "failureReasons": List[ProjectDeletionErrorTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "projectStatus": ProjectStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateSubscriptionTargetInputRequestTypeDef = TypedDict(
    "CreateSubscriptionTargetInputRequestTypeDef",
    {
        "applicableAssetTypes": Sequence[str],
        "authorizedPrincipals": Sequence[str],
        "domainIdentifier": str,
        "environmentIdentifier": str,
        "manageAccessRole": str,
        "name": str,
        "subscriptionTargetConfig": Sequence[SubscriptionTargetFormTypeDef],
        "type": str,
        "clientToken": NotRequired[str],
        "provider": NotRequired[str],
    },
)
CreateSubscriptionTargetOutputTypeDef = TypedDict(
    "CreateSubscriptionTargetOutputTypeDef",
    {
        "applicableAssetTypes": List[str],
        "authorizedPrincipals": List[str],
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "environmentId": str,
        "id": str,
        "manageAccessRole": str,
        "name": str,
        "projectId": str,
        "provider": str,
        "subscriptionTargetConfig": List[SubscriptionTargetFormTypeDef],
        "type": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSubscriptionTargetOutputTypeDef = TypedDict(
    "GetSubscriptionTargetOutputTypeDef",
    {
        "applicableAssetTypes": List[str],
        "authorizedPrincipals": List[str],
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "environmentId": str,
        "id": str,
        "manageAccessRole": str,
        "name": str,
        "projectId": str,
        "provider": str,
        "subscriptionTargetConfig": List[SubscriptionTargetFormTypeDef],
        "type": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SubscriptionTargetSummaryTypeDef = TypedDict(
    "SubscriptionTargetSummaryTypeDef",
    {
        "applicableAssetTypes": List[str],
        "authorizedPrincipals": List[str],
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "environmentId": str,
        "id": str,
        "manageAccessRole": str,
        "name": str,
        "projectId": str,
        "provider": str,
        "subscriptionTargetConfig": List[SubscriptionTargetFormTypeDef],
        "type": str,
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)

class UpdateSubscriptionTargetInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str
    applicableAssetTypes: NotRequired[Sequence[str]]
    authorizedPrincipals: NotRequired[Sequence[str]]
    manageAccessRole: NotRequired[str]
    name: NotRequired[str]
    provider: NotRequired[str]
    subscriptionTargetConfig: NotRequired[Sequence[SubscriptionTargetFormTypeDef]]

UpdateSubscriptionTargetOutputTypeDef = TypedDict(
    "UpdateSubscriptionTargetOutputTypeDef",
    {
        "applicableAssetTypes": List[str],
        "authorizedPrincipals": List[str],
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "environmentId": str,
        "id": str,
        "manageAccessRole": str,
        "name": str,
        "projectId": str,
        "provider": str,
        "subscriptionTargetConfig": List[SubscriptionTargetFormTypeDef],
        "type": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ListDataProductRevisionsOutputTypeDef(TypedDict):
    items: List[DataProductRevisionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

DataSourceRunSummaryTypeDef = TypedDict(
    "DataSourceRunSummaryTypeDef",
    {
        "createdAt": datetime,
        "dataSourceId": str,
        "id": str,
        "projectId": str,
        "status": DataSourceRunStatusType,
        "type": DataSourceRunTypeType,
        "updatedAt": datetime,
        "errorMessage": NotRequired[DataSourceErrorMessageTypeDef],
        "runStatisticsForAssets": NotRequired[RunStatisticsForAssetsTypeDef],
        "startedAt": NotRequired[datetime],
        "stoppedAt": NotRequired[datetime],
    },
)
GetDataSourceRunOutputTypeDef = TypedDict(
    "GetDataSourceRunOutputTypeDef",
    {
        "createdAt": datetime,
        "dataSourceConfigurationSnapshot": str,
        "dataSourceId": str,
        "domainId": str,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "id": str,
        "projectId": str,
        "runStatisticsForAssets": RunStatisticsForAssetsTypeDef,
        "startedAt": datetime,
        "status": DataSourceRunStatusType,
        "stoppedAt": datetime,
        "type": DataSourceRunTypeType,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartDataSourceRunOutputTypeDef = TypedDict(
    "StartDataSourceRunOutputTypeDef",
    {
        "createdAt": datetime,
        "dataSourceConfigurationSnapshot": str,
        "dataSourceId": str,
        "domainId": str,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "id": str,
        "projectId": str,
        "runStatisticsForAssets": RunStatisticsForAssetsTypeDef,
        "startedAt": datetime,
        "status": DataSourceRunStatusType,
        "stoppedAt": datetime,
        "type": DataSourceRunTypeType,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class DeploymentTypeDef(TypedDict):
    deploymentId: NotRequired[str]
    deploymentStatus: NotRequired[DeploymentStatusType]
    deploymentType: NotRequired[DeploymentTypeType]
    failureReason: NotRequired[EnvironmentErrorTypeDef]
    isDeploymentComplete: NotRequired[bool]
    messages: NotRequired[List[str]]

class ListDomainsOutputTypeDef(TypedDict):
    items: List[DomainSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ProjectGrantFilterTypeDef(TypedDict):
    domainUnitFilter: NotRequired[DomainUnitFilterForProjectTypeDef]

class DomainUnitPolicyGrantPrincipalOutputTypeDef(TypedDict):
    domainUnitDesignation: Literal["OWNER"]
    domainUnitGrantFilter: NotRequired[DomainUnitGrantFilterOutputTypeDef]
    domainUnitIdentifier: NotRequired[str]

DomainUnitGrantFilterUnionTypeDef = Union[
    DomainUnitGrantFilterTypeDef, DomainUnitGrantFilterOutputTypeDef
]

class DomainUnitOwnerPropertiesTypeDef(TypedDict):
    group: NotRequired[DomainUnitGroupPropertiesTypeDef]
    user: NotRequired[DomainUnitUserPropertiesTypeDef]

class ListDomainUnitsForParentOutputTypeDef(TypedDict):
    items: List[DomainUnitSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListEnvironmentProfilesOutputTypeDef(TypedDict):
    items: List[EnvironmentProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListEnvironmentsOutputTypeDef(TypedDict):
    items: List[EnvironmentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SubscribedAssetTypeDef(TypedDict):
    assetId: str
    assetRevision: str
    status: SubscriptionGrantStatusType
    assetScope: NotRequired[AssetScopeTypeDef]
    failureCause: NotRequired[FailureCauseTypeDef]
    failureTimestamp: NotRequired[datetime]
    grantedTimestamp: NotRequired[datetime]
    targetName: NotRequired[str]

class UpdateSubscriptionGrantStatusInputRequestTypeDef(TypedDict):
    assetIdentifier: str
    domainIdentifier: str
    identifier: str
    status: SubscriptionGrantStatusType
    failureCause: NotRequired[FailureCauseTypeDef]
    targetName: NotRequired[str]

FilterClausePaginatorTypeDef = TypedDict(
    "FilterClausePaginatorTypeDef",
    {
        "and": NotRequired[Sequence[Mapping[str, Any]]],
        "filter": NotRequired[FilterTypeDef],
        "or": NotRequired[Sequence[Mapping[str, Any]]],
    },
)
FilterClauseTypeDef = TypedDict(
    "FilterClauseTypeDef",
    {
        "and": NotRequired[Sequence[Mapping[str, Any]]],
        "filter": NotRequired[FilterTypeDef],
        "or": NotRequired[Sequence[Mapping[str, Any]]],
    },
)

class RelationalFilterConfigurationOutputTypeDef(TypedDict):
    databaseName: str
    filterExpressions: NotRequired[List[FilterExpressionTypeDef]]
    schemaName: NotRequired[str]

class RelationalFilterConfigurationTypeDef(TypedDict):
    databaseName: str
    filterExpressions: NotRequired[Sequence[FilterExpressionTypeDef]]
    schemaName: NotRequired[str]

class FormTypeDataTypeDef(TypedDict):
    domainId: str
    name: str
    revision: str
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    description: NotRequired[str]
    imports: NotRequired[List[ImportTypeDef]]
    model: NotRequired[ModelTypeDef]
    originDomainId: NotRequired[str]
    originProjectId: NotRequired[str]
    owningProjectId: NotRequired[str]
    status: NotRequired[FormTypeStatusType]

class GetFormTypeOutputTypeDef(TypedDict):
    createdAt: datetime
    createdBy: str
    description: str
    domainId: str
    imports: List[ImportTypeDef]
    model: ModelTypeDef
    name: str
    originDomainId: str
    originProjectId: str
    owningProjectId: str
    revision: str
    status: FormTypeStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class GetLineageNodeInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    eventTimestamp: NotRequired[TimestampTypeDef]

class ListLineageNodeHistoryInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    direction: NotRequired[EdgeDirectionType]
    eventTimestampGTE: NotRequired[TimestampTypeDef]
    eventTimestampLTE: NotRequired[TimestampTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortOrder: NotRequired[SortOrderType]

ListNotificationsInputRequestTypeDef = TypedDict(
    "ListNotificationsInputRequestTypeDef",
    {
        "domainIdentifier": str,
        "type": NotificationTypeType,
        "afterTimestamp": NotRequired[TimestampTypeDef],
        "beforeTimestamp": NotRequired[TimestampTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "subjects": NotRequired[Sequence[str]],
        "taskStatus": NotRequired[TaskStatusType],
    },
)

class ListTimeSeriesDataPointsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TimeSeriesEntityTypeType
    formName: str
    endedAt: NotRequired[TimestampTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    startedAt: NotRequired[TimestampTypeDef]

class TimeSeriesDataPointFormInputTypeDef(TypedDict):
    formName: str
    timestamp: TimestampTypeDef
    typeIdentifier: str
    content: NotRequired[str]
    typeRevision: NotRequired[str]

GetLineageNodeOutputTypeDef = TypedDict(
    "GetLineageNodeOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "downstreamNodes": List[LineageNodeReferenceTypeDef],
        "eventTimestamp": datetime,
        "formsOutput": List[FormOutputTypeDef],
        "id": str,
        "name": str,
        "sourceIdentifier": str,
        "typeName": str,
        "typeRevision": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "upstreamNodes": List[LineageNodeReferenceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetMetadataGenerationRunOutputTypeDef = TypedDict(
    "GetMetadataGenerationRunOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "id": str,
        "owningProjectId": str,
        "status": MetadataGenerationRunStatusType,
        "target": MetadataGenerationRunTargetTypeDef,
        "type": Literal["BUSINESS_DESCRIPTIONS"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
MetadataGenerationRunItemTypeDef = TypedDict(
    "MetadataGenerationRunItemTypeDef",
    {
        "domainId": str,
        "id": str,
        "owningProjectId": str,
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "status": NotRequired[MetadataGenerationRunStatusType],
        "target": NotRequired[MetadataGenerationRunTargetTypeDef],
        "type": NotRequired[Literal["BUSINESS_DESCRIPTIONS"]],
    },
)
StartMetadataGenerationRunInputRequestTypeDef = TypedDict(
    "StartMetadataGenerationRunInputRequestTypeDef",
    {
        "domainIdentifier": str,
        "owningProjectIdentifier": str,
        "target": MetadataGenerationRunTargetTypeDef,
        "type": Literal["BUSINESS_DESCRIPTIONS"],
        "clientToken": NotRequired[str],
    },
)

class GetTimeSeriesDataPointOutputTypeDef(TypedDict):
    domainId: str
    entityId: str
    entityType: TimeSeriesEntityTypeType
    form: TimeSeriesDataPointFormOutputTypeDef
    formName: str
    ResponseMetadata: ResponseMetadataTypeDef

class PostTimeSeriesDataPointsOutputTypeDef(TypedDict):
    domainId: str
    entityId: str
    entityType: TimeSeriesEntityTypeType
    forms: List[TimeSeriesDataPointFormOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GlueSelfGrantStatusOutputTypeDef(TypedDict):
    selfGrantStatusDetails: List[SelfGrantStatusDetailTypeDef]

class RedshiftSelfGrantStatusOutputTypeDef(TypedDict):
    selfGrantStatusDetails: List[SelfGrantStatusDetailTypeDef]

class GrantedEntityInputTypeDef(TypedDict):
    listing: NotRequired[ListingRevisionInputTypeDef]

class GrantedEntityTypeDef(TypedDict):
    listing: NotRequired[ListingRevisionTypeDef]

class SearchGroupProfilesOutputTypeDef(TypedDict):
    items: List[GroupProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

InExpressionUnionTypeDef = Union[InExpressionTypeDef, InExpressionOutputTypeDef]

class ProvisioningConfigurationOutputTypeDef(TypedDict):
    lakeFormationConfiguration: NotRequired[LakeFormationConfigurationOutputTypeDef]

LakeFormationConfigurationUnionTypeDef = Union[
    LakeFormationConfigurationTypeDef, LakeFormationConfigurationOutputTypeDef
]

class ListLineageNodeHistoryOutputTypeDef(TypedDict):
    nodes: List[LineageNodeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAssetFiltersInputListAssetFiltersPaginateTypeDef(TypedDict):
    assetIdentifier: str
    domainIdentifier: str
    status: NotRequired[FilterStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAssetRevisionsInputListAssetRevisionsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDataProductRevisionsInputListDataProductRevisionsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDataSourceRunActivitiesInputListDataSourceRunActivitiesPaginateTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    status: NotRequired[DataAssetActivityStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDataSourceRunsInputListDataSourceRunsPaginateTypeDef(TypedDict):
    dataSourceIdentifier: str
    domainIdentifier: str
    status: NotRequired[DataSourceRunStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListDataSourcesInputListDataSourcesPaginateTypeDef = TypedDict(
    "ListDataSourcesInputListDataSourcesPaginateTypeDef",
    {
        "domainIdentifier": str,
        "projectIdentifier": str,
        "environmentIdentifier": NotRequired[str],
        "name": NotRequired[str],
        "status": NotRequired[DataSourceStatusType],
        "type": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListDomainUnitsForParentInputListDomainUnitsForParentPaginateTypeDef(TypedDict):
    domainIdentifier: str
    parentDomainUnitIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDomainsInputListDomainsPaginateTypeDef(TypedDict):
    status: NotRequired[DomainStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEntityOwnersInputListEntityOwnersPaginateTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: Literal["DOMAIN_UNIT"]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentActionsInputListEnvironmentActionsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentBlueprintConfigurationsInputListEnvironmentBlueprintConfigurationsPaginateTypeDef(
    TypedDict
):
    domainIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentBlueprintsInputListEnvironmentBlueprintsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    managed: NotRequired[bool]
    name: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentProfilesInputListEnvironmentProfilesPaginateTypeDef(TypedDict):
    domainIdentifier: str
    awsAccountId: NotRequired[str]
    awsAccountRegion: NotRequired[str]
    environmentBlueprintIdentifier: NotRequired[str]
    name: NotRequired[str]
    projectIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentsInputListEnvironmentsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    projectIdentifier: str
    awsAccountId: NotRequired[str]
    awsAccountRegion: NotRequired[str]
    environmentBlueprintIdentifier: NotRequired[str]
    environmentProfileIdentifier: NotRequired[str]
    name: NotRequired[str]
    provider: NotRequired[str]
    status: NotRequired[EnvironmentStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLineageNodeHistoryInputListLineageNodeHistoryPaginateTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    direction: NotRequired[EdgeDirectionType]
    eventTimestampGTE: NotRequired[TimestampTypeDef]
    eventTimestampLTE: NotRequired[TimestampTypeDef]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListMetadataGenerationRunsInputListMetadataGenerationRunsPaginateTypeDef = TypedDict(
    "ListMetadataGenerationRunsInputListMetadataGenerationRunsPaginateTypeDef",
    {
        "domainIdentifier": str,
        "status": NotRequired[MetadataGenerationRunStatusType],
        "type": NotRequired[Literal["BUSINESS_DESCRIPTIONS"]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListNotificationsInputListNotificationsPaginateTypeDef = TypedDict(
    "ListNotificationsInputListNotificationsPaginateTypeDef",
    {
        "domainIdentifier": str,
        "type": NotificationTypeType,
        "afterTimestamp": NotRequired[TimestampTypeDef],
        "beforeTimestamp": NotRequired[TimestampTypeDef],
        "subjects": NotRequired[Sequence[str]],
        "taskStatus": NotRequired[TaskStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListPolicyGrantsInputListPolicyGrantsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TargetEntityTypeType
    policyType: ManagedPolicyTypeType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProjectMembershipsInputListProjectMembershipsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    projectIdentifier: str
    sortBy: NotRequired[Literal["NAME"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProjectsInputListProjectsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    groupIdentifier: NotRequired[str]
    name: NotRequired[str]
    userIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSubscriptionGrantsInputListSubscriptionGrantsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    environmentId: NotRequired[str]
    owningProjectId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    subscribedListingId: NotRequired[str]
    subscriptionId: NotRequired[str]
    subscriptionTargetId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSubscriptionRequestsInputListSubscriptionRequestsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    approverProjectId: NotRequired[str]
    owningProjectId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    status: NotRequired[SubscriptionRequestStatusType]
    subscribedListingId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSubscriptionTargetsInputListSubscriptionTargetsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSubscriptionsInputListSubscriptionsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    approverProjectId: NotRequired[str]
    owningProjectId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    status: NotRequired[SubscriptionStatusType]
    subscribedListingId: NotRequired[str]
    subscriptionRequestIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTimeSeriesDataPointsInputListTimeSeriesDataPointsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TimeSeriesEntityTypeType
    formName: str
    endedAt: NotRequired[TimestampTypeDef]
    startedAt: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchGroupProfilesInputSearchGroupProfilesPaginateTypeDef(TypedDict):
    domainIdentifier: str
    groupType: GroupSearchTypeType
    searchText: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchUserProfilesInputSearchUserProfilesPaginateTypeDef(TypedDict):
    domainIdentifier: str
    userType: UserSearchTypeType
    searchText: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class MemberDetailsTypeDef(TypedDict):
    group: NotRequired[GroupDetailsTypeDef]
    user: NotRequired[UserDetailsTypeDef]

NotInExpressionUnionTypeDef = Union[NotInExpressionTypeDef, NotInExpressionOutputTypeDef]
RowFilterExpressionOutputTypeDef = TypedDict(
    "RowFilterExpressionOutputTypeDef",
    {
        "equalTo": NotRequired[EqualToExpressionTypeDef],
        "greaterThan": NotRequired[GreaterThanExpressionTypeDef],
        "greaterThanOrEqualTo": NotRequired[GreaterThanOrEqualToExpressionTypeDef],
        "in": NotRequired[InExpressionOutputTypeDef],
        "isNotNull": NotRequired[IsNotNullExpressionTypeDef],
        "isNull": NotRequired[IsNullExpressionTypeDef],
        "lessThan": NotRequired[LessThanExpressionTypeDef],
        "lessThanOrEqualTo": NotRequired[LessThanOrEqualToExpressionTypeDef],
        "like": NotRequired[LikeExpressionTypeDef],
        "notEqualTo": NotRequired[NotEqualToExpressionTypeDef],
        "notIn": NotRequired[NotInExpressionOutputTypeDef],
        "notLike": NotRequired[NotLikeExpressionTypeDef],
    },
)

class TopicTypeDef(TypedDict):
    resource: NotificationResourceTypeDef
    role: NotificationRoleType
    subject: str

class PolicyGrantDetailOutputTypeDef(TypedDict):
    addToProjectMemberPool: NotRequired[AddToProjectMemberPoolPolicyGrantDetailTypeDef]
    createAssetType: NotRequired[CreateAssetTypePolicyGrantDetailTypeDef]
    createDomainUnit: NotRequired[CreateDomainUnitPolicyGrantDetailTypeDef]
    createEnvironment: NotRequired[Dict[str, Any]]
    createEnvironmentProfile: NotRequired[CreateEnvironmentProfilePolicyGrantDetailTypeDef]
    createFormType: NotRequired[CreateFormTypePolicyGrantDetailTypeDef]
    createGlossary: NotRequired[CreateGlossaryPolicyGrantDetailTypeDef]
    createProject: NotRequired[CreateProjectPolicyGrantDetailTypeDef]
    delegateCreateEnvironmentProfile: NotRequired[Dict[str, Any]]
    overrideDomainUnitOwners: NotRequired[OverrideDomainUnitOwnersPolicyGrantDetailTypeDef]
    overrideProjectOwners: NotRequired[OverrideProjectOwnersPolicyGrantDetailTypeDef]

class PolicyGrantDetailTypeDef(TypedDict):
    addToProjectMemberPool: NotRequired[AddToProjectMemberPoolPolicyGrantDetailTypeDef]
    createAssetType: NotRequired[CreateAssetTypePolicyGrantDetailTypeDef]
    createDomainUnit: NotRequired[CreateDomainUnitPolicyGrantDetailTypeDef]
    createEnvironment: NotRequired[Mapping[str, Any]]
    createEnvironmentProfile: NotRequired[CreateEnvironmentProfilePolicyGrantDetailTypeDef]
    createFormType: NotRequired[CreateFormTypePolicyGrantDetailTypeDef]
    createGlossary: NotRequired[CreateGlossaryPolicyGrantDetailTypeDef]
    createProject: NotRequired[CreateProjectPolicyGrantDetailTypeDef]
    delegateCreateEnvironmentProfile: NotRequired[Mapping[str, Any]]
    overrideDomainUnitOwners: NotRequired[OverrideDomainUnitOwnersPolicyGrantDetailTypeDef]
    overrideProjectOwners: NotRequired[OverrideProjectOwnersPolicyGrantDetailTypeDef]

class OwnerPropertiesOutputTypeDef(TypedDict):
    group: NotRequired[OwnerGroupPropertiesOutputTypeDef]
    user: NotRequired[OwnerUserPropertiesOutputTypeDef]

class OwnerPropertiesTypeDef(TypedDict):
    group: NotRequired[OwnerGroupPropertiesTypeDef]
    user: NotRequired[OwnerUserPropertiesTypeDef]

class RedshiftStorageTypeDef(TypedDict):
    redshiftClusterSource: NotRequired[RedshiftClusterStorageTypeDef]
    redshiftServerlessSource: NotRequired[RedshiftServerlessStorageTypeDef]

class RejectPredictionsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    clientToken: NotRequired[str]
    rejectChoices: NotRequired[Sequence[RejectChoiceTypeDef]]
    rejectRule: NotRequired[RejectRuleTypeDef]
    revision: NotRequired[str]

class UserProfileDetailsTypeDef(TypedDict):
    iam: NotRequired[IamUserProfileDetailsTypeDef]
    sso: NotRequired[SsoUserProfileDetailsTypeDef]

class SubscribedPrincipalInputTypeDef(TypedDict):
    project: NotRequired[SubscribedProjectInputTypeDef]

class SubscribedPrincipalTypeDef(TypedDict):
    project: NotRequired[SubscribedProjectTypeDef]

UserPolicyGrantPrincipalUnionTypeDef = Union[
    UserPolicyGrantPrincipalTypeDef, UserPolicyGrantPrincipalOutputTypeDef
]

class CreateEnvironmentActionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    name: str
    parameters: ActionParametersTypeDef
    description: NotRequired[str]

CreateEnvironmentActionOutputTypeDef = TypedDict(
    "CreateEnvironmentActionOutputTypeDef",
    {
        "description": str,
        "domainId": str,
        "environmentId": str,
        "id": str,
        "name": str,
        "parameters": ActionParametersTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EnvironmentActionSummaryTypeDef = TypedDict(
    "EnvironmentActionSummaryTypeDef",
    {
        "domainId": str,
        "environmentId": str,
        "id": str,
        "name": str,
        "parameters": ActionParametersTypeDef,
        "description": NotRequired[str],
    },
)
GetEnvironmentActionOutputTypeDef = TypedDict(
    "GetEnvironmentActionOutputTypeDef",
    {
        "description": str,
        "domainId": str,
        "environmentId": str,
        "id": str,
        "name": str,
        "parameters": ActionParametersTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class UpdateEnvironmentActionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str
    description: NotRequired[str]
    name: NotRequired[str]
    parameters: NotRequired[ActionParametersTypeDef]

UpdateEnvironmentActionOutputTypeDef = TypedDict(
    "UpdateEnvironmentActionOutputTypeDef",
    {
        "description": str,
        "domainId": str,
        "environmentId": str,
        "id": str,
        "name": str,
        "parameters": ActionParametersTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class AssetItemTypeDef(TypedDict):
    domainId: str
    identifier: str
    name: str
    owningProjectId: str
    typeIdentifier: str
    typeRevision: str
    additionalAttributes: NotRequired[AssetItemAdditionalAttributesTypeDef]
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    description: NotRequired[str]
    externalIdentifier: NotRequired[str]
    firstRevisionCreatedAt: NotRequired[datetime]
    firstRevisionCreatedBy: NotRequired[str]
    glossaryTerms: NotRequired[List[str]]

class AssetListingItemTypeDef(TypedDict):
    additionalAttributes: NotRequired[AssetListingItemAdditionalAttributesTypeDef]
    createdAt: NotRequired[datetime]
    description: NotRequired[str]
    entityId: NotRequired[str]
    entityRevision: NotRequired[str]
    entityType: NotRequired[str]
    glossaryTerms: NotRequired[List[DetailedGlossaryTermTypeDef]]
    listingCreatedBy: NotRequired[str]
    listingId: NotRequired[str]
    listingRevision: NotRequired[str]
    listingUpdatedBy: NotRequired[str]
    name: NotRequired[str]
    owningProjectId: NotRequired[str]

class DataProductListingItemTypeDef(TypedDict):
    additionalAttributes: NotRequired[DataProductListingItemAdditionalAttributesTypeDef]
    createdAt: NotRequired[datetime]
    description: NotRequired[str]
    entityId: NotRequired[str]
    entityRevision: NotRequired[str]
    glossaryTerms: NotRequired[List[DetailedGlossaryTermTypeDef]]
    items: NotRequired[List[ListingSummaryItemTypeDef]]
    listingCreatedBy: NotRequired[str]
    listingId: NotRequired[str]
    listingRevision: NotRequired[str]
    listingUpdatedBy: NotRequired[str]
    name: NotRequired[str]
    owningProjectId: NotRequired[str]

class DataProductListingTypeDef(TypedDict):
    createdAt: NotRequired[datetime]
    dataProductId: NotRequired[str]
    dataProductRevision: NotRequired[str]
    forms: NotRequired[str]
    glossaryTerms: NotRequired[List[DetailedGlossaryTermTypeDef]]
    items: NotRequired[List[ListingSummaryTypeDef]]
    owningProjectId: NotRequired[str]

class SubscribedListingItemTypeDef(TypedDict):
    assetListing: NotRequired[SubscribedAssetListingTypeDef]
    productListing: NotRequired[SubscribedProductListingTypeDef]

class CreateAssetInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    owningProjectIdentifier: str
    typeIdentifier: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    externalIdentifier: NotRequired[str]
    formsInput: NotRequired[Sequence[FormInputTypeDef]]
    glossaryTerms: NotRequired[Sequence[str]]
    predictionConfiguration: NotRequired[PredictionConfigurationTypeDef]
    typeRevision: NotRequired[str]

CreateAssetOutputTypeDef = TypedDict(
    "CreateAssetOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "externalIdentifier": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "formsOutput": List[FormOutputTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "latestTimeSeriesDataPointFormsOutput": List[TimeSeriesDataPointSummaryFormOutputTypeDef],
        "listing": AssetListingDetailsTypeDef,
        "name": str,
        "owningProjectId": str,
        "predictionConfiguration": PredictionConfigurationTypeDef,
        "readOnlyFormsOutput": List[FormOutputTypeDef],
        "revision": str,
        "typeIdentifier": str,
        "typeRevision": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateAssetRevisionInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    formsInput: NotRequired[Sequence[FormInputTypeDef]]
    glossaryTerms: NotRequired[Sequence[str]]
    predictionConfiguration: NotRequired[PredictionConfigurationTypeDef]
    typeRevision: NotRequired[str]

CreateAssetRevisionOutputTypeDef = TypedDict(
    "CreateAssetRevisionOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "externalIdentifier": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "formsOutput": List[FormOutputTypeDef],
        "glossaryTerms": List[str],
        "id": str,
        "latestTimeSeriesDataPointFormsOutput": List[TimeSeriesDataPointSummaryFormOutputTypeDef],
        "listing": AssetListingDetailsTypeDef,
        "name": str,
        "owningProjectId": str,
        "predictionConfiguration": PredictionConfigurationTypeDef,
        "readOnlyFormsOutput": List[FormOutputTypeDef],
        "revision": str,
        "typeIdentifier": str,
        "typeRevision": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EnvironmentBlueprintSummaryTypeDef = TypedDict(
    "EnvironmentBlueprintSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "provider": str,
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "updatedAt": NotRequired[datetime],
    },
)
GetEnvironmentBlueprintOutputTypeDef = TypedDict(
    "GetEnvironmentBlueprintOutputTypeDef",
    {
        "createdAt": datetime,
        "deploymentProperties": DeploymentPropertiesTypeDef,
        "description": str,
        "glossaryTerms": List[str],
        "id": str,
        "name": str,
        "provider": str,
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "updatedAt": datetime,
        "userParameters": List[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateDataProductInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    owningProjectIdentifier: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    formsInput: NotRequired[Sequence[FormInputTypeDef]]
    glossaryTerms: NotRequired[Sequence[str]]
    items: NotRequired[Sequence[DataProductItemUnionTypeDef]]

class ListDataSourceRunActivitiesOutputTypeDef(TypedDict):
    items: List[DataSourceRunActivityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDataSourcesOutputTypeDef(TypedDict):
    items: List[DataSourceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListProjectsOutputTypeDef(TypedDict):
    items: List[ProjectSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSubscriptionTargetsOutputTypeDef(TypedDict):
    items: List[SubscriptionTargetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDataSourceRunsOutputTypeDef(TypedDict):
    items: List[DataSourceRunSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

CreateEnvironmentOutputTypeDef = TypedDict(
    "CreateEnvironmentOutputTypeDef",
    {
        "awsAccountId": str,
        "awsAccountRegion": str,
        "createdAt": datetime,
        "createdBy": str,
        "deploymentProperties": DeploymentPropertiesTypeDef,
        "description": str,
        "domainId": str,
        "environmentActions": List[ConfigurableEnvironmentActionTypeDef],
        "environmentBlueprintId": str,
        "environmentProfileId": str,
        "glossaryTerms": List[str],
        "id": str,
        "lastDeployment": DeploymentTypeDef,
        "name": str,
        "projectId": str,
        "provider": str,
        "provisionedResources": List[ResourceTypeDef],
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "status": EnvironmentStatusType,
        "updatedAt": datetime,
        "userParameters": List[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetEnvironmentOutputTypeDef = TypedDict(
    "GetEnvironmentOutputTypeDef",
    {
        "awsAccountId": str,
        "awsAccountRegion": str,
        "createdAt": datetime,
        "createdBy": str,
        "deploymentProperties": DeploymentPropertiesTypeDef,
        "description": str,
        "domainId": str,
        "environmentActions": List[ConfigurableEnvironmentActionTypeDef],
        "environmentBlueprintId": str,
        "environmentProfileId": str,
        "glossaryTerms": List[str],
        "id": str,
        "lastDeployment": DeploymentTypeDef,
        "name": str,
        "projectId": str,
        "provider": str,
        "provisionedResources": List[ResourceTypeDef],
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "status": EnvironmentStatusType,
        "updatedAt": datetime,
        "userParameters": List[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateEnvironmentOutputTypeDef = TypedDict(
    "UpdateEnvironmentOutputTypeDef",
    {
        "awsAccountId": str,
        "awsAccountRegion": str,
        "createdAt": datetime,
        "createdBy": str,
        "deploymentProperties": DeploymentPropertiesTypeDef,
        "description": str,
        "domainId": str,
        "environmentActions": List[ConfigurableEnvironmentActionTypeDef],
        "environmentBlueprintId": str,
        "environmentProfileId": str,
        "glossaryTerms": List[str],
        "id": str,
        "lastDeployment": DeploymentTypeDef,
        "name": str,
        "projectId": str,
        "provider": str,
        "provisionedResources": List[ResourceTypeDef],
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "status": EnvironmentStatusType,
        "updatedAt": datetime,
        "userParameters": List[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ProjectPolicyGrantPrincipalTypeDef(TypedDict):
    projectDesignation: ProjectDesignationType
    projectGrantFilter: NotRequired[ProjectGrantFilterTypeDef]
    projectIdentifier: NotRequired[str]

class DomainUnitPolicyGrantPrincipalTypeDef(TypedDict):
    domainUnitDesignation: Literal["OWNER"]
    domainUnitGrantFilter: NotRequired[DomainUnitGrantFilterUnionTypeDef]
    domainUnitIdentifier: NotRequired[str]

CreateDomainUnitOutputTypeDef = TypedDict(
    "CreateDomainUnitOutputTypeDef",
    {
        "ancestorDomainUnitIds": List[str],
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "id": str,
        "name": str,
        "owners": List[DomainUnitOwnerPropertiesTypeDef],
        "parentDomainUnitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDomainUnitOutputTypeDef = TypedDict(
    "GetDomainUnitOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "lastUpdatedBy": str,
        "name": str,
        "owners": List[DomainUnitOwnerPropertiesTypeDef],
        "parentDomainUnitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateDomainUnitOutputTypeDef = TypedDict(
    "UpdateDomainUnitOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "lastUpdatedBy": str,
        "name": str,
        "owners": List[DomainUnitOwnerPropertiesTypeDef],
        "parentDomainUnitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class SearchInputSearchPaginateTypeDef(TypedDict):
    domainIdentifier: str
    searchScope: InventorySearchScopeType
    additionalAttributes: NotRequired[Sequence[SearchOutputAdditionalAttributeType]]
    filters: NotRequired[FilterClausePaginatorTypeDef]
    owningProjectIdentifier: NotRequired[str]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    searchText: NotRequired[str]
    sort: NotRequired[SearchSortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchListingsInputSearchListingsPaginateTypeDef(TypedDict):
    domainIdentifier: str
    additionalAttributes: NotRequired[Sequence[SearchOutputAdditionalAttributeType]]
    filters: NotRequired[FilterClausePaginatorTypeDef]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    searchText: NotRequired[str]
    sort: NotRequired[SearchSortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchTypesInputSearchTypesPaginateTypeDef(TypedDict):
    domainIdentifier: str
    managed: bool
    searchScope: TypesSearchScopeType
    filters: NotRequired[FilterClausePaginatorTypeDef]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    searchText: NotRequired[str]
    sort: NotRequired[SearchSortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    searchScope: InventorySearchScopeType
    additionalAttributes: NotRequired[Sequence[SearchOutputAdditionalAttributeType]]
    filters: NotRequired[FilterClauseTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    owningProjectIdentifier: NotRequired[str]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    searchText: NotRequired[str]
    sort: NotRequired[SearchSortTypeDef]

class SearchListingsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    additionalAttributes: NotRequired[Sequence[SearchOutputAdditionalAttributeType]]
    filters: NotRequired[FilterClauseTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    searchText: NotRequired[str]
    sort: NotRequired[SearchSortTypeDef]

class SearchTypesInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    managed: bool
    searchScope: TypesSearchScopeType
    filters: NotRequired[FilterClauseTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    searchText: NotRequired[str]
    sort: NotRequired[SearchSortTypeDef]

class GlueRunConfigurationOutputTypeDef(TypedDict):
    relationalFilterConfigurations: List[RelationalFilterConfigurationOutputTypeDef]
    accountId: NotRequired[str]
    autoImportDataQualityResult: NotRequired[bool]
    dataAccessRole: NotRequired[str]
    region: NotRequired[str]

RelationalFilterConfigurationUnionTypeDef = Union[
    RelationalFilterConfigurationTypeDef, RelationalFilterConfigurationOutputTypeDef
]

class SearchTypesResultItemTypeDef(TypedDict):
    assetTypeItem: NotRequired[AssetTypeItemTypeDef]
    formTypeItem: NotRequired[FormTypeDataTypeDef]
    lineageNodeTypeItem: NotRequired[LineageNodeTypeItemTypeDef]

class PostTimeSeriesDataPointsInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TimeSeriesEntityTypeType
    forms: Sequence[TimeSeriesDataPointFormInputTypeDef]
    clientToken: NotRequired[str]

class ListMetadataGenerationRunsOutputTypeDef(TypedDict):
    items: List[MetadataGenerationRunItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SelfGrantStatusOutputTypeDef(TypedDict):
    glueSelfGrantStatus: NotRequired[GlueSelfGrantStatusOutputTypeDef]
    redshiftSelfGrantStatus: NotRequired[RedshiftSelfGrantStatusOutputTypeDef]

class CreateSubscriptionGrantInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    grantedEntity: GrantedEntityInputTypeDef
    subscriptionTargetIdentifier: str
    assetTargetNames: NotRequired[Sequence[AssetTargetNameMapTypeDef]]
    clientToken: NotRequired[str]

CreateSubscriptionGrantOutputTypeDef = TypedDict(
    "CreateSubscriptionGrantOutputTypeDef",
    {
        "assets": List[SubscribedAssetTypeDef],
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "grantedEntity": GrantedEntityTypeDef,
        "id": str,
        "status": SubscriptionGrantOverallStatusType,
        "subscriptionId": str,
        "subscriptionTargetId": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteSubscriptionGrantOutputTypeDef = TypedDict(
    "DeleteSubscriptionGrantOutputTypeDef",
    {
        "assets": List[SubscribedAssetTypeDef],
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "grantedEntity": GrantedEntityTypeDef,
        "id": str,
        "status": SubscriptionGrantOverallStatusType,
        "subscriptionId": str,
        "subscriptionTargetId": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSubscriptionGrantOutputTypeDef = TypedDict(
    "GetSubscriptionGrantOutputTypeDef",
    {
        "assets": List[SubscribedAssetTypeDef],
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "grantedEntity": GrantedEntityTypeDef,
        "id": str,
        "status": SubscriptionGrantOverallStatusType,
        "subscriptionId": str,
        "subscriptionTargetId": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SubscriptionGrantSummaryTypeDef = TypedDict(
    "SubscriptionGrantSummaryTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "grantedEntity": GrantedEntityTypeDef,
        "id": str,
        "status": SubscriptionGrantOverallStatusType,
        "subscriptionTargetId": str,
        "updatedAt": datetime,
        "assets": NotRequired[List[SubscribedAssetTypeDef]],
        "subscriptionId": NotRequired[str],
        "updatedBy": NotRequired[str],
    },
)
UpdateSubscriptionGrantStatusOutputTypeDef = TypedDict(
    "UpdateSubscriptionGrantStatusOutputTypeDef",
    {
        "assets": List[SubscribedAssetTypeDef],
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "grantedEntity": GrantedEntityTypeDef,
        "id": str,
        "status": SubscriptionGrantOverallStatusType,
        "subscriptionId": str,
        "subscriptionTargetId": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class EnvironmentBlueprintConfigurationItemTypeDef(TypedDict):
    domainId: str
    environmentBlueprintId: str
    createdAt: NotRequired[datetime]
    enabledRegions: NotRequired[List[str]]
    manageAccessRoleArn: NotRequired[str]
    provisioningConfigurations: NotRequired[List[ProvisioningConfigurationOutputTypeDef]]
    provisioningRoleArn: NotRequired[str]
    regionalParameters: NotRequired[Dict[str, Dict[str, str]]]
    updatedAt: NotRequired[datetime]

class GetEnvironmentBlueprintConfigurationOutputTypeDef(TypedDict):
    createdAt: datetime
    domainId: str
    enabledRegions: List[str]
    environmentBlueprintId: str
    manageAccessRoleArn: str
    provisioningConfigurations: List[ProvisioningConfigurationOutputTypeDef]
    provisioningRoleArn: str
    regionalParameters: Dict[str, Dict[str, str]]
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class PutEnvironmentBlueprintConfigurationOutputTypeDef(TypedDict):
    createdAt: datetime
    domainId: str
    enabledRegions: List[str]
    environmentBlueprintId: str
    manageAccessRoleArn: str
    provisioningConfigurations: List[ProvisioningConfigurationOutputTypeDef]
    provisioningRoleArn: str
    regionalParameters: Dict[str, Dict[str, str]]
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ProvisioningConfigurationTypeDef(TypedDict):
    lakeFormationConfiguration: NotRequired[LakeFormationConfigurationUnionTypeDef]

class ProjectMemberTypeDef(TypedDict):
    designation: UserDesignationType
    memberDetails: MemberDetailsTypeDef

RowFilterExpressionTypeDef = TypedDict(
    "RowFilterExpressionTypeDef",
    {
        "equalTo": NotRequired[EqualToExpressionTypeDef],
        "greaterThan": NotRequired[GreaterThanExpressionTypeDef],
        "greaterThanOrEqualTo": NotRequired[GreaterThanOrEqualToExpressionTypeDef],
        "in": NotRequired[InExpressionUnionTypeDef],
        "isNotNull": NotRequired[IsNotNullExpressionTypeDef],
        "isNull": NotRequired[IsNullExpressionTypeDef],
        "lessThan": NotRequired[LessThanExpressionTypeDef],
        "lessThanOrEqualTo": NotRequired[LessThanOrEqualToExpressionTypeDef],
        "like": NotRequired[LikeExpressionTypeDef],
        "notEqualTo": NotRequired[NotEqualToExpressionTypeDef],
        "notIn": NotRequired[NotInExpressionUnionTypeDef],
        "notLike": NotRequired[NotLikeExpressionTypeDef],
    },
)
RowFilterOutputTypeDef = TypedDict(
    "RowFilterOutputTypeDef",
    {
        "and": NotRequired[List[Dict[str, Any]]],
        "expression": NotRequired[RowFilterExpressionOutputTypeDef],
        "or": NotRequired[List[Dict[str, Any]]],
    },
)
NotificationOutputTypeDef = TypedDict(
    "NotificationOutputTypeDef",
    {
        "actionLink": str,
        "creationTimestamp": datetime,
        "domainIdentifier": str,
        "identifier": str,
        "lastUpdatedTimestamp": datetime,
        "message": str,
        "title": str,
        "topic": TopicTypeDef,
        "type": NotificationTypeType,
        "metadata": NotRequired[Dict[str, str]],
        "status": NotRequired[TaskStatusType],
    },
)

class ListEntityOwnersOutputTypeDef(TypedDict):
    owners: List[OwnerPropertiesOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class AddEntityOwnerInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: Literal["DOMAIN_UNIT"]
    owner: OwnerPropertiesTypeDef
    clientToken: NotRequired[str]

class RemoveEntityOwnerInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: Literal["DOMAIN_UNIT"]
    owner: OwnerPropertiesTypeDef
    clientToken: NotRequired[str]

class RedshiftRunConfigurationInputTypeDef(TypedDict):
    redshiftCredentialConfiguration: RedshiftCredentialConfigurationTypeDef
    redshiftStorage: RedshiftStorageTypeDef
    relationalFilterConfigurations: Sequence[RelationalFilterConfigurationTypeDef]
    dataAccessRole: NotRequired[str]

class RedshiftRunConfigurationOutputTypeDef(TypedDict):
    redshiftCredentialConfiguration: RedshiftCredentialConfigurationTypeDef
    redshiftStorage: RedshiftStorageTypeDef
    relationalFilterConfigurations: List[RelationalFilterConfigurationOutputTypeDef]
    accountId: NotRequired[str]
    dataAccessRole: NotRequired[str]
    region: NotRequired[str]

CreateUserProfileOutputTypeDef = TypedDict(
    "CreateUserProfileOutputTypeDef",
    {
        "details": UserProfileDetailsTypeDef,
        "domainId": str,
        "id": str,
        "status": UserProfileStatusType,
        "type": UserProfileTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetUserProfileOutputTypeDef = TypedDict(
    "GetUserProfileOutputTypeDef",
    {
        "details": UserProfileDetailsTypeDef,
        "domainId": str,
        "id": str,
        "status": UserProfileStatusType,
        "type": UserProfileTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateUserProfileOutputTypeDef = TypedDict(
    "UpdateUserProfileOutputTypeDef",
    {
        "details": UserProfileDetailsTypeDef,
        "domainId": str,
        "id": str,
        "status": UserProfileStatusType,
        "type": UserProfileTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UserProfileSummaryTypeDef = TypedDict(
    "UserProfileSummaryTypeDef",
    {
        "details": NotRequired[UserProfileDetailsTypeDef],
        "domainId": NotRequired[str],
        "id": NotRequired[str],
        "status": NotRequired[UserProfileStatusType],
        "type": NotRequired[UserProfileTypeType],
    },
)

class CreateSubscriptionRequestInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    requestReason: str
    subscribedListings: Sequence[SubscribedListingInputTypeDef]
    subscribedPrincipals: Sequence[SubscribedPrincipalInputTypeDef]
    clientToken: NotRequired[str]

class ListEnvironmentActionsOutputTypeDef(TypedDict):
    items: List[EnvironmentActionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SearchInventoryResultItemTypeDef(TypedDict):
    assetItem: NotRequired[AssetItemTypeDef]
    dataProductItem: NotRequired[DataProductResultItemTypeDef]
    glossaryItem: NotRequired[GlossaryItemTypeDef]
    glossaryTermItem: NotRequired[GlossaryTermItemTypeDef]

class SearchResultItemTypeDef(TypedDict):
    assetListing: NotRequired[AssetListingItemTypeDef]
    dataProductListing: NotRequired[DataProductListingItemTypeDef]

class ListingItemTypeDef(TypedDict):
    assetListing: NotRequired[AssetListingTypeDef]
    dataProductListing: NotRequired[DataProductListingTypeDef]

SubscribedListingTypeDef = TypedDict(
    "SubscribedListingTypeDef",
    {
        "description": str,
        "id": str,
        "item": SubscribedListingItemTypeDef,
        "name": str,
        "ownerProjectId": str,
        "ownerProjectName": NotRequired[str],
        "revision": NotRequired[str],
    },
)

class ListEnvironmentBlueprintsOutputTypeDef(TypedDict):
    items: List[EnvironmentBlueprintSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PolicyGrantPrincipalOutputTypeDef(TypedDict):
    domainUnit: NotRequired[DomainUnitPolicyGrantPrincipalOutputTypeDef]
    group: NotRequired[GroupPolicyGrantPrincipalTypeDef]
    project: NotRequired[ProjectPolicyGrantPrincipalTypeDef]
    user: NotRequired[UserPolicyGrantPrincipalOutputTypeDef]

DomainUnitPolicyGrantPrincipalUnionTypeDef = Union[
    DomainUnitPolicyGrantPrincipalTypeDef, DomainUnitPolicyGrantPrincipalOutputTypeDef
]

class GlueRunConfigurationInputTypeDef(TypedDict):
    relationalFilterConfigurations: Sequence[RelationalFilterConfigurationUnionTypeDef]
    autoImportDataQualityResult: NotRequired[bool]
    dataAccessRole: NotRequired[str]

class SearchTypesOutputTypeDef(TypedDict):
    items: List[SearchTypesResultItemTypeDef]
    totalMatchCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSubscriptionGrantsOutputTypeDef(TypedDict):
    items: List[SubscriptionGrantSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListEnvironmentBlueprintConfigurationsOutputTypeDef(TypedDict):
    items: List[EnvironmentBlueprintConfigurationItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

ProvisioningConfigurationUnionTypeDef = Union[
    ProvisioningConfigurationTypeDef, ProvisioningConfigurationOutputTypeDef
]

class ListProjectMembershipsOutputTypeDef(TypedDict):
    members: List[ProjectMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

RowFilterExpressionUnionTypeDef = Union[
    RowFilterExpressionTypeDef, RowFilterExpressionOutputTypeDef
]

class RowFilterConfigurationOutputTypeDef(TypedDict):
    rowFilter: RowFilterOutputTypeDef
    sensitive: NotRequired[bool]

class ListNotificationsOutputTypeDef(TypedDict):
    notifications: List[NotificationOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DataSourceConfigurationOutputTypeDef(TypedDict):
    glueRunConfiguration: NotRequired[GlueRunConfigurationOutputTypeDef]
    redshiftRunConfiguration: NotRequired[RedshiftRunConfigurationOutputTypeDef]

class SearchUserProfilesOutputTypeDef(TypedDict):
    items: List[UserProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SearchOutputTypeDef(TypedDict):
    items: List[SearchInventoryResultItemTypeDef]
    totalMatchCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SearchListingsOutputTypeDef(TypedDict):
    items: List[SearchResultItemTypeDef]
    totalMatchCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

GetListingOutputTypeDef = TypedDict(
    "GetListingOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "domainId": str,
        "id": str,
        "item": ListingItemTypeDef,
        "listingRevision": str,
        "name": str,
        "status": ListingStatusType,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
AcceptSubscriptionRequestOutputTypeDef = TypedDict(
    "AcceptSubscriptionRequestOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "decisionComment": str,
        "domainId": str,
        "id": str,
        "requestReason": str,
        "reviewerId": str,
        "status": SubscriptionRequestStatusType,
        "subscribedListings": List[SubscribedListingTypeDef],
        "subscribedPrincipals": List[SubscribedPrincipalTypeDef],
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CancelSubscriptionOutputTypeDef = TypedDict(
    "CancelSubscriptionOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "id": str,
        "retainPermissions": bool,
        "status": SubscriptionStatusType,
        "subscribedListing": SubscribedListingTypeDef,
        "subscribedPrincipal": SubscribedPrincipalTypeDef,
        "subscriptionRequestId": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateSubscriptionRequestOutputTypeDef = TypedDict(
    "CreateSubscriptionRequestOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "decisionComment": str,
        "domainId": str,
        "id": str,
        "requestReason": str,
        "reviewerId": str,
        "status": SubscriptionRequestStatusType,
        "subscribedListings": List[SubscribedListingTypeDef],
        "subscribedPrincipals": List[SubscribedPrincipalTypeDef],
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSubscriptionOutputTypeDef = TypedDict(
    "GetSubscriptionOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "id": str,
        "retainPermissions": bool,
        "status": SubscriptionStatusType,
        "subscribedListing": SubscribedListingTypeDef,
        "subscribedPrincipal": SubscribedPrincipalTypeDef,
        "subscriptionRequestId": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSubscriptionRequestDetailsOutputTypeDef = TypedDict(
    "GetSubscriptionRequestDetailsOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "decisionComment": str,
        "domainId": str,
        "id": str,
        "requestReason": str,
        "reviewerId": str,
        "status": SubscriptionRequestStatusType,
        "subscribedListings": List[SubscribedListingTypeDef],
        "subscribedPrincipals": List[SubscribedPrincipalTypeDef],
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RejectSubscriptionRequestOutputTypeDef = TypedDict(
    "RejectSubscriptionRequestOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "decisionComment": str,
        "domainId": str,
        "id": str,
        "requestReason": str,
        "reviewerId": str,
        "status": SubscriptionRequestStatusType,
        "subscribedListings": List[SubscribedListingTypeDef],
        "subscribedPrincipals": List[SubscribedPrincipalTypeDef],
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RevokeSubscriptionOutputTypeDef = TypedDict(
    "RevokeSubscriptionOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "id": str,
        "retainPermissions": bool,
        "status": SubscriptionStatusType,
        "subscribedListing": SubscribedListingTypeDef,
        "subscribedPrincipal": SubscribedPrincipalTypeDef,
        "subscriptionRequestId": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SubscriptionRequestSummaryTypeDef = TypedDict(
    "SubscriptionRequestSummaryTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "id": str,
        "requestReason": str,
        "status": SubscriptionRequestStatusType,
        "subscribedListings": List[SubscribedListingTypeDef],
        "subscribedPrincipals": List[SubscribedPrincipalTypeDef],
        "updatedAt": datetime,
        "decisionComment": NotRequired[str],
        "reviewerId": NotRequired[str],
        "updatedBy": NotRequired[str],
    },
)
SubscriptionSummaryTypeDef = TypedDict(
    "SubscriptionSummaryTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "domainId": str,
        "id": str,
        "status": SubscriptionStatusType,
        "subscribedListing": SubscribedListingTypeDef,
        "subscribedPrincipal": SubscribedPrincipalTypeDef,
        "updatedAt": datetime,
        "retainPermissions": NotRequired[bool],
        "subscriptionRequestId": NotRequired[str],
        "updatedBy": NotRequired[str],
    },
)
UpdateSubscriptionRequestOutputTypeDef = TypedDict(
    "UpdateSubscriptionRequestOutputTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "decisionComment": str,
        "domainId": str,
        "id": str,
        "requestReason": str,
        "reviewerId": str,
        "status": SubscriptionRequestStatusType,
        "subscribedListings": List[SubscribedListingTypeDef],
        "subscribedPrincipals": List[SubscribedPrincipalTypeDef],
        "updatedAt": datetime,
        "updatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class PolicyGrantMemberTypeDef(TypedDict):
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    detail: NotRequired[PolicyGrantDetailOutputTypeDef]
    principal: NotRequired[PolicyGrantPrincipalOutputTypeDef]

class PolicyGrantPrincipalTypeDef(TypedDict):
    domainUnit: NotRequired[DomainUnitPolicyGrantPrincipalUnionTypeDef]
    group: NotRequired[GroupPolicyGrantPrincipalTypeDef]
    project: NotRequired[ProjectPolicyGrantPrincipalTypeDef]
    user: NotRequired[UserPolicyGrantPrincipalUnionTypeDef]

class DataSourceConfigurationInputTypeDef(TypedDict):
    glueRunConfiguration: NotRequired[GlueRunConfigurationInputTypeDef]
    redshiftRunConfiguration: NotRequired[RedshiftRunConfigurationInputTypeDef]

class PutEnvironmentBlueprintConfigurationInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    enabledRegions: Sequence[str]
    environmentBlueprintIdentifier: str
    manageAccessRoleArn: NotRequired[str]
    provisioningConfigurations: NotRequired[Sequence[ProvisioningConfigurationUnionTypeDef]]
    provisioningRoleArn: NotRequired[str]
    regionalParameters: NotRequired[Mapping[str, Mapping[str, str]]]

RowFilterTypeDef = TypedDict(
    "RowFilterTypeDef",
    {
        "and": NotRequired[Sequence[Mapping[str, Any]]],
        "expression": NotRequired[RowFilterExpressionUnionTypeDef],
        "or": NotRequired[Sequence[Mapping[str, Any]]],
    },
)

class AssetFilterConfigurationOutputTypeDef(TypedDict):
    columnConfiguration: NotRequired[ColumnFilterConfigurationOutputTypeDef]
    rowConfiguration: NotRequired[RowFilterConfigurationOutputTypeDef]

CreateDataSourceOutputTypeDef = TypedDict(
    "CreateDataSourceOutputTypeDef",
    {
        "assetFormsOutput": List[FormOutputTypeDef],
        "configuration": DataSourceConfigurationOutputTypeDef,
        "createdAt": datetime,
        "description": str,
        "domainId": str,
        "enableSetting": EnableSettingType,
        "environmentId": str,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "id": str,
        "lastRunAt": datetime,
        "lastRunErrorMessage": DataSourceErrorMessageTypeDef,
        "lastRunStatus": DataSourceRunStatusType,
        "name": str,
        "projectId": str,
        "publishOnImport": bool,
        "recommendation": RecommendationConfigurationTypeDef,
        "schedule": ScheduleConfigurationTypeDef,
        "status": DataSourceStatusType,
        "type": str,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteDataSourceOutputTypeDef = TypedDict(
    "DeleteDataSourceOutputTypeDef",
    {
        "assetFormsOutput": List[FormOutputTypeDef],
        "configuration": DataSourceConfigurationOutputTypeDef,
        "createdAt": datetime,
        "description": str,
        "domainId": str,
        "enableSetting": EnableSettingType,
        "environmentId": str,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "id": str,
        "lastRunAt": datetime,
        "lastRunErrorMessage": DataSourceErrorMessageTypeDef,
        "lastRunStatus": DataSourceRunStatusType,
        "name": str,
        "projectId": str,
        "publishOnImport": bool,
        "retainPermissionsOnRevokeFailure": bool,
        "schedule": ScheduleConfigurationTypeDef,
        "selfGrantStatus": SelfGrantStatusOutputTypeDef,
        "status": DataSourceStatusType,
        "type": str,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDataSourceOutputTypeDef = TypedDict(
    "GetDataSourceOutputTypeDef",
    {
        "assetFormsOutput": List[FormOutputTypeDef],
        "configuration": DataSourceConfigurationOutputTypeDef,
        "createdAt": datetime,
        "description": str,
        "domainId": str,
        "enableSetting": EnableSettingType,
        "environmentId": str,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "id": str,
        "lastRunAssetCount": int,
        "lastRunAt": datetime,
        "lastRunErrorMessage": DataSourceErrorMessageTypeDef,
        "lastRunStatus": DataSourceRunStatusType,
        "name": str,
        "projectId": str,
        "publishOnImport": bool,
        "recommendation": RecommendationConfigurationTypeDef,
        "schedule": ScheduleConfigurationTypeDef,
        "selfGrantStatus": SelfGrantStatusOutputTypeDef,
        "status": DataSourceStatusType,
        "type": str,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateDataSourceOutputTypeDef = TypedDict(
    "UpdateDataSourceOutputTypeDef",
    {
        "assetFormsOutput": List[FormOutputTypeDef],
        "configuration": DataSourceConfigurationOutputTypeDef,
        "createdAt": datetime,
        "description": str,
        "domainId": str,
        "enableSetting": EnableSettingType,
        "environmentId": str,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "id": str,
        "lastRunAt": datetime,
        "lastRunErrorMessage": DataSourceErrorMessageTypeDef,
        "lastRunStatus": DataSourceRunStatusType,
        "name": str,
        "projectId": str,
        "publishOnImport": bool,
        "recommendation": RecommendationConfigurationTypeDef,
        "retainPermissionsOnRevokeFailure": bool,
        "schedule": ScheduleConfigurationTypeDef,
        "selfGrantStatus": SelfGrantStatusOutputTypeDef,
        "status": DataSourceStatusType,
        "type": str,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ListSubscriptionRequestsOutputTypeDef(TypedDict):
    items: List[SubscriptionRequestSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSubscriptionsOutputTypeDef(TypedDict):
    items: List[SubscriptionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPolicyGrantsOutputTypeDef(TypedDict):
    grantList: List[PolicyGrantMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class AddPolicyGrantInputRequestTypeDef(TypedDict):
    detail: PolicyGrantDetailTypeDef
    domainIdentifier: str
    entityIdentifier: str
    entityType: TargetEntityTypeType
    policyType: ManagedPolicyTypeType
    principal: PolicyGrantPrincipalTypeDef
    clientToken: NotRequired[str]

class RemovePolicyGrantInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TargetEntityTypeType
    policyType: ManagedPolicyTypeType
    principal: PolicyGrantPrincipalTypeDef
    clientToken: NotRequired[str]

CreateDataSourceInputRequestTypeDef = TypedDict(
    "CreateDataSourceInputRequestTypeDef",
    {
        "domainIdentifier": str,
        "environmentIdentifier": str,
        "name": str,
        "projectIdentifier": str,
        "type": str,
        "assetFormsInput": NotRequired[Sequence[FormInputTypeDef]],
        "clientToken": NotRequired[str],
        "configuration": NotRequired[DataSourceConfigurationInputTypeDef],
        "description": NotRequired[str],
        "enableSetting": NotRequired[EnableSettingType],
        "publishOnImport": NotRequired[bool],
        "recommendation": NotRequired[RecommendationConfigurationTypeDef],
        "schedule": NotRequired[ScheduleConfigurationTypeDef],
    },
)

class UpdateDataSourceInputRequestTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    assetFormsInput: NotRequired[Sequence[FormInputTypeDef]]
    configuration: NotRequired[DataSourceConfigurationInputTypeDef]
    description: NotRequired[str]
    enableSetting: NotRequired[EnableSettingType]
    name: NotRequired[str]
    publishOnImport: NotRequired[bool]
    recommendation: NotRequired[RecommendationConfigurationTypeDef]
    retainPermissionsOnRevokeFailure: NotRequired[bool]
    schedule: NotRequired[ScheduleConfigurationTypeDef]

RowFilterUnionTypeDef = Union[RowFilterTypeDef, RowFilterOutputTypeDef]
CreateAssetFilterOutputTypeDef = TypedDict(
    "CreateAssetFilterOutputTypeDef",
    {
        "assetId": str,
        "configuration": AssetFilterConfigurationOutputTypeDef,
        "createdAt": datetime,
        "description": str,
        "domainId": str,
        "effectiveColumnNames": List[str],
        "effectiveRowFilter": str,
        "errorMessage": str,
        "id": str,
        "name": str,
        "status": FilterStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAssetFilterOutputTypeDef = TypedDict(
    "GetAssetFilterOutputTypeDef",
    {
        "assetId": str,
        "configuration": AssetFilterConfigurationOutputTypeDef,
        "createdAt": datetime,
        "description": str,
        "domainId": str,
        "effectiveColumnNames": List[str],
        "effectiveRowFilter": str,
        "errorMessage": str,
        "id": str,
        "name": str,
        "status": FilterStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateAssetFilterOutputTypeDef = TypedDict(
    "UpdateAssetFilterOutputTypeDef",
    {
        "assetId": str,
        "configuration": AssetFilterConfigurationOutputTypeDef,
        "createdAt": datetime,
        "description": str,
        "domainId": str,
        "effectiveColumnNames": List[str],
        "effectiveRowFilter": str,
        "errorMessage": str,
        "id": str,
        "name": str,
        "status": FilterStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class RowFilterConfigurationTypeDef(TypedDict):
    rowFilter: RowFilterUnionTypeDef
    sensitive: NotRequired[bool]

RowFilterConfigurationUnionTypeDef = Union[
    RowFilterConfigurationTypeDef, RowFilterConfigurationOutputTypeDef
]

class AssetFilterConfigurationTypeDef(TypedDict):
    columnConfiguration: NotRequired[ColumnFilterConfigurationUnionTypeDef]
    rowConfiguration: NotRequired[RowFilterConfigurationUnionTypeDef]

class CreateAssetFilterInputRequestTypeDef(TypedDict):
    assetIdentifier: str
    configuration: AssetFilterConfigurationTypeDef
    domainIdentifier: str
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]

class UpdateAssetFilterInputRequestTypeDef(TypedDict):
    assetIdentifier: str
    domainIdentifier: str
    identifier: str
    configuration: NotRequired[AssetFilterConfigurationTypeDef]
    description: NotRequired[str]
    name: NotRequired[str]
