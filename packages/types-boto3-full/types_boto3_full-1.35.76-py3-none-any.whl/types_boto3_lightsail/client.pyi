"""
Type annotations for lightsail service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_lightsail.client import LightsailClient

    session = Session()
    client: LightsailClient = session.client("lightsail")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    GetActiveNamesPaginator,
    GetBlueprintsPaginator,
    GetBundlesPaginator,
    GetCloudFormationStackRecordsPaginator,
    GetDiskSnapshotsPaginator,
    GetDisksPaginator,
    GetDomainsPaginator,
    GetExportSnapshotRecordsPaginator,
    GetInstanceSnapshotsPaginator,
    GetInstancesPaginator,
    GetKeyPairsPaginator,
    GetLoadBalancersPaginator,
    GetOperationsPaginator,
    GetRelationalDatabaseBlueprintsPaginator,
    GetRelationalDatabaseBundlesPaginator,
    GetRelationalDatabaseEventsPaginator,
    GetRelationalDatabaseParametersPaginator,
    GetRelationalDatabaseSnapshotsPaginator,
    GetRelationalDatabasesPaginator,
    GetStaticIpsPaginator,
)
from .type_defs import (
    AllocateStaticIpRequestRequestTypeDef,
    AllocateStaticIpResultTypeDef,
    AttachCertificateToDistributionRequestRequestTypeDef,
    AttachCertificateToDistributionResultTypeDef,
    AttachDiskRequestRequestTypeDef,
    AttachDiskResultTypeDef,
    AttachInstancesToLoadBalancerRequestRequestTypeDef,
    AttachInstancesToLoadBalancerResultTypeDef,
    AttachLoadBalancerTlsCertificateRequestRequestTypeDef,
    AttachLoadBalancerTlsCertificateResultTypeDef,
    AttachStaticIpRequestRequestTypeDef,
    AttachStaticIpResultTypeDef,
    CloseInstancePublicPortsRequestRequestTypeDef,
    CloseInstancePublicPortsResultTypeDef,
    ContainerServicesListResultTypeDef,
    CopySnapshotRequestRequestTypeDef,
    CopySnapshotResultTypeDef,
    CreateBucketAccessKeyRequestRequestTypeDef,
    CreateBucketAccessKeyResultTypeDef,
    CreateBucketRequestRequestTypeDef,
    CreateBucketResultTypeDef,
    CreateCertificateRequestRequestTypeDef,
    CreateCertificateResultTypeDef,
    CreateCloudFormationStackRequestRequestTypeDef,
    CreateCloudFormationStackResultTypeDef,
    CreateContactMethodRequestRequestTypeDef,
    CreateContactMethodResultTypeDef,
    CreateContainerServiceDeploymentRequestRequestTypeDef,
    CreateContainerServiceDeploymentResultTypeDef,
    CreateContainerServiceRegistryLoginResultTypeDef,
    CreateContainerServiceRequestRequestTypeDef,
    CreateContainerServiceResultTypeDef,
    CreateDiskFromSnapshotRequestRequestTypeDef,
    CreateDiskFromSnapshotResultTypeDef,
    CreateDiskRequestRequestTypeDef,
    CreateDiskResultTypeDef,
    CreateDiskSnapshotRequestRequestTypeDef,
    CreateDiskSnapshotResultTypeDef,
    CreateDistributionRequestRequestTypeDef,
    CreateDistributionResultTypeDef,
    CreateDomainEntryRequestRequestTypeDef,
    CreateDomainEntryResultTypeDef,
    CreateDomainRequestRequestTypeDef,
    CreateDomainResultTypeDef,
    CreateGUISessionAccessDetailsRequestRequestTypeDef,
    CreateGUISessionAccessDetailsResultTypeDef,
    CreateInstancesFromSnapshotRequestRequestTypeDef,
    CreateInstancesFromSnapshotResultTypeDef,
    CreateInstanceSnapshotRequestRequestTypeDef,
    CreateInstanceSnapshotResultTypeDef,
    CreateInstancesRequestRequestTypeDef,
    CreateInstancesResultTypeDef,
    CreateKeyPairRequestRequestTypeDef,
    CreateKeyPairResultTypeDef,
    CreateLoadBalancerRequestRequestTypeDef,
    CreateLoadBalancerResultTypeDef,
    CreateLoadBalancerTlsCertificateRequestRequestTypeDef,
    CreateLoadBalancerTlsCertificateResultTypeDef,
    CreateRelationalDatabaseFromSnapshotRequestRequestTypeDef,
    CreateRelationalDatabaseFromSnapshotResultTypeDef,
    CreateRelationalDatabaseRequestRequestTypeDef,
    CreateRelationalDatabaseResultTypeDef,
    CreateRelationalDatabaseSnapshotRequestRequestTypeDef,
    CreateRelationalDatabaseSnapshotResultTypeDef,
    DeleteAlarmRequestRequestTypeDef,
    DeleteAlarmResultTypeDef,
    DeleteAutoSnapshotRequestRequestTypeDef,
    DeleteAutoSnapshotResultTypeDef,
    DeleteBucketAccessKeyRequestRequestTypeDef,
    DeleteBucketAccessKeyResultTypeDef,
    DeleteBucketRequestRequestTypeDef,
    DeleteBucketResultTypeDef,
    DeleteCertificateRequestRequestTypeDef,
    DeleteCertificateResultTypeDef,
    DeleteContactMethodRequestRequestTypeDef,
    DeleteContactMethodResultTypeDef,
    DeleteContainerImageRequestRequestTypeDef,
    DeleteContainerServiceRequestRequestTypeDef,
    DeleteDiskRequestRequestTypeDef,
    DeleteDiskResultTypeDef,
    DeleteDiskSnapshotRequestRequestTypeDef,
    DeleteDiskSnapshotResultTypeDef,
    DeleteDistributionRequestRequestTypeDef,
    DeleteDistributionResultTypeDef,
    DeleteDomainEntryRequestRequestTypeDef,
    DeleteDomainEntryResultTypeDef,
    DeleteDomainRequestRequestTypeDef,
    DeleteDomainResultTypeDef,
    DeleteInstanceRequestRequestTypeDef,
    DeleteInstanceResultTypeDef,
    DeleteInstanceSnapshotRequestRequestTypeDef,
    DeleteInstanceSnapshotResultTypeDef,
    DeleteKeyPairRequestRequestTypeDef,
    DeleteKeyPairResultTypeDef,
    DeleteKnownHostKeysRequestRequestTypeDef,
    DeleteKnownHostKeysResultTypeDef,
    DeleteLoadBalancerRequestRequestTypeDef,
    DeleteLoadBalancerResultTypeDef,
    DeleteLoadBalancerTlsCertificateRequestRequestTypeDef,
    DeleteLoadBalancerTlsCertificateResultTypeDef,
    DeleteRelationalDatabaseRequestRequestTypeDef,
    DeleteRelationalDatabaseResultTypeDef,
    DeleteRelationalDatabaseSnapshotRequestRequestTypeDef,
    DeleteRelationalDatabaseSnapshotResultTypeDef,
    DetachCertificateFromDistributionRequestRequestTypeDef,
    DetachCertificateFromDistributionResultTypeDef,
    DetachDiskRequestRequestTypeDef,
    DetachDiskResultTypeDef,
    DetachInstancesFromLoadBalancerRequestRequestTypeDef,
    DetachInstancesFromLoadBalancerResultTypeDef,
    DetachStaticIpRequestRequestTypeDef,
    DetachStaticIpResultTypeDef,
    DisableAddOnRequestRequestTypeDef,
    DisableAddOnResultTypeDef,
    DownloadDefaultKeyPairResultTypeDef,
    EnableAddOnRequestRequestTypeDef,
    EnableAddOnResultTypeDef,
    ExportSnapshotRequestRequestTypeDef,
    ExportSnapshotResultTypeDef,
    GetActiveNamesRequestRequestTypeDef,
    GetActiveNamesResultTypeDef,
    GetAlarmsRequestRequestTypeDef,
    GetAlarmsResultTypeDef,
    GetAutoSnapshotsRequestRequestTypeDef,
    GetAutoSnapshotsResultTypeDef,
    GetBlueprintsRequestRequestTypeDef,
    GetBlueprintsResultTypeDef,
    GetBucketAccessKeysRequestRequestTypeDef,
    GetBucketAccessKeysResultTypeDef,
    GetBucketBundlesRequestRequestTypeDef,
    GetBucketBundlesResultTypeDef,
    GetBucketMetricDataRequestRequestTypeDef,
    GetBucketMetricDataResultTypeDef,
    GetBucketsRequestRequestTypeDef,
    GetBucketsResultTypeDef,
    GetBundlesRequestRequestTypeDef,
    GetBundlesResultTypeDef,
    GetCertificatesRequestRequestTypeDef,
    GetCertificatesResultTypeDef,
    GetCloudFormationStackRecordsRequestRequestTypeDef,
    GetCloudFormationStackRecordsResultTypeDef,
    GetContactMethodsRequestRequestTypeDef,
    GetContactMethodsResultTypeDef,
    GetContainerAPIMetadataResultTypeDef,
    GetContainerImagesRequestRequestTypeDef,
    GetContainerImagesResultTypeDef,
    GetContainerLogRequestRequestTypeDef,
    GetContainerLogResultTypeDef,
    GetContainerServiceDeploymentsRequestRequestTypeDef,
    GetContainerServiceDeploymentsResultTypeDef,
    GetContainerServiceMetricDataRequestRequestTypeDef,
    GetContainerServiceMetricDataResultTypeDef,
    GetContainerServicePowersResultTypeDef,
    GetContainerServicesRequestRequestTypeDef,
    GetCostEstimateRequestRequestTypeDef,
    GetCostEstimateResultTypeDef,
    GetDiskRequestRequestTypeDef,
    GetDiskResultTypeDef,
    GetDiskSnapshotRequestRequestTypeDef,
    GetDiskSnapshotResultTypeDef,
    GetDiskSnapshotsRequestRequestTypeDef,
    GetDiskSnapshotsResultTypeDef,
    GetDisksRequestRequestTypeDef,
    GetDisksResultTypeDef,
    GetDistributionBundlesResultTypeDef,
    GetDistributionLatestCacheResetRequestRequestTypeDef,
    GetDistributionLatestCacheResetResultTypeDef,
    GetDistributionMetricDataRequestRequestTypeDef,
    GetDistributionMetricDataResultTypeDef,
    GetDistributionsRequestRequestTypeDef,
    GetDistributionsResultTypeDef,
    GetDomainRequestRequestTypeDef,
    GetDomainResultTypeDef,
    GetDomainsRequestRequestTypeDef,
    GetDomainsResultTypeDef,
    GetExportSnapshotRecordsRequestRequestTypeDef,
    GetExportSnapshotRecordsResultTypeDef,
    GetInstanceAccessDetailsRequestRequestTypeDef,
    GetInstanceAccessDetailsResultTypeDef,
    GetInstanceMetricDataRequestRequestTypeDef,
    GetInstanceMetricDataResultTypeDef,
    GetInstancePortStatesRequestRequestTypeDef,
    GetInstancePortStatesResultTypeDef,
    GetInstanceRequestRequestTypeDef,
    GetInstanceResultTypeDef,
    GetInstanceSnapshotRequestRequestTypeDef,
    GetInstanceSnapshotResultTypeDef,
    GetInstanceSnapshotsRequestRequestTypeDef,
    GetInstanceSnapshotsResultTypeDef,
    GetInstancesRequestRequestTypeDef,
    GetInstancesResultTypeDef,
    GetInstanceStateRequestRequestTypeDef,
    GetInstanceStateResultTypeDef,
    GetKeyPairRequestRequestTypeDef,
    GetKeyPairResultTypeDef,
    GetKeyPairsRequestRequestTypeDef,
    GetKeyPairsResultTypeDef,
    GetLoadBalancerMetricDataRequestRequestTypeDef,
    GetLoadBalancerMetricDataResultTypeDef,
    GetLoadBalancerRequestRequestTypeDef,
    GetLoadBalancerResultTypeDef,
    GetLoadBalancersRequestRequestTypeDef,
    GetLoadBalancersResultTypeDef,
    GetLoadBalancerTlsCertificatesRequestRequestTypeDef,
    GetLoadBalancerTlsCertificatesResultTypeDef,
    GetLoadBalancerTlsPoliciesRequestRequestTypeDef,
    GetLoadBalancerTlsPoliciesResultTypeDef,
    GetOperationRequestRequestTypeDef,
    GetOperationResultTypeDef,
    GetOperationsForResourceRequestRequestTypeDef,
    GetOperationsForResourceResultTypeDef,
    GetOperationsRequestRequestTypeDef,
    GetOperationsResultTypeDef,
    GetRegionsRequestRequestTypeDef,
    GetRegionsResultTypeDef,
    GetRelationalDatabaseBlueprintsRequestRequestTypeDef,
    GetRelationalDatabaseBlueprintsResultTypeDef,
    GetRelationalDatabaseBundlesRequestRequestTypeDef,
    GetRelationalDatabaseBundlesResultTypeDef,
    GetRelationalDatabaseEventsRequestRequestTypeDef,
    GetRelationalDatabaseEventsResultTypeDef,
    GetRelationalDatabaseLogEventsRequestRequestTypeDef,
    GetRelationalDatabaseLogEventsResultTypeDef,
    GetRelationalDatabaseLogStreamsRequestRequestTypeDef,
    GetRelationalDatabaseLogStreamsResultTypeDef,
    GetRelationalDatabaseMasterUserPasswordRequestRequestTypeDef,
    GetRelationalDatabaseMasterUserPasswordResultTypeDef,
    GetRelationalDatabaseMetricDataRequestRequestTypeDef,
    GetRelationalDatabaseMetricDataResultTypeDef,
    GetRelationalDatabaseParametersRequestRequestTypeDef,
    GetRelationalDatabaseParametersResultTypeDef,
    GetRelationalDatabaseRequestRequestTypeDef,
    GetRelationalDatabaseResultTypeDef,
    GetRelationalDatabaseSnapshotRequestRequestTypeDef,
    GetRelationalDatabaseSnapshotResultTypeDef,
    GetRelationalDatabaseSnapshotsRequestRequestTypeDef,
    GetRelationalDatabaseSnapshotsResultTypeDef,
    GetRelationalDatabasesRequestRequestTypeDef,
    GetRelationalDatabasesResultTypeDef,
    GetSetupHistoryRequestRequestTypeDef,
    GetSetupHistoryResultTypeDef,
    GetStaticIpRequestRequestTypeDef,
    GetStaticIpResultTypeDef,
    GetStaticIpsRequestRequestTypeDef,
    GetStaticIpsResultTypeDef,
    ImportKeyPairRequestRequestTypeDef,
    ImportKeyPairResultTypeDef,
    IsVpcPeeredResultTypeDef,
    OpenInstancePublicPortsRequestRequestTypeDef,
    OpenInstancePublicPortsResultTypeDef,
    PeerVpcResultTypeDef,
    PutAlarmRequestRequestTypeDef,
    PutAlarmResultTypeDef,
    PutInstancePublicPortsRequestRequestTypeDef,
    PutInstancePublicPortsResultTypeDef,
    RebootInstanceRequestRequestTypeDef,
    RebootInstanceResultTypeDef,
    RebootRelationalDatabaseRequestRequestTypeDef,
    RebootRelationalDatabaseResultTypeDef,
    RegisterContainerImageRequestRequestTypeDef,
    RegisterContainerImageResultTypeDef,
    ReleaseStaticIpRequestRequestTypeDef,
    ReleaseStaticIpResultTypeDef,
    ResetDistributionCacheRequestRequestTypeDef,
    ResetDistributionCacheResultTypeDef,
    SendContactMethodVerificationRequestRequestTypeDef,
    SendContactMethodVerificationResultTypeDef,
    SetIpAddressTypeRequestRequestTypeDef,
    SetIpAddressTypeResultTypeDef,
    SetResourceAccessForBucketRequestRequestTypeDef,
    SetResourceAccessForBucketResultTypeDef,
    SetupInstanceHttpsRequestRequestTypeDef,
    SetupInstanceHttpsResultTypeDef,
    StartGUISessionRequestRequestTypeDef,
    StartGUISessionResultTypeDef,
    StartInstanceRequestRequestTypeDef,
    StartInstanceResultTypeDef,
    StartRelationalDatabaseRequestRequestTypeDef,
    StartRelationalDatabaseResultTypeDef,
    StopGUISessionRequestRequestTypeDef,
    StopGUISessionResultTypeDef,
    StopInstanceRequestRequestTypeDef,
    StopInstanceResultTypeDef,
    StopRelationalDatabaseRequestRequestTypeDef,
    StopRelationalDatabaseResultTypeDef,
    TagResourceRequestRequestTypeDef,
    TagResourceResultTypeDef,
    TestAlarmRequestRequestTypeDef,
    TestAlarmResultTypeDef,
    UnpeerVpcResultTypeDef,
    UntagResourceRequestRequestTypeDef,
    UntagResourceResultTypeDef,
    UpdateBucketBundleRequestRequestTypeDef,
    UpdateBucketBundleResultTypeDef,
    UpdateBucketRequestRequestTypeDef,
    UpdateBucketResultTypeDef,
    UpdateContainerServiceRequestRequestTypeDef,
    UpdateContainerServiceResultTypeDef,
    UpdateDistributionBundleRequestRequestTypeDef,
    UpdateDistributionBundleResultTypeDef,
    UpdateDistributionRequestRequestTypeDef,
    UpdateDistributionResultTypeDef,
    UpdateDomainEntryRequestRequestTypeDef,
    UpdateDomainEntryResultTypeDef,
    UpdateInstanceMetadataOptionsRequestRequestTypeDef,
    UpdateInstanceMetadataOptionsResultTypeDef,
    UpdateLoadBalancerAttributeRequestRequestTypeDef,
    UpdateLoadBalancerAttributeResultTypeDef,
    UpdateRelationalDatabaseParametersRequestRequestTypeDef,
    UpdateRelationalDatabaseParametersResultTypeDef,
    UpdateRelationalDatabaseRequestRequestTypeDef,
    UpdateRelationalDatabaseResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("LightsailClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AccountSetupInProgressException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    OperationFailureException: Type[BotocoreClientError]
    ServiceException: Type[BotocoreClientError]
    UnauthenticatedException: Type[BotocoreClientError]

class LightsailClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LightsailClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#close)
        """

    def allocate_static_ip(
        self, **kwargs: Unpack[AllocateStaticIpRequestRequestTypeDef]
    ) -> AllocateStaticIpResultTypeDef:
        """
        Allocates a static IP address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/allocate_static_ip.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#allocate_static_ip)
        """

    def attach_certificate_to_distribution(
        self, **kwargs: Unpack[AttachCertificateToDistributionRequestRequestTypeDef]
    ) -> AttachCertificateToDistributionResultTypeDef:
        """
        Attaches an SSL/TLS certificate to your Amazon Lightsail content delivery
        network (CDN) distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/attach_certificate_to_distribution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#attach_certificate_to_distribution)
        """

    def attach_disk(
        self, **kwargs: Unpack[AttachDiskRequestRequestTypeDef]
    ) -> AttachDiskResultTypeDef:
        """
        Attaches a block storage disk to a running or stopped Lightsail instance and
        exposes it to the instance with the specified disk name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/attach_disk.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#attach_disk)
        """

    def attach_instances_to_load_balancer(
        self, **kwargs: Unpack[AttachInstancesToLoadBalancerRequestRequestTypeDef]
    ) -> AttachInstancesToLoadBalancerResultTypeDef:
        """
        Attaches one or more Lightsail instances to a load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/attach_instances_to_load_balancer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#attach_instances_to_load_balancer)
        """

    def attach_load_balancer_tls_certificate(
        self, **kwargs: Unpack[AttachLoadBalancerTlsCertificateRequestRequestTypeDef]
    ) -> AttachLoadBalancerTlsCertificateResultTypeDef:
        """
        Attaches a Transport Layer Security (TLS) certificate to your load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/attach_load_balancer_tls_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#attach_load_balancer_tls_certificate)
        """

    def attach_static_ip(
        self, **kwargs: Unpack[AttachStaticIpRequestRequestTypeDef]
    ) -> AttachStaticIpResultTypeDef:
        """
        Attaches a static IP address to a specific Amazon Lightsail instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/attach_static_ip.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#attach_static_ip)
        """

    def close_instance_public_ports(
        self, **kwargs: Unpack[CloseInstancePublicPortsRequestRequestTypeDef]
    ) -> CloseInstancePublicPortsResultTypeDef:
        """
        Closes ports for a specific Amazon Lightsail instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/close_instance_public_ports.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#close_instance_public_ports)
        """

    def copy_snapshot(
        self, **kwargs: Unpack[CopySnapshotRequestRequestTypeDef]
    ) -> CopySnapshotResultTypeDef:
        """
        Copies a manual snapshot of an instance or disk as another manual snapshot, or
        copies an automatic snapshot of an instance or disk as a manual snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/copy_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#copy_snapshot)
        """

    def create_bucket(
        self, **kwargs: Unpack[CreateBucketRequestRequestTypeDef]
    ) -> CreateBucketResultTypeDef:
        """
        Creates an Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_bucket.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_bucket)
        """

    def create_bucket_access_key(
        self, **kwargs: Unpack[CreateBucketAccessKeyRequestRequestTypeDef]
    ) -> CreateBucketAccessKeyResultTypeDef:
        """
        Creates a new access key for the specified Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_bucket_access_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_bucket_access_key)
        """

    def create_certificate(
        self, **kwargs: Unpack[CreateCertificateRequestRequestTypeDef]
    ) -> CreateCertificateResultTypeDef:
        """
        Creates an SSL/TLS certificate for an Amazon Lightsail content delivery network
        (CDN) distribution and a container service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_certificate)
        """

    def create_cloud_formation_stack(
        self, **kwargs: Unpack[CreateCloudFormationStackRequestRequestTypeDef]
    ) -> CreateCloudFormationStackResultTypeDef:
        """
        Creates an AWS CloudFormation stack, which creates a new Amazon EC2 instance
        from an exported Amazon Lightsail snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_cloud_formation_stack.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_cloud_formation_stack)
        """

    def create_contact_method(
        self, **kwargs: Unpack[CreateContactMethodRequestRequestTypeDef]
    ) -> CreateContactMethodResultTypeDef:
        """
        Creates an email or SMS text message contact method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_contact_method.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_contact_method)
        """

    def create_container_service(
        self, **kwargs: Unpack[CreateContainerServiceRequestRequestTypeDef]
    ) -> CreateContainerServiceResultTypeDef:
        """
        Creates an Amazon Lightsail container service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_container_service.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_container_service)
        """

    def create_container_service_deployment(
        self, **kwargs: Unpack[CreateContainerServiceDeploymentRequestRequestTypeDef]
    ) -> CreateContainerServiceDeploymentResultTypeDef:
        """
        Creates a deployment for your Amazon Lightsail container service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_container_service_deployment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_container_service_deployment)
        """

    def create_container_service_registry_login(
        self,
    ) -> CreateContainerServiceRegistryLoginResultTypeDef:
        """
        Creates a temporary set of log in credentials that you can use to log in to the
        Docker process on your local machine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_container_service_registry_login.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_container_service_registry_login)
        """

    def create_disk(
        self, **kwargs: Unpack[CreateDiskRequestRequestTypeDef]
    ) -> CreateDiskResultTypeDef:
        """
        Creates a block storage disk that can be attached to an Amazon Lightsail
        instance in the same Availability Zone (<code>us-east-2a</code>).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_disk.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_disk)
        """

    def create_disk_from_snapshot(
        self, **kwargs: Unpack[CreateDiskFromSnapshotRequestRequestTypeDef]
    ) -> CreateDiskFromSnapshotResultTypeDef:
        """
        Creates a block storage disk from a manual or automatic snapshot of a disk.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_disk_from_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_disk_from_snapshot)
        """

    def create_disk_snapshot(
        self, **kwargs: Unpack[CreateDiskSnapshotRequestRequestTypeDef]
    ) -> CreateDiskSnapshotResultTypeDef:
        """
        Creates a snapshot of a block storage disk.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_disk_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_disk_snapshot)
        """

    def create_distribution(
        self, **kwargs: Unpack[CreateDistributionRequestRequestTypeDef]
    ) -> CreateDistributionResultTypeDef:
        """
        Creates an Amazon Lightsail content delivery network (CDN) distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_distribution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_distribution)
        """

    def create_domain(
        self, **kwargs: Unpack[CreateDomainRequestRequestTypeDef]
    ) -> CreateDomainResultTypeDef:
        """
        Creates a domain resource for the specified domain (example.com).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_domain)
        """

    def create_domain_entry(
        self, **kwargs: Unpack[CreateDomainEntryRequestRequestTypeDef]
    ) -> CreateDomainEntryResultTypeDef:
        """
        Creates one of the following domain name system (DNS) records in a domain DNS
        zone: Address (A), canonical name (CNAME), mail exchanger (MX), name server
        (NS), start of authority (SOA), service locator (SRV), or text (TXT).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_domain_entry.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_domain_entry)
        """

    def create_gui_session_access_details(
        self, **kwargs: Unpack[CreateGUISessionAccessDetailsRequestRequestTypeDef]
    ) -> CreateGUISessionAccessDetailsResultTypeDef:
        """
        Creates two URLs that are used to access a virtual computer's graphical user
        interface (GUI) session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_gui_session_access_details.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_gui_session_access_details)
        """

    def create_instance_snapshot(
        self, **kwargs: Unpack[CreateInstanceSnapshotRequestRequestTypeDef]
    ) -> CreateInstanceSnapshotResultTypeDef:
        """
        Creates a snapshot of a specific virtual private server, or <i>instance</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_instance_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_instance_snapshot)
        """

    def create_instances(
        self, **kwargs: Unpack[CreateInstancesRequestRequestTypeDef]
    ) -> CreateInstancesResultTypeDef:
        """
        Creates one or more Amazon Lightsail instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_instances)
        """

    def create_instances_from_snapshot(
        self, **kwargs: Unpack[CreateInstancesFromSnapshotRequestRequestTypeDef]
    ) -> CreateInstancesFromSnapshotResultTypeDef:
        """
        Creates one or more new instances from a manual or automatic snapshot of an
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_instances_from_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_instances_from_snapshot)
        """

    def create_key_pair(
        self, **kwargs: Unpack[CreateKeyPairRequestRequestTypeDef]
    ) -> CreateKeyPairResultTypeDef:
        """
        Creates a custom SSH key pair that you can use with an Amazon Lightsail
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_key_pair.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_key_pair)
        """

    def create_load_balancer(
        self, **kwargs: Unpack[CreateLoadBalancerRequestRequestTypeDef]
    ) -> CreateLoadBalancerResultTypeDef:
        """
        Creates a Lightsail load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_load_balancer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_load_balancer)
        """

    def create_load_balancer_tls_certificate(
        self, **kwargs: Unpack[CreateLoadBalancerTlsCertificateRequestRequestTypeDef]
    ) -> CreateLoadBalancerTlsCertificateResultTypeDef:
        """
        Creates an SSL/TLS certificate for an Amazon Lightsail load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_load_balancer_tls_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_load_balancer_tls_certificate)
        """

    def create_relational_database(
        self, **kwargs: Unpack[CreateRelationalDatabaseRequestRequestTypeDef]
    ) -> CreateRelationalDatabaseResultTypeDef:
        """
        Creates a new database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_relational_database.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_relational_database)
        """

    def create_relational_database_from_snapshot(
        self, **kwargs: Unpack[CreateRelationalDatabaseFromSnapshotRequestRequestTypeDef]
    ) -> CreateRelationalDatabaseFromSnapshotResultTypeDef:
        """
        Creates a new database from an existing database snapshot in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_relational_database_from_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_relational_database_from_snapshot)
        """

    def create_relational_database_snapshot(
        self, **kwargs: Unpack[CreateRelationalDatabaseSnapshotRequestRequestTypeDef]
    ) -> CreateRelationalDatabaseSnapshotResultTypeDef:
        """
        Creates a snapshot of your database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/create_relational_database_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#create_relational_database_snapshot)
        """

    def delete_alarm(
        self, **kwargs: Unpack[DeleteAlarmRequestRequestTypeDef]
    ) -> DeleteAlarmResultTypeDef:
        """
        Deletes an alarm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_alarm.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_alarm)
        """

    def delete_auto_snapshot(
        self, **kwargs: Unpack[DeleteAutoSnapshotRequestRequestTypeDef]
    ) -> DeleteAutoSnapshotResultTypeDef:
        """
        Deletes an automatic snapshot of an instance or disk.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_auto_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_auto_snapshot)
        """

    def delete_bucket(
        self, **kwargs: Unpack[DeleteBucketRequestRequestTypeDef]
    ) -> DeleteBucketResultTypeDef:
        """
        Deletes a Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_bucket.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_bucket)
        """

    def delete_bucket_access_key(
        self, **kwargs: Unpack[DeleteBucketAccessKeyRequestRequestTypeDef]
    ) -> DeleteBucketAccessKeyResultTypeDef:
        """
        Deletes an access key for the specified Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_bucket_access_key.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_bucket_access_key)
        """

    def delete_certificate(
        self, **kwargs: Unpack[DeleteCertificateRequestRequestTypeDef]
    ) -> DeleteCertificateResultTypeDef:
        """
        Deletes an SSL/TLS certificate for your Amazon Lightsail content delivery
        network (CDN) distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_certificate)
        """

    def delete_contact_method(
        self, **kwargs: Unpack[DeleteContactMethodRequestRequestTypeDef]
    ) -> DeleteContactMethodResultTypeDef:
        """
        Deletes a contact method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_contact_method.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_contact_method)
        """

    def delete_container_image(
        self, **kwargs: Unpack[DeleteContainerImageRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a container image that is registered to your Amazon Lightsail container
        service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_container_image.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_container_image)
        """

    def delete_container_service(
        self, **kwargs: Unpack[DeleteContainerServiceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes your Amazon Lightsail container service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_container_service.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_container_service)
        """

    def delete_disk(
        self, **kwargs: Unpack[DeleteDiskRequestRequestTypeDef]
    ) -> DeleteDiskResultTypeDef:
        """
        Deletes the specified block storage disk.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_disk.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_disk)
        """

    def delete_disk_snapshot(
        self, **kwargs: Unpack[DeleteDiskSnapshotRequestRequestTypeDef]
    ) -> DeleteDiskSnapshotResultTypeDef:
        """
        Deletes the specified disk snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_disk_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_disk_snapshot)
        """

    def delete_distribution(
        self, **kwargs: Unpack[DeleteDistributionRequestRequestTypeDef]
    ) -> DeleteDistributionResultTypeDef:
        """
        Deletes your Amazon Lightsail content delivery network (CDN) distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_distribution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_distribution)
        """

    def delete_domain(
        self, **kwargs: Unpack[DeleteDomainRequestRequestTypeDef]
    ) -> DeleteDomainResultTypeDef:
        """
        Deletes the specified domain recordset and all of its domain records.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_domain)
        """

    def delete_domain_entry(
        self, **kwargs: Unpack[DeleteDomainEntryRequestRequestTypeDef]
    ) -> DeleteDomainEntryResultTypeDef:
        """
        Deletes a specific domain entry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_domain_entry.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_domain_entry)
        """

    def delete_instance(
        self, **kwargs: Unpack[DeleteInstanceRequestRequestTypeDef]
    ) -> DeleteInstanceResultTypeDef:
        """
        Deletes an Amazon Lightsail instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_instance)
        """

    def delete_instance_snapshot(
        self, **kwargs: Unpack[DeleteInstanceSnapshotRequestRequestTypeDef]
    ) -> DeleteInstanceSnapshotResultTypeDef:
        """
        Deletes a specific snapshot of a virtual private server (or <i>instance</i>).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_instance_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_instance_snapshot)
        """

    def delete_key_pair(
        self, **kwargs: Unpack[DeleteKeyPairRequestRequestTypeDef]
    ) -> DeleteKeyPairResultTypeDef:
        """
        Deletes the specified key pair by removing the public key from Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_key_pair.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_key_pair)
        """

    def delete_known_host_keys(
        self, **kwargs: Unpack[DeleteKnownHostKeysRequestRequestTypeDef]
    ) -> DeleteKnownHostKeysResultTypeDef:
        """
        Deletes the known host key or certificate used by the Amazon Lightsail
        browser-based SSH or RDP clients to authenticate an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_known_host_keys.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_known_host_keys)
        """

    def delete_load_balancer(
        self, **kwargs: Unpack[DeleteLoadBalancerRequestRequestTypeDef]
    ) -> DeleteLoadBalancerResultTypeDef:
        """
        Deletes a Lightsail load balancer and all its associated SSL/TLS certificates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_load_balancer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_load_balancer)
        """

    def delete_load_balancer_tls_certificate(
        self, **kwargs: Unpack[DeleteLoadBalancerTlsCertificateRequestRequestTypeDef]
    ) -> DeleteLoadBalancerTlsCertificateResultTypeDef:
        """
        Deletes an SSL/TLS certificate associated with a Lightsail load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_load_balancer_tls_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_load_balancer_tls_certificate)
        """

    def delete_relational_database(
        self, **kwargs: Unpack[DeleteRelationalDatabaseRequestRequestTypeDef]
    ) -> DeleteRelationalDatabaseResultTypeDef:
        """
        Deletes a database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_relational_database.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_relational_database)
        """

    def delete_relational_database_snapshot(
        self, **kwargs: Unpack[DeleteRelationalDatabaseSnapshotRequestRequestTypeDef]
    ) -> DeleteRelationalDatabaseSnapshotResultTypeDef:
        """
        Deletes a database snapshot in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/delete_relational_database_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#delete_relational_database_snapshot)
        """

    def detach_certificate_from_distribution(
        self, **kwargs: Unpack[DetachCertificateFromDistributionRequestRequestTypeDef]
    ) -> DetachCertificateFromDistributionResultTypeDef:
        """
        Detaches an SSL/TLS certificate from your Amazon Lightsail content delivery
        network (CDN) distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/detach_certificate_from_distribution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#detach_certificate_from_distribution)
        """

    def detach_disk(
        self, **kwargs: Unpack[DetachDiskRequestRequestTypeDef]
    ) -> DetachDiskResultTypeDef:
        """
        Detaches a stopped block storage disk from a Lightsail instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/detach_disk.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#detach_disk)
        """

    def detach_instances_from_load_balancer(
        self, **kwargs: Unpack[DetachInstancesFromLoadBalancerRequestRequestTypeDef]
    ) -> DetachInstancesFromLoadBalancerResultTypeDef:
        """
        Detaches the specified instances from a Lightsail load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/detach_instances_from_load_balancer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#detach_instances_from_load_balancer)
        """

    def detach_static_ip(
        self, **kwargs: Unpack[DetachStaticIpRequestRequestTypeDef]
    ) -> DetachStaticIpResultTypeDef:
        """
        Detaches a static IP from the Amazon Lightsail instance to which it is attached.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/detach_static_ip.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#detach_static_ip)
        """

    def disable_add_on(
        self, **kwargs: Unpack[DisableAddOnRequestRequestTypeDef]
    ) -> DisableAddOnResultTypeDef:
        """
        Disables an add-on for an Amazon Lightsail resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/disable_add_on.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#disable_add_on)
        """

    def download_default_key_pair(self) -> DownloadDefaultKeyPairResultTypeDef:
        """
        Downloads the regional Amazon Lightsail default key pair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/download_default_key_pair.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#download_default_key_pair)
        """

    def enable_add_on(
        self, **kwargs: Unpack[EnableAddOnRequestRequestTypeDef]
    ) -> EnableAddOnResultTypeDef:
        """
        Enables or modifies an add-on for an Amazon Lightsail resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/enable_add_on.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#enable_add_on)
        """

    def export_snapshot(
        self, **kwargs: Unpack[ExportSnapshotRequestRequestTypeDef]
    ) -> ExportSnapshotResultTypeDef:
        """
        Exports an Amazon Lightsail instance or block storage disk snapshot to Amazon
        Elastic Compute Cloud (Amazon EC2).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/export_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#export_snapshot)
        """

    def get_active_names(
        self, **kwargs: Unpack[GetActiveNamesRequestRequestTypeDef]
    ) -> GetActiveNamesResultTypeDef:
        """
        Returns the names of all active (not deleted) resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_active_names.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_active_names)
        """

    def get_alarms(
        self, **kwargs: Unpack[GetAlarmsRequestRequestTypeDef]
    ) -> GetAlarmsResultTypeDef:
        """
        Returns information about the configured alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_alarms.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_alarms)
        """

    def get_auto_snapshots(
        self, **kwargs: Unpack[GetAutoSnapshotsRequestRequestTypeDef]
    ) -> GetAutoSnapshotsResultTypeDef:
        """
        Returns the available automatic snapshots for an instance or disk.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_auto_snapshots.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_auto_snapshots)
        """

    def get_blueprints(
        self, **kwargs: Unpack[GetBlueprintsRequestRequestTypeDef]
    ) -> GetBlueprintsResultTypeDef:
        """
        Returns the list of available instance images, or <i>blueprints</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_blueprints.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_blueprints)
        """

    def get_bucket_access_keys(
        self, **kwargs: Unpack[GetBucketAccessKeysRequestRequestTypeDef]
    ) -> GetBucketAccessKeysResultTypeDef:
        """
        Returns the existing access key IDs for the specified Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_bucket_access_keys.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_bucket_access_keys)
        """

    def get_bucket_bundles(
        self, **kwargs: Unpack[GetBucketBundlesRequestRequestTypeDef]
    ) -> GetBucketBundlesResultTypeDef:
        """
        Returns the bundles that you can apply to a Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_bucket_bundles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_bucket_bundles)
        """

    def get_bucket_metric_data(
        self, **kwargs: Unpack[GetBucketMetricDataRequestRequestTypeDef]
    ) -> GetBucketMetricDataResultTypeDef:
        """
        Returns the data points of a specific metric for an Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_bucket_metric_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_bucket_metric_data)
        """

    def get_buckets(
        self, **kwargs: Unpack[GetBucketsRequestRequestTypeDef]
    ) -> GetBucketsResultTypeDef:
        """
        Returns information about one or more Amazon Lightsail buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_buckets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_buckets)
        """

    def get_bundles(
        self, **kwargs: Unpack[GetBundlesRequestRequestTypeDef]
    ) -> GetBundlesResultTypeDef:
        """
        Returns the bundles that you can apply to an Amazon Lightsail instance when you
        create it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_bundles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_bundles)
        """

    def get_certificates(
        self, **kwargs: Unpack[GetCertificatesRequestRequestTypeDef]
    ) -> GetCertificatesResultTypeDef:
        """
        Returns information about one or more Amazon Lightsail SSL/TLS certificates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_certificates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_certificates)
        """

    def get_cloud_formation_stack_records(
        self, **kwargs: Unpack[GetCloudFormationStackRecordsRequestRequestTypeDef]
    ) -> GetCloudFormationStackRecordsResultTypeDef:
        """
        Returns the CloudFormation stack record created as a result of the <code>create
        cloud formation stack</code> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_cloud_formation_stack_records.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_cloud_formation_stack_records)
        """

    def get_contact_methods(
        self, **kwargs: Unpack[GetContactMethodsRequestRequestTypeDef]
    ) -> GetContactMethodsResultTypeDef:
        """
        Returns information about the configured contact methods.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_contact_methods.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_contact_methods)
        """

    def get_container_api_metadata(self) -> GetContainerAPIMetadataResultTypeDef:
        """
        Returns information about Amazon Lightsail containers, such as the current
        version of the Lightsail Control (lightsailctl) plugin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_container_api_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_container_api_metadata)
        """

    def get_container_images(
        self, **kwargs: Unpack[GetContainerImagesRequestRequestTypeDef]
    ) -> GetContainerImagesResultTypeDef:
        """
        Returns the container images that are registered to your Amazon Lightsail
        container service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_container_images.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_container_images)
        """

    def get_container_log(
        self, **kwargs: Unpack[GetContainerLogRequestRequestTypeDef]
    ) -> GetContainerLogResultTypeDef:
        """
        Returns the log events of a container of your Amazon Lightsail container
        service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_container_log.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_container_log)
        """

    def get_container_service_deployments(
        self, **kwargs: Unpack[GetContainerServiceDeploymentsRequestRequestTypeDef]
    ) -> GetContainerServiceDeploymentsResultTypeDef:
        """
        Returns the deployments for your Amazon Lightsail container service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_container_service_deployments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_container_service_deployments)
        """

    def get_container_service_metric_data(
        self, **kwargs: Unpack[GetContainerServiceMetricDataRequestRequestTypeDef]
    ) -> GetContainerServiceMetricDataResultTypeDef:
        """
        Returns the data points of a specific metric of your Amazon Lightsail container
        service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_container_service_metric_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_container_service_metric_data)
        """

    def get_container_service_powers(self) -> GetContainerServicePowersResultTypeDef:
        """
        Returns the list of powers that can be specified for your Amazon Lightsail
        container services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_container_service_powers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_container_service_powers)
        """

    def get_container_services(
        self, **kwargs: Unpack[GetContainerServicesRequestRequestTypeDef]
    ) -> ContainerServicesListResultTypeDef:
        """
        Returns information about one or more of your Amazon Lightsail container
        services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_container_services.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_container_services)
        """

    def get_cost_estimate(
        self, **kwargs: Unpack[GetCostEstimateRequestRequestTypeDef]
    ) -> GetCostEstimateResultTypeDef:
        """
        Retrieves information about the cost estimate for a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_cost_estimate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_cost_estimate)
        """

    def get_disk(self, **kwargs: Unpack[GetDiskRequestRequestTypeDef]) -> GetDiskResultTypeDef:
        """
        Returns information about a specific block storage disk.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_disk.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_disk)
        """

    def get_disk_snapshot(
        self, **kwargs: Unpack[GetDiskSnapshotRequestRequestTypeDef]
    ) -> GetDiskSnapshotResultTypeDef:
        """
        Returns information about a specific block storage disk snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_disk_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_disk_snapshot)
        """

    def get_disk_snapshots(
        self, **kwargs: Unpack[GetDiskSnapshotsRequestRequestTypeDef]
    ) -> GetDiskSnapshotsResultTypeDef:
        """
        Returns information about all block storage disk snapshots in your AWS account
        and region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_disk_snapshots.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_disk_snapshots)
        """

    def get_disks(self, **kwargs: Unpack[GetDisksRequestRequestTypeDef]) -> GetDisksResultTypeDef:
        """
        Returns information about all block storage disks in your AWS account and
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_disks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_disks)
        """

    def get_distribution_bundles(self) -> GetDistributionBundlesResultTypeDef:
        """
        Returns the bundles that can be applied to your Amazon Lightsail content
        delivery network (CDN) distributions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_distribution_bundles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_distribution_bundles)
        """

    def get_distribution_latest_cache_reset(
        self, **kwargs: Unpack[GetDistributionLatestCacheResetRequestRequestTypeDef]
    ) -> GetDistributionLatestCacheResetResultTypeDef:
        """
        Returns the timestamp and status of the last cache reset of a specific Amazon
        Lightsail content delivery network (CDN) distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_distribution_latest_cache_reset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_distribution_latest_cache_reset)
        """

    def get_distribution_metric_data(
        self, **kwargs: Unpack[GetDistributionMetricDataRequestRequestTypeDef]
    ) -> GetDistributionMetricDataResultTypeDef:
        """
        Returns the data points of a specific metric for an Amazon Lightsail content
        delivery network (CDN) distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_distribution_metric_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_distribution_metric_data)
        """

    def get_distributions(
        self, **kwargs: Unpack[GetDistributionsRequestRequestTypeDef]
    ) -> GetDistributionsResultTypeDef:
        """
        Returns information about one or more of your Amazon Lightsail content delivery
        network (CDN) distributions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_distributions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_distributions)
        """

    def get_domain(
        self, **kwargs: Unpack[GetDomainRequestRequestTypeDef]
    ) -> GetDomainResultTypeDef:
        """
        Returns information about a specific domain recordset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_domain.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_domain)
        """

    def get_domains(
        self, **kwargs: Unpack[GetDomainsRequestRequestTypeDef]
    ) -> GetDomainsResultTypeDef:
        """
        Returns a list of all domains in the user's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_domains.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_domains)
        """

    def get_export_snapshot_records(
        self, **kwargs: Unpack[GetExportSnapshotRecordsRequestRequestTypeDef]
    ) -> GetExportSnapshotRecordsResultTypeDef:
        """
        Returns all export snapshot records created as a result of the <code>export
        snapshot</code> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_export_snapshot_records.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_export_snapshot_records)
        """

    def get_instance(
        self, **kwargs: Unpack[GetInstanceRequestRequestTypeDef]
    ) -> GetInstanceResultTypeDef:
        """
        Returns information about a specific Amazon Lightsail instance, which is a
        virtual private server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_instance)
        """

    def get_instance_access_details(
        self, **kwargs: Unpack[GetInstanceAccessDetailsRequestRequestTypeDef]
    ) -> GetInstanceAccessDetailsResultTypeDef:
        """
        Returns temporary SSH keys you can use to connect to a specific virtual private
        server, or <i>instance</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_instance_access_details.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_instance_access_details)
        """

    def get_instance_metric_data(
        self, **kwargs: Unpack[GetInstanceMetricDataRequestRequestTypeDef]
    ) -> GetInstanceMetricDataResultTypeDef:
        """
        Returns the data points for the specified Amazon Lightsail instance metric,
        given an instance name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_instance_metric_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_instance_metric_data)
        """

    def get_instance_port_states(
        self, **kwargs: Unpack[GetInstancePortStatesRequestRequestTypeDef]
    ) -> GetInstancePortStatesResultTypeDef:
        """
        Returns the firewall port states for a specific Amazon Lightsail instance, the
        IP addresses allowed to connect to the instance through the ports, and the
        protocol.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_instance_port_states.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_instance_port_states)
        """

    def get_instance_snapshot(
        self, **kwargs: Unpack[GetInstanceSnapshotRequestRequestTypeDef]
    ) -> GetInstanceSnapshotResultTypeDef:
        """
        Returns information about a specific instance snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_instance_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_instance_snapshot)
        """

    def get_instance_snapshots(
        self, **kwargs: Unpack[GetInstanceSnapshotsRequestRequestTypeDef]
    ) -> GetInstanceSnapshotsResultTypeDef:
        """
        Returns all instance snapshots for the user's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_instance_snapshots.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_instance_snapshots)
        """

    def get_instance_state(
        self, **kwargs: Unpack[GetInstanceStateRequestRequestTypeDef]
    ) -> GetInstanceStateResultTypeDef:
        """
        Returns the state of a specific instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_instance_state.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_instance_state)
        """

    def get_instances(
        self, **kwargs: Unpack[GetInstancesRequestRequestTypeDef]
    ) -> GetInstancesResultTypeDef:
        """
        Returns information about all Amazon Lightsail virtual private servers, or
        <i>instances</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_instances)
        """

    def get_key_pair(
        self, **kwargs: Unpack[GetKeyPairRequestRequestTypeDef]
    ) -> GetKeyPairResultTypeDef:
        """
        Returns information about a specific key pair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_key_pair.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_key_pair)
        """

    def get_key_pairs(
        self, **kwargs: Unpack[GetKeyPairsRequestRequestTypeDef]
    ) -> GetKeyPairsResultTypeDef:
        """
        Returns information about all key pairs in the user's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_key_pairs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_key_pairs)
        """

    def get_load_balancer(
        self, **kwargs: Unpack[GetLoadBalancerRequestRequestTypeDef]
    ) -> GetLoadBalancerResultTypeDef:
        """
        Returns information about the specified Lightsail load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_load_balancer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_load_balancer)
        """

    def get_load_balancer_metric_data(
        self, **kwargs: Unpack[GetLoadBalancerMetricDataRequestRequestTypeDef]
    ) -> GetLoadBalancerMetricDataResultTypeDef:
        """
        Returns information about health metrics for your Lightsail load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_load_balancer_metric_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_load_balancer_metric_data)
        """

    def get_load_balancer_tls_certificates(
        self, **kwargs: Unpack[GetLoadBalancerTlsCertificatesRequestRequestTypeDef]
    ) -> GetLoadBalancerTlsCertificatesResultTypeDef:
        """
        Returns information about the TLS certificates that are associated with the
        specified Lightsail load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_load_balancer_tls_certificates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_load_balancer_tls_certificates)
        """

    def get_load_balancer_tls_policies(
        self, **kwargs: Unpack[GetLoadBalancerTlsPoliciesRequestRequestTypeDef]
    ) -> GetLoadBalancerTlsPoliciesResultTypeDef:
        """
        Returns a list of TLS security policies that you can apply to Lightsail load
        balancers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_load_balancer_tls_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_load_balancer_tls_policies)
        """

    def get_load_balancers(
        self, **kwargs: Unpack[GetLoadBalancersRequestRequestTypeDef]
    ) -> GetLoadBalancersResultTypeDef:
        """
        Returns information about all load balancers in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_load_balancers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_load_balancers)
        """

    def get_operation(
        self, **kwargs: Unpack[GetOperationRequestRequestTypeDef]
    ) -> GetOperationResultTypeDef:
        """
        Returns information about a specific operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_operation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_operation)
        """

    def get_operations(
        self, **kwargs: Unpack[GetOperationsRequestRequestTypeDef]
    ) -> GetOperationsResultTypeDef:
        """
        Returns information about all operations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_operations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_operations)
        """

    def get_operations_for_resource(
        self, **kwargs: Unpack[GetOperationsForResourceRequestRequestTypeDef]
    ) -> GetOperationsForResourceResultTypeDef:
        """
        Gets operations for a specific resource (an instance or a static IP).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_operations_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_operations_for_resource)
        """

    def get_regions(
        self, **kwargs: Unpack[GetRegionsRequestRequestTypeDef]
    ) -> GetRegionsResultTypeDef:
        """
        Returns a list of all valid regions for Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_regions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_regions)
        """

    def get_relational_database(
        self, **kwargs: Unpack[GetRelationalDatabaseRequestRequestTypeDef]
    ) -> GetRelationalDatabaseResultTypeDef:
        """
        Returns information about a specific database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_relational_database.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_relational_database)
        """

    def get_relational_database_blueprints(
        self, **kwargs: Unpack[GetRelationalDatabaseBlueprintsRequestRequestTypeDef]
    ) -> GetRelationalDatabaseBlueprintsResultTypeDef:
        """
        Returns a list of available database blueprints in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_relational_database_blueprints.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_relational_database_blueprints)
        """

    def get_relational_database_bundles(
        self, **kwargs: Unpack[GetRelationalDatabaseBundlesRequestRequestTypeDef]
    ) -> GetRelationalDatabaseBundlesResultTypeDef:
        """
        Returns the list of bundles that are available in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_relational_database_bundles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_relational_database_bundles)
        """

    def get_relational_database_events(
        self, **kwargs: Unpack[GetRelationalDatabaseEventsRequestRequestTypeDef]
    ) -> GetRelationalDatabaseEventsResultTypeDef:
        """
        Returns a list of events for a specific database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_relational_database_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_relational_database_events)
        """

    def get_relational_database_log_events(
        self, **kwargs: Unpack[GetRelationalDatabaseLogEventsRequestRequestTypeDef]
    ) -> GetRelationalDatabaseLogEventsResultTypeDef:
        """
        Returns a list of log events for a database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_relational_database_log_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_relational_database_log_events)
        """

    def get_relational_database_log_streams(
        self, **kwargs: Unpack[GetRelationalDatabaseLogStreamsRequestRequestTypeDef]
    ) -> GetRelationalDatabaseLogStreamsResultTypeDef:
        """
        Returns a list of available log streams for a specific database in Amazon
        Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_relational_database_log_streams.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_relational_database_log_streams)
        """

    def get_relational_database_master_user_password(
        self, **kwargs: Unpack[GetRelationalDatabaseMasterUserPasswordRequestRequestTypeDef]
    ) -> GetRelationalDatabaseMasterUserPasswordResultTypeDef:
        """
        Returns the current, previous, or pending versions of the master user password
        for a Lightsail database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_relational_database_master_user_password.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_relational_database_master_user_password)
        """

    def get_relational_database_metric_data(
        self, **kwargs: Unpack[GetRelationalDatabaseMetricDataRequestRequestTypeDef]
    ) -> GetRelationalDatabaseMetricDataResultTypeDef:
        """
        Returns the data points of the specified metric for a database in Amazon
        Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_relational_database_metric_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_relational_database_metric_data)
        """

    def get_relational_database_parameters(
        self, **kwargs: Unpack[GetRelationalDatabaseParametersRequestRequestTypeDef]
    ) -> GetRelationalDatabaseParametersResultTypeDef:
        """
        Returns all of the runtime parameters offered by the underlying database
        software, or engine, for a specific database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_relational_database_parameters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_relational_database_parameters)
        """

    def get_relational_database_snapshot(
        self, **kwargs: Unpack[GetRelationalDatabaseSnapshotRequestRequestTypeDef]
    ) -> GetRelationalDatabaseSnapshotResultTypeDef:
        """
        Returns information about a specific database snapshot in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_relational_database_snapshot.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_relational_database_snapshot)
        """

    def get_relational_database_snapshots(
        self, **kwargs: Unpack[GetRelationalDatabaseSnapshotsRequestRequestTypeDef]
    ) -> GetRelationalDatabaseSnapshotsResultTypeDef:
        """
        Returns information about all of your database snapshots in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_relational_database_snapshots.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_relational_database_snapshots)
        """

    def get_relational_databases(
        self, **kwargs: Unpack[GetRelationalDatabasesRequestRequestTypeDef]
    ) -> GetRelationalDatabasesResultTypeDef:
        """
        Returns information about all of your databases in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_relational_databases.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_relational_databases)
        """

    def get_setup_history(
        self, **kwargs: Unpack[GetSetupHistoryRequestRequestTypeDef]
    ) -> GetSetupHistoryResultTypeDef:
        """
        Returns detailed information for five of the most recent
        <code>SetupInstanceHttps</code> requests that were ran on the target instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_setup_history.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_setup_history)
        """

    def get_static_ip(
        self, **kwargs: Unpack[GetStaticIpRequestRequestTypeDef]
    ) -> GetStaticIpResultTypeDef:
        """
        Returns information about an Amazon Lightsail static IP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_static_ip.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_static_ip)
        """

    def get_static_ips(
        self, **kwargs: Unpack[GetStaticIpsRequestRequestTypeDef]
    ) -> GetStaticIpsResultTypeDef:
        """
        Returns information about all static IPs in the user's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_static_ips.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_static_ips)
        """

    def import_key_pair(
        self, **kwargs: Unpack[ImportKeyPairRequestRequestTypeDef]
    ) -> ImportKeyPairResultTypeDef:
        """
        Imports a public SSH key from a specific key pair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/import_key_pair.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#import_key_pair)
        """

    def is_vpc_peered(self) -> IsVpcPeeredResultTypeDef:
        """
        Returns a Boolean value indicating whether your Lightsail VPC is peered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/is_vpc_peered.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#is_vpc_peered)
        """

    def open_instance_public_ports(
        self, **kwargs: Unpack[OpenInstancePublicPortsRequestRequestTypeDef]
    ) -> OpenInstancePublicPortsResultTypeDef:
        """
        Opens ports for a specific Amazon Lightsail instance, and specifies the IP
        addresses allowed to connect to the instance through the ports, and the
        protocol.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/open_instance_public_ports.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#open_instance_public_ports)
        """

    def peer_vpc(self) -> PeerVpcResultTypeDef:
        """
        Peers the Lightsail VPC with the user's default VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/peer_vpc.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#peer_vpc)
        """

    def put_alarm(self, **kwargs: Unpack[PutAlarmRequestRequestTypeDef]) -> PutAlarmResultTypeDef:
        """
        Creates or updates an alarm, and associates it with the specified metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/put_alarm.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#put_alarm)
        """

    def put_instance_public_ports(
        self, **kwargs: Unpack[PutInstancePublicPortsRequestRequestTypeDef]
    ) -> PutInstancePublicPortsResultTypeDef:
        """
        Opens ports for a specific Amazon Lightsail instance, and specifies the IP
        addresses allowed to connect to the instance through the ports, and the
        protocol.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/put_instance_public_ports.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#put_instance_public_ports)
        """

    def reboot_instance(
        self, **kwargs: Unpack[RebootInstanceRequestRequestTypeDef]
    ) -> RebootInstanceResultTypeDef:
        """
        Restarts a specific instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/reboot_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#reboot_instance)
        """

    def reboot_relational_database(
        self, **kwargs: Unpack[RebootRelationalDatabaseRequestRequestTypeDef]
    ) -> RebootRelationalDatabaseResultTypeDef:
        """
        Restarts a specific database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/reboot_relational_database.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#reboot_relational_database)
        """

    def register_container_image(
        self, **kwargs: Unpack[RegisterContainerImageRequestRequestTypeDef]
    ) -> RegisterContainerImageResultTypeDef:
        """
        Registers a container image to your Amazon Lightsail container service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/register_container_image.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#register_container_image)
        """

    def release_static_ip(
        self, **kwargs: Unpack[ReleaseStaticIpRequestRequestTypeDef]
    ) -> ReleaseStaticIpResultTypeDef:
        """
        Deletes a specific static IP from your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/release_static_ip.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#release_static_ip)
        """

    def reset_distribution_cache(
        self, **kwargs: Unpack[ResetDistributionCacheRequestRequestTypeDef]
    ) -> ResetDistributionCacheResultTypeDef:
        """
        Deletes currently cached content from your Amazon Lightsail content delivery
        network (CDN) distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/reset_distribution_cache.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#reset_distribution_cache)
        """

    def send_contact_method_verification(
        self, **kwargs: Unpack[SendContactMethodVerificationRequestRequestTypeDef]
    ) -> SendContactMethodVerificationResultTypeDef:
        """
        Sends a verification request to an email contact method to ensure it's owned by
        the requester.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/send_contact_method_verification.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#send_contact_method_verification)
        """

    def set_ip_address_type(
        self, **kwargs: Unpack[SetIpAddressTypeRequestRequestTypeDef]
    ) -> SetIpAddressTypeResultTypeDef:
        """
        Sets the IP address type for an Amazon Lightsail resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/set_ip_address_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#set_ip_address_type)
        """

    def set_resource_access_for_bucket(
        self, **kwargs: Unpack[SetResourceAccessForBucketRequestRequestTypeDef]
    ) -> SetResourceAccessForBucketResultTypeDef:
        """
        Sets the Amazon Lightsail resources that can access the specified Lightsail
        bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/set_resource_access_for_bucket.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#set_resource_access_for_bucket)
        """

    def setup_instance_https(
        self, **kwargs: Unpack[SetupInstanceHttpsRequestRequestTypeDef]
    ) -> SetupInstanceHttpsResultTypeDef:
        """
        Creates an SSL/TLS certificate that secures traffic for your website.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/setup_instance_https.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#setup_instance_https)
        """

    def start_gui_session(
        self, **kwargs: Unpack[StartGUISessionRequestRequestTypeDef]
    ) -> StartGUISessionResultTypeDef:
        """
        Initiates a graphical user interface (GUI) session that's used to access a
        virtual computer's operating system and application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/start_gui_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#start_gui_session)
        """

    def start_instance(
        self, **kwargs: Unpack[StartInstanceRequestRequestTypeDef]
    ) -> StartInstanceResultTypeDef:
        """
        Starts a specific Amazon Lightsail instance from a stopped state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/start_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#start_instance)
        """

    def start_relational_database(
        self, **kwargs: Unpack[StartRelationalDatabaseRequestRequestTypeDef]
    ) -> StartRelationalDatabaseResultTypeDef:
        """
        Starts a specific database from a stopped state in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/start_relational_database.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#start_relational_database)
        """

    def stop_gui_session(
        self, **kwargs: Unpack[StopGUISessionRequestRequestTypeDef]
    ) -> StopGUISessionResultTypeDef:
        """
        Terminates a web-based NICE DCV session that's used to access a virtual
        computer's operating system or application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/stop_gui_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#stop_gui_session)
        """

    def stop_instance(
        self, **kwargs: Unpack[StopInstanceRequestRequestTypeDef]
    ) -> StopInstanceResultTypeDef:
        """
        Stops a specific Amazon Lightsail instance that is currently running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/stop_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#stop_instance)
        """

    def stop_relational_database(
        self, **kwargs: Unpack[StopRelationalDatabaseRequestRequestTypeDef]
    ) -> StopRelationalDatabaseResultTypeDef:
        """
        Stops a specific database that is currently running in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/stop_relational_database.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#stop_relational_database)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> TagResourceResultTypeDef:
        """
        Adds one or more tags to the specified Amazon Lightsail resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#tag_resource)
        """

    def test_alarm(
        self, **kwargs: Unpack[TestAlarmRequestRequestTypeDef]
    ) -> TestAlarmResultTypeDef:
        """
        Tests an alarm by displaying a banner on the Amazon Lightsail console.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/test_alarm.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#test_alarm)
        """

    def unpeer_vpc(self) -> UnpeerVpcResultTypeDef:
        """
        Unpeers the Lightsail VPC from the user's default VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/unpeer_vpc.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#unpeer_vpc)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> UntagResourceResultTypeDef:
        """
        Deletes the specified set of tag keys and their values from the specified
        Amazon Lightsail resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#untag_resource)
        """

    def update_bucket(
        self, **kwargs: Unpack[UpdateBucketRequestRequestTypeDef]
    ) -> UpdateBucketResultTypeDef:
        """
        Updates an existing Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/update_bucket.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#update_bucket)
        """

    def update_bucket_bundle(
        self, **kwargs: Unpack[UpdateBucketBundleRequestRequestTypeDef]
    ) -> UpdateBucketBundleResultTypeDef:
        """
        Updates the bundle, or storage plan, of an existing Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/update_bucket_bundle.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#update_bucket_bundle)
        """

    def update_container_service(
        self, **kwargs: Unpack[UpdateContainerServiceRequestRequestTypeDef]
    ) -> UpdateContainerServiceResultTypeDef:
        """
        Updates the configuration of your Amazon Lightsail container service, such as
        its power, scale, and public domain names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/update_container_service.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#update_container_service)
        """

    def update_distribution(
        self, **kwargs: Unpack[UpdateDistributionRequestRequestTypeDef]
    ) -> UpdateDistributionResultTypeDef:
        """
        Updates an existing Amazon Lightsail content delivery network (CDN)
        distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/update_distribution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#update_distribution)
        """

    def update_distribution_bundle(
        self, **kwargs: Unpack[UpdateDistributionBundleRequestRequestTypeDef]
    ) -> UpdateDistributionBundleResultTypeDef:
        """
        Updates the bundle of your Amazon Lightsail content delivery network (CDN)
        distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/update_distribution_bundle.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#update_distribution_bundle)
        """

    def update_domain_entry(
        self, **kwargs: Unpack[UpdateDomainEntryRequestRequestTypeDef]
    ) -> UpdateDomainEntryResultTypeDef:
        """
        Updates a domain recordset after it is created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/update_domain_entry.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#update_domain_entry)
        """

    def update_instance_metadata_options(
        self, **kwargs: Unpack[UpdateInstanceMetadataOptionsRequestRequestTypeDef]
    ) -> UpdateInstanceMetadataOptionsResultTypeDef:
        """
        Modifies the Amazon Lightsail instance metadata parameters on a running or
        stopped instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/update_instance_metadata_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#update_instance_metadata_options)
        """

    def update_load_balancer_attribute(
        self, **kwargs: Unpack[UpdateLoadBalancerAttributeRequestRequestTypeDef]
    ) -> UpdateLoadBalancerAttributeResultTypeDef:
        """
        Updates the specified attribute for a load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/update_load_balancer_attribute.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#update_load_balancer_attribute)
        """

    def update_relational_database(
        self, **kwargs: Unpack[UpdateRelationalDatabaseRequestRequestTypeDef]
    ) -> UpdateRelationalDatabaseResultTypeDef:
        """
        Allows the update of one or more attributes of a database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/update_relational_database.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#update_relational_database)
        """

    def update_relational_database_parameters(
        self, **kwargs: Unpack[UpdateRelationalDatabaseParametersRequestRequestTypeDef]
    ) -> UpdateRelationalDatabaseParametersResultTypeDef:
        """
        Allows the update of one or more parameters of a database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/update_relational_database_parameters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#update_relational_database_parameters)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_active_names"]) -> GetActiveNamesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_blueprints"]) -> GetBlueprintsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_bundles"]) -> GetBundlesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_cloud_formation_stack_records"]
    ) -> GetCloudFormationStackRecordsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_disk_snapshots"]
    ) -> GetDiskSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_disks"]) -> GetDisksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_domains"]) -> GetDomainsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_export_snapshot_records"]
    ) -> GetExportSnapshotRecordsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_instance_snapshots"]
    ) -> GetInstanceSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_instances"]) -> GetInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_key_pairs"]) -> GetKeyPairsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_load_balancers"]
    ) -> GetLoadBalancersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_operations"]) -> GetOperationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_database_blueprints"]
    ) -> GetRelationalDatabaseBlueprintsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_database_bundles"]
    ) -> GetRelationalDatabaseBundlesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_database_events"]
    ) -> GetRelationalDatabaseEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_database_parameters"]
    ) -> GetRelationalDatabaseParametersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_database_snapshots"]
    ) -> GetRelationalDatabaseSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_databases"]
    ) -> GetRelationalDatabasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_static_ips"]) -> GetStaticIpsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lightsail/client/#get_paginator)
        """
