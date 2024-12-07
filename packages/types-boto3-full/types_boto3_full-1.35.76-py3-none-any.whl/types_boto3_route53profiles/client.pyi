"""
Type annotations for route53profiles service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_route53profiles.client import Route53ProfilesClient

    session = Session()
    client: Route53ProfilesClient = session.client("route53profiles")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListProfileAssociationsPaginator,
    ListProfileResourceAssociationsPaginator,
    ListProfilesPaginator,
)
from .type_defs import (
    AssociateProfileRequestRequestTypeDef,
    AssociateProfileResponseTypeDef,
    AssociateResourceToProfileRequestRequestTypeDef,
    AssociateResourceToProfileResponseTypeDef,
    CreateProfileRequestRequestTypeDef,
    CreateProfileResponseTypeDef,
    DeleteProfileRequestRequestTypeDef,
    DeleteProfileResponseTypeDef,
    DisassociateProfileRequestRequestTypeDef,
    DisassociateProfileResponseTypeDef,
    DisassociateResourceFromProfileRequestRequestTypeDef,
    DisassociateResourceFromProfileResponseTypeDef,
    GetProfileAssociationRequestRequestTypeDef,
    GetProfileAssociationResponseTypeDef,
    GetProfileRequestRequestTypeDef,
    GetProfileResourceAssociationRequestRequestTypeDef,
    GetProfileResourceAssociationResponseTypeDef,
    GetProfileResponseTypeDef,
    ListProfileAssociationsRequestRequestTypeDef,
    ListProfileAssociationsResponseTypeDef,
    ListProfileResourceAssociationsRequestRequestTypeDef,
    ListProfileResourceAssociationsResponseTypeDef,
    ListProfilesRequestRequestTypeDef,
    ListProfilesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateProfileResourceAssociationRequestRequestTypeDef,
    UpdateProfileResourceAssociationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("Route53ProfilesClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class Route53ProfilesClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Route53ProfilesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#close)
        """

    def associate_profile(
        self, **kwargs: Unpack[AssociateProfileRequestRequestTypeDef]
    ) -> AssociateProfileResponseTypeDef:
        """
        Associates a Route 53 Profiles profile with a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/associate_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#associate_profile)
        """

    def associate_resource_to_profile(
        self, **kwargs: Unpack[AssociateResourceToProfileRequestRequestTypeDef]
    ) -> AssociateResourceToProfileResponseTypeDef:
        """
        Associates a DNS reource configuration to a Route 53 Profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/associate_resource_to_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#associate_resource_to_profile)
        """

    def create_profile(
        self, **kwargs: Unpack[CreateProfileRequestRequestTypeDef]
    ) -> CreateProfileResponseTypeDef:
        """
        Creates an empty Route 53 Profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/create_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#create_profile)
        """

    def delete_profile(
        self, **kwargs: Unpack[DeleteProfileRequestRequestTypeDef]
    ) -> DeleteProfileResponseTypeDef:
        """
        Deletes the specified Route 53 Profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/delete_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#delete_profile)
        """

    def disassociate_profile(
        self, **kwargs: Unpack[DisassociateProfileRequestRequestTypeDef]
    ) -> DisassociateProfileResponseTypeDef:
        """
        Dissociates a specified Route 53 Profile from the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/disassociate_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#disassociate_profile)
        """

    def disassociate_resource_from_profile(
        self, **kwargs: Unpack[DisassociateResourceFromProfileRequestRequestTypeDef]
    ) -> DisassociateResourceFromProfileResponseTypeDef:
        """
        Dissoaciated a specified resource, from the Route 53 Profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/disassociate_resource_from_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#disassociate_resource_from_profile)
        """

    def get_profile(
        self, **kwargs: Unpack[GetProfileRequestRequestTypeDef]
    ) -> GetProfileResponseTypeDef:
        """
        Returns information about a specified Route 53 Profile, such as whether whether
        the Profile is shared, and the current status of the Profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/get_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#get_profile)
        """

    def get_profile_association(
        self, **kwargs: Unpack[GetProfileAssociationRequestRequestTypeDef]
    ) -> GetProfileAssociationResponseTypeDef:
        """
        Retrieves a Route 53 Profile association for a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/get_profile_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#get_profile_association)
        """

    def get_profile_resource_association(
        self, **kwargs: Unpack[GetProfileResourceAssociationRequestRequestTypeDef]
    ) -> GetProfileResourceAssociationResponseTypeDef:
        """
        Returns information about a specified Route 53 Profile resource association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/get_profile_resource_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#get_profile_resource_association)
        """

    def list_profile_associations(
        self, **kwargs: Unpack[ListProfileAssociationsRequestRequestTypeDef]
    ) -> ListProfileAssociationsResponseTypeDef:
        """
        Lists all the VPCs that the specified Route 53 Profile is associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/list_profile_associations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#list_profile_associations)
        """

    def list_profile_resource_associations(
        self, **kwargs: Unpack[ListProfileResourceAssociationsRequestRequestTypeDef]
    ) -> ListProfileResourceAssociationsResponseTypeDef:
        """
        Lists all the resource associations for the specified Route 53 Profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/list_profile_resource_associations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#list_profile_resource_associations)
        """

    def list_profiles(
        self, **kwargs: Unpack[ListProfilesRequestRequestTypeDef]
    ) -> ListProfilesResponseTypeDef:
        """
        Lists all the Route 53 Profiles associated with your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/list_profiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#list_profiles)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags that you associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#list_tags_for_resource)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#untag_resource)
        """

    def update_profile_resource_association(
        self, **kwargs: Unpack[UpdateProfileResourceAssociationRequestRequestTypeDef]
    ) -> UpdateProfileResourceAssociationResponseTypeDef:
        """
        Updates the specified Route 53 Profile resourse association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/update_profile_resource_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#update_profile_resource_association)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_profile_associations"]
    ) -> ListProfileAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_profile_resource_associations"]
    ) -> ListProfileResourceAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_profiles"]) -> ListProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/client/#get_paginator)
        """
