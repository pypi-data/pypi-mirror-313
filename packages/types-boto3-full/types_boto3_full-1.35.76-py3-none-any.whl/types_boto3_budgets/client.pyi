"""
Type annotations for budgets service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_budgets.client import BudgetsClient

    session = Session()
    client: BudgetsClient = session.client("budgets")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeBudgetActionHistoriesPaginator,
    DescribeBudgetActionsForAccountPaginator,
    DescribeBudgetActionsForBudgetPaginator,
    DescribeBudgetNotificationsForAccountPaginator,
    DescribeBudgetPerformanceHistoryPaginator,
    DescribeBudgetsPaginator,
    DescribeNotificationsForBudgetPaginator,
    DescribeSubscribersForNotificationPaginator,
)
from .type_defs import (
    CreateBudgetActionRequestRequestTypeDef,
    CreateBudgetActionResponseTypeDef,
    CreateBudgetRequestRequestTypeDef,
    CreateNotificationRequestRequestTypeDef,
    CreateSubscriberRequestRequestTypeDef,
    DeleteBudgetActionRequestRequestTypeDef,
    DeleteBudgetActionResponseTypeDef,
    DeleteBudgetRequestRequestTypeDef,
    DeleteNotificationRequestRequestTypeDef,
    DeleteSubscriberRequestRequestTypeDef,
    DescribeBudgetActionHistoriesRequestRequestTypeDef,
    DescribeBudgetActionHistoriesResponseTypeDef,
    DescribeBudgetActionRequestRequestTypeDef,
    DescribeBudgetActionResponseTypeDef,
    DescribeBudgetActionsForAccountRequestRequestTypeDef,
    DescribeBudgetActionsForAccountResponseTypeDef,
    DescribeBudgetActionsForBudgetRequestRequestTypeDef,
    DescribeBudgetActionsForBudgetResponseTypeDef,
    DescribeBudgetNotificationsForAccountRequestRequestTypeDef,
    DescribeBudgetNotificationsForAccountResponseTypeDef,
    DescribeBudgetPerformanceHistoryRequestRequestTypeDef,
    DescribeBudgetPerformanceHistoryResponseTypeDef,
    DescribeBudgetRequestRequestTypeDef,
    DescribeBudgetResponseTypeDef,
    DescribeBudgetsRequestRequestTypeDef,
    DescribeBudgetsResponseTypeDef,
    DescribeNotificationsForBudgetRequestRequestTypeDef,
    DescribeNotificationsForBudgetResponseTypeDef,
    DescribeSubscribersForNotificationRequestRequestTypeDef,
    DescribeSubscribersForNotificationResponseTypeDef,
    ExecuteBudgetActionRequestRequestTypeDef,
    ExecuteBudgetActionResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateBudgetActionRequestRequestTypeDef,
    UpdateBudgetActionResponseTypeDef,
    UpdateBudgetRequestRequestTypeDef,
    UpdateNotificationRequestRequestTypeDef,
    UpdateSubscriberRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("BudgetsClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    CreationLimitExceededException: Type[BotocoreClientError]
    DuplicateRecordException: Type[BotocoreClientError]
    ExpiredNextTokenException: Type[BotocoreClientError]
    InternalErrorException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceLockedException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]

class BudgetsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BudgetsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#close)
        """

    def create_budget(self, **kwargs: Unpack[CreateBudgetRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Creates a budget and, if included, notifications and subscribers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/create_budget.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#create_budget)
        """

    def create_budget_action(
        self, **kwargs: Unpack[CreateBudgetActionRequestRequestTypeDef]
    ) -> CreateBudgetActionResponseTypeDef:
        """
        Creates a budget action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/create_budget_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#create_budget_action)
        """

    def create_notification(
        self, **kwargs: Unpack[CreateNotificationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a notification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/create_notification.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#create_notification)
        """

    def create_subscriber(
        self, **kwargs: Unpack[CreateSubscriberRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a subscriber.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/create_subscriber.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#create_subscriber)
        """

    def delete_budget(self, **kwargs: Unpack[DeleteBudgetRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a budget.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/delete_budget.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#delete_budget)
        """

    def delete_budget_action(
        self, **kwargs: Unpack[DeleteBudgetActionRequestRequestTypeDef]
    ) -> DeleteBudgetActionResponseTypeDef:
        """
        Deletes a budget action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/delete_budget_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#delete_budget_action)
        """

    def delete_notification(
        self, **kwargs: Unpack[DeleteNotificationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a notification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/delete_notification.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#delete_notification)
        """

    def delete_subscriber(
        self, **kwargs: Unpack[DeleteSubscriberRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a subscriber.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/delete_subscriber.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#delete_subscriber)
        """

    def describe_budget(
        self, **kwargs: Unpack[DescribeBudgetRequestRequestTypeDef]
    ) -> DescribeBudgetResponseTypeDef:
        """
        Describes a budget.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_budget.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#describe_budget)
        """

    def describe_budget_action(
        self, **kwargs: Unpack[DescribeBudgetActionRequestRequestTypeDef]
    ) -> DescribeBudgetActionResponseTypeDef:
        """
        Describes a budget action detail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_budget_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#describe_budget_action)
        """

    def describe_budget_action_histories(
        self, **kwargs: Unpack[DescribeBudgetActionHistoriesRequestRequestTypeDef]
    ) -> DescribeBudgetActionHistoriesResponseTypeDef:
        """
        Describes a budget action history detail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_budget_action_histories.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#describe_budget_action_histories)
        """

    def describe_budget_actions_for_account(
        self, **kwargs: Unpack[DescribeBudgetActionsForAccountRequestRequestTypeDef]
    ) -> DescribeBudgetActionsForAccountResponseTypeDef:
        """
        Describes all of the budget actions for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_budget_actions_for_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#describe_budget_actions_for_account)
        """

    def describe_budget_actions_for_budget(
        self, **kwargs: Unpack[DescribeBudgetActionsForBudgetRequestRequestTypeDef]
    ) -> DescribeBudgetActionsForBudgetResponseTypeDef:
        """
        Describes all of the budget actions for a budget.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_budget_actions_for_budget.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#describe_budget_actions_for_budget)
        """

    def describe_budget_notifications_for_account(
        self, **kwargs: Unpack[DescribeBudgetNotificationsForAccountRequestRequestTypeDef]
    ) -> DescribeBudgetNotificationsForAccountResponseTypeDef:
        """
        Lists the budget names and notifications that are associated with an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_budget_notifications_for_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#describe_budget_notifications_for_account)
        """

    def describe_budget_performance_history(
        self, **kwargs: Unpack[DescribeBudgetPerformanceHistoryRequestRequestTypeDef]
    ) -> DescribeBudgetPerformanceHistoryResponseTypeDef:
        """
        Describes the history for <code>DAILY</code>, <code>MONTHLY</code>, and
        <code>QUARTERLY</code> budgets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_budget_performance_history.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#describe_budget_performance_history)
        """

    def describe_budgets(
        self, **kwargs: Unpack[DescribeBudgetsRequestRequestTypeDef]
    ) -> DescribeBudgetsResponseTypeDef:
        """
        Lists the budgets that are associated with an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_budgets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#describe_budgets)
        """

    def describe_notifications_for_budget(
        self, **kwargs: Unpack[DescribeNotificationsForBudgetRequestRequestTypeDef]
    ) -> DescribeNotificationsForBudgetResponseTypeDef:
        """
        Lists the notifications that are associated with a budget.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_notifications_for_budget.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#describe_notifications_for_budget)
        """

    def describe_subscribers_for_notification(
        self, **kwargs: Unpack[DescribeSubscribersForNotificationRequestRequestTypeDef]
    ) -> DescribeSubscribersForNotificationResponseTypeDef:
        """
        Lists the subscribers that are associated with a notification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_subscribers_for_notification.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#describe_subscribers_for_notification)
        """

    def execute_budget_action(
        self, **kwargs: Unpack[ExecuteBudgetActionRequestRequestTypeDef]
    ) -> ExecuteBudgetActionResponseTypeDef:
        """
        Executes a budget action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/execute_budget_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#execute_budget_action)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags associated with a budget or budget action resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#list_tags_for_resource)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Creates tags for a budget or budget action resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes tags associated with a budget or budget action resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#untag_resource)
        """

    def update_budget(self, **kwargs: Unpack[UpdateBudgetRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates a budget.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/update_budget.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#update_budget)
        """

    def update_budget_action(
        self, **kwargs: Unpack[UpdateBudgetActionRequestRequestTypeDef]
    ) -> UpdateBudgetActionResponseTypeDef:
        """
        Updates a budget action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/update_budget_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#update_budget_action)
        """

    def update_notification(
        self, **kwargs: Unpack[UpdateNotificationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a notification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/update_notification.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#update_notification)
        """

    def update_subscriber(
        self, **kwargs: Unpack[UpdateSubscriberRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a subscriber.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/update_subscriber.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#update_subscriber)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_budget_action_histories"]
    ) -> DescribeBudgetActionHistoriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_budget_actions_for_account"]
    ) -> DescribeBudgetActionsForAccountPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_budget_actions_for_budget"]
    ) -> DescribeBudgetActionsForBudgetPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_budget_notifications_for_account"]
    ) -> DescribeBudgetNotificationsForAccountPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_budget_performance_history"]
    ) -> DescribeBudgetPerformanceHistoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_budgets"]
    ) -> DescribeBudgetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_notifications_for_budget"]
    ) -> DescribeNotificationsForBudgetPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_subscribers_for_notification"]
    ) -> DescribeSubscribersForNotificationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/client/#get_paginator)
        """
