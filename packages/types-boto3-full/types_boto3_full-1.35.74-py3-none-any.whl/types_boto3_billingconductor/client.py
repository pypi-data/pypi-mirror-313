"""
Type annotations for billingconductor service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_billingconductor.client import BillingConductorClient

    session = Session()
    client: BillingConductorClient = session.client("billingconductor")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAccountAssociationsPaginator,
    ListBillingGroupCostReportsPaginator,
    ListBillingGroupsPaginator,
    ListCustomLineItemsPaginator,
    ListCustomLineItemVersionsPaginator,
    ListPricingPlansAssociatedWithPricingRulePaginator,
    ListPricingPlansPaginator,
    ListPricingRulesAssociatedToPricingPlanPaginator,
    ListPricingRulesPaginator,
    ListResourcesAssociatedToCustomLineItemPaginator,
)
from .type_defs import (
    AssociateAccountsInputRequestTypeDef,
    AssociateAccountsOutputTypeDef,
    AssociatePricingRulesInputRequestTypeDef,
    AssociatePricingRulesOutputTypeDef,
    BatchAssociateResourcesToCustomLineItemInputRequestTypeDef,
    BatchAssociateResourcesToCustomLineItemOutputTypeDef,
    BatchDisassociateResourcesFromCustomLineItemInputRequestTypeDef,
    BatchDisassociateResourcesFromCustomLineItemOutputTypeDef,
    CreateBillingGroupInputRequestTypeDef,
    CreateBillingGroupOutputTypeDef,
    CreateCustomLineItemInputRequestTypeDef,
    CreateCustomLineItemOutputTypeDef,
    CreatePricingPlanInputRequestTypeDef,
    CreatePricingPlanOutputTypeDef,
    CreatePricingRuleInputRequestTypeDef,
    CreatePricingRuleOutputTypeDef,
    DeleteBillingGroupInputRequestTypeDef,
    DeleteBillingGroupOutputTypeDef,
    DeleteCustomLineItemInputRequestTypeDef,
    DeleteCustomLineItemOutputTypeDef,
    DeletePricingPlanInputRequestTypeDef,
    DeletePricingPlanOutputTypeDef,
    DeletePricingRuleInputRequestTypeDef,
    DeletePricingRuleOutputTypeDef,
    DisassociateAccountsInputRequestTypeDef,
    DisassociateAccountsOutputTypeDef,
    DisassociatePricingRulesInputRequestTypeDef,
    DisassociatePricingRulesOutputTypeDef,
    GetBillingGroupCostReportInputRequestTypeDef,
    GetBillingGroupCostReportOutputTypeDef,
    ListAccountAssociationsInputRequestTypeDef,
    ListAccountAssociationsOutputTypeDef,
    ListBillingGroupCostReportsInputRequestTypeDef,
    ListBillingGroupCostReportsOutputTypeDef,
    ListBillingGroupsInputRequestTypeDef,
    ListBillingGroupsOutputTypeDef,
    ListCustomLineItemsInputRequestTypeDef,
    ListCustomLineItemsOutputTypeDef,
    ListCustomLineItemVersionsInputRequestTypeDef,
    ListCustomLineItemVersionsOutputTypeDef,
    ListPricingPlansAssociatedWithPricingRuleInputRequestTypeDef,
    ListPricingPlansAssociatedWithPricingRuleOutputTypeDef,
    ListPricingPlansInputRequestTypeDef,
    ListPricingPlansOutputTypeDef,
    ListPricingRulesAssociatedToPricingPlanInputRequestTypeDef,
    ListPricingRulesAssociatedToPricingPlanOutputTypeDef,
    ListPricingRulesInputRequestTypeDef,
    ListPricingRulesOutputTypeDef,
    ListResourcesAssociatedToCustomLineItemInputRequestTypeDef,
    ListResourcesAssociatedToCustomLineItemOutputTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateBillingGroupInputRequestTypeDef,
    UpdateBillingGroupOutputTypeDef,
    UpdateCustomLineItemInputRequestTypeDef,
    UpdateCustomLineItemOutputTypeDef,
    UpdatePricingPlanInputRequestTypeDef,
    UpdatePricingPlanOutputTypeDef,
    UpdatePricingRuleInputRequestTypeDef,
    UpdatePricingRuleOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("BillingConductorClient",)


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
    ServiceLimitExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class BillingConductorClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BillingConductorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#close)
        """

    def associate_accounts(
        self, **kwargs: Unpack[AssociateAccountsInputRequestTypeDef]
    ) -> AssociateAccountsOutputTypeDef:
        """
        Connects an array of account IDs in a consolidated billing family to a
        predefined billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/associate_accounts.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#associate_accounts)
        """

    def associate_pricing_rules(
        self, **kwargs: Unpack[AssociatePricingRulesInputRequestTypeDef]
    ) -> AssociatePricingRulesOutputTypeDef:
        """
        Connects an array of <code>PricingRuleArns</code> to a defined
        <code>PricingPlan</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/associate_pricing_rules.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#associate_pricing_rules)
        """

    def batch_associate_resources_to_custom_line_item(
        self, **kwargs: Unpack[BatchAssociateResourcesToCustomLineItemInputRequestTypeDef]
    ) -> BatchAssociateResourcesToCustomLineItemOutputTypeDef:
        """
        Associates a batch of resources to a percentage custom line item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/batch_associate_resources_to_custom_line_item.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#batch_associate_resources_to_custom_line_item)
        """

    def batch_disassociate_resources_from_custom_line_item(
        self, **kwargs: Unpack[BatchDisassociateResourcesFromCustomLineItemInputRequestTypeDef]
    ) -> BatchDisassociateResourcesFromCustomLineItemOutputTypeDef:
        """
        Disassociates a batch of resources from a percentage custom line item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/batch_disassociate_resources_from_custom_line_item.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#batch_disassociate_resources_from_custom_line_item)
        """

    def create_billing_group(
        self, **kwargs: Unpack[CreateBillingGroupInputRequestTypeDef]
    ) -> CreateBillingGroupOutputTypeDef:
        """
        Creates a billing group that resembles a consolidated billing family that
        Amazon Web Services charges, based off of the predefined pricing plan
        computation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/create_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#create_billing_group)
        """

    def create_custom_line_item(
        self, **kwargs: Unpack[CreateCustomLineItemInputRequestTypeDef]
    ) -> CreateCustomLineItemOutputTypeDef:
        """
        Creates a custom line item that can be used to create a one-time fixed charge
        that can be applied to a single billing group for the current or previous
        billing period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/create_custom_line_item.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#create_custom_line_item)
        """

    def create_pricing_plan(
        self, **kwargs: Unpack[CreatePricingPlanInputRequestTypeDef]
    ) -> CreatePricingPlanOutputTypeDef:
        """
        Creates a pricing plan that is used for computing Amazon Web Services charges
        for billing groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/create_pricing_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#create_pricing_plan)
        """

    def create_pricing_rule(
        self, **kwargs: Unpack[CreatePricingRuleInputRequestTypeDef]
    ) -> CreatePricingRuleOutputTypeDef:
        """
        Creates a pricing rule can be associated to a pricing plan, or a set of pricing
        plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/create_pricing_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#create_pricing_rule)
        """

    def delete_billing_group(
        self, **kwargs: Unpack[DeleteBillingGroupInputRequestTypeDef]
    ) -> DeleteBillingGroupOutputTypeDef:
        """
        Deletes a billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/delete_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#delete_billing_group)
        """

    def delete_custom_line_item(
        self, **kwargs: Unpack[DeleteCustomLineItemInputRequestTypeDef]
    ) -> DeleteCustomLineItemOutputTypeDef:
        """
        Deletes the custom line item identified by the given ARN in the current, or
        previous billing period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/delete_custom_line_item.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#delete_custom_line_item)
        """

    def delete_pricing_plan(
        self, **kwargs: Unpack[DeletePricingPlanInputRequestTypeDef]
    ) -> DeletePricingPlanOutputTypeDef:
        """
        Deletes a pricing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/delete_pricing_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#delete_pricing_plan)
        """

    def delete_pricing_rule(
        self, **kwargs: Unpack[DeletePricingRuleInputRequestTypeDef]
    ) -> DeletePricingRuleOutputTypeDef:
        """
        Deletes the pricing rule that's identified by the input Amazon Resource Name
        (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/delete_pricing_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#delete_pricing_rule)
        """

    def disassociate_accounts(
        self, **kwargs: Unpack[DisassociateAccountsInputRequestTypeDef]
    ) -> DisassociateAccountsOutputTypeDef:
        """
        Removes the specified list of account IDs from the given billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/disassociate_accounts.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#disassociate_accounts)
        """

    def disassociate_pricing_rules(
        self, **kwargs: Unpack[DisassociatePricingRulesInputRequestTypeDef]
    ) -> DisassociatePricingRulesOutputTypeDef:
        """
        Disassociates a list of pricing rules from a pricing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/disassociate_pricing_rules.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#disassociate_pricing_rules)
        """

    def get_billing_group_cost_report(
        self, **kwargs: Unpack[GetBillingGroupCostReportInputRequestTypeDef]
    ) -> GetBillingGroupCostReportOutputTypeDef:
        """
        Retrieves the margin summary report, which includes the Amazon Web Services
        cost and charged amount (pro forma cost) by Amazon Web Service for a specific
        billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/get_billing_group_cost_report.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#get_billing_group_cost_report)
        """

    def list_account_associations(
        self, **kwargs: Unpack[ListAccountAssociationsInputRequestTypeDef]
    ) -> ListAccountAssociationsOutputTypeDef:
        """
        This is a paginated call to list linked accounts that are linked to the payer
        account for the specified time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/list_account_associations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#list_account_associations)
        """

    def list_billing_group_cost_reports(
        self, **kwargs: Unpack[ListBillingGroupCostReportsInputRequestTypeDef]
    ) -> ListBillingGroupCostReportsOutputTypeDef:
        """
        A paginated call to retrieve a summary report of actual Amazon Web Services
        charges and the calculated Amazon Web Services charges based on the associated
        pricing plan of a billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/list_billing_group_cost_reports.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#list_billing_group_cost_reports)
        """

    def list_billing_groups(
        self, **kwargs: Unpack[ListBillingGroupsInputRequestTypeDef]
    ) -> ListBillingGroupsOutputTypeDef:
        """
        A paginated call to retrieve a list of billing groups for the given billing
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/list_billing_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#list_billing_groups)
        """

    def list_custom_line_item_versions(
        self, **kwargs: Unpack[ListCustomLineItemVersionsInputRequestTypeDef]
    ) -> ListCustomLineItemVersionsOutputTypeDef:
        """
        A paginated call to get a list of all custom line item versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/list_custom_line_item_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#list_custom_line_item_versions)
        """

    def list_custom_line_items(
        self, **kwargs: Unpack[ListCustomLineItemsInputRequestTypeDef]
    ) -> ListCustomLineItemsOutputTypeDef:
        """
        A paginated call to get a list of all custom line items (FFLIs) for the given
        billing period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/list_custom_line_items.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#list_custom_line_items)
        """

    def list_pricing_plans(
        self, **kwargs: Unpack[ListPricingPlansInputRequestTypeDef]
    ) -> ListPricingPlansOutputTypeDef:
        """
        A paginated call to get pricing plans for the given billing period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/list_pricing_plans.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#list_pricing_plans)
        """

    def list_pricing_plans_associated_with_pricing_rule(
        self, **kwargs: Unpack[ListPricingPlansAssociatedWithPricingRuleInputRequestTypeDef]
    ) -> ListPricingPlansAssociatedWithPricingRuleOutputTypeDef:
        """
        A list of the pricing plans that are associated with a pricing rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/list_pricing_plans_associated_with_pricing_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#list_pricing_plans_associated_with_pricing_rule)
        """

    def list_pricing_rules(
        self, **kwargs: Unpack[ListPricingRulesInputRequestTypeDef]
    ) -> ListPricingRulesOutputTypeDef:
        """
        Describes a pricing rule that can be associated to a pricing plan, or set of
        pricing plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/list_pricing_rules.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#list_pricing_rules)
        """

    def list_pricing_rules_associated_to_pricing_plan(
        self, **kwargs: Unpack[ListPricingRulesAssociatedToPricingPlanInputRequestTypeDef]
    ) -> ListPricingRulesAssociatedToPricingPlanOutputTypeDef:
        """
        Lists the pricing rules that are associated with a pricing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/list_pricing_rules_associated_to_pricing_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#list_pricing_rules_associated_to_pricing_plan)
        """

    def list_resources_associated_to_custom_line_item(
        self, **kwargs: Unpack[ListResourcesAssociatedToCustomLineItemInputRequestTypeDef]
    ) -> ListResourcesAssociatedToCustomLineItemOutputTypeDef:
        """
        List the resources that are associated to a custom line item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/list_resources_associated_to_custom_line_item.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#list_resources_associated_to_custom_line_item)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        A list the tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#list_tags_for_resource)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified
        <code>resourceArn</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#untag_resource)
        """

    def update_billing_group(
        self, **kwargs: Unpack[UpdateBillingGroupInputRequestTypeDef]
    ) -> UpdateBillingGroupOutputTypeDef:
        """
        This updates an existing billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/update_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#update_billing_group)
        """

    def update_custom_line_item(
        self, **kwargs: Unpack[UpdateCustomLineItemInputRequestTypeDef]
    ) -> UpdateCustomLineItemOutputTypeDef:
        """
        Update an existing custom line item in the current or previous billing period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/update_custom_line_item.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#update_custom_line_item)
        """

    def update_pricing_plan(
        self, **kwargs: Unpack[UpdatePricingPlanInputRequestTypeDef]
    ) -> UpdatePricingPlanOutputTypeDef:
        """
        This updates an existing pricing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/update_pricing_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#update_pricing_plan)
        """

    def update_pricing_rule(
        self, **kwargs: Unpack[UpdatePricingRuleInputRequestTypeDef]
    ) -> UpdatePricingRuleOutputTypeDef:
        """
        Updates an existing pricing rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/update_pricing_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#update_pricing_rule)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_account_associations"]
    ) -> ListAccountAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_billing_group_cost_reports"]
    ) -> ListBillingGroupCostReportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_billing_groups"]
    ) -> ListBillingGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_line_item_versions"]
    ) -> ListCustomLineItemVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_line_items"]
    ) -> ListCustomLineItemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pricing_plans_associated_with_pricing_rule"]
    ) -> ListPricingPlansAssociatedWithPricingRulePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pricing_plans"]
    ) -> ListPricingPlansPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pricing_rules_associated_to_pricing_plan"]
    ) -> ListPricingRulesAssociatedToPricingPlanPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pricing_rules"]
    ) -> ListPricingRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resources_associated_to_custom_line_item"]
    ) -> ListResourcesAssociatedToCustomLineItemPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billingconductor/client/#get_paginator)
        """
