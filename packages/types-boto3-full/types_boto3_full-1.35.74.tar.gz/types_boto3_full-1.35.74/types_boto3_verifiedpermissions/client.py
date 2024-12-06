"""
Type annotations for verifiedpermissions service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_verifiedpermissions.client import VerifiedPermissionsClient

    session = Session()
    client: VerifiedPermissionsClient = session.client("verifiedpermissions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListIdentitySourcesPaginator,
    ListPoliciesPaginator,
    ListPolicyStoresPaginator,
    ListPolicyTemplatesPaginator,
)
from .type_defs import (
    BatchGetPolicyInputRequestTypeDef,
    BatchGetPolicyOutputTypeDef,
    BatchIsAuthorizedInputRequestTypeDef,
    BatchIsAuthorizedOutputTypeDef,
    BatchIsAuthorizedWithTokenInputRequestTypeDef,
    BatchIsAuthorizedWithTokenOutputTypeDef,
    CreateIdentitySourceInputRequestTypeDef,
    CreateIdentitySourceOutputTypeDef,
    CreatePolicyInputRequestTypeDef,
    CreatePolicyOutputTypeDef,
    CreatePolicyStoreInputRequestTypeDef,
    CreatePolicyStoreOutputTypeDef,
    CreatePolicyTemplateInputRequestTypeDef,
    CreatePolicyTemplateOutputTypeDef,
    DeleteIdentitySourceInputRequestTypeDef,
    DeletePolicyInputRequestTypeDef,
    DeletePolicyStoreInputRequestTypeDef,
    DeletePolicyTemplateInputRequestTypeDef,
    GetIdentitySourceInputRequestTypeDef,
    GetIdentitySourceOutputTypeDef,
    GetPolicyInputRequestTypeDef,
    GetPolicyOutputTypeDef,
    GetPolicyStoreInputRequestTypeDef,
    GetPolicyStoreOutputTypeDef,
    GetPolicyTemplateInputRequestTypeDef,
    GetPolicyTemplateOutputTypeDef,
    GetSchemaInputRequestTypeDef,
    GetSchemaOutputTypeDef,
    IsAuthorizedInputRequestTypeDef,
    IsAuthorizedOutputTypeDef,
    IsAuthorizedWithTokenInputRequestTypeDef,
    IsAuthorizedWithTokenOutputTypeDef,
    ListIdentitySourcesInputRequestTypeDef,
    ListIdentitySourcesOutputTypeDef,
    ListPoliciesInputRequestTypeDef,
    ListPoliciesOutputTypeDef,
    ListPolicyStoresInputRequestTypeDef,
    ListPolicyStoresOutputTypeDef,
    ListPolicyTemplatesInputRequestTypeDef,
    ListPolicyTemplatesOutputTypeDef,
    PutSchemaInputRequestTypeDef,
    PutSchemaOutputTypeDef,
    UpdateIdentitySourceInputRequestTypeDef,
    UpdateIdentitySourceOutputTypeDef,
    UpdatePolicyInputRequestTypeDef,
    UpdatePolicyOutputTypeDef,
    UpdatePolicyStoreInputRequestTypeDef,
    UpdatePolicyStoreOutputTypeDef,
    UpdatePolicyTemplateInputRequestTypeDef,
    UpdatePolicyTemplateOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("VerifiedPermissionsClient",)


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


class VerifiedPermissionsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        VerifiedPermissionsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#close)
        """

    def batch_get_policy(
        self, **kwargs: Unpack[BatchGetPolicyInputRequestTypeDef]
    ) -> BatchGetPolicyOutputTypeDef:
        """
        Retrieves information about a group (batch) of policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/batch_get_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#batch_get_policy)
        """

    def batch_is_authorized(
        self, **kwargs: Unpack[BatchIsAuthorizedInputRequestTypeDef]
    ) -> BatchIsAuthorizedOutputTypeDef:
        """
        Makes a series of decisions about multiple authorization requests for one
        principal or resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/batch_is_authorized.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#batch_is_authorized)
        """

    def batch_is_authorized_with_token(
        self, **kwargs: Unpack[BatchIsAuthorizedWithTokenInputRequestTypeDef]
    ) -> BatchIsAuthorizedWithTokenOutputTypeDef:
        """
        Makes a series of decisions about multiple authorization requests for one token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/batch_is_authorized_with_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#batch_is_authorized_with_token)
        """

    def create_identity_source(
        self, **kwargs: Unpack[CreateIdentitySourceInputRequestTypeDef]
    ) -> CreateIdentitySourceOutputTypeDef:
        """
        Adds an identity source to a policy store-an Amazon Cognito user pool or OpenID
        Connect (OIDC) identity provider (IdP).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/create_identity_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#create_identity_source)
        """

    def create_policy(
        self, **kwargs: Unpack[CreatePolicyInputRequestTypeDef]
    ) -> CreatePolicyOutputTypeDef:
        """
        Creates a Cedar policy and saves it in the specified policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/create_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#create_policy)
        """

    def create_policy_store(
        self, **kwargs: Unpack[CreatePolicyStoreInputRequestTypeDef]
    ) -> CreatePolicyStoreOutputTypeDef:
        """
        Creates a policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/create_policy_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#create_policy_store)
        """

    def create_policy_template(
        self, **kwargs: Unpack[CreatePolicyTemplateInputRequestTypeDef]
    ) -> CreatePolicyTemplateOutputTypeDef:
        """
        Creates a policy template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/create_policy_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#create_policy_template)
        """

    def delete_identity_source(
        self, **kwargs: Unpack[DeleteIdentitySourceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an identity source that references an identity provider (IdP) such as
        Amazon Cognito.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/delete_identity_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#delete_identity_source)
        """

    def delete_policy(self, **kwargs: Unpack[DeletePolicyInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified policy from the policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/delete_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#delete_policy)
        """

    def delete_policy_store(
        self, **kwargs: Unpack[DeletePolicyStoreInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/delete_policy_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#delete_policy_store)
        """

    def delete_policy_template(
        self, **kwargs: Unpack[DeletePolicyTemplateInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified policy template from the policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/delete_policy_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#delete_policy_template)
        """

    def get_identity_source(
        self, **kwargs: Unpack[GetIdentitySourceInputRequestTypeDef]
    ) -> GetIdentitySourceOutputTypeDef:
        """
        Retrieves the details about the specified identity source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/get_identity_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#get_identity_source)
        """

    def get_policy(self, **kwargs: Unpack[GetPolicyInputRequestTypeDef]) -> GetPolicyOutputTypeDef:
        """
        Retrieves information about the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/get_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#get_policy)
        """

    def get_policy_store(
        self, **kwargs: Unpack[GetPolicyStoreInputRequestTypeDef]
    ) -> GetPolicyStoreOutputTypeDef:
        """
        Retrieves details about a policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/get_policy_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#get_policy_store)
        """

    def get_policy_template(
        self, **kwargs: Unpack[GetPolicyTemplateInputRequestTypeDef]
    ) -> GetPolicyTemplateOutputTypeDef:
        """
        Retrieve the details for the specified policy template in the specified policy
        store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/get_policy_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#get_policy_template)
        """

    def get_schema(self, **kwargs: Unpack[GetSchemaInputRequestTypeDef]) -> GetSchemaOutputTypeDef:
        """
        Retrieve the details for the specified schema in the specified policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/get_schema.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#get_schema)
        """

    def is_authorized(
        self, **kwargs: Unpack[IsAuthorizedInputRequestTypeDef]
    ) -> IsAuthorizedOutputTypeDef:
        """
        Makes an authorization decision about a service request described in the
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/is_authorized.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#is_authorized)
        """

    def is_authorized_with_token(
        self, **kwargs: Unpack[IsAuthorizedWithTokenInputRequestTypeDef]
    ) -> IsAuthorizedWithTokenOutputTypeDef:
        """
        Makes an authorization decision about a service request described in the
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/is_authorized_with_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#is_authorized_with_token)
        """

    def list_identity_sources(
        self, **kwargs: Unpack[ListIdentitySourcesInputRequestTypeDef]
    ) -> ListIdentitySourcesOutputTypeDef:
        """
        Returns a paginated list of all of the identity sources defined in the
        specified policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/list_identity_sources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#list_identity_sources)
        """

    def list_policies(
        self, **kwargs: Unpack[ListPoliciesInputRequestTypeDef]
    ) -> ListPoliciesOutputTypeDef:
        """
        Returns a paginated list of all policies stored in the specified policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/list_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#list_policies)
        """

    def list_policy_stores(
        self, **kwargs: Unpack[ListPolicyStoresInputRequestTypeDef]
    ) -> ListPolicyStoresOutputTypeDef:
        """
        Returns a paginated list of all policy stores in the calling Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/list_policy_stores.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#list_policy_stores)
        """

    def list_policy_templates(
        self, **kwargs: Unpack[ListPolicyTemplatesInputRequestTypeDef]
    ) -> ListPolicyTemplatesOutputTypeDef:
        """
        Returns a paginated list of all policy templates in the specified policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/list_policy_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#list_policy_templates)
        """

    def put_schema(self, **kwargs: Unpack[PutSchemaInputRequestTypeDef]) -> PutSchemaOutputTypeDef:
        """
        Creates or updates the policy schema in the specified policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/put_schema.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#put_schema)
        """

    def update_identity_source(
        self, **kwargs: Unpack[UpdateIdentitySourceInputRequestTypeDef]
    ) -> UpdateIdentitySourceOutputTypeDef:
        """
        Updates the specified identity source to use a new identity provider (IdP), or
        to change the mapping of identities from the IdP to a different principal
        entity type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/update_identity_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#update_identity_source)
        """

    def update_policy(
        self, **kwargs: Unpack[UpdatePolicyInputRequestTypeDef]
    ) -> UpdatePolicyOutputTypeDef:
        """
        Modifies a Cedar static policy in the specified policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/update_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#update_policy)
        """

    def update_policy_store(
        self, **kwargs: Unpack[UpdatePolicyStoreInputRequestTypeDef]
    ) -> UpdatePolicyStoreOutputTypeDef:
        """
        Modifies the validation setting for a policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/update_policy_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#update_policy_store)
        """

    def update_policy_template(
        self, **kwargs: Unpack[UpdatePolicyTemplateInputRequestTypeDef]
    ) -> UpdatePolicyTemplateOutputTypeDef:
        """
        Updates the specified policy template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/update_policy_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#update_policy_template)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_identity_sources"]
    ) -> ListIdentitySourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_policies"]) -> ListPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_policy_stores"]
    ) -> ListPolicyStoresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_policy_templates"]
    ) -> ListPolicyTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_verifiedpermissions/client/#get_paginator)
        """
