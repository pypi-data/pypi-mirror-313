"""
Type annotations for codecommit service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_codecommit.client import CodeCommitClient

    session = Session()
    client: CodeCommitClient = session.client("codecommit")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribePullRequestEventsPaginator,
    GetCommentsForComparedCommitPaginator,
    GetCommentsForPullRequestPaginator,
    GetDifferencesPaginator,
    ListBranchesPaginator,
    ListPullRequestsPaginator,
    ListRepositoriesPaginator,
)
from .type_defs import (
    AssociateApprovalRuleTemplateWithRepositoryInputRequestTypeDef,
    BatchAssociateApprovalRuleTemplateWithRepositoriesInputRequestTypeDef,
    BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef,
    BatchDescribeMergeConflictsInputRequestTypeDef,
    BatchDescribeMergeConflictsOutputTypeDef,
    BatchDisassociateApprovalRuleTemplateFromRepositoriesInputRequestTypeDef,
    BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef,
    BatchGetCommitsInputRequestTypeDef,
    BatchGetCommitsOutputTypeDef,
    BatchGetRepositoriesInputRequestTypeDef,
    BatchGetRepositoriesOutputTypeDef,
    CreateApprovalRuleTemplateInputRequestTypeDef,
    CreateApprovalRuleTemplateOutputTypeDef,
    CreateBranchInputRequestTypeDef,
    CreateCommitInputRequestTypeDef,
    CreateCommitOutputTypeDef,
    CreatePullRequestApprovalRuleInputRequestTypeDef,
    CreatePullRequestApprovalRuleOutputTypeDef,
    CreatePullRequestInputRequestTypeDef,
    CreatePullRequestOutputTypeDef,
    CreateRepositoryInputRequestTypeDef,
    CreateRepositoryOutputTypeDef,
    CreateUnreferencedMergeCommitInputRequestTypeDef,
    CreateUnreferencedMergeCommitOutputTypeDef,
    DeleteApprovalRuleTemplateInputRequestTypeDef,
    DeleteApprovalRuleTemplateOutputTypeDef,
    DeleteBranchInputRequestTypeDef,
    DeleteBranchOutputTypeDef,
    DeleteCommentContentInputRequestTypeDef,
    DeleteCommentContentOutputTypeDef,
    DeleteFileInputRequestTypeDef,
    DeleteFileOutputTypeDef,
    DeletePullRequestApprovalRuleInputRequestTypeDef,
    DeletePullRequestApprovalRuleOutputTypeDef,
    DeleteRepositoryInputRequestTypeDef,
    DeleteRepositoryOutputTypeDef,
    DescribeMergeConflictsInputRequestTypeDef,
    DescribeMergeConflictsOutputTypeDef,
    DescribePullRequestEventsInputRequestTypeDef,
    DescribePullRequestEventsOutputTypeDef,
    DisassociateApprovalRuleTemplateFromRepositoryInputRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    EvaluatePullRequestApprovalRulesInputRequestTypeDef,
    EvaluatePullRequestApprovalRulesOutputTypeDef,
    GetApprovalRuleTemplateInputRequestTypeDef,
    GetApprovalRuleTemplateOutputTypeDef,
    GetBlobInputRequestTypeDef,
    GetBlobOutputTypeDef,
    GetBranchInputRequestTypeDef,
    GetBranchOutputTypeDef,
    GetCommentInputRequestTypeDef,
    GetCommentOutputTypeDef,
    GetCommentReactionsInputRequestTypeDef,
    GetCommentReactionsOutputTypeDef,
    GetCommentsForComparedCommitInputRequestTypeDef,
    GetCommentsForComparedCommitOutputTypeDef,
    GetCommentsForPullRequestInputRequestTypeDef,
    GetCommentsForPullRequestOutputTypeDef,
    GetCommitInputRequestTypeDef,
    GetCommitOutputTypeDef,
    GetDifferencesInputRequestTypeDef,
    GetDifferencesOutputTypeDef,
    GetFileInputRequestTypeDef,
    GetFileOutputTypeDef,
    GetFolderInputRequestTypeDef,
    GetFolderOutputTypeDef,
    GetMergeCommitInputRequestTypeDef,
    GetMergeCommitOutputTypeDef,
    GetMergeConflictsInputRequestTypeDef,
    GetMergeConflictsOutputTypeDef,
    GetMergeOptionsInputRequestTypeDef,
    GetMergeOptionsOutputTypeDef,
    GetPullRequestApprovalStatesInputRequestTypeDef,
    GetPullRequestApprovalStatesOutputTypeDef,
    GetPullRequestInputRequestTypeDef,
    GetPullRequestOutputTypeDef,
    GetPullRequestOverrideStateInputRequestTypeDef,
    GetPullRequestOverrideStateOutputTypeDef,
    GetRepositoryInputRequestTypeDef,
    GetRepositoryOutputTypeDef,
    GetRepositoryTriggersInputRequestTypeDef,
    GetRepositoryTriggersOutputTypeDef,
    ListApprovalRuleTemplatesInputRequestTypeDef,
    ListApprovalRuleTemplatesOutputTypeDef,
    ListAssociatedApprovalRuleTemplatesForRepositoryInputRequestTypeDef,
    ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef,
    ListBranchesInputRequestTypeDef,
    ListBranchesOutputTypeDef,
    ListFileCommitHistoryRequestRequestTypeDef,
    ListFileCommitHistoryResponseTypeDef,
    ListPullRequestsInputRequestTypeDef,
    ListPullRequestsOutputTypeDef,
    ListRepositoriesForApprovalRuleTemplateInputRequestTypeDef,
    ListRepositoriesForApprovalRuleTemplateOutputTypeDef,
    ListRepositoriesInputRequestTypeDef,
    ListRepositoriesOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    MergeBranchesByFastForwardInputRequestTypeDef,
    MergeBranchesByFastForwardOutputTypeDef,
    MergeBranchesBySquashInputRequestTypeDef,
    MergeBranchesBySquashOutputTypeDef,
    MergeBranchesByThreeWayInputRequestTypeDef,
    MergeBranchesByThreeWayOutputTypeDef,
    MergePullRequestByFastForwardInputRequestTypeDef,
    MergePullRequestByFastForwardOutputTypeDef,
    MergePullRequestBySquashInputRequestTypeDef,
    MergePullRequestBySquashOutputTypeDef,
    MergePullRequestByThreeWayInputRequestTypeDef,
    MergePullRequestByThreeWayOutputTypeDef,
    OverridePullRequestApprovalRulesInputRequestTypeDef,
    PostCommentForComparedCommitInputRequestTypeDef,
    PostCommentForComparedCommitOutputTypeDef,
    PostCommentForPullRequestInputRequestTypeDef,
    PostCommentForPullRequestOutputTypeDef,
    PostCommentReplyInputRequestTypeDef,
    PostCommentReplyOutputTypeDef,
    PutCommentReactionInputRequestTypeDef,
    PutFileInputRequestTypeDef,
    PutFileOutputTypeDef,
    PutRepositoryTriggersInputRequestTypeDef,
    PutRepositoryTriggersOutputTypeDef,
    TagResourceInputRequestTypeDef,
    TestRepositoryTriggersInputRequestTypeDef,
    TestRepositoryTriggersOutputTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateApprovalRuleTemplateContentInputRequestTypeDef,
    UpdateApprovalRuleTemplateContentOutputTypeDef,
    UpdateApprovalRuleTemplateDescriptionInputRequestTypeDef,
    UpdateApprovalRuleTemplateDescriptionOutputTypeDef,
    UpdateApprovalRuleTemplateNameInputRequestTypeDef,
    UpdateApprovalRuleTemplateNameOutputTypeDef,
    UpdateCommentInputRequestTypeDef,
    UpdateCommentOutputTypeDef,
    UpdateDefaultBranchInputRequestTypeDef,
    UpdatePullRequestApprovalRuleContentInputRequestTypeDef,
    UpdatePullRequestApprovalRuleContentOutputTypeDef,
    UpdatePullRequestApprovalStateInputRequestTypeDef,
    UpdatePullRequestDescriptionInputRequestTypeDef,
    UpdatePullRequestDescriptionOutputTypeDef,
    UpdatePullRequestStatusInputRequestTypeDef,
    UpdatePullRequestStatusOutputTypeDef,
    UpdatePullRequestTitleInputRequestTypeDef,
    UpdatePullRequestTitleOutputTypeDef,
    UpdateRepositoryDescriptionInputRequestTypeDef,
    UpdateRepositoryEncryptionKeyInputRequestTypeDef,
    UpdateRepositoryEncryptionKeyOutputTypeDef,
    UpdateRepositoryNameInputRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("CodeCommitClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ActorDoesNotExistException: Type[BotocoreClientError]
    ApprovalRuleContentRequiredException: Type[BotocoreClientError]
    ApprovalRuleDoesNotExistException: Type[BotocoreClientError]
    ApprovalRuleNameAlreadyExistsException: Type[BotocoreClientError]
    ApprovalRuleNameRequiredException: Type[BotocoreClientError]
    ApprovalRuleTemplateContentRequiredException: Type[BotocoreClientError]
    ApprovalRuleTemplateDoesNotExistException: Type[BotocoreClientError]
    ApprovalRuleTemplateInUseException: Type[BotocoreClientError]
    ApprovalRuleTemplateNameAlreadyExistsException: Type[BotocoreClientError]
    ApprovalRuleTemplateNameRequiredException: Type[BotocoreClientError]
    ApprovalStateRequiredException: Type[BotocoreClientError]
    AuthorDoesNotExistException: Type[BotocoreClientError]
    BeforeCommitIdAndAfterCommitIdAreSameException: Type[BotocoreClientError]
    BlobIdDoesNotExistException: Type[BotocoreClientError]
    BlobIdRequiredException: Type[BotocoreClientError]
    BranchDoesNotExistException: Type[BotocoreClientError]
    BranchNameExistsException: Type[BotocoreClientError]
    BranchNameIsTagNameException: Type[BotocoreClientError]
    BranchNameRequiredException: Type[BotocoreClientError]
    CannotDeleteApprovalRuleFromTemplateException: Type[BotocoreClientError]
    CannotModifyApprovalRuleFromTemplateException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientRequestTokenRequiredException: Type[BotocoreClientError]
    CommentContentRequiredException: Type[BotocoreClientError]
    CommentContentSizeLimitExceededException: Type[BotocoreClientError]
    CommentDeletedException: Type[BotocoreClientError]
    CommentDoesNotExistException: Type[BotocoreClientError]
    CommentIdRequiredException: Type[BotocoreClientError]
    CommentNotCreatedByCallerException: Type[BotocoreClientError]
    CommitDoesNotExistException: Type[BotocoreClientError]
    CommitIdDoesNotExistException: Type[BotocoreClientError]
    CommitIdRequiredException: Type[BotocoreClientError]
    CommitIdsLimitExceededException: Type[BotocoreClientError]
    CommitIdsListRequiredException: Type[BotocoreClientError]
    CommitMessageLengthExceededException: Type[BotocoreClientError]
    CommitRequiredException: Type[BotocoreClientError]
    ConcurrentReferenceUpdateException: Type[BotocoreClientError]
    DefaultBranchCannotBeDeletedException: Type[BotocoreClientError]
    DirectoryNameConflictsWithFileNameException: Type[BotocoreClientError]
    EncryptionIntegrityChecksFailedException: Type[BotocoreClientError]
    EncryptionKeyAccessDeniedException: Type[BotocoreClientError]
    EncryptionKeyDisabledException: Type[BotocoreClientError]
    EncryptionKeyInvalidIdException: Type[BotocoreClientError]
    EncryptionKeyInvalidUsageException: Type[BotocoreClientError]
    EncryptionKeyNotFoundException: Type[BotocoreClientError]
    EncryptionKeyRequiredException: Type[BotocoreClientError]
    EncryptionKeyUnavailableException: Type[BotocoreClientError]
    FileContentAndSourceFileSpecifiedException: Type[BotocoreClientError]
    FileContentRequiredException: Type[BotocoreClientError]
    FileContentSizeLimitExceededException: Type[BotocoreClientError]
    FileDoesNotExistException: Type[BotocoreClientError]
    FileEntryRequiredException: Type[BotocoreClientError]
    FileModeRequiredException: Type[BotocoreClientError]
    FileNameConflictsWithDirectoryNameException: Type[BotocoreClientError]
    FilePathConflictsWithSubmodulePathException: Type[BotocoreClientError]
    FileTooLargeException: Type[BotocoreClientError]
    FolderContentSizeLimitExceededException: Type[BotocoreClientError]
    FolderDoesNotExistException: Type[BotocoreClientError]
    IdempotencyParameterMismatchException: Type[BotocoreClientError]
    InvalidActorArnException: Type[BotocoreClientError]
    InvalidApprovalRuleContentException: Type[BotocoreClientError]
    InvalidApprovalRuleNameException: Type[BotocoreClientError]
    InvalidApprovalRuleTemplateContentException: Type[BotocoreClientError]
    InvalidApprovalRuleTemplateDescriptionException: Type[BotocoreClientError]
    InvalidApprovalRuleTemplateNameException: Type[BotocoreClientError]
    InvalidApprovalStateException: Type[BotocoreClientError]
    InvalidAuthorArnException: Type[BotocoreClientError]
    InvalidBlobIdException: Type[BotocoreClientError]
    InvalidBranchNameException: Type[BotocoreClientError]
    InvalidClientRequestTokenException: Type[BotocoreClientError]
    InvalidCommentIdException: Type[BotocoreClientError]
    InvalidCommitException: Type[BotocoreClientError]
    InvalidCommitIdException: Type[BotocoreClientError]
    InvalidConflictDetailLevelException: Type[BotocoreClientError]
    InvalidConflictResolutionException: Type[BotocoreClientError]
    InvalidConflictResolutionStrategyException: Type[BotocoreClientError]
    InvalidContinuationTokenException: Type[BotocoreClientError]
    InvalidDeletionParameterException: Type[BotocoreClientError]
    InvalidDescriptionException: Type[BotocoreClientError]
    InvalidDestinationCommitSpecifierException: Type[BotocoreClientError]
    InvalidEmailException: Type[BotocoreClientError]
    InvalidFileLocationException: Type[BotocoreClientError]
    InvalidFileModeException: Type[BotocoreClientError]
    InvalidFilePositionException: Type[BotocoreClientError]
    InvalidMaxConflictFilesException: Type[BotocoreClientError]
    InvalidMaxMergeHunksException: Type[BotocoreClientError]
    InvalidMaxResultsException: Type[BotocoreClientError]
    InvalidMergeOptionException: Type[BotocoreClientError]
    InvalidOrderException: Type[BotocoreClientError]
    InvalidOverrideStatusException: Type[BotocoreClientError]
    InvalidParentCommitIdException: Type[BotocoreClientError]
    InvalidPathException: Type[BotocoreClientError]
    InvalidPullRequestEventTypeException: Type[BotocoreClientError]
    InvalidPullRequestIdException: Type[BotocoreClientError]
    InvalidPullRequestStatusException: Type[BotocoreClientError]
    InvalidPullRequestStatusUpdateException: Type[BotocoreClientError]
    InvalidReactionUserArnException: Type[BotocoreClientError]
    InvalidReactionValueException: Type[BotocoreClientError]
    InvalidReferenceNameException: Type[BotocoreClientError]
    InvalidRelativeFileVersionEnumException: Type[BotocoreClientError]
    InvalidReplacementContentException: Type[BotocoreClientError]
    InvalidReplacementTypeException: Type[BotocoreClientError]
    InvalidRepositoryDescriptionException: Type[BotocoreClientError]
    InvalidRepositoryNameException: Type[BotocoreClientError]
    InvalidRepositoryTriggerBranchNameException: Type[BotocoreClientError]
    InvalidRepositoryTriggerCustomDataException: Type[BotocoreClientError]
    InvalidRepositoryTriggerDestinationArnException: Type[BotocoreClientError]
    InvalidRepositoryTriggerEventsException: Type[BotocoreClientError]
    InvalidRepositoryTriggerNameException: Type[BotocoreClientError]
    InvalidRepositoryTriggerRegionException: Type[BotocoreClientError]
    InvalidResourceArnException: Type[BotocoreClientError]
    InvalidRevisionIdException: Type[BotocoreClientError]
    InvalidRuleContentSha256Exception: Type[BotocoreClientError]
    InvalidSortByException: Type[BotocoreClientError]
    InvalidSourceCommitSpecifierException: Type[BotocoreClientError]
    InvalidSystemTagUsageException: Type[BotocoreClientError]
    InvalidTagKeysListException: Type[BotocoreClientError]
    InvalidTagsMapException: Type[BotocoreClientError]
    InvalidTargetBranchException: Type[BotocoreClientError]
    InvalidTargetException: Type[BotocoreClientError]
    InvalidTargetsException: Type[BotocoreClientError]
    InvalidTitleException: Type[BotocoreClientError]
    ManualMergeRequiredException: Type[BotocoreClientError]
    MaximumBranchesExceededException: Type[BotocoreClientError]
    MaximumConflictResolutionEntriesExceededException: Type[BotocoreClientError]
    MaximumFileContentToLoadExceededException: Type[BotocoreClientError]
    MaximumFileEntriesExceededException: Type[BotocoreClientError]
    MaximumItemsToCompareExceededException: Type[BotocoreClientError]
    MaximumNumberOfApprovalsExceededException: Type[BotocoreClientError]
    MaximumOpenPullRequestsExceededException: Type[BotocoreClientError]
    MaximumRepositoryNamesExceededException: Type[BotocoreClientError]
    MaximumRepositoryTriggersExceededException: Type[BotocoreClientError]
    MaximumRuleTemplatesAssociatedWithRepositoryException: Type[BotocoreClientError]
    MergeOptionRequiredException: Type[BotocoreClientError]
    MultipleConflictResolutionEntriesException: Type[BotocoreClientError]
    MultipleRepositoriesInPullRequestException: Type[BotocoreClientError]
    NameLengthExceededException: Type[BotocoreClientError]
    NoChangeException: Type[BotocoreClientError]
    NumberOfRuleTemplatesExceededException: Type[BotocoreClientError]
    NumberOfRulesExceededException: Type[BotocoreClientError]
    OperationNotAllowedException: Type[BotocoreClientError]
    OverrideAlreadySetException: Type[BotocoreClientError]
    OverrideStatusRequiredException: Type[BotocoreClientError]
    ParentCommitDoesNotExistException: Type[BotocoreClientError]
    ParentCommitIdOutdatedException: Type[BotocoreClientError]
    ParentCommitIdRequiredException: Type[BotocoreClientError]
    PathDoesNotExistException: Type[BotocoreClientError]
    PathRequiredException: Type[BotocoreClientError]
    PullRequestAlreadyClosedException: Type[BotocoreClientError]
    PullRequestApprovalRulesNotSatisfiedException: Type[BotocoreClientError]
    PullRequestCannotBeApprovedByAuthorException: Type[BotocoreClientError]
    PullRequestDoesNotExistException: Type[BotocoreClientError]
    PullRequestIdRequiredException: Type[BotocoreClientError]
    PullRequestStatusRequiredException: Type[BotocoreClientError]
    PutFileEntryConflictException: Type[BotocoreClientError]
    ReactionLimitExceededException: Type[BotocoreClientError]
    ReactionValueRequiredException: Type[BotocoreClientError]
    ReferenceDoesNotExistException: Type[BotocoreClientError]
    ReferenceNameRequiredException: Type[BotocoreClientError]
    ReferenceTypeNotSupportedException: Type[BotocoreClientError]
    ReplacementContentRequiredException: Type[BotocoreClientError]
    ReplacementTypeRequiredException: Type[BotocoreClientError]
    RepositoryDoesNotExistException: Type[BotocoreClientError]
    RepositoryLimitExceededException: Type[BotocoreClientError]
    RepositoryNameExistsException: Type[BotocoreClientError]
    RepositoryNameRequiredException: Type[BotocoreClientError]
    RepositoryNamesRequiredException: Type[BotocoreClientError]
    RepositoryNotAssociatedWithPullRequestException: Type[BotocoreClientError]
    RepositoryTriggerBranchNameListRequiredException: Type[BotocoreClientError]
    RepositoryTriggerDestinationArnRequiredException: Type[BotocoreClientError]
    RepositoryTriggerEventsListRequiredException: Type[BotocoreClientError]
    RepositoryTriggerNameRequiredException: Type[BotocoreClientError]
    RepositoryTriggersListRequiredException: Type[BotocoreClientError]
    ResourceArnRequiredException: Type[BotocoreClientError]
    RestrictedSourceFileException: Type[BotocoreClientError]
    RevisionIdRequiredException: Type[BotocoreClientError]
    RevisionNotCurrentException: Type[BotocoreClientError]
    SameFileContentException: Type[BotocoreClientError]
    SamePathRequestException: Type[BotocoreClientError]
    SourceAndDestinationAreSameException: Type[BotocoreClientError]
    SourceFileOrContentRequiredException: Type[BotocoreClientError]
    TagKeysListRequiredException: Type[BotocoreClientError]
    TagPolicyException: Type[BotocoreClientError]
    TagsMapRequiredException: Type[BotocoreClientError]
    TargetRequiredException: Type[BotocoreClientError]
    TargetsRequiredException: Type[BotocoreClientError]
    TipOfSourceReferenceIsDifferentException: Type[BotocoreClientError]
    TipsDivergenceExceededException: Type[BotocoreClientError]
    TitleRequiredException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]

class CodeCommitClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeCommitClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#close)
        """

    def associate_approval_rule_template_with_repository(
        self, **kwargs: Unpack[AssociateApprovalRuleTemplateWithRepositoryInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates an association between an approval rule template and a specified
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/associate_approval_rule_template_with_repository.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#associate_approval_rule_template_with_repository)
        """

    def batch_associate_approval_rule_template_with_repositories(
        self,
        **kwargs: Unpack[BatchAssociateApprovalRuleTemplateWithRepositoriesInputRequestTypeDef],
    ) -> BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef:
        """
        Creates an association between an approval rule template and one or more
        specified repositories.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/batch_associate_approval_rule_template_with_repositories.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#batch_associate_approval_rule_template_with_repositories)
        """

    def batch_describe_merge_conflicts(
        self, **kwargs: Unpack[BatchDescribeMergeConflictsInputRequestTypeDef]
    ) -> BatchDescribeMergeConflictsOutputTypeDef:
        """
        Returns information about one or more merge conflicts in the attempted merge of
        two commit specifiers using the squash or three-way merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/batch_describe_merge_conflicts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#batch_describe_merge_conflicts)
        """

    def batch_disassociate_approval_rule_template_from_repositories(
        self,
        **kwargs: Unpack[BatchDisassociateApprovalRuleTemplateFromRepositoriesInputRequestTypeDef],
    ) -> BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef:
        """
        Removes the association between an approval rule template and one or more
        specified repositories.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/batch_disassociate_approval_rule_template_from_repositories.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#batch_disassociate_approval_rule_template_from_repositories)
        """

    def batch_get_commits(
        self, **kwargs: Unpack[BatchGetCommitsInputRequestTypeDef]
    ) -> BatchGetCommitsOutputTypeDef:
        """
        Returns information about the contents of one or more commits in a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/batch_get_commits.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#batch_get_commits)
        """

    def batch_get_repositories(
        self, **kwargs: Unpack[BatchGetRepositoriesInputRequestTypeDef]
    ) -> BatchGetRepositoriesOutputTypeDef:
        """
        Returns information about one or more repositories.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/batch_get_repositories.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#batch_get_repositories)
        """

    def create_approval_rule_template(
        self, **kwargs: Unpack[CreateApprovalRuleTemplateInputRequestTypeDef]
    ) -> CreateApprovalRuleTemplateOutputTypeDef:
        """
        Creates a template for approval rules that can then be associated with one or
        more repositories in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/create_approval_rule_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#create_approval_rule_template)
        """

    def create_branch(
        self, **kwargs: Unpack[CreateBranchInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a branch in a repository and points the branch to a commit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/create_branch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#create_branch)
        """

    def create_commit(
        self, **kwargs: Unpack[CreateCommitInputRequestTypeDef]
    ) -> CreateCommitOutputTypeDef:
        """
        Creates a commit for a repository on the tip of a specified branch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/create_commit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#create_commit)
        """

    def create_pull_request(
        self, **kwargs: Unpack[CreatePullRequestInputRequestTypeDef]
    ) -> CreatePullRequestOutputTypeDef:
        """
        Creates a pull request in the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/create_pull_request.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#create_pull_request)
        """

    def create_pull_request_approval_rule(
        self, **kwargs: Unpack[CreatePullRequestApprovalRuleInputRequestTypeDef]
    ) -> CreatePullRequestApprovalRuleOutputTypeDef:
        """
        Creates an approval rule for a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/create_pull_request_approval_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#create_pull_request_approval_rule)
        """

    def create_repository(
        self, **kwargs: Unpack[CreateRepositoryInputRequestTypeDef]
    ) -> CreateRepositoryOutputTypeDef:
        """
        Creates a new, empty repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/create_repository.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#create_repository)
        """

    def create_unreferenced_merge_commit(
        self, **kwargs: Unpack[CreateUnreferencedMergeCommitInputRequestTypeDef]
    ) -> CreateUnreferencedMergeCommitOutputTypeDef:
        """
        Creates an unreferenced commit that represents the result of merging two
        branches using a specified merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/create_unreferenced_merge_commit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#create_unreferenced_merge_commit)
        """

    def delete_approval_rule_template(
        self, **kwargs: Unpack[DeleteApprovalRuleTemplateInputRequestTypeDef]
    ) -> DeleteApprovalRuleTemplateOutputTypeDef:
        """
        Deletes a specified approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/delete_approval_rule_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#delete_approval_rule_template)
        """

    def delete_branch(
        self, **kwargs: Unpack[DeleteBranchInputRequestTypeDef]
    ) -> DeleteBranchOutputTypeDef:
        """
        Deletes a branch from a repository, unless that branch is the default branch
        for the repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/delete_branch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#delete_branch)
        """

    def delete_comment_content(
        self, **kwargs: Unpack[DeleteCommentContentInputRequestTypeDef]
    ) -> DeleteCommentContentOutputTypeDef:
        """
        Deletes the content of a comment made on a change, file, or commit in a
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/delete_comment_content.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#delete_comment_content)
        """

    def delete_file(
        self, **kwargs: Unpack[DeleteFileInputRequestTypeDef]
    ) -> DeleteFileOutputTypeDef:
        """
        Deletes a specified file from a specified branch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/delete_file.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#delete_file)
        """

    def delete_pull_request_approval_rule(
        self, **kwargs: Unpack[DeletePullRequestApprovalRuleInputRequestTypeDef]
    ) -> DeletePullRequestApprovalRuleOutputTypeDef:
        """
        Deletes an approval rule from a specified pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/delete_pull_request_approval_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#delete_pull_request_approval_rule)
        """

    def delete_repository(
        self, **kwargs: Unpack[DeleteRepositoryInputRequestTypeDef]
    ) -> DeleteRepositoryOutputTypeDef:
        """
        Deletes a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/delete_repository.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#delete_repository)
        """

    def describe_merge_conflicts(
        self, **kwargs: Unpack[DescribeMergeConflictsInputRequestTypeDef]
    ) -> DescribeMergeConflictsOutputTypeDef:
        """
        Returns information about one or more merge conflicts in the attempted merge of
        two commit specifiers using the squash or three-way merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/describe_merge_conflicts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#describe_merge_conflicts)
        """

    def describe_pull_request_events(
        self, **kwargs: Unpack[DescribePullRequestEventsInputRequestTypeDef]
    ) -> DescribePullRequestEventsOutputTypeDef:
        """
        Returns information about one or more pull request events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/describe_pull_request_events.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#describe_pull_request_events)
        """

    def disassociate_approval_rule_template_from_repository(
        self, **kwargs: Unpack[DisassociateApprovalRuleTemplateFromRepositoryInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the association between a template and a repository so that approval
        rules based on the template are not automatically created when pull requests
        are created in the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/disassociate_approval_rule_template_from_repository.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#disassociate_approval_rule_template_from_repository)
        """

    def evaluate_pull_request_approval_rules(
        self, **kwargs: Unpack[EvaluatePullRequestApprovalRulesInputRequestTypeDef]
    ) -> EvaluatePullRequestApprovalRulesOutputTypeDef:
        """
        Evaluates whether a pull request has met all the conditions specified in its
        associated approval rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/evaluate_pull_request_approval_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#evaluate_pull_request_approval_rules)
        """

    def get_approval_rule_template(
        self, **kwargs: Unpack[GetApprovalRuleTemplateInputRequestTypeDef]
    ) -> GetApprovalRuleTemplateOutputTypeDef:
        """
        Returns information about a specified approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_approval_rule_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_approval_rule_template)
        """

    def get_blob(self, **kwargs: Unpack[GetBlobInputRequestTypeDef]) -> GetBlobOutputTypeDef:
        """
        Returns the base-64 encoded content of an individual blob in a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_blob.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_blob)
        """

    def get_branch(self, **kwargs: Unpack[GetBranchInputRequestTypeDef]) -> GetBranchOutputTypeDef:
        """
        Returns information about a repository branch, including its name and the last
        commit ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_branch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_branch)
        """

    def get_comment(
        self, **kwargs: Unpack[GetCommentInputRequestTypeDef]
    ) -> GetCommentOutputTypeDef:
        """
        Returns the content of a comment made on a change, file, or commit in a
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_comment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_comment)
        """

    def get_comment_reactions(
        self, **kwargs: Unpack[GetCommentReactionsInputRequestTypeDef]
    ) -> GetCommentReactionsOutputTypeDef:
        """
        Returns information about reactions to a specified comment ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_comment_reactions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_comment_reactions)
        """

    def get_comments_for_compared_commit(
        self, **kwargs: Unpack[GetCommentsForComparedCommitInputRequestTypeDef]
    ) -> GetCommentsForComparedCommitOutputTypeDef:
        """
        Returns information about comments made on the comparison between two commits.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_comments_for_compared_commit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_comments_for_compared_commit)
        """

    def get_comments_for_pull_request(
        self, **kwargs: Unpack[GetCommentsForPullRequestInputRequestTypeDef]
    ) -> GetCommentsForPullRequestOutputTypeDef:
        """
        Returns comments made on a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_comments_for_pull_request.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_comments_for_pull_request)
        """

    def get_commit(self, **kwargs: Unpack[GetCommitInputRequestTypeDef]) -> GetCommitOutputTypeDef:
        """
        Returns information about a commit, including commit message and committer
        information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_commit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_commit)
        """

    def get_differences(
        self, **kwargs: Unpack[GetDifferencesInputRequestTypeDef]
    ) -> GetDifferencesOutputTypeDef:
        """
        Returns information about the differences in a valid commit specifier (such as
        a branch, tag, HEAD, commit ID, or other fully qualified reference).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_differences.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_differences)
        """

    def get_file(self, **kwargs: Unpack[GetFileInputRequestTypeDef]) -> GetFileOutputTypeDef:
        """
        Returns the base-64 encoded contents of a specified file and its metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_file.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_file)
        """

    def get_folder(self, **kwargs: Unpack[GetFolderInputRequestTypeDef]) -> GetFolderOutputTypeDef:
        """
        Returns the contents of a specified folder in a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_folder.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_folder)
        """

    def get_merge_commit(
        self, **kwargs: Unpack[GetMergeCommitInputRequestTypeDef]
    ) -> GetMergeCommitOutputTypeDef:
        """
        Returns information about a specified merge commit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_merge_commit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_merge_commit)
        """

    def get_merge_conflicts(
        self, **kwargs: Unpack[GetMergeConflictsInputRequestTypeDef]
    ) -> GetMergeConflictsOutputTypeDef:
        """
        Returns information about merge conflicts between the before and after commit
        IDs for a pull request in a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_merge_conflicts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_merge_conflicts)
        """

    def get_merge_options(
        self, **kwargs: Unpack[GetMergeOptionsInputRequestTypeDef]
    ) -> GetMergeOptionsOutputTypeDef:
        """
        Returns information about the merge options available for merging two specified
        branches.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_merge_options.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_merge_options)
        """

    def get_pull_request(
        self, **kwargs: Unpack[GetPullRequestInputRequestTypeDef]
    ) -> GetPullRequestOutputTypeDef:
        """
        Gets information about a pull request in a specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_pull_request.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_pull_request)
        """

    def get_pull_request_approval_states(
        self, **kwargs: Unpack[GetPullRequestApprovalStatesInputRequestTypeDef]
    ) -> GetPullRequestApprovalStatesOutputTypeDef:
        """
        Gets information about the approval states for a specified pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_pull_request_approval_states.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_pull_request_approval_states)
        """

    def get_pull_request_override_state(
        self, **kwargs: Unpack[GetPullRequestOverrideStateInputRequestTypeDef]
    ) -> GetPullRequestOverrideStateOutputTypeDef:
        """
        Returns information about whether approval rules have been set aside
        (overridden) for a pull request, and if so, the Amazon Resource Name (ARN) of
        the user or identity that overrode the rules and their requirements for the
        pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_pull_request_override_state.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_pull_request_override_state)
        """

    def get_repository(
        self, **kwargs: Unpack[GetRepositoryInputRequestTypeDef]
    ) -> GetRepositoryOutputTypeDef:
        """
        Returns information about a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_repository.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_repository)
        """

    def get_repository_triggers(
        self, **kwargs: Unpack[GetRepositoryTriggersInputRequestTypeDef]
    ) -> GetRepositoryTriggersOutputTypeDef:
        """
        Gets information about triggers configured for a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_repository_triggers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_repository_triggers)
        """

    def list_approval_rule_templates(
        self, **kwargs: Unpack[ListApprovalRuleTemplatesInputRequestTypeDef]
    ) -> ListApprovalRuleTemplatesOutputTypeDef:
        """
        Lists all approval rule templates in the specified Amazon Web Services Region
        in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/list_approval_rule_templates.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#list_approval_rule_templates)
        """

    def list_associated_approval_rule_templates_for_repository(
        self, **kwargs: Unpack[ListAssociatedApprovalRuleTemplatesForRepositoryInputRequestTypeDef]
    ) -> ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef:
        """
        Lists all approval rule templates that are associated with a specified
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/list_associated_approval_rule_templates_for_repository.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#list_associated_approval_rule_templates_for_repository)
        """

    def list_branches(
        self, **kwargs: Unpack[ListBranchesInputRequestTypeDef]
    ) -> ListBranchesOutputTypeDef:
        """
        Gets information about one or more branches in a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/list_branches.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#list_branches)
        """

    def list_file_commit_history(
        self, **kwargs: Unpack[ListFileCommitHistoryRequestRequestTypeDef]
    ) -> ListFileCommitHistoryResponseTypeDef:
        """
        Retrieves a list of commits and changes to a specified file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/list_file_commit_history.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#list_file_commit_history)
        """

    def list_pull_requests(
        self, **kwargs: Unpack[ListPullRequestsInputRequestTypeDef]
    ) -> ListPullRequestsOutputTypeDef:
        """
        Returns a list of pull requests for a specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/list_pull_requests.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#list_pull_requests)
        """

    def list_repositories(
        self, **kwargs: Unpack[ListRepositoriesInputRequestTypeDef]
    ) -> ListRepositoriesOutputTypeDef:
        """
        Gets information about one or more repositories.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/list_repositories.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#list_repositories)
        """

    def list_repositories_for_approval_rule_template(
        self, **kwargs: Unpack[ListRepositoriesForApprovalRuleTemplateInputRequestTypeDef]
    ) -> ListRepositoriesForApprovalRuleTemplateOutputTypeDef:
        """
        Lists all repositories associated with the specified approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/list_repositories_for_approval_rule_template.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#list_repositories_for_approval_rule_template)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Gets information about Amazon Web Servicestags for a specified Amazon Resource
        Name (ARN) in CodeCommit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#list_tags_for_resource)
        """

    def merge_branches_by_fast_forward(
        self, **kwargs: Unpack[MergeBranchesByFastForwardInputRequestTypeDef]
    ) -> MergeBranchesByFastForwardOutputTypeDef:
        """
        Merges two branches using the fast-forward merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/merge_branches_by_fast_forward.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#merge_branches_by_fast_forward)
        """

    def merge_branches_by_squash(
        self, **kwargs: Unpack[MergeBranchesBySquashInputRequestTypeDef]
    ) -> MergeBranchesBySquashOutputTypeDef:
        """
        Merges two branches using the squash merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/merge_branches_by_squash.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#merge_branches_by_squash)
        """

    def merge_branches_by_three_way(
        self, **kwargs: Unpack[MergeBranchesByThreeWayInputRequestTypeDef]
    ) -> MergeBranchesByThreeWayOutputTypeDef:
        """
        Merges two specified branches using the three-way merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/merge_branches_by_three_way.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#merge_branches_by_three_way)
        """

    def merge_pull_request_by_fast_forward(
        self, **kwargs: Unpack[MergePullRequestByFastForwardInputRequestTypeDef]
    ) -> MergePullRequestByFastForwardOutputTypeDef:
        """
        Attempts to merge the source commit of a pull request into the specified
        destination branch for that pull request at the specified commit using the
        fast-forward merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/merge_pull_request_by_fast_forward.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#merge_pull_request_by_fast_forward)
        """

    def merge_pull_request_by_squash(
        self, **kwargs: Unpack[MergePullRequestBySquashInputRequestTypeDef]
    ) -> MergePullRequestBySquashOutputTypeDef:
        """
        Attempts to merge the source commit of a pull request into the specified
        destination branch for that pull request at the specified commit using the
        squash merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/merge_pull_request_by_squash.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#merge_pull_request_by_squash)
        """

    def merge_pull_request_by_three_way(
        self, **kwargs: Unpack[MergePullRequestByThreeWayInputRequestTypeDef]
    ) -> MergePullRequestByThreeWayOutputTypeDef:
        """
        Attempts to merge the source commit of a pull request into the specified
        destination branch for that pull request at the specified commit using the
        three-way merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/merge_pull_request_by_three_way.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#merge_pull_request_by_three_way)
        """

    def override_pull_request_approval_rules(
        self, **kwargs: Unpack[OverridePullRequestApprovalRulesInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets aside (overrides) all approval rule requirements for a specified pull
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/override_pull_request_approval_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#override_pull_request_approval_rules)
        """

    def post_comment_for_compared_commit(
        self, **kwargs: Unpack[PostCommentForComparedCommitInputRequestTypeDef]
    ) -> PostCommentForComparedCommitOutputTypeDef:
        """
        Posts a comment on the comparison between two commits.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/post_comment_for_compared_commit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#post_comment_for_compared_commit)
        """

    def post_comment_for_pull_request(
        self, **kwargs: Unpack[PostCommentForPullRequestInputRequestTypeDef]
    ) -> PostCommentForPullRequestOutputTypeDef:
        """
        Posts a comment on a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/post_comment_for_pull_request.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#post_comment_for_pull_request)
        """

    def post_comment_reply(
        self, **kwargs: Unpack[PostCommentReplyInputRequestTypeDef]
    ) -> PostCommentReplyOutputTypeDef:
        """
        Posts a comment in reply to an existing comment on a comparison between commits
        or a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/post_comment_reply.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#post_comment_reply)
        """

    def put_comment_reaction(
        self, **kwargs: Unpack[PutCommentReactionInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates a reaction to a specified comment for the user whose identity
        is used to make the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/put_comment_reaction.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#put_comment_reaction)
        """

    def put_file(self, **kwargs: Unpack[PutFileInputRequestTypeDef]) -> PutFileOutputTypeDef:
        """
        Adds or updates a file in a branch in an CodeCommit repository, and generates a
        commit for the addition in the specified branch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/put_file.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#put_file)
        """

    def put_repository_triggers(
        self, **kwargs: Unpack[PutRepositoryTriggersInputRequestTypeDef]
    ) -> PutRepositoryTriggersOutputTypeDef:
        """
        Replaces all triggers for a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/put_repository_triggers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#put_repository_triggers)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates tags for a resource in CodeCommit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#tag_resource)
        """

    def test_repository_triggers(
        self, **kwargs: Unpack[TestRepositoryTriggersInputRequestTypeDef]
    ) -> TestRepositoryTriggersOutputTypeDef:
        """
        Tests the functionality of repository triggers by sending information to the
        trigger target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/test_repository_triggers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#test_repository_triggers)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags for a resource in CodeCommit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#untag_resource)
        """

    def update_approval_rule_template_content(
        self, **kwargs: Unpack[UpdateApprovalRuleTemplateContentInputRequestTypeDef]
    ) -> UpdateApprovalRuleTemplateContentOutputTypeDef:
        """
        Updates the content of an approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_approval_rule_template_content.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_approval_rule_template_content)
        """

    def update_approval_rule_template_description(
        self, **kwargs: Unpack[UpdateApprovalRuleTemplateDescriptionInputRequestTypeDef]
    ) -> UpdateApprovalRuleTemplateDescriptionOutputTypeDef:
        """
        Updates the description for a specified approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_approval_rule_template_description.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_approval_rule_template_description)
        """

    def update_approval_rule_template_name(
        self, **kwargs: Unpack[UpdateApprovalRuleTemplateNameInputRequestTypeDef]
    ) -> UpdateApprovalRuleTemplateNameOutputTypeDef:
        """
        Updates the name of a specified approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_approval_rule_template_name.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_approval_rule_template_name)
        """

    def update_comment(
        self, **kwargs: Unpack[UpdateCommentInputRequestTypeDef]
    ) -> UpdateCommentOutputTypeDef:
        """
        Replaces the contents of a comment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_comment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_comment)
        """

    def update_default_branch(
        self, **kwargs: Unpack[UpdateDefaultBranchInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets or changes the default branch name for the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_default_branch.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_default_branch)
        """

    def update_pull_request_approval_rule_content(
        self, **kwargs: Unpack[UpdatePullRequestApprovalRuleContentInputRequestTypeDef]
    ) -> UpdatePullRequestApprovalRuleContentOutputTypeDef:
        """
        Updates the structure of an approval rule created specifically for a pull
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_pull_request_approval_rule_content.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_pull_request_approval_rule_content)
        """

    def update_pull_request_approval_state(
        self, **kwargs: Unpack[UpdatePullRequestApprovalStateInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the state of a user's approval on a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_pull_request_approval_state.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_pull_request_approval_state)
        """

    def update_pull_request_description(
        self, **kwargs: Unpack[UpdatePullRequestDescriptionInputRequestTypeDef]
    ) -> UpdatePullRequestDescriptionOutputTypeDef:
        """
        Replaces the contents of the description of a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_pull_request_description.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_pull_request_description)
        """

    def update_pull_request_status(
        self, **kwargs: Unpack[UpdatePullRequestStatusInputRequestTypeDef]
    ) -> UpdatePullRequestStatusOutputTypeDef:
        """
        Updates the status of a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_pull_request_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_pull_request_status)
        """

    def update_pull_request_title(
        self, **kwargs: Unpack[UpdatePullRequestTitleInputRequestTypeDef]
    ) -> UpdatePullRequestTitleOutputTypeDef:
        """
        Replaces the title of a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_pull_request_title.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_pull_request_title)
        """

    def update_repository_description(
        self, **kwargs: Unpack[UpdateRepositoryDescriptionInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets or changes the comment or description for a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_repository_description.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_repository_description)
        """

    def update_repository_encryption_key(
        self, **kwargs: Unpack[UpdateRepositoryEncryptionKeyInputRequestTypeDef]
    ) -> UpdateRepositoryEncryptionKeyOutputTypeDef:
        """
        Updates the Key Management Service encryption key used to encrypt and decrypt a
        CodeCommit repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_repository_encryption_key.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_repository_encryption_key)
        """

    def update_repository_name(
        self, **kwargs: Unpack[UpdateRepositoryNameInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Renames a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/update_repository_name.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#update_repository_name)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_pull_request_events"]
    ) -> DescribePullRequestEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_comments_for_compared_commit"]
    ) -> GetCommentsForComparedCommitPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_comments_for_pull_request"]
    ) -> GetCommentsForPullRequestPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_differences"]) -> GetDifferencesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_branches"]) -> ListBranchesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pull_requests"]
    ) -> ListPullRequestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_repositories"]
    ) -> ListRepositoriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/client/#get_paginator)
        """
