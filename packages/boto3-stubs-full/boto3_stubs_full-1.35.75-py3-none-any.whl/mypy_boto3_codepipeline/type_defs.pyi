"""
Type annotations for codepipeline service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/type_defs/)

Usage::

    ```python
    from mypy_boto3_codepipeline.type_defs import AWSSessionCredentialsTypeDef

    data: AWSSessionCredentialsTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ActionCategoryType,
    ActionConfigurationPropertyTypeType,
    ActionExecutionStatusType,
    ActionOwnerType,
    ApprovalStatusType,
    ConditionExecutionStatusType,
    ConditionTypeType,
    ExecutionModeType,
    ExecutionTypeType,
    ExecutorTypeType,
    FailureTypeType,
    GitPullRequestEventTypeType,
    JobStatusType,
    PipelineExecutionStatusType,
    PipelineTypeType,
    ResultType,
    RetryTriggerType,
    RuleConfigurationPropertyTypeType,
    RuleExecutionStatusType,
    SourceRevisionTypeType,
    StageExecutionStatusType,
    StageRetryModeType,
    StageTransitionTypeType,
    StartTimeRangeType,
    TriggerTypeType,
    WebhookAuthenticationTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AWSSessionCredentialsTypeDef",
    "AcknowledgeJobInputRequestTypeDef",
    "AcknowledgeJobOutputTypeDef",
    "AcknowledgeThirdPartyJobInputRequestTypeDef",
    "AcknowledgeThirdPartyJobOutputTypeDef",
    "ActionConfigurationPropertyTypeDef",
    "ActionConfigurationTypeDef",
    "ActionContextTypeDef",
    "ActionDeclarationOutputTypeDef",
    "ActionDeclarationTypeDef",
    "ActionDeclarationUnionTypeDef",
    "ActionExecutionDetailTypeDef",
    "ActionExecutionFilterTypeDef",
    "ActionExecutionInputTypeDef",
    "ActionExecutionOutputTypeDef",
    "ActionExecutionResultTypeDef",
    "ActionExecutionTypeDef",
    "ActionRevisionOutputTypeDef",
    "ActionRevisionTypeDef",
    "ActionStateTypeDef",
    "ActionTypeArtifactDetailsTypeDef",
    "ActionTypeDeclarationOutputTypeDef",
    "ActionTypeDeclarationTypeDef",
    "ActionTypeExecutorOutputTypeDef",
    "ActionTypeExecutorTypeDef",
    "ActionTypeExecutorUnionTypeDef",
    "ActionTypeIdTypeDef",
    "ActionTypeIdentifierTypeDef",
    "ActionTypePermissionsOutputTypeDef",
    "ActionTypePermissionsTypeDef",
    "ActionTypePermissionsUnionTypeDef",
    "ActionTypePropertyTypeDef",
    "ActionTypeSettingsTypeDef",
    "ActionTypeTypeDef",
    "ActionTypeUrlsTypeDef",
    "ApprovalResultTypeDef",
    "ArtifactDetailTypeDef",
    "ArtifactDetailsTypeDef",
    "ArtifactLocationTypeDef",
    "ArtifactRevisionTypeDef",
    "ArtifactStoreTypeDef",
    "ArtifactTypeDef",
    "BeforeEntryConditionsOutputTypeDef",
    "BeforeEntryConditionsTypeDef",
    "BeforeEntryConditionsUnionTypeDef",
    "BlockerDeclarationTypeDef",
    "ConditionExecutionTypeDef",
    "ConditionOutputTypeDef",
    "ConditionStateTypeDef",
    "ConditionTypeDef",
    "ConditionUnionTypeDef",
    "CreateCustomActionTypeInputRequestTypeDef",
    "CreateCustomActionTypeOutputTypeDef",
    "CreatePipelineInputRequestTypeDef",
    "CreatePipelineOutputTypeDef",
    "CurrentRevisionTypeDef",
    "DeleteCustomActionTypeInputRequestTypeDef",
    "DeletePipelineInputRequestTypeDef",
    "DeleteWebhookInputRequestTypeDef",
    "DeregisterWebhookWithThirdPartyInputRequestTypeDef",
    "DisableStageTransitionInputRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnableStageTransitionInputRequestTypeDef",
    "EncryptionKeyTypeDef",
    "ErrorDetailsTypeDef",
    "ExecutionDetailsTypeDef",
    "ExecutionTriggerTypeDef",
    "ExecutorConfigurationOutputTypeDef",
    "ExecutorConfigurationTypeDef",
    "ExecutorConfigurationUnionTypeDef",
    "FailureConditionsOutputTypeDef",
    "FailureConditionsTypeDef",
    "FailureConditionsUnionTypeDef",
    "FailureDetailsTypeDef",
    "GetActionTypeInputRequestTypeDef",
    "GetActionTypeOutputTypeDef",
    "GetJobDetailsInputRequestTypeDef",
    "GetJobDetailsOutputTypeDef",
    "GetPipelineExecutionInputRequestTypeDef",
    "GetPipelineExecutionOutputTypeDef",
    "GetPipelineInputRequestTypeDef",
    "GetPipelineOutputTypeDef",
    "GetPipelineStateInputRequestTypeDef",
    "GetPipelineStateOutputTypeDef",
    "GetThirdPartyJobDetailsInputRequestTypeDef",
    "GetThirdPartyJobDetailsOutputTypeDef",
    "GitBranchFilterCriteriaOutputTypeDef",
    "GitBranchFilterCriteriaTypeDef",
    "GitBranchFilterCriteriaUnionTypeDef",
    "GitConfigurationOutputTypeDef",
    "GitConfigurationTypeDef",
    "GitConfigurationUnionTypeDef",
    "GitFilePathFilterCriteriaOutputTypeDef",
    "GitFilePathFilterCriteriaTypeDef",
    "GitFilePathFilterCriteriaUnionTypeDef",
    "GitPullRequestFilterOutputTypeDef",
    "GitPullRequestFilterTypeDef",
    "GitPullRequestFilterUnionTypeDef",
    "GitPushFilterOutputTypeDef",
    "GitPushFilterTypeDef",
    "GitPushFilterUnionTypeDef",
    "GitTagFilterCriteriaOutputTypeDef",
    "GitTagFilterCriteriaTypeDef",
    "GitTagFilterCriteriaUnionTypeDef",
    "InputArtifactTypeDef",
    "JobDataTypeDef",
    "JobDetailsTypeDef",
    "JobTypeDef",
    "JobWorkerExecutorConfigurationOutputTypeDef",
    "JobWorkerExecutorConfigurationTypeDef",
    "JobWorkerExecutorConfigurationUnionTypeDef",
    "LambdaExecutorConfigurationTypeDef",
    "LatestInPipelineExecutionFilterTypeDef",
    "ListActionExecutionsInputListActionExecutionsPaginateTypeDef",
    "ListActionExecutionsInputRequestTypeDef",
    "ListActionExecutionsOutputTypeDef",
    "ListActionTypesInputListActionTypesPaginateTypeDef",
    "ListActionTypesInputRequestTypeDef",
    "ListActionTypesOutputTypeDef",
    "ListPipelineExecutionsInputListPipelineExecutionsPaginateTypeDef",
    "ListPipelineExecutionsInputRequestTypeDef",
    "ListPipelineExecutionsOutputTypeDef",
    "ListPipelinesInputListPipelinesPaginateTypeDef",
    "ListPipelinesInputRequestTypeDef",
    "ListPipelinesOutputTypeDef",
    "ListRuleExecutionsInputListRuleExecutionsPaginateTypeDef",
    "ListRuleExecutionsInputRequestTypeDef",
    "ListRuleExecutionsOutputTypeDef",
    "ListRuleTypesInputRequestTypeDef",
    "ListRuleTypesOutputTypeDef",
    "ListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListWebhookItemTypeDef",
    "ListWebhooksInputListWebhooksPaginateTypeDef",
    "ListWebhooksInputRequestTypeDef",
    "ListWebhooksOutputTypeDef",
    "OutputArtifactOutputTypeDef",
    "OutputArtifactTypeDef",
    "OutputArtifactUnionTypeDef",
    "OverrideStageConditionInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "PipelineContextTypeDef",
    "PipelineDeclarationOutputTypeDef",
    "PipelineDeclarationTypeDef",
    "PipelineExecutionFilterTypeDef",
    "PipelineExecutionSummaryTypeDef",
    "PipelineExecutionTypeDef",
    "PipelineMetadataTypeDef",
    "PipelineRollbackMetadataTypeDef",
    "PipelineSummaryTypeDef",
    "PipelineTriggerDeclarationOutputTypeDef",
    "PipelineTriggerDeclarationTypeDef",
    "PipelineTriggerDeclarationUnionTypeDef",
    "PipelineVariableDeclarationTypeDef",
    "PipelineVariableTypeDef",
    "PollForJobsInputRequestTypeDef",
    "PollForJobsOutputTypeDef",
    "PollForThirdPartyJobsInputRequestTypeDef",
    "PollForThirdPartyJobsOutputTypeDef",
    "PutActionRevisionInputRequestTypeDef",
    "PutActionRevisionOutputTypeDef",
    "PutApprovalResultInputRequestTypeDef",
    "PutApprovalResultOutputTypeDef",
    "PutJobFailureResultInputRequestTypeDef",
    "PutJobSuccessResultInputRequestTypeDef",
    "PutThirdPartyJobFailureResultInputRequestTypeDef",
    "PutThirdPartyJobSuccessResultInputRequestTypeDef",
    "PutWebhookInputRequestTypeDef",
    "PutWebhookOutputTypeDef",
    "RegisterWebhookWithThirdPartyInputRequestTypeDef",
    "ResolvedPipelineVariableTypeDef",
    "ResponseMetadataTypeDef",
    "RetryConfigurationTypeDef",
    "RetryStageExecutionInputRequestTypeDef",
    "RetryStageExecutionOutputTypeDef",
    "RetryStageMetadataTypeDef",
    "RollbackStageInputRequestTypeDef",
    "RollbackStageOutputTypeDef",
    "RuleConfigurationPropertyTypeDef",
    "RuleDeclarationOutputTypeDef",
    "RuleDeclarationTypeDef",
    "RuleDeclarationUnionTypeDef",
    "RuleExecutionDetailTypeDef",
    "RuleExecutionFilterTypeDef",
    "RuleExecutionInputTypeDef",
    "RuleExecutionOutputTypeDef",
    "RuleExecutionResultTypeDef",
    "RuleExecutionTypeDef",
    "RuleRevisionTypeDef",
    "RuleStateTypeDef",
    "RuleTypeIdTypeDef",
    "RuleTypeSettingsTypeDef",
    "RuleTypeTypeDef",
    "S3ArtifactLocationTypeDef",
    "S3LocationTypeDef",
    "SourceRevisionOverrideTypeDef",
    "SourceRevisionTypeDef",
    "StageConditionStateTypeDef",
    "StageConditionsExecutionTypeDef",
    "StageContextTypeDef",
    "StageDeclarationOutputTypeDef",
    "StageDeclarationTypeDef",
    "StageDeclarationUnionTypeDef",
    "StageExecutionTypeDef",
    "StageStateTypeDef",
    "StartPipelineExecutionInputRequestTypeDef",
    "StartPipelineExecutionOutputTypeDef",
    "StopExecutionTriggerTypeDef",
    "StopPipelineExecutionInputRequestTypeDef",
    "StopPipelineExecutionOutputTypeDef",
    "SucceededInStageFilterTypeDef",
    "SuccessConditionsOutputTypeDef",
    "SuccessConditionsTypeDef",
    "SuccessConditionsUnionTypeDef",
    "TagResourceInputRequestTypeDef",
    "TagTypeDef",
    "ThirdPartyJobDataTypeDef",
    "ThirdPartyJobDetailsTypeDef",
    "ThirdPartyJobTypeDef",
    "TimestampTypeDef",
    "TransitionStateTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateActionTypeInputRequestTypeDef",
    "UpdatePipelineInputRequestTypeDef",
    "UpdatePipelineOutputTypeDef",
    "WebhookAuthConfigurationTypeDef",
    "WebhookDefinitionOutputTypeDef",
    "WebhookDefinitionTypeDef",
    "WebhookFilterRuleTypeDef",
)

class AWSSessionCredentialsTypeDef(TypedDict):
    accessKeyId: str
    secretAccessKey: str
    sessionToken: str

class AcknowledgeJobInputRequestTypeDef(TypedDict):
    jobId: str
    nonce: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AcknowledgeThirdPartyJobInputRequestTypeDef(TypedDict):
    jobId: str
    nonce: str
    clientToken: str

ActionConfigurationPropertyTypeDef = TypedDict(
    "ActionConfigurationPropertyTypeDef",
    {
        "name": str,
        "required": bool,
        "key": bool,
        "secret": bool,
        "queryable": NotRequired[bool],
        "description": NotRequired[str],
        "type": NotRequired[ActionConfigurationPropertyTypeType],
    },
)

class ActionConfigurationTypeDef(TypedDict):
    configuration: NotRequired[Dict[str, str]]

class ActionContextTypeDef(TypedDict):
    name: NotRequired[str]
    actionExecutionId: NotRequired[str]

class ActionTypeIdTypeDef(TypedDict):
    category: ActionCategoryType
    owner: ActionOwnerType
    provider: str
    version: str

class InputArtifactTypeDef(TypedDict):
    name: str

class OutputArtifactOutputTypeDef(TypedDict):
    name: str
    files: NotRequired[List[str]]

class LatestInPipelineExecutionFilterTypeDef(TypedDict):
    pipelineExecutionId: str
    startTimeRange: StartTimeRangeType

class ErrorDetailsTypeDef(TypedDict):
    code: NotRequired[str]
    message: NotRequired[str]

class ActionRevisionOutputTypeDef(TypedDict):
    revisionId: str
    revisionChangeId: str
    created: datetime

TimestampTypeDef = Union[datetime, str]

class ActionTypeArtifactDetailsTypeDef(TypedDict):
    minimumCount: int
    maximumCount: int

class ActionTypeIdentifierTypeDef(TypedDict):
    category: ActionCategoryType
    owner: str
    provider: str
    version: str

class ActionTypePermissionsOutputTypeDef(TypedDict):
    allowedAccounts: List[str]

class ActionTypePropertyTypeDef(TypedDict):
    name: str
    optional: bool
    key: bool
    noEcho: bool
    queryable: NotRequired[bool]
    description: NotRequired[str]

class ActionTypeUrlsTypeDef(TypedDict):
    configurationUrl: NotRequired[str]
    entityUrlTemplate: NotRequired[str]
    executionUrlTemplate: NotRequired[str]
    revisionUrlTemplate: NotRequired[str]

class ActionTypePermissionsTypeDef(TypedDict):
    allowedAccounts: Sequence[str]

class ActionTypeSettingsTypeDef(TypedDict):
    thirdPartyConfigurationUrl: NotRequired[str]
    entityUrlTemplate: NotRequired[str]
    executionUrlTemplate: NotRequired[str]
    revisionUrlTemplate: NotRequired[str]

class ArtifactDetailsTypeDef(TypedDict):
    minimumCount: int
    maximumCount: int

class ApprovalResultTypeDef(TypedDict):
    summary: str
    status: ApprovalStatusType

class S3LocationTypeDef(TypedDict):
    bucket: NotRequired[str]
    key: NotRequired[str]

class S3ArtifactLocationTypeDef(TypedDict):
    bucketName: str
    objectKey: str

class ArtifactRevisionTypeDef(TypedDict):
    name: NotRequired[str]
    revisionId: NotRequired[str]
    revisionChangeIdentifier: NotRequired[str]
    revisionSummary: NotRequired[str]
    created: NotRequired[datetime]
    revisionUrl: NotRequired[str]

EncryptionKeyTypeDef = TypedDict(
    "EncryptionKeyTypeDef",
    {
        "id": str,
        "type": Literal["KMS"],
    },
)
BlockerDeclarationTypeDef = TypedDict(
    "BlockerDeclarationTypeDef",
    {
        "name": str,
        "type": Literal["Schedule"],
    },
)

class ConditionExecutionTypeDef(TypedDict):
    status: NotRequired[ConditionExecutionStatusType]
    summary: NotRequired[str]
    lastStatusChange: NotRequired[datetime]

class TagTypeDef(TypedDict):
    key: str
    value: str

class DeleteCustomActionTypeInputRequestTypeDef(TypedDict):
    category: ActionCategoryType
    provider: str
    version: str

class DeletePipelineInputRequestTypeDef(TypedDict):
    name: str

class DeleteWebhookInputRequestTypeDef(TypedDict):
    name: str

class DeregisterWebhookWithThirdPartyInputRequestTypeDef(TypedDict):
    webhookName: NotRequired[str]

class DisableStageTransitionInputRequestTypeDef(TypedDict):
    pipelineName: str
    stageName: str
    transitionType: StageTransitionTypeType
    reason: str

class EnableStageTransitionInputRequestTypeDef(TypedDict):
    pipelineName: str
    stageName: str
    transitionType: StageTransitionTypeType

class ExecutionDetailsTypeDef(TypedDict):
    summary: NotRequired[str]
    externalExecutionId: NotRequired[str]
    percentComplete: NotRequired[int]

class ExecutionTriggerTypeDef(TypedDict):
    triggerType: NotRequired[TriggerTypeType]
    triggerDetail: NotRequired[str]

class JobWorkerExecutorConfigurationOutputTypeDef(TypedDict):
    pollingAccounts: NotRequired[List[str]]
    pollingServicePrincipals: NotRequired[List[str]]

class LambdaExecutorConfigurationTypeDef(TypedDict):
    lambdaFunctionArn: str

class RetryConfigurationTypeDef(TypedDict):
    retryMode: NotRequired[StageRetryModeType]

FailureDetailsTypeDef = TypedDict(
    "FailureDetailsTypeDef",
    {
        "type": FailureTypeType,
        "message": str,
        "externalExecutionId": NotRequired[str],
    },
)

class GetActionTypeInputRequestTypeDef(TypedDict):
    category: ActionCategoryType
    owner: str
    provider: str
    version: str

class GetJobDetailsInputRequestTypeDef(TypedDict):
    jobId: str

class GetPipelineExecutionInputRequestTypeDef(TypedDict):
    pipelineName: str
    pipelineExecutionId: str

class GetPipelineInputRequestTypeDef(TypedDict):
    name: str
    version: NotRequired[int]

class PipelineMetadataTypeDef(TypedDict):
    pipelineArn: NotRequired[str]
    created: NotRequired[datetime]
    updated: NotRequired[datetime]
    pollingDisabledAt: NotRequired[datetime]

class GetPipelineStateInputRequestTypeDef(TypedDict):
    name: str

class GetThirdPartyJobDetailsInputRequestTypeDef(TypedDict):
    jobId: str
    clientToken: str

class GitBranchFilterCriteriaOutputTypeDef(TypedDict):
    includes: NotRequired[List[str]]
    excludes: NotRequired[List[str]]

class GitBranchFilterCriteriaTypeDef(TypedDict):
    includes: NotRequired[Sequence[str]]
    excludes: NotRequired[Sequence[str]]

class GitFilePathFilterCriteriaOutputTypeDef(TypedDict):
    includes: NotRequired[List[str]]
    excludes: NotRequired[List[str]]

class GitFilePathFilterCriteriaTypeDef(TypedDict):
    includes: NotRequired[Sequence[str]]
    excludes: NotRequired[Sequence[str]]

class GitTagFilterCriteriaOutputTypeDef(TypedDict):
    includes: NotRequired[List[str]]
    excludes: NotRequired[List[str]]

class GitTagFilterCriteriaTypeDef(TypedDict):
    includes: NotRequired[Sequence[str]]
    excludes: NotRequired[Sequence[str]]

class JobWorkerExecutorConfigurationTypeDef(TypedDict):
    pollingAccounts: NotRequired[Sequence[str]]
    pollingServicePrincipals: NotRequired[Sequence[str]]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListActionTypesInputRequestTypeDef(TypedDict):
    actionOwnerFilter: NotRequired[ActionOwnerType]
    nextToken: NotRequired[str]
    regionFilter: NotRequired[str]

class ListPipelinesInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class PipelineSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    version: NotRequired[int]
    pipelineType: NotRequired[PipelineTypeType]
    executionMode: NotRequired[ExecutionModeType]
    created: NotRequired[datetime]
    updated: NotRequired[datetime]

class ListRuleTypesInputRequestTypeDef(TypedDict):
    ruleOwnerFilter: NotRequired[Literal["AWS"]]
    regionFilter: NotRequired[str]

class ListTagsForResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListWebhooksInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class OutputArtifactTypeDef(TypedDict):
    name: str
    files: NotRequired[Sequence[str]]

class OverrideStageConditionInputRequestTypeDef(TypedDict):
    pipelineName: str
    stageName: str
    pipelineExecutionId: str
    conditionType: ConditionTypeType

class StageContextTypeDef(TypedDict):
    name: NotRequired[str]

class PipelineVariableDeclarationTypeDef(TypedDict):
    name: str
    defaultValue: NotRequired[str]
    description: NotRequired[str]

class SucceededInStageFilterTypeDef(TypedDict):
    stageName: NotRequired[str]

class PipelineRollbackMetadataTypeDef(TypedDict):
    rollbackTargetPipelineExecutionId: NotRequired[str]

class SourceRevisionTypeDef(TypedDict):
    actionName: str
    revisionId: NotRequired[str]
    revisionSummary: NotRequired[str]
    revisionUrl: NotRequired[str]

class StopExecutionTriggerTypeDef(TypedDict):
    reason: NotRequired[str]

class ResolvedPipelineVariableTypeDef(TypedDict):
    name: NotRequired[str]
    resolvedValue: NotRequired[str]

class PipelineVariableTypeDef(TypedDict):
    name: str
    value: str

class ThirdPartyJobTypeDef(TypedDict):
    clientId: NotRequired[str]
    jobId: NotRequired[str]

class RegisterWebhookWithThirdPartyInputRequestTypeDef(TypedDict):
    webhookName: NotRequired[str]

class RetryStageExecutionInputRequestTypeDef(TypedDict):
    pipelineName: str
    stageName: str
    pipelineExecutionId: str
    retryMode: StageRetryModeType

class RetryStageMetadataTypeDef(TypedDict):
    autoStageRetryAttempt: NotRequired[int]
    manualStageRetryAttempt: NotRequired[int]
    latestRetryTrigger: NotRequired[RetryTriggerType]

class RollbackStageInputRequestTypeDef(TypedDict):
    pipelineName: str
    stageName: str
    targetPipelineExecutionId: str

RuleConfigurationPropertyTypeDef = TypedDict(
    "RuleConfigurationPropertyTypeDef",
    {
        "name": str,
        "required": bool,
        "key": bool,
        "secret": bool,
        "queryable": NotRequired[bool],
        "description": NotRequired[str],
        "type": NotRequired[RuleConfigurationPropertyTypeType],
    },
)

class RuleTypeIdTypeDef(TypedDict):
    category: Literal["Rule"]
    provider: str
    owner: NotRequired[Literal["AWS"]]
    version: NotRequired[str]

class RuleRevisionTypeDef(TypedDict):
    revisionId: str
    revisionChangeId: str
    created: datetime

class RuleTypeSettingsTypeDef(TypedDict):
    thirdPartyConfigurationUrl: NotRequired[str]
    entityUrlTemplate: NotRequired[str]
    executionUrlTemplate: NotRequired[str]
    revisionUrlTemplate: NotRequired[str]

class SourceRevisionOverrideTypeDef(TypedDict):
    actionName: str
    revisionType: SourceRevisionTypeType
    revisionValue: str

class StageConditionsExecutionTypeDef(TypedDict):
    status: NotRequired[ConditionExecutionStatusType]
    summary: NotRequired[str]

StageExecutionTypeDef = TypedDict(
    "StageExecutionTypeDef",
    {
        "pipelineExecutionId": str,
        "status": StageExecutionStatusType,
        "type": NotRequired[ExecutionTypeType],
    },
)

class TransitionStateTypeDef(TypedDict):
    enabled: NotRequired[bool]
    lastChangedBy: NotRequired[str]
    lastChangedAt: NotRequired[datetime]
    disabledReason: NotRequired[str]

class StopPipelineExecutionInputRequestTypeDef(TypedDict):
    pipelineName: str
    pipelineExecutionId: str
    abandon: NotRequired[bool]
    reason: NotRequired[str]

class UntagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class WebhookAuthConfigurationTypeDef(TypedDict):
    AllowedIPRange: NotRequired[str]
    SecretToken: NotRequired[str]

class WebhookFilterRuleTypeDef(TypedDict):
    jsonPath: str
    matchEquals: NotRequired[str]

class AcknowledgeJobOutputTypeDef(TypedDict):
    status: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class AcknowledgeThirdPartyJobOutputTypeDef(TypedDict):
    status: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class PutActionRevisionOutputTypeDef(TypedDict):
    newRevision: bool
    pipelineExecutionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class PutApprovalResultOutputTypeDef(TypedDict):
    approvedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class RetryStageExecutionOutputTypeDef(TypedDict):
    pipelineExecutionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class RollbackStageOutputTypeDef(TypedDict):
    pipelineExecutionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartPipelineExecutionOutputTypeDef(TypedDict):
    pipelineExecutionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StopPipelineExecutionOutputTypeDef(TypedDict):
    pipelineExecutionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class PollForJobsInputRequestTypeDef(TypedDict):
    actionTypeId: ActionTypeIdTypeDef
    maxBatchSize: NotRequired[int]
    queryParam: NotRequired[Mapping[str, str]]

class PollForThirdPartyJobsInputRequestTypeDef(TypedDict):
    actionTypeId: ActionTypeIdTypeDef
    maxBatchSize: NotRequired[int]

class ActionDeclarationOutputTypeDef(TypedDict):
    name: str
    actionTypeId: ActionTypeIdTypeDef
    runOrder: NotRequired[int]
    configuration: NotRequired[Dict[str, str]]
    commands: NotRequired[List[str]]
    outputArtifacts: NotRequired[List[OutputArtifactOutputTypeDef]]
    inputArtifacts: NotRequired[List[InputArtifactTypeDef]]
    outputVariables: NotRequired[List[str]]
    roleArn: NotRequired[str]
    region: NotRequired[str]
    namespace: NotRequired[str]
    timeoutInMinutes: NotRequired[int]

class ActionExecutionFilterTypeDef(TypedDict):
    pipelineExecutionId: NotRequired[str]
    latestInPipelineExecution: NotRequired[LatestInPipelineExecutionFilterTypeDef]

class RuleExecutionFilterTypeDef(TypedDict):
    pipelineExecutionId: NotRequired[str]
    latestInPipelineExecution: NotRequired[LatestInPipelineExecutionFilterTypeDef]

class ActionExecutionResultTypeDef(TypedDict):
    externalExecutionId: NotRequired[str]
    externalExecutionSummary: NotRequired[str]
    externalExecutionUrl: NotRequired[str]
    errorDetails: NotRequired[ErrorDetailsTypeDef]
    logStreamARN: NotRequired[str]

class ActionExecutionTypeDef(TypedDict):
    actionExecutionId: NotRequired[str]
    status: NotRequired[ActionExecutionStatusType]
    summary: NotRequired[str]
    lastStatusChange: NotRequired[datetime]
    token: NotRequired[str]
    lastUpdatedBy: NotRequired[str]
    externalExecutionId: NotRequired[str]
    externalExecutionUrl: NotRequired[str]
    percentComplete: NotRequired[int]
    errorDetails: NotRequired[ErrorDetailsTypeDef]
    logStreamARN: NotRequired[str]

class RuleExecutionResultTypeDef(TypedDict):
    externalExecutionId: NotRequired[str]
    externalExecutionSummary: NotRequired[str]
    externalExecutionUrl: NotRequired[str]
    errorDetails: NotRequired[ErrorDetailsTypeDef]

class RuleExecutionTypeDef(TypedDict):
    ruleExecutionId: NotRequired[str]
    status: NotRequired[RuleExecutionStatusType]
    summary: NotRequired[str]
    lastStatusChange: NotRequired[datetime]
    token: NotRequired[str]
    lastUpdatedBy: NotRequired[str]
    externalExecutionId: NotRequired[str]
    externalExecutionUrl: NotRequired[str]
    errorDetails: NotRequired[ErrorDetailsTypeDef]

class ActionRevisionTypeDef(TypedDict):
    revisionId: str
    revisionChangeId: str
    created: TimestampTypeDef

class CurrentRevisionTypeDef(TypedDict):
    revision: str
    changeIdentifier: str
    created: NotRequired[TimestampTypeDef]
    revisionSummary: NotRequired[str]

ActionTypePermissionsUnionTypeDef = Union[
    ActionTypePermissionsTypeDef, ActionTypePermissionsOutputTypeDef
]
ActionTypeTypeDef = TypedDict(
    "ActionTypeTypeDef",
    {
        "id": ActionTypeIdTypeDef,
        "inputArtifactDetails": ArtifactDetailsTypeDef,
        "outputArtifactDetails": ArtifactDetailsTypeDef,
        "settings": NotRequired[ActionTypeSettingsTypeDef],
        "actionConfigurationProperties": NotRequired[List[ActionConfigurationPropertyTypeDef]],
    },
)

class PutApprovalResultInputRequestTypeDef(TypedDict):
    pipelineName: str
    stageName: str
    actionName: str
    result: ApprovalResultTypeDef
    token: str

class ArtifactDetailTypeDef(TypedDict):
    name: NotRequired[str]
    s3location: NotRequired[S3LocationTypeDef]

ArtifactLocationTypeDef = TypedDict(
    "ArtifactLocationTypeDef",
    {
        "type": NotRequired[Literal["S3"]],
        "s3Location": NotRequired[S3ArtifactLocationTypeDef],
    },
)
ArtifactStoreTypeDef = TypedDict(
    "ArtifactStoreTypeDef",
    {
        "type": Literal["S3"],
        "location": str,
        "encryptionKey": NotRequired[EncryptionKeyTypeDef],
    },
)

class CreateCustomActionTypeInputRequestTypeDef(TypedDict):
    category: ActionCategoryType
    provider: str
    version: str
    inputArtifactDetails: ArtifactDetailsTypeDef
    outputArtifactDetails: ArtifactDetailsTypeDef
    settings: NotRequired[ActionTypeSettingsTypeDef]
    configurationProperties: NotRequired[Sequence[ActionConfigurationPropertyTypeDef]]
    tags: NotRequired[Sequence[TagTypeDef]]

class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class TagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]

class ExecutorConfigurationOutputTypeDef(TypedDict):
    lambdaExecutorConfiguration: NotRequired[LambdaExecutorConfigurationTypeDef]
    jobWorkerExecutorConfiguration: NotRequired[JobWorkerExecutorConfigurationOutputTypeDef]

class PutJobFailureResultInputRequestTypeDef(TypedDict):
    jobId: str
    failureDetails: FailureDetailsTypeDef

class PutThirdPartyJobFailureResultInputRequestTypeDef(TypedDict):
    jobId: str
    clientToken: str
    failureDetails: FailureDetailsTypeDef

GitBranchFilterCriteriaUnionTypeDef = Union[
    GitBranchFilterCriteriaTypeDef, GitBranchFilterCriteriaOutputTypeDef
]

class GitPullRequestFilterOutputTypeDef(TypedDict):
    events: NotRequired[List[GitPullRequestEventTypeType]]
    branches: NotRequired[GitBranchFilterCriteriaOutputTypeDef]
    filePaths: NotRequired[GitFilePathFilterCriteriaOutputTypeDef]

GitFilePathFilterCriteriaUnionTypeDef = Union[
    GitFilePathFilterCriteriaTypeDef, GitFilePathFilterCriteriaOutputTypeDef
]

class GitPushFilterOutputTypeDef(TypedDict):
    tags: NotRequired[GitTagFilterCriteriaOutputTypeDef]
    branches: NotRequired[GitBranchFilterCriteriaOutputTypeDef]
    filePaths: NotRequired[GitFilePathFilterCriteriaOutputTypeDef]

GitTagFilterCriteriaUnionTypeDef = Union[
    GitTagFilterCriteriaTypeDef, GitTagFilterCriteriaOutputTypeDef
]
JobWorkerExecutorConfigurationUnionTypeDef = Union[
    JobWorkerExecutorConfigurationTypeDef, JobWorkerExecutorConfigurationOutputTypeDef
]

class ListActionTypesInputListActionTypesPaginateTypeDef(TypedDict):
    actionOwnerFilter: NotRequired[ActionOwnerType]
    regionFilter: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPipelinesInputListPipelinesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTagsForResourceInputListTagsForResourcePaginateTypeDef(TypedDict):
    resourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWebhooksInputListWebhooksPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPipelinesOutputTypeDef(TypedDict):
    pipelines: List[PipelineSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

OutputArtifactUnionTypeDef = Union[OutputArtifactTypeDef, OutputArtifactOutputTypeDef]

class PipelineContextTypeDef(TypedDict):
    pipelineName: NotRequired[str]
    stage: NotRequired[StageContextTypeDef]
    action: NotRequired[ActionContextTypeDef]
    pipelineArn: NotRequired[str]
    pipelineExecutionId: NotRequired[str]

class PipelineExecutionFilterTypeDef(TypedDict):
    succeededInStage: NotRequired[SucceededInStageFilterTypeDef]

class PipelineExecutionSummaryTypeDef(TypedDict):
    pipelineExecutionId: NotRequired[str]
    status: NotRequired[PipelineExecutionStatusType]
    statusSummary: NotRequired[str]
    startTime: NotRequired[datetime]
    lastUpdateTime: NotRequired[datetime]
    sourceRevisions: NotRequired[List[SourceRevisionTypeDef]]
    trigger: NotRequired[ExecutionTriggerTypeDef]
    stopTrigger: NotRequired[StopExecutionTriggerTypeDef]
    executionMode: NotRequired[ExecutionModeType]
    executionType: NotRequired[ExecutionTypeType]
    rollbackMetadata: NotRequired[PipelineRollbackMetadataTypeDef]

class PipelineExecutionTypeDef(TypedDict):
    pipelineName: NotRequired[str]
    pipelineVersion: NotRequired[int]
    pipelineExecutionId: NotRequired[str]
    status: NotRequired[PipelineExecutionStatusType]
    statusSummary: NotRequired[str]
    artifactRevisions: NotRequired[List[ArtifactRevisionTypeDef]]
    variables: NotRequired[List[ResolvedPipelineVariableTypeDef]]
    trigger: NotRequired[ExecutionTriggerTypeDef]
    executionMode: NotRequired[ExecutionModeType]
    executionType: NotRequired[ExecutionTypeType]
    rollbackMetadata: NotRequired[PipelineRollbackMetadataTypeDef]

class PollForThirdPartyJobsOutputTypeDef(TypedDict):
    jobs: List[ThirdPartyJobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class RuleDeclarationOutputTypeDef(TypedDict):
    name: str
    ruleTypeId: RuleTypeIdTypeDef
    configuration: NotRequired[Dict[str, str]]
    inputArtifacts: NotRequired[List[InputArtifactTypeDef]]
    roleArn: NotRequired[str]
    region: NotRequired[str]
    timeoutInMinutes: NotRequired[int]

class RuleDeclarationTypeDef(TypedDict):
    name: str
    ruleTypeId: RuleTypeIdTypeDef
    configuration: NotRequired[Mapping[str, str]]
    inputArtifacts: NotRequired[Sequence[InputArtifactTypeDef]]
    roleArn: NotRequired[str]
    region: NotRequired[str]
    timeoutInMinutes: NotRequired[int]

RuleTypeTypeDef = TypedDict(
    "RuleTypeTypeDef",
    {
        "id": RuleTypeIdTypeDef,
        "inputArtifactDetails": ArtifactDetailsTypeDef,
        "settings": NotRequired[RuleTypeSettingsTypeDef],
        "ruleConfigurationProperties": NotRequired[List[RuleConfigurationPropertyTypeDef]],
    },
)

class StartPipelineExecutionInputRequestTypeDef(TypedDict):
    name: str
    variables: NotRequired[Sequence[PipelineVariableTypeDef]]
    clientRequestToken: NotRequired[str]
    sourceRevisions: NotRequired[Sequence[SourceRevisionOverrideTypeDef]]

class WebhookDefinitionOutputTypeDef(TypedDict):
    name: str
    targetPipeline: str
    targetAction: str
    filters: List[WebhookFilterRuleTypeDef]
    authentication: WebhookAuthenticationTypeType
    authenticationConfiguration: WebhookAuthConfigurationTypeDef

class WebhookDefinitionTypeDef(TypedDict):
    name: str
    targetPipeline: str
    targetAction: str
    filters: Sequence[WebhookFilterRuleTypeDef]
    authentication: WebhookAuthenticationTypeType
    authenticationConfiguration: WebhookAuthConfigurationTypeDef

ListActionExecutionsInputListActionExecutionsPaginateTypeDef = TypedDict(
    "ListActionExecutionsInputListActionExecutionsPaginateTypeDef",
    {
        "pipelineName": str,
        "filter": NotRequired[ActionExecutionFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListActionExecutionsInputRequestTypeDef = TypedDict(
    "ListActionExecutionsInputRequestTypeDef",
    {
        "pipelineName": str,
        "filter": NotRequired[ActionExecutionFilterTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListRuleExecutionsInputListRuleExecutionsPaginateTypeDef = TypedDict(
    "ListRuleExecutionsInputListRuleExecutionsPaginateTypeDef",
    {
        "pipelineName": str,
        "filter": NotRequired[RuleExecutionFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListRuleExecutionsInputRequestTypeDef = TypedDict(
    "ListRuleExecutionsInputRequestTypeDef",
    {
        "pipelineName": str,
        "filter": NotRequired[RuleExecutionFilterTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

class ActionStateTypeDef(TypedDict):
    actionName: NotRequired[str]
    currentRevision: NotRequired[ActionRevisionOutputTypeDef]
    latestExecution: NotRequired[ActionExecutionTypeDef]
    entityUrl: NotRequired[str]
    revisionUrl: NotRequired[str]

class RuleExecutionOutputTypeDef(TypedDict):
    executionResult: NotRequired[RuleExecutionResultTypeDef]

class RuleStateTypeDef(TypedDict):
    ruleName: NotRequired[str]
    currentRevision: NotRequired[RuleRevisionTypeDef]
    latestExecution: NotRequired[RuleExecutionTypeDef]
    entityUrl: NotRequired[str]
    revisionUrl: NotRequired[str]

class PutActionRevisionInputRequestTypeDef(TypedDict):
    pipelineName: str
    stageName: str
    actionName: str
    actionRevision: ActionRevisionTypeDef

class PutJobSuccessResultInputRequestTypeDef(TypedDict):
    jobId: str
    currentRevision: NotRequired[CurrentRevisionTypeDef]
    continuationToken: NotRequired[str]
    executionDetails: NotRequired[ExecutionDetailsTypeDef]
    outputVariables: NotRequired[Mapping[str, str]]

class PutThirdPartyJobSuccessResultInputRequestTypeDef(TypedDict):
    jobId: str
    clientToken: str
    currentRevision: NotRequired[CurrentRevisionTypeDef]
    continuationToken: NotRequired[str]
    executionDetails: NotRequired[ExecutionDetailsTypeDef]

class CreateCustomActionTypeOutputTypeDef(TypedDict):
    actionType: ActionTypeTypeDef
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListActionTypesOutputTypeDef(TypedDict):
    actionTypes: List[ActionTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ActionExecutionInputTypeDef(TypedDict):
    actionTypeId: NotRequired[ActionTypeIdTypeDef]
    configuration: NotRequired[Dict[str, str]]
    resolvedConfiguration: NotRequired[Dict[str, str]]
    roleArn: NotRequired[str]
    region: NotRequired[str]
    inputArtifacts: NotRequired[List[ArtifactDetailTypeDef]]
    namespace: NotRequired[str]

class ActionExecutionOutputTypeDef(TypedDict):
    outputArtifacts: NotRequired[List[ArtifactDetailTypeDef]]
    executionResult: NotRequired[ActionExecutionResultTypeDef]
    outputVariables: NotRequired[Dict[str, str]]

class RuleExecutionInputTypeDef(TypedDict):
    ruleTypeId: NotRequired[RuleTypeIdTypeDef]
    configuration: NotRequired[Dict[str, str]]
    resolvedConfiguration: NotRequired[Dict[str, str]]
    roleArn: NotRequired[str]
    region: NotRequired[str]
    inputArtifacts: NotRequired[List[ArtifactDetailTypeDef]]

class ArtifactTypeDef(TypedDict):
    name: NotRequired[str]
    revision: NotRequired[str]
    location: NotRequired[ArtifactLocationTypeDef]

ActionTypeExecutorOutputTypeDef = TypedDict(
    "ActionTypeExecutorOutputTypeDef",
    {
        "configuration": ExecutorConfigurationOutputTypeDef,
        "type": ExecutorTypeType,
        "policyStatementsTemplate": NotRequired[str],
        "jobTimeout": NotRequired[int],
    },
)

class GitPullRequestFilterTypeDef(TypedDict):
    events: NotRequired[Sequence[GitPullRequestEventTypeType]]
    branches: NotRequired[GitBranchFilterCriteriaUnionTypeDef]
    filePaths: NotRequired[GitFilePathFilterCriteriaUnionTypeDef]

class GitConfigurationOutputTypeDef(TypedDict):
    sourceActionName: str
    push: NotRequired[List[GitPushFilterOutputTypeDef]]
    pullRequest: NotRequired[List[GitPullRequestFilterOutputTypeDef]]

class GitPushFilterTypeDef(TypedDict):
    tags: NotRequired[GitTagFilterCriteriaUnionTypeDef]
    branches: NotRequired[GitBranchFilterCriteriaUnionTypeDef]
    filePaths: NotRequired[GitFilePathFilterCriteriaUnionTypeDef]

class ExecutorConfigurationTypeDef(TypedDict):
    lambdaExecutorConfiguration: NotRequired[LambdaExecutorConfigurationTypeDef]
    jobWorkerExecutorConfiguration: NotRequired[JobWorkerExecutorConfigurationUnionTypeDef]

class ActionDeclarationTypeDef(TypedDict):
    name: str
    actionTypeId: ActionTypeIdTypeDef
    runOrder: NotRequired[int]
    configuration: NotRequired[Mapping[str, str]]
    commands: NotRequired[Sequence[str]]
    outputArtifacts: NotRequired[Sequence[OutputArtifactUnionTypeDef]]
    inputArtifacts: NotRequired[Sequence[InputArtifactTypeDef]]
    outputVariables: NotRequired[Sequence[str]]
    roleArn: NotRequired[str]
    region: NotRequired[str]
    namespace: NotRequired[str]
    timeoutInMinutes: NotRequired[int]

ListPipelineExecutionsInputListPipelineExecutionsPaginateTypeDef = TypedDict(
    "ListPipelineExecutionsInputListPipelineExecutionsPaginateTypeDef",
    {
        "pipelineName": str,
        "filter": NotRequired[PipelineExecutionFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListPipelineExecutionsInputRequestTypeDef = TypedDict(
    "ListPipelineExecutionsInputRequestTypeDef",
    {
        "pipelineName": str,
        "maxResults": NotRequired[int],
        "filter": NotRequired[PipelineExecutionFilterTypeDef],
        "nextToken": NotRequired[str],
    },
)

class ListPipelineExecutionsOutputTypeDef(TypedDict):
    pipelineExecutionSummaries: List[PipelineExecutionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetPipelineExecutionOutputTypeDef(TypedDict):
    pipelineExecution: PipelineExecutionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ConditionOutputTypeDef(TypedDict):
    result: NotRequired[ResultType]
    rules: NotRequired[List[RuleDeclarationOutputTypeDef]]

RuleDeclarationUnionTypeDef = Union[RuleDeclarationTypeDef, RuleDeclarationOutputTypeDef]

class ListRuleTypesOutputTypeDef(TypedDict):
    ruleTypes: List[RuleTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListWebhookItemTypeDef(TypedDict):
    definition: WebhookDefinitionOutputTypeDef
    url: str
    errorMessage: NotRequired[str]
    errorCode: NotRequired[str]
    lastTriggered: NotRequired[datetime]
    arn: NotRequired[str]
    tags: NotRequired[List[TagTypeDef]]

class PutWebhookInputRequestTypeDef(TypedDict):
    webhook: WebhookDefinitionTypeDef
    tags: NotRequired[Sequence[TagTypeDef]]

class ConditionStateTypeDef(TypedDict):
    latestExecution: NotRequired[ConditionExecutionTypeDef]
    ruleStates: NotRequired[List[RuleStateTypeDef]]

ActionExecutionDetailTypeDef = TypedDict(
    "ActionExecutionDetailTypeDef",
    {
        "pipelineExecutionId": NotRequired[str],
        "actionExecutionId": NotRequired[str],
        "pipelineVersion": NotRequired[int],
        "stageName": NotRequired[str],
        "actionName": NotRequired[str],
        "startTime": NotRequired[datetime],
        "lastUpdateTime": NotRequired[datetime],
        "updatedBy": NotRequired[str],
        "status": NotRequired[ActionExecutionStatusType],
        "input": NotRequired[ActionExecutionInputTypeDef],
        "output": NotRequired[ActionExecutionOutputTypeDef],
    },
)
RuleExecutionDetailTypeDef = TypedDict(
    "RuleExecutionDetailTypeDef",
    {
        "pipelineExecutionId": NotRequired[str],
        "ruleExecutionId": NotRequired[str],
        "pipelineVersion": NotRequired[int],
        "stageName": NotRequired[str],
        "ruleName": NotRequired[str],
        "startTime": NotRequired[datetime],
        "lastUpdateTime": NotRequired[datetime],
        "updatedBy": NotRequired[str],
        "status": NotRequired[RuleExecutionStatusType],
        "input": NotRequired[RuleExecutionInputTypeDef],
        "output": NotRequired[RuleExecutionOutputTypeDef],
    },
)

class JobDataTypeDef(TypedDict):
    actionTypeId: NotRequired[ActionTypeIdTypeDef]
    actionConfiguration: NotRequired[ActionConfigurationTypeDef]
    pipelineContext: NotRequired[PipelineContextTypeDef]
    inputArtifacts: NotRequired[List[ArtifactTypeDef]]
    outputArtifacts: NotRequired[List[ArtifactTypeDef]]
    artifactCredentials: NotRequired[AWSSessionCredentialsTypeDef]
    continuationToken: NotRequired[str]
    encryptionKey: NotRequired[EncryptionKeyTypeDef]

class ThirdPartyJobDataTypeDef(TypedDict):
    actionTypeId: NotRequired[ActionTypeIdTypeDef]
    actionConfiguration: NotRequired[ActionConfigurationTypeDef]
    pipelineContext: NotRequired[PipelineContextTypeDef]
    inputArtifacts: NotRequired[List[ArtifactTypeDef]]
    outputArtifacts: NotRequired[List[ArtifactTypeDef]]
    artifactCredentials: NotRequired[AWSSessionCredentialsTypeDef]
    continuationToken: NotRequired[str]
    encryptionKey: NotRequired[EncryptionKeyTypeDef]

ActionTypeDeclarationOutputTypeDef = TypedDict(
    "ActionTypeDeclarationOutputTypeDef",
    {
        "executor": ActionTypeExecutorOutputTypeDef,
        "id": ActionTypeIdentifierTypeDef,
        "inputArtifactDetails": ActionTypeArtifactDetailsTypeDef,
        "outputArtifactDetails": ActionTypeArtifactDetailsTypeDef,
        "description": NotRequired[str],
        "permissions": NotRequired[ActionTypePermissionsOutputTypeDef],
        "properties": NotRequired[List[ActionTypePropertyTypeDef]],
        "urls": NotRequired[ActionTypeUrlsTypeDef],
    },
)
GitPullRequestFilterUnionTypeDef = Union[
    GitPullRequestFilterTypeDef, GitPullRequestFilterOutputTypeDef
]

class PipelineTriggerDeclarationOutputTypeDef(TypedDict):
    providerType: Literal["CodeStarSourceConnection"]
    gitConfiguration: GitConfigurationOutputTypeDef

GitPushFilterUnionTypeDef = Union[GitPushFilterTypeDef, GitPushFilterOutputTypeDef]
ExecutorConfigurationUnionTypeDef = Union[
    ExecutorConfigurationTypeDef, ExecutorConfigurationOutputTypeDef
]
ActionDeclarationUnionTypeDef = Union[ActionDeclarationTypeDef, ActionDeclarationOutputTypeDef]

class BeforeEntryConditionsOutputTypeDef(TypedDict):
    conditions: List[ConditionOutputTypeDef]

class FailureConditionsOutputTypeDef(TypedDict):
    result: NotRequired[ResultType]
    retryConfiguration: NotRequired[RetryConfigurationTypeDef]
    conditions: NotRequired[List[ConditionOutputTypeDef]]

class SuccessConditionsOutputTypeDef(TypedDict):
    conditions: List[ConditionOutputTypeDef]

class ConditionTypeDef(TypedDict):
    result: NotRequired[ResultType]
    rules: NotRequired[Sequence[RuleDeclarationUnionTypeDef]]

class ListWebhooksOutputTypeDef(TypedDict):
    webhooks: List[ListWebhookItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PutWebhookOutputTypeDef(TypedDict):
    webhook: ListWebhookItemTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StageConditionStateTypeDef(TypedDict):
    latestExecution: NotRequired[StageConditionsExecutionTypeDef]
    conditionStates: NotRequired[List[ConditionStateTypeDef]]

class ListActionExecutionsOutputTypeDef(TypedDict):
    actionExecutionDetails: List[ActionExecutionDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListRuleExecutionsOutputTypeDef(TypedDict):
    ruleExecutionDetails: List[RuleExecutionDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

JobDetailsTypeDef = TypedDict(
    "JobDetailsTypeDef",
    {
        "id": NotRequired[str],
        "data": NotRequired[JobDataTypeDef],
        "accountId": NotRequired[str],
    },
)
JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "id": NotRequired[str],
        "data": NotRequired[JobDataTypeDef],
        "nonce": NotRequired[str],
        "accountId": NotRequired[str],
    },
)
ThirdPartyJobDetailsTypeDef = TypedDict(
    "ThirdPartyJobDetailsTypeDef",
    {
        "id": NotRequired[str],
        "data": NotRequired[ThirdPartyJobDataTypeDef],
        "nonce": NotRequired[str],
    },
)

class GetActionTypeOutputTypeDef(TypedDict):
    actionType: ActionTypeDeclarationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GitConfigurationTypeDef(TypedDict):
    sourceActionName: str
    push: NotRequired[Sequence[GitPushFilterUnionTypeDef]]
    pullRequest: NotRequired[Sequence[GitPullRequestFilterUnionTypeDef]]

ActionTypeExecutorTypeDef = TypedDict(
    "ActionTypeExecutorTypeDef",
    {
        "configuration": ExecutorConfigurationUnionTypeDef,
        "type": ExecutorTypeType,
        "policyStatementsTemplate": NotRequired[str],
        "jobTimeout": NotRequired[int],
    },
)

class StageDeclarationOutputTypeDef(TypedDict):
    name: str
    actions: List[ActionDeclarationOutputTypeDef]
    blockers: NotRequired[List[BlockerDeclarationTypeDef]]
    onFailure: NotRequired[FailureConditionsOutputTypeDef]
    onSuccess: NotRequired[SuccessConditionsOutputTypeDef]
    beforeEntry: NotRequired[BeforeEntryConditionsOutputTypeDef]

class BeforeEntryConditionsTypeDef(TypedDict):
    conditions: Sequence[ConditionTypeDef]

ConditionUnionTypeDef = Union[ConditionTypeDef, ConditionOutputTypeDef]

class SuccessConditionsTypeDef(TypedDict):
    conditions: Sequence[ConditionTypeDef]

class StageStateTypeDef(TypedDict):
    stageName: NotRequired[str]
    inboundExecution: NotRequired[StageExecutionTypeDef]
    inboundExecutions: NotRequired[List[StageExecutionTypeDef]]
    inboundTransitionState: NotRequired[TransitionStateTypeDef]
    actionStates: NotRequired[List[ActionStateTypeDef]]
    latestExecution: NotRequired[StageExecutionTypeDef]
    beforeEntryConditionState: NotRequired[StageConditionStateTypeDef]
    onSuccessConditionState: NotRequired[StageConditionStateTypeDef]
    onFailureConditionState: NotRequired[StageConditionStateTypeDef]
    retryStageMetadata: NotRequired[RetryStageMetadataTypeDef]

class GetJobDetailsOutputTypeDef(TypedDict):
    jobDetails: JobDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PollForJobsOutputTypeDef(TypedDict):
    jobs: List[JobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetThirdPartyJobDetailsOutputTypeDef(TypedDict):
    jobDetails: ThirdPartyJobDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

GitConfigurationUnionTypeDef = Union[GitConfigurationTypeDef, GitConfigurationOutputTypeDef]
ActionTypeExecutorUnionTypeDef = Union[ActionTypeExecutorTypeDef, ActionTypeExecutorOutputTypeDef]

class PipelineDeclarationOutputTypeDef(TypedDict):
    name: str
    roleArn: str
    stages: List[StageDeclarationOutputTypeDef]
    artifactStore: NotRequired[ArtifactStoreTypeDef]
    artifactStores: NotRequired[Dict[str, ArtifactStoreTypeDef]]
    version: NotRequired[int]
    executionMode: NotRequired[ExecutionModeType]
    pipelineType: NotRequired[PipelineTypeType]
    variables: NotRequired[List[PipelineVariableDeclarationTypeDef]]
    triggers: NotRequired[List[PipelineTriggerDeclarationOutputTypeDef]]

BeforeEntryConditionsUnionTypeDef = Union[
    BeforeEntryConditionsTypeDef, BeforeEntryConditionsOutputTypeDef
]

class FailureConditionsTypeDef(TypedDict):
    result: NotRequired[ResultType]
    retryConfiguration: NotRequired[RetryConfigurationTypeDef]
    conditions: NotRequired[Sequence[ConditionUnionTypeDef]]

SuccessConditionsUnionTypeDef = Union[SuccessConditionsTypeDef, SuccessConditionsOutputTypeDef]

class GetPipelineStateOutputTypeDef(TypedDict):
    pipelineName: str
    pipelineVersion: int
    stageStates: List[StageStateTypeDef]
    created: datetime
    updated: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class PipelineTriggerDeclarationTypeDef(TypedDict):
    providerType: Literal["CodeStarSourceConnection"]
    gitConfiguration: GitConfigurationUnionTypeDef

ActionTypeDeclarationTypeDef = TypedDict(
    "ActionTypeDeclarationTypeDef",
    {
        "executor": ActionTypeExecutorUnionTypeDef,
        "id": ActionTypeIdentifierTypeDef,
        "inputArtifactDetails": ActionTypeArtifactDetailsTypeDef,
        "outputArtifactDetails": ActionTypeArtifactDetailsTypeDef,
        "description": NotRequired[str],
        "permissions": NotRequired[ActionTypePermissionsUnionTypeDef],
        "properties": NotRequired[Sequence[ActionTypePropertyTypeDef]],
        "urls": NotRequired[ActionTypeUrlsTypeDef],
    },
)

class CreatePipelineOutputTypeDef(TypedDict):
    pipeline: PipelineDeclarationOutputTypeDef
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetPipelineOutputTypeDef(TypedDict):
    pipeline: PipelineDeclarationOutputTypeDef
    metadata: PipelineMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePipelineOutputTypeDef(TypedDict):
    pipeline: PipelineDeclarationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

FailureConditionsUnionTypeDef = Union[FailureConditionsTypeDef, FailureConditionsOutputTypeDef]
PipelineTriggerDeclarationUnionTypeDef = Union[
    PipelineTriggerDeclarationTypeDef, PipelineTriggerDeclarationOutputTypeDef
]

class UpdateActionTypeInputRequestTypeDef(TypedDict):
    actionType: ActionTypeDeclarationTypeDef

class StageDeclarationTypeDef(TypedDict):
    name: str
    actions: Sequence[ActionDeclarationUnionTypeDef]
    blockers: NotRequired[Sequence[BlockerDeclarationTypeDef]]
    onFailure: NotRequired[FailureConditionsUnionTypeDef]
    onSuccess: NotRequired[SuccessConditionsUnionTypeDef]
    beforeEntry: NotRequired[BeforeEntryConditionsUnionTypeDef]

StageDeclarationUnionTypeDef = Union[StageDeclarationTypeDef, StageDeclarationOutputTypeDef]

class PipelineDeclarationTypeDef(TypedDict):
    name: str
    roleArn: str
    stages: Sequence[StageDeclarationUnionTypeDef]
    artifactStore: NotRequired[ArtifactStoreTypeDef]
    artifactStores: NotRequired[Mapping[str, ArtifactStoreTypeDef]]
    version: NotRequired[int]
    executionMode: NotRequired[ExecutionModeType]
    pipelineType: NotRequired[PipelineTypeType]
    variables: NotRequired[Sequence[PipelineVariableDeclarationTypeDef]]
    triggers: NotRequired[Sequence[PipelineTriggerDeclarationUnionTypeDef]]

class CreatePipelineInputRequestTypeDef(TypedDict):
    pipeline: PipelineDeclarationTypeDef
    tags: NotRequired[Sequence[TagTypeDef]]

class UpdatePipelineInputRequestTypeDef(TypedDict):
    pipeline: PipelineDeclarationTypeDef
