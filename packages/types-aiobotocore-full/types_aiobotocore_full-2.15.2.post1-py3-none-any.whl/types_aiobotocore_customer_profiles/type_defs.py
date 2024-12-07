"""
Type annotations for customer-profiles service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/type_defs/)

Usage::

    ```python
    from types_aiobotocore_customer_profiles.type_defs import AddProfileKeyRequestRequestTypeDef

    data: AddProfileKeyRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AttributeMatchingModelType,
    ConflictResolvingModelType,
    DataPullModeType,
    EventStreamDestinationStatusType,
    EventStreamStateType,
    FieldContentTypeType,
    GenderType,
    IdentityResolutionJobStatusType,
    JobScheduleDayOfTheWeekType,
    LogicalOperatorType,
    MarketoConnectorOperatorType,
    MatchTypeType,
    OperatorPropertiesKeysType,
    OperatorType,
    PartyTypeType,
    RuleBasedMatchingStatusType,
    S3ConnectorOperatorType,
    SalesforceConnectorOperatorType,
    ServiceNowConnectorOperatorType,
    SourceConnectorTypeType,
    StandardIdentifierType,
    StatisticType,
    StatusType,
    TaskTypeType,
    TriggerTypeType,
    ZendeskConnectorOperatorType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AddProfileKeyRequestRequestTypeDef",
    "AddProfileKeyResponseTypeDef",
    "AdditionalSearchKeyTypeDef",
    "AddressTypeDef",
    "AppflowIntegrationTypeDef",
    "AppflowIntegrationWorkflowAttributesTypeDef",
    "AppflowIntegrationWorkflowMetricsTypeDef",
    "AppflowIntegrationWorkflowStepTypeDef",
    "AttributeDetailsOutputTypeDef",
    "AttributeDetailsTypeDef",
    "AttributeItemTypeDef",
    "AttributeTypesSelectorOutputTypeDef",
    "AttributeTypesSelectorTypeDef",
    "AttributeTypesSelectorUnionTypeDef",
    "AutoMergingOutputTypeDef",
    "AutoMergingTypeDef",
    "AutoMergingUnionTypeDef",
    "BatchTypeDef",
    "ConditionsTypeDef",
    "ConflictResolutionTypeDef",
    "ConnectorOperatorTypeDef",
    "ConsolidationOutputTypeDef",
    "ConsolidationTypeDef",
    "ConsolidationUnionTypeDef",
    "CreateCalculatedAttributeDefinitionRequestRequestTypeDef",
    "CreateCalculatedAttributeDefinitionResponseTypeDef",
    "CreateDomainRequestRequestTypeDef",
    "CreateDomainResponseTypeDef",
    "CreateEventStreamRequestRequestTypeDef",
    "CreateEventStreamResponseTypeDef",
    "CreateIntegrationWorkflowRequestRequestTypeDef",
    "CreateIntegrationWorkflowResponseTypeDef",
    "CreateProfileRequestRequestTypeDef",
    "CreateProfileResponseTypeDef",
    "DeleteCalculatedAttributeDefinitionRequestRequestTypeDef",
    "DeleteDomainRequestRequestTypeDef",
    "DeleteDomainResponseTypeDef",
    "DeleteEventStreamRequestRequestTypeDef",
    "DeleteIntegrationRequestRequestTypeDef",
    "DeleteIntegrationResponseTypeDef",
    "DeleteProfileKeyRequestRequestTypeDef",
    "DeleteProfileKeyResponseTypeDef",
    "DeleteProfileObjectRequestRequestTypeDef",
    "DeleteProfileObjectResponseTypeDef",
    "DeleteProfileObjectTypeRequestRequestTypeDef",
    "DeleteProfileObjectTypeResponseTypeDef",
    "DeleteProfileRequestRequestTypeDef",
    "DeleteProfileResponseTypeDef",
    "DeleteWorkflowRequestRequestTypeDef",
    "DestinationSummaryTypeDef",
    "DetectProfileObjectTypeRequestRequestTypeDef",
    "DetectProfileObjectTypeResponseTypeDef",
    "DetectedProfileObjectTypeTypeDef",
    "DomainStatsTypeDef",
    "EventStreamDestinationDetailsTypeDef",
    "EventStreamSummaryTypeDef",
    "ExportingConfigTypeDef",
    "ExportingLocationTypeDef",
    "FieldSourceProfileIdsTypeDef",
    "FlowDefinitionTypeDef",
    "FoundByKeyValueTypeDef",
    "GetAutoMergingPreviewRequestRequestTypeDef",
    "GetAutoMergingPreviewResponseTypeDef",
    "GetCalculatedAttributeDefinitionRequestRequestTypeDef",
    "GetCalculatedAttributeDefinitionResponseTypeDef",
    "GetCalculatedAttributeForProfileRequestRequestTypeDef",
    "GetCalculatedAttributeForProfileResponseTypeDef",
    "GetDomainRequestRequestTypeDef",
    "GetDomainResponseTypeDef",
    "GetEventStreamRequestRequestTypeDef",
    "GetEventStreamResponseTypeDef",
    "GetIdentityResolutionJobRequestRequestTypeDef",
    "GetIdentityResolutionJobResponseTypeDef",
    "GetIntegrationRequestRequestTypeDef",
    "GetIntegrationResponseTypeDef",
    "GetMatchesRequestRequestTypeDef",
    "GetMatchesResponseTypeDef",
    "GetProfileObjectTypeRequestRequestTypeDef",
    "GetProfileObjectTypeResponseTypeDef",
    "GetProfileObjectTypeTemplateRequestRequestTypeDef",
    "GetProfileObjectTypeTemplateResponseTypeDef",
    "GetSimilarProfilesRequestRequestTypeDef",
    "GetSimilarProfilesResponseTypeDef",
    "GetWorkflowRequestRequestTypeDef",
    "GetWorkflowResponseTypeDef",
    "GetWorkflowStepsRequestRequestTypeDef",
    "GetWorkflowStepsResponseTypeDef",
    "IdentityResolutionJobTypeDef",
    "IncrementalPullConfigTypeDef",
    "IntegrationConfigTypeDef",
    "JobScheduleTypeDef",
    "JobStatsTypeDef",
    "ListAccountIntegrationsRequestRequestTypeDef",
    "ListAccountIntegrationsResponseTypeDef",
    "ListCalculatedAttributeDefinitionItemTypeDef",
    "ListCalculatedAttributeDefinitionsRequestRequestTypeDef",
    "ListCalculatedAttributeDefinitionsResponseTypeDef",
    "ListCalculatedAttributeForProfileItemTypeDef",
    "ListCalculatedAttributesForProfileRequestRequestTypeDef",
    "ListCalculatedAttributesForProfileResponseTypeDef",
    "ListDomainItemTypeDef",
    "ListDomainsRequestRequestTypeDef",
    "ListDomainsResponseTypeDef",
    "ListEventStreamsRequestListEventStreamsPaginateTypeDef",
    "ListEventStreamsRequestRequestTypeDef",
    "ListEventStreamsResponseTypeDef",
    "ListIdentityResolutionJobsRequestRequestTypeDef",
    "ListIdentityResolutionJobsResponseTypeDef",
    "ListIntegrationItemTypeDef",
    "ListIntegrationsRequestRequestTypeDef",
    "ListIntegrationsResponseTypeDef",
    "ListProfileObjectTypeItemTypeDef",
    "ListProfileObjectTypeTemplateItemTypeDef",
    "ListProfileObjectTypeTemplatesRequestRequestTypeDef",
    "ListProfileObjectTypeTemplatesResponseTypeDef",
    "ListProfileObjectTypesRequestRequestTypeDef",
    "ListProfileObjectTypesResponseTypeDef",
    "ListProfileObjectsItemTypeDef",
    "ListProfileObjectsRequestRequestTypeDef",
    "ListProfileObjectsResponseTypeDef",
    "ListRuleBasedMatchesRequestRequestTypeDef",
    "ListRuleBasedMatchesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListWorkflowsItemTypeDef",
    "ListWorkflowsRequestRequestTypeDef",
    "ListWorkflowsResponseTypeDef",
    "MarketoSourcePropertiesTypeDef",
    "MatchItemTypeDef",
    "MatchingRequestTypeDef",
    "MatchingResponseTypeDef",
    "MatchingRuleOutputTypeDef",
    "MatchingRuleTypeDef",
    "MatchingRuleUnionTypeDef",
    "MergeProfilesRequestRequestTypeDef",
    "MergeProfilesResponseTypeDef",
    "ObjectFilterTypeDef",
    "ObjectTypeFieldTypeDef",
    "ObjectTypeKeyOutputTypeDef",
    "ObjectTypeKeyTypeDef",
    "ObjectTypeKeyUnionTypeDef",
    "PaginatorConfigTypeDef",
    "ProfileTypeDef",
    "PutIntegrationRequestRequestTypeDef",
    "PutIntegrationResponseTypeDef",
    "PutProfileObjectRequestRequestTypeDef",
    "PutProfileObjectResponseTypeDef",
    "PutProfileObjectTypeRequestRequestTypeDef",
    "PutProfileObjectTypeResponseTypeDef",
    "RangeTypeDef",
    "ResponseMetadataTypeDef",
    "RuleBasedMatchingRequestTypeDef",
    "RuleBasedMatchingResponseTypeDef",
    "S3ExportingConfigTypeDef",
    "S3ExportingLocationTypeDef",
    "S3SourcePropertiesTypeDef",
    "SalesforceSourcePropertiesTypeDef",
    "ScheduledTriggerPropertiesTypeDef",
    "SearchProfilesRequestRequestTypeDef",
    "SearchProfilesResponseTypeDef",
    "ServiceNowSourcePropertiesTypeDef",
    "SourceConnectorPropertiesTypeDef",
    "SourceFlowConfigTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TaskTypeDef",
    "ThresholdTypeDef",
    "TimestampTypeDef",
    "TriggerConfigTypeDef",
    "TriggerPropertiesTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAddressTypeDef",
    "UpdateCalculatedAttributeDefinitionRequestRequestTypeDef",
    "UpdateCalculatedAttributeDefinitionResponseTypeDef",
    "UpdateDomainRequestRequestTypeDef",
    "UpdateDomainResponseTypeDef",
    "UpdateProfileRequestRequestTypeDef",
    "UpdateProfileResponseTypeDef",
    "WorkflowAttributesTypeDef",
    "WorkflowMetricsTypeDef",
    "WorkflowStepItemTypeDef",
    "ZendeskSourcePropertiesTypeDef",
)


class AddProfileKeyRequestRequestTypeDef(TypedDict):
    ProfileId: str
    KeyName: str
    Values: Sequence[str]
    DomainName: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AdditionalSearchKeyTypeDef(TypedDict):
    KeyName: str
    Values: Sequence[str]


class AddressTypeDef(TypedDict):
    Address1: NotRequired[str]
    Address2: NotRequired[str]
    Address3: NotRequired[str]
    Address4: NotRequired[str]
    City: NotRequired[str]
    County: NotRequired[str]
    State: NotRequired[str]
    Province: NotRequired[str]
    Country: NotRequired[str]
    PostalCode: NotRequired[str]


class AppflowIntegrationWorkflowAttributesTypeDef(TypedDict):
    SourceConnectorType: SourceConnectorTypeType
    ConnectorProfileName: str
    RoleArn: NotRequired[str]


class AppflowIntegrationWorkflowMetricsTypeDef(TypedDict):
    RecordsProcessed: int
    StepsCompleted: int
    TotalSteps: int


class AppflowIntegrationWorkflowStepTypeDef(TypedDict):
    FlowName: str
    Status: StatusType
    ExecutionMessage: str
    RecordsProcessed: int
    BatchRecordsStartTime: str
    BatchRecordsEndTime: str
    CreatedAt: datetime
    LastUpdatedAt: datetime


class AttributeItemTypeDef(TypedDict):
    Name: str


class AttributeTypesSelectorOutputTypeDef(TypedDict):
    AttributeMatchingModel: AttributeMatchingModelType
    Address: NotRequired[List[str]]
    PhoneNumber: NotRequired[List[str]]
    EmailAddress: NotRequired[List[str]]


class AttributeTypesSelectorTypeDef(TypedDict):
    AttributeMatchingModel: AttributeMatchingModelType
    Address: NotRequired[Sequence[str]]
    PhoneNumber: NotRequired[Sequence[str]]
    EmailAddress: NotRequired[Sequence[str]]


class ConflictResolutionTypeDef(TypedDict):
    ConflictResolvingModel: ConflictResolvingModelType
    SourceName: NotRequired[str]


class ConsolidationOutputTypeDef(TypedDict):
    MatchingAttributesList: List[List[str]]


TimestampTypeDef = Union[datetime, str]


class RangeTypeDef(TypedDict):
    Value: int
    Unit: Literal["DAYS"]


class ThresholdTypeDef(TypedDict):
    Value: str
    Operator: OperatorType


class ConnectorOperatorTypeDef(TypedDict):
    Marketo: NotRequired[MarketoConnectorOperatorType]
    S3: NotRequired[S3ConnectorOperatorType]
    Salesforce: NotRequired[SalesforceConnectorOperatorType]
    ServiceNow: NotRequired[ServiceNowConnectorOperatorType]
    Zendesk: NotRequired[ZendeskConnectorOperatorType]


class ConsolidationTypeDef(TypedDict):
    MatchingAttributesList: Sequence[Sequence[str]]


class CreateEventStreamRequestRequestTypeDef(TypedDict):
    DomainName: str
    Uri: str
    EventStreamName: str
    Tags: NotRequired[Mapping[str, str]]


class DeleteCalculatedAttributeDefinitionRequestRequestTypeDef(TypedDict):
    DomainName: str
    CalculatedAttributeName: str


class DeleteDomainRequestRequestTypeDef(TypedDict):
    DomainName: str


class DeleteEventStreamRequestRequestTypeDef(TypedDict):
    DomainName: str
    EventStreamName: str


class DeleteIntegrationRequestRequestTypeDef(TypedDict):
    DomainName: str
    Uri: str


class DeleteProfileKeyRequestRequestTypeDef(TypedDict):
    ProfileId: str
    KeyName: str
    Values: Sequence[str]
    DomainName: str


class DeleteProfileObjectRequestRequestTypeDef(TypedDict):
    ProfileId: str
    ProfileObjectUniqueKey: str
    ObjectTypeName: str
    DomainName: str


class DeleteProfileObjectTypeRequestRequestTypeDef(TypedDict):
    DomainName: str
    ObjectTypeName: str


class DeleteProfileRequestRequestTypeDef(TypedDict):
    ProfileId: str
    DomainName: str


class DeleteWorkflowRequestRequestTypeDef(TypedDict):
    DomainName: str
    WorkflowId: str


class DestinationSummaryTypeDef(TypedDict):
    Uri: str
    Status: EventStreamDestinationStatusType
    UnhealthySince: NotRequired[datetime]


class DetectProfileObjectTypeRequestRequestTypeDef(TypedDict):
    Objects: Sequence[str]
    DomainName: str


class ObjectTypeFieldTypeDef(TypedDict):
    Source: NotRequired[str]
    Target: NotRequired[str]
    ContentType: NotRequired[FieldContentTypeType]


class ObjectTypeKeyOutputTypeDef(TypedDict):
    StandardIdentifiers: NotRequired[List[StandardIdentifierType]]
    FieldNames: NotRequired[List[str]]


class DomainStatsTypeDef(TypedDict):
    ProfileCount: NotRequired[int]
    MeteringProfileCount: NotRequired[int]
    ObjectCount: NotRequired[int]
    TotalSize: NotRequired[int]


class EventStreamDestinationDetailsTypeDef(TypedDict):
    Uri: str
    Status: EventStreamDestinationStatusType
    UnhealthySince: NotRequired[datetime]
    Message: NotRequired[str]


class S3ExportingConfigTypeDef(TypedDict):
    S3BucketName: str
    S3KeyName: NotRequired[str]


class S3ExportingLocationTypeDef(TypedDict):
    S3BucketName: NotRequired[str]
    S3KeyName: NotRequired[str]


class FieldSourceProfileIdsTypeDef(TypedDict):
    AccountNumber: NotRequired[str]
    AdditionalInformation: NotRequired[str]
    PartyType: NotRequired[str]
    BusinessName: NotRequired[str]
    FirstName: NotRequired[str]
    MiddleName: NotRequired[str]
    LastName: NotRequired[str]
    BirthDate: NotRequired[str]
    Gender: NotRequired[str]
    PhoneNumber: NotRequired[str]
    MobilePhoneNumber: NotRequired[str]
    HomePhoneNumber: NotRequired[str]
    BusinessPhoneNumber: NotRequired[str]
    EmailAddress: NotRequired[str]
    PersonalEmailAddress: NotRequired[str]
    BusinessEmailAddress: NotRequired[str]
    Address: NotRequired[str]
    ShippingAddress: NotRequired[str]
    MailingAddress: NotRequired[str]
    BillingAddress: NotRequired[str]
    Attributes: NotRequired[Mapping[str, str]]


class FoundByKeyValueTypeDef(TypedDict):
    KeyName: NotRequired[str]
    Values: NotRequired[List[str]]


class GetCalculatedAttributeDefinitionRequestRequestTypeDef(TypedDict):
    DomainName: str
    CalculatedAttributeName: str


class GetCalculatedAttributeForProfileRequestRequestTypeDef(TypedDict):
    DomainName: str
    ProfileId: str
    CalculatedAttributeName: str


class GetDomainRequestRequestTypeDef(TypedDict):
    DomainName: str


class GetEventStreamRequestRequestTypeDef(TypedDict):
    DomainName: str
    EventStreamName: str


class GetIdentityResolutionJobRequestRequestTypeDef(TypedDict):
    DomainName: str
    JobId: str


class JobStatsTypeDef(TypedDict):
    NumberOfProfilesReviewed: NotRequired[int]
    NumberOfMatchesFound: NotRequired[int]
    NumberOfMergesDone: NotRequired[int]


class GetIntegrationRequestRequestTypeDef(TypedDict):
    DomainName: str
    Uri: str


class GetMatchesRequestRequestTypeDef(TypedDict):
    DomainName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class MatchItemTypeDef(TypedDict):
    MatchId: NotRequired[str]
    ProfileIds: NotRequired[List[str]]
    ConfidenceScore: NotRequired[float]


class GetProfileObjectTypeRequestRequestTypeDef(TypedDict):
    DomainName: str
    ObjectTypeName: str


class GetProfileObjectTypeTemplateRequestRequestTypeDef(TypedDict):
    TemplateId: str


class GetSimilarProfilesRequestRequestTypeDef(TypedDict):
    DomainName: str
    MatchType: MatchTypeType
    SearchKey: str
    SearchValue: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class GetWorkflowRequestRequestTypeDef(TypedDict):
    DomainName: str
    WorkflowId: str


class GetWorkflowStepsRequestRequestTypeDef(TypedDict):
    DomainName: str
    WorkflowId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class IncrementalPullConfigTypeDef(TypedDict):
    DatetimeTypeFieldName: NotRequired[str]


class JobScheduleTypeDef(TypedDict):
    DayOfTheWeek: JobScheduleDayOfTheWeekType
    Time: str


class ListAccountIntegrationsRequestRequestTypeDef(TypedDict):
    Uri: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    IncludeHidden: NotRequired[bool]


class ListIntegrationItemTypeDef(TypedDict):
    DomainName: str
    Uri: str
    CreatedAt: datetime
    LastUpdatedAt: datetime
    ObjectTypeName: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]
    ObjectTypeNames: NotRequired[Dict[str, str]]
    WorkflowId: NotRequired[str]
    IsUnstructured: NotRequired[bool]
    RoleArn: NotRequired[str]


class ListCalculatedAttributeDefinitionItemTypeDef(TypedDict):
    CalculatedAttributeName: NotRequired[str]
    DisplayName: NotRequired[str]
    Description: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    LastUpdatedAt: NotRequired[datetime]
    Tags: NotRequired[Dict[str, str]]


class ListCalculatedAttributeDefinitionsRequestRequestTypeDef(TypedDict):
    DomainName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListCalculatedAttributeForProfileItemTypeDef(TypedDict):
    CalculatedAttributeName: NotRequired[str]
    DisplayName: NotRequired[str]
    IsDataPartial: NotRequired[str]
    Value: NotRequired[str]


class ListCalculatedAttributesForProfileRequestRequestTypeDef(TypedDict):
    DomainName: str
    ProfileId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDomainItemTypeDef(TypedDict):
    DomainName: str
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Tags: NotRequired[Dict[str, str]]


class ListDomainsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListEventStreamsRequestRequestTypeDef(TypedDict):
    DomainName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListIdentityResolutionJobsRequestRequestTypeDef(TypedDict):
    DomainName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListIntegrationsRequestRequestTypeDef(TypedDict):
    DomainName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    IncludeHidden: NotRequired[bool]


class ListProfileObjectTypeItemTypeDef(TypedDict):
    ObjectTypeName: str
    Description: str
    CreatedAt: NotRequired[datetime]
    LastUpdatedAt: NotRequired[datetime]
    MaxProfileObjectCount: NotRequired[int]
    MaxAvailableProfileObjectCount: NotRequired[int]
    Tags: NotRequired[Dict[str, str]]


class ListProfileObjectTypeTemplateItemTypeDef(TypedDict):
    TemplateId: NotRequired[str]
    SourceName: NotRequired[str]
    SourceObject: NotRequired[str]


class ListProfileObjectTypeTemplatesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListProfileObjectTypesRequestRequestTypeDef(TypedDict):
    DomainName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListProfileObjectsItemTypeDef(TypedDict):
    ObjectTypeName: NotRequired[str]
    ProfileObjectUniqueKey: NotRequired[str]
    Object: NotRequired[str]


class ObjectFilterTypeDef(TypedDict):
    KeyName: str
    Values: Sequence[str]


class ListRuleBasedMatchesRequestRequestTypeDef(TypedDict):
    DomainName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class ListWorkflowsItemTypeDef(TypedDict):
    WorkflowType: Literal["APPFLOW_INTEGRATION"]
    WorkflowId: str
    Status: StatusType
    StatusDescription: str
    CreatedAt: datetime
    LastUpdatedAt: datetime


class MarketoSourcePropertiesTypeDef(TypedDict):
    Object: str


class MatchingRuleOutputTypeDef(TypedDict):
    Rule: List[str]


class MatchingRuleTypeDef(TypedDict):
    Rule: Sequence[str]


class ObjectTypeKeyTypeDef(TypedDict):
    StandardIdentifiers: NotRequired[Sequence[StandardIdentifierType]]
    FieldNames: NotRequired[Sequence[str]]


class PutProfileObjectRequestRequestTypeDef(TypedDict):
    ObjectTypeName: str
    Object: str
    DomainName: str


class S3SourcePropertiesTypeDef(TypedDict):
    BucketName: str
    BucketPrefix: NotRequired[str]


class SalesforceSourcePropertiesTypeDef(TypedDict):
    Object: str
    EnableDynamicFieldUpdate: NotRequired[bool]
    IncludeDeletedRecords: NotRequired[bool]


class ServiceNowSourcePropertiesTypeDef(TypedDict):
    Object: str


class ZendeskSourcePropertiesTypeDef(TypedDict):
    Object: str


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateAddressTypeDef(TypedDict):
    Address1: NotRequired[str]
    Address2: NotRequired[str]
    Address3: NotRequired[str]
    Address4: NotRequired[str]
    City: NotRequired[str]
    County: NotRequired[str]
    State: NotRequired[str]
    Province: NotRequired[str]
    Country: NotRequired[str]
    PostalCode: NotRequired[str]


class AddProfileKeyResponseTypeDef(TypedDict):
    KeyName: str
    Values: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEventStreamResponseTypeDef(TypedDict):
    EventStreamArn: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIntegrationWorkflowResponseTypeDef(TypedDict):
    WorkflowId: str
    Message: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProfileResponseTypeDef(TypedDict):
    ProfileId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDomainResponseTypeDef(TypedDict):
    Message: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteIntegrationResponseTypeDef(TypedDict):
    Message: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteProfileKeyResponseTypeDef(TypedDict):
    Message: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteProfileObjectResponseTypeDef(TypedDict):
    Message: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteProfileObjectTypeResponseTypeDef(TypedDict):
    Message: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteProfileResponseTypeDef(TypedDict):
    Message: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetAutoMergingPreviewResponseTypeDef(TypedDict):
    DomainName: str
    NumberOfMatchesInSample: int
    NumberOfProfilesInSample: int
    NumberOfProfilesWillBeMerged: int
    ResponseMetadata: ResponseMetadataTypeDef


class GetCalculatedAttributeForProfileResponseTypeDef(TypedDict):
    CalculatedAttributeName: str
    DisplayName: str
    IsDataPartial: str
    Value: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetIntegrationResponseTypeDef(TypedDict):
    DomainName: str
    Uri: str
    ObjectTypeName: str
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Tags: Dict[str, str]
    ObjectTypeNames: Dict[str, str]
    WorkflowId: str
    IsUnstructured: bool
    RoleArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetSimilarProfilesResponseTypeDef(TypedDict):
    ProfileIds: List[str]
    MatchId: str
    MatchType: MatchTypeType
    RuleLevel: int
    ConfidenceScore: float
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRuleBasedMatchesResponseTypeDef(TypedDict):
    MatchIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class MergeProfilesResponseTypeDef(TypedDict):
    Message: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutIntegrationResponseTypeDef(TypedDict):
    DomainName: str
    Uri: str
    ObjectTypeName: str
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Tags: Dict[str, str]
    ObjectTypeNames: Dict[str, str]
    WorkflowId: str
    IsUnstructured: bool
    RoleArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutProfileObjectResponseTypeDef(TypedDict):
    ProfileObjectUniqueKey: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateProfileResponseTypeDef(TypedDict):
    ProfileId: str
    ResponseMetadata: ResponseMetadataTypeDef


class SearchProfilesRequestRequestTypeDef(TypedDict):
    DomainName: str
    KeyName: str
    Values: Sequence[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    AdditionalSearchKeys: NotRequired[Sequence[AdditionalSearchKeyTypeDef]]
    LogicalOperator: NotRequired[LogicalOperatorType]


class CreateProfileRequestRequestTypeDef(TypedDict):
    DomainName: str
    AccountNumber: NotRequired[str]
    AdditionalInformation: NotRequired[str]
    PartyType: NotRequired[PartyTypeType]
    BusinessName: NotRequired[str]
    FirstName: NotRequired[str]
    MiddleName: NotRequired[str]
    LastName: NotRequired[str]
    BirthDate: NotRequired[str]
    Gender: NotRequired[GenderType]
    PhoneNumber: NotRequired[str]
    MobilePhoneNumber: NotRequired[str]
    HomePhoneNumber: NotRequired[str]
    BusinessPhoneNumber: NotRequired[str]
    EmailAddress: NotRequired[str]
    PersonalEmailAddress: NotRequired[str]
    BusinessEmailAddress: NotRequired[str]
    Address: NotRequired[AddressTypeDef]
    ShippingAddress: NotRequired[AddressTypeDef]
    MailingAddress: NotRequired[AddressTypeDef]
    BillingAddress: NotRequired[AddressTypeDef]
    Attributes: NotRequired[Mapping[str, str]]
    PartyTypeString: NotRequired[str]
    GenderString: NotRequired[str]


class WorkflowAttributesTypeDef(TypedDict):
    AppflowIntegration: NotRequired[AppflowIntegrationWorkflowAttributesTypeDef]


class WorkflowMetricsTypeDef(TypedDict):
    AppflowIntegration: NotRequired[AppflowIntegrationWorkflowMetricsTypeDef]


class WorkflowStepItemTypeDef(TypedDict):
    AppflowIntegration: NotRequired[AppflowIntegrationWorkflowStepTypeDef]


class AttributeDetailsOutputTypeDef(TypedDict):
    Attributes: List[AttributeItemTypeDef]
    Expression: str


class AttributeDetailsTypeDef(TypedDict):
    Attributes: Sequence[AttributeItemTypeDef]
    Expression: str


AttributeTypesSelectorUnionTypeDef = Union[
    AttributeTypesSelectorTypeDef, AttributeTypesSelectorOutputTypeDef
]


class AutoMergingOutputTypeDef(TypedDict):
    Enabled: bool
    Consolidation: NotRequired[ConsolidationOutputTypeDef]
    ConflictResolution: NotRequired[ConflictResolutionTypeDef]
    MinAllowedConfidenceScoreForMerging: NotRequired[float]


class BatchTypeDef(TypedDict):
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef


class ListWorkflowsRequestRequestTypeDef(TypedDict):
    DomainName: str
    WorkflowType: NotRequired[Literal["APPFLOW_INTEGRATION"]]
    Status: NotRequired[StatusType]
    QueryStartDate: NotRequired[TimestampTypeDef]
    QueryEndDate: NotRequired[TimestampTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ScheduledTriggerPropertiesTypeDef(TypedDict):
    ScheduleExpression: str
    DataPullMode: NotRequired[DataPullModeType]
    ScheduleStartTime: NotRequired[TimestampTypeDef]
    ScheduleEndTime: NotRequired[TimestampTypeDef]
    Timezone: NotRequired[str]
    ScheduleOffset: NotRequired[int]
    FirstExecutionFrom: NotRequired[TimestampTypeDef]


class ConditionsTypeDef(TypedDict):
    Range: NotRequired[RangeTypeDef]
    ObjectCount: NotRequired[int]
    Threshold: NotRequired[ThresholdTypeDef]


class TaskTypeDef(TypedDict):
    SourceFields: Sequence[str]
    TaskType: TaskTypeType
    ConnectorOperator: NotRequired[ConnectorOperatorTypeDef]
    DestinationField: NotRequired[str]
    TaskProperties: NotRequired[Mapping[OperatorPropertiesKeysType, str]]


ConsolidationUnionTypeDef = Union[ConsolidationTypeDef, ConsolidationOutputTypeDef]


class GetAutoMergingPreviewRequestRequestTypeDef(TypedDict):
    DomainName: str
    Consolidation: ConsolidationTypeDef
    ConflictResolution: ConflictResolutionTypeDef
    MinAllowedConfidenceScoreForMerging: NotRequired[float]


class EventStreamSummaryTypeDef(TypedDict):
    DomainName: str
    EventStreamName: str
    EventStreamArn: str
    State: EventStreamStateType
    StoppedSince: NotRequired[datetime]
    DestinationSummary: NotRequired[DestinationSummaryTypeDef]
    Tags: NotRequired[Dict[str, str]]


class DetectedProfileObjectTypeTypeDef(TypedDict):
    SourceLastUpdatedTimestampFormat: NotRequired[str]
    Fields: NotRequired[Dict[str, ObjectTypeFieldTypeDef]]
    Keys: NotRequired[Dict[str, List[ObjectTypeKeyOutputTypeDef]]]


class GetProfileObjectTypeResponseTypeDef(TypedDict):
    ObjectTypeName: str
    Description: str
    TemplateId: str
    ExpirationDays: int
    EncryptionKey: str
    AllowProfileCreation: bool
    SourceLastUpdatedTimestampFormat: str
    MaxAvailableProfileObjectCount: int
    MaxProfileObjectCount: int
    Fields: Dict[str, ObjectTypeFieldTypeDef]
    Keys: Dict[str, List[ObjectTypeKeyOutputTypeDef]]
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetProfileObjectTypeTemplateResponseTypeDef(TypedDict):
    TemplateId: str
    SourceName: str
    SourceObject: str
    AllowProfileCreation: bool
    SourceLastUpdatedTimestampFormat: str
    Fields: Dict[str, ObjectTypeFieldTypeDef]
    Keys: Dict[str, List[ObjectTypeKeyOutputTypeDef]]
    ResponseMetadata: ResponseMetadataTypeDef


class PutProfileObjectTypeResponseTypeDef(TypedDict):
    ObjectTypeName: str
    Description: str
    TemplateId: str
    ExpirationDays: int
    EncryptionKey: str
    AllowProfileCreation: bool
    SourceLastUpdatedTimestampFormat: str
    MaxProfileObjectCount: int
    MaxAvailableProfileObjectCount: int
    Fields: Dict[str, ObjectTypeFieldTypeDef]
    Keys: Dict[str, List[ObjectTypeKeyOutputTypeDef]]
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetEventStreamResponseTypeDef(TypedDict):
    DomainName: str
    EventStreamArn: str
    CreatedAt: datetime
    State: EventStreamStateType
    StoppedSince: datetime
    DestinationDetails: EventStreamDestinationDetailsTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ExportingConfigTypeDef(TypedDict):
    S3Exporting: NotRequired[S3ExportingConfigTypeDef]


class ExportingLocationTypeDef(TypedDict):
    S3Exporting: NotRequired[S3ExportingLocationTypeDef]


class MergeProfilesRequestRequestTypeDef(TypedDict):
    DomainName: str
    MainProfileId: str
    ProfileIdsToBeMerged: Sequence[str]
    FieldSourceProfileIds: NotRequired[FieldSourceProfileIdsTypeDef]


class ProfileTypeDef(TypedDict):
    ProfileId: NotRequired[str]
    AccountNumber: NotRequired[str]
    AdditionalInformation: NotRequired[str]
    PartyType: NotRequired[PartyTypeType]
    BusinessName: NotRequired[str]
    FirstName: NotRequired[str]
    MiddleName: NotRequired[str]
    LastName: NotRequired[str]
    BirthDate: NotRequired[str]
    Gender: NotRequired[GenderType]
    PhoneNumber: NotRequired[str]
    MobilePhoneNumber: NotRequired[str]
    HomePhoneNumber: NotRequired[str]
    BusinessPhoneNumber: NotRequired[str]
    EmailAddress: NotRequired[str]
    PersonalEmailAddress: NotRequired[str]
    BusinessEmailAddress: NotRequired[str]
    Address: NotRequired[AddressTypeDef]
    ShippingAddress: NotRequired[AddressTypeDef]
    MailingAddress: NotRequired[AddressTypeDef]
    BillingAddress: NotRequired[AddressTypeDef]
    Attributes: NotRequired[Dict[str, str]]
    FoundByItems: NotRequired[List[FoundByKeyValueTypeDef]]
    PartyTypeString: NotRequired[str]
    GenderString: NotRequired[str]


class GetMatchesResponseTypeDef(TypedDict):
    MatchGenerationDate: datetime
    PotentialMatches: int
    Matches: List[MatchItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListAccountIntegrationsResponseTypeDef(TypedDict):
    Items: List[ListIntegrationItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListIntegrationsResponseTypeDef(TypedDict):
    Items: List[ListIntegrationItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListCalculatedAttributeDefinitionsResponseTypeDef(TypedDict):
    Items: List[ListCalculatedAttributeDefinitionItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListCalculatedAttributesForProfileResponseTypeDef(TypedDict):
    Items: List[ListCalculatedAttributeForProfileItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDomainsResponseTypeDef(TypedDict):
    Items: List[ListDomainItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListEventStreamsRequestListEventStreamsPaginateTypeDef(TypedDict):
    DomainName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProfileObjectTypesResponseTypeDef(TypedDict):
    Items: List[ListProfileObjectTypeItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListProfileObjectTypeTemplatesResponseTypeDef(TypedDict):
    Items: List[ListProfileObjectTypeTemplateItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListProfileObjectsResponseTypeDef(TypedDict):
    Items: List[ListProfileObjectsItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListProfileObjectsRequestRequestTypeDef(TypedDict):
    DomainName: str
    ObjectTypeName: str
    ProfileId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ObjectFilter: NotRequired[ObjectFilterTypeDef]


class ListWorkflowsResponseTypeDef(TypedDict):
    Items: List[ListWorkflowsItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


MatchingRuleUnionTypeDef = Union[MatchingRuleTypeDef, MatchingRuleOutputTypeDef]
ObjectTypeKeyUnionTypeDef = Union[ObjectTypeKeyTypeDef, ObjectTypeKeyOutputTypeDef]


class SourceConnectorPropertiesTypeDef(TypedDict):
    Marketo: NotRequired[MarketoSourcePropertiesTypeDef]
    S3: NotRequired[S3SourcePropertiesTypeDef]
    Salesforce: NotRequired[SalesforceSourcePropertiesTypeDef]
    ServiceNow: NotRequired[ServiceNowSourcePropertiesTypeDef]
    Zendesk: NotRequired[ZendeskSourcePropertiesTypeDef]


class UpdateProfileRequestRequestTypeDef(TypedDict):
    DomainName: str
    ProfileId: str
    AdditionalInformation: NotRequired[str]
    AccountNumber: NotRequired[str]
    PartyType: NotRequired[PartyTypeType]
    BusinessName: NotRequired[str]
    FirstName: NotRequired[str]
    MiddleName: NotRequired[str]
    LastName: NotRequired[str]
    BirthDate: NotRequired[str]
    Gender: NotRequired[GenderType]
    PhoneNumber: NotRequired[str]
    MobilePhoneNumber: NotRequired[str]
    HomePhoneNumber: NotRequired[str]
    BusinessPhoneNumber: NotRequired[str]
    EmailAddress: NotRequired[str]
    PersonalEmailAddress: NotRequired[str]
    BusinessEmailAddress: NotRequired[str]
    Address: NotRequired[UpdateAddressTypeDef]
    ShippingAddress: NotRequired[UpdateAddressTypeDef]
    MailingAddress: NotRequired[UpdateAddressTypeDef]
    BillingAddress: NotRequired[UpdateAddressTypeDef]
    Attributes: NotRequired[Mapping[str, str]]
    PartyTypeString: NotRequired[str]
    GenderString: NotRequired[str]


class GetWorkflowResponseTypeDef(TypedDict):
    WorkflowId: str
    WorkflowType: Literal["APPFLOW_INTEGRATION"]
    Status: StatusType
    ErrorDescription: str
    StartDate: datetime
    LastUpdatedAt: datetime
    Attributes: WorkflowAttributesTypeDef
    Metrics: WorkflowMetricsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetWorkflowStepsResponseTypeDef(TypedDict):
    WorkflowId: str
    WorkflowType: Literal["APPFLOW_INTEGRATION"]
    Items: List[WorkflowStepItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TriggerPropertiesTypeDef(TypedDict):
    Scheduled: NotRequired[ScheduledTriggerPropertiesTypeDef]


class CreateCalculatedAttributeDefinitionRequestRequestTypeDef(TypedDict):
    DomainName: str
    CalculatedAttributeName: str
    AttributeDetails: AttributeDetailsTypeDef
    Statistic: StatisticType
    DisplayName: NotRequired[str]
    Description: NotRequired[str]
    Conditions: NotRequired[ConditionsTypeDef]
    Tags: NotRequired[Mapping[str, str]]


class CreateCalculatedAttributeDefinitionResponseTypeDef(TypedDict):
    CalculatedAttributeName: str
    DisplayName: str
    Description: str
    AttributeDetails: AttributeDetailsOutputTypeDef
    Conditions: ConditionsTypeDef
    Statistic: StatisticType
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetCalculatedAttributeDefinitionResponseTypeDef(TypedDict):
    CalculatedAttributeName: str
    DisplayName: str
    Description: str
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Statistic: StatisticType
    Conditions: ConditionsTypeDef
    AttributeDetails: AttributeDetailsOutputTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCalculatedAttributeDefinitionRequestRequestTypeDef(TypedDict):
    DomainName: str
    CalculatedAttributeName: str
    DisplayName: NotRequired[str]
    Description: NotRequired[str]
    Conditions: NotRequired[ConditionsTypeDef]


class UpdateCalculatedAttributeDefinitionResponseTypeDef(TypedDict):
    CalculatedAttributeName: str
    DisplayName: str
    Description: str
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Statistic: StatisticType
    Conditions: ConditionsTypeDef
    AttributeDetails: AttributeDetailsOutputTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class AutoMergingTypeDef(TypedDict):
    Enabled: bool
    Consolidation: NotRequired[ConsolidationUnionTypeDef]
    ConflictResolution: NotRequired[ConflictResolutionTypeDef]
    MinAllowedConfidenceScoreForMerging: NotRequired[float]


class ListEventStreamsResponseTypeDef(TypedDict):
    Items: List[EventStreamSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DetectProfileObjectTypeResponseTypeDef(TypedDict):
    DetectedProfileObjectTypes: List[DetectedProfileObjectTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class MatchingResponseTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    JobSchedule: NotRequired[JobScheduleTypeDef]
    AutoMerging: NotRequired[AutoMergingOutputTypeDef]
    ExportingConfig: NotRequired[ExportingConfigTypeDef]


class RuleBasedMatchingResponseTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    MatchingRules: NotRequired[List[MatchingRuleOutputTypeDef]]
    Status: NotRequired[RuleBasedMatchingStatusType]
    MaxAllowedRuleLevelForMerging: NotRequired[int]
    MaxAllowedRuleLevelForMatching: NotRequired[int]
    AttributeTypesSelector: NotRequired[AttributeTypesSelectorOutputTypeDef]
    ConflictResolution: NotRequired[ConflictResolutionTypeDef]
    ExportingConfig: NotRequired[ExportingConfigTypeDef]


class GetIdentityResolutionJobResponseTypeDef(TypedDict):
    DomainName: str
    JobId: str
    Status: IdentityResolutionJobStatusType
    Message: str
    JobStartTime: datetime
    JobEndTime: datetime
    LastUpdatedAt: datetime
    JobExpirationTime: datetime
    AutoMerging: AutoMergingOutputTypeDef
    ExportingLocation: ExportingLocationTypeDef
    JobStats: JobStatsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class IdentityResolutionJobTypeDef(TypedDict):
    DomainName: NotRequired[str]
    JobId: NotRequired[str]
    Status: NotRequired[IdentityResolutionJobStatusType]
    JobStartTime: NotRequired[datetime]
    JobEndTime: NotRequired[datetime]
    JobStats: NotRequired[JobStatsTypeDef]
    ExportingLocation: NotRequired[ExportingLocationTypeDef]
    Message: NotRequired[str]


class SearchProfilesResponseTypeDef(TypedDict):
    Items: List[ProfileTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RuleBasedMatchingRequestTypeDef(TypedDict):
    Enabled: bool
    MatchingRules: NotRequired[Sequence[MatchingRuleUnionTypeDef]]
    MaxAllowedRuleLevelForMerging: NotRequired[int]
    MaxAllowedRuleLevelForMatching: NotRequired[int]
    AttributeTypesSelector: NotRequired[AttributeTypesSelectorUnionTypeDef]
    ConflictResolution: NotRequired[ConflictResolutionTypeDef]
    ExportingConfig: NotRequired[ExportingConfigTypeDef]


class PutProfileObjectTypeRequestRequestTypeDef(TypedDict):
    DomainName: str
    ObjectTypeName: str
    Description: str
    TemplateId: NotRequired[str]
    ExpirationDays: NotRequired[int]
    EncryptionKey: NotRequired[str]
    AllowProfileCreation: NotRequired[bool]
    SourceLastUpdatedTimestampFormat: NotRequired[str]
    MaxProfileObjectCount: NotRequired[int]
    Fields: NotRequired[Mapping[str, ObjectTypeFieldTypeDef]]
    Keys: NotRequired[Mapping[str, Sequence[ObjectTypeKeyUnionTypeDef]]]
    Tags: NotRequired[Mapping[str, str]]


class SourceFlowConfigTypeDef(TypedDict):
    ConnectorType: SourceConnectorTypeType
    SourceConnectorProperties: SourceConnectorPropertiesTypeDef
    ConnectorProfileName: NotRequired[str]
    IncrementalPullConfig: NotRequired[IncrementalPullConfigTypeDef]


class TriggerConfigTypeDef(TypedDict):
    TriggerType: TriggerTypeType
    TriggerProperties: NotRequired[TriggerPropertiesTypeDef]


AutoMergingUnionTypeDef = Union[AutoMergingTypeDef, AutoMergingOutputTypeDef]


class CreateDomainResponseTypeDef(TypedDict):
    DomainName: str
    DefaultExpirationDays: int
    DefaultEncryptionKey: str
    DeadLetterQueueUrl: str
    Matching: MatchingResponseTypeDef
    RuleBasedMatching: RuleBasedMatchingResponseTypeDef
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetDomainResponseTypeDef(TypedDict):
    DomainName: str
    DefaultExpirationDays: int
    DefaultEncryptionKey: str
    DeadLetterQueueUrl: str
    Stats: DomainStatsTypeDef
    Matching: MatchingResponseTypeDef
    RuleBasedMatching: RuleBasedMatchingResponseTypeDef
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDomainResponseTypeDef(TypedDict):
    DomainName: str
    DefaultExpirationDays: int
    DefaultEncryptionKey: str
    DeadLetterQueueUrl: str
    Matching: MatchingResponseTypeDef
    RuleBasedMatching: RuleBasedMatchingResponseTypeDef
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListIdentityResolutionJobsResponseTypeDef(TypedDict):
    IdentityResolutionJobsList: List[IdentityResolutionJobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class FlowDefinitionTypeDef(TypedDict):
    FlowName: str
    KmsArn: str
    SourceFlowConfig: SourceFlowConfigTypeDef
    Tasks: Sequence[TaskTypeDef]
    TriggerConfig: TriggerConfigTypeDef
    Description: NotRequired[str]


class MatchingRequestTypeDef(TypedDict):
    Enabled: bool
    JobSchedule: NotRequired[JobScheduleTypeDef]
    AutoMerging: NotRequired[AutoMergingUnionTypeDef]
    ExportingConfig: NotRequired[ExportingConfigTypeDef]


class AppflowIntegrationTypeDef(TypedDict):
    FlowDefinition: FlowDefinitionTypeDef
    Batches: NotRequired[Sequence[BatchTypeDef]]


class PutIntegrationRequestRequestTypeDef(TypedDict):
    DomainName: str
    Uri: NotRequired[str]
    ObjectTypeName: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    FlowDefinition: NotRequired[FlowDefinitionTypeDef]
    ObjectTypeNames: NotRequired[Mapping[str, str]]
    RoleArn: NotRequired[str]


class CreateDomainRequestRequestTypeDef(TypedDict):
    DomainName: str
    DefaultExpirationDays: int
    DefaultEncryptionKey: NotRequired[str]
    DeadLetterQueueUrl: NotRequired[str]
    Matching: NotRequired[MatchingRequestTypeDef]
    RuleBasedMatching: NotRequired[RuleBasedMatchingRequestTypeDef]
    Tags: NotRequired[Mapping[str, str]]


class UpdateDomainRequestRequestTypeDef(TypedDict):
    DomainName: str
    DefaultExpirationDays: NotRequired[int]
    DefaultEncryptionKey: NotRequired[str]
    DeadLetterQueueUrl: NotRequired[str]
    Matching: NotRequired[MatchingRequestTypeDef]
    RuleBasedMatching: NotRequired[RuleBasedMatchingRequestTypeDef]
    Tags: NotRequired[Mapping[str, str]]


class IntegrationConfigTypeDef(TypedDict):
    AppflowIntegration: NotRequired[AppflowIntegrationTypeDef]


class CreateIntegrationWorkflowRequestRequestTypeDef(TypedDict):
    DomainName: str
    WorkflowType: Literal["APPFLOW_INTEGRATION"]
    IntegrationConfig: IntegrationConfigTypeDef
    ObjectTypeName: str
    RoleArn: str
    Tags: NotRequired[Mapping[str, str]]
