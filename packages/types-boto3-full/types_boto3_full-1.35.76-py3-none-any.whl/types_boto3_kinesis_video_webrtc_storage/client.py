"""
Type annotations for kinesis-video-webrtc-storage service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_webrtc_storage/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_kinesis_video_webrtc_storage.client import KinesisVideoWebRTCStorageClient

    session = Session()
    client: KinesisVideoWebRTCStorageClient = session.client("kinesis-video-webrtc-storage")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    EmptyResponseMetadataTypeDef,
    JoinStorageSessionAsViewerInputRequestTypeDef,
    JoinStorageSessionInputRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("KinesisVideoWebRTCStorageClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientLimitExceededException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class KinesisVideoWebRTCStorageClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-webrtc-storage.html#KinesisVideoWebRTCStorage.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_webrtc_storage/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KinesisVideoWebRTCStorageClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-webrtc-storage.html#KinesisVideoWebRTCStorage.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_webrtc_storage/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-webrtc-storage/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_webrtc_storage/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-webrtc-storage/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_webrtc_storage/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-webrtc-storage/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_webrtc_storage/client/#close)
        """

    def join_storage_session(
        self, **kwargs: Unpack[JoinStorageSessionInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Before using this API, you must call the
        <code>GetSignalingChannelEndpoint</code> API to request the WEBRTC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-webrtc-storage/client/join_storage_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_webrtc_storage/client/#join_storage_session)
        """

    def join_storage_session_as_viewer(
        self, **kwargs: Unpack[JoinStorageSessionAsViewerInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Join the ongoing one way-video and/or multi-way audio WebRTC session as a
        viewer for an input channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-webrtc-storage/client/join_storage_session_as_viewer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_webrtc_storage/client/#join_storage_session_as_viewer)
        """
