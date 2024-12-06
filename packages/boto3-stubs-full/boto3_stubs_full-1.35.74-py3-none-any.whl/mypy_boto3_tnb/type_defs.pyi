"""
Type annotations for tnb service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_tnb/type_defs/)

Usage::

    ```python
    from mypy_boto3_tnb.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    LcmOperationTypeType,
    NsdOnboardingStateType,
    NsdOperationalStateType,
    NsdUsageStateType,
    NsLcmOperationStateType,
    NsStateType,
    OnboardingStateType,
    OperationalStateType,
    TaskStatusType,
    UpdateSolNetworkTypeType,
    UsageStateType,
    VnfInstantiationStateType,
    VnfOperationalStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "BlobTypeDef",
    "CancelSolNetworkOperationInputRequestTypeDef",
    "CreateSolFunctionPackageInputRequestTypeDef",
    "CreateSolFunctionPackageOutputTypeDef",
    "CreateSolNetworkInstanceInputRequestTypeDef",
    "CreateSolNetworkInstanceOutputTypeDef",
    "CreateSolNetworkPackageInputRequestTypeDef",
    "CreateSolNetworkPackageOutputTypeDef",
    "DeleteSolFunctionPackageInputRequestTypeDef",
    "DeleteSolNetworkInstanceInputRequestTypeDef",
    "DeleteSolNetworkPackageInputRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ErrorInfoTypeDef",
    "FunctionArtifactMetaTypeDef",
    "GetSolFunctionInstanceInputRequestTypeDef",
    "GetSolFunctionInstanceMetadataTypeDef",
    "GetSolFunctionInstanceOutputTypeDef",
    "GetSolFunctionPackageContentInputRequestTypeDef",
    "GetSolFunctionPackageContentOutputTypeDef",
    "GetSolFunctionPackageDescriptorInputRequestTypeDef",
    "GetSolFunctionPackageDescriptorOutputTypeDef",
    "GetSolFunctionPackageInputRequestTypeDef",
    "GetSolFunctionPackageMetadataTypeDef",
    "GetSolFunctionPackageOutputTypeDef",
    "GetSolInstantiatedVnfInfoTypeDef",
    "GetSolNetworkInstanceInputRequestTypeDef",
    "GetSolNetworkInstanceMetadataTypeDef",
    "GetSolNetworkInstanceOutputTypeDef",
    "GetSolNetworkOperationInputRequestTypeDef",
    "GetSolNetworkOperationMetadataTypeDef",
    "GetSolNetworkOperationOutputTypeDef",
    "GetSolNetworkOperationTaskDetailsTypeDef",
    "GetSolNetworkPackageContentInputRequestTypeDef",
    "GetSolNetworkPackageContentOutputTypeDef",
    "GetSolNetworkPackageDescriptorInputRequestTypeDef",
    "GetSolNetworkPackageDescriptorOutputTypeDef",
    "GetSolNetworkPackageInputRequestTypeDef",
    "GetSolNetworkPackageMetadataTypeDef",
    "GetSolNetworkPackageOutputTypeDef",
    "GetSolVnfInfoTypeDef",
    "GetSolVnfcResourceInfoMetadataTypeDef",
    "GetSolVnfcResourceInfoTypeDef",
    "InstantiateMetadataTypeDef",
    "InstantiateSolNetworkInstanceInputRequestTypeDef",
    "InstantiateSolNetworkInstanceOutputTypeDef",
    "LcmOperationInfoTypeDef",
    "ListSolFunctionInstanceInfoTypeDef",
    "ListSolFunctionInstanceMetadataTypeDef",
    "ListSolFunctionInstancesInputListSolFunctionInstancesPaginateTypeDef",
    "ListSolFunctionInstancesInputRequestTypeDef",
    "ListSolFunctionInstancesOutputTypeDef",
    "ListSolFunctionPackageInfoTypeDef",
    "ListSolFunctionPackageMetadataTypeDef",
    "ListSolFunctionPackagesInputListSolFunctionPackagesPaginateTypeDef",
    "ListSolFunctionPackagesInputRequestTypeDef",
    "ListSolFunctionPackagesOutputTypeDef",
    "ListSolNetworkInstanceInfoTypeDef",
    "ListSolNetworkInstanceMetadataTypeDef",
    "ListSolNetworkInstancesInputListSolNetworkInstancesPaginateTypeDef",
    "ListSolNetworkInstancesInputRequestTypeDef",
    "ListSolNetworkInstancesOutputTypeDef",
    "ListSolNetworkOperationsInfoTypeDef",
    "ListSolNetworkOperationsInputListSolNetworkOperationsPaginateTypeDef",
    "ListSolNetworkOperationsInputRequestTypeDef",
    "ListSolNetworkOperationsMetadataTypeDef",
    "ListSolNetworkOperationsOutputTypeDef",
    "ListSolNetworkPackageInfoTypeDef",
    "ListSolNetworkPackageMetadataTypeDef",
    "ListSolNetworkPackagesInputListSolNetworkPackagesPaginateTypeDef",
    "ListSolNetworkPackagesInputRequestTypeDef",
    "ListSolNetworkPackagesOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ModifyVnfInfoMetadataTypeDef",
    "NetworkArtifactMetaTypeDef",
    "PaginatorConfigTypeDef",
    "ProblemDetailsTypeDef",
    "PutSolFunctionPackageContentInputRequestTypeDef",
    "PutSolFunctionPackageContentMetadataTypeDef",
    "PutSolFunctionPackageContentOutputTypeDef",
    "PutSolNetworkPackageContentInputRequestTypeDef",
    "PutSolNetworkPackageContentMetadataTypeDef",
    "PutSolNetworkPackageContentOutputTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceInputRequestTypeDef",
    "TerminateSolNetworkInstanceInputRequestTypeDef",
    "TerminateSolNetworkInstanceOutputTypeDef",
    "ToscaOverrideTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateNsMetadataTypeDef",
    "UpdateSolFunctionPackageInputRequestTypeDef",
    "UpdateSolFunctionPackageOutputTypeDef",
    "UpdateSolNetworkInstanceInputRequestTypeDef",
    "UpdateSolNetworkInstanceOutputTypeDef",
    "UpdateSolNetworkModifyTypeDef",
    "UpdateSolNetworkPackageInputRequestTypeDef",
    "UpdateSolNetworkPackageOutputTypeDef",
    "UpdateSolNetworkServiceDataTypeDef",
    "ValidateSolFunctionPackageContentInputRequestTypeDef",
    "ValidateSolFunctionPackageContentMetadataTypeDef",
    "ValidateSolFunctionPackageContentOutputTypeDef",
    "ValidateSolNetworkPackageContentInputRequestTypeDef",
    "ValidateSolNetworkPackageContentMetadataTypeDef",
    "ValidateSolNetworkPackageContentOutputTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class CancelSolNetworkOperationInputRequestTypeDef(TypedDict):
    nsLcmOpOccId: str

class CreateSolFunctionPackageInputRequestTypeDef(TypedDict):
    tags: NotRequired[Mapping[str, str]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateSolNetworkInstanceInputRequestTypeDef(TypedDict):
    nsName: str
    nsdInfoId: str
    nsDescription: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class CreateSolNetworkPackageInputRequestTypeDef(TypedDict):
    tags: NotRequired[Mapping[str, str]]

class DeleteSolFunctionPackageInputRequestTypeDef(TypedDict):
    vnfPkgId: str

class DeleteSolNetworkInstanceInputRequestTypeDef(TypedDict):
    nsInstanceId: str

class DeleteSolNetworkPackageInputRequestTypeDef(TypedDict):
    nsdInfoId: str

class ErrorInfoTypeDef(TypedDict):
    cause: NotRequired[str]
    details: NotRequired[str]

class ToscaOverrideTypeDef(TypedDict):
    defaultValue: NotRequired[str]
    name: NotRequired[str]

class GetSolFunctionInstanceInputRequestTypeDef(TypedDict):
    vnfInstanceId: str

class GetSolFunctionInstanceMetadataTypeDef(TypedDict):
    createdAt: datetime
    lastModified: datetime

class GetSolFunctionPackageContentInputRequestTypeDef(TypedDict):
    accept: Literal["application/zip"]
    vnfPkgId: str

class GetSolFunctionPackageDescriptorInputRequestTypeDef(TypedDict):
    accept: Literal["text/plain"]
    vnfPkgId: str

class GetSolFunctionPackageInputRequestTypeDef(TypedDict):
    vnfPkgId: str

class GetSolInstantiatedVnfInfoTypeDef(TypedDict):
    vnfState: NotRequired[VnfOperationalStateType]

class GetSolNetworkInstanceInputRequestTypeDef(TypedDict):
    nsInstanceId: str

class GetSolNetworkInstanceMetadataTypeDef(TypedDict):
    createdAt: datetime
    lastModified: datetime

class LcmOperationInfoTypeDef(TypedDict):
    nsLcmOpOccId: str

class GetSolNetworkOperationInputRequestTypeDef(TypedDict):
    nsLcmOpOccId: str

class InstantiateMetadataTypeDef(TypedDict):
    nsdInfoId: str
    additionalParamsForNs: NotRequired[Dict[str, Any]]

class ModifyVnfInfoMetadataTypeDef(TypedDict):
    vnfConfigurableProperties: Dict[str, Any]
    vnfInstanceId: str

class UpdateNsMetadataTypeDef(TypedDict):
    nsdInfoId: str
    additionalParamsForNs: NotRequired[Dict[str, Any]]

class ProblemDetailsTypeDef(TypedDict):
    detail: str
    title: NotRequired[str]

class GetSolNetworkPackageContentInputRequestTypeDef(TypedDict):
    accept: Literal["application/zip"]
    nsdInfoId: str

class GetSolNetworkPackageDescriptorInputRequestTypeDef(TypedDict):
    nsdInfoId: str

class GetSolNetworkPackageInputRequestTypeDef(TypedDict):
    nsdInfoId: str

class GetSolVnfcResourceInfoMetadataTypeDef(TypedDict):
    cluster: NotRequired[str]
    helmChart: NotRequired[str]
    nodeGroup: NotRequired[str]

class InstantiateSolNetworkInstanceInputRequestTypeDef(TypedDict):
    nsInstanceId: str
    additionalParamsForNs: NotRequired[Mapping[str, Any]]
    dryRun: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]

class ListSolFunctionInstanceMetadataTypeDef(TypedDict):
    createdAt: datetime
    lastModified: datetime

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListSolFunctionInstancesInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListSolFunctionPackageMetadataTypeDef(TypedDict):
    createdAt: datetime
    lastModified: datetime

class ListSolFunctionPackagesInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListSolNetworkInstanceMetadataTypeDef(TypedDict):
    createdAt: datetime
    lastModified: datetime

class ListSolNetworkInstancesInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListSolNetworkOperationsMetadataTypeDef(TypedDict):
    createdAt: datetime
    lastModified: datetime
    nsdInfoId: NotRequired[str]
    vnfInstanceId: NotRequired[str]

class ListSolNetworkOperationsInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    nsInstanceId: NotRequired[str]

class ListSolNetworkPackageMetadataTypeDef(TypedDict):
    createdAt: datetime
    lastModified: datetime

class ListSolNetworkPackagesInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceInputRequestTypeDef(TypedDict):
    resourceArn: str

class TagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class TerminateSolNetworkInstanceInputRequestTypeDef(TypedDict):
    nsInstanceId: str
    tags: NotRequired[Mapping[str, str]]

class UntagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateSolFunctionPackageInputRequestTypeDef(TypedDict):
    operationalState: OperationalStateType
    vnfPkgId: str

class UpdateSolNetworkModifyTypeDef(TypedDict):
    vnfConfigurableProperties: Mapping[str, Any]
    vnfInstanceId: str

class UpdateSolNetworkServiceDataTypeDef(TypedDict):
    nsdInfoId: str
    additionalParamsForNs: NotRequired[Mapping[str, Any]]

class UpdateSolNetworkPackageInputRequestTypeDef(TypedDict):
    nsdInfoId: str
    nsdOperationalState: NsdOperationalStateType

class PutSolFunctionPackageContentInputRequestTypeDef(TypedDict):
    file: BlobTypeDef
    vnfPkgId: str
    contentType: NotRequired[Literal["application/zip"]]

class PutSolNetworkPackageContentInputRequestTypeDef(TypedDict):
    file: BlobTypeDef
    nsdInfoId: str
    contentType: NotRequired[Literal["application/zip"]]

class ValidateSolFunctionPackageContentInputRequestTypeDef(TypedDict):
    file: BlobTypeDef
    vnfPkgId: str
    contentType: NotRequired[Literal["application/zip"]]

class ValidateSolNetworkPackageContentInputRequestTypeDef(TypedDict):
    file: BlobTypeDef
    nsdInfoId: str
    contentType: NotRequired[Literal["application/zip"]]

CreateSolFunctionPackageOutputTypeDef = TypedDict(
    "CreateSolFunctionPackageOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "onboardingState": OnboardingStateType,
        "operationalState": OperationalStateType,
        "tags": Dict[str, str],
        "usageState": UsageStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateSolNetworkInstanceOutputTypeDef = TypedDict(
    "CreateSolNetworkInstanceOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "nsInstanceName": str,
        "nsdInfoId": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateSolNetworkPackageOutputTypeDef = TypedDict(
    "CreateSolNetworkPackageOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "nsdOnboardingState": NsdOnboardingStateType,
        "nsdOperationalState": NsdOperationalStateType,
        "nsdUsageState": NsdUsageStateType,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetSolFunctionPackageContentOutputTypeDef(TypedDict):
    contentType: Literal["application/zip"]
    packageContent: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef

class GetSolFunctionPackageDescriptorOutputTypeDef(TypedDict):
    contentType: Literal["text/plain"]
    vnfd: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef

class GetSolNetworkPackageContentOutputTypeDef(TypedDict):
    contentType: Literal["application/zip"]
    nsdContent: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef

class GetSolNetworkPackageDescriptorOutputTypeDef(TypedDict):
    contentType: Literal["text/plain"]
    nsd: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef

class InstantiateSolNetworkInstanceOutputTypeDef(TypedDict):
    nsLcmOpOccId: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class TerminateSolNetworkInstanceOutputTypeDef(TypedDict):
    nsLcmOpOccId: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSolFunctionPackageOutputTypeDef(TypedDict):
    operationalState: OperationalStateType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSolNetworkInstanceOutputTypeDef(TypedDict):
    nsLcmOpOccId: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSolNetworkPackageOutputTypeDef(TypedDict):
    nsdOperationalState: NsdOperationalStateType
    ResponseMetadata: ResponseMetadataTypeDef

class GetSolNetworkOperationTaskDetailsTypeDef(TypedDict):
    taskContext: NotRequired[Dict[str, str]]
    taskEndTime: NotRequired[datetime]
    taskErrorDetails: NotRequired[ErrorInfoTypeDef]
    taskName: NotRequired[str]
    taskStartTime: NotRequired[datetime]
    taskStatus: NotRequired[TaskStatusType]

class FunctionArtifactMetaTypeDef(TypedDict):
    overrides: NotRequired[List[ToscaOverrideTypeDef]]

class NetworkArtifactMetaTypeDef(TypedDict):
    overrides: NotRequired[List[ToscaOverrideTypeDef]]

GetSolNetworkInstanceOutputTypeDef = TypedDict(
    "GetSolNetworkInstanceOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "lcmOpInfo": LcmOperationInfoTypeDef,
        "metadata": GetSolNetworkInstanceMetadataTypeDef,
        "nsInstanceDescription": str,
        "nsInstanceName": str,
        "nsState": NsStateType,
        "nsdId": str,
        "nsdInfoId": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class GetSolNetworkOperationMetadataTypeDef(TypedDict):
    createdAt: datetime
    lastModified: datetime
    instantiateMetadata: NotRequired[InstantiateMetadataTypeDef]
    modifyVnfInfoMetadata: NotRequired[ModifyVnfInfoMetadataTypeDef]
    updateNsMetadata: NotRequired[UpdateNsMetadataTypeDef]

class GetSolVnfcResourceInfoTypeDef(TypedDict):
    metadata: NotRequired[GetSolVnfcResourceInfoMetadataTypeDef]

ListSolFunctionInstanceInfoTypeDef = TypedDict(
    "ListSolFunctionInstanceInfoTypeDef",
    {
        "arn": str,
        "id": str,
        "instantiationState": VnfInstantiationStateType,
        "metadata": ListSolFunctionInstanceMetadataTypeDef,
        "nsInstanceId": str,
        "vnfPkgId": str,
        "instantiatedVnfInfo": NotRequired[GetSolInstantiatedVnfInfoTypeDef],
        "vnfPkgName": NotRequired[str],
    },
)

class ListSolFunctionInstancesInputListSolFunctionInstancesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSolFunctionPackagesInputListSolFunctionPackagesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSolNetworkInstancesInputListSolNetworkInstancesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSolNetworkOperationsInputListSolNetworkOperationsPaginateTypeDef(TypedDict):
    nsInstanceId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSolNetworkPackagesInputListSolNetworkPackagesPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListSolFunctionPackageInfoTypeDef = TypedDict(
    "ListSolFunctionPackageInfoTypeDef",
    {
        "arn": str,
        "id": str,
        "onboardingState": OnboardingStateType,
        "operationalState": OperationalStateType,
        "usageState": UsageStateType,
        "metadata": NotRequired[ListSolFunctionPackageMetadataTypeDef],
        "vnfProductName": NotRequired[str],
        "vnfProvider": NotRequired[str],
        "vnfdId": NotRequired[str],
        "vnfdVersion": NotRequired[str],
    },
)
ListSolNetworkInstanceInfoTypeDef = TypedDict(
    "ListSolNetworkInstanceInfoTypeDef",
    {
        "arn": str,
        "id": str,
        "metadata": ListSolNetworkInstanceMetadataTypeDef,
        "nsInstanceDescription": str,
        "nsInstanceName": str,
        "nsState": NsStateType,
        "nsdId": str,
        "nsdInfoId": str,
    },
)
ListSolNetworkOperationsInfoTypeDef = TypedDict(
    "ListSolNetworkOperationsInfoTypeDef",
    {
        "arn": str,
        "id": str,
        "lcmOperationType": LcmOperationTypeType,
        "nsInstanceId": str,
        "operationState": NsLcmOperationStateType,
        "error": NotRequired[ProblemDetailsTypeDef],
        "metadata": NotRequired[ListSolNetworkOperationsMetadataTypeDef],
        "updateType": NotRequired[UpdateSolNetworkTypeType],
    },
)
ListSolNetworkPackageInfoTypeDef = TypedDict(
    "ListSolNetworkPackageInfoTypeDef",
    {
        "arn": str,
        "id": str,
        "metadata": ListSolNetworkPackageMetadataTypeDef,
        "nsdOnboardingState": NsdOnboardingStateType,
        "nsdOperationalState": NsdOperationalStateType,
        "nsdUsageState": NsdUsageStateType,
        "nsdDesigner": NotRequired[str],
        "nsdId": NotRequired[str],
        "nsdInvariantId": NotRequired[str],
        "nsdName": NotRequired[str],
        "nsdVersion": NotRequired[str],
        "vnfPkgIds": NotRequired[List[str]],
    },
)

class UpdateSolNetworkInstanceInputRequestTypeDef(TypedDict):
    nsInstanceId: str
    updateType: UpdateSolNetworkTypeType
    modifyVnfInfoData: NotRequired[UpdateSolNetworkModifyTypeDef]
    tags: NotRequired[Mapping[str, str]]
    updateNs: NotRequired[UpdateSolNetworkServiceDataTypeDef]

class GetSolFunctionPackageMetadataTypeDef(TypedDict):
    createdAt: datetime
    lastModified: datetime
    vnfd: NotRequired[FunctionArtifactMetaTypeDef]

class PutSolFunctionPackageContentMetadataTypeDef(TypedDict):
    vnfd: NotRequired[FunctionArtifactMetaTypeDef]

class ValidateSolFunctionPackageContentMetadataTypeDef(TypedDict):
    vnfd: NotRequired[FunctionArtifactMetaTypeDef]

class GetSolNetworkPackageMetadataTypeDef(TypedDict):
    createdAt: datetime
    lastModified: datetime
    nsd: NotRequired[NetworkArtifactMetaTypeDef]

class PutSolNetworkPackageContentMetadataTypeDef(TypedDict):
    nsd: NotRequired[NetworkArtifactMetaTypeDef]

class ValidateSolNetworkPackageContentMetadataTypeDef(TypedDict):
    nsd: NotRequired[NetworkArtifactMetaTypeDef]

GetSolNetworkOperationOutputTypeDef = TypedDict(
    "GetSolNetworkOperationOutputTypeDef",
    {
        "arn": str,
        "error": ProblemDetailsTypeDef,
        "id": str,
        "lcmOperationType": LcmOperationTypeType,
        "metadata": GetSolNetworkOperationMetadataTypeDef,
        "nsInstanceId": str,
        "operationState": NsLcmOperationStateType,
        "tags": Dict[str, str],
        "tasks": List[GetSolNetworkOperationTaskDetailsTypeDef],
        "updateType": UpdateSolNetworkTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class GetSolVnfInfoTypeDef(TypedDict):
    vnfState: NotRequired[VnfOperationalStateType]
    vnfcResourceInfo: NotRequired[List[GetSolVnfcResourceInfoTypeDef]]

class ListSolFunctionInstancesOutputTypeDef(TypedDict):
    functionInstances: List[ListSolFunctionInstanceInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSolFunctionPackagesOutputTypeDef(TypedDict):
    functionPackages: List[ListSolFunctionPackageInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSolNetworkInstancesOutputTypeDef(TypedDict):
    networkInstances: List[ListSolNetworkInstanceInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSolNetworkOperationsOutputTypeDef(TypedDict):
    networkOperations: List[ListSolNetworkOperationsInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSolNetworkPackagesOutputTypeDef(TypedDict):
    networkPackages: List[ListSolNetworkPackageInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

GetSolFunctionPackageOutputTypeDef = TypedDict(
    "GetSolFunctionPackageOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "metadata": GetSolFunctionPackageMetadataTypeDef,
        "onboardingState": OnboardingStateType,
        "operationalState": OperationalStateType,
        "tags": Dict[str, str],
        "usageState": UsageStateType,
        "vnfProductName": str,
        "vnfProvider": str,
        "vnfdId": str,
        "vnfdVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutSolFunctionPackageContentOutputTypeDef = TypedDict(
    "PutSolFunctionPackageContentOutputTypeDef",
    {
        "id": str,
        "metadata": PutSolFunctionPackageContentMetadataTypeDef,
        "vnfProductName": str,
        "vnfProvider": str,
        "vnfdId": str,
        "vnfdVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ValidateSolFunctionPackageContentOutputTypeDef = TypedDict(
    "ValidateSolFunctionPackageContentOutputTypeDef",
    {
        "id": str,
        "metadata": ValidateSolFunctionPackageContentMetadataTypeDef,
        "vnfProductName": str,
        "vnfProvider": str,
        "vnfdId": str,
        "vnfdVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSolNetworkPackageOutputTypeDef = TypedDict(
    "GetSolNetworkPackageOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "metadata": GetSolNetworkPackageMetadataTypeDef,
        "nsdId": str,
        "nsdName": str,
        "nsdOnboardingState": NsdOnboardingStateType,
        "nsdOperationalState": NsdOperationalStateType,
        "nsdUsageState": NsdUsageStateType,
        "nsdVersion": str,
        "tags": Dict[str, str],
        "vnfPkgIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutSolNetworkPackageContentOutputTypeDef = TypedDict(
    "PutSolNetworkPackageContentOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "metadata": PutSolNetworkPackageContentMetadataTypeDef,
        "nsdId": str,
        "nsdName": str,
        "nsdVersion": str,
        "vnfPkgIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ValidateSolNetworkPackageContentOutputTypeDef = TypedDict(
    "ValidateSolNetworkPackageContentOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "metadata": ValidateSolNetworkPackageContentMetadataTypeDef,
        "nsdId": str,
        "nsdName": str,
        "nsdVersion": str,
        "vnfPkgIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSolFunctionInstanceOutputTypeDef = TypedDict(
    "GetSolFunctionInstanceOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "instantiatedVnfInfo": GetSolVnfInfoTypeDef,
        "instantiationState": VnfInstantiationStateType,
        "metadata": GetSolFunctionInstanceMetadataTypeDef,
        "nsInstanceId": str,
        "tags": Dict[str, str],
        "vnfPkgId": str,
        "vnfProductName": str,
        "vnfProvider": str,
        "vnfdId": str,
        "vnfdVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
