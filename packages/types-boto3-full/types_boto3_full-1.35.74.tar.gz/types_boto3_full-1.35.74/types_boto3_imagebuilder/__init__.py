"""
Main interface for imagebuilder service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_imagebuilder import (
        Client,
        ImagebuilderClient,
    )

    session = Session()
    client: ImagebuilderClient = session.client("imagebuilder")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ImagebuilderClient

Client = ImagebuilderClient


__all__ = ("Client", "ImagebuilderClient")
