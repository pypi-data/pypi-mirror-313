"""
Type annotations for fms service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_fms.client import FMSClient

    session = Session()
    client: FMSClient = session.client("fms")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAdminAccountsForOrganizationPaginator,
    ListAdminsManagingAccountPaginator,
    ListAppsListsPaginator,
    ListComplianceStatusPaginator,
    ListMemberAccountsPaginator,
    ListPoliciesPaginator,
    ListProtocolsListsPaginator,
    ListThirdPartyFirewallFirewallPoliciesPaginator,
)
from .type_defs import (
    AssociateAdminAccountRequestRequestTypeDef,
    AssociateThirdPartyFirewallRequestRequestTypeDef,
    AssociateThirdPartyFirewallResponseTypeDef,
    BatchAssociateResourceRequestRequestTypeDef,
    BatchAssociateResourceResponseTypeDef,
    BatchDisassociateResourceRequestRequestTypeDef,
    BatchDisassociateResourceResponseTypeDef,
    DeleteAppsListRequestRequestTypeDef,
    DeletePolicyRequestRequestTypeDef,
    DeleteProtocolsListRequestRequestTypeDef,
    DeleteResourceSetRequestRequestTypeDef,
    DisassociateThirdPartyFirewallRequestRequestTypeDef,
    DisassociateThirdPartyFirewallResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAdminAccountResponseTypeDef,
    GetAdminScopeRequestRequestTypeDef,
    GetAdminScopeResponseTypeDef,
    GetAppsListRequestRequestTypeDef,
    GetAppsListResponseTypeDef,
    GetComplianceDetailRequestRequestTypeDef,
    GetComplianceDetailResponseTypeDef,
    GetNotificationChannelResponseTypeDef,
    GetPolicyRequestRequestTypeDef,
    GetPolicyResponseTypeDef,
    GetProtectionStatusRequestRequestTypeDef,
    GetProtectionStatusResponseTypeDef,
    GetProtocolsListRequestRequestTypeDef,
    GetProtocolsListResponseTypeDef,
    GetResourceSetRequestRequestTypeDef,
    GetResourceSetResponseTypeDef,
    GetThirdPartyFirewallAssociationStatusRequestRequestTypeDef,
    GetThirdPartyFirewallAssociationStatusResponseTypeDef,
    GetViolationDetailsRequestRequestTypeDef,
    GetViolationDetailsResponseTypeDef,
    ListAdminAccountsForOrganizationRequestRequestTypeDef,
    ListAdminAccountsForOrganizationResponseTypeDef,
    ListAdminsManagingAccountRequestRequestTypeDef,
    ListAdminsManagingAccountResponseTypeDef,
    ListAppsListsRequestRequestTypeDef,
    ListAppsListsResponseTypeDef,
    ListComplianceStatusRequestRequestTypeDef,
    ListComplianceStatusResponseTypeDef,
    ListDiscoveredResourcesRequestRequestTypeDef,
    ListDiscoveredResourcesResponseTypeDef,
    ListMemberAccountsRequestRequestTypeDef,
    ListMemberAccountsResponseTypeDef,
    ListPoliciesRequestRequestTypeDef,
    ListPoliciesResponseTypeDef,
    ListProtocolsListsRequestRequestTypeDef,
    ListProtocolsListsResponseTypeDef,
    ListResourceSetResourcesRequestRequestTypeDef,
    ListResourceSetResourcesResponseTypeDef,
    ListResourceSetsRequestRequestTypeDef,
    ListResourceSetsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListThirdPartyFirewallFirewallPoliciesRequestRequestTypeDef,
    ListThirdPartyFirewallFirewallPoliciesResponseTypeDef,
    PutAdminAccountRequestRequestTypeDef,
    PutAppsListRequestRequestTypeDef,
    PutAppsListResponseTypeDef,
    PutNotificationChannelRequestRequestTypeDef,
    PutPolicyRequestRequestTypeDef,
    PutPolicyResponseTypeDef,
    PutProtocolsListRequestRequestTypeDef,
    PutProtocolsListResponseTypeDef,
    PutResourceSetRequestRequestTypeDef,
    PutResourceSetResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("FMSClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalErrorException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    InvalidOperationException: Type[BotocoreClientError]
    InvalidTypeException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class FMSClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        FMSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#close)
        """

    def associate_admin_account(
        self, **kwargs: Unpack[AssociateAdminAccountRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets a Firewall Manager default administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/associate_admin_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#associate_admin_account)
        """

    def associate_third_party_firewall(
        self, **kwargs: Unpack[AssociateThirdPartyFirewallRequestRequestTypeDef]
    ) -> AssociateThirdPartyFirewallResponseTypeDef:
        """
        Sets the Firewall Manager policy administrator as a tenant administrator of a
        third-party firewall service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/associate_third_party_firewall.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#associate_third_party_firewall)
        """

    def batch_associate_resource(
        self, **kwargs: Unpack[BatchAssociateResourceRequestRequestTypeDef]
    ) -> BatchAssociateResourceResponseTypeDef:
        """
        Associate resources to a Firewall Manager resource set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/batch_associate_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#batch_associate_resource)
        """

    def batch_disassociate_resource(
        self, **kwargs: Unpack[BatchDisassociateResourceRequestRequestTypeDef]
    ) -> BatchDisassociateResourceResponseTypeDef:
        """
        Disassociates resources from a Firewall Manager resource set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/batch_disassociate_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#batch_disassociate_resource)
        """

    def delete_apps_list(
        self, **kwargs: Unpack[DeleteAppsListRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Permanently deletes an Firewall Manager applications list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/delete_apps_list.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#delete_apps_list)
        """

    def delete_notification_channel(self) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Firewall Manager association with the IAM role and the Amazon Simple
        Notification Service (SNS) topic that is used to record Firewall Manager SNS
        logs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/delete_notification_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#delete_notification_channel)
        """

    def delete_policy(
        self, **kwargs: Unpack[DeletePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Permanently deletes an Firewall Manager policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/delete_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#delete_policy)
        """

    def delete_protocols_list(
        self, **kwargs: Unpack[DeleteProtocolsListRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Permanently deletes an Firewall Manager protocols list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/delete_protocols_list.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#delete_protocols_list)
        """

    def delete_resource_set(
        self, **kwargs: Unpack[DeleteResourceSetRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified <a>ResourceSet</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/delete_resource_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#delete_resource_set)
        """

    def disassociate_admin_account(self) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates an Firewall Manager administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/disassociate_admin_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#disassociate_admin_account)
        """

    def disassociate_third_party_firewall(
        self, **kwargs: Unpack[DisassociateThirdPartyFirewallRequestRequestTypeDef]
    ) -> DisassociateThirdPartyFirewallResponseTypeDef:
        """
        Disassociates a Firewall Manager policy administrator from a third-party
        firewall tenant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/disassociate_third_party_firewall.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#disassociate_third_party_firewall)
        """

    def get_admin_account(self) -> GetAdminAccountResponseTypeDef:
        """
        Returns the Organizations account that is associated with Firewall Manager as
        the Firewall Manager default administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_admin_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_admin_account)
        """

    def get_admin_scope(
        self, **kwargs: Unpack[GetAdminScopeRequestRequestTypeDef]
    ) -> GetAdminScopeResponseTypeDef:
        """
        Returns information about the specified account's administrative scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_admin_scope.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_admin_scope)
        """

    def get_apps_list(
        self, **kwargs: Unpack[GetAppsListRequestRequestTypeDef]
    ) -> GetAppsListResponseTypeDef:
        """
        Returns information about the specified Firewall Manager applications list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_apps_list.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_apps_list)
        """

    def get_compliance_detail(
        self, **kwargs: Unpack[GetComplianceDetailRequestRequestTypeDef]
    ) -> GetComplianceDetailResponseTypeDef:
        """
        Returns detailed compliance information about the specified member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_compliance_detail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_compliance_detail)
        """

    def get_notification_channel(self) -> GetNotificationChannelResponseTypeDef:
        """
        Information about the Amazon Simple Notification Service (SNS) topic that is
        used to record Firewall Manager SNS logs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_notification_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_notification_channel)
        """

    def get_policy(
        self, **kwargs: Unpack[GetPolicyRequestRequestTypeDef]
    ) -> GetPolicyResponseTypeDef:
        """
        Returns information about the specified Firewall Manager policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_policy)
        """

    def get_protection_status(
        self, **kwargs: Unpack[GetProtectionStatusRequestRequestTypeDef]
    ) -> GetProtectionStatusResponseTypeDef:
        """
        If you created a Shield Advanced policy, returns policy-level attack summary
        information in the event of a potential DDoS attack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_protection_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_protection_status)
        """

    def get_protocols_list(
        self, **kwargs: Unpack[GetProtocolsListRequestRequestTypeDef]
    ) -> GetProtocolsListResponseTypeDef:
        """
        Returns information about the specified Firewall Manager protocols list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_protocols_list.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_protocols_list)
        """

    def get_resource_set(
        self, **kwargs: Unpack[GetResourceSetRequestRequestTypeDef]
    ) -> GetResourceSetResponseTypeDef:
        """
        Gets information about a specific resource set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_resource_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_resource_set)
        """

    def get_third_party_firewall_association_status(
        self, **kwargs: Unpack[GetThirdPartyFirewallAssociationStatusRequestRequestTypeDef]
    ) -> GetThirdPartyFirewallAssociationStatusResponseTypeDef:
        """
        The onboarding status of a Firewall Manager admin account to third-party
        firewall vendor tenant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_third_party_firewall_association_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_third_party_firewall_association_status)
        """

    def get_violation_details(
        self, **kwargs: Unpack[GetViolationDetailsRequestRequestTypeDef]
    ) -> GetViolationDetailsResponseTypeDef:
        """
        Retrieves violations for a resource based on the specified Firewall Manager
        policy and Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_violation_details.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_violation_details)
        """

    def list_admin_accounts_for_organization(
        self, **kwargs: Unpack[ListAdminAccountsForOrganizationRequestRequestTypeDef]
    ) -> ListAdminAccountsForOrganizationResponseTypeDef:
        """
        Returns a <code>AdminAccounts</code> object that lists the Firewall Manager
        administrators within the organization that are onboarded to Firewall Manager
        by <a>AssociateAdminAccount</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/list_admin_accounts_for_organization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#list_admin_accounts_for_organization)
        """

    def list_admins_managing_account(
        self, **kwargs: Unpack[ListAdminsManagingAccountRequestRequestTypeDef]
    ) -> ListAdminsManagingAccountResponseTypeDef:
        """
        Lists the accounts that are managing the specified Organizations member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/list_admins_managing_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#list_admins_managing_account)
        """

    def list_apps_lists(
        self, **kwargs: Unpack[ListAppsListsRequestRequestTypeDef]
    ) -> ListAppsListsResponseTypeDef:
        """
        Returns an array of <code>AppsListDataSummary</code> objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/list_apps_lists.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#list_apps_lists)
        """

    def list_compliance_status(
        self, **kwargs: Unpack[ListComplianceStatusRequestRequestTypeDef]
    ) -> ListComplianceStatusResponseTypeDef:
        """
        Returns an array of <code>PolicyComplianceStatus</code> objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/list_compliance_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#list_compliance_status)
        """

    def list_discovered_resources(
        self, **kwargs: Unpack[ListDiscoveredResourcesRequestRequestTypeDef]
    ) -> ListDiscoveredResourcesResponseTypeDef:
        """
        Returns an array of resources in the organization's accounts that are available
        to be associated with a resource set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/list_discovered_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#list_discovered_resources)
        """

    def list_member_accounts(
        self, **kwargs: Unpack[ListMemberAccountsRequestRequestTypeDef]
    ) -> ListMemberAccountsResponseTypeDef:
        """
        Returns a <code>MemberAccounts</code> object that lists the member accounts in
        the administrator's Amazon Web Services organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/list_member_accounts.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#list_member_accounts)
        """

    def list_policies(
        self, **kwargs: Unpack[ListPoliciesRequestRequestTypeDef]
    ) -> ListPoliciesResponseTypeDef:
        """
        Returns an array of <code>PolicySummary</code> objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/list_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#list_policies)
        """

    def list_protocols_lists(
        self, **kwargs: Unpack[ListProtocolsListsRequestRequestTypeDef]
    ) -> ListProtocolsListsResponseTypeDef:
        """
        Returns an array of <code>ProtocolsListDataSummary</code> objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/list_protocols_lists.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#list_protocols_lists)
        """

    def list_resource_set_resources(
        self, **kwargs: Unpack[ListResourceSetResourcesRequestRequestTypeDef]
    ) -> ListResourceSetResourcesResponseTypeDef:
        """
        Returns an array of resources that are currently associated to a resource set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/list_resource_set_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#list_resource_set_resources)
        """

    def list_resource_sets(
        self, **kwargs: Unpack[ListResourceSetsRequestRequestTypeDef]
    ) -> ListResourceSetsResponseTypeDef:
        """
        Returns an array of <code>ResourceSetSummary</code> objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/list_resource_sets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#list_resource_sets)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the list of tags for the specified Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#list_tags_for_resource)
        """

    def list_third_party_firewall_firewall_policies(
        self, **kwargs: Unpack[ListThirdPartyFirewallFirewallPoliciesRequestRequestTypeDef]
    ) -> ListThirdPartyFirewallFirewallPoliciesResponseTypeDef:
        """
        Retrieves a list of all of the third-party firewall policies that are
        associated with the third-party firewall administrator's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/list_third_party_firewall_firewall_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#list_third_party_firewall_firewall_policies)
        """

    def put_admin_account(
        self, **kwargs: Unpack[PutAdminAccountRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates an Firewall Manager administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/put_admin_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#put_admin_account)
        """

    def put_apps_list(
        self, **kwargs: Unpack[PutAppsListRequestRequestTypeDef]
    ) -> PutAppsListResponseTypeDef:
        """
        Creates an Firewall Manager applications list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/put_apps_list.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#put_apps_list)
        """

    def put_notification_channel(
        self, **kwargs: Unpack[PutNotificationChannelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Designates the IAM role and Amazon Simple Notification Service (SNS) topic that
        Firewall Manager uses to record SNS logs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/put_notification_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#put_notification_channel)
        """

    def put_policy(
        self, **kwargs: Unpack[PutPolicyRequestRequestTypeDef]
    ) -> PutPolicyResponseTypeDef:
        """
        Creates an Firewall Manager policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/put_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#put_policy)
        """

    def put_protocols_list(
        self, **kwargs: Unpack[PutProtocolsListRequestRequestTypeDef]
    ) -> PutProtocolsListResponseTypeDef:
        """
        Creates an Firewall Manager protocols list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/put_protocols_list.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#put_protocols_list)
        """

    def put_resource_set(
        self, **kwargs: Unpack[PutResourceSetRequestRequestTypeDef]
    ) -> PutResourceSetResponseTypeDef:
        """
        Creates the resource set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/put_resource_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#put_resource_set)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to an Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from an Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_admin_accounts_for_organization"]
    ) -> ListAdminAccountsForOrganizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_admins_managing_account"]
    ) -> ListAdminsManagingAccountPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_apps_lists"]) -> ListAppsListsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_compliance_status"]
    ) -> ListComplianceStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_member_accounts"]
    ) -> ListMemberAccountsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_policies"]) -> ListPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_protocols_lists"]
    ) -> ListProtocolsListsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_third_party_firewall_firewall_policies"]
    ) -> ListThirdPartyFirewallFirewallPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_fms/client/#get_paginator)
        """
