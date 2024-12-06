"""
Type annotations for opsworks service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_opsworks.client import OpsWorksClient

    session = Session()
    client: OpsWorksClient = session.client("opsworks")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import DescribeEcsClustersPaginator
from .type_defs import (
    AssignInstanceRequestRequestTypeDef,
    AssignVolumeRequestRequestTypeDef,
    AssociateElasticIpRequestRequestTypeDef,
    AttachElasticLoadBalancerRequestRequestTypeDef,
    CloneStackRequestRequestTypeDef,
    CloneStackResultTypeDef,
    CreateAppRequestRequestTypeDef,
    CreateAppResultTypeDef,
    CreateDeploymentRequestRequestTypeDef,
    CreateDeploymentResultTypeDef,
    CreateInstanceRequestRequestTypeDef,
    CreateInstanceResultTypeDef,
    CreateLayerRequestRequestTypeDef,
    CreateLayerResultTypeDef,
    CreateStackRequestRequestTypeDef,
    CreateStackResultTypeDef,
    CreateUserProfileRequestRequestTypeDef,
    CreateUserProfileResultTypeDef,
    DeleteAppRequestRequestTypeDef,
    DeleteInstanceRequestRequestTypeDef,
    DeleteLayerRequestRequestTypeDef,
    DeleteStackRequestRequestTypeDef,
    DeleteUserProfileRequestRequestTypeDef,
    DeregisterEcsClusterRequestRequestTypeDef,
    DeregisterElasticIpRequestRequestTypeDef,
    DeregisterInstanceRequestRequestTypeDef,
    DeregisterRdsDbInstanceRequestRequestTypeDef,
    DeregisterVolumeRequestRequestTypeDef,
    DescribeAgentVersionsRequestRequestTypeDef,
    DescribeAgentVersionsResultTypeDef,
    DescribeAppsRequestRequestTypeDef,
    DescribeAppsResultTypeDef,
    DescribeCommandsRequestRequestTypeDef,
    DescribeCommandsResultTypeDef,
    DescribeDeploymentsRequestRequestTypeDef,
    DescribeDeploymentsResultTypeDef,
    DescribeEcsClustersRequestRequestTypeDef,
    DescribeEcsClustersResultTypeDef,
    DescribeElasticIpsRequestRequestTypeDef,
    DescribeElasticIpsResultTypeDef,
    DescribeElasticLoadBalancersRequestRequestTypeDef,
    DescribeElasticLoadBalancersResultTypeDef,
    DescribeInstancesRequestRequestTypeDef,
    DescribeInstancesResultTypeDef,
    DescribeLayersRequestRequestTypeDef,
    DescribeLayersResultTypeDef,
    DescribeLoadBasedAutoScalingRequestRequestTypeDef,
    DescribeLoadBasedAutoScalingResultTypeDef,
    DescribeMyUserProfileResultTypeDef,
    DescribeOperatingSystemsResponseTypeDef,
    DescribePermissionsRequestRequestTypeDef,
    DescribePermissionsResultTypeDef,
    DescribeRaidArraysRequestRequestTypeDef,
    DescribeRaidArraysResultTypeDef,
    DescribeRdsDbInstancesRequestRequestTypeDef,
    DescribeRdsDbInstancesResultTypeDef,
    DescribeServiceErrorsRequestRequestTypeDef,
    DescribeServiceErrorsResultTypeDef,
    DescribeStackProvisioningParametersRequestRequestTypeDef,
    DescribeStackProvisioningParametersResultTypeDef,
    DescribeStacksRequestRequestTypeDef,
    DescribeStacksResultTypeDef,
    DescribeStackSummaryRequestRequestTypeDef,
    DescribeStackSummaryResultTypeDef,
    DescribeTimeBasedAutoScalingRequestRequestTypeDef,
    DescribeTimeBasedAutoScalingResultTypeDef,
    DescribeUserProfilesRequestRequestTypeDef,
    DescribeUserProfilesResultTypeDef,
    DescribeVolumesRequestRequestTypeDef,
    DescribeVolumesResultTypeDef,
    DetachElasticLoadBalancerRequestRequestTypeDef,
    DisassociateElasticIpRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetHostnameSuggestionRequestRequestTypeDef,
    GetHostnameSuggestionResultTypeDef,
    GrantAccessRequestRequestTypeDef,
    GrantAccessResultTypeDef,
    ListTagsRequestRequestTypeDef,
    ListTagsResultTypeDef,
    RebootInstanceRequestRequestTypeDef,
    RegisterEcsClusterRequestRequestTypeDef,
    RegisterEcsClusterResultTypeDef,
    RegisterElasticIpRequestRequestTypeDef,
    RegisterElasticIpResultTypeDef,
    RegisterInstanceRequestRequestTypeDef,
    RegisterInstanceResultTypeDef,
    RegisterRdsDbInstanceRequestRequestTypeDef,
    RegisterVolumeRequestRequestTypeDef,
    RegisterVolumeResultTypeDef,
    SetLoadBasedAutoScalingRequestRequestTypeDef,
    SetPermissionRequestRequestTypeDef,
    SetTimeBasedAutoScalingRequestRequestTypeDef,
    StartInstanceRequestRequestTypeDef,
    StartStackRequestRequestTypeDef,
    StopInstanceRequestRequestTypeDef,
    StopStackRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UnassignInstanceRequestRequestTypeDef,
    UnassignVolumeRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAppRequestRequestTypeDef,
    UpdateElasticIpRequestRequestTypeDef,
    UpdateInstanceRequestRequestTypeDef,
    UpdateLayerRequestRequestTypeDef,
    UpdateMyUserProfileRequestRequestTypeDef,
    UpdateRdsDbInstanceRequestRequestTypeDef,
    UpdateStackRequestRequestTypeDef,
    UpdateUserProfileRequestRequestTypeDef,
    UpdateVolumeRequestRequestTypeDef,
)
from .waiter import (
    AppExistsWaiter,
    DeploymentSuccessfulWaiter,
    InstanceOnlineWaiter,
    InstanceRegisteredWaiter,
    InstanceStoppedWaiter,
    InstanceTerminatedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("OpsWorksClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class OpsWorksClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OpsWorksClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#close)
        """

    def assign_instance(
        self, **kwargs: Unpack[AssignInstanceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assign a registered instance to a layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/assign_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#assign_instance)
        """

    def assign_volume(
        self, **kwargs: Unpack[AssignVolumeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assigns one of the stack's registered Amazon EBS volumes to a specified
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/assign_volume.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#assign_volume)
        """

    def associate_elastic_ip(
        self, **kwargs: Unpack[AssociateElasticIpRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates one of the stack's registered Elastic IP addresses with a specified
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/associate_elastic_ip.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#associate_elastic_ip)
        """

    def attach_elastic_load_balancer(
        self, **kwargs: Unpack[AttachElasticLoadBalancerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches an Elastic Load Balancing load balancer to a specified layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/attach_elastic_load_balancer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#attach_elastic_load_balancer)
        """

    def clone_stack(
        self, **kwargs: Unpack[CloneStackRequestRequestTypeDef]
    ) -> CloneStackResultTypeDef:
        """
        Creates a clone of a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/clone_stack.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#clone_stack)
        """

    def create_app(
        self, **kwargs: Unpack[CreateAppRequestRequestTypeDef]
    ) -> CreateAppResultTypeDef:
        """
        Creates an app for a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/create_app.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#create_app)
        """

    def create_deployment(
        self, **kwargs: Unpack[CreateDeploymentRequestRequestTypeDef]
    ) -> CreateDeploymentResultTypeDef:
        """
        Runs deployment or stack commands.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/create_deployment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#create_deployment)
        """

    def create_instance(
        self, **kwargs: Unpack[CreateInstanceRequestRequestTypeDef]
    ) -> CreateInstanceResultTypeDef:
        """
        Creates an instance in a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/create_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#create_instance)
        """

    def create_layer(
        self, **kwargs: Unpack[CreateLayerRequestRequestTypeDef]
    ) -> CreateLayerResultTypeDef:
        """
        Creates a layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/create_layer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#create_layer)
        """

    def create_stack(
        self, **kwargs: Unpack[CreateStackRequestRequestTypeDef]
    ) -> CreateStackResultTypeDef:
        """
        Creates a new stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/create_stack.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#create_stack)
        """

    def create_user_profile(
        self, **kwargs: Unpack[CreateUserProfileRequestRequestTypeDef]
    ) -> CreateUserProfileResultTypeDef:
        """
        Creates a new user profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/create_user_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#create_user_profile)
        """

    def delete_app(
        self, **kwargs: Unpack[DeleteAppRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/delete_app.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#delete_app)
        """

    def delete_instance(
        self, **kwargs: Unpack[DeleteInstanceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified instance, which terminates the associated Amazon EC2
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/delete_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#delete_instance)
        """

    def delete_layer(
        self, **kwargs: Unpack[DeleteLayerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/delete_layer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#delete_layer)
        """

    def delete_stack(
        self, **kwargs: Unpack[DeleteStackRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/delete_stack.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#delete_stack)
        """

    def delete_user_profile(
        self, **kwargs: Unpack[DeleteUserProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a user profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/delete_user_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#delete_user_profile)
        """

    def deregister_ecs_cluster(
        self, **kwargs: Unpack[DeregisterEcsClusterRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters a specified Amazon ECS cluster from a stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/deregister_ecs_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#deregister_ecs_cluster)
        """

    def deregister_elastic_ip(
        self, **kwargs: Unpack[DeregisterElasticIpRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters a specified Elastic IP address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/deregister_elastic_ip.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#deregister_elastic_ip)
        """

    def deregister_instance(
        self, **kwargs: Unpack[DeregisterInstanceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deregister an instance from OpsWorks Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/deregister_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#deregister_instance)
        """

    def deregister_rds_db_instance(
        self, **kwargs: Unpack[DeregisterRdsDbInstanceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters an Amazon RDS instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/deregister_rds_db_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#deregister_rds_db_instance)
        """

    def deregister_volume(
        self, **kwargs: Unpack[DeregisterVolumeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters an Amazon EBS volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/deregister_volume.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#deregister_volume)
        """

    def describe_agent_versions(
        self, **kwargs: Unpack[DescribeAgentVersionsRequestRequestTypeDef]
    ) -> DescribeAgentVersionsResultTypeDef:
        """
        Describes the available OpsWorks Stacks agent versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_agent_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_agent_versions)
        """

    def describe_apps(
        self, **kwargs: Unpack[DescribeAppsRequestRequestTypeDef]
    ) -> DescribeAppsResultTypeDef:
        """
        Requests a description of a specified set of apps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_apps.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_apps)
        """

    def describe_commands(
        self, **kwargs: Unpack[DescribeCommandsRequestRequestTypeDef]
    ) -> DescribeCommandsResultTypeDef:
        """
        Describes the results of specified commands.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_commands.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_commands)
        """

    def describe_deployments(
        self, **kwargs: Unpack[DescribeDeploymentsRequestRequestTypeDef]
    ) -> DescribeDeploymentsResultTypeDef:
        """
        Requests a description of a specified set of deployments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_deployments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_deployments)
        """

    def describe_ecs_clusters(
        self, **kwargs: Unpack[DescribeEcsClustersRequestRequestTypeDef]
    ) -> DescribeEcsClustersResultTypeDef:
        """
        Describes Amazon ECS clusters that are registered with a stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_ecs_clusters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_ecs_clusters)
        """

    def describe_elastic_ips(
        self, **kwargs: Unpack[DescribeElasticIpsRequestRequestTypeDef]
    ) -> DescribeElasticIpsResultTypeDef:
        """
        Describes <a
        href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html">Elastic
        IP addresses</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_elastic_ips.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_elastic_ips)
        """

    def describe_elastic_load_balancers(
        self, **kwargs: Unpack[DescribeElasticLoadBalancersRequestRequestTypeDef]
    ) -> DescribeElasticLoadBalancersResultTypeDef:
        """
        Describes a stack's Elastic Load Balancing instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_elastic_load_balancers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_elastic_load_balancers)
        """

    def describe_instances(
        self, **kwargs: Unpack[DescribeInstancesRequestRequestTypeDef]
    ) -> DescribeInstancesResultTypeDef:
        """
        Requests a description of a set of instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_instances)
        """

    def describe_layers(
        self, **kwargs: Unpack[DescribeLayersRequestRequestTypeDef]
    ) -> DescribeLayersResultTypeDef:
        """
        Requests a description of one or more layers in a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_layers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_layers)
        """

    def describe_load_based_auto_scaling(
        self, **kwargs: Unpack[DescribeLoadBasedAutoScalingRequestRequestTypeDef]
    ) -> DescribeLoadBasedAutoScalingResultTypeDef:
        """
        Describes load-based auto scaling configurations for specified layers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_load_based_auto_scaling.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_load_based_auto_scaling)
        """

    def describe_my_user_profile(self) -> DescribeMyUserProfileResultTypeDef:
        """
        Describes a user's SSH information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_my_user_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_my_user_profile)
        """

    def describe_operating_systems(self) -> DescribeOperatingSystemsResponseTypeDef:
        """
        Describes the operating systems that are supported by OpsWorks Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_operating_systems.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_operating_systems)
        """

    def describe_permissions(
        self, **kwargs: Unpack[DescribePermissionsRequestRequestTypeDef]
    ) -> DescribePermissionsResultTypeDef:
        """
        Describes the permissions for a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_permissions)
        """

    def describe_raid_arrays(
        self, **kwargs: Unpack[DescribeRaidArraysRequestRequestTypeDef]
    ) -> DescribeRaidArraysResultTypeDef:
        """
        Describe an instance's RAID arrays.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_raid_arrays.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_raid_arrays)
        """

    def describe_rds_db_instances(
        self, **kwargs: Unpack[DescribeRdsDbInstancesRequestRequestTypeDef]
    ) -> DescribeRdsDbInstancesResultTypeDef:
        """
        Describes Amazon RDS instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_rds_db_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_rds_db_instances)
        """

    def describe_service_errors(
        self, **kwargs: Unpack[DescribeServiceErrorsRequestRequestTypeDef]
    ) -> DescribeServiceErrorsResultTypeDef:
        """
        Describes OpsWorks Stacks service errors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_service_errors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_service_errors)
        """

    def describe_stack_provisioning_parameters(
        self, **kwargs: Unpack[DescribeStackProvisioningParametersRequestRequestTypeDef]
    ) -> DescribeStackProvisioningParametersResultTypeDef:
        """
        Requests a description of a stack's provisioning parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_stack_provisioning_parameters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_stack_provisioning_parameters)
        """

    def describe_stack_summary(
        self, **kwargs: Unpack[DescribeStackSummaryRequestRequestTypeDef]
    ) -> DescribeStackSummaryResultTypeDef:
        """
        Describes the number of layers and apps in a specified stack, and the number of
        instances in each state, such as <code>running_setup</code> or
        <code>online</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_stack_summary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_stack_summary)
        """

    def describe_stacks(
        self, **kwargs: Unpack[DescribeStacksRequestRequestTypeDef]
    ) -> DescribeStacksResultTypeDef:
        """
        Requests a description of one or more stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_stacks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_stacks)
        """

    def describe_time_based_auto_scaling(
        self, **kwargs: Unpack[DescribeTimeBasedAutoScalingRequestRequestTypeDef]
    ) -> DescribeTimeBasedAutoScalingResultTypeDef:
        """
        Describes time-based auto scaling configurations for specified instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_time_based_auto_scaling.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_time_based_auto_scaling)
        """

    def describe_user_profiles(
        self, **kwargs: Unpack[DescribeUserProfilesRequestRequestTypeDef]
    ) -> DescribeUserProfilesResultTypeDef:
        """
        Describe specified users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_user_profiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_user_profiles)
        """

    def describe_volumes(
        self, **kwargs: Unpack[DescribeVolumesRequestRequestTypeDef]
    ) -> DescribeVolumesResultTypeDef:
        """
        Describes an instance's Amazon EBS volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/describe_volumes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#describe_volumes)
        """

    def detach_elastic_load_balancer(
        self, **kwargs: Unpack[DetachElasticLoadBalancerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Detaches a specified Elastic Load Balancing instance from its layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/detach_elastic_load_balancer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#detach_elastic_load_balancer)
        """

    def disassociate_elastic_ip(
        self, **kwargs: Unpack[DisassociateElasticIpRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates an Elastic IP address from its instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/disassociate_elastic_ip.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#disassociate_elastic_ip)
        """

    def get_hostname_suggestion(
        self, **kwargs: Unpack[GetHostnameSuggestionRequestRequestTypeDef]
    ) -> GetHostnameSuggestionResultTypeDef:
        """
        Gets a generated host name for the specified layer, based on the current host
        name theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/get_hostname_suggestion.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#get_hostname_suggestion)
        """

    def grant_access(
        self, **kwargs: Unpack[GrantAccessRequestRequestTypeDef]
    ) -> GrantAccessResultTypeDef:
        """
        This action can be used only with Windows stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/grant_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#grant_access)
        """

    def list_tags(self, **kwargs: Unpack[ListTagsRequestRequestTypeDef]) -> ListTagsResultTypeDef:
        """
        Returns a list of tags that are applied to the specified stack or layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/list_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#list_tags)
        """

    def reboot_instance(
        self, **kwargs: Unpack[RebootInstanceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Reboots a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/reboot_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#reboot_instance)
        """

    def register_ecs_cluster(
        self, **kwargs: Unpack[RegisterEcsClusterRequestRequestTypeDef]
    ) -> RegisterEcsClusterResultTypeDef:
        """
        Registers a specified Amazon ECS cluster with a stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/register_ecs_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#register_ecs_cluster)
        """

    def register_elastic_ip(
        self, **kwargs: Unpack[RegisterElasticIpRequestRequestTypeDef]
    ) -> RegisterElasticIpResultTypeDef:
        """
        Registers an Elastic IP address with a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/register_elastic_ip.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#register_elastic_ip)
        """

    def register_instance(
        self, **kwargs: Unpack[RegisterInstanceRequestRequestTypeDef]
    ) -> RegisterInstanceResultTypeDef:
        """
        Registers instances that were created outside of OpsWorks Stacks with a
        specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/register_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#register_instance)
        """

    def register_rds_db_instance(
        self, **kwargs: Unpack[RegisterRdsDbInstanceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Registers an Amazon RDS instance with a stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/register_rds_db_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#register_rds_db_instance)
        """

    def register_volume(
        self, **kwargs: Unpack[RegisterVolumeRequestRequestTypeDef]
    ) -> RegisterVolumeResultTypeDef:
        """
        Registers an Amazon EBS volume with a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/register_volume.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#register_volume)
        """

    def set_load_based_auto_scaling(
        self, **kwargs: Unpack[SetLoadBasedAutoScalingRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specify the load-based auto scaling configuration for a specified layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/set_load_based_auto_scaling.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#set_load_based_auto_scaling)
        """

    def set_permission(
        self, **kwargs: Unpack[SetPermissionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specifies a user's permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/set_permission.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#set_permission)
        """

    def set_time_based_auto_scaling(
        self, **kwargs: Unpack[SetTimeBasedAutoScalingRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specify the time-based auto scaling configuration for a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/set_time_based_auto_scaling.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#set_time_based_auto_scaling)
        """

    def start_instance(
        self, **kwargs: Unpack[StartInstanceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/start_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#start_instance)
        """

    def start_stack(
        self, **kwargs: Unpack[StartStackRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a stack's instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/start_stack.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#start_stack)
        """

    def stop_instance(
        self, **kwargs: Unpack[StopInstanceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/stop_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#stop_instance)
        """

    def stop_stack(
        self, **kwargs: Unpack[StopStackRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/stop_stack.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#stop_stack)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Apply cost-allocation tags to a specified stack or layer in OpsWorks Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#tag_resource)
        """

    def unassign_instance(
        self, **kwargs: Unpack[UnassignInstanceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Unassigns a registered instance from all layers that are using the instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/unassign_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#unassign_instance)
        """

    def unassign_volume(
        self, **kwargs: Unpack[UnassignVolumeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Unassigns an assigned Amazon EBS volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/unassign_volume.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#unassign_volume)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags from a specified stack or layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#untag_resource)
        """

    def update_app(
        self, **kwargs: Unpack[UpdateAppRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a specified app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_app.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#update_app)
        """

    def update_elastic_ip(
        self, **kwargs: Unpack[UpdateElasticIpRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a registered Elastic IP address's name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_elastic_ip.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#update_elastic_ip)
        """

    def update_instance(
        self, **kwargs: Unpack[UpdateInstanceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#update_instance)
        """

    def update_layer(
        self, **kwargs: Unpack[UpdateLayerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a specified layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_layer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#update_layer)
        """

    def update_my_user_profile(
        self, **kwargs: Unpack[UpdateMyUserProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a user's SSH public key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_my_user_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#update_my_user_profile)
        """

    def update_rds_db_instance(
        self, **kwargs: Unpack[UpdateRdsDbInstanceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an Amazon RDS instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_rds_db_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#update_rds_db_instance)
        """

    def update_stack(
        self, **kwargs: Unpack[UpdateStackRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_stack.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#update_stack)
        """

    def update_user_profile(
        self, **kwargs: Unpack[UpdateUserProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a specified user profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_user_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#update_user_profile)
        """

    def update_volume(
        self, **kwargs: Unpack[UpdateVolumeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an Amazon EBS volume's name or mount point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/update_volume.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#update_volume)
        """

    def get_paginator(
        self, operation_name: Literal["describe_ecs_clusters"]
    ) -> DescribeEcsClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["app_exists"]) -> AppExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["deployment_successful"]
    ) -> DeploymentSuccessfulWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["instance_online"]) -> InstanceOnlineWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["instance_registered"]) -> InstanceRegisteredWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["instance_stopped"]) -> InstanceStoppedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["instance_terminated"]) -> InstanceTerminatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opsworks/client/#get_waiter)
        """
