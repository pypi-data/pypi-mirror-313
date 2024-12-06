"""
Type annotations for healthlake service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_healthlake.client import HealthLakeClient

    session = Session()
    client: HealthLakeClient = session.client("healthlake")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateFHIRDatastoreRequestRequestTypeDef,
    CreateFHIRDatastoreResponseTypeDef,
    DeleteFHIRDatastoreRequestRequestTypeDef,
    DeleteFHIRDatastoreResponseTypeDef,
    DescribeFHIRDatastoreRequestRequestTypeDef,
    DescribeFHIRDatastoreResponseTypeDef,
    DescribeFHIRExportJobRequestRequestTypeDef,
    DescribeFHIRExportJobResponseTypeDef,
    DescribeFHIRImportJobRequestRequestTypeDef,
    DescribeFHIRImportJobResponseTypeDef,
    ListFHIRDatastoresRequestRequestTypeDef,
    ListFHIRDatastoresResponseTypeDef,
    ListFHIRExportJobsRequestRequestTypeDef,
    ListFHIRExportJobsResponseTypeDef,
    ListFHIRImportJobsRequestRequestTypeDef,
    ListFHIRImportJobsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartFHIRExportJobRequestRequestTypeDef,
    StartFHIRExportJobResponseTypeDef,
    StartFHIRImportJobRequestRequestTypeDef,
    StartFHIRImportJobResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("HealthLakeClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class HealthLakeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        HealthLakeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#close)
        """

    def create_fhir_datastore(
        self, **kwargs: Unpack[CreateFHIRDatastoreRequestRequestTypeDef]
    ) -> CreateFHIRDatastoreResponseTypeDef:
        """
        Creates a data store that can ingest and export FHIR formatted data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/create_fhir_datastore.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#create_fhir_datastore)
        """

    def delete_fhir_datastore(
        self, **kwargs: Unpack[DeleteFHIRDatastoreRequestRequestTypeDef]
    ) -> DeleteFHIRDatastoreResponseTypeDef:
        """
        Deletes a data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/delete_fhir_datastore.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#delete_fhir_datastore)
        """

    def describe_fhir_datastore(
        self, **kwargs: Unpack[DescribeFHIRDatastoreRequestRequestTypeDef]
    ) -> DescribeFHIRDatastoreResponseTypeDef:
        """
        Gets the properties associated with the FHIR data store, including the data
        store ID, data store ARN, data store name, data store status, when the data
        store was created, data store type version, and the data store's endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/describe_fhir_datastore.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#describe_fhir_datastore)
        """

    def describe_fhir_export_job(
        self, **kwargs: Unpack[DescribeFHIRExportJobRequestRequestTypeDef]
    ) -> DescribeFHIRExportJobResponseTypeDef:
        """
        Displays the properties of a FHIR export job, including the ID, ARN, name, and
        the status of the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/describe_fhir_export_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#describe_fhir_export_job)
        """

    def describe_fhir_import_job(
        self, **kwargs: Unpack[DescribeFHIRImportJobRequestRequestTypeDef]
    ) -> DescribeFHIRImportJobResponseTypeDef:
        """
        Displays the properties of a FHIR import job, including the ID, ARN, name, and
        the status of the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/describe_fhir_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#describe_fhir_import_job)
        """

    def list_fhir_datastores(
        self, **kwargs: Unpack[ListFHIRDatastoresRequestRequestTypeDef]
    ) -> ListFHIRDatastoresResponseTypeDef:
        """
        Lists all FHIR data stores that are in the user's account, regardless of data
        store status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/list_fhir_datastores.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#list_fhir_datastores)
        """

    def list_fhir_export_jobs(
        self, **kwargs: Unpack[ListFHIRExportJobsRequestRequestTypeDef]
    ) -> ListFHIRExportJobsResponseTypeDef:
        """
        Lists all FHIR export jobs associated with an account and their statuses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/list_fhir_export_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#list_fhir_export_jobs)
        """

    def list_fhir_import_jobs(
        self, **kwargs: Unpack[ListFHIRImportJobsRequestRequestTypeDef]
    ) -> ListFHIRImportJobsResponseTypeDef:
        """
        Lists all FHIR import jobs associated with an account and their statuses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/list_fhir_import_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#list_fhir_import_jobs)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of all existing tags associated with a data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#list_tags_for_resource)
        """

    def start_fhir_export_job(
        self, **kwargs: Unpack[StartFHIRExportJobRequestRequestTypeDef]
    ) -> StartFHIRExportJobResponseTypeDef:
        """
        Begins a FHIR export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/start_fhir_export_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#start_fhir_export_job)
        """

    def start_fhir_import_job(
        self, **kwargs: Unpack[StartFHIRImportJobRequestRequestTypeDef]
    ) -> StartFHIRImportJobResponseTypeDef:
        """
        Begins a FHIR Import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/start_fhir_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#start_fhir_import_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds a user specified key and value tag to a data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from a data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#untag_resource)
        """
