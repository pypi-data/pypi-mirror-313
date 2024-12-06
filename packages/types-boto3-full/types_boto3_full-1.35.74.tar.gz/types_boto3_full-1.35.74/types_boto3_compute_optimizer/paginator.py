"""
Type annotations for compute-optimizer service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_compute_optimizer/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_compute_optimizer.client import ComputeOptimizerClient
    from types_boto3_compute_optimizer.paginator import (
        DescribeRecommendationExportJobsPaginator,
        GetEnrollmentStatusesForOrganizationPaginator,
        GetLambdaFunctionRecommendationsPaginator,
        GetRecommendationPreferencesPaginator,
        GetRecommendationSummariesPaginator,
    )

    session = Session()
    client: ComputeOptimizerClient = session.client("compute-optimizer")

    describe_recommendation_export_jobs_paginator: DescribeRecommendationExportJobsPaginator = client.get_paginator("describe_recommendation_export_jobs")
    get_enrollment_statuses_for_organization_paginator: GetEnrollmentStatusesForOrganizationPaginator = client.get_paginator("get_enrollment_statuses_for_organization")
    get_lambda_function_recommendations_paginator: GetLambdaFunctionRecommendationsPaginator = client.get_paginator("get_lambda_function_recommendations")
    get_recommendation_preferences_paginator: GetRecommendationPreferencesPaginator = client.get_paginator("get_recommendation_preferences")
    get_recommendation_summaries_paginator: GetRecommendationSummariesPaginator = client.get_paginator("get_recommendation_summaries")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeRecommendationExportJobsRequestDescribeRecommendationExportJobsPaginateTypeDef,
    DescribeRecommendationExportJobsResponseTypeDef,
    GetEnrollmentStatusesForOrganizationRequestGetEnrollmentStatusesForOrganizationPaginateTypeDef,
    GetEnrollmentStatusesForOrganizationResponseTypeDef,
    GetLambdaFunctionRecommendationsRequestGetLambdaFunctionRecommendationsPaginateTypeDef,
    GetLambdaFunctionRecommendationsResponseTypeDef,
    GetRecommendationPreferencesRequestGetRecommendationPreferencesPaginateTypeDef,
    GetRecommendationPreferencesResponseTypeDef,
    GetRecommendationSummariesRequestGetRecommendationSummariesPaginateTypeDef,
    GetRecommendationSummariesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeRecommendationExportJobsPaginator",
    "GetEnrollmentStatusesForOrganizationPaginator",
    "GetLambdaFunctionRecommendationsPaginator",
    "GetRecommendationPreferencesPaginator",
    "GetRecommendationSummariesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeRecommendationExportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/DescribeRecommendationExportJobs.html#ComputeOptimizer.Paginator.DescribeRecommendationExportJobs)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_compute_optimizer/paginators/#describerecommendationexportjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeRecommendationExportJobsRequestDescribeRecommendationExportJobsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeRecommendationExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/DescribeRecommendationExportJobs.html#ComputeOptimizer.Paginator.DescribeRecommendationExportJobs.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_compute_optimizer/paginators/#describerecommendationexportjobspaginator)
        """


class GetEnrollmentStatusesForOrganizationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/GetEnrollmentStatusesForOrganization.html#ComputeOptimizer.Paginator.GetEnrollmentStatusesForOrganization)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_compute_optimizer/paginators/#getenrollmentstatusesfororganizationpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetEnrollmentStatusesForOrganizationRequestGetEnrollmentStatusesForOrganizationPaginateTypeDef
        ],
    ) -> _PageIterator[GetEnrollmentStatusesForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/GetEnrollmentStatusesForOrganization.html#ComputeOptimizer.Paginator.GetEnrollmentStatusesForOrganization.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_compute_optimizer/paginators/#getenrollmentstatusesfororganizationpaginator)
        """


class GetLambdaFunctionRecommendationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/GetLambdaFunctionRecommendations.html#ComputeOptimizer.Paginator.GetLambdaFunctionRecommendations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_compute_optimizer/paginators/#getlambdafunctionrecommendationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetLambdaFunctionRecommendationsRequestGetLambdaFunctionRecommendationsPaginateTypeDef
        ],
    ) -> _PageIterator[GetLambdaFunctionRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/GetLambdaFunctionRecommendations.html#ComputeOptimizer.Paginator.GetLambdaFunctionRecommendations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_compute_optimizer/paginators/#getlambdafunctionrecommendationspaginator)
        """


class GetRecommendationPreferencesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/GetRecommendationPreferences.html#ComputeOptimizer.Paginator.GetRecommendationPreferences)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_compute_optimizer/paginators/#getrecommendationpreferencespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetRecommendationPreferencesRequestGetRecommendationPreferencesPaginateTypeDef
        ],
    ) -> _PageIterator[GetRecommendationPreferencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/GetRecommendationPreferences.html#ComputeOptimizer.Paginator.GetRecommendationPreferences.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_compute_optimizer/paginators/#getrecommendationpreferencespaginator)
        """


class GetRecommendationSummariesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/GetRecommendationSummaries.html#ComputeOptimizer.Paginator.GetRecommendationSummaries)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_compute_optimizer/paginators/#getrecommendationsummariespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            GetRecommendationSummariesRequestGetRecommendationSummariesPaginateTypeDef
        ],
    ) -> _PageIterator[GetRecommendationSummariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/GetRecommendationSummaries.html#ComputeOptimizer.Paginator.GetRecommendationSummaries.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_compute_optimizer/paginators/#getrecommendationsummariespaginator)
        """
