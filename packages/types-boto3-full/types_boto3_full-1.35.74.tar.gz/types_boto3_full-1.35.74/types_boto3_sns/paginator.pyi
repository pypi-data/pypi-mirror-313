"""
Type annotations for sns service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_sns.client import SNSClient
    from types_boto3_sns.paginator import (
        ListEndpointsByPlatformApplicationPaginator,
        ListOriginationNumbersPaginator,
        ListPhoneNumbersOptedOutPaginator,
        ListPlatformApplicationsPaginator,
        ListSMSSandboxPhoneNumbersPaginator,
        ListSubscriptionsByTopicPaginator,
        ListSubscriptionsPaginator,
        ListTopicsPaginator,
    )

    session = Session()
    client: SNSClient = session.client("sns")

    list_endpoints_by_platform_application_paginator: ListEndpointsByPlatformApplicationPaginator = client.get_paginator("list_endpoints_by_platform_application")
    list_origination_numbers_paginator: ListOriginationNumbersPaginator = client.get_paginator("list_origination_numbers")
    list_phone_numbers_opted_out_paginator: ListPhoneNumbersOptedOutPaginator = client.get_paginator("list_phone_numbers_opted_out")
    list_platform_applications_paginator: ListPlatformApplicationsPaginator = client.get_paginator("list_platform_applications")
    list_sms_sandbox_phone_numbers_paginator: ListSMSSandboxPhoneNumbersPaginator = client.get_paginator("list_sms_sandbox_phone_numbers")
    list_subscriptions_by_topic_paginator: ListSubscriptionsByTopicPaginator = client.get_paginator("list_subscriptions_by_topic")
    list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
    list_topics_paginator: ListTopicsPaginator = client.get_paginator("list_topics")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListEndpointsByPlatformApplicationInputListEndpointsByPlatformApplicationPaginateTypeDef,
    ListEndpointsByPlatformApplicationResponseTypeDef,
    ListOriginationNumbersRequestListOriginationNumbersPaginateTypeDef,
    ListOriginationNumbersResultTypeDef,
    ListPhoneNumbersOptedOutInputListPhoneNumbersOptedOutPaginateTypeDef,
    ListPhoneNumbersOptedOutResponseTypeDef,
    ListPlatformApplicationsInputListPlatformApplicationsPaginateTypeDef,
    ListPlatformApplicationsResponseTypeDef,
    ListSMSSandboxPhoneNumbersInputListSMSSandboxPhoneNumbersPaginateTypeDef,
    ListSMSSandboxPhoneNumbersResultTypeDef,
    ListSubscriptionsByTopicInputListSubscriptionsByTopicPaginateTypeDef,
    ListSubscriptionsByTopicResponseTypeDef,
    ListSubscriptionsInputListSubscriptionsPaginateTypeDef,
    ListSubscriptionsResponseTypeDef,
    ListTopicsInputListTopicsPaginateTypeDef,
    ListTopicsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListEndpointsByPlatformApplicationPaginator",
    "ListOriginationNumbersPaginator",
    "ListPhoneNumbersOptedOutPaginator",
    "ListPlatformApplicationsPaginator",
    "ListSMSSandboxPhoneNumbersPaginator",
    "ListSubscriptionsByTopicPaginator",
    "ListSubscriptionsPaginator",
    "ListTopicsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListEndpointsByPlatformApplicationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListEndpointsByPlatformApplication.html#SNS.Paginator.ListEndpointsByPlatformApplication)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/#listendpointsbyplatformapplicationpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListEndpointsByPlatformApplicationInputListEndpointsByPlatformApplicationPaginateTypeDef
        ],
    ) -> _PageIterator[ListEndpointsByPlatformApplicationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListEndpointsByPlatformApplication.html#SNS.Paginator.ListEndpointsByPlatformApplication.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/#listendpointsbyplatformapplicationpaginator)
        """

class ListOriginationNumbersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListOriginationNumbers.html#SNS.Paginator.ListOriginationNumbers)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/#listoriginationnumberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListOriginationNumbersRequestListOriginationNumbersPaginateTypeDef]
    ) -> _PageIterator[ListOriginationNumbersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListOriginationNumbers.html#SNS.Paginator.ListOriginationNumbers.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/#listoriginationnumberspaginator)
        """

class ListPhoneNumbersOptedOutPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListPhoneNumbersOptedOut.html#SNS.Paginator.ListPhoneNumbersOptedOut)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/#listphonenumbersoptedoutpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPhoneNumbersOptedOutInputListPhoneNumbersOptedOutPaginateTypeDef]
    ) -> _PageIterator[ListPhoneNumbersOptedOutResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListPhoneNumbersOptedOut.html#SNS.Paginator.ListPhoneNumbersOptedOut.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/#listphonenumbersoptedoutpaginator)
        """

class ListPlatformApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListPlatformApplications.html#SNS.Paginator.ListPlatformApplications)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/#listplatformapplicationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPlatformApplicationsInputListPlatformApplicationsPaginateTypeDef]
    ) -> _PageIterator[ListPlatformApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListPlatformApplications.html#SNS.Paginator.ListPlatformApplications.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/#listplatformapplicationspaginator)
        """

class ListSMSSandboxPhoneNumbersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListSMSSandboxPhoneNumbers.html#SNS.Paginator.ListSMSSandboxPhoneNumbers)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/#listsmssandboxphonenumberspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListSMSSandboxPhoneNumbersInputListSMSSandboxPhoneNumbersPaginateTypeDef],
    ) -> _PageIterator[ListSMSSandboxPhoneNumbersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListSMSSandboxPhoneNumbers.html#SNS.Paginator.ListSMSSandboxPhoneNumbers.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/#listsmssandboxphonenumberspaginator)
        """

class ListSubscriptionsByTopicPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListSubscriptionsByTopic.html#SNS.Paginator.ListSubscriptionsByTopic)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/#listsubscriptionsbytopicpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSubscriptionsByTopicInputListSubscriptionsByTopicPaginateTypeDef]
    ) -> _PageIterator[ListSubscriptionsByTopicResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListSubscriptionsByTopic.html#SNS.Paginator.ListSubscriptionsByTopic.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/#listsubscriptionsbytopicpaginator)
        """

class ListSubscriptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListSubscriptions.html#SNS.Paginator.ListSubscriptions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/#listsubscriptionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSubscriptionsInputListSubscriptionsPaginateTypeDef]
    ) -> _PageIterator[ListSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListSubscriptions.html#SNS.Paginator.ListSubscriptions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/#listsubscriptionspaginator)
        """

class ListTopicsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListTopics.html#SNS.Paginator.ListTopics)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/#listtopicspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTopicsInputListTopicsPaginateTypeDef]
    ) -> _PageIterator[ListTopicsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListTopics.html#SNS.Paginator.ListTopics.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sns/paginators/#listtopicspaginator)
        """
