"""
Type annotations for bcm-pricing-calculator service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bcm_pricing_calculator/type_defs/)

Usage::

    ```python
    from mypy_boto3_bcm_pricing_calculator.type_defs import AddReservedInstanceActionTypeDef

    data: AddReservedInstanceActionTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    BatchCreateBillScenarioCommitmentModificationErrorCodeType,
    BatchCreateBillScenarioUsageModificationErrorCodeType,
    BatchCreateWorkloadEstimateUsageCodeType,
    BatchDeleteBillScenarioCommitmentModificationErrorCodeType,
    BatchDeleteBillScenarioUsageModificationErrorCodeType,
    BatchUpdateBillScenarioCommitmentModificationErrorCodeType,
    BatchUpdateBillScenarioUsageModificationErrorCodeType,
    BillEstimateStatusType,
    BillScenarioStatusType,
    ListBillEstimateLineItemsFilterNameType,
    ListBillEstimatesFilterNameType,
    ListBillScenariosFilterNameType,
    ListUsageFilterNameType,
    ListWorkloadEstimatesFilterNameType,
    MatchOptionType,
    PurchaseAgreementTypeType,
    RateTypeType,
    WorkloadEstimateCostStatusType,
    WorkloadEstimateRateTypeType,
    WorkloadEstimateStatusType,
    WorkloadEstimateUpdateUsageErrorCodeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AddReservedInstanceActionTypeDef",
    "AddSavingsPlanActionTypeDef",
    "BatchCreateBillScenarioCommitmentModificationEntryTypeDef",
    "BatchCreateBillScenarioCommitmentModificationErrorTypeDef",
    "BatchCreateBillScenarioCommitmentModificationItemTypeDef",
    "BatchCreateBillScenarioCommitmentModificationRequestRequestTypeDef",
    "BatchCreateBillScenarioCommitmentModificationResponseTypeDef",
    "BatchCreateBillScenarioUsageModificationEntryTypeDef",
    "BatchCreateBillScenarioUsageModificationErrorTypeDef",
    "BatchCreateBillScenarioUsageModificationItemTypeDef",
    "BatchCreateBillScenarioUsageModificationRequestRequestTypeDef",
    "BatchCreateBillScenarioUsageModificationResponseTypeDef",
    "BatchCreateWorkloadEstimateUsageEntryTypeDef",
    "BatchCreateWorkloadEstimateUsageErrorTypeDef",
    "BatchCreateWorkloadEstimateUsageItemTypeDef",
    "BatchCreateWorkloadEstimateUsageRequestRequestTypeDef",
    "BatchCreateWorkloadEstimateUsageResponseTypeDef",
    "BatchDeleteBillScenarioCommitmentModificationErrorTypeDef",
    "BatchDeleteBillScenarioCommitmentModificationRequestRequestTypeDef",
    "BatchDeleteBillScenarioCommitmentModificationResponseTypeDef",
    "BatchDeleteBillScenarioUsageModificationErrorTypeDef",
    "BatchDeleteBillScenarioUsageModificationRequestRequestTypeDef",
    "BatchDeleteBillScenarioUsageModificationResponseTypeDef",
    "BatchDeleteWorkloadEstimateUsageErrorTypeDef",
    "BatchDeleteWorkloadEstimateUsageRequestRequestTypeDef",
    "BatchDeleteWorkloadEstimateUsageResponseTypeDef",
    "BatchUpdateBillScenarioCommitmentModificationEntryTypeDef",
    "BatchUpdateBillScenarioCommitmentModificationErrorTypeDef",
    "BatchUpdateBillScenarioCommitmentModificationRequestRequestTypeDef",
    "BatchUpdateBillScenarioCommitmentModificationResponseTypeDef",
    "BatchUpdateBillScenarioUsageModificationEntryTypeDef",
    "BatchUpdateBillScenarioUsageModificationErrorTypeDef",
    "BatchUpdateBillScenarioUsageModificationRequestRequestTypeDef",
    "BatchUpdateBillScenarioUsageModificationResponseTypeDef",
    "BatchUpdateWorkloadEstimateUsageEntryTypeDef",
    "BatchUpdateWorkloadEstimateUsageErrorTypeDef",
    "BatchUpdateWorkloadEstimateUsageRequestRequestTypeDef",
    "BatchUpdateWorkloadEstimateUsageResponseTypeDef",
    "BillEstimateCommitmentSummaryTypeDef",
    "BillEstimateCostSummaryTypeDef",
    "BillEstimateInputCommitmentModificationSummaryTypeDef",
    "BillEstimateInputUsageModificationSummaryPaginatorTypeDef",
    "BillEstimateInputUsageModificationSummaryTypeDef",
    "BillEstimateLineItemSummaryTypeDef",
    "BillEstimateSummaryTypeDef",
    "BillIntervalOutputTypeDef",
    "BillIntervalTypeDef",
    "BillIntervalUnionTypeDef",
    "BillScenarioCommitmentModificationActionTypeDef",
    "BillScenarioCommitmentModificationItemTypeDef",
    "BillScenarioSummaryTypeDef",
    "BillScenarioUsageModificationItemPaginatorTypeDef",
    "BillScenarioUsageModificationItemTypeDef",
    "CostAmountTypeDef",
    "CostDifferenceTypeDef",
    "CreateBillEstimateRequestRequestTypeDef",
    "CreateBillEstimateResponseTypeDef",
    "CreateBillScenarioRequestRequestTypeDef",
    "CreateBillScenarioResponseTypeDef",
    "CreateWorkloadEstimateRequestRequestTypeDef",
    "CreateWorkloadEstimateResponseTypeDef",
    "DeleteBillEstimateRequestRequestTypeDef",
    "DeleteBillScenarioRequestRequestTypeDef",
    "DeleteWorkloadEstimateRequestRequestTypeDef",
    "ExpressionFilterOutputTypeDef",
    "ExpressionFilterTypeDef",
    "ExpressionFilterUnionTypeDef",
    "ExpressionOutputTypeDef",
    "ExpressionPaginatorTypeDef",
    "ExpressionTypeDef",
    "ExpressionUnionTypeDef",
    "FilterTimestampTypeDef",
    "GetBillEstimateRequestRequestTypeDef",
    "GetBillEstimateResponseTypeDef",
    "GetBillScenarioRequestRequestTypeDef",
    "GetBillScenarioResponseTypeDef",
    "GetPreferencesResponseTypeDef",
    "GetWorkloadEstimateRequestRequestTypeDef",
    "GetWorkloadEstimateResponseTypeDef",
    "HistoricalUsageEntityOutputTypeDef",
    "HistoricalUsageEntityPaginatorTypeDef",
    "HistoricalUsageEntityTypeDef",
    "HistoricalUsageEntityUnionTypeDef",
    "ListBillEstimateCommitmentsRequestListBillEstimateCommitmentsPaginateTypeDef",
    "ListBillEstimateCommitmentsRequestRequestTypeDef",
    "ListBillEstimateCommitmentsResponseTypeDef",
    "ListBillEstimateInputCommitmentModificationsRequestListBillEstimateInputCommitmentModificationsPaginateTypeDef",
    "ListBillEstimateInputCommitmentModificationsRequestRequestTypeDef",
    "ListBillEstimateInputCommitmentModificationsResponseTypeDef",
    "ListBillEstimateInputUsageModificationsRequestListBillEstimateInputUsageModificationsPaginateTypeDef",
    "ListBillEstimateInputUsageModificationsRequestRequestTypeDef",
    "ListBillEstimateInputUsageModificationsResponsePaginatorTypeDef",
    "ListBillEstimateInputUsageModificationsResponseTypeDef",
    "ListBillEstimateLineItemsFilterTypeDef",
    "ListBillEstimateLineItemsRequestListBillEstimateLineItemsPaginateTypeDef",
    "ListBillEstimateLineItemsRequestRequestTypeDef",
    "ListBillEstimateLineItemsResponseTypeDef",
    "ListBillEstimatesFilterTypeDef",
    "ListBillEstimatesRequestListBillEstimatesPaginateTypeDef",
    "ListBillEstimatesRequestRequestTypeDef",
    "ListBillEstimatesResponseTypeDef",
    "ListBillScenarioCommitmentModificationsRequestListBillScenarioCommitmentModificationsPaginateTypeDef",
    "ListBillScenarioCommitmentModificationsRequestRequestTypeDef",
    "ListBillScenarioCommitmentModificationsResponseTypeDef",
    "ListBillScenarioUsageModificationsRequestListBillScenarioUsageModificationsPaginateTypeDef",
    "ListBillScenarioUsageModificationsRequestRequestTypeDef",
    "ListBillScenarioUsageModificationsResponsePaginatorTypeDef",
    "ListBillScenarioUsageModificationsResponseTypeDef",
    "ListBillScenariosFilterTypeDef",
    "ListBillScenariosRequestListBillScenariosPaginateTypeDef",
    "ListBillScenariosRequestRequestTypeDef",
    "ListBillScenariosResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUsageFilterTypeDef",
    "ListWorkloadEstimateUsageRequestListWorkloadEstimateUsagePaginateTypeDef",
    "ListWorkloadEstimateUsageRequestRequestTypeDef",
    "ListWorkloadEstimateUsageResponsePaginatorTypeDef",
    "ListWorkloadEstimateUsageResponseTypeDef",
    "ListWorkloadEstimatesFilterTypeDef",
    "ListWorkloadEstimatesRequestListWorkloadEstimatesPaginateTypeDef",
    "ListWorkloadEstimatesRequestRequestTypeDef",
    "ListWorkloadEstimatesResponseTypeDef",
    "NegateReservedInstanceActionTypeDef",
    "NegateSavingsPlanActionTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBillEstimateRequestRequestTypeDef",
    "UpdateBillEstimateResponseTypeDef",
    "UpdateBillScenarioRequestRequestTypeDef",
    "UpdateBillScenarioResponseTypeDef",
    "UpdatePreferencesRequestRequestTypeDef",
    "UpdatePreferencesResponseTypeDef",
    "UpdateWorkloadEstimateRequestRequestTypeDef",
    "UpdateWorkloadEstimateResponseTypeDef",
    "UsageAmountTypeDef",
    "UsageQuantityResultTypeDef",
    "UsageQuantityTypeDef",
    "WorkloadEstimateSummaryTypeDef",
    "WorkloadEstimateUsageItemPaginatorTypeDef",
    "WorkloadEstimateUsageItemTypeDef",
    "WorkloadEstimateUsageQuantityTypeDef",
)


class AddReservedInstanceActionTypeDef(TypedDict):
    reservedInstancesOfferingId: NotRequired[str]
    instanceCount: NotRequired[int]


class AddSavingsPlanActionTypeDef(TypedDict):
    savingsPlanOfferingId: NotRequired[str]
    commitment: NotRequired[float]


class BatchCreateBillScenarioCommitmentModificationErrorTypeDef(TypedDict):
    key: NotRequired[str]
    errorMessage: NotRequired[str]
    errorCode: NotRequired[BatchCreateBillScenarioCommitmentModificationErrorCodeType]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class BatchCreateBillScenarioUsageModificationErrorTypeDef(TypedDict):
    key: NotRequired[str]
    errorMessage: NotRequired[str]
    errorCode: NotRequired[BatchCreateBillScenarioUsageModificationErrorCodeType]


class UsageQuantityTypeDef(TypedDict):
    startHour: NotRequired[datetime]
    unit: NotRequired[str]
    amount: NotRequired[float]


class BatchCreateWorkloadEstimateUsageErrorTypeDef(TypedDict):
    key: NotRequired[str]
    errorCode: NotRequired[BatchCreateWorkloadEstimateUsageCodeType]
    errorMessage: NotRequired[str]


class WorkloadEstimateUsageQuantityTypeDef(TypedDict):
    unit: NotRequired[str]
    amount: NotRequired[float]


BatchDeleteBillScenarioCommitmentModificationErrorTypeDef = TypedDict(
    "BatchDeleteBillScenarioCommitmentModificationErrorTypeDef",
    {
        "id": NotRequired[str],
        "errorCode": NotRequired[BatchDeleteBillScenarioCommitmentModificationErrorCodeType],
        "errorMessage": NotRequired[str],
    },
)


class BatchDeleteBillScenarioCommitmentModificationRequestRequestTypeDef(TypedDict):
    billScenarioId: str
    ids: Sequence[str]


BatchDeleteBillScenarioUsageModificationErrorTypeDef = TypedDict(
    "BatchDeleteBillScenarioUsageModificationErrorTypeDef",
    {
        "id": NotRequired[str],
        "errorMessage": NotRequired[str],
        "errorCode": NotRequired[BatchDeleteBillScenarioUsageModificationErrorCodeType],
    },
)


class BatchDeleteBillScenarioUsageModificationRequestRequestTypeDef(TypedDict):
    billScenarioId: str
    ids: Sequence[str]


BatchDeleteWorkloadEstimateUsageErrorTypeDef = TypedDict(
    "BatchDeleteWorkloadEstimateUsageErrorTypeDef",
    {
        "id": NotRequired[str],
        "errorMessage": NotRequired[str],
        "errorCode": NotRequired[WorkloadEstimateUpdateUsageErrorCodeType],
    },
)


class BatchDeleteWorkloadEstimateUsageRequestRequestTypeDef(TypedDict):
    workloadEstimateId: str
    ids: Sequence[str]


BatchUpdateBillScenarioCommitmentModificationEntryTypeDef = TypedDict(
    "BatchUpdateBillScenarioCommitmentModificationEntryTypeDef",
    {
        "id": str,
        "group": NotRequired[str],
    },
)
BatchUpdateBillScenarioCommitmentModificationErrorTypeDef = TypedDict(
    "BatchUpdateBillScenarioCommitmentModificationErrorTypeDef",
    {
        "id": NotRequired[str],
        "errorCode": NotRequired[BatchUpdateBillScenarioCommitmentModificationErrorCodeType],
        "errorMessage": NotRequired[str],
    },
)
BatchUpdateBillScenarioUsageModificationErrorTypeDef = TypedDict(
    "BatchUpdateBillScenarioUsageModificationErrorTypeDef",
    {
        "id": NotRequired[str],
        "errorMessage": NotRequired[str],
        "errorCode": NotRequired[BatchUpdateBillScenarioUsageModificationErrorCodeType],
    },
)
BatchUpdateWorkloadEstimateUsageEntryTypeDef = TypedDict(
    "BatchUpdateWorkloadEstimateUsageEntryTypeDef",
    {
        "id": str,
        "group": NotRequired[str],
        "amount": NotRequired[float],
    },
)
BatchUpdateWorkloadEstimateUsageErrorTypeDef = TypedDict(
    "BatchUpdateWorkloadEstimateUsageErrorTypeDef",
    {
        "id": NotRequired[str],
        "errorMessage": NotRequired[str],
        "errorCode": NotRequired[WorkloadEstimateUpdateUsageErrorCodeType],
    },
)


class CostAmountTypeDef(TypedDict):
    amount: NotRequired[float]
    currency: NotRequired[Literal["USD"]]


class UsageQuantityResultTypeDef(TypedDict):
    amount: NotRequired[float]
    unit: NotRequired[str]


class BillIntervalOutputTypeDef(TypedDict):
    start: NotRequired[datetime]
    end: NotRequired[datetime]


TimestampTypeDef = Union[datetime, str]


class NegateReservedInstanceActionTypeDef(TypedDict):
    reservedInstancesId: NotRequired[str]


class NegateSavingsPlanActionTypeDef(TypedDict):
    savingsPlanId: NotRequired[str]


class CreateBillEstimateRequestRequestTypeDef(TypedDict):
    billScenarioId: str
    name: str
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class CreateBillScenarioRequestRequestTypeDef(TypedDict):
    name: str
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class CreateWorkloadEstimateRequestRequestTypeDef(TypedDict):
    name: str
    clientToken: NotRequired[str]
    rateType: NotRequired[WorkloadEstimateRateTypeType]
    tags: NotRequired[Mapping[str, str]]


class DeleteBillEstimateRequestRequestTypeDef(TypedDict):
    identifier: str


class DeleteBillScenarioRequestRequestTypeDef(TypedDict):
    identifier: str


class DeleteWorkloadEstimateRequestRequestTypeDef(TypedDict):
    identifier: str


class ExpressionFilterOutputTypeDef(TypedDict):
    key: NotRequired[str]
    matchOptions: NotRequired[List[str]]
    values: NotRequired[List[str]]


class ExpressionFilterTypeDef(TypedDict):
    key: NotRequired[str]
    matchOptions: NotRequired[Sequence[str]]
    values: NotRequired[Sequence[str]]


class GetBillEstimateRequestRequestTypeDef(TypedDict):
    identifier: str


class GetBillScenarioRequestRequestTypeDef(TypedDict):
    identifier: str


class GetWorkloadEstimateRequestRequestTypeDef(TypedDict):
    identifier: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListBillEstimateCommitmentsRequestRequestTypeDef(TypedDict):
    billEstimateId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListBillEstimateInputCommitmentModificationsRequestRequestTypeDef(TypedDict):
    billEstimateId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListUsageFilterTypeDef(TypedDict):
    name: ListUsageFilterNameType
    values: Sequence[str]
    matchOption: NotRequired[MatchOptionType]


class ListBillEstimateLineItemsFilterTypeDef(TypedDict):
    name: ListBillEstimateLineItemsFilterNameType
    values: Sequence[str]
    matchOption: NotRequired[MatchOptionType]


class ListBillEstimatesFilterTypeDef(TypedDict):
    name: ListBillEstimatesFilterNameType
    values: Sequence[str]
    matchOption: NotRequired[MatchOptionType]


class ListBillScenarioCommitmentModificationsRequestRequestTypeDef(TypedDict):
    billScenarioId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListBillScenariosFilterTypeDef(TypedDict):
    name: ListBillScenariosFilterNameType
    values: Sequence[str]
    matchOption: NotRequired[MatchOptionType]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    arn: str


class ListWorkloadEstimatesFilterTypeDef(TypedDict):
    name: ListWorkloadEstimatesFilterNameType
    values: Sequence[str]
    matchOption: NotRequired[MatchOptionType]


WorkloadEstimateSummaryTypeDef = TypedDict(
    "WorkloadEstimateSummaryTypeDef",
    {
        "id": str,
        "name": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "expiresAt": NotRequired[datetime],
        "rateType": NotRequired[WorkloadEstimateRateTypeType],
        "rateTimestamp": NotRequired[datetime],
        "status": NotRequired[WorkloadEstimateStatusType],
        "totalCost": NotRequired[float],
        "costCurrency": NotRequired[Literal["USD"]],
        "failureMessage": NotRequired[str],
    },
)


class TagResourceRequestRequestTypeDef(TypedDict):
    arn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    arn: str
    tagKeys: Sequence[str]


class UpdatePreferencesRequestRequestTypeDef(TypedDict):
    managementAccountRateTypeSelections: NotRequired[Sequence[RateTypeType]]
    memberAccountRateTypeSelections: NotRequired[Sequence[RateTypeType]]


CreateWorkloadEstimateResponseTypeDef = TypedDict(
    "CreateWorkloadEstimateResponseTypeDef",
    {
        "id": str,
        "name": str,
        "createdAt": datetime,
        "expiresAt": datetime,
        "rateType": WorkloadEstimateRateTypeType,
        "rateTimestamp": datetime,
        "status": WorkloadEstimateStatusType,
        "totalCost": float,
        "costCurrency": Literal["USD"],
        "failureMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class GetPreferencesResponseTypeDef(TypedDict):
    managementAccountRateTypeSelections: List[RateTypeType]
    memberAccountRateTypeSelections: List[RateTypeType]
    ResponseMetadata: ResponseMetadataTypeDef


GetWorkloadEstimateResponseTypeDef = TypedDict(
    "GetWorkloadEstimateResponseTypeDef",
    {
        "id": str,
        "name": str,
        "createdAt": datetime,
        "expiresAt": datetime,
        "rateType": WorkloadEstimateRateTypeType,
        "rateTimestamp": datetime,
        "status": WorkloadEstimateStatusType,
        "totalCost": float,
        "costCurrency": Literal["USD"],
        "failureMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePreferencesResponseTypeDef(TypedDict):
    managementAccountRateTypeSelections: List[RateTypeType]
    memberAccountRateTypeSelections: List[RateTypeType]
    ResponseMetadata: ResponseMetadataTypeDef


UpdateWorkloadEstimateResponseTypeDef = TypedDict(
    "UpdateWorkloadEstimateResponseTypeDef",
    {
        "id": str,
        "name": str,
        "createdAt": datetime,
        "expiresAt": datetime,
        "rateType": WorkloadEstimateRateTypeType,
        "rateTimestamp": datetime,
        "status": WorkloadEstimateStatusType,
        "totalCost": float,
        "costCurrency": Literal["USD"],
        "failureMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class BatchDeleteBillScenarioCommitmentModificationResponseTypeDef(TypedDict):
    errors: List[BatchDeleteBillScenarioCommitmentModificationErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchDeleteBillScenarioUsageModificationResponseTypeDef(TypedDict):
    errors: List[BatchDeleteBillScenarioUsageModificationErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchDeleteWorkloadEstimateUsageResponseTypeDef(TypedDict):
    errors: List[BatchDeleteWorkloadEstimateUsageErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchUpdateBillScenarioCommitmentModificationRequestRequestTypeDef(TypedDict):
    billScenarioId: str
    commitmentModifications: Sequence[BatchUpdateBillScenarioCommitmentModificationEntryTypeDef]


class BatchUpdateWorkloadEstimateUsageRequestRequestTypeDef(TypedDict):
    workloadEstimateId: str
    usage: Sequence[BatchUpdateWorkloadEstimateUsageEntryTypeDef]


BillEstimateCommitmentSummaryTypeDef = TypedDict(
    "BillEstimateCommitmentSummaryTypeDef",
    {
        "id": NotRequired[str],
        "purchaseAgreementType": NotRequired[PurchaseAgreementTypeType],
        "offeringId": NotRequired[str],
        "usageAccountId": NotRequired[str],
        "region": NotRequired[str],
        "termLength": NotRequired[str],
        "paymentOption": NotRequired[str],
        "upfrontPayment": NotRequired[CostAmountTypeDef],
        "monthlyPayment": NotRequired[CostAmountTypeDef],
    },
)


class CostDifferenceTypeDef(TypedDict):
    historicalCost: NotRequired[CostAmountTypeDef]
    estimatedCost: NotRequired[CostAmountTypeDef]


BillEstimateLineItemSummaryTypeDef = TypedDict(
    "BillEstimateLineItemSummaryTypeDef",
    {
        "serviceCode": str,
        "usageType": str,
        "operation": str,
        "location": NotRequired[str],
        "availabilityZone": NotRequired[str],
        "id": NotRequired[str],
        "lineItemId": NotRequired[str],
        "lineItemType": NotRequired[str],
        "payerAccountId": NotRequired[str],
        "usageAccountId": NotRequired[str],
        "estimatedUsageQuantity": NotRequired[UsageQuantityResultTypeDef],
        "estimatedCost": NotRequired[CostAmountTypeDef],
        "historicalUsageQuantity": NotRequired[UsageQuantityResultTypeDef],
        "historicalCost": NotRequired[CostAmountTypeDef],
        "savingsPlanArns": NotRequired[List[str]],
    },
)
BillEstimateSummaryTypeDef = TypedDict(
    "BillEstimateSummaryTypeDef",
    {
        "id": str,
        "name": NotRequired[str],
        "status": NotRequired[BillEstimateStatusType],
        "billInterval": NotRequired[BillIntervalOutputTypeDef],
        "createdAt": NotRequired[datetime],
        "expiresAt": NotRequired[datetime],
    },
)
BillScenarioSummaryTypeDef = TypedDict(
    "BillScenarioSummaryTypeDef",
    {
        "id": str,
        "name": NotRequired[str],
        "billInterval": NotRequired[BillIntervalOutputTypeDef],
        "status": NotRequired[BillScenarioStatusType],
        "createdAt": NotRequired[datetime],
        "expiresAt": NotRequired[datetime],
        "failureMessage": NotRequired[str],
    },
)
CreateBillScenarioResponseTypeDef = TypedDict(
    "CreateBillScenarioResponseTypeDef",
    {
        "id": str,
        "name": str,
        "billInterval": BillIntervalOutputTypeDef,
        "status": BillScenarioStatusType,
        "createdAt": datetime,
        "expiresAt": datetime,
        "failureMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetBillScenarioResponseTypeDef = TypedDict(
    "GetBillScenarioResponseTypeDef",
    {
        "id": str,
        "name": str,
        "billInterval": BillIntervalOutputTypeDef,
        "status": BillScenarioStatusType,
        "createdAt": datetime,
        "expiresAt": datetime,
        "failureMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateBillScenarioResponseTypeDef = TypedDict(
    "UpdateBillScenarioResponseTypeDef",
    {
        "id": str,
        "name": str,
        "billInterval": BillIntervalOutputTypeDef,
        "status": BillScenarioStatusType,
        "createdAt": datetime,
        "expiresAt": datetime,
        "failureMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class BillIntervalTypeDef(TypedDict):
    start: NotRequired[TimestampTypeDef]
    end: NotRequired[TimestampTypeDef]


class FilterTimestampTypeDef(TypedDict):
    afterTimestamp: NotRequired[TimestampTypeDef]
    beforeTimestamp: NotRequired[TimestampTypeDef]


class UpdateBillEstimateRequestRequestTypeDef(TypedDict):
    identifier: str
    name: NotRequired[str]
    expiresAt: NotRequired[TimestampTypeDef]


class UpdateBillScenarioRequestRequestTypeDef(TypedDict):
    identifier: str
    name: NotRequired[str]
    expiresAt: NotRequired[TimestampTypeDef]


class UpdateWorkloadEstimateRequestRequestTypeDef(TypedDict):
    identifier: str
    name: NotRequired[str]
    expiresAt: NotRequired[TimestampTypeDef]


class UsageAmountTypeDef(TypedDict):
    startHour: TimestampTypeDef
    amount: float


class BillScenarioCommitmentModificationActionTypeDef(TypedDict):
    addReservedInstanceAction: NotRequired[AddReservedInstanceActionTypeDef]
    addSavingsPlanAction: NotRequired[AddSavingsPlanActionTypeDef]
    negateReservedInstanceAction: NotRequired[NegateReservedInstanceActionTypeDef]
    negateSavingsPlanAction: NotRequired[NegateSavingsPlanActionTypeDef]


ExpressionOutputTypeDef = TypedDict(
    "ExpressionOutputTypeDef",
    {
        "and": NotRequired[List[Dict[str, Any]]],
        "or": NotRequired[List[Dict[str, Any]]],
        "not": NotRequired[Dict[str, Any]],
        "costCategories": NotRequired[ExpressionFilterOutputTypeDef],
        "dimensions": NotRequired[ExpressionFilterOutputTypeDef],
        "tags": NotRequired[ExpressionFilterOutputTypeDef],
    },
)
ExpressionPaginatorTypeDef = TypedDict(
    "ExpressionPaginatorTypeDef",
    {
        "and": NotRequired[List[Dict[str, Any]]],
        "or": NotRequired[List[Dict[str, Any]]],
        "not": NotRequired[Dict[str, Any]],
        "costCategories": NotRequired[ExpressionFilterOutputTypeDef],
        "dimensions": NotRequired[ExpressionFilterOutputTypeDef],
        "tags": NotRequired[ExpressionFilterOutputTypeDef],
    },
)
ExpressionFilterUnionTypeDef = Union[ExpressionFilterTypeDef, ExpressionFilterOutputTypeDef]


class ListBillEstimateCommitmentsRequestListBillEstimateCommitmentsPaginateTypeDef(TypedDict):
    billEstimateId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBillEstimateInputCommitmentModificationsRequestListBillEstimateInputCommitmentModificationsPaginateTypeDef(
    TypedDict
):
    billEstimateId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBillScenarioCommitmentModificationsRequestListBillScenarioCommitmentModificationsPaginateTypeDef(
    TypedDict
):
    billScenarioId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBillEstimateInputUsageModificationsRequestListBillEstimateInputUsageModificationsPaginateTypeDef(
    TypedDict
):
    billEstimateId: str
    filters: NotRequired[Sequence[ListUsageFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBillEstimateInputUsageModificationsRequestRequestTypeDef(TypedDict):
    billEstimateId: str
    filters: NotRequired[Sequence[ListUsageFilterTypeDef]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListBillScenarioUsageModificationsRequestListBillScenarioUsageModificationsPaginateTypeDef(
    TypedDict
):
    billScenarioId: str
    filters: NotRequired[Sequence[ListUsageFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBillScenarioUsageModificationsRequestRequestTypeDef(TypedDict):
    billScenarioId: str
    filters: NotRequired[Sequence[ListUsageFilterTypeDef]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListWorkloadEstimateUsageRequestListWorkloadEstimateUsagePaginateTypeDef(TypedDict):
    workloadEstimateId: str
    filters: NotRequired[Sequence[ListUsageFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkloadEstimateUsageRequestRequestTypeDef(TypedDict):
    workloadEstimateId: str
    filters: NotRequired[Sequence[ListUsageFilterTypeDef]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListBillEstimateLineItemsRequestListBillEstimateLineItemsPaginateTypeDef(TypedDict):
    billEstimateId: str
    filters: NotRequired[Sequence[ListBillEstimateLineItemsFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBillEstimateLineItemsRequestRequestTypeDef(TypedDict):
    billEstimateId: str
    filters: NotRequired[Sequence[ListBillEstimateLineItemsFilterTypeDef]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListWorkloadEstimatesResponseTypeDef(TypedDict):
    items: List[WorkloadEstimateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListBillEstimateCommitmentsResponseTypeDef(TypedDict):
    items: List[BillEstimateCommitmentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class BillEstimateCostSummaryTypeDef(TypedDict):
    totalCostDifference: NotRequired[CostDifferenceTypeDef]
    serviceCostDifferences: NotRequired[Dict[str, CostDifferenceTypeDef]]


class ListBillEstimateLineItemsResponseTypeDef(TypedDict):
    items: List[BillEstimateLineItemSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListBillEstimatesResponseTypeDef(TypedDict):
    items: List[BillEstimateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListBillScenariosResponseTypeDef(TypedDict):
    items: List[BillScenarioSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


BillIntervalUnionTypeDef = Union[BillIntervalTypeDef, BillIntervalOutputTypeDef]


class ListBillEstimatesRequestListBillEstimatesPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[ListBillEstimatesFilterTypeDef]]
    createdAtFilter: NotRequired[FilterTimestampTypeDef]
    expiresAtFilter: NotRequired[FilterTimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBillEstimatesRequestRequestTypeDef(TypedDict):
    filters: NotRequired[Sequence[ListBillEstimatesFilterTypeDef]]
    createdAtFilter: NotRequired[FilterTimestampTypeDef]
    expiresAtFilter: NotRequired[FilterTimestampTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListBillScenariosRequestListBillScenariosPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[ListBillScenariosFilterTypeDef]]
    createdAtFilter: NotRequired[FilterTimestampTypeDef]
    expiresAtFilter: NotRequired[FilterTimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBillScenariosRequestRequestTypeDef(TypedDict):
    filters: NotRequired[Sequence[ListBillScenariosFilterTypeDef]]
    createdAtFilter: NotRequired[FilterTimestampTypeDef]
    expiresAtFilter: NotRequired[FilterTimestampTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListWorkloadEstimatesRequestListWorkloadEstimatesPaginateTypeDef(TypedDict):
    createdAtFilter: NotRequired[FilterTimestampTypeDef]
    expiresAtFilter: NotRequired[FilterTimestampTypeDef]
    filters: NotRequired[Sequence[ListWorkloadEstimatesFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkloadEstimatesRequestRequestTypeDef(TypedDict):
    createdAtFilter: NotRequired[FilterTimestampTypeDef]
    expiresAtFilter: NotRequired[FilterTimestampTypeDef]
    filters: NotRequired[Sequence[ListWorkloadEstimatesFilterTypeDef]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


BatchUpdateBillScenarioUsageModificationEntryTypeDef = TypedDict(
    "BatchUpdateBillScenarioUsageModificationEntryTypeDef",
    {
        "id": str,
        "group": NotRequired[str],
        "amounts": NotRequired[Sequence[UsageAmountTypeDef]],
    },
)


class BatchCreateBillScenarioCommitmentModificationEntryTypeDef(TypedDict):
    key: str
    usageAccountId: str
    commitmentAction: BillScenarioCommitmentModificationActionTypeDef
    group: NotRequired[str]


BatchCreateBillScenarioCommitmentModificationItemTypeDef = TypedDict(
    "BatchCreateBillScenarioCommitmentModificationItemTypeDef",
    {
        "key": NotRequired[str],
        "id": NotRequired[str],
        "group": NotRequired[str],
        "usageAccountId": NotRequired[str],
        "commitmentAction": NotRequired[BillScenarioCommitmentModificationActionTypeDef],
    },
)
BillEstimateInputCommitmentModificationSummaryTypeDef = TypedDict(
    "BillEstimateInputCommitmentModificationSummaryTypeDef",
    {
        "id": NotRequired[str],
        "group": NotRequired[str],
        "usageAccountId": NotRequired[str],
        "commitmentAction": NotRequired[BillScenarioCommitmentModificationActionTypeDef],
    },
)
BillScenarioCommitmentModificationItemTypeDef = TypedDict(
    "BillScenarioCommitmentModificationItemTypeDef",
    {
        "id": NotRequired[str],
        "usageAccountId": NotRequired[str],
        "group": NotRequired[str],
        "commitmentAction": NotRequired[BillScenarioCommitmentModificationActionTypeDef],
    },
)


class HistoricalUsageEntityOutputTypeDef(TypedDict):
    serviceCode: str
    usageType: str
    operation: str
    usageAccountId: str
    billInterval: BillIntervalOutputTypeDef
    filterExpression: ExpressionOutputTypeDef
    location: NotRequired[str]


class HistoricalUsageEntityPaginatorTypeDef(TypedDict):
    serviceCode: str
    usageType: str
    operation: str
    usageAccountId: str
    billInterval: BillIntervalOutputTypeDef
    filterExpression: ExpressionPaginatorTypeDef
    location: NotRequired[str]


ExpressionTypeDef = TypedDict(
    "ExpressionTypeDef",
    {
        "and": NotRequired[Sequence[Mapping[str, Any]]],
        "or": NotRequired[Sequence[Mapping[str, Any]]],
        "not": NotRequired[Mapping[str, Any]],
        "costCategories": NotRequired[ExpressionFilterUnionTypeDef],
        "dimensions": NotRequired[ExpressionFilterUnionTypeDef],
        "tags": NotRequired[ExpressionFilterUnionTypeDef],
    },
)
CreateBillEstimateResponseTypeDef = TypedDict(
    "CreateBillEstimateResponseTypeDef",
    {
        "id": str,
        "name": str,
        "status": BillEstimateStatusType,
        "failureMessage": str,
        "billInterval": BillIntervalOutputTypeDef,
        "costSummary": BillEstimateCostSummaryTypeDef,
        "createdAt": datetime,
        "expiresAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetBillEstimateResponseTypeDef = TypedDict(
    "GetBillEstimateResponseTypeDef",
    {
        "id": str,
        "name": str,
        "status": BillEstimateStatusType,
        "failureMessage": str,
        "billInterval": BillIntervalOutputTypeDef,
        "costSummary": BillEstimateCostSummaryTypeDef,
        "createdAt": datetime,
        "expiresAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateBillEstimateResponseTypeDef = TypedDict(
    "UpdateBillEstimateResponseTypeDef",
    {
        "id": str,
        "name": str,
        "status": BillEstimateStatusType,
        "failureMessage": str,
        "billInterval": BillIntervalOutputTypeDef,
        "costSummary": BillEstimateCostSummaryTypeDef,
        "createdAt": datetime,
        "expiresAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class BatchUpdateBillScenarioUsageModificationRequestRequestTypeDef(TypedDict):
    billScenarioId: str
    usageModifications: Sequence[BatchUpdateBillScenarioUsageModificationEntryTypeDef]


class BatchCreateBillScenarioCommitmentModificationRequestRequestTypeDef(TypedDict):
    billScenarioId: str
    commitmentModifications: Sequence[BatchCreateBillScenarioCommitmentModificationEntryTypeDef]
    clientToken: NotRequired[str]


class BatchCreateBillScenarioCommitmentModificationResponseTypeDef(TypedDict):
    items: List[BatchCreateBillScenarioCommitmentModificationItemTypeDef]
    errors: List[BatchCreateBillScenarioCommitmentModificationErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListBillEstimateInputCommitmentModificationsResponseTypeDef(TypedDict):
    items: List[BillEstimateInputCommitmentModificationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class BatchUpdateBillScenarioCommitmentModificationResponseTypeDef(TypedDict):
    items: List[BillScenarioCommitmentModificationItemTypeDef]
    errors: List[BatchUpdateBillScenarioCommitmentModificationErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListBillScenarioCommitmentModificationsResponseTypeDef(TypedDict):
    items: List[BillScenarioCommitmentModificationItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


BatchCreateBillScenarioUsageModificationItemTypeDef = TypedDict(
    "BatchCreateBillScenarioUsageModificationItemTypeDef",
    {
        "serviceCode": str,
        "usageType": str,
        "operation": str,
        "location": NotRequired[str],
        "availabilityZone": NotRequired[str],
        "id": NotRequired[str],
        "group": NotRequired[str],
        "usageAccountId": NotRequired[str],
        "quantities": NotRequired[List[UsageQuantityTypeDef]],
        "historicalUsage": NotRequired[HistoricalUsageEntityOutputTypeDef],
        "key": NotRequired[str],
    },
)
BatchCreateWorkloadEstimateUsageItemTypeDef = TypedDict(
    "BatchCreateWorkloadEstimateUsageItemTypeDef",
    {
        "serviceCode": str,
        "usageType": str,
        "operation": str,
        "location": NotRequired[str],
        "id": NotRequired[str],
        "usageAccountId": NotRequired[str],
        "group": NotRequired[str],
        "quantity": NotRequired[WorkloadEstimateUsageQuantityTypeDef],
        "cost": NotRequired[float],
        "currency": NotRequired[Literal["USD"]],
        "status": NotRequired[WorkloadEstimateCostStatusType],
        "historicalUsage": NotRequired[HistoricalUsageEntityOutputTypeDef],
        "key": NotRequired[str],
    },
)
BillEstimateInputUsageModificationSummaryTypeDef = TypedDict(
    "BillEstimateInputUsageModificationSummaryTypeDef",
    {
        "serviceCode": str,
        "usageType": str,
        "operation": str,
        "location": NotRequired[str],
        "availabilityZone": NotRequired[str],
        "id": NotRequired[str],
        "group": NotRequired[str],
        "usageAccountId": NotRequired[str],
        "quantities": NotRequired[List[UsageQuantityTypeDef]],
        "historicalUsage": NotRequired[HistoricalUsageEntityOutputTypeDef],
    },
)
BillScenarioUsageModificationItemTypeDef = TypedDict(
    "BillScenarioUsageModificationItemTypeDef",
    {
        "serviceCode": str,
        "usageType": str,
        "operation": str,
        "location": NotRequired[str],
        "availabilityZone": NotRequired[str],
        "id": NotRequired[str],
        "group": NotRequired[str],
        "usageAccountId": NotRequired[str],
        "quantities": NotRequired[List[UsageQuantityTypeDef]],
        "historicalUsage": NotRequired[HistoricalUsageEntityOutputTypeDef],
    },
)
WorkloadEstimateUsageItemTypeDef = TypedDict(
    "WorkloadEstimateUsageItemTypeDef",
    {
        "serviceCode": str,
        "usageType": str,
        "operation": str,
        "location": NotRequired[str],
        "id": NotRequired[str],
        "usageAccountId": NotRequired[str],
        "group": NotRequired[str],
        "quantity": NotRequired[WorkloadEstimateUsageQuantityTypeDef],
        "cost": NotRequired[float],
        "currency": NotRequired[Literal["USD"]],
        "status": NotRequired[WorkloadEstimateCostStatusType],
        "historicalUsage": NotRequired[HistoricalUsageEntityOutputTypeDef],
    },
)
BillEstimateInputUsageModificationSummaryPaginatorTypeDef = TypedDict(
    "BillEstimateInputUsageModificationSummaryPaginatorTypeDef",
    {
        "serviceCode": str,
        "usageType": str,
        "operation": str,
        "location": NotRequired[str],
        "availabilityZone": NotRequired[str],
        "id": NotRequired[str],
        "group": NotRequired[str],
        "usageAccountId": NotRequired[str],
        "quantities": NotRequired[List[UsageQuantityTypeDef]],
        "historicalUsage": NotRequired[HistoricalUsageEntityPaginatorTypeDef],
    },
)
BillScenarioUsageModificationItemPaginatorTypeDef = TypedDict(
    "BillScenarioUsageModificationItemPaginatorTypeDef",
    {
        "serviceCode": str,
        "usageType": str,
        "operation": str,
        "location": NotRequired[str],
        "availabilityZone": NotRequired[str],
        "id": NotRequired[str],
        "group": NotRequired[str],
        "usageAccountId": NotRequired[str],
        "quantities": NotRequired[List[UsageQuantityTypeDef]],
        "historicalUsage": NotRequired[HistoricalUsageEntityPaginatorTypeDef],
    },
)
WorkloadEstimateUsageItemPaginatorTypeDef = TypedDict(
    "WorkloadEstimateUsageItemPaginatorTypeDef",
    {
        "serviceCode": str,
        "usageType": str,
        "operation": str,
        "location": NotRequired[str],
        "id": NotRequired[str],
        "usageAccountId": NotRequired[str],
        "group": NotRequired[str],
        "quantity": NotRequired[WorkloadEstimateUsageQuantityTypeDef],
        "cost": NotRequired[float],
        "currency": NotRequired[Literal["USD"]],
        "status": NotRequired[WorkloadEstimateCostStatusType],
        "historicalUsage": NotRequired[HistoricalUsageEntityPaginatorTypeDef],
    },
)
ExpressionUnionTypeDef = Union[ExpressionTypeDef, ExpressionOutputTypeDef]


class BatchCreateBillScenarioUsageModificationResponseTypeDef(TypedDict):
    items: List[BatchCreateBillScenarioUsageModificationItemTypeDef]
    errors: List[BatchCreateBillScenarioUsageModificationErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchCreateWorkloadEstimateUsageResponseTypeDef(TypedDict):
    items: List[BatchCreateWorkloadEstimateUsageItemTypeDef]
    errors: List[BatchCreateWorkloadEstimateUsageErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListBillEstimateInputUsageModificationsResponseTypeDef(TypedDict):
    items: List[BillEstimateInputUsageModificationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class BatchUpdateBillScenarioUsageModificationResponseTypeDef(TypedDict):
    items: List[BillScenarioUsageModificationItemTypeDef]
    errors: List[BatchUpdateBillScenarioUsageModificationErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListBillScenarioUsageModificationsResponseTypeDef(TypedDict):
    items: List[BillScenarioUsageModificationItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class BatchUpdateWorkloadEstimateUsageResponseTypeDef(TypedDict):
    items: List[WorkloadEstimateUsageItemTypeDef]
    errors: List[BatchUpdateWorkloadEstimateUsageErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListWorkloadEstimateUsageResponseTypeDef(TypedDict):
    items: List[WorkloadEstimateUsageItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListBillEstimateInputUsageModificationsResponsePaginatorTypeDef(TypedDict):
    items: List[BillEstimateInputUsageModificationSummaryPaginatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListBillScenarioUsageModificationsResponsePaginatorTypeDef(TypedDict):
    items: List[BillScenarioUsageModificationItemPaginatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListWorkloadEstimateUsageResponsePaginatorTypeDef(TypedDict):
    items: List[WorkloadEstimateUsageItemPaginatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class HistoricalUsageEntityTypeDef(TypedDict):
    serviceCode: str
    usageType: str
    operation: str
    usageAccountId: str
    billInterval: BillIntervalUnionTypeDef
    filterExpression: ExpressionUnionTypeDef
    location: NotRequired[str]


HistoricalUsageEntityUnionTypeDef = Union[
    HistoricalUsageEntityTypeDef, HistoricalUsageEntityOutputTypeDef
]


class BatchCreateBillScenarioUsageModificationEntryTypeDef(TypedDict):
    serviceCode: str
    usageType: str
    operation: str
    key: str
    usageAccountId: str
    availabilityZone: NotRequired[str]
    group: NotRequired[str]
    amounts: NotRequired[Sequence[UsageAmountTypeDef]]
    historicalUsage: NotRequired[HistoricalUsageEntityUnionTypeDef]


class BatchCreateWorkloadEstimateUsageEntryTypeDef(TypedDict):
    serviceCode: str
    usageType: str
    operation: str
    key: str
    usageAccountId: str
    amount: float
    group: NotRequired[str]
    historicalUsage: NotRequired[HistoricalUsageEntityUnionTypeDef]


class BatchCreateBillScenarioUsageModificationRequestRequestTypeDef(TypedDict):
    billScenarioId: str
    usageModifications: Sequence[BatchCreateBillScenarioUsageModificationEntryTypeDef]
    clientToken: NotRequired[str]


class BatchCreateWorkloadEstimateUsageRequestRequestTypeDef(TypedDict):
    workloadEstimateId: str
    usage: Sequence[BatchCreateWorkloadEstimateUsageEntryTypeDef]
    clientToken: NotRequired[str]
