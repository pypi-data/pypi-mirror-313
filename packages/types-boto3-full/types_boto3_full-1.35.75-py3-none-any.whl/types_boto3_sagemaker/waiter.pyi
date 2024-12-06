"""
Type annotations for sagemaker service client waiters.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_sagemaker.client import SageMakerClient
    from types_boto3_sagemaker.waiter import (
        EndpointDeletedWaiter,
        EndpointInServiceWaiter,
        ImageCreatedWaiter,
        ImageDeletedWaiter,
        ImageUpdatedWaiter,
        ImageVersionCreatedWaiter,
        ImageVersionDeletedWaiter,
        NotebookInstanceDeletedWaiter,
        NotebookInstanceInServiceWaiter,
        NotebookInstanceStoppedWaiter,
        ProcessingJobCompletedOrStoppedWaiter,
        TrainingJobCompletedOrStoppedWaiter,
        TransformJobCompletedOrStoppedWaiter,
    )

    session = Session()
    client: SageMakerClient = session.client("sagemaker")

    endpoint_deleted_waiter: EndpointDeletedWaiter = client.get_waiter("endpoint_deleted")
    endpoint_in_service_waiter: EndpointInServiceWaiter = client.get_waiter("endpoint_in_service")
    image_created_waiter: ImageCreatedWaiter = client.get_waiter("image_created")
    image_deleted_waiter: ImageDeletedWaiter = client.get_waiter("image_deleted")
    image_updated_waiter: ImageUpdatedWaiter = client.get_waiter("image_updated")
    image_version_created_waiter: ImageVersionCreatedWaiter = client.get_waiter("image_version_created")
    image_version_deleted_waiter: ImageVersionDeletedWaiter = client.get_waiter("image_version_deleted")
    notebook_instance_deleted_waiter: NotebookInstanceDeletedWaiter = client.get_waiter("notebook_instance_deleted")
    notebook_instance_in_service_waiter: NotebookInstanceInServiceWaiter = client.get_waiter("notebook_instance_in_service")
    notebook_instance_stopped_waiter: NotebookInstanceStoppedWaiter = client.get_waiter("notebook_instance_stopped")
    processing_job_completed_or_stopped_waiter: ProcessingJobCompletedOrStoppedWaiter = client.get_waiter("processing_job_completed_or_stopped")
    training_job_completed_or_stopped_waiter: TrainingJobCompletedOrStoppedWaiter = client.get_waiter("training_job_completed_or_stopped")
    transform_job_completed_or_stopped_waiter: TransformJobCompletedOrStoppedWaiter = client.get_waiter("transform_job_completed_or_stopped")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import (
    DescribeEndpointInputEndpointDeletedWaitTypeDef,
    DescribeEndpointInputEndpointInServiceWaitTypeDef,
    DescribeImageRequestImageCreatedWaitTypeDef,
    DescribeImageRequestImageDeletedWaitTypeDef,
    DescribeImageRequestImageUpdatedWaitTypeDef,
    DescribeImageVersionRequestImageVersionCreatedWaitTypeDef,
    DescribeImageVersionRequestImageVersionDeletedWaitTypeDef,
    DescribeNotebookInstanceInputNotebookInstanceDeletedWaitTypeDef,
    DescribeNotebookInstanceInputNotebookInstanceInServiceWaitTypeDef,
    DescribeNotebookInstanceInputNotebookInstanceStoppedWaitTypeDef,
    DescribeProcessingJobRequestProcessingJobCompletedOrStoppedWaitTypeDef,
    DescribeTrainingJobRequestTrainingJobCompletedOrStoppedWaitTypeDef,
    DescribeTransformJobRequestTransformJobCompletedOrStoppedWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "EndpointDeletedWaiter",
    "EndpointInServiceWaiter",
    "ImageCreatedWaiter",
    "ImageDeletedWaiter",
    "ImageUpdatedWaiter",
    "ImageVersionCreatedWaiter",
    "ImageVersionDeletedWaiter",
    "NotebookInstanceDeletedWaiter",
    "NotebookInstanceInServiceWaiter",
    "NotebookInstanceStoppedWaiter",
    "ProcessingJobCompletedOrStoppedWaiter",
    "TrainingJobCompletedOrStoppedWaiter",
    "TransformJobCompletedOrStoppedWaiter",
)

class EndpointDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/EndpointDeleted.html#SageMaker.Waiter.EndpointDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#endpointdeletedwaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeEndpointInputEndpointDeletedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/EndpointDeleted.html#SageMaker.Waiter.EndpointDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#endpointdeletedwaiter)
        """

class EndpointInServiceWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/EndpointInService.html#SageMaker.Waiter.EndpointInService)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#endpointinservicewaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeEndpointInputEndpointInServiceWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/EndpointInService.html#SageMaker.Waiter.EndpointInService.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#endpointinservicewaiter)
        """

class ImageCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageCreated.html#SageMaker.Waiter.ImageCreated)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#imagecreatedwaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeImageRequestImageCreatedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageCreated.html#SageMaker.Waiter.ImageCreated.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#imagecreatedwaiter)
        """

class ImageDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageDeleted.html#SageMaker.Waiter.ImageDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#imagedeletedwaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeImageRequestImageDeletedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageDeleted.html#SageMaker.Waiter.ImageDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#imagedeletedwaiter)
        """

class ImageUpdatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageUpdated.html#SageMaker.Waiter.ImageUpdated)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#imageupdatedwaiter)
    """
    def wait(self, **kwargs: Unpack[DescribeImageRequestImageUpdatedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageUpdated.html#SageMaker.Waiter.ImageUpdated.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#imageupdatedwaiter)
        """

class ImageVersionCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageVersionCreated.html#SageMaker.Waiter.ImageVersionCreated)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#imageversioncreatedwaiter)
    """
    def wait(
        self, **kwargs: Unpack[DescribeImageVersionRequestImageVersionCreatedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageVersionCreated.html#SageMaker.Waiter.ImageVersionCreated.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#imageversioncreatedwaiter)
        """

class ImageVersionDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageVersionDeleted.html#SageMaker.Waiter.ImageVersionDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#imageversiondeletedwaiter)
    """
    def wait(
        self, **kwargs: Unpack[DescribeImageVersionRequestImageVersionDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageVersionDeleted.html#SageMaker.Waiter.ImageVersionDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#imageversiondeletedwaiter)
        """

class NotebookInstanceDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/NotebookInstanceDeleted.html#SageMaker.Waiter.NotebookInstanceDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#notebookinstancedeletedwaiter)
    """
    def wait(
        self, **kwargs: Unpack[DescribeNotebookInstanceInputNotebookInstanceDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/NotebookInstanceDeleted.html#SageMaker.Waiter.NotebookInstanceDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#notebookinstancedeletedwaiter)
        """

class NotebookInstanceInServiceWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/NotebookInstanceInService.html#SageMaker.Waiter.NotebookInstanceInService)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#notebookinstanceinservicewaiter)
    """
    def wait(
        self, **kwargs: Unpack[DescribeNotebookInstanceInputNotebookInstanceInServiceWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/NotebookInstanceInService.html#SageMaker.Waiter.NotebookInstanceInService.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#notebookinstanceinservicewaiter)
        """

class NotebookInstanceStoppedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/NotebookInstanceStopped.html#SageMaker.Waiter.NotebookInstanceStopped)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#notebookinstancestoppedwaiter)
    """
    def wait(
        self, **kwargs: Unpack[DescribeNotebookInstanceInputNotebookInstanceStoppedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/NotebookInstanceStopped.html#SageMaker.Waiter.NotebookInstanceStopped.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#notebookinstancestoppedwaiter)
        """

class ProcessingJobCompletedOrStoppedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ProcessingJobCompletedOrStopped.html#SageMaker.Waiter.ProcessingJobCompletedOrStopped)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#processingjobcompletedorstoppedwaiter)
    """
    def wait(
        self,
        **kwargs: Unpack[DescribeProcessingJobRequestProcessingJobCompletedOrStoppedWaitTypeDef],
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ProcessingJobCompletedOrStopped.html#SageMaker.Waiter.ProcessingJobCompletedOrStopped.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#processingjobcompletedorstoppedwaiter)
        """

class TrainingJobCompletedOrStoppedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/TrainingJobCompletedOrStopped.html#SageMaker.Waiter.TrainingJobCompletedOrStopped)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#trainingjobcompletedorstoppedwaiter)
    """
    def wait(
        self, **kwargs: Unpack[DescribeTrainingJobRequestTrainingJobCompletedOrStoppedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/TrainingJobCompletedOrStopped.html#SageMaker.Waiter.TrainingJobCompletedOrStopped.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#trainingjobcompletedorstoppedwaiter)
        """

class TransformJobCompletedOrStoppedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/TransformJobCompletedOrStopped.html#SageMaker.Waiter.TransformJobCompletedOrStopped)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#transformjobcompletedorstoppedwaiter)
    """
    def wait(
        self, **kwargs: Unpack[DescribeTransformJobRequestTransformJobCompletedOrStoppedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/TransformJobCompletedOrStopped.html#SageMaker.Waiter.TransformJobCompletedOrStopped.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/waiters/#transformjobcompletedorstoppedwaiter)
        """
