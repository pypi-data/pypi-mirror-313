"""
Type annotations for autoscaling service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_autoscaling.client import AutoScalingClient

    session = Session()
    client: AutoScalingClient = session.client("autoscaling")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeAutoScalingGroupsPaginator,
    DescribeAutoScalingInstancesPaginator,
    DescribeLaunchConfigurationsPaginator,
    DescribeLoadBalancersPaginator,
    DescribeLoadBalancerTargetGroupsPaginator,
    DescribeNotificationConfigurationsPaginator,
    DescribePoliciesPaginator,
    DescribeScalingActivitiesPaginator,
    DescribeScheduledActionsPaginator,
    DescribeTagsPaginator,
    DescribeWarmPoolPaginator,
)
from .type_defs import (
    ActivitiesTypeTypeDef,
    ActivityTypeTypeDef,
    AttachInstancesQueryRequestTypeDef,
    AttachLoadBalancersTypeRequestTypeDef,
    AttachLoadBalancerTargetGroupsTypeRequestTypeDef,
    AttachTrafficSourcesTypeRequestTypeDef,
    AutoScalingGroupNamesTypeRequestTypeDef,
    AutoScalingGroupsTypeTypeDef,
    AutoScalingInstancesTypeTypeDef,
    BatchDeleteScheduledActionAnswerTypeDef,
    BatchDeleteScheduledActionTypeRequestTypeDef,
    BatchPutScheduledUpdateGroupActionAnswerTypeDef,
    BatchPutScheduledUpdateGroupActionTypeRequestTypeDef,
    CancelInstanceRefreshAnswerTypeDef,
    CancelInstanceRefreshTypeRequestTypeDef,
    CompleteLifecycleActionTypeRequestTypeDef,
    CreateAutoScalingGroupTypeRequestTypeDef,
    CreateLaunchConfigurationTypeRequestTypeDef,
    CreateOrUpdateTagsTypeRequestTypeDef,
    DeleteAutoScalingGroupTypeRequestTypeDef,
    DeleteLifecycleHookTypeRequestTypeDef,
    DeleteNotificationConfigurationTypeRequestTypeDef,
    DeletePolicyTypeRequestTypeDef,
    DeleteScheduledActionTypeRequestTypeDef,
    DeleteTagsTypeRequestTypeDef,
    DeleteWarmPoolTypeRequestTypeDef,
    DescribeAccountLimitsAnswerTypeDef,
    DescribeAdjustmentTypesAnswerTypeDef,
    DescribeAutoScalingInstancesTypeRequestTypeDef,
    DescribeAutoScalingNotificationTypesAnswerTypeDef,
    DescribeInstanceRefreshesAnswerTypeDef,
    DescribeInstanceRefreshesTypeRequestTypeDef,
    DescribeLifecycleHooksAnswerTypeDef,
    DescribeLifecycleHooksTypeRequestTypeDef,
    DescribeLifecycleHookTypesAnswerTypeDef,
    DescribeLoadBalancersRequestRequestTypeDef,
    DescribeLoadBalancersResponseTypeDef,
    DescribeLoadBalancerTargetGroupsRequestRequestTypeDef,
    DescribeLoadBalancerTargetGroupsResponseTypeDef,
    DescribeMetricCollectionTypesAnswerTypeDef,
    DescribeNotificationConfigurationsAnswerTypeDef,
    DescribeNotificationConfigurationsTypeRequestTypeDef,
    DescribePoliciesTypeRequestTypeDef,
    DescribeScalingActivitiesTypeRequestTypeDef,
    DescribeScheduledActionsTypeRequestTypeDef,
    DescribeTagsTypeRequestTypeDef,
    DescribeTerminationPolicyTypesAnswerTypeDef,
    DescribeTrafficSourcesRequestRequestTypeDef,
    DescribeTrafficSourcesResponseTypeDef,
    DescribeWarmPoolAnswerTypeDef,
    DescribeWarmPoolTypeRequestTypeDef,
    DetachInstancesAnswerTypeDef,
    DetachInstancesQueryRequestTypeDef,
    DetachLoadBalancersTypeRequestTypeDef,
    DetachLoadBalancerTargetGroupsTypeRequestTypeDef,
    DetachTrafficSourcesTypeRequestTypeDef,
    DisableMetricsCollectionQueryRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableMetricsCollectionQueryRequestTypeDef,
    EnterStandbyAnswerTypeDef,
    EnterStandbyQueryRequestTypeDef,
    ExecutePolicyTypeRequestTypeDef,
    ExitStandbyAnswerTypeDef,
    ExitStandbyQueryRequestTypeDef,
    GetPredictiveScalingForecastAnswerTypeDef,
    GetPredictiveScalingForecastTypeRequestTypeDef,
    LaunchConfigurationNamesTypeRequestTypeDef,
    LaunchConfigurationNameTypeRequestTypeDef,
    LaunchConfigurationsTypeTypeDef,
    PoliciesTypeTypeDef,
    PolicyARNTypeTypeDef,
    ProcessesTypeTypeDef,
    PutLifecycleHookTypeRequestTypeDef,
    PutNotificationConfigurationTypeRequestTypeDef,
    PutScalingPolicyTypeRequestTypeDef,
    PutScheduledUpdateGroupActionTypeRequestTypeDef,
    PutWarmPoolTypeRequestTypeDef,
    RecordLifecycleActionHeartbeatTypeRequestTypeDef,
    RollbackInstanceRefreshAnswerTypeDef,
    RollbackInstanceRefreshTypeRequestTypeDef,
    ScalingProcessQueryRequestTypeDef,
    ScheduledActionsTypeTypeDef,
    SetDesiredCapacityTypeRequestTypeDef,
    SetInstanceHealthQueryRequestTypeDef,
    SetInstanceProtectionQueryRequestTypeDef,
    StartInstanceRefreshAnswerTypeDef,
    StartInstanceRefreshTypeRequestTypeDef,
    TagsTypeTypeDef,
    TerminateInstanceInAutoScalingGroupTypeRequestTypeDef,
    UpdateAutoScalingGroupTypeRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("AutoScalingClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ActiveInstanceRefreshNotFoundFault: Type[BotocoreClientError]
    AlreadyExistsFault: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InstanceRefreshInProgressFault: Type[BotocoreClientError]
    InvalidNextToken: Type[BotocoreClientError]
    IrreversibleInstanceRefreshFault: Type[BotocoreClientError]
    LimitExceededFault: Type[BotocoreClientError]
    ResourceContentionFault: Type[BotocoreClientError]
    ResourceInUseFault: Type[BotocoreClientError]
    ScalingActivityInProgressFault: Type[BotocoreClientError]
    ServiceLinkedRoleFailure: Type[BotocoreClientError]

class AutoScalingClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AutoScalingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#close)
        """

    def attach_instances(
        self, **kwargs: Unpack[AttachInstancesQueryRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches one or more EC2 instances to the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/attach_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#attach_instances)
        """

    def attach_load_balancer_target_groups(
        self, **kwargs: Unpack[AttachLoadBalancerTargetGroupsTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This API operation is superseded by <a
        href="https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_AttachTrafficSources.html">AttachTrafficSources</a>,
        which can attach multiple traffic sources types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/attach_load_balancer_target_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#attach_load_balancer_target_groups)
        """

    def attach_load_balancers(
        self, **kwargs: Unpack[AttachLoadBalancersTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This API operation is superseded by <a
        href="https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_AttachTrafficSources.html">https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_AttachTrafficSources.html</a>,
        which can attach multiple traffic sources types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/attach_load_balancers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#attach_load_balancers)
        """

    def attach_traffic_sources(
        self, **kwargs: Unpack[AttachTrafficSourcesTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Attaches one or more traffic sources to the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/attach_traffic_sources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#attach_traffic_sources)
        """

    def batch_delete_scheduled_action(
        self, **kwargs: Unpack[BatchDeleteScheduledActionTypeRequestTypeDef]
    ) -> BatchDeleteScheduledActionAnswerTypeDef:
        """
        Deletes one or more scheduled actions for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/batch_delete_scheduled_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#batch_delete_scheduled_action)
        """

    def batch_put_scheduled_update_group_action(
        self, **kwargs: Unpack[BatchPutScheduledUpdateGroupActionTypeRequestTypeDef]
    ) -> BatchPutScheduledUpdateGroupActionAnswerTypeDef:
        """
        Creates or updates one or more scheduled scaling actions for an Auto Scaling
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/batch_put_scheduled_update_group_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#batch_put_scheduled_update_group_action)
        """

    def cancel_instance_refresh(
        self, **kwargs: Unpack[CancelInstanceRefreshTypeRequestTypeDef]
    ) -> CancelInstanceRefreshAnswerTypeDef:
        """
        Cancels an instance refresh or rollback that is in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/cancel_instance_refresh.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#cancel_instance_refresh)
        """

    def complete_lifecycle_action(
        self, **kwargs: Unpack[CompleteLifecycleActionTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Completes the lifecycle action for the specified token or instance with the
        specified result.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/complete_lifecycle_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#complete_lifecycle_action)
        """

    def create_auto_scaling_group(
        self, **kwargs: Unpack[CreateAutoScalingGroupTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        <b>We strongly recommend using a launch template when calling this operation to
        ensure full functionality for Amazon EC2 Auto Scaling and Amazon EC2.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/create_auto_scaling_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#create_auto_scaling_group)
        """

    def create_launch_configuration(
        self, **kwargs: Unpack[CreateLaunchConfigurationTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a launch configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/create_launch_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#create_launch_configuration)
        """

    def create_or_update_tags(
        self, **kwargs: Unpack[CreateOrUpdateTagsTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates tags for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/create_or_update_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#create_or_update_tags)
        """

    def delete_auto_scaling_group(
        self, **kwargs: Unpack[DeleteAutoScalingGroupTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/delete_auto_scaling_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#delete_auto_scaling_group)
        """

    def delete_launch_configuration(
        self, **kwargs: Unpack[LaunchConfigurationNameTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified launch configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/delete_launch_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#delete_launch_configuration)
        """

    def delete_lifecycle_hook(
        self, **kwargs: Unpack[DeleteLifecycleHookTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified lifecycle hook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/delete_lifecycle_hook.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#delete_lifecycle_hook)
        """

    def delete_notification_configuration(
        self, **kwargs: Unpack[DeleteNotificationConfigurationTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified notification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/delete_notification_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#delete_notification_configuration)
        """

    def delete_policy(
        self, **kwargs: Unpack[DeletePolicyTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified scaling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/delete_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#delete_policy)
        """

    def delete_scheduled_action(
        self, **kwargs: Unpack[DeleteScheduledActionTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified scheduled action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/delete_scheduled_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#delete_scheduled_action)
        """

    def delete_tags(
        self, **kwargs: Unpack[DeleteTagsTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/delete_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#delete_tags)
        """

    def delete_warm_pool(
        self, **kwargs: Unpack[DeleteWarmPoolTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the warm pool for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/delete_warm_pool.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#delete_warm_pool)
        """

    def describe_account_limits(self) -> DescribeAccountLimitsAnswerTypeDef:
        """
        Describes the current Amazon EC2 Auto Scaling resource quotas for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_account_limits.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_account_limits)
        """

    def describe_adjustment_types(self) -> DescribeAdjustmentTypesAnswerTypeDef:
        """
        Describes the available adjustment types for step scaling and simple scaling
        policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_adjustment_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_adjustment_types)
        """

    def describe_auto_scaling_groups(
        self, **kwargs: Unpack[AutoScalingGroupNamesTypeRequestTypeDef]
    ) -> AutoScalingGroupsTypeTypeDef:
        """
        Gets information about the Auto Scaling groups in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_auto_scaling_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_auto_scaling_groups)
        """

    def describe_auto_scaling_instances(
        self, **kwargs: Unpack[DescribeAutoScalingInstancesTypeRequestTypeDef]
    ) -> AutoScalingInstancesTypeTypeDef:
        """
        Gets information about the Auto Scaling instances in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_auto_scaling_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_auto_scaling_instances)
        """

    def describe_auto_scaling_notification_types(
        self,
    ) -> DescribeAutoScalingNotificationTypesAnswerTypeDef:
        """
        Describes the notification types that are supported by Amazon EC2 Auto Scaling.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_auto_scaling_notification_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_auto_scaling_notification_types)
        """

    def describe_instance_refreshes(
        self, **kwargs: Unpack[DescribeInstanceRefreshesTypeRequestTypeDef]
    ) -> DescribeInstanceRefreshesAnswerTypeDef:
        """
        Gets information about the instance refreshes for the specified Auto Scaling
        group from the previous six weeks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_instance_refreshes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_instance_refreshes)
        """

    def describe_launch_configurations(
        self, **kwargs: Unpack[LaunchConfigurationNamesTypeRequestTypeDef]
    ) -> LaunchConfigurationsTypeTypeDef:
        """
        Gets information about the launch configurations in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_launch_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_launch_configurations)
        """

    def describe_lifecycle_hook_types(self) -> DescribeLifecycleHookTypesAnswerTypeDef:
        """
        Describes the available types of lifecycle hooks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_lifecycle_hook_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_lifecycle_hook_types)
        """

    def describe_lifecycle_hooks(
        self, **kwargs: Unpack[DescribeLifecycleHooksTypeRequestTypeDef]
    ) -> DescribeLifecycleHooksAnswerTypeDef:
        """
        Gets information about the lifecycle hooks for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_lifecycle_hooks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_lifecycle_hooks)
        """

    def describe_load_balancer_target_groups(
        self, **kwargs: Unpack[DescribeLoadBalancerTargetGroupsRequestRequestTypeDef]
    ) -> DescribeLoadBalancerTargetGroupsResponseTypeDef:
        """
        This API operation is superseded by <a
        href="https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_DescribeTrafficSources.html">DescribeTrafficSources</a>,
        which can describe multiple traffic sources types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_load_balancer_target_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_load_balancer_target_groups)
        """

    def describe_load_balancers(
        self, **kwargs: Unpack[DescribeLoadBalancersRequestRequestTypeDef]
    ) -> DescribeLoadBalancersResponseTypeDef:
        """
        This API operation is superseded by <a
        href="https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_DescribeTrafficSources.html">DescribeTrafficSources</a>,
        which can describe multiple traffic sources types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_load_balancers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_load_balancers)
        """

    def describe_metric_collection_types(self) -> DescribeMetricCollectionTypesAnswerTypeDef:
        """
        Describes the available CloudWatch metrics for Amazon EC2 Auto Scaling.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_metric_collection_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_metric_collection_types)
        """

    def describe_notification_configurations(
        self, **kwargs: Unpack[DescribeNotificationConfigurationsTypeRequestTypeDef]
    ) -> DescribeNotificationConfigurationsAnswerTypeDef:
        """
        Gets information about the Amazon SNS notifications that are configured for one
        or more Auto Scaling groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_notification_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_notification_configurations)
        """

    def describe_policies(
        self, **kwargs: Unpack[DescribePoliciesTypeRequestTypeDef]
    ) -> PoliciesTypeTypeDef:
        """
        Gets information about the scaling policies in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_policies)
        """

    def describe_scaling_activities(
        self, **kwargs: Unpack[DescribeScalingActivitiesTypeRequestTypeDef]
    ) -> ActivitiesTypeTypeDef:
        """
        Gets information about the scaling activities in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_scaling_activities.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_scaling_activities)
        """

    def describe_scaling_process_types(self) -> ProcessesTypeTypeDef:
        """
        Describes the scaling process types for use with the <a
        href="https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_ResumeProcesses.html">ResumeProcesses</a>
        and <a
        href="https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_SuspendProcesses.html">SuspendProcesses</a>
        APIs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_scaling_process_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_scaling_process_types)
        """

    def describe_scheduled_actions(
        self, **kwargs: Unpack[DescribeScheduledActionsTypeRequestTypeDef]
    ) -> ScheduledActionsTypeTypeDef:
        """
        Gets information about the scheduled actions that haven't run or that have not
        reached their end time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_scheduled_actions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_scheduled_actions)
        """

    def describe_tags(self, **kwargs: Unpack[DescribeTagsTypeRequestTypeDef]) -> TagsTypeTypeDef:
        """
        Describes the specified tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_tags)
        """

    def describe_termination_policy_types(self) -> DescribeTerminationPolicyTypesAnswerTypeDef:
        """
        Describes the termination policies supported by Amazon EC2 Auto Scaling.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_termination_policy_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_termination_policy_types)
        """

    def describe_traffic_sources(
        self, **kwargs: Unpack[DescribeTrafficSourcesRequestRequestTypeDef]
    ) -> DescribeTrafficSourcesResponseTypeDef:
        """
        Gets information about the traffic sources for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_traffic_sources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_traffic_sources)
        """

    def describe_warm_pool(
        self, **kwargs: Unpack[DescribeWarmPoolTypeRequestTypeDef]
    ) -> DescribeWarmPoolAnswerTypeDef:
        """
        Gets information about a warm pool and its instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_warm_pool.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#describe_warm_pool)
        """

    def detach_instances(
        self, **kwargs: Unpack[DetachInstancesQueryRequestTypeDef]
    ) -> DetachInstancesAnswerTypeDef:
        """
        Removes one or more instances from the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/detach_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#detach_instances)
        """

    def detach_load_balancer_target_groups(
        self, **kwargs: Unpack[DetachLoadBalancerTargetGroupsTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This API operation is superseded by <a
        href="https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_DescribeTrafficSources.html">DetachTrafficSources</a>,
        which can detach multiple traffic sources types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/detach_load_balancer_target_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#detach_load_balancer_target_groups)
        """

    def detach_load_balancers(
        self, **kwargs: Unpack[DetachLoadBalancersTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This API operation is superseded by <a
        href="https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_DetachTrafficSources.html">DetachTrafficSources</a>,
        which can detach multiple traffic sources types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/detach_load_balancers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#detach_load_balancers)
        """

    def detach_traffic_sources(
        self, **kwargs: Unpack[DetachTrafficSourcesTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Detaches one or more traffic sources from the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/detach_traffic_sources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#detach_traffic_sources)
        """

    def disable_metrics_collection(
        self, **kwargs: Unpack[DisableMetricsCollectionQueryRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disables group metrics collection for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/disable_metrics_collection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#disable_metrics_collection)
        """

    def enable_metrics_collection(
        self, **kwargs: Unpack[EnableMetricsCollectionQueryRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables group metrics collection for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/enable_metrics_collection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#enable_metrics_collection)
        """

    def enter_standby(
        self, **kwargs: Unpack[EnterStandbyQueryRequestTypeDef]
    ) -> EnterStandbyAnswerTypeDef:
        """
        Moves the specified instances into the standby state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/enter_standby.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#enter_standby)
        """

    def execute_policy(
        self, **kwargs: Unpack[ExecutePolicyTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Executes the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/execute_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#execute_policy)
        """

    def exit_standby(
        self, **kwargs: Unpack[ExitStandbyQueryRequestTypeDef]
    ) -> ExitStandbyAnswerTypeDef:
        """
        Moves the specified instances out of the standby state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/exit_standby.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#exit_standby)
        """

    def get_predictive_scaling_forecast(
        self, **kwargs: Unpack[GetPredictiveScalingForecastTypeRequestTypeDef]
    ) -> GetPredictiveScalingForecastAnswerTypeDef:
        """
        Retrieves the forecast data for a predictive scaling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/get_predictive_scaling_forecast.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#get_predictive_scaling_forecast)
        """

    def put_lifecycle_hook(
        self, **kwargs: Unpack[PutLifecycleHookTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates a lifecycle hook for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/put_lifecycle_hook.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#put_lifecycle_hook)
        """

    def put_notification_configuration(
        self, **kwargs: Unpack[PutNotificationConfigurationTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Configures an Auto Scaling group to send notifications when specified events
        take place.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/put_notification_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#put_notification_configuration)
        """

    def put_scaling_policy(
        self, **kwargs: Unpack[PutScalingPolicyTypeRequestTypeDef]
    ) -> PolicyARNTypeTypeDef:
        """
        Creates or updates a scaling policy for an Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/put_scaling_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#put_scaling_policy)
        """

    def put_scheduled_update_group_action(
        self, **kwargs: Unpack[PutScheduledUpdateGroupActionTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates a scheduled scaling action for an Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/put_scheduled_update_group_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#put_scheduled_update_group_action)
        """

    def put_warm_pool(self, **kwargs: Unpack[PutWarmPoolTypeRequestTypeDef]) -> Dict[str, Any]:
        """
        Creates or updates a warm pool for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/put_warm_pool.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#put_warm_pool)
        """

    def record_lifecycle_action_heartbeat(
        self, **kwargs: Unpack[RecordLifecycleActionHeartbeatTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Records a heartbeat for the lifecycle action associated with the specified
        token or instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/record_lifecycle_action_heartbeat.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#record_lifecycle_action_heartbeat)
        """

    def resume_processes(
        self, **kwargs: Unpack[ScalingProcessQueryRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Resumes the specified suspended auto scaling processes, or all suspended
        process, for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/resume_processes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#resume_processes)
        """

    def rollback_instance_refresh(
        self, **kwargs: Unpack[RollbackInstanceRefreshTypeRequestTypeDef]
    ) -> RollbackInstanceRefreshAnswerTypeDef:
        """
        Cancels an instance refresh that is in progress and rolls back any changes that
        it made.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/rollback_instance_refresh.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#rollback_instance_refresh)
        """

    def set_desired_capacity(
        self, **kwargs: Unpack[SetDesiredCapacityTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the size of the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/set_desired_capacity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#set_desired_capacity)
        """

    def set_instance_health(
        self, **kwargs: Unpack[SetInstanceHealthQueryRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the health status of the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/set_instance_health.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#set_instance_health)
        """

    def set_instance_protection(
        self, **kwargs: Unpack[SetInstanceProtectionQueryRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the instance protection settings of the specified instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/set_instance_protection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#set_instance_protection)
        """

    def start_instance_refresh(
        self, **kwargs: Unpack[StartInstanceRefreshTypeRequestTypeDef]
    ) -> StartInstanceRefreshAnswerTypeDef:
        """
        Starts an instance refresh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/start_instance_refresh.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#start_instance_refresh)
        """

    def suspend_processes(
        self, **kwargs: Unpack[ScalingProcessQueryRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Suspends the specified auto scaling processes, or all processes, for the
        specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/suspend_processes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#suspend_processes)
        """

    def terminate_instance_in_auto_scaling_group(
        self, **kwargs: Unpack[TerminateInstanceInAutoScalingGroupTypeRequestTypeDef]
    ) -> ActivityTypeTypeDef:
        """
        Terminates the specified instance and optionally adjusts the desired group size.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/terminate_instance_in_auto_scaling_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#terminate_instance_in_auto_scaling_group)
        """

    def update_auto_scaling_group(
        self, **kwargs: Unpack[UpdateAutoScalingGroupTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        <b>We strongly recommend that all Auto Scaling groups use launch templates to
        ensure full functionality for Amazon EC2 Auto Scaling and Amazon EC2.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/update_auto_scaling_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#update_auto_scaling_group)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_auto_scaling_groups"]
    ) -> DescribeAutoScalingGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_auto_scaling_instances"]
    ) -> DescribeAutoScalingInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_launch_configurations"]
    ) -> DescribeLaunchConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_load_balancer_target_groups"]
    ) -> DescribeLoadBalancerTargetGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_load_balancers"]
    ) -> DescribeLoadBalancersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_notification_configurations"]
    ) -> DescribeNotificationConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_policies"]
    ) -> DescribePoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scaling_activities"]
    ) -> DescribeScalingActivitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scheduled_actions"]
    ) -> DescribeScheduledActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_tags"]) -> DescribeTagsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_warm_pool"]
    ) -> DescribeWarmPoolPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_autoscaling/client/#get_paginator)
        """
