"""
Type annotations for savingsplans service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_savingsplans/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_savingsplans.client import SavingsPlansClient

    session = Session()
    client: SavingsPlansClient = session.client("savingsplans")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateSavingsPlanRequestRequestTypeDef,
    CreateSavingsPlanResponseTypeDef,
    DeleteQueuedSavingsPlanRequestRequestTypeDef,
    DescribeSavingsPlanRatesRequestRequestTypeDef,
    DescribeSavingsPlanRatesResponseTypeDef,
    DescribeSavingsPlansOfferingRatesRequestRequestTypeDef,
    DescribeSavingsPlansOfferingRatesResponseTypeDef,
    DescribeSavingsPlansOfferingsRequestRequestTypeDef,
    DescribeSavingsPlansOfferingsResponseTypeDef,
    DescribeSavingsPlansRequestRequestTypeDef,
    DescribeSavingsPlansResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ReturnSavingsPlanRequestRequestTypeDef,
    ReturnSavingsPlanResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("SavingsPlansClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class SavingsPlansClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans.html#SavingsPlans.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_savingsplans/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SavingsPlansClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans.html#SavingsPlans.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_savingsplans/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_savingsplans/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_savingsplans/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_savingsplans/client/#close)
        """

    def create_savings_plan(
        self, **kwargs: Unpack[CreateSavingsPlanRequestRequestTypeDef]
    ) -> CreateSavingsPlanResponseTypeDef:
        """
        Creates a Savings Plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/create_savings_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_savingsplans/client/#create_savings_plan)
        """

    def delete_queued_savings_plan(
        self, **kwargs: Unpack[DeleteQueuedSavingsPlanRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the queued purchase for the specified Savings Plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/delete_queued_savings_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_savingsplans/client/#delete_queued_savings_plan)
        """

    def describe_savings_plan_rates(
        self, **kwargs: Unpack[DescribeSavingsPlanRatesRequestRequestTypeDef]
    ) -> DescribeSavingsPlanRatesResponseTypeDef:
        """
        Describes the rates for the specified Savings Plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/describe_savings_plan_rates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_savingsplans/client/#describe_savings_plan_rates)
        """

    def describe_savings_plans(
        self, **kwargs: Unpack[DescribeSavingsPlansRequestRequestTypeDef]
    ) -> DescribeSavingsPlansResponseTypeDef:
        """
        Describes the specified Savings Plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/describe_savings_plans.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_savingsplans/client/#describe_savings_plans)
        """

    def describe_savings_plans_offering_rates(
        self, **kwargs: Unpack[DescribeSavingsPlansOfferingRatesRequestRequestTypeDef]
    ) -> DescribeSavingsPlansOfferingRatesResponseTypeDef:
        """
        Describes the offering rates for the specified Savings Plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/describe_savings_plans_offering_rates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_savingsplans/client/#describe_savings_plans_offering_rates)
        """

    def describe_savings_plans_offerings(
        self, **kwargs: Unpack[DescribeSavingsPlansOfferingsRequestRequestTypeDef]
    ) -> DescribeSavingsPlansOfferingsResponseTypeDef:
        """
        Describes the offerings for the specified Savings Plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/describe_savings_plans_offerings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_savingsplans/client/#describe_savings_plans_offerings)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_savingsplans/client/#list_tags_for_resource)
        """

    def return_savings_plan(
        self, **kwargs: Unpack[ReturnSavingsPlanRequestRequestTypeDef]
    ) -> ReturnSavingsPlanResponseTypeDef:
        """
        Returns the specified Savings Plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/return_savings_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_savingsplans/client/#return_savings_plan)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_savingsplans/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_savingsplans/client/#untag_resource)
        """
