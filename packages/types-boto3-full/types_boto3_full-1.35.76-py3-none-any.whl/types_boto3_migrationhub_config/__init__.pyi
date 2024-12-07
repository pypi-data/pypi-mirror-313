"""
Main interface for migrationhub-config service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_migrationhub_config import (
        Client,
        MigrationHubConfigClient,
    )

    session = Session()
    client: MigrationHubConfigClient = session.client("migrationhub-config")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import MigrationHubConfigClient

Client = MigrationHubConfigClient

__all__ = ("Client", "MigrationHubConfigClient")
