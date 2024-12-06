"""
Main interface for geo-maps service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_geo_maps import (
        Client,
        LocationServiceMapsV2Client,
    )

    session = Session()
    client: LocationServiceMapsV2Client = session.client("geo-maps")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import LocationServiceMapsV2Client

Client = LocationServiceMapsV2Client

__all__ = ("Client", "LocationServiceMapsV2Client")
