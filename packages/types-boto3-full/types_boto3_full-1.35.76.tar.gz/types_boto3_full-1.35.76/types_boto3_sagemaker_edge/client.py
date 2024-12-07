"""
Type annotations for sagemaker-edge service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_edge/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sagemaker_edge.client import SagemakerEdgeManagerClient

    session = Session()
    client: SagemakerEdgeManagerClient = session.client("sagemaker-edge")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    EmptyResponseMetadataTypeDef,
    GetDeploymentsRequestRequestTypeDef,
    GetDeploymentsResultTypeDef,
    GetDeviceRegistrationRequestRequestTypeDef,
    GetDeviceRegistrationResultTypeDef,
    SendHeartbeatRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SagemakerEdgeManagerClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]


class SagemakerEdgeManagerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-edge.html#SagemakerEdgeManager.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_edge/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SagemakerEdgeManagerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-edge.html#SagemakerEdgeManager.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_edge/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-edge/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_edge/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-edge/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_edge/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-edge/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_edge/client/#close)
        """

    def get_deployments(
        self, **kwargs: Unpack[GetDeploymentsRequestRequestTypeDef]
    ) -> GetDeploymentsResultTypeDef:
        """
        Use to get the active deployments from a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-edge/client/get_deployments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_edge/client/#get_deployments)
        """

    def get_device_registration(
        self, **kwargs: Unpack[GetDeviceRegistrationRequestRequestTypeDef]
    ) -> GetDeviceRegistrationResultTypeDef:
        """
        Use to check if a device is registered with SageMaker Edge Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-edge/client/get_device_registration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_edge/client/#get_device_registration)
        """

    def send_heartbeat(
        self, **kwargs: Unpack[SendHeartbeatRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Use to get the current status of devices registered on SageMaker Edge Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-edge/client/send_heartbeat.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_edge/client/#send_heartbeat)
        """
