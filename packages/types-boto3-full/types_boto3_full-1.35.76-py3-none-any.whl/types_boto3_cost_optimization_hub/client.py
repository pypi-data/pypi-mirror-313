"""
Type annotations for cost-optimization-hub service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cost_optimization_hub/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_cost_optimization_hub.client import CostOptimizationHubClient

    session = Session()
    client: CostOptimizationHubClient = session.client("cost-optimization-hub")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListEnrollmentStatusesPaginator,
    ListRecommendationsPaginator,
    ListRecommendationSummariesPaginator,
)
from .type_defs import (
    GetPreferencesResponseTypeDef,
    GetRecommendationRequestRequestTypeDef,
    GetRecommendationResponseTypeDef,
    ListEnrollmentStatusesRequestRequestTypeDef,
    ListEnrollmentStatusesResponseTypeDef,
    ListRecommendationsRequestRequestTypeDef,
    ListRecommendationsResponseTypeDef,
    ListRecommendationSummariesRequestRequestTypeDef,
    ListRecommendationSummariesResponseTypeDef,
    UpdateEnrollmentStatusRequestRequestTypeDef,
    UpdateEnrollmentStatusResponseTypeDef,
    UpdatePreferencesRequestRequestTypeDef,
    UpdatePreferencesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("CostOptimizationHubClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CostOptimizationHubClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub.html#CostOptimizationHub.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cost_optimization_hub/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CostOptimizationHubClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub.html#CostOptimizationHub.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cost_optimization_hub/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cost_optimization_hub/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cost_optimization_hub/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cost_optimization_hub/client/#close)
        """

    def get_preferences(self) -> GetPreferencesResponseTypeDef:
        """
        Returns a set of preferences for an account in order to add account-specific
        preferences into the service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/client/get_preferences.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cost_optimization_hub/client/#get_preferences)
        """

    def get_recommendation(
        self, **kwargs: Unpack[GetRecommendationRequestRequestTypeDef]
    ) -> GetRecommendationResponseTypeDef:
        """
        Returns both the current and recommended resource configuration and the
        estimated cost impact for a recommendation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/client/get_recommendation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cost_optimization_hub/client/#get_recommendation)
        """

    def list_enrollment_statuses(
        self, **kwargs: Unpack[ListEnrollmentStatusesRequestRequestTypeDef]
    ) -> ListEnrollmentStatusesResponseTypeDef:
        """
        Retrieves the enrollment status for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/client/list_enrollment_statuses.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cost_optimization_hub/client/#list_enrollment_statuses)
        """

    def list_recommendation_summaries(
        self, **kwargs: Unpack[ListRecommendationSummariesRequestRequestTypeDef]
    ) -> ListRecommendationSummariesResponseTypeDef:
        """
        Returns a concise representation of savings estimates for resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/client/list_recommendation_summaries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cost_optimization_hub/client/#list_recommendation_summaries)
        """

    def list_recommendations(
        self, **kwargs: Unpack[ListRecommendationsRequestRequestTypeDef]
    ) -> ListRecommendationsResponseTypeDef:
        """
        Returns a list of recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/client/list_recommendations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cost_optimization_hub/client/#list_recommendations)
        """

    def update_enrollment_status(
        self, **kwargs: Unpack[UpdateEnrollmentStatusRequestRequestTypeDef]
    ) -> UpdateEnrollmentStatusResponseTypeDef:
        """
        Updates the enrollment (opt in and opt out) status of an account to the Cost
        Optimization Hub service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/client/update_enrollment_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cost_optimization_hub/client/#update_enrollment_status)
        """

    def update_preferences(
        self, **kwargs: Unpack[UpdatePreferencesRequestRequestTypeDef]
    ) -> UpdatePreferencesResponseTypeDef:
        """
        Updates a set of preferences for an account in order to add account-specific
        preferences into the service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/client/update_preferences.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cost_optimization_hub/client/#update_preferences)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_enrollment_statuses"]
    ) -> ListEnrollmentStatusesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cost_optimization_hub/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recommendation_summaries"]
    ) -> ListRecommendationSummariesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cost_optimization_hub/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recommendations"]
    ) -> ListRecommendationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cost-optimization-hub/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cost_optimization_hub/client/#get_paginator)
        """
