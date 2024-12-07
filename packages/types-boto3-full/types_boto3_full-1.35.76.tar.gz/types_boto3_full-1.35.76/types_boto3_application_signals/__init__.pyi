"""
Main interface for application-signals service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_application_signals import (
        Client,
        CloudWatchApplicationSignalsClient,
        ListServiceDependenciesPaginator,
        ListServiceDependentsPaginator,
        ListServiceLevelObjectivesPaginator,
        ListServiceOperationsPaginator,
        ListServicesPaginator,
    )

    session = Session()
    client: CloudWatchApplicationSignalsClient = session.client("application-signals")

    list_service_dependencies_paginator: ListServiceDependenciesPaginator = client.get_paginator("list_service_dependencies")
    list_service_dependents_paginator: ListServiceDependentsPaginator = client.get_paginator("list_service_dependents")
    list_service_level_objectives_paginator: ListServiceLevelObjectivesPaginator = client.get_paginator("list_service_level_objectives")
    list_service_operations_paginator: ListServiceOperationsPaginator = client.get_paginator("list_service_operations")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CloudWatchApplicationSignalsClient
from .paginator import (
    ListServiceDependenciesPaginator,
    ListServiceDependentsPaginator,
    ListServiceLevelObjectivesPaginator,
    ListServiceOperationsPaginator,
    ListServicesPaginator,
)

Client = CloudWatchApplicationSignalsClient

__all__ = (
    "Client",
    "CloudWatchApplicationSignalsClient",
    "ListServiceDependenciesPaginator",
    "ListServiceDependentsPaginator",
    "ListServiceLevelObjectivesPaginator",
    "ListServiceOperationsPaginator",
    "ListServicesPaginator",
)
