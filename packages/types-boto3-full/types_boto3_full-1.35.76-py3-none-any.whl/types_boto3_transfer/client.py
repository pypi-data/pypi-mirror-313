"""
Type annotations for transfer service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_transfer.client import TransferClient

    session = Session()
    client: TransferClient = session.client("transfer")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAccessesPaginator,
    ListAgreementsPaginator,
    ListCertificatesPaginator,
    ListConnectorsPaginator,
    ListExecutionsPaginator,
    ListFileTransferResultsPaginator,
    ListProfilesPaginator,
    ListSecurityPoliciesPaginator,
    ListServersPaginator,
    ListTagsForResourcePaginator,
    ListUsersPaginator,
    ListWebAppsPaginator,
    ListWorkflowsPaginator,
)
from .type_defs import (
    CreateAccessRequestRequestTypeDef,
    CreateAccessResponseTypeDef,
    CreateAgreementRequestRequestTypeDef,
    CreateAgreementResponseTypeDef,
    CreateConnectorRequestRequestTypeDef,
    CreateConnectorResponseTypeDef,
    CreateProfileRequestRequestTypeDef,
    CreateProfileResponseTypeDef,
    CreateServerRequestRequestTypeDef,
    CreateServerResponseTypeDef,
    CreateUserRequestRequestTypeDef,
    CreateUserResponseTypeDef,
    CreateWebAppRequestRequestTypeDef,
    CreateWebAppResponseTypeDef,
    CreateWorkflowRequestRequestTypeDef,
    CreateWorkflowResponseTypeDef,
    DeleteAccessRequestRequestTypeDef,
    DeleteAgreementRequestRequestTypeDef,
    DeleteCertificateRequestRequestTypeDef,
    DeleteConnectorRequestRequestTypeDef,
    DeleteHostKeyRequestRequestTypeDef,
    DeleteProfileRequestRequestTypeDef,
    DeleteServerRequestRequestTypeDef,
    DeleteSshPublicKeyRequestRequestTypeDef,
    DeleteUserRequestRequestTypeDef,
    DeleteWebAppCustomizationRequestRequestTypeDef,
    DeleteWebAppRequestRequestTypeDef,
    DeleteWorkflowRequestRequestTypeDef,
    DescribeAccessRequestRequestTypeDef,
    DescribeAccessResponseTypeDef,
    DescribeAgreementRequestRequestTypeDef,
    DescribeAgreementResponseTypeDef,
    DescribeCertificateRequestRequestTypeDef,
    DescribeCertificateResponseTypeDef,
    DescribeConnectorRequestRequestTypeDef,
    DescribeConnectorResponseTypeDef,
    DescribeExecutionRequestRequestTypeDef,
    DescribeExecutionResponseTypeDef,
    DescribeHostKeyRequestRequestTypeDef,
    DescribeHostKeyResponseTypeDef,
    DescribeProfileRequestRequestTypeDef,
    DescribeProfileResponseTypeDef,
    DescribeSecurityPolicyRequestRequestTypeDef,
    DescribeSecurityPolicyResponseTypeDef,
    DescribeServerRequestRequestTypeDef,
    DescribeServerResponseTypeDef,
    DescribeUserRequestRequestTypeDef,
    DescribeUserResponseTypeDef,
    DescribeWebAppCustomizationRequestRequestTypeDef,
    DescribeWebAppCustomizationResponseTypeDef,
    DescribeWebAppRequestRequestTypeDef,
    DescribeWebAppResponseTypeDef,
    DescribeWorkflowRequestRequestTypeDef,
    DescribeWorkflowResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ImportCertificateRequestRequestTypeDef,
    ImportCertificateResponseTypeDef,
    ImportHostKeyRequestRequestTypeDef,
    ImportHostKeyResponseTypeDef,
    ImportSshPublicKeyRequestRequestTypeDef,
    ImportSshPublicKeyResponseTypeDef,
    ListAccessesRequestRequestTypeDef,
    ListAccessesResponseTypeDef,
    ListAgreementsRequestRequestTypeDef,
    ListAgreementsResponseTypeDef,
    ListCertificatesRequestRequestTypeDef,
    ListCertificatesResponseTypeDef,
    ListConnectorsRequestRequestTypeDef,
    ListConnectorsResponseTypeDef,
    ListExecutionsRequestRequestTypeDef,
    ListExecutionsResponseTypeDef,
    ListFileTransferResultsRequestRequestTypeDef,
    ListFileTransferResultsResponseTypeDef,
    ListHostKeysRequestRequestTypeDef,
    ListHostKeysResponseTypeDef,
    ListProfilesRequestRequestTypeDef,
    ListProfilesResponseTypeDef,
    ListSecurityPoliciesRequestRequestTypeDef,
    ListSecurityPoliciesResponseTypeDef,
    ListServersRequestRequestTypeDef,
    ListServersResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUsersRequestRequestTypeDef,
    ListUsersResponseTypeDef,
    ListWebAppsRequestRequestTypeDef,
    ListWebAppsResponseTypeDef,
    ListWorkflowsRequestRequestTypeDef,
    ListWorkflowsResponseTypeDef,
    SendWorkflowStepStateRequestRequestTypeDef,
    StartDirectoryListingRequestRequestTypeDef,
    StartDirectoryListingResponseTypeDef,
    StartFileTransferRequestRequestTypeDef,
    StartFileTransferResponseTypeDef,
    StartServerRequestRequestTypeDef,
    StopServerRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    TestConnectionRequestRequestTypeDef,
    TestConnectionResponseTypeDef,
    TestIdentityProviderRequestRequestTypeDef,
    TestIdentityProviderResponseTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAccessRequestRequestTypeDef,
    UpdateAccessResponseTypeDef,
    UpdateAgreementRequestRequestTypeDef,
    UpdateAgreementResponseTypeDef,
    UpdateCertificateRequestRequestTypeDef,
    UpdateCertificateResponseTypeDef,
    UpdateConnectorRequestRequestTypeDef,
    UpdateConnectorResponseTypeDef,
    UpdateHostKeyRequestRequestTypeDef,
    UpdateHostKeyResponseTypeDef,
    UpdateProfileRequestRequestTypeDef,
    UpdateProfileResponseTypeDef,
    UpdateServerRequestRequestTypeDef,
    UpdateServerResponseTypeDef,
    UpdateUserRequestRequestTypeDef,
    UpdateUserResponseTypeDef,
    UpdateWebAppCustomizationRequestRequestTypeDef,
    UpdateWebAppCustomizationResponseTypeDef,
    UpdateWebAppRequestRequestTypeDef,
    UpdateWebAppResponseTypeDef,
)
from .waiter import ServerOfflineWaiter, ServerOnlineWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("TransferClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServiceError: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class TransferClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TransferClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#close)
        """

    def create_access(
        self, **kwargs: Unpack[CreateAccessRequestRequestTypeDef]
    ) -> CreateAccessResponseTypeDef:
        """
        Used by administrators to choose which groups in the directory should have
        access to upload and download files over the enabled protocols using Transfer
        Family.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/create_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#create_access)
        """

    def create_agreement(
        self, **kwargs: Unpack[CreateAgreementRequestRequestTypeDef]
    ) -> CreateAgreementResponseTypeDef:
        """
        Creates an agreement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/create_agreement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#create_agreement)
        """

    def create_connector(
        self, **kwargs: Unpack[CreateConnectorRequestRequestTypeDef]
    ) -> CreateConnectorResponseTypeDef:
        """
        Creates the connector, which captures the parameters for a connection for the
        AS2 or SFTP protocol.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/create_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#create_connector)
        """

    def create_profile(
        self, **kwargs: Unpack[CreateProfileRequestRequestTypeDef]
    ) -> CreateProfileResponseTypeDef:
        """
        Creates the local or partner profile to use for AS2 transfers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/create_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#create_profile)
        """

    def create_server(
        self, **kwargs: Unpack[CreateServerRequestRequestTypeDef]
    ) -> CreateServerResponseTypeDef:
        """
        Instantiates an auto-scaling virtual server based on the selected file transfer
        protocol in Amazon Web Services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/create_server.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#create_server)
        """

    def create_user(
        self, **kwargs: Unpack[CreateUserRequestRequestTypeDef]
    ) -> CreateUserResponseTypeDef:
        """
        Creates a user and associates them with an existing file transfer
        protocol-enabled server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/create_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#create_user)
        """

    def create_web_app(
        self, **kwargs: Unpack[CreateWebAppRequestRequestTypeDef]
    ) -> CreateWebAppResponseTypeDef:
        """
        Creates a web app based on specified parameters, and returns the ID for the new
        web app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/create_web_app.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#create_web_app)
        """

    def create_workflow(
        self, **kwargs: Unpack[CreateWorkflowRequestRequestTypeDef]
    ) -> CreateWorkflowResponseTypeDef:
        """
        Allows you to create a workflow with specified steps and step details the
        workflow invokes after file transfer completes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/create_workflow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#create_workflow)
        """

    def delete_access(
        self, **kwargs: Unpack[DeleteAccessRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Allows you to delete the access specified in the <code>ServerID</code> and
        <code>ExternalID</code> parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/delete_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#delete_access)
        """

    def delete_agreement(
        self, **kwargs: Unpack[DeleteAgreementRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete the agreement that's specified in the provided <code>AgreementId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/delete_agreement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#delete_agreement)
        """

    def delete_certificate(
        self, **kwargs: Unpack[DeleteCertificateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the certificate that's specified in the <code>CertificateId</code>
        parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/delete_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#delete_certificate)
        """

    def delete_connector(
        self, **kwargs: Unpack[DeleteConnectorRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the connector that's specified in the provided <code>ConnectorId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/delete_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#delete_connector)
        """

    def delete_host_key(
        self, **kwargs: Unpack[DeleteHostKeyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the host key that's specified in the <code>HostKeyId</code> parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/delete_host_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#delete_host_key)
        """

    def delete_profile(
        self, **kwargs: Unpack[DeleteProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the profile that's specified in the <code>ProfileId</code> parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/delete_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#delete_profile)
        """

    def delete_server(
        self, **kwargs: Unpack[DeleteServerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the file transfer protocol-enabled server that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/delete_server.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#delete_server)
        """

    def delete_ssh_public_key(
        self, **kwargs: Unpack[DeleteSshPublicKeyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a user's Secure Shell (SSH) public key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/delete_ssh_public_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#delete_ssh_public_key)
        """

    def delete_user(
        self, **kwargs: Unpack[DeleteUserRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the user belonging to a file transfer protocol-enabled server you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/delete_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#delete_user)
        """

    def delete_web_app(
        self, **kwargs: Unpack[DeleteWebAppRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified web app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/delete_web_app.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#delete_web_app)
        """

    def delete_web_app_customization(
        self, **kwargs: Unpack[DeleteWebAppCustomizationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the <code>WebAppCustomization</code> object that corresponds to the web
        app ID specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/delete_web_app_customization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#delete_web_app_customization)
        """

    def delete_workflow(
        self, **kwargs: Unpack[DeleteWorkflowRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/delete_workflow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#delete_workflow)
        """

    def describe_access(
        self, **kwargs: Unpack[DescribeAccessRequestRequestTypeDef]
    ) -> DescribeAccessResponseTypeDef:
        """
        Describes the access that is assigned to the specific file transfer
        protocol-enabled server, as identified by its <code>ServerId</code> property
        and its <code>ExternalId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/describe_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#describe_access)
        """

    def describe_agreement(
        self, **kwargs: Unpack[DescribeAgreementRequestRequestTypeDef]
    ) -> DescribeAgreementResponseTypeDef:
        """
        Describes the agreement that's identified by the <code>AgreementId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/describe_agreement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#describe_agreement)
        """

    def describe_certificate(
        self, **kwargs: Unpack[DescribeCertificateRequestRequestTypeDef]
    ) -> DescribeCertificateResponseTypeDef:
        """
        Describes the certificate that's identified by the <code>CertificateId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/describe_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#describe_certificate)
        """

    def describe_connector(
        self, **kwargs: Unpack[DescribeConnectorRequestRequestTypeDef]
    ) -> DescribeConnectorResponseTypeDef:
        """
        Describes the connector that's identified by the <code>ConnectorId.</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/describe_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#describe_connector)
        """

    def describe_execution(
        self, **kwargs: Unpack[DescribeExecutionRequestRequestTypeDef]
    ) -> DescribeExecutionResponseTypeDef:
        """
        You can use <code>DescribeExecution</code> to check the details of the
        execution of the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/describe_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#describe_execution)
        """

    def describe_host_key(
        self, **kwargs: Unpack[DescribeHostKeyRequestRequestTypeDef]
    ) -> DescribeHostKeyResponseTypeDef:
        """
        Returns the details of the host key that's specified by the
        <code>HostKeyId</code> and <code>ServerId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/describe_host_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#describe_host_key)
        """

    def describe_profile(
        self, **kwargs: Unpack[DescribeProfileRequestRequestTypeDef]
    ) -> DescribeProfileResponseTypeDef:
        """
        Returns the details of the profile that's specified by the
        <code>ProfileId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/describe_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#describe_profile)
        """

    def describe_security_policy(
        self, **kwargs: Unpack[DescribeSecurityPolicyRequestRequestTypeDef]
    ) -> DescribeSecurityPolicyResponseTypeDef:
        """
        Describes the security policy that is attached to your server or SFTP connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/describe_security_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#describe_security_policy)
        """

    def describe_server(
        self, **kwargs: Unpack[DescribeServerRequestRequestTypeDef]
    ) -> DescribeServerResponseTypeDef:
        """
        Describes a file transfer protocol-enabled server that you specify by passing
        the <code>ServerId</code> parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/describe_server.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#describe_server)
        """

    def describe_user(
        self, **kwargs: Unpack[DescribeUserRequestRequestTypeDef]
    ) -> DescribeUserResponseTypeDef:
        """
        Describes the user assigned to the specific file transfer protocol-enabled
        server, as identified by its <code>ServerId</code> property.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/describe_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#describe_user)
        """

    def describe_web_app(
        self, **kwargs: Unpack[DescribeWebAppRequestRequestTypeDef]
    ) -> DescribeWebAppResponseTypeDef:
        """
        Describes the web app that's identified by <code>WebAppId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/describe_web_app.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#describe_web_app)
        """

    def describe_web_app_customization(
        self, **kwargs: Unpack[DescribeWebAppCustomizationRequestRequestTypeDef]
    ) -> DescribeWebAppCustomizationResponseTypeDef:
        """
        Describes the web app customization object that's identified by
        <code>WebAppId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/describe_web_app_customization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#describe_web_app_customization)
        """

    def describe_workflow(
        self, **kwargs: Unpack[DescribeWorkflowRequestRequestTypeDef]
    ) -> DescribeWorkflowResponseTypeDef:
        """
        Describes the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/describe_workflow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#describe_workflow)
        """

    def import_certificate(
        self, **kwargs: Unpack[ImportCertificateRequestRequestTypeDef]
    ) -> ImportCertificateResponseTypeDef:
        """
        Imports the signing and encryption certificates that you need to create local
        (AS2) profiles and partner profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/import_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#import_certificate)
        """

    def import_host_key(
        self, **kwargs: Unpack[ImportHostKeyRequestRequestTypeDef]
    ) -> ImportHostKeyResponseTypeDef:
        """
        Adds a host key to the server that's specified by the <code>ServerId</code>
        parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/import_host_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#import_host_key)
        """

    def import_ssh_public_key(
        self, **kwargs: Unpack[ImportSshPublicKeyRequestRequestTypeDef]
    ) -> ImportSshPublicKeyResponseTypeDef:
        """
        Adds a Secure Shell (SSH) public key to a Transfer Family user identified by a
        <code>UserName</code> value assigned to the specific file transfer
        protocol-enabled server, identified by <code>ServerId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/import_ssh_public_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#import_ssh_public_key)
        """

    def list_accesses(
        self, **kwargs: Unpack[ListAccessesRequestRequestTypeDef]
    ) -> ListAccessesResponseTypeDef:
        """
        Lists the details for all the accesses you have on your server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/list_accesses.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#list_accesses)
        """

    def list_agreements(
        self, **kwargs: Unpack[ListAgreementsRequestRequestTypeDef]
    ) -> ListAgreementsResponseTypeDef:
        """
        Returns a list of the agreements for the server that's identified by the
        <code>ServerId</code> that you supply.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/list_agreements.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#list_agreements)
        """

    def list_certificates(
        self, **kwargs: Unpack[ListCertificatesRequestRequestTypeDef]
    ) -> ListCertificatesResponseTypeDef:
        """
        Returns a list of the current certificates that have been imported into
        Transfer Family.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/list_certificates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#list_certificates)
        """

    def list_connectors(
        self, **kwargs: Unpack[ListConnectorsRequestRequestTypeDef]
    ) -> ListConnectorsResponseTypeDef:
        """
        Lists the connectors for the specified Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/list_connectors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#list_connectors)
        """

    def list_executions(
        self, **kwargs: Unpack[ListExecutionsRequestRequestTypeDef]
    ) -> ListExecutionsResponseTypeDef:
        """
        Lists all in-progress executions for the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/list_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#list_executions)
        """

    def list_file_transfer_results(
        self, **kwargs: Unpack[ListFileTransferResultsRequestRequestTypeDef]
    ) -> ListFileTransferResultsResponseTypeDef:
        """
        Returns real-time updates and detailed information on the status of each
        individual file being transferred in a specific file transfer operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/list_file_transfer_results.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#list_file_transfer_results)
        """

    def list_host_keys(
        self, **kwargs: Unpack[ListHostKeysRequestRequestTypeDef]
    ) -> ListHostKeysResponseTypeDef:
        """
        Returns a list of host keys for the server that's specified by the
        <code>ServerId</code> parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/list_host_keys.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#list_host_keys)
        """

    def list_profiles(
        self, **kwargs: Unpack[ListProfilesRequestRequestTypeDef]
    ) -> ListProfilesResponseTypeDef:
        """
        Returns a list of the profiles for your system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/list_profiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#list_profiles)
        """

    def list_security_policies(
        self, **kwargs: Unpack[ListSecurityPoliciesRequestRequestTypeDef]
    ) -> ListSecurityPoliciesResponseTypeDef:
        """
        Lists the security policies that are attached to your servers and SFTP
        connectors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/list_security_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#list_security_policies)
        """

    def list_servers(
        self, **kwargs: Unpack[ListServersRequestRequestTypeDef]
    ) -> ListServersResponseTypeDef:
        """
        Lists the file transfer protocol-enabled servers that are associated with your
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/list_servers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#list_servers)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all of the tags associated with the Amazon Resource Name (ARN) that you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#list_tags_for_resource)
        """

    def list_users(
        self, **kwargs: Unpack[ListUsersRequestRequestTypeDef]
    ) -> ListUsersResponseTypeDef:
        """
        Lists the users for a file transfer protocol-enabled server that you specify by
        passing the <code>ServerId</code> parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/list_users.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#list_users)
        """

    def list_web_apps(
        self, **kwargs: Unpack[ListWebAppsRequestRequestTypeDef]
    ) -> ListWebAppsResponseTypeDef:
        """
        Lists all web apps associated with your Amazon Web Services account for your
        current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/list_web_apps.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#list_web_apps)
        """

    def list_workflows(
        self, **kwargs: Unpack[ListWorkflowsRequestRequestTypeDef]
    ) -> ListWorkflowsResponseTypeDef:
        """
        Lists all workflows associated with your Amazon Web Services account for your
        current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/list_workflows.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#list_workflows)
        """

    def send_workflow_step_state(
        self, **kwargs: Unpack[SendWorkflowStepStateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sends a callback for asynchronous custom steps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/send_workflow_step_state.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#send_workflow_step_state)
        """

    def start_directory_listing(
        self, **kwargs: Unpack[StartDirectoryListingRequestRequestTypeDef]
    ) -> StartDirectoryListingResponseTypeDef:
        """
        Retrieves a list of the contents of a directory from a remote SFTP server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/start_directory_listing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#start_directory_listing)
        """

    def start_file_transfer(
        self, **kwargs: Unpack[StartFileTransferRequestRequestTypeDef]
    ) -> StartFileTransferResponseTypeDef:
        """
        Begins a file transfer between local Amazon Web Services storage and a remote
        AS2 or SFTP server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/start_file_transfer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#start_file_transfer)
        """

    def start_server(
        self, **kwargs: Unpack[StartServerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Changes the state of a file transfer protocol-enabled server from
        <code>OFFLINE</code> to <code>ONLINE</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/start_server.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#start_server)
        """

    def stop_server(
        self, **kwargs: Unpack[StopServerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Changes the state of a file transfer protocol-enabled server from
        <code>ONLINE</code> to <code>OFFLINE</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/stop_server.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#stop_server)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches a key-value pair to a resource, as identified by its Amazon Resource
        Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#tag_resource)
        """

    def test_connection(
        self, **kwargs: Unpack[TestConnectionRequestRequestTypeDef]
    ) -> TestConnectionResponseTypeDef:
        """
        Tests whether your SFTP connector is set up successfully.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/test_connection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#test_connection)
        """

    def test_identity_provider(
        self, **kwargs: Unpack[TestIdentityProviderRequestRequestTypeDef]
    ) -> TestIdentityProviderResponseTypeDef:
        """
        If the <code>IdentityProviderType</code> of a file transfer protocol-enabled
        server is <code>AWS_DIRECTORY_SERVICE</code> or <code>API_Gateway</code>, tests
        whether your identity provider is set up successfully.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/test_identity_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#test_identity_provider)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Detaches a key-value pair from a resource, as identified by its Amazon Resource
        Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#untag_resource)
        """

    def update_access(
        self, **kwargs: Unpack[UpdateAccessRequestRequestTypeDef]
    ) -> UpdateAccessResponseTypeDef:
        """
        Allows you to update parameters for the access specified in the
        <code>ServerID</code> and <code>ExternalID</code> parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/update_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#update_access)
        """

    def update_agreement(
        self, **kwargs: Unpack[UpdateAgreementRequestRequestTypeDef]
    ) -> UpdateAgreementResponseTypeDef:
        """
        Updates some of the parameters for an existing agreement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/update_agreement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#update_agreement)
        """

    def update_certificate(
        self, **kwargs: Unpack[UpdateCertificateRequestRequestTypeDef]
    ) -> UpdateCertificateResponseTypeDef:
        """
        Updates the active and inactive dates for a certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/update_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#update_certificate)
        """

    def update_connector(
        self, **kwargs: Unpack[UpdateConnectorRequestRequestTypeDef]
    ) -> UpdateConnectorResponseTypeDef:
        """
        Updates some of the parameters for an existing connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/update_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#update_connector)
        """

    def update_host_key(
        self, **kwargs: Unpack[UpdateHostKeyRequestRequestTypeDef]
    ) -> UpdateHostKeyResponseTypeDef:
        """
        Updates the description for the host key that's specified by the
        <code>ServerId</code> and <code>HostKeyId</code> parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/update_host_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#update_host_key)
        """

    def update_profile(
        self, **kwargs: Unpack[UpdateProfileRequestRequestTypeDef]
    ) -> UpdateProfileResponseTypeDef:
        """
        Updates some of the parameters for an existing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/update_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#update_profile)
        """

    def update_server(
        self, **kwargs: Unpack[UpdateServerRequestRequestTypeDef]
    ) -> UpdateServerResponseTypeDef:
        """
        Updates the file transfer protocol-enabled server's properties after that
        server has been created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/update_server.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#update_server)
        """

    def update_user(
        self, **kwargs: Unpack[UpdateUserRequestRequestTypeDef]
    ) -> UpdateUserResponseTypeDef:
        """
        Assigns new properties to a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/update_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#update_user)
        """

    def update_web_app(
        self, **kwargs: Unpack[UpdateWebAppRequestRequestTypeDef]
    ) -> UpdateWebAppResponseTypeDef:
        """
        Assigns new properties to a web app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/update_web_app.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#update_web_app)
        """

    def update_web_app_customization(
        self, **kwargs: Unpack[UpdateWebAppCustomizationRequestRequestTypeDef]
    ) -> UpdateWebAppCustomizationResponseTypeDef:
        """
        Assigns new customization properties to a web app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/update_web_app_customization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#update_web_app_customization)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_accesses"]) -> ListAccessesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_agreements"]) -> ListAgreementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_certificates"]
    ) -> ListCertificatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_connectors"]) -> ListConnectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_executions"]) -> ListExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_file_transfer_results"]
    ) -> ListFileTransferResultsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_profiles"]) -> ListProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_security_policies"]
    ) -> ListSecurityPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_servers"]) -> ListServersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_web_apps"]) -> ListWebAppsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workflows"]) -> ListWorkflowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["server_offline"]) -> ServerOfflineWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["server_online"]) -> ServerOnlineWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transfer/client/#get_waiter)
        """
