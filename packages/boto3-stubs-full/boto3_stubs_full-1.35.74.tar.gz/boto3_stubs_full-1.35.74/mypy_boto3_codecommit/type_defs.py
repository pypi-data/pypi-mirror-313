"""
Type annotations for codecommit service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/type_defs/)

Usage::

    ```python
    from mypy_boto3_codecommit.type_defs import ApprovalRuleEventMetadataTypeDef

    data: ApprovalRuleEventMetadataTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ApprovalStateType,
    BatchGetRepositoriesErrorCodeEnumType,
    ChangeTypeEnumType,
    ConflictDetailLevelTypeEnumType,
    ConflictResolutionStrategyTypeEnumType,
    FileModeTypeEnumType,
    MergeOptionTypeEnumType,
    ObjectTypeEnumType,
    OrderEnumType,
    OverrideStatusType,
    PullRequestEventTypeType,
    PullRequestStatusEnumType,
    RelativeFileVersionEnumType,
    ReplacementTypeEnumType,
    RepositoryTriggerEventEnumType,
    SortByEnumType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ApprovalRuleEventMetadataTypeDef",
    "ApprovalRuleOverriddenEventMetadataTypeDef",
    "ApprovalRuleTemplateTypeDef",
    "ApprovalRuleTypeDef",
    "ApprovalStateChangedEventMetadataTypeDef",
    "ApprovalTypeDef",
    "AssociateApprovalRuleTemplateWithRepositoryInputRequestTypeDef",
    "BatchAssociateApprovalRuleTemplateWithRepositoriesErrorTypeDef",
    "BatchAssociateApprovalRuleTemplateWithRepositoriesInputRequestTypeDef",
    "BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef",
    "BatchDescribeMergeConflictsErrorTypeDef",
    "BatchDescribeMergeConflictsInputRequestTypeDef",
    "BatchDescribeMergeConflictsOutputTypeDef",
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesErrorTypeDef",
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesInputRequestTypeDef",
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef",
    "BatchGetCommitsErrorTypeDef",
    "BatchGetCommitsInputRequestTypeDef",
    "BatchGetCommitsOutputTypeDef",
    "BatchGetRepositoriesErrorTypeDef",
    "BatchGetRepositoriesInputRequestTypeDef",
    "BatchGetRepositoriesOutputTypeDef",
    "BlobMetadataTypeDef",
    "BlobTypeDef",
    "BranchInfoTypeDef",
    "CommentTypeDef",
    "CommentsForComparedCommitTypeDef",
    "CommentsForPullRequestTypeDef",
    "CommitTypeDef",
    "ConflictMetadataTypeDef",
    "ConflictResolutionTypeDef",
    "ConflictTypeDef",
    "CreateApprovalRuleTemplateInputRequestTypeDef",
    "CreateApprovalRuleTemplateOutputTypeDef",
    "CreateBranchInputRequestTypeDef",
    "CreateCommitInputRequestTypeDef",
    "CreateCommitOutputTypeDef",
    "CreatePullRequestApprovalRuleInputRequestTypeDef",
    "CreatePullRequestApprovalRuleOutputTypeDef",
    "CreatePullRequestInputRequestTypeDef",
    "CreatePullRequestOutputTypeDef",
    "CreateRepositoryInputRequestTypeDef",
    "CreateRepositoryOutputTypeDef",
    "CreateUnreferencedMergeCommitInputRequestTypeDef",
    "CreateUnreferencedMergeCommitOutputTypeDef",
    "DeleteApprovalRuleTemplateInputRequestTypeDef",
    "DeleteApprovalRuleTemplateOutputTypeDef",
    "DeleteBranchInputRequestTypeDef",
    "DeleteBranchOutputTypeDef",
    "DeleteCommentContentInputRequestTypeDef",
    "DeleteCommentContentOutputTypeDef",
    "DeleteFileEntryTypeDef",
    "DeleteFileInputRequestTypeDef",
    "DeleteFileOutputTypeDef",
    "DeletePullRequestApprovalRuleInputRequestTypeDef",
    "DeletePullRequestApprovalRuleOutputTypeDef",
    "DeleteRepositoryInputRequestTypeDef",
    "DeleteRepositoryOutputTypeDef",
    "DescribeMergeConflictsInputRequestTypeDef",
    "DescribeMergeConflictsOutputTypeDef",
    "DescribePullRequestEventsInputDescribePullRequestEventsPaginateTypeDef",
    "DescribePullRequestEventsInputRequestTypeDef",
    "DescribePullRequestEventsOutputTypeDef",
    "DifferenceTypeDef",
    "DisassociateApprovalRuleTemplateFromRepositoryInputRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EvaluatePullRequestApprovalRulesInputRequestTypeDef",
    "EvaluatePullRequestApprovalRulesOutputTypeDef",
    "EvaluationTypeDef",
    "FileMetadataTypeDef",
    "FileModesTypeDef",
    "FileSizesTypeDef",
    "FileTypeDef",
    "FileVersionTypeDef",
    "FolderTypeDef",
    "GetApprovalRuleTemplateInputRequestTypeDef",
    "GetApprovalRuleTemplateOutputTypeDef",
    "GetBlobInputRequestTypeDef",
    "GetBlobOutputTypeDef",
    "GetBranchInputRequestTypeDef",
    "GetBranchOutputTypeDef",
    "GetCommentInputRequestTypeDef",
    "GetCommentOutputTypeDef",
    "GetCommentReactionsInputRequestTypeDef",
    "GetCommentReactionsOutputTypeDef",
    "GetCommentsForComparedCommitInputGetCommentsForComparedCommitPaginateTypeDef",
    "GetCommentsForComparedCommitInputRequestTypeDef",
    "GetCommentsForComparedCommitOutputTypeDef",
    "GetCommentsForPullRequestInputGetCommentsForPullRequestPaginateTypeDef",
    "GetCommentsForPullRequestInputRequestTypeDef",
    "GetCommentsForPullRequestOutputTypeDef",
    "GetCommitInputRequestTypeDef",
    "GetCommitOutputTypeDef",
    "GetDifferencesInputGetDifferencesPaginateTypeDef",
    "GetDifferencesInputRequestTypeDef",
    "GetDifferencesOutputTypeDef",
    "GetFileInputRequestTypeDef",
    "GetFileOutputTypeDef",
    "GetFolderInputRequestTypeDef",
    "GetFolderOutputTypeDef",
    "GetMergeCommitInputRequestTypeDef",
    "GetMergeCommitOutputTypeDef",
    "GetMergeConflictsInputRequestTypeDef",
    "GetMergeConflictsOutputTypeDef",
    "GetMergeOptionsInputRequestTypeDef",
    "GetMergeOptionsOutputTypeDef",
    "GetPullRequestApprovalStatesInputRequestTypeDef",
    "GetPullRequestApprovalStatesOutputTypeDef",
    "GetPullRequestInputRequestTypeDef",
    "GetPullRequestOutputTypeDef",
    "GetPullRequestOverrideStateInputRequestTypeDef",
    "GetPullRequestOverrideStateOutputTypeDef",
    "GetRepositoryInputRequestTypeDef",
    "GetRepositoryOutputTypeDef",
    "GetRepositoryTriggersInputRequestTypeDef",
    "GetRepositoryTriggersOutputTypeDef",
    "IsBinaryFileTypeDef",
    "ListApprovalRuleTemplatesInputRequestTypeDef",
    "ListApprovalRuleTemplatesOutputTypeDef",
    "ListAssociatedApprovalRuleTemplatesForRepositoryInputRequestTypeDef",
    "ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef",
    "ListBranchesInputListBranchesPaginateTypeDef",
    "ListBranchesInputRequestTypeDef",
    "ListBranchesOutputTypeDef",
    "ListFileCommitHistoryRequestRequestTypeDef",
    "ListFileCommitHistoryResponseTypeDef",
    "ListPullRequestsInputListPullRequestsPaginateTypeDef",
    "ListPullRequestsInputRequestTypeDef",
    "ListPullRequestsOutputTypeDef",
    "ListRepositoriesForApprovalRuleTemplateInputRequestTypeDef",
    "ListRepositoriesForApprovalRuleTemplateOutputTypeDef",
    "ListRepositoriesInputListRepositoriesPaginateTypeDef",
    "ListRepositoriesInputRequestTypeDef",
    "ListRepositoriesOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "LocationTypeDef",
    "MergeBranchesByFastForwardInputRequestTypeDef",
    "MergeBranchesByFastForwardOutputTypeDef",
    "MergeBranchesBySquashInputRequestTypeDef",
    "MergeBranchesBySquashOutputTypeDef",
    "MergeBranchesByThreeWayInputRequestTypeDef",
    "MergeBranchesByThreeWayOutputTypeDef",
    "MergeHunkDetailTypeDef",
    "MergeHunkTypeDef",
    "MergeMetadataTypeDef",
    "MergeOperationsTypeDef",
    "MergePullRequestByFastForwardInputRequestTypeDef",
    "MergePullRequestByFastForwardOutputTypeDef",
    "MergePullRequestBySquashInputRequestTypeDef",
    "MergePullRequestBySquashOutputTypeDef",
    "MergePullRequestByThreeWayInputRequestTypeDef",
    "MergePullRequestByThreeWayOutputTypeDef",
    "ObjectTypesTypeDef",
    "OriginApprovalRuleTemplateTypeDef",
    "OverridePullRequestApprovalRulesInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "PostCommentForComparedCommitInputRequestTypeDef",
    "PostCommentForComparedCommitOutputTypeDef",
    "PostCommentForPullRequestInputRequestTypeDef",
    "PostCommentForPullRequestOutputTypeDef",
    "PostCommentReplyInputRequestTypeDef",
    "PostCommentReplyOutputTypeDef",
    "PullRequestCreatedEventMetadataTypeDef",
    "PullRequestEventTypeDef",
    "PullRequestMergedStateChangedEventMetadataTypeDef",
    "PullRequestSourceReferenceUpdatedEventMetadataTypeDef",
    "PullRequestStatusChangedEventMetadataTypeDef",
    "PullRequestTargetTypeDef",
    "PullRequestTypeDef",
    "PutCommentReactionInputRequestTypeDef",
    "PutFileEntryTypeDef",
    "PutFileInputRequestTypeDef",
    "PutFileOutputTypeDef",
    "PutRepositoryTriggersInputRequestTypeDef",
    "PutRepositoryTriggersOutputTypeDef",
    "ReactionForCommentTypeDef",
    "ReactionValueFormatsTypeDef",
    "ReplaceContentEntryTypeDef",
    "RepositoryMetadataTypeDef",
    "RepositoryNameIdPairTypeDef",
    "RepositoryTriggerExecutionFailureTypeDef",
    "RepositoryTriggerOutputTypeDef",
    "RepositoryTriggerTypeDef",
    "RepositoryTriggerUnionTypeDef",
    "ResponseMetadataTypeDef",
    "SetFileModeEntryTypeDef",
    "SourceFileSpecifierTypeDef",
    "SubModuleTypeDef",
    "SymbolicLinkTypeDef",
    "TagResourceInputRequestTypeDef",
    "TargetTypeDef",
    "TestRepositoryTriggersInputRequestTypeDef",
    "TestRepositoryTriggersOutputTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateApprovalRuleTemplateContentInputRequestTypeDef",
    "UpdateApprovalRuleTemplateContentOutputTypeDef",
    "UpdateApprovalRuleTemplateDescriptionInputRequestTypeDef",
    "UpdateApprovalRuleTemplateDescriptionOutputTypeDef",
    "UpdateApprovalRuleTemplateNameInputRequestTypeDef",
    "UpdateApprovalRuleTemplateNameOutputTypeDef",
    "UpdateCommentInputRequestTypeDef",
    "UpdateCommentOutputTypeDef",
    "UpdateDefaultBranchInputRequestTypeDef",
    "UpdatePullRequestApprovalRuleContentInputRequestTypeDef",
    "UpdatePullRequestApprovalRuleContentOutputTypeDef",
    "UpdatePullRequestApprovalStateInputRequestTypeDef",
    "UpdatePullRequestDescriptionInputRequestTypeDef",
    "UpdatePullRequestDescriptionOutputTypeDef",
    "UpdatePullRequestStatusInputRequestTypeDef",
    "UpdatePullRequestStatusOutputTypeDef",
    "UpdatePullRequestTitleInputRequestTypeDef",
    "UpdatePullRequestTitleOutputTypeDef",
    "UpdateRepositoryDescriptionInputRequestTypeDef",
    "UpdateRepositoryEncryptionKeyInputRequestTypeDef",
    "UpdateRepositoryEncryptionKeyOutputTypeDef",
    "UpdateRepositoryNameInputRequestTypeDef",
    "UserInfoTypeDef",
)


class ApprovalRuleEventMetadataTypeDef(TypedDict):
    approvalRuleName: NotRequired[str]
    approvalRuleId: NotRequired[str]
    approvalRuleContent: NotRequired[str]


class ApprovalRuleOverriddenEventMetadataTypeDef(TypedDict):
    revisionId: NotRequired[str]
    overrideStatus: NotRequired[OverrideStatusType]


class ApprovalRuleTemplateTypeDef(TypedDict):
    approvalRuleTemplateId: NotRequired[str]
    approvalRuleTemplateName: NotRequired[str]
    approvalRuleTemplateDescription: NotRequired[str]
    approvalRuleTemplateContent: NotRequired[str]
    ruleContentSha256: NotRequired[str]
    lastModifiedDate: NotRequired[datetime]
    creationDate: NotRequired[datetime]
    lastModifiedUser: NotRequired[str]


class OriginApprovalRuleTemplateTypeDef(TypedDict):
    approvalRuleTemplateId: NotRequired[str]
    approvalRuleTemplateName: NotRequired[str]


class ApprovalStateChangedEventMetadataTypeDef(TypedDict):
    revisionId: NotRequired[str]
    approvalStatus: NotRequired[ApprovalStateType]


class ApprovalTypeDef(TypedDict):
    userArn: NotRequired[str]
    approvalState: NotRequired[ApprovalStateType]


class AssociateApprovalRuleTemplateWithRepositoryInputRequestTypeDef(TypedDict):
    approvalRuleTemplateName: str
    repositoryName: str


class BatchAssociateApprovalRuleTemplateWithRepositoriesErrorTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    errorCode: NotRequired[str]
    errorMessage: NotRequired[str]


class BatchAssociateApprovalRuleTemplateWithRepositoriesInputRequestTypeDef(TypedDict):
    approvalRuleTemplateName: str
    repositoryNames: Sequence[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class BatchDescribeMergeConflictsErrorTypeDef(TypedDict):
    filePath: str
    exceptionName: str
    message: str


class BatchDescribeMergeConflictsInputRequestTypeDef(TypedDict):
    repositoryName: str
    destinationCommitSpecifier: str
    sourceCommitSpecifier: str
    mergeOption: MergeOptionTypeEnumType
    maxMergeHunks: NotRequired[int]
    maxConflictFiles: NotRequired[int]
    filePaths: NotRequired[Sequence[str]]
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]
    nextToken: NotRequired[str]


class BatchDisassociateApprovalRuleTemplateFromRepositoriesErrorTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    errorCode: NotRequired[str]
    errorMessage: NotRequired[str]


class BatchDisassociateApprovalRuleTemplateFromRepositoriesInputRequestTypeDef(TypedDict):
    approvalRuleTemplateName: str
    repositoryNames: Sequence[str]


class BatchGetCommitsErrorTypeDef(TypedDict):
    commitId: NotRequired[str]
    errorCode: NotRequired[str]
    errorMessage: NotRequired[str]


class BatchGetCommitsInputRequestTypeDef(TypedDict):
    commitIds: Sequence[str]
    repositoryName: str


class BatchGetRepositoriesErrorTypeDef(TypedDict):
    repositoryId: NotRequired[str]
    repositoryName: NotRequired[str]
    errorCode: NotRequired[BatchGetRepositoriesErrorCodeEnumType]
    errorMessage: NotRequired[str]


class BatchGetRepositoriesInputRequestTypeDef(TypedDict):
    repositoryNames: Sequence[str]


class RepositoryMetadataTypeDef(TypedDict):
    accountId: NotRequired[str]
    repositoryId: NotRequired[str]
    repositoryName: NotRequired[str]
    repositoryDescription: NotRequired[str]
    defaultBranch: NotRequired[str]
    lastModifiedDate: NotRequired[datetime]
    creationDate: NotRequired[datetime]
    cloneUrlHttp: NotRequired[str]
    cloneUrlSsh: NotRequired[str]
    Arn: NotRequired[str]
    kmsKeyId: NotRequired[str]


class BlobMetadataTypeDef(TypedDict):
    blobId: NotRequired[str]
    path: NotRequired[str]
    mode: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class BranchInfoTypeDef(TypedDict):
    branchName: NotRequired[str]
    commitId: NotRequired[str]


class CommentTypeDef(TypedDict):
    commentId: NotRequired[str]
    content: NotRequired[str]
    inReplyTo: NotRequired[str]
    creationDate: NotRequired[datetime]
    lastModifiedDate: NotRequired[datetime]
    authorArn: NotRequired[str]
    deleted: NotRequired[bool]
    clientRequestToken: NotRequired[str]
    callerReactions: NotRequired[List[str]]
    reactionCounts: NotRequired[Dict[str, int]]


class LocationTypeDef(TypedDict):
    filePath: NotRequired[str]
    filePosition: NotRequired[int]
    relativeFileVersion: NotRequired[RelativeFileVersionEnumType]


class UserInfoTypeDef(TypedDict):
    name: NotRequired[str]
    email: NotRequired[str]
    date: NotRequired[str]


class FileModesTypeDef(TypedDict):
    source: NotRequired[FileModeTypeEnumType]
    destination: NotRequired[FileModeTypeEnumType]
    base: NotRequired[FileModeTypeEnumType]


class FileSizesTypeDef(TypedDict):
    source: NotRequired[int]
    destination: NotRequired[int]
    base: NotRequired[int]


class IsBinaryFileTypeDef(TypedDict):
    source: NotRequired[bool]
    destination: NotRequired[bool]
    base: NotRequired[bool]


class MergeOperationsTypeDef(TypedDict):
    source: NotRequired[ChangeTypeEnumType]
    destination: NotRequired[ChangeTypeEnumType]


class ObjectTypesTypeDef(TypedDict):
    source: NotRequired[ObjectTypeEnumType]
    destination: NotRequired[ObjectTypeEnumType]
    base: NotRequired[ObjectTypeEnumType]


class DeleteFileEntryTypeDef(TypedDict):
    filePath: str


class SetFileModeEntryTypeDef(TypedDict):
    filePath: str
    fileMode: FileModeTypeEnumType


class CreateApprovalRuleTemplateInputRequestTypeDef(TypedDict):
    approvalRuleTemplateName: str
    approvalRuleTemplateContent: str
    approvalRuleTemplateDescription: NotRequired[str]


class CreateBranchInputRequestTypeDef(TypedDict):
    repositoryName: str
    branchName: str
    commitId: str


class FileMetadataTypeDef(TypedDict):
    absolutePath: NotRequired[str]
    blobId: NotRequired[str]
    fileMode: NotRequired[FileModeTypeEnumType]


class CreatePullRequestApprovalRuleInputRequestTypeDef(TypedDict):
    pullRequestId: str
    approvalRuleName: str
    approvalRuleContent: str


class TargetTypeDef(TypedDict):
    repositoryName: str
    sourceReference: str
    destinationReference: NotRequired[str]


class CreateRepositoryInputRequestTypeDef(TypedDict):
    repositoryName: str
    repositoryDescription: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    kmsKeyId: NotRequired[str]


class DeleteApprovalRuleTemplateInputRequestTypeDef(TypedDict):
    approvalRuleTemplateName: str


class DeleteBranchInputRequestTypeDef(TypedDict):
    repositoryName: str
    branchName: str


class DeleteCommentContentInputRequestTypeDef(TypedDict):
    commentId: str


class DeleteFileInputRequestTypeDef(TypedDict):
    repositoryName: str
    branchName: str
    filePath: str
    parentCommitId: str
    keepEmptyFolders: NotRequired[bool]
    commitMessage: NotRequired[str]
    name: NotRequired[str]
    email: NotRequired[str]


class DeletePullRequestApprovalRuleInputRequestTypeDef(TypedDict):
    pullRequestId: str
    approvalRuleName: str


class DeleteRepositoryInputRequestTypeDef(TypedDict):
    repositoryName: str


class DescribeMergeConflictsInputRequestTypeDef(TypedDict):
    repositoryName: str
    destinationCommitSpecifier: str
    sourceCommitSpecifier: str
    mergeOption: MergeOptionTypeEnumType
    filePath: str
    maxMergeHunks: NotRequired[int]
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]
    nextToken: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribePullRequestEventsInputRequestTypeDef(TypedDict):
    pullRequestId: str
    pullRequestEventType: NotRequired[PullRequestEventTypeType]
    actorArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class DisassociateApprovalRuleTemplateFromRepositoryInputRequestTypeDef(TypedDict):
    approvalRuleTemplateName: str
    repositoryName: str


class EvaluatePullRequestApprovalRulesInputRequestTypeDef(TypedDict):
    pullRequestId: str
    revisionId: str


class EvaluationTypeDef(TypedDict):
    approved: NotRequired[bool]
    overridden: NotRequired[bool]
    approvalRulesSatisfied: NotRequired[List[str]]
    approvalRulesNotSatisfied: NotRequired[List[str]]


class FileTypeDef(TypedDict):
    blobId: NotRequired[str]
    absolutePath: NotRequired[str]
    relativePath: NotRequired[str]
    fileMode: NotRequired[FileModeTypeEnumType]


class FolderTypeDef(TypedDict):
    treeId: NotRequired[str]
    absolutePath: NotRequired[str]
    relativePath: NotRequired[str]


class GetApprovalRuleTemplateInputRequestTypeDef(TypedDict):
    approvalRuleTemplateName: str


class GetBlobInputRequestTypeDef(TypedDict):
    repositoryName: str
    blobId: str


class GetBranchInputRequestTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    branchName: NotRequired[str]


class GetCommentInputRequestTypeDef(TypedDict):
    commentId: str


class GetCommentReactionsInputRequestTypeDef(TypedDict):
    commentId: str
    reactionUserArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class GetCommentsForComparedCommitInputRequestTypeDef(TypedDict):
    repositoryName: str
    afterCommitId: str
    beforeCommitId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class GetCommentsForPullRequestInputRequestTypeDef(TypedDict):
    pullRequestId: str
    repositoryName: NotRequired[str]
    beforeCommitId: NotRequired[str]
    afterCommitId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class GetCommitInputRequestTypeDef(TypedDict):
    repositoryName: str
    commitId: str


class GetDifferencesInputRequestTypeDef(TypedDict):
    repositoryName: str
    afterCommitSpecifier: str
    beforeCommitSpecifier: NotRequired[str]
    beforePath: NotRequired[str]
    afterPath: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetFileInputRequestTypeDef(TypedDict):
    repositoryName: str
    filePath: str
    commitSpecifier: NotRequired[str]


class GetFolderInputRequestTypeDef(TypedDict):
    repositoryName: str
    folderPath: str
    commitSpecifier: NotRequired[str]


class SubModuleTypeDef(TypedDict):
    commitId: NotRequired[str]
    absolutePath: NotRequired[str]
    relativePath: NotRequired[str]


class SymbolicLinkTypeDef(TypedDict):
    blobId: NotRequired[str]
    absolutePath: NotRequired[str]
    relativePath: NotRequired[str]
    fileMode: NotRequired[FileModeTypeEnumType]


class GetMergeCommitInputRequestTypeDef(TypedDict):
    repositoryName: str
    sourceCommitSpecifier: str
    destinationCommitSpecifier: str
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]


class GetMergeConflictsInputRequestTypeDef(TypedDict):
    repositoryName: str
    destinationCommitSpecifier: str
    sourceCommitSpecifier: str
    mergeOption: MergeOptionTypeEnumType
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    maxConflictFiles: NotRequired[int]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]
    nextToken: NotRequired[str]


class GetMergeOptionsInputRequestTypeDef(TypedDict):
    repositoryName: str
    sourceCommitSpecifier: str
    destinationCommitSpecifier: str
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]


class GetPullRequestApprovalStatesInputRequestTypeDef(TypedDict):
    pullRequestId: str
    revisionId: str


class GetPullRequestInputRequestTypeDef(TypedDict):
    pullRequestId: str


class GetPullRequestOverrideStateInputRequestTypeDef(TypedDict):
    pullRequestId: str
    revisionId: str


class GetRepositoryInputRequestTypeDef(TypedDict):
    repositoryName: str


class GetRepositoryTriggersInputRequestTypeDef(TypedDict):
    repositoryName: str


class RepositoryTriggerOutputTypeDef(TypedDict):
    name: str
    destinationArn: str
    events: List[RepositoryTriggerEventEnumType]
    customData: NotRequired[str]
    branches: NotRequired[List[str]]


class ListApprovalRuleTemplatesInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListAssociatedApprovalRuleTemplatesForRepositoryInputRequestTypeDef(TypedDict):
    repositoryName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListBranchesInputRequestTypeDef(TypedDict):
    repositoryName: str
    nextToken: NotRequired[str]


class ListFileCommitHistoryRequestRequestTypeDef(TypedDict):
    repositoryName: str
    filePath: str
    commitSpecifier: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListPullRequestsInputRequestTypeDef(TypedDict):
    repositoryName: str
    authorArn: NotRequired[str]
    pullRequestStatus: NotRequired[PullRequestStatusEnumType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListRepositoriesForApprovalRuleTemplateInputRequestTypeDef(TypedDict):
    approvalRuleTemplateName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListRepositoriesInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    sortBy: NotRequired[SortByEnumType]
    order: NotRequired[OrderEnumType]


class RepositoryNameIdPairTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    repositoryId: NotRequired[str]


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    nextToken: NotRequired[str]


class MergeBranchesByFastForwardInputRequestTypeDef(TypedDict):
    repositoryName: str
    sourceCommitSpecifier: str
    destinationCommitSpecifier: str
    targetBranch: NotRequired[str]


class MergeHunkDetailTypeDef(TypedDict):
    startLine: NotRequired[int]
    endLine: NotRequired[int]
    hunkContent: NotRequired[str]


class MergeMetadataTypeDef(TypedDict):
    isMerged: NotRequired[bool]
    mergedBy: NotRequired[str]
    mergeCommitId: NotRequired[str]
    mergeOption: NotRequired[MergeOptionTypeEnumType]


class MergePullRequestByFastForwardInputRequestTypeDef(TypedDict):
    pullRequestId: str
    repositoryName: str
    sourceCommitId: NotRequired[str]


class OverridePullRequestApprovalRulesInputRequestTypeDef(TypedDict):
    pullRequestId: str
    revisionId: str
    overrideStatus: OverrideStatusType


class PostCommentReplyInputRequestTypeDef(TypedDict):
    inReplyTo: str
    content: str
    clientRequestToken: NotRequired[str]


class PullRequestCreatedEventMetadataTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    sourceCommitId: NotRequired[str]
    destinationCommitId: NotRequired[str]
    mergeBase: NotRequired[str]


class PullRequestSourceReferenceUpdatedEventMetadataTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    beforeCommitId: NotRequired[str]
    afterCommitId: NotRequired[str]
    mergeBase: NotRequired[str]


class PullRequestStatusChangedEventMetadataTypeDef(TypedDict):
    pullRequestStatus: NotRequired[PullRequestStatusEnumType]


class PutCommentReactionInputRequestTypeDef(TypedDict):
    commentId: str
    reactionValue: str


class SourceFileSpecifierTypeDef(TypedDict):
    filePath: str
    isMove: NotRequired[bool]


class ReactionValueFormatsTypeDef(TypedDict):
    emoji: NotRequired[str]
    shortCode: NotRequired[str]
    unicode: NotRequired[str]


class RepositoryTriggerExecutionFailureTypeDef(TypedDict):
    trigger: NotRequired[str]
    failureMessage: NotRequired[str]


class RepositoryTriggerTypeDef(TypedDict):
    name: str
    destinationArn: str
    events: Sequence[RepositoryTriggerEventEnumType]
    customData: NotRequired[str]
    branches: NotRequired[Sequence[str]]


class TagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateApprovalRuleTemplateContentInputRequestTypeDef(TypedDict):
    approvalRuleTemplateName: str
    newRuleContent: str
    existingRuleContentSha256: NotRequired[str]


class UpdateApprovalRuleTemplateDescriptionInputRequestTypeDef(TypedDict):
    approvalRuleTemplateName: str
    approvalRuleTemplateDescription: str


class UpdateApprovalRuleTemplateNameInputRequestTypeDef(TypedDict):
    oldApprovalRuleTemplateName: str
    newApprovalRuleTemplateName: str


class UpdateCommentInputRequestTypeDef(TypedDict):
    commentId: str
    content: str


class UpdateDefaultBranchInputRequestTypeDef(TypedDict):
    repositoryName: str
    defaultBranchName: str


class UpdatePullRequestApprovalRuleContentInputRequestTypeDef(TypedDict):
    pullRequestId: str
    approvalRuleName: str
    newRuleContent: str
    existingRuleContentSha256: NotRequired[str]


class UpdatePullRequestApprovalStateInputRequestTypeDef(TypedDict):
    pullRequestId: str
    revisionId: str
    approvalState: ApprovalStateType


class UpdatePullRequestDescriptionInputRequestTypeDef(TypedDict):
    pullRequestId: str
    description: str


class UpdatePullRequestStatusInputRequestTypeDef(TypedDict):
    pullRequestId: str
    pullRequestStatus: PullRequestStatusEnumType


class UpdatePullRequestTitleInputRequestTypeDef(TypedDict):
    pullRequestId: str
    title: str


class UpdateRepositoryDescriptionInputRequestTypeDef(TypedDict):
    repositoryName: str
    repositoryDescription: NotRequired[str]


class UpdateRepositoryEncryptionKeyInputRequestTypeDef(TypedDict):
    repositoryName: str
    kmsKeyId: str


class UpdateRepositoryNameInputRequestTypeDef(TypedDict):
    oldName: str
    newName: str


class ApprovalRuleTypeDef(TypedDict):
    approvalRuleId: NotRequired[str]
    approvalRuleName: NotRequired[str]
    approvalRuleContent: NotRequired[str]
    ruleContentSha256: NotRequired[str]
    lastModifiedDate: NotRequired[datetime]
    creationDate: NotRequired[datetime]
    lastModifiedUser: NotRequired[str]
    originApprovalRuleTemplate: NotRequired[OriginApprovalRuleTemplateTypeDef]


class BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef(TypedDict):
    associatedRepositoryNames: List[str]
    errors: List[BatchAssociateApprovalRuleTemplateWithRepositoriesErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateApprovalRuleTemplateOutputTypeDef(TypedDict):
    approvalRuleTemplate: ApprovalRuleTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUnreferencedMergeCommitOutputTypeDef(TypedDict):
    commitId: str
    treeId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteApprovalRuleTemplateOutputTypeDef(TypedDict):
    approvalRuleTemplateId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteFileOutputTypeDef(TypedDict):
    commitId: str
    blobId: str
    treeId: str
    filePath: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeletePullRequestApprovalRuleOutputTypeDef(TypedDict):
    approvalRuleId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRepositoryOutputTypeDef(TypedDict):
    repositoryId: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetApprovalRuleTemplateOutputTypeDef(TypedDict):
    approvalRuleTemplate: ApprovalRuleTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetBlobOutputTypeDef(TypedDict):
    content: bytes
    ResponseMetadata: ResponseMetadataTypeDef


class GetFileOutputTypeDef(TypedDict):
    commitId: str
    blobId: str
    filePath: str
    fileMode: FileModeTypeEnumType
    fileSize: int
    fileContent: bytes
    ResponseMetadata: ResponseMetadataTypeDef


class GetMergeCommitOutputTypeDef(TypedDict):
    sourceCommitId: str
    destinationCommitId: str
    baseCommitId: str
    mergedCommitId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetMergeOptionsOutputTypeDef(TypedDict):
    mergeOptions: List[MergeOptionTypeEnumType]
    sourceCommitId: str
    destinationCommitId: str
    baseCommitId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetPullRequestApprovalStatesOutputTypeDef(TypedDict):
    approvals: List[ApprovalTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetPullRequestOverrideStateOutputTypeDef(TypedDict):
    overridden: bool
    overrider: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListApprovalRuleTemplatesOutputTypeDef(TypedDict):
    approvalRuleTemplateNames: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef(TypedDict):
    approvalRuleTemplateNames: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListBranchesOutputTypeDef(TypedDict):
    branches: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPullRequestsOutputTypeDef(TypedDict):
    pullRequestIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListRepositoriesForApprovalRuleTemplateOutputTypeDef(TypedDict):
    repositoryNames: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class MergeBranchesByFastForwardOutputTypeDef(TypedDict):
    commitId: str
    treeId: str
    ResponseMetadata: ResponseMetadataTypeDef


class MergeBranchesBySquashOutputTypeDef(TypedDict):
    commitId: str
    treeId: str
    ResponseMetadata: ResponseMetadataTypeDef


class MergeBranchesByThreeWayOutputTypeDef(TypedDict):
    commitId: str
    treeId: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutFileOutputTypeDef(TypedDict):
    commitId: str
    blobId: str
    treeId: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutRepositoryTriggersOutputTypeDef(TypedDict):
    configurationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateApprovalRuleTemplateContentOutputTypeDef(TypedDict):
    approvalRuleTemplate: ApprovalRuleTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateApprovalRuleTemplateDescriptionOutputTypeDef(TypedDict):
    approvalRuleTemplate: ApprovalRuleTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateApprovalRuleTemplateNameOutputTypeDef(TypedDict):
    approvalRuleTemplate: ApprovalRuleTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRepositoryEncryptionKeyOutputTypeDef(TypedDict):
    repositoryId: str
    kmsKeyId: str
    originalKmsKeyId: str
    ResponseMetadata: ResponseMetadataTypeDef


class BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef(TypedDict):
    disassociatedRepositoryNames: List[str]
    errors: List[BatchDisassociateApprovalRuleTemplateFromRepositoriesErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetRepositoriesOutputTypeDef(TypedDict):
    repositories: List[RepositoryMetadataTypeDef]
    repositoriesNotFound: List[str]
    errors: List[BatchGetRepositoriesErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRepositoryOutputTypeDef(TypedDict):
    repositoryMetadata: RepositoryMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetRepositoryOutputTypeDef(TypedDict):
    repositoryMetadata: RepositoryMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DifferenceTypeDef(TypedDict):
    beforeBlob: NotRequired[BlobMetadataTypeDef]
    afterBlob: NotRequired[BlobMetadataTypeDef]
    changeType: NotRequired[ChangeTypeEnumType]


class PutFileInputRequestTypeDef(TypedDict):
    repositoryName: str
    branchName: str
    fileContent: BlobTypeDef
    filePath: str
    fileMode: NotRequired[FileModeTypeEnumType]
    parentCommitId: NotRequired[str]
    commitMessage: NotRequired[str]
    name: NotRequired[str]
    email: NotRequired[str]


class ReplaceContentEntryTypeDef(TypedDict):
    filePath: str
    replacementType: ReplacementTypeEnumType
    content: NotRequired[BlobTypeDef]
    fileMode: NotRequired[FileModeTypeEnumType]


class DeleteBranchOutputTypeDef(TypedDict):
    deletedBranch: BranchInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetBranchOutputTypeDef(TypedDict):
    branch: BranchInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteCommentContentOutputTypeDef(TypedDict):
    comment: CommentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetCommentOutputTypeDef(TypedDict):
    comment: CommentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PostCommentReplyOutputTypeDef(TypedDict):
    comment: CommentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCommentOutputTypeDef(TypedDict):
    comment: CommentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CommentsForComparedCommitTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    beforeCommitId: NotRequired[str]
    afterCommitId: NotRequired[str]
    beforeBlobId: NotRequired[str]
    afterBlobId: NotRequired[str]
    location: NotRequired[LocationTypeDef]
    comments: NotRequired[List[CommentTypeDef]]


class CommentsForPullRequestTypeDef(TypedDict):
    pullRequestId: NotRequired[str]
    repositoryName: NotRequired[str]
    beforeCommitId: NotRequired[str]
    afterCommitId: NotRequired[str]
    beforeBlobId: NotRequired[str]
    afterBlobId: NotRequired[str]
    location: NotRequired[LocationTypeDef]
    comments: NotRequired[List[CommentTypeDef]]


class PostCommentForComparedCommitInputRequestTypeDef(TypedDict):
    repositoryName: str
    afterCommitId: str
    content: str
    beforeCommitId: NotRequired[str]
    location: NotRequired[LocationTypeDef]
    clientRequestToken: NotRequired[str]


class PostCommentForComparedCommitOutputTypeDef(TypedDict):
    repositoryName: str
    beforeCommitId: str
    afterCommitId: str
    beforeBlobId: str
    afterBlobId: str
    location: LocationTypeDef
    comment: CommentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PostCommentForPullRequestInputRequestTypeDef(TypedDict):
    pullRequestId: str
    repositoryName: str
    beforeCommitId: str
    afterCommitId: str
    content: str
    location: NotRequired[LocationTypeDef]
    clientRequestToken: NotRequired[str]


class PostCommentForPullRequestOutputTypeDef(TypedDict):
    repositoryName: str
    pullRequestId: str
    beforeCommitId: str
    afterCommitId: str
    beforeBlobId: str
    afterBlobId: str
    location: LocationTypeDef
    comment: CommentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CommitTypeDef(TypedDict):
    commitId: NotRequired[str]
    treeId: NotRequired[str]
    parents: NotRequired[List[str]]
    message: NotRequired[str]
    author: NotRequired[UserInfoTypeDef]
    committer: NotRequired[UserInfoTypeDef]
    additionalData: NotRequired[str]


class ConflictMetadataTypeDef(TypedDict):
    filePath: NotRequired[str]
    fileSizes: NotRequired[FileSizesTypeDef]
    fileModes: NotRequired[FileModesTypeDef]
    objectTypes: NotRequired[ObjectTypesTypeDef]
    numberOfConflicts: NotRequired[int]
    isBinaryFile: NotRequired[IsBinaryFileTypeDef]
    contentConflict: NotRequired[bool]
    fileModeConflict: NotRequired[bool]
    objectTypeConflict: NotRequired[bool]
    mergeOperations: NotRequired[MergeOperationsTypeDef]


class CreateCommitOutputTypeDef(TypedDict):
    commitId: str
    treeId: str
    filesAdded: List[FileMetadataTypeDef]
    filesUpdated: List[FileMetadataTypeDef]
    filesDeleted: List[FileMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePullRequestInputRequestTypeDef(TypedDict):
    title: str
    targets: Sequence[TargetTypeDef]
    description: NotRequired[str]
    clientRequestToken: NotRequired[str]


class DescribePullRequestEventsInputDescribePullRequestEventsPaginateTypeDef(TypedDict):
    pullRequestId: str
    pullRequestEventType: NotRequired[PullRequestEventTypeType]
    actorArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetCommentsForComparedCommitInputGetCommentsForComparedCommitPaginateTypeDef(TypedDict):
    repositoryName: str
    afterCommitId: str
    beforeCommitId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetCommentsForPullRequestInputGetCommentsForPullRequestPaginateTypeDef(TypedDict):
    pullRequestId: str
    repositoryName: NotRequired[str]
    beforeCommitId: NotRequired[str]
    afterCommitId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetDifferencesInputGetDifferencesPaginateTypeDef(TypedDict):
    repositoryName: str
    afterCommitSpecifier: str
    beforeCommitSpecifier: NotRequired[str]
    beforePath: NotRequired[str]
    afterPath: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBranchesInputListBranchesPaginateTypeDef(TypedDict):
    repositoryName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPullRequestsInputListPullRequestsPaginateTypeDef(TypedDict):
    repositoryName: str
    authorArn: NotRequired[str]
    pullRequestStatus: NotRequired[PullRequestStatusEnumType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRepositoriesInputListRepositoriesPaginateTypeDef(TypedDict):
    sortBy: NotRequired[SortByEnumType]
    order: NotRequired[OrderEnumType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class EvaluatePullRequestApprovalRulesOutputTypeDef(TypedDict):
    evaluation: EvaluationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetFolderOutputTypeDef(TypedDict):
    commitId: str
    folderPath: str
    treeId: str
    subFolders: List[FolderTypeDef]
    files: List[FileTypeDef]
    symbolicLinks: List[SymbolicLinkTypeDef]
    subModules: List[SubModuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetRepositoryTriggersOutputTypeDef(TypedDict):
    configurationId: str
    triggers: List[RepositoryTriggerOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListRepositoriesOutputTypeDef(TypedDict):
    repositories: List[RepositoryNameIdPairTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class MergeHunkTypeDef(TypedDict):
    isConflict: NotRequired[bool]
    source: NotRequired[MergeHunkDetailTypeDef]
    destination: NotRequired[MergeHunkDetailTypeDef]
    base: NotRequired[MergeHunkDetailTypeDef]


class PullRequestMergedStateChangedEventMetadataTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    destinationReference: NotRequired[str]
    mergeMetadata: NotRequired[MergeMetadataTypeDef]


class PullRequestTargetTypeDef(TypedDict):
    repositoryName: NotRequired[str]
    sourceReference: NotRequired[str]
    destinationReference: NotRequired[str]
    destinationCommit: NotRequired[str]
    sourceCommit: NotRequired[str]
    mergeBase: NotRequired[str]
    mergeMetadata: NotRequired[MergeMetadataTypeDef]


class PutFileEntryTypeDef(TypedDict):
    filePath: str
    fileMode: NotRequired[FileModeTypeEnumType]
    fileContent: NotRequired[BlobTypeDef]
    sourceFile: NotRequired[SourceFileSpecifierTypeDef]


class ReactionForCommentTypeDef(TypedDict):
    reaction: NotRequired[ReactionValueFormatsTypeDef]
    reactionUsers: NotRequired[List[str]]
    reactionsFromDeletedUsersCount: NotRequired[int]


class TestRepositoryTriggersOutputTypeDef(TypedDict):
    successfulExecutions: List[str]
    failedExecutions: List[RepositoryTriggerExecutionFailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


RepositoryTriggerUnionTypeDef = Union[RepositoryTriggerTypeDef, RepositoryTriggerOutputTypeDef]


class TestRepositoryTriggersInputRequestTypeDef(TypedDict):
    repositoryName: str
    triggers: Sequence[RepositoryTriggerTypeDef]


class CreatePullRequestApprovalRuleOutputTypeDef(TypedDict):
    approvalRule: ApprovalRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePullRequestApprovalRuleContentOutputTypeDef(TypedDict):
    approvalRule: ApprovalRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDifferencesOutputTypeDef(TypedDict):
    differences: List[DifferenceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ConflictResolutionTypeDef(TypedDict):
    replaceContents: NotRequired[Sequence[ReplaceContentEntryTypeDef]]
    deleteFiles: NotRequired[Sequence[DeleteFileEntryTypeDef]]
    setFileModes: NotRequired[Sequence[SetFileModeEntryTypeDef]]


class GetCommentsForComparedCommitOutputTypeDef(TypedDict):
    commentsForComparedCommitData: List[CommentsForComparedCommitTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetCommentsForPullRequestOutputTypeDef(TypedDict):
    commentsForPullRequestData: List[CommentsForPullRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class BatchGetCommitsOutputTypeDef(TypedDict):
    commits: List[CommitTypeDef]
    errors: List[BatchGetCommitsErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class FileVersionTypeDef(TypedDict):
    commit: NotRequired[CommitTypeDef]
    blobId: NotRequired[str]
    path: NotRequired[str]
    revisionChildren: NotRequired[List[str]]


class GetCommitOutputTypeDef(TypedDict):
    commit: CommitTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetMergeConflictsOutputTypeDef(TypedDict):
    mergeable: bool
    destinationCommitId: str
    sourceCommitId: str
    baseCommitId: str
    conflictMetadataList: List[ConflictMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ConflictTypeDef(TypedDict):
    conflictMetadata: NotRequired[ConflictMetadataTypeDef]
    mergeHunks: NotRequired[List[MergeHunkTypeDef]]


class DescribeMergeConflictsOutputTypeDef(TypedDict):
    conflictMetadata: ConflictMetadataTypeDef
    mergeHunks: List[MergeHunkTypeDef]
    destinationCommitId: str
    sourceCommitId: str
    baseCommitId: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PullRequestEventTypeDef(TypedDict):
    pullRequestId: NotRequired[str]
    eventDate: NotRequired[datetime]
    pullRequestEventType: NotRequired[PullRequestEventTypeType]
    actorArn: NotRequired[str]
    pullRequestCreatedEventMetadata: NotRequired[PullRequestCreatedEventMetadataTypeDef]
    pullRequestStatusChangedEventMetadata: NotRequired[PullRequestStatusChangedEventMetadataTypeDef]
    pullRequestSourceReferenceUpdatedEventMetadata: NotRequired[
        PullRequestSourceReferenceUpdatedEventMetadataTypeDef
    ]
    pullRequestMergedStateChangedEventMetadata: NotRequired[
        PullRequestMergedStateChangedEventMetadataTypeDef
    ]
    approvalRuleEventMetadata: NotRequired[ApprovalRuleEventMetadataTypeDef]
    approvalStateChangedEventMetadata: NotRequired[ApprovalStateChangedEventMetadataTypeDef]
    approvalRuleOverriddenEventMetadata: NotRequired[ApprovalRuleOverriddenEventMetadataTypeDef]


class PullRequestTypeDef(TypedDict):
    pullRequestId: NotRequired[str]
    title: NotRequired[str]
    description: NotRequired[str]
    lastActivityDate: NotRequired[datetime]
    creationDate: NotRequired[datetime]
    pullRequestStatus: NotRequired[PullRequestStatusEnumType]
    authorArn: NotRequired[str]
    pullRequestTargets: NotRequired[List[PullRequestTargetTypeDef]]
    clientRequestToken: NotRequired[str]
    revisionId: NotRequired[str]
    approvalRules: NotRequired[List[ApprovalRuleTypeDef]]


class CreateCommitInputRequestTypeDef(TypedDict):
    repositoryName: str
    branchName: str
    parentCommitId: NotRequired[str]
    authorName: NotRequired[str]
    email: NotRequired[str]
    commitMessage: NotRequired[str]
    keepEmptyFolders: NotRequired[bool]
    putFiles: NotRequired[Sequence[PutFileEntryTypeDef]]
    deleteFiles: NotRequired[Sequence[DeleteFileEntryTypeDef]]
    setFileModes: NotRequired[Sequence[SetFileModeEntryTypeDef]]


class GetCommentReactionsOutputTypeDef(TypedDict):
    reactionsForComment: List[ReactionForCommentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PutRepositoryTriggersInputRequestTypeDef(TypedDict):
    repositoryName: str
    triggers: Sequence[RepositoryTriggerUnionTypeDef]


class CreateUnreferencedMergeCommitInputRequestTypeDef(TypedDict):
    repositoryName: str
    sourceCommitSpecifier: str
    destinationCommitSpecifier: str
    mergeOption: MergeOptionTypeEnumType
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]
    authorName: NotRequired[str]
    email: NotRequired[str]
    commitMessage: NotRequired[str]
    keepEmptyFolders: NotRequired[bool]
    conflictResolution: NotRequired[ConflictResolutionTypeDef]


class MergeBranchesBySquashInputRequestTypeDef(TypedDict):
    repositoryName: str
    sourceCommitSpecifier: str
    destinationCommitSpecifier: str
    targetBranch: NotRequired[str]
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]
    authorName: NotRequired[str]
    email: NotRequired[str]
    commitMessage: NotRequired[str]
    keepEmptyFolders: NotRequired[bool]
    conflictResolution: NotRequired[ConflictResolutionTypeDef]


class MergeBranchesByThreeWayInputRequestTypeDef(TypedDict):
    repositoryName: str
    sourceCommitSpecifier: str
    destinationCommitSpecifier: str
    targetBranch: NotRequired[str]
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]
    authorName: NotRequired[str]
    email: NotRequired[str]
    commitMessage: NotRequired[str]
    keepEmptyFolders: NotRequired[bool]
    conflictResolution: NotRequired[ConflictResolutionTypeDef]


class MergePullRequestBySquashInputRequestTypeDef(TypedDict):
    pullRequestId: str
    repositoryName: str
    sourceCommitId: NotRequired[str]
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]
    commitMessage: NotRequired[str]
    authorName: NotRequired[str]
    email: NotRequired[str]
    keepEmptyFolders: NotRequired[bool]
    conflictResolution: NotRequired[ConflictResolutionTypeDef]


class MergePullRequestByThreeWayInputRequestTypeDef(TypedDict):
    pullRequestId: str
    repositoryName: str
    sourceCommitId: NotRequired[str]
    conflictDetailLevel: NotRequired[ConflictDetailLevelTypeEnumType]
    conflictResolutionStrategy: NotRequired[ConflictResolutionStrategyTypeEnumType]
    commitMessage: NotRequired[str]
    authorName: NotRequired[str]
    email: NotRequired[str]
    keepEmptyFolders: NotRequired[bool]
    conflictResolution: NotRequired[ConflictResolutionTypeDef]


class ListFileCommitHistoryResponseTypeDef(TypedDict):
    revisionDag: List[FileVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class BatchDescribeMergeConflictsOutputTypeDef(TypedDict):
    conflicts: List[ConflictTypeDef]
    errors: List[BatchDescribeMergeConflictsErrorTypeDef]
    destinationCommitId: str
    sourceCommitId: str
    baseCommitId: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DescribePullRequestEventsOutputTypeDef(TypedDict):
    pullRequestEvents: List[PullRequestEventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreatePullRequestOutputTypeDef(TypedDict):
    pullRequest: PullRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetPullRequestOutputTypeDef(TypedDict):
    pullRequest: PullRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class MergePullRequestByFastForwardOutputTypeDef(TypedDict):
    pullRequest: PullRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class MergePullRequestBySquashOutputTypeDef(TypedDict):
    pullRequest: PullRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class MergePullRequestByThreeWayOutputTypeDef(TypedDict):
    pullRequest: PullRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePullRequestDescriptionOutputTypeDef(TypedDict):
    pullRequest: PullRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePullRequestStatusOutputTypeDef(TypedDict):
    pullRequest: PullRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePullRequestTitleOutputTypeDef(TypedDict):
    pullRequest: PullRequestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
