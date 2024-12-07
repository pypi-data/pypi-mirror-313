"""
Type annotations for applicationcostprofiler service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_applicationcostprofiler/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_applicationcostprofiler.client import ApplicationCostProfilerClient

    session = Session()
    client: ApplicationCostProfilerClient = session.client("applicationcostprofiler")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListReportDefinitionsPaginator
from .type_defs import (
    DeleteReportDefinitionRequestRequestTypeDef,
    DeleteReportDefinitionResultTypeDef,
    GetReportDefinitionRequestRequestTypeDef,
    GetReportDefinitionResultTypeDef,
    ImportApplicationUsageRequestRequestTypeDef,
    ImportApplicationUsageResultTypeDef,
    ListReportDefinitionsRequestRequestTypeDef,
    ListReportDefinitionsResultTypeDef,
    PutReportDefinitionRequestRequestTypeDef,
    PutReportDefinitionResultTypeDef,
    UpdateReportDefinitionRequestRequestTypeDef,
    UpdateReportDefinitionResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ApplicationCostProfilerClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ApplicationCostProfilerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler.html#ApplicationCostProfiler.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_applicationcostprofiler/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ApplicationCostProfilerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler.html#ApplicationCostProfiler.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_applicationcostprofiler/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_applicationcostprofiler/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_applicationcostprofiler/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_applicationcostprofiler/client/#close)
        """

    def delete_report_definition(
        self, **kwargs: Unpack[DeleteReportDefinitionRequestRequestTypeDef]
    ) -> DeleteReportDefinitionResultTypeDef:
        """
        Deletes the specified report definition in AWS Application Cost Profiler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler/client/delete_report_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_applicationcostprofiler/client/#delete_report_definition)
        """

    def get_report_definition(
        self, **kwargs: Unpack[GetReportDefinitionRequestRequestTypeDef]
    ) -> GetReportDefinitionResultTypeDef:
        """
        Retrieves the definition of a report already configured in AWS Application Cost
        Profiler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler/client/get_report_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_applicationcostprofiler/client/#get_report_definition)
        """

    def import_application_usage(
        self, **kwargs: Unpack[ImportApplicationUsageRequestRequestTypeDef]
    ) -> ImportApplicationUsageResultTypeDef:
        """
        Ingests application usage data from Amazon Simple Storage Service (Amazon S3).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler/client/import_application_usage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_applicationcostprofiler/client/#import_application_usage)
        """

    def list_report_definitions(
        self, **kwargs: Unpack[ListReportDefinitionsRequestRequestTypeDef]
    ) -> ListReportDefinitionsResultTypeDef:
        """
        Retrieves a list of all reports and their configurations for your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler/client/list_report_definitions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_applicationcostprofiler/client/#list_report_definitions)
        """

    def put_report_definition(
        self, **kwargs: Unpack[PutReportDefinitionRequestRequestTypeDef]
    ) -> PutReportDefinitionResultTypeDef:
        """
        Creates the report definition for a report in Application Cost Profiler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler/client/put_report_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_applicationcostprofiler/client/#put_report_definition)
        """

    def update_report_definition(
        self, **kwargs: Unpack[UpdateReportDefinitionRequestRequestTypeDef]
    ) -> UpdateReportDefinitionResultTypeDef:
        """
        Updates existing report in AWS Application Cost Profiler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler/client/update_report_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_applicationcostprofiler/client/#update_report_definition)
        """

    def get_paginator(
        self, operation_name: Literal["list_report_definitions"]
    ) -> ListReportDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/applicationcostprofiler/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_applicationcostprofiler/client/#get_paginator)
        """
