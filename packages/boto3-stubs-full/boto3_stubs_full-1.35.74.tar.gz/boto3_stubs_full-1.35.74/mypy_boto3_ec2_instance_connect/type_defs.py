"""
Type annotations for ec2-instance-connect service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2_instance_connect/type_defs/)

Usage::

    ```python
    from mypy_boto3_ec2_instance_connect.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ResponseMetadataTypeDef",
    "SendSSHPublicKeyRequestRequestTypeDef",
    "SendSSHPublicKeyResponseTypeDef",
    "SendSerialConsoleSSHPublicKeyRequestRequestTypeDef",
    "SendSerialConsoleSSHPublicKeyResponseTypeDef",
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class SendSSHPublicKeyRequestRequestTypeDef(TypedDict):
    InstanceId: str
    InstanceOSUser: str
    SSHPublicKey: str
    AvailabilityZone: NotRequired[str]


class SendSerialConsoleSSHPublicKeyRequestRequestTypeDef(TypedDict):
    InstanceId: str
    SSHPublicKey: str
    SerialPort: NotRequired[int]


class SendSSHPublicKeyResponseTypeDef(TypedDict):
    RequestId: str
    Success: bool
    ResponseMetadata: ResponseMetadataTypeDef


class SendSerialConsoleSSHPublicKeyResponseTypeDef(TypedDict):
    RequestId: str
    Success: bool
    ResponseMetadata: ResponseMetadataTypeDef
