"""
Type annotations for elastictranscoder service client waiters.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elastictranscoder/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_elastictranscoder.client import ElasticTranscoderClient
    from types_boto3_elastictranscoder.waiter import (
        JobCompleteWaiter,
    )

    session = Session()
    client: ElasticTranscoderClient = session.client("elastictranscoder")

    job_complete_waiter: JobCompleteWaiter = client.get_waiter("job_complete")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import ReadJobRequestJobCompleteWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("JobCompleteWaiter",)

class JobCompleteWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/waiter/JobComplete.html#ElasticTranscoder.Waiter.JobComplete)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elastictranscoder/waiters/#jobcompletewaiter)
    """
    def wait(self, **kwargs: Unpack[ReadJobRequestJobCompleteWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/waiter/JobComplete.html#ElasticTranscoder.Waiter.JobComplete.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elastictranscoder/waiters/#jobcompletewaiter)
        """
