"""
Type annotations for security-ir service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_security_ir.client import SecurityIncidentResponseClient

    session = Session()
    client: SecurityIncidentResponseClient = session.client("security-ir")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListCaseEditsPaginator,
    ListCasesPaginator,
    ListCommentsPaginator,
    ListMembershipsPaginator,
)
from .type_defs import (
    BatchGetMemberAccountDetailsRequestRequestTypeDef,
    BatchGetMemberAccountDetailsResponseTypeDef,
    CancelMembershipRequestRequestTypeDef,
    CancelMembershipResponseTypeDef,
    CloseCaseRequestRequestTypeDef,
    CloseCaseResponseTypeDef,
    CreateCaseCommentRequestRequestTypeDef,
    CreateCaseCommentResponseTypeDef,
    CreateCaseRequestRequestTypeDef,
    CreateCaseResponseTypeDef,
    CreateMembershipRequestRequestTypeDef,
    CreateMembershipResponseTypeDef,
    GetCaseAttachmentDownloadUrlRequestRequestTypeDef,
    GetCaseAttachmentDownloadUrlResponseTypeDef,
    GetCaseAttachmentUploadUrlRequestRequestTypeDef,
    GetCaseAttachmentUploadUrlResponseTypeDef,
    GetCaseRequestRequestTypeDef,
    GetCaseResponseTypeDef,
    GetMembershipRequestRequestTypeDef,
    GetMembershipResponseTypeDef,
    ListCaseEditsRequestRequestTypeDef,
    ListCaseEditsResponseTypeDef,
    ListCasesRequestRequestTypeDef,
    ListCasesResponseTypeDef,
    ListCommentsRequestRequestTypeDef,
    ListCommentsResponseTypeDef,
    ListMembershipsRequestRequestTypeDef,
    ListMembershipsResponseTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateCaseCommentRequestRequestTypeDef,
    UpdateCaseCommentResponseTypeDef,
    UpdateCaseRequestRequestTypeDef,
    UpdateCaseStatusRequestRequestTypeDef,
    UpdateCaseStatusResponseTypeDef,
    UpdateMembershipRequestRequestTypeDef,
    UpdateResolverTypeRequestRequestTypeDef,
    UpdateResolverTypeResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("SecurityIncidentResponseClient",)

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
    InvalidTokenException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    SecurityIncidentResponseNotActiveException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class SecurityIncidentResponseClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir.html#SecurityIncidentResponse.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SecurityIncidentResponseClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir.html#SecurityIncidentResponse.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#close)
        """

    def batch_get_member_account_details(
        self, **kwargs: Unpack[BatchGetMemberAccountDetailsRequestRequestTypeDef]
    ) -> BatchGetMemberAccountDetailsResponseTypeDef:
        """
        Grants permission to view an existing membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/batch_get_member_account_details.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#batch_get_member_account_details)
        """

    def cancel_membership(
        self, **kwargs: Unpack[CancelMembershipRequestRequestTypeDef]
    ) -> CancelMembershipResponseTypeDef:
        """
        Grants permissions to cancel an existing membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/cancel_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#cancel_membership)
        """

    def close_case(
        self, **kwargs: Unpack[CloseCaseRequestRequestTypeDef]
    ) -> CloseCaseResponseTypeDef:
        """
        Grants permission to close an existing case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/close_case.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#close_case)
        """

    def create_case(
        self, **kwargs: Unpack[CreateCaseRequestRequestTypeDef]
    ) -> CreateCaseResponseTypeDef:
        """
        Grants permission to create a new case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/create_case.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#create_case)
        """

    def create_case_comment(
        self, **kwargs: Unpack[CreateCaseCommentRequestRequestTypeDef]
    ) -> CreateCaseCommentResponseTypeDef:
        """
        Grants permission to add a comment to an existing case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/create_case_comment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#create_case_comment)
        """

    def create_membership(
        self, **kwargs: Unpack[CreateMembershipRequestRequestTypeDef]
    ) -> CreateMembershipResponseTypeDef:
        """
        Grants permissions to create a new membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/create_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#create_membership)
        """

    def get_case(self, **kwargs: Unpack[GetCaseRequestRequestTypeDef]) -> GetCaseResponseTypeDef:
        """
        Grant permission to view a designated case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_case.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#get_case)
        """

    def get_case_attachment_download_url(
        self, **kwargs: Unpack[GetCaseAttachmentDownloadUrlRequestRequestTypeDef]
    ) -> GetCaseAttachmentDownloadUrlResponseTypeDef:
        """
        Grants permission to obtain an Amazon S3 presigned URL to download an
        attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_case_attachment_download_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#get_case_attachment_download_url)
        """

    def get_case_attachment_upload_url(
        self, **kwargs: Unpack[GetCaseAttachmentUploadUrlRequestRequestTypeDef]
    ) -> GetCaseAttachmentUploadUrlResponseTypeDef:
        """
        Grants permission to upload an attachment to a case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_case_attachment_upload_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#get_case_attachment_upload_url)
        """

    def get_membership(
        self, **kwargs: Unpack[GetMembershipRequestRequestTypeDef]
    ) -> GetMembershipResponseTypeDef:
        """
        Grants permission to get details of a designated service membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#get_membership)
        """

    def list_case_edits(
        self, **kwargs: Unpack[ListCaseEditsRequestRequestTypeDef]
    ) -> ListCaseEditsResponseTypeDef:
        """
        Grants permissions to view the aidt log for edits made to a designated case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/list_case_edits.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#list_case_edits)
        """

    def list_cases(
        self, **kwargs: Unpack[ListCasesRequestRequestTypeDef]
    ) -> ListCasesResponseTypeDef:
        """
        Grants permission to list all cases the requester has access to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/list_cases.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#list_cases)
        """

    def list_comments(
        self, **kwargs: Unpack[ListCommentsRequestRequestTypeDef]
    ) -> ListCommentsResponseTypeDef:
        """
        Grants permissions to list and view comments for a designated case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/list_comments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#list_comments)
        """

    def list_memberships(
        self, **kwargs: Unpack[ListMembershipsRequestRequestTypeDef]
    ) -> ListMembershipsResponseTypeDef:
        """
        Grants permission to query the memberships a principal has access to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/list_memberships.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#list_memberships)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Grants permission to view currently configured tags on a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#list_tags_for_resource)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Grants permission to add a tag(s) to a designated resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Grants permission to remove a tag(s) from a designate resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#untag_resource)
        """

    def update_case(self, **kwargs: Unpack[UpdateCaseRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Grants permission to update an existing case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/update_case.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#update_case)
        """

    def update_case_comment(
        self, **kwargs: Unpack[UpdateCaseCommentRequestRequestTypeDef]
    ) -> UpdateCaseCommentResponseTypeDef:
        """
        Grants permission to update an existing case comment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/update_case_comment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#update_case_comment)
        """

    def update_case_status(
        self, **kwargs: Unpack[UpdateCaseStatusRequestRequestTypeDef]
    ) -> UpdateCaseStatusResponseTypeDef:
        """
        Grants permission to update the status for a designated cases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/update_case_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#update_case_status)
        """

    def update_membership(
        self, **kwargs: Unpack[UpdateMembershipRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Grants access to UpdateMembership to change membership configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/update_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#update_membership)
        """

    def update_resolver_type(
        self, **kwargs: Unpack[UpdateResolverTypeRequestRequestTypeDef]
    ) -> UpdateResolverTypeResponseTypeDef:
        """
        Grants permission to update the resolver type for a case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/update_resolver_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#update_resolver_type)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_case_edits"]) -> ListCaseEditsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_cases"]) -> ListCasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_comments"]) -> ListCommentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_memberships"]
    ) -> ListMembershipsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_security_ir/client/#get_paginator)
        """
