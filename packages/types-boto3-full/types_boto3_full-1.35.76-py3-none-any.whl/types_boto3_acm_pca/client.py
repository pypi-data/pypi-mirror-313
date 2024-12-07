"""
Type annotations for acm-pca service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_acm_pca.client import ACMPCAClient

    session = Session()
    client: ACMPCAClient = session.client("acm-pca")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListCertificateAuthoritiesPaginator,
    ListPermissionsPaginator,
    ListTagsPaginator,
)
from .type_defs import (
    CreateCertificateAuthorityAuditReportRequestRequestTypeDef,
    CreateCertificateAuthorityAuditReportResponseTypeDef,
    CreateCertificateAuthorityRequestRequestTypeDef,
    CreateCertificateAuthorityResponseTypeDef,
    CreatePermissionRequestRequestTypeDef,
    DeleteCertificateAuthorityRequestRequestTypeDef,
    DeletePermissionRequestRequestTypeDef,
    DeletePolicyRequestRequestTypeDef,
    DescribeCertificateAuthorityAuditReportRequestRequestTypeDef,
    DescribeCertificateAuthorityAuditReportResponseTypeDef,
    DescribeCertificateAuthorityRequestRequestTypeDef,
    DescribeCertificateAuthorityResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCertificateAuthorityCertificateRequestRequestTypeDef,
    GetCertificateAuthorityCertificateResponseTypeDef,
    GetCertificateAuthorityCsrRequestRequestTypeDef,
    GetCertificateAuthorityCsrResponseTypeDef,
    GetCertificateRequestRequestTypeDef,
    GetCertificateResponseTypeDef,
    GetPolicyRequestRequestTypeDef,
    GetPolicyResponseTypeDef,
    ImportCertificateAuthorityCertificateRequestRequestTypeDef,
    IssueCertificateRequestRequestTypeDef,
    IssueCertificateResponseTypeDef,
    ListCertificateAuthoritiesRequestRequestTypeDef,
    ListCertificateAuthoritiesResponseTypeDef,
    ListPermissionsRequestRequestTypeDef,
    ListPermissionsResponseTypeDef,
    ListTagsRequestRequestTypeDef,
    ListTagsResponseTypeDef,
    PutPolicyRequestRequestTypeDef,
    RestoreCertificateAuthorityRequestRequestTypeDef,
    RevokeCertificateRequestRequestTypeDef,
    TagCertificateAuthorityRequestRequestTypeDef,
    UntagCertificateAuthorityRequestRequestTypeDef,
    UpdateCertificateAuthorityRequestRequestTypeDef,
)
from .waiter import (
    AuditReportCreatedWaiter,
    CertificateAuthorityCSRCreatedWaiter,
    CertificateIssuedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ACMPCAClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    CertificateMismatchException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    InvalidArgsException: Type[BotocoreClientError]
    InvalidArnException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidPolicyException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    InvalidTagException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    LockoutPreventedException: Type[BotocoreClientError]
    MalformedCSRException: Type[BotocoreClientError]
    MalformedCertificateException: Type[BotocoreClientError]
    PermissionAlreadyExistsException: Type[BotocoreClientError]
    RequestAlreadyProcessedException: Type[BotocoreClientError]
    RequestFailedException: Type[BotocoreClientError]
    RequestInProgressException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]


class ACMPCAClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca.html#ACMPCA.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ACMPCAClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca.html#ACMPCA.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#close)
        """

    def create_certificate_authority(
        self, **kwargs: Unpack[CreateCertificateAuthorityRequestRequestTypeDef]
    ) -> CreateCertificateAuthorityResponseTypeDef:
        """
        Creates a root or subordinate private certificate authority (CA).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/create_certificate_authority.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#create_certificate_authority)
        """

    def create_certificate_authority_audit_report(
        self, **kwargs: Unpack[CreateCertificateAuthorityAuditReportRequestRequestTypeDef]
    ) -> CreateCertificateAuthorityAuditReportResponseTypeDef:
        """
        Creates an audit report that lists every time that your CA private key is used
        to issue a certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/create_certificate_authority_audit_report.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#create_certificate_authority_audit_report)
        """

    def create_permission(
        self, **kwargs: Unpack[CreatePermissionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Grants one or more permissions on a private CA to the Certificate Manager (ACM)
        service principal (<code>acm.amazonaws.com</code>).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/create_permission.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#create_permission)
        """

    def delete_certificate_authority(
        self, **kwargs: Unpack[DeleteCertificateAuthorityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a private certificate authority (CA).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/delete_certificate_authority.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#delete_certificate_authority)
        """

    def delete_permission(
        self, **kwargs: Unpack[DeletePermissionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Revokes permissions on a private CA granted to the Certificate Manager (ACM)
        service principal (acm.amazonaws.com).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/delete_permission.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#delete_permission)
        """

    def delete_policy(
        self, **kwargs: Unpack[DeletePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the resource-based policy attached to a private CA.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/delete_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#delete_policy)
        """

    def describe_certificate_authority(
        self, **kwargs: Unpack[DescribeCertificateAuthorityRequestRequestTypeDef]
    ) -> DescribeCertificateAuthorityResponseTypeDef:
        """
        Lists information about your private certificate authority (CA) or one that has
        been shared with you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/describe_certificate_authority.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#describe_certificate_authority)
        """

    def describe_certificate_authority_audit_report(
        self, **kwargs: Unpack[DescribeCertificateAuthorityAuditReportRequestRequestTypeDef]
    ) -> DescribeCertificateAuthorityAuditReportResponseTypeDef:
        """
        Lists information about a specific audit report created by calling the <a
        href="https://docs.aws.amazon.com/privateca/latest/APIReference/API_CreateCertificateAuthorityAuditReport.html">CreateCertificateAuthorityAuditReport</a>
        action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/describe_certificate_authority_audit_report.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#describe_certificate_authority_audit_report)
        """

    def get_certificate(
        self, **kwargs: Unpack[GetCertificateRequestRequestTypeDef]
    ) -> GetCertificateResponseTypeDef:
        """
        Retrieves a certificate from your private CA or one that has been shared with
        you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/get_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#get_certificate)
        """

    def get_certificate_authority_certificate(
        self, **kwargs: Unpack[GetCertificateAuthorityCertificateRequestRequestTypeDef]
    ) -> GetCertificateAuthorityCertificateResponseTypeDef:
        """
        Retrieves the certificate and certificate chain for your private certificate
        authority (CA) or one that has been shared with you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/get_certificate_authority_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#get_certificate_authority_certificate)
        """

    def get_certificate_authority_csr(
        self, **kwargs: Unpack[GetCertificateAuthorityCsrRequestRequestTypeDef]
    ) -> GetCertificateAuthorityCsrResponseTypeDef:
        """
        Retrieves the certificate signing request (CSR) for your private certificate
        authority (CA).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/get_certificate_authority_csr.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#get_certificate_authority_csr)
        """

    def get_policy(
        self, **kwargs: Unpack[GetPolicyRequestRequestTypeDef]
    ) -> GetPolicyResponseTypeDef:
        """
        Retrieves the resource-based policy attached to a private CA.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/get_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#get_policy)
        """

    def import_certificate_authority_certificate(
        self, **kwargs: Unpack[ImportCertificateAuthorityCertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Imports a signed private CA certificate into Amazon Web Services Private CA.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/import_certificate_authority_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#import_certificate_authority_certificate)
        """

    def issue_certificate(
        self, **kwargs: Unpack[IssueCertificateRequestRequestTypeDef]
    ) -> IssueCertificateResponseTypeDef:
        """
        Uses your private certificate authority (CA), or one that has been shared with
        you, to issue a client certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/issue_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#issue_certificate)
        """

    def list_certificate_authorities(
        self, **kwargs: Unpack[ListCertificateAuthoritiesRequestRequestTypeDef]
    ) -> ListCertificateAuthoritiesResponseTypeDef:
        """
        Lists the private certificate authorities that you created by using the <a
        href="https://docs.aws.amazon.com/privateca/latest/APIReference/API_CreateCertificateAuthority.html">CreateCertificateAuthority</a>
        action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/list_certificate_authorities.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#list_certificate_authorities)
        """

    def list_permissions(
        self, **kwargs: Unpack[ListPermissionsRequestRequestTypeDef]
    ) -> ListPermissionsResponseTypeDef:
        """
        List all permissions on a private CA, if any, granted to the Certificate
        Manager (ACM) service principal (acm.amazonaws.com).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/list_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#list_permissions)
        """

    def list_tags(self, **kwargs: Unpack[ListTagsRequestRequestTypeDef]) -> ListTagsResponseTypeDef:
        """
        Lists the tags, if any, that are associated with your private CA or one that
        has been shared with you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/list_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#list_tags)
        """

    def put_policy(
        self, **kwargs: Unpack[PutPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches a resource-based policy to a private CA.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/put_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#put_policy)
        """

    def restore_certificate_authority(
        self, **kwargs: Unpack[RestoreCertificateAuthorityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Restores a certificate authority (CA) that is in the <code>DELETED</code> state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/restore_certificate_authority.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#restore_certificate_authority)
        """

    def revoke_certificate(
        self, **kwargs: Unpack[RevokeCertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Revokes a certificate that was issued inside Amazon Web Services Private CA.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/revoke_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#revoke_certificate)
        """

    def tag_certificate_authority(
        self, **kwargs: Unpack[TagCertificateAuthorityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds one or more tags to your private CA.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/tag_certificate_authority.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#tag_certificate_authority)
        """

    def untag_certificate_authority(
        self, **kwargs: Unpack[UntagCertificateAuthorityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove one or more tags from your private CA.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/untag_certificate_authority.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#untag_certificate_authority)
        """

    def update_certificate_authority(
        self, **kwargs: Unpack[UpdateCertificateAuthorityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the status or configuration of a private certificate authority (CA).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/update_certificate_authority.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#update_certificate_authority)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_certificate_authorities"]
    ) -> ListCertificateAuthoritiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_permissions"]
    ) -> ListPermissionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tags"]) -> ListTagsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["audit_report_created"]) -> AuditReportCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["certificate_authority_csr_created"]
    ) -> CertificateAuthorityCSRCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["certificate_issued"]) -> CertificateIssuedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm_pca/client/#get_waiter)
        """
