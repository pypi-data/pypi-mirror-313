"""
Type annotations for cognito-sync service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_cognito_sync.client import CognitoSyncClient

    session = Session()
    client: CognitoSyncClient = session.client("cognito-sync")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    BulkPublishRequestRequestTypeDef,
    BulkPublishResponseTypeDef,
    DeleteDatasetRequestRequestTypeDef,
    DeleteDatasetResponseTypeDef,
    DescribeDatasetRequestRequestTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeIdentityPoolUsageRequestRequestTypeDef,
    DescribeIdentityPoolUsageResponseTypeDef,
    DescribeIdentityUsageRequestRequestTypeDef,
    DescribeIdentityUsageResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetBulkPublishDetailsRequestRequestTypeDef,
    GetBulkPublishDetailsResponseTypeDef,
    GetCognitoEventsRequestRequestTypeDef,
    GetCognitoEventsResponseTypeDef,
    GetIdentityPoolConfigurationRequestRequestTypeDef,
    GetIdentityPoolConfigurationResponseTypeDef,
    ListDatasetsRequestRequestTypeDef,
    ListDatasetsResponseTypeDef,
    ListIdentityPoolUsageRequestRequestTypeDef,
    ListIdentityPoolUsageResponseTypeDef,
    ListRecordsRequestRequestTypeDef,
    ListRecordsResponseTypeDef,
    RegisterDeviceRequestRequestTypeDef,
    RegisterDeviceResponseTypeDef,
    SetCognitoEventsRequestRequestTypeDef,
    SetIdentityPoolConfigurationRequestRequestTypeDef,
    SetIdentityPoolConfigurationResponseTypeDef,
    SubscribeToDatasetRequestRequestTypeDef,
    UnsubscribeFromDatasetRequestRequestTypeDef,
    UpdateRecordsRequestRequestTypeDef,
    UpdateRecordsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("CognitoSyncClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AlreadyStreamedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    DuplicateRequestException: Type[BotocoreClientError]
    InternalErrorException: Type[BotocoreClientError]
    InvalidConfigurationException: Type[BotocoreClientError]
    InvalidLambdaFunctionOutputException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LambdaThrottledException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]

class CognitoSyncClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CognitoSyncClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#close)
        """

    def bulk_publish(
        self, **kwargs: Unpack[BulkPublishRequestRequestTypeDef]
    ) -> BulkPublishResponseTypeDef:
        """
        Initiates a bulk publish of all existing datasets for an Identity Pool to the
        configured stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/bulk_publish.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#bulk_publish)
        """

    def delete_dataset(
        self, **kwargs: Unpack[DeleteDatasetRequestRequestTypeDef]
    ) -> DeleteDatasetResponseTypeDef:
        """
        Deletes the specific dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/delete_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#delete_dataset)
        """

    def describe_dataset(
        self, **kwargs: Unpack[DescribeDatasetRequestRequestTypeDef]
    ) -> DescribeDatasetResponseTypeDef:
        """
        Gets meta data about a dataset by identity and dataset name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/describe_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#describe_dataset)
        """

    def describe_identity_pool_usage(
        self, **kwargs: Unpack[DescribeIdentityPoolUsageRequestRequestTypeDef]
    ) -> DescribeIdentityPoolUsageResponseTypeDef:
        """
        Gets usage details (for example, data storage) about a particular identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/describe_identity_pool_usage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#describe_identity_pool_usage)
        """

    def describe_identity_usage(
        self, **kwargs: Unpack[DescribeIdentityUsageRequestRequestTypeDef]
    ) -> DescribeIdentityUsageResponseTypeDef:
        """
        Gets usage information for an identity, including number of datasets and data
        usage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/describe_identity_usage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#describe_identity_usage)
        """

    def get_bulk_publish_details(
        self, **kwargs: Unpack[GetBulkPublishDetailsRequestRequestTypeDef]
    ) -> GetBulkPublishDetailsResponseTypeDef:
        """
        Get the status of the last BulkPublish operation for an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/get_bulk_publish_details.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#get_bulk_publish_details)
        """

    def get_cognito_events(
        self, **kwargs: Unpack[GetCognitoEventsRequestRequestTypeDef]
    ) -> GetCognitoEventsResponseTypeDef:
        """
        Gets the events and the corresponding Lambda functions associated with an
        identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/get_cognito_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#get_cognito_events)
        """

    def get_identity_pool_configuration(
        self, **kwargs: Unpack[GetIdentityPoolConfigurationRequestRequestTypeDef]
    ) -> GetIdentityPoolConfigurationResponseTypeDef:
        """
        Gets the configuration settings of an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/get_identity_pool_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#get_identity_pool_configuration)
        """

    def list_datasets(
        self, **kwargs: Unpack[ListDatasetsRequestRequestTypeDef]
    ) -> ListDatasetsResponseTypeDef:
        """
        Lists datasets for an identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/list_datasets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#list_datasets)
        """

    def list_identity_pool_usage(
        self, **kwargs: Unpack[ListIdentityPoolUsageRequestRequestTypeDef]
    ) -> ListIdentityPoolUsageResponseTypeDef:
        """
        Gets a list of identity pools registered with Cognito.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/list_identity_pool_usage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#list_identity_pool_usage)
        """

    def list_records(
        self, **kwargs: Unpack[ListRecordsRequestRequestTypeDef]
    ) -> ListRecordsResponseTypeDef:
        """
        Gets paginated records, optionally changed after a particular sync count for a
        dataset and identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/list_records.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#list_records)
        """

    def register_device(
        self, **kwargs: Unpack[RegisterDeviceRequestRequestTypeDef]
    ) -> RegisterDeviceResponseTypeDef:
        """
        Registers a device to receive push sync notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/register_device.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#register_device)
        """

    def set_cognito_events(
        self, **kwargs: Unpack[SetCognitoEventsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the AWS Lambda function for a given event type for an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/set_cognito_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#set_cognito_events)
        """

    def set_identity_pool_configuration(
        self, **kwargs: Unpack[SetIdentityPoolConfigurationRequestRequestTypeDef]
    ) -> SetIdentityPoolConfigurationResponseTypeDef:
        """
        Sets the necessary configuration for push sync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/set_identity_pool_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#set_identity_pool_configuration)
        """

    def subscribe_to_dataset(
        self, **kwargs: Unpack[SubscribeToDatasetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Subscribes to receive notifications when a dataset is modified by another
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/subscribe_to_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#subscribe_to_dataset)
        """

    def unsubscribe_from_dataset(
        self, **kwargs: Unpack[UnsubscribeFromDatasetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Unsubscribes from receiving notifications when a dataset is modified by another
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/unsubscribe_from_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#unsubscribe_from_dataset)
        """

    def update_records(
        self, **kwargs: Unpack[UpdateRecordsRequestRequestTypeDef]
    ) -> UpdateRecordsResponseTypeDef:
        """
        Posts updates to records and adds and deletes records for a dataset and user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync/client/update_records.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cognito_sync/client/#update_records)
        """
