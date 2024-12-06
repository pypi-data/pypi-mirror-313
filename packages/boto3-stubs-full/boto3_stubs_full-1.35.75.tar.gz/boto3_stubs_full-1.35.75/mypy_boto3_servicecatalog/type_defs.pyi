"""
Type annotations for servicecatalog service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog/type_defs/)

Usage::

    ```python
    from mypy_boto3_servicecatalog.type_defs import AcceptPortfolioShareInputRequestTypeDef

    data: AcceptPortfolioShareInputRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AccessLevelFilterKeyType,
    AccessStatusType,
    ChangeActionType,
    CopyProductStatusType,
    DescribePortfolioShareTypeType,
    EngineWorkflowStatusType,
    EvaluationTypeType,
    LastSyncStatusType,
    OrganizationNodeTypeType,
    PortfolioShareTypeType,
    PrincipalTypeType,
    ProductTypeType,
    ProductViewFilterByType,
    ProductViewSortByType,
    PropertyKeyType,
    ProvisionedProductPlanStatusType,
    ProvisionedProductStatusType,
    ProvisioningArtifactGuidanceType,
    ProvisioningArtifactTypeType,
    RecordStatusType,
    ReplacementType,
    RequiresRecreationType,
    ResourceAttributeType,
    ServiceActionAssociationErrorCodeType,
    ServiceActionDefinitionKeyType,
    ShareStatusType,
    SortOrderType,
    StackInstanceStatusType,
    StackSetOperationTypeType,
    StatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AcceptPortfolioShareInputRequestTypeDef",
    "AccessLevelFilterTypeDef",
    "AssociateBudgetWithResourceInputRequestTypeDef",
    "AssociatePrincipalWithPortfolioInputRequestTypeDef",
    "AssociateProductWithPortfolioInputRequestTypeDef",
    "AssociateServiceActionWithProvisioningArtifactInputRequestTypeDef",
    "AssociateTagOptionWithResourceInputRequestTypeDef",
    "BatchAssociateServiceActionWithProvisioningArtifactInputRequestTypeDef",
    "BatchAssociateServiceActionWithProvisioningArtifactOutputTypeDef",
    "BatchDisassociateServiceActionFromProvisioningArtifactInputRequestTypeDef",
    "BatchDisassociateServiceActionFromProvisioningArtifactOutputTypeDef",
    "BudgetDetailTypeDef",
    "CloudWatchDashboardTypeDef",
    "CodeStarParametersTypeDef",
    "ConstraintDetailTypeDef",
    "ConstraintSummaryTypeDef",
    "CopyProductInputRequestTypeDef",
    "CopyProductOutputTypeDef",
    "CreateConstraintInputRequestTypeDef",
    "CreateConstraintOutputTypeDef",
    "CreatePortfolioInputRequestTypeDef",
    "CreatePortfolioOutputTypeDef",
    "CreatePortfolioShareInputRequestTypeDef",
    "CreatePortfolioShareOutputTypeDef",
    "CreateProductInputRequestTypeDef",
    "CreateProductOutputTypeDef",
    "CreateProvisionedProductPlanInputRequestTypeDef",
    "CreateProvisionedProductPlanOutputTypeDef",
    "CreateProvisioningArtifactInputRequestTypeDef",
    "CreateProvisioningArtifactOutputTypeDef",
    "CreateServiceActionInputRequestTypeDef",
    "CreateServiceActionOutputTypeDef",
    "CreateTagOptionInputRequestTypeDef",
    "CreateTagOptionOutputTypeDef",
    "DeleteConstraintInputRequestTypeDef",
    "DeletePortfolioInputRequestTypeDef",
    "DeletePortfolioShareInputRequestTypeDef",
    "DeletePortfolioShareOutputTypeDef",
    "DeleteProductInputRequestTypeDef",
    "DeleteProvisionedProductPlanInputRequestTypeDef",
    "DeleteProvisioningArtifactInputRequestTypeDef",
    "DeleteServiceActionInputRequestTypeDef",
    "DeleteTagOptionInputRequestTypeDef",
    "DescribeConstraintInputRequestTypeDef",
    "DescribeConstraintOutputTypeDef",
    "DescribeCopyProductStatusInputRequestTypeDef",
    "DescribeCopyProductStatusOutputTypeDef",
    "DescribePortfolioInputRequestTypeDef",
    "DescribePortfolioOutputTypeDef",
    "DescribePortfolioShareStatusInputRequestTypeDef",
    "DescribePortfolioShareStatusOutputTypeDef",
    "DescribePortfolioSharesInputRequestTypeDef",
    "DescribePortfolioSharesOutputTypeDef",
    "DescribeProductAsAdminInputRequestTypeDef",
    "DescribeProductAsAdminOutputTypeDef",
    "DescribeProductInputRequestTypeDef",
    "DescribeProductOutputTypeDef",
    "DescribeProductViewInputRequestTypeDef",
    "DescribeProductViewOutputTypeDef",
    "DescribeProvisionedProductInputRequestTypeDef",
    "DescribeProvisionedProductOutputTypeDef",
    "DescribeProvisionedProductPlanInputRequestTypeDef",
    "DescribeProvisionedProductPlanOutputTypeDef",
    "DescribeProvisioningArtifactInputRequestTypeDef",
    "DescribeProvisioningArtifactOutputTypeDef",
    "DescribeProvisioningParametersInputRequestTypeDef",
    "DescribeProvisioningParametersOutputTypeDef",
    "DescribeRecordInputRequestTypeDef",
    "DescribeRecordOutputTypeDef",
    "DescribeServiceActionExecutionParametersInputRequestTypeDef",
    "DescribeServiceActionExecutionParametersOutputTypeDef",
    "DescribeServiceActionInputRequestTypeDef",
    "DescribeServiceActionOutputTypeDef",
    "DescribeTagOptionInputRequestTypeDef",
    "DescribeTagOptionOutputTypeDef",
    "DisassociateBudgetFromResourceInputRequestTypeDef",
    "DisassociatePrincipalFromPortfolioInputRequestTypeDef",
    "DisassociateProductFromPortfolioInputRequestTypeDef",
    "DisassociateServiceActionFromProvisioningArtifactInputRequestTypeDef",
    "DisassociateTagOptionFromResourceInputRequestTypeDef",
    "EngineWorkflowResourceIdentifierTypeDef",
    "ExecuteProvisionedProductPlanInputRequestTypeDef",
    "ExecuteProvisionedProductPlanOutputTypeDef",
    "ExecuteProvisionedProductServiceActionInputRequestTypeDef",
    "ExecuteProvisionedProductServiceActionOutputTypeDef",
    "ExecutionParameterTypeDef",
    "FailedServiceActionAssociationTypeDef",
    "GetAWSOrganizationsAccessStatusOutputTypeDef",
    "GetProvisionedProductOutputsInputRequestTypeDef",
    "GetProvisionedProductOutputsOutputTypeDef",
    "ImportAsProvisionedProductInputRequestTypeDef",
    "ImportAsProvisionedProductOutputTypeDef",
    "LastSyncTypeDef",
    "LaunchPathSummaryTypeDef",
    "LaunchPathTypeDef",
    "ListAcceptedPortfolioSharesInputListAcceptedPortfolioSharesPaginateTypeDef",
    "ListAcceptedPortfolioSharesInputRequestTypeDef",
    "ListAcceptedPortfolioSharesOutputTypeDef",
    "ListBudgetsForResourceInputRequestTypeDef",
    "ListBudgetsForResourceOutputTypeDef",
    "ListConstraintsForPortfolioInputListConstraintsForPortfolioPaginateTypeDef",
    "ListConstraintsForPortfolioInputRequestTypeDef",
    "ListConstraintsForPortfolioOutputTypeDef",
    "ListLaunchPathsInputListLaunchPathsPaginateTypeDef",
    "ListLaunchPathsInputRequestTypeDef",
    "ListLaunchPathsOutputTypeDef",
    "ListOrganizationPortfolioAccessInputListOrganizationPortfolioAccessPaginateTypeDef",
    "ListOrganizationPortfolioAccessInputRequestTypeDef",
    "ListOrganizationPortfolioAccessOutputTypeDef",
    "ListPortfolioAccessInputRequestTypeDef",
    "ListPortfolioAccessOutputTypeDef",
    "ListPortfoliosForProductInputListPortfoliosForProductPaginateTypeDef",
    "ListPortfoliosForProductInputRequestTypeDef",
    "ListPortfoliosForProductOutputTypeDef",
    "ListPortfoliosInputListPortfoliosPaginateTypeDef",
    "ListPortfoliosInputRequestTypeDef",
    "ListPortfoliosOutputTypeDef",
    "ListPrincipalsForPortfolioInputListPrincipalsForPortfolioPaginateTypeDef",
    "ListPrincipalsForPortfolioInputRequestTypeDef",
    "ListPrincipalsForPortfolioOutputTypeDef",
    "ListProvisionedProductPlansInputListProvisionedProductPlansPaginateTypeDef",
    "ListProvisionedProductPlansInputRequestTypeDef",
    "ListProvisionedProductPlansOutputTypeDef",
    "ListProvisioningArtifactsForServiceActionInputListProvisioningArtifactsForServiceActionPaginateTypeDef",
    "ListProvisioningArtifactsForServiceActionInputRequestTypeDef",
    "ListProvisioningArtifactsForServiceActionOutputTypeDef",
    "ListProvisioningArtifactsInputRequestTypeDef",
    "ListProvisioningArtifactsOutputTypeDef",
    "ListRecordHistoryInputListRecordHistoryPaginateTypeDef",
    "ListRecordHistoryInputRequestTypeDef",
    "ListRecordHistoryOutputTypeDef",
    "ListRecordHistorySearchFilterTypeDef",
    "ListResourcesForTagOptionInputListResourcesForTagOptionPaginateTypeDef",
    "ListResourcesForTagOptionInputRequestTypeDef",
    "ListResourcesForTagOptionOutputTypeDef",
    "ListServiceActionsForProvisioningArtifactInputListServiceActionsForProvisioningArtifactPaginateTypeDef",
    "ListServiceActionsForProvisioningArtifactInputRequestTypeDef",
    "ListServiceActionsForProvisioningArtifactOutputTypeDef",
    "ListServiceActionsInputListServiceActionsPaginateTypeDef",
    "ListServiceActionsInputRequestTypeDef",
    "ListServiceActionsOutputTypeDef",
    "ListStackInstancesForProvisionedProductInputRequestTypeDef",
    "ListStackInstancesForProvisionedProductOutputTypeDef",
    "ListTagOptionsFiltersTypeDef",
    "ListTagOptionsInputListTagOptionsPaginateTypeDef",
    "ListTagOptionsInputRequestTypeDef",
    "ListTagOptionsOutputTypeDef",
    "NotifyProvisionProductEngineWorkflowResultInputRequestTypeDef",
    "NotifyTerminateProvisionedProductEngineWorkflowResultInputRequestTypeDef",
    "NotifyUpdateProvisionedProductEngineWorkflowResultInputRequestTypeDef",
    "OrganizationNodeTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterConstraintsTypeDef",
    "PortfolioDetailTypeDef",
    "PortfolioShareDetailTypeDef",
    "PrincipalTypeDef",
    "ProductViewAggregationValueTypeDef",
    "ProductViewDetailTypeDef",
    "ProductViewSummaryTypeDef",
    "ProvisionProductInputRequestTypeDef",
    "ProvisionProductOutputTypeDef",
    "ProvisionedProductAttributeTypeDef",
    "ProvisionedProductDetailTypeDef",
    "ProvisionedProductPlanDetailsTypeDef",
    "ProvisionedProductPlanSummaryTypeDef",
    "ProvisioningArtifactDetailTypeDef",
    "ProvisioningArtifactOutputTypeDef",
    "ProvisioningArtifactParameterTypeDef",
    "ProvisioningArtifactPreferencesTypeDef",
    "ProvisioningArtifactPropertiesTypeDef",
    "ProvisioningArtifactSummaryTypeDef",
    "ProvisioningArtifactTypeDef",
    "ProvisioningArtifactViewTypeDef",
    "ProvisioningParameterTypeDef",
    "ProvisioningPreferencesTypeDef",
    "RecordDetailTypeDef",
    "RecordErrorTypeDef",
    "RecordOutputTypeDef",
    "RecordTagTypeDef",
    "RejectPortfolioShareInputRequestTypeDef",
    "ResourceChangeDetailTypeDef",
    "ResourceChangeTypeDef",
    "ResourceDetailTypeDef",
    "ResourceTargetDefinitionTypeDef",
    "ResponseMetadataTypeDef",
    "ScanProvisionedProductsInputRequestTypeDef",
    "ScanProvisionedProductsInputScanProvisionedProductsPaginateTypeDef",
    "ScanProvisionedProductsOutputTypeDef",
    "SearchProductsAsAdminInputRequestTypeDef",
    "SearchProductsAsAdminInputSearchProductsAsAdminPaginateTypeDef",
    "SearchProductsAsAdminOutputTypeDef",
    "SearchProductsInputRequestTypeDef",
    "SearchProductsOutputTypeDef",
    "SearchProvisionedProductsInputRequestTypeDef",
    "SearchProvisionedProductsOutputTypeDef",
    "ServiceActionAssociationTypeDef",
    "ServiceActionDetailTypeDef",
    "ServiceActionSummaryTypeDef",
    "ShareDetailsTypeDef",
    "ShareErrorTypeDef",
    "SourceConnectionDetailTypeDef",
    "SourceConnectionParametersTypeDef",
    "SourceConnectionTypeDef",
    "StackInstanceTypeDef",
    "TagOptionDetailTypeDef",
    "TagOptionSummaryTypeDef",
    "TagTypeDef",
    "TerminateProvisionedProductInputRequestTypeDef",
    "TerminateProvisionedProductOutputTypeDef",
    "UniqueTagResourceIdentifierTypeDef",
    "UpdateConstraintInputRequestTypeDef",
    "UpdateConstraintOutputTypeDef",
    "UpdatePortfolioInputRequestTypeDef",
    "UpdatePortfolioOutputTypeDef",
    "UpdatePortfolioShareInputRequestTypeDef",
    "UpdatePortfolioShareOutputTypeDef",
    "UpdateProductInputRequestTypeDef",
    "UpdateProductOutputTypeDef",
    "UpdateProvisionedProductInputRequestTypeDef",
    "UpdateProvisionedProductOutputTypeDef",
    "UpdateProvisionedProductPropertiesInputRequestTypeDef",
    "UpdateProvisionedProductPropertiesOutputTypeDef",
    "UpdateProvisioningArtifactInputRequestTypeDef",
    "UpdateProvisioningArtifactOutputTypeDef",
    "UpdateProvisioningParameterTypeDef",
    "UpdateProvisioningPreferencesTypeDef",
    "UpdateServiceActionInputRequestTypeDef",
    "UpdateServiceActionOutputTypeDef",
    "UpdateTagOptionInputRequestTypeDef",
    "UpdateTagOptionOutputTypeDef",
    "UsageInstructionTypeDef",
)

class AcceptPortfolioShareInputRequestTypeDef(TypedDict):
    PortfolioId: str
    AcceptLanguage: NotRequired[str]
    PortfolioShareType: NotRequired[PortfolioShareTypeType]

class AccessLevelFilterTypeDef(TypedDict):
    Key: NotRequired[AccessLevelFilterKeyType]
    Value: NotRequired[str]

class AssociateBudgetWithResourceInputRequestTypeDef(TypedDict):
    BudgetName: str
    ResourceId: str

class AssociatePrincipalWithPortfolioInputRequestTypeDef(TypedDict):
    PortfolioId: str
    PrincipalARN: str
    PrincipalType: PrincipalTypeType
    AcceptLanguage: NotRequired[str]

class AssociateProductWithPortfolioInputRequestTypeDef(TypedDict):
    ProductId: str
    PortfolioId: str
    AcceptLanguage: NotRequired[str]
    SourcePortfolioId: NotRequired[str]

class AssociateServiceActionWithProvisioningArtifactInputRequestTypeDef(TypedDict):
    ProductId: str
    ProvisioningArtifactId: str
    ServiceActionId: str
    AcceptLanguage: NotRequired[str]
    IdempotencyToken: NotRequired[str]

class AssociateTagOptionWithResourceInputRequestTypeDef(TypedDict):
    ResourceId: str
    TagOptionId: str

class ServiceActionAssociationTypeDef(TypedDict):
    ServiceActionId: str
    ProductId: str
    ProvisioningArtifactId: str

class FailedServiceActionAssociationTypeDef(TypedDict):
    ServiceActionId: NotRequired[str]
    ProductId: NotRequired[str]
    ProvisioningArtifactId: NotRequired[str]
    ErrorCode: NotRequired[ServiceActionAssociationErrorCodeType]
    ErrorMessage: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BudgetDetailTypeDef(TypedDict):
    BudgetName: NotRequired[str]

class CloudWatchDashboardTypeDef(TypedDict):
    Name: NotRequired[str]

class CodeStarParametersTypeDef(TypedDict):
    ConnectionArn: str
    Repository: str
    Branch: str
    ArtifactPath: str

ConstraintDetailTypeDef = TypedDict(
    "ConstraintDetailTypeDef",
    {
        "ConstraintId": NotRequired[str],
        "Type": NotRequired[str],
        "Description": NotRequired[str],
        "Owner": NotRequired[str],
        "ProductId": NotRequired[str],
        "PortfolioId": NotRequired[str],
    },
)
ConstraintSummaryTypeDef = TypedDict(
    "ConstraintSummaryTypeDef",
    {
        "Type": NotRequired[str],
        "Description": NotRequired[str],
    },
)

class CopyProductInputRequestTypeDef(TypedDict):
    SourceProductArn: str
    IdempotencyToken: str
    AcceptLanguage: NotRequired[str]
    TargetProductId: NotRequired[str]
    TargetProductName: NotRequired[str]
    SourceProvisioningArtifactIdentifiers: NotRequired[Sequence[Mapping[Literal["Id"], str]]]
    CopyOptions: NotRequired[Sequence[Literal["CopyTags"]]]

CreateConstraintInputRequestTypeDef = TypedDict(
    "CreateConstraintInputRequestTypeDef",
    {
        "PortfolioId": str,
        "ProductId": str,
        "Parameters": str,
        "Type": str,
        "IdempotencyToken": str,
        "AcceptLanguage": NotRequired[str],
        "Description": NotRequired[str],
    },
)

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class PortfolioDetailTypeDef(TypedDict):
    Id: NotRequired[str]
    ARN: NotRequired[str]
    DisplayName: NotRequired[str]
    Description: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    ProviderName: NotRequired[str]

OrganizationNodeTypeDef = TypedDict(
    "OrganizationNodeTypeDef",
    {
        "Type": NotRequired[OrganizationNodeTypeType],
        "Value": NotRequired[str],
    },
)
ProvisioningArtifactPropertiesTypeDef = TypedDict(
    "ProvisioningArtifactPropertiesTypeDef",
    {
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "Info": NotRequired[Mapping[str, str]],
        "Type": NotRequired[ProvisioningArtifactTypeType],
        "DisableTemplateValidation": NotRequired[bool],
    },
)
ProvisioningArtifactDetailTypeDef = TypedDict(
    "ProvisioningArtifactDetailTypeDef",
    {
        "Id": NotRequired[str],
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "Type": NotRequired[ProvisioningArtifactTypeType],
        "CreatedTime": NotRequired[datetime],
        "Active": NotRequired[bool],
        "Guidance": NotRequired[ProvisioningArtifactGuidanceType],
        "SourceRevision": NotRequired[str],
    },
)

class UpdateProvisioningParameterTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]
    UsePreviousValue: NotRequired[bool]

class CreateServiceActionInputRequestTypeDef(TypedDict):
    Name: str
    DefinitionType: Literal["SSM_AUTOMATION"]
    Definition: Mapping[ServiceActionDefinitionKeyType, str]
    IdempotencyToken: str
    Description: NotRequired[str]
    AcceptLanguage: NotRequired[str]

class CreateTagOptionInputRequestTypeDef(TypedDict):
    Key: str
    Value: str

class TagOptionDetailTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]
    Active: NotRequired[bool]
    Id: NotRequired[str]
    Owner: NotRequired[str]

class DeleteConstraintInputRequestTypeDef(TypedDict):
    Id: str
    AcceptLanguage: NotRequired[str]

class DeletePortfolioInputRequestTypeDef(TypedDict):
    Id: str
    AcceptLanguage: NotRequired[str]

class DeleteProductInputRequestTypeDef(TypedDict):
    Id: str
    AcceptLanguage: NotRequired[str]

class DeleteProvisionedProductPlanInputRequestTypeDef(TypedDict):
    PlanId: str
    AcceptLanguage: NotRequired[str]
    IgnoreErrors: NotRequired[bool]

class DeleteProvisioningArtifactInputRequestTypeDef(TypedDict):
    ProductId: str
    ProvisioningArtifactId: str
    AcceptLanguage: NotRequired[str]

class DeleteServiceActionInputRequestTypeDef(TypedDict):
    Id: str
    AcceptLanguage: NotRequired[str]
    IdempotencyToken: NotRequired[str]

class DeleteTagOptionInputRequestTypeDef(TypedDict):
    Id: str

class DescribeConstraintInputRequestTypeDef(TypedDict):
    Id: str
    AcceptLanguage: NotRequired[str]

class DescribeCopyProductStatusInputRequestTypeDef(TypedDict):
    CopyProductToken: str
    AcceptLanguage: NotRequired[str]

class DescribePortfolioInputRequestTypeDef(TypedDict):
    Id: str
    AcceptLanguage: NotRequired[str]

class DescribePortfolioShareStatusInputRequestTypeDef(TypedDict):
    PortfolioShareToken: str

DescribePortfolioSharesInputRequestTypeDef = TypedDict(
    "DescribePortfolioSharesInputRequestTypeDef",
    {
        "PortfolioId": str,
        "Type": DescribePortfolioShareTypeType,
        "PageToken": NotRequired[str],
        "PageSize": NotRequired[int],
    },
)
PortfolioShareDetailTypeDef = TypedDict(
    "PortfolioShareDetailTypeDef",
    {
        "PrincipalId": NotRequired[str],
        "Type": NotRequired[DescribePortfolioShareTypeType],
        "Accepted": NotRequired[bool],
        "ShareTagOptions": NotRequired[bool],
        "SharePrincipals": NotRequired[bool],
    },
)

class DescribeProductAsAdminInputRequestTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    Id: NotRequired[str]
    Name: NotRequired[str]
    SourcePortfolioId: NotRequired[str]

class ProvisioningArtifactSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    ProvisioningArtifactMetadata: NotRequired[Dict[str, str]]

class DescribeProductInputRequestTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    Id: NotRequired[str]
    Name: NotRequired[str]

class LaunchPathTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]

ProductViewSummaryTypeDef = TypedDict(
    "ProductViewSummaryTypeDef",
    {
        "Id": NotRequired[str],
        "ProductId": NotRequired[str],
        "Name": NotRequired[str],
        "Owner": NotRequired[str],
        "ShortDescription": NotRequired[str],
        "Type": NotRequired[ProductTypeType],
        "Distributor": NotRequired[str],
        "HasDefaultPath": NotRequired[bool],
        "SupportEmail": NotRequired[str],
        "SupportDescription": NotRequired[str],
        "SupportUrl": NotRequired[str],
    },
)

class ProvisioningArtifactTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    Guidance: NotRequired[ProvisioningArtifactGuidanceType]

class DescribeProductViewInputRequestTypeDef(TypedDict):
    Id: str
    AcceptLanguage: NotRequired[str]

class DescribeProvisionedProductInputRequestTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    Id: NotRequired[str]
    Name: NotRequired[str]

ProvisionedProductDetailTypeDef = TypedDict(
    "ProvisionedProductDetailTypeDef",
    {
        "Name": NotRequired[str],
        "Arn": NotRequired[str],
        "Type": NotRequired[str],
        "Id": NotRequired[str],
        "Status": NotRequired[ProvisionedProductStatusType],
        "StatusMessage": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
        "IdempotencyToken": NotRequired[str],
        "LastRecordId": NotRequired[str],
        "LastProvisioningRecordId": NotRequired[str],
        "LastSuccessfulProvisioningRecordId": NotRequired[str],
        "ProductId": NotRequired[str],
        "ProvisioningArtifactId": NotRequired[str],
        "LaunchRoleArn": NotRequired[str],
    },
)

class DescribeProvisionedProductPlanInputRequestTypeDef(TypedDict):
    PlanId: str
    AcceptLanguage: NotRequired[str]
    PageSize: NotRequired[int]
    PageToken: NotRequired[str]

class DescribeProvisioningArtifactInputRequestTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    ProvisioningArtifactId: NotRequired[str]
    ProductId: NotRequired[str]
    ProvisioningArtifactName: NotRequired[str]
    ProductName: NotRequired[str]
    Verbose: NotRequired[bool]
    IncludeProvisioningArtifactParameters: NotRequired[bool]

class DescribeProvisioningParametersInputRequestTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    ProductId: NotRequired[str]
    ProductName: NotRequired[str]
    ProvisioningArtifactId: NotRequired[str]
    ProvisioningArtifactName: NotRequired[str]
    PathId: NotRequired[str]
    PathName: NotRequired[str]

class ProvisioningArtifactOutputTypeDef(TypedDict):
    Key: NotRequired[str]
    Description: NotRequired[str]

class ProvisioningArtifactPreferencesTypeDef(TypedDict):
    StackSetAccounts: NotRequired[List[str]]
    StackSetRegions: NotRequired[List[str]]

class TagOptionSummaryTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[List[str]]

UsageInstructionTypeDef = TypedDict(
    "UsageInstructionTypeDef",
    {
        "Type": NotRequired[str],
        "Value": NotRequired[str],
    },
)

class DescribeRecordInputRequestTypeDef(TypedDict):
    Id: str
    AcceptLanguage: NotRequired[str]
    PageToken: NotRequired[str]
    PageSize: NotRequired[int]

class RecordOutputTypeDef(TypedDict):
    OutputKey: NotRequired[str]
    OutputValue: NotRequired[str]
    Description: NotRequired[str]

class DescribeServiceActionExecutionParametersInputRequestTypeDef(TypedDict):
    ProvisionedProductId: str
    ServiceActionId: str
    AcceptLanguage: NotRequired[str]

ExecutionParameterTypeDef = TypedDict(
    "ExecutionParameterTypeDef",
    {
        "Name": NotRequired[str],
        "Type": NotRequired[str],
        "DefaultValues": NotRequired[List[str]],
    },
)

class DescribeServiceActionInputRequestTypeDef(TypedDict):
    Id: str
    AcceptLanguage: NotRequired[str]

class DescribeTagOptionInputRequestTypeDef(TypedDict):
    Id: str

class DisassociateBudgetFromResourceInputRequestTypeDef(TypedDict):
    BudgetName: str
    ResourceId: str

class DisassociatePrincipalFromPortfolioInputRequestTypeDef(TypedDict):
    PortfolioId: str
    PrincipalARN: str
    AcceptLanguage: NotRequired[str]
    PrincipalType: NotRequired[PrincipalTypeType]

class DisassociateProductFromPortfolioInputRequestTypeDef(TypedDict):
    ProductId: str
    PortfolioId: str
    AcceptLanguage: NotRequired[str]

class DisassociateServiceActionFromProvisioningArtifactInputRequestTypeDef(TypedDict):
    ProductId: str
    ProvisioningArtifactId: str
    ServiceActionId: str
    AcceptLanguage: NotRequired[str]
    IdempotencyToken: NotRequired[str]

class DisassociateTagOptionFromResourceInputRequestTypeDef(TypedDict):
    ResourceId: str
    TagOptionId: str

class UniqueTagResourceIdentifierTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]

class ExecuteProvisionedProductPlanInputRequestTypeDef(TypedDict):
    PlanId: str
    IdempotencyToken: str
    AcceptLanguage: NotRequired[str]

class ExecuteProvisionedProductServiceActionInputRequestTypeDef(TypedDict):
    ProvisionedProductId: str
    ServiceActionId: str
    ExecuteToken: str
    AcceptLanguage: NotRequired[str]
    Parameters: NotRequired[Mapping[str, Sequence[str]]]

class GetProvisionedProductOutputsInputRequestTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    ProvisionedProductId: NotRequired[str]
    ProvisionedProductName: NotRequired[str]
    OutputKeys: NotRequired[Sequence[str]]
    PageSize: NotRequired[int]
    PageToken: NotRequired[str]

class ImportAsProvisionedProductInputRequestTypeDef(TypedDict):
    ProductId: str
    ProvisioningArtifactId: str
    ProvisionedProductName: str
    PhysicalId: str
    IdempotencyToken: str
    AcceptLanguage: NotRequired[str]

class LastSyncTypeDef(TypedDict):
    LastSyncTime: NotRequired[datetime]
    LastSyncStatus: NotRequired[LastSyncStatusType]
    LastSyncStatusMessage: NotRequired[str]
    LastSuccessfulSyncTime: NotRequired[datetime]
    LastSuccessfulSyncProvisioningArtifactId: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAcceptedPortfolioSharesInputRequestTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    PageToken: NotRequired[str]
    PageSize: NotRequired[int]
    PortfolioShareType: NotRequired[PortfolioShareTypeType]

class ListBudgetsForResourceInputRequestTypeDef(TypedDict):
    ResourceId: str
    AcceptLanguage: NotRequired[str]
    PageSize: NotRequired[int]
    PageToken: NotRequired[str]

class ListConstraintsForPortfolioInputRequestTypeDef(TypedDict):
    PortfolioId: str
    AcceptLanguage: NotRequired[str]
    ProductId: NotRequired[str]
    PageSize: NotRequired[int]
    PageToken: NotRequired[str]

class ListLaunchPathsInputRequestTypeDef(TypedDict):
    ProductId: str
    AcceptLanguage: NotRequired[str]
    PageSize: NotRequired[int]
    PageToken: NotRequired[str]

class ListOrganizationPortfolioAccessInputRequestTypeDef(TypedDict):
    PortfolioId: str
    OrganizationNodeType: OrganizationNodeTypeType
    AcceptLanguage: NotRequired[str]
    PageToken: NotRequired[str]
    PageSize: NotRequired[int]

class ListPortfolioAccessInputRequestTypeDef(TypedDict):
    PortfolioId: str
    AcceptLanguage: NotRequired[str]
    OrganizationParentId: NotRequired[str]
    PageToken: NotRequired[str]
    PageSize: NotRequired[int]

class ListPortfoliosForProductInputRequestTypeDef(TypedDict):
    ProductId: str
    AcceptLanguage: NotRequired[str]
    PageToken: NotRequired[str]
    PageSize: NotRequired[int]

class ListPortfoliosInputRequestTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    PageToken: NotRequired[str]
    PageSize: NotRequired[int]

class ListPrincipalsForPortfolioInputRequestTypeDef(TypedDict):
    PortfolioId: str
    AcceptLanguage: NotRequired[str]
    PageSize: NotRequired[int]
    PageToken: NotRequired[str]

class PrincipalTypeDef(TypedDict):
    PrincipalARN: NotRequired[str]
    PrincipalType: NotRequired[PrincipalTypeType]

class ProvisionedProductPlanSummaryTypeDef(TypedDict):
    PlanName: NotRequired[str]
    PlanId: NotRequired[str]
    ProvisionProductId: NotRequired[str]
    ProvisionProductName: NotRequired[str]
    PlanType: NotRequired[Literal["CLOUDFORMATION"]]
    ProvisioningArtifactId: NotRequired[str]

class ListProvisioningArtifactsForServiceActionInputRequestTypeDef(TypedDict):
    ServiceActionId: str
    PageSize: NotRequired[int]
    PageToken: NotRequired[str]
    AcceptLanguage: NotRequired[str]

class ListProvisioningArtifactsInputRequestTypeDef(TypedDict):
    ProductId: str
    AcceptLanguage: NotRequired[str]

class ListRecordHistorySearchFilterTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]

class ListResourcesForTagOptionInputRequestTypeDef(TypedDict):
    TagOptionId: str
    ResourceType: NotRequired[str]
    PageSize: NotRequired[int]
    PageToken: NotRequired[str]

class ResourceDetailTypeDef(TypedDict):
    Id: NotRequired[str]
    ARN: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    CreatedTime: NotRequired[datetime]

class ListServiceActionsForProvisioningArtifactInputRequestTypeDef(TypedDict):
    ProductId: str
    ProvisioningArtifactId: str
    PageSize: NotRequired[int]
    PageToken: NotRequired[str]
    AcceptLanguage: NotRequired[str]

class ServiceActionSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    DefinitionType: NotRequired[Literal["SSM_AUTOMATION"]]

class ListServiceActionsInputRequestTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    PageSize: NotRequired[int]
    PageToken: NotRequired[str]

class ListStackInstancesForProvisionedProductInputRequestTypeDef(TypedDict):
    ProvisionedProductId: str
    AcceptLanguage: NotRequired[str]
    PageToken: NotRequired[str]
    PageSize: NotRequired[int]

class StackInstanceTypeDef(TypedDict):
    Account: NotRequired[str]
    Region: NotRequired[str]
    StackInstanceStatus: NotRequired[StackInstanceStatusType]

class ListTagOptionsFiltersTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]
    Active: NotRequired[bool]

class NotifyTerminateProvisionedProductEngineWorkflowResultInputRequestTypeDef(TypedDict):
    WorkflowToken: str
    RecordId: str
    Status: EngineWorkflowStatusType
    IdempotencyToken: str
    FailureReason: NotRequired[str]

class ParameterConstraintsTypeDef(TypedDict):
    AllowedValues: NotRequired[List[str]]
    AllowedPattern: NotRequired[str]
    ConstraintDescription: NotRequired[str]
    MaxLength: NotRequired[str]
    MinLength: NotRequired[str]
    MaxValue: NotRequired[str]
    MinValue: NotRequired[str]

class ProductViewAggregationValueTypeDef(TypedDict):
    Value: NotRequired[str]
    ApproximateCount: NotRequired[int]

class ProvisioningParameterTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]

class ProvisioningPreferencesTypeDef(TypedDict):
    StackSetAccounts: NotRequired[Sequence[str]]
    StackSetRegions: NotRequired[Sequence[str]]
    StackSetFailureToleranceCount: NotRequired[int]
    StackSetFailureTolerancePercentage: NotRequired[int]
    StackSetMaxConcurrencyCount: NotRequired[int]
    StackSetMaxConcurrencyPercentage: NotRequired[int]

class RecordErrorTypeDef(TypedDict):
    Code: NotRequired[str]
    Description: NotRequired[str]

class RecordTagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]

class RejectPortfolioShareInputRequestTypeDef(TypedDict):
    PortfolioId: str
    AcceptLanguage: NotRequired[str]
    PortfolioShareType: NotRequired[PortfolioShareTypeType]

class ResourceTargetDefinitionTypeDef(TypedDict):
    Attribute: NotRequired[ResourceAttributeType]
    Name: NotRequired[str]
    RequiresRecreation: NotRequired[RequiresRecreationType]

class SearchProductsAsAdminInputRequestTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    PortfolioId: NotRequired[str]
    Filters: NotRequired[Mapping[ProductViewFilterByType, Sequence[str]]]
    SortBy: NotRequired[ProductViewSortByType]
    SortOrder: NotRequired[SortOrderType]
    PageToken: NotRequired[str]
    PageSize: NotRequired[int]
    ProductSource: NotRequired[Literal["ACCOUNT"]]

class SearchProductsInputRequestTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    Filters: NotRequired[Mapping[ProductViewFilterByType, Sequence[str]]]
    PageSize: NotRequired[int]
    SortBy: NotRequired[ProductViewSortByType]
    SortOrder: NotRequired[SortOrderType]
    PageToken: NotRequired[str]

class ShareErrorTypeDef(TypedDict):
    Accounts: NotRequired[List[str]]
    Message: NotRequired[str]
    Error: NotRequired[str]

class TerminateProvisionedProductInputRequestTypeDef(TypedDict):
    TerminateToken: str
    ProvisionedProductName: NotRequired[str]
    ProvisionedProductId: NotRequired[str]
    IgnoreErrors: NotRequired[bool]
    AcceptLanguage: NotRequired[str]
    RetainPhysicalResources: NotRequired[bool]

class UpdateConstraintInputRequestTypeDef(TypedDict):
    Id: str
    AcceptLanguage: NotRequired[str]
    Description: NotRequired[str]
    Parameters: NotRequired[str]

class UpdateProvisioningPreferencesTypeDef(TypedDict):
    StackSetAccounts: NotRequired[Sequence[str]]
    StackSetRegions: NotRequired[Sequence[str]]
    StackSetFailureToleranceCount: NotRequired[int]
    StackSetFailureTolerancePercentage: NotRequired[int]
    StackSetMaxConcurrencyCount: NotRequired[int]
    StackSetMaxConcurrencyPercentage: NotRequired[int]
    StackSetOperationType: NotRequired[StackSetOperationTypeType]

class UpdateProvisionedProductPropertiesInputRequestTypeDef(TypedDict):
    ProvisionedProductId: str
    ProvisionedProductProperties: Mapping[PropertyKeyType, str]
    IdempotencyToken: str
    AcceptLanguage: NotRequired[str]

class UpdateProvisioningArtifactInputRequestTypeDef(TypedDict):
    ProductId: str
    ProvisioningArtifactId: str
    AcceptLanguage: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    Active: NotRequired[bool]
    Guidance: NotRequired[ProvisioningArtifactGuidanceType]

class UpdateServiceActionInputRequestTypeDef(TypedDict):
    Id: str
    Name: NotRequired[str]
    Definition: NotRequired[Mapping[ServiceActionDefinitionKeyType, str]]
    Description: NotRequired[str]
    AcceptLanguage: NotRequired[str]

class UpdateTagOptionInputRequestTypeDef(TypedDict):
    Id: str
    Value: NotRequired[str]
    Active: NotRequired[bool]

class ListProvisionedProductPlansInputRequestTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    ProvisionProductId: NotRequired[str]
    PageSize: NotRequired[int]
    PageToken: NotRequired[str]
    AccessLevelFilter: NotRequired[AccessLevelFilterTypeDef]

class ScanProvisionedProductsInputRequestTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    AccessLevelFilter: NotRequired[AccessLevelFilterTypeDef]
    PageSize: NotRequired[int]
    PageToken: NotRequired[str]

class SearchProvisionedProductsInputRequestTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    AccessLevelFilter: NotRequired[AccessLevelFilterTypeDef]
    Filters: NotRequired[Mapping[Literal["SearchQuery"], Sequence[str]]]
    SortBy: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    PageSize: NotRequired[int]
    PageToken: NotRequired[str]

class BatchAssociateServiceActionWithProvisioningArtifactInputRequestTypeDef(TypedDict):
    ServiceActionAssociations: Sequence[ServiceActionAssociationTypeDef]
    AcceptLanguage: NotRequired[str]

class BatchDisassociateServiceActionFromProvisioningArtifactInputRequestTypeDef(TypedDict):
    ServiceActionAssociations: Sequence[ServiceActionAssociationTypeDef]
    AcceptLanguage: NotRequired[str]

class BatchAssociateServiceActionWithProvisioningArtifactOutputTypeDef(TypedDict):
    FailedServiceActionAssociations: List[FailedServiceActionAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDisassociateServiceActionFromProvisioningArtifactOutputTypeDef(TypedDict):
    FailedServiceActionAssociations: List[FailedServiceActionAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CopyProductOutputTypeDef(TypedDict):
    CopyProductToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePortfolioShareOutputTypeDef(TypedDict):
    PortfolioShareToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateProvisionedProductPlanOutputTypeDef(TypedDict):
    PlanName: str
    PlanId: str
    ProvisionProductId: str
    ProvisionedProductName: str
    ProvisioningArtifactId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeletePortfolioShareOutputTypeDef(TypedDict):
    PortfolioShareToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeCopyProductStatusOutputTypeDef(TypedDict):
    CopyProductStatus: CopyProductStatusType
    TargetProductId: str
    StatusDetail: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetAWSOrganizationsAccessStatusOutputTypeDef(TypedDict):
    AccessStatus: AccessStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class ListPortfolioAccessOutputTypeDef(TypedDict):
    AccountIds: List[str]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePortfolioShareOutputTypeDef(TypedDict):
    PortfolioShareToken: str
    Status: ShareStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateProvisionedProductPropertiesOutputTypeDef(TypedDict):
    ProvisionedProductId: str
    ProvisionedProductProperties: Dict[PropertyKeyType, str]
    RecordId: str
    Status: RecordStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class ListBudgetsForResourceOutputTypeDef(TypedDict):
    Budgets: List[BudgetDetailTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class SourceConnectionParametersTypeDef(TypedDict):
    CodeStar: NotRequired[CodeStarParametersTypeDef]

class CreateConstraintOutputTypeDef(TypedDict):
    ConstraintDetail: ConstraintDetailTypeDef
    ConstraintParameters: str
    Status: StatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeConstraintOutputTypeDef(TypedDict):
    ConstraintDetail: ConstraintDetailTypeDef
    ConstraintParameters: str
    Status: StatusType
    ResponseMetadata: ResponseMetadataTypeDef

class ListConstraintsForPortfolioOutputTypeDef(TypedDict):
    ConstraintDetails: List[ConstraintDetailTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConstraintOutputTypeDef(TypedDict):
    ConstraintDetail: ConstraintDetailTypeDef
    ConstraintParameters: str
    Status: StatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePortfolioInputRequestTypeDef(TypedDict):
    DisplayName: str
    ProviderName: str
    IdempotencyToken: str
    AcceptLanguage: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class LaunchPathSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    ConstraintSummaries: NotRequired[List[ConstraintSummaryTypeDef]]
    Tags: NotRequired[List[TagTypeDef]]
    Name: NotRequired[str]

ProvisionedProductAttributeTypeDef = TypedDict(
    "ProvisionedProductAttributeTypeDef",
    {
        "Name": NotRequired[str],
        "Arn": NotRequired[str],
        "Type": NotRequired[str],
        "Id": NotRequired[str],
        "Status": NotRequired[ProvisionedProductStatusType],
        "StatusMessage": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
        "IdempotencyToken": NotRequired[str],
        "LastRecordId": NotRequired[str],
        "LastProvisioningRecordId": NotRequired[str],
        "LastSuccessfulProvisioningRecordId": NotRequired[str],
        "Tags": NotRequired[List[TagTypeDef]],
        "PhysicalId": NotRequired[str],
        "ProductId": NotRequired[str],
        "ProductName": NotRequired[str],
        "ProvisioningArtifactId": NotRequired[str],
        "ProvisioningArtifactName": NotRequired[str],
        "UserArn": NotRequired[str],
        "UserArnSession": NotRequired[str],
    },
)

class UpdatePortfolioInputRequestTypeDef(TypedDict):
    Id: str
    AcceptLanguage: NotRequired[str]
    DisplayName: NotRequired[str]
    Description: NotRequired[str]
    ProviderName: NotRequired[str]
    AddTags: NotRequired[Sequence[TagTypeDef]]
    RemoveTags: NotRequired[Sequence[str]]

class CreatePortfolioOutputTypeDef(TypedDict):
    PortfolioDetail: PortfolioDetailTypeDef
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListAcceptedPortfolioSharesOutputTypeDef(TypedDict):
    PortfolioDetails: List[PortfolioDetailTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListPortfoliosForProductOutputTypeDef(TypedDict):
    PortfolioDetails: List[PortfolioDetailTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListPortfoliosOutputTypeDef(TypedDict):
    PortfolioDetails: List[PortfolioDetailTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePortfolioOutputTypeDef(TypedDict):
    PortfolioDetail: PortfolioDetailTypeDef
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePortfolioShareInputRequestTypeDef(TypedDict):
    PortfolioId: str
    AcceptLanguage: NotRequired[str]
    AccountId: NotRequired[str]
    OrganizationNode: NotRequired[OrganizationNodeTypeDef]
    ShareTagOptions: NotRequired[bool]
    SharePrincipals: NotRequired[bool]

class DeletePortfolioShareInputRequestTypeDef(TypedDict):
    PortfolioId: str
    AcceptLanguage: NotRequired[str]
    AccountId: NotRequired[str]
    OrganizationNode: NotRequired[OrganizationNodeTypeDef]

class ListOrganizationPortfolioAccessOutputTypeDef(TypedDict):
    OrganizationNodes: List[OrganizationNodeTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePortfolioShareInputRequestTypeDef(TypedDict):
    PortfolioId: str
    AcceptLanguage: NotRequired[str]
    AccountId: NotRequired[str]
    OrganizationNode: NotRequired[OrganizationNodeTypeDef]
    ShareTagOptions: NotRequired[bool]
    SharePrincipals: NotRequired[bool]

class CreateProvisioningArtifactInputRequestTypeDef(TypedDict):
    ProductId: str
    Parameters: ProvisioningArtifactPropertiesTypeDef
    IdempotencyToken: str
    AcceptLanguage: NotRequired[str]

class CreateProvisioningArtifactOutputTypeDef(TypedDict):
    ProvisioningArtifactDetail: ProvisioningArtifactDetailTypeDef
    Info: Dict[str, str]
    Status: StatusType
    ResponseMetadata: ResponseMetadataTypeDef

class ListProvisioningArtifactsOutputTypeDef(TypedDict):
    ProvisioningArtifactDetails: List[ProvisioningArtifactDetailTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateProvisioningArtifactOutputTypeDef(TypedDict):
    ProvisioningArtifactDetail: ProvisioningArtifactDetailTypeDef
    Info: Dict[str, str]
    Status: StatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateProvisionedProductPlanInputRequestTypeDef(TypedDict):
    PlanName: str
    PlanType: Literal["CLOUDFORMATION"]
    ProductId: str
    ProvisionedProductName: str
    ProvisioningArtifactId: str
    IdempotencyToken: str
    AcceptLanguage: NotRequired[str]
    NotificationArns: NotRequired[Sequence[str]]
    PathId: NotRequired[str]
    ProvisioningParameters: NotRequired[Sequence[UpdateProvisioningParameterTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]

class ProvisionedProductPlanDetailsTypeDef(TypedDict):
    CreatedTime: NotRequired[datetime]
    PathId: NotRequired[str]
    ProductId: NotRequired[str]
    PlanName: NotRequired[str]
    PlanId: NotRequired[str]
    ProvisionProductId: NotRequired[str]
    ProvisionProductName: NotRequired[str]
    PlanType: NotRequired[Literal["CLOUDFORMATION"]]
    ProvisioningArtifactId: NotRequired[str]
    Status: NotRequired[ProvisionedProductPlanStatusType]
    UpdatedTime: NotRequired[datetime]
    NotificationArns: NotRequired[List[str]]
    ProvisioningParameters: NotRequired[List[UpdateProvisioningParameterTypeDef]]
    Tags: NotRequired[List[TagTypeDef]]
    StatusMessage: NotRequired[str]

class CreateTagOptionOutputTypeDef(TypedDict):
    TagOptionDetail: TagOptionDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribePortfolioOutputTypeDef(TypedDict):
    PortfolioDetail: PortfolioDetailTypeDef
    Tags: List[TagTypeDef]
    TagOptions: List[TagOptionDetailTypeDef]
    Budgets: List[BudgetDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeTagOptionOutputTypeDef(TypedDict):
    TagOptionDetail: TagOptionDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagOptionsOutputTypeDef(TypedDict):
    TagOptionDetails: List[TagOptionDetailTypeDef]
    PageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTagOptionOutputTypeDef(TypedDict):
    TagOptionDetail: TagOptionDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribePortfolioSharesOutputTypeDef(TypedDict):
    NextPageToken: str
    PortfolioShareDetails: List[PortfolioShareDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeProductOutputTypeDef(TypedDict):
    ProductViewSummary: ProductViewSummaryTypeDef
    ProvisioningArtifacts: List[ProvisioningArtifactTypeDef]
    Budgets: List[BudgetDetailTypeDef]
    LaunchPaths: List[LaunchPathTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeProductViewOutputTypeDef(TypedDict):
    ProductViewSummary: ProductViewSummaryTypeDef
    ProvisioningArtifacts: List[ProvisioningArtifactTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ProvisioningArtifactViewTypeDef(TypedDict):
    ProductViewSummary: NotRequired[ProductViewSummaryTypeDef]
    ProvisioningArtifact: NotRequired[ProvisioningArtifactTypeDef]

class DescribeProvisionedProductOutputTypeDef(TypedDict):
    ProvisionedProductDetail: ProvisionedProductDetailTypeDef
    CloudWatchDashboards: List[CloudWatchDashboardTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ScanProvisionedProductsOutputTypeDef(TypedDict):
    ProvisionedProducts: List[ProvisionedProductDetailTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetProvisionedProductOutputsOutputTypeDef(TypedDict):
    Outputs: List[RecordOutputTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class NotifyUpdateProvisionedProductEngineWorkflowResultInputRequestTypeDef(TypedDict):
    WorkflowToken: str
    RecordId: str
    Status: EngineWorkflowStatusType
    IdempotencyToken: str
    FailureReason: NotRequired[str]
    Outputs: NotRequired[Sequence[RecordOutputTypeDef]]

class DescribeServiceActionExecutionParametersOutputTypeDef(TypedDict):
    ServiceActionParameters: List[ExecutionParameterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class EngineWorkflowResourceIdentifierTypeDef(TypedDict):
    UniqueTag: NotRequired[UniqueTagResourceIdentifierTypeDef]

class ListAcceptedPortfolioSharesInputListAcceptedPortfolioSharesPaginateTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    PortfolioShareType: NotRequired[PortfolioShareTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConstraintsForPortfolioInputListConstraintsForPortfolioPaginateTypeDef(TypedDict):
    PortfolioId: str
    AcceptLanguage: NotRequired[str]
    ProductId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLaunchPathsInputListLaunchPathsPaginateTypeDef(TypedDict):
    ProductId: str
    AcceptLanguage: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOrganizationPortfolioAccessInputListOrganizationPortfolioAccessPaginateTypeDef(TypedDict):
    PortfolioId: str
    OrganizationNodeType: OrganizationNodeTypeType
    AcceptLanguage: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPortfoliosForProductInputListPortfoliosForProductPaginateTypeDef(TypedDict):
    ProductId: str
    AcceptLanguage: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPortfoliosInputListPortfoliosPaginateTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPrincipalsForPortfolioInputListPrincipalsForPortfolioPaginateTypeDef(TypedDict):
    PortfolioId: str
    AcceptLanguage: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProvisionedProductPlansInputListProvisionedProductPlansPaginateTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    ProvisionProductId: NotRequired[str]
    AccessLevelFilter: NotRequired[AccessLevelFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProvisioningArtifactsForServiceActionInputListProvisioningArtifactsForServiceActionPaginateTypeDef(
    TypedDict
):
    ServiceActionId: str
    AcceptLanguage: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourcesForTagOptionInputListResourcesForTagOptionPaginateTypeDef(TypedDict):
    TagOptionId: str
    ResourceType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceActionsForProvisioningArtifactInputListServiceActionsForProvisioningArtifactPaginateTypeDef(
    TypedDict
):
    ProductId: str
    ProvisioningArtifactId: str
    AcceptLanguage: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceActionsInputListServiceActionsPaginateTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ScanProvisionedProductsInputScanProvisionedProductsPaginateTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    AccessLevelFilter: NotRequired[AccessLevelFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchProductsAsAdminInputSearchProductsAsAdminPaginateTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    PortfolioId: NotRequired[str]
    Filters: NotRequired[Mapping[ProductViewFilterByType, Sequence[str]]]
    SortBy: NotRequired[ProductViewSortByType]
    SortOrder: NotRequired[SortOrderType]
    ProductSource: NotRequired[Literal["ACCOUNT"]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPrincipalsForPortfolioOutputTypeDef(TypedDict):
    Principals: List[PrincipalTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListProvisionedProductPlansOutputTypeDef(TypedDict):
    ProvisionedProductPlans: List[ProvisionedProductPlanSummaryTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListRecordHistoryInputListRecordHistoryPaginateTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    AccessLevelFilter: NotRequired[AccessLevelFilterTypeDef]
    SearchFilter: NotRequired[ListRecordHistorySearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRecordHistoryInputRequestTypeDef(TypedDict):
    AcceptLanguage: NotRequired[str]
    AccessLevelFilter: NotRequired[AccessLevelFilterTypeDef]
    SearchFilter: NotRequired[ListRecordHistorySearchFilterTypeDef]
    PageSize: NotRequired[int]
    PageToken: NotRequired[str]

class ListResourcesForTagOptionOutputTypeDef(TypedDict):
    ResourceDetails: List[ResourceDetailTypeDef]
    PageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListServiceActionsForProvisioningArtifactOutputTypeDef(TypedDict):
    ServiceActionSummaries: List[ServiceActionSummaryTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListServiceActionsOutputTypeDef(TypedDict):
    ServiceActionSummaries: List[ServiceActionSummaryTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ServiceActionDetailTypeDef(TypedDict):
    ServiceActionSummary: NotRequired[ServiceActionSummaryTypeDef]
    Definition: NotRequired[Dict[ServiceActionDefinitionKeyType, str]]

class ListStackInstancesForProvisionedProductOutputTypeDef(TypedDict):
    StackInstances: List[StackInstanceTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagOptionsInputListTagOptionsPaginateTypeDef(TypedDict):
    Filters: NotRequired[ListTagOptionsFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTagOptionsInputRequestTypeDef(TypedDict):
    Filters: NotRequired[ListTagOptionsFiltersTypeDef]
    PageSize: NotRequired[int]
    PageToken: NotRequired[str]

class ProvisioningArtifactParameterTypeDef(TypedDict):
    ParameterKey: NotRequired[str]
    DefaultValue: NotRequired[str]
    ParameterType: NotRequired[str]
    IsNoEcho: NotRequired[bool]
    Description: NotRequired[str]
    ParameterConstraints: NotRequired[ParameterConstraintsTypeDef]

class SearchProductsOutputTypeDef(TypedDict):
    ProductViewSummaries: List[ProductViewSummaryTypeDef]
    ProductViewAggregations: Dict[str, List[ProductViewAggregationValueTypeDef]]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ProvisionProductInputRequestTypeDef(TypedDict):
    ProvisionedProductName: str
    ProvisionToken: str
    AcceptLanguage: NotRequired[str]
    ProductId: NotRequired[str]
    ProductName: NotRequired[str]
    ProvisioningArtifactId: NotRequired[str]
    ProvisioningArtifactName: NotRequired[str]
    PathId: NotRequired[str]
    PathName: NotRequired[str]
    ProvisioningParameters: NotRequired[Sequence[ProvisioningParameterTypeDef]]
    ProvisioningPreferences: NotRequired[ProvisioningPreferencesTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    NotificationArns: NotRequired[Sequence[str]]

class RecordDetailTypeDef(TypedDict):
    RecordId: NotRequired[str]
    ProvisionedProductName: NotRequired[str]
    Status: NotRequired[RecordStatusType]
    CreatedTime: NotRequired[datetime]
    UpdatedTime: NotRequired[datetime]
    ProvisionedProductType: NotRequired[str]
    RecordType: NotRequired[str]
    ProvisionedProductId: NotRequired[str]
    ProductId: NotRequired[str]
    ProvisioningArtifactId: NotRequired[str]
    PathId: NotRequired[str]
    RecordErrors: NotRequired[List[RecordErrorTypeDef]]
    RecordTags: NotRequired[List[RecordTagTypeDef]]
    LaunchRoleArn: NotRequired[str]

class ResourceChangeDetailTypeDef(TypedDict):
    Target: NotRequired[ResourceTargetDefinitionTypeDef]
    Evaluation: NotRequired[EvaluationTypeType]
    CausingEntity: NotRequired[str]

class ShareDetailsTypeDef(TypedDict):
    SuccessfulShares: NotRequired[List[str]]
    ShareErrors: NotRequired[List[ShareErrorTypeDef]]

class UpdateProvisionedProductInputRequestTypeDef(TypedDict):
    UpdateToken: str
    AcceptLanguage: NotRequired[str]
    ProvisionedProductName: NotRequired[str]
    ProvisionedProductId: NotRequired[str]
    ProductId: NotRequired[str]
    ProductName: NotRequired[str]
    ProvisioningArtifactId: NotRequired[str]
    ProvisioningArtifactName: NotRequired[str]
    PathId: NotRequired[str]
    PathName: NotRequired[str]
    ProvisioningParameters: NotRequired[Sequence[UpdateProvisioningParameterTypeDef]]
    ProvisioningPreferences: NotRequired[UpdateProvisioningPreferencesTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

SourceConnectionDetailTypeDef = TypedDict(
    "SourceConnectionDetailTypeDef",
    {
        "Type": NotRequired[Literal["CODESTAR"]],
        "ConnectionParameters": NotRequired[SourceConnectionParametersTypeDef],
        "LastSync": NotRequired[LastSyncTypeDef],
    },
)
SourceConnectionTypeDef = TypedDict(
    "SourceConnectionTypeDef",
    {
        "ConnectionParameters": SourceConnectionParametersTypeDef,
        "Type": NotRequired[Literal["CODESTAR"]],
    },
)

class ListLaunchPathsOutputTypeDef(TypedDict):
    LaunchPathSummaries: List[LaunchPathSummaryTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class SearchProvisionedProductsOutputTypeDef(TypedDict):
    ProvisionedProducts: List[ProvisionedProductAttributeTypeDef]
    TotalResultsCount: int
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListProvisioningArtifactsForServiceActionOutputTypeDef(TypedDict):
    ProvisioningArtifactViews: List[ProvisioningArtifactViewTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class NotifyProvisionProductEngineWorkflowResultInputRequestTypeDef(TypedDict):
    WorkflowToken: str
    RecordId: str
    Status: EngineWorkflowStatusType
    IdempotencyToken: str
    FailureReason: NotRequired[str]
    ResourceIdentifier: NotRequired[EngineWorkflowResourceIdentifierTypeDef]
    Outputs: NotRequired[Sequence[RecordOutputTypeDef]]

class CreateServiceActionOutputTypeDef(TypedDict):
    ServiceActionDetail: ServiceActionDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeServiceActionOutputTypeDef(TypedDict):
    ServiceActionDetail: ServiceActionDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateServiceActionOutputTypeDef(TypedDict):
    ServiceActionDetail: ServiceActionDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeProvisioningArtifactOutputTypeDef(TypedDict):
    ProvisioningArtifactDetail: ProvisioningArtifactDetailTypeDef
    Info: Dict[str, str]
    Status: StatusType
    ProvisioningArtifactParameters: List[ProvisioningArtifactParameterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeProvisioningParametersOutputTypeDef(TypedDict):
    ProvisioningArtifactParameters: List[ProvisioningArtifactParameterTypeDef]
    ConstraintSummaries: List[ConstraintSummaryTypeDef]
    UsageInstructions: List[UsageInstructionTypeDef]
    TagOptions: List[TagOptionSummaryTypeDef]
    ProvisioningArtifactPreferences: ProvisioningArtifactPreferencesTypeDef
    ProvisioningArtifactOutputs: List[ProvisioningArtifactOutputTypeDef]
    ProvisioningArtifactOutputKeys: List[ProvisioningArtifactOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeRecordOutputTypeDef(TypedDict):
    RecordDetail: RecordDetailTypeDef
    RecordOutputs: List[RecordOutputTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ExecuteProvisionedProductPlanOutputTypeDef(TypedDict):
    RecordDetail: RecordDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ExecuteProvisionedProductServiceActionOutputTypeDef(TypedDict):
    RecordDetail: RecordDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ImportAsProvisionedProductOutputTypeDef(TypedDict):
    RecordDetail: RecordDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListRecordHistoryOutputTypeDef(TypedDict):
    RecordDetails: List[RecordDetailTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ProvisionProductOutputTypeDef(TypedDict):
    RecordDetail: RecordDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class TerminateProvisionedProductOutputTypeDef(TypedDict):
    RecordDetail: RecordDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateProvisionedProductOutputTypeDef(TypedDict):
    RecordDetail: RecordDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ResourceChangeTypeDef(TypedDict):
    Action: NotRequired[ChangeActionType]
    LogicalResourceId: NotRequired[str]
    PhysicalResourceId: NotRequired[str]
    ResourceType: NotRequired[str]
    Replacement: NotRequired[ReplacementType]
    Scope: NotRequired[List[ResourceAttributeType]]
    Details: NotRequired[List[ResourceChangeDetailTypeDef]]

class DescribePortfolioShareStatusOutputTypeDef(TypedDict):
    PortfolioShareToken: str
    PortfolioId: str
    OrganizationNodeValue: str
    Status: ShareStatusType
    ShareDetails: ShareDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ProductViewDetailTypeDef(TypedDict):
    ProductViewSummary: NotRequired[ProductViewSummaryTypeDef]
    Status: NotRequired[StatusType]
    ProductARN: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    SourceConnection: NotRequired[SourceConnectionDetailTypeDef]

class CreateProductInputRequestTypeDef(TypedDict):
    Name: str
    Owner: str
    ProductType: ProductTypeType
    IdempotencyToken: str
    AcceptLanguage: NotRequired[str]
    Description: NotRequired[str]
    Distributor: NotRequired[str]
    SupportDescription: NotRequired[str]
    SupportEmail: NotRequired[str]
    SupportUrl: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ProvisioningArtifactParameters: NotRequired[ProvisioningArtifactPropertiesTypeDef]
    SourceConnection: NotRequired[SourceConnectionTypeDef]

class UpdateProductInputRequestTypeDef(TypedDict):
    Id: str
    AcceptLanguage: NotRequired[str]
    Name: NotRequired[str]
    Owner: NotRequired[str]
    Description: NotRequired[str]
    Distributor: NotRequired[str]
    SupportDescription: NotRequired[str]
    SupportEmail: NotRequired[str]
    SupportUrl: NotRequired[str]
    AddTags: NotRequired[Sequence[TagTypeDef]]
    RemoveTags: NotRequired[Sequence[str]]
    SourceConnection: NotRequired[SourceConnectionTypeDef]

class DescribeProvisionedProductPlanOutputTypeDef(TypedDict):
    ProvisionedProductPlanDetails: ProvisionedProductPlanDetailsTypeDef
    ResourceChanges: List[ResourceChangeTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateProductOutputTypeDef(TypedDict):
    ProductViewDetail: ProductViewDetailTypeDef
    ProvisioningArtifactDetail: ProvisioningArtifactDetailTypeDef
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeProductAsAdminOutputTypeDef(TypedDict):
    ProductViewDetail: ProductViewDetailTypeDef
    ProvisioningArtifactSummaries: List[ProvisioningArtifactSummaryTypeDef]
    Tags: List[TagTypeDef]
    TagOptions: List[TagOptionDetailTypeDef]
    Budgets: List[BudgetDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class SearchProductsAsAdminOutputTypeDef(TypedDict):
    ProductViewDetails: List[ProductViewDetailTypeDef]
    NextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateProductOutputTypeDef(TypedDict):
    ProductViewDetail: ProductViewDetailTypeDef
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
