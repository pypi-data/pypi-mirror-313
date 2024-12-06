"""
Main interface for bedrock-data-automation-runtime service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_bedrock_data_automation_runtime import (
        Client,
        RuntimeforBedrockDataAutomationClient,
    )

    session = Session()
    client: RuntimeforBedrockDataAutomationClient = session.client("bedrock-data-automation-runtime")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import RuntimeforBedrockDataAutomationClient

Client = RuntimeforBedrockDataAutomationClient


__all__ = ("Client", "RuntimeforBedrockDataAutomationClient")
