"""
Type annotations for route53-recovery-readiness service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/type_defs/)

Usage::

    ```python
    from mypy_boto3_route53_recovery_readiness.type_defs import CellOutputTypeDef

    data: CellOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import ReadinessType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "CellOutputTypeDef",
    "CreateCellRequestRequestTypeDef",
    "CreateCellResponseTypeDef",
    "CreateCrossAccountAuthorizationRequestRequestTypeDef",
    "CreateCrossAccountAuthorizationResponseTypeDef",
    "CreateReadinessCheckRequestRequestTypeDef",
    "CreateReadinessCheckResponseTypeDef",
    "CreateRecoveryGroupRequestRequestTypeDef",
    "CreateRecoveryGroupResponseTypeDef",
    "CreateResourceSetRequestRequestTypeDef",
    "CreateResourceSetResponseTypeDef",
    "DNSTargetResourceTypeDef",
    "DeleteCellRequestRequestTypeDef",
    "DeleteCrossAccountAuthorizationRequestRequestTypeDef",
    "DeleteReadinessCheckRequestRequestTypeDef",
    "DeleteRecoveryGroupRequestRequestTypeDef",
    "DeleteResourceSetRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetArchitectureRecommendationsRequestRequestTypeDef",
    "GetArchitectureRecommendationsResponseTypeDef",
    "GetCellReadinessSummaryRequestGetCellReadinessSummaryPaginateTypeDef",
    "GetCellReadinessSummaryRequestRequestTypeDef",
    "GetCellReadinessSummaryResponseTypeDef",
    "GetCellRequestRequestTypeDef",
    "GetCellResponseTypeDef",
    "GetReadinessCheckRequestRequestTypeDef",
    "GetReadinessCheckResourceStatusRequestGetReadinessCheckResourceStatusPaginateTypeDef",
    "GetReadinessCheckResourceStatusRequestRequestTypeDef",
    "GetReadinessCheckResourceStatusResponseTypeDef",
    "GetReadinessCheckResponseTypeDef",
    "GetReadinessCheckStatusRequestGetReadinessCheckStatusPaginateTypeDef",
    "GetReadinessCheckStatusRequestRequestTypeDef",
    "GetReadinessCheckStatusResponseTypeDef",
    "GetRecoveryGroupReadinessSummaryRequestGetRecoveryGroupReadinessSummaryPaginateTypeDef",
    "GetRecoveryGroupReadinessSummaryRequestRequestTypeDef",
    "GetRecoveryGroupReadinessSummaryResponseTypeDef",
    "GetRecoveryGroupRequestRequestTypeDef",
    "GetRecoveryGroupResponseTypeDef",
    "GetResourceSetRequestRequestTypeDef",
    "GetResourceSetResponseTypeDef",
    "ListCellsRequestListCellsPaginateTypeDef",
    "ListCellsRequestRequestTypeDef",
    "ListCellsResponseTypeDef",
    "ListCrossAccountAuthorizationsRequestListCrossAccountAuthorizationsPaginateTypeDef",
    "ListCrossAccountAuthorizationsRequestRequestTypeDef",
    "ListCrossAccountAuthorizationsResponseTypeDef",
    "ListReadinessChecksRequestListReadinessChecksPaginateTypeDef",
    "ListReadinessChecksRequestRequestTypeDef",
    "ListReadinessChecksResponseTypeDef",
    "ListRecoveryGroupsRequestListRecoveryGroupsPaginateTypeDef",
    "ListRecoveryGroupsRequestRequestTypeDef",
    "ListRecoveryGroupsResponseTypeDef",
    "ListResourceSetsRequestListResourceSetsPaginateTypeDef",
    "ListResourceSetsRequestRequestTypeDef",
    "ListResourceSetsResponseTypeDef",
    "ListRulesOutputTypeDef",
    "ListRulesRequestListRulesPaginateTypeDef",
    "ListRulesRequestRequestTypeDef",
    "ListRulesResponseTypeDef",
    "ListTagsForResourcesRequestRequestTypeDef",
    "ListTagsForResourcesResponseTypeDef",
    "MessageTypeDef",
    "NLBResourceTypeDef",
    "PaginatorConfigTypeDef",
    "R53ResourceRecordTypeDef",
    "ReadinessCheckOutputTypeDef",
    "ReadinessCheckSummaryTypeDef",
    "RecommendationTypeDef",
    "RecoveryGroupOutputTypeDef",
    "ResourceOutputTypeDef",
    "ResourceResultTypeDef",
    "ResourceSetOutputTypeDef",
    "ResourceTypeDef",
    "ResourceUnionTypeDef",
    "ResponseMetadataTypeDef",
    "RuleResultTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TargetResourceTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCellRequestRequestTypeDef",
    "UpdateCellResponseTypeDef",
    "UpdateReadinessCheckRequestRequestTypeDef",
    "UpdateReadinessCheckResponseTypeDef",
    "UpdateRecoveryGroupRequestRequestTypeDef",
    "UpdateRecoveryGroupResponseTypeDef",
    "UpdateResourceSetRequestRequestTypeDef",
    "UpdateResourceSetResponseTypeDef",
)


class CellOutputTypeDef(TypedDict):
    CellArn: str
    CellName: str
    Cells: List[str]
    ParentReadinessScopes: List[str]
    Tags: NotRequired[Dict[str, str]]


class CreateCellRequestRequestTypeDef(TypedDict):
    CellName: str
    Cells: NotRequired[Sequence[str]]
    Tags: NotRequired[Mapping[str, str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateCrossAccountAuthorizationRequestRequestTypeDef(TypedDict):
    CrossAccountAuthorization: str


class CreateReadinessCheckRequestRequestTypeDef(TypedDict):
    ReadinessCheckName: str
    ResourceSetName: str
    Tags: NotRequired[Mapping[str, str]]


class CreateRecoveryGroupRequestRequestTypeDef(TypedDict):
    RecoveryGroupName: str
    Cells: NotRequired[Sequence[str]]
    Tags: NotRequired[Mapping[str, str]]


class DeleteCellRequestRequestTypeDef(TypedDict):
    CellName: str


class DeleteCrossAccountAuthorizationRequestRequestTypeDef(TypedDict):
    CrossAccountAuthorization: str


class DeleteReadinessCheckRequestRequestTypeDef(TypedDict):
    ReadinessCheckName: str


class DeleteRecoveryGroupRequestRequestTypeDef(TypedDict):
    RecoveryGroupName: str


class DeleteResourceSetRequestRequestTypeDef(TypedDict):
    ResourceSetName: str


class GetArchitectureRecommendationsRequestRequestTypeDef(TypedDict):
    RecoveryGroupName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class RecommendationTypeDef(TypedDict):
    RecommendationText: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetCellReadinessSummaryRequestRequestTypeDef(TypedDict):
    CellName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ReadinessCheckSummaryTypeDef(TypedDict):
    Readiness: NotRequired[ReadinessType]
    ReadinessCheckName: NotRequired[str]


class GetCellRequestRequestTypeDef(TypedDict):
    CellName: str


class GetReadinessCheckRequestRequestTypeDef(TypedDict):
    ReadinessCheckName: str


class GetReadinessCheckResourceStatusRequestRequestTypeDef(TypedDict):
    ReadinessCheckName: str
    ResourceIdentifier: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetReadinessCheckStatusRequestRequestTypeDef(TypedDict):
    ReadinessCheckName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class MessageTypeDef(TypedDict):
    MessageText: NotRequired[str]


class ResourceResultTypeDef(TypedDict):
    LastCheckedTimestamp: datetime
    Readiness: ReadinessType
    ComponentId: NotRequired[str]
    ResourceArn: NotRequired[str]


class GetRecoveryGroupReadinessSummaryRequestRequestTypeDef(TypedDict):
    RecoveryGroupName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetRecoveryGroupRequestRequestTypeDef(TypedDict):
    RecoveryGroupName: str


class GetResourceSetRequestRequestTypeDef(TypedDict):
    ResourceSetName: str


class ListCellsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListCrossAccountAuthorizationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListReadinessChecksRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ReadinessCheckOutputTypeDef(TypedDict):
    ReadinessCheckArn: str
    ResourceSet: str
    ReadinessCheckName: NotRequired[str]
    Tags: NotRequired[Dict[str, str]]


class ListRecoveryGroupsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class RecoveryGroupOutputTypeDef(TypedDict):
    Cells: List[str]
    RecoveryGroupArn: str
    RecoveryGroupName: str
    Tags: NotRequired[Dict[str, str]]


class ListResourceSetsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListRulesOutputTypeDef(TypedDict):
    ResourceType: str
    RuleDescription: str
    RuleId: str


class ListRulesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ResourceType: NotRequired[str]


class ListTagsForResourcesRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class NLBResourceTypeDef(TypedDict):
    Arn: NotRequired[str]


class R53ResourceRecordTypeDef(TypedDict):
    DomainName: NotRequired[str]
    RecordSetId: NotRequired[str]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateCellRequestRequestTypeDef(TypedDict):
    CellName: str
    Cells: Sequence[str]


class UpdateReadinessCheckRequestRequestTypeDef(TypedDict):
    ReadinessCheckName: str
    ResourceSetName: str


class UpdateRecoveryGroupRequestRequestTypeDef(TypedDict):
    Cells: Sequence[str]
    RecoveryGroupName: str


class CreateCellResponseTypeDef(TypedDict):
    CellArn: str
    CellName: str
    Cells: List[str]
    ParentReadinessScopes: List[str]
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCrossAccountAuthorizationResponseTypeDef(TypedDict):
    CrossAccountAuthorization: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateReadinessCheckResponseTypeDef(TypedDict):
    ReadinessCheckArn: str
    ReadinessCheckName: str
    ResourceSet: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRecoveryGroupResponseTypeDef(TypedDict):
    Cells: List[str]
    RecoveryGroupArn: str
    RecoveryGroupName: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetCellResponseTypeDef(TypedDict):
    CellArn: str
    CellName: str
    Cells: List[str]
    ParentReadinessScopes: List[str]
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetReadinessCheckResponseTypeDef(TypedDict):
    ReadinessCheckArn: str
    ReadinessCheckName: str
    ResourceSet: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetRecoveryGroupResponseTypeDef(TypedDict):
    Cells: List[str]
    RecoveryGroupArn: str
    RecoveryGroupName: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListCellsResponseTypeDef(TypedDict):
    Cells: List[CellOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListCrossAccountAuthorizationsResponseTypeDef(TypedDict):
    CrossAccountAuthorizations: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourcesResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCellResponseTypeDef(TypedDict):
    CellArn: str
    CellName: str
    Cells: List[str]
    ParentReadinessScopes: List[str]
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateReadinessCheckResponseTypeDef(TypedDict):
    ReadinessCheckArn: str
    ReadinessCheckName: str
    ResourceSet: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRecoveryGroupResponseTypeDef(TypedDict):
    Cells: List[str]
    RecoveryGroupArn: str
    RecoveryGroupName: str
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetArchitectureRecommendationsResponseTypeDef(TypedDict):
    LastAuditTimestamp: datetime
    Recommendations: List[RecommendationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetCellReadinessSummaryRequestGetCellReadinessSummaryPaginateTypeDef(TypedDict):
    CellName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetReadinessCheckResourceStatusRequestGetReadinessCheckResourceStatusPaginateTypeDef(
    TypedDict
):
    ReadinessCheckName: str
    ResourceIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetReadinessCheckStatusRequestGetReadinessCheckStatusPaginateTypeDef(TypedDict):
    ReadinessCheckName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetRecoveryGroupReadinessSummaryRequestGetRecoveryGroupReadinessSummaryPaginateTypeDef(
    TypedDict
):
    RecoveryGroupName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCellsRequestListCellsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCrossAccountAuthorizationsRequestListCrossAccountAuthorizationsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListReadinessChecksRequestListReadinessChecksPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRecoveryGroupsRequestListRecoveryGroupsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourceSetsRequestListResourceSetsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRulesRequestListRulesPaginateTypeDef(TypedDict):
    ResourceType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetCellReadinessSummaryResponseTypeDef(TypedDict):
    Readiness: ReadinessType
    ReadinessChecks: List[ReadinessCheckSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetRecoveryGroupReadinessSummaryResponseTypeDef(TypedDict):
    Readiness: ReadinessType
    ReadinessChecks: List[ReadinessCheckSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RuleResultTypeDef(TypedDict):
    LastCheckedTimestamp: datetime
    Messages: List[MessageTypeDef]
    Readiness: ReadinessType
    RuleId: str


class GetReadinessCheckStatusResponseTypeDef(TypedDict):
    Messages: List[MessageTypeDef]
    Readiness: ReadinessType
    Resources: List[ResourceResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListReadinessChecksResponseTypeDef(TypedDict):
    ReadinessChecks: List[ReadinessCheckOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRecoveryGroupsResponseTypeDef(TypedDict):
    RecoveryGroups: List[RecoveryGroupOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRulesResponseTypeDef(TypedDict):
    Rules: List[ListRulesOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TargetResourceTypeDef(TypedDict):
    NLBResource: NotRequired[NLBResourceTypeDef]
    R53Resource: NotRequired[R53ResourceRecordTypeDef]


class GetReadinessCheckResourceStatusResponseTypeDef(TypedDict):
    Readiness: ReadinessType
    Rules: List[RuleResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DNSTargetResourceTypeDef(TypedDict):
    DomainName: NotRequired[str]
    HostedZoneArn: NotRequired[str]
    RecordSetId: NotRequired[str]
    RecordType: NotRequired[str]
    TargetResource: NotRequired[TargetResourceTypeDef]


class ResourceOutputTypeDef(TypedDict):
    ComponentId: NotRequired[str]
    DnsTargetResource: NotRequired[DNSTargetResourceTypeDef]
    ReadinessScopes: NotRequired[List[str]]
    ResourceArn: NotRequired[str]


class ResourceTypeDef(TypedDict):
    ComponentId: NotRequired[str]
    DnsTargetResource: NotRequired[DNSTargetResourceTypeDef]
    ReadinessScopes: NotRequired[Sequence[str]]
    ResourceArn: NotRequired[str]


class CreateResourceSetResponseTypeDef(TypedDict):
    ResourceSetArn: str
    ResourceSetName: str
    ResourceSetType: str
    Resources: List[ResourceOutputTypeDef]
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetResourceSetResponseTypeDef(TypedDict):
    ResourceSetArn: str
    ResourceSetName: str
    ResourceSetType: str
    Resources: List[ResourceOutputTypeDef]
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ResourceSetOutputTypeDef(TypedDict):
    ResourceSetArn: str
    ResourceSetName: str
    ResourceSetType: str
    Resources: List[ResourceOutputTypeDef]
    Tags: NotRequired[Dict[str, str]]


class UpdateResourceSetResponseTypeDef(TypedDict):
    ResourceSetArn: str
    ResourceSetName: str
    ResourceSetType: str
    Resources: List[ResourceOutputTypeDef]
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


ResourceUnionTypeDef = Union[ResourceTypeDef, ResourceOutputTypeDef]


class UpdateResourceSetRequestRequestTypeDef(TypedDict):
    ResourceSetName: str
    ResourceSetType: str
    Resources: Sequence[ResourceTypeDef]


class ListResourceSetsResponseTypeDef(TypedDict):
    ResourceSets: List[ResourceSetOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateResourceSetRequestRequestTypeDef(TypedDict):
    ResourceSetName: str
    ResourceSetType: str
    Resources: Sequence[ResourceUnionTypeDef]
    Tags: NotRequired[Mapping[str, str]]
