"""
Main interface for ec2-instance-connect service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_ec2_instance_connect import (
        Client,
        EC2InstanceConnectClient,
    )

    session = Session()
    client: EC2InstanceConnectClient = session.client("ec2-instance-connect")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import EC2InstanceConnectClient

Client = EC2InstanceConnectClient


__all__ = ("Client", "EC2InstanceConnectClient")
