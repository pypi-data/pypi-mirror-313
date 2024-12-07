"""
Type annotations for controlcatalog service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controlcatalog/type_defs/)

Usage::

    ```python
    from mypy_boto3_controlcatalog.type_defs import AssociatedDomainSummaryTypeDef

    data: AssociatedDomainSummaryTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import ControlBehaviorType, ControlScopeType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AssociatedDomainSummaryTypeDef",
    "AssociatedObjectiveSummaryTypeDef",
    "CommonControlFilterTypeDef",
    "CommonControlSummaryTypeDef",
    "ControlParameterTypeDef",
    "ControlSummaryTypeDef",
    "DomainResourceFilterTypeDef",
    "DomainSummaryTypeDef",
    "GetControlRequestRequestTypeDef",
    "GetControlResponseTypeDef",
    "ImplementationDetailsTypeDef",
    "ListCommonControlsRequestListCommonControlsPaginateTypeDef",
    "ListCommonControlsRequestRequestTypeDef",
    "ListCommonControlsResponseTypeDef",
    "ListControlsRequestListControlsPaginateTypeDef",
    "ListControlsRequestRequestTypeDef",
    "ListControlsResponseTypeDef",
    "ListDomainsRequestListDomainsPaginateTypeDef",
    "ListDomainsRequestRequestTypeDef",
    "ListDomainsResponseTypeDef",
    "ListObjectivesRequestListObjectivesPaginateTypeDef",
    "ListObjectivesRequestRequestTypeDef",
    "ListObjectivesResponseTypeDef",
    "ObjectiveFilterTypeDef",
    "ObjectiveResourceFilterTypeDef",
    "ObjectiveSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "RegionConfigurationTypeDef",
    "ResponseMetadataTypeDef",
)


class AssociatedDomainSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]


class AssociatedObjectiveSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]


class ObjectiveResourceFilterTypeDef(TypedDict):
    Arn: NotRequired[str]


class ControlParameterTypeDef(TypedDict):
    Name: str


class ControlSummaryTypeDef(TypedDict):
    Arn: str
    Name: str
    Description: str


class DomainResourceFilterTypeDef(TypedDict):
    Arn: NotRequired[str]


class DomainSummaryTypeDef(TypedDict):
    Arn: str
    Name: str
    Description: str
    CreateTime: datetime
    LastUpdateTime: datetime


class GetControlRequestRequestTypeDef(TypedDict):
    ControlArn: str


ImplementationDetailsTypeDef = TypedDict(
    "ImplementationDetailsTypeDef",
    {
        "Type": str,
    },
)


class RegionConfigurationTypeDef(TypedDict):
    Scope: ControlScopeType
    DeployableRegions: NotRequired[List[str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListControlsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDomainsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ObjectiveSummaryTypeDef(TypedDict):
    Arn: str
    Name: str
    Description: str
    Domain: AssociatedDomainSummaryTypeDef
    CreateTime: datetime
    LastUpdateTime: datetime


class CommonControlSummaryTypeDef(TypedDict):
    Arn: str
    Name: str
    Description: str
    Domain: AssociatedDomainSummaryTypeDef
    Objective: AssociatedObjectiveSummaryTypeDef
    CreateTime: datetime
    LastUpdateTime: datetime


class CommonControlFilterTypeDef(TypedDict):
    Objectives: NotRequired[Sequence[ObjectiveResourceFilterTypeDef]]


class ObjectiveFilterTypeDef(TypedDict):
    Domains: NotRequired[Sequence[DomainResourceFilterTypeDef]]


class GetControlResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    Description: str
    Behavior: ControlBehaviorType
    RegionConfiguration: RegionConfigurationTypeDef
    Implementation: ImplementationDetailsTypeDef
    Parameters: List[ControlParameterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListControlsResponseTypeDef(TypedDict):
    Controls: List[ControlSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDomainsResponseTypeDef(TypedDict):
    Domains: List[DomainSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListControlsRequestListControlsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDomainsRequestListDomainsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListObjectivesResponseTypeDef(TypedDict):
    Objectives: List[ObjectiveSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListCommonControlsResponseTypeDef(TypedDict):
    CommonControls: List[CommonControlSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListCommonControlsRequestListCommonControlsPaginateTypeDef(TypedDict):
    CommonControlFilter: NotRequired[CommonControlFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCommonControlsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    CommonControlFilter: NotRequired[CommonControlFilterTypeDef]


class ListObjectivesRequestListObjectivesPaginateTypeDef(TypedDict):
    ObjectiveFilter: NotRequired[ObjectiveFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListObjectivesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ObjectiveFilter: NotRequired[ObjectiveFilterTypeDef]
