"""
Type annotations for service-quotas service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/type_defs/)

Usage::

    ```python
    from mypy_boto3_service_quotas.type_defs import DeleteServiceQuotaIncreaseRequestFromTemplateRequestRequestTypeDef

    data: DeleteServiceQuotaIncreaseRequestFromTemplateRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AppliedLevelEnumType,
    ErrorCodeType,
    PeriodUnitType,
    QuotaContextScopeType,
    RequestStatusType,
    ServiceQuotaTemplateAssociationStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "DeleteServiceQuotaIncreaseRequestFromTemplateRequestRequestTypeDef",
    "ErrorReasonTypeDef",
    "GetAWSDefaultServiceQuotaRequestRequestTypeDef",
    "GetAWSDefaultServiceQuotaResponseTypeDef",
    "GetAssociationForServiceQuotaTemplateResponseTypeDef",
    "GetRequestedServiceQuotaChangeRequestRequestTypeDef",
    "GetRequestedServiceQuotaChangeResponseTypeDef",
    "GetServiceQuotaIncreaseRequestFromTemplateRequestRequestTypeDef",
    "GetServiceQuotaIncreaseRequestFromTemplateResponseTypeDef",
    "GetServiceQuotaRequestRequestTypeDef",
    "GetServiceQuotaResponseTypeDef",
    "ListAWSDefaultServiceQuotasRequestListAWSDefaultServiceQuotasPaginateTypeDef",
    "ListAWSDefaultServiceQuotasRequestRequestTypeDef",
    "ListAWSDefaultServiceQuotasResponseTypeDef",
    "ListRequestedServiceQuotaChangeHistoryByQuotaRequestListRequestedServiceQuotaChangeHistoryByQuotaPaginateTypeDef",
    "ListRequestedServiceQuotaChangeHistoryByQuotaRequestRequestTypeDef",
    "ListRequestedServiceQuotaChangeHistoryByQuotaResponseTypeDef",
    "ListRequestedServiceQuotaChangeHistoryRequestListRequestedServiceQuotaChangeHistoryPaginateTypeDef",
    "ListRequestedServiceQuotaChangeHistoryRequestRequestTypeDef",
    "ListRequestedServiceQuotaChangeHistoryResponseTypeDef",
    "ListServiceQuotaIncreaseRequestsInTemplateRequestListServiceQuotaIncreaseRequestsInTemplatePaginateTypeDef",
    "ListServiceQuotaIncreaseRequestsInTemplateRequestRequestTypeDef",
    "ListServiceQuotaIncreaseRequestsInTemplateResponseTypeDef",
    "ListServiceQuotasRequestListServiceQuotasPaginateTypeDef",
    "ListServiceQuotasRequestRequestTypeDef",
    "ListServiceQuotasResponseTypeDef",
    "ListServicesRequestListServicesPaginateTypeDef",
    "ListServicesRequestRequestTypeDef",
    "ListServicesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MetricInfoTypeDef",
    "PaginatorConfigTypeDef",
    "PutServiceQuotaIncreaseRequestIntoTemplateRequestRequestTypeDef",
    "PutServiceQuotaIncreaseRequestIntoTemplateResponseTypeDef",
    "QuotaContextInfoTypeDef",
    "QuotaPeriodTypeDef",
    "RequestServiceQuotaIncreaseRequestRequestTypeDef",
    "RequestServiceQuotaIncreaseResponseTypeDef",
    "RequestedServiceQuotaChangeTypeDef",
    "ResponseMetadataTypeDef",
    "ServiceInfoTypeDef",
    "ServiceQuotaIncreaseRequestInTemplateTypeDef",
    "ServiceQuotaTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
)


class DeleteServiceQuotaIncreaseRequestFromTemplateRequestRequestTypeDef(TypedDict):
    ServiceCode: str
    QuotaCode: str
    AwsRegion: str


class ErrorReasonTypeDef(TypedDict):
    ErrorCode: NotRequired[ErrorCodeType]
    ErrorMessage: NotRequired[str]


class GetAWSDefaultServiceQuotaRequestRequestTypeDef(TypedDict):
    ServiceCode: str
    QuotaCode: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class GetRequestedServiceQuotaChangeRequestRequestTypeDef(TypedDict):
    RequestId: str


class GetServiceQuotaIncreaseRequestFromTemplateRequestRequestTypeDef(TypedDict):
    ServiceCode: str
    QuotaCode: str
    AwsRegion: str


ServiceQuotaIncreaseRequestInTemplateTypeDef = TypedDict(
    "ServiceQuotaIncreaseRequestInTemplateTypeDef",
    {
        "ServiceCode": NotRequired[str],
        "ServiceName": NotRequired[str],
        "QuotaCode": NotRequired[str],
        "QuotaName": NotRequired[str],
        "DesiredValue": NotRequired[float],
        "AwsRegion": NotRequired[str],
        "Unit": NotRequired[str],
        "GlobalQuota": NotRequired[bool],
    },
)


class GetServiceQuotaRequestRequestTypeDef(TypedDict):
    ServiceCode: str
    QuotaCode: str
    ContextId: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAWSDefaultServiceQuotasRequestRequestTypeDef(TypedDict):
    ServiceCode: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListRequestedServiceQuotaChangeHistoryByQuotaRequestRequestTypeDef(TypedDict):
    ServiceCode: str
    QuotaCode: str
    Status: NotRequired[RequestStatusType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    QuotaRequestedAtLevel: NotRequired[AppliedLevelEnumType]


class ListRequestedServiceQuotaChangeHistoryRequestRequestTypeDef(TypedDict):
    ServiceCode: NotRequired[str]
    Status: NotRequired[RequestStatusType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    QuotaRequestedAtLevel: NotRequired[AppliedLevelEnumType]


class ListServiceQuotaIncreaseRequestsInTemplateRequestRequestTypeDef(TypedDict):
    ServiceCode: NotRequired[str]
    AwsRegion: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListServiceQuotasRequestRequestTypeDef(TypedDict):
    ServiceCode: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    QuotaCode: NotRequired[str]
    QuotaAppliedAtLevel: NotRequired[AppliedLevelEnumType]


class ListServicesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


ServiceInfoTypeDef = TypedDict(
    "ServiceInfoTypeDef",
    {
        "ServiceCode": NotRequired[str],
        "ServiceName": NotRequired[str],
    },
)


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class MetricInfoTypeDef(TypedDict):
    MetricNamespace: NotRequired[str]
    MetricName: NotRequired[str]
    MetricDimensions: NotRequired[Dict[str, str]]
    MetricStatisticRecommendation: NotRequired[str]


class PutServiceQuotaIncreaseRequestIntoTemplateRequestRequestTypeDef(TypedDict):
    QuotaCode: str
    ServiceCode: str
    AwsRegion: str
    DesiredValue: float


class QuotaContextInfoTypeDef(TypedDict):
    ContextScope: NotRequired[QuotaContextScopeType]
    ContextScopeType: NotRequired[str]
    ContextId: NotRequired[str]


class QuotaPeriodTypeDef(TypedDict):
    PeriodValue: NotRequired[int]
    PeriodUnit: NotRequired[PeriodUnitType]


class RequestServiceQuotaIncreaseRequestRequestTypeDef(TypedDict):
    ServiceCode: str
    QuotaCode: str
    DesiredValue: float
    ContextId: NotRequired[str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


class GetAssociationForServiceQuotaTemplateResponseTypeDef(TypedDict):
    ServiceQuotaTemplateAssociationStatus: ServiceQuotaTemplateAssociationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetServiceQuotaIncreaseRequestFromTemplateResponseTypeDef(TypedDict):
    ServiceQuotaIncreaseRequestInTemplate: ServiceQuotaIncreaseRequestInTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListServiceQuotaIncreaseRequestsInTemplateResponseTypeDef(TypedDict):
    ServiceQuotaIncreaseRequestInTemplateList: List[ServiceQuotaIncreaseRequestInTemplateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PutServiceQuotaIncreaseRequestIntoTemplateResponseTypeDef(TypedDict):
    ServiceQuotaIncreaseRequestInTemplate: ServiceQuotaIncreaseRequestInTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAWSDefaultServiceQuotasRequestListAWSDefaultServiceQuotasPaginateTypeDef(TypedDict):
    ServiceCode: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRequestedServiceQuotaChangeHistoryByQuotaRequestListRequestedServiceQuotaChangeHistoryByQuotaPaginateTypeDef(
    TypedDict
):
    ServiceCode: str
    QuotaCode: str
    Status: NotRequired[RequestStatusType]
    QuotaRequestedAtLevel: NotRequired[AppliedLevelEnumType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRequestedServiceQuotaChangeHistoryRequestListRequestedServiceQuotaChangeHistoryPaginateTypeDef(
    TypedDict
):
    ServiceCode: NotRequired[str]
    Status: NotRequired[RequestStatusType]
    QuotaRequestedAtLevel: NotRequired[AppliedLevelEnumType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServiceQuotaIncreaseRequestsInTemplateRequestListServiceQuotaIncreaseRequestsInTemplatePaginateTypeDef(
    TypedDict
):
    ServiceCode: NotRequired[str]
    AwsRegion: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServiceQuotasRequestListServiceQuotasPaginateTypeDef(TypedDict):
    ServiceCode: str
    QuotaCode: NotRequired[str]
    QuotaAppliedAtLevel: NotRequired[AppliedLevelEnumType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServicesRequestListServicesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServicesResponseTypeDef(TypedDict):
    Services: List[ServiceInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


RequestedServiceQuotaChangeTypeDef = TypedDict(
    "RequestedServiceQuotaChangeTypeDef",
    {
        "Id": NotRequired[str],
        "CaseId": NotRequired[str],
        "ServiceCode": NotRequired[str],
        "ServiceName": NotRequired[str],
        "QuotaCode": NotRequired[str],
        "QuotaName": NotRequired[str],
        "DesiredValue": NotRequired[float],
        "Status": NotRequired[RequestStatusType],
        "Created": NotRequired[datetime],
        "LastUpdated": NotRequired[datetime],
        "Requester": NotRequired[str],
        "QuotaArn": NotRequired[str],
        "GlobalQuota": NotRequired[bool],
        "Unit": NotRequired[str],
        "QuotaRequestedAtLevel": NotRequired[AppliedLevelEnumType],
        "QuotaContext": NotRequired[QuotaContextInfoTypeDef],
    },
)
ServiceQuotaTypeDef = TypedDict(
    "ServiceQuotaTypeDef",
    {
        "ServiceCode": NotRequired[str],
        "ServiceName": NotRequired[str],
        "QuotaArn": NotRequired[str],
        "QuotaCode": NotRequired[str],
        "QuotaName": NotRequired[str],
        "Value": NotRequired[float],
        "Unit": NotRequired[str],
        "Adjustable": NotRequired[bool],
        "GlobalQuota": NotRequired[bool],
        "UsageMetric": NotRequired[MetricInfoTypeDef],
        "Period": NotRequired[QuotaPeriodTypeDef],
        "ErrorReason": NotRequired[ErrorReasonTypeDef],
        "QuotaAppliedAtLevel": NotRequired[AppliedLevelEnumType],
        "QuotaContext": NotRequired[QuotaContextInfoTypeDef],
    },
)


class GetRequestedServiceQuotaChangeResponseTypeDef(TypedDict):
    RequestedQuota: RequestedServiceQuotaChangeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListRequestedServiceQuotaChangeHistoryByQuotaResponseTypeDef(TypedDict):
    RequestedQuotas: List[RequestedServiceQuotaChangeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRequestedServiceQuotaChangeHistoryResponseTypeDef(TypedDict):
    RequestedQuotas: List[RequestedServiceQuotaChangeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RequestServiceQuotaIncreaseResponseTypeDef(TypedDict):
    RequestedQuota: RequestedServiceQuotaChangeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAWSDefaultServiceQuotaResponseTypeDef(TypedDict):
    Quota: ServiceQuotaTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetServiceQuotaResponseTypeDef(TypedDict):
    Quota: ServiceQuotaTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAWSDefaultServiceQuotasResponseTypeDef(TypedDict):
    Quotas: List[ServiceQuotaTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListServiceQuotasResponseTypeDef(TypedDict):
    Quotas: List[ServiceQuotaTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
