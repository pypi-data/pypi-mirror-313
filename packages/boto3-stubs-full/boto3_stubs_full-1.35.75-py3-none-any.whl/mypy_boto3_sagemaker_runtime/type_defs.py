"""
Type annotations for sagemaker-runtime service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_runtime/type_defs/)

Usage::

    ```python
    from mypy_boto3_sagemaker_runtime.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import IO, Any, Dict, Union

from botocore.eventstream import EventStream
from botocore.response import StreamingBody

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "BlobTypeDef",
    "InternalStreamFailureTypeDef",
    "InvokeEndpointAsyncInputRequestTypeDef",
    "InvokeEndpointAsyncOutputTypeDef",
    "InvokeEndpointInputRequestTypeDef",
    "InvokeEndpointOutputTypeDef",
    "InvokeEndpointWithResponseStreamInputRequestTypeDef",
    "InvokeEndpointWithResponseStreamOutputTypeDef",
    "ModelStreamErrorTypeDef",
    "PayloadPartTypeDef",
    "ResponseMetadataTypeDef",
    "ResponseStreamTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class InternalStreamFailureTypeDef(TypedDict):
    Message: NotRequired[str]


class InvokeEndpointAsyncInputRequestTypeDef(TypedDict):
    EndpointName: str
    InputLocation: str
    ContentType: NotRequired[str]
    Accept: NotRequired[str]
    CustomAttributes: NotRequired[str]
    InferenceId: NotRequired[str]
    RequestTTLSeconds: NotRequired[int]
    InvocationTimeoutSeconds: NotRequired[int]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ModelStreamErrorTypeDef(TypedDict):
    Message: NotRequired[str]
    ErrorCode: NotRequired[str]


class PayloadPartTypeDef(TypedDict):
    Bytes: NotRequired[bytes]


class InvokeEndpointInputRequestTypeDef(TypedDict):
    EndpointName: str
    Body: BlobTypeDef
    ContentType: NotRequired[str]
    Accept: NotRequired[str]
    CustomAttributes: NotRequired[str]
    TargetModel: NotRequired[str]
    TargetVariant: NotRequired[str]
    TargetContainerHostname: NotRequired[str]
    InferenceId: NotRequired[str]
    EnableExplanations: NotRequired[str]
    InferenceComponentName: NotRequired[str]
    SessionId: NotRequired[str]


class InvokeEndpointWithResponseStreamInputRequestTypeDef(TypedDict):
    EndpointName: str
    Body: BlobTypeDef
    ContentType: NotRequired[str]
    Accept: NotRequired[str]
    CustomAttributes: NotRequired[str]
    TargetVariant: NotRequired[str]
    TargetContainerHostname: NotRequired[str]
    InferenceId: NotRequired[str]
    InferenceComponentName: NotRequired[str]
    SessionId: NotRequired[str]


class InvokeEndpointAsyncOutputTypeDef(TypedDict):
    InferenceId: str
    OutputLocation: str
    FailureLocation: str
    ResponseMetadata: ResponseMetadataTypeDef


class InvokeEndpointOutputTypeDef(TypedDict):
    Body: StreamingBody
    ContentType: str
    InvokedProductionVariant: str
    CustomAttributes: str
    NewSessionId: str
    ClosedSessionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ResponseStreamTypeDef(TypedDict):
    PayloadPart: NotRequired[PayloadPartTypeDef]
    ModelStreamError: NotRequired[ModelStreamErrorTypeDef]
    InternalStreamFailure: NotRequired[InternalStreamFailureTypeDef]


class InvokeEndpointWithResponseStreamOutputTypeDef(TypedDict):
    Body: "EventStream[ResponseStreamTypeDef]"
    ContentType: str
    InvokedProductionVariant: str
    CustomAttributes: str
    ResponseMetadata: ResponseMetadataTypeDef
