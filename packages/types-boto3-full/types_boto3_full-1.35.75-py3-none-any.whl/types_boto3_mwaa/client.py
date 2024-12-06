"""
Type annotations for mwaa service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_mwaa.client import MWAAClient

    session = Session()
    client: MWAAClient = session.client("mwaa")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListEnvironmentsPaginator
from .type_defs import (
    CreateCliTokenRequestRequestTypeDef,
    CreateCliTokenResponseTypeDef,
    CreateEnvironmentInputRequestTypeDef,
    CreateEnvironmentOutputTypeDef,
    CreateWebLoginTokenRequestRequestTypeDef,
    CreateWebLoginTokenResponseTypeDef,
    DeleteEnvironmentInputRequestTypeDef,
    GetEnvironmentInputRequestTypeDef,
    GetEnvironmentOutputTypeDef,
    InvokeRestApiRequestRequestTypeDef,
    InvokeRestApiResponseTypeDef,
    ListEnvironmentsInputRequestTypeDef,
    ListEnvironmentsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    PublishMetricsInputRequestTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateEnvironmentInputRequestTypeDef,
    UpdateEnvironmentOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("MWAAClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    RestApiClientException: Type[BotocoreClientError]
    RestApiServerException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class MWAAClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MWAAClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#close)
        """

    def create_cli_token(
        self, **kwargs: Unpack[CreateCliTokenRequestRequestTypeDef]
    ) -> CreateCliTokenResponseTypeDef:
        """
        Creates a CLI token for the Airflow CLI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/client/create_cli_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#create_cli_token)
        """

    def create_environment(
        self, **kwargs: Unpack[CreateEnvironmentInputRequestTypeDef]
    ) -> CreateEnvironmentOutputTypeDef:
        """
        Creates an Amazon Managed Workflows for Apache Airflow (Amazon MWAA)
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/client/create_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#create_environment)
        """

    def create_web_login_token(
        self, **kwargs: Unpack[CreateWebLoginTokenRequestRequestTypeDef]
    ) -> CreateWebLoginTokenResponseTypeDef:
        """
        Creates a web login token for the Airflow Web UI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/client/create_web_login_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#create_web_login_token)
        """

    def delete_environment(
        self, **kwargs: Unpack[DeleteEnvironmentInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Amazon Managed Workflows for Apache Airflow (Amazon MWAA)
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/client/delete_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#delete_environment)
        """

    def get_environment(
        self, **kwargs: Unpack[GetEnvironmentInputRequestTypeDef]
    ) -> GetEnvironmentOutputTypeDef:
        """
        Describes an Amazon Managed Workflows for Apache Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/client/get_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#get_environment)
        """

    def invoke_rest_api(
        self, **kwargs: Unpack[InvokeRestApiRequestRequestTypeDef]
    ) -> InvokeRestApiResponseTypeDef:
        """
        Invokes the Apache Airflow REST API on the webserver with the specified inputs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/client/invoke_rest_api.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#invoke_rest_api)
        """

    def list_environments(
        self, **kwargs: Unpack[ListEnvironmentsInputRequestTypeDef]
    ) -> ListEnvironmentsOutputTypeDef:
        """
        Lists the Amazon Managed Workflows for Apache Airflow (MWAA) environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/client/list_environments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#list_environments)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the key-value tag pairs associated to the Amazon Managed Workflows for
        Apache Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#list_tags_for_resource)
        """

    def publish_metrics(
        self, **kwargs: Unpack[PublishMetricsInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        <b>Internal only</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/client/publish_metrics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#publish_metrics)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates key-value tag pairs to your Amazon Managed Workflows for Apache
        Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes key-value tag pairs associated to your Amazon Managed Workflows for
        Apache Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#untag_resource)
        """

    def update_environment(
        self, **kwargs: Unpack[UpdateEnvironmentInputRequestTypeDef]
    ) -> UpdateEnvironmentOutputTypeDef:
        """
        Updates an Amazon Managed Workflows for Apache Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/client/update_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#update_environment)
        """

    def get_paginator(
        self, operation_name: Literal["list_environments"]
    ) -> ListEnvironmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mwaa/client/#get_paginator)
        """
