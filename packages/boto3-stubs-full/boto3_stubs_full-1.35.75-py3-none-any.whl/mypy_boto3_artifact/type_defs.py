"""
Type annotations for artifact service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/type_defs/)

Usage::

    ```python
    from mypy_boto3_artifact.type_defs import AccountSettingsTypeDef

    data: AccountSettingsTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List

from .literals import (
    AcceptanceTypeType,
    NotificationSubscriptionStatusType,
    PublishedStateType,
    UploadStateType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AccountSettingsTypeDef",
    "GetAccountSettingsResponseTypeDef",
    "GetReportMetadataRequestRequestTypeDef",
    "GetReportMetadataResponseTypeDef",
    "GetReportRequestRequestTypeDef",
    "GetReportResponseTypeDef",
    "GetTermForReportRequestRequestTypeDef",
    "GetTermForReportResponseTypeDef",
    "ListReportsRequestListReportsPaginateTypeDef",
    "ListReportsRequestRequestTypeDef",
    "ListReportsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutAccountSettingsRequestRequestTypeDef",
    "PutAccountSettingsResponseTypeDef",
    "ReportDetailTypeDef",
    "ReportSummaryTypeDef",
    "ResponseMetadataTypeDef",
)


class AccountSettingsTypeDef(TypedDict):
    notificationSubscriptionStatus: NotRequired[NotificationSubscriptionStatusType]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class GetReportMetadataRequestRequestTypeDef(TypedDict):
    reportId: str
    reportVersion: NotRequired[int]


ReportDetailTypeDef = TypedDict(
    "ReportDetailTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "description": NotRequired[str],
        "periodStart": NotRequired[datetime],
        "periodEnd": NotRequired[datetime],
        "createdAt": NotRequired[datetime],
        "lastModifiedAt": NotRequired[datetime],
        "deletedAt": NotRequired[datetime],
        "state": NotRequired[PublishedStateType],
        "arn": NotRequired[str],
        "series": NotRequired[str],
        "category": NotRequired[str],
        "companyName": NotRequired[str],
        "productName": NotRequired[str],
        "termArn": NotRequired[str],
        "version": NotRequired[int],
        "acceptanceType": NotRequired[AcceptanceTypeType],
        "sequenceNumber": NotRequired[int],
        "uploadState": NotRequired[UploadStateType],
        "statusMessage": NotRequired[str],
    },
)


class GetReportRequestRequestTypeDef(TypedDict):
    reportId: str
    termToken: str
    reportVersion: NotRequired[int]


class GetTermForReportRequestRequestTypeDef(TypedDict):
    reportId: str
    reportVersion: NotRequired[int]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListReportsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


ReportSummaryTypeDef = TypedDict(
    "ReportSummaryTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "state": NotRequired[PublishedStateType],
        "arn": NotRequired[str],
        "version": NotRequired[int],
        "uploadState": NotRequired[UploadStateType],
        "description": NotRequired[str],
        "periodStart": NotRequired[datetime],
        "periodEnd": NotRequired[datetime],
        "series": NotRequired[str],
        "category": NotRequired[str],
        "companyName": NotRequired[str],
        "productName": NotRequired[str],
        "statusMessage": NotRequired[str],
        "acceptanceType": NotRequired[AcceptanceTypeType],
    },
)


class PutAccountSettingsRequestRequestTypeDef(TypedDict):
    notificationSubscriptionStatus: NotRequired[NotificationSubscriptionStatusType]


class GetAccountSettingsResponseTypeDef(TypedDict):
    accountSettings: AccountSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetReportResponseTypeDef(TypedDict):
    documentPresignedUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetTermForReportResponseTypeDef(TypedDict):
    documentPresignedUrl: str
    termToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutAccountSettingsResponseTypeDef(TypedDict):
    accountSettings: AccountSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetReportMetadataResponseTypeDef(TypedDict):
    reportDetails: ReportDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListReportsRequestListReportsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListReportsResponseTypeDef(TypedDict):
    reports: List[ReportSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
