"""
Type annotations for storagegateway service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_storagegateway.client import StorageGatewayClient

    session = Session()
    client: StorageGatewayClient = session.client("storagegateway")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeTapeArchivesPaginator,
    DescribeTapeRecoveryPointsPaginator,
    DescribeTapesPaginator,
    DescribeVTLDevicesPaginator,
    ListFileSharesPaginator,
    ListFileSystemAssociationsPaginator,
    ListGatewaysPaginator,
    ListTagsForResourcePaginator,
    ListTapePoolsPaginator,
    ListTapesPaginator,
    ListVolumesPaginator,
)
from .type_defs import (
    ActivateGatewayInputRequestTypeDef,
    ActivateGatewayOutputTypeDef,
    AddCacheInputRequestTypeDef,
    AddCacheOutputTypeDef,
    AddTagsToResourceInputRequestTypeDef,
    AddTagsToResourceOutputTypeDef,
    AddUploadBufferInputRequestTypeDef,
    AddUploadBufferOutputTypeDef,
    AddWorkingStorageInputRequestTypeDef,
    AddWorkingStorageOutputTypeDef,
    AssignTapePoolInputRequestTypeDef,
    AssignTapePoolOutputTypeDef,
    AssociateFileSystemInputRequestTypeDef,
    AssociateFileSystemOutputTypeDef,
    AttachVolumeInputRequestTypeDef,
    AttachVolumeOutputTypeDef,
    CancelArchivalInputRequestTypeDef,
    CancelArchivalOutputTypeDef,
    CancelRetrievalInputRequestTypeDef,
    CancelRetrievalOutputTypeDef,
    CreateCachediSCSIVolumeInputRequestTypeDef,
    CreateCachediSCSIVolumeOutputTypeDef,
    CreateNFSFileShareInputRequestTypeDef,
    CreateNFSFileShareOutputTypeDef,
    CreateSMBFileShareInputRequestTypeDef,
    CreateSMBFileShareOutputTypeDef,
    CreateSnapshotFromVolumeRecoveryPointInputRequestTypeDef,
    CreateSnapshotFromVolumeRecoveryPointOutputTypeDef,
    CreateSnapshotInputRequestTypeDef,
    CreateSnapshotOutputTypeDef,
    CreateStorediSCSIVolumeInputRequestTypeDef,
    CreateStorediSCSIVolumeOutputTypeDef,
    CreateTapePoolInputRequestTypeDef,
    CreateTapePoolOutputTypeDef,
    CreateTapesInputRequestTypeDef,
    CreateTapesOutputTypeDef,
    CreateTapeWithBarcodeInputRequestTypeDef,
    CreateTapeWithBarcodeOutputTypeDef,
    DeleteAutomaticTapeCreationPolicyInputRequestTypeDef,
    DeleteAutomaticTapeCreationPolicyOutputTypeDef,
    DeleteBandwidthRateLimitInputRequestTypeDef,
    DeleteBandwidthRateLimitOutputTypeDef,
    DeleteChapCredentialsInputRequestTypeDef,
    DeleteChapCredentialsOutputTypeDef,
    DeleteFileShareInputRequestTypeDef,
    DeleteFileShareOutputTypeDef,
    DeleteGatewayInputRequestTypeDef,
    DeleteGatewayOutputTypeDef,
    DeleteSnapshotScheduleInputRequestTypeDef,
    DeleteSnapshotScheduleOutputTypeDef,
    DeleteTapeArchiveInputRequestTypeDef,
    DeleteTapeArchiveOutputTypeDef,
    DeleteTapeInputRequestTypeDef,
    DeleteTapeOutputTypeDef,
    DeleteTapePoolInputRequestTypeDef,
    DeleteTapePoolOutputTypeDef,
    DeleteVolumeInputRequestTypeDef,
    DeleteVolumeOutputTypeDef,
    DescribeAvailabilityMonitorTestInputRequestTypeDef,
    DescribeAvailabilityMonitorTestOutputTypeDef,
    DescribeBandwidthRateLimitInputRequestTypeDef,
    DescribeBandwidthRateLimitOutputTypeDef,
    DescribeBandwidthRateLimitScheduleInputRequestTypeDef,
    DescribeBandwidthRateLimitScheduleOutputTypeDef,
    DescribeCachediSCSIVolumesInputRequestTypeDef,
    DescribeCachediSCSIVolumesOutputTypeDef,
    DescribeCacheInputRequestTypeDef,
    DescribeCacheOutputTypeDef,
    DescribeChapCredentialsInputRequestTypeDef,
    DescribeChapCredentialsOutputTypeDef,
    DescribeFileSystemAssociationsInputRequestTypeDef,
    DescribeFileSystemAssociationsOutputTypeDef,
    DescribeGatewayInformationInputRequestTypeDef,
    DescribeGatewayInformationOutputTypeDef,
    DescribeMaintenanceStartTimeInputRequestTypeDef,
    DescribeMaintenanceStartTimeOutputTypeDef,
    DescribeNFSFileSharesInputRequestTypeDef,
    DescribeNFSFileSharesOutputTypeDef,
    DescribeSMBFileSharesInputRequestTypeDef,
    DescribeSMBFileSharesOutputTypeDef,
    DescribeSMBSettingsInputRequestTypeDef,
    DescribeSMBSettingsOutputTypeDef,
    DescribeSnapshotScheduleInputRequestTypeDef,
    DescribeSnapshotScheduleOutputTypeDef,
    DescribeStorediSCSIVolumesInputRequestTypeDef,
    DescribeStorediSCSIVolumesOutputTypeDef,
    DescribeTapeArchivesInputRequestTypeDef,
    DescribeTapeArchivesOutputTypeDef,
    DescribeTapeRecoveryPointsInputRequestTypeDef,
    DescribeTapeRecoveryPointsOutputTypeDef,
    DescribeTapesInputRequestTypeDef,
    DescribeTapesOutputTypeDef,
    DescribeUploadBufferInputRequestTypeDef,
    DescribeUploadBufferOutputTypeDef,
    DescribeVTLDevicesInputRequestTypeDef,
    DescribeVTLDevicesOutputTypeDef,
    DescribeWorkingStorageInputRequestTypeDef,
    DescribeWorkingStorageOutputTypeDef,
    DetachVolumeInputRequestTypeDef,
    DetachVolumeOutputTypeDef,
    DisableGatewayInputRequestTypeDef,
    DisableGatewayOutputTypeDef,
    DisassociateFileSystemInputRequestTypeDef,
    DisassociateFileSystemOutputTypeDef,
    JoinDomainInputRequestTypeDef,
    JoinDomainOutputTypeDef,
    ListAutomaticTapeCreationPoliciesInputRequestTypeDef,
    ListAutomaticTapeCreationPoliciesOutputTypeDef,
    ListFileSharesInputRequestTypeDef,
    ListFileSharesOutputTypeDef,
    ListFileSystemAssociationsInputRequestTypeDef,
    ListFileSystemAssociationsOutputTypeDef,
    ListGatewaysInputRequestTypeDef,
    ListGatewaysOutputTypeDef,
    ListLocalDisksInputRequestTypeDef,
    ListLocalDisksOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTapePoolsInputRequestTypeDef,
    ListTapePoolsOutputTypeDef,
    ListTapesInputRequestTypeDef,
    ListTapesOutputTypeDef,
    ListVolumeInitiatorsInputRequestTypeDef,
    ListVolumeInitiatorsOutputTypeDef,
    ListVolumeRecoveryPointsInputRequestTypeDef,
    ListVolumeRecoveryPointsOutputTypeDef,
    ListVolumesInputRequestTypeDef,
    ListVolumesOutputTypeDef,
    NotifyWhenUploadedInputRequestTypeDef,
    NotifyWhenUploadedOutputTypeDef,
    RefreshCacheInputRequestTypeDef,
    RefreshCacheOutputTypeDef,
    RemoveTagsFromResourceInputRequestTypeDef,
    RemoveTagsFromResourceOutputTypeDef,
    ResetCacheInputRequestTypeDef,
    ResetCacheOutputTypeDef,
    RetrieveTapeArchiveInputRequestTypeDef,
    RetrieveTapeArchiveOutputTypeDef,
    RetrieveTapeRecoveryPointInputRequestTypeDef,
    RetrieveTapeRecoveryPointOutputTypeDef,
    SetLocalConsolePasswordInputRequestTypeDef,
    SetLocalConsolePasswordOutputTypeDef,
    SetSMBGuestPasswordInputRequestTypeDef,
    SetSMBGuestPasswordOutputTypeDef,
    ShutdownGatewayInputRequestTypeDef,
    ShutdownGatewayOutputTypeDef,
    StartAvailabilityMonitorTestInputRequestTypeDef,
    StartAvailabilityMonitorTestOutputTypeDef,
    StartGatewayInputRequestTypeDef,
    StartGatewayOutputTypeDef,
    UpdateAutomaticTapeCreationPolicyInputRequestTypeDef,
    UpdateAutomaticTapeCreationPolicyOutputTypeDef,
    UpdateBandwidthRateLimitInputRequestTypeDef,
    UpdateBandwidthRateLimitOutputTypeDef,
    UpdateBandwidthRateLimitScheduleInputRequestTypeDef,
    UpdateBandwidthRateLimitScheduleOutputTypeDef,
    UpdateChapCredentialsInputRequestTypeDef,
    UpdateChapCredentialsOutputTypeDef,
    UpdateFileSystemAssociationInputRequestTypeDef,
    UpdateFileSystemAssociationOutputTypeDef,
    UpdateGatewayInformationInputRequestTypeDef,
    UpdateGatewayInformationOutputTypeDef,
    UpdateGatewaySoftwareNowInputRequestTypeDef,
    UpdateGatewaySoftwareNowOutputTypeDef,
    UpdateMaintenanceStartTimeInputRequestTypeDef,
    UpdateMaintenanceStartTimeOutputTypeDef,
    UpdateNFSFileShareInputRequestTypeDef,
    UpdateNFSFileShareOutputTypeDef,
    UpdateSMBFileShareInputRequestTypeDef,
    UpdateSMBFileShareOutputTypeDef,
    UpdateSMBFileShareVisibilityInputRequestTypeDef,
    UpdateSMBFileShareVisibilityOutputTypeDef,
    UpdateSMBLocalGroupsInputRequestTypeDef,
    UpdateSMBLocalGroupsOutputTypeDef,
    UpdateSMBSecurityStrategyInputRequestTypeDef,
    UpdateSMBSecurityStrategyOutputTypeDef,
    UpdateSnapshotScheduleInputRequestTypeDef,
    UpdateSnapshotScheduleOutputTypeDef,
    UpdateVTLDeviceTypeInputRequestTypeDef,
    UpdateVTLDeviceTypeOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("StorageGatewayClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InvalidGatewayRequestException: Type[BotocoreClientError]
    ServiceUnavailableError: Type[BotocoreClientError]

class StorageGatewayClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        StorageGatewayClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#close)
        """

    def activate_gateway(
        self, **kwargs: Unpack[ActivateGatewayInputRequestTypeDef]
    ) -> ActivateGatewayOutputTypeDef:
        """
        Activates the gateway you previously deployed on your host.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/activate_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#activate_gateway)
        """

    def add_cache(self, **kwargs: Unpack[AddCacheInputRequestTypeDef]) -> AddCacheOutputTypeDef:
        """
        Configures one or more gateway local disks as cache for a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/add_cache.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#add_cache)
        """

    def add_tags_to_resource(
        self, **kwargs: Unpack[AddTagsToResourceInputRequestTypeDef]
    ) -> AddTagsToResourceOutputTypeDef:
        """
        Adds one or more tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/add_tags_to_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#add_tags_to_resource)
        """

    def add_upload_buffer(
        self, **kwargs: Unpack[AddUploadBufferInputRequestTypeDef]
    ) -> AddUploadBufferOutputTypeDef:
        """
        Configures one or more gateway local disks as upload buffer for a specified
        gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/add_upload_buffer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#add_upload_buffer)
        """

    def add_working_storage(
        self, **kwargs: Unpack[AddWorkingStorageInputRequestTypeDef]
    ) -> AddWorkingStorageOutputTypeDef:
        """
        Configures one or more gateway local disks as working storage for a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/add_working_storage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#add_working_storage)
        """

    def assign_tape_pool(
        self, **kwargs: Unpack[AssignTapePoolInputRequestTypeDef]
    ) -> AssignTapePoolOutputTypeDef:
        """
        Assigns a tape to a tape pool for archiving.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/assign_tape_pool.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#assign_tape_pool)
        """

    def associate_file_system(
        self, **kwargs: Unpack[AssociateFileSystemInputRequestTypeDef]
    ) -> AssociateFileSystemOutputTypeDef:
        """
        Associate an Amazon FSx file system with the FSx File Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/associate_file_system.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#associate_file_system)
        """

    def attach_volume(
        self, **kwargs: Unpack[AttachVolumeInputRequestTypeDef]
    ) -> AttachVolumeOutputTypeDef:
        """
        Connects a volume to an iSCSI connection and then attaches the volume to the
        specified gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/attach_volume.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#attach_volume)
        """

    def cancel_archival(
        self, **kwargs: Unpack[CancelArchivalInputRequestTypeDef]
    ) -> CancelArchivalOutputTypeDef:
        """
        Cancels archiving of a virtual tape to the virtual tape shelf (VTS) after the
        archiving process is initiated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/cancel_archival.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#cancel_archival)
        """

    def cancel_retrieval(
        self, **kwargs: Unpack[CancelRetrievalInputRequestTypeDef]
    ) -> CancelRetrievalOutputTypeDef:
        """
        Cancels retrieval of a virtual tape from the virtual tape shelf (VTS) to a
        gateway after the retrieval process is initiated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/cancel_retrieval.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#cancel_retrieval)
        """

    def create_cached_iscsi_volume(
        self, **kwargs: Unpack[CreateCachediSCSIVolumeInputRequestTypeDef]
    ) -> CreateCachediSCSIVolumeOutputTypeDef:
        """
        Creates a cached volume on a specified cached volume gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/create_cached_iscsi_volume.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#create_cached_iscsi_volume)
        """

    def create_nfs_file_share(
        self, **kwargs: Unpack[CreateNFSFileShareInputRequestTypeDef]
    ) -> CreateNFSFileShareOutputTypeDef:
        """
        Creates a Network File System (NFS) file share on an existing S3 File Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/create_nfs_file_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#create_nfs_file_share)
        """

    def create_smb_file_share(
        self, **kwargs: Unpack[CreateSMBFileShareInputRequestTypeDef]
    ) -> CreateSMBFileShareOutputTypeDef:
        """
        Creates a Server Message Block (SMB) file share on an existing S3 File Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/create_smb_file_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#create_smb_file_share)
        """

    def create_snapshot(
        self, **kwargs: Unpack[CreateSnapshotInputRequestTypeDef]
    ) -> CreateSnapshotOutputTypeDef:
        """
        Initiates a snapshot of a volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/create_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#create_snapshot)
        """

    def create_snapshot_from_volume_recovery_point(
        self, **kwargs: Unpack[CreateSnapshotFromVolumeRecoveryPointInputRequestTypeDef]
    ) -> CreateSnapshotFromVolumeRecoveryPointOutputTypeDef:
        """
        Initiates a snapshot of a gateway from a volume recovery point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/create_snapshot_from_volume_recovery_point.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#create_snapshot_from_volume_recovery_point)
        """

    def create_stored_iscsi_volume(
        self, **kwargs: Unpack[CreateStorediSCSIVolumeInputRequestTypeDef]
    ) -> CreateStorediSCSIVolumeOutputTypeDef:
        """
        Creates a volume on a specified gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/create_stored_iscsi_volume.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#create_stored_iscsi_volume)
        """

    def create_tape_pool(
        self, **kwargs: Unpack[CreateTapePoolInputRequestTypeDef]
    ) -> CreateTapePoolOutputTypeDef:
        """
        Creates a new custom tape pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/create_tape_pool.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#create_tape_pool)
        """

    def create_tape_with_barcode(
        self, **kwargs: Unpack[CreateTapeWithBarcodeInputRequestTypeDef]
    ) -> CreateTapeWithBarcodeOutputTypeDef:
        """
        Creates a virtual tape by using your own barcode.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/create_tape_with_barcode.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#create_tape_with_barcode)
        """

    def create_tapes(
        self, **kwargs: Unpack[CreateTapesInputRequestTypeDef]
    ) -> CreateTapesOutputTypeDef:
        """
        Creates one or more virtual tapes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/create_tapes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#create_tapes)
        """

    def delete_automatic_tape_creation_policy(
        self, **kwargs: Unpack[DeleteAutomaticTapeCreationPolicyInputRequestTypeDef]
    ) -> DeleteAutomaticTapeCreationPolicyOutputTypeDef:
        """
        Deletes the automatic tape creation policy of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/delete_automatic_tape_creation_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#delete_automatic_tape_creation_policy)
        """

    def delete_bandwidth_rate_limit(
        self, **kwargs: Unpack[DeleteBandwidthRateLimitInputRequestTypeDef]
    ) -> DeleteBandwidthRateLimitOutputTypeDef:
        """
        Deletes the bandwidth rate limits of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/delete_bandwidth_rate_limit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#delete_bandwidth_rate_limit)
        """

    def delete_chap_credentials(
        self, **kwargs: Unpack[DeleteChapCredentialsInputRequestTypeDef]
    ) -> DeleteChapCredentialsOutputTypeDef:
        """
        Deletes Challenge-Handshake Authentication Protocol (CHAP) credentials for a
        specified iSCSI target and initiator pair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/delete_chap_credentials.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#delete_chap_credentials)
        """

    def delete_file_share(
        self, **kwargs: Unpack[DeleteFileShareInputRequestTypeDef]
    ) -> DeleteFileShareOutputTypeDef:
        """
        Deletes a file share from an S3 File Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/delete_file_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#delete_file_share)
        """

    def delete_gateway(
        self, **kwargs: Unpack[DeleteGatewayInputRequestTypeDef]
    ) -> DeleteGatewayOutputTypeDef:
        """
        Deletes a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/delete_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#delete_gateway)
        """

    def delete_snapshot_schedule(
        self, **kwargs: Unpack[DeleteSnapshotScheduleInputRequestTypeDef]
    ) -> DeleteSnapshotScheduleOutputTypeDef:
        """
        Deletes a snapshot of a volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/delete_snapshot_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#delete_snapshot_schedule)
        """

    def delete_tape(
        self, **kwargs: Unpack[DeleteTapeInputRequestTypeDef]
    ) -> DeleteTapeOutputTypeDef:
        """
        Deletes the specified virtual tape.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/delete_tape.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#delete_tape)
        """

    def delete_tape_archive(
        self, **kwargs: Unpack[DeleteTapeArchiveInputRequestTypeDef]
    ) -> DeleteTapeArchiveOutputTypeDef:
        """
        Deletes the specified virtual tape from the virtual tape shelf (VTS).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/delete_tape_archive.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#delete_tape_archive)
        """

    def delete_tape_pool(
        self, **kwargs: Unpack[DeleteTapePoolInputRequestTypeDef]
    ) -> DeleteTapePoolOutputTypeDef:
        """
        Delete a custom tape pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/delete_tape_pool.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#delete_tape_pool)
        """

    def delete_volume(
        self, **kwargs: Unpack[DeleteVolumeInputRequestTypeDef]
    ) -> DeleteVolumeOutputTypeDef:
        """
        Deletes the specified storage volume that you previously created using the
        <a>CreateCachediSCSIVolume</a> or <a>CreateStorediSCSIVolume</a> API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/delete_volume.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#delete_volume)
        """

    def describe_availability_monitor_test(
        self, **kwargs: Unpack[DescribeAvailabilityMonitorTestInputRequestTypeDef]
    ) -> DescribeAvailabilityMonitorTestOutputTypeDef:
        """
        Returns information about the most recent high availability monitoring test
        that was performed on the host in a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_availability_monitor_test.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_availability_monitor_test)
        """

    def describe_bandwidth_rate_limit(
        self, **kwargs: Unpack[DescribeBandwidthRateLimitInputRequestTypeDef]
    ) -> DescribeBandwidthRateLimitOutputTypeDef:
        """
        Returns the bandwidth rate limits of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_bandwidth_rate_limit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_bandwidth_rate_limit)
        """

    def describe_bandwidth_rate_limit_schedule(
        self, **kwargs: Unpack[DescribeBandwidthRateLimitScheduleInputRequestTypeDef]
    ) -> DescribeBandwidthRateLimitScheduleOutputTypeDef:
        """
        Returns information about the bandwidth rate limit schedule of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_bandwidth_rate_limit_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_bandwidth_rate_limit_schedule)
        """

    def describe_cache(
        self, **kwargs: Unpack[DescribeCacheInputRequestTypeDef]
    ) -> DescribeCacheOutputTypeDef:
        """
        Returns information about the cache of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_cache.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_cache)
        """

    def describe_cached_iscsi_volumes(
        self, **kwargs: Unpack[DescribeCachediSCSIVolumesInputRequestTypeDef]
    ) -> DescribeCachediSCSIVolumesOutputTypeDef:
        """
        Returns a description of the gateway volumes specified in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_cached_iscsi_volumes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_cached_iscsi_volumes)
        """

    def describe_chap_credentials(
        self, **kwargs: Unpack[DescribeChapCredentialsInputRequestTypeDef]
    ) -> DescribeChapCredentialsOutputTypeDef:
        """
        Returns an array of Challenge-Handshake Authentication Protocol (CHAP)
        credentials information for a specified iSCSI target, one for each
        target-initiator pair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_chap_credentials.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_chap_credentials)
        """

    def describe_file_system_associations(
        self, **kwargs: Unpack[DescribeFileSystemAssociationsInputRequestTypeDef]
    ) -> DescribeFileSystemAssociationsOutputTypeDef:
        """
        Gets the file system association information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_file_system_associations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_file_system_associations)
        """

    def describe_gateway_information(
        self, **kwargs: Unpack[DescribeGatewayInformationInputRequestTypeDef]
    ) -> DescribeGatewayInformationOutputTypeDef:
        """
        Returns metadata about a gateway such as its name, network interfaces, time
        zone, status, and software version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_gateway_information.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_gateway_information)
        """

    def describe_maintenance_start_time(
        self, **kwargs: Unpack[DescribeMaintenanceStartTimeInputRequestTypeDef]
    ) -> DescribeMaintenanceStartTimeOutputTypeDef:
        """
        Returns your gateway's maintenance window schedule information, with values for
        monthly or weekly cadence, specific day and time to begin maintenance, and
        which types of updates to apply.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_maintenance_start_time.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_maintenance_start_time)
        """

    def describe_nfs_file_shares(
        self, **kwargs: Unpack[DescribeNFSFileSharesInputRequestTypeDef]
    ) -> DescribeNFSFileSharesOutputTypeDef:
        """
        Gets a description for one or more Network File System (NFS) file shares from
        an S3 File Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_nfs_file_shares.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_nfs_file_shares)
        """

    def describe_smb_file_shares(
        self, **kwargs: Unpack[DescribeSMBFileSharesInputRequestTypeDef]
    ) -> DescribeSMBFileSharesOutputTypeDef:
        """
        Gets a description for one or more Server Message Block (SMB) file shares from
        a S3 File Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_smb_file_shares.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_smb_file_shares)
        """

    def describe_smb_settings(
        self, **kwargs: Unpack[DescribeSMBSettingsInputRequestTypeDef]
    ) -> DescribeSMBSettingsOutputTypeDef:
        """
        Gets a description of a Server Message Block (SMB) file share settings from a
        file gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_smb_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_smb_settings)
        """

    def describe_snapshot_schedule(
        self, **kwargs: Unpack[DescribeSnapshotScheduleInputRequestTypeDef]
    ) -> DescribeSnapshotScheduleOutputTypeDef:
        """
        Describes the snapshot schedule for the specified gateway volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_snapshot_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_snapshot_schedule)
        """

    def describe_stored_iscsi_volumes(
        self, **kwargs: Unpack[DescribeStorediSCSIVolumesInputRequestTypeDef]
    ) -> DescribeStorediSCSIVolumesOutputTypeDef:
        """
        Returns the description of the gateway volumes specified in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_stored_iscsi_volumes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_stored_iscsi_volumes)
        """

    def describe_tape_archives(
        self, **kwargs: Unpack[DescribeTapeArchivesInputRequestTypeDef]
    ) -> DescribeTapeArchivesOutputTypeDef:
        """
        Returns a description of specified virtual tapes in the virtual tape shelf
        (VTS).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_tape_archives.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_tape_archives)
        """

    def describe_tape_recovery_points(
        self, **kwargs: Unpack[DescribeTapeRecoveryPointsInputRequestTypeDef]
    ) -> DescribeTapeRecoveryPointsOutputTypeDef:
        """
        Returns a list of virtual tape recovery points that are available for the
        specified tape gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_tape_recovery_points.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_tape_recovery_points)
        """

    def describe_tapes(
        self, **kwargs: Unpack[DescribeTapesInputRequestTypeDef]
    ) -> DescribeTapesOutputTypeDef:
        """
        Returns a description of virtual tapes that correspond to the specified Amazon
        Resource Names (ARNs).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_tapes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_tapes)
        """

    def describe_upload_buffer(
        self, **kwargs: Unpack[DescribeUploadBufferInputRequestTypeDef]
    ) -> DescribeUploadBufferOutputTypeDef:
        """
        Returns information about the upload buffer of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_upload_buffer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_upload_buffer)
        """

    def describe_vtl_devices(
        self, **kwargs: Unpack[DescribeVTLDevicesInputRequestTypeDef]
    ) -> DescribeVTLDevicesOutputTypeDef:
        """
        Returns a description of virtual tape library (VTL) devices for the specified
        tape gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_vtl_devices.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_vtl_devices)
        """

    def describe_working_storage(
        self, **kwargs: Unpack[DescribeWorkingStorageInputRequestTypeDef]
    ) -> DescribeWorkingStorageOutputTypeDef:
        """
        Returns information about the working storage of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/describe_working_storage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#describe_working_storage)
        """

    def detach_volume(
        self, **kwargs: Unpack[DetachVolumeInputRequestTypeDef]
    ) -> DetachVolumeOutputTypeDef:
        """
        Disconnects a volume from an iSCSI connection and then detaches the volume from
        the specified gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/detach_volume.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#detach_volume)
        """

    def disable_gateway(
        self, **kwargs: Unpack[DisableGatewayInputRequestTypeDef]
    ) -> DisableGatewayOutputTypeDef:
        """
        Disables a tape gateway when the gateway is no longer functioning.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/disable_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#disable_gateway)
        """

    def disassociate_file_system(
        self, **kwargs: Unpack[DisassociateFileSystemInputRequestTypeDef]
    ) -> DisassociateFileSystemOutputTypeDef:
        """
        Disassociates an Amazon FSx file system from the specified gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/disassociate_file_system.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#disassociate_file_system)
        """

    def join_domain(
        self, **kwargs: Unpack[JoinDomainInputRequestTypeDef]
    ) -> JoinDomainOutputTypeDef:
        """
        Adds a file gateway to an Active Directory domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/join_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#join_domain)
        """

    def list_automatic_tape_creation_policies(
        self, **kwargs: Unpack[ListAutomaticTapeCreationPoliciesInputRequestTypeDef]
    ) -> ListAutomaticTapeCreationPoliciesOutputTypeDef:
        """
        Lists the automatic tape creation policies for a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/list_automatic_tape_creation_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#list_automatic_tape_creation_policies)
        """

    def list_file_shares(
        self, **kwargs: Unpack[ListFileSharesInputRequestTypeDef]
    ) -> ListFileSharesOutputTypeDef:
        """
        Gets a list of the file shares for a specific S3 File Gateway, or the list of
        file shares that belong to the calling Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/list_file_shares.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#list_file_shares)
        """

    def list_file_system_associations(
        self, **kwargs: Unpack[ListFileSystemAssociationsInputRequestTypeDef]
    ) -> ListFileSystemAssociationsOutputTypeDef:
        """
        Gets a list of <code>FileSystemAssociationSummary</code> objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/list_file_system_associations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#list_file_system_associations)
        """

    def list_gateways(
        self, **kwargs: Unpack[ListGatewaysInputRequestTypeDef]
    ) -> ListGatewaysOutputTypeDef:
        """
        Lists gateways owned by an Amazon Web Services account in an Amazon Web
        Services Region specified in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/list_gateways.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#list_gateways)
        """

    def list_local_disks(
        self, **kwargs: Unpack[ListLocalDisksInputRequestTypeDef]
    ) -> ListLocalDisksOutputTypeDef:
        """
        Returns a list of the gateway's local disks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/list_local_disks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#list_local_disks)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags that have been added to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#list_tags_for_resource)
        """

    def list_tape_pools(
        self, **kwargs: Unpack[ListTapePoolsInputRequestTypeDef]
    ) -> ListTapePoolsOutputTypeDef:
        """
        Lists custom tape pools.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/list_tape_pools.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#list_tape_pools)
        """

    def list_tapes(self, **kwargs: Unpack[ListTapesInputRequestTypeDef]) -> ListTapesOutputTypeDef:
        """
        Lists virtual tapes in your virtual tape library (VTL) and your virtual tape
        shelf (VTS).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/list_tapes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#list_tapes)
        """

    def list_volume_initiators(
        self, **kwargs: Unpack[ListVolumeInitiatorsInputRequestTypeDef]
    ) -> ListVolumeInitiatorsOutputTypeDef:
        """
        Lists iSCSI initiators that are connected to a volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/list_volume_initiators.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#list_volume_initiators)
        """

    def list_volume_recovery_points(
        self, **kwargs: Unpack[ListVolumeRecoveryPointsInputRequestTypeDef]
    ) -> ListVolumeRecoveryPointsOutputTypeDef:
        """
        Lists the recovery points for a specified gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/list_volume_recovery_points.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#list_volume_recovery_points)
        """

    def list_volumes(
        self, **kwargs: Unpack[ListVolumesInputRequestTypeDef]
    ) -> ListVolumesOutputTypeDef:
        """
        Lists the iSCSI stored volumes of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/list_volumes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#list_volumes)
        """

    def notify_when_uploaded(
        self, **kwargs: Unpack[NotifyWhenUploadedInputRequestTypeDef]
    ) -> NotifyWhenUploadedOutputTypeDef:
        """
        Sends you notification through CloudWatch Events when all files written to your
        file share have been uploaded to Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/notify_when_uploaded.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#notify_when_uploaded)
        """

    def refresh_cache(
        self, **kwargs: Unpack[RefreshCacheInputRequestTypeDef]
    ) -> RefreshCacheOutputTypeDef:
        """
        Refreshes the cached inventory of objects for the specified file share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/refresh_cache.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#refresh_cache)
        """

    def remove_tags_from_resource(
        self, **kwargs: Unpack[RemoveTagsFromResourceInputRequestTypeDef]
    ) -> RemoveTagsFromResourceOutputTypeDef:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/remove_tags_from_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#remove_tags_from_resource)
        """

    def reset_cache(
        self, **kwargs: Unpack[ResetCacheInputRequestTypeDef]
    ) -> ResetCacheOutputTypeDef:
        """
        Resets all cache disks that have encountered an error and makes the disks
        available for reconfiguration as cache storage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/reset_cache.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#reset_cache)
        """

    def retrieve_tape_archive(
        self, **kwargs: Unpack[RetrieveTapeArchiveInputRequestTypeDef]
    ) -> RetrieveTapeArchiveOutputTypeDef:
        """
        Retrieves an archived virtual tape from the virtual tape shelf (VTS) to a tape
        gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/retrieve_tape_archive.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#retrieve_tape_archive)
        """

    def retrieve_tape_recovery_point(
        self, **kwargs: Unpack[RetrieveTapeRecoveryPointInputRequestTypeDef]
    ) -> RetrieveTapeRecoveryPointOutputTypeDef:
        """
        Retrieves the recovery point for the specified virtual tape.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/retrieve_tape_recovery_point.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#retrieve_tape_recovery_point)
        """

    def set_local_console_password(
        self, **kwargs: Unpack[SetLocalConsolePasswordInputRequestTypeDef]
    ) -> SetLocalConsolePasswordOutputTypeDef:
        """
        Sets the password for your VM local console.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/set_local_console_password.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#set_local_console_password)
        """

    def set_smb_guest_password(
        self, **kwargs: Unpack[SetSMBGuestPasswordInputRequestTypeDef]
    ) -> SetSMBGuestPasswordOutputTypeDef:
        """
        Sets the password for the guest user <code>smbguest</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/set_smb_guest_password.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#set_smb_guest_password)
        """

    def shutdown_gateway(
        self, **kwargs: Unpack[ShutdownGatewayInputRequestTypeDef]
    ) -> ShutdownGatewayOutputTypeDef:
        """
        Shuts down a Tape Gateway or Volume Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/shutdown_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#shutdown_gateway)
        """

    def start_availability_monitor_test(
        self, **kwargs: Unpack[StartAvailabilityMonitorTestInputRequestTypeDef]
    ) -> StartAvailabilityMonitorTestOutputTypeDef:
        """
        Start a test that verifies that the specified gateway is configured for High
        Availability monitoring in your host environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/start_availability_monitor_test.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#start_availability_monitor_test)
        """

    def start_gateway(
        self, **kwargs: Unpack[StartGatewayInputRequestTypeDef]
    ) -> StartGatewayOutputTypeDef:
        """
        Starts a gateway that you previously shut down (see <a>ShutdownGateway</a>).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/start_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#start_gateway)
        """

    def update_automatic_tape_creation_policy(
        self, **kwargs: Unpack[UpdateAutomaticTapeCreationPolicyInputRequestTypeDef]
    ) -> UpdateAutomaticTapeCreationPolicyOutputTypeDef:
        """
        Updates the automatic tape creation policy of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/update_automatic_tape_creation_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#update_automatic_tape_creation_policy)
        """

    def update_bandwidth_rate_limit(
        self, **kwargs: Unpack[UpdateBandwidthRateLimitInputRequestTypeDef]
    ) -> UpdateBandwidthRateLimitOutputTypeDef:
        """
        Updates the bandwidth rate limits of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/update_bandwidth_rate_limit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#update_bandwidth_rate_limit)
        """

    def update_bandwidth_rate_limit_schedule(
        self, **kwargs: Unpack[UpdateBandwidthRateLimitScheduleInputRequestTypeDef]
    ) -> UpdateBandwidthRateLimitScheduleOutputTypeDef:
        """
        Updates the bandwidth rate limit schedule for a specified gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/update_bandwidth_rate_limit_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#update_bandwidth_rate_limit_schedule)
        """

    def update_chap_credentials(
        self, **kwargs: Unpack[UpdateChapCredentialsInputRequestTypeDef]
    ) -> UpdateChapCredentialsOutputTypeDef:
        """
        Updates the Challenge-Handshake Authentication Protocol (CHAP) credentials for
        a specified iSCSI target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/update_chap_credentials.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#update_chap_credentials)
        """

    def update_file_system_association(
        self, **kwargs: Unpack[UpdateFileSystemAssociationInputRequestTypeDef]
    ) -> UpdateFileSystemAssociationOutputTypeDef:
        """
        Updates a file system association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/update_file_system_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#update_file_system_association)
        """

    def update_gateway_information(
        self, **kwargs: Unpack[UpdateGatewayInformationInputRequestTypeDef]
    ) -> UpdateGatewayInformationOutputTypeDef:
        """
        Updates a gateway's metadata, which includes the gateway's name, time zone, and
        metadata cache size.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/update_gateway_information.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#update_gateway_information)
        """

    def update_gateway_software_now(
        self, **kwargs: Unpack[UpdateGatewaySoftwareNowInputRequestTypeDef]
    ) -> UpdateGatewaySoftwareNowOutputTypeDef:
        """
        Updates the gateway virtual machine (VM) software.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/update_gateway_software_now.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#update_gateway_software_now)
        """

    def update_maintenance_start_time(
        self, **kwargs: Unpack[UpdateMaintenanceStartTimeInputRequestTypeDef]
    ) -> UpdateMaintenanceStartTimeOutputTypeDef:
        """
        Updates a gateway's maintenance window schedule, with settings for monthly or
        weekly cadence, specific day and time to begin maintenance, and which types of
        updates to apply.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/update_maintenance_start_time.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#update_maintenance_start_time)
        """

    def update_nfs_file_share(
        self, **kwargs: Unpack[UpdateNFSFileShareInputRequestTypeDef]
    ) -> UpdateNFSFileShareOutputTypeDef:
        """
        Updates a Network File System (NFS) file share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/update_nfs_file_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#update_nfs_file_share)
        """

    def update_smb_file_share(
        self, **kwargs: Unpack[UpdateSMBFileShareInputRequestTypeDef]
    ) -> UpdateSMBFileShareOutputTypeDef:
        """
        Updates a Server Message Block (SMB) file share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/update_smb_file_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#update_smb_file_share)
        """

    def update_smb_file_share_visibility(
        self, **kwargs: Unpack[UpdateSMBFileShareVisibilityInputRequestTypeDef]
    ) -> UpdateSMBFileShareVisibilityOutputTypeDef:
        """
        Controls whether the shares on an S3 File Gateway are visible in a net view or
        browse list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/update_smb_file_share_visibility.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#update_smb_file_share_visibility)
        """

    def update_smb_local_groups(
        self, **kwargs: Unpack[UpdateSMBLocalGroupsInputRequestTypeDef]
    ) -> UpdateSMBLocalGroupsOutputTypeDef:
        """
        Updates the list of Active Directory users and groups that have special
        permissions for SMB file shares on the gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/update_smb_local_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#update_smb_local_groups)
        """

    def update_smb_security_strategy(
        self, **kwargs: Unpack[UpdateSMBSecurityStrategyInputRequestTypeDef]
    ) -> UpdateSMBSecurityStrategyOutputTypeDef:
        """
        Updates the SMB security strategy level for an Amazon S3 file gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/update_smb_security_strategy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#update_smb_security_strategy)
        """

    def update_snapshot_schedule(
        self, **kwargs: Unpack[UpdateSnapshotScheduleInputRequestTypeDef]
    ) -> UpdateSnapshotScheduleOutputTypeDef:
        """
        Updates a snapshot schedule configured for a gateway volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/update_snapshot_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#update_snapshot_schedule)
        """

    def update_vtl_device_type(
        self, **kwargs: Unpack[UpdateVTLDeviceTypeInputRequestTypeDef]
    ) -> UpdateVTLDeviceTypeOutputTypeDef:
        """
        Updates the type of medium changer in a tape gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/update_vtl_device_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#update_vtl_device_type)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_tape_archives"]
    ) -> DescribeTapeArchivesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_tape_recovery_points"]
    ) -> DescribeTapeRecoveryPointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_tapes"]) -> DescribeTapesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_vtl_devices"]
    ) -> DescribeVTLDevicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_file_shares"]) -> ListFileSharesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_file_system_associations"]
    ) -> ListFileSystemAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_gateways"]) -> ListGatewaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tape_pools"]) -> ListTapePoolsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tapes"]) -> ListTapesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_volumes"]) -> ListVolumesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_storagegateway/client/#get_paginator)
        """
