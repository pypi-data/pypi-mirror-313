"""
Type annotations for marketplace-deployment service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_deployment/type_defs/)

Usage::

    ```python
    from mypy_boto3_marketplace_deployment.type_defs import DeploymentParameterInputTypeDef

    data: DeploymentParameterInputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, Mapping, Sequence, Union

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "DeploymentParameterInputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutDeploymentParameterRequestRequestTypeDef",
    "PutDeploymentParameterResponseTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
)

class DeploymentParameterInputTypeDef(TypedDict):
    name: str
    secretString: str

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: NotRequired[Mapping[str, str]]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PutDeploymentParameterResponseTypeDef(TypedDict):
    agreementId: str
    deploymentParameterId: str
    resourceArn: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PutDeploymentParameterRequestRequestTypeDef(TypedDict):
    agreementId: str
    catalog: str
    deploymentParameter: DeploymentParameterInputTypeDef
    productId: str
    clientToken: NotRequired[str]
    expirationDate: NotRequired[TimestampTypeDef]
    tags: NotRequired[Mapping[str, str]]
