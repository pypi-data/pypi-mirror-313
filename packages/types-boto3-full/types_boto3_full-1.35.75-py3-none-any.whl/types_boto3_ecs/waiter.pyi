"""
Type annotations for ecs service client waiters.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecs/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_ecs.client import ECSClient
    from types_boto3_ecs.waiter import (
        ServicesInactiveWaiter,
        ServicesStableWaiter,
        TasksRunningWaiter,
        TasksStoppedWaiter,
    )

    session = Session()
    client: ECSClient = session.client("ecs")

    services_inactive_waiter: ServicesInactiveWaiter = client.get_waiter("services_inactive")
    services_stable_waiter: ServicesStableWaiter = client.get_waiter("services_stable")
    tasks_running_waiter: TasksRunningWaiter = client.get_waiter("tasks_running")
    tasks_stopped_waiter: TasksStoppedWaiter = client.get_waiter("tasks_stopped")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import (
    DescribeServicesRequestServicesInactiveWaitTypeDef,
    DescribeServicesRequestServicesStableWaitTypeDef,
    DescribeTasksRequestTasksRunningWaitTypeDef,
    DescribeTasksRequestTasksStoppedWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ServicesInactiveWaiter",
    "ServicesStableWaiter",
    "TasksRunningWaiter",
    "TasksStoppedWaiter",
)

class ServicesInactiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/ServicesInactive.html#ECS.Waiter.ServicesInactive)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecs/waiters/#servicesinactivewaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeServicesRequestServicesInactiveWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/ServicesInactive.html#ECS.Waiter.ServicesInactive.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecs/waiters/#servicesinactivewaiter)
        """

class ServicesStableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/ServicesStable.html#ECS.Waiter.ServicesStable)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecs/waiters/#servicesstablewaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeServicesRequestServicesStableWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/ServicesStable.html#ECS.Waiter.ServicesStable.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecs/waiters/#servicesstablewaiter)
        """

class TasksRunningWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/TasksRunning.html#ECS.Waiter.TasksRunning)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecs/waiters/#tasksrunningwaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeTasksRequestTasksRunningWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/TasksRunning.html#ECS.Waiter.TasksRunning.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecs/waiters/#tasksrunningwaiter)
        """

class TasksStoppedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/TasksStopped.html#ECS.Waiter.TasksStopped)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecs/waiters/#tasksstoppedwaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeTasksRequestTasksStoppedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/waiter/TasksStopped.html#ECS.Waiter.TasksStopped.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecs/waiters/#tasksstoppedwaiter)
        """
