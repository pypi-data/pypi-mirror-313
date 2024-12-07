"""
Type annotations for bedrock-data-automation-runtime service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation_runtime/type_defs/)

Usage::

    ```python
    from types_boto3_bedrock_data_automation_runtime.type_defs import BlueprintTypeDef

    data: BlueprintTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, Mapping, Sequence

from .literals import AutomationJobStatusType, BlueprintStageType, DataAutomationStageType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "BlueprintTypeDef",
    "DataAutomationConfigurationTypeDef",
    "EncryptionConfigurationTypeDef",
    "EventBridgeConfigurationTypeDef",
    "GetDataAutomationStatusRequestRequestTypeDef",
    "GetDataAutomationStatusResponseTypeDef",
    "InputConfigurationTypeDef",
    "InvokeDataAutomationAsyncRequestRequestTypeDef",
    "InvokeDataAutomationAsyncResponseTypeDef",
    "NotificationConfigurationTypeDef",
    "OutputConfigurationTypeDef",
    "ResponseMetadataTypeDef",
)


class BlueprintTypeDef(TypedDict):
    blueprintArn: str
    version: NotRequired[str]
    stage: NotRequired[BlueprintStageType]


class DataAutomationConfigurationTypeDef(TypedDict):
    dataAutomationArn: str
    stage: NotRequired[DataAutomationStageType]


class EncryptionConfigurationTypeDef(TypedDict):
    kmsKeyId: str
    kmsEncryptionContext: NotRequired[Mapping[str, str]]


class EventBridgeConfigurationTypeDef(TypedDict):
    eventBridgeEnabled: bool


class GetDataAutomationStatusRequestRequestTypeDef(TypedDict):
    invocationArn: str


class OutputConfigurationTypeDef(TypedDict):
    s3Uri: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class InputConfigurationTypeDef(TypedDict):
    s3Uri: str


class NotificationConfigurationTypeDef(TypedDict):
    eventBridgeConfiguration: EventBridgeConfigurationTypeDef


class GetDataAutomationStatusResponseTypeDef(TypedDict):
    status: AutomationJobStatusType
    errorType: str
    errorMessage: str
    outputConfiguration: OutputConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class InvokeDataAutomationAsyncResponseTypeDef(TypedDict):
    invocationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class InvokeDataAutomationAsyncRequestRequestTypeDef(TypedDict):
    inputConfiguration: InputConfigurationTypeDef
    outputConfiguration: OutputConfigurationTypeDef
    clientToken: NotRequired[str]
    dataAutomationConfiguration: NotRequired[DataAutomationConfigurationTypeDef]
    encryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    notificationConfiguration: NotRequired[NotificationConfigurationTypeDef]
    blueprints: NotRequired[Sequence[BlueprintTypeDef]]
