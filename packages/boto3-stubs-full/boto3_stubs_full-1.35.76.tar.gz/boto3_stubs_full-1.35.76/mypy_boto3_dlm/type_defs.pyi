"""
Type annotations for dlm service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dlm/type_defs/)

Usage::

    ```python
    from mypy_boto3_dlm.type_defs import RetentionArchiveTierTypeDef

    data: RetentionArchiveTierTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    DefaultPoliciesTypeValuesType,
    DefaultPolicyTypeValuesType,
    GettablePolicyStateValuesType,
    LocationValuesType,
    PolicyLanguageValuesType,
    PolicyTypeValuesType,
    ResourceLocationValuesType,
    ResourceTypeValuesType,
    RetentionIntervalUnitValuesType,
    SettablePolicyStateValuesType,
    StageValuesType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ActionOutputTypeDef",
    "ActionTypeDef",
    "ActionUnionTypeDef",
    "ArchiveRetainRuleTypeDef",
    "ArchiveRuleTypeDef",
    "CreateLifecyclePolicyRequestRequestTypeDef",
    "CreateLifecyclePolicyResponseTypeDef",
    "CreateRuleOutputTypeDef",
    "CreateRuleTypeDef",
    "CreateRuleUnionTypeDef",
    "CrossRegionCopyActionTypeDef",
    "CrossRegionCopyDeprecateRuleTypeDef",
    "CrossRegionCopyRetainRuleTypeDef",
    "CrossRegionCopyRuleTypeDef",
    "CrossRegionCopyTargetTypeDef",
    "DeleteLifecyclePolicyRequestRequestTypeDef",
    "DeprecateRuleTypeDef",
    "EncryptionConfigurationTypeDef",
    "EventParametersOutputTypeDef",
    "EventParametersTypeDef",
    "EventParametersUnionTypeDef",
    "EventSourceOutputTypeDef",
    "EventSourceTypeDef",
    "EventSourceUnionTypeDef",
    "ExclusionsOutputTypeDef",
    "ExclusionsTypeDef",
    "ExclusionsUnionTypeDef",
    "FastRestoreRuleOutputTypeDef",
    "FastRestoreRuleTypeDef",
    "FastRestoreRuleUnionTypeDef",
    "GetLifecyclePoliciesRequestRequestTypeDef",
    "GetLifecyclePoliciesResponseTypeDef",
    "GetLifecyclePolicyRequestRequestTypeDef",
    "GetLifecyclePolicyResponseTypeDef",
    "LifecyclePolicySummaryTypeDef",
    "LifecyclePolicyTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ParametersOutputTypeDef",
    "ParametersTypeDef",
    "ParametersUnionTypeDef",
    "PolicyDetailsOutputTypeDef",
    "PolicyDetailsTypeDef",
    "ResponseMetadataTypeDef",
    "RetainRuleTypeDef",
    "RetentionArchiveTierTypeDef",
    "ScheduleOutputTypeDef",
    "ScheduleTypeDef",
    "ScheduleUnionTypeDef",
    "ScriptOutputTypeDef",
    "ScriptTypeDef",
    "ScriptUnionTypeDef",
    "ShareRuleOutputTypeDef",
    "ShareRuleTypeDef",
    "ShareRuleUnionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateLifecyclePolicyRequestRequestTypeDef",
)

class RetentionArchiveTierTypeDef(TypedDict):
    Count: NotRequired[int]
    Interval: NotRequired[int]
    IntervalUnit: NotRequired[RetentionIntervalUnitValuesType]

class CrossRegionCopyTargetTypeDef(TypedDict):
    TargetRegion: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ScriptOutputTypeDef(TypedDict):
    ExecutionHandler: str
    Stages: NotRequired[List[StageValuesType]]
    ExecutionHandlerService: NotRequired[Literal["AWS_SYSTEMS_MANAGER"]]
    ExecuteOperationOnScriptFailure: NotRequired[bool]
    ExecutionTimeout: NotRequired[int]
    MaximumRetryCount: NotRequired[int]

class CrossRegionCopyRetainRuleTypeDef(TypedDict):
    Interval: NotRequired[int]
    IntervalUnit: NotRequired[RetentionIntervalUnitValuesType]

class EncryptionConfigurationTypeDef(TypedDict):
    Encrypted: bool
    CmkArn: NotRequired[str]

class CrossRegionCopyDeprecateRuleTypeDef(TypedDict):
    Interval: NotRequired[int]
    IntervalUnit: NotRequired[RetentionIntervalUnitValuesType]

class DeleteLifecyclePolicyRequestRequestTypeDef(TypedDict):
    PolicyId: str

class DeprecateRuleTypeDef(TypedDict):
    Count: NotRequired[int]
    Interval: NotRequired[int]
    IntervalUnit: NotRequired[RetentionIntervalUnitValuesType]

class EventParametersOutputTypeDef(TypedDict):
    EventType: Literal["shareSnapshot"]
    SnapshotOwner: List[str]
    DescriptionRegex: str

class EventParametersTypeDef(TypedDict):
    EventType: Literal["shareSnapshot"]
    SnapshotOwner: Sequence[str]
    DescriptionRegex: str

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class FastRestoreRuleOutputTypeDef(TypedDict):
    AvailabilityZones: List[str]
    Count: NotRequired[int]
    Interval: NotRequired[int]
    IntervalUnit: NotRequired[RetentionIntervalUnitValuesType]

class FastRestoreRuleTypeDef(TypedDict):
    AvailabilityZones: Sequence[str]
    Count: NotRequired[int]
    Interval: NotRequired[int]
    IntervalUnit: NotRequired[RetentionIntervalUnitValuesType]

class GetLifecyclePoliciesRequestRequestTypeDef(TypedDict):
    PolicyIds: NotRequired[Sequence[str]]
    State: NotRequired[GettablePolicyStateValuesType]
    ResourceTypes: NotRequired[Sequence[ResourceTypeValuesType]]
    TargetTags: NotRequired[Sequence[str]]
    TagsToAdd: NotRequired[Sequence[str]]
    DefaultPolicyType: NotRequired[DefaultPoliciesTypeValuesType]

class LifecyclePolicySummaryTypeDef(TypedDict):
    PolicyId: NotRequired[str]
    Description: NotRequired[str]
    State: NotRequired[GettablePolicyStateValuesType]
    Tags: NotRequired[Dict[str, str]]
    PolicyType: NotRequired[PolicyTypeValuesType]
    DefaultPolicy: NotRequired[bool]

class GetLifecyclePolicyRequestRequestTypeDef(TypedDict):
    PolicyId: str

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class RetainRuleTypeDef(TypedDict):
    Count: NotRequired[int]
    Interval: NotRequired[int]
    IntervalUnit: NotRequired[RetentionIntervalUnitValuesType]

class ShareRuleOutputTypeDef(TypedDict):
    TargetAccounts: List[str]
    UnshareInterval: NotRequired[int]
    UnshareIntervalUnit: NotRequired[RetentionIntervalUnitValuesType]

class ScriptTypeDef(TypedDict):
    ExecutionHandler: str
    Stages: NotRequired[Sequence[StageValuesType]]
    ExecutionHandlerService: NotRequired[Literal["AWS_SYSTEMS_MANAGER"]]
    ExecuteOperationOnScriptFailure: NotRequired[bool]
    ExecutionTimeout: NotRequired[int]
    MaximumRetryCount: NotRequired[int]

class ShareRuleTypeDef(TypedDict):
    TargetAccounts: Sequence[str]
    UnshareInterval: NotRequired[int]
    UnshareIntervalUnit: NotRequired[RetentionIntervalUnitValuesType]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class ArchiveRetainRuleTypeDef(TypedDict):
    RetentionArchiveTier: RetentionArchiveTierTypeDef

class CreateLifecyclePolicyResponseTypeDef(TypedDict):
    PolicyId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRuleOutputTypeDef(TypedDict):
    Location: NotRequired[LocationValuesType]
    Interval: NotRequired[int]
    IntervalUnit: NotRequired[Literal["HOURS"]]
    Times: NotRequired[List[str]]
    CronExpression: NotRequired[str]
    Scripts: NotRequired[List[ScriptOutputTypeDef]]

class CrossRegionCopyActionTypeDef(TypedDict):
    Target: str
    EncryptionConfiguration: EncryptionConfigurationTypeDef
    RetainRule: NotRequired[CrossRegionCopyRetainRuleTypeDef]

class CrossRegionCopyRuleTypeDef(TypedDict):
    Encrypted: bool
    TargetRegion: NotRequired[str]
    Target: NotRequired[str]
    CmkArn: NotRequired[str]
    CopyTags: NotRequired[bool]
    RetainRule: NotRequired[CrossRegionCopyRetainRuleTypeDef]
    DeprecateRule: NotRequired[CrossRegionCopyDeprecateRuleTypeDef]

EventSourceOutputTypeDef = TypedDict(
    "EventSourceOutputTypeDef",
    {
        "Type": Literal["MANAGED_CWE"],
        "Parameters": NotRequired[EventParametersOutputTypeDef],
    },
)
EventParametersUnionTypeDef = Union[EventParametersTypeDef, EventParametersOutputTypeDef]

class ExclusionsOutputTypeDef(TypedDict):
    ExcludeBootVolumes: NotRequired[bool]
    ExcludeVolumeTypes: NotRequired[List[str]]
    ExcludeTags: NotRequired[List[TagTypeDef]]

class ExclusionsTypeDef(TypedDict):
    ExcludeBootVolumes: NotRequired[bool]
    ExcludeVolumeTypes: NotRequired[Sequence[str]]
    ExcludeTags: NotRequired[Sequence[TagTypeDef]]

class ParametersOutputTypeDef(TypedDict):
    ExcludeBootVolume: NotRequired[bool]
    NoReboot: NotRequired[bool]
    ExcludeDataVolumeTags: NotRequired[List[TagTypeDef]]

class ParametersTypeDef(TypedDict):
    ExcludeBootVolume: NotRequired[bool]
    NoReboot: NotRequired[bool]
    ExcludeDataVolumeTags: NotRequired[Sequence[TagTypeDef]]

FastRestoreRuleUnionTypeDef = Union[FastRestoreRuleTypeDef, FastRestoreRuleOutputTypeDef]

class GetLifecyclePoliciesResponseTypeDef(TypedDict):
    Policies: List[LifecyclePolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

ScriptUnionTypeDef = Union[ScriptTypeDef, ScriptOutputTypeDef]
ShareRuleUnionTypeDef = Union[ShareRuleTypeDef, ShareRuleOutputTypeDef]

class ArchiveRuleTypeDef(TypedDict):
    RetainRule: ArchiveRetainRuleTypeDef

class ActionOutputTypeDef(TypedDict):
    Name: str
    CrossRegionCopy: List[CrossRegionCopyActionTypeDef]

class ActionTypeDef(TypedDict):
    Name: str
    CrossRegionCopy: Sequence[CrossRegionCopyActionTypeDef]

EventSourceTypeDef = TypedDict(
    "EventSourceTypeDef",
    {
        "Type": Literal["MANAGED_CWE"],
        "Parameters": NotRequired[EventParametersUnionTypeDef],
    },
)
ExclusionsUnionTypeDef = Union[ExclusionsTypeDef, ExclusionsOutputTypeDef]
ParametersUnionTypeDef = Union[ParametersTypeDef, ParametersOutputTypeDef]

class CreateRuleTypeDef(TypedDict):
    Location: NotRequired[LocationValuesType]
    Interval: NotRequired[int]
    IntervalUnit: NotRequired[Literal["HOURS"]]
    Times: NotRequired[Sequence[str]]
    CronExpression: NotRequired[str]
    Scripts: NotRequired[Sequence[ScriptUnionTypeDef]]

class ScheduleOutputTypeDef(TypedDict):
    Name: NotRequired[str]
    CopyTags: NotRequired[bool]
    TagsToAdd: NotRequired[List[TagTypeDef]]
    VariableTags: NotRequired[List[TagTypeDef]]
    CreateRule: NotRequired[CreateRuleOutputTypeDef]
    RetainRule: NotRequired[RetainRuleTypeDef]
    FastRestoreRule: NotRequired[FastRestoreRuleOutputTypeDef]
    CrossRegionCopyRules: NotRequired[List[CrossRegionCopyRuleTypeDef]]
    ShareRules: NotRequired[List[ShareRuleOutputTypeDef]]
    DeprecateRule: NotRequired[DeprecateRuleTypeDef]
    ArchiveRule: NotRequired[ArchiveRuleTypeDef]

ActionUnionTypeDef = Union[ActionTypeDef, ActionOutputTypeDef]
EventSourceUnionTypeDef = Union[EventSourceTypeDef, EventSourceOutputTypeDef]
CreateRuleUnionTypeDef = Union[CreateRuleTypeDef, CreateRuleOutputTypeDef]

class PolicyDetailsOutputTypeDef(TypedDict):
    PolicyType: NotRequired[PolicyTypeValuesType]
    ResourceTypes: NotRequired[List[ResourceTypeValuesType]]
    ResourceLocations: NotRequired[List[ResourceLocationValuesType]]
    TargetTags: NotRequired[List[TagTypeDef]]
    Schedules: NotRequired[List[ScheduleOutputTypeDef]]
    Parameters: NotRequired[ParametersOutputTypeDef]
    EventSource: NotRequired[EventSourceOutputTypeDef]
    Actions: NotRequired[List[ActionOutputTypeDef]]
    PolicyLanguage: NotRequired[PolicyLanguageValuesType]
    ResourceType: NotRequired[ResourceTypeValuesType]
    CreateInterval: NotRequired[int]
    RetainInterval: NotRequired[int]
    CopyTags: NotRequired[bool]
    CrossRegionCopyTargets: NotRequired[List[CrossRegionCopyTargetTypeDef]]
    ExtendDeletion: NotRequired[bool]
    Exclusions: NotRequired[ExclusionsOutputTypeDef]

class ScheduleTypeDef(TypedDict):
    Name: NotRequired[str]
    CopyTags: NotRequired[bool]
    TagsToAdd: NotRequired[Sequence[TagTypeDef]]
    VariableTags: NotRequired[Sequence[TagTypeDef]]
    CreateRule: NotRequired[CreateRuleUnionTypeDef]
    RetainRule: NotRequired[RetainRuleTypeDef]
    FastRestoreRule: NotRequired[FastRestoreRuleUnionTypeDef]
    CrossRegionCopyRules: NotRequired[Sequence[CrossRegionCopyRuleTypeDef]]
    ShareRules: NotRequired[Sequence[ShareRuleUnionTypeDef]]
    DeprecateRule: NotRequired[DeprecateRuleTypeDef]
    ArchiveRule: NotRequired[ArchiveRuleTypeDef]

class LifecyclePolicyTypeDef(TypedDict):
    PolicyId: NotRequired[str]
    Description: NotRequired[str]
    State: NotRequired[GettablePolicyStateValuesType]
    StatusMessage: NotRequired[str]
    ExecutionRoleArn: NotRequired[str]
    DateCreated: NotRequired[datetime]
    DateModified: NotRequired[datetime]
    PolicyDetails: NotRequired[PolicyDetailsOutputTypeDef]
    Tags: NotRequired[Dict[str, str]]
    PolicyArn: NotRequired[str]
    DefaultPolicy: NotRequired[bool]

ScheduleUnionTypeDef = Union[ScheduleTypeDef, ScheduleOutputTypeDef]

class GetLifecyclePolicyResponseTypeDef(TypedDict):
    Policy: LifecyclePolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PolicyDetailsTypeDef(TypedDict):
    PolicyType: NotRequired[PolicyTypeValuesType]
    ResourceTypes: NotRequired[Sequence[ResourceTypeValuesType]]
    ResourceLocations: NotRequired[Sequence[ResourceLocationValuesType]]
    TargetTags: NotRequired[Sequence[TagTypeDef]]
    Schedules: NotRequired[Sequence[ScheduleUnionTypeDef]]
    Parameters: NotRequired[ParametersUnionTypeDef]
    EventSource: NotRequired[EventSourceUnionTypeDef]
    Actions: NotRequired[Sequence[ActionUnionTypeDef]]
    PolicyLanguage: NotRequired[PolicyLanguageValuesType]
    ResourceType: NotRequired[ResourceTypeValuesType]
    CreateInterval: NotRequired[int]
    RetainInterval: NotRequired[int]
    CopyTags: NotRequired[bool]
    CrossRegionCopyTargets: NotRequired[Sequence[CrossRegionCopyTargetTypeDef]]
    ExtendDeletion: NotRequired[bool]
    Exclusions: NotRequired[ExclusionsUnionTypeDef]

class CreateLifecyclePolicyRequestRequestTypeDef(TypedDict):
    ExecutionRoleArn: str
    Description: str
    State: SettablePolicyStateValuesType
    PolicyDetails: NotRequired[PolicyDetailsTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    DefaultPolicy: NotRequired[DefaultPolicyTypeValuesType]
    CreateInterval: NotRequired[int]
    RetainInterval: NotRequired[int]
    CopyTags: NotRequired[bool]
    ExtendDeletion: NotRequired[bool]
    CrossRegionCopyTargets: NotRequired[Sequence[CrossRegionCopyTargetTypeDef]]
    Exclusions: NotRequired[ExclusionsTypeDef]

class UpdateLifecyclePolicyRequestRequestTypeDef(TypedDict):
    PolicyId: str
    ExecutionRoleArn: NotRequired[str]
    State: NotRequired[SettablePolicyStateValuesType]
    Description: NotRequired[str]
    PolicyDetails: NotRequired[PolicyDetailsTypeDef]
    CreateInterval: NotRequired[int]
    RetainInterval: NotRequired[int]
    CopyTags: NotRequired[bool]
    ExtendDeletion: NotRequired[bool]
    CrossRegionCopyTargets: NotRequired[Sequence[CrossRegionCopyTargetTypeDef]]
    Exclusions: NotRequired[ExclusionsTypeDef]
