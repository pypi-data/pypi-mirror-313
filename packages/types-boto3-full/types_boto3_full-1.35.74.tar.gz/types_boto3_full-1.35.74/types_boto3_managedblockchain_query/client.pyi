"""
Type annotations for managedblockchain-query service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_managedblockchain_query.client import ManagedBlockchainQueryClient

    session = Session()
    client: ManagedBlockchainQueryClient = session.client("managedblockchain-query")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAssetContractsPaginator,
    ListFilteredTransactionEventsPaginator,
    ListTokenBalancesPaginator,
    ListTransactionEventsPaginator,
    ListTransactionsPaginator,
)
from .type_defs import (
    BatchGetTokenBalanceInputRequestTypeDef,
    BatchGetTokenBalanceOutputTypeDef,
    GetAssetContractInputRequestTypeDef,
    GetAssetContractOutputTypeDef,
    GetTokenBalanceInputRequestTypeDef,
    GetTokenBalanceOutputTypeDef,
    GetTransactionInputRequestTypeDef,
    GetTransactionOutputTypeDef,
    ListAssetContractsInputRequestTypeDef,
    ListAssetContractsOutputTypeDef,
    ListFilteredTransactionEventsInputRequestTypeDef,
    ListFilteredTransactionEventsOutputTypeDef,
    ListTokenBalancesInputRequestTypeDef,
    ListTokenBalancesOutputTypeDef,
    ListTransactionEventsInputRequestTypeDef,
    ListTransactionEventsOutputTypeDef,
    ListTransactionsInputRequestTypeDef,
    ListTransactionsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ManagedBlockchainQueryClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class ManagedBlockchainQueryClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query.html#ManagedBlockchainQuery.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ManagedBlockchainQueryClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query.html#ManagedBlockchainQuery.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#close)
        """

    def batch_get_token_balance(
        self, **kwargs: Unpack[BatchGetTokenBalanceInputRequestTypeDef]
    ) -> BatchGetTokenBalanceOutputTypeDef:
        """
        Gets the token balance for a batch of tokens by using the
        <code>BatchGetTokenBalance</code> action for every token in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/batch_get_token_balance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#batch_get_token_balance)
        """

    def get_asset_contract(
        self, **kwargs: Unpack[GetAssetContractInputRequestTypeDef]
    ) -> GetAssetContractOutputTypeDef:
        """
        Gets the information about a specific contract deployed on the blockchain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/get_asset_contract.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#get_asset_contract)
        """

    def get_token_balance(
        self, **kwargs: Unpack[GetTokenBalanceInputRequestTypeDef]
    ) -> GetTokenBalanceOutputTypeDef:
        """
        Gets the balance of a specific token, including native tokens, for a given
        address (wallet or contract) on the blockchain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/get_token_balance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#get_token_balance)
        """

    def get_transaction(
        self, **kwargs: Unpack[GetTransactionInputRequestTypeDef]
    ) -> GetTransactionOutputTypeDef:
        """
        Gets the details of a transaction.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/get_transaction.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#get_transaction)
        """

    def list_asset_contracts(
        self, **kwargs: Unpack[ListAssetContractsInputRequestTypeDef]
    ) -> ListAssetContractsOutputTypeDef:
        """
        Lists all the contracts for a given contract type deployed by an address
        (either a contract address or a wallet address).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/list_asset_contracts.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#list_asset_contracts)
        """

    def list_filtered_transaction_events(
        self, **kwargs: Unpack[ListFilteredTransactionEventsInputRequestTypeDef]
    ) -> ListFilteredTransactionEventsOutputTypeDef:
        """
        Lists all the transaction events for an address on the blockchain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/list_filtered_transaction_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#list_filtered_transaction_events)
        """

    def list_token_balances(
        self, **kwargs: Unpack[ListTokenBalancesInputRequestTypeDef]
    ) -> ListTokenBalancesOutputTypeDef:
        """
        This action returns the following for a given blockchain network:.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/list_token_balances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#list_token_balances)
        """

    def list_transaction_events(
        self, **kwargs: Unpack[ListTransactionEventsInputRequestTypeDef]
    ) -> ListTransactionEventsOutputTypeDef:
        """
        Lists all the transaction events for a transaction.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/list_transaction_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#list_transaction_events)
        """

    def list_transactions(
        self, **kwargs: Unpack[ListTransactionsInputRequestTypeDef]
    ) -> ListTransactionsOutputTypeDef:
        """
        Lists all the transaction events for a transaction.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/list_transactions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#list_transactions)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_asset_contracts"]
    ) -> ListAssetContractsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_filtered_transaction_events"]
    ) -> ListFilteredTransactionEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_token_balances"]
    ) -> ListTokenBalancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_transaction_events"]
    ) -> ListTransactionEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_transactions"]
    ) -> ListTransactionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_managedblockchain_query/client/#get_paginator)
        """
