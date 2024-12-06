"""
Type annotations for auditmanager service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_auditmanager.client import AuditManagerClient

    session = Session()
    client: AuditManagerClient = session.client("auditmanager")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    AssociateAssessmentReportEvidenceFolderRequestRequestTypeDef,
    BatchAssociateAssessmentReportEvidenceRequestRequestTypeDef,
    BatchAssociateAssessmentReportEvidenceResponseTypeDef,
    BatchCreateDelegationByAssessmentRequestRequestTypeDef,
    BatchCreateDelegationByAssessmentResponseTypeDef,
    BatchDeleteDelegationByAssessmentRequestRequestTypeDef,
    BatchDeleteDelegationByAssessmentResponseTypeDef,
    BatchDisassociateAssessmentReportEvidenceRequestRequestTypeDef,
    BatchDisassociateAssessmentReportEvidenceResponseTypeDef,
    BatchImportEvidenceToAssessmentControlRequestRequestTypeDef,
    BatchImportEvidenceToAssessmentControlResponseTypeDef,
    CreateAssessmentFrameworkRequestRequestTypeDef,
    CreateAssessmentFrameworkResponseTypeDef,
    CreateAssessmentReportRequestRequestTypeDef,
    CreateAssessmentReportResponseTypeDef,
    CreateAssessmentRequestRequestTypeDef,
    CreateAssessmentResponseTypeDef,
    CreateControlRequestRequestTypeDef,
    CreateControlResponseTypeDef,
    DeleteAssessmentFrameworkRequestRequestTypeDef,
    DeleteAssessmentFrameworkShareRequestRequestTypeDef,
    DeleteAssessmentReportRequestRequestTypeDef,
    DeleteAssessmentRequestRequestTypeDef,
    DeleteControlRequestRequestTypeDef,
    DeregisterAccountResponseTypeDef,
    DeregisterOrganizationAdminAccountRequestRequestTypeDef,
    DisassociateAssessmentReportEvidenceFolderRequestRequestTypeDef,
    GetAccountStatusResponseTypeDef,
    GetAssessmentFrameworkRequestRequestTypeDef,
    GetAssessmentFrameworkResponseTypeDef,
    GetAssessmentReportUrlRequestRequestTypeDef,
    GetAssessmentReportUrlResponseTypeDef,
    GetAssessmentRequestRequestTypeDef,
    GetAssessmentResponseTypeDef,
    GetChangeLogsRequestRequestTypeDef,
    GetChangeLogsResponseTypeDef,
    GetControlRequestRequestTypeDef,
    GetControlResponseTypeDef,
    GetDelegationsRequestRequestTypeDef,
    GetDelegationsResponseTypeDef,
    GetEvidenceByEvidenceFolderRequestRequestTypeDef,
    GetEvidenceByEvidenceFolderResponseTypeDef,
    GetEvidenceFileUploadUrlRequestRequestTypeDef,
    GetEvidenceFileUploadUrlResponseTypeDef,
    GetEvidenceFolderRequestRequestTypeDef,
    GetEvidenceFolderResponseTypeDef,
    GetEvidenceFoldersByAssessmentControlRequestRequestTypeDef,
    GetEvidenceFoldersByAssessmentControlResponseTypeDef,
    GetEvidenceFoldersByAssessmentRequestRequestTypeDef,
    GetEvidenceFoldersByAssessmentResponseTypeDef,
    GetEvidenceRequestRequestTypeDef,
    GetEvidenceResponseTypeDef,
    GetInsightsByAssessmentRequestRequestTypeDef,
    GetInsightsByAssessmentResponseTypeDef,
    GetInsightsResponseTypeDef,
    GetOrganizationAdminAccountResponseTypeDef,
    GetServicesInScopeResponseTypeDef,
    GetSettingsRequestRequestTypeDef,
    GetSettingsResponseTypeDef,
    ListAssessmentControlInsightsByControlDomainRequestRequestTypeDef,
    ListAssessmentControlInsightsByControlDomainResponseTypeDef,
    ListAssessmentFrameworkShareRequestsRequestRequestTypeDef,
    ListAssessmentFrameworkShareRequestsResponseTypeDef,
    ListAssessmentFrameworksRequestRequestTypeDef,
    ListAssessmentFrameworksResponseTypeDef,
    ListAssessmentReportsRequestRequestTypeDef,
    ListAssessmentReportsResponseTypeDef,
    ListAssessmentsRequestRequestTypeDef,
    ListAssessmentsResponseTypeDef,
    ListControlDomainInsightsByAssessmentRequestRequestTypeDef,
    ListControlDomainInsightsByAssessmentResponseTypeDef,
    ListControlDomainInsightsRequestRequestTypeDef,
    ListControlDomainInsightsResponseTypeDef,
    ListControlInsightsByControlDomainRequestRequestTypeDef,
    ListControlInsightsByControlDomainResponseTypeDef,
    ListControlsRequestRequestTypeDef,
    ListControlsResponseTypeDef,
    ListKeywordsForDataSourceRequestRequestTypeDef,
    ListKeywordsForDataSourceResponseTypeDef,
    ListNotificationsRequestRequestTypeDef,
    ListNotificationsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RegisterAccountRequestRequestTypeDef,
    RegisterAccountResponseTypeDef,
    RegisterOrganizationAdminAccountRequestRequestTypeDef,
    RegisterOrganizationAdminAccountResponseTypeDef,
    StartAssessmentFrameworkShareRequestRequestTypeDef,
    StartAssessmentFrameworkShareResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAssessmentControlRequestRequestTypeDef,
    UpdateAssessmentControlResponseTypeDef,
    UpdateAssessmentControlSetStatusRequestRequestTypeDef,
    UpdateAssessmentControlSetStatusResponseTypeDef,
    UpdateAssessmentFrameworkRequestRequestTypeDef,
    UpdateAssessmentFrameworkResponseTypeDef,
    UpdateAssessmentFrameworkShareRequestRequestTypeDef,
    UpdateAssessmentFrameworkShareResponseTypeDef,
    UpdateAssessmentRequestRequestTypeDef,
    UpdateAssessmentResponseTypeDef,
    UpdateAssessmentStatusRequestRequestTypeDef,
    UpdateAssessmentStatusResponseTypeDef,
    UpdateControlRequestRequestTypeDef,
    UpdateControlResponseTypeDef,
    UpdateSettingsRequestRequestTypeDef,
    UpdateSettingsResponseTypeDef,
    ValidateAssessmentReportIntegrityRequestRequestTypeDef,
    ValidateAssessmentReportIntegrityResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("AuditManagerClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class AuditManagerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AuditManagerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#close)
        """

    def associate_assessment_report_evidence_folder(
        self, **kwargs: Unpack[AssociateAssessmentReportEvidenceFolderRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates an evidence folder to an assessment report in an Audit Manager
        assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/associate_assessment_report_evidence_folder.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#associate_assessment_report_evidence_folder)
        """

    def batch_associate_assessment_report_evidence(
        self, **kwargs: Unpack[BatchAssociateAssessmentReportEvidenceRequestRequestTypeDef]
    ) -> BatchAssociateAssessmentReportEvidenceResponseTypeDef:
        """
        Associates a list of evidence to an assessment report in an Audit Manager
        assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/batch_associate_assessment_report_evidence.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#batch_associate_assessment_report_evidence)
        """

    def batch_create_delegation_by_assessment(
        self, **kwargs: Unpack[BatchCreateDelegationByAssessmentRequestRequestTypeDef]
    ) -> BatchCreateDelegationByAssessmentResponseTypeDef:
        """
        Creates a batch of delegations for an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/batch_create_delegation_by_assessment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#batch_create_delegation_by_assessment)
        """

    def batch_delete_delegation_by_assessment(
        self, **kwargs: Unpack[BatchDeleteDelegationByAssessmentRequestRequestTypeDef]
    ) -> BatchDeleteDelegationByAssessmentResponseTypeDef:
        """
        Deletes a batch of delegations for an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/batch_delete_delegation_by_assessment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#batch_delete_delegation_by_assessment)
        """

    def batch_disassociate_assessment_report_evidence(
        self, **kwargs: Unpack[BatchDisassociateAssessmentReportEvidenceRequestRequestTypeDef]
    ) -> BatchDisassociateAssessmentReportEvidenceResponseTypeDef:
        """
        Disassociates a list of evidence from an assessment report in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/batch_disassociate_assessment_report_evidence.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#batch_disassociate_assessment_report_evidence)
        """

    def batch_import_evidence_to_assessment_control(
        self, **kwargs: Unpack[BatchImportEvidenceToAssessmentControlRequestRequestTypeDef]
    ) -> BatchImportEvidenceToAssessmentControlResponseTypeDef:
        """
        Adds one or more pieces of evidence to a control in an Audit Manager assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/batch_import_evidence_to_assessment_control.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#batch_import_evidence_to_assessment_control)
        """

    def create_assessment(
        self, **kwargs: Unpack[CreateAssessmentRequestRequestTypeDef]
    ) -> CreateAssessmentResponseTypeDef:
        """
        Creates an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/create_assessment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#create_assessment)
        """

    def create_assessment_framework(
        self, **kwargs: Unpack[CreateAssessmentFrameworkRequestRequestTypeDef]
    ) -> CreateAssessmentFrameworkResponseTypeDef:
        """
        Creates a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/create_assessment_framework.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#create_assessment_framework)
        """

    def create_assessment_report(
        self, **kwargs: Unpack[CreateAssessmentReportRequestRequestTypeDef]
    ) -> CreateAssessmentReportResponseTypeDef:
        """
        Creates an assessment report for the specified assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/create_assessment_report.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#create_assessment_report)
        """

    def create_control(
        self, **kwargs: Unpack[CreateControlRequestRequestTypeDef]
    ) -> CreateControlResponseTypeDef:
        """
        Creates a new custom control in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/create_control.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#create_control)
        """

    def delete_assessment(
        self, **kwargs: Unpack[DeleteAssessmentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/delete_assessment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#delete_assessment)
        """

    def delete_assessment_framework(
        self, **kwargs: Unpack[DeleteAssessmentFrameworkRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/delete_assessment_framework.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#delete_assessment_framework)
        """

    def delete_assessment_framework_share(
        self, **kwargs: Unpack[DeleteAssessmentFrameworkShareRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a share request for a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/delete_assessment_framework_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#delete_assessment_framework_share)
        """

    def delete_assessment_report(
        self, **kwargs: Unpack[DeleteAssessmentReportRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an assessment report in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/delete_assessment_report.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#delete_assessment_report)
        """

    def delete_control(
        self, **kwargs: Unpack[DeleteControlRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a custom control in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/delete_control.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#delete_control)
        """

    def deregister_account(self) -> DeregisterAccountResponseTypeDef:
        """
        Deregisters an account in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/deregister_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#deregister_account)
        """

    def deregister_organization_admin_account(
        self, **kwargs: Unpack[DeregisterOrganizationAdminAccountRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified Amazon Web Services account as a delegated administrator
        for Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/deregister_organization_admin_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#deregister_organization_admin_account)
        """

    def disassociate_assessment_report_evidence_folder(
        self, **kwargs: Unpack[DisassociateAssessmentReportEvidenceFolderRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates an evidence folder from the specified assessment report in Audit
        Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/disassociate_assessment_report_evidence_folder.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#disassociate_assessment_report_evidence_folder)
        """

    def get_account_status(self) -> GetAccountStatusResponseTypeDef:
        """
        Gets the registration status of an account in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_account_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_account_status)
        """

    def get_assessment(
        self, **kwargs: Unpack[GetAssessmentRequestRequestTypeDef]
    ) -> GetAssessmentResponseTypeDef:
        """
        Gets information about a specified assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_assessment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_assessment)
        """

    def get_assessment_framework(
        self, **kwargs: Unpack[GetAssessmentFrameworkRequestRequestTypeDef]
    ) -> GetAssessmentFrameworkResponseTypeDef:
        """
        Gets information about a specified framework.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_assessment_framework.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_assessment_framework)
        """

    def get_assessment_report_url(
        self, **kwargs: Unpack[GetAssessmentReportUrlRequestRequestTypeDef]
    ) -> GetAssessmentReportUrlResponseTypeDef:
        """
        Gets the URL of an assessment report in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_assessment_report_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_assessment_report_url)
        """

    def get_change_logs(
        self, **kwargs: Unpack[GetChangeLogsRequestRequestTypeDef]
    ) -> GetChangeLogsResponseTypeDef:
        """
        Gets a list of changelogs from Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_change_logs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_change_logs)
        """

    def get_control(
        self, **kwargs: Unpack[GetControlRequestRequestTypeDef]
    ) -> GetControlResponseTypeDef:
        """
        Gets information about a specified control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_control.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_control)
        """

    def get_delegations(
        self, **kwargs: Unpack[GetDelegationsRequestRequestTypeDef]
    ) -> GetDelegationsResponseTypeDef:
        """
        Gets a list of delegations from an audit owner to a delegate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_delegations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_delegations)
        """

    def get_evidence(
        self, **kwargs: Unpack[GetEvidenceRequestRequestTypeDef]
    ) -> GetEvidenceResponseTypeDef:
        """
        Gets information about a specified evidence item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_evidence.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_evidence)
        """

    def get_evidence_by_evidence_folder(
        self, **kwargs: Unpack[GetEvidenceByEvidenceFolderRequestRequestTypeDef]
    ) -> GetEvidenceByEvidenceFolderResponseTypeDef:
        """
        Gets all evidence from a specified evidence folder in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_evidence_by_evidence_folder.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_evidence_by_evidence_folder)
        """

    def get_evidence_file_upload_url(
        self, **kwargs: Unpack[GetEvidenceFileUploadUrlRequestRequestTypeDef]
    ) -> GetEvidenceFileUploadUrlResponseTypeDef:
        """
        Creates a presigned Amazon S3 URL that can be used to upload a file as manual
        evidence.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_evidence_file_upload_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_evidence_file_upload_url)
        """

    def get_evidence_folder(
        self, **kwargs: Unpack[GetEvidenceFolderRequestRequestTypeDef]
    ) -> GetEvidenceFolderResponseTypeDef:
        """
        Gets an evidence folder from a specified assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_evidence_folder.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_evidence_folder)
        """

    def get_evidence_folders_by_assessment(
        self, **kwargs: Unpack[GetEvidenceFoldersByAssessmentRequestRequestTypeDef]
    ) -> GetEvidenceFoldersByAssessmentResponseTypeDef:
        """
        Gets the evidence folders from a specified assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_evidence_folders_by_assessment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_evidence_folders_by_assessment)
        """

    def get_evidence_folders_by_assessment_control(
        self, **kwargs: Unpack[GetEvidenceFoldersByAssessmentControlRequestRequestTypeDef]
    ) -> GetEvidenceFoldersByAssessmentControlResponseTypeDef:
        """
        Gets a list of evidence folders that are associated with a specified control in
        an Audit Manager assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_evidence_folders_by_assessment_control.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_evidence_folders_by_assessment_control)
        """

    def get_insights(self) -> GetInsightsResponseTypeDef:
        """
        Gets the latest analytics data for all your current active assessments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_insights.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_insights)
        """

    def get_insights_by_assessment(
        self, **kwargs: Unpack[GetInsightsByAssessmentRequestRequestTypeDef]
    ) -> GetInsightsByAssessmentResponseTypeDef:
        """
        Gets the latest analytics data for a specific active assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_insights_by_assessment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_insights_by_assessment)
        """

    def get_organization_admin_account(self) -> GetOrganizationAdminAccountResponseTypeDef:
        """
        Gets the name of the delegated Amazon Web Services administrator account for a
        specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_organization_admin_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_organization_admin_account)
        """

    def get_services_in_scope(self) -> GetServicesInScopeResponseTypeDef:
        """
        Gets a list of the Amazon Web Services from which Audit Manager can collect
        evidence.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_services_in_scope.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_services_in_scope)
        """

    def get_settings(
        self, **kwargs: Unpack[GetSettingsRequestRequestTypeDef]
    ) -> GetSettingsResponseTypeDef:
        """
        Gets the settings for a specified Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#get_settings)
        """

    def list_assessment_control_insights_by_control_domain(
        self, **kwargs: Unpack[ListAssessmentControlInsightsByControlDomainRequestRequestTypeDef]
    ) -> ListAssessmentControlInsightsByControlDomainResponseTypeDef:
        """
        Lists the latest analytics data for controls within a specific control domain
        and a specific active assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_assessment_control_insights_by_control_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#list_assessment_control_insights_by_control_domain)
        """

    def list_assessment_framework_share_requests(
        self, **kwargs: Unpack[ListAssessmentFrameworkShareRequestsRequestRequestTypeDef]
    ) -> ListAssessmentFrameworkShareRequestsResponseTypeDef:
        """
        Returns a list of sent or received share requests for custom frameworks in
        Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_assessment_framework_share_requests.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#list_assessment_framework_share_requests)
        """

    def list_assessment_frameworks(
        self, **kwargs: Unpack[ListAssessmentFrameworksRequestRequestTypeDef]
    ) -> ListAssessmentFrameworksResponseTypeDef:
        """
        Returns a list of the frameworks that are available in the Audit Manager
        framework library.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_assessment_frameworks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#list_assessment_frameworks)
        """

    def list_assessment_reports(
        self, **kwargs: Unpack[ListAssessmentReportsRequestRequestTypeDef]
    ) -> ListAssessmentReportsResponseTypeDef:
        """
        Returns a list of assessment reports created in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_assessment_reports.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#list_assessment_reports)
        """

    def list_assessments(
        self, **kwargs: Unpack[ListAssessmentsRequestRequestTypeDef]
    ) -> ListAssessmentsResponseTypeDef:
        """
        Returns a list of current and past assessments from Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_assessments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#list_assessments)
        """

    def list_control_domain_insights(
        self, **kwargs: Unpack[ListControlDomainInsightsRequestRequestTypeDef]
    ) -> ListControlDomainInsightsResponseTypeDef:
        """
        Lists the latest analytics data for control domains across all of your active
        assessments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_control_domain_insights.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#list_control_domain_insights)
        """

    def list_control_domain_insights_by_assessment(
        self, **kwargs: Unpack[ListControlDomainInsightsByAssessmentRequestRequestTypeDef]
    ) -> ListControlDomainInsightsByAssessmentResponseTypeDef:
        """
        Lists analytics data for control domains within a specified active assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_control_domain_insights_by_assessment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#list_control_domain_insights_by_assessment)
        """

    def list_control_insights_by_control_domain(
        self, **kwargs: Unpack[ListControlInsightsByControlDomainRequestRequestTypeDef]
    ) -> ListControlInsightsByControlDomainResponseTypeDef:
        """
        Lists the latest analytics data for controls within a specific control domain
        across all active assessments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_control_insights_by_control_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#list_control_insights_by_control_domain)
        """

    def list_controls(
        self, **kwargs: Unpack[ListControlsRequestRequestTypeDef]
    ) -> ListControlsResponseTypeDef:
        """
        Returns a list of controls from Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_controls.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#list_controls)
        """

    def list_keywords_for_data_source(
        self, **kwargs: Unpack[ListKeywordsForDataSourceRequestRequestTypeDef]
    ) -> ListKeywordsForDataSourceResponseTypeDef:
        """
        Returns a list of keywords that are pre-mapped to the specified control data
        source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_keywords_for_data_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#list_keywords_for_data_source)
        """

    def list_notifications(
        self, **kwargs: Unpack[ListNotificationsRequestRequestTypeDef]
    ) -> ListNotificationsResponseTypeDef:
        """
        Returns a list of all Audit Manager notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_notifications.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#list_notifications)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for the specified resource in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#list_tags_for_resource)
        """

    def register_account(
        self, **kwargs: Unpack[RegisterAccountRequestRequestTypeDef]
    ) -> RegisterAccountResponseTypeDef:
        """
        Enables Audit Manager for the specified Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/register_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#register_account)
        """

    def register_organization_admin_account(
        self, **kwargs: Unpack[RegisterOrganizationAdminAccountRequestRequestTypeDef]
    ) -> RegisterOrganizationAdminAccountResponseTypeDef:
        """
        Enables an Amazon Web Services account within the organization as the delegated
        administrator for Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/register_organization_admin_account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#register_organization_admin_account)
        """

    def start_assessment_framework_share(
        self, **kwargs: Unpack[StartAssessmentFrameworkShareRequestRequestTypeDef]
    ) -> StartAssessmentFrameworkShareResponseTypeDef:
        """
        Creates a share request for a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/start_assessment_framework_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#start_assessment_framework_share)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags the specified resource in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag from a resource in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#untag_resource)
        """

    def update_assessment(
        self, **kwargs: Unpack[UpdateAssessmentRequestRequestTypeDef]
    ) -> UpdateAssessmentResponseTypeDef:
        """
        Edits an Audit Manager assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/update_assessment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#update_assessment)
        """

    def update_assessment_control(
        self, **kwargs: Unpack[UpdateAssessmentControlRequestRequestTypeDef]
    ) -> UpdateAssessmentControlResponseTypeDef:
        """
        Updates a control within an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/update_assessment_control.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#update_assessment_control)
        """

    def update_assessment_control_set_status(
        self, **kwargs: Unpack[UpdateAssessmentControlSetStatusRequestRequestTypeDef]
    ) -> UpdateAssessmentControlSetStatusResponseTypeDef:
        """
        Updates the status of a control set in an Audit Manager assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/update_assessment_control_set_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#update_assessment_control_set_status)
        """

    def update_assessment_framework(
        self, **kwargs: Unpack[UpdateAssessmentFrameworkRequestRequestTypeDef]
    ) -> UpdateAssessmentFrameworkResponseTypeDef:
        """
        Updates a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/update_assessment_framework.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#update_assessment_framework)
        """

    def update_assessment_framework_share(
        self, **kwargs: Unpack[UpdateAssessmentFrameworkShareRequestRequestTypeDef]
    ) -> UpdateAssessmentFrameworkShareResponseTypeDef:
        """
        Updates a share request for a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/update_assessment_framework_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#update_assessment_framework_share)
        """

    def update_assessment_status(
        self, **kwargs: Unpack[UpdateAssessmentStatusRequestRequestTypeDef]
    ) -> UpdateAssessmentStatusResponseTypeDef:
        """
        Updates the status of an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/update_assessment_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#update_assessment_status)
        """

    def update_control(
        self, **kwargs: Unpack[UpdateControlRequestRequestTypeDef]
    ) -> UpdateControlResponseTypeDef:
        """
        Updates a custom control in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/update_control.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#update_control)
        """

    def update_settings(
        self, **kwargs: Unpack[UpdateSettingsRequestRequestTypeDef]
    ) -> UpdateSettingsResponseTypeDef:
        """
        Updates Audit Manager settings for the current account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/update_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#update_settings)
        """

    def validate_assessment_report_integrity(
        self, **kwargs: Unpack[ValidateAssessmentReportIntegrityRequestRequestTypeDef]
    ) -> ValidateAssessmentReportIntegrityResponseTypeDef:
        """
        Validates the integrity of an assessment report in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/validate_assessment_report_integrity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_auditmanager/client/#validate_assessment_report_integrity)
        """
