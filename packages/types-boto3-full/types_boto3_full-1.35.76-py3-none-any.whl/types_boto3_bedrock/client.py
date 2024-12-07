"""
Type annotations for bedrock service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_bedrock.client import BedrockClient

    session = Session()
    client: BedrockClient = session.client("bedrock")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListCustomModelsPaginator,
    ListEvaluationJobsPaginator,
    ListGuardrailsPaginator,
    ListImportedModelsPaginator,
    ListInferenceProfilesPaginator,
    ListMarketplaceModelEndpointsPaginator,
    ListModelCopyJobsPaginator,
    ListModelCustomizationJobsPaginator,
    ListModelImportJobsPaginator,
    ListModelInvocationJobsPaginator,
    ListPromptRoutersPaginator,
    ListProvisionedModelThroughputsPaginator,
)
from .type_defs import (
    BatchDeleteEvaluationJobRequestRequestTypeDef,
    BatchDeleteEvaluationJobResponseTypeDef,
    CreateEvaluationJobRequestRequestTypeDef,
    CreateEvaluationJobResponseTypeDef,
    CreateGuardrailRequestRequestTypeDef,
    CreateGuardrailResponseTypeDef,
    CreateGuardrailVersionRequestRequestTypeDef,
    CreateGuardrailVersionResponseTypeDef,
    CreateInferenceProfileRequestRequestTypeDef,
    CreateInferenceProfileResponseTypeDef,
    CreateMarketplaceModelEndpointRequestRequestTypeDef,
    CreateMarketplaceModelEndpointResponseTypeDef,
    CreateModelCopyJobRequestRequestTypeDef,
    CreateModelCopyJobResponseTypeDef,
    CreateModelCustomizationJobRequestRequestTypeDef,
    CreateModelCustomizationJobResponseTypeDef,
    CreateModelImportJobRequestRequestTypeDef,
    CreateModelImportJobResponseTypeDef,
    CreateModelInvocationJobRequestRequestTypeDef,
    CreateModelInvocationJobResponseTypeDef,
    CreateProvisionedModelThroughputRequestRequestTypeDef,
    CreateProvisionedModelThroughputResponseTypeDef,
    DeleteCustomModelRequestRequestTypeDef,
    DeleteGuardrailRequestRequestTypeDef,
    DeleteImportedModelRequestRequestTypeDef,
    DeleteInferenceProfileRequestRequestTypeDef,
    DeleteMarketplaceModelEndpointRequestRequestTypeDef,
    DeleteProvisionedModelThroughputRequestRequestTypeDef,
    DeregisterMarketplaceModelEndpointRequestRequestTypeDef,
    GetCustomModelRequestRequestTypeDef,
    GetCustomModelResponseTypeDef,
    GetEvaluationJobRequestRequestTypeDef,
    GetEvaluationJobResponseTypeDef,
    GetFoundationModelRequestRequestTypeDef,
    GetFoundationModelResponseTypeDef,
    GetGuardrailRequestRequestTypeDef,
    GetGuardrailResponseTypeDef,
    GetImportedModelRequestRequestTypeDef,
    GetImportedModelResponseTypeDef,
    GetInferenceProfileRequestRequestTypeDef,
    GetInferenceProfileResponseTypeDef,
    GetMarketplaceModelEndpointRequestRequestTypeDef,
    GetMarketplaceModelEndpointResponseTypeDef,
    GetModelCopyJobRequestRequestTypeDef,
    GetModelCopyJobResponseTypeDef,
    GetModelCustomizationJobRequestRequestTypeDef,
    GetModelCustomizationJobResponseTypeDef,
    GetModelImportJobRequestRequestTypeDef,
    GetModelImportJobResponseTypeDef,
    GetModelInvocationJobRequestRequestTypeDef,
    GetModelInvocationJobResponseTypeDef,
    GetModelInvocationLoggingConfigurationResponseTypeDef,
    GetPromptRouterRequestRequestTypeDef,
    GetPromptRouterResponseTypeDef,
    GetProvisionedModelThroughputRequestRequestTypeDef,
    GetProvisionedModelThroughputResponseTypeDef,
    ListCustomModelsRequestRequestTypeDef,
    ListCustomModelsResponseTypeDef,
    ListEvaluationJobsRequestRequestTypeDef,
    ListEvaluationJobsResponseTypeDef,
    ListFoundationModelsRequestRequestTypeDef,
    ListFoundationModelsResponseTypeDef,
    ListGuardrailsRequestRequestTypeDef,
    ListGuardrailsResponseTypeDef,
    ListImportedModelsRequestRequestTypeDef,
    ListImportedModelsResponseTypeDef,
    ListInferenceProfilesRequestRequestTypeDef,
    ListInferenceProfilesResponseTypeDef,
    ListMarketplaceModelEndpointsRequestRequestTypeDef,
    ListMarketplaceModelEndpointsResponseTypeDef,
    ListModelCopyJobsRequestRequestTypeDef,
    ListModelCopyJobsResponseTypeDef,
    ListModelCustomizationJobsRequestRequestTypeDef,
    ListModelCustomizationJobsResponseTypeDef,
    ListModelImportJobsRequestRequestTypeDef,
    ListModelImportJobsResponseTypeDef,
    ListModelInvocationJobsRequestRequestTypeDef,
    ListModelInvocationJobsResponseTypeDef,
    ListPromptRoutersRequestRequestTypeDef,
    ListPromptRoutersResponseTypeDef,
    ListProvisionedModelThroughputsRequestRequestTypeDef,
    ListProvisionedModelThroughputsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutModelInvocationLoggingConfigurationRequestRequestTypeDef,
    RegisterMarketplaceModelEndpointRequestRequestTypeDef,
    RegisterMarketplaceModelEndpointResponseTypeDef,
    StopEvaluationJobRequestRequestTypeDef,
    StopModelCustomizationJobRequestRequestTypeDef,
    StopModelInvocationJobRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateGuardrailRequestRequestTypeDef,
    UpdateGuardrailResponseTypeDef,
    UpdateMarketplaceModelEndpointRequestRequestTypeDef,
    UpdateMarketplaceModelEndpointResponseTypeDef,
    UpdateProvisionedModelThroughputRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("BedrockClient",)


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
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class BedrockClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BedrockClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#close)
        """

    def batch_delete_evaluation_job(
        self, **kwargs: Unpack[BatchDeleteEvaluationJobRequestRequestTypeDef]
    ) -> BatchDeleteEvaluationJobResponseTypeDef:
        """
        Deletes a batch of evaluation jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/batch_delete_evaluation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#batch_delete_evaluation_job)
        """

    def create_evaluation_job(
        self, **kwargs: Unpack[CreateEvaluationJobRequestRequestTypeDef]
    ) -> CreateEvaluationJobResponseTypeDef:
        """
        Creates an evaluation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_evaluation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#create_evaluation_job)
        """

    def create_guardrail(
        self, **kwargs: Unpack[CreateGuardrailRequestRequestTypeDef]
    ) -> CreateGuardrailResponseTypeDef:
        """
        Creates a guardrail to block topics and to implement safeguards for your
        generative AI applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_guardrail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#create_guardrail)
        """

    def create_guardrail_version(
        self, **kwargs: Unpack[CreateGuardrailVersionRequestRequestTypeDef]
    ) -> CreateGuardrailVersionResponseTypeDef:
        """
        Creates a version of the guardrail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_guardrail_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#create_guardrail_version)
        """

    def create_inference_profile(
        self, **kwargs: Unpack[CreateInferenceProfileRequestRequestTypeDef]
    ) -> CreateInferenceProfileResponseTypeDef:
        """
        Creates an application inference profile to track metrics and costs when
        invoking a model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_inference_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#create_inference_profile)
        """

    def create_marketplace_model_endpoint(
        self, **kwargs: Unpack[CreateMarketplaceModelEndpointRequestRequestTypeDef]
    ) -> CreateMarketplaceModelEndpointResponseTypeDef:
        """
        Creates an endpoint for a model from Amazon Bedrock Marketplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_marketplace_model_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#create_marketplace_model_endpoint)
        """

    def create_model_copy_job(
        self, **kwargs: Unpack[CreateModelCopyJobRequestRequestTypeDef]
    ) -> CreateModelCopyJobResponseTypeDef:
        """
        Copies a model to another region so that it can be used there.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_model_copy_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#create_model_copy_job)
        """

    def create_model_customization_job(
        self, **kwargs: Unpack[CreateModelCustomizationJobRequestRequestTypeDef]
    ) -> CreateModelCustomizationJobResponseTypeDef:
        """
        Creates a fine-tuning job to customize a base model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_model_customization_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#create_model_customization_job)
        """

    def create_model_import_job(
        self, **kwargs: Unpack[CreateModelImportJobRequestRequestTypeDef]
    ) -> CreateModelImportJobResponseTypeDef:
        """
        Creates a model import job to import model that you have customized in other
        environments, such as Amazon SageMaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_model_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#create_model_import_job)
        """

    def create_model_invocation_job(
        self, **kwargs: Unpack[CreateModelInvocationJobRequestRequestTypeDef]
    ) -> CreateModelInvocationJobResponseTypeDef:
        """
        Creates a batch inference job to invoke a model on multiple prompts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_model_invocation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#create_model_invocation_job)
        """

    def create_provisioned_model_throughput(
        self, **kwargs: Unpack[CreateProvisionedModelThroughputRequestRequestTypeDef]
    ) -> CreateProvisionedModelThroughputResponseTypeDef:
        """
        Creates dedicated throughput for a base or custom model with the model units
        and for the duration that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/create_provisioned_model_throughput.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#create_provisioned_model_throughput)
        """

    def delete_custom_model(
        self, **kwargs: Unpack[DeleteCustomModelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a custom model that you created earlier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/delete_custom_model.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#delete_custom_model)
        """

    def delete_guardrail(
        self, **kwargs: Unpack[DeleteGuardrailRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a guardrail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/delete_guardrail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#delete_guardrail)
        """

    def delete_imported_model(
        self, **kwargs: Unpack[DeleteImportedModelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a custom model that you imported earlier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/delete_imported_model.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#delete_imported_model)
        """

    def delete_inference_profile(
        self, **kwargs: Unpack[DeleteInferenceProfileRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an application inference profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/delete_inference_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#delete_inference_profile)
        """

    def delete_marketplace_model_endpoint(
        self, **kwargs: Unpack[DeleteMarketplaceModelEndpointRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an endpoint for a model from Amazon Bedrock Marketplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/delete_marketplace_model_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#delete_marketplace_model_endpoint)
        """

    def delete_model_invocation_logging_configuration(self) -> Dict[str, Any]:
        """
        Delete the invocation logging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/delete_model_invocation_logging_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#delete_model_invocation_logging_configuration)
        """

    def delete_provisioned_model_throughput(
        self, **kwargs: Unpack[DeleteProvisionedModelThroughputRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Provisioned Throughput.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/delete_provisioned_model_throughput.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#delete_provisioned_model_throughput)
        """

    def deregister_marketplace_model_endpoint(
        self, **kwargs: Unpack[DeregisterMarketplaceModelEndpointRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deregisters an endpoint for a model from Amazon Bedrock Marketplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/deregister_marketplace_model_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#deregister_marketplace_model_endpoint)
        """

    def get_custom_model(
        self, **kwargs: Unpack[GetCustomModelRequestRequestTypeDef]
    ) -> GetCustomModelResponseTypeDef:
        """
        Get the properties associated with a Amazon Bedrock custom model that you have
        created.For more information, see <a
        href="https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html">Custom
        models</a> in the <a
        href="https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service...

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_custom_model.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_custom_model)
        """

    def get_evaluation_job(
        self, **kwargs: Unpack[GetEvaluationJobRequestRequestTypeDef]
    ) -> GetEvaluationJobResponseTypeDef:
        """
        Gets information about an evaluation job, such as the status of the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_evaluation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_evaluation_job)
        """

    def get_foundation_model(
        self, **kwargs: Unpack[GetFoundationModelRequestRequestTypeDef]
    ) -> GetFoundationModelResponseTypeDef:
        """
        Get details about a Amazon Bedrock foundation model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_foundation_model.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_foundation_model)
        """

    def get_guardrail(
        self, **kwargs: Unpack[GetGuardrailRequestRequestTypeDef]
    ) -> GetGuardrailResponseTypeDef:
        """
        Gets details about a guardrail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_guardrail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_guardrail)
        """

    def get_imported_model(
        self, **kwargs: Unpack[GetImportedModelRequestRequestTypeDef]
    ) -> GetImportedModelResponseTypeDef:
        """
        Gets properties associated with a customized model you imported.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_imported_model.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_imported_model)
        """

    def get_inference_profile(
        self, **kwargs: Unpack[GetInferenceProfileRequestRequestTypeDef]
    ) -> GetInferenceProfileResponseTypeDef:
        """
        Gets information about an inference profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_inference_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_inference_profile)
        """

    def get_marketplace_model_endpoint(
        self, **kwargs: Unpack[GetMarketplaceModelEndpointRequestRequestTypeDef]
    ) -> GetMarketplaceModelEndpointResponseTypeDef:
        """
        Retrieves details about a specific endpoint for a model from Amazon Bedrock
        Marketplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_marketplace_model_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_marketplace_model_endpoint)
        """

    def get_model_copy_job(
        self, **kwargs: Unpack[GetModelCopyJobRequestRequestTypeDef]
    ) -> GetModelCopyJobResponseTypeDef:
        """
        Retrieves information about a model copy job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_model_copy_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_model_copy_job)
        """

    def get_model_customization_job(
        self, **kwargs: Unpack[GetModelCustomizationJobRequestRequestTypeDef]
    ) -> GetModelCustomizationJobResponseTypeDef:
        """
        Retrieves the properties associated with a model-customization job, including
        the status of the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_model_customization_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_model_customization_job)
        """

    def get_model_import_job(
        self, **kwargs: Unpack[GetModelImportJobRequestRequestTypeDef]
    ) -> GetModelImportJobResponseTypeDef:
        """
        Retrieves the properties associated with import model job, including the status
        of the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_model_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_model_import_job)
        """

    def get_model_invocation_job(
        self, **kwargs: Unpack[GetModelInvocationJobRequestRequestTypeDef]
    ) -> GetModelInvocationJobResponseTypeDef:
        """
        Gets details about a batch inference job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_model_invocation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_model_invocation_job)
        """

    def get_model_invocation_logging_configuration(
        self,
    ) -> GetModelInvocationLoggingConfigurationResponseTypeDef:
        """
        Get the current configuration values for model invocation logging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_model_invocation_logging_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_model_invocation_logging_configuration)
        """

    def get_prompt_router(
        self, **kwargs: Unpack[GetPromptRouterRequestRequestTypeDef]
    ) -> GetPromptRouterResponseTypeDef:
        """
        Retrieves details about a prompt router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_prompt_router.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_prompt_router)
        """

    def get_provisioned_model_throughput(
        self, **kwargs: Unpack[GetProvisionedModelThroughputRequestRequestTypeDef]
    ) -> GetProvisionedModelThroughputResponseTypeDef:
        """
        Returns details for a Provisioned Throughput.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_provisioned_model_throughput.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_provisioned_model_throughput)
        """

    def list_custom_models(
        self, **kwargs: Unpack[ListCustomModelsRequestRequestTypeDef]
    ) -> ListCustomModelsResponseTypeDef:
        """
        Returns a list of the custom models that you have created with the
        <code>CreateModelCustomizationJob</code> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_custom_models.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#list_custom_models)
        """

    def list_evaluation_jobs(
        self, **kwargs: Unpack[ListEvaluationJobsRequestRequestTypeDef]
    ) -> ListEvaluationJobsResponseTypeDef:
        """
        Lists all existing evaluation jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_evaluation_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#list_evaluation_jobs)
        """

    def list_foundation_models(
        self, **kwargs: Unpack[ListFoundationModelsRequestRequestTypeDef]
    ) -> ListFoundationModelsResponseTypeDef:
        """
        Lists Amazon Bedrock foundation models that you can use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_foundation_models.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#list_foundation_models)
        """

    def list_guardrails(
        self, **kwargs: Unpack[ListGuardrailsRequestRequestTypeDef]
    ) -> ListGuardrailsResponseTypeDef:
        """
        Lists details about all the guardrails in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_guardrails.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#list_guardrails)
        """

    def list_imported_models(
        self, **kwargs: Unpack[ListImportedModelsRequestRequestTypeDef]
    ) -> ListImportedModelsResponseTypeDef:
        """
        Returns a list of models you've imported.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_imported_models.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#list_imported_models)
        """

    def list_inference_profiles(
        self, **kwargs: Unpack[ListInferenceProfilesRequestRequestTypeDef]
    ) -> ListInferenceProfilesResponseTypeDef:
        """
        Returns a list of inference profiles that you can use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_inference_profiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#list_inference_profiles)
        """

    def list_marketplace_model_endpoints(
        self, **kwargs: Unpack[ListMarketplaceModelEndpointsRequestRequestTypeDef]
    ) -> ListMarketplaceModelEndpointsResponseTypeDef:
        """
        Lists the endpoints for models from Amazon Bedrock Marketplace in your Amazon
        Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_marketplace_model_endpoints.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#list_marketplace_model_endpoints)
        """

    def list_model_copy_jobs(
        self, **kwargs: Unpack[ListModelCopyJobsRequestRequestTypeDef]
    ) -> ListModelCopyJobsResponseTypeDef:
        """
        Returns a list of model copy jobs that you have submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_model_copy_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#list_model_copy_jobs)
        """

    def list_model_customization_jobs(
        self, **kwargs: Unpack[ListModelCustomizationJobsRequestRequestTypeDef]
    ) -> ListModelCustomizationJobsResponseTypeDef:
        """
        Returns a list of model customization jobs that you have submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_model_customization_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#list_model_customization_jobs)
        """

    def list_model_import_jobs(
        self, **kwargs: Unpack[ListModelImportJobsRequestRequestTypeDef]
    ) -> ListModelImportJobsResponseTypeDef:
        """
        Returns a list of import jobs you've submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_model_import_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#list_model_import_jobs)
        """

    def list_model_invocation_jobs(
        self, **kwargs: Unpack[ListModelInvocationJobsRequestRequestTypeDef]
    ) -> ListModelInvocationJobsResponseTypeDef:
        """
        Lists all batch inference jobs in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_model_invocation_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#list_model_invocation_jobs)
        """

    def list_prompt_routers(
        self, **kwargs: Unpack[ListPromptRoutersRequestRequestTypeDef]
    ) -> ListPromptRoutersResponseTypeDef:
        """
        Retrieves a list of prompt routers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_prompt_routers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#list_prompt_routers)
        """

    def list_provisioned_model_throughputs(
        self, **kwargs: Unpack[ListProvisionedModelThroughputsRequestRequestTypeDef]
    ) -> ListProvisionedModelThroughputsResponseTypeDef:
        """
        Lists the Provisioned Throughputs in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_provisioned_model_throughputs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#list_provisioned_model_throughputs)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List the tags associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#list_tags_for_resource)
        """

    def put_model_invocation_logging_configuration(
        self, **kwargs: Unpack[PutModelInvocationLoggingConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Set the configuration values for model invocation logging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/put_model_invocation_logging_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#put_model_invocation_logging_configuration)
        """

    def register_marketplace_model_endpoint(
        self, **kwargs: Unpack[RegisterMarketplaceModelEndpointRequestRequestTypeDef]
    ) -> RegisterMarketplaceModelEndpointResponseTypeDef:
        """
        Registers an existing Amazon SageMaker endpoint with Amazon Bedrock
        Marketplace, allowing it to be used with Amazon Bedrock APIs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/register_marketplace_model_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#register_marketplace_model_endpoint)
        """

    def stop_evaluation_job(
        self, **kwargs: Unpack[StopEvaluationJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops an evaluation job that is current being created or running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/stop_evaluation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#stop_evaluation_job)
        """

    def stop_model_customization_job(
        self, **kwargs: Unpack[StopModelCustomizationJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops an active model customization job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/stop_model_customization_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#stop_model_customization_job)
        """

    def stop_model_invocation_job(
        self, **kwargs: Unpack[StopModelInvocationJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops a batch inference job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/stop_model_invocation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#stop_model_invocation_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Associate tags with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#untag_resource)
        """

    def update_guardrail(
        self, **kwargs: Unpack[UpdateGuardrailRequestRequestTypeDef]
    ) -> UpdateGuardrailResponseTypeDef:
        """
        Updates a guardrail with the values you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/update_guardrail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#update_guardrail)
        """

    def update_marketplace_model_endpoint(
        self, **kwargs: Unpack[UpdateMarketplaceModelEndpointRequestRequestTypeDef]
    ) -> UpdateMarketplaceModelEndpointResponseTypeDef:
        """
        Updates the configuration of an existing endpoint for a model from Amazon
        Bedrock Marketplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/update_marketplace_model_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#update_marketplace_model_endpoint)
        """

    def update_provisioned_model_throughput(
        self, **kwargs: Unpack[UpdateProvisionedModelThroughputRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the name or associated model for a Provisioned Throughput.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/update_provisioned_model_throughput.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#update_provisioned_model_throughput)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_models"]
    ) -> ListCustomModelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_evaluation_jobs"]
    ) -> ListEvaluationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_guardrails"]) -> ListGuardrailsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_imported_models"]
    ) -> ListImportedModelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_inference_profiles"]
    ) -> ListInferenceProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_marketplace_model_endpoints"]
    ) -> ListMarketplaceModelEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_copy_jobs"]
    ) -> ListModelCopyJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_customization_jobs"]
    ) -> ListModelCustomizationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_import_jobs"]
    ) -> ListModelImportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_invocation_jobs"]
    ) -> ListModelInvocationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_prompt_routers"]
    ) -> ListPromptRoutersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_provisioned_model_throughputs"]
    ) -> ListProvisionedModelThroughputsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/client/#get_paginator)
        """
