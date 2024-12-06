"""
Main interface for cur service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_cur import (
        Client,
        CostandUsageReportServiceClient,
        DescribeReportDefinitionsPaginator,
    )

    session = Session()
    client: CostandUsageReportServiceClient = session.client("cur")

    describe_report_definitions_paginator: DescribeReportDefinitionsPaginator = client.get_paginator("describe_report_definitions")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CostandUsageReportServiceClient
from .paginator import DescribeReportDefinitionsPaginator

Client = CostandUsageReportServiceClient

__all__ = ("Client", "CostandUsageReportServiceClient", "DescribeReportDefinitionsPaginator")
