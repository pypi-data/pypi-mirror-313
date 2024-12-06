"""
Type annotations for backup service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_backup.client import BackupClient

    session = Session()
    client: BackupClient = session.client("backup")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListBackupJobsPaginator,
    ListBackupPlansPaginator,
    ListBackupPlanTemplatesPaginator,
    ListBackupPlanVersionsPaginator,
    ListBackupSelectionsPaginator,
    ListBackupVaultsPaginator,
    ListCopyJobsPaginator,
    ListLegalHoldsPaginator,
    ListProtectedResourcesByBackupVaultPaginator,
    ListProtectedResourcesPaginator,
    ListRecoveryPointsByBackupVaultPaginator,
    ListRecoveryPointsByLegalHoldPaginator,
    ListRecoveryPointsByResourcePaginator,
    ListRestoreJobsByProtectedResourcePaginator,
    ListRestoreJobsPaginator,
    ListRestoreTestingPlansPaginator,
    ListRestoreTestingSelectionsPaginator,
)
from .type_defs import (
    CancelLegalHoldInputRequestTypeDef,
    CreateBackupPlanInputRequestTypeDef,
    CreateBackupPlanOutputTypeDef,
    CreateBackupSelectionInputRequestTypeDef,
    CreateBackupSelectionOutputTypeDef,
    CreateBackupVaultInputRequestTypeDef,
    CreateBackupVaultOutputTypeDef,
    CreateFrameworkInputRequestTypeDef,
    CreateFrameworkOutputTypeDef,
    CreateLegalHoldInputRequestTypeDef,
    CreateLegalHoldOutputTypeDef,
    CreateLogicallyAirGappedBackupVaultInputRequestTypeDef,
    CreateLogicallyAirGappedBackupVaultOutputTypeDef,
    CreateReportPlanInputRequestTypeDef,
    CreateReportPlanOutputTypeDef,
    CreateRestoreTestingPlanInputRequestTypeDef,
    CreateRestoreTestingPlanOutputTypeDef,
    CreateRestoreTestingSelectionInputRequestTypeDef,
    CreateRestoreTestingSelectionOutputTypeDef,
    DeleteBackupPlanInputRequestTypeDef,
    DeleteBackupPlanOutputTypeDef,
    DeleteBackupSelectionInputRequestTypeDef,
    DeleteBackupVaultAccessPolicyInputRequestTypeDef,
    DeleteBackupVaultInputRequestTypeDef,
    DeleteBackupVaultLockConfigurationInputRequestTypeDef,
    DeleteBackupVaultNotificationsInputRequestTypeDef,
    DeleteFrameworkInputRequestTypeDef,
    DeleteRecoveryPointInputRequestTypeDef,
    DeleteReportPlanInputRequestTypeDef,
    DeleteRestoreTestingPlanInputRequestTypeDef,
    DeleteRestoreTestingSelectionInputRequestTypeDef,
    DescribeBackupJobInputRequestTypeDef,
    DescribeBackupJobOutputTypeDef,
    DescribeBackupVaultInputRequestTypeDef,
    DescribeBackupVaultOutputTypeDef,
    DescribeCopyJobInputRequestTypeDef,
    DescribeCopyJobOutputTypeDef,
    DescribeFrameworkInputRequestTypeDef,
    DescribeFrameworkOutputTypeDef,
    DescribeGlobalSettingsOutputTypeDef,
    DescribeProtectedResourceInputRequestTypeDef,
    DescribeProtectedResourceOutputTypeDef,
    DescribeRecoveryPointInputRequestTypeDef,
    DescribeRecoveryPointOutputTypeDef,
    DescribeRegionSettingsOutputTypeDef,
    DescribeReportJobInputRequestTypeDef,
    DescribeReportJobOutputTypeDef,
    DescribeReportPlanInputRequestTypeDef,
    DescribeReportPlanOutputTypeDef,
    DescribeRestoreJobInputRequestTypeDef,
    DescribeRestoreJobOutputTypeDef,
    DisassociateRecoveryPointFromParentInputRequestTypeDef,
    DisassociateRecoveryPointInputRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportBackupPlanTemplateInputRequestTypeDef,
    ExportBackupPlanTemplateOutputTypeDef,
    GetBackupPlanFromJSONInputRequestTypeDef,
    GetBackupPlanFromJSONOutputTypeDef,
    GetBackupPlanFromTemplateInputRequestTypeDef,
    GetBackupPlanFromTemplateOutputTypeDef,
    GetBackupPlanInputRequestTypeDef,
    GetBackupPlanOutputTypeDef,
    GetBackupSelectionInputRequestTypeDef,
    GetBackupSelectionOutputTypeDef,
    GetBackupVaultAccessPolicyInputRequestTypeDef,
    GetBackupVaultAccessPolicyOutputTypeDef,
    GetBackupVaultNotificationsInputRequestTypeDef,
    GetBackupVaultNotificationsOutputTypeDef,
    GetLegalHoldInputRequestTypeDef,
    GetLegalHoldOutputTypeDef,
    GetRecoveryPointRestoreMetadataInputRequestTypeDef,
    GetRecoveryPointRestoreMetadataOutputTypeDef,
    GetRestoreJobMetadataInputRequestTypeDef,
    GetRestoreJobMetadataOutputTypeDef,
    GetRestoreTestingInferredMetadataInputRequestTypeDef,
    GetRestoreTestingInferredMetadataOutputTypeDef,
    GetRestoreTestingPlanInputRequestTypeDef,
    GetRestoreTestingPlanOutputTypeDef,
    GetRestoreTestingSelectionInputRequestTypeDef,
    GetRestoreTestingSelectionOutputTypeDef,
    GetSupportedResourceTypesOutputTypeDef,
    ListBackupJobsInputRequestTypeDef,
    ListBackupJobsOutputTypeDef,
    ListBackupJobSummariesInputRequestTypeDef,
    ListBackupJobSummariesOutputTypeDef,
    ListBackupPlansInputRequestTypeDef,
    ListBackupPlansOutputTypeDef,
    ListBackupPlanTemplatesInputRequestTypeDef,
    ListBackupPlanTemplatesOutputTypeDef,
    ListBackupPlanVersionsInputRequestTypeDef,
    ListBackupPlanVersionsOutputTypeDef,
    ListBackupSelectionsInputRequestTypeDef,
    ListBackupSelectionsOutputTypeDef,
    ListBackupVaultsInputRequestTypeDef,
    ListBackupVaultsOutputTypeDef,
    ListCopyJobsInputRequestTypeDef,
    ListCopyJobsOutputTypeDef,
    ListCopyJobSummariesInputRequestTypeDef,
    ListCopyJobSummariesOutputTypeDef,
    ListFrameworksInputRequestTypeDef,
    ListFrameworksOutputTypeDef,
    ListLegalHoldsInputRequestTypeDef,
    ListLegalHoldsOutputTypeDef,
    ListProtectedResourcesByBackupVaultInputRequestTypeDef,
    ListProtectedResourcesByBackupVaultOutputTypeDef,
    ListProtectedResourcesInputRequestTypeDef,
    ListProtectedResourcesOutputTypeDef,
    ListRecoveryPointsByBackupVaultInputRequestTypeDef,
    ListRecoveryPointsByBackupVaultOutputTypeDef,
    ListRecoveryPointsByLegalHoldInputRequestTypeDef,
    ListRecoveryPointsByLegalHoldOutputTypeDef,
    ListRecoveryPointsByResourceInputRequestTypeDef,
    ListRecoveryPointsByResourceOutputTypeDef,
    ListReportJobsInputRequestTypeDef,
    ListReportJobsOutputTypeDef,
    ListReportPlansInputRequestTypeDef,
    ListReportPlansOutputTypeDef,
    ListRestoreJobsByProtectedResourceInputRequestTypeDef,
    ListRestoreJobsByProtectedResourceOutputTypeDef,
    ListRestoreJobsInputRequestTypeDef,
    ListRestoreJobsOutputTypeDef,
    ListRestoreJobSummariesInputRequestTypeDef,
    ListRestoreJobSummariesOutputTypeDef,
    ListRestoreTestingPlansInputRequestTypeDef,
    ListRestoreTestingPlansOutputTypeDef,
    ListRestoreTestingSelectionsInputRequestTypeDef,
    ListRestoreTestingSelectionsOutputTypeDef,
    ListTagsInputRequestTypeDef,
    ListTagsOutputTypeDef,
    PutBackupVaultAccessPolicyInputRequestTypeDef,
    PutBackupVaultLockConfigurationInputRequestTypeDef,
    PutBackupVaultNotificationsInputRequestTypeDef,
    PutRestoreValidationResultInputRequestTypeDef,
    StartBackupJobInputRequestTypeDef,
    StartBackupJobOutputTypeDef,
    StartCopyJobInputRequestTypeDef,
    StartCopyJobOutputTypeDef,
    StartReportJobInputRequestTypeDef,
    StartReportJobOutputTypeDef,
    StartRestoreJobInputRequestTypeDef,
    StartRestoreJobOutputTypeDef,
    StopBackupJobInputRequestTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateBackupPlanInputRequestTypeDef,
    UpdateBackupPlanOutputTypeDef,
    UpdateFrameworkInputRequestTypeDef,
    UpdateFrameworkOutputTypeDef,
    UpdateGlobalSettingsInputRequestTypeDef,
    UpdateRecoveryPointLifecycleInputRequestTypeDef,
    UpdateRecoveryPointLifecycleOutputTypeDef,
    UpdateRegionSettingsInputRequestTypeDef,
    UpdateReportPlanInputRequestTypeDef,
    UpdateReportPlanOutputTypeDef,
    UpdateRestoreTestingPlanInputRequestTypeDef,
    UpdateRestoreTestingPlanOutputTypeDef,
    UpdateRestoreTestingSelectionInputRequestTypeDef,
    UpdateRestoreTestingSelectionOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("BackupClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DependencyFailureException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidResourceStateException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MissingParameterValueException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]

class BackupClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BackupClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html#Backup.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#close)
        """

    def cancel_legal_hold(
        self, **kwargs: Unpack[CancelLegalHoldInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified legal hold on a recovery point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/cancel_legal_hold.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#cancel_legal_hold)
        """

    def create_backup_plan(
        self, **kwargs: Unpack[CreateBackupPlanInputRequestTypeDef]
    ) -> CreateBackupPlanOutputTypeDef:
        """
        Creates a backup plan using a backup plan name and backup rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/create_backup_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#create_backup_plan)
        """

    def create_backup_selection(
        self, **kwargs: Unpack[CreateBackupSelectionInputRequestTypeDef]
    ) -> CreateBackupSelectionOutputTypeDef:
        """
        Creates a JSON document that specifies a set of resources to assign to a backup
        plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/create_backup_selection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#create_backup_selection)
        """

    def create_backup_vault(
        self, **kwargs: Unpack[CreateBackupVaultInputRequestTypeDef]
    ) -> CreateBackupVaultOutputTypeDef:
        """
        Creates a logical container where backups are stored.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/create_backup_vault.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#create_backup_vault)
        """

    def create_framework(
        self, **kwargs: Unpack[CreateFrameworkInputRequestTypeDef]
    ) -> CreateFrameworkOutputTypeDef:
        """
        Creates a framework with one or more controls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/create_framework.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#create_framework)
        """

    def create_legal_hold(
        self, **kwargs: Unpack[CreateLegalHoldInputRequestTypeDef]
    ) -> CreateLegalHoldOutputTypeDef:
        """
        Creates a legal hold on a recovery point (backup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/create_legal_hold.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#create_legal_hold)
        """

    def create_logically_air_gapped_backup_vault(
        self, **kwargs: Unpack[CreateLogicallyAirGappedBackupVaultInputRequestTypeDef]
    ) -> CreateLogicallyAirGappedBackupVaultOutputTypeDef:
        """
        Creates a logical container to where backups may be copied.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/create_logically_air_gapped_backup_vault.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#create_logically_air_gapped_backup_vault)
        """

    def create_report_plan(
        self, **kwargs: Unpack[CreateReportPlanInputRequestTypeDef]
    ) -> CreateReportPlanOutputTypeDef:
        """
        Creates a report plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/create_report_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#create_report_plan)
        """

    def create_restore_testing_plan(
        self, **kwargs: Unpack[CreateRestoreTestingPlanInputRequestTypeDef]
    ) -> CreateRestoreTestingPlanOutputTypeDef:
        """
        Creates a restore testing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/create_restore_testing_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#create_restore_testing_plan)
        """

    def create_restore_testing_selection(
        self, **kwargs: Unpack[CreateRestoreTestingSelectionInputRequestTypeDef]
    ) -> CreateRestoreTestingSelectionOutputTypeDef:
        """
        This request can be sent after CreateRestoreTestingPlan request returns
        successfully.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/create_restore_testing_selection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#create_restore_testing_selection)
        """

    def delete_backup_plan(
        self, **kwargs: Unpack[DeleteBackupPlanInputRequestTypeDef]
    ) -> DeleteBackupPlanOutputTypeDef:
        """
        Deletes a backup plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/delete_backup_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#delete_backup_plan)
        """

    def delete_backup_selection(
        self, **kwargs: Unpack[DeleteBackupSelectionInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the resource selection associated with a backup plan that is specified
        by the <code>SelectionId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/delete_backup_selection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#delete_backup_selection)
        """

    def delete_backup_vault(
        self, **kwargs: Unpack[DeleteBackupVaultInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the backup vault identified by its name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/delete_backup_vault.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#delete_backup_vault)
        """

    def delete_backup_vault_access_policy(
        self, **kwargs: Unpack[DeleteBackupVaultAccessPolicyInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the policy document that manages permissions on a backup vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/delete_backup_vault_access_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#delete_backup_vault_access_policy)
        """

    def delete_backup_vault_lock_configuration(
        self, **kwargs: Unpack[DeleteBackupVaultLockConfigurationInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes Backup Vault Lock from a backup vault specified by a backup vault name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/delete_backup_vault_lock_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#delete_backup_vault_lock_configuration)
        """

    def delete_backup_vault_notifications(
        self, **kwargs: Unpack[DeleteBackupVaultNotificationsInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes event notifications for the specified backup vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/delete_backup_vault_notifications.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#delete_backup_vault_notifications)
        """

    def delete_framework(
        self, **kwargs: Unpack[DeleteFrameworkInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the framework specified by a framework name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/delete_framework.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#delete_framework)
        """

    def delete_recovery_point(
        self, **kwargs: Unpack[DeleteRecoveryPointInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the recovery point specified by a recovery point ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/delete_recovery_point.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#delete_recovery_point)
        """

    def delete_report_plan(
        self, **kwargs: Unpack[DeleteReportPlanInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the report plan specified by a report plan name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/delete_report_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#delete_report_plan)
        """

    def delete_restore_testing_plan(
        self, **kwargs: Unpack[DeleteRestoreTestingPlanInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This request deletes the specified restore testing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/delete_restore_testing_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#delete_restore_testing_plan)
        """

    def delete_restore_testing_selection(
        self, **kwargs: Unpack[DeleteRestoreTestingSelectionInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Input the Restore Testing Plan name and Restore Testing Selection name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/delete_restore_testing_selection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#delete_restore_testing_selection)
        """

    def describe_backup_job(
        self, **kwargs: Unpack[DescribeBackupJobInputRequestTypeDef]
    ) -> DescribeBackupJobOutputTypeDef:
        """
        Returns backup job details for the specified <code>BackupJobId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/describe_backup_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#describe_backup_job)
        """

    def describe_backup_vault(
        self, **kwargs: Unpack[DescribeBackupVaultInputRequestTypeDef]
    ) -> DescribeBackupVaultOutputTypeDef:
        """
        Returns metadata about a backup vault specified by its name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/describe_backup_vault.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#describe_backup_vault)
        """

    def describe_copy_job(
        self, **kwargs: Unpack[DescribeCopyJobInputRequestTypeDef]
    ) -> DescribeCopyJobOutputTypeDef:
        """
        Returns metadata associated with creating a copy of a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/describe_copy_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#describe_copy_job)
        """

    def describe_framework(
        self, **kwargs: Unpack[DescribeFrameworkInputRequestTypeDef]
    ) -> DescribeFrameworkOutputTypeDef:
        """
        Returns the framework details for the specified <code>FrameworkName</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/describe_framework.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#describe_framework)
        """

    def describe_global_settings(self) -> DescribeGlobalSettingsOutputTypeDef:
        """
        Describes whether the Amazon Web Services account is opted in to cross-account
        backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/describe_global_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#describe_global_settings)
        """

    def describe_protected_resource(
        self, **kwargs: Unpack[DescribeProtectedResourceInputRequestTypeDef]
    ) -> DescribeProtectedResourceOutputTypeDef:
        """
        Returns information about a saved resource, including the last time it was
        backed up, its Amazon Resource Name (ARN), and the Amazon Web Services service
        type of the saved resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/describe_protected_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#describe_protected_resource)
        """

    def describe_recovery_point(
        self, **kwargs: Unpack[DescribeRecoveryPointInputRequestTypeDef]
    ) -> DescribeRecoveryPointOutputTypeDef:
        """
        Returns metadata associated with a recovery point, including ID, status,
        encryption, and lifecycle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/describe_recovery_point.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#describe_recovery_point)
        """

    def describe_region_settings(self) -> DescribeRegionSettingsOutputTypeDef:
        """
        Returns the current service opt-in settings for the Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/describe_region_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#describe_region_settings)
        """

    def describe_report_job(
        self, **kwargs: Unpack[DescribeReportJobInputRequestTypeDef]
    ) -> DescribeReportJobOutputTypeDef:
        """
        Returns the details associated with creating a report as specified by its
        <code>ReportJobId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/describe_report_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#describe_report_job)
        """

    def describe_report_plan(
        self, **kwargs: Unpack[DescribeReportPlanInputRequestTypeDef]
    ) -> DescribeReportPlanOutputTypeDef:
        """
        Returns a list of all report plans for an Amazon Web Services account and
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/describe_report_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#describe_report_plan)
        """

    def describe_restore_job(
        self, **kwargs: Unpack[DescribeRestoreJobInputRequestTypeDef]
    ) -> DescribeRestoreJobOutputTypeDef:
        """
        Returns metadata associated with a restore job that is specified by a job ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/describe_restore_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#describe_restore_job)
        """

    def disassociate_recovery_point(
        self, **kwargs: Unpack[DisassociateRecoveryPointInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified continuous backup recovery point from Backup and releases
        control of that continuous backup to the source service, such as Amazon RDS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/disassociate_recovery_point.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#disassociate_recovery_point)
        """

    def disassociate_recovery_point_from_parent(
        self, **kwargs: Unpack[DisassociateRecoveryPointFromParentInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This action to a specific child (nested) recovery point removes the
        relationship between the specified recovery point and its parent (composite)
        recovery point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/disassociate_recovery_point_from_parent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#disassociate_recovery_point_from_parent)
        """

    def export_backup_plan_template(
        self, **kwargs: Unpack[ExportBackupPlanTemplateInputRequestTypeDef]
    ) -> ExportBackupPlanTemplateOutputTypeDef:
        """
        Returns the backup plan that is specified by the plan ID as a backup template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/export_backup_plan_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#export_backup_plan_template)
        """

    def get_backup_plan(
        self, **kwargs: Unpack[GetBackupPlanInputRequestTypeDef]
    ) -> GetBackupPlanOutputTypeDef:
        """
        Returns <code>BackupPlan</code> details for the specified
        <code>BackupPlanId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_backup_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_backup_plan)
        """

    def get_backup_plan_from_json(
        self, **kwargs: Unpack[GetBackupPlanFromJSONInputRequestTypeDef]
    ) -> GetBackupPlanFromJSONOutputTypeDef:
        """
        Returns a valid JSON document specifying a backup plan or an error.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_backup_plan_from_json.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_backup_plan_from_json)
        """

    def get_backup_plan_from_template(
        self, **kwargs: Unpack[GetBackupPlanFromTemplateInputRequestTypeDef]
    ) -> GetBackupPlanFromTemplateOutputTypeDef:
        """
        Returns the template specified by its <code>templateId</code> as a backup plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_backup_plan_from_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_backup_plan_from_template)
        """

    def get_backup_selection(
        self, **kwargs: Unpack[GetBackupSelectionInputRequestTypeDef]
    ) -> GetBackupSelectionOutputTypeDef:
        """
        Returns selection metadata and a document in JSON format that specifies a list
        of resources that are associated with a backup plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_backup_selection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_backup_selection)
        """

    def get_backup_vault_access_policy(
        self, **kwargs: Unpack[GetBackupVaultAccessPolicyInputRequestTypeDef]
    ) -> GetBackupVaultAccessPolicyOutputTypeDef:
        """
        Returns the access policy document that is associated with the named backup
        vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_backup_vault_access_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_backup_vault_access_policy)
        """

    def get_backup_vault_notifications(
        self, **kwargs: Unpack[GetBackupVaultNotificationsInputRequestTypeDef]
    ) -> GetBackupVaultNotificationsOutputTypeDef:
        """
        Returns event notifications for the specified backup vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_backup_vault_notifications.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_backup_vault_notifications)
        """

    def get_legal_hold(
        self, **kwargs: Unpack[GetLegalHoldInputRequestTypeDef]
    ) -> GetLegalHoldOutputTypeDef:
        """
        This action returns details for a specified legal hold.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_legal_hold.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_legal_hold)
        """

    def get_recovery_point_restore_metadata(
        self, **kwargs: Unpack[GetRecoveryPointRestoreMetadataInputRequestTypeDef]
    ) -> GetRecoveryPointRestoreMetadataOutputTypeDef:
        """
        Returns a set of metadata key-value pairs that were used to create the backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_recovery_point_restore_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_recovery_point_restore_metadata)
        """

    def get_restore_job_metadata(
        self, **kwargs: Unpack[GetRestoreJobMetadataInputRequestTypeDef]
    ) -> GetRestoreJobMetadataOutputTypeDef:
        """
        This request returns the metadata for the specified restore job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_restore_job_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_restore_job_metadata)
        """

    def get_restore_testing_inferred_metadata(
        self, **kwargs: Unpack[GetRestoreTestingInferredMetadataInputRequestTypeDef]
    ) -> GetRestoreTestingInferredMetadataOutputTypeDef:
        """
        This request returns the minimal required set of metadata needed to start a
        restore job with secure default settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_restore_testing_inferred_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_restore_testing_inferred_metadata)
        """

    def get_restore_testing_plan(
        self, **kwargs: Unpack[GetRestoreTestingPlanInputRequestTypeDef]
    ) -> GetRestoreTestingPlanOutputTypeDef:
        """
        Returns <code>RestoreTestingPlan</code> details for the specified
        <code>RestoreTestingPlanName</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_restore_testing_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_restore_testing_plan)
        """

    def get_restore_testing_selection(
        self, **kwargs: Unpack[GetRestoreTestingSelectionInputRequestTypeDef]
    ) -> GetRestoreTestingSelectionOutputTypeDef:
        """
        Returns RestoreTestingSelection, which displays resources and elements of the
        restore testing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_restore_testing_selection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_restore_testing_selection)
        """

    def get_supported_resource_types(self) -> GetSupportedResourceTypesOutputTypeDef:
        """
        Returns the Amazon Web Services resource types supported by Backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_supported_resource_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_supported_resource_types)
        """

    def list_backup_job_summaries(
        self, **kwargs: Unpack[ListBackupJobSummariesInputRequestTypeDef]
    ) -> ListBackupJobSummariesOutputTypeDef:
        """
        This is a request for a summary of backup jobs created or running within the
        most recent 30 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_backup_job_summaries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_backup_job_summaries)
        """

    def list_backup_jobs(
        self, **kwargs: Unpack[ListBackupJobsInputRequestTypeDef]
    ) -> ListBackupJobsOutputTypeDef:
        """
        Returns a list of existing backup jobs for an authenticated account for the
        last 30 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_backup_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_backup_jobs)
        """

    def list_backup_plan_templates(
        self, **kwargs: Unpack[ListBackupPlanTemplatesInputRequestTypeDef]
    ) -> ListBackupPlanTemplatesOutputTypeDef:
        """
        Lists the backup plan templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_backup_plan_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_backup_plan_templates)
        """

    def list_backup_plan_versions(
        self, **kwargs: Unpack[ListBackupPlanVersionsInputRequestTypeDef]
    ) -> ListBackupPlanVersionsOutputTypeDef:
        """
        Returns version metadata of your backup plans, including Amazon Resource Names
        (ARNs), backup plan IDs, creation and deletion dates, plan names, and version
        IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_backup_plan_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_backup_plan_versions)
        """

    def list_backup_plans(
        self, **kwargs: Unpack[ListBackupPlansInputRequestTypeDef]
    ) -> ListBackupPlansOutputTypeDef:
        """
        Lists the active backup plans for the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_backup_plans.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_backup_plans)
        """

    def list_backup_selections(
        self, **kwargs: Unpack[ListBackupSelectionsInputRequestTypeDef]
    ) -> ListBackupSelectionsOutputTypeDef:
        """
        Returns an array containing metadata of the resources associated with the
        target backup plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_backup_selections.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_backup_selections)
        """

    def list_backup_vaults(
        self, **kwargs: Unpack[ListBackupVaultsInputRequestTypeDef]
    ) -> ListBackupVaultsOutputTypeDef:
        """
        Returns a list of recovery point storage containers along with information
        about them.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_backup_vaults.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_backup_vaults)
        """

    def list_copy_job_summaries(
        self, **kwargs: Unpack[ListCopyJobSummariesInputRequestTypeDef]
    ) -> ListCopyJobSummariesOutputTypeDef:
        """
        This request obtains a list of copy jobs created or running within the the most
        recent 30 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_copy_job_summaries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_copy_job_summaries)
        """

    def list_copy_jobs(
        self, **kwargs: Unpack[ListCopyJobsInputRequestTypeDef]
    ) -> ListCopyJobsOutputTypeDef:
        """
        Returns metadata about your copy jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_copy_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_copy_jobs)
        """

    def list_frameworks(
        self, **kwargs: Unpack[ListFrameworksInputRequestTypeDef]
    ) -> ListFrameworksOutputTypeDef:
        """
        Returns a list of all frameworks for an Amazon Web Services account and Amazon
        Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_frameworks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_frameworks)
        """

    def list_legal_holds(
        self, **kwargs: Unpack[ListLegalHoldsInputRequestTypeDef]
    ) -> ListLegalHoldsOutputTypeDef:
        """
        This action returns metadata about active and previous legal holds.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_legal_holds.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_legal_holds)
        """

    def list_protected_resources(
        self, **kwargs: Unpack[ListProtectedResourcesInputRequestTypeDef]
    ) -> ListProtectedResourcesOutputTypeDef:
        """
        Returns an array of resources successfully backed up by Backup, including the
        time the resource was saved, an Amazon Resource Name (ARN) of the resource, and
        a resource type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_protected_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_protected_resources)
        """

    def list_protected_resources_by_backup_vault(
        self, **kwargs: Unpack[ListProtectedResourcesByBackupVaultInputRequestTypeDef]
    ) -> ListProtectedResourcesByBackupVaultOutputTypeDef:
        """
        This request lists the protected resources corresponding to each backup vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_protected_resources_by_backup_vault.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_protected_resources_by_backup_vault)
        """

    def list_recovery_points_by_backup_vault(
        self, **kwargs: Unpack[ListRecoveryPointsByBackupVaultInputRequestTypeDef]
    ) -> ListRecoveryPointsByBackupVaultOutputTypeDef:
        """
        Returns detailed information about the recovery points stored in a backup vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_recovery_points_by_backup_vault.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_recovery_points_by_backup_vault)
        """

    def list_recovery_points_by_legal_hold(
        self, **kwargs: Unpack[ListRecoveryPointsByLegalHoldInputRequestTypeDef]
    ) -> ListRecoveryPointsByLegalHoldOutputTypeDef:
        """
        This action returns recovery point ARNs (Amazon Resource Names) of the
        specified legal hold.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_recovery_points_by_legal_hold.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_recovery_points_by_legal_hold)
        """

    def list_recovery_points_by_resource(
        self, **kwargs: Unpack[ListRecoveryPointsByResourceInputRequestTypeDef]
    ) -> ListRecoveryPointsByResourceOutputTypeDef:
        """
        The information about the recovery points of the type specified by a resource
        Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_recovery_points_by_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_recovery_points_by_resource)
        """

    def list_report_jobs(
        self, **kwargs: Unpack[ListReportJobsInputRequestTypeDef]
    ) -> ListReportJobsOutputTypeDef:
        """
        Returns details about your report jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_report_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_report_jobs)
        """

    def list_report_plans(
        self, **kwargs: Unpack[ListReportPlansInputRequestTypeDef]
    ) -> ListReportPlansOutputTypeDef:
        """
        Returns a list of your report plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_report_plans.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_report_plans)
        """

    def list_restore_job_summaries(
        self, **kwargs: Unpack[ListRestoreJobSummariesInputRequestTypeDef]
    ) -> ListRestoreJobSummariesOutputTypeDef:
        """
        This request obtains a summary of restore jobs created or running within the
        the most recent 30 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_restore_job_summaries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_restore_job_summaries)
        """

    def list_restore_jobs(
        self, **kwargs: Unpack[ListRestoreJobsInputRequestTypeDef]
    ) -> ListRestoreJobsOutputTypeDef:
        """
        Returns a list of jobs that Backup initiated to restore a saved resource,
        including details about the recovery process.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_restore_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_restore_jobs)
        """

    def list_restore_jobs_by_protected_resource(
        self, **kwargs: Unpack[ListRestoreJobsByProtectedResourceInputRequestTypeDef]
    ) -> ListRestoreJobsByProtectedResourceOutputTypeDef:
        """
        This returns restore jobs that contain the specified protected resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_restore_jobs_by_protected_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_restore_jobs_by_protected_resource)
        """

    def list_restore_testing_plans(
        self, **kwargs: Unpack[ListRestoreTestingPlansInputRequestTypeDef]
    ) -> ListRestoreTestingPlansOutputTypeDef:
        """
        Returns a list of restore testing plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_restore_testing_plans.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_restore_testing_plans)
        """

    def list_restore_testing_selections(
        self, **kwargs: Unpack[ListRestoreTestingSelectionsInputRequestTypeDef]
    ) -> ListRestoreTestingSelectionsOutputTypeDef:
        """
        Returns a list of restore testing selections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_restore_testing_selections.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_restore_testing_selections)
        """

    def list_tags(self, **kwargs: Unpack[ListTagsInputRequestTypeDef]) -> ListTagsOutputTypeDef:
        """
        Returns the tags assigned to the resource, such as a target recovery point,
        backup plan, or backup vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/list_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#list_tags)
        """

    def put_backup_vault_access_policy(
        self, **kwargs: Unpack[PutBackupVaultAccessPolicyInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets a resource-based policy that is used to manage access permissions on the
        target backup vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/put_backup_vault_access_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#put_backup_vault_access_policy)
        """

    def put_backup_vault_lock_configuration(
        self, **kwargs: Unpack[PutBackupVaultLockConfigurationInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Applies Backup Vault Lock to a backup vault, preventing attempts to delete any
        recovery point stored in or created in a backup vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/put_backup_vault_lock_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#put_backup_vault_lock_configuration)
        """

    def put_backup_vault_notifications(
        self, **kwargs: Unpack[PutBackupVaultNotificationsInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Turns on notifications on a backup vault for the specified topic and events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/put_backup_vault_notifications.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#put_backup_vault_notifications)
        """

    def put_restore_validation_result(
        self, **kwargs: Unpack[PutRestoreValidationResultInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This request allows you to send your independent self-run restore test
        validation results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/put_restore_validation_result.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#put_restore_validation_result)
        """

    def start_backup_job(
        self, **kwargs: Unpack[StartBackupJobInputRequestTypeDef]
    ) -> StartBackupJobOutputTypeDef:
        """
        Starts an on-demand backup job for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/start_backup_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#start_backup_job)
        """

    def start_copy_job(
        self, **kwargs: Unpack[StartCopyJobInputRequestTypeDef]
    ) -> StartCopyJobOutputTypeDef:
        """
        Starts a job to create a one-time copy of the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/start_copy_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#start_copy_job)
        """

    def start_report_job(
        self, **kwargs: Unpack[StartReportJobInputRequestTypeDef]
    ) -> StartReportJobOutputTypeDef:
        """
        Starts an on-demand report job for the specified report plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/start_report_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#start_report_job)
        """

    def start_restore_job(
        self, **kwargs: Unpack[StartRestoreJobInputRequestTypeDef]
    ) -> StartRestoreJobOutputTypeDef:
        """
        Recovers the saved resource identified by an Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/start_restore_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#start_restore_job)
        """

    def stop_backup_job(
        self, **kwargs: Unpack[StopBackupJobInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attempts to cancel a job to create a one-time backup of a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/stop_backup_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#stop_backup_job)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assigns a set of key-value pairs to a recovery point, backup plan, or backup
        vault identified by an Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a set of key-value pairs from a recovery point, backup plan, or backup
        vault identified by an Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#untag_resource)
        """

    def update_backup_plan(
        self, **kwargs: Unpack[UpdateBackupPlanInputRequestTypeDef]
    ) -> UpdateBackupPlanOutputTypeDef:
        """
        Updates the specified backup plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/update_backup_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#update_backup_plan)
        """

    def update_framework(
        self, **kwargs: Unpack[UpdateFrameworkInputRequestTypeDef]
    ) -> UpdateFrameworkOutputTypeDef:
        """
        Updates the specified framework.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/update_framework.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#update_framework)
        """

    def update_global_settings(
        self, **kwargs: Unpack[UpdateGlobalSettingsInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates whether the Amazon Web Services account is opted in to cross-account
        backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/update_global_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#update_global_settings)
        """

    def update_recovery_point_lifecycle(
        self, **kwargs: Unpack[UpdateRecoveryPointLifecycleInputRequestTypeDef]
    ) -> UpdateRecoveryPointLifecycleOutputTypeDef:
        """
        Sets the transition lifecycle of a recovery point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/update_recovery_point_lifecycle.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#update_recovery_point_lifecycle)
        """

    def update_region_settings(
        self, **kwargs: Unpack[UpdateRegionSettingsInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the current service opt-in settings for the Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/update_region_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#update_region_settings)
        """

    def update_report_plan(
        self, **kwargs: Unpack[UpdateReportPlanInputRequestTypeDef]
    ) -> UpdateReportPlanOutputTypeDef:
        """
        Updates the specified report plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/update_report_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#update_report_plan)
        """

    def update_restore_testing_plan(
        self, **kwargs: Unpack[UpdateRestoreTestingPlanInputRequestTypeDef]
    ) -> UpdateRestoreTestingPlanOutputTypeDef:
        """
        This request will send changes to your specified restore testing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/update_restore_testing_plan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#update_restore_testing_plan)
        """

    def update_restore_testing_selection(
        self, **kwargs: Unpack[UpdateRestoreTestingSelectionInputRequestTypeDef]
    ) -> UpdateRestoreTestingSelectionOutputTypeDef:
        """
        Updates the specified restore testing selection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/update_restore_testing_selection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#update_restore_testing_selection)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_backup_jobs"]) -> ListBackupJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_backup_plan_templates"]
    ) -> ListBackupPlanTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_backup_plan_versions"]
    ) -> ListBackupPlanVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_backup_plans"]
    ) -> ListBackupPlansPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_backup_selections"]
    ) -> ListBackupSelectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_backup_vaults"]
    ) -> ListBackupVaultsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_copy_jobs"]) -> ListCopyJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_legal_holds"]) -> ListLegalHoldsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_protected_resources_by_backup_vault"]
    ) -> ListProtectedResourcesByBackupVaultPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_protected_resources"]
    ) -> ListProtectedResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recovery_points_by_backup_vault"]
    ) -> ListRecoveryPointsByBackupVaultPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recovery_points_by_legal_hold"]
    ) -> ListRecoveryPointsByLegalHoldPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recovery_points_by_resource"]
    ) -> ListRecoveryPointsByResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_restore_jobs_by_protected_resource"]
    ) -> ListRestoreJobsByProtectedResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_restore_jobs"]
    ) -> ListRestoreJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_restore_testing_plans"]
    ) -> ListRestoreTestingPlansPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_restore_testing_selections"]
    ) -> ListRestoreTestingSelectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backup/client/#get_paginator)
        """
