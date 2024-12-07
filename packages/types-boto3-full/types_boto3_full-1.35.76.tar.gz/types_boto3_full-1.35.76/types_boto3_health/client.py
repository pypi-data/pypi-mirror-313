"""
Type annotations for health service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_health.client import HealthClient

    session = Session()
    client: HealthClient = session.client("health")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeAffectedAccountsForOrganizationPaginator,
    DescribeAffectedEntitiesForOrganizationPaginator,
    DescribeAffectedEntitiesPaginator,
    DescribeEventAggregatesPaginator,
    DescribeEventsForOrganizationPaginator,
    DescribeEventsPaginator,
    DescribeEventTypesPaginator,
)
from .type_defs import (
    DescribeAffectedAccountsForOrganizationRequestRequestTypeDef,
    DescribeAffectedAccountsForOrganizationResponseTypeDef,
    DescribeAffectedEntitiesForOrganizationRequestRequestTypeDef,
    DescribeAffectedEntitiesForOrganizationResponseTypeDef,
    DescribeAffectedEntitiesRequestRequestTypeDef,
    DescribeAffectedEntitiesResponseTypeDef,
    DescribeEntityAggregatesForOrganizationRequestRequestTypeDef,
    DescribeEntityAggregatesForOrganizationResponseTypeDef,
    DescribeEntityAggregatesRequestRequestTypeDef,
    DescribeEntityAggregatesResponseTypeDef,
    DescribeEventAggregatesRequestRequestTypeDef,
    DescribeEventAggregatesResponseTypeDef,
    DescribeEventDetailsForOrganizationRequestRequestTypeDef,
    DescribeEventDetailsForOrganizationResponseTypeDef,
    DescribeEventDetailsRequestRequestTypeDef,
    DescribeEventDetailsResponseTypeDef,
    DescribeEventsForOrganizationRequestRequestTypeDef,
    DescribeEventsForOrganizationResponseTypeDef,
    DescribeEventsRequestRequestTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeEventTypesRequestRequestTypeDef,
    DescribeEventTypesResponseTypeDef,
    DescribeHealthServiceStatusForOrganizationResponseTypeDef,
    EmptyResponseMetadataTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("HealthClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    InvalidPaginationToken: Type[BotocoreClientError]
    UnsupportedLocale: Type[BotocoreClientError]


class HealthClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        HealthClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#close)
        """

    def describe_affected_accounts_for_organization(
        self, **kwargs: Unpack[DescribeAffectedAccountsForOrganizationRequestRequestTypeDef]
    ) -> DescribeAffectedAccountsForOrganizationResponseTypeDef:
        """
        Returns a list of accounts in the organization from Organizations that are
        affected by the provided event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_affected_accounts_for_organization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#describe_affected_accounts_for_organization)
        """

    def describe_affected_entities(
        self, **kwargs: Unpack[DescribeAffectedEntitiesRequestRequestTypeDef]
    ) -> DescribeAffectedEntitiesResponseTypeDef:
        """
        Returns a list of entities that have been affected by the specified events,
        based on the specified filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_affected_entities.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#describe_affected_entities)
        """

    def describe_affected_entities_for_organization(
        self, **kwargs: Unpack[DescribeAffectedEntitiesForOrganizationRequestRequestTypeDef]
    ) -> DescribeAffectedEntitiesForOrganizationResponseTypeDef:
        """
        Returns a list of entities that have been affected by one or more events for
        one or more accounts in your organization in Organizations, based on the filter
        criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_affected_entities_for_organization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#describe_affected_entities_for_organization)
        """

    def describe_entity_aggregates(
        self, **kwargs: Unpack[DescribeEntityAggregatesRequestRequestTypeDef]
    ) -> DescribeEntityAggregatesResponseTypeDef:
        """
        Returns the number of entities that are affected by each of the specified
        events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_entity_aggregates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#describe_entity_aggregates)
        """

    def describe_entity_aggregates_for_organization(
        self, **kwargs: Unpack[DescribeEntityAggregatesForOrganizationRequestRequestTypeDef]
    ) -> DescribeEntityAggregatesForOrganizationResponseTypeDef:
        """
        Returns a list of entity aggregates for your Organizations that are affected by
        each of the specified events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_entity_aggregates_for_organization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#describe_entity_aggregates_for_organization)
        """

    def describe_event_aggregates(
        self, **kwargs: Unpack[DescribeEventAggregatesRequestRequestTypeDef]
    ) -> DescribeEventAggregatesResponseTypeDef:
        """
        Returns the number of events of each event type (issue, scheduled change, and
        account notification).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_event_aggregates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#describe_event_aggregates)
        """

    def describe_event_details(
        self, **kwargs: Unpack[DescribeEventDetailsRequestRequestTypeDef]
    ) -> DescribeEventDetailsResponseTypeDef:
        """
        Returns detailed information about one or more specified events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_event_details.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#describe_event_details)
        """

    def describe_event_details_for_organization(
        self, **kwargs: Unpack[DescribeEventDetailsForOrganizationRequestRequestTypeDef]
    ) -> DescribeEventDetailsForOrganizationResponseTypeDef:
        """
        Returns detailed information about one or more specified events for one or more
        Amazon Web Services accounts in your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_event_details_for_organization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#describe_event_details_for_organization)
        """

    def describe_event_types(
        self, **kwargs: Unpack[DescribeEventTypesRequestRequestTypeDef]
    ) -> DescribeEventTypesResponseTypeDef:
        """
        Returns the event types that meet the specified filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_event_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#describe_event_types)
        """

    def describe_events(
        self, **kwargs: Unpack[DescribeEventsRequestRequestTypeDef]
    ) -> DescribeEventsResponseTypeDef:
        """
        Returns information about events that meet the specified filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#describe_events)
        """

    def describe_events_for_organization(
        self, **kwargs: Unpack[DescribeEventsForOrganizationRequestRequestTypeDef]
    ) -> DescribeEventsForOrganizationResponseTypeDef:
        """
        Returns information about events across your organization in Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_events_for_organization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#describe_events_for_organization)
        """

    def describe_health_service_status_for_organization(
        self,
    ) -> DescribeHealthServiceStatusForOrganizationResponseTypeDef:
        """
        This operation provides status information on enabling or disabling Health to
        work with your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_health_service_status_for_organization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#describe_health_service_status_for_organization)
        """

    def disable_health_service_access_for_organization(self) -> EmptyResponseMetadataTypeDef:
        """
        Disables Health from working with Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/disable_health_service_access_for_organization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#disable_health_service_access_for_organization)
        """

    def enable_health_service_access_for_organization(self) -> EmptyResponseMetadataTypeDef:
        """
        Enables Health to work with Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/enable_health_service_access_for_organization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#enable_health_service_access_for_organization)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_affected_accounts_for_organization"]
    ) -> DescribeAffectedAccountsForOrganizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_affected_entities_for_organization"]
    ) -> DescribeAffectedEntitiesForOrganizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_affected_entities"]
    ) -> DescribeAffectedEntitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_event_aggregates"]
    ) -> DescribeEventAggregatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_event_types"]
    ) -> DescribeEventTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_events_for_organization"]
    ) -> DescribeEventsForOrganizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_events"]) -> DescribeEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/client/#get_paginator)
        """
