"""
Main interface for amplifybackend service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_amplifybackend import (
        AmplifyBackendClient,
        Client,
        ListBackendJobsPaginator,
    )

    session = Session()
    client: AmplifyBackendClient = session.client("amplifybackend")

    list_backend_jobs_paginator: ListBackendJobsPaginator = client.get_paginator("list_backend_jobs")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import AmplifyBackendClient
from .paginator import ListBackendJobsPaginator

Client = AmplifyBackendClient


__all__ = ("AmplifyBackendClient", "Client", "ListBackendJobsPaginator")
