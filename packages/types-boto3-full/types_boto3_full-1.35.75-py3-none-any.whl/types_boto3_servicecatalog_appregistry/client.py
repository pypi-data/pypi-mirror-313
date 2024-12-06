"""
Type annotations for servicecatalog-appregistry service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_servicecatalog_appregistry.client import AppRegistryClient

    session = Session()
    client: AppRegistryClient = session.client("servicecatalog-appregistry")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListApplicationsPaginator,
    ListAssociatedAttributeGroupsPaginator,
    ListAssociatedResourcesPaginator,
    ListAttributeGroupsForApplicationPaginator,
    ListAttributeGroupsPaginator,
)
from .type_defs import (
    AssociateAttributeGroupRequestRequestTypeDef,
    AssociateAttributeGroupResponseTypeDef,
    AssociateResourceRequestRequestTypeDef,
    AssociateResourceResponseTypeDef,
    CreateApplicationRequestRequestTypeDef,
    CreateApplicationResponseTypeDef,
    CreateAttributeGroupRequestRequestTypeDef,
    CreateAttributeGroupResponseTypeDef,
    DeleteApplicationRequestRequestTypeDef,
    DeleteApplicationResponseTypeDef,
    DeleteAttributeGroupRequestRequestTypeDef,
    DeleteAttributeGroupResponseTypeDef,
    DisassociateAttributeGroupRequestRequestTypeDef,
    DisassociateAttributeGroupResponseTypeDef,
    DisassociateResourceRequestRequestTypeDef,
    DisassociateResourceResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetApplicationRequestRequestTypeDef,
    GetApplicationResponseTypeDef,
    GetAssociatedResourceRequestRequestTypeDef,
    GetAssociatedResourceResponseTypeDef,
    GetAttributeGroupRequestRequestTypeDef,
    GetAttributeGroupResponseTypeDef,
    GetConfigurationResponseTypeDef,
    ListApplicationsRequestRequestTypeDef,
    ListApplicationsResponseTypeDef,
    ListAssociatedAttributeGroupsRequestRequestTypeDef,
    ListAssociatedAttributeGroupsResponseTypeDef,
    ListAssociatedResourcesRequestRequestTypeDef,
    ListAssociatedResourcesResponseTypeDef,
    ListAttributeGroupsForApplicationRequestRequestTypeDef,
    ListAttributeGroupsForApplicationResponseTypeDef,
    ListAttributeGroupsRequestRequestTypeDef,
    ListAttributeGroupsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutConfigurationRequestRequestTypeDef,
    SyncResourceRequestRequestTypeDef,
    SyncResourceResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateApplicationRequestRequestTypeDef,
    UpdateApplicationResponseTypeDef,
    UpdateAttributeGroupRequestRequestTypeDef,
    UpdateAttributeGroupResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("AppRegistryClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class AppRegistryClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry.html#AppRegistry.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppRegistryClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry.html#AppRegistry.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#close)
        """

    def associate_attribute_group(
        self, **kwargs: Unpack[AssociateAttributeGroupRequestRequestTypeDef]
    ) -> AssociateAttributeGroupResponseTypeDef:
        """
        Associates an attribute group with an application to augment the application's
        metadata with the group's attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/associate_attribute_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#associate_attribute_group)
        """

    def associate_resource(
        self, **kwargs: Unpack[AssociateResourceRequestRequestTypeDef]
    ) -> AssociateResourceResponseTypeDef:
        """
        Associates a resource with an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/associate_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#associate_resource)
        """

    def create_application(
        self, **kwargs: Unpack[CreateApplicationRequestRequestTypeDef]
    ) -> CreateApplicationResponseTypeDef:
        """
        Creates a new application that is the top-level node in a hierarchy of related
        cloud resource abstractions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/create_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#create_application)
        """

    def create_attribute_group(
        self, **kwargs: Unpack[CreateAttributeGroupRequestRequestTypeDef]
    ) -> CreateAttributeGroupResponseTypeDef:
        """
        Creates a new attribute group as a container for user-defined attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/create_attribute_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#create_attribute_group)
        """

    def delete_application(
        self, **kwargs: Unpack[DeleteApplicationRequestRequestTypeDef]
    ) -> DeleteApplicationResponseTypeDef:
        """
        Deletes an application that is specified either by its application ID, name, or
        ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/delete_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#delete_application)
        """

    def delete_attribute_group(
        self, **kwargs: Unpack[DeleteAttributeGroupRequestRequestTypeDef]
    ) -> DeleteAttributeGroupResponseTypeDef:
        """
        Deletes an attribute group, specified either by its attribute group ID, name,
        or ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/delete_attribute_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#delete_attribute_group)
        """

    def disassociate_attribute_group(
        self, **kwargs: Unpack[DisassociateAttributeGroupRequestRequestTypeDef]
    ) -> DisassociateAttributeGroupResponseTypeDef:
        """
        Disassociates an attribute group from an application to remove the extra
        attributes contained in the attribute group from the application's metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/disassociate_attribute_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#disassociate_attribute_group)
        """

    def disassociate_resource(
        self, **kwargs: Unpack[DisassociateResourceRequestRequestTypeDef]
    ) -> DisassociateResourceResponseTypeDef:
        """
        Disassociates a resource from application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/disassociate_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#disassociate_resource)
        """

    def get_application(
        self, **kwargs: Unpack[GetApplicationRequestRequestTypeDef]
    ) -> GetApplicationResponseTypeDef:
        """
        Retrieves metadata information about one of your applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/get_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#get_application)
        """

    def get_associated_resource(
        self, **kwargs: Unpack[GetAssociatedResourceRequestRequestTypeDef]
    ) -> GetAssociatedResourceResponseTypeDef:
        """
        Gets the resource associated with the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/get_associated_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#get_associated_resource)
        """

    def get_attribute_group(
        self, **kwargs: Unpack[GetAttributeGroupRequestRequestTypeDef]
    ) -> GetAttributeGroupResponseTypeDef:
        """
        Retrieves an attribute group by its ARN, ID, or name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/get_attribute_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#get_attribute_group)
        """

    def get_configuration(self) -> GetConfigurationResponseTypeDef:
        """
        Retrieves a <code>TagKey</code> configuration from an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/get_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#get_configuration)
        """

    def list_applications(
        self, **kwargs: Unpack[ListApplicationsRequestRequestTypeDef]
    ) -> ListApplicationsResponseTypeDef:
        """
        Retrieves a list of all of your applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/list_applications.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#list_applications)
        """

    def list_associated_attribute_groups(
        self, **kwargs: Unpack[ListAssociatedAttributeGroupsRequestRequestTypeDef]
    ) -> ListAssociatedAttributeGroupsResponseTypeDef:
        """
        Lists all attribute groups that are associated with specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/list_associated_attribute_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#list_associated_attribute_groups)
        """

    def list_associated_resources(
        self, **kwargs: Unpack[ListAssociatedResourcesRequestRequestTypeDef]
    ) -> ListAssociatedResourcesResponseTypeDef:
        """
        Lists all of the resources that are associated with the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/list_associated_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#list_associated_resources)
        """

    def list_attribute_groups(
        self, **kwargs: Unpack[ListAttributeGroupsRequestRequestTypeDef]
    ) -> ListAttributeGroupsResponseTypeDef:
        """
        Lists all attribute groups which you have access to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/list_attribute_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#list_attribute_groups)
        """

    def list_attribute_groups_for_application(
        self, **kwargs: Unpack[ListAttributeGroupsForApplicationRequestRequestTypeDef]
    ) -> ListAttributeGroupsForApplicationResponseTypeDef:
        """
        Lists the details of all attribute groups associated with a specific
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/list_attribute_groups_for_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#list_attribute_groups_for_application)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all of the tags on the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#list_tags_for_resource)
        """

    def put_configuration(
        self, **kwargs: Unpack[PutConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates a <code>TagKey</code> configuration to an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/put_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#put_configuration)
        """

    def sync_resource(
        self, **kwargs: Unpack[SyncResourceRequestRequestTypeDef]
    ) -> SyncResourceResponseTypeDef:
        """
        Syncs the resource with current AppRegistry records.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/sync_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#sync_resource)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#untag_resource)
        """

    def update_application(
        self, **kwargs: Unpack[UpdateApplicationRequestRequestTypeDef]
    ) -> UpdateApplicationResponseTypeDef:
        """
        Updates an existing application with new attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/update_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#update_application)
        """

    def update_attribute_group(
        self, **kwargs: Unpack[UpdateAttributeGroupRequestRequestTypeDef]
    ) -> UpdateAttributeGroupResponseTypeDef:
        """
        Updates an existing attribute group with new details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/update_attribute_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#update_attribute_group)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_associated_attribute_groups"]
    ) -> ListAssociatedAttributeGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_associated_resources"]
    ) -> ListAssociatedResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_attribute_groups_for_application"]
    ) -> ListAttributeGroupsForApplicationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_attribute_groups"]
    ) -> ListAttributeGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog-appregistry/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_servicecatalog_appregistry/client/#get_paginator)
        """
