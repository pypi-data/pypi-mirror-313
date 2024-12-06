"""
Type annotations for migrationhuborchestrator service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migrationhuborchestrator/type_defs/)

Usage::

    ```python
    from mypy_boto3_migrationhuborchestrator.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    DataTypeType,
    MigrationWorkflowStatusEnumType,
    OwnerType,
    PluginHealthType,
    RunEnvironmentType,
    StepActionTypeType,
    StepGroupStatusType,
    StepStatusType,
    TargetTypeType,
    TemplateStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "CreateMigrationWorkflowRequestRequestTypeDef",
    "CreateMigrationWorkflowResponseTypeDef",
    "CreateTemplateRequestRequestTypeDef",
    "CreateTemplateResponseTypeDef",
    "CreateWorkflowStepGroupRequestRequestTypeDef",
    "CreateWorkflowStepGroupResponseTypeDef",
    "CreateWorkflowStepRequestRequestTypeDef",
    "CreateWorkflowStepResponseTypeDef",
    "DeleteMigrationWorkflowRequestRequestTypeDef",
    "DeleteMigrationWorkflowResponseTypeDef",
    "DeleteTemplateRequestRequestTypeDef",
    "DeleteWorkflowStepGroupRequestRequestTypeDef",
    "DeleteWorkflowStepRequestRequestTypeDef",
    "GetMigrationWorkflowRequestRequestTypeDef",
    "GetMigrationWorkflowResponseTypeDef",
    "GetMigrationWorkflowTemplateRequestRequestTypeDef",
    "GetMigrationWorkflowTemplateResponseTypeDef",
    "GetTemplateStepGroupRequestRequestTypeDef",
    "GetTemplateStepGroupResponseTypeDef",
    "GetTemplateStepRequestRequestTypeDef",
    "GetTemplateStepResponseTypeDef",
    "GetWorkflowStepGroupRequestRequestTypeDef",
    "GetWorkflowStepGroupResponseTypeDef",
    "GetWorkflowStepRequestRequestTypeDef",
    "GetWorkflowStepResponseTypeDef",
    "ListMigrationWorkflowTemplatesRequestListTemplatesPaginateTypeDef",
    "ListMigrationWorkflowTemplatesRequestRequestTypeDef",
    "ListMigrationWorkflowTemplatesResponseTypeDef",
    "ListMigrationWorkflowsRequestListWorkflowsPaginateTypeDef",
    "ListMigrationWorkflowsRequestRequestTypeDef",
    "ListMigrationWorkflowsResponseTypeDef",
    "ListPluginsRequestListPluginsPaginateTypeDef",
    "ListPluginsRequestRequestTypeDef",
    "ListPluginsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTemplateStepGroupsRequestListTemplateStepGroupsPaginateTypeDef",
    "ListTemplateStepGroupsRequestRequestTypeDef",
    "ListTemplateStepGroupsResponseTypeDef",
    "ListTemplateStepsRequestListTemplateStepsPaginateTypeDef",
    "ListTemplateStepsRequestRequestTypeDef",
    "ListTemplateStepsResponseTypeDef",
    "ListWorkflowStepGroupsRequestListWorkflowStepGroupsPaginateTypeDef",
    "ListWorkflowStepGroupsRequestRequestTypeDef",
    "ListWorkflowStepGroupsResponseTypeDef",
    "ListWorkflowStepsRequestListWorkflowStepsPaginateTypeDef",
    "ListWorkflowStepsRequestRequestTypeDef",
    "ListWorkflowStepsResponseTypeDef",
    "MigrationWorkflowSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "PlatformCommandTypeDef",
    "PlatformScriptKeyTypeDef",
    "PluginSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "RetryWorkflowStepRequestRequestTypeDef",
    "RetryWorkflowStepResponseTypeDef",
    "StartMigrationWorkflowRequestRequestTypeDef",
    "StartMigrationWorkflowResponseTypeDef",
    "StepAutomationConfigurationTypeDef",
    "StepInputOutputTypeDef",
    "StepInputTypeDef",
    "StepInputUnionTypeDef",
    "StepOutputTypeDef",
    "StopMigrationWorkflowRequestRequestTypeDef",
    "StopMigrationWorkflowResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TemplateInputTypeDef",
    "TemplateSourceTypeDef",
    "TemplateStepGroupSummaryTypeDef",
    "TemplateStepSummaryTypeDef",
    "TemplateSummaryTypeDef",
    "ToolTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateMigrationWorkflowRequestRequestTypeDef",
    "UpdateMigrationWorkflowResponseTypeDef",
    "UpdateTemplateRequestRequestTypeDef",
    "UpdateTemplateResponseTypeDef",
    "UpdateWorkflowStepGroupRequestRequestTypeDef",
    "UpdateWorkflowStepGroupResponseTypeDef",
    "UpdateWorkflowStepRequestRequestTypeDef",
    "UpdateWorkflowStepResponseTypeDef",
    "WorkflowStepAutomationConfigurationTypeDef",
    "WorkflowStepExtraOutputTypeDef",
    "WorkflowStepGroupSummaryTypeDef",
    "WorkflowStepOutputTypeDef",
    "WorkflowStepOutputUnionOutputTypeDef",
    "WorkflowStepOutputUnionTypeDef",
    "WorkflowStepOutputUnionUnionTypeDef",
    "WorkflowStepSummaryTypeDef",
    "WorkflowStepUnionTypeDef",
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class StepInputOutputTypeDef(TypedDict):
    integerValue: NotRequired[int]
    stringValue: NotRequired[str]
    listOfStringsValue: NotRequired[List[str]]
    mapOfStringValue: NotRequired[Dict[str, str]]

class TemplateSourceTypeDef(TypedDict):
    workflowId: NotRequired[str]

CreateWorkflowStepGroupRequestRequestTypeDef = TypedDict(
    "CreateWorkflowStepGroupRequestRequestTypeDef",
    {
        "workflowId": str,
        "name": str,
        "description": NotRequired[str],
        "next": NotRequired[Sequence[str]],
        "previous": NotRequired[Sequence[str]],
    },
)

class ToolTypeDef(TypedDict):
    name: NotRequired[str]
    url: NotRequired[str]

DeleteMigrationWorkflowRequestRequestTypeDef = TypedDict(
    "DeleteMigrationWorkflowRequestRequestTypeDef",
    {
        "id": str,
    },
)
DeleteTemplateRequestRequestTypeDef = TypedDict(
    "DeleteTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)
DeleteWorkflowStepGroupRequestRequestTypeDef = TypedDict(
    "DeleteWorkflowStepGroupRequestRequestTypeDef",
    {
        "workflowId": str,
        "id": str,
    },
)
DeleteWorkflowStepRequestRequestTypeDef = TypedDict(
    "DeleteWorkflowStepRequestRequestTypeDef",
    {
        "id": str,
        "stepGroupId": str,
        "workflowId": str,
    },
)
GetMigrationWorkflowRequestRequestTypeDef = TypedDict(
    "GetMigrationWorkflowRequestRequestTypeDef",
    {
        "id": str,
    },
)
GetMigrationWorkflowTemplateRequestRequestTypeDef = TypedDict(
    "GetMigrationWorkflowTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)

class TemplateInputTypeDef(TypedDict):
    inputName: NotRequired[str]
    dataType: NotRequired[DataTypeType]
    required: NotRequired[bool]

GetTemplateStepGroupRequestRequestTypeDef = TypedDict(
    "GetTemplateStepGroupRequestRequestTypeDef",
    {
        "templateId": str,
        "id": str,
    },
)
GetTemplateStepRequestRequestTypeDef = TypedDict(
    "GetTemplateStepRequestRequestTypeDef",
    {
        "id": str,
        "templateId": str,
        "stepGroupId": str,
    },
)

class StepOutputTypeDef(TypedDict):
    name: NotRequired[str]
    dataType: NotRequired[DataTypeType]
    required: NotRequired[bool]

GetWorkflowStepGroupRequestRequestTypeDef = TypedDict(
    "GetWorkflowStepGroupRequestRequestTypeDef",
    {
        "id": str,
        "workflowId": str,
    },
)
GetWorkflowStepRequestRequestTypeDef = TypedDict(
    "GetWorkflowStepRequestRequestTypeDef",
    {
        "workflowId": str,
        "stepGroupId": str,
        "id": str,
    },
)

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListMigrationWorkflowTemplatesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    name: NotRequired[str]

TemplateSummaryTypeDef = TypedDict(
    "TemplateSummaryTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "arn": NotRequired[str],
        "description": NotRequired[str],
    },
)

class ListMigrationWorkflowsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    templateId: NotRequired[str]
    adsApplicationConfigurationName: NotRequired[str]
    status: NotRequired[MigrationWorkflowStatusEnumType]
    name: NotRequired[str]

MigrationWorkflowSummaryTypeDef = TypedDict(
    "MigrationWorkflowSummaryTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "templateId": NotRequired[str],
        "adsApplicationConfigurationName": NotRequired[str],
        "status": NotRequired[MigrationWorkflowStatusEnumType],
        "creationTime": NotRequired[datetime],
        "endTime": NotRequired[datetime],
        "statusMessage": NotRequired[str],
        "completedSteps": NotRequired[int],
        "totalSteps": NotRequired[int],
    },
)

class ListPluginsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class PluginSummaryTypeDef(TypedDict):
    pluginId: NotRequired[str]
    hostname: NotRequired[str]
    status: NotRequired[PluginHealthType]
    ipAddress: NotRequired[str]
    version: NotRequired[str]
    registeredTime: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class ListTemplateStepGroupsRequestRequestTypeDef(TypedDict):
    templateId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

TemplateStepGroupSummaryTypeDef = TypedDict(
    "TemplateStepGroupSummaryTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "previous": NotRequired[List[str]],
        "next": NotRequired[List[str]],
    },
)

class ListTemplateStepsRequestRequestTypeDef(TypedDict):
    templateId: str
    stepGroupId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

TemplateStepSummaryTypeDef = TypedDict(
    "TemplateStepSummaryTypeDef",
    {
        "id": NotRequired[str],
        "stepGroupId": NotRequired[str],
        "templateId": NotRequired[str],
        "name": NotRequired[str],
        "stepActionType": NotRequired[StepActionTypeType],
        "targetType": NotRequired[TargetTypeType],
        "owner": NotRequired[OwnerType],
        "previous": NotRequired[List[str]],
        "next": NotRequired[List[str]],
    },
)

class ListWorkflowStepGroupsRequestRequestTypeDef(TypedDict):
    workflowId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

WorkflowStepGroupSummaryTypeDef = TypedDict(
    "WorkflowStepGroupSummaryTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "owner": NotRequired[OwnerType],
        "status": NotRequired[StepGroupStatusType],
        "previous": NotRequired[List[str]],
        "next": NotRequired[List[str]],
    },
)

class ListWorkflowStepsRequestRequestTypeDef(TypedDict):
    workflowId: str
    stepGroupId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

WorkflowStepSummaryTypeDef = TypedDict(
    "WorkflowStepSummaryTypeDef",
    {
        "stepId": NotRequired[str],
        "name": NotRequired[str],
        "stepActionType": NotRequired[StepActionTypeType],
        "owner": NotRequired[OwnerType],
        "previous": NotRequired[List[str]],
        "next": NotRequired[List[str]],
        "status": NotRequired[StepStatusType],
        "statusMessage": NotRequired[str],
        "noOfSrvCompleted": NotRequired[int],
        "noOfSrvFailed": NotRequired[int],
        "totalNoOfSrv": NotRequired[int],
        "description": NotRequired[str],
        "scriptLocation": NotRequired[str],
    },
)

class PlatformCommandTypeDef(TypedDict):
    linux: NotRequired[str]
    windows: NotRequired[str]

class PlatformScriptKeyTypeDef(TypedDict):
    linux: NotRequired[str]
    windows: NotRequired[str]

RetryWorkflowStepRequestRequestTypeDef = TypedDict(
    "RetryWorkflowStepRequestRequestTypeDef",
    {
        "workflowId": str,
        "stepGroupId": str,
        "id": str,
    },
)
StartMigrationWorkflowRequestRequestTypeDef = TypedDict(
    "StartMigrationWorkflowRequestRequestTypeDef",
    {
        "id": str,
    },
)

class StepInputTypeDef(TypedDict):
    integerValue: NotRequired[int]
    stringValue: NotRequired[str]
    listOfStringsValue: NotRequired[Sequence[str]]
    mapOfStringValue: NotRequired[Mapping[str, str]]

StopMigrationWorkflowRequestRequestTypeDef = TypedDict(
    "StopMigrationWorkflowRequestRequestTypeDef",
    {
        "id": str,
    },
)

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

UpdateTemplateRequestRequestTypeDef = TypedDict(
    "UpdateTemplateRequestRequestTypeDef",
    {
        "id": str,
        "templateName": NotRequired[str],
        "templateDescription": NotRequired[str],
        "clientToken": NotRequired[str],
    },
)
UpdateWorkflowStepGroupRequestRequestTypeDef = TypedDict(
    "UpdateWorkflowStepGroupRequestRequestTypeDef",
    {
        "workflowId": str,
        "id": str,
        "name": NotRequired[str],
        "description": NotRequired[str],
        "next": NotRequired[Sequence[str]],
        "previous": NotRequired[Sequence[str]],
    },
)

class WorkflowStepOutputUnionOutputTypeDef(TypedDict):
    integerValue: NotRequired[int]
    stringValue: NotRequired[str]
    listOfStringValue: NotRequired[List[str]]

class WorkflowStepOutputUnionTypeDef(TypedDict):
    integerValue: NotRequired[int]
    stringValue: NotRequired[str]
    listOfStringValue: NotRequired[Sequence[str]]

class CreateTemplateResponseTypeDef(TypedDict):
    templateId: str
    templateArn: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

CreateWorkflowStepResponseTypeDef = TypedDict(
    "CreateWorkflowStepResponseTypeDef",
    {
        "id": str,
        "stepGroupId": str,
        "workflowId": str,
        "name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteMigrationWorkflowResponseTypeDef = TypedDict(
    "DeleteMigrationWorkflowResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "status": MigrationWorkflowStatusEnumType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

RetryWorkflowStepResponseTypeDef = TypedDict(
    "RetryWorkflowStepResponseTypeDef",
    {
        "stepGroupId": str,
        "workflowId": str,
        "id": str,
        "status": StepStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartMigrationWorkflowResponseTypeDef = TypedDict(
    "StartMigrationWorkflowResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "status": MigrationWorkflowStatusEnumType,
        "statusMessage": str,
        "lastStartTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StopMigrationWorkflowResponseTypeDef = TypedDict(
    "StopMigrationWorkflowResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "status": MigrationWorkflowStatusEnumType,
        "statusMessage": str,
        "lastStopTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class UpdateTemplateResponseTypeDef(TypedDict):
    templateId: str
    templateArn: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

UpdateWorkflowStepResponseTypeDef = TypedDict(
    "UpdateWorkflowStepResponseTypeDef",
    {
        "id": str,
        "stepGroupId": str,
        "workflowId": str,
        "name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateMigrationWorkflowResponseTypeDef = TypedDict(
    "CreateMigrationWorkflowResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "templateId": str,
        "adsApplicationConfigurationId": str,
        "workflowInputs": Dict[str, StepInputOutputTypeDef],
        "stepTargets": List[str],
        "status": MigrationWorkflowStatusEnumType,
        "creationTime": datetime,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateMigrationWorkflowResponseTypeDef = TypedDict(
    "UpdateMigrationWorkflowResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "templateId": str,
        "adsApplicationConfigurationId": str,
        "workflowInputs": Dict[str, StepInputOutputTypeDef],
        "stepTargets": List[str],
        "status": MigrationWorkflowStatusEnumType,
        "creationTime": datetime,
        "lastModifiedTime": datetime,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateTemplateRequestRequestTypeDef(TypedDict):
    templateName: str
    templateSource: TemplateSourceTypeDef
    templateDescription: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

CreateWorkflowStepGroupResponseTypeDef = TypedDict(
    "CreateWorkflowStepGroupResponseTypeDef",
    {
        "workflowId": str,
        "name": str,
        "id": str,
        "description": str,
        "tools": List[ToolTypeDef],
        "next": List[str],
        "previous": List[str],
        "creationTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetMigrationWorkflowResponseTypeDef = TypedDict(
    "GetMigrationWorkflowResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "templateId": str,
        "adsApplicationConfigurationId": str,
        "adsApplicationName": str,
        "status": MigrationWorkflowStatusEnumType,
        "statusMessage": str,
        "creationTime": datetime,
        "lastStartTime": datetime,
        "lastStopTime": datetime,
        "lastModifiedTime": datetime,
        "endTime": datetime,
        "tools": List[ToolTypeDef],
        "totalSteps": int,
        "completedSteps": int,
        "workflowInputs": Dict[str, StepInputOutputTypeDef],
        "tags": Dict[str, str],
        "workflowBucket": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetTemplateStepGroupResponseTypeDef = TypedDict(
    "GetTemplateStepGroupResponseTypeDef",
    {
        "templateId": str,
        "id": str,
        "name": str,
        "description": str,
        "status": StepGroupStatusType,
        "creationTime": datetime,
        "lastModifiedTime": datetime,
        "tools": List[ToolTypeDef],
        "previous": List[str],
        "next": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetWorkflowStepGroupResponseTypeDef = TypedDict(
    "GetWorkflowStepGroupResponseTypeDef",
    {
        "id": str,
        "workflowId": str,
        "name": str,
        "description": str,
        "status": StepGroupStatusType,
        "owner": OwnerType,
        "creationTime": datetime,
        "lastModifiedTime": datetime,
        "endTime": datetime,
        "tools": List[ToolTypeDef],
        "previous": List[str],
        "next": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateWorkflowStepGroupResponseTypeDef = TypedDict(
    "UpdateWorkflowStepGroupResponseTypeDef",
    {
        "workflowId": str,
        "name": str,
        "id": str,
        "description": str,
        "tools": List[ToolTypeDef],
        "next": List[str],
        "previous": List[str],
        "lastModifiedTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetMigrationWorkflowTemplateResponseTypeDef = TypedDict(
    "GetMigrationWorkflowTemplateResponseTypeDef",
    {
        "id": str,
        "templateArn": str,
        "name": str,
        "description": str,
        "inputs": List[TemplateInputTypeDef],
        "tools": List[ToolTypeDef],
        "creationTime": datetime,
        "owner": str,
        "status": TemplateStatusType,
        "statusMessage": str,
        "templateClass": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ListMigrationWorkflowTemplatesRequestListTemplatesPaginateTypeDef(TypedDict):
    name: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMigrationWorkflowsRequestListWorkflowsPaginateTypeDef(TypedDict):
    templateId: NotRequired[str]
    adsApplicationConfigurationName: NotRequired[str]
    status: NotRequired[MigrationWorkflowStatusEnumType]
    name: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPluginsRequestListPluginsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTemplateStepGroupsRequestListTemplateStepGroupsPaginateTypeDef(TypedDict):
    templateId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTemplateStepsRequestListTemplateStepsPaginateTypeDef(TypedDict):
    templateId: str
    stepGroupId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWorkflowStepGroupsRequestListWorkflowStepGroupsPaginateTypeDef(TypedDict):
    workflowId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWorkflowStepsRequestListWorkflowStepsPaginateTypeDef(TypedDict):
    workflowId: str
    stepGroupId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMigrationWorkflowTemplatesResponseTypeDef(TypedDict):
    templateSummary: List[TemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListMigrationWorkflowsResponseTypeDef(TypedDict):
    migrationWorkflowSummary: List[MigrationWorkflowSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPluginsResponseTypeDef(TypedDict):
    plugins: List[PluginSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTemplateStepGroupsResponseTypeDef(TypedDict):
    templateStepGroupSummary: List[TemplateStepGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTemplateStepsResponseTypeDef(TypedDict):
    templateStepSummaryList: List[TemplateStepSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListWorkflowStepGroupsResponseTypeDef(TypedDict):
    workflowStepGroupsSummary: List[WorkflowStepGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListWorkflowStepsResponseTypeDef(TypedDict):
    workflowStepsSummary: List[WorkflowStepSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class StepAutomationConfigurationTypeDef(TypedDict):
    scriptLocationS3Bucket: NotRequired[str]
    scriptLocationS3Key: NotRequired[PlatformScriptKeyTypeDef]
    command: NotRequired[PlatformCommandTypeDef]
    runEnvironment: NotRequired[RunEnvironmentType]
    targetType: NotRequired[TargetTypeType]

class WorkflowStepAutomationConfigurationTypeDef(TypedDict):
    scriptLocationS3Bucket: NotRequired[str]
    scriptLocationS3Key: NotRequired[PlatformScriptKeyTypeDef]
    command: NotRequired[PlatformCommandTypeDef]
    runEnvironment: NotRequired[RunEnvironmentType]
    targetType: NotRequired[TargetTypeType]

StepInputUnionTypeDef = Union[StepInputTypeDef, StepInputOutputTypeDef]
UpdateMigrationWorkflowRequestRequestTypeDef = TypedDict(
    "UpdateMigrationWorkflowRequestRequestTypeDef",
    {
        "id": str,
        "name": NotRequired[str],
        "description": NotRequired[str],
        "inputParameters": NotRequired[Mapping[str, StepInputTypeDef]],
        "stepTargets": NotRequired[Sequence[str]],
    },
)

class WorkflowStepExtraOutputTypeDef(TypedDict):
    name: NotRequired[str]
    dataType: NotRequired[DataTypeType]
    required: NotRequired[bool]
    value: NotRequired[WorkflowStepOutputUnionOutputTypeDef]

WorkflowStepOutputUnionUnionTypeDef = Union[
    WorkflowStepOutputUnionTypeDef, WorkflowStepOutputUnionOutputTypeDef
]
GetTemplateStepResponseTypeDef = TypedDict(
    "GetTemplateStepResponseTypeDef",
    {
        "id": str,
        "stepGroupId": str,
        "templateId": str,
        "name": str,
        "description": str,
        "stepActionType": StepActionTypeType,
        "creationTime": str,
        "previous": List[str],
        "next": List[str],
        "outputs": List[StepOutputTypeDef],
        "stepAutomationConfiguration": StepAutomationConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateMigrationWorkflowRequestRequestTypeDef(TypedDict):
    name: str
    templateId: str
    inputParameters: Mapping[str, StepInputUnionTypeDef]
    description: NotRequired[str]
    applicationConfigurationId: NotRequired[str]
    stepTargets: NotRequired[Sequence[str]]
    tags: NotRequired[Mapping[str, str]]

GetWorkflowStepResponseTypeDef = TypedDict(
    "GetWorkflowStepResponseTypeDef",
    {
        "name": str,
        "stepGroupId": str,
        "workflowId": str,
        "stepId": str,
        "description": str,
        "stepActionType": StepActionTypeType,
        "owner": OwnerType,
        "workflowStepAutomationConfiguration": WorkflowStepAutomationConfigurationTypeDef,
        "stepTarget": List[str],
        "outputs": List[WorkflowStepExtraOutputTypeDef],
        "previous": List[str],
        "next": List[str],
        "status": StepStatusType,
        "statusMessage": str,
        "scriptOutputLocation": str,
        "creationTime": datetime,
        "lastStartTime": datetime,
        "endTime": datetime,
        "noOfSrvCompleted": int,
        "noOfSrvFailed": int,
        "totalNoOfSrv": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class WorkflowStepOutputTypeDef(TypedDict):
    name: NotRequired[str]
    dataType: NotRequired[DataTypeType]
    required: NotRequired[bool]
    value: NotRequired[WorkflowStepOutputUnionUnionTypeDef]

UpdateWorkflowStepRequestRequestTypeDef = TypedDict(
    "UpdateWorkflowStepRequestRequestTypeDef",
    {
        "id": str,
        "stepGroupId": str,
        "workflowId": str,
        "name": NotRequired[str],
        "description": NotRequired[str],
        "stepActionType": NotRequired[StepActionTypeType],
        "workflowStepAutomationConfiguration": NotRequired[
            WorkflowStepAutomationConfigurationTypeDef
        ],
        "stepTarget": NotRequired[Sequence[str]],
        "outputs": NotRequired[Sequence[WorkflowStepOutputTypeDef]],
        "previous": NotRequired[Sequence[str]],
        "next": NotRequired[Sequence[str]],
        "status": NotRequired[StepStatusType],
    },
)
WorkflowStepUnionTypeDef = Union[WorkflowStepOutputTypeDef, WorkflowStepExtraOutputTypeDef]
CreateWorkflowStepRequestRequestTypeDef = TypedDict(
    "CreateWorkflowStepRequestRequestTypeDef",
    {
        "name": str,
        "stepGroupId": str,
        "workflowId": str,
        "stepActionType": StepActionTypeType,
        "description": NotRequired[str],
        "workflowStepAutomationConfiguration": NotRequired[
            WorkflowStepAutomationConfigurationTypeDef
        ],
        "stepTarget": NotRequired[Sequence[str]],
        "outputs": NotRequired[Sequence[WorkflowStepUnionTypeDef]],
        "previous": NotRequired[Sequence[str]],
        "next": NotRequired[Sequence[str]],
    },
)
