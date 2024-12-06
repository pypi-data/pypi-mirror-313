"""
Type annotations for redshift-serverless service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_redshift_serverless.client import RedshiftServerlessClient

    session = Session()
    client: RedshiftServerlessClient = session.client("redshift-serverless")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListCustomDomainAssociationsPaginator,
    ListEndpointAccessPaginator,
    ListManagedWorkgroupsPaginator,
    ListNamespacesPaginator,
    ListRecoveryPointsPaginator,
    ListScheduledActionsPaginator,
    ListSnapshotCopyConfigurationsPaginator,
    ListSnapshotsPaginator,
    ListTableRestoreStatusPaginator,
    ListUsageLimitsPaginator,
    ListWorkgroupsPaginator,
)
from .type_defs import (
    ConvertRecoveryPointToSnapshotRequestRequestTypeDef,
    ConvertRecoveryPointToSnapshotResponseTypeDef,
    CreateCustomDomainAssociationRequestRequestTypeDef,
    CreateCustomDomainAssociationResponseTypeDef,
    CreateEndpointAccessRequestRequestTypeDef,
    CreateEndpointAccessResponseTypeDef,
    CreateNamespaceRequestRequestTypeDef,
    CreateNamespaceResponseTypeDef,
    CreateScheduledActionRequestRequestTypeDef,
    CreateScheduledActionResponseTypeDef,
    CreateSnapshotCopyConfigurationRequestRequestTypeDef,
    CreateSnapshotCopyConfigurationResponseTypeDef,
    CreateSnapshotRequestRequestTypeDef,
    CreateSnapshotResponseTypeDef,
    CreateUsageLimitRequestRequestTypeDef,
    CreateUsageLimitResponseTypeDef,
    CreateWorkgroupRequestRequestTypeDef,
    CreateWorkgroupResponseTypeDef,
    DeleteCustomDomainAssociationRequestRequestTypeDef,
    DeleteEndpointAccessRequestRequestTypeDef,
    DeleteEndpointAccessResponseTypeDef,
    DeleteNamespaceRequestRequestTypeDef,
    DeleteNamespaceResponseTypeDef,
    DeleteResourcePolicyRequestRequestTypeDef,
    DeleteScheduledActionRequestRequestTypeDef,
    DeleteScheduledActionResponseTypeDef,
    DeleteSnapshotCopyConfigurationRequestRequestTypeDef,
    DeleteSnapshotCopyConfigurationResponseTypeDef,
    DeleteSnapshotRequestRequestTypeDef,
    DeleteSnapshotResponseTypeDef,
    DeleteUsageLimitRequestRequestTypeDef,
    DeleteUsageLimitResponseTypeDef,
    DeleteWorkgroupRequestRequestTypeDef,
    DeleteWorkgroupResponseTypeDef,
    GetCredentialsRequestRequestTypeDef,
    GetCredentialsResponseTypeDef,
    GetCustomDomainAssociationRequestRequestTypeDef,
    GetCustomDomainAssociationResponseTypeDef,
    GetEndpointAccessRequestRequestTypeDef,
    GetEndpointAccessResponseTypeDef,
    GetNamespaceRequestRequestTypeDef,
    GetNamespaceResponseTypeDef,
    GetRecoveryPointRequestRequestTypeDef,
    GetRecoveryPointResponseTypeDef,
    GetResourcePolicyRequestRequestTypeDef,
    GetResourcePolicyResponseTypeDef,
    GetScheduledActionRequestRequestTypeDef,
    GetScheduledActionResponseTypeDef,
    GetSnapshotRequestRequestTypeDef,
    GetSnapshotResponseTypeDef,
    GetTableRestoreStatusRequestRequestTypeDef,
    GetTableRestoreStatusResponseTypeDef,
    GetUsageLimitRequestRequestTypeDef,
    GetUsageLimitResponseTypeDef,
    GetWorkgroupRequestRequestTypeDef,
    GetWorkgroupResponseTypeDef,
    ListCustomDomainAssociationsRequestRequestTypeDef,
    ListCustomDomainAssociationsResponseTypeDef,
    ListEndpointAccessRequestRequestTypeDef,
    ListEndpointAccessResponseTypeDef,
    ListManagedWorkgroupsRequestRequestTypeDef,
    ListManagedWorkgroupsResponseTypeDef,
    ListNamespacesRequestRequestTypeDef,
    ListNamespacesResponseTypeDef,
    ListRecoveryPointsRequestRequestTypeDef,
    ListRecoveryPointsResponseTypeDef,
    ListScheduledActionsRequestRequestTypeDef,
    ListScheduledActionsResponseTypeDef,
    ListSnapshotCopyConfigurationsRequestRequestTypeDef,
    ListSnapshotCopyConfigurationsResponseTypeDef,
    ListSnapshotsRequestRequestTypeDef,
    ListSnapshotsResponseTypeDef,
    ListTableRestoreStatusRequestRequestTypeDef,
    ListTableRestoreStatusResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUsageLimitsRequestRequestTypeDef,
    ListUsageLimitsResponseTypeDef,
    ListWorkgroupsRequestRequestTypeDef,
    ListWorkgroupsResponseTypeDef,
    PutResourcePolicyRequestRequestTypeDef,
    PutResourcePolicyResponseTypeDef,
    RestoreFromRecoveryPointRequestRequestTypeDef,
    RestoreFromRecoveryPointResponseTypeDef,
    RestoreFromSnapshotRequestRequestTypeDef,
    RestoreFromSnapshotResponseTypeDef,
    RestoreTableFromRecoveryPointRequestRequestTypeDef,
    RestoreTableFromRecoveryPointResponseTypeDef,
    RestoreTableFromSnapshotRequestRequestTypeDef,
    RestoreTableFromSnapshotResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateCustomDomainAssociationRequestRequestTypeDef,
    UpdateCustomDomainAssociationResponseTypeDef,
    UpdateEndpointAccessRequestRequestTypeDef,
    UpdateEndpointAccessResponseTypeDef,
    UpdateNamespaceRequestRequestTypeDef,
    UpdateNamespaceResponseTypeDef,
    UpdateScheduledActionRequestRequestTypeDef,
    UpdateScheduledActionResponseTypeDef,
    UpdateSnapshotCopyConfigurationRequestRequestTypeDef,
    UpdateSnapshotCopyConfigurationResponseTypeDef,
    UpdateSnapshotRequestRequestTypeDef,
    UpdateSnapshotResponseTypeDef,
    UpdateUsageLimitRequestRequestTypeDef,
    UpdateUsageLimitResponseTypeDef,
    UpdateWorkgroupRequestRequestTypeDef,
    UpdateWorkgroupResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("RedshiftServerlessClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InsufficientCapacityException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidPaginationException: Type[BotocoreClientError]
    Ipv6CidrBlockNotFoundException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class RedshiftServerlessClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RedshiftServerlessClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless.html#RedshiftServerless.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#close)
        """

    def convert_recovery_point_to_snapshot(
        self, **kwargs: Unpack[ConvertRecoveryPointToSnapshotRequestRequestTypeDef]
    ) -> ConvertRecoveryPointToSnapshotResponseTypeDef:
        """
        Converts a recovery point to a snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/convert_recovery_point_to_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#convert_recovery_point_to_snapshot)
        """

    def create_custom_domain_association(
        self, **kwargs: Unpack[CreateCustomDomainAssociationRequestRequestTypeDef]
    ) -> CreateCustomDomainAssociationResponseTypeDef:
        """
        Creates a custom domain association for Amazon Redshift Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/create_custom_domain_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#create_custom_domain_association)
        """

    def create_endpoint_access(
        self, **kwargs: Unpack[CreateEndpointAccessRequestRequestTypeDef]
    ) -> CreateEndpointAccessResponseTypeDef:
        """
        Creates an Amazon Redshift Serverless managed VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/create_endpoint_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#create_endpoint_access)
        """

    def create_namespace(
        self, **kwargs: Unpack[CreateNamespaceRequestRequestTypeDef]
    ) -> CreateNamespaceResponseTypeDef:
        """
        Creates a namespace in Amazon Redshift Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/create_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#create_namespace)
        """

    def create_scheduled_action(
        self, **kwargs: Unpack[CreateScheduledActionRequestRequestTypeDef]
    ) -> CreateScheduledActionResponseTypeDef:
        """
        Creates a scheduled action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/create_scheduled_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#create_scheduled_action)
        """

    def create_snapshot(
        self, **kwargs: Unpack[CreateSnapshotRequestRequestTypeDef]
    ) -> CreateSnapshotResponseTypeDef:
        """
        Creates a snapshot of all databases in a namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/create_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#create_snapshot)
        """

    def create_snapshot_copy_configuration(
        self, **kwargs: Unpack[CreateSnapshotCopyConfigurationRequestRequestTypeDef]
    ) -> CreateSnapshotCopyConfigurationResponseTypeDef:
        """
        Creates a snapshot copy configuration that lets you copy snapshots to another
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/create_snapshot_copy_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#create_snapshot_copy_configuration)
        """

    def create_usage_limit(
        self, **kwargs: Unpack[CreateUsageLimitRequestRequestTypeDef]
    ) -> CreateUsageLimitResponseTypeDef:
        """
        Creates a usage limit for a specified Amazon Redshift Serverless usage type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/create_usage_limit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#create_usage_limit)
        """

    def create_workgroup(
        self, **kwargs: Unpack[CreateWorkgroupRequestRequestTypeDef]
    ) -> CreateWorkgroupResponseTypeDef:
        """
        Creates an workgroup in Amazon Redshift Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/create_workgroup.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#create_workgroup)
        """

    def delete_custom_domain_association(
        self, **kwargs: Unpack[DeleteCustomDomainAssociationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a custom domain association for Amazon Redshift Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/delete_custom_domain_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#delete_custom_domain_association)
        """

    def delete_endpoint_access(
        self, **kwargs: Unpack[DeleteEndpointAccessRequestRequestTypeDef]
    ) -> DeleteEndpointAccessResponseTypeDef:
        """
        Deletes an Amazon Redshift Serverless managed VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/delete_endpoint_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#delete_endpoint_access)
        """

    def delete_namespace(
        self, **kwargs: Unpack[DeleteNamespaceRequestRequestTypeDef]
    ) -> DeleteNamespaceResponseTypeDef:
        """
        Deletes a namespace from Amazon Redshift Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/delete_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#delete_namespace)
        """

    def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified resource policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/delete_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#delete_resource_policy)
        """

    def delete_scheduled_action(
        self, **kwargs: Unpack[DeleteScheduledActionRequestRequestTypeDef]
    ) -> DeleteScheduledActionResponseTypeDef:
        """
        Deletes a scheduled action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/delete_scheduled_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#delete_scheduled_action)
        """

    def delete_snapshot(
        self, **kwargs: Unpack[DeleteSnapshotRequestRequestTypeDef]
    ) -> DeleteSnapshotResponseTypeDef:
        """
        Deletes a snapshot from Amazon Redshift Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/delete_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#delete_snapshot)
        """

    def delete_snapshot_copy_configuration(
        self, **kwargs: Unpack[DeleteSnapshotCopyConfigurationRequestRequestTypeDef]
    ) -> DeleteSnapshotCopyConfigurationResponseTypeDef:
        """
        Deletes a snapshot copy configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/delete_snapshot_copy_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#delete_snapshot_copy_configuration)
        """

    def delete_usage_limit(
        self, **kwargs: Unpack[DeleteUsageLimitRequestRequestTypeDef]
    ) -> DeleteUsageLimitResponseTypeDef:
        """
        Deletes a usage limit from Amazon Redshift Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/delete_usage_limit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#delete_usage_limit)
        """

    def delete_workgroup(
        self, **kwargs: Unpack[DeleteWorkgroupRequestRequestTypeDef]
    ) -> DeleteWorkgroupResponseTypeDef:
        """
        Deletes a workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/delete_workgroup.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#delete_workgroup)
        """

    def get_credentials(
        self, **kwargs: Unpack[GetCredentialsRequestRequestTypeDef]
    ) -> GetCredentialsResponseTypeDef:
        """
        Returns a database user name and temporary password with temporary
        authorization to log in to Amazon Redshift Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_credentials.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_credentials)
        """

    def get_custom_domain_association(
        self, **kwargs: Unpack[GetCustomDomainAssociationRequestRequestTypeDef]
    ) -> GetCustomDomainAssociationResponseTypeDef:
        """
        Gets information about a specific custom domain association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_custom_domain_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_custom_domain_association)
        """

    def get_endpoint_access(
        self, **kwargs: Unpack[GetEndpointAccessRequestRequestTypeDef]
    ) -> GetEndpointAccessResponseTypeDef:
        """
        Returns information, such as the name, about a VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_endpoint_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_endpoint_access)
        """

    def get_namespace(
        self, **kwargs: Unpack[GetNamespaceRequestRequestTypeDef]
    ) -> GetNamespaceResponseTypeDef:
        """
        Returns information about a namespace in Amazon Redshift Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_namespace)
        """

    def get_recovery_point(
        self, **kwargs: Unpack[GetRecoveryPointRequestRequestTypeDef]
    ) -> GetRecoveryPointResponseTypeDef:
        """
        Returns information about a recovery point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_recovery_point.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_recovery_point)
        """

    def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyRequestRequestTypeDef]
    ) -> GetResourcePolicyResponseTypeDef:
        """
        Returns a resource policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_resource_policy)
        """

    def get_scheduled_action(
        self, **kwargs: Unpack[GetScheduledActionRequestRequestTypeDef]
    ) -> GetScheduledActionResponseTypeDef:
        """
        Returns information about a scheduled action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_scheduled_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_scheduled_action)
        """

    def get_snapshot(
        self, **kwargs: Unpack[GetSnapshotRequestRequestTypeDef]
    ) -> GetSnapshotResponseTypeDef:
        """
        Returns information about a specific snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_snapshot)
        """

    def get_table_restore_status(
        self, **kwargs: Unpack[GetTableRestoreStatusRequestRequestTypeDef]
    ) -> GetTableRestoreStatusResponseTypeDef:
        """
        Returns information about a <code>TableRestoreStatus</code> object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_table_restore_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_table_restore_status)
        """

    def get_usage_limit(
        self, **kwargs: Unpack[GetUsageLimitRequestRequestTypeDef]
    ) -> GetUsageLimitResponseTypeDef:
        """
        Returns information about a usage limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_usage_limit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_usage_limit)
        """

    def get_workgroup(
        self, **kwargs: Unpack[GetWorkgroupRequestRequestTypeDef]
    ) -> GetWorkgroupResponseTypeDef:
        """
        Returns information about a specific workgroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_workgroup.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_workgroup)
        """

    def list_custom_domain_associations(
        self, **kwargs: Unpack[ListCustomDomainAssociationsRequestRequestTypeDef]
    ) -> ListCustomDomainAssociationsResponseTypeDef:
        """
        Lists custom domain associations for Amazon Redshift Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/list_custom_domain_associations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#list_custom_domain_associations)
        """

    def list_endpoint_access(
        self, **kwargs: Unpack[ListEndpointAccessRequestRequestTypeDef]
    ) -> ListEndpointAccessResponseTypeDef:
        """
        Returns an array of <code>EndpointAccess</code> objects and relevant
        information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/list_endpoint_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#list_endpoint_access)
        """

    def list_managed_workgroups(
        self, **kwargs: Unpack[ListManagedWorkgroupsRequestRequestTypeDef]
    ) -> ListManagedWorkgroupsResponseTypeDef:
        """
        Returns information about a list of specified managed workgroups in your
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/list_managed_workgroups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#list_managed_workgroups)
        """

    def list_namespaces(
        self, **kwargs: Unpack[ListNamespacesRequestRequestTypeDef]
    ) -> ListNamespacesResponseTypeDef:
        """
        Returns information about a list of specified namespaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/list_namespaces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#list_namespaces)
        """

    def list_recovery_points(
        self, **kwargs: Unpack[ListRecoveryPointsRequestRequestTypeDef]
    ) -> ListRecoveryPointsResponseTypeDef:
        """
        Returns an array of recovery points.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/list_recovery_points.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#list_recovery_points)
        """

    def list_scheduled_actions(
        self, **kwargs: Unpack[ListScheduledActionsRequestRequestTypeDef]
    ) -> ListScheduledActionsResponseTypeDef:
        """
        Returns a list of scheduled actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/list_scheduled_actions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#list_scheduled_actions)
        """

    def list_snapshot_copy_configurations(
        self, **kwargs: Unpack[ListSnapshotCopyConfigurationsRequestRequestTypeDef]
    ) -> ListSnapshotCopyConfigurationsResponseTypeDef:
        """
        Returns a list of snapshot copy configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/list_snapshot_copy_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#list_snapshot_copy_configurations)
        """

    def list_snapshots(
        self, **kwargs: Unpack[ListSnapshotsRequestRequestTypeDef]
    ) -> ListSnapshotsResponseTypeDef:
        """
        Returns a list of snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/list_snapshots.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#list_snapshots)
        """

    def list_table_restore_status(
        self, **kwargs: Unpack[ListTableRestoreStatusRequestRequestTypeDef]
    ) -> ListTableRestoreStatusResponseTypeDef:
        """
        Returns information about an array of <code>TableRestoreStatus</code> objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/list_table_restore_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#list_table_restore_status)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags assigned to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#list_tags_for_resource)
        """

    def list_usage_limits(
        self, **kwargs: Unpack[ListUsageLimitsRequestRequestTypeDef]
    ) -> ListUsageLimitsResponseTypeDef:
        """
        Lists all usage limits within Amazon Redshift Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/list_usage_limits.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#list_usage_limits)
        """

    def list_workgroups(
        self, **kwargs: Unpack[ListWorkgroupsRequestRequestTypeDef]
    ) -> ListWorkgroupsResponseTypeDef:
        """
        Returns information about a list of specified workgroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/list_workgroups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#list_workgroups)
        """

    def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestRequestTypeDef]
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Creates or updates a resource policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/put_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#put_resource_policy)
        """

    def restore_from_recovery_point(
        self, **kwargs: Unpack[RestoreFromRecoveryPointRequestRequestTypeDef]
    ) -> RestoreFromRecoveryPointResponseTypeDef:
        """
        Restore the data from a recovery point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/restore_from_recovery_point.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#restore_from_recovery_point)
        """

    def restore_from_snapshot(
        self, **kwargs: Unpack[RestoreFromSnapshotRequestRequestTypeDef]
    ) -> RestoreFromSnapshotResponseTypeDef:
        """
        Restores a namespace from a snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/restore_from_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#restore_from_snapshot)
        """

    def restore_table_from_recovery_point(
        self, **kwargs: Unpack[RestoreTableFromRecoveryPointRequestRequestTypeDef]
    ) -> RestoreTableFromRecoveryPointResponseTypeDef:
        """
        Restores a table from a recovery point to your Amazon Redshift Serverless
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/restore_table_from_recovery_point.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#restore_table_from_recovery_point)
        """

    def restore_table_from_snapshot(
        self, **kwargs: Unpack[RestoreTableFromSnapshotRequestRequestTypeDef]
    ) -> RestoreTableFromSnapshotResponseTypeDef:
        """
        Restores a table from a snapshot to your Amazon Redshift Serverless instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/restore_table_from_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#restore_table_from_snapshot)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Assigns one or more tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag or set of tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#untag_resource)
        """

    def update_custom_domain_association(
        self, **kwargs: Unpack[UpdateCustomDomainAssociationRequestRequestTypeDef]
    ) -> UpdateCustomDomainAssociationResponseTypeDef:
        """
        Updates an Amazon Redshift Serverless certificate associated with a custom
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/update_custom_domain_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#update_custom_domain_association)
        """

    def update_endpoint_access(
        self, **kwargs: Unpack[UpdateEndpointAccessRequestRequestTypeDef]
    ) -> UpdateEndpointAccessResponseTypeDef:
        """
        Updates an Amazon Redshift Serverless managed endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/update_endpoint_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#update_endpoint_access)
        """

    def update_namespace(
        self, **kwargs: Unpack[UpdateNamespaceRequestRequestTypeDef]
    ) -> UpdateNamespaceResponseTypeDef:
        """
        Updates a namespace with the specified settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/update_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#update_namespace)
        """

    def update_scheduled_action(
        self, **kwargs: Unpack[UpdateScheduledActionRequestRequestTypeDef]
    ) -> UpdateScheduledActionResponseTypeDef:
        """
        Updates a scheduled action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/update_scheduled_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#update_scheduled_action)
        """

    def update_snapshot(
        self, **kwargs: Unpack[UpdateSnapshotRequestRequestTypeDef]
    ) -> UpdateSnapshotResponseTypeDef:
        """
        Updates a snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/update_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#update_snapshot)
        """

    def update_snapshot_copy_configuration(
        self, **kwargs: Unpack[UpdateSnapshotCopyConfigurationRequestRequestTypeDef]
    ) -> UpdateSnapshotCopyConfigurationResponseTypeDef:
        """
        Updates a snapshot copy configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/update_snapshot_copy_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#update_snapshot_copy_configuration)
        """

    def update_usage_limit(
        self, **kwargs: Unpack[UpdateUsageLimitRequestRequestTypeDef]
    ) -> UpdateUsageLimitResponseTypeDef:
        """
        Update a usage limit in Amazon Redshift Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/update_usage_limit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#update_usage_limit)
        """

    def update_workgroup(
        self, **kwargs: Unpack[UpdateWorkgroupRequestRequestTypeDef]
    ) -> UpdateWorkgroupResponseTypeDef:
        """
        Updates a workgroup with the specified configuration settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/update_workgroup.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#update_workgroup)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_domain_associations"]
    ) -> ListCustomDomainAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_endpoint_access"]
    ) -> ListEndpointAccessPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_managed_workgroups"]
    ) -> ListManagedWorkgroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_namespaces"]) -> ListNamespacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recovery_points"]
    ) -> ListRecoveryPointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_scheduled_actions"]
    ) -> ListScheduledActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_snapshot_copy_configurations"]
    ) -> ListSnapshotCopyConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_snapshots"]) -> ListSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_table_restore_status"]
    ) -> ListTableRestoreStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_usage_limits"]
    ) -> ListUsageLimitsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workgroups"]) -> ListWorkgroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift_serverless/client/#get_paginator)
        """
