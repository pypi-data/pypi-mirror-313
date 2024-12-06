"""
Type annotations for serverlessrepo service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_serverlessrepo/type_defs/)

Usage::

    ```python
    from mypy_boto3_serverlessrepo.type_defs import ApplicationDependencySummaryTypeDef

    data: ApplicationDependencySummaryTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Dict, List, Sequence, Union

from .literals import CapabilityType, StatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ApplicationDependencySummaryTypeDef",
    "ApplicationPolicyStatementOutputTypeDef",
    "ApplicationPolicyStatementTypeDef",
    "ApplicationPolicyStatementUnionTypeDef",
    "ApplicationSummaryTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateApplicationVersionRequestRequestTypeDef",
    "CreateApplicationVersionResponseTypeDef",
    "CreateCloudFormationChangeSetRequestRequestTypeDef",
    "CreateCloudFormationChangeSetResponseTypeDef",
    "CreateCloudFormationTemplateRequestRequestTypeDef",
    "CreateCloudFormationTemplateResponseTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetApplicationPolicyRequestRequestTypeDef",
    "GetApplicationPolicyResponseTypeDef",
    "GetApplicationRequestRequestTypeDef",
    "GetApplicationResponseTypeDef",
    "GetCloudFormationTemplateRequestRequestTypeDef",
    "GetCloudFormationTemplateResponseTypeDef",
    "ListApplicationDependenciesRequestListApplicationDependenciesPaginateTypeDef",
    "ListApplicationDependenciesRequestRequestTypeDef",
    "ListApplicationDependenciesResponseTypeDef",
    "ListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef",
    "ListApplicationVersionsRequestRequestTypeDef",
    "ListApplicationVersionsResponseTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListApplicationsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterDefinitionTypeDef",
    "ParameterValueTypeDef",
    "PutApplicationPolicyRequestRequestTypeDef",
    "PutApplicationPolicyResponseTypeDef",
    "ResponseMetadataTypeDef",
    "RollbackConfigurationTypeDef",
    "RollbackTriggerTypeDef",
    "TagTypeDef",
    "UnshareApplicationRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateApplicationResponseTypeDef",
    "VersionSummaryTypeDef",
    "VersionTypeDef",
)

class ApplicationDependencySummaryTypeDef(TypedDict):
    ApplicationId: str
    SemanticVersion: str

class ApplicationPolicyStatementOutputTypeDef(TypedDict):
    Actions: List[str]
    Principals: List[str]
    PrincipalOrgIDs: NotRequired[List[str]]
    StatementId: NotRequired[str]

class ApplicationPolicyStatementTypeDef(TypedDict):
    Actions: Sequence[str]
    Principals: Sequence[str]
    PrincipalOrgIDs: NotRequired[Sequence[str]]
    StatementId: NotRequired[str]

class ApplicationSummaryTypeDef(TypedDict):
    ApplicationId: str
    Author: str
    Description: str
    Name: str
    CreationTime: NotRequired[str]
    HomePageUrl: NotRequired[str]
    Labels: NotRequired[List[str]]
    SpdxLicenseId: NotRequired[str]

class CreateApplicationRequestRequestTypeDef(TypedDict):
    Author: str
    Description: str
    Name: str
    HomePageUrl: NotRequired[str]
    Labels: NotRequired[Sequence[str]]
    LicenseBody: NotRequired[str]
    LicenseUrl: NotRequired[str]
    ReadmeBody: NotRequired[str]
    ReadmeUrl: NotRequired[str]
    SemanticVersion: NotRequired[str]
    SourceCodeArchiveUrl: NotRequired[str]
    SourceCodeUrl: NotRequired[str]
    SpdxLicenseId: NotRequired[str]
    TemplateBody: NotRequired[str]
    TemplateUrl: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateApplicationVersionRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    SemanticVersion: str
    SourceCodeArchiveUrl: NotRequired[str]
    SourceCodeUrl: NotRequired[str]
    TemplateBody: NotRequired[str]
    TemplateUrl: NotRequired[str]

ParameterDefinitionTypeDef = TypedDict(
    "ParameterDefinitionTypeDef",
    {
        "Name": str,
        "ReferencedByResources": List[str],
        "AllowedPattern": NotRequired[str],
        "AllowedValues": NotRequired[List[str]],
        "ConstraintDescription": NotRequired[str],
        "DefaultValue": NotRequired[str],
        "Description": NotRequired[str],
        "MaxLength": NotRequired[int],
        "MaxValue": NotRequired[int],
        "MinLength": NotRequired[int],
        "MinValue": NotRequired[int],
        "NoEcho": NotRequired[bool],
        "Type": NotRequired[str],
    },
)

class ParameterValueTypeDef(TypedDict):
    Name: str
    Value: str

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class CreateCloudFormationTemplateRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    SemanticVersion: NotRequired[str]

class DeleteApplicationRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class GetApplicationPolicyRequestRequestTypeDef(TypedDict):
    ApplicationId: str

class GetApplicationRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    SemanticVersion: NotRequired[str]

class GetCloudFormationTemplateRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    TemplateId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListApplicationDependenciesRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    MaxItems: NotRequired[int]
    NextToken: NotRequired[str]
    SemanticVersion: NotRequired[str]

class ListApplicationVersionsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    MaxItems: NotRequired[int]
    NextToken: NotRequired[str]

class VersionSummaryTypeDef(TypedDict):
    ApplicationId: str
    CreationTime: str
    SemanticVersion: str
    SourceCodeUrl: NotRequired[str]

class ListApplicationsRequestRequestTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    NextToken: NotRequired[str]

RollbackTriggerTypeDef = TypedDict(
    "RollbackTriggerTypeDef",
    {
        "Arn": str,
        "Type": str,
    },
)

class UnshareApplicationRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    OrganizationId: str

class UpdateApplicationRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    Author: NotRequired[str]
    Description: NotRequired[str]
    HomePageUrl: NotRequired[str]
    Labels: NotRequired[Sequence[str]]
    ReadmeBody: NotRequired[str]
    ReadmeUrl: NotRequired[str]

ApplicationPolicyStatementUnionTypeDef = Union[
    ApplicationPolicyStatementTypeDef, ApplicationPolicyStatementOutputTypeDef
]

class CreateCloudFormationChangeSetResponseTypeDef(TypedDict):
    ApplicationId: str
    ChangeSetId: str
    SemanticVersion: str
    StackId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCloudFormationTemplateResponseTypeDef(TypedDict):
    ApplicationId: str
    CreationTime: str
    ExpirationTime: str
    SemanticVersion: str
    Status: StatusType
    TemplateId: str
    TemplateUrl: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetApplicationPolicyResponseTypeDef(TypedDict):
    Statements: List[ApplicationPolicyStatementOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetCloudFormationTemplateResponseTypeDef(TypedDict):
    ApplicationId: str
    CreationTime: str
    ExpirationTime: str
    SemanticVersion: str
    Status: StatusType
    TemplateId: str
    TemplateUrl: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListApplicationDependenciesResponseTypeDef(TypedDict):
    Dependencies: List[ApplicationDependencySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListApplicationsResponseTypeDef(TypedDict):
    Applications: List[ApplicationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PutApplicationPolicyResponseTypeDef(TypedDict):
    Statements: List[ApplicationPolicyStatementOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateApplicationVersionResponseTypeDef(TypedDict):
    ApplicationId: str
    CreationTime: str
    ParameterDefinitions: List[ParameterDefinitionTypeDef]
    RequiredCapabilities: List[CapabilityType]
    ResourcesSupported: bool
    SemanticVersion: str
    SourceCodeArchiveUrl: str
    SourceCodeUrl: str
    TemplateUrl: str
    ResponseMetadata: ResponseMetadataTypeDef

class VersionTypeDef(TypedDict):
    ApplicationId: str
    CreationTime: str
    ParameterDefinitions: List[ParameterDefinitionTypeDef]
    RequiredCapabilities: List[CapabilityType]
    ResourcesSupported: bool
    SemanticVersion: str
    TemplateUrl: str
    SourceCodeArchiveUrl: NotRequired[str]
    SourceCodeUrl: NotRequired[str]

class ListApplicationDependenciesRequestListApplicationDependenciesPaginateTypeDef(TypedDict):
    ApplicationId: str
    SemanticVersion: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef(TypedDict):
    ApplicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationsRequestListApplicationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationVersionsResponseTypeDef(TypedDict):
    Versions: List[VersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class RollbackConfigurationTypeDef(TypedDict):
    MonitoringTimeInMinutes: NotRequired[int]
    RollbackTriggers: NotRequired[Sequence[RollbackTriggerTypeDef]]

class PutApplicationPolicyRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    Statements: Sequence[ApplicationPolicyStatementUnionTypeDef]

class CreateApplicationResponseTypeDef(TypedDict):
    ApplicationId: str
    Author: str
    CreationTime: str
    Description: str
    HomePageUrl: str
    IsVerifiedAuthor: bool
    Labels: List[str]
    LicenseUrl: str
    Name: str
    ReadmeUrl: str
    SpdxLicenseId: str
    VerifiedAuthorUrl: str
    Version: VersionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetApplicationResponseTypeDef(TypedDict):
    ApplicationId: str
    Author: str
    CreationTime: str
    Description: str
    HomePageUrl: str
    IsVerifiedAuthor: bool
    Labels: List[str]
    LicenseUrl: str
    Name: str
    ReadmeUrl: str
    SpdxLicenseId: str
    VerifiedAuthorUrl: str
    Version: VersionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateApplicationResponseTypeDef(TypedDict):
    ApplicationId: str
    Author: str
    CreationTime: str
    Description: str
    HomePageUrl: str
    IsVerifiedAuthor: bool
    Labels: List[str]
    LicenseUrl: str
    Name: str
    ReadmeUrl: str
    SpdxLicenseId: str
    VerifiedAuthorUrl: str
    Version: VersionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCloudFormationChangeSetRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    StackName: str
    Capabilities: NotRequired[Sequence[str]]
    ChangeSetName: NotRequired[str]
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    NotificationArns: NotRequired[Sequence[str]]
    ParameterOverrides: NotRequired[Sequence[ParameterValueTypeDef]]
    ResourceTypes: NotRequired[Sequence[str]]
    RollbackConfiguration: NotRequired[RollbackConfigurationTypeDef]
    SemanticVersion: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    TemplateId: NotRequired[str]
