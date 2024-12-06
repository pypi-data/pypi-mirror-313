"""
Type annotations for elb service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_elb.client import ElasticLoadBalancingClient

    session = Session()
    client: ElasticLoadBalancingClient = session.client("elb")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import DescribeAccountLimitsPaginator, DescribeLoadBalancersPaginator
from .type_defs import (
    AddAvailabilityZonesInputRequestTypeDef,
    AddAvailabilityZonesOutputTypeDef,
    AddTagsInputRequestTypeDef,
    ApplySecurityGroupsToLoadBalancerInputRequestTypeDef,
    ApplySecurityGroupsToLoadBalancerOutputTypeDef,
    AttachLoadBalancerToSubnetsInputRequestTypeDef,
    AttachLoadBalancerToSubnetsOutputTypeDef,
    ConfigureHealthCheckInputRequestTypeDef,
    ConfigureHealthCheckOutputTypeDef,
    CreateAccessPointInputRequestTypeDef,
    CreateAccessPointOutputTypeDef,
    CreateAppCookieStickinessPolicyInputRequestTypeDef,
    CreateLBCookieStickinessPolicyInputRequestTypeDef,
    CreateLoadBalancerListenerInputRequestTypeDef,
    CreateLoadBalancerPolicyInputRequestTypeDef,
    DeleteAccessPointInputRequestTypeDef,
    DeleteLoadBalancerListenerInputRequestTypeDef,
    DeleteLoadBalancerPolicyInputRequestTypeDef,
    DeregisterEndPointsInputRequestTypeDef,
    DeregisterEndPointsOutputTypeDef,
    DescribeAccessPointsInputRequestTypeDef,
    DescribeAccessPointsOutputTypeDef,
    DescribeAccountLimitsInputRequestTypeDef,
    DescribeAccountLimitsOutputTypeDef,
    DescribeEndPointStateInputRequestTypeDef,
    DescribeEndPointStateOutputTypeDef,
    DescribeLoadBalancerAttributesInputRequestTypeDef,
    DescribeLoadBalancerAttributesOutputTypeDef,
    DescribeLoadBalancerPoliciesInputRequestTypeDef,
    DescribeLoadBalancerPoliciesOutputTypeDef,
    DescribeLoadBalancerPolicyTypesInputRequestTypeDef,
    DescribeLoadBalancerPolicyTypesOutputTypeDef,
    DescribeTagsInputRequestTypeDef,
    DescribeTagsOutputTypeDef,
    DetachLoadBalancerFromSubnetsInputRequestTypeDef,
    DetachLoadBalancerFromSubnetsOutputTypeDef,
    ModifyLoadBalancerAttributesInputRequestTypeDef,
    ModifyLoadBalancerAttributesOutputTypeDef,
    RegisterEndPointsInputRequestTypeDef,
    RegisterEndPointsOutputTypeDef,
    RemoveAvailabilityZonesInputRequestTypeDef,
    RemoveAvailabilityZonesOutputTypeDef,
    RemoveTagsInputRequestTypeDef,
    SetLoadBalancerListenerSSLCertificateInputRequestTypeDef,
    SetLoadBalancerPoliciesForBackendServerInputRequestTypeDef,
    SetLoadBalancerPoliciesOfListenerInputRequestTypeDef,
)
from .waiter import AnyInstanceInServiceWaiter, InstanceDeregisteredWaiter, InstanceInServiceWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ElasticLoadBalancingClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessPointNotFoundException: Type[BotocoreClientError]
    CertificateNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DependencyThrottleException: Type[BotocoreClientError]
    DuplicateAccessPointNameException: Type[BotocoreClientError]
    DuplicateListenerException: Type[BotocoreClientError]
    DuplicatePolicyNameException: Type[BotocoreClientError]
    DuplicateTagKeysException: Type[BotocoreClientError]
    InvalidConfigurationRequestException: Type[BotocoreClientError]
    InvalidEndPointException: Type[BotocoreClientError]
    InvalidSchemeException: Type[BotocoreClientError]
    InvalidSecurityGroupException: Type[BotocoreClientError]
    InvalidSubnetException: Type[BotocoreClientError]
    ListenerNotFoundException: Type[BotocoreClientError]
    LoadBalancerAttributeNotFoundException: Type[BotocoreClientError]
    OperationNotPermittedException: Type[BotocoreClientError]
    PolicyNotFoundException: Type[BotocoreClientError]
    PolicyTypeNotFoundException: Type[BotocoreClientError]
    SubnetNotFoundException: Type[BotocoreClientError]
    TooManyAccessPointsException: Type[BotocoreClientError]
    TooManyPoliciesException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnsupportedProtocolException: Type[BotocoreClientError]

class ElasticLoadBalancingClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElasticLoadBalancingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#close)
        """

    def add_tags(self, **kwargs: Unpack[AddTagsInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/add_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#add_tags)
        """

    def apply_security_groups_to_load_balancer(
        self, **kwargs: Unpack[ApplySecurityGroupsToLoadBalancerInputRequestTypeDef]
    ) -> ApplySecurityGroupsToLoadBalancerOutputTypeDef:
        """
        Associates one or more security groups with your load balancer in a virtual
        private cloud (VPC).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/apply_security_groups_to_load_balancer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#apply_security_groups_to_load_balancer)
        """

    def attach_load_balancer_to_subnets(
        self, **kwargs: Unpack[AttachLoadBalancerToSubnetsInputRequestTypeDef]
    ) -> AttachLoadBalancerToSubnetsOutputTypeDef:
        """
        Adds one or more subnets to the set of configured subnets for the specified
        load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/attach_load_balancer_to_subnets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#attach_load_balancer_to_subnets)
        """

    def configure_health_check(
        self, **kwargs: Unpack[ConfigureHealthCheckInputRequestTypeDef]
    ) -> ConfigureHealthCheckOutputTypeDef:
        """
        Specifies the health check settings to use when evaluating the health state of
        your EC2 instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/configure_health_check.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#configure_health_check)
        """

    def create_app_cookie_stickiness_policy(
        self, **kwargs: Unpack[CreateAppCookieStickinessPolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Generates a stickiness policy with sticky session lifetimes that follow that of
        an application-generated cookie.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/create_app_cookie_stickiness_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#create_app_cookie_stickiness_policy)
        """

    def create_lb_cookie_stickiness_policy(
        self, **kwargs: Unpack[CreateLBCookieStickinessPolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Generates a stickiness policy with sticky session lifetimes controlled by the
        lifetime of the browser (user-agent) or a specified expiration period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/create_lb_cookie_stickiness_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#create_lb_cookie_stickiness_policy)
        """

    def create_load_balancer(
        self, **kwargs: Unpack[CreateAccessPointInputRequestTypeDef]
    ) -> CreateAccessPointOutputTypeDef:
        """
        Creates a Classic Load Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/create_load_balancer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#create_load_balancer)
        """

    def create_load_balancer_listeners(
        self, **kwargs: Unpack[CreateLoadBalancerListenerInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates one or more listeners for the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/create_load_balancer_listeners.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#create_load_balancer_listeners)
        """

    def create_load_balancer_policy(
        self, **kwargs: Unpack[CreateLoadBalancerPolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a policy with the specified attributes for the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/create_load_balancer_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#create_load_balancer_policy)
        """

    def delete_load_balancer(
        self, **kwargs: Unpack[DeleteAccessPointInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/delete_load_balancer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#delete_load_balancer)
        """

    def delete_load_balancer_listeners(
        self, **kwargs: Unpack[DeleteLoadBalancerListenerInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified listeners from the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/delete_load_balancer_listeners.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#delete_load_balancer_listeners)
        """

    def delete_load_balancer_policy(
        self, **kwargs: Unpack[DeleteLoadBalancerPolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified policy from the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/delete_load_balancer_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#delete_load_balancer_policy)
        """

    def deregister_instances_from_load_balancer(
        self, **kwargs: Unpack[DeregisterEndPointsInputRequestTypeDef]
    ) -> DeregisterEndPointsOutputTypeDef:
        """
        Deregisters the specified instances from the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/deregister_instances_from_load_balancer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#deregister_instances_from_load_balancer)
        """

    def describe_account_limits(
        self, **kwargs: Unpack[DescribeAccountLimitsInputRequestTypeDef]
    ) -> DescribeAccountLimitsOutputTypeDef:
        """
        Describes the current Elastic Load Balancing resource limits for your AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/describe_account_limits.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#describe_account_limits)
        """

    def describe_instance_health(
        self, **kwargs: Unpack[DescribeEndPointStateInputRequestTypeDef]
    ) -> DescribeEndPointStateOutputTypeDef:
        """
        Describes the state of the specified instances with respect to the specified
        load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/describe_instance_health.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#describe_instance_health)
        """

    def describe_load_balancer_attributes(
        self, **kwargs: Unpack[DescribeLoadBalancerAttributesInputRequestTypeDef]
    ) -> DescribeLoadBalancerAttributesOutputTypeDef:
        """
        Describes the attributes for the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/describe_load_balancer_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#describe_load_balancer_attributes)
        """

    def describe_load_balancer_policies(
        self, **kwargs: Unpack[DescribeLoadBalancerPoliciesInputRequestTypeDef]
    ) -> DescribeLoadBalancerPoliciesOutputTypeDef:
        """
        Describes the specified policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/describe_load_balancer_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#describe_load_balancer_policies)
        """

    def describe_load_balancer_policy_types(
        self, **kwargs: Unpack[DescribeLoadBalancerPolicyTypesInputRequestTypeDef]
    ) -> DescribeLoadBalancerPolicyTypesOutputTypeDef:
        """
        Describes the specified load balancer policy types or all load balancer policy
        types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/describe_load_balancer_policy_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#describe_load_balancer_policy_types)
        """

    def describe_load_balancers(
        self, **kwargs: Unpack[DescribeAccessPointsInputRequestTypeDef]
    ) -> DescribeAccessPointsOutputTypeDef:
        """
        Describes the specified the load balancers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/describe_load_balancers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#describe_load_balancers)
        """

    def describe_tags(
        self, **kwargs: Unpack[DescribeTagsInputRequestTypeDef]
    ) -> DescribeTagsOutputTypeDef:
        """
        Describes the tags associated with the specified load balancers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/describe_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#describe_tags)
        """

    def detach_load_balancer_from_subnets(
        self, **kwargs: Unpack[DetachLoadBalancerFromSubnetsInputRequestTypeDef]
    ) -> DetachLoadBalancerFromSubnetsOutputTypeDef:
        """
        Removes the specified subnets from the set of configured subnets for the load
        balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/detach_load_balancer_from_subnets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#detach_load_balancer_from_subnets)
        """

    def disable_availability_zones_for_load_balancer(
        self, **kwargs: Unpack[RemoveAvailabilityZonesInputRequestTypeDef]
    ) -> RemoveAvailabilityZonesOutputTypeDef:
        """
        Removes the specified Availability Zones from the set of Availability Zones for
        the specified load balancer in EC2-Classic or a default VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/disable_availability_zones_for_load_balancer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#disable_availability_zones_for_load_balancer)
        """

    def enable_availability_zones_for_load_balancer(
        self, **kwargs: Unpack[AddAvailabilityZonesInputRequestTypeDef]
    ) -> AddAvailabilityZonesOutputTypeDef:
        """
        Adds the specified Availability Zones to the set of Availability Zones for the
        specified load balancer in EC2-Classic or a default VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/enable_availability_zones_for_load_balancer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#enable_availability_zones_for_load_balancer)
        """

    def modify_load_balancer_attributes(
        self, **kwargs: Unpack[ModifyLoadBalancerAttributesInputRequestTypeDef]
    ) -> ModifyLoadBalancerAttributesOutputTypeDef:
        """
        Modifies the attributes of the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/modify_load_balancer_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#modify_load_balancer_attributes)
        """

    def register_instances_with_load_balancer(
        self, **kwargs: Unpack[RegisterEndPointsInputRequestTypeDef]
    ) -> RegisterEndPointsOutputTypeDef:
        """
        Adds the specified instances to the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/register_instances_with_load_balancer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#register_instances_with_load_balancer)
        """

    def remove_tags(self, **kwargs: Unpack[RemoveTagsInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/remove_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#remove_tags)
        """

    def set_load_balancer_listener_ssl_certificate(
        self, **kwargs: Unpack[SetLoadBalancerListenerSSLCertificateInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets the certificate that terminates the specified listener's SSL connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/set_load_balancer_listener_ssl_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#set_load_balancer_listener_ssl_certificate)
        """

    def set_load_balancer_policies_for_backend_server(
        self, **kwargs: Unpack[SetLoadBalancerPoliciesForBackendServerInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Replaces the set of policies associated with the specified port on which the
        EC2 instance is listening with a new set of policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/set_load_balancer_policies_for_backend_server.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#set_load_balancer_policies_for_backend_server)
        """

    def set_load_balancer_policies_of_listener(
        self, **kwargs: Unpack[SetLoadBalancerPoliciesOfListenerInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Replaces the current set of policies for the specified load balancer port with
        the specified set of policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/set_load_balancer_policies_of_listener.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#set_load_balancer_policies_of_listener)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_account_limits"]
    ) -> DescribeAccountLimitsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_load_balancers"]
    ) -> DescribeLoadBalancersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["any_instance_in_service"]
    ) -> AnyInstanceInServiceWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["instance_deregistered"]
    ) -> InstanceDeregisteredWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["instance_in_service"]) -> InstanceInServiceWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb/client/#get_waiter)
        """
