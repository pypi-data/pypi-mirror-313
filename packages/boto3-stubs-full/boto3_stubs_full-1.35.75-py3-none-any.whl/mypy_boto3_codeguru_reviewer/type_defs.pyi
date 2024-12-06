"""
Type annotations for codeguru-reviewer service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_reviewer/type_defs/)

Usage::

    ```python
    from mypy_boto3_codeguru_reviewer.type_defs import KMSKeyDetailsTypeDef

    data: KMSKeyDetailsTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AnalysisTypeType,
    ConfigFileStateType,
    EncryptionOptionType,
    JobStateType,
    ProviderTypeType,
    ReactionType,
    RecommendationCategoryType,
    RepositoryAssociationStateType,
    SeverityType,
    TypeType,
    VendorNameType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AssociateRepositoryRequestRequestTypeDef",
    "AssociateRepositoryResponseTypeDef",
    "BranchDiffSourceCodeTypeTypeDef",
    "CodeArtifactsTypeDef",
    "CodeCommitRepositoryTypeDef",
    "CodeReviewSummaryTypeDef",
    "CodeReviewTypeDef",
    "CodeReviewTypeTypeDef",
    "CommitDiffSourceCodeTypeTypeDef",
    "CreateCodeReviewRequestRequestTypeDef",
    "CreateCodeReviewResponseTypeDef",
    "DescribeCodeReviewRequestCodeReviewCompletedWaitTypeDef",
    "DescribeCodeReviewRequestRequestTypeDef",
    "DescribeCodeReviewResponseTypeDef",
    "DescribeRecommendationFeedbackRequestRequestTypeDef",
    "DescribeRecommendationFeedbackResponseTypeDef",
    "DescribeRepositoryAssociationRequestRepositoryAssociationSucceededWaitTypeDef",
    "DescribeRepositoryAssociationRequestRequestTypeDef",
    "DescribeRepositoryAssociationResponseTypeDef",
    "DisassociateRepositoryRequestRequestTypeDef",
    "DisassociateRepositoryResponseTypeDef",
    "EventInfoTypeDef",
    "KMSKeyDetailsTypeDef",
    "ListCodeReviewsRequestRequestTypeDef",
    "ListCodeReviewsResponseTypeDef",
    "ListRecommendationFeedbackRequestRequestTypeDef",
    "ListRecommendationFeedbackResponseTypeDef",
    "ListRecommendationsRequestRequestTypeDef",
    "ListRecommendationsResponseTypeDef",
    "ListRepositoryAssociationsRequestListRepositoryAssociationsPaginateTypeDef",
    "ListRepositoryAssociationsRequestRequestTypeDef",
    "ListRepositoryAssociationsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MetricsSummaryTypeDef",
    "MetricsTypeDef",
    "PaginatorConfigTypeDef",
    "PutRecommendationFeedbackRequestRequestTypeDef",
    "RecommendationFeedbackSummaryTypeDef",
    "RecommendationFeedbackTypeDef",
    "RecommendationSummaryTypeDef",
    "RepositoryAnalysisTypeDef",
    "RepositoryAssociationSummaryTypeDef",
    "RepositoryAssociationTypeDef",
    "RepositoryHeadSourceCodeTypeTypeDef",
    "RepositoryTypeDef",
    "RequestMetadataTypeDef",
    "ResponseMetadataTypeDef",
    "RuleMetadataTypeDef",
    "S3BucketRepositoryTypeDef",
    "S3RepositoryDetailsTypeDef",
    "S3RepositoryTypeDef",
    "SourceCodeTypeTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ThirdPartySourceRepositoryTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "WaiterConfigTypeDef",
)

class KMSKeyDetailsTypeDef(TypedDict):
    KMSKeyId: NotRequired[str]
    EncryptionOption: NotRequired[EncryptionOptionType]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BranchDiffSourceCodeTypeTypeDef(TypedDict):
    SourceBranchName: str
    DestinationBranchName: str

class CodeArtifactsTypeDef(TypedDict):
    SourceCodeArtifactsObjectKey: str
    BuildArtifactsObjectKey: NotRequired[str]

class CodeCommitRepositoryTypeDef(TypedDict):
    Name: str

class MetricsSummaryTypeDef(TypedDict):
    MeteredLinesOfCodeCount: NotRequired[int]
    SuppressedLinesOfCodeCount: NotRequired[int]
    FindingsCount: NotRequired[int]

class MetricsTypeDef(TypedDict):
    MeteredLinesOfCodeCount: NotRequired[int]
    SuppressedLinesOfCodeCount: NotRequired[int]
    FindingsCount: NotRequired[int]

class CommitDiffSourceCodeTypeTypeDef(TypedDict):
    SourceCommit: NotRequired[str]
    DestinationCommit: NotRequired[str]
    MergeBaseCommit: NotRequired[str]

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class DescribeCodeReviewRequestRequestTypeDef(TypedDict):
    CodeReviewArn: str

class DescribeRecommendationFeedbackRequestRequestTypeDef(TypedDict):
    CodeReviewArn: str
    RecommendationId: str
    UserId: NotRequired[str]

class RecommendationFeedbackTypeDef(TypedDict):
    CodeReviewArn: NotRequired[str]
    RecommendationId: NotRequired[str]
    Reactions: NotRequired[List[ReactionType]]
    UserId: NotRequired[str]
    CreatedTimeStamp: NotRequired[datetime]
    LastUpdatedTimeStamp: NotRequired[datetime]

class DescribeRepositoryAssociationRequestRequestTypeDef(TypedDict):
    AssociationArn: str

class DisassociateRepositoryRequestRequestTypeDef(TypedDict):
    AssociationArn: str

class EventInfoTypeDef(TypedDict):
    Name: NotRequired[str]
    State: NotRequired[str]

ListCodeReviewsRequestRequestTypeDef = TypedDict(
    "ListCodeReviewsRequestRequestTypeDef",
    {
        "Type": TypeType,
        "ProviderTypes": NotRequired[Sequence[ProviderTypeType]],
        "States": NotRequired[Sequence[JobStateType]],
        "RepositoryNames": NotRequired[Sequence[str]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

class ListRecommendationFeedbackRequestRequestTypeDef(TypedDict):
    CodeReviewArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    UserIds: NotRequired[Sequence[str]]
    RecommendationIds: NotRequired[Sequence[str]]

class RecommendationFeedbackSummaryTypeDef(TypedDict):
    RecommendationId: NotRequired[str]
    Reactions: NotRequired[List[ReactionType]]
    UserId: NotRequired[str]

class ListRecommendationsRequestRequestTypeDef(TypedDict):
    CodeReviewArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListRepositoryAssociationsRequestRequestTypeDef(TypedDict):
    ProviderTypes: NotRequired[Sequence[ProviderTypeType]]
    States: NotRequired[Sequence[RepositoryAssociationStateType]]
    Names: NotRequired[Sequence[str]]
    Owners: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class RepositoryAssociationSummaryTypeDef(TypedDict):
    AssociationArn: NotRequired[str]
    ConnectionArn: NotRequired[str]
    LastUpdatedTimeStamp: NotRequired[datetime]
    AssociationId: NotRequired[str]
    Name: NotRequired[str]
    Owner: NotRequired[str]
    ProviderType: NotRequired[ProviderTypeType]
    State: NotRequired[RepositoryAssociationStateType]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class PutRecommendationFeedbackRequestRequestTypeDef(TypedDict):
    CodeReviewArn: str
    RecommendationId: str
    Reactions: Sequence[ReactionType]

class RuleMetadataTypeDef(TypedDict):
    RuleId: NotRequired[str]
    RuleName: NotRequired[str]
    ShortDescription: NotRequired[str]
    LongDescription: NotRequired[str]
    RuleTags: NotRequired[List[str]]

class RepositoryHeadSourceCodeTypeTypeDef(TypedDict):
    BranchName: str

class S3RepositoryTypeDef(TypedDict):
    Name: str
    BucketName: str

class ThirdPartySourceRepositoryTypeDef(TypedDict):
    Name: str
    ConnectionArn: str
    Owner: str

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    TagKeys: Sequence[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class S3RepositoryDetailsTypeDef(TypedDict):
    BucketName: NotRequired[str]
    CodeArtifacts: NotRequired[CodeArtifactsTypeDef]

class DescribeCodeReviewRequestCodeReviewCompletedWaitTypeDef(TypedDict):
    CodeReviewArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeRepositoryAssociationRequestRepositoryAssociationSucceededWaitTypeDef(TypedDict):
    AssociationArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeRecommendationFeedbackResponseTypeDef(TypedDict):
    RecommendationFeedback: RecommendationFeedbackTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class RequestMetadataTypeDef(TypedDict):
    RequestId: NotRequired[str]
    Requester: NotRequired[str]
    EventInfo: NotRequired[EventInfoTypeDef]
    VendorName: NotRequired[VendorNameType]

class ListRecommendationFeedbackResponseTypeDef(TypedDict):
    RecommendationFeedbackSummaries: List[RecommendationFeedbackSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListRepositoryAssociationsRequestListRepositoryAssociationsPaginateTypeDef(TypedDict):
    ProviderTypes: NotRequired[Sequence[ProviderTypeType]]
    States: NotRequired[Sequence[RepositoryAssociationStateType]]
    Names: NotRequired[Sequence[str]]
    Owners: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRepositoryAssociationsResponseTypeDef(TypedDict):
    RepositoryAssociationSummaries: List[RepositoryAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class RecommendationSummaryTypeDef(TypedDict):
    FilePath: NotRequired[str]
    RecommendationId: NotRequired[str]
    StartLine: NotRequired[int]
    EndLine: NotRequired[int]
    Description: NotRequired[str]
    RecommendationCategory: NotRequired[RecommendationCategoryType]
    RuleMetadata: NotRequired[RuleMetadataTypeDef]
    Severity: NotRequired[SeverityType]

class RepositoryTypeDef(TypedDict):
    CodeCommit: NotRequired[CodeCommitRepositoryTypeDef]
    Bitbucket: NotRequired[ThirdPartySourceRepositoryTypeDef]
    GitHubEnterpriseServer: NotRequired[ThirdPartySourceRepositoryTypeDef]
    S3Bucket: NotRequired[S3RepositoryTypeDef]

class RepositoryAssociationTypeDef(TypedDict):
    AssociationId: NotRequired[str]
    AssociationArn: NotRequired[str]
    ConnectionArn: NotRequired[str]
    Name: NotRequired[str]
    Owner: NotRequired[str]
    ProviderType: NotRequired[ProviderTypeType]
    State: NotRequired[RepositoryAssociationStateType]
    StateReason: NotRequired[str]
    LastUpdatedTimeStamp: NotRequired[datetime]
    CreatedTimeStamp: NotRequired[datetime]
    KMSKeyDetails: NotRequired[KMSKeyDetailsTypeDef]
    S3RepositoryDetails: NotRequired[S3RepositoryDetailsTypeDef]

class S3BucketRepositoryTypeDef(TypedDict):
    Name: str
    Details: NotRequired[S3RepositoryDetailsTypeDef]

class ListRecommendationsResponseTypeDef(TypedDict):
    RecommendationSummaries: List[RecommendationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class AssociateRepositoryRequestRequestTypeDef(TypedDict):
    Repository: RepositoryTypeDef
    ClientRequestToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    KMSKeyDetails: NotRequired[KMSKeyDetailsTypeDef]

class AssociateRepositoryResponseTypeDef(TypedDict):
    RepositoryAssociation: RepositoryAssociationTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeRepositoryAssociationResponseTypeDef(TypedDict):
    RepositoryAssociation: RepositoryAssociationTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociateRepositoryResponseTypeDef(TypedDict):
    RepositoryAssociation: RepositoryAssociationTypeDef
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class SourceCodeTypeTypeDef(TypedDict):
    CommitDiff: NotRequired[CommitDiffSourceCodeTypeTypeDef]
    RepositoryHead: NotRequired[RepositoryHeadSourceCodeTypeTypeDef]
    BranchDiff: NotRequired[BranchDiffSourceCodeTypeTypeDef]
    S3BucketRepository: NotRequired[S3BucketRepositoryTypeDef]
    RequestMetadata: NotRequired[RequestMetadataTypeDef]

CodeReviewSummaryTypeDef = TypedDict(
    "CodeReviewSummaryTypeDef",
    {
        "Name": NotRequired[str],
        "CodeReviewArn": NotRequired[str],
        "RepositoryName": NotRequired[str],
        "Owner": NotRequired[str],
        "ProviderType": NotRequired[ProviderTypeType],
        "State": NotRequired[JobStateType],
        "CreatedTimeStamp": NotRequired[datetime],
        "LastUpdatedTimeStamp": NotRequired[datetime],
        "Type": NotRequired[TypeType],
        "PullRequestId": NotRequired[str],
        "MetricsSummary": NotRequired[MetricsSummaryTypeDef],
        "SourceCodeType": NotRequired[SourceCodeTypeTypeDef],
    },
)
CodeReviewTypeDef = TypedDict(
    "CodeReviewTypeDef",
    {
        "Name": NotRequired[str],
        "CodeReviewArn": NotRequired[str],
        "RepositoryName": NotRequired[str],
        "Owner": NotRequired[str],
        "ProviderType": NotRequired[ProviderTypeType],
        "State": NotRequired[JobStateType],
        "StateReason": NotRequired[str],
        "CreatedTimeStamp": NotRequired[datetime],
        "LastUpdatedTimeStamp": NotRequired[datetime],
        "Type": NotRequired[TypeType],
        "PullRequestId": NotRequired[str],
        "SourceCodeType": NotRequired[SourceCodeTypeTypeDef],
        "AssociationArn": NotRequired[str],
        "Metrics": NotRequired[MetricsTypeDef],
        "AnalysisTypes": NotRequired[List[AnalysisTypeType]],
        "ConfigFileState": NotRequired[ConfigFileStateType],
    },
)

class RepositoryAnalysisTypeDef(TypedDict):
    RepositoryHead: NotRequired[RepositoryHeadSourceCodeTypeTypeDef]
    SourceCodeType: NotRequired[SourceCodeTypeTypeDef]

class ListCodeReviewsResponseTypeDef(TypedDict):
    CodeReviewSummaries: List[CodeReviewSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateCodeReviewResponseTypeDef(TypedDict):
    CodeReview: CodeReviewTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeCodeReviewResponseTypeDef(TypedDict):
    CodeReview: CodeReviewTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CodeReviewTypeTypeDef(TypedDict):
    RepositoryAnalysis: RepositoryAnalysisTypeDef
    AnalysisTypes: NotRequired[Sequence[AnalysisTypeType]]

CreateCodeReviewRequestRequestTypeDef = TypedDict(
    "CreateCodeReviewRequestRequestTypeDef",
    {
        "Name": str,
        "RepositoryAssociationArn": str,
        "Type": CodeReviewTypeTypeDef,
        "ClientRequestToken": NotRequired[str],
    },
)
