"""
Type annotations for qapps service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/type_defs/)

Usage::

    ```python
    from types_aiobotocore_qapps.type_defs import AssociateLibraryItemReviewInputRequestTypeDef

    data: AssociateLibraryItemReviewInputRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AppRequiredCapabilityType,
    AppStatusType,
    CardOutputSourceType,
    CardTypeType,
    DocumentScopeType,
    ExecutionStatusType,
    LibraryItemStatusType,
    PluginTypeType,
    SenderType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AppDefinitionInputOutputTypeDef",
    "AppDefinitionInputTypeDef",
    "AppDefinitionTypeDef",
    "AssociateLibraryItemReviewInputRequestTypeDef",
    "AssociateQAppWithUserInputRequestTypeDef",
    "AttributeFilterOutputTypeDef",
    "AttributeFilterTypeDef",
    "AttributeFilterUnionTypeDef",
    "CardInputOutputTypeDef",
    "CardInputTypeDef",
    "CardInputUnionTypeDef",
    "CardStatusTypeDef",
    "CardTypeDef",
    "CardValueTypeDef",
    "CategoryTypeDef",
    "ConversationMessageTypeDef",
    "CreateLibraryItemInputRequestTypeDef",
    "CreateLibraryItemOutputTypeDef",
    "CreateQAppInputRequestTypeDef",
    "CreateQAppOutputTypeDef",
    "DeleteLibraryItemInputRequestTypeDef",
    "DeleteQAppInputRequestTypeDef",
    "DisassociateLibraryItemReviewInputRequestTypeDef",
    "DisassociateQAppFromUserInputRequestTypeDef",
    "DocumentAttributeOutputTypeDef",
    "DocumentAttributeTypeDef",
    "DocumentAttributeUnionTypeDef",
    "DocumentAttributeValueOutputTypeDef",
    "DocumentAttributeValueTypeDef",
    "DocumentAttributeValueUnionTypeDef",
    "EmptyResponseMetadataTypeDef",
    "FileUploadCardInputTypeDef",
    "FileUploadCardTypeDef",
    "GetLibraryItemInputRequestTypeDef",
    "GetLibraryItemOutputTypeDef",
    "GetQAppInputRequestTypeDef",
    "GetQAppOutputTypeDef",
    "GetQAppSessionInputRequestTypeDef",
    "GetQAppSessionOutputTypeDef",
    "ImportDocumentInputRequestTypeDef",
    "ImportDocumentOutputTypeDef",
    "LibraryItemMemberTypeDef",
    "ListLibraryItemsInputListLibraryItemsPaginateTypeDef",
    "ListLibraryItemsInputRequestTypeDef",
    "ListLibraryItemsOutputTypeDef",
    "ListQAppsInputListQAppsPaginateTypeDef",
    "ListQAppsInputRequestTypeDef",
    "ListQAppsOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PredictAppDefinitionTypeDef",
    "PredictQAppInputOptionsTypeDef",
    "PredictQAppInputRequestTypeDef",
    "PredictQAppOutputTypeDef",
    "QPluginCardInputTypeDef",
    "QPluginCardTypeDef",
    "QQueryCardInputOutputTypeDef",
    "QQueryCardInputTypeDef",
    "QQueryCardInputUnionTypeDef",
    "QQueryCardTypeDef",
    "ResponseMetadataTypeDef",
    "StartQAppSessionInputRequestTypeDef",
    "StartQAppSessionOutputTypeDef",
    "StopQAppSessionInputRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TextInputCardInputTypeDef",
    "TextInputCardTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateLibraryItemInputRequestTypeDef",
    "UpdateLibraryItemMetadataInputRequestTypeDef",
    "UpdateLibraryItemOutputTypeDef",
    "UpdateQAppInputRequestTypeDef",
    "UpdateQAppOutputTypeDef",
    "UpdateQAppSessionInputRequestTypeDef",
    "UpdateQAppSessionOutputTypeDef",
    "UserAppItemTypeDef",
)


class AssociateLibraryItemReviewInputRequestTypeDef(TypedDict):
    instanceId: str
    libraryItemId: str


class AssociateQAppWithUserInputRequestTypeDef(TypedDict):
    instanceId: str
    appId: str


FileUploadCardInputTypeDef = TypedDict(
    "FileUploadCardInputTypeDef",
    {
        "title": str,
        "id": str,
        "type": CardTypeType,
        "filename": NotRequired[str],
        "fileId": NotRequired[str],
        "allowOverride": NotRequired[bool],
    },
)
QPluginCardInputTypeDef = TypedDict(
    "QPluginCardInputTypeDef",
    {
        "title": str,
        "id": str,
        "type": CardTypeType,
        "prompt": str,
        "pluginId": str,
    },
)
TextInputCardInputTypeDef = TypedDict(
    "TextInputCardInputTypeDef",
    {
        "title": str,
        "id": str,
        "type": CardTypeType,
        "placeholder": NotRequired[str],
        "defaultValue": NotRequired[str],
    },
)


class CardStatusTypeDef(TypedDict):
    currentState: ExecutionStatusType
    currentValue: str


FileUploadCardTypeDef = TypedDict(
    "FileUploadCardTypeDef",
    {
        "id": str,
        "title": str,
        "dependencies": List[str],
        "type": CardTypeType,
        "filename": NotRequired[str],
        "fileId": NotRequired[str],
        "allowOverride": NotRequired[bool],
    },
)
QPluginCardTypeDef = TypedDict(
    "QPluginCardTypeDef",
    {
        "id": str,
        "title": str,
        "dependencies": List[str],
        "type": CardTypeType,
        "prompt": str,
        "pluginType": PluginTypeType,
        "pluginId": str,
    },
)
TextInputCardTypeDef = TypedDict(
    "TextInputCardTypeDef",
    {
        "id": str,
        "title": str,
        "dependencies": List[str],
        "type": CardTypeType,
        "placeholder": NotRequired[str],
        "defaultValue": NotRequired[str],
    },
)


class CardValueTypeDef(TypedDict):
    cardId: str
    value: str


CategoryTypeDef = TypedDict(
    "CategoryTypeDef",
    {
        "id": str,
        "title": str,
    },
)
ConversationMessageTypeDef = TypedDict(
    "ConversationMessageTypeDef",
    {
        "body": str,
        "type": SenderType,
    },
)


class CreateLibraryItemInputRequestTypeDef(TypedDict):
    instanceId: str
    appId: str
    appVersion: int
    categories: Sequence[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeleteLibraryItemInputRequestTypeDef(TypedDict):
    instanceId: str
    libraryItemId: str


class DeleteQAppInputRequestTypeDef(TypedDict):
    instanceId: str
    appId: str


class DisassociateLibraryItemReviewInputRequestTypeDef(TypedDict):
    instanceId: str
    libraryItemId: str


class DisassociateQAppFromUserInputRequestTypeDef(TypedDict):
    instanceId: str
    appId: str


class DocumentAttributeValueOutputTypeDef(TypedDict):
    stringValue: NotRequired[str]
    stringListValue: NotRequired[List[str]]
    longValue: NotRequired[int]
    dateValue: NotRequired[datetime]


TimestampTypeDef = Union[datetime, str]


class GetLibraryItemInputRequestTypeDef(TypedDict):
    instanceId: str
    libraryItemId: str
    appId: NotRequired[str]


class GetQAppInputRequestTypeDef(TypedDict):
    instanceId: str
    appId: str


class GetQAppSessionInputRequestTypeDef(TypedDict):
    instanceId: str
    sessionId: str


class ImportDocumentInputRequestTypeDef(TypedDict):
    instanceId: str
    cardId: str
    appId: str
    fileContentsBase64: str
    fileName: str
    scope: DocumentScopeType
    sessionId: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListLibraryItemsInputRequestTypeDef(TypedDict):
    instanceId: str
    limit: NotRequired[int]
    nextToken: NotRequired[str]
    categoryId: NotRequired[str]


class ListQAppsInputRequestTypeDef(TypedDict):
    instanceId: str
    limit: NotRequired[int]
    nextToken: NotRequired[str]


class UserAppItemTypeDef(TypedDict):
    appId: str
    appArn: str
    title: str
    createdAt: datetime
    description: NotRequired[str]
    canEdit: NotRequired[bool]
    status: NotRequired[str]
    isVerified: NotRequired[bool]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str


class StopQAppSessionInputRequestTypeDef(TypedDict):
    instanceId: str
    sessionId: str


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceARN: str
    tagKeys: Sequence[str]


class UpdateLibraryItemInputRequestTypeDef(TypedDict):
    instanceId: str
    libraryItemId: str
    status: NotRequired[LibraryItemStatusType]
    categories: NotRequired[Sequence[str]]


class UpdateLibraryItemMetadataInputRequestTypeDef(TypedDict):
    instanceId: str
    libraryItemId: str
    isVerified: NotRequired[bool]


class StartQAppSessionInputRequestTypeDef(TypedDict):
    instanceId: str
    appId: str
    appVersion: int
    initialValues: NotRequired[Sequence[CardValueTypeDef]]
    tags: NotRequired[Mapping[str, str]]


class UpdateQAppSessionInputRequestTypeDef(TypedDict):
    instanceId: str
    sessionId: str
    values: NotRequired[Sequence[CardValueTypeDef]]


class LibraryItemMemberTypeDef(TypedDict):
    libraryItemId: str
    appId: str
    appVersion: int
    categories: List[CategoryTypeDef]
    status: str
    createdAt: datetime
    createdBy: str
    ratingCount: int
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]
    isRatedByUser: NotRequired[bool]
    userCount: NotRequired[int]
    isVerified: NotRequired[bool]


class PredictQAppInputOptionsTypeDef(TypedDict):
    conversation: NotRequired[Sequence[ConversationMessageTypeDef]]
    problemStatement: NotRequired[str]


class CreateLibraryItemOutputTypeDef(TypedDict):
    libraryItemId: str
    status: str
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    ratingCount: int
    isVerified: bool
    ResponseMetadata: ResponseMetadataTypeDef


class CreateQAppOutputTypeDef(TypedDict):
    appId: str
    appArn: str
    title: str
    description: str
    initialPrompt: str
    appVersion: int
    status: AppStatusType
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    requiredCapabilities: List[AppRequiredCapabilityType]
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetLibraryItemOutputTypeDef(TypedDict):
    libraryItemId: str
    appId: str
    appVersion: int
    categories: List[CategoryTypeDef]
    status: str
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    ratingCount: int
    isRatedByUser: bool
    userCount: int
    isVerified: bool
    ResponseMetadata: ResponseMetadataTypeDef


class GetQAppSessionOutputTypeDef(TypedDict):
    sessionId: str
    sessionArn: str
    status: ExecutionStatusType
    cardStatus: Dict[str, CardStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ImportDocumentOutputTypeDef(TypedDict):
    fileId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class StartQAppSessionOutputTypeDef(TypedDict):
    sessionId: str
    sessionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateLibraryItemOutputTypeDef(TypedDict):
    libraryItemId: str
    appId: str
    appVersion: int
    categories: List[CategoryTypeDef]
    status: str
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    ratingCount: int
    isRatedByUser: bool
    userCount: int
    isVerified: bool
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateQAppOutputTypeDef(TypedDict):
    appId: str
    appArn: str
    title: str
    description: str
    initialPrompt: str
    appVersion: int
    status: AppStatusType
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    requiredCapabilities: List[AppRequiredCapabilityType]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateQAppSessionOutputTypeDef(TypedDict):
    sessionId: str
    sessionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DocumentAttributeOutputTypeDef(TypedDict):
    name: str
    value: DocumentAttributeValueOutputTypeDef


class DocumentAttributeValueTypeDef(TypedDict):
    stringValue: NotRequired[str]
    stringListValue: NotRequired[Sequence[str]]
    longValue: NotRequired[int]
    dateValue: NotRequired[TimestampTypeDef]


class ListLibraryItemsInputListLibraryItemsPaginateTypeDef(TypedDict):
    instanceId: str
    categoryId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListQAppsInputListQAppsPaginateTypeDef(TypedDict):
    instanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListQAppsOutputTypeDef(TypedDict):
    apps: List[UserAppItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListLibraryItemsOutputTypeDef(TypedDict):
    libraryItems: List[LibraryItemMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PredictQAppInputRequestTypeDef(TypedDict):
    instanceId: str
    options: NotRequired[PredictQAppInputOptionsTypeDef]


class AttributeFilterOutputTypeDef(TypedDict):
    andAllFilters: NotRequired[List[Dict[str, Any]]]
    orAllFilters: NotRequired[List[Dict[str, Any]]]
    notFilter: NotRequired[Dict[str, Any]]
    equalsTo: NotRequired[DocumentAttributeOutputTypeDef]
    containsAll: NotRequired[DocumentAttributeOutputTypeDef]
    containsAny: NotRequired[DocumentAttributeOutputTypeDef]
    greaterThan: NotRequired[DocumentAttributeOutputTypeDef]
    greaterThanOrEquals: NotRequired[DocumentAttributeOutputTypeDef]
    lessThan: NotRequired[DocumentAttributeOutputTypeDef]
    lessThanOrEquals: NotRequired[DocumentAttributeOutputTypeDef]


DocumentAttributeValueUnionTypeDef = Union[
    DocumentAttributeValueTypeDef, DocumentAttributeValueOutputTypeDef
]
QQueryCardInputOutputTypeDef = TypedDict(
    "QQueryCardInputOutputTypeDef",
    {
        "title": str,
        "id": str,
        "type": CardTypeType,
        "prompt": str,
        "outputSource": NotRequired[CardOutputSourceType],
        "attributeFilter": NotRequired[AttributeFilterOutputTypeDef],
    },
)
QQueryCardTypeDef = TypedDict(
    "QQueryCardTypeDef",
    {
        "id": str,
        "title": str,
        "dependencies": List[str],
        "type": CardTypeType,
        "prompt": str,
        "outputSource": CardOutputSourceType,
        "attributeFilter": NotRequired[AttributeFilterOutputTypeDef],
    },
)


class DocumentAttributeTypeDef(TypedDict):
    name: str
    value: DocumentAttributeValueUnionTypeDef


class CardInputOutputTypeDef(TypedDict):
    textInput: NotRequired[TextInputCardInputTypeDef]
    qQuery: NotRequired[QQueryCardInputOutputTypeDef]
    qPlugin: NotRequired[QPluginCardInputTypeDef]
    fileUpload: NotRequired[FileUploadCardInputTypeDef]


class CardTypeDef(TypedDict):
    textInput: NotRequired[TextInputCardTypeDef]
    qQuery: NotRequired[QQueryCardTypeDef]
    qPlugin: NotRequired[QPluginCardTypeDef]
    fileUpload: NotRequired[FileUploadCardTypeDef]


DocumentAttributeUnionTypeDef = Union[DocumentAttributeTypeDef, DocumentAttributeOutputTypeDef]


class AppDefinitionInputOutputTypeDef(TypedDict):
    cards: List[CardInputOutputTypeDef]
    initialPrompt: NotRequired[str]


class AppDefinitionTypeDef(TypedDict):
    appDefinitionVersion: str
    cards: List[CardTypeDef]
    canEdit: NotRequired[bool]


class AttributeFilterTypeDef(TypedDict):
    andAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    orAllFilters: NotRequired[Sequence[Mapping[str, Any]]]
    notFilter: NotRequired[Mapping[str, Any]]
    equalsTo: NotRequired[DocumentAttributeUnionTypeDef]
    containsAll: NotRequired[DocumentAttributeUnionTypeDef]
    containsAny: NotRequired[DocumentAttributeUnionTypeDef]
    greaterThan: NotRequired[DocumentAttributeUnionTypeDef]
    greaterThanOrEquals: NotRequired[DocumentAttributeUnionTypeDef]
    lessThan: NotRequired[DocumentAttributeUnionTypeDef]
    lessThanOrEquals: NotRequired[DocumentAttributeUnionTypeDef]


class PredictAppDefinitionTypeDef(TypedDict):
    title: str
    appDefinition: AppDefinitionInputOutputTypeDef
    description: NotRequired[str]


class GetQAppOutputTypeDef(TypedDict):
    appId: str
    appArn: str
    title: str
    description: str
    initialPrompt: str
    appVersion: int
    status: AppStatusType
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    requiredCapabilities: List[AppRequiredCapabilityType]
    appDefinition: AppDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


AttributeFilterUnionTypeDef = Union[AttributeFilterTypeDef, AttributeFilterOutputTypeDef]


class PredictQAppOutputTypeDef(TypedDict):
    app: PredictAppDefinitionTypeDef
    problemStatement: str
    ResponseMetadata: ResponseMetadataTypeDef


QQueryCardInputTypeDef = TypedDict(
    "QQueryCardInputTypeDef",
    {
        "title": str,
        "id": str,
        "type": CardTypeType,
        "prompt": str,
        "outputSource": NotRequired[CardOutputSourceType],
        "attributeFilter": NotRequired[AttributeFilterUnionTypeDef],
    },
)
QQueryCardInputUnionTypeDef = Union[QQueryCardInputTypeDef, QQueryCardInputOutputTypeDef]


class CardInputTypeDef(TypedDict):
    textInput: NotRequired[TextInputCardInputTypeDef]
    qQuery: NotRequired[QQueryCardInputUnionTypeDef]
    qPlugin: NotRequired[QPluginCardInputTypeDef]
    fileUpload: NotRequired[FileUploadCardInputTypeDef]


CardInputUnionTypeDef = Union[CardInputTypeDef, CardInputOutputTypeDef]


class AppDefinitionInputTypeDef(TypedDict):
    cards: Sequence[CardInputUnionTypeDef]
    initialPrompt: NotRequired[str]


class CreateQAppInputRequestTypeDef(TypedDict):
    instanceId: str
    title: str
    appDefinition: AppDefinitionInputTypeDef
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class UpdateQAppInputRequestTypeDef(TypedDict):
    instanceId: str
    appId: str
    title: NotRequired[str]
    description: NotRequired[str]
    appDefinition: NotRequired[AppDefinitionInputTypeDef]
