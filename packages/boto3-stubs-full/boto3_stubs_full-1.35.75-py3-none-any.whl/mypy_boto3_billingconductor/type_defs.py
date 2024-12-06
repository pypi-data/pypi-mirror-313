"""
Type annotations for billingconductor service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billingconductor/type_defs/)

Usage::

    ```python
    from mypy_boto3_billingconductor.type_defs import AccountAssociationsListElementTypeDef

    data: AccountAssociationsListElementTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AssociateResourceErrorReasonType,
    BillingGroupStatusType,
    CurrencyCodeType,
    CustomLineItemRelationshipType,
    CustomLineItemTypeType,
    GroupByAttributeNameType,
    PricingRuleScopeType,
    PricingRuleTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccountAssociationsListElementTypeDef",
    "AccountGroupingTypeDef",
    "AssociateAccountsInputRequestTypeDef",
    "AssociateAccountsOutputTypeDef",
    "AssociatePricingRulesInputRequestTypeDef",
    "AssociatePricingRulesOutputTypeDef",
    "AssociateResourceErrorTypeDef",
    "AssociateResourceResponseElementTypeDef",
    "AttributeTypeDef",
    "BatchAssociateResourcesToCustomLineItemInputRequestTypeDef",
    "BatchAssociateResourcesToCustomLineItemOutputTypeDef",
    "BatchDisassociateResourcesFromCustomLineItemInputRequestTypeDef",
    "BatchDisassociateResourcesFromCustomLineItemOutputTypeDef",
    "BillingGroupCostReportElementTypeDef",
    "BillingGroupCostReportResultElementTypeDef",
    "BillingGroupListElementTypeDef",
    "BillingPeriodRangeTypeDef",
    "ComputationPreferenceTypeDef",
    "CreateBillingGroupInputRequestTypeDef",
    "CreateBillingGroupOutputTypeDef",
    "CreateCustomLineItemInputRequestTypeDef",
    "CreateCustomLineItemOutputTypeDef",
    "CreateFreeTierConfigTypeDef",
    "CreatePricingPlanInputRequestTypeDef",
    "CreatePricingPlanOutputTypeDef",
    "CreatePricingRuleInputRequestTypeDef",
    "CreatePricingRuleOutputTypeDef",
    "CreateTieringInputTypeDef",
    "CustomLineItemBillingPeriodRangeTypeDef",
    "CustomLineItemChargeDetailsTypeDef",
    "CustomLineItemFlatChargeDetailsTypeDef",
    "CustomLineItemListElementTypeDef",
    "CustomLineItemPercentageChargeDetailsTypeDef",
    "CustomLineItemVersionListElementTypeDef",
    "DeleteBillingGroupInputRequestTypeDef",
    "DeleteBillingGroupOutputTypeDef",
    "DeleteCustomLineItemInputRequestTypeDef",
    "DeleteCustomLineItemOutputTypeDef",
    "DeletePricingPlanInputRequestTypeDef",
    "DeletePricingPlanOutputTypeDef",
    "DeletePricingRuleInputRequestTypeDef",
    "DeletePricingRuleOutputTypeDef",
    "DisassociateAccountsInputRequestTypeDef",
    "DisassociateAccountsOutputTypeDef",
    "DisassociatePricingRulesInputRequestTypeDef",
    "DisassociatePricingRulesOutputTypeDef",
    "DisassociateResourceResponseElementTypeDef",
    "FreeTierConfigTypeDef",
    "GetBillingGroupCostReportInputRequestTypeDef",
    "GetBillingGroupCostReportOutputTypeDef",
    "LineItemFilterOutputTypeDef",
    "LineItemFilterTypeDef",
    "LineItemFilterUnionTypeDef",
    "ListAccountAssociationsFilterTypeDef",
    "ListAccountAssociationsInputListAccountAssociationsPaginateTypeDef",
    "ListAccountAssociationsInputRequestTypeDef",
    "ListAccountAssociationsOutputTypeDef",
    "ListBillingGroupAccountGroupingTypeDef",
    "ListBillingGroupCostReportsFilterTypeDef",
    "ListBillingGroupCostReportsInputListBillingGroupCostReportsPaginateTypeDef",
    "ListBillingGroupCostReportsInputRequestTypeDef",
    "ListBillingGroupCostReportsOutputTypeDef",
    "ListBillingGroupsFilterTypeDef",
    "ListBillingGroupsInputListBillingGroupsPaginateTypeDef",
    "ListBillingGroupsInputRequestTypeDef",
    "ListBillingGroupsOutputTypeDef",
    "ListCustomLineItemChargeDetailsTypeDef",
    "ListCustomLineItemFlatChargeDetailsTypeDef",
    "ListCustomLineItemPercentageChargeDetailsTypeDef",
    "ListCustomLineItemVersionsBillingPeriodRangeFilterTypeDef",
    "ListCustomLineItemVersionsFilterTypeDef",
    "ListCustomLineItemVersionsInputListCustomLineItemVersionsPaginateTypeDef",
    "ListCustomLineItemVersionsInputRequestTypeDef",
    "ListCustomLineItemVersionsOutputTypeDef",
    "ListCustomLineItemsFilterTypeDef",
    "ListCustomLineItemsInputListCustomLineItemsPaginateTypeDef",
    "ListCustomLineItemsInputRequestTypeDef",
    "ListCustomLineItemsOutputTypeDef",
    "ListPricingPlansAssociatedWithPricingRuleInputListPricingPlansAssociatedWithPricingRulePaginateTypeDef",
    "ListPricingPlansAssociatedWithPricingRuleInputRequestTypeDef",
    "ListPricingPlansAssociatedWithPricingRuleOutputTypeDef",
    "ListPricingPlansFilterTypeDef",
    "ListPricingPlansInputListPricingPlansPaginateTypeDef",
    "ListPricingPlansInputRequestTypeDef",
    "ListPricingPlansOutputTypeDef",
    "ListPricingRulesAssociatedToPricingPlanInputListPricingRulesAssociatedToPricingPlanPaginateTypeDef",
    "ListPricingRulesAssociatedToPricingPlanInputRequestTypeDef",
    "ListPricingRulesAssociatedToPricingPlanOutputTypeDef",
    "ListPricingRulesFilterTypeDef",
    "ListPricingRulesInputListPricingRulesPaginateTypeDef",
    "ListPricingRulesInputRequestTypeDef",
    "ListPricingRulesOutputTypeDef",
    "ListResourcesAssociatedToCustomLineItemFilterTypeDef",
    "ListResourcesAssociatedToCustomLineItemInputListResourcesAssociatedToCustomLineItemPaginateTypeDef",
    "ListResourcesAssociatedToCustomLineItemInputRequestTypeDef",
    "ListResourcesAssociatedToCustomLineItemOutputTypeDef",
    "ListResourcesAssociatedToCustomLineItemResponseElementTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PricingPlanListElementTypeDef",
    "PricingRuleListElementTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TieringTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBillingGroupAccountGroupingTypeDef",
    "UpdateBillingGroupInputRequestTypeDef",
    "UpdateBillingGroupOutputTypeDef",
    "UpdateCustomLineItemChargeDetailsTypeDef",
    "UpdateCustomLineItemFlatChargeDetailsTypeDef",
    "UpdateCustomLineItemInputRequestTypeDef",
    "UpdateCustomLineItemOutputTypeDef",
    "UpdateCustomLineItemPercentageChargeDetailsTypeDef",
    "UpdateFreeTierConfigTypeDef",
    "UpdatePricingPlanInputRequestTypeDef",
    "UpdatePricingPlanOutputTypeDef",
    "UpdatePricingRuleInputRequestTypeDef",
    "UpdatePricingRuleOutputTypeDef",
    "UpdateTieringInputTypeDef",
)


class AccountAssociationsListElementTypeDef(TypedDict):
    AccountId: NotRequired[str]
    BillingGroupArn: NotRequired[str]
    AccountName: NotRequired[str]
    AccountEmail: NotRequired[str]


class AccountGroupingTypeDef(TypedDict):
    LinkedAccountIds: Sequence[str]
    AutoAssociate: NotRequired[bool]


class AssociateAccountsInputRequestTypeDef(TypedDict):
    Arn: str
    AccountIds: Sequence[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AssociatePricingRulesInputRequestTypeDef(TypedDict):
    Arn: str
    PricingRuleArns: Sequence[str]


class AssociateResourceErrorTypeDef(TypedDict):
    Message: NotRequired[str]
    Reason: NotRequired[AssociateResourceErrorReasonType]


class AttributeTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class CustomLineItemBillingPeriodRangeTypeDef(TypedDict):
    InclusiveStartBillingPeriod: str
    ExclusiveEndBillingPeriod: NotRequired[str]


class BillingGroupCostReportElementTypeDef(TypedDict):
    Arn: NotRequired[str]
    AWSCost: NotRequired[str]
    ProformaCost: NotRequired[str]
    Margin: NotRequired[str]
    MarginPercentage: NotRequired[str]
    Currency: NotRequired[str]


class ComputationPreferenceTypeDef(TypedDict):
    PricingPlanArn: str


class ListBillingGroupAccountGroupingTypeDef(TypedDict):
    AutoAssociate: NotRequired[bool]


class BillingPeriodRangeTypeDef(TypedDict):
    InclusiveStartBillingPeriod: str
    ExclusiveEndBillingPeriod: str


class CreateFreeTierConfigTypeDef(TypedDict):
    Activated: bool


class CreatePricingPlanInputRequestTypeDef(TypedDict):
    Name: str
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    PricingRuleArns: NotRequired[Sequence[str]]
    Tags: NotRequired[Mapping[str, str]]


class CustomLineItemFlatChargeDetailsTypeDef(TypedDict):
    ChargeValue: float


class CustomLineItemPercentageChargeDetailsTypeDef(TypedDict):
    PercentageValue: float
    AssociatedValues: NotRequired[Sequence[str]]


class DeleteBillingGroupInputRequestTypeDef(TypedDict):
    Arn: str


class DeletePricingPlanInputRequestTypeDef(TypedDict):
    Arn: str


class DeletePricingRuleInputRequestTypeDef(TypedDict):
    Arn: str


class DisassociateAccountsInputRequestTypeDef(TypedDict):
    Arn: str
    AccountIds: Sequence[str]


class DisassociatePricingRulesInputRequestTypeDef(TypedDict):
    Arn: str
    PricingRuleArns: Sequence[str]


class FreeTierConfigTypeDef(TypedDict):
    Activated: bool


class LineItemFilterOutputTypeDef(TypedDict):
    Attribute: Literal["LINE_ITEM_TYPE"]
    MatchOption: Literal["NOT_EQUAL"]
    Values: List[Literal["SAVINGS_PLAN_NEGATION"]]


class LineItemFilterTypeDef(TypedDict):
    Attribute: Literal["LINE_ITEM_TYPE"]
    MatchOption: Literal["NOT_EQUAL"]
    Values: Sequence[Literal["SAVINGS_PLAN_NEGATION"]]


class ListAccountAssociationsFilterTypeDef(TypedDict):
    Association: NotRequired[str]
    AccountId: NotRequired[str]
    AccountIds: NotRequired[Sequence[str]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListBillingGroupCostReportsFilterTypeDef(TypedDict):
    BillingGroupArns: NotRequired[Sequence[str]]


class ListBillingGroupsFilterTypeDef(TypedDict):
    Arns: NotRequired[Sequence[str]]
    PricingPlan: NotRequired[str]
    Statuses: NotRequired[Sequence[BillingGroupStatusType]]
    AutoAssociate: NotRequired[bool]


class ListCustomLineItemFlatChargeDetailsTypeDef(TypedDict):
    ChargeValue: float


class ListCustomLineItemPercentageChargeDetailsTypeDef(TypedDict):
    PercentageValue: float


class ListCustomLineItemVersionsBillingPeriodRangeFilterTypeDef(TypedDict):
    StartBillingPeriod: NotRequired[str]
    EndBillingPeriod: NotRequired[str]


class ListCustomLineItemsFilterTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    BillingGroups: NotRequired[Sequence[str]]
    Arns: NotRequired[Sequence[str]]
    AccountIds: NotRequired[Sequence[str]]


class ListPricingPlansAssociatedWithPricingRuleInputRequestTypeDef(TypedDict):
    PricingRuleArn: str
    BillingPeriod: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListPricingPlansFilterTypeDef(TypedDict):
    Arns: NotRequired[Sequence[str]]


class PricingPlanListElementTypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]
    Description: NotRequired[str]
    Size: NotRequired[int]
    CreationTime: NotRequired[int]
    LastModifiedTime: NotRequired[int]


class ListPricingRulesAssociatedToPricingPlanInputRequestTypeDef(TypedDict):
    PricingPlanArn: str
    BillingPeriod: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListPricingRulesFilterTypeDef(TypedDict):
    Arns: NotRequired[Sequence[str]]


class ListResourcesAssociatedToCustomLineItemFilterTypeDef(TypedDict):
    Relationship: NotRequired[CustomLineItemRelationshipType]


class ListResourcesAssociatedToCustomLineItemResponseElementTypeDef(TypedDict):
    Arn: NotRequired[str]
    Relationship: NotRequired[CustomLineItemRelationshipType]
    EndBillingPeriod: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateBillingGroupAccountGroupingTypeDef(TypedDict):
    AutoAssociate: NotRequired[bool]


class UpdateCustomLineItemFlatChargeDetailsTypeDef(TypedDict):
    ChargeValue: float


class UpdateCustomLineItemPercentageChargeDetailsTypeDef(TypedDict):
    PercentageValue: float


class UpdateFreeTierConfigTypeDef(TypedDict):
    Activated: bool


class UpdatePricingPlanInputRequestTypeDef(TypedDict):
    Arn: str
    Name: NotRequired[str]
    Description: NotRequired[str]


class AssociateAccountsOutputTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociatePricingRulesOutputTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBillingGroupOutputTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCustomLineItemOutputTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePricingPlanOutputTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePricingRuleOutputTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteBillingGroupOutputTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteCustomLineItemOutputTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeletePricingPlanOutputTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeletePricingRuleOutputTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateAccountsOutputTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociatePricingRulesOutputTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListAccountAssociationsOutputTypeDef(TypedDict):
    LinkedAccounts: List[AccountAssociationsListElementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPricingPlansAssociatedWithPricingRuleOutputTypeDef(TypedDict):
    BillingPeriod: str
    PricingRuleArn: str
    PricingPlanArns: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPricingRulesAssociatedToPricingPlanOutputTypeDef(TypedDict):
    BillingPeriod: str
    PricingPlanArn: str
    PricingRuleArns: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePricingPlanOutputTypeDef(TypedDict):
    Arn: str
    Name: str
    Description: str
    Size: int
    LastModifiedTime: int
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateResourceResponseElementTypeDef(TypedDict):
    Arn: NotRequired[str]
    Error: NotRequired[AssociateResourceErrorTypeDef]


class DisassociateResourceResponseElementTypeDef(TypedDict):
    Arn: NotRequired[str]
    Error: NotRequired[AssociateResourceErrorTypeDef]


class BillingGroupCostReportResultElementTypeDef(TypedDict):
    Arn: NotRequired[str]
    AWSCost: NotRequired[str]
    ProformaCost: NotRequired[str]
    Margin: NotRequired[str]
    MarginPercentage: NotRequired[str]
    Currency: NotRequired[str]
    Attributes: NotRequired[List[AttributeTypeDef]]


class BatchAssociateResourcesToCustomLineItemInputRequestTypeDef(TypedDict):
    TargetArn: str
    ResourceArns: Sequence[str]
    BillingPeriodRange: NotRequired[CustomLineItemBillingPeriodRangeTypeDef]


class BatchDisassociateResourcesFromCustomLineItemInputRequestTypeDef(TypedDict):
    TargetArn: str
    ResourceArns: Sequence[str]
    BillingPeriodRange: NotRequired[CustomLineItemBillingPeriodRangeTypeDef]


class DeleteCustomLineItemInputRequestTypeDef(TypedDict):
    Arn: str
    BillingPeriodRange: NotRequired[CustomLineItemBillingPeriodRangeTypeDef]


class ListBillingGroupCostReportsOutputTypeDef(TypedDict):
    BillingGroupCostReports: List[BillingGroupCostReportElementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateBillingGroupInputRequestTypeDef(TypedDict):
    Name: str
    AccountGrouping: AccountGroupingTypeDef
    ComputationPreference: ComputationPreferenceTypeDef
    ClientToken: NotRequired[str]
    PrimaryAccountId: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class BillingGroupListElementTypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]
    Description: NotRequired[str]
    PrimaryAccountId: NotRequired[str]
    ComputationPreference: NotRequired[ComputationPreferenceTypeDef]
    Size: NotRequired[int]
    CreationTime: NotRequired[int]
    LastModifiedTime: NotRequired[int]
    Status: NotRequired[BillingGroupStatusType]
    StatusReason: NotRequired[str]
    AccountGrouping: NotRequired[ListBillingGroupAccountGroupingTypeDef]


class GetBillingGroupCostReportInputRequestTypeDef(TypedDict):
    Arn: str
    BillingPeriodRange: NotRequired[BillingPeriodRangeTypeDef]
    GroupBy: NotRequired[Sequence[GroupByAttributeNameType]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class CreateTieringInputTypeDef(TypedDict):
    FreeTier: CreateFreeTierConfigTypeDef


class TieringTypeDef(TypedDict):
    FreeTier: FreeTierConfigTypeDef


LineItemFilterUnionTypeDef = Union[LineItemFilterTypeDef, LineItemFilterOutputTypeDef]


class ListAccountAssociationsInputRequestTypeDef(TypedDict):
    BillingPeriod: NotRequired[str]
    Filters: NotRequired[ListAccountAssociationsFilterTypeDef]
    NextToken: NotRequired[str]


class ListAccountAssociationsInputListAccountAssociationsPaginateTypeDef(TypedDict):
    BillingPeriod: NotRequired[str]
    Filters: NotRequired[ListAccountAssociationsFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPricingPlansAssociatedWithPricingRuleInputListPricingPlansAssociatedWithPricingRulePaginateTypeDef(
    TypedDict
):
    PricingRuleArn: str
    BillingPeriod: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPricingRulesAssociatedToPricingPlanInputListPricingRulesAssociatedToPricingPlanPaginateTypeDef(
    TypedDict
):
    PricingPlanArn: str
    BillingPeriod: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBillingGroupCostReportsInputListBillingGroupCostReportsPaginateTypeDef(TypedDict):
    BillingPeriod: NotRequired[str]
    Filters: NotRequired[ListBillingGroupCostReportsFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBillingGroupCostReportsInputRequestTypeDef(TypedDict):
    BillingPeriod: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[ListBillingGroupCostReportsFilterTypeDef]


class ListBillingGroupsInputListBillingGroupsPaginateTypeDef(TypedDict):
    BillingPeriod: NotRequired[str]
    Filters: NotRequired[ListBillingGroupsFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBillingGroupsInputRequestTypeDef(TypedDict):
    BillingPeriod: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[ListBillingGroupsFilterTypeDef]


ListCustomLineItemChargeDetailsTypeDef = TypedDict(
    "ListCustomLineItemChargeDetailsTypeDef",
    {
        "Type": CustomLineItemTypeType,
        "Flat": NotRequired[ListCustomLineItemFlatChargeDetailsTypeDef],
        "Percentage": NotRequired[ListCustomLineItemPercentageChargeDetailsTypeDef],
        "LineItemFilters": NotRequired[List[LineItemFilterOutputTypeDef]],
    },
)


class ListCustomLineItemVersionsFilterTypeDef(TypedDict):
    BillingPeriodRange: NotRequired[ListCustomLineItemVersionsBillingPeriodRangeFilterTypeDef]


class ListCustomLineItemsInputListCustomLineItemsPaginateTypeDef(TypedDict):
    BillingPeriod: NotRequired[str]
    Filters: NotRequired[ListCustomLineItemsFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCustomLineItemsInputRequestTypeDef(TypedDict):
    BillingPeriod: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[ListCustomLineItemsFilterTypeDef]


class ListPricingPlansInputListPricingPlansPaginateTypeDef(TypedDict):
    BillingPeriod: NotRequired[str]
    Filters: NotRequired[ListPricingPlansFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPricingPlansInputRequestTypeDef(TypedDict):
    BillingPeriod: NotRequired[str]
    Filters: NotRequired[ListPricingPlansFilterTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListPricingPlansOutputTypeDef(TypedDict):
    BillingPeriod: str
    PricingPlans: List[PricingPlanListElementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPricingRulesInputListPricingRulesPaginateTypeDef(TypedDict):
    BillingPeriod: NotRequired[str]
    Filters: NotRequired[ListPricingRulesFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPricingRulesInputRequestTypeDef(TypedDict):
    BillingPeriod: NotRequired[str]
    Filters: NotRequired[ListPricingRulesFilterTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListResourcesAssociatedToCustomLineItemInputListResourcesAssociatedToCustomLineItemPaginateTypeDef(
    TypedDict
):
    Arn: str
    BillingPeriod: NotRequired[str]
    Filters: NotRequired[ListResourcesAssociatedToCustomLineItemFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourcesAssociatedToCustomLineItemInputRequestTypeDef(TypedDict):
    Arn: str
    BillingPeriod: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[ListResourcesAssociatedToCustomLineItemFilterTypeDef]


class ListResourcesAssociatedToCustomLineItemOutputTypeDef(TypedDict):
    Arn: str
    AssociatedResources: List[ListResourcesAssociatedToCustomLineItemResponseElementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateBillingGroupInputRequestTypeDef(TypedDict):
    Arn: str
    Name: NotRequired[str]
    Status: NotRequired[BillingGroupStatusType]
    ComputationPreference: NotRequired[ComputationPreferenceTypeDef]
    Description: NotRequired[str]
    AccountGrouping: NotRequired[UpdateBillingGroupAccountGroupingTypeDef]


class UpdateBillingGroupOutputTypeDef(TypedDict):
    Arn: str
    Name: str
    Description: str
    PrimaryAccountId: str
    PricingPlanArn: str
    Size: int
    LastModifiedTime: int
    Status: BillingGroupStatusType
    StatusReason: str
    AccountGrouping: UpdateBillingGroupAccountGroupingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTieringInputTypeDef(TypedDict):
    FreeTier: UpdateFreeTierConfigTypeDef


class BatchAssociateResourcesToCustomLineItemOutputTypeDef(TypedDict):
    SuccessfullyAssociatedResources: List[AssociateResourceResponseElementTypeDef]
    FailedAssociatedResources: List[AssociateResourceResponseElementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchDisassociateResourcesFromCustomLineItemOutputTypeDef(TypedDict):
    SuccessfullyDisassociatedResources: List[DisassociateResourceResponseElementTypeDef]
    FailedDisassociatedResources: List[DisassociateResourceResponseElementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetBillingGroupCostReportOutputTypeDef(TypedDict):
    BillingGroupCostReportResults: List[BillingGroupCostReportResultElementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListBillingGroupsOutputTypeDef(TypedDict):
    BillingGroups: List[BillingGroupListElementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


CreatePricingRuleInputRequestTypeDef = TypedDict(
    "CreatePricingRuleInputRequestTypeDef",
    {
        "Name": str,
        "Scope": PricingRuleScopeType,
        "Type": PricingRuleTypeType,
        "ClientToken": NotRequired[str],
        "Description": NotRequired[str],
        "ModifierPercentage": NotRequired[float],
        "Service": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
        "BillingEntity": NotRequired[str],
        "Tiering": NotRequired[CreateTieringInputTypeDef],
        "UsageType": NotRequired[str],
        "Operation": NotRequired[str],
    },
)
PricingRuleListElementTypeDef = TypedDict(
    "PricingRuleListElementTypeDef",
    {
        "Name": NotRequired[str],
        "Arn": NotRequired[str],
        "Description": NotRequired[str],
        "Scope": NotRequired[PricingRuleScopeType],
        "Type": NotRequired[PricingRuleTypeType],
        "ModifierPercentage": NotRequired[float],
        "Service": NotRequired[str],
        "AssociatedPricingPlanCount": NotRequired[int],
        "CreationTime": NotRequired[int],
        "LastModifiedTime": NotRequired[int],
        "BillingEntity": NotRequired[str],
        "Tiering": NotRequired[TieringTypeDef],
        "UsageType": NotRequired[str],
        "Operation": NotRequired[str],
    },
)
CustomLineItemChargeDetailsTypeDef = TypedDict(
    "CustomLineItemChargeDetailsTypeDef",
    {
        "Type": CustomLineItemTypeType,
        "Flat": NotRequired[CustomLineItemFlatChargeDetailsTypeDef],
        "Percentage": NotRequired[CustomLineItemPercentageChargeDetailsTypeDef],
        "LineItemFilters": NotRequired[Sequence[LineItemFilterUnionTypeDef]],
    },
)


class UpdateCustomLineItemChargeDetailsTypeDef(TypedDict):
    Flat: NotRequired[UpdateCustomLineItemFlatChargeDetailsTypeDef]
    Percentage: NotRequired[UpdateCustomLineItemPercentageChargeDetailsTypeDef]
    LineItemFilters: NotRequired[Sequence[LineItemFilterUnionTypeDef]]


class CustomLineItemListElementTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]
    ChargeDetails: NotRequired[ListCustomLineItemChargeDetailsTypeDef]
    CurrencyCode: NotRequired[CurrencyCodeType]
    Description: NotRequired[str]
    ProductCode: NotRequired[str]
    BillingGroupArn: NotRequired[str]
    CreationTime: NotRequired[int]
    LastModifiedTime: NotRequired[int]
    AssociationSize: NotRequired[int]
    AccountId: NotRequired[str]


class CustomLineItemVersionListElementTypeDef(TypedDict):
    Name: NotRequired[str]
    ChargeDetails: NotRequired[ListCustomLineItemChargeDetailsTypeDef]
    CurrencyCode: NotRequired[CurrencyCodeType]
    Description: NotRequired[str]
    ProductCode: NotRequired[str]
    BillingGroupArn: NotRequired[str]
    CreationTime: NotRequired[int]
    LastModifiedTime: NotRequired[int]
    AssociationSize: NotRequired[int]
    StartBillingPeriod: NotRequired[str]
    EndBillingPeriod: NotRequired[str]
    Arn: NotRequired[str]
    StartTime: NotRequired[int]
    AccountId: NotRequired[str]


class UpdateCustomLineItemOutputTypeDef(TypedDict):
    Arn: str
    BillingGroupArn: str
    Name: str
    Description: str
    ChargeDetails: ListCustomLineItemChargeDetailsTypeDef
    LastModifiedTime: int
    AssociationSize: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListCustomLineItemVersionsInputListCustomLineItemVersionsPaginateTypeDef(TypedDict):
    Arn: str
    Filters: NotRequired[ListCustomLineItemVersionsFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCustomLineItemVersionsInputRequestTypeDef(TypedDict):
    Arn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[ListCustomLineItemVersionsFilterTypeDef]


UpdatePricingRuleInputRequestTypeDef = TypedDict(
    "UpdatePricingRuleInputRequestTypeDef",
    {
        "Arn": str,
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "Type": NotRequired[PricingRuleTypeType],
        "ModifierPercentage": NotRequired[float],
        "Tiering": NotRequired[UpdateTieringInputTypeDef],
    },
)
UpdatePricingRuleOutputTypeDef = TypedDict(
    "UpdatePricingRuleOutputTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Description": str,
        "Scope": PricingRuleScopeType,
        "Type": PricingRuleTypeType,
        "ModifierPercentage": float,
        "Service": str,
        "AssociatedPricingPlanCount": int,
        "LastModifiedTime": int,
        "BillingEntity": str,
        "Tiering": UpdateTieringInputTypeDef,
        "UsageType": str,
        "Operation": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListPricingRulesOutputTypeDef(TypedDict):
    BillingPeriod: str
    PricingRules: List[PricingRuleListElementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateCustomLineItemInputRequestTypeDef(TypedDict):
    Name: str
    Description: str
    BillingGroupArn: str
    ChargeDetails: CustomLineItemChargeDetailsTypeDef
    ClientToken: NotRequired[str]
    BillingPeriodRange: NotRequired[CustomLineItemBillingPeriodRangeTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    AccountId: NotRequired[str]


class UpdateCustomLineItemInputRequestTypeDef(TypedDict):
    Arn: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    ChargeDetails: NotRequired[UpdateCustomLineItemChargeDetailsTypeDef]
    BillingPeriodRange: NotRequired[CustomLineItemBillingPeriodRangeTypeDef]


class ListCustomLineItemsOutputTypeDef(TypedDict):
    CustomLineItems: List[CustomLineItemListElementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListCustomLineItemVersionsOutputTypeDef(TypedDict):
    CustomLineItemVersions: List[CustomLineItemVersionListElementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
