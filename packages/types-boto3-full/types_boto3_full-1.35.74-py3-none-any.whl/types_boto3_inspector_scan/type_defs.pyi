"""
Type annotations for inspector-scan service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_inspector_scan/type_defs/)

Usage::

    ```python
    from types_boto3_inspector_scan.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping

from .literals import OutputFormatType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = ("ResponseMetadataTypeDef", "ScanSbomRequestRequestTypeDef", "ScanSbomResponseTypeDef")

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ScanSbomRequestRequestTypeDef(TypedDict):
    sbom: Mapping[str, Any]
    outputFormat: NotRequired[OutputFormatType]

class ScanSbomResponseTypeDef(TypedDict):
    sbom: Dict[str, Any]
    ResponseMetadata: ResponseMetadataTypeDef
