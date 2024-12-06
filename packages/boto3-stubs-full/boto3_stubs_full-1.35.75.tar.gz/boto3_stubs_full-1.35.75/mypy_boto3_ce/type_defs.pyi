"""
Type annotations for ce service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ce/type_defs/)

Usage::

    ```python
    from mypy_boto3_ce.type_defs import AnomalyDateIntervalTypeDef

    data: AnomalyDateIntervalTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AccountScopeType,
    AnalysisStatusType,
    AnalysisTypeType,
    AnomalyFeedbackTypeType,
    AnomalySubscriptionFrequencyType,
    ApproximationDimensionType,
    ContextType,
    CostAllocationTagBackfillStatusType,
    CostAllocationTagStatusType,
    CostAllocationTagTypeType,
    CostCategoryInheritedValueDimensionNameType,
    CostCategoryRuleTypeType,
    CostCategorySplitChargeMethodType,
    CostCategoryStatusType,
    DimensionType,
    ErrorCodeType,
    FindingReasonCodeType,
    GenerationStatusType,
    GranularityType,
    GroupDefinitionTypeType,
    LookbackPeriodInDaysType,
    MatchOptionType,
    MetricType,
    MonitorTypeType,
    NumericOperatorType,
    OfferingClassType,
    PaymentOptionType,
    PlatformDifferenceType,
    RecommendationTargetType,
    RightsizingTypeType,
    SavingsPlansDataTypeType,
    SortOrderType,
    SubscriberStatusType,
    SubscriberTypeType,
    SupportedSavingsPlansTypeType,
    TermInYearsType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AnalysisDetailsTypeDef",
    "AnalysisSummaryTypeDef",
    "AnomalyDateIntervalTypeDef",
    "AnomalyMonitorOutputTypeDef",
    "AnomalyMonitorTypeDef",
    "AnomalyScoreTypeDef",
    "AnomalySubscriptionOutputTypeDef",
    "AnomalySubscriptionTypeDef",
    "AnomalyTypeDef",
    "CommitmentPurchaseAnalysisConfigurationOutputTypeDef",
    "CommitmentPurchaseAnalysisConfigurationTypeDef",
    "CostAllocationTagBackfillRequestTypeDef",
    "CostAllocationTagStatusEntryTypeDef",
    "CostAllocationTagTypeDef",
    "CostCategoryInheritedValueDimensionTypeDef",
    "CostCategoryProcessingStatusTypeDef",
    "CostCategoryReferenceTypeDef",
    "CostCategoryRuleOutputTypeDef",
    "CostCategoryRuleTypeDef",
    "CostCategoryRuleUnionTypeDef",
    "CostCategorySplitChargeRuleOutputTypeDef",
    "CostCategorySplitChargeRuleParameterOutputTypeDef",
    "CostCategorySplitChargeRuleParameterTypeDef",
    "CostCategorySplitChargeRuleParameterUnionTypeDef",
    "CostCategorySplitChargeRuleTypeDef",
    "CostCategorySplitChargeRuleUnionTypeDef",
    "CostCategoryTypeDef",
    "CostCategoryValuesOutputTypeDef",
    "CostCategoryValuesTypeDef",
    "CostCategoryValuesUnionTypeDef",
    "CoverageByTimeTypeDef",
    "CoverageCostTypeDef",
    "CoverageHoursTypeDef",
    "CoverageNormalizedUnitsTypeDef",
    "CoverageTypeDef",
    "CreateAnomalyMonitorRequestRequestTypeDef",
    "CreateAnomalyMonitorResponseTypeDef",
    "CreateAnomalySubscriptionRequestRequestTypeDef",
    "CreateAnomalySubscriptionResponseTypeDef",
    "CreateCostCategoryDefinitionRequestRequestTypeDef",
    "CreateCostCategoryDefinitionResponseTypeDef",
    "CurrentInstanceTypeDef",
    "DateIntervalTypeDef",
    "DeleteAnomalyMonitorRequestRequestTypeDef",
    "DeleteAnomalySubscriptionRequestRequestTypeDef",
    "DeleteCostCategoryDefinitionRequestRequestTypeDef",
    "DeleteCostCategoryDefinitionResponseTypeDef",
    "DescribeCostCategoryDefinitionRequestRequestTypeDef",
    "DescribeCostCategoryDefinitionResponseTypeDef",
    "DimensionValuesOutputTypeDef",
    "DimensionValuesTypeDef",
    "DimensionValuesUnionTypeDef",
    "DimensionValuesWithAttributesTypeDef",
    "DiskResourceUtilizationTypeDef",
    "DynamoDBCapacityDetailsTypeDef",
    "EBSResourceUtilizationTypeDef",
    "EC2InstanceDetailsTypeDef",
    "EC2ResourceDetailsTypeDef",
    "EC2ResourceUtilizationTypeDef",
    "EC2SpecificationTypeDef",
    "ESInstanceDetailsTypeDef",
    "ElastiCacheInstanceDetailsTypeDef",
    "ExpressionOutputTypeDef",
    "ExpressionTypeDef",
    "ExpressionUnionTypeDef",
    "ForecastResultTypeDef",
    "GenerationSummaryTypeDef",
    "GetAnomaliesRequestRequestTypeDef",
    "GetAnomaliesResponseTypeDef",
    "GetAnomalyMonitorsRequestRequestTypeDef",
    "GetAnomalyMonitorsResponseTypeDef",
    "GetAnomalySubscriptionsRequestRequestTypeDef",
    "GetAnomalySubscriptionsResponseTypeDef",
    "GetApproximateUsageRecordsRequestRequestTypeDef",
    "GetApproximateUsageRecordsResponseTypeDef",
    "GetCommitmentPurchaseAnalysisRequestRequestTypeDef",
    "GetCommitmentPurchaseAnalysisResponseTypeDef",
    "GetCostAndUsageRequestRequestTypeDef",
    "GetCostAndUsageResponseTypeDef",
    "GetCostAndUsageWithResourcesRequestRequestTypeDef",
    "GetCostAndUsageWithResourcesResponseTypeDef",
    "GetCostCategoriesRequestRequestTypeDef",
    "GetCostCategoriesResponseTypeDef",
    "GetCostForecastRequestRequestTypeDef",
    "GetCostForecastResponseTypeDef",
    "GetDimensionValuesRequestRequestTypeDef",
    "GetDimensionValuesResponseTypeDef",
    "GetReservationCoverageRequestRequestTypeDef",
    "GetReservationCoverageResponseTypeDef",
    "GetReservationPurchaseRecommendationRequestRequestTypeDef",
    "GetReservationPurchaseRecommendationResponseTypeDef",
    "GetReservationUtilizationRequestRequestTypeDef",
    "GetReservationUtilizationResponseTypeDef",
    "GetRightsizingRecommendationRequestRequestTypeDef",
    "GetRightsizingRecommendationResponseTypeDef",
    "GetSavingsPlanPurchaseRecommendationDetailsRequestRequestTypeDef",
    "GetSavingsPlanPurchaseRecommendationDetailsResponseTypeDef",
    "GetSavingsPlansCoverageRequestRequestTypeDef",
    "GetSavingsPlansCoverageResponseTypeDef",
    "GetSavingsPlansPurchaseRecommendationRequestRequestTypeDef",
    "GetSavingsPlansPurchaseRecommendationResponseTypeDef",
    "GetSavingsPlansUtilizationDetailsRequestRequestTypeDef",
    "GetSavingsPlansUtilizationDetailsResponseTypeDef",
    "GetSavingsPlansUtilizationRequestRequestTypeDef",
    "GetSavingsPlansUtilizationResponseTypeDef",
    "GetTagsRequestRequestTypeDef",
    "GetTagsResponseTypeDef",
    "GetUsageForecastRequestRequestTypeDef",
    "GetUsageForecastResponseTypeDef",
    "GroupDefinitionTypeDef",
    "GroupTypeDef",
    "ImpactTypeDef",
    "InstanceDetailsTypeDef",
    "ListCommitmentPurchaseAnalysesRequestRequestTypeDef",
    "ListCommitmentPurchaseAnalysesResponseTypeDef",
    "ListCostAllocationTagBackfillHistoryRequestRequestTypeDef",
    "ListCostAllocationTagBackfillHistoryResponseTypeDef",
    "ListCostAllocationTagsRequestRequestTypeDef",
    "ListCostAllocationTagsResponseTypeDef",
    "ListCostCategoryDefinitionsRequestRequestTypeDef",
    "ListCostCategoryDefinitionsResponseTypeDef",
    "ListSavingsPlansPurchaseRecommendationGenerationRequestRequestTypeDef",
    "ListSavingsPlansPurchaseRecommendationGenerationResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MemoryDBInstanceDetailsTypeDef",
    "MetricValueTypeDef",
    "ModifyRecommendationDetailTypeDef",
    "NetworkResourceUtilizationTypeDef",
    "ProvideAnomalyFeedbackRequestRequestTypeDef",
    "ProvideAnomalyFeedbackResponseTypeDef",
    "RDSInstanceDetailsTypeDef",
    "RecommendationDetailDataTypeDef",
    "RecommendationDetailHourlyMetricsTypeDef",
    "RedshiftInstanceDetailsTypeDef",
    "ReservationAggregatesTypeDef",
    "ReservationCoverageGroupTypeDef",
    "ReservationPurchaseRecommendationDetailTypeDef",
    "ReservationPurchaseRecommendationMetadataTypeDef",
    "ReservationPurchaseRecommendationSummaryTypeDef",
    "ReservationPurchaseRecommendationTypeDef",
    "ReservationUtilizationGroupTypeDef",
    "ReservedCapacityDetailsTypeDef",
    "ResourceDetailsTypeDef",
    "ResourceTagTypeDef",
    "ResourceUtilizationTypeDef",
    "ResponseMetadataTypeDef",
    "ResultByTimeTypeDef",
    "RightsizingRecommendationConfigurationTypeDef",
    "RightsizingRecommendationMetadataTypeDef",
    "RightsizingRecommendationSummaryTypeDef",
    "RightsizingRecommendationTypeDef",
    "RootCauseImpactTypeDef",
    "RootCauseTypeDef",
    "SavingsPlansAmortizedCommitmentTypeDef",
    "SavingsPlansCoverageDataTypeDef",
    "SavingsPlansCoverageTypeDef",
    "SavingsPlansDetailsTypeDef",
    "SavingsPlansPurchaseAnalysisConfigurationOutputTypeDef",
    "SavingsPlansPurchaseAnalysisConfigurationTypeDef",
    "SavingsPlansPurchaseAnalysisConfigurationUnionTypeDef",
    "SavingsPlansPurchaseAnalysisDetailsTypeDef",
    "SavingsPlansPurchaseRecommendationDetailTypeDef",
    "SavingsPlansPurchaseRecommendationMetadataTypeDef",
    "SavingsPlansPurchaseRecommendationSummaryTypeDef",
    "SavingsPlansPurchaseRecommendationTypeDef",
    "SavingsPlansSavingsTypeDef",
    "SavingsPlansTypeDef",
    "SavingsPlansUtilizationAggregatesTypeDef",
    "SavingsPlansUtilizationByTimeTypeDef",
    "SavingsPlansUtilizationDetailTypeDef",
    "SavingsPlansUtilizationTypeDef",
    "ServiceSpecificationTypeDef",
    "SortDefinitionTypeDef",
    "StartCommitmentPurchaseAnalysisRequestRequestTypeDef",
    "StartCommitmentPurchaseAnalysisResponseTypeDef",
    "StartCostAllocationTagBackfillRequestRequestTypeDef",
    "StartCostAllocationTagBackfillResponseTypeDef",
    "StartSavingsPlansPurchaseRecommendationGenerationResponseTypeDef",
    "SubscriberTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagValuesOutputTypeDef",
    "TagValuesTypeDef",
    "TagValuesUnionTypeDef",
    "TargetInstanceTypeDef",
    "TerminateRecommendationDetailTypeDef",
    "TotalImpactFilterTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAnomalyMonitorRequestRequestTypeDef",
    "UpdateAnomalyMonitorResponseTypeDef",
    "UpdateAnomalySubscriptionRequestRequestTypeDef",
    "UpdateAnomalySubscriptionResponseTypeDef",
    "UpdateCostAllocationTagsStatusErrorTypeDef",
    "UpdateCostAllocationTagsStatusRequestRequestTypeDef",
    "UpdateCostAllocationTagsStatusResponseTypeDef",
    "UpdateCostCategoryDefinitionRequestRequestTypeDef",
    "UpdateCostCategoryDefinitionResponseTypeDef",
    "UtilizationByTimeTypeDef",
)

class AnomalyDateIntervalTypeDef(TypedDict):
    StartDate: str
    EndDate: NotRequired[str]

class AnomalyScoreTypeDef(TypedDict):
    MaxScore: float
    CurrentScore: float

SubscriberTypeDef = TypedDict(
    "SubscriberTypeDef",
    {
        "Address": NotRequired[str],
        "Type": NotRequired[SubscriberTypeType],
        "Status": NotRequired[SubscriberStatusType],
    },
)

class ImpactTypeDef(TypedDict):
    MaxImpact: float
    TotalImpact: NotRequired[float]
    TotalActualSpend: NotRequired[float]
    TotalExpectedSpend: NotRequired[float]
    TotalImpactPercentage: NotRequired[float]

class CostAllocationTagBackfillRequestTypeDef(TypedDict):
    BackfillFrom: NotRequired[str]
    RequestedAt: NotRequired[str]
    CompletedAt: NotRequired[str]
    BackfillStatus: NotRequired[CostAllocationTagBackfillStatusType]
    LastUpdatedAt: NotRequired[str]

class CostAllocationTagStatusEntryTypeDef(TypedDict):
    TagKey: str
    Status: CostAllocationTagStatusType

CostAllocationTagTypeDef = TypedDict(
    "CostAllocationTagTypeDef",
    {
        "TagKey": str,
        "Type": CostAllocationTagTypeType,
        "Status": CostAllocationTagStatusType,
        "LastUpdatedDate": NotRequired[str],
        "LastUsedDate": NotRequired[str],
    },
)

class CostCategoryInheritedValueDimensionTypeDef(TypedDict):
    DimensionName: NotRequired[CostCategoryInheritedValueDimensionNameType]
    DimensionKey: NotRequired[str]

class CostCategoryProcessingStatusTypeDef(TypedDict):
    Component: NotRequired[Literal["COST_EXPLORER"]]
    Status: NotRequired[CostCategoryStatusType]

CostCategorySplitChargeRuleParameterOutputTypeDef = TypedDict(
    "CostCategorySplitChargeRuleParameterOutputTypeDef",
    {
        "Type": Literal["ALLOCATION_PERCENTAGES"],
        "Values": List[str],
    },
)
CostCategorySplitChargeRuleParameterTypeDef = TypedDict(
    "CostCategorySplitChargeRuleParameterTypeDef",
    {
        "Type": Literal["ALLOCATION_PERCENTAGES"],
        "Values": Sequence[str],
    },
)

class CostCategoryValuesOutputTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[List[str]]
    MatchOptions: NotRequired[List[MatchOptionType]]

class CostCategoryValuesTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[Sequence[str]]
    MatchOptions: NotRequired[Sequence[MatchOptionType]]

class DateIntervalTypeDef(TypedDict):
    Start: str
    End: str

class CoverageCostTypeDef(TypedDict):
    OnDemandCost: NotRequired[str]

class CoverageHoursTypeDef(TypedDict):
    OnDemandHours: NotRequired[str]
    ReservedHours: NotRequired[str]
    TotalRunningHours: NotRequired[str]
    CoverageHoursPercentage: NotRequired[str]

class CoverageNormalizedUnitsTypeDef(TypedDict):
    OnDemandNormalizedUnits: NotRequired[str]
    ReservedNormalizedUnits: NotRequired[str]
    TotalRunningNormalizedUnits: NotRequired[str]
    CoverageNormalizedUnitsPercentage: NotRequired[str]

class ResourceTagTypeDef(TypedDict):
    Key: str
    Value: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class TagValuesOutputTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[List[str]]
    MatchOptions: NotRequired[List[MatchOptionType]]

class DeleteAnomalyMonitorRequestRequestTypeDef(TypedDict):
    MonitorArn: str

class DeleteAnomalySubscriptionRequestRequestTypeDef(TypedDict):
    SubscriptionArn: str

class DeleteCostCategoryDefinitionRequestRequestTypeDef(TypedDict):
    CostCategoryArn: str

class DescribeCostCategoryDefinitionRequestRequestTypeDef(TypedDict):
    CostCategoryArn: str
    EffectiveOn: NotRequired[str]

class DimensionValuesOutputTypeDef(TypedDict):
    Key: NotRequired[DimensionType]
    Values: NotRequired[List[str]]
    MatchOptions: NotRequired[List[MatchOptionType]]

class DimensionValuesTypeDef(TypedDict):
    Key: NotRequired[DimensionType]
    Values: NotRequired[Sequence[str]]
    MatchOptions: NotRequired[Sequence[MatchOptionType]]

class DimensionValuesWithAttributesTypeDef(TypedDict):
    Value: NotRequired[str]
    Attributes: NotRequired[Dict[str, str]]

class DiskResourceUtilizationTypeDef(TypedDict):
    DiskReadOpsPerSecond: NotRequired[str]
    DiskWriteOpsPerSecond: NotRequired[str]
    DiskReadBytesPerSecond: NotRequired[str]
    DiskWriteBytesPerSecond: NotRequired[str]

class DynamoDBCapacityDetailsTypeDef(TypedDict):
    CapacityUnits: NotRequired[str]
    Region: NotRequired[str]

class EBSResourceUtilizationTypeDef(TypedDict):
    EbsReadOpsPerSecond: NotRequired[str]
    EbsWriteOpsPerSecond: NotRequired[str]
    EbsReadBytesPerSecond: NotRequired[str]
    EbsWriteBytesPerSecond: NotRequired[str]

class EC2InstanceDetailsTypeDef(TypedDict):
    Family: NotRequired[str]
    InstanceType: NotRequired[str]
    Region: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    Platform: NotRequired[str]
    Tenancy: NotRequired[str]
    CurrentGeneration: NotRequired[bool]
    SizeFlexEligible: NotRequired[bool]

class EC2ResourceDetailsTypeDef(TypedDict):
    HourlyOnDemandRate: NotRequired[str]
    InstanceType: NotRequired[str]
    Platform: NotRequired[str]
    Region: NotRequired[str]
    Sku: NotRequired[str]
    Memory: NotRequired[str]
    NetworkPerformance: NotRequired[str]
    Storage: NotRequired[str]
    Vcpu: NotRequired[str]

class NetworkResourceUtilizationTypeDef(TypedDict):
    NetworkInBytesPerSecond: NotRequired[str]
    NetworkOutBytesPerSecond: NotRequired[str]
    NetworkPacketsInPerSecond: NotRequired[str]
    NetworkPacketsOutPerSecond: NotRequired[str]

class EC2SpecificationTypeDef(TypedDict):
    OfferingClass: NotRequired[OfferingClassType]

class ESInstanceDetailsTypeDef(TypedDict):
    InstanceClass: NotRequired[str]
    InstanceSize: NotRequired[str]
    Region: NotRequired[str]
    CurrentGeneration: NotRequired[bool]
    SizeFlexEligible: NotRequired[bool]

class ElastiCacheInstanceDetailsTypeDef(TypedDict):
    Family: NotRequired[str]
    NodeType: NotRequired[str]
    Region: NotRequired[str]
    ProductDescription: NotRequired[str]
    CurrentGeneration: NotRequired[bool]
    SizeFlexEligible: NotRequired[bool]

class GenerationSummaryTypeDef(TypedDict):
    RecommendationId: NotRequired[str]
    GenerationStatus: NotRequired[GenerationStatusType]
    GenerationStartedTime: NotRequired[str]
    GenerationCompletionTime: NotRequired[str]
    EstimatedCompletionTime: NotRequired[str]

class TotalImpactFilterTypeDef(TypedDict):
    NumericOperator: NumericOperatorType
    StartValue: float
    EndValue: NotRequired[float]

class GetAnomalyMonitorsRequestRequestTypeDef(TypedDict):
    MonitorArnList: NotRequired[Sequence[str]]
    NextPageToken: NotRequired[str]
    MaxResults: NotRequired[int]

class GetAnomalySubscriptionsRequestRequestTypeDef(TypedDict):
    SubscriptionArnList: NotRequired[Sequence[str]]
    MonitorArn: NotRequired[str]
    NextPageToken: NotRequired[str]
    MaxResults: NotRequired[int]

class GetApproximateUsageRecordsRequestRequestTypeDef(TypedDict):
    Granularity: GranularityType
    ApproximationDimension: ApproximationDimensionType
    Services: NotRequired[Sequence[str]]

class GetCommitmentPurchaseAnalysisRequestRequestTypeDef(TypedDict):
    AnalysisId: str

GroupDefinitionTypeDef = TypedDict(
    "GroupDefinitionTypeDef",
    {
        "Type": NotRequired[GroupDefinitionTypeType],
        "Key": NotRequired[str],
    },
)

class SortDefinitionTypeDef(TypedDict):
    Key: str
    SortOrder: NotRequired[SortOrderType]

class MetricValueTypeDef(TypedDict):
    Amount: NotRequired[str]
    Unit: NotRequired[str]

class ReservationPurchaseRecommendationMetadataTypeDef(TypedDict):
    RecommendationId: NotRequired[str]
    GenerationTimestamp: NotRequired[str]
    AdditionalMetadata: NotRequired[str]

class ReservationAggregatesTypeDef(TypedDict):
    UtilizationPercentage: NotRequired[str]
    UtilizationPercentageInUnits: NotRequired[str]
    PurchasedHours: NotRequired[str]
    PurchasedUnits: NotRequired[str]
    TotalActualHours: NotRequired[str]
    TotalActualUnits: NotRequired[str]
    UnusedHours: NotRequired[str]
    UnusedUnits: NotRequired[str]
    OnDemandCostOfRIHoursUsed: NotRequired[str]
    NetRISavings: NotRequired[str]
    TotalPotentialRISavings: NotRequired[str]
    AmortizedUpfrontFee: NotRequired[str]
    AmortizedRecurringFee: NotRequired[str]
    TotalAmortizedFee: NotRequired[str]
    RICostForUnusedHours: NotRequired[str]
    RealizedSavings: NotRequired[str]
    UnrealizedSavings: NotRequired[str]

class RightsizingRecommendationConfigurationTypeDef(TypedDict):
    RecommendationTarget: RecommendationTargetType
    BenefitsConsidered: bool

class RightsizingRecommendationMetadataTypeDef(TypedDict):
    RecommendationId: NotRequired[str]
    GenerationTimestamp: NotRequired[str]
    LookbackPeriodInDays: NotRequired[LookbackPeriodInDaysType]
    AdditionalMetadata: NotRequired[str]

class RightsizingRecommendationSummaryTypeDef(TypedDict):
    TotalRecommendationCount: NotRequired[str]
    EstimatedTotalMonthlySavingsAmount: NotRequired[str]
    SavingsCurrencyCode: NotRequired[str]
    SavingsPercentage: NotRequired[str]

class GetSavingsPlanPurchaseRecommendationDetailsRequestRequestTypeDef(TypedDict):
    RecommendationDetailId: str

class SavingsPlansPurchaseRecommendationMetadataTypeDef(TypedDict):
    RecommendationId: NotRequired[str]
    GenerationTimestamp: NotRequired[str]
    AdditionalMetadata: NotRequired[str]

class MemoryDBInstanceDetailsTypeDef(TypedDict):
    Family: NotRequired[str]
    NodeType: NotRequired[str]
    Region: NotRequired[str]
    CurrentGeneration: NotRequired[bool]
    SizeFlexEligible: NotRequired[bool]

class RDSInstanceDetailsTypeDef(TypedDict):
    Family: NotRequired[str]
    InstanceType: NotRequired[str]
    Region: NotRequired[str]
    DatabaseEngine: NotRequired[str]
    DatabaseEdition: NotRequired[str]
    DeploymentOption: NotRequired[str]
    LicenseModel: NotRequired[str]
    CurrentGeneration: NotRequired[bool]
    SizeFlexEligible: NotRequired[bool]

class RedshiftInstanceDetailsTypeDef(TypedDict):
    Family: NotRequired[str]
    NodeType: NotRequired[str]
    Region: NotRequired[str]
    CurrentGeneration: NotRequired[bool]
    SizeFlexEligible: NotRequired[bool]

class ListCommitmentPurchaseAnalysesRequestRequestTypeDef(TypedDict):
    AnalysisStatus: NotRequired[AnalysisStatusType]
    NextPageToken: NotRequired[str]
    PageSize: NotRequired[int]
    AnalysisIds: NotRequired[Sequence[str]]

class ListCostAllocationTagBackfillHistoryRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

ListCostAllocationTagsRequestRequestTypeDef = TypedDict(
    "ListCostAllocationTagsRequestRequestTypeDef",
    {
        "Status": NotRequired[CostAllocationTagStatusType],
        "TagKeys": NotRequired[Sequence[str]],
        "Type": NotRequired[CostAllocationTagTypeType],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

class ListCostCategoryDefinitionsRequestRequestTypeDef(TypedDict):
    EffectiveOn: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListSavingsPlansPurchaseRecommendationGenerationRequestRequestTypeDef(TypedDict):
    GenerationStatus: NotRequired[GenerationStatusType]
    RecommendationIds: NotRequired[Sequence[str]]
    PageSize: NotRequired[int]
    NextPageToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class ProvideAnomalyFeedbackRequestRequestTypeDef(TypedDict):
    AnomalyId: str
    Feedback: AnomalyFeedbackTypeType

class RecommendationDetailHourlyMetricsTypeDef(TypedDict):
    StartTime: NotRequired[str]
    EstimatedOnDemandCost: NotRequired[str]
    CurrentCoverage: NotRequired[str]
    EstimatedCoverage: NotRequired[str]
    EstimatedNewCommitmentUtilization: NotRequired[str]

class ReservationPurchaseRecommendationSummaryTypeDef(TypedDict):
    TotalEstimatedMonthlySavingsAmount: NotRequired[str]
    TotalEstimatedMonthlySavingsPercentage: NotRequired[str]
    CurrencyCode: NotRequired[str]

class TerminateRecommendationDetailTypeDef(TypedDict):
    EstimatedMonthlySavings: NotRequired[str]
    CurrencyCode: NotRequired[str]

class RootCauseImpactTypeDef(TypedDict):
    Contribution: float

class SavingsPlansAmortizedCommitmentTypeDef(TypedDict):
    AmortizedRecurringCommitment: NotRequired[str]
    AmortizedUpfrontCommitment: NotRequired[str]
    TotalAmortizedCommitment: NotRequired[str]

class SavingsPlansCoverageDataTypeDef(TypedDict):
    SpendCoveredBySavingsPlans: NotRequired[str]
    OnDemandCost: NotRequired[str]
    TotalCost: NotRequired[str]
    CoveragePercentage: NotRequired[str]

class SavingsPlansDetailsTypeDef(TypedDict):
    Region: NotRequired[str]
    InstanceFamily: NotRequired[str]
    OfferingId: NotRequired[str]

class SavingsPlansTypeDef(TypedDict):
    PaymentOption: NotRequired[PaymentOptionType]
    SavingsPlansType: NotRequired[SupportedSavingsPlansTypeType]
    Region: NotRequired[str]
    InstanceFamily: NotRequired[str]
    TermInYears: NotRequired[TermInYearsType]
    SavingsPlansCommitment: NotRequired[float]
    OfferingId: NotRequired[str]

class SavingsPlansPurchaseRecommendationSummaryTypeDef(TypedDict):
    EstimatedROI: NotRequired[str]
    CurrencyCode: NotRequired[str]
    EstimatedTotalCost: NotRequired[str]
    CurrentOnDemandSpend: NotRequired[str]
    EstimatedSavingsAmount: NotRequired[str]
    TotalRecommendationCount: NotRequired[str]
    DailyCommitmentToPurchase: NotRequired[str]
    HourlyCommitmentToPurchase: NotRequired[str]
    EstimatedSavingsPercentage: NotRequired[str]
    EstimatedMonthlySavingsAmount: NotRequired[str]
    EstimatedOnDemandCostWithCurrentCommitment: NotRequired[str]

class SavingsPlansSavingsTypeDef(TypedDict):
    NetSavings: NotRequired[str]
    OnDemandCostEquivalent: NotRequired[str]

class SavingsPlansUtilizationTypeDef(TypedDict):
    TotalCommitment: NotRequired[str]
    UsedCommitment: NotRequired[str]
    UnusedCommitment: NotRequired[str]
    UtilizationPercentage: NotRequired[str]

class StartCostAllocationTagBackfillRequestRequestTypeDef(TypedDict):
    BackfillFrom: str

class TagValuesTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[Sequence[str]]
    MatchOptions: NotRequired[Sequence[MatchOptionType]]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    ResourceTagKeys: Sequence[str]

class UpdateAnomalyMonitorRequestRequestTypeDef(TypedDict):
    MonitorArn: str
    MonitorName: NotRequired[str]

class UpdateCostAllocationTagsStatusErrorTypeDef(TypedDict):
    TagKey: NotRequired[str]
    Code: NotRequired[str]
    Message: NotRequired[str]

class UpdateCostAllocationTagsStatusRequestRequestTypeDef(TypedDict):
    CostAllocationTagsStatus: Sequence[CostAllocationTagStatusEntryTypeDef]

class CostCategoryReferenceTypeDef(TypedDict):
    CostCategoryArn: NotRequired[str]
    Name: NotRequired[str]
    EffectiveStart: NotRequired[str]
    EffectiveEnd: NotRequired[str]
    NumberOfRules: NotRequired[int]
    ProcessingStatus: NotRequired[List[CostCategoryProcessingStatusTypeDef]]
    Values: NotRequired[List[str]]
    DefaultValue: NotRequired[str]

class CostCategorySplitChargeRuleOutputTypeDef(TypedDict):
    Source: str
    Targets: List[str]
    Method: CostCategorySplitChargeMethodType
    Parameters: NotRequired[List[CostCategorySplitChargeRuleParameterOutputTypeDef]]

CostCategorySplitChargeRuleParameterUnionTypeDef = Union[
    CostCategorySplitChargeRuleParameterTypeDef, CostCategorySplitChargeRuleParameterOutputTypeDef
]
CostCategoryValuesUnionTypeDef = Union[CostCategoryValuesTypeDef, CostCategoryValuesOutputTypeDef]

class ForecastResultTypeDef(TypedDict):
    TimePeriod: NotRequired[DateIntervalTypeDef]
    MeanValue: NotRequired[str]
    PredictionIntervalLowerBound: NotRequired[str]
    PredictionIntervalUpperBound: NotRequired[str]

class CoverageTypeDef(TypedDict):
    CoverageHours: NotRequired[CoverageHoursTypeDef]
    CoverageNormalizedUnits: NotRequired[CoverageNormalizedUnitsTypeDef]
    CoverageCost: NotRequired[CoverageCostTypeDef]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    ResourceTags: Sequence[ResourceTagTypeDef]

class CreateAnomalyMonitorResponseTypeDef(TypedDict):
    MonitorArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAnomalySubscriptionResponseTypeDef(TypedDict):
    SubscriptionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCostCategoryDefinitionResponseTypeDef(TypedDict):
    CostCategoryArn: str
    EffectiveStart: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteCostCategoryDefinitionResponseTypeDef(TypedDict):
    CostCategoryArn: str
    EffectiveEnd: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetApproximateUsageRecordsResponseTypeDef(TypedDict):
    Services: Dict[str, int]
    TotalRecords: int
    LookbackPeriod: DateIntervalTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetCostCategoriesResponseTypeDef(TypedDict):
    NextPageToken: str
    CostCategoryNames: List[str]
    CostCategoryValues: List[str]
    ReturnSize: int
    TotalSize: int
    ResponseMetadata: ResponseMetadataTypeDef

class GetTagsResponseTypeDef(TypedDict):
    NextPageToken: str
    Tags: List[str]
    ReturnSize: int
    TotalSize: int
    ResponseMetadata: ResponseMetadataTypeDef

class ListCostAllocationTagBackfillHistoryResponseTypeDef(TypedDict):
    BackfillRequests: List[CostAllocationTagBackfillRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListCostAllocationTagsResponseTypeDef(TypedDict):
    CostAllocationTags: List[CostAllocationTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    ResourceTags: List[ResourceTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ProvideAnomalyFeedbackResponseTypeDef(TypedDict):
    AnomalyId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartCommitmentPurchaseAnalysisResponseTypeDef(TypedDict):
    AnalysisId: str
    AnalysisStartedTime: str
    EstimatedCompletionTime: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartCostAllocationTagBackfillResponseTypeDef(TypedDict):
    BackfillRequest: CostAllocationTagBackfillRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartSavingsPlansPurchaseRecommendationGenerationResponseTypeDef(TypedDict):
    RecommendationId: str
    GenerationStartedTime: str
    EstimatedCompletionTime: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAnomalyMonitorResponseTypeDef(TypedDict):
    MonitorArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAnomalySubscriptionResponseTypeDef(TypedDict):
    SubscriptionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateCostCategoryDefinitionResponseTypeDef(TypedDict):
    CostCategoryArn: str
    EffectiveStart: str
    ResponseMetadata: ResponseMetadataTypeDef

class ExpressionOutputTypeDef(TypedDict):
    Or: NotRequired[List[Dict[str, Any]]]
    And: NotRequired[List[Dict[str, Any]]]
    Not: NotRequired[Dict[str, Any]]
    Dimensions: NotRequired[DimensionValuesOutputTypeDef]
    Tags: NotRequired[TagValuesOutputTypeDef]
    CostCategories: NotRequired[CostCategoryValuesOutputTypeDef]

DimensionValuesUnionTypeDef = Union[DimensionValuesTypeDef, DimensionValuesOutputTypeDef]

class GetDimensionValuesResponseTypeDef(TypedDict):
    DimensionValues: List[DimensionValuesWithAttributesTypeDef]
    ReturnSize: int
    TotalSize: int
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ReservedCapacityDetailsTypeDef(TypedDict):
    DynamoDBCapacityDetails: NotRequired[DynamoDBCapacityDetailsTypeDef]

class ResourceDetailsTypeDef(TypedDict):
    EC2ResourceDetails: NotRequired[EC2ResourceDetailsTypeDef]

class EC2ResourceUtilizationTypeDef(TypedDict):
    MaxCpuUtilizationPercentage: NotRequired[str]
    MaxMemoryUtilizationPercentage: NotRequired[str]
    MaxStorageUtilizationPercentage: NotRequired[str]
    EBSResourceUtilization: NotRequired[EBSResourceUtilizationTypeDef]
    DiskResourceUtilization: NotRequired[DiskResourceUtilizationTypeDef]
    NetworkResourceUtilization: NotRequired[NetworkResourceUtilizationTypeDef]

class ServiceSpecificationTypeDef(TypedDict):
    EC2Specification: NotRequired[EC2SpecificationTypeDef]

class ListSavingsPlansPurchaseRecommendationGenerationResponseTypeDef(TypedDict):
    GenerationSummaryList: List[GenerationSummaryTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetAnomaliesRequestRequestTypeDef(TypedDict):
    DateInterval: AnomalyDateIntervalTypeDef
    MonitorArn: NotRequired[str]
    Feedback: NotRequired[AnomalyFeedbackTypeType]
    TotalImpact: NotRequired[TotalImpactFilterTypeDef]
    NextPageToken: NotRequired[str]
    MaxResults: NotRequired[int]

class GroupTypeDef(TypedDict):
    Keys: NotRequired[List[str]]
    Metrics: NotRequired[Dict[str, MetricValueTypeDef]]

class ReservationUtilizationGroupTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]
    Attributes: NotRequired[Dict[str, str]]
    Utilization: NotRequired[ReservationAggregatesTypeDef]

class InstanceDetailsTypeDef(TypedDict):
    EC2InstanceDetails: NotRequired[EC2InstanceDetailsTypeDef]
    RDSInstanceDetails: NotRequired[RDSInstanceDetailsTypeDef]
    RedshiftInstanceDetails: NotRequired[RedshiftInstanceDetailsTypeDef]
    ElastiCacheInstanceDetails: NotRequired[ElastiCacheInstanceDetailsTypeDef]
    ESInstanceDetails: NotRequired[ESInstanceDetailsTypeDef]
    MemoryDBInstanceDetails: NotRequired[MemoryDBInstanceDetailsTypeDef]

class RecommendationDetailDataTypeDef(TypedDict):
    AccountScope: NotRequired[AccountScopeType]
    LookbackPeriodInDays: NotRequired[LookbackPeriodInDaysType]
    SavingsPlansType: NotRequired[SupportedSavingsPlansTypeType]
    TermInYears: NotRequired[TermInYearsType]
    PaymentOption: NotRequired[PaymentOptionType]
    AccountId: NotRequired[str]
    CurrencyCode: NotRequired[str]
    InstanceFamily: NotRequired[str]
    Region: NotRequired[str]
    OfferingId: NotRequired[str]
    GenerationTimestamp: NotRequired[str]
    LatestUsageTimestamp: NotRequired[str]
    CurrentAverageHourlyOnDemandSpend: NotRequired[str]
    CurrentMaximumHourlyOnDemandSpend: NotRequired[str]
    CurrentMinimumHourlyOnDemandSpend: NotRequired[str]
    EstimatedAverageUtilization: NotRequired[str]
    EstimatedMonthlySavingsAmount: NotRequired[str]
    EstimatedOnDemandCost: NotRequired[str]
    EstimatedOnDemandCostWithCurrentCommitment: NotRequired[str]
    EstimatedROI: NotRequired[str]
    EstimatedSPCost: NotRequired[str]
    EstimatedSavingsAmount: NotRequired[str]
    EstimatedSavingsPercentage: NotRequired[str]
    ExistingHourlyCommitment: NotRequired[str]
    HourlyCommitmentToPurchase: NotRequired[str]
    UpfrontCost: NotRequired[str]
    CurrentAverageCoverage: NotRequired[str]
    EstimatedAverageCoverage: NotRequired[str]
    MetricsOverLookbackPeriod: NotRequired[List[RecommendationDetailHourlyMetricsTypeDef]]

class SavingsPlansPurchaseAnalysisDetailsTypeDef(TypedDict):
    CurrencyCode: NotRequired[str]
    LookbackPeriodInHours: NotRequired[str]
    CurrentAverageCoverage: NotRequired[str]
    CurrentAverageHourlyOnDemandSpend: NotRequired[str]
    CurrentMaximumHourlyOnDemandSpend: NotRequired[str]
    CurrentMinimumHourlyOnDemandSpend: NotRequired[str]
    CurrentOnDemandSpend: NotRequired[str]
    ExistingHourlyCommitment: NotRequired[str]
    HourlyCommitmentToPurchase: NotRequired[str]
    EstimatedAverageCoverage: NotRequired[str]
    EstimatedAverageUtilization: NotRequired[str]
    EstimatedMonthlySavingsAmount: NotRequired[str]
    EstimatedOnDemandCost: NotRequired[str]
    EstimatedOnDemandCostWithCurrentCommitment: NotRequired[str]
    EstimatedROI: NotRequired[str]
    EstimatedSavingsAmount: NotRequired[str]
    EstimatedSavingsPercentage: NotRequired[str]
    EstimatedCommitmentCost: NotRequired[str]
    LatestUsageTimestamp: NotRequired[str]
    UpfrontCost: NotRequired[str]
    AdditionalMetadata: NotRequired[str]
    MetricsOverLookbackPeriod: NotRequired[List[RecommendationDetailHourlyMetricsTypeDef]]

class RootCauseTypeDef(TypedDict):
    Service: NotRequired[str]
    Region: NotRequired[str]
    LinkedAccount: NotRequired[str]
    LinkedAccountName: NotRequired[str]
    UsageType: NotRequired[str]
    Impact: NotRequired[RootCauseImpactTypeDef]

class SavingsPlansCoverageTypeDef(TypedDict):
    Attributes: NotRequired[Dict[str, str]]
    Coverage: NotRequired[SavingsPlansCoverageDataTypeDef]
    TimePeriod: NotRequired[DateIntervalTypeDef]

class SavingsPlansPurchaseRecommendationDetailTypeDef(TypedDict):
    SavingsPlansDetails: NotRequired[SavingsPlansDetailsTypeDef]
    AccountId: NotRequired[str]
    UpfrontCost: NotRequired[str]
    EstimatedROI: NotRequired[str]
    CurrencyCode: NotRequired[str]
    EstimatedSPCost: NotRequired[str]
    EstimatedOnDemandCost: NotRequired[str]
    EstimatedOnDemandCostWithCurrentCommitment: NotRequired[str]
    EstimatedSavingsAmount: NotRequired[str]
    EstimatedSavingsPercentage: NotRequired[str]
    HourlyCommitmentToPurchase: NotRequired[str]
    EstimatedAverageUtilization: NotRequired[str]
    EstimatedMonthlySavingsAmount: NotRequired[str]
    CurrentMinimumHourlyOnDemandSpend: NotRequired[str]
    CurrentMaximumHourlyOnDemandSpend: NotRequired[str]
    CurrentAverageHourlyOnDemandSpend: NotRequired[str]
    RecommendationDetailId: NotRequired[str]

class SavingsPlansPurchaseAnalysisConfigurationOutputTypeDef(TypedDict):
    AnalysisType: AnalysisTypeType
    SavingsPlansToAdd: List[SavingsPlansTypeDef]
    LookBackTimePeriod: DateIntervalTypeDef
    AccountScope: NotRequired[AccountScopeType]
    AccountId: NotRequired[str]
    SavingsPlansToExclude: NotRequired[List[str]]

class SavingsPlansPurchaseAnalysisConfigurationTypeDef(TypedDict):
    AnalysisType: AnalysisTypeType
    SavingsPlansToAdd: Sequence[SavingsPlansTypeDef]
    LookBackTimePeriod: DateIntervalTypeDef
    AccountScope: NotRequired[AccountScopeType]
    AccountId: NotRequired[str]
    SavingsPlansToExclude: NotRequired[Sequence[str]]

class SavingsPlansUtilizationAggregatesTypeDef(TypedDict):
    Utilization: SavingsPlansUtilizationTypeDef
    Savings: NotRequired[SavingsPlansSavingsTypeDef]
    AmortizedCommitment: NotRequired[SavingsPlansAmortizedCommitmentTypeDef]

class SavingsPlansUtilizationByTimeTypeDef(TypedDict):
    TimePeriod: DateIntervalTypeDef
    Utilization: SavingsPlansUtilizationTypeDef
    Savings: NotRequired[SavingsPlansSavingsTypeDef]
    AmortizedCommitment: NotRequired[SavingsPlansAmortizedCommitmentTypeDef]

class SavingsPlansUtilizationDetailTypeDef(TypedDict):
    SavingsPlanArn: NotRequired[str]
    Attributes: NotRequired[Dict[str, str]]
    Utilization: NotRequired[SavingsPlansUtilizationTypeDef]
    Savings: NotRequired[SavingsPlansSavingsTypeDef]
    AmortizedCommitment: NotRequired[SavingsPlansAmortizedCommitmentTypeDef]

TagValuesUnionTypeDef = Union[TagValuesTypeDef, TagValuesOutputTypeDef]

class UpdateCostAllocationTagsStatusResponseTypeDef(TypedDict):
    Errors: List[UpdateCostAllocationTagsStatusErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListCostCategoryDefinitionsResponseTypeDef(TypedDict):
    CostCategoryReferences: List[CostCategoryReferenceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CostCategorySplitChargeRuleTypeDef(TypedDict):
    Source: str
    Targets: Sequence[str]
    Method: CostCategorySplitChargeMethodType
    Parameters: NotRequired[Sequence[CostCategorySplitChargeRuleParameterUnionTypeDef]]

class GetCostForecastResponseTypeDef(TypedDict):
    Total: MetricValueTypeDef
    ForecastResultsByTime: List[ForecastResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetUsageForecastResponseTypeDef(TypedDict):
    Total: MetricValueTypeDef
    ForecastResultsByTime: List[ForecastResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ReservationCoverageGroupTypeDef(TypedDict):
    Attributes: NotRequired[Dict[str, str]]
    Coverage: NotRequired[CoverageTypeDef]

class AnomalyMonitorOutputTypeDef(TypedDict):
    MonitorName: str
    MonitorType: MonitorTypeType
    MonitorArn: NotRequired[str]
    CreationDate: NotRequired[str]
    LastUpdatedDate: NotRequired[str]
    LastEvaluatedDate: NotRequired[str]
    MonitorDimension: NotRequired[Literal["SERVICE"]]
    MonitorSpecification: NotRequired[ExpressionOutputTypeDef]
    DimensionalValueCount: NotRequired[int]

class AnomalySubscriptionOutputTypeDef(TypedDict):
    MonitorArnList: List[str]
    Subscribers: List[SubscriberTypeDef]
    Frequency: AnomalySubscriptionFrequencyType
    SubscriptionName: str
    SubscriptionArn: NotRequired[str]
    AccountId: NotRequired[str]
    Threshold: NotRequired[float]
    ThresholdExpression: NotRequired[ExpressionOutputTypeDef]

CostCategoryRuleOutputTypeDef = TypedDict(
    "CostCategoryRuleOutputTypeDef",
    {
        "Value": NotRequired[str],
        "Rule": NotRequired[ExpressionOutputTypeDef],
        "InheritedValue": NotRequired[CostCategoryInheritedValueDimensionTypeDef],
        "Type": NotRequired[CostCategoryRuleTypeType],
    },
)

class ResourceUtilizationTypeDef(TypedDict):
    EC2ResourceUtilization: NotRequired[EC2ResourceUtilizationTypeDef]

class ResultByTimeTypeDef(TypedDict):
    TimePeriod: NotRequired[DateIntervalTypeDef]
    Total: NotRequired[Dict[str, MetricValueTypeDef]]
    Groups: NotRequired[List[GroupTypeDef]]
    Estimated: NotRequired[bool]

class UtilizationByTimeTypeDef(TypedDict):
    TimePeriod: NotRequired[DateIntervalTypeDef]
    Groups: NotRequired[List[ReservationUtilizationGroupTypeDef]]
    Total: NotRequired[ReservationAggregatesTypeDef]

class ReservationPurchaseRecommendationDetailTypeDef(TypedDict):
    AccountId: NotRequired[str]
    InstanceDetails: NotRequired[InstanceDetailsTypeDef]
    RecommendedNumberOfInstancesToPurchase: NotRequired[str]
    RecommendedNormalizedUnitsToPurchase: NotRequired[str]
    MinimumNumberOfInstancesUsedPerHour: NotRequired[str]
    MinimumNormalizedUnitsUsedPerHour: NotRequired[str]
    MaximumNumberOfInstancesUsedPerHour: NotRequired[str]
    MaximumNormalizedUnitsUsedPerHour: NotRequired[str]
    AverageNumberOfInstancesUsedPerHour: NotRequired[str]
    AverageNormalizedUnitsUsedPerHour: NotRequired[str]
    AverageUtilization: NotRequired[str]
    EstimatedBreakEvenInMonths: NotRequired[str]
    CurrencyCode: NotRequired[str]
    EstimatedMonthlySavingsAmount: NotRequired[str]
    EstimatedMonthlySavingsPercentage: NotRequired[str]
    EstimatedMonthlyOnDemandCost: NotRequired[str]
    EstimatedReservationCostForLookbackPeriod: NotRequired[str]
    UpfrontCost: NotRequired[str]
    RecurringStandardMonthlyCost: NotRequired[str]
    ReservedCapacityDetails: NotRequired[ReservedCapacityDetailsTypeDef]
    RecommendedNumberOfCapacityUnitsToPurchase: NotRequired[str]
    MinimumNumberOfCapacityUnitsUsedPerHour: NotRequired[str]
    MaximumNumberOfCapacityUnitsUsedPerHour: NotRequired[str]
    AverageNumberOfCapacityUnitsUsedPerHour: NotRequired[str]

class GetSavingsPlanPurchaseRecommendationDetailsResponseTypeDef(TypedDict):
    RecommendationDetailId: str
    RecommendationDetailData: RecommendationDetailDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AnalysisDetailsTypeDef(TypedDict):
    SavingsPlansPurchaseAnalysisDetails: NotRequired[SavingsPlansPurchaseAnalysisDetailsTypeDef]

class AnomalyTypeDef(TypedDict):
    AnomalyId: str
    AnomalyScore: AnomalyScoreTypeDef
    Impact: ImpactTypeDef
    MonitorArn: str
    AnomalyStartDate: NotRequired[str]
    AnomalyEndDate: NotRequired[str]
    DimensionValue: NotRequired[str]
    RootCauses: NotRequired[List[RootCauseTypeDef]]
    Feedback: NotRequired[AnomalyFeedbackTypeType]

class GetSavingsPlansCoverageResponseTypeDef(TypedDict):
    SavingsPlansCoverages: List[SavingsPlansCoverageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class SavingsPlansPurchaseRecommendationTypeDef(TypedDict):
    AccountScope: NotRequired[AccountScopeType]
    SavingsPlansType: NotRequired[SupportedSavingsPlansTypeType]
    TermInYears: NotRequired[TermInYearsType]
    PaymentOption: NotRequired[PaymentOptionType]
    LookbackPeriodInDays: NotRequired[LookbackPeriodInDaysType]
    SavingsPlansPurchaseRecommendationDetails: NotRequired[
        List[SavingsPlansPurchaseRecommendationDetailTypeDef]
    ]
    SavingsPlansPurchaseRecommendationSummary: NotRequired[
        SavingsPlansPurchaseRecommendationSummaryTypeDef
    ]

class CommitmentPurchaseAnalysisConfigurationOutputTypeDef(TypedDict):
    SavingsPlansPurchaseAnalysisConfiguration: NotRequired[
        SavingsPlansPurchaseAnalysisConfigurationOutputTypeDef
    ]

SavingsPlansPurchaseAnalysisConfigurationUnionTypeDef = Union[
    SavingsPlansPurchaseAnalysisConfigurationTypeDef,
    SavingsPlansPurchaseAnalysisConfigurationOutputTypeDef,
]

class GetSavingsPlansUtilizationResponseTypeDef(TypedDict):
    SavingsPlansUtilizationsByTime: List[SavingsPlansUtilizationByTimeTypeDef]
    Total: SavingsPlansUtilizationAggregatesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSavingsPlansUtilizationDetailsResponseTypeDef(TypedDict):
    SavingsPlansUtilizationDetails: List[SavingsPlansUtilizationDetailTypeDef]
    Total: SavingsPlansUtilizationAggregatesTypeDef
    TimePeriod: DateIntervalTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ExpressionTypeDef(TypedDict):
    Or: NotRequired[Sequence[Mapping[str, Any]]]
    And: NotRequired[Sequence[Mapping[str, Any]]]
    Not: NotRequired[Mapping[str, Any]]
    Dimensions: NotRequired[DimensionValuesUnionTypeDef]
    Tags: NotRequired[TagValuesUnionTypeDef]
    CostCategories: NotRequired[CostCategoryValuesUnionTypeDef]

CostCategorySplitChargeRuleUnionTypeDef = Union[
    CostCategorySplitChargeRuleTypeDef, CostCategorySplitChargeRuleOutputTypeDef
]

class CoverageByTimeTypeDef(TypedDict):
    TimePeriod: NotRequired[DateIntervalTypeDef]
    Groups: NotRequired[List[ReservationCoverageGroupTypeDef]]
    Total: NotRequired[CoverageTypeDef]

class GetAnomalyMonitorsResponseTypeDef(TypedDict):
    AnomalyMonitors: List[AnomalyMonitorOutputTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetAnomalySubscriptionsResponseTypeDef(TypedDict):
    AnomalySubscriptions: List[AnomalySubscriptionOutputTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class CostCategoryTypeDef(TypedDict):
    CostCategoryArn: str
    EffectiveStart: str
    Name: str
    RuleVersion: Literal["CostCategoryExpression.v1"]
    Rules: List[CostCategoryRuleOutputTypeDef]
    EffectiveEnd: NotRequired[str]
    SplitChargeRules: NotRequired[List[CostCategorySplitChargeRuleOutputTypeDef]]
    ProcessingStatus: NotRequired[List[CostCategoryProcessingStatusTypeDef]]
    DefaultValue: NotRequired[str]

class CurrentInstanceTypeDef(TypedDict):
    ResourceId: NotRequired[str]
    InstanceName: NotRequired[str]
    Tags: NotRequired[List[TagValuesOutputTypeDef]]
    ResourceDetails: NotRequired[ResourceDetailsTypeDef]
    ResourceUtilization: NotRequired[ResourceUtilizationTypeDef]
    ReservationCoveredHoursInLookbackPeriod: NotRequired[str]
    SavingsPlansCoveredHoursInLookbackPeriod: NotRequired[str]
    OnDemandHoursInLookbackPeriod: NotRequired[str]
    TotalRunningHoursInLookbackPeriod: NotRequired[str]
    MonthlyCost: NotRequired[str]
    CurrencyCode: NotRequired[str]

class TargetInstanceTypeDef(TypedDict):
    EstimatedMonthlyCost: NotRequired[str]
    EstimatedMonthlySavings: NotRequired[str]
    CurrencyCode: NotRequired[str]
    DefaultTargetInstance: NotRequired[bool]
    ResourceDetails: NotRequired[ResourceDetailsTypeDef]
    ExpectedResourceUtilization: NotRequired[ResourceUtilizationTypeDef]
    PlatformDifferences: NotRequired[List[PlatformDifferenceType]]

class GetCostAndUsageResponseTypeDef(TypedDict):
    NextPageToken: str
    GroupDefinitions: List[GroupDefinitionTypeDef]
    ResultsByTime: List[ResultByTimeTypeDef]
    DimensionValueAttributes: List[DimensionValuesWithAttributesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetCostAndUsageWithResourcesResponseTypeDef(TypedDict):
    NextPageToken: str
    GroupDefinitions: List[GroupDefinitionTypeDef]
    ResultsByTime: List[ResultByTimeTypeDef]
    DimensionValueAttributes: List[DimensionValuesWithAttributesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetReservationUtilizationResponseTypeDef(TypedDict):
    UtilizationsByTime: List[UtilizationByTimeTypeDef]
    Total: ReservationAggregatesTypeDef
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ReservationPurchaseRecommendationTypeDef(TypedDict):
    AccountScope: NotRequired[AccountScopeType]
    LookbackPeriodInDays: NotRequired[LookbackPeriodInDaysType]
    TermInYears: NotRequired[TermInYearsType]
    PaymentOption: NotRequired[PaymentOptionType]
    ServiceSpecification: NotRequired[ServiceSpecificationTypeDef]
    RecommendationDetails: NotRequired[List[ReservationPurchaseRecommendationDetailTypeDef]]
    RecommendationSummary: NotRequired[ReservationPurchaseRecommendationSummaryTypeDef]

class GetAnomaliesResponseTypeDef(TypedDict):
    Anomalies: List[AnomalyTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetSavingsPlansPurchaseRecommendationResponseTypeDef(TypedDict):
    Metadata: SavingsPlansPurchaseRecommendationMetadataTypeDef
    SavingsPlansPurchaseRecommendation: SavingsPlansPurchaseRecommendationTypeDef
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class AnalysisSummaryTypeDef(TypedDict):
    EstimatedCompletionTime: NotRequired[str]
    AnalysisCompletionTime: NotRequired[str]
    AnalysisStartedTime: NotRequired[str]
    AnalysisStatus: NotRequired[AnalysisStatusType]
    ErrorCode: NotRequired[ErrorCodeType]
    AnalysisId: NotRequired[str]
    CommitmentPurchaseAnalysisConfiguration: NotRequired[
        CommitmentPurchaseAnalysisConfigurationOutputTypeDef
    ]

class GetCommitmentPurchaseAnalysisResponseTypeDef(TypedDict):
    EstimatedCompletionTime: str
    AnalysisCompletionTime: str
    AnalysisStartedTime: str
    AnalysisId: str
    AnalysisStatus: AnalysisStatusType
    ErrorCode: ErrorCodeType
    AnalysisDetails: AnalysisDetailsTypeDef
    CommitmentPurchaseAnalysisConfiguration: CommitmentPurchaseAnalysisConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CommitmentPurchaseAnalysisConfigurationTypeDef(TypedDict):
    SavingsPlansPurchaseAnalysisConfiguration: NotRequired[
        SavingsPlansPurchaseAnalysisConfigurationUnionTypeDef
    ]

ExpressionUnionTypeDef = Union[ExpressionTypeDef, ExpressionOutputTypeDef]

class GetCostAndUsageRequestRequestTypeDef(TypedDict):
    TimePeriod: DateIntervalTypeDef
    Granularity: GranularityType
    Metrics: Sequence[str]
    Filter: NotRequired[ExpressionTypeDef]
    GroupBy: NotRequired[Sequence[GroupDefinitionTypeDef]]
    NextPageToken: NotRequired[str]

class GetCostAndUsageWithResourcesRequestRequestTypeDef(TypedDict):
    TimePeriod: DateIntervalTypeDef
    Granularity: GranularityType
    Filter: ExpressionTypeDef
    Metrics: NotRequired[Sequence[str]]
    GroupBy: NotRequired[Sequence[GroupDefinitionTypeDef]]
    NextPageToken: NotRequired[str]

class GetCostCategoriesRequestRequestTypeDef(TypedDict):
    TimePeriod: DateIntervalTypeDef
    SearchString: NotRequired[str]
    CostCategoryName: NotRequired[str]
    Filter: NotRequired[ExpressionTypeDef]
    SortBy: NotRequired[Sequence[SortDefinitionTypeDef]]
    MaxResults: NotRequired[int]
    NextPageToken: NotRequired[str]

class GetCostForecastRequestRequestTypeDef(TypedDict):
    TimePeriod: DateIntervalTypeDef
    Metric: MetricType
    Granularity: GranularityType
    Filter: NotRequired[ExpressionTypeDef]
    PredictionIntervalLevel: NotRequired[int]

class GetDimensionValuesRequestRequestTypeDef(TypedDict):
    TimePeriod: DateIntervalTypeDef
    Dimension: DimensionType
    SearchString: NotRequired[str]
    Context: NotRequired[ContextType]
    Filter: NotRequired[ExpressionTypeDef]
    SortBy: NotRequired[Sequence[SortDefinitionTypeDef]]
    MaxResults: NotRequired[int]
    NextPageToken: NotRequired[str]

class GetReservationCoverageRequestRequestTypeDef(TypedDict):
    TimePeriod: DateIntervalTypeDef
    GroupBy: NotRequired[Sequence[GroupDefinitionTypeDef]]
    Granularity: NotRequired[GranularityType]
    Filter: NotRequired[ExpressionTypeDef]
    Metrics: NotRequired[Sequence[str]]
    NextPageToken: NotRequired[str]
    SortBy: NotRequired[SortDefinitionTypeDef]
    MaxResults: NotRequired[int]

class GetReservationPurchaseRecommendationRequestRequestTypeDef(TypedDict):
    Service: str
    AccountId: NotRequired[str]
    Filter: NotRequired[ExpressionTypeDef]
    AccountScope: NotRequired[AccountScopeType]
    LookbackPeriodInDays: NotRequired[LookbackPeriodInDaysType]
    TermInYears: NotRequired[TermInYearsType]
    PaymentOption: NotRequired[PaymentOptionType]
    ServiceSpecification: NotRequired[ServiceSpecificationTypeDef]
    PageSize: NotRequired[int]
    NextPageToken: NotRequired[str]

class GetReservationUtilizationRequestRequestTypeDef(TypedDict):
    TimePeriod: DateIntervalTypeDef
    GroupBy: NotRequired[Sequence[GroupDefinitionTypeDef]]
    Granularity: NotRequired[GranularityType]
    Filter: NotRequired[ExpressionTypeDef]
    SortBy: NotRequired[SortDefinitionTypeDef]
    NextPageToken: NotRequired[str]
    MaxResults: NotRequired[int]

class GetRightsizingRecommendationRequestRequestTypeDef(TypedDict):
    Service: str
    Filter: NotRequired[ExpressionTypeDef]
    Configuration: NotRequired[RightsizingRecommendationConfigurationTypeDef]
    PageSize: NotRequired[int]
    NextPageToken: NotRequired[str]

class GetSavingsPlansCoverageRequestRequestTypeDef(TypedDict):
    TimePeriod: DateIntervalTypeDef
    GroupBy: NotRequired[Sequence[GroupDefinitionTypeDef]]
    Granularity: NotRequired[GranularityType]
    Filter: NotRequired[ExpressionTypeDef]
    Metrics: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortBy: NotRequired[SortDefinitionTypeDef]

class GetSavingsPlansPurchaseRecommendationRequestRequestTypeDef(TypedDict):
    SavingsPlansType: SupportedSavingsPlansTypeType
    TermInYears: TermInYearsType
    PaymentOption: PaymentOptionType
    LookbackPeriodInDays: LookbackPeriodInDaysType
    AccountScope: NotRequired[AccountScopeType]
    NextPageToken: NotRequired[str]
    PageSize: NotRequired[int]
    Filter: NotRequired[ExpressionTypeDef]

class GetSavingsPlansUtilizationDetailsRequestRequestTypeDef(TypedDict):
    TimePeriod: DateIntervalTypeDef
    Filter: NotRequired[ExpressionTypeDef]
    DataType: NotRequired[Sequence[SavingsPlansDataTypeType]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortBy: NotRequired[SortDefinitionTypeDef]

class GetSavingsPlansUtilizationRequestRequestTypeDef(TypedDict):
    TimePeriod: DateIntervalTypeDef
    Granularity: NotRequired[GranularityType]
    Filter: NotRequired[ExpressionTypeDef]
    SortBy: NotRequired[SortDefinitionTypeDef]

class GetTagsRequestRequestTypeDef(TypedDict):
    TimePeriod: DateIntervalTypeDef
    SearchString: NotRequired[str]
    TagKey: NotRequired[str]
    Filter: NotRequired[ExpressionTypeDef]
    SortBy: NotRequired[Sequence[SortDefinitionTypeDef]]
    MaxResults: NotRequired[int]
    NextPageToken: NotRequired[str]

class GetUsageForecastRequestRequestTypeDef(TypedDict):
    TimePeriod: DateIntervalTypeDef
    Metric: MetricType
    Granularity: GranularityType
    Filter: NotRequired[ExpressionTypeDef]
    PredictionIntervalLevel: NotRequired[int]

class UpdateAnomalySubscriptionRequestRequestTypeDef(TypedDict):
    SubscriptionArn: str
    Threshold: NotRequired[float]
    Frequency: NotRequired[AnomalySubscriptionFrequencyType]
    MonitorArnList: NotRequired[Sequence[str]]
    Subscribers: NotRequired[Sequence[SubscriberTypeDef]]
    SubscriptionName: NotRequired[str]
    ThresholdExpression: NotRequired[ExpressionTypeDef]

class GetReservationCoverageResponseTypeDef(TypedDict):
    CoveragesByTime: List[CoverageByTimeTypeDef]
    Total: CoverageTypeDef
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeCostCategoryDefinitionResponseTypeDef(TypedDict):
    CostCategory: CostCategoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ModifyRecommendationDetailTypeDef(TypedDict):
    TargetInstances: NotRequired[List[TargetInstanceTypeDef]]

class GetReservationPurchaseRecommendationResponseTypeDef(TypedDict):
    Metadata: ReservationPurchaseRecommendationMetadataTypeDef
    Recommendations: List[ReservationPurchaseRecommendationTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListCommitmentPurchaseAnalysesResponseTypeDef(TypedDict):
    AnalysisSummaryList: List[AnalysisSummaryTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartCommitmentPurchaseAnalysisRequestRequestTypeDef(TypedDict):
    CommitmentPurchaseAnalysisConfiguration: CommitmentPurchaseAnalysisConfigurationTypeDef

class AnomalyMonitorTypeDef(TypedDict):
    MonitorName: str
    MonitorType: MonitorTypeType
    MonitorArn: NotRequired[str]
    CreationDate: NotRequired[str]
    LastUpdatedDate: NotRequired[str]
    LastEvaluatedDate: NotRequired[str]
    MonitorDimension: NotRequired[Literal["SERVICE"]]
    MonitorSpecification: NotRequired[ExpressionUnionTypeDef]
    DimensionalValueCount: NotRequired[int]

class AnomalySubscriptionTypeDef(TypedDict):
    MonitorArnList: Sequence[str]
    Subscribers: Sequence[SubscriberTypeDef]
    Frequency: AnomalySubscriptionFrequencyType
    SubscriptionName: str
    SubscriptionArn: NotRequired[str]
    AccountId: NotRequired[str]
    Threshold: NotRequired[float]
    ThresholdExpression: NotRequired[ExpressionUnionTypeDef]

CostCategoryRuleTypeDef = TypedDict(
    "CostCategoryRuleTypeDef",
    {
        "Value": NotRequired[str],
        "Rule": NotRequired[ExpressionUnionTypeDef],
        "InheritedValue": NotRequired[CostCategoryInheritedValueDimensionTypeDef],
        "Type": NotRequired[CostCategoryRuleTypeType],
    },
)

class RightsizingRecommendationTypeDef(TypedDict):
    AccountId: NotRequired[str]
    CurrentInstance: NotRequired[CurrentInstanceTypeDef]
    RightsizingType: NotRequired[RightsizingTypeType]
    ModifyRecommendationDetail: NotRequired[ModifyRecommendationDetailTypeDef]
    TerminateRecommendationDetail: NotRequired[TerminateRecommendationDetailTypeDef]
    FindingReasonCodes: NotRequired[List[FindingReasonCodeType]]

class CreateAnomalyMonitorRequestRequestTypeDef(TypedDict):
    AnomalyMonitor: AnomalyMonitorTypeDef
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]

class CreateAnomalySubscriptionRequestRequestTypeDef(TypedDict):
    AnomalySubscription: AnomalySubscriptionTypeDef
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]

CostCategoryRuleUnionTypeDef = Union[CostCategoryRuleTypeDef, CostCategoryRuleOutputTypeDef]

class UpdateCostCategoryDefinitionRequestRequestTypeDef(TypedDict):
    CostCategoryArn: str
    RuleVersion: Literal["CostCategoryExpression.v1"]
    Rules: Sequence[CostCategoryRuleTypeDef]
    EffectiveStart: NotRequired[str]
    DefaultValue: NotRequired[str]
    SplitChargeRules: NotRequired[Sequence[CostCategorySplitChargeRuleTypeDef]]

class GetRightsizingRecommendationResponseTypeDef(TypedDict):
    Metadata: RightsizingRecommendationMetadataTypeDef
    Summary: RightsizingRecommendationSummaryTypeDef
    RightsizingRecommendations: List[RightsizingRecommendationTypeDef]
    NextPageToken: str
    Configuration: RightsizingRecommendationConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCostCategoryDefinitionRequestRequestTypeDef(TypedDict):
    Name: str
    RuleVersion: Literal["CostCategoryExpression.v1"]
    Rules: Sequence[CostCategoryRuleUnionTypeDef]
    EffectiveStart: NotRequired[str]
    DefaultValue: NotRequired[str]
    SplitChargeRules: NotRequired[Sequence[CostCategorySplitChargeRuleUnionTypeDef]]
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]
