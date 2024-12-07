"""
Type annotations for omics service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_omics.client import OmicsClient

    session = Session()
    client: OmicsClient = session.client("omics")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAnnotationImportJobsPaginator,
    ListAnnotationStoresPaginator,
    ListAnnotationStoreVersionsPaginator,
    ListMultipartReadSetUploadsPaginator,
    ListReadSetActivationJobsPaginator,
    ListReadSetExportJobsPaginator,
    ListReadSetImportJobsPaginator,
    ListReadSetsPaginator,
    ListReadSetUploadPartsPaginator,
    ListReferenceImportJobsPaginator,
    ListReferencesPaginator,
    ListReferenceStoresPaginator,
    ListRunCachesPaginator,
    ListRunGroupsPaginator,
    ListRunsPaginator,
    ListRunTasksPaginator,
    ListSequenceStoresPaginator,
    ListSharesPaginator,
    ListVariantImportJobsPaginator,
    ListVariantStoresPaginator,
    ListWorkflowsPaginator,
)
from .type_defs import (
    AbortMultipartReadSetUploadRequestRequestTypeDef,
    AcceptShareRequestRequestTypeDef,
    AcceptShareResponseTypeDef,
    BatchDeleteReadSetRequestRequestTypeDef,
    BatchDeleteReadSetResponseTypeDef,
    CancelAnnotationImportRequestRequestTypeDef,
    CancelRunRequestRequestTypeDef,
    CancelVariantImportRequestRequestTypeDef,
    CompleteMultipartReadSetUploadRequestRequestTypeDef,
    CompleteMultipartReadSetUploadResponseTypeDef,
    CreateAnnotationStoreRequestRequestTypeDef,
    CreateAnnotationStoreResponseTypeDef,
    CreateAnnotationStoreVersionRequestRequestTypeDef,
    CreateAnnotationStoreVersionResponseTypeDef,
    CreateMultipartReadSetUploadRequestRequestTypeDef,
    CreateMultipartReadSetUploadResponseTypeDef,
    CreateReferenceStoreRequestRequestTypeDef,
    CreateReferenceStoreResponseTypeDef,
    CreateRunCacheRequestRequestTypeDef,
    CreateRunCacheResponseTypeDef,
    CreateRunGroupRequestRequestTypeDef,
    CreateRunGroupResponseTypeDef,
    CreateSequenceStoreRequestRequestTypeDef,
    CreateSequenceStoreResponseTypeDef,
    CreateShareRequestRequestTypeDef,
    CreateShareResponseTypeDef,
    CreateVariantStoreRequestRequestTypeDef,
    CreateVariantStoreResponseTypeDef,
    CreateWorkflowRequestRequestTypeDef,
    CreateWorkflowResponseTypeDef,
    DeleteAnnotationStoreRequestRequestTypeDef,
    DeleteAnnotationStoreResponseTypeDef,
    DeleteAnnotationStoreVersionsRequestRequestTypeDef,
    DeleteAnnotationStoreVersionsResponseTypeDef,
    DeleteReferenceRequestRequestTypeDef,
    DeleteReferenceStoreRequestRequestTypeDef,
    DeleteRunCacheRequestRequestTypeDef,
    DeleteRunGroupRequestRequestTypeDef,
    DeleteRunRequestRequestTypeDef,
    DeleteS3AccessPolicyRequestRequestTypeDef,
    DeleteSequenceStoreRequestRequestTypeDef,
    DeleteShareRequestRequestTypeDef,
    DeleteShareResponseTypeDef,
    DeleteVariantStoreRequestRequestTypeDef,
    DeleteVariantStoreResponseTypeDef,
    DeleteWorkflowRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAnnotationImportRequestRequestTypeDef,
    GetAnnotationImportResponseTypeDef,
    GetAnnotationStoreRequestRequestTypeDef,
    GetAnnotationStoreResponseTypeDef,
    GetAnnotationStoreVersionRequestRequestTypeDef,
    GetAnnotationStoreVersionResponseTypeDef,
    GetReadSetActivationJobRequestRequestTypeDef,
    GetReadSetActivationJobResponseTypeDef,
    GetReadSetExportJobRequestRequestTypeDef,
    GetReadSetExportJobResponseTypeDef,
    GetReadSetImportJobRequestRequestTypeDef,
    GetReadSetImportJobResponseTypeDef,
    GetReadSetMetadataRequestRequestTypeDef,
    GetReadSetMetadataResponseTypeDef,
    GetReadSetRequestRequestTypeDef,
    GetReadSetResponseTypeDef,
    GetReferenceImportJobRequestRequestTypeDef,
    GetReferenceImportJobResponseTypeDef,
    GetReferenceMetadataRequestRequestTypeDef,
    GetReferenceMetadataResponseTypeDef,
    GetReferenceRequestRequestTypeDef,
    GetReferenceResponseTypeDef,
    GetReferenceStoreRequestRequestTypeDef,
    GetReferenceStoreResponseTypeDef,
    GetRunCacheRequestRequestTypeDef,
    GetRunCacheResponseTypeDef,
    GetRunGroupRequestRequestTypeDef,
    GetRunGroupResponseTypeDef,
    GetRunRequestRequestTypeDef,
    GetRunResponseTypeDef,
    GetRunTaskRequestRequestTypeDef,
    GetRunTaskResponseTypeDef,
    GetS3AccessPolicyRequestRequestTypeDef,
    GetS3AccessPolicyResponseTypeDef,
    GetSequenceStoreRequestRequestTypeDef,
    GetSequenceStoreResponseTypeDef,
    GetShareRequestRequestTypeDef,
    GetShareResponseTypeDef,
    GetVariantImportRequestRequestTypeDef,
    GetVariantImportResponseTypeDef,
    GetVariantStoreRequestRequestTypeDef,
    GetVariantStoreResponseTypeDef,
    GetWorkflowRequestRequestTypeDef,
    GetWorkflowResponseTypeDef,
    ListAnnotationImportJobsRequestRequestTypeDef,
    ListAnnotationImportJobsResponseTypeDef,
    ListAnnotationStoresRequestRequestTypeDef,
    ListAnnotationStoresResponseTypeDef,
    ListAnnotationStoreVersionsRequestRequestTypeDef,
    ListAnnotationStoreVersionsResponseTypeDef,
    ListMultipartReadSetUploadsRequestRequestTypeDef,
    ListMultipartReadSetUploadsResponseTypeDef,
    ListReadSetActivationJobsRequestRequestTypeDef,
    ListReadSetActivationJobsResponseTypeDef,
    ListReadSetExportJobsRequestRequestTypeDef,
    ListReadSetExportJobsResponseTypeDef,
    ListReadSetImportJobsRequestRequestTypeDef,
    ListReadSetImportJobsResponseTypeDef,
    ListReadSetsRequestRequestTypeDef,
    ListReadSetsResponseTypeDef,
    ListReadSetUploadPartsRequestRequestTypeDef,
    ListReadSetUploadPartsResponseTypeDef,
    ListReferenceImportJobsRequestRequestTypeDef,
    ListReferenceImportJobsResponseTypeDef,
    ListReferencesRequestRequestTypeDef,
    ListReferencesResponseTypeDef,
    ListReferenceStoresRequestRequestTypeDef,
    ListReferenceStoresResponseTypeDef,
    ListRunCachesRequestRequestTypeDef,
    ListRunCachesResponseTypeDef,
    ListRunGroupsRequestRequestTypeDef,
    ListRunGroupsResponseTypeDef,
    ListRunsRequestRequestTypeDef,
    ListRunsResponseTypeDef,
    ListRunTasksRequestRequestTypeDef,
    ListRunTasksResponseTypeDef,
    ListSequenceStoresRequestRequestTypeDef,
    ListSequenceStoresResponseTypeDef,
    ListSharesRequestRequestTypeDef,
    ListSharesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVariantImportJobsRequestRequestTypeDef,
    ListVariantImportJobsResponseTypeDef,
    ListVariantStoresRequestRequestTypeDef,
    ListVariantStoresResponseTypeDef,
    ListWorkflowsRequestRequestTypeDef,
    ListWorkflowsResponseTypeDef,
    PutS3AccessPolicyRequestRequestTypeDef,
    PutS3AccessPolicyResponseTypeDef,
    StartAnnotationImportRequestRequestTypeDef,
    StartAnnotationImportResponseTypeDef,
    StartReadSetActivationJobRequestRequestTypeDef,
    StartReadSetActivationJobResponseTypeDef,
    StartReadSetExportJobRequestRequestTypeDef,
    StartReadSetExportJobResponseTypeDef,
    StartReadSetImportJobRequestRequestTypeDef,
    StartReadSetImportJobResponseTypeDef,
    StartReferenceImportJobRequestRequestTypeDef,
    StartReferenceImportJobResponseTypeDef,
    StartRunRequestRequestTypeDef,
    StartRunResponseTypeDef,
    StartVariantImportRequestRequestTypeDef,
    StartVariantImportResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAnnotationStoreRequestRequestTypeDef,
    UpdateAnnotationStoreResponseTypeDef,
    UpdateAnnotationStoreVersionRequestRequestTypeDef,
    UpdateAnnotationStoreVersionResponseTypeDef,
    UpdateRunCacheRequestRequestTypeDef,
    UpdateRunGroupRequestRequestTypeDef,
    UpdateSequenceStoreRequestRequestTypeDef,
    UpdateSequenceStoreResponseTypeDef,
    UpdateVariantStoreRequestRequestTypeDef,
    UpdateVariantStoreResponseTypeDef,
    UpdateWorkflowRequestRequestTypeDef,
    UploadReadSetPartRequestRequestTypeDef,
    UploadReadSetPartResponseTypeDef,
)
from .waiter import (
    AnnotationImportJobCreatedWaiter,
    AnnotationStoreCreatedWaiter,
    AnnotationStoreDeletedWaiter,
    AnnotationStoreVersionCreatedWaiter,
    AnnotationStoreVersionDeletedWaiter,
    ReadSetActivationJobCompletedWaiter,
    ReadSetExportJobCompletedWaiter,
    ReadSetImportJobCompletedWaiter,
    ReferenceImportJobCompletedWaiter,
    RunCompletedWaiter,
    RunRunningWaiter,
    TaskCompletedWaiter,
    TaskRunningWaiter,
    VariantImportJobCreatedWaiter,
    VariantStoreCreatedWaiter,
    VariantStoreDeletedWaiter,
    WorkflowActiveWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("OmicsClient",)

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
    NotSupportedOperationException: Type[BotocoreClientError]
    RangeNotSatisfiableException: Type[BotocoreClientError]
    RequestTimeoutException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class OmicsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OmicsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics.html#Omics.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#close)
        """

    def abort_multipart_read_set_upload(
        self, **kwargs: Unpack[AbortMultipartReadSetUploadRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops a multipart upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/abort_multipart_read_set_upload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#abort_multipart_read_set_upload)
        """

    def accept_share(
        self, **kwargs: Unpack[AcceptShareRequestRequestTypeDef]
    ) -> AcceptShareResponseTypeDef:
        """
        Accept a resource share request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/accept_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#accept_share)
        """

    def batch_delete_read_set(
        self, **kwargs: Unpack[BatchDeleteReadSetRequestRequestTypeDef]
    ) -> BatchDeleteReadSetResponseTypeDef:
        """
        Deletes one or more read sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/batch_delete_read_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#batch_delete_read_set)
        """

    def cancel_annotation_import_job(
        self, **kwargs: Unpack[CancelAnnotationImportRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels an annotation import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/cancel_annotation_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#cancel_annotation_import_job)
        """

    def cancel_run(
        self, **kwargs: Unpack[CancelRunRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels a run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/cancel_run.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#cancel_run)
        """

    def cancel_variant_import_job(
        self, **kwargs: Unpack[CancelVariantImportRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels a variant import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/cancel_variant_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#cancel_variant_import_job)
        """

    def complete_multipart_read_set_upload(
        self, **kwargs: Unpack[CompleteMultipartReadSetUploadRequestRequestTypeDef]
    ) -> CompleteMultipartReadSetUploadResponseTypeDef:
        """
        Concludes a multipart upload once you have uploaded all the components.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/complete_multipart_read_set_upload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#complete_multipart_read_set_upload)
        """

    def create_annotation_store(
        self, **kwargs: Unpack[CreateAnnotationStoreRequestRequestTypeDef]
    ) -> CreateAnnotationStoreResponseTypeDef:
        """
        Creates an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_annotation_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#create_annotation_store)
        """

    def create_annotation_store_version(
        self, **kwargs: Unpack[CreateAnnotationStoreVersionRequestRequestTypeDef]
    ) -> CreateAnnotationStoreVersionResponseTypeDef:
        """
        Creates a new version of an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_annotation_store_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#create_annotation_store_version)
        """

    def create_multipart_read_set_upload(
        self, **kwargs: Unpack[CreateMultipartReadSetUploadRequestRequestTypeDef]
    ) -> CreateMultipartReadSetUploadResponseTypeDef:
        """
        Begins a multipart read set upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_multipart_read_set_upload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#create_multipart_read_set_upload)
        """

    def create_reference_store(
        self, **kwargs: Unpack[CreateReferenceStoreRequestRequestTypeDef]
    ) -> CreateReferenceStoreResponseTypeDef:
        """
        Creates a reference store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_reference_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#create_reference_store)
        """

    def create_run_cache(
        self, **kwargs: Unpack[CreateRunCacheRequestRequestTypeDef]
    ) -> CreateRunCacheResponseTypeDef:
        """
        You can create a run cache to save the task outputs from completed tasks in a
        run for a private workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_run_cache.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#create_run_cache)
        """

    def create_run_group(
        self, **kwargs: Unpack[CreateRunGroupRequestRequestTypeDef]
    ) -> CreateRunGroupResponseTypeDef:
        """
        You can optionally create a run group to limit the compute resources for the
        runs that you add to the group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_run_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#create_run_group)
        """

    def create_sequence_store(
        self, **kwargs: Unpack[CreateSequenceStoreRequestRequestTypeDef]
    ) -> CreateSequenceStoreResponseTypeDef:
        """
        Creates a sequence store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_sequence_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#create_sequence_store)
        """

    def create_share(
        self, **kwargs: Unpack[CreateShareRequestRequestTypeDef]
    ) -> CreateShareResponseTypeDef:
        """
        Creates a cross-account shared resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#create_share)
        """

    def create_variant_store(
        self, **kwargs: Unpack[CreateVariantStoreRequestRequestTypeDef]
    ) -> CreateVariantStoreResponseTypeDef:
        """
        Creates a variant store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_variant_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#create_variant_store)
        """

    def create_workflow(
        self, **kwargs: Unpack[CreateWorkflowRequestRequestTypeDef]
    ) -> CreateWorkflowResponseTypeDef:
        """
        Creates a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/create_workflow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#create_workflow)
        """

    def delete_annotation_store(
        self, **kwargs: Unpack[DeleteAnnotationStoreRequestRequestTypeDef]
    ) -> DeleteAnnotationStoreResponseTypeDef:
        """
        Deletes an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_annotation_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#delete_annotation_store)
        """

    def delete_annotation_store_versions(
        self, **kwargs: Unpack[DeleteAnnotationStoreVersionsRequestRequestTypeDef]
    ) -> DeleteAnnotationStoreVersionsResponseTypeDef:
        """
        Deletes one or multiple versions of an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_annotation_store_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#delete_annotation_store_versions)
        """

    def delete_reference(
        self, **kwargs: Unpack[DeleteReferenceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a genome reference.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_reference.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#delete_reference)
        """

    def delete_reference_store(
        self, **kwargs: Unpack[DeleteReferenceStoreRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a genome reference store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_reference_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#delete_reference_store)
        """

    def delete_run(
        self, **kwargs: Unpack[DeleteRunRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_run.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#delete_run)
        """

    def delete_run_cache(
        self, **kwargs: Unpack[DeleteRunCacheRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a run cache.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_run_cache.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#delete_run_cache)
        """

    def delete_run_group(
        self, **kwargs: Unpack[DeleteRunGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a workflow run group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_run_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#delete_run_group)
        """

    def delete_s3_access_policy(
        self, **kwargs: Unpack[DeleteS3AccessPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an access policy for the specified store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_s3_access_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#delete_s3_access_policy)
        """

    def delete_sequence_store(
        self, **kwargs: Unpack[DeleteSequenceStoreRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a sequence store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_sequence_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#delete_sequence_store)
        """

    def delete_share(
        self, **kwargs: Unpack[DeleteShareRequestRequestTypeDef]
    ) -> DeleteShareResponseTypeDef:
        """
        Deletes a resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#delete_share)
        """

    def delete_variant_store(
        self, **kwargs: Unpack[DeleteVariantStoreRequestRequestTypeDef]
    ) -> DeleteVariantStoreResponseTypeDef:
        """
        Deletes a variant store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_variant_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#delete_variant_store)
        """

    def delete_workflow(
        self, **kwargs: Unpack[DeleteWorkflowRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/delete_workflow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#delete_workflow)
        """

    def get_annotation_import_job(
        self, **kwargs: Unpack[GetAnnotationImportRequestRequestTypeDef]
    ) -> GetAnnotationImportResponseTypeDef:
        """
        Gets information about an annotation import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_annotation_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_annotation_import_job)
        """

    def get_annotation_store(
        self, **kwargs: Unpack[GetAnnotationStoreRequestRequestTypeDef]
    ) -> GetAnnotationStoreResponseTypeDef:
        """
        Gets information about an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_annotation_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_annotation_store)
        """

    def get_annotation_store_version(
        self, **kwargs: Unpack[GetAnnotationStoreVersionRequestRequestTypeDef]
    ) -> GetAnnotationStoreVersionResponseTypeDef:
        """
        Retrieves the metadata for an annotation store version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_annotation_store_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_annotation_store_version)
        """

    def get_read_set(
        self, **kwargs: Unpack[GetReadSetRequestRequestTypeDef]
    ) -> GetReadSetResponseTypeDef:
        """
        Gets a file from a read set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_read_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_read_set)
        """

    def get_read_set_activation_job(
        self, **kwargs: Unpack[GetReadSetActivationJobRequestRequestTypeDef]
    ) -> GetReadSetActivationJobResponseTypeDef:
        """
        Gets information about a read set activation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_read_set_activation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_read_set_activation_job)
        """

    def get_read_set_export_job(
        self, **kwargs: Unpack[GetReadSetExportJobRequestRequestTypeDef]
    ) -> GetReadSetExportJobResponseTypeDef:
        """
        Gets information about a read set export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_read_set_export_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_read_set_export_job)
        """

    def get_read_set_import_job(
        self, **kwargs: Unpack[GetReadSetImportJobRequestRequestTypeDef]
    ) -> GetReadSetImportJobResponseTypeDef:
        """
        Gets information about a read set import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_read_set_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_read_set_import_job)
        """

    def get_read_set_metadata(
        self, **kwargs: Unpack[GetReadSetMetadataRequestRequestTypeDef]
    ) -> GetReadSetMetadataResponseTypeDef:
        """
        Gets details about a read set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_read_set_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_read_set_metadata)
        """

    def get_reference(
        self, **kwargs: Unpack[GetReferenceRequestRequestTypeDef]
    ) -> GetReferenceResponseTypeDef:
        """
        Gets a reference file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_reference.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_reference)
        """

    def get_reference_import_job(
        self, **kwargs: Unpack[GetReferenceImportJobRequestRequestTypeDef]
    ) -> GetReferenceImportJobResponseTypeDef:
        """
        Gets information about a reference import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_reference_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_reference_import_job)
        """

    def get_reference_metadata(
        self, **kwargs: Unpack[GetReferenceMetadataRequestRequestTypeDef]
    ) -> GetReferenceMetadataResponseTypeDef:
        """
        Gets information about a genome reference's metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_reference_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_reference_metadata)
        """

    def get_reference_store(
        self, **kwargs: Unpack[GetReferenceStoreRequestRequestTypeDef]
    ) -> GetReferenceStoreResponseTypeDef:
        """
        Gets information about a reference store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_reference_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_reference_store)
        """

    def get_run(self, **kwargs: Unpack[GetRunRequestRequestTypeDef]) -> GetRunResponseTypeDef:
        """
        Gets information about a workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_run.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_run)
        """

    def get_run_cache(
        self, **kwargs: Unpack[GetRunCacheRequestRequestTypeDef]
    ) -> GetRunCacheResponseTypeDef:
        """
        Retrieve the details for the specified run cache.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_run_cache.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_run_cache)
        """

    def get_run_group(
        self, **kwargs: Unpack[GetRunGroupRequestRequestTypeDef]
    ) -> GetRunGroupResponseTypeDef:
        """
        Gets information about a workflow run group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_run_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_run_group)
        """

    def get_run_task(
        self, **kwargs: Unpack[GetRunTaskRequestRequestTypeDef]
    ) -> GetRunTaskResponseTypeDef:
        """
        Gets information about a workflow run task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_run_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_run_task)
        """

    def get_s3_access_policy(
        self, **kwargs: Unpack[GetS3AccessPolicyRequestRequestTypeDef]
    ) -> GetS3AccessPolicyResponseTypeDef:
        """
        Retrieves details about an access policy on a given store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_s3_access_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_s3_access_policy)
        """

    def get_sequence_store(
        self, **kwargs: Unpack[GetSequenceStoreRequestRequestTypeDef]
    ) -> GetSequenceStoreResponseTypeDef:
        """
        Gets information about a sequence store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_sequence_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_sequence_store)
        """

    def get_share(self, **kwargs: Unpack[GetShareRequestRequestTypeDef]) -> GetShareResponseTypeDef:
        """
        Retrieves the metadata for the specified resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_share)
        """

    def get_variant_import_job(
        self, **kwargs: Unpack[GetVariantImportRequestRequestTypeDef]
    ) -> GetVariantImportResponseTypeDef:
        """
        Gets information about a variant import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_variant_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_variant_import_job)
        """

    def get_variant_store(
        self, **kwargs: Unpack[GetVariantStoreRequestRequestTypeDef]
    ) -> GetVariantStoreResponseTypeDef:
        """
        Gets information about a variant store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_variant_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_variant_store)
        """

    def get_workflow(
        self, **kwargs: Unpack[GetWorkflowRequestRequestTypeDef]
    ) -> GetWorkflowResponseTypeDef:
        """
        Gets information about a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_workflow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_workflow)
        """

    def list_annotation_import_jobs(
        self, **kwargs: Unpack[ListAnnotationImportJobsRequestRequestTypeDef]
    ) -> ListAnnotationImportJobsResponseTypeDef:
        """
        Retrieves a list of annotation import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_annotation_import_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_annotation_import_jobs)
        """

    def list_annotation_store_versions(
        self, **kwargs: Unpack[ListAnnotationStoreVersionsRequestRequestTypeDef]
    ) -> ListAnnotationStoreVersionsResponseTypeDef:
        """
        Lists the versions of an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_annotation_store_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_annotation_store_versions)
        """

    def list_annotation_stores(
        self, **kwargs: Unpack[ListAnnotationStoresRequestRequestTypeDef]
    ) -> ListAnnotationStoresResponseTypeDef:
        """
        Retrieves a list of annotation stores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_annotation_stores.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_annotation_stores)
        """

    def list_multipart_read_set_uploads(
        self, **kwargs: Unpack[ListMultipartReadSetUploadsRequestRequestTypeDef]
    ) -> ListMultipartReadSetUploadsResponseTypeDef:
        """
        Lists multipart read set uploads and for in progress uploads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_multipart_read_set_uploads.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_multipart_read_set_uploads)
        """

    def list_read_set_activation_jobs(
        self, **kwargs: Unpack[ListReadSetActivationJobsRequestRequestTypeDef]
    ) -> ListReadSetActivationJobsResponseTypeDef:
        """
        Retrieves a list of read set activation jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_read_set_activation_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_read_set_activation_jobs)
        """

    def list_read_set_export_jobs(
        self, **kwargs: Unpack[ListReadSetExportJobsRequestRequestTypeDef]
    ) -> ListReadSetExportJobsResponseTypeDef:
        """
        Retrieves a list of read set export jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_read_set_export_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_read_set_export_jobs)
        """

    def list_read_set_import_jobs(
        self, **kwargs: Unpack[ListReadSetImportJobsRequestRequestTypeDef]
    ) -> ListReadSetImportJobsResponseTypeDef:
        """
        Retrieves a list of read set import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_read_set_import_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_read_set_import_jobs)
        """

    def list_read_set_upload_parts(
        self, **kwargs: Unpack[ListReadSetUploadPartsRequestRequestTypeDef]
    ) -> ListReadSetUploadPartsResponseTypeDef:
        """
        This operation will list all parts in a requested multipart upload for a
        sequence store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_read_set_upload_parts.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_read_set_upload_parts)
        """

    def list_read_sets(
        self, **kwargs: Unpack[ListReadSetsRequestRequestTypeDef]
    ) -> ListReadSetsResponseTypeDef:
        """
        Retrieves a list of read sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_read_sets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_read_sets)
        """

    def list_reference_import_jobs(
        self, **kwargs: Unpack[ListReferenceImportJobsRequestRequestTypeDef]
    ) -> ListReferenceImportJobsResponseTypeDef:
        """
        Retrieves a list of reference import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_reference_import_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_reference_import_jobs)
        """

    def list_reference_stores(
        self, **kwargs: Unpack[ListReferenceStoresRequestRequestTypeDef]
    ) -> ListReferenceStoresResponseTypeDef:
        """
        Retrieves a list of reference stores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_reference_stores.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_reference_stores)
        """

    def list_references(
        self, **kwargs: Unpack[ListReferencesRequestRequestTypeDef]
    ) -> ListReferencesResponseTypeDef:
        """
        Retrieves a list of references.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_references.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_references)
        """

    def list_run_caches(
        self, **kwargs: Unpack[ListRunCachesRequestRequestTypeDef]
    ) -> ListRunCachesResponseTypeDef:
        """
        Retrieves a list of your run caches.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_run_caches.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_run_caches)
        """

    def list_run_groups(
        self, **kwargs: Unpack[ListRunGroupsRequestRequestTypeDef]
    ) -> ListRunGroupsResponseTypeDef:
        """
        Retrieves a list of run groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_run_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_run_groups)
        """

    def list_run_tasks(
        self, **kwargs: Unpack[ListRunTasksRequestRequestTypeDef]
    ) -> ListRunTasksResponseTypeDef:
        """
        Retrieves a list of tasks for a run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_run_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_run_tasks)
        """

    def list_runs(self, **kwargs: Unpack[ListRunsRequestRequestTypeDef]) -> ListRunsResponseTypeDef:
        """
        Retrieves a list of runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_runs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_runs)
        """

    def list_sequence_stores(
        self, **kwargs: Unpack[ListSequenceStoresRequestRequestTypeDef]
    ) -> ListSequenceStoresResponseTypeDef:
        """
        Retrieves a list of sequence stores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_sequence_stores.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_sequence_stores)
        """

    def list_shares(
        self, **kwargs: Unpack[ListSharesRequestRequestTypeDef]
    ) -> ListSharesResponseTypeDef:
        """
        Retrieves the resource shares associated with an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_shares.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_shares)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves a list of tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_tags_for_resource)
        """

    def list_variant_import_jobs(
        self, **kwargs: Unpack[ListVariantImportJobsRequestRequestTypeDef]
    ) -> ListVariantImportJobsResponseTypeDef:
        """
        Retrieves a list of variant import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_variant_import_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_variant_import_jobs)
        """

    def list_variant_stores(
        self, **kwargs: Unpack[ListVariantStoresRequestRequestTypeDef]
    ) -> ListVariantStoresResponseTypeDef:
        """
        Retrieves a list of variant stores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_variant_stores.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_variant_stores)
        """

    def list_workflows(
        self, **kwargs: Unpack[ListWorkflowsRequestRequestTypeDef]
    ) -> ListWorkflowsResponseTypeDef:
        """
        Retrieves a list of workflows.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/list_workflows.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#list_workflows)
        """

    def put_s3_access_policy(
        self, **kwargs: Unpack[PutS3AccessPolicyRequestRequestTypeDef]
    ) -> PutS3AccessPolicyResponseTypeDef:
        """
        Adds an access policy to the specified store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/put_s3_access_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#put_s3_access_policy)
        """

    def start_annotation_import_job(
        self, **kwargs: Unpack[StartAnnotationImportRequestRequestTypeDef]
    ) -> StartAnnotationImportResponseTypeDef:
        """
        Starts an annotation import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/start_annotation_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#start_annotation_import_job)
        """

    def start_read_set_activation_job(
        self, **kwargs: Unpack[StartReadSetActivationJobRequestRequestTypeDef]
    ) -> StartReadSetActivationJobResponseTypeDef:
        """
        Activates an archived read set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/start_read_set_activation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#start_read_set_activation_job)
        """

    def start_read_set_export_job(
        self, **kwargs: Unpack[StartReadSetExportJobRequestRequestTypeDef]
    ) -> StartReadSetExportJobResponseTypeDef:
        """
        Exports a read set to Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/start_read_set_export_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#start_read_set_export_job)
        """

    def start_read_set_import_job(
        self, **kwargs: Unpack[StartReadSetImportJobRequestRequestTypeDef]
    ) -> StartReadSetImportJobResponseTypeDef:
        """
        Starts a read set import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/start_read_set_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#start_read_set_import_job)
        """

    def start_reference_import_job(
        self, **kwargs: Unpack[StartReferenceImportJobRequestRequestTypeDef]
    ) -> StartReferenceImportJobResponseTypeDef:
        """
        Starts a reference import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/start_reference_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#start_reference_import_job)
        """

    def start_run(self, **kwargs: Unpack[StartRunRequestRequestTypeDef]) -> StartRunResponseTypeDef:
        """
        Starts a workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/start_run.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#start_run)
        """

    def start_variant_import_job(
        self, **kwargs: Unpack[StartVariantImportRequestRequestTypeDef]
    ) -> StartVariantImportResponseTypeDef:
        """
        Starts a variant import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/start_variant_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#start_variant_import_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#untag_resource)
        """

    def update_annotation_store(
        self, **kwargs: Unpack[UpdateAnnotationStoreRequestRequestTypeDef]
    ) -> UpdateAnnotationStoreResponseTypeDef:
        """
        Updates an annotation store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/update_annotation_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#update_annotation_store)
        """

    def update_annotation_store_version(
        self, **kwargs: Unpack[UpdateAnnotationStoreVersionRequestRequestTypeDef]
    ) -> UpdateAnnotationStoreVersionResponseTypeDef:
        """
        Updates the description of an annotation store version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/update_annotation_store_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#update_annotation_store_version)
        """

    def update_run_cache(
        self, **kwargs: Unpack[UpdateRunCacheRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Update a run cache.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/update_run_cache.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#update_run_cache)
        """

    def update_run_group(
        self, **kwargs: Unpack[UpdateRunGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a run group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/update_run_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#update_run_group)
        """

    def update_sequence_store(
        self, **kwargs: Unpack[UpdateSequenceStoreRequestRequestTypeDef]
    ) -> UpdateSequenceStoreResponseTypeDef:
        """
        Update one or more parameters for the sequence store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/update_sequence_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#update_sequence_store)
        """

    def update_variant_store(
        self, **kwargs: Unpack[UpdateVariantStoreRequestRequestTypeDef]
    ) -> UpdateVariantStoreResponseTypeDef:
        """
        Updates a variant store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/update_variant_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#update_variant_store)
        """

    def update_workflow(
        self, **kwargs: Unpack[UpdateWorkflowRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/update_workflow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#update_workflow)
        """

    def upload_read_set_part(
        self, **kwargs: Unpack[UploadReadSetPartRequestRequestTypeDef]
    ) -> UploadReadSetPartResponseTypeDef:
        """
        This operation uploads a specific part of a read set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/upload_read_set_part.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#upload_read_set_part)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_annotation_import_jobs"]
    ) -> ListAnnotationImportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_annotation_store_versions"]
    ) -> ListAnnotationStoreVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_annotation_stores"]
    ) -> ListAnnotationStoresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_multipart_read_set_uploads"]
    ) -> ListMultipartReadSetUploadsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_read_set_activation_jobs"]
    ) -> ListReadSetActivationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_read_set_export_jobs"]
    ) -> ListReadSetExportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_read_set_import_jobs"]
    ) -> ListReadSetImportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_read_set_upload_parts"]
    ) -> ListReadSetUploadPartsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_read_sets"]) -> ListReadSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_reference_import_jobs"]
    ) -> ListReferenceImportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_reference_stores"]
    ) -> ListReferenceStoresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_references"]) -> ListReferencesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_run_caches"]) -> ListRunCachesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_run_groups"]) -> ListRunGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_run_tasks"]) -> ListRunTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_runs"]) -> ListRunsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_sequence_stores"]
    ) -> ListSequenceStoresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_shares"]) -> ListSharesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_variant_import_jobs"]
    ) -> ListVariantImportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_variant_stores"]
    ) -> ListVariantStoresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workflows"]) -> ListWorkflowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["annotation_import_job_created"]
    ) -> AnnotationImportJobCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["annotation_store_created"]
    ) -> AnnotationStoreCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["annotation_store_deleted"]
    ) -> AnnotationStoreDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["annotation_store_version_created"]
    ) -> AnnotationStoreVersionCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["annotation_store_version_deleted"]
    ) -> AnnotationStoreVersionDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["read_set_activation_job_completed"]
    ) -> ReadSetActivationJobCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["read_set_export_job_completed"]
    ) -> ReadSetExportJobCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["read_set_import_job_completed"]
    ) -> ReadSetImportJobCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["reference_import_job_completed"]
    ) -> ReferenceImportJobCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["run_completed"]) -> RunCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["run_running"]) -> RunRunningWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["task_completed"]) -> TaskCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["task_running"]) -> TaskRunningWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["variant_import_job_created"]
    ) -> VariantImportJobCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["variant_store_created"]
    ) -> VariantStoreCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["variant_store_deleted"]
    ) -> VariantStoreDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["workflow_active"]) -> WorkflowActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/omics/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_omics/client/#get_waiter)
        """
