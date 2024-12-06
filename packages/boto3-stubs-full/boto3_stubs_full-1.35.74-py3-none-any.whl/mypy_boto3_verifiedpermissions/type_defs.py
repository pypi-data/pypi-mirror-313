"""
Type annotations for verifiedpermissions service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_verifiedpermissions/type_defs/)

Usage::

    ```python
    from mypy_boto3_verifiedpermissions.type_defs import ActionIdentifierTypeDef

    data: ActionIdentifierTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    BatchGetPolicyErrorCodeType,
    DecisionType,
    PolicyEffectType,
    PolicyTypeType,
    ValidationModeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ActionIdentifierTypeDef",
    "AttributeValueOutputTypeDef",
    "AttributeValueTypeDef",
    "AttributeValueUnionTypeDef",
    "BatchGetPolicyErrorItemTypeDef",
    "BatchGetPolicyInputItemTypeDef",
    "BatchGetPolicyInputRequestTypeDef",
    "BatchGetPolicyOutputItemTypeDef",
    "BatchGetPolicyOutputTypeDef",
    "BatchIsAuthorizedInputItemOutputTypeDef",
    "BatchIsAuthorizedInputItemTypeDef",
    "BatchIsAuthorizedInputItemUnionTypeDef",
    "BatchIsAuthorizedInputRequestTypeDef",
    "BatchIsAuthorizedOutputItemTypeDef",
    "BatchIsAuthorizedOutputTypeDef",
    "BatchIsAuthorizedWithTokenInputItemOutputTypeDef",
    "BatchIsAuthorizedWithTokenInputItemTypeDef",
    "BatchIsAuthorizedWithTokenInputItemUnionTypeDef",
    "BatchIsAuthorizedWithTokenInputRequestTypeDef",
    "BatchIsAuthorizedWithTokenOutputItemTypeDef",
    "BatchIsAuthorizedWithTokenOutputTypeDef",
    "CognitoGroupConfigurationDetailTypeDef",
    "CognitoGroupConfigurationItemTypeDef",
    "CognitoGroupConfigurationTypeDef",
    "CognitoUserPoolConfigurationDetailTypeDef",
    "CognitoUserPoolConfigurationItemTypeDef",
    "CognitoUserPoolConfigurationTypeDef",
    "ConfigurationDetailTypeDef",
    "ConfigurationItemTypeDef",
    "ConfigurationTypeDef",
    "ContextDefinitionOutputTypeDef",
    "ContextDefinitionTypeDef",
    "ContextDefinitionUnionTypeDef",
    "CreateIdentitySourceInputRequestTypeDef",
    "CreateIdentitySourceOutputTypeDef",
    "CreatePolicyInputRequestTypeDef",
    "CreatePolicyOutputTypeDef",
    "CreatePolicyStoreInputRequestTypeDef",
    "CreatePolicyStoreOutputTypeDef",
    "CreatePolicyTemplateInputRequestTypeDef",
    "CreatePolicyTemplateOutputTypeDef",
    "DeleteIdentitySourceInputRequestTypeDef",
    "DeletePolicyInputRequestTypeDef",
    "DeletePolicyStoreInputRequestTypeDef",
    "DeletePolicyTemplateInputRequestTypeDef",
    "DeterminingPolicyItemTypeDef",
    "EntitiesDefinitionTypeDef",
    "EntityIdentifierTypeDef",
    "EntityItemTypeDef",
    "EntityReferenceTypeDef",
    "EvaluationErrorItemTypeDef",
    "GetIdentitySourceInputRequestTypeDef",
    "GetIdentitySourceOutputTypeDef",
    "GetPolicyInputRequestTypeDef",
    "GetPolicyOutputTypeDef",
    "GetPolicyStoreInputRequestTypeDef",
    "GetPolicyStoreOutputTypeDef",
    "GetPolicyTemplateInputRequestTypeDef",
    "GetPolicyTemplateOutputTypeDef",
    "GetSchemaInputRequestTypeDef",
    "GetSchemaOutputTypeDef",
    "IdentitySourceDetailsTypeDef",
    "IdentitySourceFilterTypeDef",
    "IdentitySourceItemDetailsTypeDef",
    "IdentitySourceItemTypeDef",
    "IsAuthorizedInputRequestTypeDef",
    "IsAuthorizedOutputTypeDef",
    "IsAuthorizedWithTokenInputRequestTypeDef",
    "IsAuthorizedWithTokenOutputTypeDef",
    "ListIdentitySourcesInputListIdentitySourcesPaginateTypeDef",
    "ListIdentitySourcesInputRequestTypeDef",
    "ListIdentitySourcesOutputTypeDef",
    "ListPoliciesInputListPoliciesPaginateTypeDef",
    "ListPoliciesInputRequestTypeDef",
    "ListPoliciesOutputTypeDef",
    "ListPolicyStoresInputListPolicyStoresPaginateTypeDef",
    "ListPolicyStoresInputRequestTypeDef",
    "ListPolicyStoresOutputTypeDef",
    "ListPolicyTemplatesInputListPolicyTemplatesPaginateTypeDef",
    "ListPolicyTemplatesInputRequestTypeDef",
    "ListPolicyTemplatesOutputTypeDef",
    "OpenIdConnectAccessTokenConfigurationDetailTypeDef",
    "OpenIdConnectAccessTokenConfigurationItemTypeDef",
    "OpenIdConnectAccessTokenConfigurationTypeDef",
    "OpenIdConnectConfigurationDetailTypeDef",
    "OpenIdConnectConfigurationItemTypeDef",
    "OpenIdConnectConfigurationTypeDef",
    "OpenIdConnectGroupConfigurationDetailTypeDef",
    "OpenIdConnectGroupConfigurationItemTypeDef",
    "OpenIdConnectGroupConfigurationTypeDef",
    "OpenIdConnectIdentityTokenConfigurationDetailTypeDef",
    "OpenIdConnectIdentityTokenConfigurationItemTypeDef",
    "OpenIdConnectIdentityTokenConfigurationTypeDef",
    "OpenIdConnectTokenSelectionDetailTypeDef",
    "OpenIdConnectTokenSelectionItemTypeDef",
    "OpenIdConnectTokenSelectionTypeDef",
    "PaginatorConfigTypeDef",
    "PolicyDefinitionDetailTypeDef",
    "PolicyDefinitionItemTypeDef",
    "PolicyDefinitionTypeDef",
    "PolicyFilterTypeDef",
    "PolicyItemTypeDef",
    "PolicyStoreItemTypeDef",
    "PolicyTemplateItemTypeDef",
    "PutSchemaInputRequestTypeDef",
    "PutSchemaOutputTypeDef",
    "ResponseMetadataTypeDef",
    "SchemaDefinitionTypeDef",
    "StaticPolicyDefinitionDetailTypeDef",
    "StaticPolicyDefinitionItemTypeDef",
    "StaticPolicyDefinitionTypeDef",
    "TemplateLinkedPolicyDefinitionDetailTypeDef",
    "TemplateLinkedPolicyDefinitionItemTypeDef",
    "TemplateLinkedPolicyDefinitionTypeDef",
    "UpdateCognitoGroupConfigurationTypeDef",
    "UpdateCognitoUserPoolConfigurationTypeDef",
    "UpdateConfigurationTypeDef",
    "UpdateIdentitySourceInputRequestTypeDef",
    "UpdateIdentitySourceOutputTypeDef",
    "UpdateOpenIdConnectAccessTokenConfigurationTypeDef",
    "UpdateOpenIdConnectConfigurationTypeDef",
    "UpdateOpenIdConnectGroupConfigurationTypeDef",
    "UpdateOpenIdConnectIdentityTokenConfigurationTypeDef",
    "UpdateOpenIdConnectTokenSelectionTypeDef",
    "UpdatePolicyDefinitionTypeDef",
    "UpdatePolicyInputRequestTypeDef",
    "UpdatePolicyOutputTypeDef",
    "UpdatePolicyStoreInputRequestTypeDef",
    "UpdatePolicyStoreOutputTypeDef",
    "UpdatePolicyTemplateInputRequestTypeDef",
    "UpdatePolicyTemplateOutputTypeDef",
    "UpdateStaticPolicyDefinitionTypeDef",
    "ValidationSettingsTypeDef",
)


class ActionIdentifierTypeDef(TypedDict):
    actionType: str
    actionId: str


class EntityIdentifierTypeDef(TypedDict):
    entityType: str
    entityId: str


class BatchGetPolicyErrorItemTypeDef(TypedDict):
    code: BatchGetPolicyErrorCodeType
    policyStoreId: str
    policyId: str
    message: str


class BatchGetPolicyInputItemTypeDef(TypedDict):
    policyStoreId: str
    policyId: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeterminingPolicyItemTypeDef(TypedDict):
    policyId: str


class EvaluationErrorItemTypeDef(TypedDict):
    errorDescription: str


class CognitoGroupConfigurationDetailTypeDef(TypedDict):
    groupEntityType: NotRequired[str]


class CognitoGroupConfigurationItemTypeDef(TypedDict):
    groupEntityType: NotRequired[str]


class CognitoGroupConfigurationTypeDef(TypedDict):
    groupEntityType: str


class ValidationSettingsTypeDef(TypedDict):
    mode: ValidationModeType


class CreatePolicyTemplateInputRequestTypeDef(TypedDict):
    policyStoreId: str
    statement: str
    clientToken: NotRequired[str]
    description: NotRequired[str]


class DeleteIdentitySourceInputRequestTypeDef(TypedDict):
    policyStoreId: str
    identitySourceId: str


class DeletePolicyInputRequestTypeDef(TypedDict):
    policyStoreId: str
    policyId: str


class DeletePolicyStoreInputRequestTypeDef(TypedDict):
    policyStoreId: str


class DeletePolicyTemplateInputRequestTypeDef(TypedDict):
    policyStoreId: str
    policyTemplateId: str


class GetIdentitySourceInputRequestTypeDef(TypedDict):
    policyStoreId: str
    identitySourceId: str


class IdentitySourceDetailsTypeDef(TypedDict):
    clientIds: NotRequired[List[str]]
    userPoolArn: NotRequired[str]
    discoveryUrl: NotRequired[str]
    openIdIssuer: NotRequired[Literal["COGNITO"]]


class GetPolicyInputRequestTypeDef(TypedDict):
    policyStoreId: str
    policyId: str


class GetPolicyStoreInputRequestTypeDef(TypedDict):
    policyStoreId: str


class GetPolicyTemplateInputRequestTypeDef(TypedDict):
    policyStoreId: str
    policyTemplateId: str


class GetSchemaInputRequestTypeDef(TypedDict):
    policyStoreId: str


class IdentitySourceFilterTypeDef(TypedDict):
    principalEntityType: NotRequired[str]


class IdentitySourceItemDetailsTypeDef(TypedDict):
    clientIds: NotRequired[List[str]]
    userPoolArn: NotRequired[str]
    discoveryUrl: NotRequired[str]
    openIdIssuer: NotRequired[Literal["COGNITO"]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListPolicyStoresInputRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class PolicyStoreItemTypeDef(TypedDict):
    policyStoreId: str
    arn: str
    createdDate: datetime
    lastUpdatedDate: NotRequired[datetime]
    description: NotRequired[str]


class ListPolicyTemplatesInputRequestTypeDef(TypedDict):
    policyStoreId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class PolicyTemplateItemTypeDef(TypedDict):
    policyStoreId: str
    policyTemplateId: str
    createdDate: datetime
    lastUpdatedDate: datetime
    description: NotRequired[str]


class OpenIdConnectAccessTokenConfigurationDetailTypeDef(TypedDict):
    principalIdClaim: NotRequired[str]
    audiences: NotRequired[List[str]]


class OpenIdConnectAccessTokenConfigurationItemTypeDef(TypedDict):
    principalIdClaim: NotRequired[str]
    audiences: NotRequired[List[str]]


class OpenIdConnectAccessTokenConfigurationTypeDef(TypedDict):
    principalIdClaim: NotRequired[str]
    audiences: NotRequired[Sequence[str]]


class OpenIdConnectGroupConfigurationDetailTypeDef(TypedDict):
    groupClaim: str
    groupEntityType: str


class OpenIdConnectGroupConfigurationItemTypeDef(TypedDict):
    groupClaim: str
    groupEntityType: str


class OpenIdConnectGroupConfigurationTypeDef(TypedDict):
    groupClaim: str
    groupEntityType: str


class OpenIdConnectIdentityTokenConfigurationDetailTypeDef(TypedDict):
    principalIdClaim: NotRequired[str]
    clientIds: NotRequired[List[str]]


class OpenIdConnectIdentityTokenConfigurationItemTypeDef(TypedDict):
    principalIdClaim: NotRequired[str]
    clientIds: NotRequired[List[str]]


class OpenIdConnectIdentityTokenConfigurationTypeDef(TypedDict):
    principalIdClaim: NotRequired[str]
    clientIds: NotRequired[Sequence[str]]


class StaticPolicyDefinitionDetailTypeDef(TypedDict):
    statement: str
    description: NotRequired[str]


class StaticPolicyDefinitionItemTypeDef(TypedDict):
    description: NotRequired[str]


class StaticPolicyDefinitionTypeDef(TypedDict):
    statement: str
    description: NotRequired[str]


class SchemaDefinitionTypeDef(TypedDict):
    cedarJson: NotRequired[str]


class UpdateCognitoGroupConfigurationTypeDef(TypedDict):
    groupEntityType: str


class UpdateOpenIdConnectAccessTokenConfigurationTypeDef(TypedDict):
    principalIdClaim: NotRequired[str]
    audiences: NotRequired[Sequence[str]]


class UpdateOpenIdConnectGroupConfigurationTypeDef(TypedDict):
    groupClaim: str
    groupEntityType: str


class UpdateOpenIdConnectIdentityTokenConfigurationTypeDef(TypedDict):
    principalIdClaim: NotRequired[str]
    clientIds: NotRequired[Sequence[str]]


class UpdateStaticPolicyDefinitionTypeDef(TypedDict):
    statement: str
    description: NotRequired[str]


class UpdatePolicyTemplateInputRequestTypeDef(TypedDict):
    policyStoreId: str
    policyTemplateId: str
    statement: str
    description: NotRequired[str]


AttributeValueOutputTypeDef = TypedDict(
    "AttributeValueOutputTypeDef",
    {
        "boolean": NotRequired[bool],
        "entityIdentifier": NotRequired[EntityIdentifierTypeDef],
        "long": NotRequired[int],
        "string": NotRequired[str],
        "set": NotRequired[List[Dict[str, Any]]],
        "record": NotRequired[Dict[str, Dict[str, Any]]],
        "ipaddr": NotRequired[str],
        "decimal": NotRequired[str],
    },
)
AttributeValueTypeDef = TypedDict(
    "AttributeValueTypeDef",
    {
        "boolean": NotRequired[bool],
        "entityIdentifier": NotRequired[EntityIdentifierTypeDef],
        "long": NotRequired[int],
        "string": NotRequired[str],
        "set": NotRequired[Sequence[Mapping[str, Any]]],
        "record": NotRequired[Mapping[str, Mapping[str, Any]]],
        "ipaddr": NotRequired[str],
        "decimal": NotRequired[str],
    },
)


class EntityReferenceTypeDef(TypedDict):
    unspecified: NotRequired[bool]
    identifier: NotRequired[EntityIdentifierTypeDef]


class TemplateLinkedPolicyDefinitionDetailTypeDef(TypedDict):
    policyTemplateId: str
    principal: NotRequired[EntityIdentifierTypeDef]
    resource: NotRequired[EntityIdentifierTypeDef]


class TemplateLinkedPolicyDefinitionItemTypeDef(TypedDict):
    policyTemplateId: str
    principal: NotRequired[EntityIdentifierTypeDef]
    resource: NotRequired[EntityIdentifierTypeDef]


class TemplateLinkedPolicyDefinitionTypeDef(TypedDict):
    policyTemplateId: str
    principal: NotRequired[EntityIdentifierTypeDef]
    resource: NotRequired[EntityIdentifierTypeDef]


class BatchGetPolicyInputRequestTypeDef(TypedDict):
    requests: Sequence[BatchGetPolicyInputItemTypeDef]


class CreateIdentitySourceOutputTypeDef(TypedDict):
    createdDate: datetime
    identitySourceId: str
    lastUpdatedDate: datetime
    policyStoreId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePolicyOutputTypeDef(TypedDict):
    policyStoreId: str
    policyId: str
    policyType: PolicyTypeType
    principal: EntityIdentifierTypeDef
    resource: EntityIdentifierTypeDef
    actions: List[ActionIdentifierTypeDef]
    createdDate: datetime
    lastUpdatedDate: datetime
    effect: PolicyEffectType
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePolicyStoreOutputTypeDef(TypedDict):
    policyStoreId: str
    arn: str
    createdDate: datetime
    lastUpdatedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePolicyTemplateOutputTypeDef(TypedDict):
    policyStoreId: str
    policyTemplateId: str
    createdDate: datetime
    lastUpdatedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetPolicyTemplateOutputTypeDef(TypedDict):
    policyStoreId: str
    policyTemplateId: str
    description: str
    statement: str
    createdDate: datetime
    lastUpdatedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetSchemaOutputTypeDef(TypedDict):
    policyStoreId: str
    schema: str
    createdDate: datetime
    lastUpdatedDate: datetime
    namespaces: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutSchemaOutputTypeDef(TypedDict):
    policyStoreId: str
    namespaces: List[str]
    createdDate: datetime
    lastUpdatedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateIdentitySourceOutputTypeDef(TypedDict):
    createdDate: datetime
    identitySourceId: str
    lastUpdatedDate: datetime
    policyStoreId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePolicyOutputTypeDef(TypedDict):
    policyStoreId: str
    policyId: str
    policyType: PolicyTypeType
    principal: EntityIdentifierTypeDef
    resource: EntityIdentifierTypeDef
    actions: List[ActionIdentifierTypeDef]
    createdDate: datetime
    lastUpdatedDate: datetime
    effect: PolicyEffectType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePolicyStoreOutputTypeDef(TypedDict):
    policyStoreId: str
    arn: str
    createdDate: datetime
    lastUpdatedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePolicyTemplateOutputTypeDef(TypedDict):
    policyStoreId: str
    policyTemplateId: str
    createdDate: datetime
    lastUpdatedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class IsAuthorizedOutputTypeDef(TypedDict):
    decision: DecisionType
    determiningPolicies: List[DeterminingPolicyItemTypeDef]
    errors: List[EvaluationErrorItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class IsAuthorizedWithTokenOutputTypeDef(TypedDict):
    decision: DecisionType
    determiningPolicies: List[DeterminingPolicyItemTypeDef]
    errors: List[EvaluationErrorItemTypeDef]
    principal: EntityIdentifierTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CognitoUserPoolConfigurationDetailTypeDef(TypedDict):
    userPoolArn: str
    clientIds: List[str]
    issuer: str
    groupConfiguration: NotRequired[CognitoGroupConfigurationDetailTypeDef]


class CognitoUserPoolConfigurationItemTypeDef(TypedDict):
    userPoolArn: str
    clientIds: List[str]
    issuer: str
    groupConfiguration: NotRequired[CognitoGroupConfigurationItemTypeDef]


class CognitoUserPoolConfigurationTypeDef(TypedDict):
    userPoolArn: str
    clientIds: NotRequired[Sequence[str]]
    groupConfiguration: NotRequired[CognitoGroupConfigurationTypeDef]


class CreatePolicyStoreInputRequestTypeDef(TypedDict):
    validationSettings: ValidationSettingsTypeDef
    clientToken: NotRequired[str]
    description: NotRequired[str]


class GetPolicyStoreOutputTypeDef(TypedDict):
    policyStoreId: str
    arn: str
    validationSettings: ValidationSettingsTypeDef
    createdDate: datetime
    lastUpdatedDate: datetime
    description: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePolicyStoreInputRequestTypeDef(TypedDict):
    policyStoreId: str
    validationSettings: ValidationSettingsTypeDef
    description: NotRequired[str]


class ListIdentitySourcesInputRequestTypeDef(TypedDict):
    policyStoreId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    filters: NotRequired[Sequence[IdentitySourceFilterTypeDef]]


class ListIdentitySourcesInputListIdentitySourcesPaginateTypeDef(TypedDict):
    policyStoreId: str
    filters: NotRequired[Sequence[IdentitySourceFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPolicyStoresInputListPolicyStoresPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPolicyTemplatesInputListPolicyTemplatesPaginateTypeDef(TypedDict):
    policyStoreId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPolicyStoresOutputTypeDef(TypedDict):
    policyStores: List[PolicyStoreItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPolicyTemplatesOutputTypeDef(TypedDict):
    policyTemplates: List[PolicyTemplateItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class OpenIdConnectTokenSelectionDetailTypeDef(TypedDict):
    accessTokenOnly: NotRequired[OpenIdConnectAccessTokenConfigurationDetailTypeDef]
    identityTokenOnly: NotRequired[OpenIdConnectIdentityTokenConfigurationDetailTypeDef]


class OpenIdConnectTokenSelectionItemTypeDef(TypedDict):
    accessTokenOnly: NotRequired[OpenIdConnectAccessTokenConfigurationItemTypeDef]
    identityTokenOnly: NotRequired[OpenIdConnectIdentityTokenConfigurationItemTypeDef]


class OpenIdConnectTokenSelectionTypeDef(TypedDict):
    accessTokenOnly: NotRequired[OpenIdConnectAccessTokenConfigurationTypeDef]
    identityTokenOnly: NotRequired[OpenIdConnectIdentityTokenConfigurationTypeDef]


class PutSchemaInputRequestTypeDef(TypedDict):
    policyStoreId: str
    definition: SchemaDefinitionTypeDef


class UpdateCognitoUserPoolConfigurationTypeDef(TypedDict):
    userPoolArn: str
    clientIds: NotRequired[Sequence[str]]
    groupConfiguration: NotRequired[UpdateCognitoGroupConfigurationTypeDef]


class UpdateOpenIdConnectTokenSelectionTypeDef(TypedDict):
    accessTokenOnly: NotRequired[UpdateOpenIdConnectAccessTokenConfigurationTypeDef]
    identityTokenOnly: NotRequired[UpdateOpenIdConnectIdentityTokenConfigurationTypeDef]


class UpdatePolicyDefinitionTypeDef(TypedDict):
    static: NotRequired[UpdateStaticPolicyDefinitionTypeDef]


class ContextDefinitionOutputTypeDef(TypedDict):
    contextMap: NotRequired[Dict[str, AttributeValueOutputTypeDef]]


AttributeValueUnionTypeDef = Union[AttributeValueTypeDef, AttributeValueOutputTypeDef]


class PolicyFilterTypeDef(TypedDict):
    principal: NotRequired[EntityReferenceTypeDef]
    resource: NotRequired[EntityReferenceTypeDef]
    policyType: NotRequired[PolicyTypeType]
    policyTemplateId: NotRequired[str]


class PolicyDefinitionDetailTypeDef(TypedDict):
    static: NotRequired[StaticPolicyDefinitionDetailTypeDef]
    templateLinked: NotRequired[TemplateLinkedPolicyDefinitionDetailTypeDef]


class PolicyDefinitionItemTypeDef(TypedDict):
    static: NotRequired[StaticPolicyDefinitionItemTypeDef]
    templateLinked: NotRequired[TemplateLinkedPolicyDefinitionItemTypeDef]


class PolicyDefinitionTypeDef(TypedDict):
    static: NotRequired[StaticPolicyDefinitionTypeDef]
    templateLinked: NotRequired[TemplateLinkedPolicyDefinitionTypeDef]


class OpenIdConnectConfigurationDetailTypeDef(TypedDict):
    issuer: str
    tokenSelection: OpenIdConnectTokenSelectionDetailTypeDef
    entityIdPrefix: NotRequired[str]
    groupConfiguration: NotRequired[OpenIdConnectGroupConfigurationDetailTypeDef]


class OpenIdConnectConfigurationItemTypeDef(TypedDict):
    issuer: str
    tokenSelection: OpenIdConnectTokenSelectionItemTypeDef
    entityIdPrefix: NotRequired[str]
    groupConfiguration: NotRequired[OpenIdConnectGroupConfigurationItemTypeDef]


class OpenIdConnectConfigurationTypeDef(TypedDict):
    issuer: str
    tokenSelection: OpenIdConnectTokenSelectionTypeDef
    entityIdPrefix: NotRequired[str]
    groupConfiguration: NotRequired[OpenIdConnectGroupConfigurationTypeDef]


class UpdateOpenIdConnectConfigurationTypeDef(TypedDict):
    issuer: str
    tokenSelection: UpdateOpenIdConnectTokenSelectionTypeDef
    entityIdPrefix: NotRequired[str]
    groupConfiguration: NotRequired[UpdateOpenIdConnectGroupConfigurationTypeDef]


class UpdatePolicyInputRequestTypeDef(TypedDict):
    policyStoreId: str
    policyId: str
    definition: UpdatePolicyDefinitionTypeDef


class BatchIsAuthorizedInputItemOutputTypeDef(TypedDict):
    principal: NotRequired[EntityIdentifierTypeDef]
    action: NotRequired[ActionIdentifierTypeDef]
    resource: NotRequired[EntityIdentifierTypeDef]
    context: NotRequired[ContextDefinitionOutputTypeDef]


class BatchIsAuthorizedWithTokenInputItemOutputTypeDef(TypedDict):
    action: NotRequired[ActionIdentifierTypeDef]
    resource: NotRequired[EntityIdentifierTypeDef]
    context: NotRequired[ContextDefinitionOutputTypeDef]


class ContextDefinitionTypeDef(TypedDict):
    contextMap: NotRequired[Mapping[str, AttributeValueUnionTypeDef]]


class EntityItemTypeDef(TypedDict):
    identifier: EntityIdentifierTypeDef
    attributes: NotRequired[Mapping[str, AttributeValueUnionTypeDef]]
    parents: NotRequired[Sequence[EntityIdentifierTypeDef]]


ListPoliciesInputListPoliciesPaginateTypeDef = TypedDict(
    "ListPoliciesInputListPoliciesPaginateTypeDef",
    {
        "policyStoreId": str,
        "filter": NotRequired[PolicyFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListPoliciesInputRequestTypeDef = TypedDict(
    "ListPoliciesInputRequestTypeDef",
    {
        "policyStoreId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "filter": NotRequired[PolicyFilterTypeDef],
    },
)


class BatchGetPolicyOutputItemTypeDef(TypedDict):
    policyStoreId: str
    policyId: str
    policyType: PolicyTypeType
    definition: PolicyDefinitionDetailTypeDef
    createdDate: datetime
    lastUpdatedDate: datetime


class GetPolicyOutputTypeDef(TypedDict):
    policyStoreId: str
    policyId: str
    policyType: PolicyTypeType
    principal: EntityIdentifierTypeDef
    resource: EntityIdentifierTypeDef
    actions: List[ActionIdentifierTypeDef]
    definition: PolicyDefinitionDetailTypeDef
    createdDate: datetime
    lastUpdatedDate: datetime
    effect: PolicyEffectType
    ResponseMetadata: ResponseMetadataTypeDef


class PolicyItemTypeDef(TypedDict):
    policyStoreId: str
    policyId: str
    policyType: PolicyTypeType
    definition: PolicyDefinitionItemTypeDef
    createdDate: datetime
    lastUpdatedDate: datetime
    principal: NotRequired[EntityIdentifierTypeDef]
    resource: NotRequired[EntityIdentifierTypeDef]
    actions: NotRequired[List[ActionIdentifierTypeDef]]
    effect: NotRequired[PolicyEffectType]


class CreatePolicyInputRequestTypeDef(TypedDict):
    policyStoreId: str
    definition: PolicyDefinitionTypeDef
    clientToken: NotRequired[str]


class ConfigurationDetailTypeDef(TypedDict):
    cognitoUserPoolConfiguration: NotRequired[CognitoUserPoolConfigurationDetailTypeDef]
    openIdConnectConfiguration: NotRequired[OpenIdConnectConfigurationDetailTypeDef]


class ConfigurationItemTypeDef(TypedDict):
    cognitoUserPoolConfiguration: NotRequired[CognitoUserPoolConfigurationItemTypeDef]
    openIdConnectConfiguration: NotRequired[OpenIdConnectConfigurationItemTypeDef]


class ConfigurationTypeDef(TypedDict):
    cognitoUserPoolConfiguration: NotRequired[CognitoUserPoolConfigurationTypeDef]
    openIdConnectConfiguration: NotRequired[OpenIdConnectConfigurationTypeDef]


class UpdateConfigurationTypeDef(TypedDict):
    cognitoUserPoolConfiguration: NotRequired[UpdateCognitoUserPoolConfigurationTypeDef]
    openIdConnectConfiguration: NotRequired[UpdateOpenIdConnectConfigurationTypeDef]


class BatchIsAuthorizedOutputItemTypeDef(TypedDict):
    request: BatchIsAuthorizedInputItemOutputTypeDef
    decision: DecisionType
    determiningPolicies: List[DeterminingPolicyItemTypeDef]
    errors: List[EvaluationErrorItemTypeDef]


class BatchIsAuthorizedWithTokenOutputItemTypeDef(TypedDict):
    request: BatchIsAuthorizedWithTokenInputItemOutputTypeDef
    decision: DecisionType
    determiningPolicies: List[DeterminingPolicyItemTypeDef]
    errors: List[EvaluationErrorItemTypeDef]


ContextDefinitionUnionTypeDef = Union[ContextDefinitionTypeDef, ContextDefinitionOutputTypeDef]


class EntitiesDefinitionTypeDef(TypedDict):
    entityList: NotRequired[Sequence[EntityItemTypeDef]]


class BatchGetPolicyOutputTypeDef(TypedDict):
    results: List[BatchGetPolicyOutputItemTypeDef]
    errors: List[BatchGetPolicyErrorItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListPoliciesOutputTypeDef(TypedDict):
    policies: List[PolicyItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetIdentitySourceOutputTypeDef(TypedDict):
    createdDate: datetime
    details: IdentitySourceDetailsTypeDef
    identitySourceId: str
    lastUpdatedDate: datetime
    policyStoreId: str
    principalEntityType: str
    configuration: ConfigurationDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class IdentitySourceItemTypeDef(TypedDict):
    createdDate: datetime
    identitySourceId: str
    lastUpdatedDate: datetime
    policyStoreId: str
    principalEntityType: str
    details: NotRequired[IdentitySourceItemDetailsTypeDef]
    configuration: NotRequired[ConfigurationItemTypeDef]


class CreateIdentitySourceInputRequestTypeDef(TypedDict):
    policyStoreId: str
    configuration: ConfigurationTypeDef
    clientToken: NotRequired[str]
    principalEntityType: NotRequired[str]


class UpdateIdentitySourceInputRequestTypeDef(TypedDict):
    policyStoreId: str
    identitySourceId: str
    updateConfiguration: UpdateConfigurationTypeDef
    principalEntityType: NotRequired[str]


class BatchIsAuthorizedOutputTypeDef(TypedDict):
    results: List[BatchIsAuthorizedOutputItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchIsAuthorizedWithTokenOutputTypeDef(TypedDict):
    principal: EntityIdentifierTypeDef
    results: List[BatchIsAuthorizedWithTokenOutputItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchIsAuthorizedInputItemTypeDef(TypedDict):
    principal: NotRequired[EntityIdentifierTypeDef]
    action: NotRequired[ActionIdentifierTypeDef]
    resource: NotRequired[EntityIdentifierTypeDef]
    context: NotRequired[ContextDefinitionUnionTypeDef]


class BatchIsAuthorizedWithTokenInputItemTypeDef(TypedDict):
    action: NotRequired[ActionIdentifierTypeDef]
    resource: NotRequired[EntityIdentifierTypeDef]
    context: NotRequired[ContextDefinitionUnionTypeDef]


class IsAuthorizedInputRequestTypeDef(TypedDict):
    policyStoreId: str
    principal: NotRequired[EntityIdentifierTypeDef]
    action: NotRequired[ActionIdentifierTypeDef]
    resource: NotRequired[EntityIdentifierTypeDef]
    context: NotRequired[ContextDefinitionTypeDef]
    entities: NotRequired[EntitiesDefinitionTypeDef]


class IsAuthorizedWithTokenInputRequestTypeDef(TypedDict):
    policyStoreId: str
    identityToken: NotRequired[str]
    accessToken: NotRequired[str]
    action: NotRequired[ActionIdentifierTypeDef]
    resource: NotRequired[EntityIdentifierTypeDef]
    context: NotRequired[ContextDefinitionTypeDef]
    entities: NotRequired[EntitiesDefinitionTypeDef]


class ListIdentitySourcesOutputTypeDef(TypedDict):
    identitySources: List[IdentitySourceItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


BatchIsAuthorizedInputItemUnionTypeDef = Union[
    BatchIsAuthorizedInputItemTypeDef, BatchIsAuthorizedInputItemOutputTypeDef
]
BatchIsAuthorizedWithTokenInputItemUnionTypeDef = Union[
    BatchIsAuthorizedWithTokenInputItemTypeDef, BatchIsAuthorizedWithTokenInputItemOutputTypeDef
]


class BatchIsAuthorizedInputRequestTypeDef(TypedDict):
    policyStoreId: str
    requests: Sequence[BatchIsAuthorizedInputItemUnionTypeDef]
    entities: NotRequired[EntitiesDefinitionTypeDef]


class BatchIsAuthorizedWithTokenInputRequestTypeDef(TypedDict):
    policyStoreId: str
    requests: Sequence[BatchIsAuthorizedWithTokenInputItemUnionTypeDef]
    identityToken: NotRequired[str]
    accessToken: NotRequired[str]
    entities: NotRequired[EntitiesDefinitionTypeDef]
