"""
Type annotations for redshift service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_redshift.client import RedshiftClient

    session = Session()
    client: RedshiftClient = session.client("redshift")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeClusterDbRevisionsPaginator,
    DescribeClusterParameterGroupsPaginator,
    DescribeClusterParametersPaginator,
    DescribeClusterSecurityGroupsPaginator,
    DescribeClusterSnapshotsPaginator,
    DescribeClustersPaginator,
    DescribeClusterSubnetGroupsPaginator,
    DescribeClusterTracksPaginator,
    DescribeClusterVersionsPaginator,
    DescribeCustomDomainAssociationsPaginator,
    DescribeDataSharesForConsumerPaginator,
    DescribeDataSharesForProducerPaginator,
    DescribeDataSharesPaginator,
    DescribeDefaultClusterParametersPaginator,
    DescribeEndpointAccessPaginator,
    DescribeEndpointAuthorizationPaginator,
    DescribeEventsPaginator,
    DescribeEventSubscriptionsPaginator,
    DescribeHsmClientCertificatesPaginator,
    DescribeHsmConfigurationsPaginator,
    DescribeInboundIntegrationsPaginator,
    DescribeIntegrationsPaginator,
    DescribeNodeConfigurationOptionsPaginator,
    DescribeOrderableClusterOptionsPaginator,
    DescribeRedshiftIdcApplicationsPaginator,
    DescribeReservedNodeExchangeStatusPaginator,
    DescribeReservedNodeOfferingsPaginator,
    DescribeReservedNodesPaginator,
    DescribeScheduledActionsPaginator,
    DescribeSnapshotCopyGrantsPaginator,
    DescribeSnapshotSchedulesPaginator,
    DescribeTableRestoreStatusPaginator,
    DescribeTagsPaginator,
    DescribeUsageLimitsPaginator,
    GetReservedNodeExchangeConfigurationOptionsPaginator,
    GetReservedNodeExchangeOfferingsPaginator,
    ListRecommendationsPaginator,
)
from .type_defs import (
    AcceptReservedNodeExchangeInputMessageRequestTypeDef,
    AcceptReservedNodeExchangeOutputMessageTypeDef,
    AccountAttributeListTypeDef,
    AssociateDataShareConsumerMessageRequestTypeDef,
    AuthorizeClusterSecurityGroupIngressMessageRequestTypeDef,
    AuthorizeClusterSecurityGroupIngressResultTypeDef,
    AuthorizeDataShareMessageRequestTypeDef,
    AuthorizeEndpointAccessMessageRequestTypeDef,
    AuthorizeSnapshotAccessMessageRequestTypeDef,
    AuthorizeSnapshotAccessResultTypeDef,
    BatchDeleteClusterSnapshotsRequestRequestTypeDef,
    BatchDeleteClusterSnapshotsResultTypeDef,
    BatchModifyClusterSnapshotsMessageRequestTypeDef,
    BatchModifyClusterSnapshotsOutputMessageTypeDef,
    CancelResizeMessageRequestTypeDef,
    ClusterCredentialsTypeDef,
    ClusterDbRevisionsMessageTypeDef,
    ClusterExtendedCredentialsTypeDef,
    ClusterParameterGroupDetailsTypeDef,
    ClusterParameterGroupNameMessageTypeDef,
    ClusterParameterGroupsMessageTypeDef,
    ClusterSecurityGroupMessageTypeDef,
    ClustersMessageTypeDef,
    ClusterSubnetGroupMessageTypeDef,
    ClusterVersionsMessageTypeDef,
    CopyClusterSnapshotMessageRequestTypeDef,
    CopyClusterSnapshotResultTypeDef,
    CreateAuthenticationProfileMessageRequestTypeDef,
    CreateAuthenticationProfileResultTypeDef,
    CreateClusterMessageRequestTypeDef,
    CreateClusterParameterGroupMessageRequestTypeDef,
    CreateClusterParameterGroupResultTypeDef,
    CreateClusterResultTypeDef,
    CreateClusterSecurityGroupMessageRequestTypeDef,
    CreateClusterSecurityGroupResultTypeDef,
    CreateClusterSnapshotMessageRequestTypeDef,
    CreateClusterSnapshotResultTypeDef,
    CreateClusterSubnetGroupMessageRequestTypeDef,
    CreateClusterSubnetGroupResultTypeDef,
    CreateCustomDomainAssociationMessageRequestTypeDef,
    CreateCustomDomainAssociationResultTypeDef,
    CreateEndpointAccessMessageRequestTypeDef,
    CreateEventSubscriptionMessageRequestTypeDef,
    CreateEventSubscriptionResultTypeDef,
    CreateHsmClientCertificateMessageRequestTypeDef,
    CreateHsmClientCertificateResultTypeDef,
    CreateHsmConfigurationMessageRequestTypeDef,
    CreateHsmConfigurationResultTypeDef,
    CreateIntegrationMessageRequestTypeDef,
    CreateRedshiftIdcApplicationMessageRequestTypeDef,
    CreateRedshiftIdcApplicationResultTypeDef,
    CreateScheduledActionMessageRequestTypeDef,
    CreateSnapshotCopyGrantMessageRequestTypeDef,
    CreateSnapshotCopyGrantResultTypeDef,
    CreateSnapshotScheduleMessageRequestTypeDef,
    CreateTagsMessageRequestTypeDef,
    CreateUsageLimitMessageRequestTypeDef,
    CustomDomainAssociationsMessageTypeDef,
    CustomerStorageMessageTypeDef,
    DataShareResponseTypeDef,
    DeauthorizeDataShareMessageRequestTypeDef,
    DeleteAuthenticationProfileMessageRequestTypeDef,
    DeleteAuthenticationProfileResultTypeDef,
    DeleteClusterMessageRequestTypeDef,
    DeleteClusterParameterGroupMessageRequestTypeDef,
    DeleteClusterResultTypeDef,
    DeleteClusterSecurityGroupMessageRequestTypeDef,
    DeleteClusterSnapshotMessageRequestTypeDef,
    DeleteClusterSnapshotResultTypeDef,
    DeleteClusterSubnetGroupMessageRequestTypeDef,
    DeleteCustomDomainAssociationMessageRequestTypeDef,
    DeleteEndpointAccessMessageRequestTypeDef,
    DeleteEventSubscriptionMessageRequestTypeDef,
    DeleteHsmClientCertificateMessageRequestTypeDef,
    DeleteHsmConfigurationMessageRequestTypeDef,
    DeleteIntegrationMessageRequestTypeDef,
    DeleteRedshiftIdcApplicationMessageRequestTypeDef,
    DeleteResourcePolicyMessageRequestTypeDef,
    DeleteScheduledActionMessageRequestTypeDef,
    DeleteSnapshotCopyGrantMessageRequestTypeDef,
    DeleteSnapshotScheduleMessageRequestTypeDef,
    DeleteTagsMessageRequestTypeDef,
    DeleteUsageLimitMessageRequestTypeDef,
    DeregisterNamespaceInputMessageRequestTypeDef,
    DeregisterNamespaceOutputMessageTypeDef,
    DescribeAccountAttributesMessageRequestTypeDef,
    DescribeAuthenticationProfilesMessageRequestTypeDef,
    DescribeAuthenticationProfilesResultTypeDef,
    DescribeClusterDbRevisionsMessageRequestTypeDef,
    DescribeClusterParameterGroupsMessageRequestTypeDef,
    DescribeClusterParametersMessageRequestTypeDef,
    DescribeClusterSecurityGroupsMessageRequestTypeDef,
    DescribeClustersMessageRequestTypeDef,
    DescribeClusterSnapshotsMessageRequestTypeDef,
    DescribeClusterSubnetGroupsMessageRequestTypeDef,
    DescribeClusterTracksMessageRequestTypeDef,
    DescribeClusterVersionsMessageRequestTypeDef,
    DescribeCustomDomainAssociationsMessageRequestTypeDef,
    DescribeDataSharesForConsumerMessageRequestTypeDef,
    DescribeDataSharesForConsumerResultTypeDef,
    DescribeDataSharesForProducerMessageRequestTypeDef,
    DescribeDataSharesForProducerResultTypeDef,
    DescribeDataSharesMessageRequestTypeDef,
    DescribeDataSharesResultTypeDef,
    DescribeDefaultClusterParametersMessageRequestTypeDef,
    DescribeDefaultClusterParametersResultTypeDef,
    DescribeEndpointAccessMessageRequestTypeDef,
    DescribeEndpointAuthorizationMessageRequestTypeDef,
    DescribeEventCategoriesMessageRequestTypeDef,
    DescribeEventsMessageRequestTypeDef,
    DescribeEventSubscriptionsMessageRequestTypeDef,
    DescribeHsmClientCertificatesMessageRequestTypeDef,
    DescribeHsmConfigurationsMessageRequestTypeDef,
    DescribeInboundIntegrationsMessageRequestTypeDef,
    DescribeIntegrationsMessageRequestTypeDef,
    DescribeLoggingStatusMessageRequestTypeDef,
    DescribeNodeConfigurationOptionsMessageRequestTypeDef,
    DescribeOrderableClusterOptionsMessageRequestTypeDef,
    DescribePartnersInputMessageRequestTypeDef,
    DescribePartnersOutputMessageTypeDef,
    DescribeRedshiftIdcApplicationsMessageRequestTypeDef,
    DescribeRedshiftIdcApplicationsResultTypeDef,
    DescribeReservedNodeExchangeStatusInputMessageRequestTypeDef,
    DescribeReservedNodeExchangeStatusOutputMessageTypeDef,
    DescribeReservedNodeOfferingsMessageRequestTypeDef,
    DescribeReservedNodesMessageRequestTypeDef,
    DescribeResizeMessageRequestTypeDef,
    DescribeScheduledActionsMessageRequestTypeDef,
    DescribeSnapshotCopyGrantsMessageRequestTypeDef,
    DescribeSnapshotSchedulesMessageRequestTypeDef,
    DescribeSnapshotSchedulesOutputMessageTypeDef,
    DescribeTableRestoreStatusMessageRequestTypeDef,
    DescribeTagsMessageRequestTypeDef,
    DescribeUsageLimitsMessageRequestTypeDef,
    DisableLoggingMessageRequestTypeDef,
    DisableSnapshotCopyMessageRequestTypeDef,
    DisableSnapshotCopyResultTypeDef,
    DisassociateDataShareConsumerMessageRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableLoggingMessageRequestTypeDef,
    EnableSnapshotCopyMessageRequestTypeDef,
    EnableSnapshotCopyResultTypeDef,
    EndpointAccessListTypeDef,
    EndpointAccessResponseTypeDef,
    EndpointAuthorizationListTypeDef,
    EndpointAuthorizationResponseTypeDef,
    EventCategoriesMessageTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    FailoverPrimaryComputeInputMessageRequestTypeDef,
    FailoverPrimaryComputeResultTypeDef,
    GetClusterCredentialsMessageRequestTypeDef,
    GetClusterCredentialsWithIAMMessageRequestTypeDef,
    GetReservedNodeExchangeConfigurationOptionsInputMessageRequestTypeDef,
    GetReservedNodeExchangeConfigurationOptionsOutputMessageTypeDef,
    GetReservedNodeExchangeOfferingsInputMessageRequestTypeDef,
    GetReservedNodeExchangeOfferingsOutputMessageTypeDef,
    GetResourcePolicyMessageRequestTypeDef,
    GetResourcePolicyResultTypeDef,
    HsmClientCertificateMessageTypeDef,
    HsmConfigurationMessageTypeDef,
    InboundIntegrationsMessageTypeDef,
    IntegrationResponseTypeDef,
    IntegrationsMessageTypeDef,
    ListRecommendationsMessageRequestTypeDef,
    ListRecommendationsResultTypeDef,
    LoggingStatusTypeDef,
    ModifyAquaInputMessageRequestTypeDef,
    ModifyAquaOutputMessageTypeDef,
    ModifyAuthenticationProfileMessageRequestTypeDef,
    ModifyAuthenticationProfileResultTypeDef,
    ModifyClusterDbRevisionMessageRequestTypeDef,
    ModifyClusterDbRevisionResultTypeDef,
    ModifyClusterIamRolesMessageRequestTypeDef,
    ModifyClusterIamRolesResultTypeDef,
    ModifyClusterMaintenanceMessageRequestTypeDef,
    ModifyClusterMaintenanceResultTypeDef,
    ModifyClusterMessageRequestTypeDef,
    ModifyClusterParameterGroupMessageRequestTypeDef,
    ModifyClusterResultTypeDef,
    ModifyClusterSnapshotMessageRequestTypeDef,
    ModifyClusterSnapshotResultTypeDef,
    ModifyClusterSnapshotScheduleMessageRequestTypeDef,
    ModifyClusterSubnetGroupMessageRequestTypeDef,
    ModifyClusterSubnetGroupResultTypeDef,
    ModifyCustomDomainAssociationMessageRequestTypeDef,
    ModifyCustomDomainAssociationResultTypeDef,
    ModifyEndpointAccessMessageRequestTypeDef,
    ModifyEventSubscriptionMessageRequestTypeDef,
    ModifyEventSubscriptionResultTypeDef,
    ModifyIntegrationMessageRequestTypeDef,
    ModifyRedshiftIdcApplicationMessageRequestTypeDef,
    ModifyRedshiftIdcApplicationResultTypeDef,
    ModifyScheduledActionMessageRequestTypeDef,
    ModifySnapshotCopyRetentionPeriodMessageRequestTypeDef,
    ModifySnapshotCopyRetentionPeriodResultTypeDef,
    ModifySnapshotScheduleMessageRequestTypeDef,
    ModifyUsageLimitMessageRequestTypeDef,
    NodeConfigurationOptionsMessageTypeDef,
    OrderableClusterOptionsMessageTypeDef,
    PartnerIntegrationInputMessageRequestTypeDef,
    PartnerIntegrationOutputMessageTypeDef,
    PauseClusterMessageRequestTypeDef,
    PauseClusterResultTypeDef,
    PurchaseReservedNodeOfferingMessageRequestTypeDef,
    PurchaseReservedNodeOfferingResultTypeDef,
    PutResourcePolicyMessageRequestTypeDef,
    PutResourcePolicyResultTypeDef,
    RebootClusterMessageRequestTypeDef,
    RebootClusterResultTypeDef,
    RegisterNamespaceInputMessageRequestTypeDef,
    RegisterNamespaceOutputMessageTypeDef,
    RejectDataShareMessageRequestTypeDef,
    ReservedNodeOfferingsMessageTypeDef,
    ReservedNodesMessageTypeDef,
    ResetClusterParameterGroupMessageRequestTypeDef,
    ResizeClusterMessageRequestTypeDef,
    ResizeClusterResultTypeDef,
    ResizeProgressMessageTypeDef,
    RestoreFromClusterSnapshotMessageRequestTypeDef,
    RestoreFromClusterSnapshotResultTypeDef,
    RestoreTableFromClusterSnapshotMessageRequestTypeDef,
    RestoreTableFromClusterSnapshotResultTypeDef,
    ResumeClusterMessageRequestTypeDef,
    ResumeClusterResultTypeDef,
    RevokeClusterSecurityGroupIngressMessageRequestTypeDef,
    RevokeClusterSecurityGroupIngressResultTypeDef,
    RevokeEndpointAccessMessageRequestTypeDef,
    RevokeSnapshotAccessMessageRequestTypeDef,
    RevokeSnapshotAccessResultTypeDef,
    RotateEncryptionKeyMessageRequestTypeDef,
    RotateEncryptionKeyResultTypeDef,
    ScheduledActionResponseTypeDef,
    ScheduledActionsMessageTypeDef,
    SnapshotCopyGrantMessageTypeDef,
    SnapshotMessageTypeDef,
    SnapshotScheduleResponseTypeDef,
    TableRestoreStatusMessageTypeDef,
    TaggedResourceListMessageTypeDef,
    TrackListMessageTypeDef,
    UpdatePartnerStatusInputMessageRequestTypeDef,
    UsageLimitListTypeDef,
    UsageLimitResponseTypeDef,
)
from .waiter import (
    ClusterAvailableWaiter,
    ClusterDeletedWaiter,
    ClusterRestoredWaiter,
    SnapshotAvailableWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("RedshiftClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessToClusterDeniedFault: Type[BotocoreClientError]
    AccessToSnapshotDeniedFault: Type[BotocoreClientError]
    AuthenticationProfileAlreadyExistsFault: Type[BotocoreClientError]
    AuthenticationProfileNotFoundFault: Type[BotocoreClientError]
    AuthenticationProfileQuotaExceededFault: Type[BotocoreClientError]
    AuthorizationAlreadyExistsFault: Type[BotocoreClientError]
    AuthorizationNotFoundFault: Type[BotocoreClientError]
    AuthorizationQuotaExceededFault: Type[BotocoreClientError]
    BatchDeleteRequestSizeExceededFault: Type[BotocoreClientError]
    BatchModifyClusterSnapshotsLimitExceededFault: Type[BotocoreClientError]
    BucketNotFoundFault: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClusterAlreadyExistsFault: Type[BotocoreClientError]
    ClusterNotFoundFault: Type[BotocoreClientError]
    ClusterOnLatestRevisionFault: Type[BotocoreClientError]
    ClusterParameterGroupAlreadyExistsFault: Type[BotocoreClientError]
    ClusterParameterGroupNotFoundFault: Type[BotocoreClientError]
    ClusterParameterGroupQuotaExceededFault: Type[BotocoreClientError]
    ClusterQuotaExceededFault: Type[BotocoreClientError]
    ClusterSecurityGroupAlreadyExistsFault: Type[BotocoreClientError]
    ClusterSecurityGroupNotFoundFault: Type[BotocoreClientError]
    ClusterSecurityGroupQuotaExceededFault: Type[BotocoreClientError]
    ClusterSnapshotAlreadyExistsFault: Type[BotocoreClientError]
    ClusterSnapshotNotFoundFault: Type[BotocoreClientError]
    ClusterSnapshotQuotaExceededFault: Type[BotocoreClientError]
    ClusterSubnetGroupAlreadyExistsFault: Type[BotocoreClientError]
    ClusterSubnetGroupNotFoundFault: Type[BotocoreClientError]
    ClusterSubnetGroupQuotaExceededFault: Type[BotocoreClientError]
    ClusterSubnetQuotaExceededFault: Type[BotocoreClientError]
    ConflictPolicyUpdateFault: Type[BotocoreClientError]
    CopyToRegionDisabledFault: Type[BotocoreClientError]
    CustomCnameAssociationFault: Type[BotocoreClientError]
    CustomDomainAssociationNotFoundFault: Type[BotocoreClientError]
    DependentServiceAccessDeniedFault: Type[BotocoreClientError]
    DependentServiceRequestThrottlingFault: Type[BotocoreClientError]
    DependentServiceUnavailableFault: Type[BotocoreClientError]
    EndpointAlreadyExistsFault: Type[BotocoreClientError]
    EndpointAuthorizationAlreadyExistsFault: Type[BotocoreClientError]
    EndpointAuthorizationNotFoundFault: Type[BotocoreClientError]
    EndpointAuthorizationsPerClusterLimitExceededFault: Type[BotocoreClientError]
    EndpointNotFoundFault: Type[BotocoreClientError]
    EndpointsPerAuthorizationLimitExceededFault: Type[BotocoreClientError]
    EndpointsPerClusterLimitExceededFault: Type[BotocoreClientError]
    EventSubscriptionQuotaExceededFault: Type[BotocoreClientError]
    HsmClientCertificateAlreadyExistsFault: Type[BotocoreClientError]
    HsmClientCertificateNotFoundFault: Type[BotocoreClientError]
    HsmClientCertificateQuotaExceededFault: Type[BotocoreClientError]
    HsmConfigurationAlreadyExistsFault: Type[BotocoreClientError]
    HsmConfigurationNotFoundFault: Type[BotocoreClientError]
    HsmConfigurationQuotaExceededFault: Type[BotocoreClientError]
    InProgressTableRestoreQuotaExceededFault: Type[BotocoreClientError]
    IncompatibleOrderableOptions: Type[BotocoreClientError]
    InsufficientClusterCapacityFault: Type[BotocoreClientError]
    InsufficientS3BucketPolicyFault: Type[BotocoreClientError]
    IntegrationAlreadyExistsFault: Type[BotocoreClientError]
    IntegrationConflictOperationFault: Type[BotocoreClientError]
    IntegrationConflictStateFault: Type[BotocoreClientError]
    IntegrationNotFoundFault: Type[BotocoreClientError]
    IntegrationQuotaExceededFault: Type[BotocoreClientError]
    IntegrationSourceNotFoundFault: Type[BotocoreClientError]
    IntegrationTargetNotFoundFault: Type[BotocoreClientError]
    InvalidAuthenticationProfileRequestFault: Type[BotocoreClientError]
    InvalidAuthorizationStateFault: Type[BotocoreClientError]
    InvalidClusterParameterGroupStateFault: Type[BotocoreClientError]
    InvalidClusterSecurityGroupStateFault: Type[BotocoreClientError]
    InvalidClusterSnapshotScheduleStateFault: Type[BotocoreClientError]
    InvalidClusterSnapshotStateFault: Type[BotocoreClientError]
    InvalidClusterStateFault: Type[BotocoreClientError]
    InvalidClusterSubnetGroupStateFault: Type[BotocoreClientError]
    InvalidClusterSubnetStateFault: Type[BotocoreClientError]
    InvalidClusterTrackFault: Type[BotocoreClientError]
    InvalidDataShareFault: Type[BotocoreClientError]
    InvalidElasticIpFault: Type[BotocoreClientError]
    InvalidEndpointStateFault: Type[BotocoreClientError]
    InvalidHsmClientCertificateStateFault: Type[BotocoreClientError]
    InvalidHsmConfigurationStateFault: Type[BotocoreClientError]
    InvalidNamespaceFault: Type[BotocoreClientError]
    InvalidPolicyFault: Type[BotocoreClientError]
    InvalidReservedNodeStateFault: Type[BotocoreClientError]
    InvalidRestoreFault: Type[BotocoreClientError]
    InvalidRetentionPeriodFault: Type[BotocoreClientError]
    InvalidS3BucketNameFault: Type[BotocoreClientError]
    InvalidS3KeyPrefixFault: Type[BotocoreClientError]
    InvalidScheduleFault: Type[BotocoreClientError]
    InvalidScheduledActionFault: Type[BotocoreClientError]
    InvalidSnapshotCopyGrantStateFault: Type[BotocoreClientError]
    InvalidSubnet: Type[BotocoreClientError]
    InvalidSubscriptionStateFault: Type[BotocoreClientError]
    InvalidTableRestoreArgumentFault: Type[BotocoreClientError]
    InvalidTagFault: Type[BotocoreClientError]
    InvalidUsageLimitFault: Type[BotocoreClientError]
    InvalidVPCNetworkStateFault: Type[BotocoreClientError]
    Ipv6CidrBlockNotFoundFault: Type[BotocoreClientError]
    LimitExceededFault: Type[BotocoreClientError]
    NumberOfNodesPerClusterLimitExceededFault: Type[BotocoreClientError]
    NumberOfNodesQuotaExceededFault: Type[BotocoreClientError]
    PartnerNotFoundFault: Type[BotocoreClientError]
    RedshiftIdcApplicationAlreadyExistsFault: Type[BotocoreClientError]
    RedshiftIdcApplicationNotExistsFault: Type[BotocoreClientError]
    RedshiftIdcApplicationQuotaExceededFault: Type[BotocoreClientError]
    ReservedNodeAlreadyExistsFault: Type[BotocoreClientError]
    ReservedNodeAlreadyMigratedFault: Type[BotocoreClientError]
    ReservedNodeExchangeNotFoundFault: Type[BotocoreClientError]
    ReservedNodeNotFoundFault: Type[BotocoreClientError]
    ReservedNodeOfferingNotFoundFault: Type[BotocoreClientError]
    ReservedNodeQuotaExceededFault: Type[BotocoreClientError]
    ResizeNotFoundFault: Type[BotocoreClientError]
    ResourceNotFoundFault: Type[BotocoreClientError]
    SNSInvalidTopicFault: Type[BotocoreClientError]
    SNSNoAuthorizationFault: Type[BotocoreClientError]
    SNSTopicArnNotFoundFault: Type[BotocoreClientError]
    ScheduleDefinitionTypeUnsupportedFault: Type[BotocoreClientError]
    ScheduledActionAlreadyExistsFault: Type[BotocoreClientError]
    ScheduledActionNotFoundFault: Type[BotocoreClientError]
    ScheduledActionQuotaExceededFault: Type[BotocoreClientError]
    ScheduledActionTypeUnsupportedFault: Type[BotocoreClientError]
    SnapshotCopyAlreadyDisabledFault: Type[BotocoreClientError]
    SnapshotCopyAlreadyEnabledFault: Type[BotocoreClientError]
    SnapshotCopyDisabledFault: Type[BotocoreClientError]
    SnapshotCopyGrantAlreadyExistsFault: Type[BotocoreClientError]
    SnapshotCopyGrantNotFoundFault: Type[BotocoreClientError]
    SnapshotCopyGrantQuotaExceededFault: Type[BotocoreClientError]
    SnapshotScheduleAlreadyExistsFault: Type[BotocoreClientError]
    SnapshotScheduleNotFoundFault: Type[BotocoreClientError]
    SnapshotScheduleQuotaExceededFault: Type[BotocoreClientError]
    SnapshotScheduleUpdateInProgressFault: Type[BotocoreClientError]
    SourceNotFoundFault: Type[BotocoreClientError]
    SubnetAlreadyInUse: Type[BotocoreClientError]
    SubscriptionAlreadyExistFault: Type[BotocoreClientError]
    SubscriptionCategoryNotFoundFault: Type[BotocoreClientError]
    SubscriptionEventIdNotFoundFault: Type[BotocoreClientError]
    SubscriptionNotFoundFault: Type[BotocoreClientError]
    SubscriptionSeverityNotFoundFault: Type[BotocoreClientError]
    TableLimitExceededFault: Type[BotocoreClientError]
    TableRestoreNotFoundFault: Type[BotocoreClientError]
    TagLimitExceededFault: Type[BotocoreClientError]
    UnauthorizedOperation: Type[BotocoreClientError]
    UnauthorizedPartnerIntegrationFault: Type[BotocoreClientError]
    UnknownSnapshotCopyRegionFault: Type[BotocoreClientError]
    UnsupportedOperationFault: Type[BotocoreClientError]
    UnsupportedOptionFault: Type[BotocoreClientError]
    UsageLimitAlreadyExistsFault: Type[BotocoreClientError]
    UsageLimitNotFoundFault: Type[BotocoreClientError]


class RedshiftClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RedshiftClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#close)
        """

    def accept_reserved_node_exchange(
        self, **kwargs: Unpack[AcceptReservedNodeExchangeInputMessageRequestTypeDef]
    ) -> AcceptReservedNodeExchangeOutputMessageTypeDef:
        """
        Exchanges a DC1 Reserved Node for a DC2 Reserved Node with no changes to the
        configuration (term, payment type, or number of nodes) and no additional costs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/accept_reserved_node_exchange.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#accept_reserved_node_exchange)
        """

    def add_partner(
        self, **kwargs: Unpack[PartnerIntegrationInputMessageRequestTypeDef]
    ) -> PartnerIntegrationOutputMessageTypeDef:
        """
        Adds a partner integration to a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/add_partner.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#add_partner)
        """

    def associate_data_share_consumer(
        self, **kwargs: Unpack[AssociateDataShareConsumerMessageRequestTypeDef]
    ) -> DataShareResponseTypeDef:
        """
        From a datashare consumer account, associates a datashare with the account
        (AssociateEntireAccount) or the specified namespace (ConsumerArn).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/associate_data_share_consumer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#associate_data_share_consumer)
        """

    def authorize_cluster_security_group_ingress(
        self, **kwargs: Unpack[AuthorizeClusterSecurityGroupIngressMessageRequestTypeDef]
    ) -> AuthorizeClusterSecurityGroupIngressResultTypeDef:
        """
        Adds an inbound (ingress) rule to an Amazon Redshift security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/authorize_cluster_security_group_ingress.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#authorize_cluster_security_group_ingress)
        """

    def authorize_data_share(
        self, **kwargs: Unpack[AuthorizeDataShareMessageRequestTypeDef]
    ) -> DataShareResponseTypeDef:
        """
        From a data producer account, authorizes the sharing of a datashare with one or
        more consumer accounts or managing entities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/authorize_data_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#authorize_data_share)
        """

    def authorize_endpoint_access(
        self, **kwargs: Unpack[AuthorizeEndpointAccessMessageRequestTypeDef]
    ) -> EndpointAuthorizationResponseTypeDef:
        """
        Grants access to a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/authorize_endpoint_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#authorize_endpoint_access)
        """

    def authorize_snapshot_access(
        self, **kwargs: Unpack[AuthorizeSnapshotAccessMessageRequestTypeDef]
    ) -> AuthorizeSnapshotAccessResultTypeDef:
        """
        Authorizes the specified Amazon Web Services account to restore the specified
        snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/authorize_snapshot_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#authorize_snapshot_access)
        """

    def batch_delete_cluster_snapshots(
        self, **kwargs: Unpack[BatchDeleteClusterSnapshotsRequestRequestTypeDef]
    ) -> BatchDeleteClusterSnapshotsResultTypeDef:
        """
        Deletes a set of cluster snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/batch_delete_cluster_snapshots.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#batch_delete_cluster_snapshots)
        """

    def batch_modify_cluster_snapshots(
        self, **kwargs: Unpack[BatchModifyClusterSnapshotsMessageRequestTypeDef]
    ) -> BatchModifyClusterSnapshotsOutputMessageTypeDef:
        """
        Modifies the settings for a set of cluster snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/batch_modify_cluster_snapshots.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#batch_modify_cluster_snapshots)
        """

    def cancel_resize(
        self, **kwargs: Unpack[CancelResizeMessageRequestTypeDef]
    ) -> ResizeProgressMessageTypeDef:
        """
        Cancels a resize operation for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/cancel_resize.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#cancel_resize)
        """

    def copy_cluster_snapshot(
        self, **kwargs: Unpack[CopyClusterSnapshotMessageRequestTypeDef]
    ) -> CopyClusterSnapshotResultTypeDef:
        """
        Copies the specified automated cluster snapshot to a new manual cluster
        snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/copy_cluster_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#copy_cluster_snapshot)
        """

    def create_authentication_profile(
        self, **kwargs: Unpack[CreateAuthenticationProfileMessageRequestTypeDef]
    ) -> CreateAuthenticationProfileResultTypeDef:
        """
        Creates an authentication profile with the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_authentication_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_authentication_profile)
        """

    def create_cluster(
        self, **kwargs: Unpack[CreateClusterMessageRequestTypeDef]
    ) -> CreateClusterResultTypeDef:
        """
        Creates a new cluster with the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_cluster)
        """

    def create_cluster_parameter_group(
        self, **kwargs: Unpack[CreateClusterParameterGroupMessageRequestTypeDef]
    ) -> CreateClusterParameterGroupResultTypeDef:
        """
        Creates an Amazon Redshift parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_cluster_parameter_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_cluster_parameter_group)
        """

    def create_cluster_security_group(
        self, **kwargs: Unpack[CreateClusterSecurityGroupMessageRequestTypeDef]
    ) -> CreateClusterSecurityGroupResultTypeDef:
        """
        Creates a new Amazon Redshift security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_cluster_security_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_cluster_security_group)
        """

    def create_cluster_snapshot(
        self, **kwargs: Unpack[CreateClusterSnapshotMessageRequestTypeDef]
    ) -> CreateClusterSnapshotResultTypeDef:
        """
        Creates a manual snapshot of the specified cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_cluster_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_cluster_snapshot)
        """

    def create_cluster_subnet_group(
        self, **kwargs: Unpack[CreateClusterSubnetGroupMessageRequestTypeDef]
    ) -> CreateClusterSubnetGroupResultTypeDef:
        """
        Creates a new Amazon Redshift subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_cluster_subnet_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_cluster_subnet_group)
        """

    def create_custom_domain_association(
        self, **kwargs: Unpack[CreateCustomDomainAssociationMessageRequestTypeDef]
    ) -> CreateCustomDomainAssociationResultTypeDef:
        """
        Used to create a custom domain name for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_custom_domain_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_custom_domain_association)
        """

    def create_endpoint_access(
        self, **kwargs: Unpack[CreateEndpointAccessMessageRequestTypeDef]
    ) -> EndpointAccessResponseTypeDef:
        """
        Creates a Redshift-managed VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_endpoint_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_endpoint_access)
        """

    def create_event_subscription(
        self, **kwargs: Unpack[CreateEventSubscriptionMessageRequestTypeDef]
    ) -> CreateEventSubscriptionResultTypeDef:
        """
        Creates an Amazon Redshift event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_event_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_event_subscription)
        """

    def create_hsm_client_certificate(
        self, **kwargs: Unpack[CreateHsmClientCertificateMessageRequestTypeDef]
    ) -> CreateHsmClientCertificateResultTypeDef:
        """
        Creates an HSM client certificate that an Amazon Redshift cluster will use to
        connect to the client's HSM in order to store and retrieve the keys used to
        encrypt the cluster databases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_hsm_client_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_hsm_client_certificate)
        """

    def create_hsm_configuration(
        self, **kwargs: Unpack[CreateHsmConfigurationMessageRequestTypeDef]
    ) -> CreateHsmConfigurationResultTypeDef:
        """
        Creates an HSM configuration that contains the information required by an
        Amazon Redshift cluster to store and use database encryption keys in a Hardware
        Security Module (HSM).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_hsm_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_hsm_configuration)
        """

    def create_integration(
        self, **kwargs: Unpack[CreateIntegrationMessageRequestTypeDef]
    ) -> IntegrationResponseTypeDef:
        """
        Creates a zero-ETL integration or S3 event integration with Amazon Redshift.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_integration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_integration)
        """

    def create_redshift_idc_application(
        self, **kwargs: Unpack[CreateRedshiftIdcApplicationMessageRequestTypeDef]
    ) -> CreateRedshiftIdcApplicationResultTypeDef:
        """
        Creates an Amazon Redshift application for use with IAM Identity Center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_redshift_idc_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_redshift_idc_application)
        """

    def create_scheduled_action(
        self, **kwargs: Unpack[CreateScheduledActionMessageRequestTypeDef]
    ) -> ScheduledActionResponseTypeDef:
        """
        Creates a scheduled action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_scheduled_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_scheduled_action)
        """

    def create_snapshot_copy_grant(
        self, **kwargs: Unpack[CreateSnapshotCopyGrantMessageRequestTypeDef]
    ) -> CreateSnapshotCopyGrantResultTypeDef:
        """
        Creates a snapshot copy grant that permits Amazon Redshift to use an encrypted
        symmetric key from Key Management Service (KMS) to encrypt copied snapshots in
        a destination region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_snapshot_copy_grant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_snapshot_copy_grant)
        """

    def create_snapshot_schedule(
        self, **kwargs: Unpack[CreateSnapshotScheduleMessageRequestTypeDef]
    ) -> SnapshotScheduleResponseTypeDef:
        """
        Create a snapshot schedule that can be associated to a cluster and which
        overrides the default system backup schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_snapshot_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_snapshot_schedule)
        """

    def create_tags(
        self, **kwargs: Unpack[CreateTagsMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds tags to a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_tags)
        """

    def create_usage_limit(
        self, **kwargs: Unpack[CreateUsageLimitMessageRequestTypeDef]
    ) -> UsageLimitResponseTypeDef:
        """
        Creates a usage limit for a specified Amazon Redshift feature on a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/create_usage_limit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#create_usage_limit)
        """

    def deauthorize_data_share(
        self, **kwargs: Unpack[DeauthorizeDataShareMessageRequestTypeDef]
    ) -> DataShareResponseTypeDef:
        """
        From a datashare producer account, removes authorization from the specified
        datashare.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/deauthorize_data_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#deauthorize_data_share)
        """

    def delete_authentication_profile(
        self, **kwargs: Unpack[DeleteAuthenticationProfileMessageRequestTypeDef]
    ) -> DeleteAuthenticationProfileResultTypeDef:
        """
        Deletes an authentication profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_authentication_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_authentication_profile)
        """

    def delete_cluster(
        self, **kwargs: Unpack[DeleteClusterMessageRequestTypeDef]
    ) -> DeleteClusterResultTypeDef:
        """
        Deletes a previously provisioned cluster without its final snapshot being
        created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_cluster)
        """

    def delete_cluster_parameter_group(
        self, **kwargs: Unpack[DeleteClusterParameterGroupMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified Amazon Redshift parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_cluster_parameter_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_cluster_parameter_group)
        """

    def delete_cluster_security_group(
        self, **kwargs: Unpack[DeleteClusterSecurityGroupMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Redshift security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_cluster_security_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_cluster_security_group)
        """

    def delete_cluster_snapshot(
        self, **kwargs: Unpack[DeleteClusterSnapshotMessageRequestTypeDef]
    ) -> DeleteClusterSnapshotResultTypeDef:
        """
        Deletes the specified manual snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_cluster_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_cluster_snapshot)
        """

    def delete_cluster_subnet_group(
        self, **kwargs: Unpack[DeleteClusterSubnetGroupMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified cluster subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_cluster_subnet_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_cluster_subnet_group)
        """

    def delete_custom_domain_association(
        self, **kwargs: Unpack[DeleteCustomDomainAssociationMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Contains information about deleting a custom domain association for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_custom_domain_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_custom_domain_association)
        """

    def delete_endpoint_access(
        self, **kwargs: Unpack[DeleteEndpointAccessMessageRequestTypeDef]
    ) -> EndpointAccessResponseTypeDef:
        """
        Deletes a Redshift-managed VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_endpoint_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_endpoint_access)
        """

    def delete_event_subscription(
        self, **kwargs: Unpack[DeleteEventSubscriptionMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Redshift event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_event_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_event_subscription)
        """

    def delete_hsm_client_certificate(
        self, **kwargs: Unpack[DeleteHsmClientCertificateMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified HSM client certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_hsm_client_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_hsm_client_certificate)
        """

    def delete_hsm_configuration(
        self, **kwargs: Unpack[DeleteHsmConfigurationMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Amazon Redshift HSM configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_hsm_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_hsm_configuration)
        """

    def delete_integration(
        self, **kwargs: Unpack[DeleteIntegrationMessageRequestTypeDef]
    ) -> IntegrationResponseTypeDef:
        """
        Deletes a zero-ETL integration or S3 event integration with Amazon Redshift.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_integration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_integration)
        """

    def delete_partner(
        self, **kwargs: Unpack[PartnerIntegrationInputMessageRequestTypeDef]
    ) -> PartnerIntegrationOutputMessageTypeDef:
        """
        Deletes a partner integration from a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_partner.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_partner)
        """

    def delete_redshift_idc_application(
        self, **kwargs: Unpack[DeleteRedshiftIdcApplicationMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Redshift IAM Identity Center application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_redshift_idc_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_redshift_idc_application)
        """

    def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the resource policy for a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_resource_policy)
        """

    def delete_scheduled_action(
        self, **kwargs: Unpack[DeleteScheduledActionMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a scheduled action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_scheduled_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_scheduled_action)
        """

    def delete_snapshot_copy_grant(
        self, **kwargs: Unpack[DeleteSnapshotCopyGrantMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified snapshot copy grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_snapshot_copy_grant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_snapshot_copy_grant)
        """

    def delete_snapshot_schedule(
        self, **kwargs: Unpack[DeleteSnapshotScheduleMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a snapshot schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_snapshot_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_snapshot_schedule)
        """

    def delete_tags(
        self, **kwargs: Unpack[DeleteTagsMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_tags)
        """

    def delete_usage_limit(
        self, **kwargs: Unpack[DeleteUsageLimitMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a usage limit from a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/delete_usage_limit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#delete_usage_limit)
        """

    def deregister_namespace(
        self, **kwargs: Unpack[DeregisterNamespaceInputMessageRequestTypeDef]
    ) -> DeregisterNamespaceOutputMessageTypeDef:
        """
        Deregisters a cluster or serverless namespace from the Amazon Web Services Glue
        Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/deregister_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#deregister_namespace)
        """

    def describe_account_attributes(
        self, **kwargs: Unpack[DescribeAccountAttributesMessageRequestTypeDef]
    ) -> AccountAttributeListTypeDef:
        """
        Returns a list of attributes attached to an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_account_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_account_attributes)
        """

    def describe_authentication_profiles(
        self, **kwargs: Unpack[DescribeAuthenticationProfilesMessageRequestTypeDef]
    ) -> DescribeAuthenticationProfilesResultTypeDef:
        """
        Describes an authentication profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_authentication_profiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_authentication_profiles)
        """

    def describe_cluster_db_revisions(
        self, **kwargs: Unpack[DescribeClusterDbRevisionsMessageRequestTypeDef]
    ) -> ClusterDbRevisionsMessageTypeDef:
        """
        Returns an array of <code>ClusterDbRevision</code> objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_cluster_db_revisions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_cluster_db_revisions)
        """

    def describe_cluster_parameter_groups(
        self, **kwargs: Unpack[DescribeClusterParameterGroupsMessageRequestTypeDef]
    ) -> ClusterParameterGroupsMessageTypeDef:
        """
        Returns a list of Amazon Redshift parameter groups, including parameter groups
        you created and the default parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_cluster_parameter_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_cluster_parameter_groups)
        """

    def describe_cluster_parameters(
        self, **kwargs: Unpack[DescribeClusterParametersMessageRequestTypeDef]
    ) -> ClusterParameterGroupDetailsTypeDef:
        """
        Returns a detailed list of parameters contained within the specified Amazon
        Redshift parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_cluster_parameters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_cluster_parameters)
        """

    def describe_cluster_security_groups(
        self, **kwargs: Unpack[DescribeClusterSecurityGroupsMessageRequestTypeDef]
    ) -> ClusterSecurityGroupMessageTypeDef:
        """
        Returns information about Amazon Redshift security groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_cluster_security_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_cluster_security_groups)
        """

    def describe_cluster_snapshots(
        self, **kwargs: Unpack[DescribeClusterSnapshotsMessageRequestTypeDef]
    ) -> SnapshotMessageTypeDef:
        """
        Returns one or more snapshot objects, which contain metadata about your cluster
        snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_cluster_snapshots.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_cluster_snapshots)
        """

    def describe_cluster_subnet_groups(
        self, **kwargs: Unpack[DescribeClusterSubnetGroupsMessageRequestTypeDef]
    ) -> ClusterSubnetGroupMessageTypeDef:
        """
        Returns one or more cluster subnet group objects, which contain metadata about
        your cluster subnet groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_cluster_subnet_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_cluster_subnet_groups)
        """

    def describe_cluster_tracks(
        self, **kwargs: Unpack[DescribeClusterTracksMessageRequestTypeDef]
    ) -> TrackListMessageTypeDef:
        """
        Returns a list of all the available maintenance tracks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_cluster_tracks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_cluster_tracks)
        """

    def describe_cluster_versions(
        self, **kwargs: Unpack[DescribeClusterVersionsMessageRequestTypeDef]
    ) -> ClusterVersionsMessageTypeDef:
        """
        Returns descriptions of the available Amazon Redshift cluster versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_cluster_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_cluster_versions)
        """

    def describe_clusters(
        self, **kwargs: Unpack[DescribeClustersMessageRequestTypeDef]
    ) -> ClustersMessageTypeDef:
        """
        Returns properties of provisioned clusters including general cluster
        properties, cluster database properties, maintenance and backup properties, and
        security and access properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_clusters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_clusters)
        """

    def describe_custom_domain_associations(
        self, **kwargs: Unpack[DescribeCustomDomainAssociationsMessageRequestTypeDef]
    ) -> CustomDomainAssociationsMessageTypeDef:
        """
        Contains information about custom domain associations for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_custom_domain_associations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_custom_domain_associations)
        """

    def describe_data_shares(
        self, **kwargs: Unpack[DescribeDataSharesMessageRequestTypeDef]
    ) -> DescribeDataSharesResultTypeDef:
        """
        Shows the status of any inbound or outbound datashares available in the
        specified account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_data_shares.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_data_shares)
        """

    def describe_data_shares_for_consumer(
        self, **kwargs: Unpack[DescribeDataSharesForConsumerMessageRequestTypeDef]
    ) -> DescribeDataSharesForConsumerResultTypeDef:
        """
        Returns a list of datashares where the account identifier being called is a
        consumer account identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_data_shares_for_consumer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_data_shares_for_consumer)
        """

    def describe_data_shares_for_producer(
        self, **kwargs: Unpack[DescribeDataSharesForProducerMessageRequestTypeDef]
    ) -> DescribeDataSharesForProducerResultTypeDef:
        """
        Returns a list of datashares when the account identifier being called is a
        producer account identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_data_shares_for_producer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_data_shares_for_producer)
        """

    def describe_default_cluster_parameters(
        self, **kwargs: Unpack[DescribeDefaultClusterParametersMessageRequestTypeDef]
    ) -> DescribeDefaultClusterParametersResultTypeDef:
        """
        Returns a list of parameter settings for the specified parameter group family.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_default_cluster_parameters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_default_cluster_parameters)
        """

    def describe_endpoint_access(
        self, **kwargs: Unpack[DescribeEndpointAccessMessageRequestTypeDef]
    ) -> EndpointAccessListTypeDef:
        """
        Describes a Redshift-managed VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_endpoint_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_endpoint_access)
        """

    def describe_endpoint_authorization(
        self, **kwargs: Unpack[DescribeEndpointAuthorizationMessageRequestTypeDef]
    ) -> EndpointAuthorizationListTypeDef:
        """
        Describes an endpoint authorization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_endpoint_authorization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_endpoint_authorization)
        """

    def describe_event_categories(
        self, **kwargs: Unpack[DescribeEventCategoriesMessageRequestTypeDef]
    ) -> EventCategoriesMessageTypeDef:
        """
        Displays a list of event categories for all event source types, or for a
        specified source type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_event_categories.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_event_categories)
        """

    def describe_event_subscriptions(
        self, **kwargs: Unpack[DescribeEventSubscriptionsMessageRequestTypeDef]
    ) -> EventSubscriptionsMessageTypeDef:
        """
        Lists descriptions of all the Amazon Redshift event notification subscriptions
        for a customer account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_event_subscriptions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_event_subscriptions)
        """

    def describe_events(
        self, **kwargs: Unpack[DescribeEventsMessageRequestTypeDef]
    ) -> EventsMessageTypeDef:
        """
        Returns events related to clusters, security groups, snapshots, and parameter
        groups for the past 14 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_events)
        """

    def describe_hsm_client_certificates(
        self, **kwargs: Unpack[DescribeHsmClientCertificatesMessageRequestTypeDef]
    ) -> HsmClientCertificateMessageTypeDef:
        """
        Returns information about the specified HSM client certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_hsm_client_certificates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_hsm_client_certificates)
        """

    def describe_hsm_configurations(
        self, **kwargs: Unpack[DescribeHsmConfigurationsMessageRequestTypeDef]
    ) -> HsmConfigurationMessageTypeDef:
        """
        Returns information about the specified Amazon Redshift HSM configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_hsm_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_hsm_configurations)
        """

    def describe_inbound_integrations(
        self, **kwargs: Unpack[DescribeInboundIntegrationsMessageRequestTypeDef]
    ) -> InboundIntegrationsMessageTypeDef:
        """
        Returns a list of inbound integrations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_inbound_integrations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_inbound_integrations)
        """

    def describe_integrations(
        self, **kwargs: Unpack[DescribeIntegrationsMessageRequestTypeDef]
    ) -> IntegrationsMessageTypeDef:
        """
        Describes one or more zero-ETL or S3 event integrations with Amazon Redshift.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_integrations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_integrations)
        """

    def describe_logging_status(
        self, **kwargs: Unpack[DescribeLoggingStatusMessageRequestTypeDef]
    ) -> LoggingStatusTypeDef:
        """
        Describes whether information, such as queries and connection attempts, is
        being logged for the specified Amazon Redshift cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_logging_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_logging_status)
        """

    def describe_node_configuration_options(
        self, **kwargs: Unpack[DescribeNodeConfigurationOptionsMessageRequestTypeDef]
    ) -> NodeConfigurationOptionsMessageTypeDef:
        """
        Returns properties of possible node configurations such as node type, number of
        nodes, and disk usage for the specified action type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_node_configuration_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_node_configuration_options)
        """

    def describe_orderable_cluster_options(
        self, **kwargs: Unpack[DescribeOrderableClusterOptionsMessageRequestTypeDef]
    ) -> OrderableClusterOptionsMessageTypeDef:
        """
        Returns a list of orderable cluster options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_orderable_cluster_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_orderable_cluster_options)
        """

    def describe_partners(
        self, **kwargs: Unpack[DescribePartnersInputMessageRequestTypeDef]
    ) -> DescribePartnersOutputMessageTypeDef:
        """
        Returns information about the partner integrations defined for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_partners.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_partners)
        """

    def describe_redshift_idc_applications(
        self, **kwargs: Unpack[DescribeRedshiftIdcApplicationsMessageRequestTypeDef]
    ) -> DescribeRedshiftIdcApplicationsResultTypeDef:
        """
        Lists the Amazon Redshift IAM Identity Center applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_redshift_idc_applications.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_redshift_idc_applications)
        """

    def describe_reserved_node_exchange_status(
        self, **kwargs: Unpack[DescribeReservedNodeExchangeStatusInputMessageRequestTypeDef]
    ) -> DescribeReservedNodeExchangeStatusOutputMessageTypeDef:
        """
        Returns exchange status details and associated metadata for a reserved-node
        exchange.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_reserved_node_exchange_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_reserved_node_exchange_status)
        """

    def describe_reserved_node_offerings(
        self, **kwargs: Unpack[DescribeReservedNodeOfferingsMessageRequestTypeDef]
    ) -> ReservedNodeOfferingsMessageTypeDef:
        """
        Returns a list of the available reserved node offerings by Amazon Redshift with
        their descriptions including the node type, the fixed and recurring costs of
        reserving the node and duration the node will be reserved for you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_reserved_node_offerings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_reserved_node_offerings)
        """

    def describe_reserved_nodes(
        self, **kwargs: Unpack[DescribeReservedNodesMessageRequestTypeDef]
    ) -> ReservedNodesMessageTypeDef:
        """
        Returns the descriptions of the reserved nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_reserved_nodes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_reserved_nodes)
        """

    def describe_resize(
        self, **kwargs: Unpack[DescribeResizeMessageRequestTypeDef]
    ) -> ResizeProgressMessageTypeDef:
        """
        Returns information about the last resize operation for the specified cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_resize.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_resize)
        """

    def describe_scheduled_actions(
        self, **kwargs: Unpack[DescribeScheduledActionsMessageRequestTypeDef]
    ) -> ScheduledActionsMessageTypeDef:
        """
        Describes properties of scheduled actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_scheduled_actions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_scheduled_actions)
        """

    def describe_snapshot_copy_grants(
        self, **kwargs: Unpack[DescribeSnapshotCopyGrantsMessageRequestTypeDef]
    ) -> SnapshotCopyGrantMessageTypeDef:
        """
        Returns a list of snapshot copy grants owned by the Amazon Web Services account
        in the destination region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_snapshot_copy_grants.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_snapshot_copy_grants)
        """

    def describe_snapshot_schedules(
        self, **kwargs: Unpack[DescribeSnapshotSchedulesMessageRequestTypeDef]
    ) -> DescribeSnapshotSchedulesOutputMessageTypeDef:
        """
        Returns a list of snapshot schedules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_snapshot_schedules.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_snapshot_schedules)
        """

    def describe_storage(self) -> CustomerStorageMessageTypeDef:
        """
        Returns account level backups storage size and provisional storage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_storage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_storage)
        """

    def describe_table_restore_status(
        self, **kwargs: Unpack[DescribeTableRestoreStatusMessageRequestTypeDef]
    ) -> TableRestoreStatusMessageTypeDef:
        """
        Lists the status of one or more table restore requests made using the
        <a>RestoreTableFromClusterSnapshot</a> API action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_table_restore_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_table_restore_status)
        """

    def describe_tags(
        self, **kwargs: Unpack[DescribeTagsMessageRequestTypeDef]
    ) -> TaggedResourceListMessageTypeDef:
        """
        Returns a list of tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_tags)
        """

    def describe_usage_limits(
        self, **kwargs: Unpack[DescribeUsageLimitsMessageRequestTypeDef]
    ) -> UsageLimitListTypeDef:
        """
        Shows usage limits on a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_usage_limits.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#describe_usage_limits)
        """

    def disable_logging(
        self, **kwargs: Unpack[DisableLoggingMessageRequestTypeDef]
    ) -> LoggingStatusTypeDef:
        """
        Stops logging information, such as queries and connection attempts, for the
        specified Amazon Redshift cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/disable_logging.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#disable_logging)
        """

    def disable_snapshot_copy(
        self, **kwargs: Unpack[DisableSnapshotCopyMessageRequestTypeDef]
    ) -> DisableSnapshotCopyResultTypeDef:
        """
        Disables the automatic copying of snapshots from one region to another region
        for a specified cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/disable_snapshot_copy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#disable_snapshot_copy)
        """

    def disassociate_data_share_consumer(
        self, **kwargs: Unpack[DisassociateDataShareConsumerMessageRequestTypeDef]
    ) -> DataShareResponseTypeDef:
        """
        From a datashare consumer account, remove association for the specified
        datashare.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/disassociate_data_share_consumer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#disassociate_data_share_consumer)
        """

    def enable_logging(
        self, **kwargs: Unpack[EnableLoggingMessageRequestTypeDef]
    ) -> LoggingStatusTypeDef:
        """
        Starts logging information, such as queries and connection attempts, for the
        specified Amazon Redshift cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/enable_logging.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#enable_logging)
        """

    def enable_snapshot_copy(
        self, **kwargs: Unpack[EnableSnapshotCopyMessageRequestTypeDef]
    ) -> EnableSnapshotCopyResultTypeDef:
        """
        Enables the automatic copy of snapshots from one region to another region for a
        specified cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/enable_snapshot_copy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#enable_snapshot_copy)
        """

    def failover_primary_compute(
        self, **kwargs: Unpack[FailoverPrimaryComputeInputMessageRequestTypeDef]
    ) -> FailoverPrimaryComputeResultTypeDef:
        """
        Fails over the primary compute unit of the specified Multi-AZ cluster to
        another Availability Zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/failover_primary_compute.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#failover_primary_compute)
        """

    def get_cluster_credentials(
        self, **kwargs: Unpack[GetClusterCredentialsMessageRequestTypeDef]
    ) -> ClusterCredentialsTypeDef:
        """
        Returns a database user name and temporary password with temporary
        authorization to log on to an Amazon Redshift database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_cluster_credentials.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_cluster_credentials)
        """

    def get_cluster_credentials_with_iam(
        self, **kwargs: Unpack[GetClusterCredentialsWithIAMMessageRequestTypeDef]
    ) -> ClusterExtendedCredentialsTypeDef:
        """
        Returns a database user name and temporary password with temporary
        authorization to log in to an Amazon Redshift database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_cluster_credentials_with_iam.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_cluster_credentials_with_iam)
        """

    def get_reserved_node_exchange_configuration_options(
        self,
        **kwargs: Unpack[GetReservedNodeExchangeConfigurationOptionsInputMessageRequestTypeDef],
    ) -> GetReservedNodeExchangeConfigurationOptionsOutputMessageTypeDef:
        """
        Gets the configuration options for the reserved-node exchange.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_reserved_node_exchange_configuration_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_reserved_node_exchange_configuration_options)
        """

    def get_reserved_node_exchange_offerings(
        self, **kwargs: Unpack[GetReservedNodeExchangeOfferingsInputMessageRequestTypeDef]
    ) -> GetReservedNodeExchangeOfferingsOutputMessageTypeDef:
        """
        Returns an array of DC2 ReservedNodeOfferings that matches the payment type,
        term, and usage price of the given DC1 reserved node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_reserved_node_exchange_offerings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_reserved_node_exchange_offerings)
        """

    def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyMessageRequestTypeDef]
    ) -> GetResourcePolicyResultTypeDef:
        """
        Get the resource policy for a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_resource_policy)
        """

    def list_recommendations(
        self, **kwargs: Unpack[ListRecommendationsMessageRequestTypeDef]
    ) -> ListRecommendationsResultTypeDef:
        """
        List the Amazon Redshift Advisor recommendations for one or multiple Amazon
        Redshift clusters in an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/list_recommendations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#list_recommendations)
        """

    def modify_aqua_configuration(
        self, **kwargs: Unpack[ModifyAquaInputMessageRequestTypeDef]
    ) -> ModifyAquaOutputMessageTypeDef:
        """
        This operation is retired.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_aqua_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_aqua_configuration)
        """

    def modify_authentication_profile(
        self, **kwargs: Unpack[ModifyAuthenticationProfileMessageRequestTypeDef]
    ) -> ModifyAuthenticationProfileResultTypeDef:
        """
        Modifies an authentication profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_authentication_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_authentication_profile)
        """

    def modify_cluster(
        self, **kwargs: Unpack[ModifyClusterMessageRequestTypeDef]
    ) -> ModifyClusterResultTypeDef:
        """
        Modifies the settings for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_cluster)
        """

    def modify_cluster_db_revision(
        self, **kwargs: Unpack[ModifyClusterDbRevisionMessageRequestTypeDef]
    ) -> ModifyClusterDbRevisionResultTypeDef:
        """
        Modifies the database revision of a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_cluster_db_revision.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_cluster_db_revision)
        """

    def modify_cluster_iam_roles(
        self, **kwargs: Unpack[ModifyClusterIamRolesMessageRequestTypeDef]
    ) -> ModifyClusterIamRolesResultTypeDef:
        """
        Modifies the list of Identity and Access Management (IAM) roles that can be
        used by the cluster to access other Amazon Web Services services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_cluster_iam_roles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_cluster_iam_roles)
        """

    def modify_cluster_maintenance(
        self, **kwargs: Unpack[ModifyClusterMaintenanceMessageRequestTypeDef]
    ) -> ModifyClusterMaintenanceResultTypeDef:
        """
        Modifies the maintenance settings of a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_cluster_maintenance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_cluster_maintenance)
        """

    def modify_cluster_parameter_group(
        self, **kwargs: Unpack[ModifyClusterParameterGroupMessageRequestTypeDef]
    ) -> ClusterParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_cluster_parameter_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_cluster_parameter_group)
        """

    def modify_cluster_snapshot(
        self, **kwargs: Unpack[ModifyClusterSnapshotMessageRequestTypeDef]
    ) -> ModifyClusterSnapshotResultTypeDef:
        """
        Modifies the settings for a snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_cluster_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_cluster_snapshot)
        """

    def modify_cluster_snapshot_schedule(
        self, **kwargs: Unpack[ModifyClusterSnapshotScheduleMessageRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies a snapshot schedule for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_cluster_snapshot_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_cluster_snapshot_schedule)
        """

    def modify_cluster_subnet_group(
        self, **kwargs: Unpack[ModifyClusterSubnetGroupMessageRequestTypeDef]
    ) -> ModifyClusterSubnetGroupResultTypeDef:
        """
        Modifies a cluster subnet group to include the specified list of VPC subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_cluster_subnet_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_cluster_subnet_group)
        """

    def modify_custom_domain_association(
        self, **kwargs: Unpack[ModifyCustomDomainAssociationMessageRequestTypeDef]
    ) -> ModifyCustomDomainAssociationResultTypeDef:
        """
        Contains information for changing a custom domain association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_custom_domain_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_custom_domain_association)
        """

    def modify_endpoint_access(
        self, **kwargs: Unpack[ModifyEndpointAccessMessageRequestTypeDef]
    ) -> EndpointAccessResponseTypeDef:
        """
        Modifies a Redshift-managed VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_endpoint_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_endpoint_access)
        """

    def modify_event_subscription(
        self, **kwargs: Unpack[ModifyEventSubscriptionMessageRequestTypeDef]
    ) -> ModifyEventSubscriptionResultTypeDef:
        """
        Modifies an existing Amazon Redshift event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_event_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_event_subscription)
        """

    def modify_integration(
        self, **kwargs: Unpack[ModifyIntegrationMessageRequestTypeDef]
    ) -> IntegrationResponseTypeDef:
        """
        Modifies a zero-ETL integration or S3 event integration with Amazon Redshift.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_integration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_integration)
        """

    def modify_redshift_idc_application(
        self, **kwargs: Unpack[ModifyRedshiftIdcApplicationMessageRequestTypeDef]
    ) -> ModifyRedshiftIdcApplicationResultTypeDef:
        """
        Changes an existing Amazon Redshift IAM Identity Center application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_redshift_idc_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_redshift_idc_application)
        """

    def modify_scheduled_action(
        self, **kwargs: Unpack[ModifyScheduledActionMessageRequestTypeDef]
    ) -> ScheduledActionResponseTypeDef:
        """
        Modifies a scheduled action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_scheduled_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_scheduled_action)
        """

    def modify_snapshot_copy_retention_period(
        self, **kwargs: Unpack[ModifySnapshotCopyRetentionPeriodMessageRequestTypeDef]
    ) -> ModifySnapshotCopyRetentionPeriodResultTypeDef:
        """
        Modifies the number of days to retain snapshots in the destination Amazon Web
        Services Region after they are copied from the source Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_snapshot_copy_retention_period.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_snapshot_copy_retention_period)
        """

    def modify_snapshot_schedule(
        self, **kwargs: Unpack[ModifySnapshotScheduleMessageRequestTypeDef]
    ) -> SnapshotScheduleResponseTypeDef:
        """
        Modifies a snapshot schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_snapshot_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_snapshot_schedule)
        """

    def modify_usage_limit(
        self, **kwargs: Unpack[ModifyUsageLimitMessageRequestTypeDef]
    ) -> UsageLimitResponseTypeDef:
        """
        Modifies a usage limit in a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/modify_usage_limit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#modify_usage_limit)
        """

    def pause_cluster(
        self, **kwargs: Unpack[PauseClusterMessageRequestTypeDef]
    ) -> PauseClusterResultTypeDef:
        """
        Pauses a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/pause_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#pause_cluster)
        """

    def purchase_reserved_node_offering(
        self, **kwargs: Unpack[PurchaseReservedNodeOfferingMessageRequestTypeDef]
    ) -> PurchaseReservedNodeOfferingResultTypeDef:
        """
        Allows you to purchase reserved nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/purchase_reserved_node_offering.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#purchase_reserved_node_offering)
        """

    def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyMessageRequestTypeDef]
    ) -> PutResourcePolicyResultTypeDef:
        """
        Updates the resource policy for a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/put_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#put_resource_policy)
        """

    def reboot_cluster(
        self, **kwargs: Unpack[RebootClusterMessageRequestTypeDef]
    ) -> RebootClusterResultTypeDef:
        """
        Reboots a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/reboot_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#reboot_cluster)
        """

    def register_namespace(
        self, **kwargs: Unpack[RegisterNamespaceInputMessageRequestTypeDef]
    ) -> RegisterNamespaceOutputMessageTypeDef:
        """
        Registers a cluster or serverless namespace to the Amazon Web Services Glue
        Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/register_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#register_namespace)
        """

    def reject_data_share(
        self, **kwargs: Unpack[RejectDataShareMessageRequestTypeDef]
    ) -> DataShareResponseTypeDef:
        """
        From a datashare consumer account, rejects the specified datashare.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/reject_data_share.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#reject_data_share)
        """

    def reset_cluster_parameter_group(
        self, **kwargs: Unpack[ResetClusterParameterGroupMessageRequestTypeDef]
    ) -> ClusterParameterGroupNameMessageTypeDef:
        """
        Sets one or more parameters of the specified parameter group to their default
        values and sets the source values of the parameters to "engine-default".

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/reset_cluster_parameter_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#reset_cluster_parameter_group)
        """

    def resize_cluster(
        self, **kwargs: Unpack[ResizeClusterMessageRequestTypeDef]
    ) -> ResizeClusterResultTypeDef:
        """
        Changes the size of the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/resize_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#resize_cluster)
        """

    def restore_from_cluster_snapshot(
        self, **kwargs: Unpack[RestoreFromClusterSnapshotMessageRequestTypeDef]
    ) -> RestoreFromClusterSnapshotResultTypeDef:
        """
        Creates a new cluster from a snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/restore_from_cluster_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#restore_from_cluster_snapshot)
        """

    def restore_table_from_cluster_snapshot(
        self, **kwargs: Unpack[RestoreTableFromClusterSnapshotMessageRequestTypeDef]
    ) -> RestoreTableFromClusterSnapshotResultTypeDef:
        """
        Creates a new table from a table in an Amazon Redshift cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/restore_table_from_cluster_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#restore_table_from_cluster_snapshot)
        """

    def resume_cluster(
        self, **kwargs: Unpack[ResumeClusterMessageRequestTypeDef]
    ) -> ResumeClusterResultTypeDef:
        """
        Resumes a paused cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/resume_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#resume_cluster)
        """

    def revoke_cluster_security_group_ingress(
        self, **kwargs: Unpack[RevokeClusterSecurityGroupIngressMessageRequestTypeDef]
    ) -> RevokeClusterSecurityGroupIngressResultTypeDef:
        """
        Revokes an ingress rule in an Amazon Redshift security group for a previously
        authorized IP range or Amazon EC2 security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/revoke_cluster_security_group_ingress.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#revoke_cluster_security_group_ingress)
        """

    def revoke_endpoint_access(
        self, **kwargs: Unpack[RevokeEndpointAccessMessageRequestTypeDef]
    ) -> EndpointAuthorizationResponseTypeDef:
        """
        Revokes access to a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/revoke_endpoint_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#revoke_endpoint_access)
        """

    def revoke_snapshot_access(
        self, **kwargs: Unpack[RevokeSnapshotAccessMessageRequestTypeDef]
    ) -> RevokeSnapshotAccessResultTypeDef:
        """
        Removes the ability of the specified Amazon Web Services account to restore the
        specified snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/revoke_snapshot_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#revoke_snapshot_access)
        """

    def rotate_encryption_key(
        self, **kwargs: Unpack[RotateEncryptionKeyMessageRequestTypeDef]
    ) -> RotateEncryptionKeyResultTypeDef:
        """
        Rotates the encryption keys for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/rotate_encryption_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#rotate_encryption_key)
        """

    def update_partner_status(
        self, **kwargs: Unpack[UpdatePartnerStatusInputMessageRequestTypeDef]
    ) -> PartnerIntegrationOutputMessageTypeDef:
        """
        Updates the status of a partner integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/update_partner_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#update_partner_status)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cluster_db_revisions"]
    ) -> DescribeClusterDbRevisionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cluster_parameter_groups"]
    ) -> DescribeClusterParameterGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cluster_parameters"]
    ) -> DescribeClusterParametersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cluster_security_groups"]
    ) -> DescribeClusterSecurityGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cluster_snapshots"]
    ) -> DescribeClusterSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cluster_subnet_groups"]
    ) -> DescribeClusterSubnetGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cluster_tracks"]
    ) -> DescribeClusterTracksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cluster_versions"]
    ) -> DescribeClusterVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_clusters"]
    ) -> DescribeClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_custom_domain_associations"]
    ) -> DescribeCustomDomainAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_data_shares_for_consumer"]
    ) -> DescribeDataSharesForConsumerPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_data_shares_for_producer"]
    ) -> DescribeDataSharesForProducerPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_data_shares"]
    ) -> DescribeDataSharesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_default_cluster_parameters"]
    ) -> DescribeDefaultClusterParametersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_endpoint_access"]
    ) -> DescribeEndpointAccessPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_endpoint_authorization"]
    ) -> DescribeEndpointAuthorizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_event_subscriptions"]
    ) -> DescribeEventSubscriptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_events"]) -> DescribeEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_hsm_client_certificates"]
    ) -> DescribeHsmClientCertificatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_hsm_configurations"]
    ) -> DescribeHsmConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_inbound_integrations"]
    ) -> DescribeInboundIntegrationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_integrations"]
    ) -> DescribeIntegrationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_node_configuration_options"]
    ) -> DescribeNodeConfigurationOptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_orderable_cluster_options"]
    ) -> DescribeOrderableClusterOptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_redshift_idc_applications"]
    ) -> DescribeRedshiftIdcApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_node_exchange_status"]
    ) -> DescribeReservedNodeExchangeStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_node_offerings"]
    ) -> DescribeReservedNodeOfferingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_nodes"]
    ) -> DescribeReservedNodesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scheduled_actions"]
    ) -> DescribeScheduledActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_snapshot_copy_grants"]
    ) -> DescribeSnapshotCopyGrantsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_snapshot_schedules"]
    ) -> DescribeSnapshotSchedulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_table_restore_status"]
    ) -> DescribeTableRestoreStatusPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_tags"]) -> DescribeTagsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_usage_limits"]
    ) -> DescribeUsageLimitsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_reserved_node_exchange_configuration_options"]
    ) -> GetReservedNodeExchangeConfigurationOptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_reserved_node_exchange_offerings"]
    ) -> GetReservedNodeExchangeOfferingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recommendations"]
    ) -> ListRecommendationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["cluster_available"]) -> ClusterAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["cluster_deleted"]) -> ClusterDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["cluster_restored"]) -> ClusterRestoredWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["snapshot_available"]) -> SnapshotAvailableWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_redshift/client/#get_waiter)
        """
