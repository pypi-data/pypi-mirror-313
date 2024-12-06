"""
Main interface for codeguru-security service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_codeguru_security import (
        Client,
        CodeGuruSecurityClient,
        GetFindingsPaginator,
        ListFindingsMetricsPaginator,
        ListScansPaginator,
    )

    session = Session()
    client: CodeGuruSecurityClient = session.client("codeguru-security")

    get_findings_paginator: GetFindingsPaginator = client.get_paginator("get_findings")
    list_findings_metrics_paginator: ListFindingsMetricsPaginator = client.get_paginator("list_findings_metrics")
    list_scans_paginator: ListScansPaginator = client.get_paginator("list_scans")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CodeGuruSecurityClient
from .paginator import GetFindingsPaginator, ListFindingsMetricsPaginator, ListScansPaginator

Client = CodeGuruSecurityClient


__all__ = (
    "Client",
    "CodeGuruSecurityClient",
    "GetFindingsPaginator",
    "ListFindingsMetricsPaginator",
    "ListScansPaginator",
)
