"""
Type annotations for ecr-public service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_ecr_public.client import ECRPublicClient

    session = Session()
    client: ECRPublicClient = session.client("ecr-public")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeImagesPaginator,
    DescribeImageTagsPaginator,
    DescribeRegistriesPaginator,
    DescribeRepositoriesPaginator,
)
from .type_defs import (
    BatchCheckLayerAvailabilityRequestRequestTypeDef,
    BatchCheckLayerAvailabilityResponseTypeDef,
    BatchDeleteImageRequestRequestTypeDef,
    BatchDeleteImageResponseTypeDef,
    CompleteLayerUploadRequestRequestTypeDef,
    CompleteLayerUploadResponseTypeDef,
    CreateRepositoryRequestRequestTypeDef,
    CreateRepositoryResponseTypeDef,
    DeleteRepositoryPolicyRequestRequestTypeDef,
    DeleteRepositoryPolicyResponseTypeDef,
    DeleteRepositoryRequestRequestTypeDef,
    DeleteRepositoryResponseTypeDef,
    DescribeImagesRequestRequestTypeDef,
    DescribeImagesResponseTypeDef,
    DescribeImageTagsRequestRequestTypeDef,
    DescribeImageTagsResponseTypeDef,
    DescribeRegistriesRequestRequestTypeDef,
    DescribeRegistriesResponseTypeDef,
    DescribeRepositoriesRequestRequestTypeDef,
    DescribeRepositoriesResponseTypeDef,
    GetAuthorizationTokenResponseTypeDef,
    GetRegistryCatalogDataResponseTypeDef,
    GetRepositoryCatalogDataRequestRequestTypeDef,
    GetRepositoryCatalogDataResponseTypeDef,
    GetRepositoryPolicyRequestRequestTypeDef,
    GetRepositoryPolicyResponseTypeDef,
    InitiateLayerUploadRequestRequestTypeDef,
    InitiateLayerUploadResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutImageRequestRequestTypeDef,
    PutImageResponseTypeDef,
    PutRegistryCatalogDataRequestRequestTypeDef,
    PutRegistryCatalogDataResponseTypeDef,
    PutRepositoryCatalogDataRequestRequestTypeDef,
    PutRepositoryCatalogDataResponseTypeDef,
    SetRepositoryPolicyRequestRequestTypeDef,
    SetRepositoryPolicyResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UploadLayerPartRequestRequestTypeDef,
    UploadLayerPartResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ECRPublicClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    EmptyUploadException: Type[BotocoreClientError]
    ImageAlreadyExistsException: Type[BotocoreClientError]
    ImageDigestDoesNotMatchException: Type[BotocoreClientError]
    ImageNotFoundException: Type[BotocoreClientError]
    ImageTagAlreadyExistsException: Type[BotocoreClientError]
    InvalidLayerException: Type[BotocoreClientError]
    InvalidLayerPartException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidTagParameterException: Type[BotocoreClientError]
    LayerAlreadyExistsException: Type[BotocoreClientError]
    LayerPartTooSmallException: Type[BotocoreClientError]
    LayersNotFoundException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ReferencedImagesNotFoundException: Type[BotocoreClientError]
    RegistryNotFoundException: Type[BotocoreClientError]
    RepositoryAlreadyExistsException: Type[BotocoreClientError]
    RepositoryCatalogDataNotFoundException: Type[BotocoreClientError]
    RepositoryNotEmptyException: Type[BotocoreClientError]
    RepositoryNotFoundException: Type[BotocoreClientError]
    RepositoryPolicyNotFoundException: Type[BotocoreClientError]
    ServerException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnsupportedCommandException: Type[BotocoreClientError]
    UploadNotFoundException: Type[BotocoreClientError]


class ECRPublicClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ECRPublicClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#close)
        """

    def batch_check_layer_availability(
        self, **kwargs: Unpack[BatchCheckLayerAvailabilityRequestRequestTypeDef]
    ) -> BatchCheckLayerAvailabilityResponseTypeDef:
        """
        Checks the availability of one or more image layers that are within a
        repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/batch_check_layer_availability.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#batch_check_layer_availability)
        """

    def batch_delete_image(
        self, **kwargs: Unpack[BatchDeleteImageRequestRequestTypeDef]
    ) -> BatchDeleteImageResponseTypeDef:
        """
        Deletes a list of specified images that are within a repository in a public
        registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/batch_delete_image.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#batch_delete_image)
        """

    def complete_layer_upload(
        self, **kwargs: Unpack[CompleteLayerUploadRequestRequestTypeDef]
    ) -> CompleteLayerUploadResponseTypeDef:
        """
        Informs Amazon ECR that the image layer upload is complete for a specified
        public registry, repository name, and upload ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/complete_layer_upload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#complete_layer_upload)
        """

    def create_repository(
        self, **kwargs: Unpack[CreateRepositoryRequestRequestTypeDef]
    ) -> CreateRepositoryResponseTypeDef:
        """
        Creates a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/create_repository.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#create_repository)
        """

    def delete_repository(
        self, **kwargs: Unpack[DeleteRepositoryRequestRequestTypeDef]
    ) -> DeleteRepositoryResponseTypeDef:
        """
        Deletes a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/delete_repository.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#delete_repository)
        """

    def delete_repository_policy(
        self, **kwargs: Unpack[DeleteRepositoryPolicyRequestRequestTypeDef]
    ) -> DeleteRepositoryPolicyResponseTypeDef:
        """
        Deletes the repository policy that's associated with the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/delete_repository_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#delete_repository_policy)
        """

    def describe_image_tags(
        self, **kwargs: Unpack[DescribeImageTagsRequestRequestTypeDef]
    ) -> DescribeImageTagsResponseTypeDef:
        """
        Returns the image tag details for a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/describe_image_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#describe_image_tags)
        """

    def describe_images(
        self, **kwargs: Unpack[DescribeImagesRequestRequestTypeDef]
    ) -> DescribeImagesResponseTypeDef:
        """
        Returns metadata that's related to the images in a repository in a public
        registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/describe_images.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#describe_images)
        """

    def describe_registries(
        self, **kwargs: Unpack[DescribeRegistriesRequestRequestTypeDef]
    ) -> DescribeRegistriesResponseTypeDef:
        """
        Returns details for a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/describe_registries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#describe_registries)
        """

    def describe_repositories(
        self, **kwargs: Unpack[DescribeRepositoriesRequestRequestTypeDef]
    ) -> DescribeRepositoriesResponseTypeDef:
        """
        Describes repositories that are in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/describe_repositories.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#describe_repositories)
        """

    def get_authorization_token(self) -> GetAuthorizationTokenResponseTypeDef:
        """
        Retrieves an authorization token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/get_authorization_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#get_authorization_token)
        """

    def get_registry_catalog_data(self) -> GetRegistryCatalogDataResponseTypeDef:
        """
        Retrieves catalog metadata for a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/get_registry_catalog_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#get_registry_catalog_data)
        """

    def get_repository_catalog_data(
        self, **kwargs: Unpack[GetRepositoryCatalogDataRequestRequestTypeDef]
    ) -> GetRepositoryCatalogDataResponseTypeDef:
        """
        Retrieve catalog metadata for a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/get_repository_catalog_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#get_repository_catalog_data)
        """

    def get_repository_policy(
        self, **kwargs: Unpack[GetRepositoryPolicyRequestRequestTypeDef]
    ) -> GetRepositoryPolicyResponseTypeDef:
        """
        Retrieves the repository policy for the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/get_repository_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#get_repository_policy)
        """

    def initiate_layer_upload(
        self, **kwargs: Unpack[InitiateLayerUploadRequestRequestTypeDef]
    ) -> InitiateLayerUploadResponseTypeDef:
        """
        Notifies Amazon ECR that you intend to upload an image layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/initiate_layer_upload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#initiate_layer_upload)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List the tags for an Amazon ECR Public resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#list_tags_for_resource)
        """

    def put_image(self, **kwargs: Unpack[PutImageRequestRequestTypeDef]) -> PutImageResponseTypeDef:
        """
        Creates or updates the image manifest and tags that are associated with an
        image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/put_image.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#put_image)
        """

    def put_registry_catalog_data(
        self, **kwargs: Unpack[PutRegistryCatalogDataRequestRequestTypeDef]
    ) -> PutRegistryCatalogDataResponseTypeDef:
        """
        Create or update the catalog data for a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/put_registry_catalog_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#put_registry_catalog_data)
        """

    def put_repository_catalog_data(
        self, **kwargs: Unpack[PutRepositoryCatalogDataRequestRequestTypeDef]
    ) -> PutRepositoryCatalogDataResponseTypeDef:
        """
        Creates or updates the catalog data for a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/put_repository_catalog_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#put_repository_catalog_data)
        """

    def set_repository_policy(
        self, **kwargs: Unpack[SetRepositoryPolicyRequestRequestTypeDef]
    ) -> SetRepositoryPolicyResponseTypeDef:
        """
        Applies a repository policy to the specified public repository to control
        access permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/set_repository_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#set_repository_policy)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified
        <code>resourceArn</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#untag_resource)
        """

    def upload_layer_part(
        self, **kwargs: Unpack[UploadLayerPartRequestRequestTypeDef]
    ) -> UploadLayerPartResponseTypeDef:
        """
        Uploads an image layer part to Amazon ECR.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/upload_layer_part.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#upload_layer_part)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_image_tags"]
    ) -> DescribeImageTagsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_images"]) -> DescribeImagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_registries"]
    ) -> DescribeRegistriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_repositories"]
    ) -> DescribeRepositoriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr_public/client/#get_paginator)
        """
