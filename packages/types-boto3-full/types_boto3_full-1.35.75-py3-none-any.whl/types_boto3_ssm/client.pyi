"""
Type annotations for ssm service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_ssm.client import SSMClient

    session = Session()
    client: SSMClient = session.client("ssm")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeActivationsPaginator,
    DescribeAssociationExecutionsPaginator,
    DescribeAssociationExecutionTargetsPaginator,
    DescribeAutomationExecutionsPaginator,
    DescribeAutomationStepExecutionsPaginator,
    DescribeAvailablePatchesPaginator,
    DescribeEffectiveInstanceAssociationsPaginator,
    DescribeEffectivePatchesForPatchBaselinePaginator,
    DescribeInstanceAssociationsStatusPaginator,
    DescribeInstanceInformationPaginator,
    DescribeInstancePatchesPaginator,
    DescribeInstancePatchStatesForPatchGroupPaginator,
    DescribeInstancePatchStatesPaginator,
    DescribeInstancePropertiesPaginator,
    DescribeInventoryDeletionsPaginator,
    DescribeMaintenanceWindowExecutionsPaginator,
    DescribeMaintenanceWindowExecutionTaskInvocationsPaginator,
    DescribeMaintenanceWindowExecutionTasksPaginator,
    DescribeMaintenanceWindowSchedulePaginator,
    DescribeMaintenanceWindowsForTargetPaginator,
    DescribeMaintenanceWindowsPaginator,
    DescribeMaintenanceWindowTargetsPaginator,
    DescribeMaintenanceWindowTasksPaginator,
    DescribeOpsItemsPaginator,
    DescribeParametersPaginator,
    DescribePatchBaselinesPaginator,
    DescribePatchGroupsPaginator,
    DescribePatchPropertiesPaginator,
    DescribeSessionsPaginator,
    GetInventoryPaginator,
    GetInventorySchemaPaginator,
    GetOpsSummaryPaginator,
    GetParameterHistoryPaginator,
    GetParametersByPathPaginator,
    GetResourcePoliciesPaginator,
    ListAssociationsPaginator,
    ListAssociationVersionsPaginator,
    ListCommandInvocationsPaginator,
    ListCommandsPaginator,
    ListComplianceItemsPaginator,
    ListComplianceSummariesPaginator,
    ListDocumentsPaginator,
    ListDocumentVersionsPaginator,
    ListNodesPaginator,
    ListNodesSummaryPaginator,
    ListOpsItemEventsPaginator,
    ListOpsItemRelatedItemsPaginator,
    ListOpsMetadataPaginator,
    ListResourceComplianceSummariesPaginator,
    ListResourceDataSyncPaginator,
)
from .type_defs import (
    AddTagsToResourceRequestRequestTypeDef,
    AssociateOpsItemRelatedItemRequestRequestTypeDef,
    AssociateOpsItemRelatedItemResponseTypeDef,
    CancelCommandRequestRequestTypeDef,
    CancelMaintenanceWindowExecutionRequestRequestTypeDef,
    CancelMaintenanceWindowExecutionResultTypeDef,
    CreateActivationRequestRequestTypeDef,
    CreateActivationResultTypeDef,
    CreateAssociationBatchRequestRequestTypeDef,
    CreateAssociationBatchResultTypeDef,
    CreateAssociationRequestRequestTypeDef,
    CreateAssociationResultTypeDef,
    CreateDocumentRequestRequestTypeDef,
    CreateDocumentResultTypeDef,
    CreateMaintenanceWindowRequestRequestTypeDef,
    CreateMaintenanceWindowResultTypeDef,
    CreateOpsItemRequestRequestTypeDef,
    CreateOpsItemResponseTypeDef,
    CreateOpsMetadataRequestRequestTypeDef,
    CreateOpsMetadataResultTypeDef,
    CreatePatchBaselineRequestRequestTypeDef,
    CreatePatchBaselineResultTypeDef,
    CreateResourceDataSyncRequestRequestTypeDef,
    DeleteActivationRequestRequestTypeDef,
    DeleteAssociationRequestRequestTypeDef,
    DeleteDocumentRequestRequestTypeDef,
    DeleteInventoryRequestRequestTypeDef,
    DeleteInventoryResultTypeDef,
    DeleteMaintenanceWindowRequestRequestTypeDef,
    DeleteMaintenanceWindowResultTypeDef,
    DeleteOpsItemRequestRequestTypeDef,
    DeleteOpsMetadataRequestRequestTypeDef,
    DeleteParameterRequestRequestTypeDef,
    DeleteParametersRequestRequestTypeDef,
    DeleteParametersResultTypeDef,
    DeletePatchBaselineRequestRequestTypeDef,
    DeletePatchBaselineResultTypeDef,
    DeleteResourceDataSyncRequestRequestTypeDef,
    DeleteResourcePolicyRequestRequestTypeDef,
    DeregisterManagedInstanceRequestRequestTypeDef,
    DeregisterPatchBaselineForPatchGroupRequestRequestTypeDef,
    DeregisterPatchBaselineForPatchGroupResultTypeDef,
    DeregisterTargetFromMaintenanceWindowRequestRequestTypeDef,
    DeregisterTargetFromMaintenanceWindowResultTypeDef,
    DeregisterTaskFromMaintenanceWindowRequestRequestTypeDef,
    DeregisterTaskFromMaintenanceWindowResultTypeDef,
    DescribeActivationsRequestRequestTypeDef,
    DescribeActivationsResultTypeDef,
    DescribeAssociationExecutionsRequestRequestTypeDef,
    DescribeAssociationExecutionsResultTypeDef,
    DescribeAssociationExecutionTargetsRequestRequestTypeDef,
    DescribeAssociationExecutionTargetsResultTypeDef,
    DescribeAssociationRequestRequestTypeDef,
    DescribeAssociationResultTypeDef,
    DescribeAutomationExecutionsRequestRequestTypeDef,
    DescribeAutomationExecutionsResultTypeDef,
    DescribeAutomationStepExecutionsRequestRequestTypeDef,
    DescribeAutomationStepExecutionsResultTypeDef,
    DescribeAvailablePatchesRequestRequestTypeDef,
    DescribeAvailablePatchesResultTypeDef,
    DescribeDocumentPermissionRequestRequestTypeDef,
    DescribeDocumentPermissionResponseTypeDef,
    DescribeDocumentRequestRequestTypeDef,
    DescribeDocumentResultTypeDef,
    DescribeEffectiveInstanceAssociationsRequestRequestTypeDef,
    DescribeEffectiveInstanceAssociationsResultTypeDef,
    DescribeEffectivePatchesForPatchBaselineRequestRequestTypeDef,
    DescribeEffectivePatchesForPatchBaselineResultTypeDef,
    DescribeInstanceAssociationsStatusRequestRequestTypeDef,
    DescribeInstanceAssociationsStatusResultTypeDef,
    DescribeInstanceInformationRequestRequestTypeDef,
    DescribeInstanceInformationResultTypeDef,
    DescribeInstancePatchesRequestRequestTypeDef,
    DescribeInstancePatchesResultTypeDef,
    DescribeInstancePatchStatesForPatchGroupRequestRequestTypeDef,
    DescribeInstancePatchStatesForPatchGroupResultTypeDef,
    DescribeInstancePatchStatesRequestRequestTypeDef,
    DescribeInstancePatchStatesResultTypeDef,
    DescribeInstancePropertiesRequestRequestTypeDef,
    DescribeInstancePropertiesResultTypeDef,
    DescribeInventoryDeletionsRequestRequestTypeDef,
    DescribeInventoryDeletionsResultTypeDef,
    DescribeMaintenanceWindowExecutionsRequestRequestTypeDef,
    DescribeMaintenanceWindowExecutionsResultTypeDef,
    DescribeMaintenanceWindowExecutionTaskInvocationsRequestRequestTypeDef,
    DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef,
    DescribeMaintenanceWindowExecutionTasksRequestRequestTypeDef,
    DescribeMaintenanceWindowExecutionTasksResultTypeDef,
    DescribeMaintenanceWindowScheduleRequestRequestTypeDef,
    DescribeMaintenanceWindowScheduleResultTypeDef,
    DescribeMaintenanceWindowsForTargetRequestRequestTypeDef,
    DescribeMaintenanceWindowsForTargetResultTypeDef,
    DescribeMaintenanceWindowsRequestRequestTypeDef,
    DescribeMaintenanceWindowsResultTypeDef,
    DescribeMaintenanceWindowTargetsRequestRequestTypeDef,
    DescribeMaintenanceWindowTargetsResultTypeDef,
    DescribeMaintenanceWindowTasksRequestRequestTypeDef,
    DescribeMaintenanceWindowTasksResultTypeDef,
    DescribeOpsItemsRequestRequestTypeDef,
    DescribeOpsItemsResponseTypeDef,
    DescribeParametersRequestRequestTypeDef,
    DescribeParametersResultTypeDef,
    DescribePatchBaselinesRequestRequestTypeDef,
    DescribePatchBaselinesResultTypeDef,
    DescribePatchGroupsRequestRequestTypeDef,
    DescribePatchGroupsResultTypeDef,
    DescribePatchGroupStateRequestRequestTypeDef,
    DescribePatchGroupStateResultTypeDef,
    DescribePatchPropertiesRequestRequestTypeDef,
    DescribePatchPropertiesResultTypeDef,
    DescribeSessionsRequestRequestTypeDef,
    DescribeSessionsResponseTypeDef,
    DisassociateOpsItemRelatedItemRequestRequestTypeDef,
    GetAutomationExecutionRequestRequestTypeDef,
    GetAutomationExecutionResultTypeDef,
    GetCalendarStateRequestRequestTypeDef,
    GetCalendarStateResponseTypeDef,
    GetCommandInvocationRequestRequestTypeDef,
    GetCommandInvocationResultTypeDef,
    GetConnectionStatusRequestRequestTypeDef,
    GetConnectionStatusResponseTypeDef,
    GetDefaultPatchBaselineRequestRequestTypeDef,
    GetDefaultPatchBaselineResultTypeDef,
    GetDeployablePatchSnapshotForInstanceRequestRequestTypeDef,
    GetDeployablePatchSnapshotForInstanceResultTypeDef,
    GetDocumentRequestRequestTypeDef,
    GetDocumentResultTypeDef,
    GetExecutionPreviewRequestRequestTypeDef,
    GetExecutionPreviewResponseTypeDef,
    GetInventoryRequestRequestTypeDef,
    GetInventoryResultTypeDef,
    GetInventorySchemaRequestRequestTypeDef,
    GetInventorySchemaResultTypeDef,
    GetMaintenanceWindowExecutionRequestRequestTypeDef,
    GetMaintenanceWindowExecutionResultTypeDef,
    GetMaintenanceWindowExecutionTaskInvocationRequestRequestTypeDef,
    GetMaintenanceWindowExecutionTaskInvocationResultTypeDef,
    GetMaintenanceWindowExecutionTaskRequestRequestTypeDef,
    GetMaintenanceWindowExecutionTaskResultTypeDef,
    GetMaintenanceWindowRequestRequestTypeDef,
    GetMaintenanceWindowResultTypeDef,
    GetMaintenanceWindowTaskRequestRequestTypeDef,
    GetMaintenanceWindowTaskResultTypeDef,
    GetOpsItemRequestRequestTypeDef,
    GetOpsItemResponseTypeDef,
    GetOpsMetadataRequestRequestTypeDef,
    GetOpsMetadataResultTypeDef,
    GetOpsSummaryRequestRequestTypeDef,
    GetOpsSummaryResultTypeDef,
    GetParameterHistoryRequestRequestTypeDef,
    GetParameterHistoryResultTypeDef,
    GetParameterRequestRequestTypeDef,
    GetParameterResultTypeDef,
    GetParametersByPathRequestRequestTypeDef,
    GetParametersByPathResultTypeDef,
    GetParametersRequestRequestTypeDef,
    GetParametersResultTypeDef,
    GetPatchBaselineForPatchGroupRequestRequestTypeDef,
    GetPatchBaselineForPatchGroupResultTypeDef,
    GetPatchBaselineRequestRequestTypeDef,
    GetPatchBaselineResultTypeDef,
    GetResourcePoliciesRequestRequestTypeDef,
    GetResourcePoliciesResponseTypeDef,
    GetServiceSettingRequestRequestTypeDef,
    GetServiceSettingResultTypeDef,
    LabelParameterVersionRequestRequestTypeDef,
    LabelParameterVersionResultTypeDef,
    ListAssociationsRequestRequestTypeDef,
    ListAssociationsResultTypeDef,
    ListAssociationVersionsRequestRequestTypeDef,
    ListAssociationVersionsResultTypeDef,
    ListCommandInvocationsRequestRequestTypeDef,
    ListCommandInvocationsResultTypeDef,
    ListCommandsRequestRequestTypeDef,
    ListCommandsResultTypeDef,
    ListComplianceItemsRequestRequestTypeDef,
    ListComplianceItemsResultTypeDef,
    ListComplianceSummariesRequestRequestTypeDef,
    ListComplianceSummariesResultTypeDef,
    ListDocumentMetadataHistoryRequestRequestTypeDef,
    ListDocumentMetadataHistoryResponseTypeDef,
    ListDocumentsRequestRequestTypeDef,
    ListDocumentsResultTypeDef,
    ListDocumentVersionsRequestRequestTypeDef,
    ListDocumentVersionsResultTypeDef,
    ListInventoryEntriesRequestRequestTypeDef,
    ListInventoryEntriesResultTypeDef,
    ListNodesRequestRequestTypeDef,
    ListNodesResultTypeDef,
    ListNodesSummaryRequestRequestTypeDef,
    ListNodesSummaryResultTypeDef,
    ListOpsItemEventsRequestRequestTypeDef,
    ListOpsItemEventsResponseTypeDef,
    ListOpsItemRelatedItemsRequestRequestTypeDef,
    ListOpsItemRelatedItemsResponseTypeDef,
    ListOpsMetadataRequestRequestTypeDef,
    ListOpsMetadataResultTypeDef,
    ListResourceComplianceSummariesRequestRequestTypeDef,
    ListResourceComplianceSummariesResultTypeDef,
    ListResourceDataSyncRequestRequestTypeDef,
    ListResourceDataSyncResultTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResultTypeDef,
    ModifyDocumentPermissionRequestRequestTypeDef,
    PutComplianceItemsRequestRequestTypeDef,
    PutInventoryRequestRequestTypeDef,
    PutInventoryResultTypeDef,
    PutParameterRequestRequestTypeDef,
    PutParameterResultTypeDef,
    PutResourcePolicyRequestRequestTypeDef,
    PutResourcePolicyResponseTypeDef,
    RegisterDefaultPatchBaselineRequestRequestTypeDef,
    RegisterDefaultPatchBaselineResultTypeDef,
    RegisterPatchBaselineForPatchGroupRequestRequestTypeDef,
    RegisterPatchBaselineForPatchGroupResultTypeDef,
    RegisterTargetWithMaintenanceWindowRequestRequestTypeDef,
    RegisterTargetWithMaintenanceWindowResultTypeDef,
    RegisterTaskWithMaintenanceWindowRequestRequestTypeDef,
    RegisterTaskWithMaintenanceWindowResultTypeDef,
    RemoveTagsFromResourceRequestRequestTypeDef,
    ResetServiceSettingRequestRequestTypeDef,
    ResetServiceSettingResultTypeDef,
    ResumeSessionRequestRequestTypeDef,
    ResumeSessionResponseTypeDef,
    SendAutomationSignalRequestRequestTypeDef,
    SendCommandRequestRequestTypeDef,
    SendCommandResultTypeDef,
    StartAssociationsOnceRequestRequestTypeDef,
    StartAutomationExecutionRequestRequestTypeDef,
    StartAutomationExecutionResultTypeDef,
    StartChangeRequestExecutionRequestRequestTypeDef,
    StartChangeRequestExecutionResultTypeDef,
    StartExecutionPreviewRequestRequestTypeDef,
    StartExecutionPreviewResponseTypeDef,
    StartSessionRequestRequestTypeDef,
    StartSessionResponseTypeDef,
    StopAutomationExecutionRequestRequestTypeDef,
    TerminateSessionRequestRequestTypeDef,
    TerminateSessionResponseTypeDef,
    UnlabelParameterVersionRequestRequestTypeDef,
    UnlabelParameterVersionResultTypeDef,
    UpdateAssociationRequestRequestTypeDef,
    UpdateAssociationResultTypeDef,
    UpdateAssociationStatusRequestRequestTypeDef,
    UpdateAssociationStatusResultTypeDef,
    UpdateDocumentDefaultVersionRequestRequestTypeDef,
    UpdateDocumentDefaultVersionResultTypeDef,
    UpdateDocumentMetadataRequestRequestTypeDef,
    UpdateDocumentRequestRequestTypeDef,
    UpdateDocumentResultTypeDef,
    UpdateMaintenanceWindowRequestRequestTypeDef,
    UpdateMaintenanceWindowResultTypeDef,
    UpdateMaintenanceWindowTargetRequestRequestTypeDef,
    UpdateMaintenanceWindowTargetResultTypeDef,
    UpdateMaintenanceWindowTaskRequestRequestTypeDef,
    UpdateMaintenanceWindowTaskResultTypeDef,
    UpdateManagedInstanceRoleRequestRequestTypeDef,
    UpdateOpsItemRequestRequestTypeDef,
    UpdateOpsMetadataRequestRequestTypeDef,
    UpdateOpsMetadataResultTypeDef,
    UpdatePatchBaselineRequestRequestTypeDef,
    UpdatePatchBaselineResultTypeDef,
    UpdateResourceDataSyncRequestRequestTypeDef,
    UpdateServiceSettingRequestRequestTypeDef,
)
from .waiter import CommandExecutedWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("SSMClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    AssociatedInstances: Type[BotocoreClientError]
    AssociationAlreadyExists: Type[BotocoreClientError]
    AssociationDoesNotExist: Type[BotocoreClientError]
    AssociationExecutionDoesNotExist: Type[BotocoreClientError]
    AssociationLimitExceeded: Type[BotocoreClientError]
    AssociationVersionLimitExceeded: Type[BotocoreClientError]
    AutomationDefinitionNotApprovedException: Type[BotocoreClientError]
    AutomationDefinitionNotFoundException: Type[BotocoreClientError]
    AutomationDefinitionVersionNotFoundException: Type[BotocoreClientError]
    AutomationExecutionLimitExceededException: Type[BotocoreClientError]
    AutomationExecutionNotFoundException: Type[BotocoreClientError]
    AutomationStepNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ComplianceTypeCountLimitExceededException: Type[BotocoreClientError]
    CustomSchemaCountLimitExceededException: Type[BotocoreClientError]
    DocumentAlreadyExists: Type[BotocoreClientError]
    DocumentLimitExceeded: Type[BotocoreClientError]
    DocumentPermissionLimit: Type[BotocoreClientError]
    DocumentVersionLimitExceeded: Type[BotocoreClientError]
    DoesNotExistException: Type[BotocoreClientError]
    DuplicateDocumentContent: Type[BotocoreClientError]
    DuplicateDocumentVersionName: Type[BotocoreClientError]
    DuplicateInstanceId: Type[BotocoreClientError]
    FeatureNotAvailableException: Type[BotocoreClientError]
    HierarchyLevelLimitExceededException: Type[BotocoreClientError]
    HierarchyTypeMismatchException: Type[BotocoreClientError]
    IdempotentParameterMismatch: Type[BotocoreClientError]
    IncompatiblePolicyException: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InvalidActivation: Type[BotocoreClientError]
    InvalidActivationId: Type[BotocoreClientError]
    InvalidAggregatorException: Type[BotocoreClientError]
    InvalidAllowedPatternException: Type[BotocoreClientError]
    InvalidAssociation: Type[BotocoreClientError]
    InvalidAssociationVersion: Type[BotocoreClientError]
    InvalidAutomationExecutionParametersException: Type[BotocoreClientError]
    InvalidAutomationSignalException: Type[BotocoreClientError]
    InvalidAutomationStatusUpdateException: Type[BotocoreClientError]
    InvalidCommandId: Type[BotocoreClientError]
    InvalidDeleteInventoryParametersException: Type[BotocoreClientError]
    InvalidDeletionIdException: Type[BotocoreClientError]
    InvalidDocument: Type[BotocoreClientError]
    InvalidDocumentContent: Type[BotocoreClientError]
    InvalidDocumentOperation: Type[BotocoreClientError]
    InvalidDocumentSchemaVersion: Type[BotocoreClientError]
    InvalidDocumentType: Type[BotocoreClientError]
    InvalidDocumentVersion: Type[BotocoreClientError]
    InvalidFilter: Type[BotocoreClientError]
    InvalidFilterKey: Type[BotocoreClientError]
    InvalidFilterOption: Type[BotocoreClientError]
    InvalidFilterValue: Type[BotocoreClientError]
    InvalidInstanceId: Type[BotocoreClientError]
    InvalidInstanceInformationFilterValue: Type[BotocoreClientError]
    InvalidInstancePropertyFilterValue: Type[BotocoreClientError]
    InvalidInventoryGroupException: Type[BotocoreClientError]
    InvalidInventoryItemContextException: Type[BotocoreClientError]
    InvalidInventoryRequestException: Type[BotocoreClientError]
    InvalidItemContentException: Type[BotocoreClientError]
    InvalidKeyId: Type[BotocoreClientError]
    InvalidNextToken: Type[BotocoreClientError]
    InvalidNotificationConfig: Type[BotocoreClientError]
    InvalidOptionException: Type[BotocoreClientError]
    InvalidOutputFolder: Type[BotocoreClientError]
    InvalidOutputLocation: Type[BotocoreClientError]
    InvalidParameters: Type[BotocoreClientError]
    InvalidPermissionType: Type[BotocoreClientError]
    InvalidPluginName: Type[BotocoreClientError]
    InvalidPolicyAttributeException: Type[BotocoreClientError]
    InvalidPolicyTypeException: Type[BotocoreClientError]
    InvalidResourceId: Type[BotocoreClientError]
    InvalidResourceType: Type[BotocoreClientError]
    InvalidResultAttributeException: Type[BotocoreClientError]
    InvalidRole: Type[BotocoreClientError]
    InvalidSchedule: Type[BotocoreClientError]
    InvalidTag: Type[BotocoreClientError]
    InvalidTarget: Type[BotocoreClientError]
    InvalidTargetMaps: Type[BotocoreClientError]
    InvalidTypeNameException: Type[BotocoreClientError]
    InvalidUpdate: Type[BotocoreClientError]
    InvocationDoesNotExist: Type[BotocoreClientError]
    ItemContentMismatchException: Type[BotocoreClientError]
    ItemSizeLimitExceededException: Type[BotocoreClientError]
    MalformedResourcePolicyDocumentException: Type[BotocoreClientError]
    MaxDocumentSizeExceeded: Type[BotocoreClientError]
    OpsItemAccessDeniedException: Type[BotocoreClientError]
    OpsItemAlreadyExistsException: Type[BotocoreClientError]
    OpsItemConflictException: Type[BotocoreClientError]
    OpsItemInvalidParameterException: Type[BotocoreClientError]
    OpsItemLimitExceededException: Type[BotocoreClientError]
    OpsItemNotFoundException: Type[BotocoreClientError]
    OpsItemRelatedItemAlreadyExistsException: Type[BotocoreClientError]
    OpsItemRelatedItemAssociationNotFoundException: Type[BotocoreClientError]
    OpsMetadataAlreadyExistsException: Type[BotocoreClientError]
    OpsMetadataInvalidArgumentException: Type[BotocoreClientError]
    OpsMetadataKeyLimitExceededException: Type[BotocoreClientError]
    OpsMetadataLimitExceededException: Type[BotocoreClientError]
    OpsMetadataNotFoundException: Type[BotocoreClientError]
    OpsMetadataTooManyUpdatesException: Type[BotocoreClientError]
    ParameterAlreadyExists: Type[BotocoreClientError]
    ParameterLimitExceeded: Type[BotocoreClientError]
    ParameterMaxVersionLimitExceeded: Type[BotocoreClientError]
    ParameterNotFound: Type[BotocoreClientError]
    ParameterPatternMismatchException: Type[BotocoreClientError]
    ParameterVersionLabelLimitExceeded: Type[BotocoreClientError]
    ParameterVersionNotFound: Type[BotocoreClientError]
    PoliciesLimitExceededException: Type[BotocoreClientError]
    ResourceDataSyncAlreadyExistsException: Type[BotocoreClientError]
    ResourceDataSyncConflictException: Type[BotocoreClientError]
    ResourceDataSyncCountExceededException: Type[BotocoreClientError]
    ResourceDataSyncInvalidConfigurationException: Type[BotocoreClientError]
    ResourceDataSyncNotFoundException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourcePolicyConflictException: Type[BotocoreClientError]
    ResourcePolicyInvalidParameterException: Type[BotocoreClientError]
    ResourcePolicyLimitExceededException: Type[BotocoreClientError]
    ResourcePolicyNotFoundException: Type[BotocoreClientError]
    ServiceSettingNotFound: Type[BotocoreClientError]
    StatusUnchanged: Type[BotocoreClientError]
    SubTypeCountLimitExceededException: Type[BotocoreClientError]
    TargetInUseException: Type[BotocoreClientError]
    TargetNotConnected: Type[BotocoreClientError]
    TooManyTagsError: Type[BotocoreClientError]
    TooManyUpdates: Type[BotocoreClientError]
    TotalSizeLimitExceededException: Type[BotocoreClientError]
    UnsupportedCalendarException: Type[BotocoreClientError]
    UnsupportedFeatureRequiredException: Type[BotocoreClientError]
    UnsupportedInventoryItemContextException: Type[BotocoreClientError]
    UnsupportedInventorySchemaVersionException: Type[BotocoreClientError]
    UnsupportedOperatingSystem: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]
    UnsupportedParameterType: Type[BotocoreClientError]
    UnsupportedPlatformType: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class SSMClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SSMClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#close)
        """

    def add_tags_to_resource(
        self, **kwargs: Unpack[AddTagsToResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds or overwrites one or more tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/add_tags_to_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#add_tags_to_resource)
        """

    def associate_ops_item_related_item(
        self, **kwargs: Unpack[AssociateOpsItemRelatedItemRequestRequestTypeDef]
    ) -> AssociateOpsItemRelatedItemResponseTypeDef:
        """
        Associates a related item to a Systems Manager OpsCenter OpsItem.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/associate_ops_item_related_item.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#associate_ops_item_related_item)
        """

    def cancel_command(
        self, **kwargs: Unpack[CancelCommandRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Attempts to cancel the command specified by the Command ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/cancel_command.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#cancel_command)
        """

    def cancel_maintenance_window_execution(
        self, **kwargs: Unpack[CancelMaintenanceWindowExecutionRequestRequestTypeDef]
    ) -> CancelMaintenanceWindowExecutionResultTypeDef:
        """
        Stops a maintenance window execution that is already in progress and cancels
        any tasks in the window that haven't already starting running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/cancel_maintenance_window_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#cancel_maintenance_window_execution)
        """

    def create_activation(
        self, **kwargs: Unpack[CreateActivationRequestRequestTypeDef]
    ) -> CreateActivationResultTypeDef:
        """
        Generates an activation code and activation ID you can use to register your
        on-premises servers, edge devices, or virtual machine (VM) with Amazon Web
        Services Systems Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/create_activation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#create_activation)
        """

    def create_association(
        self, **kwargs: Unpack[CreateAssociationRequestRequestTypeDef]
    ) -> CreateAssociationResultTypeDef:
        """
        A State Manager association defines the state that you want to maintain on your
        managed nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/create_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#create_association)
        """

    def create_association_batch(
        self, **kwargs: Unpack[CreateAssociationBatchRequestRequestTypeDef]
    ) -> CreateAssociationBatchResultTypeDef:
        """
        Associates the specified Amazon Web Services Systems Manager document (SSM
        document) with the specified managed nodes or targets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/create_association_batch.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#create_association_batch)
        """

    def create_document(
        self, **kwargs: Unpack[CreateDocumentRequestRequestTypeDef]
    ) -> CreateDocumentResultTypeDef:
        """
        Creates a Amazon Web Services Systems Manager (SSM document).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/create_document.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#create_document)
        """

    def create_maintenance_window(
        self, **kwargs: Unpack[CreateMaintenanceWindowRequestRequestTypeDef]
    ) -> CreateMaintenanceWindowResultTypeDef:
        """
        Creates a new maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/create_maintenance_window.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#create_maintenance_window)
        """

    def create_ops_item(
        self, **kwargs: Unpack[CreateOpsItemRequestRequestTypeDef]
    ) -> CreateOpsItemResponseTypeDef:
        """
        Creates a new OpsItem.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/create_ops_item.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#create_ops_item)
        """

    def create_ops_metadata(
        self, **kwargs: Unpack[CreateOpsMetadataRequestRequestTypeDef]
    ) -> CreateOpsMetadataResultTypeDef:
        """
        If you create a new application in Application Manager, Amazon Web Services
        Systems Manager calls this API operation to specify information about the new
        application, including the application type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/create_ops_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#create_ops_metadata)
        """

    def create_patch_baseline(
        self, **kwargs: Unpack[CreatePatchBaselineRequestRequestTypeDef]
    ) -> CreatePatchBaselineResultTypeDef:
        """
        Creates a patch baseline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/create_patch_baseline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#create_patch_baseline)
        """

    def create_resource_data_sync(
        self, **kwargs: Unpack[CreateResourceDataSyncRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        A resource data sync helps you view data from multiple sources in a single
        location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/create_resource_data_sync.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#create_resource_data_sync)
        """

    def delete_activation(
        self, **kwargs: Unpack[DeleteActivationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an activation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/delete_activation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#delete_activation)
        """

    def delete_association(
        self, **kwargs: Unpack[DeleteAssociationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the specified Amazon Web Services Systems Manager document (SSM
        document) from the specified managed node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/delete_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#delete_association)
        """

    def delete_document(
        self, **kwargs: Unpack[DeleteDocumentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the Amazon Web Services Systems Manager document (SSM document) and all
        managed node associations to the document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/delete_document.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#delete_document)
        """

    def delete_inventory(
        self, **kwargs: Unpack[DeleteInventoryRequestRequestTypeDef]
    ) -> DeleteInventoryResultTypeDef:
        """
        Delete a custom inventory type or the data associated with a custom Inventory
        type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/delete_inventory.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#delete_inventory)
        """

    def delete_maintenance_window(
        self, **kwargs: Unpack[DeleteMaintenanceWindowRequestRequestTypeDef]
    ) -> DeleteMaintenanceWindowResultTypeDef:
        """
        Deletes a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/delete_maintenance_window.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#delete_maintenance_window)
        """

    def delete_ops_item(
        self, **kwargs: Unpack[DeleteOpsItemRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete an OpsItem.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/delete_ops_item.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#delete_ops_item)
        """

    def delete_ops_metadata(
        self, **kwargs: Unpack[DeleteOpsMetadataRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete OpsMetadata related to an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/delete_ops_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#delete_ops_metadata)
        """

    def delete_parameter(
        self, **kwargs: Unpack[DeleteParameterRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete a parameter from the system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/delete_parameter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#delete_parameter)
        """

    def delete_parameters(
        self, **kwargs: Unpack[DeleteParametersRequestRequestTypeDef]
    ) -> DeleteParametersResultTypeDef:
        """
        Delete a list of parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/delete_parameters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#delete_parameters)
        """

    def delete_patch_baseline(
        self, **kwargs: Unpack[DeletePatchBaselineRequestRequestTypeDef]
    ) -> DeletePatchBaselineResultTypeDef:
        """
        Deletes a patch baseline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/delete_patch_baseline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#delete_patch_baseline)
        """

    def delete_resource_data_sync(
        self, **kwargs: Unpack[DeleteResourceDataSyncRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a resource data sync configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/delete_resource_data_sync.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#delete_resource_data_sync)
        """

    def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Systems Manager resource policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/delete_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#delete_resource_policy)
        """

    def deregister_managed_instance(
        self, **kwargs: Unpack[DeregisterManagedInstanceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the server or virtual machine from the list of registered servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/deregister_managed_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#deregister_managed_instance)
        """

    def deregister_patch_baseline_for_patch_group(
        self, **kwargs: Unpack[DeregisterPatchBaselineForPatchGroupRequestRequestTypeDef]
    ) -> DeregisterPatchBaselineForPatchGroupResultTypeDef:
        """
        Removes a patch group from a patch baseline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/deregister_patch_baseline_for_patch_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#deregister_patch_baseline_for_patch_group)
        """

    def deregister_target_from_maintenance_window(
        self, **kwargs: Unpack[DeregisterTargetFromMaintenanceWindowRequestRequestTypeDef]
    ) -> DeregisterTargetFromMaintenanceWindowResultTypeDef:
        """
        Removes a target from a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/deregister_target_from_maintenance_window.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#deregister_target_from_maintenance_window)
        """

    def deregister_task_from_maintenance_window(
        self, **kwargs: Unpack[DeregisterTaskFromMaintenanceWindowRequestRequestTypeDef]
    ) -> DeregisterTaskFromMaintenanceWindowResultTypeDef:
        """
        Removes a task from a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/deregister_task_from_maintenance_window.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#deregister_task_from_maintenance_window)
        """

    def describe_activations(
        self, **kwargs: Unpack[DescribeActivationsRequestRequestTypeDef]
    ) -> DescribeActivationsResultTypeDef:
        """
        Describes details about the activation, such as the date and time the
        activation was created, its expiration date, the Identity and Access Management
        (IAM) role assigned to the managed nodes in the activation, and the number of
        nodes registered by using this activation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_activations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_activations)
        """

    def describe_association(
        self, **kwargs: Unpack[DescribeAssociationRequestRequestTypeDef]
    ) -> DescribeAssociationResultTypeDef:
        """
        Describes the association for the specified target or managed node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_association)
        """

    def describe_association_execution_targets(
        self, **kwargs: Unpack[DescribeAssociationExecutionTargetsRequestRequestTypeDef]
    ) -> DescribeAssociationExecutionTargetsResultTypeDef:
        """
        Views information about a specific execution of a specific association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_association_execution_targets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_association_execution_targets)
        """

    def describe_association_executions(
        self, **kwargs: Unpack[DescribeAssociationExecutionsRequestRequestTypeDef]
    ) -> DescribeAssociationExecutionsResultTypeDef:
        """
        Views all executions for a specific association ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_association_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_association_executions)
        """

    def describe_automation_executions(
        self, **kwargs: Unpack[DescribeAutomationExecutionsRequestRequestTypeDef]
    ) -> DescribeAutomationExecutionsResultTypeDef:
        """
        Provides details about all active and terminated Automation executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_automation_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_automation_executions)
        """

    def describe_automation_step_executions(
        self, **kwargs: Unpack[DescribeAutomationStepExecutionsRequestRequestTypeDef]
    ) -> DescribeAutomationStepExecutionsResultTypeDef:
        """
        Information about all active and terminated step executions in an Automation
        workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_automation_step_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_automation_step_executions)
        """

    def describe_available_patches(
        self, **kwargs: Unpack[DescribeAvailablePatchesRequestRequestTypeDef]
    ) -> DescribeAvailablePatchesResultTypeDef:
        """
        Lists all patches eligible to be included in a patch baseline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_available_patches.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_available_patches)
        """

    def describe_document(
        self, **kwargs: Unpack[DescribeDocumentRequestRequestTypeDef]
    ) -> DescribeDocumentResultTypeDef:
        """
        Describes the specified Amazon Web Services Systems Manager document (SSM
        document).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_document.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_document)
        """

    def describe_document_permission(
        self, **kwargs: Unpack[DescribeDocumentPermissionRequestRequestTypeDef]
    ) -> DescribeDocumentPermissionResponseTypeDef:
        """
        Describes the permissions for a Amazon Web Services Systems Manager document
        (SSM document).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_document_permission.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_document_permission)
        """

    def describe_effective_instance_associations(
        self, **kwargs: Unpack[DescribeEffectiveInstanceAssociationsRequestRequestTypeDef]
    ) -> DescribeEffectiveInstanceAssociationsResultTypeDef:
        """
        All associations for the managed nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_effective_instance_associations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_effective_instance_associations)
        """

    def describe_effective_patches_for_patch_baseline(
        self, **kwargs: Unpack[DescribeEffectivePatchesForPatchBaselineRequestRequestTypeDef]
    ) -> DescribeEffectivePatchesForPatchBaselineResultTypeDef:
        """
        Retrieves the current effective patches (the patch and the approval state) for
        the specified patch baseline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_effective_patches_for_patch_baseline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_effective_patches_for_patch_baseline)
        """

    def describe_instance_associations_status(
        self, **kwargs: Unpack[DescribeInstanceAssociationsStatusRequestRequestTypeDef]
    ) -> DescribeInstanceAssociationsStatusResultTypeDef:
        """
        The status of the associations for the managed nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_instance_associations_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_instance_associations_status)
        """

    def describe_instance_information(
        self, **kwargs: Unpack[DescribeInstanceInformationRequestRequestTypeDef]
    ) -> DescribeInstanceInformationResultTypeDef:
        """
        Provides information about one or more of your managed nodes, including the
        operating system platform, SSM Agent version, association status, and IP
        address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_instance_information.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_instance_information)
        """

    def describe_instance_patch_states(
        self, **kwargs: Unpack[DescribeInstancePatchStatesRequestRequestTypeDef]
    ) -> DescribeInstancePatchStatesResultTypeDef:
        """
        Retrieves the high-level patch state of one or more managed nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_instance_patch_states.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_instance_patch_states)
        """

    def describe_instance_patch_states_for_patch_group(
        self, **kwargs: Unpack[DescribeInstancePatchStatesForPatchGroupRequestRequestTypeDef]
    ) -> DescribeInstancePatchStatesForPatchGroupResultTypeDef:
        """
        Retrieves the high-level patch state for the managed nodes in the specified
        patch group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_instance_patch_states_for_patch_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_instance_patch_states_for_patch_group)
        """

    def describe_instance_patches(
        self, **kwargs: Unpack[DescribeInstancePatchesRequestRequestTypeDef]
    ) -> DescribeInstancePatchesResultTypeDef:
        """
        Retrieves information about the patches on the specified managed node and their
        state relative to the patch baseline being used for the node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_instance_patches.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_instance_patches)
        """

    def describe_instance_properties(
        self, **kwargs: Unpack[DescribeInstancePropertiesRequestRequestTypeDef]
    ) -> DescribeInstancePropertiesResultTypeDef:
        """
        An API operation used by the Systems Manager console to display information
        about Systems Manager managed nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_instance_properties.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_instance_properties)
        """

    def describe_inventory_deletions(
        self, **kwargs: Unpack[DescribeInventoryDeletionsRequestRequestTypeDef]
    ) -> DescribeInventoryDeletionsResultTypeDef:
        """
        Describes a specific delete inventory operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_inventory_deletions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_inventory_deletions)
        """

    def describe_maintenance_window_execution_task_invocations(
        self,
        **kwargs: Unpack[DescribeMaintenanceWindowExecutionTaskInvocationsRequestRequestTypeDef],
    ) -> DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef:
        """
        Retrieves the individual task executions (one per target) for a particular task
        run as part of a maintenance window execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_maintenance_window_execution_task_invocations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_maintenance_window_execution_task_invocations)
        """

    def describe_maintenance_window_execution_tasks(
        self, **kwargs: Unpack[DescribeMaintenanceWindowExecutionTasksRequestRequestTypeDef]
    ) -> DescribeMaintenanceWindowExecutionTasksResultTypeDef:
        """
        For a given maintenance window execution, lists the tasks that were run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_maintenance_window_execution_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_maintenance_window_execution_tasks)
        """

    def describe_maintenance_window_executions(
        self, **kwargs: Unpack[DescribeMaintenanceWindowExecutionsRequestRequestTypeDef]
    ) -> DescribeMaintenanceWindowExecutionsResultTypeDef:
        """
        Lists the executions of a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_maintenance_window_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_maintenance_window_executions)
        """

    def describe_maintenance_window_schedule(
        self, **kwargs: Unpack[DescribeMaintenanceWindowScheduleRequestRequestTypeDef]
    ) -> DescribeMaintenanceWindowScheduleResultTypeDef:
        """
        Retrieves information about upcoming executions of a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_maintenance_window_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_maintenance_window_schedule)
        """

    def describe_maintenance_window_targets(
        self, **kwargs: Unpack[DescribeMaintenanceWindowTargetsRequestRequestTypeDef]
    ) -> DescribeMaintenanceWindowTargetsResultTypeDef:
        """
        Lists the targets registered with the maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_maintenance_window_targets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_maintenance_window_targets)
        """

    def describe_maintenance_window_tasks(
        self, **kwargs: Unpack[DescribeMaintenanceWindowTasksRequestRequestTypeDef]
    ) -> DescribeMaintenanceWindowTasksResultTypeDef:
        """
        Lists the tasks in a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_maintenance_window_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_maintenance_window_tasks)
        """

    def describe_maintenance_windows(
        self, **kwargs: Unpack[DescribeMaintenanceWindowsRequestRequestTypeDef]
    ) -> DescribeMaintenanceWindowsResultTypeDef:
        """
        Retrieves the maintenance windows in an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_maintenance_windows.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_maintenance_windows)
        """

    def describe_maintenance_windows_for_target(
        self, **kwargs: Unpack[DescribeMaintenanceWindowsForTargetRequestRequestTypeDef]
    ) -> DescribeMaintenanceWindowsForTargetResultTypeDef:
        """
        Retrieves information about the maintenance window targets or tasks that a
        managed node is associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_maintenance_windows_for_target.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_maintenance_windows_for_target)
        """

    def describe_ops_items(
        self, **kwargs: Unpack[DescribeOpsItemsRequestRequestTypeDef]
    ) -> DescribeOpsItemsResponseTypeDef:
        """
        Query a set of OpsItems.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_ops_items.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_ops_items)
        """

    def describe_parameters(
        self, **kwargs: Unpack[DescribeParametersRequestRequestTypeDef]
    ) -> DescribeParametersResultTypeDef:
        """
        Lists the parameters in your Amazon Web Services account or the parameters
        shared with you when you enable the <a
        href="https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_DescribeParameters.html#systemsmanager-DescribeParameters-request-Shared">Shared</a>
        option.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_parameters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_parameters)
        """

    def describe_patch_baselines(
        self, **kwargs: Unpack[DescribePatchBaselinesRequestRequestTypeDef]
    ) -> DescribePatchBaselinesResultTypeDef:
        """
        Lists the patch baselines in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_patch_baselines.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_patch_baselines)
        """

    def describe_patch_group_state(
        self, **kwargs: Unpack[DescribePatchGroupStateRequestRequestTypeDef]
    ) -> DescribePatchGroupStateResultTypeDef:
        """
        Returns high-level aggregated patch compliance state information for a patch
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_patch_group_state.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_patch_group_state)
        """

    def describe_patch_groups(
        self, **kwargs: Unpack[DescribePatchGroupsRequestRequestTypeDef]
    ) -> DescribePatchGroupsResultTypeDef:
        """
        Lists all patch groups that have been registered with patch baselines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_patch_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_patch_groups)
        """

    def describe_patch_properties(
        self, **kwargs: Unpack[DescribePatchPropertiesRequestRequestTypeDef]
    ) -> DescribePatchPropertiesResultTypeDef:
        """
        Lists the properties of available patches organized by product, product family,
        classification, severity, and other properties of available patches.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_patch_properties.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_patch_properties)
        """

    def describe_sessions(
        self, **kwargs: Unpack[DescribeSessionsRequestRequestTypeDef]
    ) -> DescribeSessionsResponseTypeDef:
        """
        Retrieves a list of all active sessions (both connected and disconnected) or
        terminated sessions from the past 30 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/describe_sessions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#describe_sessions)
        """

    def disassociate_ops_item_related_item(
        self, **kwargs: Unpack[DisassociateOpsItemRelatedItemRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the association between an OpsItem and a related item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/disassociate_ops_item_related_item.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#disassociate_ops_item_related_item)
        """

    def get_automation_execution(
        self, **kwargs: Unpack[GetAutomationExecutionRequestRequestTypeDef]
    ) -> GetAutomationExecutionResultTypeDef:
        """
        Get detailed information about a particular Automation execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_automation_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_automation_execution)
        """

    def get_calendar_state(
        self, **kwargs: Unpack[GetCalendarStateRequestRequestTypeDef]
    ) -> GetCalendarStateResponseTypeDef:
        """
        Gets the state of a Amazon Web Services Systems Manager change calendar at the
        current time or a specified time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_calendar_state.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_calendar_state)
        """

    def get_command_invocation(
        self, **kwargs: Unpack[GetCommandInvocationRequestRequestTypeDef]
    ) -> GetCommandInvocationResultTypeDef:
        """
        Returns detailed information about command execution for an invocation or
        plugin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_command_invocation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_command_invocation)
        """

    def get_connection_status(
        self, **kwargs: Unpack[GetConnectionStatusRequestRequestTypeDef]
    ) -> GetConnectionStatusResponseTypeDef:
        """
        Retrieves the Session Manager connection status for a managed node to determine
        whether it is running and ready to receive Session Manager connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_connection_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_connection_status)
        """

    def get_default_patch_baseline(
        self, **kwargs: Unpack[GetDefaultPatchBaselineRequestRequestTypeDef]
    ) -> GetDefaultPatchBaselineResultTypeDef:
        """
        Retrieves the default patch baseline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_default_patch_baseline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_default_patch_baseline)
        """

    def get_deployable_patch_snapshot_for_instance(
        self, **kwargs: Unpack[GetDeployablePatchSnapshotForInstanceRequestRequestTypeDef]
    ) -> GetDeployablePatchSnapshotForInstanceResultTypeDef:
        """
        Retrieves the current snapshot for the patch baseline the managed node uses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_deployable_patch_snapshot_for_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_deployable_patch_snapshot_for_instance)
        """

    def get_document(
        self, **kwargs: Unpack[GetDocumentRequestRequestTypeDef]
    ) -> GetDocumentResultTypeDef:
        """
        Gets the contents of the specified Amazon Web Services Systems Manager document
        (SSM document).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_document.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_document)
        """

    def get_execution_preview(
        self, **kwargs: Unpack[GetExecutionPreviewRequestRequestTypeDef]
    ) -> GetExecutionPreviewResponseTypeDef:
        """
        Initiates the process of retrieving an existing preview that shows the effects
        that running a specified Automation runbook would have on the targeted
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_execution_preview.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_execution_preview)
        """

    def get_inventory(
        self, **kwargs: Unpack[GetInventoryRequestRequestTypeDef]
    ) -> GetInventoryResultTypeDef:
        """
        Query inventory information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_inventory.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_inventory)
        """

    def get_inventory_schema(
        self, **kwargs: Unpack[GetInventorySchemaRequestRequestTypeDef]
    ) -> GetInventorySchemaResultTypeDef:
        """
        Return a list of inventory type names for the account, or return a list of
        attribute names for a specific Inventory item type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_inventory_schema.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_inventory_schema)
        """

    def get_maintenance_window(
        self, **kwargs: Unpack[GetMaintenanceWindowRequestRequestTypeDef]
    ) -> GetMaintenanceWindowResultTypeDef:
        """
        Retrieves a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_maintenance_window.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_maintenance_window)
        """

    def get_maintenance_window_execution(
        self, **kwargs: Unpack[GetMaintenanceWindowExecutionRequestRequestTypeDef]
    ) -> GetMaintenanceWindowExecutionResultTypeDef:
        """
        Retrieves details about a specific a maintenance window execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_maintenance_window_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_maintenance_window_execution)
        """

    def get_maintenance_window_execution_task(
        self, **kwargs: Unpack[GetMaintenanceWindowExecutionTaskRequestRequestTypeDef]
    ) -> GetMaintenanceWindowExecutionTaskResultTypeDef:
        """
        Retrieves the details about a specific task run as part of a maintenance window
        execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_maintenance_window_execution_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_maintenance_window_execution_task)
        """

    def get_maintenance_window_execution_task_invocation(
        self, **kwargs: Unpack[GetMaintenanceWindowExecutionTaskInvocationRequestRequestTypeDef]
    ) -> GetMaintenanceWindowExecutionTaskInvocationResultTypeDef:
        """
        Retrieves information about a specific task running on a specific target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_maintenance_window_execution_task_invocation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_maintenance_window_execution_task_invocation)
        """

    def get_maintenance_window_task(
        self, **kwargs: Unpack[GetMaintenanceWindowTaskRequestRequestTypeDef]
    ) -> GetMaintenanceWindowTaskResultTypeDef:
        """
        Retrieves the details of a maintenance window task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_maintenance_window_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_maintenance_window_task)
        """

    def get_ops_item(
        self, **kwargs: Unpack[GetOpsItemRequestRequestTypeDef]
    ) -> GetOpsItemResponseTypeDef:
        """
        Get information about an OpsItem by using the ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_ops_item.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_ops_item)
        """

    def get_ops_metadata(
        self, **kwargs: Unpack[GetOpsMetadataRequestRequestTypeDef]
    ) -> GetOpsMetadataResultTypeDef:
        """
        View operational metadata related to an application in Application Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_ops_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_ops_metadata)
        """

    def get_ops_summary(
        self, **kwargs: Unpack[GetOpsSummaryRequestRequestTypeDef]
    ) -> GetOpsSummaryResultTypeDef:
        """
        View a summary of operations metadata (OpsData) based on specified filters and
        aggregators.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_ops_summary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_ops_summary)
        """

    def get_parameter(
        self, **kwargs: Unpack[GetParameterRequestRequestTypeDef]
    ) -> GetParameterResultTypeDef:
        """
        Get information about a single parameter by specifying the parameter name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_parameter)
        """

    def get_parameter_history(
        self, **kwargs: Unpack[GetParameterHistoryRequestRequestTypeDef]
    ) -> GetParameterHistoryResultTypeDef:
        """
        Retrieves the history of all changes to a parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameter_history.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_parameter_history)
        """

    def get_parameters(
        self, **kwargs: Unpack[GetParametersRequestRequestTypeDef]
    ) -> GetParametersResultTypeDef:
        """
        Get information about one or more parameters by specifying multiple parameter
        names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_parameters)
        """

    def get_parameters_by_path(
        self, **kwargs: Unpack[GetParametersByPathRequestRequestTypeDef]
    ) -> GetParametersByPathResultTypeDef:
        """
        Retrieve information about one or more parameters in a specific hierarchy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameters_by_path.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_parameters_by_path)
        """

    def get_patch_baseline(
        self, **kwargs: Unpack[GetPatchBaselineRequestRequestTypeDef]
    ) -> GetPatchBaselineResultTypeDef:
        """
        Retrieves information about a patch baseline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_patch_baseline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_patch_baseline)
        """

    def get_patch_baseline_for_patch_group(
        self, **kwargs: Unpack[GetPatchBaselineForPatchGroupRequestRequestTypeDef]
    ) -> GetPatchBaselineForPatchGroupResultTypeDef:
        """
        Retrieves the patch baseline that should be used for the specified patch group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_patch_baseline_for_patch_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_patch_baseline_for_patch_group)
        """

    def get_resource_policies(
        self, **kwargs: Unpack[GetResourcePoliciesRequestRequestTypeDef]
    ) -> GetResourcePoliciesResponseTypeDef:
        """
        Returns an array of the <code>Policy</code> object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_resource_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_resource_policies)
        """

    def get_service_setting(
        self, **kwargs: Unpack[GetServiceSettingRequestRequestTypeDef]
    ) -> GetServiceSettingResultTypeDef:
        """
        <code>ServiceSetting</code> is an account-level setting for an Amazon Web
        Services service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_service_setting.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_service_setting)
        """

    def label_parameter_version(
        self, **kwargs: Unpack[LabelParameterVersionRequestRequestTypeDef]
    ) -> LabelParameterVersionResultTypeDef:
        """
        A parameter label is a user-defined alias to help you manage different versions
        of a parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/label_parameter_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#label_parameter_version)
        """

    def list_association_versions(
        self, **kwargs: Unpack[ListAssociationVersionsRequestRequestTypeDef]
    ) -> ListAssociationVersionsResultTypeDef:
        """
        Retrieves all versions of an association for a specific association ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_association_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_association_versions)
        """

    def list_associations(
        self, **kwargs: Unpack[ListAssociationsRequestRequestTypeDef]
    ) -> ListAssociationsResultTypeDef:
        """
        Returns all State Manager associations in the current Amazon Web Services
        account and Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_associations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_associations)
        """

    def list_command_invocations(
        self, **kwargs: Unpack[ListCommandInvocationsRequestRequestTypeDef]
    ) -> ListCommandInvocationsResultTypeDef:
        """
        An invocation is copy of a command sent to a specific managed node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_command_invocations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_command_invocations)
        """

    def list_commands(
        self, **kwargs: Unpack[ListCommandsRequestRequestTypeDef]
    ) -> ListCommandsResultTypeDef:
        """
        Lists the commands requested by users of the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_commands.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_commands)
        """

    def list_compliance_items(
        self, **kwargs: Unpack[ListComplianceItemsRequestRequestTypeDef]
    ) -> ListComplianceItemsResultTypeDef:
        """
        For a specified resource ID, this API operation returns a list of compliance
        statuses for different resource types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_compliance_items.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_compliance_items)
        """

    def list_compliance_summaries(
        self, **kwargs: Unpack[ListComplianceSummariesRequestRequestTypeDef]
    ) -> ListComplianceSummariesResultTypeDef:
        """
        Returns a summary count of compliant and non-compliant resources for a
        compliance type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_compliance_summaries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_compliance_summaries)
        """

    def list_document_metadata_history(
        self, **kwargs: Unpack[ListDocumentMetadataHistoryRequestRequestTypeDef]
    ) -> ListDocumentMetadataHistoryResponseTypeDef:
        """
        Information about approval reviews for a version of a change template in Change
        Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_document_metadata_history.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_document_metadata_history)
        """

    def list_document_versions(
        self, **kwargs: Unpack[ListDocumentVersionsRequestRequestTypeDef]
    ) -> ListDocumentVersionsResultTypeDef:
        """
        List all versions for a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_document_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_document_versions)
        """

    def list_documents(
        self, **kwargs: Unpack[ListDocumentsRequestRequestTypeDef]
    ) -> ListDocumentsResultTypeDef:
        """
        Returns all Systems Manager (SSM) documents in the current Amazon Web Services
        account and Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_documents.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_documents)
        """

    def list_inventory_entries(
        self, **kwargs: Unpack[ListInventoryEntriesRequestRequestTypeDef]
    ) -> ListInventoryEntriesResultTypeDef:
        """
        A list of inventory items returned by the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_inventory_entries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_inventory_entries)
        """

    def list_nodes(
        self, **kwargs: Unpack[ListNodesRequestRequestTypeDef]
    ) -> ListNodesResultTypeDef:
        """
        Takes in filters and returns a list of managed nodes matching the filter
        criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_nodes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_nodes)
        """

    def list_nodes_summary(
        self, **kwargs: Unpack[ListNodesSummaryRequestRequestTypeDef]
    ) -> ListNodesSummaryResultTypeDef:
        """
        Generates a summary of managed instance/node metadata based on the filters and
        aggregators you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_nodes_summary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_nodes_summary)
        """

    def list_ops_item_events(
        self, **kwargs: Unpack[ListOpsItemEventsRequestRequestTypeDef]
    ) -> ListOpsItemEventsResponseTypeDef:
        """
        Returns a list of all OpsItem events in the current Amazon Web Services Region
        and Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_ops_item_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_ops_item_events)
        """

    def list_ops_item_related_items(
        self, **kwargs: Unpack[ListOpsItemRelatedItemsRequestRequestTypeDef]
    ) -> ListOpsItemRelatedItemsResponseTypeDef:
        """
        Lists all related-item resources associated with a Systems Manager OpsCenter
        OpsItem.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_ops_item_related_items.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_ops_item_related_items)
        """

    def list_ops_metadata(
        self, **kwargs: Unpack[ListOpsMetadataRequestRequestTypeDef]
    ) -> ListOpsMetadataResultTypeDef:
        """
        Amazon Web Services Systems Manager calls this API operation when displaying
        all Application Manager OpsMetadata objects or blobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_ops_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_ops_metadata)
        """

    def list_resource_compliance_summaries(
        self, **kwargs: Unpack[ListResourceComplianceSummariesRequestRequestTypeDef]
    ) -> ListResourceComplianceSummariesResultTypeDef:
        """
        Returns a resource-level summary count.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_resource_compliance_summaries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_resource_compliance_summaries)
        """

    def list_resource_data_sync(
        self, **kwargs: Unpack[ListResourceDataSyncRequestRequestTypeDef]
    ) -> ListResourceDataSyncResultTypeDef:
        """
        Lists your resource data sync configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_resource_data_sync.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_resource_data_sync)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResultTypeDef:
        """
        Returns a list of the tags assigned to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#list_tags_for_resource)
        """

    def modify_document_permission(
        self, **kwargs: Unpack[ModifyDocumentPermissionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Shares a Amazon Web Services Systems Manager document (SSM document)publicly or
        privately.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/modify_document_permission.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#modify_document_permission)
        """

    def put_compliance_items(
        self, **kwargs: Unpack[PutComplianceItemsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Registers a compliance type and other compliance details on a designated
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/put_compliance_items.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#put_compliance_items)
        """

    def put_inventory(
        self, **kwargs: Unpack[PutInventoryRequestRequestTypeDef]
    ) -> PutInventoryResultTypeDef:
        """
        Bulk update custom inventory items on one or more managed nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/put_inventory.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#put_inventory)
        """

    def put_parameter(
        self, **kwargs: Unpack[PutParameterRequestRequestTypeDef]
    ) -> PutParameterResultTypeDef:
        """
        Add a parameter to the system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/put_parameter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#put_parameter)
        """

    def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestRequestTypeDef]
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Creates or updates a Systems Manager resource policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/put_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#put_resource_policy)
        """

    def register_default_patch_baseline(
        self, **kwargs: Unpack[RegisterDefaultPatchBaselineRequestRequestTypeDef]
    ) -> RegisterDefaultPatchBaselineResultTypeDef:
        """
        Defines the default patch baseline for the relevant operating system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/register_default_patch_baseline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#register_default_patch_baseline)
        """

    def register_patch_baseline_for_patch_group(
        self, **kwargs: Unpack[RegisterPatchBaselineForPatchGroupRequestRequestTypeDef]
    ) -> RegisterPatchBaselineForPatchGroupResultTypeDef:
        """
        Registers a patch baseline for a patch group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/register_patch_baseline_for_patch_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#register_patch_baseline_for_patch_group)
        """

    def register_target_with_maintenance_window(
        self, **kwargs: Unpack[RegisterTargetWithMaintenanceWindowRequestRequestTypeDef]
    ) -> RegisterTargetWithMaintenanceWindowResultTypeDef:
        """
        Registers a target with a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/register_target_with_maintenance_window.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#register_target_with_maintenance_window)
        """

    def register_task_with_maintenance_window(
        self, **kwargs: Unpack[RegisterTaskWithMaintenanceWindowRequestRequestTypeDef]
    ) -> RegisterTaskWithMaintenanceWindowResultTypeDef:
        """
        Adds a new task to a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/register_task_with_maintenance_window.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#register_task_with_maintenance_window)
        """

    def remove_tags_from_resource(
        self, **kwargs: Unpack[RemoveTagsFromResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tag keys from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/remove_tags_from_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#remove_tags_from_resource)
        """

    def reset_service_setting(
        self, **kwargs: Unpack[ResetServiceSettingRequestRequestTypeDef]
    ) -> ResetServiceSettingResultTypeDef:
        """
        <code>ServiceSetting</code> is an account-level setting for an Amazon Web
        Services service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/reset_service_setting.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#reset_service_setting)
        """

    def resume_session(
        self, **kwargs: Unpack[ResumeSessionRequestRequestTypeDef]
    ) -> ResumeSessionResponseTypeDef:
        """
        Reconnects a session to a managed node after it has been disconnected.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/resume_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#resume_session)
        """

    def send_automation_signal(
        self, **kwargs: Unpack[SendAutomationSignalRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sends a signal to an Automation execution to change the current behavior or
        status of the execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/send_automation_signal.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#send_automation_signal)
        """

    def send_command(
        self, **kwargs: Unpack[SendCommandRequestRequestTypeDef]
    ) -> SendCommandResultTypeDef:
        """
        Runs commands on one or more managed nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/send_command.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#send_command)
        """

    def start_associations_once(
        self, **kwargs: Unpack[StartAssociationsOnceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Runs an association immediately and only one time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/start_associations_once.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#start_associations_once)
        """

    def start_automation_execution(
        self, **kwargs: Unpack[StartAutomationExecutionRequestRequestTypeDef]
    ) -> StartAutomationExecutionResultTypeDef:
        """
        Initiates execution of an Automation runbook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/start_automation_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#start_automation_execution)
        """

    def start_change_request_execution(
        self, **kwargs: Unpack[StartChangeRequestExecutionRequestRequestTypeDef]
    ) -> StartChangeRequestExecutionResultTypeDef:
        """
        Creates a change request for Change Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/start_change_request_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#start_change_request_execution)
        """

    def start_execution_preview(
        self, **kwargs: Unpack[StartExecutionPreviewRequestRequestTypeDef]
    ) -> StartExecutionPreviewResponseTypeDef:
        """
        Initiates the process of creating a preview showing the effects that running a
        specified Automation runbook would have on the targeted resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/start_execution_preview.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#start_execution_preview)
        """

    def start_session(
        self, **kwargs: Unpack[StartSessionRequestRequestTypeDef]
    ) -> StartSessionResponseTypeDef:
        """
        Initiates a connection to a target (for example, a managed node) for a Session
        Manager session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/start_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#start_session)
        """

    def stop_automation_execution(
        self, **kwargs: Unpack[StopAutomationExecutionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stop an Automation that is currently running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/stop_automation_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#stop_automation_execution)
        """

    def terminate_session(
        self, **kwargs: Unpack[TerminateSessionRequestRequestTypeDef]
    ) -> TerminateSessionResponseTypeDef:
        """
        Permanently ends a session and closes the data connection between the Session
        Manager client and SSM Agent on the managed node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/terminate_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#terminate_session)
        """

    def unlabel_parameter_version(
        self, **kwargs: Unpack[UnlabelParameterVersionRequestRequestTypeDef]
    ) -> UnlabelParameterVersionResultTypeDef:
        """
        Remove a label or labels from a parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/unlabel_parameter_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#unlabel_parameter_version)
        """

    def update_association(
        self, **kwargs: Unpack[UpdateAssociationRequestRequestTypeDef]
    ) -> UpdateAssociationResultTypeDef:
        """
        Updates an association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/update_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#update_association)
        """

    def update_association_status(
        self, **kwargs: Unpack[UpdateAssociationStatusRequestRequestTypeDef]
    ) -> UpdateAssociationStatusResultTypeDef:
        """
        Updates the status of the Amazon Web Services Systems Manager document (SSM
        document) associated with the specified managed node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/update_association_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#update_association_status)
        """

    def update_document(
        self, **kwargs: Unpack[UpdateDocumentRequestRequestTypeDef]
    ) -> UpdateDocumentResultTypeDef:
        """
        Updates one or more values for an SSM document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/update_document.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#update_document)
        """

    def update_document_default_version(
        self, **kwargs: Unpack[UpdateDocumentDefaultVersionRequestRequestTypeDef]
    ) -> UpdateDocumentDefaultVersionResultTypeDef:
        """
        Set the default version of a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/update_document_default_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#update_document_default_version)
        """

    def update_document_metadata(
        self, **kwargs: Unpack[UpdateDocumentMetadataRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates information related to approval reviews for a specific version of a
        change template in Change Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/update_document_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#update_document_metadata)
        """

    def update_maintenance_window(
        self, **kwargs: Unpack[UpdateMaintenanceWindowRequestRequestTypeDef]
    ) -> UpdateMaintenanceWindowResultTypeDef:
        """
        Updates an existing maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/update_maintenance_window.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#update_maintenance_window)
        """

    def update_maintenance_window_target(
        self, **kwargs: Unpack[UpdateMaintenanceWindowTargetRequestRequestTypeDef]
    ) -> UpdateMaintenanceWindowTargetResultTypeDef:
        """
        Modifies the target of an existing maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/update_maintenance_window_target.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#update_maintenance_window_target)
        """

    def update_maintenance_window_task(
        self, **kwargs: Unpack[UpdateMaintenanceWindowTaskRequestRequestTypeDef]
    ) -> UpdateMaintenanceWindowTaskResultTypeDef:
        """
        Modifies a task assigned to a maintenance window.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/update_maintenance_window_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#update_maintenance_window_task)
        """

    def update_managed_instance_role(
        self, **kwargs: Unpack[UpdateManagedInstanceRoleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Changes the Identity and Access Management (IAM) role that is assigned to the
        on-premises server, edge device, or virtual machines (VM).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/update_managed_instance_role.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#update_managed_instance_role)
        """

    def update_ops_item(
        self, **kwargs: Unpack[UpdateOpsItemRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Edit or change an OpsItem.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/update_ops_item.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#update_ops_item)
        """

    def update_ops_metadata(
        self, **kwargs: Unpack[UpdateOpsMetadataRequestRequestTypeDef]
    ) -> UpdateOpsMetadataResultTypeDef:
        """
        Amazon Web Services Systems Manager calls this API operation when you edit
        OpsMetadata in Application Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/update_ops_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#update_ops_metadata)
        """

    def update_patch_baseline(
        self, **kwargs: Unpack[UpdatePatchBaselineRequestRequestTypeDef]
    ) -> UpdatePatchBaselineResultTypeDef:
        """
        Modifies an existing patch baseline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/update_patch_baseline.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#update_patch_baseline)
        """

    def update_resource_data_sync(
        self, **kwargs: Unpack[UpdateResourceDataSyncRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update a resource data sync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/update_resource_data_sync.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#update_resource_data_sync)
        """

    def update_service_setting(
        self, **kwargs: Unpack[UpdateServiceSettingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        <code>ServiceSetting</code> is an account-level setting for an Amazon Web
        Services service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/update_service_setting.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#update_service_setting)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_activations"]
    ) -> DescribeActivationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_association_execution_targets"]
    ) -> DescribeAssociationExecutionTargetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_association_executions"]
    ) -> DescribeAssociationExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_automation_executions"]
    ) -> DescribeAutomationExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_automation_step_executions"]
    ) -> DescribeAutomationStepExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_available_patches"]
    ) -> DescribeAvailablePatchesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_effective_instance_associations"]
    ) -> DescribeEffectiveInstanceAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_effective_patches_for_patch_baseline"]
    ) -> DescribeEffectivePatchesForPatchBaselinePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_associations_status"]
    ) -> DescribeInstanceAssociationsStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_information"]
    ) -> DescribeInstanceInformationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_patch_states_for_patch_group"]
    ) -> DescribeInstancePatchStatesForPatchGroupPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_patch_states"]
    ) -> DescribeInstancePatchStatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_patches"]
    ) -> DescribeInstancePatchesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_instance_properties"]
    ) -> DescribeInstancePropertiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_inventory_deletions"]
    ) -> DescribeInventoryDeletionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_maintenance_window_execution_task_invocations"]
    ) -> DescribeMaintenanceWindowExecutionTaskInvocationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_maintenance_window_execution_tasks"]
    ) -> DescribeMaintenanceWindowExecutionTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_maintenance_window_executions"]
    ) -> DescribeMaintenanceWindowExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_maintenance_window_schedule"]
    ) -> DescribeMaintenanceWindowSchedulePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_maintenance_window_targets"]
    ) -> DescribeMaintenanceWindowTargetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_maintenance_window_tasks"]
    ) -> DescribeMaintenanceWindowTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_maintenance_windows_for_target"]
    ) -> DescribeMaintenanceWindowsForTargetPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_maintenance_windows"]
    ) -> DescribeMaintenanceWindowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_ops_items"]
    ) -> DescribeOpsItemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_parameters"]
    ) -> DescribeParametersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_patch_baselines"]
    ) -> DescribePatchBaselinesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_patch_groups"]
    ) -> DescribePatchGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_patch_properties"]
    ) -> DescribePatchPropertiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_sessions"]
    ) -> DescribeSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_inventory"]) -> GetInventoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_inventory_schema"]
    ) -> GetInventorySchemaPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_ops_summary"]) -> GetOpsSummaryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_parameter_history"]
    ) -> GetParameterHistoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_parameters_by_path"]
    ) -> GetParametersByPathPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_policies"]
    ) -> GetResourcePoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_association_versions"]
    ) -> ListAssociationVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_associations"]
    ) -> ListAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_command_invocations"]
    ) -> ListCommandInvocationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_commands"]) -> ListCommandsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_compliance_items"]
    ) -> ListComplianceItemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_compliance_summaries"]
    ) -> ListComplianceSummariesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_document_versions"]
    ) -> ListDocumentVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_documents"]) -> ListDocumentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_nodes"]) -> ListNodesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_nodes_summary"]
    ) -> ListNodesSummaryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ops_item_events"]
    ) -> ListOpsItemEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ops_item_related_items"]
    ) -> ListOpsItemRelatedItemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ops_metadata"]
    ) -> ListOpsMetadataPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_compliance_summaries"]
    ) -> ListResourceComplianceSummariesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_data_sync"]
    ) -> ListResourceDataSyncPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_paginator)
        """

    def get_waiter(self, waiter_name: Literal["command_executed"]) -> CommandExecutedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm/client/#get_waiter)
        """
