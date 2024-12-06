"""
Type annotations for amplifyuibuilder service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_amplifyuibuilder.client import AmplifyUIBuilderClient

    session = Session()
    client: AmplifyUIBuilderClient = session.client("amplifyuibuilder")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ExportComponentsPaginator,
    ExportFormsPaginator,
    ExportThemesPaginator,
    ListCodegenJobsPaginator,
    ListComponentsPaginator,
    ListFormsPaginator,
    ListThemesPaginator,
)
from .type_defs import (
    CreateComponentRequestRequestTypeDef,
    CreateComponentResponseTypeDef,
    CreateFormRequestRequestTypeDef,
    CreateFormResponseTypeDef,
    CreateThemeRequestRequestTypeDef,
    CreateThemeResponseTypeDef,
    DeleteComponentRequestRequestTypeDef,
    DeleteFormRequestRequestTypeDef,
    DeleteThemeRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    ExchangeCodeForTokenRequestRequestTypeDef,
    ExchangeCodeForTokenResponseTypeDef,
    ExportComponentsRequestRequestTypeDef,
    ExportComponentsResponseTypeDef,
    ExportFormsRequestRequestTypeDef,
    ExportFormsResponseTypeDef,
    ExportThemesRequestRequestTypeDef,
    ExportThemesResponseTypeDef,
    GetCodegenJobRequestRequestTypeDef,
    GetCodegenJobResponseTypeDef,
    GetComponentRequestRequestTypeDef,
    GetComponentResponseTypeDef,
    GetFormRequestRequestTypeDef,
    GetFormResponseTypeDef,
    GetMetadataRequestRequestTypeDef,
    GetMetadataResponseTypeDef,
    GetThemeRequestRequestTypeDef,
    GetThemeResponseTypeDef,
    ListCodegenJobsRequestRequestTypeDef,
    ListCodegenJobsResponseTypeDef,
    ListComponentsRequestRequestTypeDef,
    ListComponentsResponseTypeDef,
    ListFormsRequestRequestTypeDef,
    ListFormsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListThemesRequestRequestTypeDef,
    ListThemesResponseTypeDef,
    PutMetadataFlagRequestRequestTypeDef,
    RefreshTokenRequestRequestTypeDef,
    RefreshTokenResponseTypeDef,
    StartCodegenJobRequestRequestTypeDef,
    StartCodegenJobResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateComponentRequestRequestTypeDef,
    UpdateComponentResponseTypeDef,
    UpdateFormRequestRequestTypeDef,
    UpdateFormResponseTypeDef,
    UpdateThemeRequestRequestTypeDef,
    UpdateThemeResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("AmplifyUIBuilderClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]

class AmplifyUIBuilderClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AmplifyUIBuilderClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder.html#AmplifyUIBuilder.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#close)
        """

    def create_component(
        self, **kwargs: Unpack[CreateComponentRequestRequestTypeDef]
    ) -> CreateComponentResponseTypeDef:
        """
        Creates a new component for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/create_component.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#create_component)
        """

    def create_form(
        self, **kwargs: Unpack[CreateFormRequestRequestTypeDef]
    ) -> CreateFormResponseTypeDef:
        """
        Creates a new form for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/create_form.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#create_form)
        """

    def create_theme(
        self, **kwargs: Unpack[CreateThemeRequestRequestTypeDef]
    ) -> CreateThemeResponseTypeDef:
        """
        Creates a theme to apply to the components in an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/create_theme.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#create_theme)
        """

    def delete_component(
        self, **kwargs: Unpack[DeleteComponentRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a component from an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/delete_component.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#delete_component)
        """

    def delete_form(
        self, **kwargs: Unpack[DeleteFormRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a form from an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/delete_form.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#delete_form)
        """

    def delete_theme(
        self, **kwargs: Unpack[DeleteThemeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a theme from an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/delete_theme.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#delete_theme)
        """

    def exchange_code_for_token(
        self, **kwargs: Unpack[ExchangeCodeForTokenRequestRequestTypeDef]
    ) -> ExchangeCodeForTokenResponseTypeDef:
        """
        This is for internal use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/exchange_code_for_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#exchange_code_for_token)
        """

    def export_components(
        self, **kwargs: Unpack[ExportComponentsRequestRequestTypeDef]
    ) -> ExportComponentsResponseTypeDef:
        """
        Exports component configurations to code that is ready to integrate into an
        Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/export_components.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#export_components)
        """

    def export_forms(
        self, **kwargs: Unpack[ExportFormsRequestRequestTypeDef]
    ) -> ExportFormsResponseTypeDef:
        """
        Exports form configurations to code that is ready to integrate into an Amplify
        app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/export_forms.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#export_forms)
        """

    def export_themes(
        self, **kwargs: Unpack[ExportThemesRequestRequestTypeDef]
    ) -> ExportThemesResponseTypeDef:
        """
        Exports theme configurations to code that is ready to integrate into an Amplify
        app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/export_themes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#export_themes)
        """

    def get_codegen_job(
        self, **kwargs: Unpack[GetCodegenJobRequestRequestTypeDef]
    ) -> GetCodegenJobResponseTypeDef:
        """
        Returns an existing code generation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_codegen_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#get_codegen_job)
        """

    def get_component(
        self, **kwargs: Unpack[GetComponentRequestRequestTypeDef]
    ) -> GetComponentResponseTypeDef:
        """
        Returns an existing component for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_component.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#get_component)
        """

    def get_form(self, **kwargs: Unpack[GetFormRequestRequestTypeDef]) -> GetFormResponseTypeDef:
        """
        Returns an existing form for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_form.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#get_form)
        """

    def get_metadata(
        self, **kwargs: Unpack[GetMetadataRequestRequestTypeDef]
    ) -> GetMetadataResponseTypeDef:
        """
        Returns existing metadata for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#get_metadata)
        """

    def get_theme(self, **kwargs: Unpack[GetThemeRequestRequestTypeDef]) -> GetThemeResponseTypeDef:
        """
        Returns an existing theme for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_theme.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#get_theme)
        """

    def list_codegen_jobs(
        self, **kwargs: Unpack[ListCodegenJobsRequestRequestTypeDef]
    ) -> ListCodegenJobsResponseTypeDef:
        """
        Retrieves a list of code generation jobs for a specified Amplify app and
        backend environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/list_codegen_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#list_codegen_jobs)
        """

    def list_components(
        self, **kwargs: Unpack[ListComponentsRequestRequestTypeDef]
    ) -> ListComponentsResponseTypeDef:
        """
        Retrieves a list of components for a specified Amplify app and backend
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/list_components.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#list_components)
        """

    def list_forms(
        self, **kwargs: Unpack[ListFormsRequestRequestTypeDef]
    ) -> ListFormsResponseTypeDef:
        """
        Retrieves a list of forms for a specified Amplify app and backend environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/list_forms.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#list_forms)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a specified Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#list_tags_for_resource)
        """

    def list_themes(
        self, **kwargs: Unpack[ListThemesRequestRequestTypeDef]
    ) -> ListThemesResponseTypeDef:
        """
        Retrieves a list of themes for a specified Amplify app and backend environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/list_themes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#list_themes)
        """

    def put_metadata_flag(
        self, **kwargs: Unpack[PutMetadataFlagRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stores the metadata information about a feature on a form.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/put_metadata_flag.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#put_metadata_flag)
        """

    def refresh_token(
        self, **kwargs: Unpack[RefreshTokenRequestRequestTypeDef]
    ) -> RefreshTokenResponseTypeDef:
        """
        This is for internal use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/refresh_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#refresh_token)
        """

    def start_codegen_job(
        self, **kwargs: Unpack[StartCodegenJobRequestRequestTypeDef]
    ) -> StartCodegenJobResponseTypeDef:
        """
        Starts a code generation job for a specified Amplify app and backend
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/start_codegen_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#start_codegen_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags the resource with a tag key and value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Untags a resource with a specified Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#untag_resource)
        """

    def update_component(
        self, **kwargs: Unpack[UpdateComponentRequestRequestTypeDef]
    ) -> UpdateComponentResponseTypeDef:
        """
        Updates an existing component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/update_component.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#update_component)
        """

    def update_form(
        self, **kwargs: Unpack[UpdateFormRequestRequestTypeDef]
    ) -> UpdateFormResponseTypeDef:
        """
        Updates an existing form.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/update_form.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#update_form)
        """

    def update_theme(
        self, **kwargs: Unpack[UpdateThemeRequestRequestTypeDef]
    ) -> UpdateThemeResponseTypeDef:
        """
        Updates an existing theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/update_theme.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#update_theme)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["export_components"]
    ) -> ExportComponentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["export_forms"]) -> ExportFormsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["export_themes"]) -> ExportThemesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_codegen_jobs"]
    ) -> ListCodegenJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_components"]) -> ListComponentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_forms"]) -> ListFormsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_themes"]) -> ListThemesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/client/#get_paginator)
        """
