"""
Type annotations for license-manager-user-subscriptions service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager_user_subscriptions/type_defs/)

Usage::

    ```python
    from types_aiobotocore_license_manager_user_subscriptions.type_defs import ActiveDirectoryIdentityProviderTypeDef

    data: ActiveDirectoryIdentityProviderTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Sequence

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ActiveDirectoryIdentityProviderTypeDef",
    "AssociateUserRequestRequestTypeDef",
    "AssociateUserResponseTypeDef",
    "DeregisterIdentityProviderRequestRequestTypeDef",
    "DeregisterIdentityProviderResponseTypeDef",
    "DisassociateUserRequestRequestTypeDef",
    "DisassociateUserResponseTypeDef",
    "FilterTypeDef",
    "IdentityProviderSummaryTypeDef",
    "IdentityProviderTypeDef",
    "InstanceSummaryTypeDef",
    "InstanceUserSummaryTypeDef",
    "ListIdentityProvidersRequestListIdentityProvidersPaginateTypeDef",
    "ListIdentityProvidersRequestRequestTypeDef",
    "ListIdentityProvidersResponseTypeDef",
    "ListInstancesRequestListInstancesPaginateTypeDef",
    "ListInstancesRequestRequestTypeDef",
    "ListInstancesResponseTypeDef",
    "ListProductSubscriptionsRequestListProductSubscriptionsPaginateTypeDef",
    "ListProductSubscriptionsRequestRequestTypeDef",
    "ListProductSubscriptionsResponseTypeDef",
    "ListUserAssociationsRequestListUserAssociationsPaginateTypeDef",
    "ListUserAssociationsRequestRequestTypeDef",
    "ListUserAssociationsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ProductUserSummaryTypeDef",
    "RegisterIdentityProviderRequestRequestTypeDef",
    "RegisterIdentityProviderResponseTypeDef",
    "ResponseMetadataTypeDef",
    "SettingsOutputTypeDef",
    "SettingsTypeDef",
    "StartProductSubscriptionRequestRequestTypeDef",
    "StartProductSubscriptionResponseTypeDef",
    "StopProductSubscriptionRequestRequestTypeDef",
    "StopProductSubscriptionResponseTypeDef",
    "UpdateIdentityProviderSettingsRequestRequestTypeDef",
    "UpdateIdentityProviderSettingsResponseTypeDef",
    "UpdateSettingsTypeDef",
)

class ActiveDirectoryIdentityProviderTypeDef(TypedDict):
    DirectoryId: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class FilterTypeDef(TypedDict):
    Attribute: NotRequired[str]
    Operation: NotRequired[str]
    Value: NotRequired[str]

class SettingsOutputTypeDef(TypedDict):
    SecurityGroupId: str
    Subnets: List[str]

class InstanceSummaryTypeDef(TypedDict):
    InstanceId: str
    Products: List[str]
    Status: str
    LastStatusCheckDate: NotRequired[str]
    StatusMessage: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListIdentityProvidersRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class SettingsTypeDef(TypedDict):
    SecurityGroupId: str
    Subnets: Sequence[str]

class UpdateSettingsTypeDef(TypedDict):
    AddSubnets: Sequence[str]
    RemoveSubnets: Sequence[str]
    SecurityGroupId: NotRequired[str]

class IdentityProviderTypeDef(TypedDict):
    ActiveDirectoryIdentityProvider: NotRequired[ActiveDirectoryIdentityProviderTypeDef]

class ListInstancesRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListInstancesResponseTypeDef(TypedDict):
    InstanceSummaries: List[InstanceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListIdentityProvidersRequestListIdentityProvidersPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListInstancesRequestListInstancesPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class AssociateUserRequestRequestTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    InstanceId: str
    Username: str
    Domain: NotRequired[str]

class DeregisterIdentityProviderRequestRequestTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    Product: str

class DisassociateUserRequestRequestTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    InstanceId: str
    Username: str
    Domain: NotRequired[str]

class IdentityProviderSummaryTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    Product: str
    Settings: SettingsOutputTypeDef
    Status: str
    FailureMessage: NotRequired[str]

class InstanceUserSummaryTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    InstanceId: str
    Status: str
    Username: str
    AssociationDate: NotRequired[str]
    DisassociationDate: NotRequired[str]
    Domain: NotRequired[str]
    StatusMessage: NotRequired[str]

class ListProductSubscriptionsRequestListProductSubscriptionsPaginateTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    Product: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProductSubscriptionsRequestRequestTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    Product: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListUserAssociationsRequestListUserAssociationsPaginateTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    InstanceId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListUserAssociationsRequestRequestTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    InstanceId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ProductUserSummaryTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    Product: str
    Status: str
    Username: str
    Domain: NotRequired[str]
    StatusMessage: NotRequired[str]
    SubscriptionEndDate: NotRequired[str]
    SubscriptionStartDate: NotRequired[str]

class RegisterIdentityProviderRequestRequestTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    Product: str
    Settings: NotRequired[SettingsTypeDef]

class StartProductSubscriptionRequestRequestTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    Product: str
    Username: str
    Domain: NotRequired[str]

class StopProductSubscriptionRequestRequestTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    Product: str
    Username: str
    Domain: NotRequired[str]

class UpdateIdentityProviderSettingsRequestRequestTypeDef(TypedDict):
    IdentityProvider: IdentityProviderTypeDef
    Product: str
    UpdateSettings: UpdateSettingsTypeDef

class DeregisterIdentityProviderResponseTypeDef(TypedDict):
    IdentityProviderSummary: IdentityProviderSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListIdentityProvidersResponseTypeDef(TypedDict):
    IdentityProviderSummaries: List[IdentityProviderSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class RegisterIdentityProviderResponseTypeDef(TypedDict):
    IdentityProviderSummary: IdentityProviderSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateIdentityProviderSettingsResponseTypeDef(TypedDict):
    IdentityProviderSummary: IdentityProviderSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AssociateUserResponseTypeDef(TypedDict):
    InstanceUserSummary: InstanceUserSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociateUserResponseTypeDef(TypedDict):
    InstanceUserSummary: InstanceUserSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListUserAssociationsResponseTypeDef(TypedDict):
    InstanceUserSummaries: List[InstanceUserSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListProductSubscriptionsResponseTypeDef(TypedDict):
    ProductUserSummaries: List[ProductUserSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class StartProductSubscriptionResponseTypeDef(TypedDict):
    ProductUserSummary: ProductUserSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StopProductSubscriptionResponseTypeDef(TypedDict):
    ProductUserSummary: ProductUserSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
