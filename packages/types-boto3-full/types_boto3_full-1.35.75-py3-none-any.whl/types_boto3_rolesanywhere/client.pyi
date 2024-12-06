"""
Type annotations for rolesanywhere service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_rolesanywhere.client import IAMRolesAnywhereClient

    session = Session()
    client: IAMRolesAnywhereClient = session.client("rolesanywhere")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListCrlsPaginator,
    ListProfilesPaginator,
    ListSubjectsPaginator,
    ListTrustAnchorsPaginator,
)
from .type_defs import (
    CreateProfileRequestRequestTypeDef,
    CreateTrustAnchorRequestRequestTypeDef,
    CrlDetailResponseTypeDef,
    DeleteAttributeMappingRequestRequestTypeDef,
    DeleteAttributeMappingResponseTypeDef,
    ImportCrlRequestRequestTypeDef,
    ListCrlsResponseTypeDef,
    ListProfilesResponseTypeDef,
    ListRequestRequestTypeDef,
    ListSubjectsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTrustAnchorsResponseTypeDef,
    ProfileDetailResponseTypeDef,
    PutAttributeMappingRequestRequestTypeDef,
    PutAttributeMappingResponseTypeDef,
    PutNotificationSettingsRequestRequestTypeDef,
    PutNotificationSettingsResponseTypeDef,
    ResetNotificationSettingsRequestRequestTypeDef,
    ResetNotificationSettingsResponseTypeDef,
    ScalarCrlRequestRequestTypeDef,
    ScalarProfileRequestRequestTypeDef,
    ScalarSubjectRequestRequestTypeDef,
    ScalarTrustAnchorRequestRequestTypeDef,
    SubjectDetailResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    TrustAnchorDetailResponseTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateCrlRequestRequestTypeDef,
    UpdateProfileRequestRequestTypeDef,
    UpdateTrustAnchorRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("IAMRolesAnywhereClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class IAMRolesAnywhereClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere.html#IAMRolesAnywhere.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IAMRolesAnywhereClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere.html#IAMRolesAnywhere.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#close)
        """

    def create_profile(
        self, **kwargs: Unpack[CreateProfileRequestRequestTypeDef]
    ) -> ProfileDetailResponseTypeDef:
        """
        Creates a <i>profile</i>, a list of the roles that Roles Anywhere service is
        trusted to assume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/create_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#create_profile)
        """

    def create_trust_anchor(
        self, **kwargs: Unpack[CreateTrustAnchorRequestRequestTypeDef]
    ) -> TrustAnchorDetailResponseTypeDef:
        """
        Creates a trust anchor to establish trust between IAM Roles Anywhere and your
        certificate authority (CA).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/create_trust_anchor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#create_trust_anchor)
        """

    def delete_attribute_mapping(
        self, **kwargs: Unpack[DeleteAttributeMappingRequestRequestTypeDef]
    ) -> DeleteAttributeMappingResponseTypeDef:
        """
        Delete an entry from the attribute mapping rules enforced by a given profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/delete_attribute_mapping.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#delete_attribute_mapping)
        """

    def delete_crl(
        self, **kwargs: Unpack[ScalarCrlRequestRequestTypeDef]
    ) -> CrlDetailResponseTypeDef:
        """
        Deletes a certificate revocation list (CRL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/delete_crl.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#delete_crl)
        """

    def delete_profile(
        self, **kwargs: Unpack[ScalarProfileRequestRequestTypeDef]
    ) -> ProfileDetailResponseTypeDef:
        """
        Deletes a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/delete_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#delete_profile)
        """

    def delete_trust_anchor(
        self, **kwargs: Unpack[ScalarTrustAnchorRequestRequestTypeDef]
    ) -> TrustAnchorDetailResponseTypeDef:
        """
        Deletes a trust anchor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/delete_trust_anchor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#delete_trust_anchor)
        """

    def disable_crl(
        self, **kwargs: Unpack[ScalarCrlRequestRequestTypeDef]
    ) -> CrlDetailResponseTypeDef:
        """
        Disables a certificate revocation list (CRL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/disable_crl.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#disable_crl)
        """

    def disable_profile(
        self, **kwargs: Unpack[ScalarProfileRequestRequestTypeDef]
    ) -> ProfileDetailResponseTypeDef:
        """
        Disables a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/disable_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#disable_profile)
        """

    def disable_trust_anchor(
        self, **kwargs: Unpack[ScalarTrustAnchorRequestRequestTypeDef]
    ) -> TrustAnchorDetailResponseTypeDef:
        """
        Disables a trust anchor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/disable_trust_anchor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#disable_trust_anchor)
        """

    def enable_crl(
        self, **kwargs: Unpack[ScalarCrlRequestRequestTypeDef]
    ) -> CrlDetailResponseTypeDef:
        """
        Enables a certificate revocation list (CRL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/enable_crl.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#enable_crl)
        """

    def enable_profile(
        self, **kwargs: Unpack[ScalarProfileRequestRequestTypeDef]
    ) -> ProfileDetailResponseTypeDef:
        """
        Enables temporary credential requests for a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/enable_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#enable_profile)
        """

    def enable_trust_anchor(
        self, **kwargs: Unpack[ScalarTrustAnchorRequestRequestTypeDef]
    ) -> TrustAnchorDetailResponseTypeDef:
        """
        Enables a trust anchor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/enable_trust_anchor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#enable_trust_anchor)
        """

    def get_crl(self, **kwargs: Unpack[ScalarCrlRequestRequestTypeDef]) -> CrlDetailResponseTypeDef:
        """
        Gets a certificate revocation list (CRL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/get_crl.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#get_crl)
        """

    def get_profile(
        self, **kwargs: Unpack[ScalarProfileRequestRequestTypeDef]
    ) -> ProfileDetailResponseTypeDef:
        """
        Gets a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/get_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#get_profile)
        """

    def get_subject(
        self, **kwargs: Unpack[ScalarSubjectRequestRequestTypeDef]
    ) -> SubjectDetailResponseTypeDef:
        """
        Gets a <i>subject</i>, which associates a certificate identity with
        authentication attempts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/get_subject.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#get_subject)
        """

    def get_trust_anchor(
        self, **kwargs: Unpack[ScalarTrustAnchorRequestRequestTypeDef]
    ) -> TrustAnchorDetailResponseTypeDef:
        """
        Gets a trust anchor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/get_trust_anchor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#get_trust_anchor)
        """

    def import_crl(
        self, **kwargs: Unpack[ImportCrlRequestRequestTypeDef]
    ) -> CrlDetailResponseTypeDef:
        """
        Imports the certificate revocation list (CRL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/import_crl.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#import_crl)
        """

    def list_crls(self, **kwargs: Unpack[ListRequestRequestTypeDef]) -> ListCrlsResponseTypeDef:
        """
        Lists all certificate revocation lists (CRL) in the authenticated account and
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/list_crls.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#list_crls)
        """

    def list_profiles(
        self, **kwargs: Unpack[ListRequestRequestTypeDef]
    ) -> ListProfilesResponseTypeDef:
        """
        Lists all profiles in the authenticated account and Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/list_profiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#list_profiles)
        """

    def list_subjects(
        self, **kwargs: Unpack[ListRequestRequestTypeDef]
    ) -> ListSubjectsResponseTypeDef:
        """
        Lists the subjects in the authenticated account and Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/list_subjects.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#list_subjects)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags attached to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#list_tags_for_resource)
        """

    def list_trust_anchors(
        self, **kwargs: Unpack[ListRequestRequestTypeDef]
    ) -> ListTrustAnchorsResponseTypeDef:
        """
        Lists the trust anchors in the authenticated account and Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/list_trust_anchors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#list_trust_anchors)
        """

    def put_attribute_mapping(
        self, **kwargs: Unpack[PutAttributeMappingRequestRequestTypeDef]
    ) -> PutAttributeMappingResponseTypeDef:
        """
        Put an entry in the attribute mapping rules that will be enforced by a given
        profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/put_attribute_mapping.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#put_attribute_mapping)
        """

    def put_notification_settings(
        self, **kwargs: Unpack[PutNotificationSettingsRequestRequestTypeDef]
    ) -> PutNotificationSettingsResponseTypeDef:
        """
        Attaches a list of <i>notification settings</i> to a trust anchor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/put_notification_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#put_notification_settings)
        """

    def reset_notification_settings(
        self, **kwargs: Unpack[ResetNotificationSettingsRequestRequestTypeDef]
    ) -> ResetNotificationSettingsResponseTypeDef:
        """
        Resets the <i>custom notification setting</i> to IAM Roles Anywhere default
        setting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/reset_notification_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#reset_notification_settings)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Attaches tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#untag_resource)
        """

    def update_crl(
        self, **kwargs: Unpack[UpdateCrlRequestRequestTypeDef]
    ) -> CrlDetailResponseTypeDef:
        """
        Updates the certificate revocation list (CRL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/update_crl.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#update_crl)
        """

    def update_profile(
        self, **kwargs: Unpack[UpdateProfileRequestRequestTypeDef]
    ) -> ProfileDetailResponseTypeDef:
        """
        Updates a <i>profile</i>, a list of the roles that IAM Roles Anywhere service
        is trusted to assume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/update_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#update_profile)
        """

    def update_trust_anchor(
        self, **kwargs: Unpack[UpdateTrustAnchorRequestRequestTypeDef]
    ) -> TrustAnchorDetailResponseTypeDef:
        """
        Updates a trust anchor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/update_trust_anchor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#update_trust_anchor)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_crls"]) -> ListCrlsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_profiles"]) -> ListProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_subjects"]) -> ListSubjectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_trust_anchors"]
    ) -> ListTrustAnchorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rolesanywhere/client/#get_paginator)
        """
