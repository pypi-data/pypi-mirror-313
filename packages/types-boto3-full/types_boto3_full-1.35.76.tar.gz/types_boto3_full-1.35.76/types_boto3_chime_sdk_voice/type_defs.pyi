"""
Type annotations for chime-sdk-voice service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_chime_sdk_voice/type_defs/)

Usage::

    ```python
    from types_boto3_chime_sdk_voice.type_defs import AddressTypeDef

    data: AddressTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AlexaSkillStatusType,
    CallingNameStatusType,
    CallLegTypeType,
    CapabilityType,
    ContactCenterSystemTypeType,
    ErrorCodeType,
    GeoMatchLevelType,
    NotificationTargetType,
    NumberSelectionBehaviorType,
    OrderedPhoneNumberStatusType,
    OriginationRouteProtocolType,
    PhoneNumberAssociationNameType,
    PhoneNumberOrderStatusType,
    PhoneNumberOrderTypeType,
    PhoneNumberProductTypeType,
    PhoneNumberStatusType,
    PhoneNumberTypeType,
    ProxySessionStatusType,
    SessionBorderControllerTypeType,
    SipRuleTriggerTypeType,
    VoiceConnectorAwsRegionType,
    VoiceConnectorIntegrationTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AddressTypeDef",
    "AssociatePhoneNumbersWithVoiceConnectorGroupRequestRequestTypeDef",
    "AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef",
    "AssociatePhoneNumbersWithVoiceConnectorRequestRequestTypeDef",
    "AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef",
    "BatchDeletePhoneNumberRequestRequestTypeDef",
    "BatchDeletePhoneNumberResponseTypeDef",
    "BatchUpdatePhoneNumberRequestRequestTypeDef",
    "BatchUpdatePhoneNumberResponseTypeDef",
    "CallDetailsTypeDef",
    "CandidateAddressTypeDef",
    "CreatePhoneNumberOrderRequestRequestTypeDef",
    "CreatePhoneNumberOrderResponseTypeDef",
    "CreateProxySessionRequestRequestTypeDef",
    "CreateProxySessionResponseTypeDef",
    "CreateSipMediaApplicationCallRequestRequestTypeDef",
    "CreateSipMediaApplicationCallResponseTypeDef",
    "CreateSipMediaApplicationRequestRequestTypeDef",
    "CreateSipMediaApplicationResponseTypeDef",
    "CreateSipRuleRequestRequestTypeDef",
    "CreateSipRuleResponseTypeDef",
    "CreateVoiceConnectorGroupRequestRequestTypeDef",
    "CreateVoiceConnectorGroupResponseTypeDef",
    "CreateVoiceConnectorRequestRequestTypeDef",
    "CreateVoiceConnectorResponseTypeDef",
    "CreateVoiceProfileDomainRequestRequestTypeDef",
    "CreateVoiceProfileDomainResponseTypeDef",
    "CreateVoiceProfileRequestRequestTypeDef",
    "CreateVoiceProfileResponseTypeDef",
    "CredentialTypeDef",
    "DNISEmergencyCallingConfigurationTypeDef",
    "DeletePhoneNumberRequestRequestTypeDef",
    "DeleteProxySessionRequestRequestTypeDef",
    "DeleteSipMediaApplicationRequestRequestTypeDef",
    "DeleteSipRuleRequestRequestTypeDef",
    "DeleteVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef",
    "DeleteVoiceConnectorExternalSystemsConfigurationRequestRequestTypeDef",
    "DeleteVoiceConnectorGroupRequestRequestTypeDef",
    "DeleteVoiceConnectorOriginationRequestRequestTypeDef",
    "DeleteVoiceConnectorProxyRequestRequestTypeDef",
    "DeleteVoiceConnectorRequestRequestTypeDef",
    "DeleteVoiceConnectorStreamingConfigurationRequestRequestTypeDef",
    "DeleteVoiceConnectorTerminationCredentialsRequestRequestTypeDef",
    "DeleteVoiceConnectorTerminationRequestRequestTypeDef",
    "DeleteVoiceProfileDomainRequestRequestTypeDef",
    "DeleteVoiceProfileRequestRequestTypeDef",
    "DisassociatePhoneNumbersFromVoiceConnectorGroupRequestRequestTypeDef",
    "DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef",
    "DisassociatePhoneNumbersFromVoiceConnectorRequestRequestTypeDef",
    "DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef",
    "EmergencyCallingConfigurationOutputTypeDef",
    "EmergencyCallingConfigurationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExternalSystemsConfigurationTypeDef",
    "GeoMatchParamsTypeDef",
    "GetGlobalSettingsResponseTypeDef",
    "GetPhoneNumberOrderRequestRequestTypeDef",
    "GetPhoneNumberOrderResponseTypeDef",
    "GetPhoneNumberRequestRequestTypeDef",
    "GetPhoneNumberResponseTypeDef",
    "GetPhoneNumberSettingsResponseTypeDef",
    "GetProxySessionRequestRequestTypeDef",
    "GetProxySessionResponseTypeDef",
    "GetSipMediaApplicationAlexaSkillConfigurationRequestRequestTypeDef",
    "GetSipMediaApplicationAlexaSkillConfigurationResponseTypeDef",
    "GetSipMediaApplicationLoggingConfigurationRequestRequestTypeDef",
    "GetSipMediaApplicationLoggingConfigurationResponseTypeDef",
    "GetSipMediaApplicationRequestRequestTypeDef",
    "GetSipMediaApplicationResponseTypeDef",
    "GetSipRuleRequestRequestTypeDef",
    "GetSipRuleResponseTypeDef",
    "GetSpeakerSearchTaskRequestRequestTypeDef",
    "GetSpeakerSearchTaskResponseTypeDef",
    "GetVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef",
    "GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef",
    "GetVoiceConnectorExternalSystemsConfigurationRequestRequestTypeDef",
    "GetVoiceConnectorExternalSystemsConfigurationResponseTypeDef",
    "GetVoiceConnectorGroupRequestRequestTypeDef",
    "GetVoiceConnectorGroupResponseTypeDef",
    "GetVoiceConnectorLoggingConfigurationRequestRequestTypeDef",
    "GetVoiceConnectorLoggingConfigurationResponseTypeDef",
    "GetVoiceConnectorOriginationRequestRequestTypeDef",
    "GetVoiceConnectorOriginationResponseTypeDef",
    "GetVoiceConnectorProxyRequestRequestTypeDef",
    "GetVoiceConnectorProxyResponseTypeDef",
    "GetVoiceConnectorRequestRequestTypeDef",
    "GetVoiceConnectorResponseTypeDef",
    "GetVoiceConnectorStreamingConfigurationRequestRequestTypeDef",
    "GetVoiceConnectorStreamingConfigurationResponseTypeDef",
    "GetVoiceConnectorTerminationHealthRequestRequestTypeDef",
    "GetVoiceConnectorTerminationHealthResponseTypeDef",
    "GetVoiceConnectorTerminationRequestRequestTypeDef",
    "GetVoiceConnectorTerminationResponseTypeDef",
    "GetVoiceProfileDomainRequestRequestTypeDef",
    "GetVoiceProfileDomainResponseTypeDef",
    "GetVoiceProfileRequestRequestTypeDef",
    "GetVoiceProfileResponseTypeDef",
    "GetVoiceToneAnalysisTaskRequestRequestTypeDef",
    "GetVoiceToneAnalysisTaskResponseTypeDef",
    "ListAvailableVoiceConnectorRegionsResponseTypeDef",
    "ListPhoneNumberOrdersRequestRequestTypeDef",
    "ListPhoneNumberOrdersResponseTypeDef",
    "ListPhoneNumbersRequestRequestTypeDef",
    "ListPhoneNumbersResponseTypeDef",
    "ListProxySessionsRequestRequestTypeDef",
    "ListProxySessionsResponseTypeDef",
    "ListSipMediaApplicationsRequestListSipMediaApplicationsPaginateTypeDef",
    "ListSipMediaApplicationsRequestRequestTypeDef",
    "ListSipMediaApplicationsResponseTypeDef",
    "ListSipRulesRequestListSipRulesPaginateTypeDef",
    "ListSipRulesRequestRequestTypeDef",
    "ListSipRulesResponseTypeDef",
    "ListSupportedPhoneNumberCountriesRequestRequestTypeDef",
    "ListSupportedPhoneNumberCountriesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListVoiceConnectorGroupsRequestRequestTypeDef",
    "ListVoiceConnectorGroupsResponseTypeDef",
    "ListVoiceConnectorTerminationCredentialsRequestRequestTypeDef",
    "ListVoiceConnectorTerminationCredentialsResponseTypeDef",
    "ListVoiceConnectorsRequestRequestTypeDef",
    "ListVoiceConnectorsResponseTypeDef",
    "ListVoiceProfileDomainsRequestRequestTypeDef",
    "ListVoiceProfileDomainsResponseTypeDef",
    "ListVoiceProfilesRequestRequestTypeDef",
    "ListVoiceProfilesResponseTypeDef",
    "LoggingConfigurationTypeDef",
    "MediaInsightsConfigurationTypeDef",
    "OrderedPhoneNumberTypeDef",
    "OriginationOutputTypeDef",
    "OriginationRouteTypeDef",
    "OriginationTypeDef",
    "PaginatorConfigTypeDef",
    "ParticipantTypeDef",
    "PhoneNumberAssociationTypeDef",
    "PhoneNumberCapabilitiesTypeDef",
    "PhoneNumberCountryTypeDef",
    "PhoneNumberErrorTypeDef",
    "PhoneNumberOrderTypeDef",
    "PhoneNumberTypeDef",
    "ProxySessionTypeDef",
    "ProxyTypeDef",
    "PutSipMediaApplicationAlexaSkillConfigurationRequestRequestTypeDef",
    "PutSipMediaApplicationAlexaSkillConfigurationResponseTypeDef",
    "PutSipMediaApplicationLoggingConfigurationRequestRequestTypeDef",
    "PutSipMediaApplicationLoggingConfigurationResponseTypeDef",
    "PutVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef",
    "PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef",
    "PutVoiceConnectorExternalSystemsConfigurationRequestRequestTypeDef",
    "PutVoiceConnectorExternalSystemsConfigurationResponseTypeDef",
    "PutVoiceConnectorLoggingConfigurationRequestRequestTypeDef",
    "PutVoiceConnectorLoggingConfigurationResponseTypeDef",
    "PutVoiceConnectorOriginationRequestRequestTypeDef",
    "PutVoiceConnectorOriginationResponseTypeDef",
    "PutVoiceConnectorProxyRequestRequestTypeDef",
    "PutVoiceConnectorProxyResponseTypeDef",
    "PutVoiceConnectorStreamingConfigurationRequestRequestTypeDef",
    "PutVoiceConnectorStreamingConfigurationResponseTypeDef",
    "PutVoiceConnectorTerminationCredentialsRequestRequestTypeDef",
    "PutVoiceConnectorTerminationRequestRequestTypeDef",
    "PutVoiceConnectorTerminationResponseTypeDef",
    "ResponseMetadataTypeDef",
    "RestorePhoneNumberRequestRequestTypeDef",
    "RestorePhoneNumberResponseTypeDef",
    "SearchAvailablePhoneNumbersRequestRequestTypeDef",
    "SearchAvailablePhoneNumbersResponseTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "SipMediaApplicationAlexaSkillConfigurationOutputTypeDef",
    "SipMediaApplicationAlexaSkillConfigurationTypeDef",
    "SipMediaApplicationCallTypeDef",
    "SipMediaApplicationEndpointTypeDef",
    "SipMediaApplicationLoggingConfigurationTypeDef",
    "SipMediaApplicationTypeDef",
    "SipRuleTargetApplicationTypeDef",
    "SipRuleTypeDef",
    "SpeakerSearchDetailsTypeDef",
    "SpeakerSearchResultTypeDef",
    "SpeakerSearchTaskTypeDef",
    "StartSpeakerSearchTaskRequestRequestTypeDef",
    "StartSpeakerSearchTaskResponseTypeDef",
    "StartVoiceToneAnalysisTaskRequestRequestTypeDef",
    "StartVoiceToneAnalysisTaskResponseTypeDef",
    "StopSpeakerSearchTaskRequestRequestTypeDef",
    "StopVoiceToneAnalysisTaskRequestRequestTypeDef",
    "StreamingConfigurationOutputTypeDef",
    "StreamingConfigurationTypeDef",
    "StreamingNotificationTargetTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TerminationHealthTypeDef",
    "TerminationOutputTypeDef",
    "TerminationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateGlobalSettingsRequestRequestTypeDef",
    "UpdatePhoneNumberRequestItemTypeDef",
    "UpdatePhoneNumberRequestRequestTypeDef",
    "UpdatePhoneNumberResponseTypeDef",
    "UpdatePhoneNumberSettingsRequestRequestTypeDef",
    "UpdateProxySessionRequestRequestTypeDef",
    "UpdateProxySessionResponseTypeDef",
    "UpdateSipMediaApplicationCallRequestRequestTypeDef",
    "UpdateSipMediaApplicationCallResponseTypeDef",
    "UpdateSipMediaApplicationRequestRequestTypeDef",
    "UpdateSipMediaApplicationResponseTypeDef",
    "UpdateSipRuleRequestRequestTypeDef",
    "UpdateSipRuleResponseTypeDef",
    "UpdateVoiceConnectorGroupRequestRequestTypeDef",
    "UpdateVoiceConnectorGroupResponseTypeDef",
    "UpdateVoiceConnectorRequestRequestTypeDef",
    "UpdateVoiceConnectorResponseTypeDef",
    "UpdateVoiceProfileDomainRequestRequestTypeDef",
    "UpdateVoiceProfileDomainResponseTypeDef",
    "UpdateVoiceProfileRequestRequestTypeDef",
    "UpdateVoiceProfileResponseTypeDef",
    "ValidateE911AddressRequestRequestTypeDef",
    "ValidateE911AddressResponseTypeDef",
    "VoiceConnectorGroupTypeDef",
    "VoiceConnectorItemTypeDef",
    "VoiceConnectorSettingsTypeDef",
    "VoiceConnectorTypeDef",
    "VoiceProfileDomainSummaryTypeDef",
    "VoiceProfileDomainTypeDef",
    "VoiceProfileSummaryTypeDef",
    "VoiceProfileTypeDef",
    "VoiceToneAnalysisTaskTypeDef",
)

class AddressTypeDef(TypedDict):
    streetName: NotRequired[str]
    streetSuffix: NotRequired[str]
    postDirectional: NotRequired[str]
    preDirectional: NotRequired[str]
    streetNumber: NotRequired[str]
    city: NotRequired[str]
    state: NotRequired[str]
    postalCode: NotRequired[str]
    postalCodePlus4: NotRequired[str]
    country: NotRequired[str]

class AssociatePhoneNumbersWithVoiceConnectorGroupRequestRequestTypeDef(TypedDict):
    VoiceConnectorGroupId: str
    E164PhoneNumbers: Sequence[str]
    ForceAssociate: NotRequired[bool]

class PhoneNumberErrorTypeDef(TypedDict):
    PhoneNumberId: NotRequired[str]
    ErrorCode: NotRequired[ErrorCodeType]
    ErrorMessage: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AssociatePhoneNumbersWithVoiceConnectorRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    E164PhoneNumbers: Sequence[str]
    ForceAssociate: NotRequired[bool]

class BatchDeletePhoneNumberRequestRequestTypeDef(TypedDict):
    PhoneNumberIds: Sequence[str]

class UpdatePhoneNumberRequestItemTypeDef(TypedDict):
    PhoneNumberId: str
    ProductType: NotRequired[PhoneNumberProductTypeType]
    CallingName: NotRequired[str]
    Name: NotRequired[str]

class CallDetailsTypeDef(TypedDict):
    VoiceConnectorId: NotRequired[str]
    TransactionId: NotRequired[str]
    IsCaller: NotRequired[bool]

class CandidateAddressTypeDef(TypedDict):
    streetInfo: NotRequired[str]
    streetNumber: NotRequired[str]
    city: NotRequired[str]
    state: NotRequired[str]
    postalCode: NotRequired[str]
    postalCodePlus4: NotRequired[str]
    country: NotRequired[str]

class CreatePhoneNumberOrderRequestRequestTypeDef(TypedDict):
    ProductType: PhoneNumberProductTypeType
    E164PhoneNumbers: Sequence[str]
    Name: NotRequired[str]

class GeoMatchParamsTypeDef(TypedDict):
    Country: str
    AreaCode: str

class CreateSipMediaApplicationCallRequestRequestTypeDef(TypedDict):
    FromPhoneNumber: str
    ToPhoneNumber: str
    SipMediaApplicationId: str
    SipHeaders: NotRequired[Mapping[str, str]]
    ArgumentsMap: NotRequired[Mapping[str, str]]

class SipMediaApplicationCallTypeDef(TypedDict):
    TransactionId: NotRequired[str]

class SipMediaApplicationEndpointTypeDef(TypedDict):
    LambdaArn: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class SipRuleTargetApplicationTypeDef(TypedDict):
    SipMediaApplicationId: NotRequired[str]
    Priority: NotRequired[int]
    AwsRegion: NotRequired[str]

class VoiceConnectorItemTypeDef(TypedDict):
    VoiceConnectorId: str
    Priority: int

class VoiceConnectorTypeDef(TypedDict):
    VoiceConnectorId: NotRequired[str]
    AwsRegion: NotRequired[VoiceConnectorAwsRegionType]
    Name: NotRequired[str]
    OutboundHostName: NotRequired[str]
    RequireEncryption: NotRequired[bool]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]
    VoiceConnectorArn: NotRequired[str]
    IntegrationType: NotRequired[VoiceConnectorIntegrationTypeType]

class ServerSideEncryptionConfigurationTypeDef(TypedDict):
    KmsKeyArn: str

class CreateVoiceProfileRequestRequestTypeDef(TypedDict):
    SpeakerSearchTaskId: str

class VoiceProfileTypeDef(TypedDict):
    VoiceProfileId: NotRequired[str]
    VoiceProfileArn: NotRequired[str]
    VoiceProfileDomainId: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]
    ExpirationTimestamp: NotRequired[datetime]

class CredentialTypeDef(TypedDict):
    Username: NotRequired[str]
    Password: NotRequired[str]

class DNISEmergencyCallingConfigurationTypeDef(TypedDict):
    EmergencyPhoneNumber: str
    CallingCountry: str
    TestPhoneNumber: NotRequired[str]

class DeletePhoneNumberRequestRequestTypeDef(TypedDict):
    PhoneNumberId: str

class DeleteProxySessionRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    ProxySessionId: str

class DeleteSipMediaApplicationRequestRequestTypeDef(TypedDict):
    SipMediaApplicationId: str

class DeleteSipRuleRequestRequestTypeDef(TypedDict):
    SipRuleId: str

class DeleteVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class DeleteVoiceConnectorExternalSystemsConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class DeleteVoiceConnectorGroupRequestRequestTypeDef(TypedDict):
    VoiceConnectorGroupId: str

class DeleteVoiceConnectorOriginationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class DeleteVoiceConnectorProxyRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class DeleteVoiceConnectorRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class DeleteVoiceConnectorStreamingConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class DeleteVoiceConnectorTerminationCredentialsRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    Usernames: Sequence[str]

class DeleteVoiceConnectorTerminationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class DeleteVoiceProfileDomainRequestRequestTypeDef(TypedDict):
    VoiceProfileDomainId: str

class DeleteVoiceProfileRequestRequestTypeDef(TypedDict):
    VoiceProfileId: str

class DisassociatePhoneNumbersFromVoiceConnectorGroupRequestRequestTypeDef(TypedDict):
    VoiceConnectorGroupId: str
    E164PhoneNumbers: Sequence[str]

class DisassociatePhoneNumbersFromVoiceConnectorRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    E164PhoneNumbers: Sequence[str]

class ExternalSystemsConfigurationTypeDef(TypedDict):
    SessionBorderControllerTypes: NotRequired[List[SessionBorderControllerTypeType]]
    ContactCenterSystemTypes: NotRequired[List[ContactCenterSystemTypeType]]

class VoiceConnectorSettingsTypeDef(TypedDict):
    CdrBucket: NotRequired[str]

class GetPhoneNumberOrderRequestRequestTypeDef(TypedDict):
    PhoneNumberOrderId: str

class GetPhoneNumberRequestRequestTypeDef(TypedDict):
    PhoneNumberId: str

class GetProxySessionRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    ProxySessionId: str

class GetSipMediaApplicationAlexaSkillConfigurationRequestRequestTypeDef(TypedDict):
    SipMediaApplicationId: str

class SipMediaApplicationAlexaSkillConfigurationOutputTypeDef(TypedDict):
    AlexaSkillStatus: AlexaSkillStatusType
    AlexaSkillIds: List[str]

class GetSipMediaApplicationLoggingConfigurationRequestRequestTypeDef(TypedDict):
    SipMediaApplicationId: str

class SipMediaApplicationLoggingConfigurationTypeDef(TypedDict):
    EnableSipMediaApplicationMessageLogs: NotRequired[bool]

class GetSipMediaApplicationRequestRequestTypeDef(TypedDict):
    SipMediaApplicationId: str

class GetSipRuleRequestRequestTypeDef(TypedDict):
    SipRuleId: str

class GetSpeakerSearchTaskRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    SpeakerSearchTaskId: str

class GetVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class GetVoiceConnectorExternalSystemsConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class GetVoiceConnectorGroupRequestRequestTypeDef(TypedDict):
    VoiceConnectorGroupId: str

class GetVoiceConnectorLoggingConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class LoggingConfigurationTypeDef(TypedDict):
    EnableSIPLogs: NotRequired[bool]
    EnableMediaMetricLogs: NotRequired[bool]

class GetVoiceConnectorOriginationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class GetVoiceConnectorProxyRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class ProxyTypeDef(TypedDict):
    DefaultSessionExpiryMinutes: NotRequired[int]
    Disabled: NotRequired[bool]
    FallBackPhoneNumber: NotRequired[str]
    PhoneNumberCountries: NotRequired[List[str]]

class GetVoiceConnectorRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class GetVoiceConnectorStreamingConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class GetVoiceConnectorTerminationHealthRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class TerminationHealthTypeDef(TypedDict):
    Timestamp: NotRequired[datetime]
    Source: NotRequired[str]

class GetVoiceConnectorTerminationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class TerminationOutputTypeDef(TypedDict):
    CpsLimit: NotRequired[int]
    DefaultPhoneNumber: NotRequired[str]
    CallingRegions: NotRequired[List[str]]
    CidrAllowedList: NotRequired[List[str]]
    Disabled: NotRequired[bool]

class GetVoiceProfileDomainRequestRequestTypeDef(TypedDict):
    VoiceProfileDomainId: str

class GetVoiceProfileRequestRequestTypeDef(TypedDict):
    VoiceProfileId: str

class GetVoiceToneAnalysisTaskRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    VoiceToneAnalysisTaskId: str
    IsCaller: bool

class ListPhoneNumberOrdersRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListPhoneNumbersRequestRequestTypeDef(TypedDict):
    Status: NotRequired[str]
    ProductType: NotRequired[PhoneNumberProductTypeType]
    FilterName: NotRequired[PhoneNumberAssociationNameType]
    FilterValue: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListProxySessionsRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    Status: NotRequired[ProxySessionStatusType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListSipMediaApplicationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListSipRulesRequestRequestTypeDef(TypedDict):
    SipMediaApplicationId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListSupportedPhoneNumberCountriesRequestRequestTypeDef(TypedDict):
    ProductType: PhoneNumberProductTypeType

class PhoneNumberCountryTypeDef(TypedDict):
    CountryCode: NotRequired[str]
    SupportedPhoneNumberTypes: NotRequired[List[PhoneNumberTypeType]]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str

class ListVoiceConnectorGroupsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListVoiceConnectorTerminationCredentialsRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str

class ListVoiceConnectorsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListVoiceProfileDomainsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class VoiceProfileDomainSummaryTypeDef(TypedDict):
    VoiceProfileDomainId: NotRequired[str]
    VoiceProfileDomainArn: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]

class ListVoiceProfilesRequestRequestTypeDef(TypedDict):
    VoiceProfileDomainId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class VoiceProfileSummaryTypeDef(TypedDict):
    VoiceProfileId: NotRequired[str]
    VoiceProfileArn: NotRequired[str]
    VoiceProfileDomainId: NotRequired[str]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]
    ExpirationTimestamp: NotRequired[datetime]

class MediaInsightsConfigurationTypeDef(TypedDict):
    Disabled: NotRequired[bool]
    ConfigurationArn: NotRequired[str]

class OrderedPhoneNumberTypeDef(TypedDict):
    E164PhoneNumber: NotRequired[str]
    Status: NotRequired[OrderedPhoneNumberStatusType]

OriginationRouteTypeDef = TypedDict(
    "OriginationRouteTypeDef",
    {
        "Host": NotRequired[str],
        "Port": NotRequired[int],
        "Protocol": NotRequired[OriginationRouteProtocolType],
        "Priority": NotRequired[int],
        "Weight": NotRequired[int],
    },
)

class ParticipantTypeDef(TypedDict):
    PhoneNumber: NotRequired[str]
    ProxyPhoneNumber: NotRequired[str]

class PhoneNumberAssociationTypeDef(TypedDict):
    Value: NotRequired[str]
    Name: NotRequired[PhoneNumberAssociationNameType]
    AssociatedTimestamp: NotRequired[datetime]

class PhoneNumberCapabilitiesTypeDef(TypedDict):
    InboundCall: NotRequired[bool]
    OutboundCall: NotRequired[bool]
    InboundSMS: NotRequired[bool]
    OutboundSMS: NotRequired[bool]
    InboundMMS: NotRequired[bool]
    OutboundMMS: NotRequired[bool]

class SipMediaApplicationAlexaSkillConfigurationTypeDef(TypedDict):
    AlexaSkillStatus: AlexaSkillStatusType
    AlexaSkillIds: Sequence[str]

class PutVoiceConnectorExternalSystemsConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    SessionBorderControllerTypes: NotRequired[Sequence[SessionBorderControllerTypeType]]
    ContactCenterSystemTypes: NotRequired[Sequence[ContactCenterSystemTypeType]]

class PutVoiceConnectorProxyRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    DefaultSessionExpiryMinutes: int
    PhoneNumberPoolCountries: Sequence[str]
    FallBackPhoneNumber: NotRequired[str]
    Disabled: NotRequired[bool]

class TerminationTypeDef(TypedDict):
    CpsLimit: NotRequired[int]
    DefaultPhoneNumber: NotRequired[str]
    CallingRegions: NotRequired[Sequence[str]]
    CidrAllowedList: NotRequired[Sequence[str]]
    Disabled: NotRequired[bool]

class RestorePhoneNumberRequestRequestTypeDef(TypedDict):
    PhoneNumberId: str

class SearchAvailablePhoneNumbersRequestRequestTypeDef(TypedDict):
    AreaCode: NotRequired[str]
    City: NotRequired[str]
    Country: NotRequired[str]
    State: NotRequired[str]
    TollFreePrefix: NotRequired[str]
    PhoneNumberType: NotRequired[PhoneNumberTypeType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class SpeakerSearchResultTypeDef(TypedDict):
    ConfidenceScore: NotRequired[float]
    VoiceProfileId: NotRequired[str]

class StartSpeakerSearchTaskRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    TransactionId: str
    VoiceProfileDomainId: str
    ClientRequestToken: NotRequired[str]
    CallLeg: NotRequired[CallLegTypeType]

class StartVoiceToneAnalysisTaskRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    TransactionId: str
    LanguageCode: Literal["en-US"]
    ClientRequestToken: NotRequired[str]

class StopSpeakerSearchTaskRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    SpeakerSearchTaskId: str

class StopVoiceToneAnalysisTaskRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    VoiceToneAnalysisTaskId: str

class StreamingNotificationTargetTypeDef(TypedDict):
    NotificationTarget: NotRequired[NotificationTargetType]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]

class UpdatePhoneNumberRequestRequestTypeDef(TypedDict):
    PhoneNumberId: str
    ProductType: NotRequired[PhoneNumberProductTypeType]
    CallingName: NotRequired[str]
    Name: NotRequired[str]

class UpdatePhoneNumberSettingsRequestRequestTypeDef(TypedDict):
    CallingName: str

class UpdateProxySessionRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    ProxySessionId: str
    Capabilities: Sequence[CapabilityType]
    ExpiryMinutes: NotRequired[int]

class UpdateSipMediaApplicationCallRequestRequestTypeDef(TypedDict):
    SipMediaApplicationId: str
    TransactionId: str
    Arguments: Mapping[str, str]

class UpdateVoiceConnectorRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    Name: str
    RequireEncryption: bool

class UpdateVoiceProfileDomainRequestRequestTypeDef(TypedDict):
    VoiceProfileDomainId: str
    Name: NotRequired[str]
    Description: NotRequired[str]

class UpdateVoiceProfileRequestRequestTypeDef(TypedDict):
    VoiceProfileId: str
    SpeakerSearchTaskId: str

class ValidateE911AddressRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    StreetNumber: str
    StreetInfo: str
    City: str
    State: str
    Country: str
    PostalCode: str

class AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef(TypedDict):
    PhoneNumberErrors: List[PhoneNumberErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef(TypedDict):
    PhoneNumberErrors: List[PhoneNumberErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDeletePhoneNumberResponseTypeDef(TypedDict):
    PhoneNumberErrors: List[PhoneNumberErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchUpdatePhoneNumberResponseTypeDef(TypedDict):
    PhoneNumberErrors: List[PhoneNumberErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef(TypedDict):
    PhoneNumberErrors: List[PhoneNumberErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef(TypedDict):
    PhoneNumberErrors: List[PhoneNumberErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetPhoneNumberSettingsResponseTypeDef(TypedDict):
    CallingName: str
    CallingNameUpdatedTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ListAvailableVoiceConnectorRegionsResponseTypeDef(TypedDict):
    VoiceConnectorRegions: List[VoiceConnectorAwsRegionType]
    ResponseMetadata: ResponseMetadataTypeDef

class ListVoiceConnectorTerminationCredentialsResponseTypeDef(TypedDict):
    Usernames: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class SearchAvailablePhoneNumbersResponseTypeDef(TypedDict):
    E164PhoneNumbers: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class BatchUpdatePhoneNumberRequestRequestTypeDef(TypedDict):
    UpdatePhoneNumberRequestItems: Sequence[UpdatePhoneNumberRequestItemTypeDef]

class VoiceToneAnalysisTaskTypeDef(TypedDict):
    VoiceToneAnalysisTaskId: NotRequired[str]
    VoiceToneAnalysisTaskStatus: NotRequired[str]
    CallDetails: NotRequired[CallDetailsTypeDef]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]
    StartedTimestamp: NotRequired[datetime]
    StatusMessage: NotRequired[str]

class ValidateE911AddressResponseTypeDef(TypedDict):
    ValidationResult: int
    AddressExternalId: str
    Address: AddressTypeDef
    CandidateAddressList: List[CandidateAddressTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateProxySessionRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    ParticipantPhoneNumbers: Sequence[str]
    Capabilities: Sequence[CapabilityType]
    Name: NotRequired[str]
    ExpiryMinutes: NotRequired[int]
    NumberSelectionBehavior: NotRequired[NumberSelectionBehaviorType]
    GeoMatchLevel: NotRequired[GeoMatchLevelType]
    GeoMatchParams: NotRequired[GeoMatchParamsTypeDef]

class CreateSipMediaApplicationCallResponseTypeDef(TypedDict):
    SipMediaApplicationCall: SipMediaApplicationCallTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSipMediaApplicationCallResponseTypeDef(TypedDict):
    SipMediaApplicationCall: SipMediaApplicationCallTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SipMediaApplicationTypeDef(TypedDict):
    SipMediaApplicationId: NotRequired[str]
    AwsRegion: NotRequired[str]
    Name: NotRequired[str]
    Endpoints: NotRequired[List[SipMediaApplicationEndpointTypeDef]]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]
    SipMediaApplicationArn: NotRequired[str]

class UpdateSipMediaApplicationRequestRequestTypeDef(TypedDict):
    SipMediaApplicationId: str
    Name: NotRequired[str]
    Endpoints: NotRequired[Sequence[SipMediaApplicationEndpointTypeDef]]

class CreateSipMediaApplicationRequestRequestTypeDef(TypedDict):
    AwsRegion: str
    Name: str
    Endpoints: Sequence[SipMediaApplicationEndpointTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateVoiceConnectorRequestRequestTypeDef(TypedDict):
    Name: str
    RequireEncryption: bool
    AwsRegion: NotRequired[VoiceConnectorAwsRegionType]
    Tags: NotRequired[Sequence[TagTypeDef]]
    IntegrationType: NotRequired[VoiceConnectorIntegrationTypeType]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]

class CreateSipRuleRequestRequestTypeDef(TypedDict):
    Name: str
    TriggerType: SipRuleTriggerTypeType
    TriggerValue: str
    Disabled: NotRequired[bool]
    TargetApplications: NotRequired[Sequence[SipRuleTargetApplicationTypeDef]]

class SipRuleTypeDef(TypedDict):
    SipRuleId: NotRequired[str]
    Name: NotRequired[str]
    Disabled: NotRequired[bool]
    TriggerType: NotRequired[SipRuleTriggerTypeType]
    TriggerValue: NotRequired[str]
    TargetApplications: NotRequired[List[SipRuleTargetApplicationTypeDef]]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]

class UpdateSipRuleRequestRequestTypeDef(TypedDict):
    SipRuleId: str
    Name: str
    Disabled: NotRequired[bool]
    TargetApplications: NotRequired[Sequence[SipRuleTargetApplicationTypeDef]]

class CreateVoiceConnectorGroupRequestRequestTypeDef(TypedDict):
    Name: str
    VoiceConnectorItems: NotRequired[Sequence[VoiceConnectorItemTypeDef]]

class UpdateVoiceConnectorGroupRequestRequestTypeDef(TypedDict):
    VoiceConnectorGroupId: str
    Name: str
    VoiceConnectorItems: Sequence[VoiceConnectorItemTypeDef]

class VoiceConnectorGroupTypeDef(TypedDict):
    VoiceConnectorGroupId: NotRequired[str]
    Name: NotRequired[str]
    VoiceConnectorItems: NotRequired[List[VoiceConnectorItemTypeDef]]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]
    VoiceConnectorGroupArn: NotRequired[str]

class CreateVoiceConnectorResponseTypeDef(TypedDict):
    VoiceConnector: VoiceConnectorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceConnectorResponseTypeDef(TypedDict):
    VoiceConnector: VoiceConnectorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListVoiceConnectorsResponseTypeDef(TypedDict):
    VoiceConnectors: List[VoiceConnectorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateVoiceConnectorResponseTypeDef(TypedDict):
    VoiceConnector: VoiceConnectorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateVoiceProfileDomainRequestRequestTypeDef(TypedDict):
    Name: str
    ServerSideEncryptionConfiguration: ServerSideEncryptionConfigurationTypeDef
    Description: NotRequired[str]
    ClientRequestToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class VoiceProfileDomainTypeDef(TypedDict):
    VoiceProfileDomainId: NotRequired[str]
    VoiceProfileDomainArn: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    ServerSideEncryptionConfiguration: NotRequired[ServerSideEncryptionConfigurationTypeDef]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]

class CreateVoiceProfileResponseTypeDef(TypedDict):
    VoiceProfile: VoiceProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceProfileResponseTypeDef(TypedDict):
    VoiceProfile: VoiceProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateVoiceProfileResponseTypeDef(TypedDict):
    VoiceProfile: VoiceProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorTerminationCredentialsRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    Credentials: NotRequired[Sequence[CredentialTypeDef]]

class EmergencyCallingConfigurationOutputTypeDef(TypedDict):
    DNIS: NotRequired[List[DNISEmergencyCallingConfigurationTypeDef]]

class EmergencyCallingConfigurationTypeDef(TypedDict):
    DNIS: NotRequired[Sequence[DNISEmergencyCallingConfigurationTypeDef]]

class GetVoiceConnectorExternalSystemsConfigurationResponseTypeDef(TypedDict):
    ExternalSystemsConfiguration: ExternalSystemsConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorExternalSystemsConfigurationResponseTypeDef(TypedDict):
    ExternalSystemsConfiguration: ExternalSystemsConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetGlobalSettingsResponseTypeDef(TypedDict):
    VoiceConnector: VoiceConnectorSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGlobalSettingsRequestRequestTypeDef(TypedDict):
    VoiceConnector: NotRequired[VoiceConnectorSettingsTypeDef]

class GetSipMediaApplicationAlexaSkillConfigurationResponseTypeDef(TypedDict):
    SipMediaApplicationAlexaSkillConfiguration: (
        SipMediaApplicationAlexaSkillConfigurationOutputTypeDef
    )
    ResponseMetadata: ResponseMetadataTypeDef

class PutSipMediaApplicationAlexaSkillConfigurationResponseTypeDef(TypedDict):
    SipMediaApplicationAlexaSkillConfiguration: (
        SipMediaApplicationAlexaSkillConfigurationOutputTypeDef
    )
    ResponseMetadata: ResponseMetadataTypeDef

class GetSipMediaApplicationLoggingConfigurationResponseTypeDef(TypedDict):
    SipMediaApplicationLoggingConfiguration: SipMediaApplicationLoggingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutSipMediaApplicationLoggingConfigurationRequestRequestTypeDef(TypedDict):
    SipMediaApplicationId: str
    SipMediaApplicationLoggingConfiguration: NotRequired[
        SipMediaApplicationLoggingConfigurationTypeDef
    ]

class PutSipMediaApplicationLoggingConfigurationResponseTypeDef(TypedDict):
    SipMediaApplicationLoggingConfiguration: SipMediaApplicationLoggingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceConnectorLoggingConfigurationResponseTypeDef(TypedDict):
    LoggingConfiguration: LoggingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorLoggingConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    LoggingConfiguration: LoggingConfigurationTypeDef

class PutVoiceConnectorLoggingConfigurationResponseTypeDef(TypedDict):
    LoggingConfiguration: LoggingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceConnectorProxyResponseTypeDef(TypedDict):
    Proxy: ProxyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorProxyResponseTypeDef(TypedDict):
    Proxy: ProxyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceConnectorTerminationHealthResponseTypeDef(TypedDict):
    TerminationHealth: TerminationHealthTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceConnectorTerminationResponseTypeDef(TypedDict):
    Termination: TerminationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorTerminationResponseTypeDef(TypedDict):
    Termination: TerminationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListSipMediaApplicationsRequestListSipMediaApplicationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSipRulesRequestListSipRulesPaginateTypeDef(TypedDict):
    SipMediaApplicationId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSupportedPhoneNumberCountriesResponseTypeDef(TypedDict):
    PhoneNumberCountries: List[PhoneNumberCountryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListVoiceProfileDomainsResponseTypeDef(TypedDict):
    VoiceProfileDomains: List[VoiceProfileDomainSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListVoiceProfilesResponseTypeDef(TypedDict):
    VoiceProfiles: List[VoiceProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PhoneNumberOrderTypeDef(TypedDict):
    PhoneNumberOrderId: NotRequired[str]
    ProductType: NotRequired[PhoneNumberProductTypeType]
    Status: NotRequired[PhoneNumberOrderStatusType]
    OrderType: NotRequired[PhoneNumberOrderTypeType]
    OrderedPhoneNumbers: NotRequired[List[OrderedPhoneNumberTypeDef]]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]

class OriginationOutputTypeDef(TypedDict):
    Routes: NotRequired[List[OriginationRouteTypeDef]]
    Disabled: NotRequired[bool]

class OriginationTypeDef(TypedDict):
    Routes: NotRequired[Sequence[OriginationRouteTypeDef]]
    Disabled: NotRequired[bool]

class ProxySessionTypeDef(TypedDict):
    VoiceConnectorId: NotRequired[str]
    ProxySessionId: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[ProxySessionStatusType]
    ExpiryMinutes: NotRequired[int]
    Capabilities: NotRequired[List[CapabilityType]]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]
    EndedTimestamp: NotRequired[datetime]
    Participants: NotRequired[List[ParticipantTypeDef]]
    NumberSelectionBehavior: NotRequired[NumberSelectionBehaviorType]
    GeoMatchLevel: NotRequired[GeoMatchLevelType]
    GeoMatchParams: NotRequired[GeoMatchParamsTypeDef]

PhoneNumberTypeDef = TypedDict(
    "PhoneNumberTypeDef",
    {
        "PhoneNumberId": NotRequired[str],
        "E164PhoneNumber": NotRequired[str],
        "Country": NotRequired[str],
        "Type": NotRequired[PhoneNumberTypeType],
        "ProductType": NotRequired[PhoneNumberProductTypeType],
        "Status": NotRequired[PhoneNumberStatusType],
        "Capabilities": NotRequired[PhoneNumberCapabilitiesTypeDef],
        "Associations": NotRequired[List[PhoneNumberAssociationTypeDef]],
        "CallingName": NotRequired[str],
        "CallingNameStatus": NotRequired[CallingNameStatusType],
        "CreatedTimestamp": NotRequired[datetime],
        "UpdatedTimestamp": NotRequired[datetime],
        "DeletionTimestamp": NotRequired[datetime],
        "OrderId": NotRequired[str],
        "Name": NotRequired[str],
    },
)

class PutSipMediaApplicationAlexaSkillConfigurationRequestRequestTypeDef(TypedDict):
    SipMediaApplicationId: str
    SipMediaApplicationAlexaSkillConfiguration: NotRequired[
        SipMediaApplicationAlexaSkillConfigurationTypeDef
    ]

class PutVoiceConnectorTerminationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    Termination: TerminationTypeDef

class SpeakerSearchDetailsTypeDef(TypedDict):
    Results: NotRequired[List[SpeakerSearchResultTypeDef]]
    VoiceprintGenerationStatus: NotRequired[str]

class StreamingConfigurationOutputTypeDef(TypedDict):
    DataRetentionInHours: int
    Disabled: bool
    StreamingNotificationTargets: NotRequired[List[StreamingNotificationTargetTypeDef]]
    MediaInsightsConfiguration: NotRequired[MediaInsightsConfigurationTypeDef]

class StreamingConfigurationTypeDef(TypedDict):
    DataRetentionInHours: int
    Disabled: bool
    StreamingNotificationTargets: NotRequired[Sequence[StreamingNotificationTargetTypeDef]]
    MediaInsightsConfiguration: NotRequired[MediaInsightsConfigurationTypeDef]

class GetVoiceToneAnalysisTaskResponseTypeDef(TypedDict):
    VoiceToneAnalysisTask: VoiceToneAnalysisTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartVoiceToneAnalysisTaskResponseTypeDef(TypedDict):
    VoiceToneAnalysisTask: VoiceToneAnalysisTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSipMediaApplicationResponseTypeDef(TypedDict):
    SipMediaApplication: SipMediaApplicationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSipMediaApplicationResponseTypeDef(TypedDict):
    SipMediaApplication: SipMediaApplicationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListSipMediaApplicationsResponseTypeDef(TypedDict):
    SipMediaApplications: List[SipMediaApplicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateSipMediaApplicationResponseTypeDef(TypedDict):
    SipMediaApplication: SipMediaApplicationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSipRuleResponseTypeDef(TypedDict):
    SipRule: SipRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSipRuleResponseTypeDef(TypedDict):
    SipRule: SipRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListSipRulesResponseTypeDef(TypedDict):
    SipRules: List[SipRuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateSipRuleResponseTypeDef(TypedDict):
    SipRule: SipRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateVoiceConnectorGroupResponseTypeDef(TypedDict):
    VoiceConnectorGroup: VoiceConnectorGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceConnectorGroupResponseTypeDef(TypedDict):
    VoiceConnectorGroup: VoiceConnectorGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListVoiceConnectorGroupsResponseTypeDef(TypedDict):
    VoiceConnectorGroups: List[VoiceConnectorGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateVoiceConnectorGroupResponseTypeDef(TypedDict):
    VoiceConnectorGroup: VoiceConnectorGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateVoiceProfileDomainResponseTypeDef(TypedDict):
    VoiceProfileDomain: VoiceProfileDomainTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceProfileDomainResponseTypeDef(TypedDict):
    VoiceProfileDomain: VoiceProfileDomainTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateVoiceProfileDomainResponseTypeDef(TypedDict):
    VoiceProfileDomain: VoiceProfileDomainTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef(TypedDict):
    EmergencyCallingConfiguration: EmergencyCallingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef(TypedDict):
    EmergencyCallingConfiguration: EmergencyCallingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorEmergencyCallingConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    EmergencyCallingConfiguration: EmergencyCallingConfigurationTypeDef

class CreatePhoneNumberOrderResponseTypeDef(TypedDict):
    PhoneNumberOrder: PhoneNumberOrderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetPhoneNumberOrderResponseTypeDef(TypedDict):
    PhoneNumberOrder: PhoneNumberOrderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListPhoneNumberOrdersResponseTypeDef(TypedDict):
    PhoneNumberOrders: List[PhoneNumberOrderTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetVoiceConnectorOriginationResponseTypeDef(TypedDict):
    Origination: OriginationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorOriginationResponseTypeDef(TypedDict):
    Origination: OriginationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorOriginationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    Origination: OriginationTypeDef

class CreateProxySessionResponseTypeDef(TypedDict):
    ProxySession: ProxySessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetProxySessionResponseTypeDef(TypedDict):
    ProxySession: ProxySessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListProxySessionsResponseTypeDef(TypedDict):
    ProxySessions: List[ProxySessionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateProxySessionResponseTypeDef(TypedDict):
    ProxySession: ProxySessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetPhoneNumberResponseTypeDef(TypedDict):
    PhoneNumber: PhoneNumberTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListPhoneNumbersResponseTypeDef(TypedDict):
    PhoneNumbers: List[PhoneNumberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class RestorePhoneNumberResponseTypeDef(TypedDict):
    PhoneNumber: PhoneNumberTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePhoneNumberResponseTypeDef(TypedDict):
    PhoneNumber: PhoneNumberTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SpeakerSearchTaskTypeDef(TypedDict):
    SpeakerSearchTaskId: NotRequired[str]
    SpeakerSearchTaskStatus: NotRequired[str]
    CallDetails: NotRequired[CallDetailsTypeDef]
    SpeakerSearchDetails: NotRequired[SpeakerSearchDetailsTypeDef]
    CreatedTimestamp: NotRequired[datetime]
    UpdatedTimestamp: NotRequired[datetime]
    StartedTimestamp: NotRequired[datetime]
    StatusMessage: NotRequired[str]

class GetVoiceConnectorStreamingConfigurationResponseTypeDef(TypedDict):
    StreamingConfiguration: StreamingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorStreamingConfigurationResponseTypeDef(TypedDict):
    StreamingConfiguration: StreamingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutVoiceConnectorStreamingConfigurationRequestRequestTypeDef(TypedDict):
    VoiceConnectorId: str
    StreamingConfiguration: StreamingConfigurationTypeDef

class GetSpeakerSearchTaskResponseTypeDef(TypedDict):
    SpeakerSearchTask: SpeakerSearchTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartSpeakerSearchTaskResponseTypeDef(TypedDict):
    SpeakerSearchTask: SpeakerSearchTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
