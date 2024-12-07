"""
Type annotations for iotdeviceadvisor service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_iotdeviceadvisor.client import IoTDeviceAdvisorClient

    session = Session()
    client: IoTDeviceAdvisorClient = session.client("iotdeviceadvisor")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateSuiteDefinitionRequestRequestTypeDef,
    CreateSuiteDefinitionResponseTypeDef,
    DeleteSuiteDefinitionRequestRequestTypeDef,
    GetEndpointRequestRequestTypeDef,
    GetEndpointResponseTypeDef,
    GetSuiteDefinitionRequestRequestTypeDef,
    GetSuiteDefinitionResponseTypeDef,
    GetSuiteRunReportRequestRequestTypeDef,
    GetSuiteRunReportResponseTypeDef,
    GetSuiteRunRequestRequestTypeDef,
    GetSuiteRunResponseTypeDef,
    ListSuiteDefinitionsRequestRequestTypeDef,
    ListSuiteDefinitionsResponseTypeDef,
    ListSuiteRunsRequestRequestTypeDef,
    ListSuiteRunsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartSuiteRunRequestRequestTypeDef,
    StartSuiteRunResponseTypeDef,
    StopSuiteRunRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateSuiteDefinitionRequestRequestTypeDef,
    UpdateSuiteDefinitionResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("IoTDeviceAdvisorClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class IoTDeviceAdvisorClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTDeviceAdvisorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor.html#IoTDeviceAdvisor.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#close)
        """

    def create_suite_definition(
        self, **kwargs: Unpack[CreateSuiteDefinitionRequestRequestTypeDef]
    ) -> CreateSuiteDefinitionResponseTypeDef:
        """
        Creates a Device Advisor test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/create_suite_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#create_suite_definition)
        """

    def delete_suite_definition(
        self, **kwargs: Unpack[DeleteSuiteDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Device Advisor test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/delete_suite_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#delete_suite_definition)
        """

    def get_endpoint(
        self, **kwargs: Unpack[GetEndpointRequestRequestTypeDef]
    ) -> GetEndpointResponseTypeDef:
        """
        Gets information about an Device Advisor endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/get_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#get_endpoint)
        """

    def get_suite_definition(
        self, **kwargs: Unpack[GetSuiteDefinitionRequestRequestTypeDef]
    ) -> GetSuiteDefinitionResponseTypeDef:
        """
        Gets information about a Device Advisor test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/get_suite_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#get_suite_definition)
        """

    def get_suite_run(
        self, **kwargs: Unpack[GetSuiteRunRequestRequestTypeDef]
    ) -> GetSuiteRunResponseTypeDef:
        """
        Gets information about a Device Advisor test suite run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/get_suite_run.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#get_suite_run)
        """

    def get_suite_run_report(
        self, **kwargs: Unpack[GetSuiteRunReportRequestRequestTypeDef]
    ) -> GetSuiteRunReportResponseTypeDef:
        """
        Gets a report download link for a successful Device Advisor qualifying test
        suite run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/get_suite_run_report.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#get_suite_run_report)
        """

    def list_suite_definitions(
        self, **kwargs: Unpack[ListSuiteDefinitionsRequestRequestTypeDef]
    ) -> ListSuiteDefinitionsResponseTypeDef:
        """
        Lists the Device Advisor test suites you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/list_suite_definitions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#list_suite_definitions)
        """

    def list_suite_runs(
        self, **kwargs: Unpack[ListSuiteRunsRequestRequestTypeDef]
    ) -> ListSuiteRunsResponseTypeDef:
        """
        Lists runs of the specified Device Advisor test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/list_suite_runs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#list_suite_runs)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags attached to an IoT Device Advisor resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#list_tags_for_resource)
        """

    def start_suite_run(
        self, **kwargs: Unpack[StartSuiteRunRequestRequestTypeDef]
    ) -> StartSuiteRunResponseTypeDef:
        """
        Starts a Device Advisor test suite run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/start_suite_run.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#start_suite_run)
        """

    def stop_suite_run(self, **kwargs: Unpack[StopSuiteRunRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Stops a Device Advisor test suite run that is currently running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/stop_suite_run.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#stop_suite_run)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds to and modifies existing tags of an IoT Device Advisor resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from an IoT Device Advisor resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#untag_resource)
        """

    def update_suite_definition(
        self, **kwargs: Unpack[UpdateSuiteDefinitionRequestRequestTypeDef]
    ) -> UpdateSuiteDefinitionResponseTypeDef:
        """
        Updates a Device Advisor test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotdeviceadvisor/client/update_suite_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/client/#update_suite_definition)
        """
