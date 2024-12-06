"""
Type annotations for budgets service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_budgets/type_defs/)

Usage::

    ```python
    from mypy_boto3_budgets.type_defs import ActionThresholdTypeDef

    data: ActionThresholdTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ActionStatusType,
    ActionSubTypeType,
    ActionTypeType,
    ApprovalModelType,
    AutoAdjustTypeType,
    BudgetTypeType,
    ComparisonOperatorType,
    EventTypeType,
    ExecutionTypeType,
    NotificationStateType,
    NotificationTypeType,
    SubscriptionTypeType,
    ThresholdTypeType,
    TimeUnitType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ActionHistoryDetailsTypeDef",
    "ActionHistoryTypeDef",
    "ActionThresholdTypeDef",
    "ActionTypeDef",
    "AutoAdjustDataOutputTypeDef",
    "AutoAdjustDataTypeDef",
    "AutoAdjustDataUnionTypeDef",
    "BudgetNotificationsForAccountTypeDef",
    "BudgetOutputTypeDef",
    "BudgetPerformanceHistoryTypeDef",
    "BudgetTypeDef",
    "BudgetedAndActualAmountsTypeDef",
    "CalculatedSpendTypeDef",
    "CostTypesTypeDef",
    "CreateBudgetActionRequestRequestTypeDef",
    "CreateBudgetActionResponseTypeDef",
    "CreateBudgetRequestRequestTypeDef",
    "CreateNotificationRequestRequestTypeDef",
    "CreateSubscriberRequestRequestTypeDef",
    "DefinitionOutputTypeDef",
    "DefinitionTypeDef",
    "DeleteBudgetActionRequestRequestTypeDef",
    "DeleteBudgetActionResponseTypeDef",
    "DeleteBudgetRequestRequestTypeDef",
    "DeleteNotificationRequestRequestTypeDef",
    "DeleteSubscriberRequestRequestTypeDef",
    "DescribeBudgetActionHistoriesRequestDescribeBudgetActionHistoriesPaginateTypeDef",
    "DescribeBudgetActionHistoriesRequestRequestTypeDef",
    "DescribeBudgetActionHistoriesResponseTypeDef",
    "DescribeBudgetActionRequestRequestTypeDef",
    "DescribeBudgetActionResponseTypeDef",
    "DescribeBudgetActionsForAccountRequestDescribeBudgetActionsForAccountPaginateTypeDef",
    "DescribeBudgetActionsForAccountRequestRequestTypeDef",
    "DescribeBudgetActionsForAccountResponseTypeDef",
    "DescribeBudgetActionsForBudgetRequestDescribeBudgetActionsForBudgetPaginateTypeDef",
    "DescribeBudgetActionsForBudgetRequestRequestTypeDef",
    "DescribeBudgetActionsForBudgetResponseTypeDef",
    "DescribeBudgetNotificationsForAccountRequestDescribeBudgetNotificationsForAccountPaginateTypeDef",
    "DescribeBudgetNotificationsForAccountRequestRequestTypeDef",
    "DescribeBudgetNotificationsForAccountResponseTypeDef",
    "DescribeBudgetPerformanceHistoryRequestDescribeBudgetPerformanceHistoryPaginateTypeDef",
    "DescribeBudgetPerformanceHistoryRequestRequestTypeDef",
    "DescribeBudgetPerformanceHistoryResponseTypeDef",
    "DescribeBudgetRequestRequestTypeDef",
    "DescribeBudgetResponseTypeDef",
    "DescribeBudgetsRequestDescribeBudgetsPaginateTypeDef",
    "DescribeBudgetsRequestRequestTypeDef",
    "DescribeBudgetsResponseTypeDef",
    "DescribeNotificationsForBudgetRequestDescribeNotificationsForBudgetPaginateTypeDef",
    "DescribeNotificationsForBudgetRequestRequestTypeDef",
    "DescribeNotificationsForBudgetResponseTypeDef",
    "DescribeSubscribersForNotificationRequestDescribeSubscribersForNotificationPaginateTypeDef",
    "DescribeSubscribersForNotificationRequestRequestTypeDef",
    "DescribeSubscribersForNotificationResponseTypeDef",
    "ExecuteBudgetActionRequestRequestTypeDef",
    "ExecuteBudgetActionResponseTypeDef",
    "HistoricalOptionsTypeDef",
    "IamActionDefinitionOutputTypeDef",
    "IamActionDefinitionTypeDef",
    "IamActionDefinitionUnionTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NotificationTypeDef",
    "NotificationWithSubscribersTypeDef",
    "PaginatorConfigTypeDef",
    "ResourceTagTypeDef",
    "ResponseMetadataTypeDef",
    "ScpActionDefinitionOutputTypeDef",
    "ScpActionDefinitionTypeDef",
    "ScpActionDefinitionUnionTypeDef",
    "SpendTypeDef",
    "SsmActionDefinitionOutputTypeDef",
    "SsmActionDefinitionTypeDef",
    "SsmActionDefinitionUnionTypeDef",
    "SubscriberTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimePeriodOutputTypeDef",
    "TimePeriodTypeDef",
    "TimePeriodUnionTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBudgetActionRequestRequestTypeDef",
    "UpdateBudgetActionResponseTypeDef",
    "UpdateBudgetRequestRequestTypeDef",
    "UpdateNotificationRequestRequestTypeDef",
    "UpdateSubscriberRequestRequestTypeDef",
)

class ActionThresholdTypeDef(TypedDict):
    ActionThresholdValue: float
    ActionThresholdType: ThresholdTypeType

class SubscriberTypeDef(TypedDict):
    SubscriptionType: SubscriptionTypeType
    Address: str

class HistoricalOptionsTypeDef(TypedDict):
    BudgetAdjustmentPeriod: int
    LookBackAvailablePeriods: NotRequired[int]

TimestampTypeDef = Union[datetime, str]

class NotificationTypeDef(TypedDict):
    NotificationType: NotificationTypeType
    ComparisonOperator: ComparisonOperatorType
    Threshold: float
    ThresholdType: NotRequired[ThresholdTypeType]
    NotificationState: NotRequired[NotificationStateType]

class CostTypesTypeDef(TypedDict):
    IncludeTax: NotRequired[bool]
    IncludeSubscription: NotRequired[bool]
    UseBlended: NotRequired[bool]
    IncludeRefund: NotRequired[bool]
    IncludeCredit: NotRequired[bool]
    IncludeUpfront: NotRequired[bool]
    IncludeRecurring: NotRequired[bool]
    IncludeOtherSubscription: NotRequired[bool]
    IncludeSupport: NotRequired[bool]
    IncludeDiscount: NotRequired[bool]
    UseAmortized: NotRequired[bool]

class SpendTypeDef(TypedDict):
    Amount: str
    Unit: str

class TimePeriodOutputTypeDef(TypedDict):
    Start: NotRequired[datetime]
    End: NotRequired[datetime]

class ResourceTagTypeDef(TypedDict):
    Key: str
    Value: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class IamActionDefinitionOutputTypeDef(TypedDict):
    PolicyArn: str
    Roles: NotRequired[List[str]]
    Groups: NotRequired[List[str]]
    Users: NotRequired[List[str]]

class ScpActionDefinitionOutputTypeDef(TypedDict):
    PolicyId: str
    TargetIds: List[str]

class SsmActionDefinitionOutputTypeDef(TypedDict):
    ActionSubType: ActionSubTypeType
    Region: str
    InstanceIds: List[str]

class DeleteBudgetActionRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    ActionId: str

class DeleteBudgetRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeBudgetActionRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    ActionId: str

class DescribeBudgetActionsForAccountRequestRequestTypeDef(TypedDict):
    AccountId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeBudgetActionsForBudgetRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeBudgetNotificationsForAccountRequestRequestTypeDef(TypedDict):
    AccountId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeBudgetRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str

class DescribeBudgetsRequestRequestTypeDef(TypedDict):
    AccountId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeNotificationsForBudgetRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ExecuteBudgetActionRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    ActionId: str
    ExecutionType: ExecutionTypeType

class IamActionDefinitionTypeDef(TypedDict):
    PolicyArn: str
    Roles: NotRequired[Sequence[str]]
    Groups: NotRequired[Sequence[str]]
    Users: NotRequired[Sequence[str]]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str

class ScpActionDefinitionTypeDef(TypedDict):
    PolicyId: str
    TargetIds: Sequence[str]

class SsmActionDefinitionTypeDef(TypedDict):
    ActionSubType: ActionSubTypeType
    Region: str
    InstanceIds: Sequence[str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    ResourceTagKeys: Sequence[str]

class AutoAdjustDataOutputTypeDef(TypedDict):
    AutoAdjustType: AutoAdjustTypeType
    HistoricalOptions: NotRequired[HistoricalOptionsTypeDef]
    LastAutoAdjustTime: NotRequired[datetime]

class AutoAdjustDataTypeDef(TypedDict):
    AutoAdjustType: AutoAdjustTypeType
    HistoricalOptions: NotRequired[HistoricalOptionsTypeDef]
    LastAutoAdjustTime: NotRequired[TimestampTypeDef]

class TimePeriodTypeDef(TypedDict):
    Start: NotRequired[TimestampTypeDef]
    End: NotRequired[TimestampTypeDef]

class BudgetNotificationsForAccountTypeDef(TypedDict):
    Notifications: NotRequired[List[NotificationTypeDef]]
    BudgetName: NotRequired[str]

class CreateNotificationRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Notification: NotificationTypeDef
    Subscribers: Sequence[SubscriberTypeDef]

class CreateSubscriberRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Notification: NotificationTypeDef
    Subscriber: SubscriberTypeDef

class DeleteNotificationRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Notification: NotificationTypeDef

class DeleteSubscriberRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Notification: NotificationTypeDef
    Subscriber: SubscriberTypeDef

class DescribeSubscribersForNotificationRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Notification: NotificationTypeDef
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class NotificationWithSubscribersTypeDef(TypedDict):
    Notification: NotificationTypeDef
    Subscribers: Sequence[SubscriberTypeDef]

class UpdateNotificationRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    OldNotification: NotificationTypeDef
    NewNotification: NotificationTypeDef

class UpdateSubscriberRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Notification: NotificationTypeDef
    OldSubscriber: SubscriberTypeDef
    NewSubscriber: SubscriberTypeDef

class CalculatedSpendTypeDef(TypedDict):
    ActualSpend: SpendTypeDef
    ForecastedSpend: NotRequired[SpendTypeDef]

class BudgetedAndActualAmountsTypeDef(TypedDict):
    BudgetedAmount: NotRequired[SpendTypeDef]
    ActualAmount: NotRequired[SpendTypeDef]
    TimePeriod: NotRequired[TimePeriodOutputTypeDef]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    ResourceTags: Sequence[ResourceTagTypeDef]

class CreateBudgetActionResponseTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    ActionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeNotificationsForBudgetResponseTypeDef(TypedDict):
    Notifications: List[NotificationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeSubscribersForNotificationResponseTypeDef(TypedDict):
    Subscribers: List[SubscriberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ExecuteBudgetActionResponseTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    ActionId: str
    ExecutionType: ExecutionTypeType
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    ResourceTags: List[ResourceTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DefinitionOutputTypeDef(TypedDict):
    IamActionDefinition: NotRequired[IamActionDefinitionOutputTypeDef]
    ScpActionDefinition: NotRequired[ScpActionDefinitionOutputTypeDef]
    SsmActionDefinition: NotRequired[SsmActionDefinitionOutputTypeDef]

class DescribeBudgetActionsForAccountRequestDescribeBudgetActionsForAccountPaginateTypeDef(
    TypedDict
):
    AccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeBudgetActionsForBudgetRequestDescribeBudgetActionsForBudgetPaginateTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeBudgetNotificationsForAccountRequestDescribeBudgetNotificationsForAccountPaginateTypeDef(
    TypedDict
):
    AccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeBudgetsRequestDescribeBudgetsPaginateTypeDef(TypedDict):
    AccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeNotificationsForBudgetRequestDescribeNotificationsForBudgetPaginateTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeSubscribersForNotificationRequestDescribeSubscribersForNotificationPaginateTypeDef(
    TypedDict
):
    AccountId: str
    BudgetName: str
    Notification: NotificationTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

IamActionDefinitionUnionTypeDef = Union[
    IamActionDefinitionTypeDef, IamActionDefinitionOutputTypeDef
]
ScpActionDefinitionUnionTypeDef = Union[
    ScpActionDefinitionTypeDef, ScpActionDefinitionOutputTypeDef
]
SsmActionDefinitionUnionTypeDef = Union[
    SsmActionDefinitionTypeDef, SsmActionDefinitionOutputTypeDef
]
AutoAdjustDataUnionTypeDef = Union[AutoAdjustDataTypeDef, AutoAdjustDataOutputTypeDef]

class DescribeBudgetActionHistoriesRequestDescribeBudgetActionHistoriesPaginateTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    ActionId: str
    TimePeriod: NotRequired[TimePeriodTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeBudgetActionHistoriesRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    ActionId: str
    TimePeriod: NotRequired[TimePeriodTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeBudgetPerformanceHistoryRequestDescribeBudgetPerformanceHistoryPaginateTypeDef(
    TypedDict
):
    AccountId: str
    BudgetName: str
    TimePeriod: NotRequired[TimePeriodTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeBudgetPerformanceHistoryRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    TimePeriod: NotRequired[TimePeriodTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

TimePeriodUnionTypeDef = Union[TimePeriodTypeDef, TimePeriodOutputTypeDef]

class DescribeBudgetNotificationsForAccountResponseTypeDef(TypedDict):
    BudgetNotificationsForAccount: List[BudgetNotificationsForAccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class BudgetOutputTypeDef(TypedDict):
    BudgetName: str
    TimeUnit: TimeUnitType
    BudgetType: BudgetTypeType
    BudgetLimit: NotRequired[SpendTypeDef]
    PlannedBudgetLimits: NotRequired[Dict[str, SpendTypeDef]]
    CostFilters: NotRequired[Dict[str, List[str]]]
    CostTypes: NotRequired[CostTypesTypeDef]
    TimePeriod: NotRequired[TimePeriodOutputTypeDef]
    CalculatedSpend: NotRequired[CalculatedSpendTypeDef]
    LastUpdatedTime: NotRequired[datetime]
    AutoAdjustData: NotRequired[AutoAdjustDataOutputTypeDef]

class BudgetPerformanceHistoryTypeDef(TypedDict):
    BudgetName: NotRequired[str]
    BudgetType: NotRequired[BudgetTypeType]
    CostFilters: NotRequired[Dict[str, List[str]]]
    CostTypes: NotRequired[CostTypesTypeDef]
    TimeUnit: NotRequired[TimeUnitType]
    BudgetedAndActualAmountsList: NotRequired[List[BudgetedAndActualAmountsTypeDef]]

class ActionTypeDef(TypedDict):
    ActionId: str
    BudgetName: str
    NotificationType: NotificationTypeType
    ActionType: ActionTypeType
    ActionThreshold: ActionThresholdTypeDef
    Definition: DefinitionOutputTypeDef
    ExecutionRoleArn: str
    ApprovalModel: ApprovalModelType
    Status: ActionStatusType
    Subscribers: List[SubscriberTypeDef]

class DefinitionTypeDef(TypedDict):
    IamActionDefinition: NotRequired[IamActionDefinitionUnionTypeDef]
    ScpActionDefinition: NotRequired[ScpActionDefinitionUnionTypeDef]
    SsmActionDefinition: NotRequired[SsmActionDefinitionUnionTypeDef]

class BudgetTypeDef(TypedDict):
    BudgetName: str
    TimeUnit: TimeUnitType
    BudgetType: BudgetTypeType
    BudgetLimit: NotRequired[SpendTypeDef]
    PlannedBudgetLimits: NotRequired[Mapping[str, SpendTypeDef]]
    CostFilters: NotRequired[Mapping[str, Sequence[str]]]
    CostTypes: NotRequired[CostTypesTypeDef]
    TimePeriod: NotRequired[TimePeriodUnionTypeDef]
    CalculatedSpend: NotRequired[CalculatedSpendTypeDef]
    LastUpdatedTime: NotRequired[TimestampTypeDef]
    AutoAdjustData: NotRequired[AutoAdjustDataUnionTypeDef]

class DescribeBudgetResponseTypeDef(TypedDict):
    Budget: BudgetOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeBudgetsResponseTypeDef(TypedDict):
    Budgets: List[BudgetOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeBudgetPerformanceHistoryResponseTypeDef(TypedDict):
    BudgetPerformanceHistory: BudgetPerformanceHistoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ActionHistoryDetailsTypeDef(TypedDict):
    Message: str
    Action: ActionTypeDef

class DeleteBudgetActionResponseTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Action: ActionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeBudgetActionResponseTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Action: ActionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeBudgetActionsForAccountResponseTypeDef(TypedDict):
    Actions: List[ActionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeBudgetActionsForBudgetResponseTypeDef(TypedDict):
    Actions: List[ActionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateBudgetActionResponseTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    OldAction: ActionTypeDef
    NewAction: ActionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBudgetActionRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    NotificationType: NotificationTypeType
    ActionType: ActionTypeType
    ActionThreshold: ActionThresholdTypeDef
    Definition: DefinitionTypeDef
    ExecutionRoleArn: str
    ApprovalModel: ApprovalModelType
    Subscribers: Sequence[SubscriberTypeDef]
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]

class UpdateBudgetActionRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    ActionId: str
    NotificationType: NotRequired[NotificationTypeType]
    ActionThreshold: NotRequired[ActionThresholdTypeDef]
    Definition: NotRequired[DefinitionTypeDef]
    ExecutionRoleArn: NotRequired[str]
    ApprovalModel: NotRequired[ApprovalModelType]
    Subscribers: NotRequired[Sequence[SubscriberTypeDef]]

class CreateBudgetRequestRequestTypeDef(TypedDict):
    AccountId: str
    Budget: BudgetTypeDef
    NotificationsWithSubscribers: NotRequired[Sequence[NotificationWithSubscribersTypeDef]]
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]

class UpdateBudgetRequestRequestTypeDef(TypedDict):
    AccountId: str
    NewBudget: BudgetTypeDef

class ActionHistoryTypeDef(TypedDict):
    Timestamp: datetime
    Status: ActionStatusType
    EventType: EventTypeType
    ActionHistoryDetails: ActionHistoryDetailsTypeDef

class DescribeBudgetActionHistoriesResponseTypeDef(TypedDict):
    ActionHistories: List[ActionHistoryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
