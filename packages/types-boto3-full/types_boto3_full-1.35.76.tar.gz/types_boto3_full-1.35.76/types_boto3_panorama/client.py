"""
Type annotations for panorama service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_panorama.client import PanoramaClient

    session = Session()
    client: PanoramaClient = session.client("panorama")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateApplicationInstanceRequestRequestTypeDef,
    CreateApplicationInstanceResponseTypeDef,
    CreateJobForDevicesRequestRequestTypeDef,
    CreateJobForDevicesResponseTypeDef,
    CreateNodeFromTemplateJobRequestRequestTypeDef,
    CreateNodeFromTemplateJobResponseTypeDef,
    CreatePackageImportJobRequestRequestTypeDef,
    CreatePackageImportJobResponseTypeDef,
    CreatePackageRequestRequestTypeDef,
    CreatePackageResponseTypeDef,
    DeleteDeviceRequestRequestTypeDef,
    DeleteDeviceResponseTypeDef,
    DeletePackageRequestRequestTypeDef,
    DeregisterPackageVersionRequestRequestTypeDef,
    DescribeApplicationInstanceDetailsRequestRequestTypeDef,
    DescribeApplicationInstanceDetailsResponseTypeDef,
    DescribeApplicationInstanceRequestRequestTypeDef,
    DescribeApplicationInstanceResponseTypeDef,
    DescribeDeviceJobRequestRequestTypeDef,
    DescribeDeviceJobResponseTypeDef,
    DescribeDeviceRequestRequestTypeDef,
    DescribeDeviceResponseTypeDef,
    DescribeNodeFromTemplateJobRequestRequestTypeDef,
    DescribeNodeFromTemplateJobResponseTypeDef,
    DescribeNodeRequestRequestTypeDef,
    DescribeNodeResponseTypeDef,
    DescribePackageImportJobRequestRequestTypeDef,
    DescribePackageImportJobResponseTypeDef,
    DescribePackageRequestRequestTypeDef,
    DescribePackageResponseTypeDef,
    DescribePackageVersionRequestRequestTypeDef,
    DescribePackageVersionResponseTypeDef,
    ListApplicationInstanceDependenciesRequestRequestTypeDef,
    ListApplicationInstanceDependenciesResponseTypeDef,
    ListApplicationInstanceNodeInstancesRequestRequestTypeDef,
    ListApplicationInstanceNodeInstancesResponseTypeDef,
    ListApplicationInstancesRequestRequestTypeDef,
    ListApplicationInstancesResponseTypeDef,
    ListDevicesJobsRequestRequestTypeDef,
    ListDevicesJobsResponseTypeDef,
    ListDevicesRequestRequestTypeDef,
    ListDevicesResponseTypeDef,
    ListNodeFromTemplateJobsRequestRequestTypeDef,
    ListNodeFromTemplateJobsResponseTypeDef,
    ListNodesRequestRequestTypeDef,
    ListNodesResponseTypeDef,
    ListPackageImportJobsRequestRequestTypeDef,
    ListPackageImportJobsResponseTypeDef,
    ListPackagesRequestRequestTypeDef,
    ListPackagesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ProvisionDeviceRequestRequestTypeDef,
    ProvisionDeviceResponseTypeDef,
    RegisterPackageVersionRequestRequestTypeDef,
    RemoveApplicationInstanceRequestRequestTypeDef,
    SignalApplicationInstanceNodeInstancesRequestRequestTypeDef,
    SignalApplicationInstanceNodeInstancesResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDeviceMetadataRequestRequestTypeDef,
    UpdateDeviceMetadataResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("PanoramaClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class PanoramaClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PanoramaClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#close)
        """

    def create_application_instance(
        self, **kwargs: Unpack[CreateApplicationInstanceRequestRequestTypeDef]
    ) -> CreateApplicationInstanceResponseTypeDef:
        """
        Creates an application instance and deploys it to a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/create_application_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#create_application_instance)
        """

    def create_job_for_devices(
        self, **kwargs: Unpack[CreateJobForDevicesRequestRequestTypeDef]
    ) -> CreateJobForDevicesResponseTypeDef:
        """
        Creates a job to run on a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/create_job_for_devices.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#create_job_for_devices)
        """

    def create_node_from_template_job(
        self, **kwargs: Unpack[CreateNodeFromTemplateJobRequestRequestTypeDef]
    ) -> CreateNodeFromTemplateJobResponseTypeDef:
        """
        Creates a camera stream node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/create_node_from_template_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#create_node_from_template_job)
        """

    def create_package(
        self, **kwargs: Unpack[CreatePackageRequestRequestTypeDef]
    ) -> CreatePackageResponseTypeDef:
        """
        Creates a package and storage location in an Amazon S3 access point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/create_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#create_package)
        """

    def create_package_import_job(
        self, **kwargs: Unpack[CreatePackageImportJobRequestRequestTypeDef]
    ) -> CreatePackageImportJobResponseTypeDef:
        """
        Imports a node package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/create_package_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#create_package_import_job)
        """

    def delete_device(
        self, **kwargs: Unpack[DeleteDeviceRequestRequestTypeDef]
    ) -> DeleteDeviceResponseTypeDef:
        """
        Deletes a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/delete_device.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#delete_device)
        """

    def delete_package(
        self, **kwargs: Unpack[DeletePackageRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/delete_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#delete_package)
        """

    def deregister_package_version(
        self, **kwargs: Unpack[DeregisterPackageVersionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deregisters a package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/deregister_package_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#deregister_package_version)
        """

    def describe_application_instance(
        self, **kwargs: Unpack[DescribeApplicationInstanceRequestRequestTypeDef]
    ) -> DescribeApplicationInstanceResponseTypeDef:
        """
        Returns information about an application instance on a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_application_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#describe_application_instance)
        """

    def describe_application_instance_details(
        self, **kwargs: Unpack[DescribeApplicationInstanceDetailsRequestRequestTypeDef]
    ) -> DescribeApplicationInstanceDetailsResponseTypeDef:
        """
        Returns information about an application instance's configuration manifest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_application_instance_details.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#describe_application_instance_details)
        """

    def describe_device(
        self, **kwargs: Unpack[DescribeDeviceRequestRequestTypeDef]
    ) -> DescribeDeviceResponseTypeDef:
        """
        Returns information about a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_device.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#describe_device)
        """

    def describe_device_job(
        self, **kwargs: Unpack[DescribeDeviceJobRequestRequestTypeDef]
    ) -> DescribeDeviceJobResponseTypeDef:
        """
        Returns information about a device job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_device_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#describe_device_job)
        """

    def describe_node(
        self, **kwargs: Unpack[DescribeNodeRequestRequestTypeDef]
    ) -> DescribeNodeResponseTypeDef:
        """
        Returns information about a node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_node.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#describe_node)
        """

    def describe_node_from_template_job(
        self, **kwargs: Unpack[DescribeNodeFromTemplateJobRequestRequestTypeDef]
    ) -> DescribeNodeFromTemplateJobResponseTypeDef:
        """
        Returns information about a job to create a camera stream node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_node_from_template_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#describe_node_from_template_job)
        """

    def describe_package(
        self, **kwargs: Unpack[DescribePackageRequestRequestTypeDef]
    ) -> DescribePackageResponseTypeDef:
        """
        Returns information about a package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#describe_package)
        """

    def describe_package_import_job(
        self, **kwargs: Unpack[DescribePackageImportJobRequestRequestTypeDef]
    ) -> DescribePackageImportJobResponseTypeDef:
        """
        Returns information about a package import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_package_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#describe_package_import_job)
        """

    def describe_package_version(
        self, **kwargs: Unpack[DescribePackageVersionRequestRequestTypeDef]
    ) -> DescribePackageVersionResponseTypeDef:
        """
        Returns information about a package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/describe_package_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#describe_package_version)
        """

    def list_application_instance_dependencies(
        self, **kwargs: Unpack[ListApplicationInstanceDependenciesRequestRequestTypeDef]
    ) -> ListApplicationInstanceDependenciesResponseTypeDef:
        """
        Returns a list of application instance dependencies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_application_instance_dependencies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#list_application_instance_dependencies)
        """

    def list_application_instance_node_instances(
        self, **kwargs: Unpack[ListApplicationInstanceNodeInstancesRequestRequestTypeDef]
    ) -> ListApplicationInstanceNodeInstancesResponseTypeDef:
        """
        Returns a list of application node instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_application_instance_node_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#list_application_instance_node_instances)
        """

    def list_application_instances(
        self, **kwargs: Unpack[ListApplicationInstancesRequestRequestTypeDef]
    ) -> ListApplicationInstancesResponseTypeDef:
        """
        Returns a list of application instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_application_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#list_application_instances)
        """

    def list_devices(
        self, **kwargs: Unpack[ListDevicesRequestRequestTypeDef]
    ) -> ListDevicesResponseTypeDef:
        """
        Returns a list of devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_devices.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#list_devices)
        """

    def list_devices_jobs(
        self, **kwargs: Unpack[ListDevicesJobsRequestRequestTypeDef]
    ) -> ListDevicesJobsResponseTypeDef:
        """
        Returns a list of jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_devices_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#list_devices_jobs)
        """

    def list_node_from_template_jobs(
        self, **kwargs: Unpack[ListNodeFromTemplateJobsRequestRequestTypeDef]
    ) -> ListNodeFromTemplateJobsResponseTypeDef:
        """
        Returns a list of camera stream node jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_node_from_template_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#list_node_from_template_jobs)
        """

    def list_nodes(
        self, **kwargs: Unpack[ListNodesRequestRequestTypeDef]
    ) -> ListNodesResponseTypeDef:
        """
        Returns a list of nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_nodes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#list_nodes)
        """

    def list_package_import_jobs(
        self, **kwargs: Unpack[ListPackageImportJobsRequestRequestTypeDef]
    ) -> ListPackageImportJobsResponseTypeDef:
        """
        Returns a list of package import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_package_import_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#list_package_import_jobs)
        """

    def list_packages(
        self, **kwargs: Unpack[ListPackagesRequestRequestTypeDef]
    ) -> ListPackagesResponseTypeDef:
        """
        Returns a list of packages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_packages.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#list_packages)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#list_tags_for_resource)
        """

    def provision_device(
        self, **kwargs: Unpack[ProvisionDeviceRequestRequestTypeDef]
    ) -> ProvisionDeviceResponseTypeDef:
        """
        Creates a device and returns a configuration archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/provision_device.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#provision_device)
        """

    def register_package_version(
        self, **kwargs: Unpack[RegisterPackageVersionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Registers a package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/register_package_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#register_package_version)
        """

    def remove_application_instance(
        self, **kwargs: Unpack[RemoveApplicationInstanceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes an application instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/remove_application_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#remove_application_instance)
        """

    def signal_application_instance_node_instances(
        self, **kwargs: Unpack[SignalApplicationInstanceNodeInstancesRequestRequestTypeDef]
    ) -> SignalApplicationInstanceNodeInstancesResponseTypeDef:
        """
        Signal camera nodes to stop or resume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/signal_application_instance_node_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#signal_application_instance_node_instances)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#untag_resource)
        """

    def update_device_metadata(
        self, **kwargs: Unpack[UpdateDeviceMetadataRequestRequestTypeDef]
    ) -> UpdateDeviceMetadataResponseTypeDef:
        """
        Updates a device's metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama/client/update_device_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_panorama/client/#update_device_metadata)
        """
