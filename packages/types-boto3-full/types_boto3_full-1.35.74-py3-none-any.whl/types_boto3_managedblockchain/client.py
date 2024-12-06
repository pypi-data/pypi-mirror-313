"""
Type annotations for managedblockchain service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_managedblockchain.client import ManagedBlockchainClient

    session = Session()
    client: ManagedBlockchainClient = session.client("managedblockchain")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import ListAccessorsPaginator
from .type_defs import (
    CreateAccessorInputRequestTypeDef,
    CreateAccessorOutputTypeDef,
    CreateMemberInputRequestTypeDef,
    CreateMemberOutputTypeDef,
    CreateNetworkInputRequestTypeDef,
    CreateNetworkOutputTypeDef,
    CreateNodeInputRequestTypeDef,
    CreateNodeOutputTypeDef,
    CreateProposalInputRequestTypeDef,
    CreateProposalOutputTypeDef,
    DeleteAccessorInputRequestTypeDef,
    DeleteMemberInputRequestTypeDef,
    DeleteNodeInputRequestTypeDef,
    GetAccessorInputRequestTypeDef,
    GetAccessorOutputTypeDef,
    GetMemberInputRequestTypeDef,
    GetMemberOutputTypeDef,
    GetNetworkInputRequestTypeDef,
    GetNetworkOutputTypeDef,
    GetNodeInputRequestTypeDef,
    GetNodeOutputTypeDef,
    GetProposalInputRequestTypeDef,
    GetProposalOutputTypeDef,
    ListAccessorsInputRequestTypeDef,
    ListAccessorsOutputTypeDef,
    ListInvitationsInputRequestTypeDef,
    ListInvitationsOutputTypeDef,
    ListMembersInputRequestTypeDef,
    ListMembersOutputTypeDef,
    ListNetworksInputRequestTypeDef,
    ListNetworksOutputTypeDef,
    ListNodesInputRequestTypeDef,
    ListNodesOutputTypeDef,
    ListProposalsInputRequestTypeDef,
    ListProposalsOutputTypeDef,
    ListProposalVotesInputRequestTypeDef,
    ListProposalVotesOutputTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RejectInvitationInputRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateMemberInputRequestTypeDef,
    UpdateNodeInputRequestTypeDef,
    VoteOnProposalInputRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ManagedBlockchainClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    IllegalActionException: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceNotReadyException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]


class ManagedBlockchainClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ManagedBlockchainClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#close)
        """

    def create_accessor(
        self, **kwargs: Unpack[CreateAccessorInputRequestTypeDef]
    ) -> CreateAccessorOutputTypeDef:
        """
        Creates a new accessor for use with Amazon Managed Blockchain service that
        supports token based access.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/create_accessor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#create_accessor)
        """

    def create_member(
        self, **kwargs: Unpack[CreateMemberInputRequestTypeDef]
    ) -> CreateMemberOutputTypeDef:
        """
        Creates a member within a Managed Blockchain network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/create_member.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#create_member)
        """

    def create_network(
        self, **kwargs: Unpack[CreateNetworkInputRequestTypeDef]
    ) -> CreateNetworkOutputTypeDef:
        """
        Creates a new blockchain network using Amazon Managed Blockchain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/create_network.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#create_network)
        """

    def create_node(
        self, **kwargs: Unpack[CreateNodeInputRequestTypeDef]
    ) -> CreateNodeOutputTypeDef:
        """
        Creates a node on the specified blockchain network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/create_node.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#create_node)
        """

    def create_proposal(
        self, **kwargs: Unpack[CreateProposalInputRequestTypeDef]
    ) -> CreateProposalOutputTypeDef:
        """
        Creates a proposal for a change to the network that other members of the
        network can vote on, for example, a proposal to add a new member to the
        network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/create_proposal.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#create_proposal)
        """

    def delete_accessor(
        self, **kwargs: Unpack[DeleteAccessorInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an accessor that your Amazon Web Services account owns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/delete_accessor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#delete_accessor)
        """

    def delete_member(self, **kwargs: Unpack[DeleteMemberInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/delete_member.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#delete_member)
        """

    def delete_node(self, **kwargs: Unpack[DeleteNodeInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a node that your Amazon Web Services account owns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/delete_node.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#delete_node)
        """

    def get_accessor(
        self, **kwargs: Unpack[GetAccessorInputRequestTypeDef]
    ) -> GetAccessorOutputTypeDef:
        """
        Returns detailed information about an accessor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/get_accessor.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#get_accessor)
        """

    def get_member(self, **kwargs: Unpack[GetMemberInputRequestTypeDef]) -> GetMemberOutputTypeDef:
        """
        Returns detailed information about a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/get_member.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#get_member)
        """

    def get_network(
        self, **kwargs: Unpack[GetNetworkInputRequestTypeDef]
    ) -> GetNetworkOutputTypeDef:
        """
        Returns detailed information about a network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/get_network.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#get_network)
        """

    def get_node(self, **kwargs: Unpack[GetNodeInputRequestTypeDef]) -> GetNodeOutputTypeDef:
        """
        Returns detailed information about a node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/get_node.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#get_node)
        """

    def get_proposal(
        self, **kwargs: Unpack[GetProposalInputRequestTypeDef]
    ) -> GetProposalOutputTypeDef:
        """
        Returns detailed information about a proposal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/get_proposal.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#get_proposal)
        """

    def list_accessors(
        self, **kwargs: Unpack[ListAccessorsInputRequestTypeDef]
    ) -> ListAccessorsOutputTypeDef:
        """
        Returns a list of the accessors and their properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/list_accessors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#list_accessors)
        """

    def list_invitations(
        self, **kwargs: Unpack[ListInvitationsInputRequestTypeDef]
    ) -> ListInvitationsOutputTypeDef:
        """
        Returns a list of all invitations for the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/list_invitations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#list_invitations)
        """

    def list_members(
        self, **kwargs: Unpack[ListMembersInputRequestTypeDef]
    ) -> ListMembersOutputTypeDef:
        """
        Returns a list of the members in a network and properties of their
        configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/list_members.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#list_members)
        """

    def list_networks(
        self, **kwargs: Unpack[ListNetworksInputRequestTypeDef]
    ) -> ListNetworksOutputTypeDef:
        """
        Returns information about the networks in which the current Amazon Web Services
        account participates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/list_networks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#list_networks)
        """

    def list_nodes(self, **kwargs: Unpack[ListNodesInputRequestTypeDef]) -> ListNodesOutputTypeDef:
        """
        Returns information about the nodes within a network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/list_nodes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#list_nodes)
        """

    def list_proposal_votes(
        self, **kwargs: Unpack[ListProposalVotesInputRequestTypeDef]
    ) -> ListProposalVotesOutputTypeDef:
        """
        Returns the list of votes for a specified proposal, including the value of each
        vote and the unique identifier of the member that cast the vote.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/list_proposal_votes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#list_proposal_votes)
        """

    def list_proposals(
        self, **kwargs: Unpack[ListProposalsInputRequestTypeDef]
    ) -> ListProposalsOutputTypeDef:
        """
        Returns a list of proposals for the network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/list_proposals.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#list_proposals)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#list_tags_for_resource)
        """

    def reject_invitation(
        self, **kwargs: Unpack[RejectInvitationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Rejects an invitation to join a network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/reject_invitation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#reject_invitation)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds or overwrites the specified tags for the specified Amazon Managed
        Blockchain resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified tags from the Amazon Managed Blockchain resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#untag_resource)
        """

    def update_member(self, **kwargs: Unpack[UpdateMemberInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates a member configuration with new parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/update_member.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#update_member)
        """

    def update_node(self, **kwargs: Unpack[UpdateNodeInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates a node configuration with new parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/update_node.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#update_node)
        """

    def vote_on_proposal(
        self, **kwargs: Unpack[VoteOnProposalInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Casts a vote for a specified <code>ProposalId</code> on behalf of a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/vote_on_proposal.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#vote_on_proposal)
        """

    def get_paginator(self, operation_name: Literal["list_accessors"]) -> ListAccessorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain/client/#get_paginator)
        """
