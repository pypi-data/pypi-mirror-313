"""
Type annotations for connectcases service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_connectcases.client import ConnectCasesClient

    session = Session()
    client: ConnectCasesClient = session.client("connectcases")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import SearchCasesPaginator, SearchRelatedItemsPaginator
from .type_defs import (
    BatchGetFieldRequestRequestTypeDef,
    BatchGetFieldResponseTypeDef,
    BatchPutFieldOptionsRequestRequestTypeDef,
    BatchPutFieldOptionsResponseTypeDef,
    CreateCaseRequestRequestTypeDef,
    CreateCaseResponseTypeDef,
    CreateDomainRequestRequestTypeDef,
    CreateDomainResponseTypeDef,
    CreateFieldRequestRequestTypeDef,
    CreateFieldResponseTypeDef,
    CreateLayoutRequestRequestTypeDef,
    CreateLayoutResponseTypeDef,
    CreateRelatedItemRequestRequestTypeDef,
    CreateRelatedItemResponseTypeDef,
    CreateTemplateRequestRequestTypeDef,
    CreateTemplateResponseTypeDef,
    DeleteDomainRequestRequestTypeDef,
    DeleteFieldRequestRequestTypeDef,
    DeleteLayoutRequestRequestTypeDef,
    DeleteTemplateRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCaseAuditEventsRequestRequestTypeDef,
    GetCaseAuditEventsResponseTypeDef,
    GetCaseEventConfigurationRequestRequestTypeDef,
    GetCaseEventConfigurationResponseTypeDef,
    GetCaseRequestRequestTypeDef,
    GetCaseResponseTypeDef,
    GetDomainRequestRequestTypeDef,
    GetDomainResponseTypeDef,
    GetLayoutRequestRequestTypeDef,
    GetLayoutResponseTypeDef,
    GetTemplateRequestRequestTypeDef,
    GetTemplateResponseTypeDef,
    ListCasesForContactRequestRequestTypeDef,
    ListCasesForContactResponseTypeDef,
    ListDomainsRequestRequestTypeDef,
    ListDomainsResponseTypeDef,
    ListFieldOptionsRequestRequestTypeDef,
    ListFieldOptionsResponseTypeDef,
    ListFieldsRequestRequestTypeDef,
    ListFieldsResponseTypeDef,
    ListLayoutsRequestRequestTypeDef,
    ListLayoutsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTemplatesRequestRequestTypeDef,
    ListTemplatesResponseTypeDef,
    PutCaseEventConfigurationRequestRequestTypeDef,
    SearchCasesRequestRequestTypeDef,
    SearchCasesResponseTypeDef,
    SearchRelatedItemsRequestRequestTypeDef,
    SearchRelatedItemsResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateCaseRequestRequestTypeDef,
    UpdateFieldRequestRequestTypeDef,
    UpdateLayoutRequestRequestTypeDef,
    UpdateTemplateRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ConnectCasesClient",)

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

class ConnectCasesClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases.html#ConnectCases.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ConnectCasesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases.html#ConnectCases.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#close)
        """

    def batch_get_field(
        self, **kwargs: Unpack[BatchGetFieldRequestRequestTypeDef]
    ) -> BatchGetFieldResponseTypeDef:
        """
        Returns the description for the list of fields in the request parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/batch_get_field.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#batch_get_field)
        """

    def batch_put_field_options(
        self, **kwargs: Unpack[BatchPutFieldOptionsRequestRequestTypeDef]
    ) -> BatchPutFieldOptionsResponseTypeDef:
        """
        Creates and updates a set of field options for a single select field in a Cases
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/batch_put_field_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#batch_put_field_options)
        """

    def create_case(
        self, **kwargs: Unpack[CreateCaseRequestRequestTypeDef]
    ) -> CreateCaseResponseTypeDef:
        """
        If you provide a value for <code>PerformedBy.UserArn</code> you must also have
        <a
        href="https://docs.aws.amazon.com/connect/latest/APIReference/API_DescribeUser.html">connect:DescribeUser</a>
        permission on the User ARN resource that you provide.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/create_case.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#create_case)
        """

    def create_domain(
        self, **kwargs: Unpack[CreateDomainRequestRequestTypeDef]
    ) -> CreateDomainResponseTypeDef:
        """
        Creates a domain, which is a container for all case data, such as cases,
        fields, templates and layouts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/create_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#create_domain)
        """

    def create_field(
        self, **kwargs: Unpack[CreateFieldRequestRequestTypeDef]
    ) -> CreateFieldResponseTypeDef:
        """
        Creates a field in the Cases domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/create_field.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#create_field)
        """

    def create_layout(
        self, **kwargs: Unpack[CreateLayoutRequestRequestTypeDef]
    ) -> CreateLayoutResponseTypeDef:
        """
        Creates a layout in the Cases domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/create_layout.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#create_layout)
        """

    def create_related_item(
        self, **kwargs: Unpack[CreateRelatedItemRequestRequestTypeDef]
    ) -> CreateRelatedItemResponseTypeDef:
        """
        Creates a related item (comments, tasks, and contacts) and associates it with a
        case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/create_related_item.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#create_related_item)
        """

    def create_template(
        self, **kwargs: Unpack[CreateTemplateRequestRequestTypeDef]
    ) -> CreateTemplateResponseTypeDef:
        """
        Creates a template in the Cases domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/create_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#create_template)
        """

    def delete_domain(self, **kwargs: Unpack[DeleteDomainRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a Cases domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/delete_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#delete_domain)
        """

    def delete_field(self, **kwargs: Unpack[DeleteFieldRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a field from a cases template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/delete_field.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#delete_field)
        """

    def delete_layout(self, **kwargs: Unpack[DeleteLayoutRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a layout from a cases template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/delete_layout.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#delete_layout)
        """

    def delete_template(
        self, **kwargs: Unpack[DeleteTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a cases template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/delete_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#delete_template)
        """

    def get_case(self, **kwargs: Unpack[GetCaseRequestRequestTypeDef]) -> GetCaseResponseTypeDef:
        """
        Returns information about a specific case if it exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/get_case.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#get_case)
        """

    def get_case_audit_events(
        self, **kwargs: Unpack[GetCaseAuditEventsRequestRequestTypeDef]
    ) -> GetCaseAuditEventsResponseTypeDef:
        """
        Returns the audit history about a specific case if it exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/get_case_audit_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#get_case_audit_events)
        """

    def get_case_event_configuration(
        self, **kwargs: Unpack[GetCaseEventConfigurationRequestRequestTypeDef]
    ) -> GetCaseEventConfigurationResponseTypeDef:
        """
        Returns the case event publishing configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/get_case_event_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#get_case_event_configuration)
        """

    def get_domain(
        self, **kwargs: Unpack[GetDomainRequestRequestTypeDef]
    ) -> GetDomainResponseTypeDef:
        """
        Returns information about a specific domain if it exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/get_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#get_domain)
        """

    def get_layout(
        self, **kwargs: Unpack[GetLayoutRequestRequestTypeDef]
    ) -> GetLayoutResponseTypeDef:
        """
        Returns the details for the requested layout.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/get_layout.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#get_layout)
        """

    def get_template(
        self, **kwargs: Unpack[GetTemplateRequestRequestTypeDef]
    ) -> GetTemplateResponseTypeDef:
        """
        Returns the details for the requested template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/get_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#get_template)
        """

    def list_cases_for_contact(
        self, **kwargs: Unpack[ListCasesForContactRequestRequestTypeDef]
    ) -> ListCasesForContactResponseTypeDef:
        """
        Lists cases for a given contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/list_cases_for_contact.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#list_cases_for_contact)
        """

    def list_domains(
        self, **kwargs: Unpack[ListDomainsRequestRequestTypeDef]
    ) -> ListDomainsResponseTypeDef:
        """
        Lists all cases domains in the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/list_domains.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#list_domains)
        """

    def list_field_options(
        self, **kwargs: Unpack[ListFieldOptionsRequestRequestTypeDef]
    ) -> ListFieldOptionsResponseTypeDef:
        """
        Lists all of the field options for a field identifier in the domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/list_field_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#list_field_options)
        """

    def list_fields(
        self, **kwargs: Unpack[ListFieldsRequestRequestTypeDef]
    ) -> ListFieldsResponseTypeDef:
        """
        Lists all fields in a Cases domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/list_fields.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#list_fields)
        """

    def list_layouts(
        self, **kwargs: Unpack[ListLayoutsRequestRequestTypeDef]
    ) -> ListLayoutsResponseTypeDef:
        """
        Lists all layouts in the given cases domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/list_layouts.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#list_layouts)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#list_tags_for_resource)
        """

    def list_templates(
        self, **kwargs: Unpack[ListTemplatesRequestRequestTypeDef]
    ) -> ListTemplatesResponseTypeDef:
        """
        Lists all of the templates in a Cases domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/list_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#list_templates)
        """

    def put_case_event_configuration(
        self, **kwargs: Unpack[PutCaseEventConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds case event publishing configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/put_case_event_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#put_case_event_configuration)
        """

    def search_cases(
        self, **kwargs: Unpack[SearchCasesRequestRequestTypeDef]
    ) -> SearchCasesResponseTypeDef:
        """
        Searches for cases within their associated Cases domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/search_cases.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#search_cases)
        """

    def search_related_items(
        self, **kwargs: Unpack[SearchRelatedItemsRequestRequestTypeDef]
    ) -> SearchRelatedItemsResponseTypeDef:
        """
        Searches for related items that are associated with a case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/search_related_items.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#search_related_items)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Untags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#untag_resource)
        """

    def update_case(self, **kwargs: Unpack[UpdateCaseRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        If you provide a value for <code>PerformedBy.UserArn</code> you must also have
        <a
        href="https://docs.aws.amazon.com/connect/latest/APIReference/API_DescribeUser.html">connect:DescribeUser</a>
        permission on the User ARN resource that you provide.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/update_case.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#update_case)
        """

    def update_field(self, **kwargs: Unpack[UpdateFieldRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates the properties of an existing field.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/update_field.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#update_field)
        """

    def update_layout(self, **kwargs: Unpack[UpdateLayoutRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates the attributes of an existing layout.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/update_layout.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#update_layout)
        """

    def update_template(
        self, **kwargs: Unpack[UpdateTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the attributes of an existing template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/update_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#update_template)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_cases"]) -> SearchCasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_related_items"]
    ) -> SearchRelatedItemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/client/#get_paginator)
        """
