"""
Type annotations for dsql service client waiters.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dsql/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_dsql.client import AuroraDSQLClient
    from types_boto3_dsql.waiter import (
        ClusterActiveWaiter,
        ClusterNotExistsWaiter,
    )

    session = Session()
    client: AuroraDSQLClient = session.client("dsql")

    cluster_active_waiter: ClusterActiveWaiter = client.get_waiter("cluster_active")
    cluster_not_exists_waiter: ClusterNotExistsWaiter = client.get_waiter("cluster_not_exists")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import (
    GetClusterInputClusterActiveWaitTypeDef,
    GetClusterInputClusterNotExistsWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ClusterActiveWaiter", "ClusterNotExistsWaiter")

class ClusterActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dsql/waiter/ClusterActive.html#AuroraDSQL.Waiter.ClusterActive)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dsql/waiters/#clusteractivewaiter)
    """
    def wait(self, **kwargs: Unpack[GetClusterInputClusterActiveWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dsql/waiter/ClusterActive.html#AuroraDSQL.Waiter.ClusterActive.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dsql/waiters/#clusteractivewaiter)
        """

class ClusterNotExistsWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dsql/waiter/ClusterNotExists.html#AuroraDSQL.Waiter.ClusterNotExists)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dsql/waiters/#clusternotexistswaiter)
    """
    def wait(self, **kwargs: Unpack[GetClusterInputClusterNotExistsWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dsql/waiter/ClusterNotExists.html#AuroraDSQL.Waiter.ClusterNotExists.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dsql/waiters/#clusternotexistswaiter)
        """
