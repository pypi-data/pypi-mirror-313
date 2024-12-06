"""
Type annotations for b2bi service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_b2bi.client import B2BIClient

    session = Session()
    client: B2BIClient = session.client("b2bi")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListCapabilitiesPaginator,
    ListPartnershipsPaginator,
    ListProfilesPaginator,
    ListTransformersPaginator,
)
from .type_defs import (
    CreateCapabilityRequestRequestTypeDef,
    CreateCapabilityResponseTypeDef,
    CreatePartnershipRequestRequestTypeDef,
    CreatePartnershipResponseTypeDef,
    CreateProfileRequestRequestTypeDef,
    CreateProfileResponseTypeDef,
    CreateStarterMappingTemplateRequestRequestTypeDef,
    CreateStarterMappingTemplateResponseTypeDef,
    CreateTransformerRequestRequestTypeDef,
    CreateTransformerResponseTypeDef,
    DeleteCapabilityRequestRequestTypeDef,
    DeletePartnershipRequestRequestTypeDef,
    DeleteProfileRequestRequestTypeDef,
    DeleteTransformerRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GenerateMappingRequestRequestTypeDef,
    GenerateMappingResponseTypeDef,
    GetCapabilityRequestRequestTypeDef,
    GetCapabilityResponseTypeDef,
    GetPartnershipRequestRequestTypeDef,
    GetPartnershipResponseTypeDef,
    GetProfileRequestRequestTypeDef,
    GetProfileResponseTypeDef,
    GetTransformerJobRequestRequestTypeDef,
    GetTransformerJobResponseTypeDef,
    GetTransformerRequestRequestTypeDef,
    GetTransformerResponseTypeDef,
    ListCapabilitiesRequestRequestTypeDef,
    ListCapabilitiesResponseTypeDef,
    ListPartnershipsRequestRequestTypeDef,
    ListPartnershipsResponseTypeDef,
    ListProfilesRequestRequestTypeDef,
    ListProfilesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTransformersRequestRequestTypeDef,
    ListTransformersResponseTypeDef,
    StartTransformerJobRequestRequestTypeDef,
    StartTransformerJobResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    TestConversionRequestRequestTypeDef,
    TestConversionResponseTypeDef,
    TestMappingRequestRequestTypeDef,
    TestMappingResponseTypeDef,
    TestParsingRequestRequestTypeDef,
    TestParsingResponseTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateCapabilityRequestRequestTypeDef,
    UpdateCapabilityResponseTypeDef,
    UpdatePartnershipRequestRequestTypeDef,
    UpdatePartnershipResponseTypeDef,
    UpdateProfileRequestRequestTypeDef,
    UpdateProfileResponseTypeDef,
    UpdateTransformerRequestRequestTypeDef,
    UpdateTransformerResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("B2BIClient",)

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
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class B2BIClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        B2BIClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#close)
        """

    def create_capability(
        self, **kwargs: Unpack[CreateCapabilityRequestRequestTypeDef]
    ) -> CreateCapabilityResponseTypeDef:
        """
        Instantiates a capability based on the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/create_capability.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#create_capability)
        """

    def create_partnership(
        self, **kwargs: Unpack[CreatePartnershipRequestRequestTypeDef]
    ) -> CreatePartnershipResponseTypeDef:
        """
        Creates a partnership between a customer and a trading partner, based on the
        supplied parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/create_partnership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#create_partnership)
        """

    def create_profile(
        self, **kwargs: Unpack[CreateProfileRequestRequestTypeDef]
    ) -> CreateProfileResponseTypeDef:
        """
        Creates a customer profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/create_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#create_profile)
        """

    def create_starter_mapping_template(
        self, **kwargs: Unpack[CreateStarterMappingTemplateRequestRequestTypeDef]
    ) -> CreateStarterMappingTemplateResponseTypeDef:
        """
        Amazon Web Services B2B Data Interchange uses a mapping template in JSONata or
        XSLT format to transform a customer input file into a JSON or XML file that can
        be converted to EDI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/create_starter_mapping_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#create_starter_mapping_template)
        """

    def create_transformer(
        self, **kwargs: Unpack[CreateTransformerRequestRequestTypeDef]
    ) -> CreateTransformerResponseTypeDef:
        """
        Creates a transformer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/create_transformer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#create_transformer)
        """

    def delete_capability(
        self, **kwargs: Unpack[DeleteCapabilityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified capability.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/delete_capability.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#delete_capability)
        """

    def delete_partnership(
        self, **kwargs: Unpack[DeletePartnershipRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified partnership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/delete_partnership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#delete_partnership)
        """

    def delete_profile(
        self, **kwargs: Unpack[DeleteProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/delete_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#delete_profile)
        """

    def delete_transformer(
        self, **kwargs: Unpack[DeleteTransformerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified transformer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/delete_transformer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#delete_transformer)
        """

    def generate_mapping(
        self, **kwargs: Unpack[GenerateMappingRequestRequestTypeDef]
    ) -> GenerateMappingResponseTypeDef:
        """
        Takes sample input and output documents and uses Amazon Bedrock to generate a
        mapping automatically.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/generate_mapping.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#generate_mapping)
        """

    def get_capability(
        self, **kwargs: Unpack[GetCapabilityRequestRequestTypeDef]
    ) -> GetCapabilityResponseTypeDef:
        """
        Retrieves the details for the specified capability.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/get_capability.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#get_capability)
        """

    def get_partnership(
        self, **kwargs: Unpack[GetPartnershipRequestRequestTypeDef]
    ) -> GetPartnershipResponseTypeDef:
        """
        Retrieves the details for a partnership, based on the partner and profile IDs
        specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/get_partnership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#get_partnership)
        """

    def get_profile(
        self, **kwargs: Unpack[GetProfileRequestRequestTypeDef]
    ) -> GetProfileResponseTypeDef:
        """
        Retrieves the details for the profile specified by the profile ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/get_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#get_profile)
        """

    def get_transformer(
        self, **kwargs: Unpack[GetTransformerRequestRequestTypeDef]
    ) -> GetTransformerResponseTypeDef:
        """
        Retrieves the details for the transformer specified by the transformer ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/get_transformer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#get_transformer)
        """

    def get_transformer_job(
        self, **kwargs: Unpack[GetTransformerJobRequestRequestTypeDef]
    ) -> GetTransformerJobResponseTypeDef:
        """
        Returns the details of the transformer run, based on the Transformer job ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/get_transformer_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#get_transformer_job)
        """

    def list_capabilities(
        self, **kwargs: Unpack[ListCapabilitiesRequestRequestTypeDef]
    ) -> ListCapabilitiesResponseTypeDef:
        """
        Lists the capabilities associated with your Amazon Web Services account for
        your current or specified region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/list_capabilities.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#list_capabilities)
        """

    def list_partnerships(
        self, **kwargs: Unpack[ListPartnershipsRequestRequestTypeDef]
    ) -> ListPartnershipsResponseTypeDef:
        """
        Lists the partnerships associated with your Amazon Web Services account for
        your current or specified region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/list_partnerships.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#list_partnerships)
        """

    def list_profiles(
        self, **kwargs: Unpack[ListProfilesRequestRequestTypeDef]
    ) -> ListProfilesResponseTypeDef:
        """
        Lists the profiles associated with your Amazon Web Services account for your
        current or specified region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/list_profiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#list_profiles)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all of the tags associated with the Amazon Resource Name (ARN) that you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#list_tags_for_resource)
        """

    def list_transformers(
        self, **kwargs: Unpack[ListTransformersRequestRequestTypeDef]
    ) -> ListTransformersResponseTypeDef:
        """
        Lists the available transformers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/list_transformers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#list_transformers)
        """

    def start_transformer_job(
        self, **kwargs: Unpack[StartTransformerJobRequestRequestTypeDef]
    ) -> StartTransformerJobResponseTypeDef:
        """
        Runs a job, using a transformer, to parse input EDI (electronic data
        interchange) file into the output structures used by Amazon Web Services B2B
        Data Interchange.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/start_transformer_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#start_transformer_job)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches a key-value pair to a resource, as identified by its Amazon Resource
        Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#tag_resource)
        """

    def test_conversion(
        self, **kwargs: Unpack[TestConversionRequestRequestTypeDef]
    ) -> TestConversionResponseTypeDef:
        """
        This operation mimics the latter half of a typical Outbound EDI request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/test_conversion.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#test_conversion)
        """

    def test_mapping(
        self, **kwargs: Unpack[TestMappingRequestRequestTypeDef]
    ) -> TestMappingResponseTypeDef:
        """
        Maps the input file according to the provided template file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/test_mapping.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#test_mapping)
        """

    def test_parsing(
        self, **kwargs: Unpack[TestParsingRequestRequestTypeDef]
    ) -> TestParsingResponseTypeDef:
        """
        Parses the input EDI (electronic data interchange) file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/test_parsing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#test_parsing)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Detaches a key-value pair from the specified resource, as identified by its
        Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#untag_resource)
        """

    def update_capability(
        self, **kwargs: Unpack[UpdateCapabilityRequestRequestTypeDef]
    ) -> UpdateCapabilityResponseTypeDef:
        """
        Updates some of the parameters for a capability, based on the specified
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/update_capability.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#update_capability)
        """

    def update_partnership(
        self, **kwargs: Unpack[UpdatePartnershipRequestRequestTypeDef]
    ) -> UpdatePartnershipResponseTypeDef:
        """
        Updates some of the parameters for a partnership between a customer and trading
        partner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/update_partnership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#update_partnership)
        """

    def update_profile(
        self, **kwargs: Unpack[UpdateProfileRequestRequestTypeDef]
    ) -> UpdateProfileResponseTypeDef:
        """
        Updates the specified parameters for a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/update_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#update_profile)
        """

    def update_transformer(
        self, **kwargs: Unpack[UpdateTransformerRequestRequestTypeDef]
    ) -> UpdateTransformerResponseTypeDef:
        """
        Updates the specified parameters for a transformer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/update_transformer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#update_transformer)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_capabilities"]
    ) -> ListCapabilitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_partnerships"]
    ) -> ListPartnershipsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_profiles"]) -> ListProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_transformers"]
    ) -> ListTransformersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_b2bi/client/#get_paginator)
        """
