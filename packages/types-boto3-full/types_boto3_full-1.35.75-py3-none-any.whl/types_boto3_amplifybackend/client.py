"""
Type annotations for amplifybackend service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_amplifybackend.client import AmplifyBackendClient

    session = Session()
    client: AmplifyBackendClient = session.client("amplifybackend")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListBackendJobsPaginator
from .type_defs import (
    CloneBackendRequestRequestTypeDef,
    CloneBackendResponseTypeDef,
    CreateBackendAPIRequestRequestTypeDef,
    CreateBackendAPIResponseTypeDef,
    CreateBackendAuthRequestRequestTypeDef,
    CreateBackendAuthResponseTypeDef,
    CreateBackendConfigRequestRequestTypeDef,
    CreateBackendConfigResponseTypeDef,
    CreateBackendRequestRequestTypeDef,
    CreateBackendResponseTypeDef,
    CreateBackendStorageRequestRequestTypeDef,
    CreateBackendStorageResponseTypeDef,
    CreateTokenRequestRequestTypeDef,
    CreateTokenResponseTypeDef,
    DeleteBackendAPIRequestRequestTypeDef,
    DeleteBackendAPIResponseTypeDef,
    DeleteBackendAuthRequestRequestTypeDef,
    DeleteBackendAuthResponseTypeDef,
    DeleteBackendRequestRequestTypeDef,
    DeleteBackendResponseTypeDef,
    DeleteBackendStorageRequestRequestTypeDef,
    DeleteBackendStorageResponseTypeDef,
    DeleteTokenRequestRequestTypeDef,
    DeleteTokenResponseTypeDef,
    GenerateBackendAPIModelsRequestRequestTypeDef,
    GenerateBackendAPIModelsResponseTypeDef,
    GetBackendAPIModelsRequestRequestTypeDef,
    GetBackendAPIModelsResponseTypeDef,
    GetBackendAPIRequestRequestTypeDef,
    GetBackendAPIResponseTypeDef,
    GetBackendAuthRequestRequestTypeDef,
    GetBackendAuthResponseTypeDef,
    GetBackendJobRequestRequestTypeDef,
    GetBackendJobResponseTypeDef,
    GetBackendRequestRequestTypeDef,
    GetBackendResponseTypeDef,
    GetBackendStorageRequestRequestTypeDef,
    GetBackendStorageResponseTypeDef,
    GetTokenRequestRequestTypeDef,
    GetTokenResponseTypeDef,
    ImportBackendAuthRequestRequestTypeDef,
    ImportBackendAuthResponseTypeDef,
    ImportBackendStorageRequestRequestTypeDef,
    ImportBackendStorageResponseTypeDef,
    ListBackendJobsRequestRequestTypeDef,
    ListBackendJobsResponseTypeDef,
    ListS3BucketsRequestRequestTypeDef,
    ListS3BucketsResponseTypeDef,
    RemoveAllBackendsRequestRequestTypeDef,
    RemoveAllBackendsResponseTypeDef,
    RemoveBackendConfigRequestRequestTypeDef,
    RemoveBackendConfigResponseTypeDef,
    UpdateBackendAPIRequestRequestTypeDef,
    UpdateBackendAPIResponseTypeDef,
    UpdateBackendAuthRequestRequestTypeDef,
    UpdateBackendAuthResponseTypeDef,
    UpdateBackendConfigRequestRequestTypeDef,
    UpdateBackendConfigResponseTypeDef,
    UpdateBackendJobRequestRequestTypeDef,
    UpdateBackendJobResponseTypeDef,
    UpdateBackendStorageRequestRequestTypeDef,
    UpdateBackendStorageResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("AmplifyBackendClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    GatewayTimeoutException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class AmplifyBackendClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AmplifyBackendClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#close)
        """

    def clone_backend(
        self, **kwargs: Unpack[CloneBackendRequestRequestTypeDef]
    ) -> CloneBackendResponseTypeDef:
        """
        This operation clones an existing backend.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/clone_backend.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#clone_backend)
        """

    def create_backend(
        self, **kwargs: Unpack[CreateBackendRequestRequestTypeDef]
    ) -> CreateBackendResponseTypeDef:
        """
        This operation creates a backend for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/create_backend.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#create_backend)
        """

    def create_backend_api(
        self, **kwargs: Unpack[CreateBackendAPIRequestRequestTypeDef]
    ) -> CreateBackendAPIResponseTypeDef:
        """
        Creates a new backend API resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/create_backend_api.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#create_backend_api)
        """

    def create_backend_auth(
        self, **kwargs: Unpack[CreateBackendAuthRequestRequestTypeDef]
    ) -> CreateBackendAuthResponseTypeDef:
        """
        Creates a new backend authentication resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/create_backend_auth.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#create_backend_auth)
        """

    def create_backend_config(
        self, **kwargs: Unpack[CreateBackendConfigRequestRequestTypeDef]
    ) -> CreateBackendConfigResponseTypeDef:
        """
        Creates a config object for a backend.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/create_backend_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#create_backend_config)
        """

    def create_backend_storage(
        self, **kwargs: Unpack[CreateBackendStorageRequestRequestTypeDef]
    ) -> CreateBackendStorageResponseTypeDef:
        """
        Creates a backend storage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/create_backend_storage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#create_backend_storage)
        """

    def create_token(
        self, **kwargs: Unpack[CreateTokenRequestRequestTypeDef]
    ) -> CreateTokenResponseTypeDef:
        """
        Generates a one-time challenge code to authenticate a user into your Amplify
        Admin UI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/create_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#create_token)
        """

    def delete_backend(
        self, **kwargs: Unpack[DeleteBackendRequestRequestTypeDef]
    ) -> DeleteBackendResponseTypeDef:
        """
        Removes an existing environment from your Amplify project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/delete_backend.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#delete_backend)
        """

    def delete_backend_api(
        self, **kwargs: Unpack[DeleteBackendAPIRequestRequestTypeDef]
    ) -> DeleteBackendAPIResponseTypeDef:
        """
        Deletes an existing backend API resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/delete_backend_api.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#delete_backend_api)
        """

    def delete_backend_auth(
        self, **kwargs: Unpack[DeleteBackendAuthRequestRequestTypeDef]
    ) -> DeleteBackendAuthResponseTypeDef:
        """
        Deletes an existing backend authentication resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/delete_backend_auth.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#delete_backend_auth)
        """

    def delete_backend_storage(
        self, **kwargs: Unpack[DeleteBackendStorageRequestRequestTypeDef]
    ) -> DeleteBackendStorageResponseTypeDef:
        """
        Removes the specified backend storage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/delete_backend_storage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#delete_backend_storage)
        """

    def delete_token(
        self, **kwargs: Unpack[DeleteTokenRequestRequestTypeDef]
    ) -> DeleteTokenResponseTypeDef:
        """
        Deletes the challenge token based on the given appId and sessionId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/delete_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#delete_token)
        """

    def generate_backend_api_models(
        self, **kwargs: Unpack[GenerateBackendAPIModelsRequestRequestTypeDef]
    ) -> GenerateBackendAPIModelsResponseTypeDef:
        """
        Generates a model schema for an existing backend API resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/generate_backend_api_models.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#generate_backend_api_models)
        """

    def get_backend(
        self, **kwargs: Unpack[GetBackendRequestRequestTypeDef]
    ) -> GetBackendResponseTypeDef:
        """
        Provides project-level details for your Amplify UI project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/get_backend.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#get_backend)
        """

    def get_backend_api(
        self, **kwargs: Unpack[GetBackendAPIRequestRequestTypeDef]
    ) -> GetBackendAPIResponseTypeDef:
        """
        Gets the details for a backend API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/get_backend_api.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#get_backend_api)
        """

    def get_backend_api_models(
        self, **kwargs: Unpack[GetBackendAPIModelsRequestRequestTypeDef]
    ) -> GetBackendAPIModelsResponseTypeDef:
        """
        Gets a model introspection schema for an existing backend API resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/get_backend_api_models.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#get_backend_api_models)
        """

    def get_backend_auth(
        self, **kwargs: Unpack[GetBackendAuthRequestRequestTypeDef]
    ) -> GetBackendAuthResponseTypeDef:
        """
        Gets a backend auth details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/get_backend_auth.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#get_backend_auth)
        """

    def get_backend_job(
        self, **kwargs: Unpack[GetBackendJobRequestRequestTypeDef]
    ) -> GetBackendJobResponseTypeDef:
        """
        Returns information about a specific job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/get_backend_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#get_backend_job)
        """

    def get_backend_storage(
        self, **kwargs: Unpack[GetBackendStorageRequestRequestTypeDef]
    ) -> GetBackendStorageResponseTypeDef:
        """
        Gets details for a backend storage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/get_backend_storage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#get_backend_storage)
        """

    def get_token(self, **kwargs: Unpack[GetTokenRequestRequestTypeDef]) -> GetTokenResponseTypeDef:
        """
        Gets the challenge token based on the given appId and sessionId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/get_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#get_token)
        """

    def import_backend_auth(
        self, **kwargs: Unpack[ImportBackendAuthRequestRequestTypeDef]
    ) -> ImportBackendAuthResponseTypeDef:
        """
        Imports an existing backend authentication resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/import_backend_auth.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#import_backend_auth)
        """

    def import_backend_storage(
        self, **kwargs: Unpack[ImportBackendStorageRequestRequestTypeDef]
    ) -> ImportBackendStorageResponseTypeDef:
        """
        Imports an existing backend storage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/import_backend_storage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#import_backend_storage)
        """

    def list_backend_jobs(
        self, **kwargs: Unpack[ListBackendJobsRequestRequestTypeDef]
    ) -> ListBackendJobsResponseTypeDef:
        """
        Lists the jobs for the backend of an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/list_backend_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#list_backend_jobs)
        """

    def list_s3_buckets(
        self, **kwargs: Unpack[ListS3BucketsRequestRequestTypeDef]
    ) -> ListS3BucketsResponseTypeDef:
        """
        The list of S3 buckets in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/list_s3_buckets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#list_s3_buckets)
        """

    def remove_all_backends(
        self, **kwargs: Unpack[RemoveAllBackendsRequestRequestTypeDef]
    ) -> RemoveAllBackendsResponseTypeDef:
        """
        Removes all backend environments from your Amplify project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/remove_all_backends.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#remove_all_backends)
        """

    def remove_backend_config(
        self, **kwargs: Unpack[RemoveBackendConfigRequestRequestTypeDef]
    ) -> RemoveBackendConfigResponseTypeDef:
        """
        Removes the AWS resources required to access the Amplify Admin UI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/remove_backend_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#remove_backend_config)
        """

    def update_backend_api(
        self, **kwargs: Unpack[UpdateBackendAPIRequestRequestTypeDef]
    ) -> UpdateBackendAPIResponseTypeDef:
        """
        Updates an existing backend API resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/update_backend_api.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#update_backend_api)
        """

    def update_backend_auth(
        self, **kwargs: Unpack[UpdateBackendAuthRequestRequestTypeDef]
    ) -> UpdateBackendAuthResponseTypeDef:
        """
        Updates an existing backend authentication resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/update_backend_auth.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#update_backend_auth)
        """

    def update_backend_config(
        self, **kwargs: Unpack[UpdateBackendConfigRequestRequestTypeDef]
    ) -> UpdateBackendConfigResponseTypeDef:
        """
        Updates the AWS resources required to access the Amplify Admin UI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/update_backend_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#update_backend_config)
        """

    def update_backend_job(
        self, **kwargs: Unpack[UpdateBackendJobRequestRequestTypeDef]
    ) -> UpdateBackendJobResponseTypeDef:
        """
        Updates a specific job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/update_backend_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#update_backend_job)
        """

    def update_backend_storage(
        self, **kwargs: Unpack[UpdateBackendStorageRequestRequestTypeDef]
    ) -> UpdateBackendStorageResponseTypeDef:
        """
        Updates an existing backend storage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/update_backend_storage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#update_backend_storage)
        """

    def get_paginator(
        self, operation_name: Literal["list_backend_jobs"]
    ) -> ListBackendJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifybackend/client/#get_paginator)
        """
