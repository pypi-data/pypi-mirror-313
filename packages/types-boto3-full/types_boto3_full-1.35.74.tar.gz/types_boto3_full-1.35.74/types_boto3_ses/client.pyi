"""
Type annotations for ses service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_ses.client import SESClient

    session = Session()
    client: SESClient = session.client("ses")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListConfigurationSetsPaginator,
    ListCustomVerificationEmailTemplatesPaginator,
    ListIdentitiesPaginator,
    ListReceiptRuleSetsPaginator,
    ListTemplatesPaginator,
)
from .type_defs import (
    CloneReceiptRuleSetRequestRequestTypeDef,
    CreateConfigurationSetEventDestinationRequestRequestTypeDef,
    CreateConfigurationSetRequestRequestTypeDef,
    CreateConfigurationSetTrackingOptionsRequestRequestTypeDef,
    CreateCustomVerificationEmailTemplateRequestRequestTypeDef,
    CreateReceiptFilterRequestRequestTypeDef,
    CreateReceiptRuleRequestRequestTypeDef,
    CreateReceiptRuleSetRequestRequestTypeDef,
    CreateTemplateRequestRequestTypeDef,
    DeleteConfigurationSetEventDestinationRequestRequestTypeDef,
    DeleteConfigurationSetRequestRequestTypeDef,
    DeleteConfigurationSetTrackingOptionsRequestRequestTypeDef,
    DeleteCustomVerificationEmailTemplateRequestRequestTypeDef,
    DeleteIdentityPolicyRequestRequestTypeDef,
    DeleteIdentityRequestRequestTypeDef,
    DeleteReceiptFilterRequestRequestTypeDef,
    DeleteReceiptRuleRequestRequestTypeDef,
    DeleteReceiptRuleSetRequestRequestTypeDef,
    DeleteTemplateRequestRequestTypeDef,
    DeleteVerifiedEmailAddressRequestRequestTypeDef,
    DescribeActiveReceiptRuleSetResponseTypeDef,
    DescribeConfigurationSetRequestRequestTypeDef,
    DescribeConfigurationSetResponseTypeDef,
    DescribeReceiptRuleRequestRequestTypeDef,
    DescribeReceiptRuleResponseTypeDef,
    DescribeReceiptRuleSetRequestRequestTypeDef,
    DescribeReceiptRuleSetResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAccountSendingEnabledResponseTypeDef,
    GetCustomVerificationEmailTemplateRequestRequestTypeDef,
    GetCustomVerificationEmailTemplateResponseTypeDef,
    GetIdentityDkimAttributesRequestRequestTypeDef,
    GetIdentityDkimAttributesResponseTypeDef,
    GetIdentityMailFromDomainAttributesRequestRequestTypeDef,
    GetIdentityMailFromDomainAttributesResponseTypeDef,
    GetIdentityNotificationAttributesRequestRequestTypeDef,
    GetIdentityNotificationAttributesResponseTypeDef,
    GetIdentityPoliciesRequestRequestTypeDef,
    GetIdentityPoliciesResponseTypeDef,
    GetIdentityVerificationAttributesRequestRequestTypeDef,
    GetIdentityVerificationAttributesResponseTypeDef,
    GetSendQuotaResponseTypeDef,
    GetSendStatisticsResponseTypeDef,
    GetTemplateRequestRequestTypeDef,
    GetTemplateResponseTypeDef,
    ListConfigurationSetsRequestRequestTypeDef,
    ListConfigurationSetsResponseTypeDef,
    ListCustomVerificationEmailTemplatesRequestRequestTypeDef,
    ListCustomVerificationEmailTemplatesResponseTypeDef,
    ListIdentitiesRequestRequestTypeDef,
    ListIdentitiesResponseTypeDef,
    ListIdentityPoliciesRequestRequestTypeDef,
    ListIdentityPoliciesResponseTypeDef,
    ListReceiptFiltersResponseTypeDef,
    ListReceiptRuleSetsRequestRequestTypeDef,
    ListReceiptRuleSetsResponseTypeDef,
    ListTemplatesRequestRequestTypeDef,
    ListTemplatesResponseTypeDef,
    ListVerifiedEmailAddressesResponseTypeDef,
    PutConfigurationSetDeliveryOptionsRequestRequestTypeDef,
    PutIdentityPolicyRequestRequestTypeDef,
    ReorderReceiptRuleSetRequestRequestTypeDef,
    SendBounceRequestRequestTypeDef,
    SendBounceResponseTypeDef,
    SendBulkTemplatedEmailRequestRequestTypeDef,
    SendBulkTemplatedEmailResponseTypeDef,
    SendCustomVerificationEmailRequestRequestTypeDef,
    SendCustomVerificationEmailResponseTypeDef,
    SendEmailRequestRequestTypeDef,
    SendEmailResponseTypeDef,
    SendRawEmailRequestRequestTypeDef,
    SendRawEmailResponseTypeDef,
    SendTemplatedEmailRequestRequestTypeDef,
    SendTemplatedEmailResponseTypeDef,
    SetActiveReceiptRuleSetRequestRequestTypeDef,
    SetIdentityDkimEnabledRequestRequestTypeDef,
    SetIdentityFeedbackForwardingEnabledRequestRequestTypeDef,
    SetIdentityHeadersInNotificationsEnabledRequestRequestTypeDef,
    SetIdentityMailFromDomainRequestRequestTypeDef,
    SetIdentityNotificationTopicRequestRequestTypeDef,
    SetReceiptRulePositionRequestRequestTypeDef,
    TestRenderTemplateRequestRequestTypeDef,
    TestRenderTemplateResponseTypeDef,
    UpdateAccountSendingEnabledRequestRequestTypeDef,
    UpdateConfigurationSetEventDestinationRequestRequestTypeDef,
    UpdateConfigurationSetReputationMetricsEnabledRequestRequestTypeDef,
    UpdateConfigurationSetSendingEnabledRequestRequestTypeDef,
    UpdateConfigurationSetTrackingOptionsRequestRequestTypeDef,
    UpdateCustomVerificationEmailTemplateRequestRequestTypeDef,
    UpdateReceiptRuleRequestRequestTypeDef,
    UpdateTemplateRequestRequestTypeDef,
    VerifyDomainDkimRequestRequestTypeDef,
    VerifyDomainDkimResponseTypeDef,
    VerifyDomainIdentityRequestRequestTypeDef,
    VerifyDomainIdentityResponseTypeDef,
    VerifyEmailAddressRequestRequestTypeDef,
    VerifyEmailIdentityRequestRequestTypeDef,
)
from .waiter import IdentityExistsWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("SESClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccountSendingPausedException: Type[BotocoreClientError]
    AlreadyExistsException: Type[BotocoreClientError]
    CannotDeleteException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConfigurationSetAlreadyExistsException: Type[BotocoreClientError]
    ConfigurationSetDoesNotExistException: Type[BotocoreClientError]
    ConfigurationSetSendingPausedException: Type[BotocoreClientError]
    CustomVerificationEmailInvalidContentException: Type[BotocoreClientError]
    CustomVerificationEmailTemplateAlreadyExistsException: Type[BotocoreClientError]
    CustomVerificationEmailTemplateDoesNotExistException: Type[BotocoreClientError]
    EventDestinationAlreadyExistsException: Type[BotocoreClientError]
    EventDestinationDoesNotExistException: Type[BotocoreClientError]
    FromEmailAddressNotVerifiedException: Type[BotocoreClientError]
    InvalidCloudWatchDestinationException: Type[BotocoreClientError]
    InvalidConfigurationSetException: Type[BotocoreClientError]
    InvalidDeliveryOptionsException: Type[BotocoreClientError]
    InvalidFirehoseDestinationException: Type[BotocoreClientError]
    InvalidLambdaFunctionException: Type[BotocoreClientError]
    InvalidPolicyException: Type[BotocoreClientError]
    InvalidRenderingParameterException: Type[BotocoreClientError]
    InvalidS3ConfigurationException: Type[BotocoreClientError]
    InvalidSNSDestinationException: Type[BotocoreClientError]
    InvalidSnsTopicException: Type[BotocoreClientError]
    InvalidTemplateException: Type[BotocoreClientError]
    InvalidTrackingOptionsException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MailFromDomainNotVerifiedException: Type[BotocoreClientError]
    MessageRejected: Type[BotocoreClientError]
    MissingRenderingAttributeException: Type[BotocoreClientError]
    ProductionAccessNotGrantedException: Type[BotocoreClientError]
    RuleDoesNotExistException: Type[BotocoreClientError]
    RuleSetDoesNotExistException: Type[BotocoreClientError]
    TemplateDoesNotExistException: Type[BotocoreClientError]
    TrackingOptionsAlreadyExistsException: Type[BotocoreClientError]
    TrackingOptionsDoesNotExistException: Type[BotocoreClientError]

class SESClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses.html#SES.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SESClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses.html#SES.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#close)
        """

    def clone_receipt_rule_set(
        self, **kwargs: Unpack[CloneReceiptRuleSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a receipt rule set by cloning an existing one.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/clone_receipt_rule_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#clone_receipt_rule_set)
        """

    def create_configuration_set(
        self, **kwargs: Unpack[CreateConfigurationSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/create_configuration_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#create_configuration_set)
        """

    def create_configuration_set_event_destination(
        self, **kwargs: Unpack[CreateConfigurationSetEventDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a configuration set event destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/create_configuration_set_event_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#create_configuration_set_event_destination)
        """

    def create_configuration_set_tracking_options(
        self, **kwargs: Unpack[CreateConfigurationSetTrackingOptionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates an association between a configuration set and a custom domain for open
        and click event tracking.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/create_configuration_set_tracking_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#create_configuration_set_tracking_options)
        """

    def create_custom_verification_email_template(
        self, **kwargs: Unpack[CreateCustomVerificationEmailTemplateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a new custom verification email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/create_custom_verification_email_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#create_custom_verification_email_template)
        """

    def create_receipt_filter(
        self, **kwargs: Unpack[CreateReceiptFilterRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a new IP address filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/create_receipt_filter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#create_receipt_filter)
        """

    def create_receipt_rule(
        self, **kwargs: Unpack[CreateReceiptRuleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a receipt rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/create_receipt_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#create_receipt_rule)
        """

    def create_receipt_rule_set(
        self, **kwargs: Unpack[CreateReceiptRuleSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates an empty receipt rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/create_receipt_rule_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#create_receipt_rule_set)
        """

    def create_template(
        self, **kwargs: Unpack[CreateTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates an email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/create_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#create_template)
        """

    def delete_configuration_set(
        self, **kwargs: Unpack[DeleteConfigurationSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/delete_configuration_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#delete_configuration_set)
        """

    def delete_configuration_set_event_destination(
        self, **kwargs: Unpack[DeleteConfigurationSetEventDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a configuration set event destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/delete_configuration_set_event_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#delete_configuration_set_event_destination)
        """

    def delete_configuration_set_tracking_options(
        self, **kwargs: Unpack[DeleteConfigurationSetTrackingOptionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an association between a configuration set and a custom domain for open
        and click event tracking.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/delete_configuration_set_tracking_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#delete_configuration_set_tracking_options)
        """

    def delete_custom_verification_email_template(
        self, **kwargs: Unpack[DeleteCustomVerificationEmailTemplateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an existing custom verification email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/delete_custom_verification_email_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#delete_custom_verification_email_template)
        """

    def delete_identity(
        self, **kwargs: Unpack[DeleteIdentityRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified identity (an email address or a domain) from the list of
        verified identities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/delete_identity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#delete_identity)
        """

    def delete_identity_policy(
        self, **kwargs: Unpack[DeleteIdentityPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified sending authorization policy for the given identity (an
        email address or a domain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/delete_identity_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#delete_identity_policy)
        """

    def delete_receipt_filter(
        self, **kwargs: Unpack[DeleteReceiptFilterRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified IP address filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/delete_receipt_filter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#delete_receipt_filter)
        """

    def delete_receipt_rule(
        self, **kwargs: Unpack[DeleteReceiptRuleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified receipt rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/delete_receipt_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#delete_receipt_rule)
        """

    def delete_receipt_rule_set(
        self, **kwargs: Unpack[DeleteReceiptRuleSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified receipt rule set and all of the receipt rules it contains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/delete_receipt_rule_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#delete_receipt_rule_set)
        """

    def delete_template(
        self, **kwargs: Unpack[DeleteTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/delete_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#delete_template)
        """

    def delete_verified_email_address(
        self, **kwargs: Unpack[DeleteVerifiedEmailAddressRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/delete_verified_email_address.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#delete_verified_email_address)
        """

    def describe_active_receipt_rule_set(self) -> DescribeActiveReceiptRuleSetResponseTypeDef:
        """
        Returns the metadata and receipt rules for the receipt rule set that is
        currently active.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/describe_active_receipt_rule_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#describe_active_receipt_rule_set)
        """

    def describe_configuration_set(
        self, **kwargs: Unpack[DescribeConfigurationSetRequestRequestTypeDef]
    ) -> DescribeConfigurationSetResponseTypeDef:
        """
        Returns the details of the specified configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/describe_configuration_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#describe_configuration_set)
        """

    def describe_receipt_rule(
        self, **kwargs: Unpack[DescribeReceiptRuleRequestRequestTypeDef]
    ) -> DescribeReceiptRuleResponseTypeDef:
        """
        Returns the details of the specified receipt rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/describe_receipt_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#describe_receipt_rule)
        """

    def describe_receipt_rule_set(
        self, **kwargs: Unpack[DescribeReceiptRuleSetRequestRequestTypeDef]
    ) -> DescribeReceiptRuleSetResponseTypeDef:
        """
        Returns the details of the specified receipt rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/describe_receipt_rule_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#describe_receipt_rule_set)
        """

    def get_account_sending_enabled(self) -> GetAccountSendingEnabledResponseTypeDef:
        """
        Returns the email sending status of the Amazon SES account for the current
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/get_account_sending_enabled.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#get_account_sending_enabled)
        """

    def get_custom_verification_email_template(
        self, **kwargs: Unpack[GetCustomVerificationEmailTemplateRequestRequestTypeDef]
    ) -> GetCustomVerificationEmailTemplateResponseTypeDef:
        """
        Returns the custom email verification template for the template name you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/get_custom_verification_email_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#get_custom_verification_email_template)
        """

    def get_identity_dkim_attributes(
        self, **kwargs: Unpack[GetIdentityDkimAttributesRequestRequestTypeDef]
    ) -> GetIdentityDkimAttributesResponseTypeDef:
        """
        Returns the current status of Easy DKIM signing for an entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/get_identity_dkim_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#get_identity_dkim_attributes)
        """

    def get_identity_mail_from_domain_attributes(
        self, **kwargs: Unpack[GetIdentityMailFromDomainAttributesRequestRequestTypeDef]
    ) -> GetIdentityMailFromDomainAttributesResponseTypeDef:
        """
        Returns the custom MAIL FROM attributes for a list of identities (email
        addresses : domains).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/get_identity_mail_from_domain_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#get_identity_mail_from_domain_attributes)
        """

    def get_identity_notification_attributes(
        self, **kwargs: Unpack[GetIdentityNotificationAttributesRequestRequestTypeDef]
    ) -> GetIdentityNotificationAttributesResponseTypeDef:
        """
        Given a list of verified identities (email addresses and/or domains), returns a
        structure describing identity notification attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/get_identity_notification_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#get_identity_notification_attributes)
        """

    def get_identity_policies(
        self, **kwargs: Unpack[GetIdentityPoliciesRequestRequestTypeDef]
    ) -> GetIdentityPoliciesResponseTypeDef:
        """
        Returns the requested sending authorization policies for the given identity (an
        email address or a domain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/get_identity_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#get_identity_policies)
        """

    def get_identity_verification_attributes(
        self, **kwargs: Unpack[GetIdentityVerificationAttributesRequestRequestTypeDef]
    ) -> GetIdentityVerificationAttributesResponseTypeDef:
        """
        Given a list of identities (email addresses and/or domains), returns the
        verification status and (for domain identities) the verification token for each
        identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/get_identity_verification_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#get_identity_verification_attributes)
        """

    def get_send_quota(self) -> GetSendQuotaResponseTypeDef:
        """
        Provides the sending limits for the Amazon SES account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/get_send_quota.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#get_send_quota)
        """

    def get_send_statistics(self) -> GetSendStatisticsResponseTypeDef:
        """
        Provides sending statistics for the current Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/get_send_statistics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#get_send_statistics)
        """

    def get_template(
        self, **kwargs: Unpack[GetTemplateRequestRequestTypeDef]
    ) -> GetTemplateResponseTypeDef:
        """
        Displays the template object (which includes the Subject line, HTML part and
        text part) for the template you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/get_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#get_template)
        """

    def list_configuration_sets(
        self, **kwargs: Unpack[ListConfigurationSetsRequestRequestTypeDef]
    ) -> ListConfigurationSetsResponseTypeDef:
        """
        Provides a list of the configuration sets associated with your Amazon SES
        account in the current Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/list_configuration_sets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#list_configuration_sets)
        """

    def list_custom_verification_email_templates(
        self, **kwargs: Unpack[ListCustomVerificationEmailTemplatesRequestRequestTypeDef]
    ) -> ListCustomVerificationEmailTemplatesResponseTypeDef:
        """
        Lists the existing custom verification email templates for your account in the
        current Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/list_custom_verification_email_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#list_custom_verification_email_templates)
        """

    def list_identities(
        self, **kwargs: Unpack[ListIdentitiesRequestRequestTypeDef]
    ) -> ListIdentitiesResponseTypeDef:
        """
        Returns a list containing all of the identities (email addresses and domains)
        for your Amazon Web Services account in the current Amazon Web Services Region,
        regardless of verification status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/list_identities.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#list_identities)
        """

    def list_identity_policies(
        self, **kwargs: Unpack[ListIdentityPoliciesRequestRequestTypeDef]
    ) -> ListIdentityPoliciesResponseTypeDef:
        """
        Returns a list of sending authorization policies that are attached to the given
        identity (an email address or a domain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/list_identity_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#list_identity_policies)
        """

    def list_receipt_filters(self) -> ListReceiptFiltersResponseTypeDef:
        """
        Lists the IP address filters associated with your Amazon Web Services account
        in the current Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/list_receipt_filters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#list_receipt_filters)
        """

    def list_receipt_rule_sets(
        self, **kwargs: Unpack[ListReceiptRuleSetsRequestRequestTypeDef]
    ) -> ListReceiptRuleSetsResponseTypeDef:
        """
        Lists the receipt rule sets that exist under your Amazon Web Services account
        in the current Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/list_receipt_rule_sets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#list_receipt_rule_sets)
        """

    def list_templates(
        self, **kwargs: Unpack[ListTemplatesRequestRequestTypeDef]
    ) -> ListTemplatesResponseTypeDef:
        """
        Lists the email templates present in your Amazon SES account in the current
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/list_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#list_templates)
        """

    def list_verified_email_addresses(self) -> ListVerifiedEmailAddressesResponseTypeDef:
        """
        Deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/list_verified_email_addresses.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#list_verified_email_addresses)
        """

    def put_configuration_set_delivery_options(
        self, **kwargs: Unpack[PutConfigurationSetDeliveryOptionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds or updates the delivery options for a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/put_configuration_set_delivery_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#put_configuration_set_delivery_options)
        """

    def put_identity_policy(
        self, **kwargs: Unpack[PutIdentityPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds or updates a sending authorization policy for the specified identity (an
        email address or a domain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/put_identity_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#put_identity_policy)
        """

    def reorder_receipt_rule_set(
        self, **kwargs: Unpack[ReorderReceiptRuleSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Reorders the receipt rules within a receipt rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/reorder_receipt_rule_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#reorder_receipt_rule_set)
        """

    def send_bounce(
        self, **kwargs: Unpack[SendBounceRequestRequestTypeDef]
    ) -> SendBounceResponseTypeDef:
        """
        Generates and sends a bounce message to the sender of an email you received
        through Amazon SES.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/send_bounce.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#send_bounce)
        """

    def send_bulk_templated_email(
        self, **kwargs: Unpack[SendBulkTemplatedEmailRequestRequestTypeDef]
    ) -> SendBulkTemplatedEmailResponseTypeDef:
        """
        Composes an email message to multiple destinations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/send_bulk_templated_email.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#send_bulk_templated_email)
        """

    def send_custom_verification_email(
        self, **kwargs: Unpack[SendCustomVerificationEmailRequestRequestTypeDef]
    ) -> SendCustomVerificationEmailResponseTypeDef:
        """
        Adds an email address to the list of identities for your Amazon SES account in
        the current Amazon Web Services Region and attempts to verify it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/send_custom_verification_email.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#send_custom_verification_email)
        """

    def send_email(
        self, **kwargs: Unpack[SendEmailRequestRequestTypeDef]
    ) -> SendEmailResponseTypeDef:
        """
        Composes an email message and immediately queues it for sending.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/send_email.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#send_email)
        """

    def send_raw_email(
        self, **kwargs: Unpack[SendRawEmailRequestRequestTypeDef]
    ) -> SendRawEmailResponseTypeDef:
        """
        Composes an email message and immediately queues it for sending.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/send_raw_email.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#send_raw_email)
        """

    def send_templated_email(
        self, **kwargs: Unpack[SendTemplatedEmailRequestRequestTypeDef]
    ) -> SendTemplatedEmailResponseTypeDef:
        """
        Composes an email message using an email template and immediately queues it for
        sending.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/send_templated_email.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#send_templated_email)
        """

    def set_active_receipt_rule_set(
        self, **kwargs: Unpack[SetActiveReceiptRuleSetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets the specified receipt rule set as the active receipt rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/set_active_receipt_rule_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#set_active_receipt_rule_set)
        """

    def set_identity_dkim_enabled(
        self, **kwargs: Unpack[SetIdentityDkimEnabledRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enables or disables Easy DKIM signing of email sent from an identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/set_identity_dkim_enabled.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#set_identity_dkim_enabled)
        """

    def set_identity_feedback_forwarding_enabled(
        self, **kwargs: Unpack[SetIdentityFeedbackForwardingEnabledRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Given an identity (an email address or a domain), enables or disables whether
        Amazon SES forwards bounce and complaint notifications as email.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/set_identity_feedback_forwarding_enabled.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#set_identity_feedback_forwarding_enabled)
        """

    def set_identity_headers_in_notifications_enabled(
        self, **kwargs: Unpack[SetIdentityHeadersInNotificationsEnabledRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Given an identity (an email address or a domain), sets whether Amazon SES
        includes the original email headers in the Amazon Simple Notification Service
        (Amazon SNS) notifications of a specified type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/set_identity_headers_in_notifications_enabled.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#set_identity_headers_in_notifications_enabled)
        """

    def set_identity_mail_from_domain(
        self, **kwargs: Unpack[SetIdentityMailFromDomainRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enables or disables the custom MAIL FROM domain setup for a verified identity
        (an email address or a domain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/set_identity_mail_from_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#set_identity_mail_from_domain)
        """

    def set_identity_notification_topic(
        self, **kwargs: Unpack[SetIdentityNotificationTopicRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets an Amazon Simple Notification Service (Amazon SNS) topic to use when
        delivering notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/set_identity_notification_topic.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#set_identity_notification_topic)
        """

    def set_receipt_rule_position(
        self, **kwargs: Unpack[SetReceiptRulePositionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets the position of the specified receipt rule in the receipt rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/set_receipt_rule_position.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#set_receipt_rule_position)
        """

    def test_render_template(
        self, **kwargs: Unpack[TestRenderTemplateRequestRequestTypeDef]
    ) -> TestRenderTemplateResponseTypeDef:
        """
        Creates a preview of the MIME content of an email when provided with a template
        and a set of replacement data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/test_render_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#test_render_template)
        """

    def update_account_sending_enabled(
        self, **kwargs: Unpack[UpdateAccountSendingEnabledRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables or disables email sending across your entire Amazon SES account in the
        current Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/update_account_sending_enabled.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#update_account_sending_enabled)
        """

    def update_configuration_set_event_destination(
        self, **kwargs: Unpack[UpdateConfigurationSetEventDestinationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the event destination of a configuration set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/update_configuration_set_event_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#update_configuration_set_event_destination)
        """

    def update_configuration_set_reputation_metrics_enabled(
        self, **kwargs: Unpack[UpdateConfigurationSetReputationMetricsEnabledRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables or disables the publishing of reputation metrics for emails sent using
        a specific configuration set in a given Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/update_configuration_set_reputation_metrics_enabled.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#update_configuration_set_reputation_metrics_enabled)
        """

    def update_configuration_set_sending_enabled(
        self, **kwargs: Unpack[UpdateConfigurationSetSendingEnabledRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables or disables email sending for messages sent using a specific
        configuration set in a given Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/update_configuration_set_sending_enabled.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#update_configuration_set_sending_enabled)
        """

    def update_configuration_set_tracking_options(
        self, **kwargs: Unpack[UpdateConfigurationSetTrackingOptionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Modifies an association between a configuration set and a custom domain for
        open and click event tracking.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/update_configuration_set_tracking_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#update_configuration_set_tracking_options)
        """

    def update_custom_verification_email_template(
        self, **kwargs: Unpack[UpdateCustomVerificationEmailTemplateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an existing custom verification email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/update_custom_verification_email_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#update_custom_verification_email_template)
        """

    def update_receipt_rule(
        self, **kwargs: Unpack[UpdateReceiptRuleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a receipt rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/update_receipt_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#update_receipt_rule)
        """

    def update_template(
        self, **kwargs: Unpack[UpdateTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an email template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/update_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#update_template)
        """

    def verify_domain_dkim(
        self, **kwargs: Unpack[VerifyDomainDkimRequestRequestTypeDef]
    ) -> VerifyDomainDkimResponseTypeDef:
        """
        Returns a set of DKIM tokens for a domain identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/verify_domain_dkim.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#verify_domain_dkim)
        """

    def verify_domain_identity(
        self, **kwargs: Unpack[VerifyDomainIdentityRequestRequestTypeDef]
    ) -> VerifyDomainIdentityResponseTypeDef:
        """
        Adds a domain to the list of identities for your Amazon SES account in the
        current Amazon Web Services Region and attempts to verify it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/verify_domain_identity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#verify_domain_identity)
        """

    def verify_email_address(
        self, **kwargs: Unpack[VerifyEmailAddressRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/verify_email_address.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#verify_email_address)
        """

    def verify_email_identity(
        self, **kwargs: Unpack[VerifyEmailIdentityRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds an email address to the list of identities for your Amazon SES account in
        the current Amazon Web Services Region and attempts to verify it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/verify_email_identity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#verify_email_identity)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configuration_sets"]
    ) -> ListConfigurationSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_verification_email_templates"]
    ) -> ListCustomVerificationEmailTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_identities"]) -> ListIdentitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_receipt_rule_sets"]
    ) -> ListReceiptRuleSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_templates"]) -> ListTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#get_paginator)
        """

    def get_waiter(self, waiter_name: Literal["identity_exists"]) -> IdentityExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ses/client/#get_waiter)
        """
