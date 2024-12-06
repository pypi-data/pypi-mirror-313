"""
Type annotations for customer-profiles service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_customer_profiles/type_defs/)

Usage::

    ```python
    from types_boto3_customer_profiles.type_defs import AddProfileKeyRequestRequestTypeDef

    data: AddProfileKeyRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AttributeDimensionTypeType,
    AttributeMatchingModelType,
    ComparisonOperatorType,
    ConflictResolvingModelType,
    DataFormatType,
    DataPullModeType,
    DateDimensionTypeType,
    EstimateStatusType,
    EventStreamDestinationStatusType,
    EventStreamStateType,
    EventTriggerLogicalOperatorType,
    FieldContentTypeType,
    FilterDimensionTypeType,
    GenderType,
    IdentityResolutionJobStatusType,
    IncludeOptionsType,
    IncludeType,
    JobScheduleDayOfTheWeekType,
    LogicalOperatorType,
    MarketoConnectorOperatorType,
    MatchTypeType,
    OperatorPropertiesKeysType,
    OperatorType,
    PartyTypeType,
    PeriodUnitType,
    QueryResultType,
    RuleBasedMatchingStatusType,
    S3ConnectorOperatorType,
    SalesforceConnectorOperatorType,
    SegmentSnapshotStatusType,
    ServiceNowConnectorOperatorType,
    SourceConnectorTypeType,
    StandardIdentifierType,
    StatisticType,
    StatusType,
    StringDimensionTypeType,
    TaskTypeType,
    TriggerTypeType,
    TypeType,
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
    "AddressDimensionOutputTypeDef",
    "AddressDimensionTypeDef",
    "AddressDimensionUnionTypeDef",
    "AddressTypeDef",
    "AppflowIntegrationTypeDef",
    "AppflowIntegrationWorkflowAttributesTypeDef",
    "AppflowIntegrationWorkflowMetricsTypeDef",
    "AppflowIntegrationWorkflowStepTypeDef",
    "AttributeDetailsOutputTypeDef",
    "AttributeDetailsTypeDef",
    "AttributeDimensionOutputTypeDef",
    "AttributeDimensionTypeDef",
    "AttributeDimensionUnionTypeDef",
    "AttributeItemTypeDef",
    "AttributeTypesSelectorOutputTypeDef",
    "AttributeTypesSelectorTypeDef",
    "AttributeTypesSelectorUnionTypeDef",
    "AttributeValueItemTypeDef",
    "AutoMergingOutputTypeDef",
    "AutoMergingTypeDef",
    "AutoMergingUnionTypeDef",
    "BatchGetCalculatedAttributeForProfileErrorTypeDef",
    "BatchGetCalculatedAttributeForProfileRequestRequestTypeDef",
    "BatchGetCalculatedAttributeForProfileResponseTypeDef",
    "BatchGetProfileErrorTypeDef",
    "BatchGetProfileRequestRequestTypeDef",
    "BatchGetProfileResponseTypeDef",
    "BatchTypeDef",
    "CalculatedAttributeDimensionOutputTypeDef",
    "CalculatedAttributeDimensionTypeDef",
    "CalculatedAttributeDimensionUnionTypeDef",
    "CalculatedAttributeValueTypeDef",
    "ConditionOverridesTypeDef",
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
    "CreateEventTriggerRequestRequestTypeDef",
    "CreateEventTriggerResponseTypeDef",
    "CreateIntegrationWorkflowRequestRequestTypeDef",
    "CreateIntegrationWorkflowResponseTypeDef",
    "CreateProfileRequestRequestTypeDef",
    "CreateProfileResponseTypeDef",
    "CreateSegmentDefinitionRequestRequestTypeDef",
    "CreateSegmentDefinitionResponseTypeDef",
    "CreateSegmentEstimateRequestRequestTypeDef",
    "CreateSegmentEstimateResponseTypeDef",
    "CreateSegmentSnapshotRequestRequestTypeDef",
    "CreateSegmentSnapshotResponseTypeDef",
    "DateDimensionOutputTypeDef",
    "DateDimensionTypeDef",
    "DateDimensionUnionTypeDef",
    "DeleteCalculatedAttributeDefinitionRequestRequestTypeDef",
    "DeleteDomainRequestRequestTypeDef",
    "DeleteDomainResponseTypeDef",
    "DeleteEventStreamRequestRequestTypeDef",
    "DeleteEventTriggerRequestRequestTypeDef",
    "DeleteEventTriggerResponseTypeDef",
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
    "DeleteSegmentDefinitionRequestRequestTypeDef",
    "DeleteSegmentDefinitionResponseTypeDef",
    "DeleteWorkflowRequestRequestTypeDef",
    "DestinationSummaryTypeDef",
    "DetectProfileObjectTypeRequestRequestTypeDef",
    "DetectProfileObjectTypeResponseTypeDef",
    "DetectedProfileObjectTypeTypeDef",
    "DimensionOutputTypeDef",
    "DimensionTypeDef",
    "DimensionUnionTypeDef",
    "DomainStatsTypeDef",
    "EventStreamDestinationDetailsTypeDef",
    "EventStreamSummaryTypeDef",
    "EventTriggerConditionOutputTypeDef",
    "EventTriggerConditionTypeDef",
    "EventTriggerConditionUnionTypeDef",
    "EventTriggerDimensionOutputTypeDef",
    "EventTriggerDimensionTypeDef",
    "EventTriggerDimensionUnionTypeDef",
    "EventTriggerLimitsOutputTypeDef",
    "EventTriggerLimitsTypeDef",
    "EventTriggerSummaryItemTypeDef",
    "ExportingConfigTypeDef",
    "ExportingLocationTypeDef",
    "ExtraLengthValueProfileDimensionOutputTypeDef",
    "ExtraLengthValueProfileDimensionTypeDef",
    "ExtraLengthValueProfileDimensionUnionTypeDef",
    "FieldSourceProfileIdsTypeDef",
    "FilterAttributeDimensionOutputTypeDef",
    "FilterAttributeDimensionTypeDef",
    "FilterAttributeDimensionUnionTypeDef",
    "FilterDimensionOutputTypeDef",
    "FilterDimensionTypeDef",
    "FilterDimensionUnionTypeDef",
    "FilterGroupOutputTypeDef",
    "FilterGroupTypeDef",
    "FilterGroupUnionTypeDef",
    "FilterOutputTypeDef",
    "FilterTypeDef",
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
    "GetEventTriggerRequestRequestTypeDef",
    "GetEventTriggerResponseTypeDef",
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
    "GetSegmentDefinitionRequestRequestTypeDef",
    "GetSegmentDefinitionResponseTypeDef",
    "GetSegmentEstimateRequestRequestTypeDef",
    "GetSegmentEstimateResponseTypeDef",
    "GetSegmentMembershipRequestRequestTypeDef",
    "GetSegmentMembershipResponseTypeDef",
    "GetSegmentSnapshotRequestRequestTypeDef",
    "GetSegmentSnapshotResponseTypeDef",
    "GetSimilarProfilesRequestGetSimilarProfilesPaginateTypeDef",
    "GetSimilarProfilesRequestRequestTypeDef",
    "GetSimilarProfilesResponseTypeDef",
    "GetWorkflowRequestRequestTypeDef",
    "GetWorkflowResponseTypeDef",
    "GetWorkflowStepsRequestRequestTypeDef",
    "GetWorkflowStepsResponseTypeDef",
    "GroupOutputTypeDef",
    "GroupTypeDef",
    "GroupUnionTypeDef",
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
    "ListEventTriggersRequestListEventTriggersPaginateTypeDef",
    "ListEventTriggersRequestRequestTypeDef",
    "ListEventTriggersResponseTypeDef",
    "ListIdentityResolutionJobsRequestRequestTypeDef",
    "ListIdentityResolutionJobsResponseTypeDef",
    "ListIntegrationItemTypeDef",
    "ListIntegrationsRequestRequestTypeDef",
    "ListIntegrationsResponseTypeDef",
    "ListObjectTypeAttributeItemTypeDef",
    "ListObjectTypeAttributesRequestListObjectTypeAttributesPaginateTypeDef",
    "ListObjectTypeAttributesRequestRequestTypeDef",
    "ListObjectTypeAttributesResponseTypeDef",
    "ListProfileObjectTypeItemTypeDef",
    "ListProfileObjectTypeTemplateItemTypeDef",
    "ListProfileObjectTypeTemplatesRequestRequestTypeDef",
    "ListProfileObjectTypeTemplatesResponseTypeDef",
    "ListProfileObjectTypesRequestRequestTypeDef",
    "ListProfileObjectTypesResponseTypeDef",
    "ListProfileObjectsItemTypeDef",
    "ListProfileObjectsRequestRequestTypeDef",
    "ListProfileObjectsResponseTypeDef",
    "ListRuleBasedMatchesRequestListRuleBasedMatchesPaginateTypeDef",
    "ListRuleBasedMatchesRequestRequestTypeDef",
    "ListRuleBasedMatchesResponseTypeDef",
    "ListSegmentDefinitionsRequestListSegmentDefinitionsPaginateTypeDef",
    "ListSegmentDefinitionsRequestRequestTypeDef",
    "ListSegmentDefinitionsResponseTypeDef",
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
    "ObjectAttributeOutputTypeDef",
    "ObjectAttributeTypeDef",
    "ObjectAttributeUnionTypeDef",
    "ObjectFilterTypeDef",
    "ObjectTypeFieldTypeDef",
    "ObjectTypeKeyOutputTypeDef",
    "ObjectTypeKeyTypeDef",
    "ObjectTypeKeyUnionTypeDef",
    "PaginatorConfigTypeDef",
    "PeriodTypeDef",
    "ProfileAttributeValuesRequestRequestTypeDef",
    "ProfileAttributeValuesResponseTypeDef",
    "ProfileAttributesOutputTypeDef",
    "ProfileAttributesTypeDef",
    "ProfileAttributesUnionTypeDef",
    "ProfileDimensionOutputTypeDef",
    "ProfileDimensionTypeDef",
    "ProfileDimensionUnionTypeDef",
    "ProfileQueryFailuresTypeDef",
    "ProfileQueryResultTypeDef",
    "ProfileTypeDef",
    "PutIntegrationRequestRequestTypeDef",
    "PutIntegrationResponseTypeDef",
    "PutProfileObjectRequestRequestTypeDef",
    "PutProfileObjectResponseTypeDef",
    "PutProfileObjectTypeRequestRequestTypeDef",
    "PutProfileObjectTypeResponseTypeDef",
    "RangeOverrideTypeDef",
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
    "SegmentDefinitionItemTypeDef",
    "SegmentGroupOutputTypeDef",
    "SegmentGroupStructureTypeDef",
    "SegmentGroupTypeDef",
    "ServiceNowSourcePropertiesTypeDef",
    "SourceConnectorPropertiesTypeDef",
    "SourceFlowConfigTypeDef",
    "SourceSegmentTypeDef",
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
    "UpdateEventTriggerRequestRequestTypeDef",
    "UpdateEventTriggerResponseTypeDef",
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

class ProfileDimensionOutputTypeDef(TypedDict):
    DimensionType: StringDimensionTypeType
    Values: List[str]

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

class AttributeDimensionOutputTypeDef(TypedDict):
    DimensionType: AttributeDimensionTypeType
    Values: List[str]

class AttributeDimensionTypeDef(TypedDict):
    DimensionType: AttributeDimensionTypeType
    Values: Sequence[str]

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

class AttributeValueItemTypeDef(TypedDict):
    Value: NotRequired[str]

class ConflictResolutionTypeDef(TypedDict):
    ConflictResolvingModel: ConflictResolvingModelType
    SourceName: NotRequired[str]

class ConsolidationOutputTypeDef(TypedDict):
    MatchingAttributesList: List[List[str]]

class BatchGetCalculatedAttributeForProfileErrorTypeDef(TypedDict):
    Code: str
    Message: str
    ProfileId: str

class CalculatedAttributeValueTypeDef(TypedDict):
    CalculatedAttributeName: NotRequired[str]
    DisplayName: NotRequired[str]
    IsDataPartial: NotRequired[str]
    ProfileId: NotRequired[str]
    Value: NotRequired[str]

class BatchGetProfileErrorTypeDef(TypedDict):
    Code: str
    Message: str
    ProfileId: str

class BatchGetProfileRequestRequestTypeDef(TypedDict):
    DomainName: str
    ProfileIds: Sequence[str]

TimestampTypeDef = Union[datetime, str]

class RangeOverrideTypeDef(TypedDict):
    Start: int
    Unit: Literal["DAYS"]
    End: NotRequired[int]

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

class CreateSegmentSnapshotRequestRequestTypeDef(TypedDict):
    DomainName: str
    SegmentDefinitionName: str
    DataFormat: DataFormatType
    EncryptionKey: NotRequired[str]
    RoleArn: NotRequired[str]
    DestinationUri: NotRequired[str]

class DateDimensionOutputTypeDef(TypedDict):
    DimensionType: DateDimensionTypeType
    Values: List[str]

class DateDimensionTypeDef(TypedDict):
    DimensionType: DateDimensionTypeType
    Values: Sequence[str]

class DeleteCalculatedAttributeDefinitionRequestRequestTypeDef(TypedDict):
    DomainName: str
    CalculatedAttributeName: str

class DeleteDomainRequestRequestTypeDef(TypedDict):
    DomainName: str

class DeleteEventStreamRequestRequestTypeDef(TypedDict):
    DomainName: str
    EventStreamName: str

class DeleteEventTriggerRequestRequestTypeDef(TypedDict):
    DomainName: str
    EventTriggerName: str

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

class DeleteSegmentDefinitionRequestRequestTypeDef(TypedDict):
    DomainName: str
    SegmentDefinitionName: str

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

class ObjectAttributeOutputTypeDef(TypedDict):
    ComparisonOperator: ComparisonOperatorType
    Values: List[str]
    Source: NotRequired[str]
    FieldName: NotRequired[str]

class PeriodTypeDef(TypedDict):
    Unit: PeriodUnitType
    Value: int
    MaxInvocationsPerProfile: NotRequired[int]
    Unlimited: NotRequired[bool]

class EventTriggerSummaryItemTypeDef(TypedDict):
    ObjectTypeName: NotRequired[str]
    EventTriggerName: NotRequired[str]
    Description: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    LastUpdatedAt: NotRequired[datetime]
    Tags: NotRequired[Dict[str, str]]

class S3ExportingConfigTypeDef(TypedDict):
    S3BucketName: str
    S3KeyName: NotRequired[str]

class S3ExportingLocationTypeDef(TypedDict):
    S3BucketName: NotRequired[str]
    S3KeyName: NotRequired[str]

class ExtraLengthValueProfileDimensionOutputTypeDef(TypedDict):
    DimensionType: StringDimensionTypeType
    Values: List[str]

class ExtraLengthValueProfileDimensionTypeDef(TypedDict):
    DimensionType: StringDimensionTypeType
    Values: Sequence[str]

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

class FilterAttributeDimensionOutputTypeDef(TypedDict):
    DimensionType: FilterDimensionTypeType
    Values: List[str]

class FilterAttributeDimensionTypeDef(TypedDict):
    DimensionType: FilterDimensionTypeType
    Values: Sequence[str]

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

class GetEventTriggerRequestRequestTypeDef(TypedDict):
    DomainName: str
    EventTriggerName: str

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

class GetSegmentDefinitionRequestRequestTypeDef(TypedDict):
    DomainName: str
    SegmentDefinitionName: str

class GetSegmentEstimateRequestRequestTypeDef(TypedDict):
    DomainName: str
    EstimateId: str

class GetSegmentMembershipRequestRequestTypeDef(TypedDict):
    DomainName: str
    SegmentDefinitionName: str
    ProfileIds: Sequence[str]

class ProfileQueryFailuresTypeDef(TypedDict):
    ProfileId: str
    Message: str
    Status: NotRequired[int]

class GetSegmentSnapshotRequestRequestTypeDef(TypedDict):
    DomainName: str
    SegmentDefinitionName: str
    SnapshotId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

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

class SourceSegmentTypeDef(TypedDict):
    SegmentDefinitionName: NotRequired[str]

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
    EventTriggerNames: NotRequired[List[str]]

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

class ListEventStreamsRequestRequestTypeDef(TypedDict):
    DomainName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListEventTriggersRequestRequestTypeDef(TypedDict):
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

class ListObjectTypeAttributeItemTypeDef(TypedDict):
    AttributeName: str
    LastUpdatedAt: datetime

class ListObjectTypeAttributesRequestRequestTypeDef(TypedDict):
    DomainName: str
    ObjectTypeName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

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

class ListSegmentDefinitionsRequestRequestTypeDef(TypedDict):
    DomainName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class SegmentDefinitionItemTypeDef(TypedDict):
    SegmentDefinitionName: NotRequired[str]
    DisplayName: NotRequired[str]
    Description: NotRequired[str]
    SegmentDefinitionArn: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    Tags: NotRequired[Dict[str, str]]

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

class ObjectAttributeTypeDef(TypedDict):
    ComparisonOperator: ComparisonOperatorType
    Values: Sequence[str]
    Source: NotRequired[str]
    FieldName: NotRequired[str]

class ObjectTypeKeyTypeDef(TypedDict):
    StandardIdentifiers: NotRequired[Sequence[StandardIdentifierType]]
    FieldNames: NotRequired[Sequence[str]]

class ProfileAttributeValuesRequestRequestTypeDef(TypedDict):
    DomainName: str
    AttributeName: str

class ProfileDimensionTypeDef(TypedDict):
    DimensionType: StringDimensionTypeType
    Values: Sequence[str]

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

class CreateSegmentDefinitionResponseTypeDef(TypedDict):
    SegmentDefinitionName: str
    DisplayName: str
    Description: str
    CreatedAt: datetime
    SegmentDefinitionArn: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSegmentEstimateResponseTypeDef(TypedDict):
    DomainName: str
    EstimateId: str
    StatusCode: int
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSegmentSnapshotResponseTypeDef(TypedDict):
    SnapshotId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDomainResponseTypeDef(TypedDict):
    Message: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteEventTriggerResponseTypeDef(TypedDict):
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

class DeleteSegmentDefinitionResponseTypeDef(TypedDict):
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
    EventTriggerNames: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetSegmentEstimateResponseTypeDef(TypedDict):
    DomainName: str
    EstimateId: str
    Status: EstimateStatusType
    Estimate: str
    Message: str
    StatusCode: int
    ResponseMetadata: ResponseMetadataTypeDef

class GetSegmentSnapshotResponseTypeDef(TypedDict):
    SnapshotId: str
    Status: SegmentSnapshotStatusType
    StatusMessage: str
    DataFormat: DataFormatType
    EncryptionKey: str
    RoleArn: str
    DestinationUri: str
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
    EventTriggerNames: List[str]
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

class AddressDimensionOutputTypeDef(TypedDict):
    City: NotRequired[ProfileDimensionOutputTypeDef]
    Country: NotRequired[ProfileDimensionOutputTypeDef]
    County: NotRequired[ProfileDimensionOutputTypeDef]
    PostalCode: NotRequired[ProfileDimensionOutputTypeDef]
    Province: NotRequired[ProfileDimensionOutputTypeDef]
    State: NotRequired[ProfileDimensionOutputTypeDef]

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

AttributeDimensionUnionTypeDef = Union[AttributeDimensionTypeDef, AttributeDimensionOutputTypeDef]
AttributeTypesSelectorUnionTypeDef = Union[
    AttributeTypesSelectorTypeDef, AttributeTypesSelectorOutputTypeDef
]

class ProfileAttributeValuesResponseTypeDef(TypedDict):
    DomainName: str
    AttributeName: str
    Items: List[AttributeValueItemTypeDef]
    StatusCode: int
    ResponseMetadata: ResponseMetadataTypeDef

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

class ConditionOverridesTypeDef(TypedDict):
    Range: NotRequired[RangeOverrideTypeDef]

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

DateDimensionUnionTypeDef = Union[DateDimensionTypeDef, DateDimensionOutputTypeDef]

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

class EventTriggerDimensionOutputTypeDef(TypedDict):
    ObjectAttributes: List[ObjectAttributeOutputTypeDef]

class EventTriggerLimitsOutputTypeDef(TypedDict):
    EventExpiration: NotRequired[int]
    Periods: NotRequired[List[PeriodTypeDef]]

class EventTriggerLimitsTypeDef(TypedDict):
    EventExpiration: NotRequired[int]
    Periods: NotRequired[Sequence[PeriodTypeDef]]

class ListEventTriggersResponseTypeDef(TypedDict):
    Items: List[EventTriggerSummaryItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ExportingConfigTypeDef(TypedDict):
    S3Exporting: NotRequired[S3ExportingConfigTypeDef]

class ExportingLocationTypeDef(TypedDict):
    S3Exporting: NotRequired[S3ExportingLocationTypeDef]

ExtraLengthValueProfileDimensionUnionTypeDef = Union[
    ExtraLengthValueProfileDimensionTypeDef, ExtraLengthValueProfileDimensionOutputTypeDef
]

class MergeProfilesRequestRequestTypeDef(TypedDict):
    DomainName: str
    MainProfileId: str
    ProfileIdsToBeMerged: Sequence[str]
    FieldSourceProfileIds: NotRequired[FieldSourceProfileIdsTypeDef]

class FilterDimensionOutputTypeDef(TypedDict):
    Attributes: Dict[str, FilterAttributeDimensionOutputTypeDef]

FilterAttributeDimensionUnionTypeDef = Union[
    FilterAttributeDimensionTypeDef, FilterAttributeDimensionOutputTypeDef
]

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

class GetSimilarProfilesRequestGetSimilarProfilesPaginateTypeDef(TypedDict):
    DomainName: str
    MatchType: MatchTypeType
    SearchKey: str
    SearchValue: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEventStreamsRequestListEventStreamsPaginateTypeDef(TypedDict):
    DomainName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEventTriggersRequestListEventTriggersPaginateTypeDef(TypedDict):
    DomainName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListObjectTypeAttributesRequestListObjectTypeAttributesPaginateTypeDef(TypedDict):
    DomainName: str
    ObjectTypeName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRuleBasedMatchesRequestListRuleBasedMatchesPaginateTypeDef(TypedDict):
    DomainName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSegmentDefinitionsRequestListSegmentDefinitionsPaginateTypeDef(TypedDict):
    DomainName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

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

class ListObjectTypeAttributesResponseTypeDef(TypedDict):
    Items: List[ListObjectTypeAttributeItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

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

class ListSegmentDefinitionsResponseTypeDef(TypedDict):
    Items: List[SegmentDefinitionItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListWorkflowsResponseTypeDef(TypedDict):
    Items: List[ListWorkflowsItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

MatchingRuleUnionTypeDef = Union[MatchingRuleTypeDef, MatchingRuleOutputTypeDef]
ObjectAttributeUnionTypeDef = Union[ObjectAttributeTypeDef, ObjectAttributeOutputTypeDef]
ObjectTypeKeyUnionTypeDef = Union[ObjectTypeKeyTypeDef, ObjectTypeKeyOutputTypeDef]
ProfileDimensionUnionTypeDef = Union[ProfileDimensionTypeDef, ProfileDimensionOutputTypeDef]

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

class ProfileAttributesOutputTypeDef(TypedDict):
    AccountNumber: NotRequired[ProfileDimensionOutputTypeDef]
    AdditionalInformation: NotRequired[ExtraLengthValueProfileDimensionOutputTypeDef]
    FirstName: NotRequired[ProfileDimensionOutputTypeDef]
    LastName: NotRequired[ProfileDimensionOutputTypeDef]
    MiddleName: NotRequired[ProfileDimensionOutputTypeDef]
    GenderString: NotRequired[ProfileDimensionOutputTypeDef]
    PartyTypeString: NotRequired[ProfileDimensionOutputTypeDef]
    BirthDate: NotRequired[DateDimensionOutputTypeDef]
    PhoneNumber: NotRequired[ProfileDimensionOutputTypeDef]
    BusinessName: NotRequired[ProfileDimensionOutputTypeDef]
    BusinessPhoneNumber: NotRequired[ProfileDimensionOutputTypeDef]
    HomePhoneNumber: NotRequired[ProfileDimensionOutputTypeDef]
    MobilePhoneNumber: NotRequired[ProfileDimensionOutputTypeDef]
    EmailAddress: NotRequired[ProfileDimensionOutputTypeDef]
    PersonalEmailAddress: NotRequired[ProfileDimensionOutputTypeDef]
    BusinessEmailAddress: NotRequired[ProfileDimensionOutputTypeDef]
    Address: NotRequired[AddressDimensionOutputTypeDef]
    ShippingAddress: NotRequired[AddressDimensionOutputTypeDef]
    MailingAddress: NotRequired[AddressDimensionOutputTypeDef]
    BillingAddress: NotRequired[AddressDimensionOutputTypeDef]
    Attributes: NotRequired[Dict[str, AttributeDimensionOutputTypeDef]]

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

class BatchGetCalculatedAttributeForProfileRequestRequestTypeDef(TypedDict):
    CalculatedAttributeName: str
    DomainName: str
    ProfileIds: Sequence[str]
    ConditionOverrides: NotRequired[ConditionOverridesTypeDef]

class BatchGetCalculatedAttributeForProfileResponseTypeDef(TypedDict):
    Errors: List[BatchGetCalculatedAttributeForProfileErrorTypeDef]
    CalculatedAttributeValues: List[CalculatedAttributeValueTypeDef]
    ConditionOverrides: ConditionOverridesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CalculatedAttributeDimensionOutputTypeDef(TypedDict):
    DimensionType: AttributeDimensionTypeType
    Values: List[str]
    ConditionOverrides: NotRequired[ConditionOverridesTypeDef]

class CalculatedAttributeDimensionTypeDef(TypedDict):
    DimensionType: AttributeDimensionTypeType
    Values: Sequence[str]
    ConditionOverrides: NotRequired[ConditionOverridesTypeDef]

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

class EventTriggerConditionOutputTypeDef(TypedDict):
    EventTriggerDimensions: List[EventTriggerDimensionOutputTypeDef]
    LogicalOperator: EventTriggerLogicalOperatorType

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

FilterGroupOutputTypeDef = TypedDict(
    "FilterGroupOutputTypeDef",
    {
        "Type": TypeType,
        "Dimensions": List[FilterDimensionOutputTypeDef],
    },
)

class FilterDimensionTypeDef(TypedDict):
    Attributes: Mapping[str, FilterAttributeDimensionUnionTypeDef]

class BatchGetProfileResponseTypeDef(TypedDict):
    Errors: List[BatchGetProfileErrorTypeDef]
    Profiles: List[ProfileTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ProfileQueryResultTypeDef(TypedDict):
    ProfileId: str
    QueryResult: QueryResultType
    Profile: NotRequired[ProfileTypeDef]

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

class EventTriggerDimensionTypeDef(TypedDict):
    ObjectAttributes: Sequence[ObjectAttributeUnionTypeDef]

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

class AddressDimensionTypeDef(TypedDict):
    City: NotRequired[ProfileDimensionUnionTypeDef]
    Country: NotRequired[ProfileDimensionUnionTypeDef]
    County: NotRequired[ProfileDimensionUnionTypeDef]
    PostalCode: NotRequired[ProfileDimensionUnionTypeDef]
    Province: NotRequired[ProfileDimensionUnionTypeDef]
    State: NotRequired[ProfileDimensionUnionTypeDef]

class SourceFlowConfigTypeDef(TypedDict):
    ConnectorType: SourceConnectorTypeType
    SourceConnectorProperties: SourceConnectorPropertiesTypeDef
    ConnectorProfileName: NotRequired[str]
    IncrementalPullConfig: NotRequired[IncrementalPullConfigTypeDef]

class TriggerConfigTypeDef(TypedDict):
    TriggerType: TriggerTypeType
    TriggerProperties: NotRequired[TriggerPropertiesTypeDef]

class DimensionOutputTypeDef(TypedDict):
    ProfileAttributes: NotRequired[ProfileAttributesOutputTypeDef]
    CalculatedAttributes: NotRequired[Dict[str, CalculatedAttributeDimensionOutputTypeDef]]

CalculatedAttributeDimensionUnionTypeDef = Union[
    CalculatedAttributeDimensionTypeDef, CalculatedAttributeDimensionOutputTypeDef
]
AutoMergingUnionTypeDef = Union[AutoMergingTypeDef, AutoMergingOutputTypeDef]

class CreateEventTriggerResponseTypeDef(TypedDict):
    EventTriggerName: str
    ObjectTypeName: str
    Description: str
    EventTriggerConditions: List[EventTriggerConditionOutputTypeDef]
    SegmentFilter: str
    EventTriggerLimits: EventTriggerLimitsOutputTypeDef
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetEventTriggerResponseTypeDef(TypedDict):
    EventTriggerName: str
    ObjectTypeName: str
    Description: str
    EventTriggerConditions: List[EventTriggerConditionOutputTypeDef]
    SegmentFilter: str
    EventTriggerLimits: EventTriggerLimitsOutputTypeDef
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEventTriggerResponseTypeDef(TypedDict):
    EventTriggerName: str
    ObjectTypeName: str
    Description: str
    EventTriggerConditions: List[EventTriggerConditionOutputTypeDef]
    SegmentFilter: str
    EventTriggerLimits: EventTriggerLimitsOutputTypeDef
    CreatedAt: datetime
    LastUpdatedAt: datetime
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

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

class FilterOutputTypeDef(TypedDict):
    Include: IncludeType
    Groups: List[FilterGroupOutputTypeDef]

FilterDimensionUnionTypeDef = Union[FilterDimensionTypeDef, FilterDimensionOutputTypeDef]

class GetSegmentMembershipResponseTypeDef(TypedDict):
    SegmentDefinitionName: str
    Profiles: List[ProfileQueryResultTypeDef]
    Failures: List[ProfileQueryFailuresTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

EventTriggerDimensionUnionTypeDef = Union[
    EventTriggerDimensionTypeDef, EventTriggerDimensionOutputTypeDef
]
AddressDimensionUnionTypeDef = Union[AddressDimensionTypeDef, AddressDimensionOutputTypeDef]

class FlowDefinitionTypeDef(TypedDict):
    FlowName: str
    KmsArn: str
    SourceFlowConfig: SourceFlowConfigTypeDef
    Tasks: Sequence[TaskTypeDef]
    TriggerConfig: TriggerConfigTypeDef
    Description: NotRequired[str]

GroupOutputTypeDef = TypedDict(
    "GroupOutputTypeDef",
    {
        "Dimensions": NotRequired[List[DimensionOutputTypeDef]],
        "SourceSegments": NotRequired[List[SourceSegmentTypeDef]],
        "SourceType": NotRequired[IncludeOptionsType],
        "Type": NotRequired[IncludeOptionsType],
    },
)

class MatchingRequestTypeDef(TypedDict):
    Enabled: bool
    JobSchedule: NotRequired[JobScheduleTypeDef]
    AutoMerging: NotRequired[AutoMergingUnionTypeDef]
    ExportingConfig: NotRequired[ExportingConfigTypeDef]

class CreateCalculatedAttributeDefinitionResponseTypeDef(TypedDict):
    CalculatedAttributeName: str
    DisplayName: str
    Description: str
    AttributeDetails: AttributeDetailsOutputTypeDef
    Conditions: ConditionsTypeDef
    Filter: FilterOutputTypeDef
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
    Filter: FilterOutputTypeDef
    Conditions: ConditionsTypeDef
    AttributeDetails: AttributeDetailsOutputTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

FilterGroupTypeDef = TypedDict(
    "FilterGroupTypeDef",
    {
        "Type": TypeType,
        "Dimensions": Sequence[FilterDimensionUnionTypeDef],
    },
)

class EventTriggerConditionTypeDef(TypedDict):
    EventTriggerDimensions: Sequence[EventTriggerDimensionUnionTypeDef]
    LogicalOperator: EventTriggerLogicalOperatorType

class ProfileAttributesTypeDef(TypedDict):
    AccountNumber: NotRequired[ProfileDimensionUnionTypeDef]
    AdditionalInformation: NotRequired[ExtraLengthValueProfileDimensionUnionTypeDef]
    FirstName: NotRequired[ProfileDimensionUnionTypeDef]
    LastName: NotRequired[ProfileDimensionUnionTypeDef]
    MiddleName: NotRequired[ProfileDimensionUnionTypeDef]
    GenderString: NotRequired[ProfileDimensionUnionTypeDef]
    PartyTypeString: NotRequired[ProfileDimensionUnionTypeDef]
    BirthDate: NotRequired[DateDimensionUnionTypeDef]
    PhoneNumber: NotRequired[ProfileDimensionUnionTypeDef]
    BusinessName: NotRequired[ProfileDimensionUnionTypeDef]
    BusinessPhoneNumber: NotRequired[ProfileDimensionUnionTypeDef]
    HomePhoneNumber: NotRequired[ProfileDimensionUnionTypeDef]
    MobilePhoneNumber: NotRequired[ProfileDimensionUnionTypeDef]
    EmailAddress: NotRequired[ProfileDimensionUnionTypeDef]
    PersonalEmailAddress: NotRequired[ProfileDimensionUnionTypeDef]
    BusinessEmailAddress: NotRequired[ProfileDimensionUnionTypeDef]
    Address: NotRequired[AddressDimensionUnionTypeDef]
    ShippingAddress: NotRequired[AddressDimensionUnionTypeDef]
    MailingAddress: NotRequired[AddressDimensionUnionTypeDef]
    BillingAddress: NotRequired[AddressDimensionUnionTypeDef]
    Attributes: NotRequired[Mapping[str, AttributeDimensionUnionTypeDef]]

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
    EventTriggerNames: NotRequired[Sequence[str]]

class SegmentGroupOutputTypeDef(TypedDict):
    Groups: NotRequired[List[GroupOutputTypeDef]]
    Include: NotRequired[IncludeOptionsType]

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

FilterGroupUnionTypeDef = Union[FilterGroupTypeDef, FilterGroupOutputTypeDef]
EventTriggerConditionUnionTypeDef = Union[
    EventTriggerConditionTypeDef, EventTriggerConditionOutputTypeDef
]

class UpdateEventTriggerRequestRequestTypeDef(TypedDict):
    DomainName: str
    EventTriggerName: str
    ObjectTypeName: NotRequired[str]
    Description: NotRequired[str]
    EventTriggerConditions: NotRequired[Sequence[EventTriggerConditionTypeDef]]
    SegmentFilter: NotRequired[str]
    EventTriggerLimits: NotRequired[EventTriggerLimitsTypeDef]

ProfileAttributesUnionTypeDef = Union[ProfileAttributesTypeDef, ProfileAttributesOutputTypeDef]

class IntegrationConfigTypeDef(TypedDict):
    AppflowIntegration: NotRequired[AppflowIntegrationTypeDef]

class GetSegmentDefinitionResponseTypeDef(TypedDict):
    SegmentDefinitionName: str
    DisplayName: str
    Description: str
    SegmentGroups: SegmentGroupOutputTypeDef
    SegmentDefinitionArn: str
    CreatedAt: datetime
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class FilterTypeDef(TypedDict):
    Include: IncludeType
    Groups: Sequence[FilterGroupUnionTypeDef]

class CreateEventTriggerRequestRequestTypeDef(TypedDict):
    DomainName: str
    EventTriggerName: str
    ObjectTypeName: str
    EventTriggerConditions: Sequence[EventTriggerConditionUnionTypeDef]
    Description: NotRequired[str]
    SegmentFilter: NotRequired[str]
    EventTriggerLimits: NotRequired[EventTriggerLimitsTypeDef]
    Tags: NotRequired[Mapping[str, str]]

class DimensionTypeDef(TypedDict):
    ProfileAttributes: NotRequired[ProfileAttributesUnionTypeDef]
    CalculatedAttributes: NotRequired[Mapping[str, CalculatedAttributeDimensionUnionTypeDef]]

class CreateIntegrationWorkflowRequestRequestTypeDef(TypedDict):
    DomainName: str
    WorkflowType: Literal["APPFLOW_INTEGRATION"]
    IntegrationConfig: IntegrationConfigTypeDef
    ObjectTypeName: str
    RoleArn: str
    Tags: NotRequired[Mapping[str, str]]

class CreateCalculatedAttributeDefinitionRequestRequestTypeDef(TypedDict):
    DomainName: str
    CalculatedAttributeName: str
    AttributeDetails: AttributeDetailsTypeDef
    Statistic: StatisticType
    DisplayName: NotRequired[str]
    Description: NotRequired[str]
    Conditions: NotRequired[ConditionsTypeDef]
    Filter: NotRequired[FilterTypeDef]
    Tags: NotRequired[Mapping[str, str]]

DimensionUnionTypeDef = Union[DimensionTypeDef, DimensionOutputTypeDef]
GroupTypeDef = TypedDict(
    "GroupTypeDef",
    {
        "Dimensions": NotRequired[Sequence[DimensionUnionTypeDef]],
        "SourceSegments": NotRequired[Sequence[SourceSegmentTypeDef]],
        "SourceType": NotRequired[IncludeOptionsType],
        "Type": NotRequired[IncludeOptionsType],
    },
)
GroupUnionTypeDef = Union[GroupTypeDef, GroupOutputTypeDef]

class SegmentGroupStructureTypeDef(TypedDict):
    Groups: NotRequired[Sequence[GroupUnionTypeDef]]
    Include: NotRequired[IncludeOptionsType]

class SegmentGroupTypeDef(TypedDict):
    Groups: NotRequired[Sequence[GroupUnionTypeDef]]
    Include: NotRequired[IncludeOptionsType]

class CreateSegmentEstimateRequestRequestTypeDef(TypedDict):
    DomainName: str
    SegmentQuery: SegmentGroupStructureTypeDef

class CreateSegmentDefinitionRequestRequestTypeDef(TypedDict):
    DomainName: str
    SegmentDefinitionName: str
    DisplayName: str
    SegmentGroups: SegmentGroupTypeDef
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
