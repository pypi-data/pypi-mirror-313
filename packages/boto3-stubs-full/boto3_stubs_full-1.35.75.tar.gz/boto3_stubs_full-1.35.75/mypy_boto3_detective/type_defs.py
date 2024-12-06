"""
Type annotations for detective service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/type_defs/)

Usage::

    ```python
    from mypy_boto3_detective.type_defs import AcceptInvitationRequestRequestTypeDef

    data: AcceptInvitationRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    DatasourcePackageIngestStateType,
    DatasourcePackageType,
    EntityTypeType,
    FieldType,
    IndicatorTypeType,
    InvitationTypeType,
    MemberDisabledReasonType,
    MemberStatusType,
    SeverityType,
    SortOrderType,
    StateType,
    StatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AcceptInvitationRequestRequestTypeDef",
    "AccountTypeDef",
    "AdministratorTypeDef",
    "BatchGetGraphMemberDatasourcesRequestRequestTypeDef",
    "BatchGetGraphMemberDatasourcesResponseTypeDef",
    "BatchGetMembershipDatasourcesRequestRequestTypeDef",
    "BatchGetMembershipDatasourcesResponseTypeDef",
    "CreateGraphRequestRequestTypeDef",
    "CreateGraphResponseTypeDef",
    "CreateMembersRequestRequestTypeDef",
    "CreateMembersResponseTypeDef",
    "DatasourcePackageIngestDetailTypeDef",
    "DatasourcePackageUsageInfoTypeDef",
    "DateFilterTypeDef",
    "DeleteGraphRequestRequestTypeDef",
    "DeleteMembersRequestRequestTypeDef",
    "DeleteMembersResponseTypeDef",
    "DescribeOrganizationConfigurationRequestRequestTypeDef",
    "DescribeOrganizationConfigurationResponseTypeDef",
    "DisassociateMembershipRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnableOrganizationAdminAccountRequestRequestTypeDef",
    "FilterCriteriaTypeDef",
    "FlaggedIpAddressDetailTypeDef",
    "GetInvestigationRequestRequestTypeDef",
    "GetInvestigationResponseTypeDef",
    "GetMembersRequestRequestTypeDef",
    "GetMembersResponseTypeDef",
    "GraphTypeDef",
    "ImpossibleTravelDetailTypeDef",
    "IndicatorDetailTypeDef",
    "IndicatorTypeDef",
    "InvestigationDetailTypeDef",
    "ListDatasourcePackagesRequestRequestTypeDef",
    "ListDatasourcePackagesResponseTypeDef",
    "ListGraphsRequestRequestTypeDef",
    "ListGraphsResponseTypeDef",
    "ListIndicatorsRequestRequestTypeDef",
    "ListIndicatorsResponseTypeDef",
    "ListInvestigationsRequestRequestTypeDef",
    "ListInvestigationsResponseTypeDef",
    "ListInvitationsRequestRequestTypeDef",
    "ListInvitationsResponseTypeDef",
    "ListMembersRequestRequestTypeDef",
    "ListMembersResponseTypeDef",
    "ListOrganizationAdminAccountsRequestRequestTypeDef",
    "ListOrganizationAdminAccountsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MemberDetailTypeDef",
    "MembershipDatasourcesTypeDef",
    "NewAsoDetailTypeDef",
    "NewGeolocationDetailTypeDef",
    "NewUserAgentDetailTypeDef",
    "RejectInvitationRequestRequestTypeDef",
    "RelatedFindingDetailTypeDef",
    "RelatedFindingGroupDetailTypeDef",
    "ResponseMetadataTypeDef",
    "SortCriteriaTypeDef",
    "StartInvestigationRequestRequestTypeDef",
    "StartInvestigationResponseTypeDef",
    "StartMonitoringMemberRequestRequestTypeDef",
    "StringFilterTypeDef",
    "TTPsObservedDetailTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampForCollectionTypeDef",
    "TimestampTypeDef",
    "UnprocessedAccountTypeDef",
    "UnprocessedGraphTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDatasourcePackagesRequestRequestTypeDef",
    "UpdateInvestigationStateRequestRequestTypeDef",
    "UpdateOrganizationConfigurationRequestRequestTypeDef",
)


class AcceptInvitationRequestRequestTypeDef(TypedDict):
    GraphArn: str


class AccountTypeDef(TypedDict):
    AccountId: str
    EmailAddress: str


class AdministratorTypeDef(TypedDict):
    AccountId: NotRequired[str]
    GraphArn: NotRequired[str]
    DelegationTime: NotRequired[datetime]


class BatchGetGraphMemberDatasourcesRequestRequestTypeDef(TypedDict):
    GraphArn: str
    AccountIds: Sequence[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class UnprocessedAccountTypeDef(TypedDict):
    AccountId: NotRequired[str]
    Reason: NotRequired[str]


class BatchGetMembershipDatasourcesRequestRequestTypeDef(TypedDict):
    GraphArns: Sequence[str]


class UnprocessedGraphTypeDef(TypedDict):
    GraphArn: NotRequired[str]
    Reason: NotRequired[str]


class CreateGraphRequestRequestTypeDef(TypedDict):
    Tags: NotRequired[Mapping[str, str]]


class TimestampForCollectionTypeDef(TypedDict):
    Timestamp: NotRequired[datetime]


class DatasourcePackageUsageInfoTypeDef(TypedDict):
    VolumeUsageInBytes: NotRequired[int]
    VolumeUsageUpdateTime: NotRequired[datetime]


TimestampTypeDef = Union[datetime, str]


class DeleteGraphRequestRequestTypeDef(TypedDict):
    GraphArn: str


class DeleteMembersRequestRequestTypeDef(TypedDict):
    GraphArn: str
    AccountIds: Sequence[str]


class DescribeOrganizationConfigurationRequestRequestTypeDef(TypedDict):
    GraphArn: str


class DisassociateMembershipRequestRequestTypeDef(TypedDict):
    GraphArn: str


class EnableOrganizationAdminAccountRequestRequestTypeDef(TypedDict):
    AccountId: str


class StringFilterTypeDef(TypedDict):
    Value: str


class FlaggedIpAddressDetailTypeDef(TypedDict):
    IpAddress: NotRequired[str]
    Reason: NotRequired[Literal["AWS_THREAT_INTELLIGENCE"]]


class GetInvestigationRequestRequestTypeDef(TypedDict):
    GraphArn: str
    InvestigationId: str


class GetMembersRequestRequestTypeDef(TypedDict):
    GraphArn: str
    AccountIds: Sequence[str]


class GraphTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreatedTime: NotRequired[datetime]


class ImpossibleTravelDetailTypeDef(TypedDict):
    StartingIpAddress: NotRequired[str]
    EndingIpAddress: NotRequired[str]
    StartingLocation: NotRequired[str]
    EndingLocation: NotRequired[str]
    HourlyTimeDelta: NotRequired[int]


class NewAsoDetailTypeDef(TypedDict):
    Aso: NotRequired[str]
    IsNewForEntireAccount: NotRequired[bool]


class NewGeolocationDetailTypeDef(TypedDict):
    Location: NotRequired[str]
    IpAddress: NotRequired[str]
    IsNewForEntireAccount: NotRequired[bool]


class NewUserAgentDetailTypeDef(TypedDict):
    UserAgent: NotRequired[str]
    IsNewForEntireAccount: NotRequired[bool]


RelatedFindingDetailTypeDef = TypedDict(
    "RelatedFindingDetailTypeDef",
    {
        "Arn": NotRequired[str],
        "Type": NotRequired[str],
        "IpAddress": NotRequired[str],
    },
)


class RelatedFindingGroupDetailTypeDef(TypedDict):
    Id: NotRequired[str]


class TTPsObservedDetailTypeDef(TypedDict):
    Tactic: NotRequired[str]
    Technique: NotRequired[str]
    Procedure: NotRequired[str]
    IpAddress: NotRequired[str]
    APIName: NotRequired[str]
    APISuccessCount: NotRequired[int]
    APIFailureCount: NotRequired[int]


class InvestigationDetailTypeDef(TypedDict):
    InvestigationId: NotRequired[str]
    Severity: NotRequired[SeverityType]
    Status: NotRequired[StatusType]
    State: NotRequired[StateType]
    CreatedTime: NotRequired[datetime]
    EntityArn: NotRequired[str]
    EntityType: NotRequired[EntityTypeType]


class ListDatasourcePackagesRequestRequestTypeDef(TypedDict):
    GraphArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListGraphsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListIndicatorsRequestRequestTypeDef(TypedDict):
    GraphArn: str
    InvestigationId: str
    IndicatorType: NotRequired[IndicatorTypeType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class SortCriteriaTypeDef(TypedDict):
    Field: NotRequired[FieldType]
    SortOrder: NotRequired[SortOrderType]


class ListInvitationsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListMembersRequestRequestTypeDef(TypedDict):
    GraphArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListOrganizationAdminAccountsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class RejectInvitationRequestRequestTypeDef(TypedDict):
    GraphArn: str


class StartMonitoringMemberRequestRequestTypeDef(TypedDict):
    GraphArn: str
    AccountId: str


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateDatasourcePackagesRequestRequestTypeDef(TypedDict):
    GraphArn: str
    DatasourcePackages: Sequence[DatasourcePackageType]


class UpdateInvestigationStateRequestRequestTypeDef(TypedDict):
    GraphArn: str
    InvestigationId: str
    State: StateType


class UpdateOrganizationConfigurationRequestRequestTypeDef(TypedDict):
    GraphArn: str
    AutoEnable: NotRequired[bool]


class CreateMembersRequestRequestTypeDef(TypedDict):
    GraphArn: str
    Accounts: Sequence[AccountTypeDef]
    Message: NotRequired[str]
    DisableEmailNotification: NotRequired[bool]


class CreateGraphResponseTypeDef(TypedDict):
    GraphArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeOrganizationConfigurationResponseTypeDef(TypedDict):
    AutoEnable: bool
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetInvestigationResponseTypeDef(TypedDict):
    GraphArn: str
    InvestigationId: str
    EntityArn: str
    EntityType: EntityTypeType
    CreatedTime: datetime
    ScopeStartTime: datetime
    ScopeEndTime: datetime
    Status: StatusType
    Severity: SeverityType
    State: StateType
    ResponseMetadata: ResponseMetadataTypeDef


class ListOrganizationAdminAccountsResponseTypeDef(TypedDict):
    Administrators: List[AdministratorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class StartInvestigationResponseTypeDef(TypedDict):
    InvestigationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteMembersResponseTypeDef(TypedDict):
    AccountIds: List[str]
    UnprocessedAccounts: List[UnprocessedAccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DatasourcePackageIngestDetailTypeDef(TypedDict):
    DatasourcePackageIngestState: NotRequired[DatasourcePackageIngestStateType]
    LastIngestStateChange: NotRequired[
        Dict[DatasourcePackageIngestStateType, TimestampForCollectionTypeDef]
    ]


class MembershipDatasourcesTypeDef(TypedDict):
    AccountId: NotRequired[str]
    GraphArn: NotRequired[str]
    DatasourcePackageIngestHistory: NotRequired[
        Dict[
            DatasourcePackageType,
            Dict[DatasourcePackageIngestStateType, TimestampForCollectionTypeDef],
        ]
    ]


class MemberDetailTypeDef(TypedDict):
    AccountId: NotRequired[str]
    EmailAddress: NotRequired[str]
    GraphArn: NotRequired[str]
    MasterId: NotRequired[str]
    AdministratorId: NotRequired[str]
    Status: NotRequired[MemberStatusType]
    DisabledReason: NotRequired[MemberDisabledReasonType]
    InvitedTime: NotRequired[datetime]
    UpdatedTime: NotRequired[datetime]
    VolumeUsageInBytes: NotRequired[int]
    VolumeUsageUpdatedTime: NotRequired[datetime]
    PercentOfGraphUtilization: NotRequired[float]
    PercentOfGraphUtilizationUpdatedTime: NotRequired[datetime]
    InvitationType: NotRequired[InvitationTypeType]
    VolumeUsageByDatasourcePackage: NotRequired[
        Dict[DatasourcePackageType, DatasourcePackageUsageInfoTypeDef]
    ]
    DatasourcePackageIngestStates: NotRequired[
        Dict[DatasourcePackageType, DatasourcePackageIngestStateType]
    ]


class DateFilterTypeDef(TypedDict):
    StartInclusive: TimestampTypeDef
    EndInclusive: TimestampTypeDef


class StartInvestigationRequestRequestTypeDef(TypedDict):
    GraphArn: str
    EntityArn: str
    ScopeStartTime: TimestampTypeDef
    ScopeEndTime: TimestampTypeDef


class ListGraphsResponseTypeDef(TypedDict):
    GraphList: List[GraphTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class IndicatorDetailTypeDef(TypedDict):
    TTPsObservedDetail: NotRequired[TTPsObservedDetailTypeDef]
    ImpossibleTravelDetail: NotRequired[ImpossibleTravelDetailTypeDef]
    FlaggedIpAddressDetail: NotRequired[FlaggedIpAddressDetailTypeDef]
    NewGeolocationDetail: NotRequired[NewGeolocationDetailTypeDef]
    NewAsoDetail: NotRequired[NewAsoDetailTypeDef]
    NewUserAgentDetail: NotRequired[NewUserAgentDetailTypeDef]
    RelatedFindingDetail: NotRequired[RelatedFindingDetailTypeDef]
    RelatedFindingGroupDetail: NotRequired[RelatedFindingGroupDetailTypeDef]


class ListInvestigationsResponseTypeDef(TypedDict):
    InvestigationDetails: List[InvestigationDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDatasourcePackagesResponseTypeDef(TypedDict):
    DatasourcePackages: Dict[DatasourcePackageType, DatasourcePackageIngestDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class BatchGetGraphMemberDatasourcesResponseTypeDef(TypedDict):
    MemberDatasources: List[MembershipDatasourcesTypeDef]
    UnprocessedAccounts: List[UnprocessedAccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetMembershipDatasourcesResponseTypeDef(TypedDict):
    MembershipDatasources: List[MembershipDatasourcesTypeDef]
    UnprocessedGraphs: List[UnprocessedGraphTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMembersResponseTypeDef(TypedDict):
    Members: List[MemberDetailTypeDef]
    UnprocessedAccounts: List[UnprocessedAccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetMembersResponseTypeDef(TypedDict):
    MemberDetails: List[MemberDetailTypeDef]
    UnprocessedAccounts: List[UnprocessedAccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListInvitationsResponseTypeDef(TypedDict):
    Invitations: List[MemberDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListMembersResponseTypeDef(TypedDict):
    MemberDetails: List[MemberDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class FilterCriteriaTypeDef(TypedDict):
    Severity: NotRequired[StringFilterTypeDef]
    Status: NotRequired[StringFilterTypeDef]
    State: NotRequired[StringFilterTypeDef]
    EntityArn: NotRequired[StringFilterTypeDef]
    CreatedTime: NotRequired[DateFilterTypeDef]


class IndicatorTypeDef(TypedDict):
    IndicatorType: NotRequired[IndicatorTypeType]
    IndicatorDetail: NotRequired[IndicatorDetailTypeDef]


class ListInvestigationsRequestRequestTypeDef(TypedDict):
    GraphArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    FilterCriteria: NotRequired[FilterCriteriaTypeDef]
    SortCriteria: NotRequired[SortCriteriaTypeDef]


class ListIndicatorsResponseTypeDef(TypedDict):
    GraphArn: str
    InvestigationId: str
    Indicators: List[IndicatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
