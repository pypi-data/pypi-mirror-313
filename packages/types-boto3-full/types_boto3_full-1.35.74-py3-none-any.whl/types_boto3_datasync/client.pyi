"""
Type annotations for datasync service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_datasync.client import DataSyncClient

    session = Session()
    client: DataSyncClient = session.client("datasync")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeStorageSystemResourceMetricsPaginator,
    ListAgentsPaginator,
    ListDiscoveryJobsPaginator,
    ListLocationsPaginator,
    ListStorageSystemsPaginator,
    ListTagsForResourcePaginator,
    ListTaskExecutionsPaginator,
    ListTasksPaginator,
)
from .type_defs import (
    AddStorageSystemRequestRequestTypeDef,
    AddStorageSystemResponseTypeDef,
    CancelTaskExecutionRequestRequestTypeDef,
    CreateAgentRequestRequestTypeDef,
    CreateAgentResponseTypeDef,
    CreateLocationAzureBlobRequestRequestTypeDef,
    CreateLocationAzureBlobResponseTypeDef,
    CreateLocationEfsRequestRequestTypeDef,
    CreateLocationEfsResponseTypeDef,
    CreateLocationFsxLustreRequestRequestTypeDef,
    CreateLocationFsxLustreResponseTypeDef,
    CreateLocationFsxOntapRequestRequestTypeDef,
    CreateLocationFsxOntapResponseTypeDef,
    CreateLocationFsxOpenZfsRequestRequestTypeDef,
    CreateLocationFsxOpenZfsResponseTypeDef,
    CreateLocationFsxWindowsRequestRequestTypeDef,
    CreateLocationFsxWindowsResponseTypeDef,
    CreateLocationHdfsRequestRequestTypeDef,
    CreateLocationHdfsResponseTypeDef,
    CreateLocationNfsRequestRequestTypeDef,
    CreateLocationNfsResponseTypeDef,
    CreateLocationObjectStorageRequestRequestTypeDef,
    CreateLocationObjectStorageResponseTypeDef,
    CreateLocationS3RequestRequestTypeDef,
    CreateLocationS3ResponseTypeDef,
    CreateLocationSmbRequestRequestTypeDef,
    CreateLocationSmbResponseTypeDef,
    CreateTaskRequestRequestTypeDef,
    CreateTaskResponseTypeDef,
    DeleteAgentRequestRequestTypeDef,
    DeleteLocationRequestRequestTypeDef,
    DeleteTaskRequestRequestTypeDef,
    DescribeAgentRequestRequestTypeDef,
    DescribeAgentResponseTypeDef,
    DescribeDiscoveryJobRequestRequestTypeDef,
    DescribeDiscoveryJobResponseTypeDef,
    DescribeLocationAzureBlobRequestRequestTypeDef,
    DescribeLocationAzureBlobResponseTypeDef,
    DescribeLocationEfsRequestRequestTypeDef,
    DescribeLocationEfsResponseTypeDef,
    DescribeLocationFsxLustreRequestRequestTypeDef,
    DescribeLocationFsxLustreResponseTypeDef,
    DescribeLocationFsxOntapRequestRequestTypeDef,
    DescribeLocationFsxOntapResponseTypeDef,
    DescribeLocationFsxOpenZfsRequestRequestTypeDef,
    DescribeLocationFsxOpenZfsResponseTypeDef,
    DescribeLocationFsxWindowsRequestRequestTypeDef,
    DescribeLocationFsxWindowsResponseTypeDef,
    DescribeLocationHdfsRequestRequestTypeDef,
    DescribeLocationHdfsResponseTypeDef,
    DescribeLocationNfsRequestRequestTypeDef,
    DescribeLocationNfsResponseTypeDef,
    DescribeLocationObjectStorageRequestRequestTypeDef,
    DescribeLocationObjectStorageResponseTypeDef,
    DescribeLocationS3RequestRequestTypeDef,
    DescribeLocationS3ResponseTypeDef,
    DescribeLocationSmbRequestRequestTypeDef,
    DescribeLocationSmbResponseTypeDef,
    DescribeStorageSystemRequestRequestTypeDef,
    DescribeStorageSystemResourceMetricsRequestRequestTypeDef,
    DescribeStorageSystemResourceMetricsResponseTypeDef,
    DescribeStorageSystemResourcesRequestRequestTypeDef,
    DescribeStorageSystemResourcesResponseTypeDef,
    DescribeStorageSystemResponseTypeDef,
    DescribeTaskExecutionRequestRequestTypeDef,
    DescribeTaskExecutionResponseTypeDef,
    DescribeTaskRequestRequestTypeDef,
    DescribeTaskResponseTypeDef,
    GenerateRecommendationsRequestRequestTypeDef,
    ListAgentsRequestRequestTypeDef,
    ListAgentsResponseTypeDef,
    ListDiscoveryJobsRequestRequestTypeDef,
    ListDiscoveryJobsResponseTypeDef,
    ListLocationsRequestRequestTypeDef,
    ListLocationsResponseTypeDef,
    ListStorageSystemsRequestRequestTypeDef,
    ListStorageSystemsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTaskExecutionsRequestRequestTypeDef,
    ListTaskExecutionsResponseTypeDef,
    ListTasksRequestRequestTypeDef,
    ListTasksResponseTypeDef,
    RemoveStorageSystemRequestRequestTypeDef,
    StartDiscoveryJobRequestRequestTypeDef,
    StartDiscoveryJobResponseTypeDef,
    StartTaskExecutionRequestRequestTypeDef,
    StartTaskExecutionResponseTypeDef,
    StopDiscoveryJobRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAgentRequestRequestTypeDef,
    UpdateDiscoveryJobRequestRequestTypeDef,
    UpdateLocationAzureBlobRequestRequestTypeDef,
    UpdateLocationHdfsRequestRequestTypeDef,
    UpdateLocationNfsRequestRequestTypeDef,
    UpdateLocationObjectStorageRequestRequestTypeDef,
    UpdateLocationSmbRequestRequestTypeDef,
    UpdateStorageSystemRequestRequestTypeDef,
    UpdateTaskExecutionRequestRequestTypeDef,
    UpdateTaskRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("DataSyncClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]

class DataSyncClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DataSyncClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#close)
        """

    def add_storage_system(
        self, **kwargs: Unpack[AddStorageSystemRequestRequestTypeDef]
    ) -> AddStorageSystemResponseTypeDef:
        """
        Creates an Amazon Web Services resource for an on-premises storage system that
        you want DataSync Discovery to collect information about.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/add_storage_system.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#add_storage_system)
        """

    def cancel_task_execution(
        self, **kwargs: Unpack[CancelTaskExecutionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops an DataSync task execution that's in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/cancel_task_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#cancel_task_execution)
        """

    def create_agent(
        self, **kwargs: Unpack[CreateAgentRequestRequestTypeDef]
    ) -> CreateAgentResponseTypeDef:
        """
        Activates an DataSync agent that you deploy in your storage environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/create_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#create_agent)
        """

    def create_location_azure_blob(
        self, **kwargs: Unpack[CreateLocationAzureBlobRequestRequestTypeDef]
    ) -> CreateLocationAzureBlobResponseTypeDef:
        """
        Creates a transfer <i>location</i> for a Microsoft Azure Blob Storage container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/create_location_azure_blob.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#create_location_azure_blob)
        """

    def create_location_efs(
        self, **kwargs: Unpack[CreateLocationEfsRequestRequestTypeDef]
    ) -> CreateLocationEfsResponseTypeDef:
        """
        Creates a transfer <i>location</i> for an Amazon EFS file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/create_location_efs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#create_location_efs)
        """

    def create_location_fsx_lustre(
        self, **kwargs: Unpack[CreateLocationFsxLustreRequestRequestTypeDef]
    ) -> CreateLocationFsxLustreResponseTypeDef:
        """
        Creates a transfer <i>location</i> for an Amazon FSx for Lustre file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/create_location_fsx_lustre.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#create_location_fsx_lustre)
        """

    def create_location_fsx_ontap(
        self, **kwargs: Unpack[CreateLocationFsxOntapRequestRequestTypeDef]
    ) -> CreateLocationFsxOntapResponseTypeDef:
        """
        Creates a transfer <i>location</i> for an Amazon FSx for NetApp ONTAP file
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/create_location_fsx_ontap.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#create_location_fsx_ontap)
        """

    def create_location_fsx_open_zfs(
        self, **kwargs: Unpack[CreateLocationFsxOpenZfsRequestRequestTypeDef]
    ) -> CreateLocationFsxOpenZfsResponseTypeDef:
        """
        Creates a transfer <i>location</i> for an Amazon FSx for OpenZFS file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/create_location_fsx_open_zfs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#create_location_fsx_open_zfs)
        """

    def create_location_fsx_windows(
        self, **kwargs: Unpack[CreateLocationFsxWindowsRequestRequestTypeDef]
    ) -> CreateLocationFsxWindowsResponseTypeDef:
        """
        Creates a transfer <i>location</i> for an Amazon FSx for Windows File Server
        file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/create_location_fsx_windows.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#create_location_fsx_windows)
        """

    def create_location_hdfs(
        self, **kwargs: Unpack[CreateLocationHdfsRequestRequestTypeDef]
    ) -> CreateLocationHdfsResponseTypeDef:
        """
        Creates a transfer <i>location</i> for a Hadoop Distributed File System (HDFS).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/create_location_hdfs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#create_location_hdfs)
        """

    def create_location_nfs(
        self, **kwargs: Unpack[CreateLocationNfsRequestRequestTypeDef]
    ) -> CreateLocationNfsResponseTypeDef:
        """
        Creates a transfer <i>location</i> for a Network File System (NFS) file server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/create_location_nfs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#create_location_nfs)
        """

    def create_location_object_storage(
        self, **kwargs: Unpack[CreateLocationObjectStorageRequestRequestTypeDef]
    ) -> CreateLocationObjectStorageResponseTypeDef:
        """
        Creates a transfer <i>location</i> for an object storage system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/create_location_object_storage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#create_location_object_storage)
        """

    def create_location_s3(
        self, **kwargs: Unpack[CreateLocationS3RequestRequestTypeDef]
    ) -> CreateLocationS3ResponseTypeDef:
        """
        Creates a transfer <i>location</i> for an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/create_location_s3.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#create_location_s3)
        """

    def create_location_smb(
        self, **kwargs: Unpack[CreateLocationSmbRequestRequestTypeDef]
    ) -> CreateLocationSmbResponseTypeDef:
        """
        Creates a transfer <i>location</i> for a Server Message Block (SMB) file server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/create_location_smb.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#create_location_smb)
        """

    def create_task(
        self, **kwargs: Unpack[CreateTaskRequestRequestTypeDef]
    ) -> CreateTaskResponseTypeDef:
        """
        Configures a <i>task</i>, which defines where and how DataSync transfers your
        data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/create_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#create_task)
        """

    def delete_agent(self, **kwargs: Unpack[DeleteAgentRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes an DataSync agent resource from your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/delete_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#delete_agent)
        """

    def delete_location(
        self, **kwargs: Unpack[DeleteLocationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a transfer location resource from DataSync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/delete_location.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#delete_location)
        """

    def delete_task(self, **kwargs: Unpack[DeleteTaskRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a transfer task resource from DataSync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/delete_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#delete_task)
        """

    def describe_agent(
        self, **kwargs: Unpack[DescribeAgentRequestRequestTypeDef]
    ) -> DescribeAgentResponseTypeDef:
        """
        Returns information about an DataSync agent, such as its name, service endpoint
        type, and status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_agent)
        """

    def describe_discovery_job(
        self, **kwargs: Unpack[DescribeDiscoveryJobRequestRequestTypeDef]
    ) -> DescribeDiscoveryJobResponseTypeDef:
        """
        Returns information about a DataSync discovery job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_discovery_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_discovery_job)
        """

    def describe_location_azure_blob(
        self, **kwargs: Unpack[DescribeLocationAzureBlobRequestRequestTypeDef]
    ) -> DescribeLocationAzureBlobResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for Microsoft Azure
        Blob Storage is configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_location_azure_blob.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_location_azure_blob)
        """

    def describe_location_efs(
        self, **kwargs: Unpack[DescribeLocationEfsRequestRequestTypeDef]
    ) -> DescribeLocationEfsResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for an Amazon EFS file
        system is configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_location_efs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_location_efs)
        """

    def describe_location_fsx_lustre(
        self, **kwargs: Unpack[DescribeLocationFsxLustreRequestRequestTypeDef]
    ) -> DescribeLocationFsxLustreResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for an Amazon FSx for
        Lustre file system is configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_location_fsx_lustre.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_location_fsx_lustre)
        """

    def describe_location_fsx_ontap(
        self, **kwargs: Unpack[DescribeLocationFsxOntapRequestRequestTypeDef]
    ) -> DescribeLocationFsxOntapResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for an Amazon FSx for
        NetApp ONTAP file system is configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_location_fsx_ontap.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_location_fsx_ontap)
        """

    def describe_location_fsx_open_zfs(
        self, **kwargs: Unpack[DescribeLocationFsxOpenZfsRequestRequestTypeDef]
    ) -> DescribeLocationFsxOpenZfsResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for an Amazon FSx for
        OpenZFS file system is configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_location_fsx_open_zfs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_location_fsx_open_zfs)
        """

    def describe_location_fsx_windows(
        self, **kwargs: Unpack[DescribeLocationFsxWindowsRequestRequestTypeDef]
    ) -> DescribeLocationFsxWindowsResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for an Amazon FSx for
        Windows File Server file system is configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_location_fsx_windows.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_location_fsx_windows)
        """

    def describe_location_hdfs(
        self, **kwargs: Unpack[DescribeLocationHdfsRequestRequestTypeDef]
    ) -> DescribeLocationHdfsResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for a Hadoop
        Distributed File System (HDFS) is configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_location_hdfs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_location_hdfs)
        """

    def describe_location_nfs(
        self, **kwargs: Unpack[DescribeLocationNfsRequestRequestTypeDef]
    ) -> DescribeLocationNfsResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for a Network File
        System (NFS) file server is configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_location_nfs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_location_nfs)
        """

    def describe_location_object_storage(
        self, **kwargs: Unpack[DescribeLocationObjectStorageRequestRequestTypeDef]
    ) -> DescribeLocationObjectStorageResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for an object storage
        system is configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_location_object_storage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_location_object_storage)
        """

    def describe_location_s3(
        self, **kwargs: Unpack[DescribeLocationS3RequestRequestTypeDef]
    ) -> DescribeLocationS3ResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for an S3 bucket is
        configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_location_s3.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_location_s3)
        """

    def describe_location_smb(
        self, **kwargs: Unpack[DescribeLocationSmbRequestRequestTypeDef]
    ) -> DescribeLocationSmbResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for a Server Message
        Block (SMB) file server is configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_location_smb.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_location_smb)
        """

    def describe_storage_system(
        self, **kwargs: Unpack[DescribeStorageSystemRequestRequestTypeDef]
    ) -> DescribeStorageSystemResponseTypeDef:
        """
        Returns information about an on-premises storage system that you're using with
        DataSync Discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_storage_system.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_storage_system)
        """

    def describe_storage_system_resource_metrics(
        self, **kwargs: Unpack[DescribeStorageSystemResourceMetricsRequestRequestTypeDef]
    ) -> DescribeStorageSystemResourceMetricsResponseTypeDef:
        """
        Returns information, including performance data and capacity usage, which
        DataSync Discovery collects about a specific resource in your-premises storage
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_storage_system_resource_metrics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_storage_system_resource_metrics)
        """

    def describe_storage_system_resources(
        self, **kwargs: Unpack[DescribeStorageSystemResourcesRequestRequestTypeDef]
    ) -> DescribeStorageSystemResourcesResponseTypeDef:
        """
        Returns information that DataSync Discovery collects about resources in your
        on-premises storage system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_storage_system_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_storage_system_resources)
        """

    def describe_task(
        self, **kwargs: Unpack[DescribeTaskRequestRequestTypeDef]
    ) -> DescribeTaskResponseTypeDef:
        """
        Provides information about a <i>task</i>, which defines where and how DataSync
        transfers your data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_task)
        """

    def describe_task_execution(
        self, **kwargs: Unpack[DescribeTaskExecutionRequestRequestTypeDef]
    ) -> DescribeTaskExecutionResponseTypeDef:
        """
        Provides information about an execution of your DataSync task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/describe_task_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#describe_task_execution)
        """

    def generate_recommendations(
        self, **kwargs: Unpack[GenerateRecommendationsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates recommendations about where to migrate your data to in Amazon Web
        Services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/generate_recommendations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#generate_recommendations)
        """

    def list_agents(
        self, **kwargs: Unpack[ListAgentsRequestRequestTypeDef]
    ) -> ListAgentsResponseTypeDef:
        """
        Returns a list of DataSync agents that belong to an Amazon Web Services account
        in the Amazon Web Services Region specified in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/list_agents.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#list_agents)
        """

    def list_discovery_jobs(
        self, **kwargs: Unpack[ListDiscoveryJobsRequestRequestTypeDef]
    ) -> ListDiscoveryJobsResponseTypeDef:
        """
        Provides a list of the existing discovery jobs in the Amazon Web Services
        Region and Amazon Web Services account where you're using DataSync Discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/list_discovery_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#list_discovery_jobs)
        """

    def list_locations(
        self, **kwargs: Unpack[ListLocationsRequestRequestTypeDef]
    ) -> ListLocationsResponseTypeDef:
        """
        Returns a list of source and destination locations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/list_locations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#list_locations)
        """

    def list_storage_systems(
        self, **kwargs: Unpack[ListStorageSystemsRequestRequestTypeDef]
    ) -> ListStorageSystemsResponseTypeDef:
        """
        Lists the on-premises storage systems that you're using with DataSync Discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/list_storage_systems.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#list_storage_systems)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns all the tags associated with an Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#list_tags_for_resource)
        """

    def list_task_executions(
        self, **kwargs: Unpack[ListTaskExecutionsRequestRequestTypeDef]
    ) -> ListTaskExecutionsResponseTypeDef:
        """
        Returns a list of executions for an DataSync transfer task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/list_task_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#list_task_executions)
        """

    def list_tasks(
        self, **kwargs: Unpack[ListTasksRequestRequestTypeDef]
    ) -> ListTasksResponseTypeDef:
        """
        Returns a list of the DataSync tasks you created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/list_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#list_tasks)
        """

    def remove_storage_system(
        self, **kwargs: Unpack[RemoveStorageSystemRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Permanently removes a storage system resource from DataSync Discovery,
        including the associated discovery jobs, collected data, and recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/remove_storage_system.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#remove_storage_system)
        """

    def start_discovery_job(
        self, **kwargs: Unpack[StartDiscoveryJobRequestRequestTypeDef]
    ) -> StartDiscoveryJobResponseTypeDef:
        """
        Runs a DataSync discovery job on your on-premises storage system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/start_discovery_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#start_discovery_job)
        """

    def start_task_execution(
        self, **kwargs: Unpack[StartTaskExecutionRequestRequestTypeDef]
    ) -> StartTaskExecutionResponseTypeDef:
        """
        Starts an DataSync transfer task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/start_task_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#start_task_execution)
        """

    def stop_discovery_job(
        self, **kwargs: Unpack[StopDiscoveryJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops a running DataSync discovery job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/stop_discovery_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#stop_discovery_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Applies a <i>tag</i> to an Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from an Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#untag_resource)
        """

    def update_agent(self, **kwargs: Unpack[UpdateAgentRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates the name of an DataSync agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/update_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#update_agent)
        """

    def update_discovery_job(
        self, **kwargs: Unpack[UpdateDiscoveryJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Edits a DataSync discovery job configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/update_discovery_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#update_discovery_job)
        """

    def update_location_azure_blob(
        self, **kwargs: Unpack[UpdateLocationAzureBlobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Modifies some configurations of the Microsoft Azure Blob Storage transfer
        location that you're using with DataSync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/update_location_azure_blob.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#update_location_azure_blob)
        """

    def update_location_hdfs(
        self, **kwargs: Unpack[UpdateLocationHdfsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates some parameters of a previously created location for a Hadoop
        Distributed File System cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/update_location_hdfs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#update_location_hdfs)
        """

    def update_location_nfs(
        self, **kwargs: Unpack[UpdateLocationNfsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Modifies some configurations of the Network File System (NFS) transfer location
        that you're using with DataSync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/update_location_nfs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#update_location_nfs)
        """

    def update_location_object_storage(
        self, **kwargs: Unpack[UpdateLocationObjectStorageRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates some parameters of an existing DataSync location for an object storage
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/update_location_object_storage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#update_location_object_storage)
        """

    def update_location_smb(
        self, **kwargs: Unpack[UpdateLocationSmbRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates some of the parameters of a Server Message Block (SMB) file server
        location that you can use for DataSync transfers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/update_location_smb.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#update_location_smb)
        """

    def update_storage_system(
        self, **kwargs: Unpack[UpdateStorageSystemRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Modifies some configurations of an on-premises storage system resource that
        you're using with DataSync Discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/update_storage_system.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#update_storage_system)
        """

    def update_task(self, **kwargs: Unpack[UpdateTaskRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates the configuration of a <i>task</i>, which defines where and how
        DataSync transfers your data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/update_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#update_task)
        """

    def update_task_execution(
        self, **kwargs: Unpack[UpdateTaskExecutionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the configuration of a running DataSync task execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/update_task_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#update_task_execution)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_storage_system_resource_metrics"]
    ) -> DescribeStorageSystemResourceMetricsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_agents"]) -> ListAgentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_discovery_jobs"]
    ) -> ListDiscoveryJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_locations"]) -> ListLocationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_storage_systems"]
    ) -> ListStorageSystemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_task_executions"]
    ) -> ListTaskExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tasks"]) -> ListTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datasync/client/#get_paginator)
        """
