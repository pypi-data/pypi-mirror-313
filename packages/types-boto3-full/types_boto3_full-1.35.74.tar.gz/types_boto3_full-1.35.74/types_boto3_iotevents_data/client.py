"""
Type annotations for iotevents-data service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_iotevents_data.client import IoTEventsDataClient

    session = Session()
    client: IoTEventsDataClient = session.client("iotevents-data")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    BatchAcknowledgeAlarmRequestRequestTypeDef,
    BatchAcknowledgeAlarmResponseTypeDef,
    BatchDeleteDetectorRequestRequestTypeDef,
    BatchDeleteDetectorResponseTypeDef,
    BatchDisableAlarmRequestRequestTypeDef,
    BatchDisableAlarmResponseTypeDef,
    BatchEnableAlarmRequestRequestTypeDef,
    BatchEnableAlarmResponseTypeDef,
    BatchPutMessageRequestRequestTypeDef,
    BatchPutMessageResponseTypeDef,
    BatchResetAlarmRequestRequestTypeDef,
    BatchResetAlarmResponseTypeDef,
    BatchSnoozeAlarmRequestRequestTypeDef,
    BatchSnoozeAlarmResponseTypeDef,
    BatchUpdateDetectorRequestRequestTypeDef,
    BatchUpdateDetectorResponseTypeDef,
    DescribeAlarmRequestRequestTypeDef,
    DescribeAlarmResponseTypeDef,
    DescribeDetectorRequestRequestTypeDef,
    DescribeDetectorResponseTypeDef,
    ListAlarmsRequestRequestTypeDef,
    ListAlarmsResponseTypeDef,
    ListDetectorsRequestRequestTypeDef,
    ListDetectorsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("IoTEventsDataClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class IoTEventsDataClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTEventsDataClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data.html#IoTEventsData.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/#close)
        """

    def batch_acknowledge_alarm(
        self, **kwargs: Unpack[BatchAcknowledgeAlarmRequestRequestTypeDef]
    ) -> BatchAcknowledgeAlarmResponseTypeDef:
        """
        Acknowledges one or more alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data/client/batch_acknowledge_alarm.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/#batch_acknowledge_alarm)
        """

    def batch_delete_detector(
        self, **kwargs: Unpack[BatchDeleteDetectorRequestRequestTypeDef]
    ) -> BatchDeleteDetectorResponseTypeDef:
        """
        Deletes one or more detectors that were created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data/client/batch_delete_detector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/#batch_delete_detector)
        """

    def batch_disable_alarm(
        self, **kwargs: Unpack[BatchDisableAlarmRequestRequestTypeDef]
    ) -> BatchDisableAlarmResponseTypeDef:
        """
        Disables one or more alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data/client/batch_disable_alarm.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/#batch_disable_alarm)
        """

    def batch_enable_alarm(
        self, **kwargs: Unpack[BatchEnableAlarmRequestRequestTypeDef]
    ) -> BatchEnableAlarmResponseTypeDef:
        """
        Enables one or more alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data/client/batch_enable_alarm.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/#batch_enable_alarm)
        """

    def batch_put_message(
        self, **kwargs: Unpack[BatchPutMessageRequestRequestTypeDef]
    ) -> BatchPutMessageResponseTypeDef:
        """
        Sends a set of messages to the IoT Events system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data/client/batch_put_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/#batch_put_message)
        """

    def batch_reset_alarm(
        self, **kwargs: Unpack[BatchResetAlarmRequestRequestTypeDef]
    ) -> BatchResetAlarmResponseTypeDef:
        """
        Resets one or more alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data/client/batch_reset_alarm.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/#batch_reset_alarm)
        """

    def batch_snooze_alarm(
        self, **kwargs: Unpack[BatchSnoozeAlarmRequestRequestTypeDef]
    ) -> BatchSnoozeAlarmResponseTypeDef:
        """
        Changes one or more alarms to the snooze mode.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data/client/batch_snooze_alarm.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/#batch_snooze_alarm)
        """

    def batch_update_detector(
        self, **kwargs: Unpack[BatchUpdateDetectorRequestRequestTypeDef]
    ) -> BatchUpdateDetectorResponseTypeDef:
        """
        Updates the state, variable values, and timer settings of one or more detectors
        (instances) of a specified detector model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data/client/batch_update_detector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/#batch_update_detector)
        """

    def describe_alarm(
        self, **kwargs: Unpack[DescribeAlarmRequestRequestTypeDef]
    ) -> DescribeAlarmResponseTypeDef:
        """
        Retrieves information about an alarm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data/client/describe_alarm.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/#describe_alarm)
        """

    def describe_detector(
        self, **kwargs: Unpack[DescribeDetectorRequestRequestTypeDef]
    ) -> DescribeDetectorResponseTypeDef:
        """
        Returns information about the specified detector (instance).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data/client/describe_detector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/#describe_detector)
        """

    def list_alarms(
        self, **kwargs: Unpack[ListAlarmsRequestRequestTypeDef]
    ) -> ListAlarmsResponseTypeDef:
        """
        Lists one or more alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data/client/list_alarms.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/#list_alarms)
        """

    def list_detectors(
        self, **kwargs: Unpack[ListDetectorsRequestRequestTypeDef]
    ) -> ListDetectorsResponseTypeDef:
        """
        Lists detectors (the instances of a detector model).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents-data/client/list_detectors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotevents_data/client/#list_detectors)
        """
