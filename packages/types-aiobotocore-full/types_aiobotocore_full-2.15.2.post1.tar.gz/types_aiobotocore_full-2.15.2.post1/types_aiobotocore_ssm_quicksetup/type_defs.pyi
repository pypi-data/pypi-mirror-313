"""
Type annotations for ssm-quicksetup service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_quicksetup/type_defs/)

Usage::

    ```python
    from types_aiobotocore_ssm_quicksetup.type_defs import ConfigurationDefinitionInputTypeDef

    data: ConfigurationDefinitionInputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import StatusType, StatusTypeType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ConfigurationDefinitionInputTypeDef",
    "ConfigurationDefinitionSummaryTypeDef",
    "ConfigurationDefinitionTypeDef",
    "ConfigurationManagerSummaryTypeDef",
    "CreateConfigurationManagerInputRequestTypeDef",
    "CreateConfigurationManagerOutputTypeDef",
    "DeleteConfigurationManagerInputRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "FilterTypeDef",
    "GetConfigurationManagerInputRequestTypeDef",
    "GetConfigurationManagerOutputTypeDef",
    "GetServiceSettingsOutputTypeDef",
    "ListConfigurationManagersInputListConfigurationManagersPaginateTypeDef",
    "ListConfigurationManagersInputRequestTypeDef",
    "ListConfigurationManagersOutputTypeDef",
    "ListQuickSetupTypesOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "QuickSetupTypeOutputTypeDef",
    "ResponseMetadataTypeDef",
    "ServiceSettingsTypeDef",
    "StatusSummaryTypeDef",
    "TagEntryTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateConfigurationDefinitionInputRequestTypeDef",
    "UpdateConfigurationManagerInputRequestTypeDef",
    "UpdateServiceSettingsInputRequestTypeDef",
)

ConfigurationDefinitionInputTypeDef = TypedDict(
    "ConfigurationDefinitionInputTypeDef",
    {
        "Parameters": Mapping[str, str],
        "Type": str,
        "LocalDeploymentAdministrationRoleArn": NotRequired[str],
        "LocalDeploymentExecutionRoleName": NotRequired[str],
        "TypeVersion": NotRequired[str],
    },
)
ConfigurationDefinitionSummaryTypeDef = TypedDict(
    "ConfigurationDefinitionSummaryTypeDef",
    {
        "FirstClassParameters": NotRequired[Dict[str, str]],
        "Id": NotRequired[str],
        "Type": NotRequired[str],
        "TypeVersion": NotRequired[str],
    },
)
ConfigurationDefinitionTypeDef = TypedDict(
    "ConfigurationDefinitionTypeDef",
    {
        "Parameters": Dict[str, str],
        "Type": str,
        "Id": NotRequired[str],
        "LocalDeploymentAdministrationRoleArn": NotRequired[str],
        "LocalDeploymentExecutionRoleName": NotRequired[str],
        "TypeVersion": NotRequired[str],
    },
)
StatusSummaryTypeDef = TypedDict(
    "StatusSummaryTypeDef",
    {
        "LastUpdatedAt": datetime,
        "StatusType": StatusTypeType,
        "Status": NotRequired[StatusType],
        "StatusDetails": NotRequired[Dict[str, str]],
        "StatusMessage": NotRequired[str],
    },
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeleteConfigurationManagerInputRequestTypeDef(TypedDict):
    ManagerArn: str

class FilterTypeDef(TypedDict):
    Key: str
    Values: Sequence[str]

class GetConfigurationManagerInputRequestTypeDef(TypedDict):
    ManagerArn: str

class ServiceSettingsTypeDef(TypedDict):
    ExplorerEnablingRoleArn: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

QuickSetupTypeOutputTypeDef = TypedDict(
    "QuickSetupTypeOutputTypeDef",
    {
        "LatestVersion": NotRequired[str],
        "Type": NotRequired[str],
    },
)

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class TagEntryTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]

class TagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateConfigurationDefinitionInputRequestTypeDef(TypedDict):
    Id: str
    ManagerArn: str
    LocalDeploymentAdministrationRoleArn: NotRequired[str]
    LocalDeploymentExecutionRoleName: NotRequired[str]
    Parameters: NotRequired[Mapping[str, str]]
    TypeVersion: NotRequired[str]

class UpdateConfigurationManagerInputRequestTypeDef(TypedDict):
    ManagerArn: str
    Description: NotRequired[str]
    Name: NotRequired[str]

class UpdateServiceSettingsInputRequestTypeDef(TypedDict):
    ExplorerEnablingRoleArn: NotRequired[str]

class CreateConfigurationManagerInputRequestTypeDef(TypedDict):
    ConfigurationDefinitions: Sequence[ConfigurationDefinitionInputTypeDef]
    Description: NotRequired[str]
    Name: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class ConfigurationManagerSummaryTypeDef(TypedDict):
    ManagerArn: str
    ConfigurationDefinitionSummaries: NotRequired[List[ConfigurationDefinitionSummaryTypeDef]]
    Description: NotRequired[str]
    Name: NotRequired[str]
    StatusSummaries: NotRequired[List[StatusSummaryTypeDef]]

class CreateConfigurationManagerOutputTypeDef(TypedDict):
    ManagerArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetConfigurationManagerOutputTypeDef(TypedDict):
    ConfigurationDefinitions: List[ConfigurationDefinitionTypeDef]
    CreatedAt: datetime
    Description: str
    LastModifiedAt: datetime
    ManagerArn: str
    Name: str
    StatusSummaries: List[StatusSummaryTypeDef]
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListConfigurationManagersInputRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxItems: NotRequired[int]
    StartingToken: NotRequired[str]

class GetServiceSettingsOutputTypeDef(TypedDict):
    ServiceSettings: ServiceSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListConfigurationManagersInputListConfigurationManagersPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQuickSetupTypesOutputTypeDef(TypedDict):
    QuickSetupTypeList: List[QuickSetupTypeOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListConfigurationManagersOutputTypeDef(TypedDict):
    ConfigurationManagersList: List[ConfigurationManagerSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
