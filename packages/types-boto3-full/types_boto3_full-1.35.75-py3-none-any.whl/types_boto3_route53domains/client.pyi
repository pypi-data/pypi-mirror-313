"""
Type annotations for route53domains service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_route53domains.client import Route53DomainsClient

    session = Session()
    client: Route53DomainsClient = session.client("route53domains")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListDomainsPaginator,
    ListOperationsPaginator,
    ListPricesPaginator,
    ViewBillingPaginator,
)
from .type_defs import (
    AcceptDomainTransferFromAnotherAwsAccountRequestRequestTypeDef,
    AcceptDomainTransferFromAnotherAwsAccountResponseTypeDef,
    AssociateDelegationSignerToDomainRequestRequestTypeDef,
    AssociateDelegationSignerToDomainResponseTypeDef,
    CancelDomainTransferToAnotherAwsAccountRequestRequestTypeDef,
    CancelDomainTransferToAnotherAwsAccountResponseTypeDef,
    CheckDomainAvailabilityRequestRequestTypeDef,
    CheckDomainAvailabilityResponseTypeDef,
    CheckDomainTransferabilityRequestRequestTypeDef,
    CheckDomainTransferabilityResponseTypeDef,
    DeleteDomainRequestRequestTypeDef,
    DeleteDomainResponseTypeDef,
    DeleteTagsForDomainRequestRequestTypeDef,
    DisableDomainAutoRenewRequestRequestTypeDef,
    DisableDomainTransferLockRequestRequestTypeDef,
    DisableDomainTransferLockResponseTypeDef,
    DisassociateDelegationSignerFromDomainRequestRequestTypeDef,
    DisassociateDelegationSignerFromDomainResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableDomainAutoRenewRequestRequestTypeDef,
    EnableDomainTransferLockRequestRequestTypeDef,
    EnableDomainTransferLockResponseTypeDef,
    GetContactReachabilityStatusRequestRequestTypeDef,
    GetContactReachabilityStatusResponseTypeDef,
    GetDomainDetailRequestRequestTypeDef,
    GetDomainDetailResponseTypeDef,
    GetDomainSuggestionsRequestRequestTypeDef,
    GetDomainSuggestionsResponseTypeDef,
    GetOperationDetailRequestRequestTypeDef,
    GetOperationDetailResponseTypeDef,
    ListDomainsRequestRequestTypeDef,
    ListDomainsResponseTypeDef,
    ListOperationsRequestRequestTypeDef,
    ListOperationsResponseTypeDef,
    ListPricesRequestRequestTypeDef,
    ListPricesResponseTypeDef,
    ListTagsForDomainRequestRequestTypeDef,
    ListTagsForDomainResponseTypeDef,
    PushDomainRequestRequestTypeDef,
    RegisterDomainRequestRequestTypeDef,
    RegisterDomainResponseTypeDef,
    RejectDomainTransferFromAnotherAwsAccountRequestRequestTypeDef,
    RejectDomainTransferFromAnotherAwsAccountResponseTypeDef,
    RenewDomainRequestRequestTypeDef,
    RenewDomainResponseTypeDef,
    ResendContactReachabilityEmailRequestRequestTypeDef,
    ResendContactReachabilityEmailResponseTypeDef,
    ResendOperationAuthorizationRequestRequestTypeDef,
    RetrieveDomainAuthCodeRequestRequestTypeDef,
    RetrieveDomainAuthCodeResponseTypeDef,
    TransferDomainRequestRequestTypeDef,
    TransferDomainResponseTypeDef,
    TransferDomainToAnotherAwsAccountRequestRequestTypeDef,
    TransferDomainToAnotherAwsAccountResponseTypeDef,
    UpdateDomainContactPrivacyRequestRequestTypeDef,
    UpdateDomainContactPrivacyResponseTypeDef,
    UpdateDomainContactRequestRequestTypeDef,
    UpdateDomainContactResponseTypeDef,
    UpdateDomainNameserversRequestRequestTypeDef,
    UpdateDomainNameserversResponseTypeDef,
    UpdateTagsForDomainRequestRequestTypeDef,
    ViewBillingRequestRequestTypeDef,
    ViewBillingResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("Route53DomainsClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    DnssecLimitExceeded: Type[BotocoreClientError]
    DomainLimitExceeded: Type[BotocoreClientError]
    DuplicateRequest: Type[BotocoreClientError]
    InvalidInput: Type[BotocoreClientError]
    OperationLimitExceeded: Type[BotocoreClientError]
    TLDRulesViolation: Type[BotocoreClientError]
    UnsupportedTLD: Type[BotocoreClientError]

class Route53DomainsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Route53DomainsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#close)
        """

    def accept_domain_transfer_from_another_aws_account(
        self, **kwargs: Unpack[AcceptDomainTransferFromAnotherAwsAccountRequestRequestTypeDef]
    ) -> AcceptDomainTransferFromAnotherAwsAccountResponseTypeDef:
        """
        Accepts the transfer of a domain from another Amazon Web Services account to
        the currentAmazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/accept_domain_transfer_from_another_aws_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#accept_domain_transfer_from_another_aws_account)
        """

    def associate_delegation_signer_to_domain(
        self, **kwargs: Unpack[AssociateDelegationSignerToDomainRequestRequestTypeDef]
    ) -> AssociateDelegationSignerToDomainResponseTypeDef:
        """
        Creates a delegation signer (DS) record in the registry zone for this domain
        name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/associate_delegation_signer_to_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#associate_delegation_signer_to_domain)
        """

    def cancel_domain_transfer_to_another_aws_account(
        self, **kwargs: Unpack[CancelDomainTransferToAnotherAwsAccountRequestRequestTypeDef]
    ) -> CancelDomainTransferToAnotherAwsAccountResponseTypeDef:
        """
        Cancels the transfer of a domain from the current Amazon Web Services account
        to another Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/cancel_domain_transfer_to_another_aws_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#cancel_domain_transfer_to_another_aws_account)
        """

    def check_domain_availability(
        self, **kwargs: Unpack[CheckDomainAvailabilityRequestRequestTypeDef]
    ) -> CheckDomainAvailabilityResponseTypeDef:
        """
        This operation checks the availability of one domain name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/check_domain_availability.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#check_domain_availability)
        """

    def check_domain_transferability(
        self, **kwargs: Unpack[CheckDomainTransferabilityRequestRequestTypeDef]
    ) -> CheckDomainTransferabilityResponseTypeDef:
        """
        Checks whether a domain name can be transferred to Amazon Route 53.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/check_domain_transferability.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#check_domain_transferability)
        """

    def delete_domain(
        self, **kwargs: Unpack[DeleteDomainRequestRequestTypeDef]
    ) -> DeleteDomainResponseTypeDef:
        """
        This operation deletes the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/delete_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#delete_domain)
        """

    def delete_tags_for_domain(
        self, **kwargs: Unpack[DeleteTagsForDomainRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This operation deletes the specified tags for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/delete_tags_for_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#delete_tags_for_domain)
        """

    def disable_domain_auto_renew(
        self, **kwargs: Unpack[DisableDomainAutoRenewRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This operation disables automatic renewal of domain registration for the
        specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/disable_domain_auto_renew.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#disable_domain_auto_renew)
        """

    def disable_domain_transfer_lock(
        self, **kwargs: Unpack[DisableDomainTransferLockRequestRequestTypeDef]
    ) -> DisableDomainTransferLockResponseTypeDef:
        """
        This operation removes the transfer lock on the domain (specifically the
        <code>clientTransferProhibited</code> status) to allow domain transfers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/disable_domain_transfer_lock.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#disable_domain_transfer_lock)
        """

    def disassociate_delegation_signer_from_domain(
        self, **kwargs: Unpack[DisassociateDelegationSignerFromDomainRequestRequestTypeDef]
    ) -> DisassociateDelegationSignerFromDomainResponseTypeDef:
        """
        Deletes a delegation signer (DS) record in the registry zone for this domain
        name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/disassociate_delegation_signer_from_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#disassociate_delegation_signer_from_domain)
        """

    def enable_domain_auto_renew(
        self, **kwargs: Unpack[EnableDomainAutoRenewRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This operation configures Amazon Route 53 to automatically renew the specified
        domain before the domain registration expires.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/enable_domain_auto_renew.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#enable_domain_auto_renew)
        """

    def enable_domain_transfer_lock(
        self, **kwargs: Unpack[EnableDomainTransferLockRequestRequestTypeDef]
    ) -> EnableDomainTransferLockResponseTypeDef:
        """
        This operation sets the transfer lock on the domain (specifically the
        <code>clientTransferProhibited</code> status) to prevent domain transfers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/enable_domain_transfer_lock.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#enable_domain_transfer_lock)
        """

    def get_contact_reachability_status(
        self, **kwargs: Unpack[GetContactReachabilityStatusRequestRequestTypeDef]
    ) -> GetContactReachabilityStatusResponseTypeDef:
        """
        For operations that require confirmation that the email address for the
        registrant contact is valid, such as registering a new domain, this operation
        returns information about whether the registrant contact has responded.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/get_contact_reachability_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#get_contact_reachability_status)
        """

    def get_domain_detail(
        self, **kwargs: Unpack[GetDomainDetailRequestRequestTypeDef]
    ) -> GetDomainDetailResponseTypeDef:
        """
        This operation returns detailed information about a specified domain that is
        associated with the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/get_domain_detail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#get_domain_detail)
        """

    def get_domain_suggestions(
        self, **kwargs: Unpack[GetDomainSuggestionsRequestRequestTypeDef]
    ) -> GetDomainSuggestionsResponseTypeDef:
        """
        The GetDomainSuggestions operation returns a list of suggested domain names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/get_domain_suggestions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#get_domain_suggestions)
        """

    def get_operation_detail(
        self, **kwargs: Unpack[GetOperationDetailRequestRequestTypeDef]
    ) -> GetOperationDetailResponseTypeDef:
        """
        This operation returns the current status of an operation that is not completed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/get_operation_detail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#get_operation_detail)
        """

    def list_domains(
        self, **kwargs: Unpack[ListDomainsRequestRequestTypeDef]
    ) -> ListDomainsResponseTypeDef:
        """
        This operation returns all the domain names registered with Amazon Route 53 for
        the current Amazon Web Services account if no filtering conditions are used.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/list_domains.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#list_domains)
        """

    def list_operations(
        self, **kwargs: Unpack[ListOperationsRequestRequestTypeDef]
    ) -> ListOperationsResponseTypeDef:
        """
        Returns information about all of the operations that return an operation ID and
        that have ever been performed on domains that were registered by the current
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/list_operations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#list_operations)
        """

    def list_prices(
        self, **kwargs: Unpack[ListPricesRequestRequestTypeDef]
    ) -> ListPricesResponseTypeDef:
        """
        Lists the following prices for either all the TLDs supported by Route 53, or
        the specified TLD:.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/list_prices.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#list_prices)
        """

    def list_tags_for_domain(
        self, **kwargs: Unpack[ListTagsForDomainRequestRequestTypeDef]
    ) -> ListTagsForDomainResponseTypeDef:
        """
        This operation returns all of the tags that are associated with the specified
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/list_tags_for_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#list_tags_for_domain)
        """

    def push_domain(
        self, **kwargs: Unpack[PushDomainRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Moves a domain from Amazon Web Services to another registrar.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/push_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#push_domain)
        """

    def register_domain(
        self, **kwargs: Unpack[RegisterDomainRequestRequestTypeDef]
    ) -> RegisterDomainResponseTypeDef:
        """
        This operation registers a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/register_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#register_domain)
        """

    def reject_domain_transfer_from_another_aws_account(
        self, **kwargs: Unpack[RejectDomainTransferFromAnotherAwsAccountRequestRequestTypeDef]
    ) -> RejectDomainTransferFromAnotherAwsAccountResponseTypeDef:
        """
        Rejects the transfer of a domain from another Amazon Web Services account to
        the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/reject_domain_transfer_from_another_aws_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#reject_domain_transfer_from_another_aws_account)
        """

    def renew_domain(
        self, **kwargs: Unpack[RenewDomainRequestRequestTypeDef]
    ) -> RenewDomainResponseTypeDef:
        """
        This operation renews a domain for the specified number of years.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/renew_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#renew_domain)
        """

    def resend_contact_reachability_email(
        self, **kwargs: Unpack[ResendContactReachabilityEmailRequestRequestTypeDef]
    ) -> ResendContactReachabilityEmailResponseTypeDef:
        """
        For operations that require confirmation that the email address for the
        registrant contact is valid, such as registering a new domain, this operation
        resends the confirmation email to the current email address for the registrant
        contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/resend_contact_reachability_email.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#resend_contact_reachability_email)
        """

    def resend_operation_authorization(
        self, **kwargs: Unpack[ResendOperationAuthorizationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Resend the form of authorization email for this operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/resend_operation_authorization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#resend_operation_authorization)
        """

    def retrieve_domain_auth_code(
        self, **kwargs: Unpack[RetrieveDomainAuthCodeRequestRequestTypeDef]
    ) -> RetrieveDomainAuthCodeResponseTypeDef:
        """
        This operation returns the authorization code for the domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/retrieve_domain_auth_code.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#retrieve_domain_auth_code)
        """

    def transfer_domain(
        self, **kwargs: Unpack[TransferDomainRequestRequestTypeDef]
    ) -> TransferDomainResponseTypeDef:
        """
        Transfers a domain from another registrar to Amazon Route 53.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/transfer_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#transfer_domain)
        """

    def transfer_domain_to_another_aws_account(
        self, **kwargs: Unpack[TransferDomainToAnotherAwsAccountRequestRequestTypeDef]
    ) -> TransferDomainToAnotherAwsAccountResponseTypeDef:
        """
        Transfers a domain from the current Amazon Web Services account to another
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/transfer_domain_to_another_aws_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#transfer_domain_to_another_aws_account)
        """

    def update_domain_contact(
        self, **kwargs: Unpack[UpdateDomainContactRequestRequestTypeDef]
    ) -> UpdateDomainContactResponseTypeDef:
        """
        This operation updates the contact information for a particular domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/update_domain_contact.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#update_domain_contact)
        """

    def update_domain_contact_privacy(
        self, **kwargs: Unpack[UpdateDomainContactPrivacyRequestRequestTypeDef]
    ) -> UpdateDomainContactPrivacyResponseTypeDef:
        """
        This operation updates the specified domain contact's privacy setting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/update_domain_contact_privacy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#update_domain_contact_privacy)
        """

    def update_domain_nameservers(
        self, **kwargs: Unpack[UpdateDomainNameserversRequestRequestTypeDef]
    ) -> UpdateDomainNameserversResponseTypeDef:
        """
        This operation replaces the current set of name servers for the domain with the
        specified set of name servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/update_domain_nameservers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#update_domain_nameservers)
        """

    def update_tags_for_domain(
        self, **kwargs: Unpack[UpdateTagsForDomainRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This operation adds or updates tags for a specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/update_tags_for_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#update_tags_for_domain)
        """

    def view_billing(
        self, **kwargs: Unpack[ViewBillingRequestRequestTypeDef]
    ) -> ViewBillingResponseTypeDef:
        """
        Returns all the domain-related billing records for the current Amazon Web
        Services account for a specified period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/view_billing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#view_billing)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_domains"]) -> ListDomainsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_operations"]) -> ListOperationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_prices"]) -> ListPricesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["view_billing"]) -> ViewBillingPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53domains/client/#get_paginator)
        """
