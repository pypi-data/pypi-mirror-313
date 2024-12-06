"""
Type annotations for cloudtrail-data service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail_data/type_defs/)

Usage::

    ```python
    from mypy_boto3_cloudtrail_data.type_defs import AuditEventResultEntryTypeDef

    data: AuditEventResultEntryTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Sequence

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AuditEventResultEntryTypeDef",
    "AuditEventTypeDef",
    "PutAuditEventsRequestRequestTypeDef",
    "PutAuditEventsResponseTypeDef",
    "ResponseMetadataTypeDef",
    "ResultErrorEntryTypeDef",
)

AuditEventResultEntryTypeDef = TypedDict(
    "AuditEventResultEntryTypeDef",
    {
        "eventID": str,
        "id": str,
    },
)
AuditEventTypeDef = TypedDict(
    "AuditEventTypeDef",
    {
        "eventData": str,
        "id": str,
        "eventDataChecksum": NotRequired[str],
    },
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

ResultErrorEntryTypeDef = TypedDict(
    "ResultErrorEntryTypeDef",
    {
        "errorCode": str,
        "errorMessage": str,
        "id": str,
    },
)

class PutAuditEventsRequestRequestTypeDef(TypedDict):
    auditEvents: Sequence[AuditEventTypeDef]
    channelArn: str
    externalId: NotRequired[str]

class PutAuditEventsResponseTypeDef(TypedDict):
    failed: List[ResultErrorEntryTypeDef]
    successful: List[AuditEventResultEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
