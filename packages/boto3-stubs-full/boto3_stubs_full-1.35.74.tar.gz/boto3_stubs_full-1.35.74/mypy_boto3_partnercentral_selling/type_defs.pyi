"""
Type annotations for partnercentral-selling service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_selling/type_defs/)

Usage::

    ```python
    from mypy_boto3_partnercentral_selling.type_defs import AccountReceiverTypeDef

    data: AccountReceiverTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AwsClosedLostReasonType,
    AwsFundingUsedType,
    AwsMemberBusinessTitleType,
    AwsOpportunityStageType,
    ChannelType,
    ClosedLostReasonType,
    CompetitorNameType,
    CountryCodeType,
    CurrencyCodeType,
    DeliveryModelType,
    EngagementScoreType,
    ExpectedCustomerSpendCurrencyCodeEnumType,
    IndustryType,
    InvitationStatusType,
    InvolvementTypeChangeReasonType,
    MarketingSourceType,
    NationalSecurityType,
    OpportunityOriginType,
    OpportunitySortNameType,
    OpportunityTypeType,
    PrimaryNeedFromAwsType,
    ReasonCodeType,
    ReceiverResponsibilityType,
    RelatedEntityTypeType,
    RevenueModelType,
    ReviewStatusType,
    SalesActivityType,
    SalesInvolvementTypeType,
    SolutionSortNameType,
    SolutionStatusType,
    SortOrderType,
    StageType,
    TaskStatusType,
    VisibilityType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccountReceiverTypeDef",
    "AccountSummaryTypeDef",
    "AccountTypeDef",
    "AddressSummaryTypeDef",
    "AddressTypeDef",
    "AssignOpportunityRequestRequestTypeDef",
    "AssigneeContactTypeDef",
    "AssociateOpportunityRequestRequestTypeDef",
    "AwsOpportunityCustomerTypeDef",
    "AwsOpportunityInsightsTypeDef",
    "AwsOpportunityLifeCycleTypeDef",
    "AwsOpportunityProjectTypeDef",
    "AwsOpportunityRelatedEntitiesTypeDef",
    "AwsSubmissionTypeDef",
    "AwsTeamMemberTypeDef",
    "ContactTypeDef",
    "CreateOpportunityRequestRequestTypeDef",
    "CreateOpportunityResponseTypeDef",
    "CustomerOutputTypeDef",
    "CustomerSummaryTypeDef",
    "CustomerTypeDef",
    "DisassociateOpportunityRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EngagementCustomerTypeDef",
    "EngagementInvitationSummaryTypeDef",
    "ExpectedCustomerSpendTypeDef",
    "GetAwsOpportunitySummaryRequestRequestTypeDef",
    "GetAwsOpportunitySummaryResponseTypeDef",
    "GetEngagementInvitationRequestRequestTypeDef",
    "GetEngagementInvitationResponseTypeDef",
    "GetOpportunityRequestRequestTypeDef",
    "GetOpportunityResponseTypeDef",
    "LastModifiedDateTypeDef",
    "LifeCycleOutputTypeDef",
    "LifeCycleSummaryTypeDef",
    "LifeCycleTypeDef",
    "ListEngagementInvitationsRequestListEngagementInvitationsPaginateTypeDef",
    "ListEngagementInvitationsRequestRequestTypeDef",
    "ListEngagementInvitationsResponseTypeDef",
    "ListOpportunitiesRequestListOpportunitiesPaginateTypeDef",
    "ListOpportunitiesRequestRequestTypeDef",
    "ListOpportunitiesResponseTypeDef",
    "ListSolutionsRequestListSolutionsPaginateTypeDef",
    "ListSolutionsRequestRequestTypeDef",
    "ListSolutionsResponseTypeDef",
    "MarketingOutputTypeDef",
    "MarketingTypeDef",
    "MonetaryValueTypeDef",
    "NextStepsHistoryOutputTypeDef",
    "NextStepsHistoryTypeDef",
    "NextStepsHistoryUnionTypeDef",
    "OpportunityEngagementInvitationSortTypeDef",
    "OpportunityInvitationPayloadTypeDef",
    "OpportunitySortTypeDef",
    "OpportunitySummaryTypeDef",
    "PaginatorConfigTypeDef",
    "PayloadTypeDef",
    "ProfileNextStepsHistoryTypeDef",
    "ProjectDetailsTypeDef",
    "ProjectOutputTypeDef",
    "ProjectSummaryTypeDef",
    "ProjectTypeDef",
    "ReceiverTypeDef",
    "RejectEngagementInvitationRequestRequestTypeDef",
    "RelatedEntityIdentifiersTypeDef",
    "ResponseMetadataTypeDef",
    "SenderContactTypeDef",
    "SoftwareRevenueTypeDef",
    "SolutionBaseTypeDef",
    "SolutionSortTypeDef",
    "StartEngagementByAcceptingInvitationTaskRequestRequestTypeDef",
    "StartEngagementByAcceptingInvitationTaskResponseTypeDef",
    "StartEngagementFromOpportunityTaskRequestRequestTypeDef",
    "StartEngagementFromOpportunityTaskResponseTypeDef",
    "TimestampTypeDef",
    "UpdateOpportunityRequestRequestTypeDef",
    "UpdateOpportunityResponseTypeDef",
)

class AccountReceiverTypeDef(TypedDict):
    AwsAccountId: str
    Alias: NotRequired[str]

class AddressSummaryTypeDef(TypedDict):
    City: NotRequired[str]
    CountryCode: NotRequired[CountryCodeType]
    PostalCode: NotRequired[str]
    StateOrRegion: NotRequired[str]

class AddressTypeDef(TypedDict):
    City: NotRequired[str]
    CountryCode: NotRequired[CountryCodeType]
    PostalCode: NotRequired[str]
    StateOrRegion: NotRequired[str]
    StreetAddress: NotRequired[str]

class AssigneeContactTypeDef(TypedDict):
    BusinessTitle: str
    Email: str
    FirstName: str
    LastName: str

class AssociateOpportunityRequestRequestTypeDef(TypedDict):
    Catalog: str
    OpportunityIdentifier: str
    RelatedEntityIdentifier: str
    RelatedEntityType: RelatedEntityTypeType

class ContactTypeDef(TypedDict):
    BusinessTitle: NotRequired[str]
    Email: NotRequired[str]
    FirstName: NotRequired[str]
    LastName: NotRequired[str]
    Phone: NotRequired[str]

class AwsOpportunityInsightsTypeDef(TypedDict):
    EngagementScore: NotRequired[EngagementScoreType]
    NextBestActions: NotRequired[str]

class ProfileNextStepsHistoryTypeDef(TypedDict):
    Time: datetime
    Value: str

class ExpectedCustomerSpendTypeDef(TypedDict):
    Amount: str
    CurrencyCode: ExpectedCustomerSpendCurrencyCodeEnumType
    Frequency: Literal["Monthly"]
    TargetCompany: str

class AwsOpportunityRelatedEntitiesTypeDef(TypedDict):
    AwsProducts: NotRequired[List[str]]
    Solutions: NotRequired[List[str]]

class AwsSubmissionTypeDef(TypedDict):
    InvolvementType: SalesInvolvementTypeType
    Visibility: NotRequired[VisibilityType]

class AwsTeamMemberTypeDef(TypedDict):
    BusinessTitle: NotRequired[AwsMemberBusinessTitleType]
    Email: NotRequired[str]
    FirstName: NotRequired[str]
    LastName: NotRequired[str]

class MarketingTypeDef(TypedDict):
    AwsFundingUsed: NotRequired[AwsFundingUsedType]
    CampaignName: NotRequired[str]
    Channels: NotRequired[Sequence[ChannelType]]
    Source: NotRequired[MarketingSourceType]
    UseCases: NotRequired[Sequence[str]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DisassociateOpportunityRequestRequestTypeDef(TypedDict):
    Catalog: str
    OpportunityIdentifier: str
    RelatedEntityIdentifier: str
    RelatedEntityType: RelatedEntityTypeType

class EngagementCustomerTypeDef(TypedDict):
    CompanyName: str
    CountryCode: CountryCodeType
    Industry: IndustryType
    WebsiteUrl: str

class GetAwsOpportunitySummaryRequestRequestTypeDef(TypedDict):
    Catalog: str
    RelatedOpportunityIdentifier: str

class GetEngagementInvitationRequestRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str

class GetOpportunityRequestRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str

class MarketingOutputTypeDef(TypedDict):
    AwsFundingUsed: NotRequired[AwsFundingUsedType]
    CampaignName: NotRequired[str]
    Channels: NotRequired[List[ChannelType]]
    Source: NotRequired[MarketingSourceType]
    UseCases: NotRequired[List[str]]

class RelatedEntityIdentifiersTypeDef(TypedDict):
    AwsMarketplaceOffers: NotRequired[List[str]]
    AwsProducts: NotRequired[List[str]]
    Solutions: NotRequired[List[str]]

TimestampTypeDef = Union[datetime, str]

class NextStepsHistoryOutputTypeDef(TypedDict):
    Time: datetime
    Value: str

class LifeCycleSummaryTypeDef(TypedDict):
    ClosedLostReason: NotRequired[ClosedLostReasonType]
    NextSteps: NotRequired[str]
    ReviewComments: NotRequired[str]
    ReviewStatus: NotRequired[ReviewStatusType]
    ReviewStatusReason: NotRequired[str]
    Stage: NotRequired[StageType]
    TargetCloseDate: NotRequired[str]

class OpportunityEngagementInvitationSortTypeDef(TypedDict):
    SortBy: Literal["InvitationDate"]
    SortOrder: SortOrderType

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class OpportunitySortTypeDef(TypedDict):
    SortBy: OpportunitySortNameType
    SortOrder: SortOrderType

class SolutionSortTypeDef(TypedDict):
    SortBy: SolutionSortNameType
    SortOrder: SortOrderType

class SolutionBaseTypeDef(TypedDict):
    Catalog: str
    Category: str
    CreatedDate: datetime
    Id: str
    Name: str
    Status: SolutionStatusType

class MonetaryValueTypeDef(TypedDict):
    Amount: str
    CurrencyCode: CurrencyCodeType

class SenderContactTypeDef(TypedDict):
    Email: str
    BusinessTitle: NotRequired[str]
    FirstName: NotRequired[str]
    LastName: NotRequired[str]
    Phone: NotRequired[str]

class RejectEngagementInvitationRequestRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str
    RejectionReason: NotRequired[str]

class StartEngagementByAcceptingInvitationTaskRequestRequestTypeDef(TypedDict):
    Catalog: str
    ClientToken: str
    Identifier: str

class ReceiverTypeDef(TypedDict):
    Account: NotRequired[AccountReceiverTypeDef]

class AccountSummaryTypeDef(TypedDict):
    CompanyName: str
    Address: NotRequired[AddressSummaryTypeDef]
    Industry: NotRequired[IndustryType]
    OtherIndustry: NotRequired[str]
    WebsiteUrl: NotRequired[str]

class AccountTypeDef(TypedDict):
    CompanyName: str
    Address: NotRequired[AddressTypeDef]
    AwsAccountId: NotRequired[str]
    Duns: NotRequired[str]
    Industry: NotRequired[IndustryType]
    OtherIndustry: NotRequired[str]
    WebsiteUrl: NotRequired[str]

class AssignOpportunityRequestRequestTypeDef(TypedDict):
    Assignee: AssigneeContactTypeDef
    Catalog: str
    Identifier: str

class AwsOpportunityCustomerTypeDef(TypedDict):
    Contacts: NotRequired[List[ContactTypeDef]]

class AwsOpportunityLifeCycleTypeDef(TypedDict):
    ClosedLostReason: NotRequired[AwsClosedLostReasonType]
    NextSteps: NotRequired[str]
    NextStepsHistory: NotRequired[List[ProfileNextStepsHistoryTypeDef]]
    Stage: NotRequired[AwsOpportunityStageType]
    TargetCloseDate: NotRequired[str]

class AwsOpportunityProjectTypeDef(TypedDict):
    ExpectedCustomerSpend: NotRequired[List[ExpectedCustomerSpendTypeDef]]

class ProjectDetailsTypeDef(TypedDict):
    BusinessProblem: str
    ExpectedCustomerSpend: List[ExpectedCustomerSpendTypeDef]
    TargetCompletionDate: str
    Title: str

class ProjectOutputTypeDef(TypedDict):
    AdditionalComments: NotRequired[str]
    ApnPrograms: NotRequired[List[str]]
    CompetitorName: NotRequired[CompetitorNameType]
    CustomerBusinessProblem: NotRequired[str]
    CustomerUseCase: NotRequired[str]
    DeliveryModels: NotRequired[List[DeliveryModelType]]
    ExpectedCustomerSpend: NotRequired[List[ExpectedCustomerSpendTypeDef]]
    OtherCompetitorNames: NotRequired[str]
    OtherSolutionDescription: NotRequired[str]
    RelatedOpportunityIdentifier: NotRequired[str]
    SalesActivities: NotRequired[List[SalesActivityType]]
    Title: NotRequired[str]

class ProjectSummaryTypeDef(TypedDict):
    DeliveryModels: NotRequired[List[DeliveryModelType]]
    ExpectedCustomerSpend: NotRequired[List[ExpectedCustomerSpendTypeDef]]

class ProjectTypeDef(TypedDict):
    AdditionalComments: NotRequired[str]
    ApnPrograms: NotRequired[Sequence[str]]
    CompetitorName: NotRequired[CompetitorNameType]
    CustomerBusinessProblem: NotRequired[str]
    CustomerUseCase: NotRequired[str]
    DeliveryModels: NotRequired[Sequence[DeliveryModelType]]
    ExpectedCustomerSpend: NotRequired[Sequence[ExpectedCustomerSpendTypeDef]]
    OtherCompetitorNames: NotRequired[str]
    OtherSolutionDescription: NotRequired[str]
    RelatedOpportunityIdentifier: NotRequired[str]
    SalesActivities: NotRequired[Sequence[SalesActivityType]]
    Title: NotRequired[str]

class StartEngagementFromOpportunityTaskRequestRequestTypeDef(TypedDict):
    AwsSubmission: AwsSubmissionTypeDef
    Catalog: str
    ClientToken: str
    Identifier: str

class CreateOpportunityResponseTypeDef(TypedDict):
    Id: str
    LastModifiedDate: datetime
    PartnerOpportunityIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class StartEngagementByAcceptingInvitationTaskResponseTypeDef(TypedDict):
    EngagementInvitationId: str
    Message: str
    OpportunityId: str
    ReasonCode: ReasonCodeType
    StartTime: datetime
    TaskArn: str
    TaskId: str
    TaskStatus: TaskStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class StartEngagementFromOpportunityTaskResponseTypeDef(TypedDict):
    Message: str
    OpportunityId: str
    ReasonCode: ReasonCodeType
    StartTime: datetime
    TaskArn: str
    TaskId: str
    TaskStatus: TaskStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateOpportunityResponseTypeDef(TypedDict):
    Id: str
    LastModifiedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class LastModifiedDateTypeDef(TypedDict):
    AfterLastModifiedDate: NotRequired[TimestampTypeDef]
    BeforeLastModifiedDate: NotRequired[TimestampTypeDef]

class NextStepsHistoryTypeDef(TypedDict):
    Time: TimestampTypeDef
    Value: str

class LifeCycleOutputTypeDef(TypedDict):
    ClosedLostReason: NotRequired[ClosedLostReasonType]
    NextSteps: NotRequired[str]
    NextStepsHistory: NotRequired[List[NextStepsHistoryOutputTypeDef]]
    ReviewComments: NotRequired[str]
    ReviewStatus: NotRequired[ReviewStatusType]
    ReviewStatusReason: NotRequired[str]
    Stage: NotRequired[StageType]
    TargetCloseDate: NotRequired[str]

class ListEngagementInvitationsRequestRequestTypeDef(TypedDict):
    Catalog: str
    ParticipantType: Literal["RECEIVER"]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    PayloadType: NotRequired[Sequence[Literal["OpportunityInvitation"]]]
    Sort: NotRequired[OpportunityEngagementInvitationSortTypeDef]

class ListEngagementInvitationsRequestListEngagementInvitationsPaginateTypeDef(TypedDict):
    Catalog: str
    ParticipantType: Literal["RECEIVER"]
    PayloadType: NotRequired[Sequence[Literal["OpportunityInvitation"]]]
    Sort: NotRequired[OpportunityEngagementInvitationSortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSolutionsRequestListSolutionsPaginateTypeDef(TypedDict):
    Catalog: str
    Category: NotRequired[Sequence[str]]
    Identifier: NotRequired[Sequence[str]]
    Sort: NotRequired[SolutionSortTypeDef]
    Status: NotRequired[Sequence[SolutionStatusType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSolutionsRequestRequestTypeDef(TypedDict):
    Catalog: str
    Category: NotRequired[Sequence[str]]
    Identifier: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Sort: NotRequired[SolutionSortTypeDef]
    Status: NotRequired[Sequence[SolutionStatusType]]

class ListSolutionsResponseTypeDef(TypedDict):
    SolutionSummaries: List[SolutionBaseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class SoftwareRevenueTypeDef(TypedDict):
    DeliveryModel: NotRequired[RevenueModelType]
    EffectiveDate: NotRequired[str]
    ExpirationDate: NotRequired[str]
    Value: NotRequired[MonetaryValueTypeDef]

class EngagementInvitationSummaryTypeDef(TypedDict):
    Catalog: str
    Id: str
    Arn: NotRequired[str]
    EngagementTitle: NotRequired[str]
    ExpirationDate: NotRequired[datetime]
    InvitationDate: NotRequired[datetime]
    PayloadType: NotRequired[Literal["OpportunityInvitation"]]
    Receiver: NotRequired[ReceiverTypeDef]
    SenderAwsAccountId: NotRequired[str]
    SenderCompanyName: NotRequired[str]
    Status: NotRequired[InvitationStatusType]

class CustomerSummaryTypeDef(TypedDict):
    Account: NotRequired[AccountSummaryTypeDef]

class CustomerOutputTypeDef(TypedDict):
    Account: NotRequired[AccountTypeDef]
    Contacts: NotRequired[List[ContactTypeDef]]

class CustomerTypeDef(TypedDict):
    Account: NotRequired[AccountTypeDef]
    Contacts: NotRequired[Sequence[ContactTypeDef]]

class GetAwsOpportunitySummaryResponseTypeDef(TypedDict):
    Catalog: str
    Customer: AwsOpportunityCustomerTypeDef
    Insights: AwsOpportunityInsightsTypeDef
    InvolvementType: SalesInvolvementTypeType
    InvolvementTypeChangeReason: InvolvementTypeChangeReasonType
    LifeCycle: AwsOpportunityLifeCycleTypeDef
    OpportunityTeam: List[AwsTeamMemberTypeDef]
    Origin: OpportunityOriginType
    Project: AwsOpportunityProjectTypeDef
    RelatedEntityIds: AwsOpportunityRelatedEntitiesTypeDef
    RelatedOpportunityId: str
    Visibility: VisibilityType
    ResponseMetadata: ResponseMetadataTypeDef

class OpportunityInvitationPayloadTypeDef(TypedDict):
    Customer: EngagementCustomerTypeDef
    Project: ProjectDetailsTypeDef
    ReceiverResponsibilities: List[ReceiverResponsibilityType]
    SenderContacts: NotRequired[List[SenderContactTypeDef]]

class ListOpportunitiesRequestListOpportunitiesPaginateTypeDef(TypedDict):
    Catalog: str
    CustomerCompanyName: NotRequired[Sequence[str]]
    Identifier: NotRequired[Sequence[str]]
    LastModifiedDate: NotRequired[LastModifiedDateTypeDef]
    LifeCycleReviewStatus: NotRequired[Sequence[ReviewStatusType]]
    LifeCycleStage: NotRequired[Sequence[StageType]]
    Sort: NotRequired[OpportunitySortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOpportunitiesRequestRequestTypeDef(TypedDict):
    Catalog: str
    CustomerCompanyName: NotRequired[Sequence[str]]
    Identifier: NotRequired[Sequence[str]]
    LastModifiedDate: NotRequired[LastModifiedDateTypeDef]
    LifeCycleReviewStatus: NotRequired[Sequence[ReviewStatusType]]
    LifeCycleStage: NotRequired[Sequence[StageType]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Sort: NotRequired[OpportunitySortTypeDef]

NextStepsHistoryUnionTypeDef = Union[NextStepsHistoryTypeDef, NextStepsHistoryOutputTypeDef]

class ListEngagementInvitationsResponseTypeDef(TypedDict):
    EngagementInvitationSummaries: List[EngagementInvitationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class OpportunitySummaryTypeDef(TypedDict):
    Catalog: str
    CreatedDate: NotRequired[datetime]
    Customer: NotRequired[CustomerSummaryTypeDef]
    Id: NotRequired[str]
    LastModifiedDate: NotRequired[datetime]
    LifeCycle: NotRequired[LifeCycleSummaryTypeDef]
    OpportunityType: NotRequired[OpportunityTypeType]
    PartnerOpportunityIdentifier: NotRequired[str]
    Project: NotRequired[ProjectSummaryTypeDef]

class GetOpportunityResponseTypeDef(TypedDict):
    Catalog: str
    CreatedDate: datetime
    Customer: CustomerOutputTypeDef
    Id: str
    LastModifiedDate: datetime
    LifeCycle: LifeCycleOutputTypeDef
    Marketing: MarketingOutputTypeDef
    NationalSecurity: NationalSecurityType
    OpportunityTeam: List[ContactTypeDef]
    OpportunityType: OpportunityTypeType
    PartnerOpportunityIdentifier: str
    PrimaryNeedsFromAws: List[PrimaryNeedFromAwsType]
    Project: ProjectOutputTypeDef
    RelatedEntityIdentifiers: RelatedEntityIdentifiersTypeDef
    SoftwareRevenue: SoftwareRevenueTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PayloadTypeDef(TypedDict):
    OpportunityInvitation: NotRequired[OpportunityInvitationPayloadTypeDef]

class LifeCycleTypeDef(TypedDict):
    ClosedLostReason: NotRequired[ClosedLostReasonType]
    NextSteps: NotRequired[str]
    NextStepsHistory: NotRequired[Sequence[NextStepsHistoryUnionTypeDef]]
    ReviewComments: NotRequired[str]
    ReviewStatus: NotRequired[ReviewStatusType]
    ReviewStatusReason: NotRequired[str]
    Stage: NotRequired[StageType]
    TargetCloseDate: NotRequired[str]

class ListOpportunitiesResponseTypeDef(TypedDict):
    OpportunitySummaries: List[OpportunitySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetEngagementInvitationResponseTypeDef(TypedDict):
    Arn: str
    Catalog: str
    EngagementTitle: str
    ExpirationDate: datetime
    Id: str
    InvitationDate: datetime
    Payload: PayloadTypeDef
    PayloadType: Literal["OpportunityInvitation"]
    Receiver: ReceiverTypeDef
    RejectionReason: str
    SenderAwsAccountId: str
    SenderCompanyName: str
    Status: InvitationStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateOpportunityRequestRequestTypeDef(TypedDict):
    Catalog: str
    ClientToken: str
    Customer: NotRequired[CustomerTypeDef]
    LifeCycle: NotRequired[LifeCycleTypeDef]
    Marketing: NotRequired[MarketingTypeDef]
    NationalSecurity: NotRequired[NationalSecurityType]
    OpportunityTeam: NotRequired[Sequence[ContactTypeDef]]
    OpportunityType: NotRequired[OpportunityTypeType]
    Origin: NotRequired[OpportunityOriginType]
    PartnerOpportunityIdentifier: NotRequired[str]
    PrimaryNeedsFromAws: NotRequired[Sequence[PrimaryNeedFromAwsType]]
    Project: NotRequired[ProjectTypeDef]
    SoftwareRevenue: NotRequired[SoftwareRevenueTypeDef]

class UpdateOpportunityRequestRequestTypeDef(TypedDict):
    Catalog: str
    Identifier: str
    LastModifiedDate: TimestampTypeDef
    Customer: NotRequired[CustomerTypeDef]
    LifeCycle: NotRequired[LifeCycleTypeDef]
    Marketing: NotRequired[MarketingTypeDef]
    NationalSecurity: NotRequired[NationalSecurityType]
    OpportunityType: NotRequired[OpportunityTypeType]
    PartnerOpportunityIdentifier: NotRequired[str]
    PrimaryNeedsFromAws: NotRequired[Sequence[PrimaryNeedFromAwsType]]
    Project: NotRequired[ProjectTypeDef]
    SoftwareRevenue: NotRequired[SoftwareRevenueTypeDef]
