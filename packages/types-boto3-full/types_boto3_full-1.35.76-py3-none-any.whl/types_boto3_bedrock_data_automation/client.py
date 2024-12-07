"""
Type annotations for bedrock-data-automation service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_bedrock_data_automation.client import DataAutomationforBedrockClient

    session = Session()
    client: DataAutomationforBedrockClient = session.client("bedrock-data-automation")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListBlueprintsPaginator, ListDataAutomationProjectsPaginator
from .type_defs import (
    CreateBlueprintRequestRequestTypeDef,
    CreateBlueprintResponseTypeDef,
    CreateBlueprintVersionRequestRequestTypeDef,
    CreateBlueprintVersionResponseTypeDef,
    CreateDataAutomationProjectRequestRequestTypeDef,
    CreateDataAutomationProjectResponseTypeDef,
    DeleteBlueprintRequestRequestTypeDef,
    DeleteDataAutomationProjectRequestRequestTypeDef,
    DeleteDataAutomationProjectResponseTypeDef,
    GetBlueprintRequestRequestTypeDef,
    GetBlueprintResponseTypeDef,
    GetDataAutomationProjectRequestRequestTypeDef,
    GetDataAutomationProjectResponseTypeDef,
    ListBlueprintsRequestRequestTypeDef,
    ListBlueprintsResponseTypeDef,
    ListDataAutomationProjectsRequestRequestTypeDef,
    ListDataAutomationProjectsResponseTypeDef,
    UpdateBlueprintRequestRequestTypeDef,
    UpdateBlueprintResponseTypeDef,
    UpdateDataAutomationProjectRequestRequestTypeDef,
    UpdateDataAutomationProjectResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("DataAutomationforBedrockClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class DataAutomationforBedrockClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation.html#DataAutomationforBedrock.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DataAutomationforBedrockClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation.html#DataAutomationforBedrock.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#close)
        """

    def create_blueprint(
        self, **kwargs: Unpack[CreateBlueprintRequestRequestTypeDef]
    ) -> CreateBlueprintResponseTypeDef:
        """
        Creates an Amazon Bedrock Keystone Blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/create_blueprint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#create_blueprint)
        """

    def create_blueprint_version(
        self, **kwargs: Unpack[CreateBlueprintVersionRequestRequestTypeDef]
    ) -> CreateBlueprintVersionResponseTypeDef:
        """
        Creates a new version of an existing Amazon Bedrock Keystone Blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/create_blueprint_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#create_blueprint_version)
        """

    def create_data_automation_project(
        self, **kwargs: Unpack[CreateDataAutomationProjectRequestRequestTypeDef]
    ) -> CreateDataAutomationProjectResponseTypeDef:
        """
        Creates an Amazon Bedrock Keystone DataAutomationProject.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/create_data_automation_project.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#create_data_automation_project)
        """

    def delete_blueprint(
        self, **kwargs: Unpack[DeleteBlueprintRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an existing Amazon Bedrock Keystone Blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/delete_blueprint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#delete_blueprint)
        """

    def delete_data_automation_project(
        self, **kwargs: Unpack[DeleteDataAutomationProjectRequestRequestTypeDef]
    ) -> DeleteDataAutomationProjectResponseTypeDef:
        """
        Deletes an existing Amazon Bedrock Keystone DataAutomationProject.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/delete_data_automation_project.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#delete_data_automation_project)
        """

    def get_blueprint(
        self, **kwargs: Unpack[GetBlueprintRequestRequestTypeDef]
    ) -> GetBlueprintResponseTypeDef:
        """
        Gets an existing Amazon Bedrock Keystone Blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/get_blueprint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#get_blueprint)
        """

    def get_data_automation_project(
        self, **kwargs: Unpack[GetDataAutomationProjectRequestRequestTypeDef]
    ) -> GetDataAutomationProjectResponseTypeDef:
        """
        Gets an existing Amazon Bedrock Keystone DataAutomationProject.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/get_data_automation_project.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#get_data_automation_project)
        """

    def list_blueprints(
        self, **kwargs: Unpack[ListBlueprintsRequestRequestTypeDef]
    ) -> ListBlueprintsResponseTypeDef:
        """
        Lists all existing Amazon Bedrock Keystone Blueprints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/list_blueprints.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#list_blueprints)
        """

    def list_data_automation_projects(
        self, **kwargs: Unpack[ListDataAutomationProjectsRequestRequestTypeDef]
    ) -> ListDataAutomationProjectsResponseTypeDef:
        """
        Lists all existing Amazon Bedrock Keystone DataAutomationProjects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/list_data_automation_projects.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#list_data_automation_projects)
        """

    def update_blueprint(
        self, **kwargs: Unpack[UpdateBlueprintRequestRequestTypeDef]
    ) -> UpdateBlueprintResponseTypeDef:
        """
        Updates an existing Amazon Bedrock Blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/update_blueprint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#update_blueprint)
        """

    def update_data_automation_project(
        self, **kwargs: Unpack[UpdateDataAutomationProjectRequestRequestTypeDef]
    ) -> UpdateDataAutomationProjectResponseTypeDef:
        """
        Updates an existing Amazon Bedrock DataAutomationProject.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/update_data_automation_project.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#update_data_automation_project)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_blueprints"]) -> ListBlueprintsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_automation_projects"]
    ) -> ListDataAutomationProjectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_data_automation/client/#get_paginator)
        """
