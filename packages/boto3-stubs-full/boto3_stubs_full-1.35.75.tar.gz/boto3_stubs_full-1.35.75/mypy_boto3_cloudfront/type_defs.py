"""
Type annotations for cloudfront service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/type_defs/)

Usage::

    ```python
    from mypy_boto3_cloudfront.type_defs import AliasICPRecordalTypeDef

    data: AliasICPRecordalTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    CachePolicyCookieBehaviorType,
    CachePolicyHeaderBehaviorType,
    CachePolicyQueryStringBehaviorType,
    CachePolicyTypeType,
    CertificateSourceType,
    ContinuousDeploymentPolicyTypeType,
    EventTypeType,
    FrameOptionsListType,
    FunctionRuntimeType,
    FunctionStageType,
    GeoRestrictionTypeType,
    HttpVersionType,
    ICPRecordalStatusType,
    ItemSelectionType,
    MethodType,
    MinimumProtocolVersionType,
    OriginAccessControlOriginTypesType,
    OriginAccessControlSigningBehaviorsType,
    OriginGroupSelectionCriteriaType,
    OriginProtocolPolicyType,
    OriginRequestPolicyCookieBehaviorType,
    OriginRequestPolicyHeaderBehaviorType,
    OriginRequestPolicyQueryStringBehaviorType,
    OriginRequestPolicyTypeType,
    PriceClassType,
    RealtimeMetricsSubscriptionStatusType,
    ReferrerPolicyListType,
    ResponseHeadersPolicyAccessControlAllowMethodsValuesType,
    ResponseHeadersPolicyTypeType,
    SslProtocolType,
    SSLSupportMethodType,
    ViewerProtocolPolicyType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ActiveTrustedKeyGroupsTypeDef",
    "ActiveTrustedSignersTypeDef",
    "AliasICPRecordalTypeDef",
    "AliasesOutputTypeDef",
    "AliasesTypeDef",
    "AliasesUnionTypeDef",
    "AllowedMethodsOutputTypeDef",
    "AllowedMethodsTypeDef",
    "AllowedMethodsUnionTypeDef",
    "AnycastIpListCollectionTypeDef",
    "AnycastIpListSummaryTypeDef",
    "AnycastIpListTypeDef",
    "AssociateAliasRequestRequestTypeDef",
    "BlobTypeDef",
    "CacheBehaviorOutputTypeDef",
    "CacheBehaviorTypeDef",
    "CacheBehaviorUnionTypeDef",
    "CacheBehaviorsOutputTypeDef",
    "CacheBehaviorsTypeDef",
    "CacheBehaviorsUnionTypeDef",
    "CachePolicyConfigOutputTypeDef",
    "CachePolicyConfigTypeDef",
    "CachePolicyCookiesConfigOutputTypeDef",
    "CachePolicyCookiesConfigTypeDef",
    "CachePolicyCookiesConfigUnionTypeDef",
    "CachePolicyHeadersConfigOutputTypeDef",
    "CachePolicyHeadersConfigTypeDef",
    "CachePolicyHeadersConfigUnionTypeDef",
    "CachePolicyListTypeDef",
    "CachePolicyQueryStringsConfigOutputTypeDef",
    "CachePolicyQueryStringsConfigTypeDef",
    "CachePolicyQueryStringsConfigUnionTypeDef",
    "CachePolicySummaryTypeDef",
    "CachePolicyTypeDef",
    "CachedMethodsOutputTypeDef",
    "CachedMethodsTypeDef",
    "CachedMethodsUnionTypeDef",
    "CloudFrontOriginAccessIdentityConfigTypeDef",
    "CloudFrontOriginAccessIdentityListTypeDef",
    "CloudFrontOriginAccessIdentitySummaryTypeDef",
    "CloudFrontOriginAccessIdentityTypeDef",
    "ConflictingAliasTypeDef",
    "ConflictingAliasesListTypeDef",
    "ContentTypeProfileConfigOutputTypeDef",
    "ContentTypeProfileConfigTypeDef",
    "ContentTypeProfileConfigUnionTypeDef",
    "ContentTypeProfileTypeDef",
    "ContentTypeProfilesOutputTypeDef",
    "ContentTypeProfilesTypeDef",
    "ContentTypeProfilesUnionTypeDef",
    "ContinuousDeploymentPolicyConfigOutputTypeDef",
    "ContinuousDeploymentPolicyConfigTypeDef",
    "ContinuousDeploymentPolicyListTypeDef",
    "ContinuousDeploymentPolicySummaryTypeDef",
    "ContinuousDeploymentPolicyTypeDef",
    "ContinuousDeploymentSingleHeaderConfigTypeDef",
    "ContinuousDeploymentSingleWeightConfigTypeDef",
    "CookieNamesOutputTypeDef",
    "CookieNamesTypeDef",
    "CookieNamesUnionTypeDef",
    "CookiePreferenceOutputTypeDef",
    "CookiePreferenceTypeDef",
    "CookiePreferenceUnionTypeDef",
    "CopyDistributionRequestRequestTypeDef",
    "CopyDistributionResultTypeDef",
    "CreateAnycastIpListRequestRequestTypeDef",
    "CreateAnycastIpListResultTypeDef",
    "CreateCachePolicyRequestRequestTypeDef",
    "CreateCachePolicyResultTypeDef",
    "CreateCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    "CreateCloudFrontOriginAccessIdentityResultTypeDef",
    "CreateContinuousDeploymentPolicyRequestRequestTypeDef",
    "CreateContinuousDeploymentPolicyResultTypeDef",
    "CreateDistributionRequestRequestTypeDef",
    "CreateDistributionResultTypeDef",
    "CreateDistributionWithTagsRequestRequestTypeDef",
    "CreateDistributionWithTagsResultTypeDef",
    "CreateFieldLevelEncryptionConfigRequestRequestTypeDef",
    "CreateFieldLevelEncryptionConfigResultTypeDef",
    "CreateFieldLevelEncryptionProfileRequestRequestTypeDef",
    "CreateFieldLevelEncryptionProfileResultTypeDef",
    "CreateFunctionRequestRequestTypeDef",
    "CreateFunctionResultTypeDef",
    "CreateInvalidationRequestRequestTypeDef",
    "CreateInvalidationResultTypeDef",
    "CreateKeyGroupRequestRequestTypeDef",
    "CreateKeyGroupResultTypeDef",
    "CreateKeyValueStoreRequestRequestTypeDef",
    "CreateKeyValueStoreResultTypeDef",
    "CreateMonitoringSubscriptionRequestRequestTypeDef",
    "CreateMonitoringSubscriptionResultTypeDef",
    "CreateOriginAccessControlRequestRequestTypeDef",
    "CreateOriginAccessControlResultTypeDef",
    "CreateOriginRequestPolicyRequestRequestTypeDef",
    "CreateOriginRequestPolicyResultTypeDef",
    "CreatePublicKeyRequestRequestTypeDef",
    "CreatePublicKeyResultTypeDef",
    "CreateRealtimeLogConfigRequestRequestTypeDef",
    "CreateRealtimeLogConfigResultTypeDef",
    "CreateResponseHeadersPolicyRequestRequestTypeDef",
    "CreateResponseHeadersPolicyResultTypeDef",
    "CreateStreamingDistributionRequestRequestTypeDef",
    "CreateStreamingDistributionResultTypeDef",
    "CreateStreamingDistributionWithTagsRequestRequestTypeDef",
    "CreateStreamingDistributionWithTagsResultTypeDef",
    "CreateVpcOriginRequestRequestTypeDef",
    "CreateVpcOriginResultTypeDef",
    "CustomErrorResponseTypeDef",
    "CustomErrorResponsesOutputTypeDef",
    "CustomErrorResponsesTypeDef",
    "CustomErrorResponsesUnionTypeDef",
    "CustomHeadersOutputTypeDef",
    "CustomHeadersTypeDef",
    "CustomHeadersUnionTypeDef",
    "CustomOriginConfigOutputTypeDef",
    "CustomOriginConfigTypeDef",
    "CustomOriginConfigUnionTypeDef",
    "DefaultCacheBehaviorOutputTypeDef",
    "DefaultCacheBehaviorTypeDef",
    "DefaultCacheBehaviorUnionTypeDef",
    "DeleteAnycastIpListRequestRequestTypeDef",
    "DeleteCachePolicyRequestRequestTypeDef",
    "DeleteCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    "DeleteContinuousDeploymentPolicyRequestRequestTypeDef",
    "DeleteDistributionRequestRequestTypeDef",
    "DeleteFieldLevelEncryptionConfigRequestRequestTypeDef",
    "DeleteFieldLevelEncryptionProfileRequestRequestTypeDef",
    "DeleteFunctionRequestRequestTypeDef",
    "DeleteKeyGroupRequestRequestTypeDef",
    "DeleteKeyValueStoreRequestRequestTypeDef",
    "DeleteMonitoringSubscriptionRequestRequestTypeDef",
    "DeleteOriginAccessControlRequestRequestTypeDef",
    "DeleteOriginRequestPolicyRequestRequestTypeDef",
    "DeletePublicKeyRequestRequestTypeDef",
    "DeleteRealtimeLogConfigRequestRequestTypeDef",
    "DeleteResponseHeadersPolicyRequestRequestTypeDef",
    "DeleteStreamingDistributionRequestRequestTypeDef",
    "DeleteVpcOriginRequestRequestTypeDef",
    "DeleteVpcOriginResultTypeDef",
    "DescribeFunctionRequestRequestTypeDef",
    "DescribeFunctionResultTypeDef",
    "DescribeKeyValueStoreRequestRequestTypeDef",
    "DescribeKeyValueStoreResultTypeDef",
    "DistributionConfigOutputTypeDef",
    "DistributionConfigTypeDef",
    "DistributionConfigUnionTypeDef",
    "DistributionConfigWithTagsTypeDef",
    "DistributionIdListTypeDef",
    "DistributionListTypeDef",
    "DistributionSummaryTypeDef",
    "DistributionTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionEntitiesOutputTypeDef",
    "EncryptionEntitiesTypeDef",
    "EncryptionEntitiesUnionTypeDef",
    "EncryptionEntityOutputTypeDef",
    "EncryptionEntityTypeDef",
    "EncryptionEntityUnionTypeDef",
    "EndPointTypeDef",
    "FieldLevelEncryptionConfigOutputTypeDef",
    "FieldLevelEncryptionConfigTypeDef",
    "FieldLevelEncryptionListTypeDef",
    "FieldLevelEncryptionProfileConfigOutputTypeDef",
    "FieldLevelEncryptionProfileConfigTypeDef",
    "FieldLevelEncryptionProfileListTypeDef",
    "FieldLevelEncryptionProfileSummaryTypeDef",
    "FieldLevelEncryptionProfileTypeDef",
    "FieldLevelEncryptionSummaryTypeDef",
    "FieldLevelEncryptionTypeDef",
    "FieldPatternsOutputTypeDef",
    "FieldPatternsTypeDef",
    "FieldPatternsUnionTypeDef",
    "ForwardedValuesOutputTypeDef",
    "ForwardedValuesTypeDef",
    "ForwardedValuesUnionTypeDef",
    "FunctionAssociationTypeDef",
    "FunctionAssociationsOutputTypeDef",
    "FunctionAssociationsTypeDef",
    "FunctionAssociationsUnionTypeDef",
    "FunctionConfigOutputTypeDef",
    "FunctionConfigTypeDef",
    "FunctionListTypeDef",
    "FunctionMetadataTypeDef",
    "FunctionSummaryTypeDef",
    "GeoRestrictionOutputTypeDef",
    "GeoRestrictionTypeDef",
    "GeoRestrictionUnionTypeDef",
    "GetAnycastIpListRequestRequestTypeDef",
    "GetAnycastIpListResultTypeDef",
    "GetCachePolicyConfigRequestRequestTypeDef",
    "GetCachePolicyConfigResultTypeDef",
    "GetCachePolicyRequestRequestTypeDef",
    "GetCachePolicyResultTypeDef",
    "GetCloudFrontOriginAccessIdentityConfigRequestRequestTypeDef",
    "GetCloudFrontOriginAccessIdentityConfigResultTypeDef",
    "GetCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    "GetCloudFrontOriginAccessIdentityResultTypeDef",
    "GetContinuousDeploymentPolicyConfigRequestRequestTypeDef",
    "GetContinuousDeploymentPolicyConfigResultTypeDef",
    "GetContinuousDeploymentPolicyRequestRequestTypeDef",
    "GetContinuousDeploymentPolicyResultTypeDef",
    "GetDistributionConfigRequestRequestTypeDef",
    "GetDistributionConfigResultTypeDef",
    "GetDistributionRequestDistributionDeployedWaitTypeDef",
    "GetDistributionRequestRequestTypeDef",
    "GetDistributionResultTypeDef",
    "GetFieldLevelEncryptionConfigRequestRequestTypeDef",
    "GetFieldLevelEncryptionConfigResultTypeDef",
    "GetFieldLevelEncryptionProfileConfigRequestRequestTypeDef",
    "GetFieldLevelEncryptionProfileConfigResultTypeDef",
    "GetFieldLevelEncryptionProfileRequestRequestTypeDef",
    "GetFieldLevelEncryptionProfileResultTypeDef",
    "GetFieldLevelEncryptionRequestRequestTypeDef",
    "GetFieldLevelEncryptionResultTypeDef",
    "GetFunctionRequestRequestTypeDef",
    "GetFunctionResultTypeDef",
    "GetInvalidationRequestInvalidationCompletedWaitTypeDef",
    "GetInvalidationRequestRequestTypeDef",
    "GetInvalidationResultTypeDef",
    "GetKeyGroupConfigRequestRequestTypeDef",
    "GetKeyGroupConfigResultTypeDef",
    "GetKeyGroupRequestRequestTypeDef",
    "GetKeyGroupResultTypeDef",
    "GetMonitoringSubscriptionRequestRequestTypeDef",
    "GetMonitoringSubscriptionResultTypeDef",
    "GetOriginAccessControlConfigRequestRequestTypeDef",
    "GetOriginAccessControlConfigResultTypeDef",
    "GetOriginAccessControlRequestRequestTypeDef",
    "GetOriginAccessControlResultTypeDef",
    "GetOriginRequestPolicyConfigRequestRequestTypeDef",
    "GetOriginRequestPolicyConfigResultTypeDef",
    "GetOriginRequestPolicyRequestRequestTypeDef",
    "GetOriginRequestPolicyResultTypeDef",
    "GetPublicKeyConfigRequestRequestTypeDef",
    "GetPublicKeyConfigResultTypeDef",
    "GetPublicKeyRequestRequestTypeDef",
    "GetPublicKeyResultTypeDef",
    "GetRealtimeLogConfigRequestRequestTypeDef",
    "GetRealtimeLogConfigResultTypeDef",
    "GetResponseHeadersPolicyConfigRequestRequestTypeDef",
    "GetResponseHeadersPolicyConfigResultTypeDef",
    "GetResponseHeadersPolicyRequestRequestTypeDef",
    "GetResponseHeadersPolicyResultTypeDef",
    "GetStreamingDistributionConfigRequestRequestTypeDef",
    "GetStreamingDistributionConfigResultTypeDef",
    "GetStreamingDistributionRequestRequestTypeDef",
    "GetStreamingDistributionRequestStreamingDistributionDeployedWaitTypeDef",
    "GetStreamingDistributionResultTypeDef",
    "GetVpcOriginRequestRequestTypeDef",
    "GetVpcOriginResultTypeDef",
    "GrpcConfigTypeDef",
    "HeadersOutputTypeDef",
    "HeadersTypeDef",
    "HeadersUnionTypeDef",
    "ImportSourceTypeDef",
    "InvalidationBatchOutputTypeDef",
    "InvalidationBatchTypeDef",
    "InvalidationListTypeDef",
    "InvalidationSummaryTypeDef",
    "InvalidationTypeDef",
    "KGKeyPairIdsTypeDef",
    "KeyGroupConfigOutputTypeDef",
    "KeyGroupConfigTypeDef",
    "KeyGroupListTypeDef",
    "KeyGroupSummaryTypeDef",
    "KeyGroupTypeDef",
    "KeyPairIdsTypeDef",
    "KeyValueStoreAssociationTypeDef",
    "KeyValueStoreAssociationsOutputTypeDef",
    "KeyValueStoreAssociationsTypeDef",
    "KeyValueStoreAssociationsUnionTypeDef",
    "KeyValueStoreListTypeDef",
    "KeyValueStoreTypeDef",
    "KinesisStreamConfigTypeDef",
    "LambdaFunctionAssociationTypeDef",
    "LambdaFunctionAssociationsOutputTypeDef",
    "LambdaFunctionAssociationsTypeDef",
    "LambdaFunctionAssociationsUnionTypeDef",
    "ListAnycastIpListsRequestRequestTypeDef",
    "ListAnycastIpListsResultTypeDef",
    "ListCachePoliciesRequestRequestTypeDef",
    "ListCachePoliciesResultTypeDef",
    "ListCloudFrontOriginAccessIdentitiesRequestListCloudFrontOriginAccessIdentitiesPaginateTypeDef",
    "ListCloudFrontOriginAccessIdentitiesRequestRequestTypeDef",
    "ListCloudFrontOriginAccessIdentitiesResultTypeDef",
    "ListConflictingAliasesRequestRequestTypeDef",
    "ListConflictingAliasesResultTypeDef",
    "ListContinuousDeploymentPoliciesRequestRequestTypeDef",
    "ListContinuousDeploymentPoliciesResultTypeDef",
    "ListDistributionsByAnycastIpListIdRequestRequestTypeDef",
    "ListDistributionsByAnycastIpListIdResultTypeDef",
    "ListDistributionsByCachePolicyIdRequestRequestTypeDef",
    "ListDistributionsByCachePolicyIdResultTypeDef",
    "ListDistributionsByKeyGroupRequestRequestTypeDef",
    "ListDistributionsByKeyGroupResultTypeDef",
    "ListDistributionsByOriginRequestPolicyIdRequestRequestTypeDef",
    "ListDistributionsByOriginRequestPolicyIdResultTypeDef",
    "ListDistributionsByRealtimeLogConfigRequestRequestTypeDef",
    "ListDistributionsByRealtimeLogConfigResultTypeDef",
    "ListDistributionsByResponseHeadersPolicyIdRequestRequestTypeDef",
    "ListDistributionsByResponseHeadersPolicyIdResultTypeDef",
    "ListDistributionsByVpcOriginIdRequestRequestTypeDef",
    "ListDistributionsByVpcOriginIdResultTypeDef",
    "ListDistributionsByWebACLIdRequestRequestTypeDef",
    "ListDistributionsByWebACLIdResultTypeDef",
    "ListDistributionsRequestListDistributionsPaginateTypeDef",
    "ListDistributionsRequestRequestTypeDef",
    "ListDistributionsResultTypeDef",
    "ListFieldLevelEncryptionConfigsRequestRequestTypeDef",
    "ListFieldLevelEncryptionConfigsResultTypeDef",
    "ListFieldLevelEncryptionProfilesRequestRequestTypeDef",
    "ListFieldLevelEncryptionProfilesResultTypeDef",
    "ListFunctionsRequestRequestTypeDef",
    "ListFunctionsResultTypeDef",
    "ListInvalidationsRequestListInvalidationsPaginateTypeDef",
    "ListInvalidationsRequestRequestTypeDef",
    "ListInvalidationsResultTypeDef",
    "ListKeyGroupsRequestRequestTypeDef",
    "ListKeyGroupsResultTypeDef",
    "ListKeyValueStoresRequestListKeyValueStoresPaginateTypeDef",
    "ListKeyValueStoresRequestRequestTypeDef",
    "ListKeyValueStoresResultTypeDef",
    "ListOriginAccessControlsRequestRequestTypeDef",
    "ListOriginAccessControlsResultTypeDef",
    "ListOriginRequestPoliciesRequestRequestTypeDef",
    "ListOriginRequestPoliciesResultTypeDef",
    "ListPublicKeysRequestListPublicKeysPaginateTypeDef",
    "ListPublicKeysRequestRequestTypeDef",
    "ListPublicKeysResultTypeDef",
    "ListRealtimeLogConfigsRequestRequestTypeDef",
    "ListRealtimeLogConfigsResultTypeDef",
    "ListResponseHeadersPoliciesRequestRequestTypeDef",
    "ListResponseHeadersPoliciesResultTypeDef",
    "ListStreamingDistributionsRequestListStreamingDistributionsPaginateTypeDef",
    "ListStreamingDistributionsRequestRequestTypeDef",
    "ListStreamingDistributionsResultTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResultTypeDef",
    "ListVpcOriginsRequestRequestTypeDef",
    "ListVpcOriginsResultTypeDef",
    "LoggingConfigTypeDef",
    "MonitoringSubscriptionTypeDef",
    "OriginAccessControlConfigTypeDef",
    "OriginAccessControlListTypeDef",
    "OriginAccessControlSummaryTypeDef",
    "OriginAccessControlTypeDef",
    "OriginCustomHeaderTypeDef",
    "OriginGroupFailoverCriteriaOutputTypeDef",
    "OriginGroupFailoverCriteriaTypeDef",
    "OriginGroupFailoverCriteriaUnionTypeDef",
    "OriginGroupMemberTypeDef",
    "OriginGroupMembersOutputTypeDef",
    "OriginGroupMembersTypeDef",
    "OriginGroupMembersUnionTypeDef",
    "OriginGroupOutputTypeDef",
    "OriginGroupTypeDef",
    "OriginGroupUnionTypeDef",
    "OriginGroupsOutputTypeDef",
    "OriginGroupsTypeDef",
    "OriginGroupsUnionTypeDef",
    "OriginOutputTypeDef",
    "OriginRequestPolicyConfigOutputTypeDef",
    "OriginRequestPolicyConfigTypeDef",
    "OriginRequestPolicyCookiesConfigOutputTypeDef",
    "OriginRequestPolicyCookiesConfigTypeDef",
    "OriginRequestPolicyCookiesConfigUnionTypeDef",
    "OriginRequestPolicyHeadersConfigOutputTypeDef",
    "OriginRequestPolicyHeadersConfigTypeDef",
    "OriginRequestPolicyHeadersConfigUnionTypeDef",
    "OriginRequestPolicyListTypeDef",
    "OriginRequestPolicyQueryStringsConfigOutputTypeDef",
    "OriginRequestPolicyQueryStringsConfigTypeDef",
    "OriginRequestPolicyQueryStringsConfigUnionTypeDef",
    "OriginRequestPolicySummaryTypeDef",
    "OriginRequestPolicyTypeDef",
    "OriginShieldTypeDef",
    "OriginSslProtocolsOutputTypeDef",
    "OriginSslProtocolsTypeDef",
    "OriginSslProtocolsUnionTypeDef",
    "OriginTypeDef",
    "OriginUnionTypeDef",
    "OriginsOutputTypeDef",
    "OriginsTypeDef",
    "OriginsUnionTypeDef",
    "PaginatorConfigTypeDef",
    "ParametersInCacheKeyAndForwardedToOriginOutputTypeDef",
    "ParametersInCacheKeyAndForwardedToOriginTypeDef",
    "ParametersInCacheKeyAndForwardedToOriginUnionTypeDef",
    "PathsOutputTypeDef",
    "PathsTypeDef",
    "PathsUnionTypeDef",
    "PublicKeyConfigTypeDef",
    "PublicKeyListTypeDef",
    "PublicKeySummaryTypeDef",
    "PublicKeyTypeDef",
    "PublishFunctionRequestRequestTypeDef",
    "PublishFunctionResultTypeDef",
    "QueryArgProfileConfigOutputTypeDef",
    "QueryArgProfileConfigTypeDef",
    "QueryArgProfileConfigUnionTypeDef",
    "QueryArgProfileTypeDef",
    "QueryArgProfilesOutputTypeDef",
    "QueryArgProfilesTypeDef",
    "QueryArgProfilesUnionTypeDef",
    "QueryStringCacheKeysOutputTypeDef",
    "QueryStringCacheKeysTypeDef",
    "QueryStringCacheKeysUnionTypeDef",
    "QueryStringNamesOutputTypeDef",
    "QueryStringNamesTypeDef",
    "QueryStringNamesUnionTypeDef",
    "RealtimeLogConfigTypeDef",
    "RealtimeLogConfigsTypeDef",
    "RealtimeMetricsSubscriptionConfigTypeDef",
    "ResponseHeadersPolicyAccessControlAllowHeadersOutputTypeDef",
    "ResponseHeadersPolicyAccessControlAllowHeadersTypeDef",
    "ResponseHeadersPolicyAccessControlAllowHeadersUnionTypeDef",
    "ResponseHeadersPolicyAccessControlAllowMethodsOutputTypeDef",
    "ResponseHeadersPolicyAccessControlAllowMethodsTypeDef",
    "ResponseHeadersPolicyAccessControlAllowMethodsUnionTypeDef",
    "ResponseHeadersPolicyAccessControlAllowOriginsOutputTypeDef",
    "ResponseHeadersPolicyAccessControlAllowOriginsTypeDef",
    "ResponseHeadersPolicyAccessControlAllowOriginsUnionTypeDef",
    "ResponseHeadersPolicyAccessControlExposeHeadersOutputTypeDef",
    "ResponseHeadersPolicyAccessControlExposeHeadersTypeDef",
    "ResponseHeadersPolicyAccessControlExposeHeadersUnionTypeDef",
    "ResponseHeadersPolicyConfigOutputTypeDef",
    "ResponseHeadersPolicyConfigTypeDef",
    "ResponseHeadersPolicyContentSecurityPolicyTypeDef",
    "ResponseHeadersPolicyContentTypeOptionsTypeDef",
    "ResponseHeadersPolicyCorsConfigOutputTypeDef",
    "ResponseHeadersPolicyCorsConfigTypeDef",
    "ResponseHeadersPolicyCorsConfigUnionTypeDef",
    "ResponseHeadersPolicyCustomHeaderTypeDef",
    "ResponseHeadersPolicyCustomHeadersConfigOutputTypeDef",
    "ResponseHeadersPolicyCustomHeadersConfigTypeDef",
    "ResponseHeadersPolicyCustomHeadersConfigUnionTypeDef",
    "ResponseHeadersPolicyFrameOptionsTypeDef",
    "ResponseHeadersPolicyListTypeDef",
    "ResponseHeadersPolicyReferrerPolicyTypeDef",
    "ResponseHeadersPolicyRemoveHeaderTypeDef",
    "ResponseHeadersPolicyRemoveHeadersConfigOutputTypeDef",
    "ResponseHeadersPolicyRemoveHeadersConfigTypeDef",
    "ResponseHeadersPolicyRemoveHeadersConfigUnionTypeDef",
    "ResponseHeadersPolicySecurityHeadersConfigTypeDef",
    "ResponseHeadersPolicyServerTimingHeadersConfigTypeDef",
    "ResponseHeadersPolicyStrictTransportSecurityTypeDef",
    "ResponseHeadersPolicySummaryTypeDef",
    "ResponseHeadersPolicyTypeDef",
    "ResponseHeadersPolicyXSSProtectionTypeDef",
    "ResponseMetadataTypeDef",
    "RestrictionsOutputTypeDef",
    "RestrictionsTypeDef",
    "RestrictionsUnionTypeDef",
    "S3OriginConfigTypeDef",
    "S3OriginTypeDef",
    "SessionStickinessConfigTypeDef",
    "SignerTypeDef",
    "StagingDistributionDnsNamesOutputTypeDef",
    "StagingDistributionDnsNamesTypeDef",
    "StagingDistributionDnsNamesUnionTypeDef",
    "StatusCodesOutputTypeDef",
    "StatusCodesTypeDef",
    "StatusCodesUnionTypeDef",
    "StreamingDistributionConfigOutputTypeDef",
    "StreamingDistributionConfigTypeDef",
    "StreamingDistributionConfigUnionTypeDef",
    "StreamingDistributionConfigWithTagsTypeDef",
    "StreamingDistributionListTypeDef",
    "StreamingDistributionSummaryTypeDef",
    "StreamingDistributionTypeDef",
    "StreamingLoggingConfigTypeDef",
    "TagKeysTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TagsOutputTypeDef",
    "TagsTypeDef",
    "TagsUnionTypeDef",
    "TestFunctionRequestRequestTypeDef",
    "TestFunctionResultTypeDef",
    "TestResultTypeDef",
    "TrafficConfigTypeDef",
    "TrustedKeyGroupsOutputTypeDef",
    "TrustedKeyGroupsTypeDef",
    "TrustedKeyGroupsUnionTypeDef",
    "TrustedSignersOutputTypeDef",
    "TrustedSignersTypeDef",
    "TrustedSignersUnionTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCachePolicyRequestRequestTypeDef",
    "UpdateCachePolicyResultTypeDef",
    "UpdateCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    "UpdateCloudFrontOriginAccessIdentityResultTypeDef",
    "UpdateContinuousDeploymentPolicyRequestRequestTypeDef",
    "UpdateContinuousDeploymentPolicyResultTypeDef",
    "UpdateDistributionRequestRequestTypeDef",
    "UpdateDistributionResultTypeDef",
    "UpdateDistributionWithStagingConfigRequestRequestTypeDef",
    "UpdateDistributionWithStagingConfigResultTypeDef",
    "UpdateFieldLevelEncryptionConfigRequestRequestTypeDef",
    "UpdateFieldLevelEncryptionConfigResultTypeDef",
    "UpdateFieldLevelEncryptionProfileRequestRequestTypeDef",
    "UpdateFieldLevelEncryptionProfileResultTypeDef",
    "UpdateFunctionRequestRequestTypeDef",
    "UpdateFunctionResultTypeDef",
    "UpdateKeyGroupRequestRequestTypeDef",
    "UpdateKeyGroupResultTypeDef",
    "UpdateKeyValueStoreRequestRequestTypeDef",
    "UpdateKeyValueStoreResultTypeDef",
    "UpdateOriginAccessControlRequestRequestTypeDef",
    "UpdateOriginAccessControlResultTypeDef",
    "UpdateOriginRequestPolicyRequestRequestTypeDef",
    "UpdateOriginRequestPolicyResultTypeDef",
    "UpdatePublicKeyRequestRequestTypeDef",
    "UpdatePublicKeyResultTypeDef",
    "UpdateRealtimeLogConfigRequestRequestTypeDef",
    "UpdateRealtimeLogConfigResultTypeDef",
    "UpdateResponseHeadersPolicyRequestRequestTypeDef",
    "UpdateResponseHeadersPolicyResultTypeDef",
    "UpdateStreamingDistributionRequestRequestTypeDef",
    "UpdateStreamingDistributionResultTypeDef",
    "UpdateVpcOriginRequestRequestTypeDef",
    "UpdateVpcOriginResultTypeDef",
    "ViewerCertificateTypeDef",
    "VpcOriginConfigTypeDef",
    "VpcOriginEndpointConfigOutputTypeDef",
    "VpcOriginEndpointConfigTypeDef",
    "VpcOriginListTypeDef",
    "VpcOriginSummaryTypeDef",
    "VpcOriginTypeDef",
    "WaiterConfigTypeDef",
)


class AliasICPRecordalTypeDef(TypedDict):
    CNAME: NotRequired[str]
    ICPRecordalStatus: NotRequired[ICPRecordalStatusType]


class AliasesOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[str]]


class AliasesTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[str]]


class CachedMethodsOutputTypeDef(TypedDict):
    Quantity: int
    Items: List[MethodType]


class AnycastIpListSummaryTypeDef(TypedDict):
    Id: str
    Name: str
    Status: str
    Arn: str
    IpCount: int
    LastModifiedTime: datetime


class AnycastIpListTypeDef(TypedDict):
    Id: str
    Name: str
    Status: str
    Arn: str
    AnycastIps: List[str]
    IpCount: int
    LastModifiedTime: datetime


class AssociateAliasRequestRequestTypeDef(TypedDict):
    TargetDistributionId: str
    Alias: str


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class GrpcConfigTypeDef(TypedDict):
    Enabled: bool


class TrustedKeyGroupsOutputTypeDef(TypedDict):
    Enabled: bool
    Quantity: int
    Items: NotRequired[List[str]]


class TrustedSignersOutputTypeDef(TypedDict):
    Enabled: bool
    Quantity: int
    Items: NotRequired[List[str]]


class CookieNamesOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[str]]


class HeadersOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[str]]


class QueryStringNamesOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[str]]


class CachedMethodsTypeDef(TypedDict):
    Quantity: int
    Items: Sequence[MethodType]


class CloudFrontOriginAccessIdentityConfigTypeDef(TypedDict):
    CallerReference: str
    Comment: str


class CloudFrontOriginAccessIdentitySummaryTypeDef(TypedDict):
    Id: str
    S3CanonicalUserId: str
    Comment: str


class ConflictingAliasTypeDef(TypedDict):
    Alias: NotRequired[str]
    DistributionId: NotRequired[str]
    AccountId: NotRequired[str]


class ContentTypeProfileTypeDef(TypedDict):
    Format: Literal["URLEncoded"]
    ContentType: str
    ProfileId: NotRequired[str]


class StagingDistributionDnsNamesOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[str]]


class ContinuousDeploymentSingleHeaderConfigTypeDef(TypedDict):
    Header: str
    Value: str


class SessionStickinessConfigTypeDef(TypedDict):
    IdleTTL: int
    MaximumTTL: int


class CookieNamesTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[str]]


class CopyDistributionRequestRequestTypeDef(TypedDict):
    PrimaryDistributionId: str
    CallerReference: str
    Staging: NotRequired[bool]
    IfMatch: NotRequired[str]
    Enabled: NotRequired[bool]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class KeyGroupConfigTypeDef(TypedDict):
    Name: str
    Items: Sequence[str]
    Comment: NotRequired[str]


class ImportSourceTypeDef(TypedDict):
    SourceType: Literal["S3"]
    SourceARN: str


class KeyValueStoreTypeDef(TypedDict):
    Name: str
    Id: str
    Comment: str
    ARN: str
    LastModifiedTime: datetime
    Status: NotRequired[str]


class OriginAccessControlConfigTypeDef(TypedDict):
    Name: str
    SigningProtocol: Literal["sigv4"]
    SigningBehavior: OriginAccessControlSigningBehaviorsType
    OriginAccessControlOriginType: OriginAccessControlOriginTypesType
    Description: NotRequired[str]


class PublicKeyConfigTypeDef(TypedDict):
    CallerReference: str
    Name: str
    EncodedKey: str
    Comment: NotRequired[str]


class CustomErrorResponseTypeDef(TypedDict):
    ErrorCode: int
    ResponsePagePath: NotRequired[str]
    ResponseCode: NotRequired[str]
    ErrorCachingMinTTL: NotRequired[int]


class OriginCustomHeaderTypeDef(TypedDict):
    HeaderName: str
    HeaderValue: str


class OriginSslProtocolsOutputTypeDef(TypedDict):
    Quantity: int
    Items: List[SslProtocolType]


class DeleteAnycastIpListRequestRequestTypeDef(TypedDict):
    Id: str
    IfMatch: str


class DeleteCachePolicyRequestRequestTypeDef(TypedDict):
    Id: str
    IfMatch: NotRequired[str]


class DeleteCloudFrontOriginAccessIdentityRequestRequestTypeDef(TypedDict):
    Id: str
    IfMatch: NotRequired[str]


class DeleteContinuousDeploymentPolicyRequestRequestTypeDef(TypedDict):
    Id: str
    IfMatch: NotRequired[str]


class DeleteDistributionRequestRequestTypeDef(TypedDict):
    Id: str
    IfMatch: NotRequired[str]


class DeleteFieldLevelEncryptionConfigRequestRequestTypeDef(TypedDict):
    Id: str
    IfMatch: NotRequired[str]


class DeleteFieldLevelEncryptionProfileRequestRequestTypeDef(TypedDict):
    Id: str
    IfMatch: NotRequired[str]


class DeleteFunctionRequestRequestTypeDef(TypedDict):
    Name: str
    IfMatch: str


class DeleteKeyGroupRequestRequestTypeDef(TypedDict):
    Id: str
    IfMatch: NotRequired[str]


class DeleteKeyValueStoreRequestRequestTypeDef(TypedDict):
    Name: str
    IfMatch: str


class DeleteMonitoringSubscriptionRequestRequestTypeDef(TypedDict):
    DistributionId: str


class DeleteOriginAccessControlRequestRequestTypeDef(TypedDict):
    Id: str
    IfMatch: NotRequired[str]


class DeleteOriginRequestPolicyRequestRequestTypeDef(TypedDict):
    Id: str
    IfMatch: NotRequired[str]


class DeletePublicKeyRequestRequestTypeDef(TypedDict):
    Id: str
    IfMatch: NotRequired[str]


class DeleteRealtimeLogConfigRequestRequestTypeDef(TypedDict):
    Name: NotRequired[str]
    ARN: NotRequired[str]


class DeleteResponseHeadersPolicyRequestRequestTypeDef(TypedDict):
    Id: str
    IfMatch: NotRequired[str]


class DeleteStreamingDistributionRequestRequestTypeDef(TypedDict):
    Id: str
    IfMatch: NotRequired[str]


class DeleteVpcOriginRequestRequestTypeDef(TypedDict):
    Id: str
    IfMatch: str


class DescribeFunctionRequestRequestTypeDef(TypedDict):
    Name: str
    Stage: NotRequired[FunctionStageType]


class DescribeKeyValueStoreRequestRequestTypeDef(TypedDict):
    Name: str


class LoggingConfigTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    IncludeCookies: NotRequired[bool]
    Bucket: NotRequired[str]
    Prefix: NotRequired[str]


class ViewerCertificateTypeDef(TypedDict):
    CloudFrontDefaultCertificate: NotRequired[bool]
    IAMCertificateId: NotRequired[str]
    ACMCertificateArn: NotRequired[str]
    SSLSupportMethod: NotRequired[SSLSupportMethodType]
    MinimumProtocolVersion: NotRequired[MinimumProtocolVersionType]
    Certificate: NotRequired[str]
    CertificateSource: NotRequired[CertificateSourceType]


class DistributionIdListTypeDef(TypedDict):
    Marker: str
    MaxItems: int
    IsTruncated: bool
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[str]]


class FieldPatternsOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[str]]


class KinesisStreamConfigTypeDef(TypedDict):
    RoleARN: str
    StreamARN: str


class FieldPatternsTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[str]]


class QueryStringCacheKeysOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[str]]


class FunctionAssociationTypeDef(TypedDict):
    FunctionARN: str
    EventType: EventTypeType


class FunctionMetadataTypeDef(TypedDict):
    FunctionARN: str
    LastModifiedTime: datetime
    Stage: NotRequired[FunctionStageType]
    CreatedTime: NotRequired[datetime]


class GeoRestrictionOutputTypeDef(TypedDict):
    RestrictionType: GeoRestrictionTypeType
    Quantity: int
    Items: NotRequired[List[str]]


class GeoRestrictionTypeDef(TypedDict):
    RestrictionType: GeoRestrictionTypeType
    Quantity: int
    Items: NotRequired[Sequence[str]]


class GetAnycastIpListRequestRequestTypeDef(TypedDict):
    Id: str


class GetCachePolicyConfigRequestRequestTypeDef(TypedDict):
    Id: str


class GetCachePolicyRequestRequestTypeDef(TypedDict):
    Id: str


class GetCloudFrontOriginAccessIdentityConfigRequestRequestTypeDef(TypedDict):
    Id: str


class GetCloudFrontOriginAccessIdentityRequestRequestTypeDef(TypedDict):
    Id: str


class GetContinuousDeploymentPolicyConfigRequestRequestTypeDef(TypedDict):
    Id: str


class GetContinuousDeploymentPolicyRequestRequestTypeDef(TypedDict):
    Id: str


class GetDistributionConfigRequestRequestTypeDef(TypedDict):
    Id: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class GetDistributionRequestRequestTypeDef(TypedDict):
    Id: str


class GetFieldLevelEncryptionConfigRequestRequestTypeDef(TypedDict):
    Id: str


class GetFieldLevelEncryptionProfileConfigRequestRequestTypeDef(TypedDict):
    Id: str


class GetFieldLevelEncryptionProfileRequestRequestTypeDef(TypedDict):
    Id: str


class GetFieldLevelEncryptionRequestRequestTypeDef(TypedDict):
    Id: str


class GetFunctionRequestRequestTypeDef(TypedDict):
    Name: str
    Stage: NotRequired[FunctionStageType]


class GetInvalidationRequestRequestTypeDef(TypedDict):
    DistributionId: str
    Id: str


class GetKeyGroupConfigRequestRequestTypeDef(TypedDict):
    Id: str


class KeyGroupConfigOutputTypeDef(TypedDict):
    Name: str
    Items: List[str]
    Comment: NotRequired[str]


class GetKeyGroupRequestRequestTypeDef(TypedDict):
    Id: str


class GetMonitoringSubscriptionRequestRequestTypeDef(TypedDict):
    DistributionId: str


class GetOriginAccessControlConfigRequestRequestTypeDef(TypedDict):
    Id: str


class GetOriginAccessControlRequestRequestTypeDef(TypedDict):
    Id: str


class GetOriginRequestPolicyConfigRequestRequestTypeDef(TypedDict):
    Id: str


class GetOriginRequestPolicyRequestRequestTypeDef(TypedDict):
    Id: str


class GetPublicKeyConfigRequestRequestTypeDef(TypedDict):
    Id: str


class GetPublicKeyRequestRequestTypeDef(TypedDict):
    Id: str


class GetRealtimeLogConfigRequestRequestTypeDef(TypedDict):
    Name: NotRequired[str]
    ARN: NotRequired[str]


class GetResponseHeadersPolicyConfigRequestRequestTypeDef(TypedDict):
    Id: str


class GetResponseHeadersPolicyRequestRequestTypeDef(TypedDict):
    Id: str


class GetStreamingDistributionConfigRequestRequestTypeDef(TypedDict):
    Id: str


class GetStreamingDistributionRequestRequestTypeDef(TypedDict):
    Id: str


class GetVpcOriginRequestRequestTypeDef(TypedDict):
    Id: str


class HeadersTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[str]]


class PathsOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[str]]


class InvalidationSummaryTypeDef(TypedDict):
    Id: str
    CreateTime: datetime
    Status: str


class KeyPairIdsTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[str]]


class KeyValueStoreAssociationTypeDef(TypedDict):
    KeyValueStoreARN: str


class LambdaFunctionAssociationTypeDef(TypedDict):
    LambdaFunctionARN: str
    EventType: EventTypeType
    IncludeBody: NotRequired[bool]


class ListAnycastIpListsRequestRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[int]


ListCachePoliciesRequestRequestTypeDef = TypedDict(
    "ListCachePoliciesRequestRequestTypeDef",
    {
        "Type": NotRequired[CachePolicyTypeType],
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListCloudFrontOriginAccessIdentitiesRequestRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListConflictingAliasesRequestRequestTypeDef(TypedDict):
    DistributionId: str
    Alias: str
    Marker: NotRequired[str]
    MaxItems: NotRequired[int]


class ListContinuousDeploymentPoliciesRequestRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListDistributionsByAnycastIpListIdRequestRequestTypeDef(TypedDict):
    AnycastIpListId: str
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListDistributionsByCachePolicyIdRequestRequestTypeDef(TypedDict):
    CachePolicyId: str
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListDistributionsByKeyGroupRequestRequestTypeDef(TypedDict):
    KeyGroupId: str
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListDistributionsByOriginRequestPolicyIdRequestRequestTypeDef(TypedDict):
    OriginRequestPolicyId: str
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListDistributionsByRealtimeLogConfigRequestRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]
    RealtimeLogConfigName: NotRequired[str]
    RealtimeLogConfigArn: NotRequired[str]


class ListDistributionsByResponseHeadersPolicyIdRequestRequestTypeDef(TypedDict):
    ResponseHeadersPolicyId: str
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListDistributionsByVpcOriginIdRequestRequestTypeDef(TypedDict):
    VpcOriginId: str
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListDistributionsByWebACLIdRequestRequestTypeDef(TypedDict):
    WebACLId: str
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListDistributionsRequestRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListFieldLevelEncryptionConfigsRequestRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListFieldLevelEncryptionProfilesRequestRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListFunctionsRequestRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]
    Stage: NotRequired[FunctionStageType]


class ListInvalidationsRequestRequestTypeDef(TypedDict):
    DistributionId: str
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListKeyGroupsRequestRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListKeyValueStoresRequestRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]
    Status: NotRequired[str]


class ListOriginAccessControlsRequestRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


ListOriginRequestPoliciesRequestRequestTypeDef = TypedDict(
    "ListOriginRequestPoliciesRequestRequestTypeDef",
    {
        "Type": NotRequired[OriginRequestPolicyTypeType],
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)


class ListPublicKeysRequestRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListRealtimeLogConfigsRequestRequestTypeDef(TypedDict):
    MaxItems: NotRequired[str]
    Marker: NotRequired[str]


ListResponseHeadersPoliciesRequestRequestTypeDef = TypedDict(
    "ListResponseHeadersPoliciesRequestRequestTypeDef",
    {
        "Type": NotRequired[ResponseHeadersPolicyTypeType],
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)


class ListStreamingDistributionsRequestRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    Resource: str


class ListVpcOriginsRequestRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class RealtimeMetricsSubscriptionConfigTypeDef(TypedDict):
    RealtimeMetricsSubscriptionStatus: RealtimeMetricsSubscriptionStatusType


class OriginAccessControlSummaryTypeDef(TypedDict):
    Id: str
    Description: str
    Name: str
    SigningProtocol: Literal["sigv4"]
    SigningBehavior: OriginAccessControlSigningBehaviorsType
    OriginAccessControlOriginType: OriginAccessControlOriginTypesType


class StatusCodesOutputTypeDef(TypedDict):
    Quantity: int
    Items: List[int]


class OriginGroupMemberTypeDef(TypedDict):
    OriginId: str


class OriginShieldTypeDef(TypedDict):
    Enabled: bool
    OriginShieldRegion: NotRequired[str]


class S3OriginConfigTypeDef(TypedDict):
    OriginAccessIdentity: str


class VpcOriginConfigTypeDef(TypedDict):
    VpcOriginId: str


class OriginSslProtocolsTypeDef(TypedDict):
    Quantity: int
    Items: Sequence[SslProtocolType]


class PathsTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[str]]


class PublicKeySummaryTypeDef(TypedDict):
    Id: str
    Name: str
    CreatedTime: datetime
    EncodedKey: str
    Comment: NotRequired[str]


class PublishFunctionRequestRequestTypeDef(TypedDict):
    Name: str
    IfMatch: str


class QueryArgProfileTypeDef(TypedDict):
    QueryArg: str
    ProfileId: str


class QueryStringCacheKeysTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[str]]


class QueryStringNamesTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[str]]


class ResponseHeadersPolicyAccessControlAllowHeadersOutputTypeDef(TypedDict):
    Quantity: int
    Items: List[str]


class ResponseHeadersPolicyAccessControlAllowHeadersTypeDef(TypedDict):
    Quantity: int
    Items: Sequence[str]


class ResponseHeadersPolicyAccessControlAllowMethodsOutputTypeDef(TypedDict):
    Quantity: int
    Items: List[ResponseHeadersPolicyAccessControlAllowMethodsValuesType]


class ResponseHeadersPolicyAccessControlAllowMethodsTypeDef(TypedDict):
    Quantity: int
    Items: Sequence[ResponseHeadersPolicyAccessControlAllowMethodsValuesType]


class ResponseHeadersPolicyAccessControlAllowOriginsOutputTypeDef(TypedDict):
    Quantity: int
    Items: List[str]


class ResponseHeadersPolicyAccessControlAllowOriginsTypeDef(TypedDict):
    Quantity: int
    Items: Sequence[str]


class ResponseHeadersPolicyAccessControlExposeHeadersOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[str]]


class ResponseHeadersPolicyAccessControlExposeHeadersTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[str]]


class ResponseHeadersPolicyServerTimingHeadersConfigTypeDef(TypedDict):
    Enabled: bool
    SamplingRate: NotRequired[float]


class ResponseHeadersPolicyContentSecurityPolicyTypeDef(TypedDict):
    Override: bool
    ContentSecurityPolicy: str


class ResponseHeadersPolicyContentTypeOptionsTypeDef(TypedDict):
    Override: bool


class ResponseHeadersPolicyCustomHeaderTypeDef(TypedDict):
    Header: str
    Value: str
    Override: bool


class ResponseHeadersPolicyFrameOptionsTypeDef(TypedDict):
    Override: bool
    FrameOption: FrameOptionsListType


class ResponseHeadersPolicyReferrerPolicyTypeDef(TypedDict):
    Override: bool
    ReferrerPolicy: ReferrerPolicyListType


class ResponseHeadersPolicyRemoveHeaderTypeDef(TypedDict):
    Header: str


class ResponseHeadersPolicyStrictTransportSecurityTypeDef(TypedDict):
    Override: bool
    AccessControlMaxAgeSec: int
    IncludeSubdomains: NotRequired[bool]
    Preload: NotRequired[bool]


class ResponseHeadersPolicyXSSProtectionTypeDef(TypedDict):
    Override: bool
    Protection: bool
    ModeBlock: NotRequired[bool]
    ReportUri: NotRequired[str]


class S3OriginTypeDef(TypedDict):
    DomainName: str
    OriginAccessIdentity: str


class StagingDistributionDnsNamesTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[str]]


class StatusCodesTypeDef(TypedDict):
    Quantity: int
    Items: Sequence[int]


class StreamingLoggingConfigTypeDef(TypedDict):
    Enabled: bool
    Bucket: str
    Prefix: str


class TagKeysTypeDef(TypedDict):
    Items: NotRequired[Sequence[str]]


class TagTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]


class TrustedKeyGroupsTypeDef(TypedDict):
    Enabled: bool
    Quantity: int
    Items: NotRequired[Sequence[str]]


class TrustedSignersTypeDef(TypedDict):
    Enabled: bool
    Quantity: int
    Items: NotRequired[Sequence[str]]


class UpdateDistributionWithStagingConfigRequestRequestTypeDef(TypedDict):
    Id: str
    StagingDistributionId: NotRequired[str]
    IfMatch: NotRequired[str]


class UpdateKeyValueStoreRequestRequestTypeDef(TypedDict):
    Name: str
    Comment: str
    IfMatch: str


class VpcOriginSummaryTypeDef(TypedDict):
    Id: str
    Name: str
    Status: str
    CreatedTime: datetime
    LastModifiedTime: datetime
    Arn: str
    OriginEndpointArn: str


AliasesUnionTypeDef = Union[AliasesTypeDef, AliasesOutputTypeDef]


class AllowedMethodsOutputTypeDef(TypedDict):
    Quantity: int
    Items: List[MethodType]
    CachedMethods: NotRequired[CachedMethodsOutputTypeDef]


class AnycastIpListCollectionTypeDef(TypedDict):
    Marker: str
    MaxItems: int
    IsTruncated: bool
    Quantity: int
    Items: NotRequired[List[AnycastIpListSummaryTypeDef]]
    NextMarker: NotRequired[str]


class TestFunctionRequestRequestTypeDef(TypedDict):
    Name: str
    IfMatch: str
    EventObject: BlobTypeDef
    Stage: NotRequired[FunctionStageType]


class CachePolicyCookiesConfigOutputTypeDef(TypedDict):
    CookieBehavior: CachePolicyCookieBehaviorType
    Cookies: NotRequired[CookieNamesOutputTypeDef]


class CookiePreferenceOutputTypeDef(TypedDict):
    Forward: ItemSelectionType
    WhitelistedNames: NotRequired[CookieNamesOutputTypeDef]


class OriginRequestPolicyCookiesConfigOutputTypeDef(TypedDict):
    CookieBehavior: OriginRequestPolicyCookieBehaviorType
    Cookies: NotRequired[CookieNamesOutputTypeDef]


class CachePolicyHeadersConfigOutputTypeDef(TypedDict):
    HeaderBehavior: CachePolicyHeaderBehaviorType
    Headers: NotRequired[HeadersOutputTypeDef]


class OriginRequestPolicyHeadersConfigOutputTypeDef(TypedDict):
    HeaderBehavior: OriginRequestPolicyHeaderBehaviorType
    Headers: NotRequired[HeadersOutputTypeDef]


class CachePolicyQueryStringsConfigOutputTypeDef(TypedDict):
    QueryStringBehavior: CachePolicyQueryStringBehaviorType
    QueryStrings: NotRequired[QueryStringNamesOutputTypeDef]


class OriginRequestPolicyQueryStringsConfigOutputTypeDef(TypedDict):
    QueryStringBehavior: OriginRequestPolicyQueryStringBehaviorType
    QueryStrings: NotRequired[QueryStringNamesOutputTypeDef]


CachedMethodsUnionTypeDef = Union[CachedMethodsTypeDef, CachedMethodsOutputTypeDef]


class CloudFrontOriginAccessIdentityTypeDef(TypedDict):
    Id: str
    S3CanonicalUserId: str
    CloudFrontOriginAccessIdentityConfig: NotRequired[CloudFrontOriginAccessIdentityConfigTypeDef]


class CreateCloudFrontOriginAccessIdentityRequestRequestTypeDef(TypedDict):
    CloudFrontOriginAccessIdentityConfig: CloudFrontOriginAccessIdentityConfigTypeDef


class UpdateCloudFrontOriginAccessIdentityRequestRequestTypeDef(TypedDict):
    CloudFrontOriginAccessIdentityConfig: CloudFrontOriginAccessIdentityConfigTypeDef
    Id: str
    IfMatch: NotRequired[str]


class CloudFrontOriginAccessIdentityListTypeDef(TypedDict):
    Marker: str
    MaxItems: int
    IsTruncated: bool
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[CloudFrontOriginAccessIdentitySummaryTypeDef]]


class ConflictingAliasesListTypeDef(TypedDict):
    NextMarker: NotRequired[str]
    MaxItems: NotRequired[int]
    Quantity: NotRequired[int]
    Items: NotRequired[List[ConflictingAliasTypeDef]]


class ContentTypeProfilesOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[ContentTypeProfileTypeDef]]


class ContentTypeProfilesTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[ContentTypeProfileTypeDef]]


class ContinuousDeploymentSingleWeightConfigTypeDef(TypedDict):
    Weight: float
    SessionStickinessConfig: NotRequired[SessionStickinessConfigTypeDef]


CookieNamesUnionTypeDef = Union[CookieNamesTypeDef, CookieNamesOutputTypeDef]


class CreateAnycastIpListResultTypeDef(TypedDict):
    AnycastIpList: AnycastIpListTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetAnycastIpListResultTypeDef(TypedDict):
    AnycastIpList: AnycastIpListTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetCloudFrontOriginAccessIdentityConfigResultTypeDef(TypedDict):
    CloudFrontOriginAccessIdentityConfig: CloudFrontOriginAccessIdentityConfigTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetFunctionResultTypeDef(TypedDict):
    FunctionCode: StreamingBody
    ETag: str
    ContentType: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateKeyGroupRequestRequestTypeDef(TypedDict):
    KeyGroupConfig: KeyGroupConfigTypeDef


class UpdateKeyGroupRequestRequestTypeDef(TypedDict):
    KeyGroupConfig: KeyGroupConfigTypeDef
    Id: str
    IfMatch: NotRequired[str]


class CreateKeyValueStoreRequestRequestTypeDef(TypedDict):
    Name: str
    Comment: NotRequired[str]
    ImportSource: NotRequired[ImportSourceTypeDef]


class CreateKeyValueStoreResultTypeDef(TypedDict):
    KeyValueStore: KeyValueStoreTypeDef
    ETag: str
    Location: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeKeyValueStoreResultTypeDef(TypedDict):
    KeyValueStore: KeyValueStoreTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class KeyValueStoreListTypeDef(TypedDict):
    MaxItems: int
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[KeyValueStoreTypeDef]]


class UpdateKeyValueStoreResultTypeDef(TypedDict):
    KeyValueStore: KeyValueStoreTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOriginAccessControlRequestRequestTypeDef(TypedDict):
    OriginAccessControlConfig: OriginAccessControlConfigTypeDef


class GetOriginAccessControlConfigResultTypeDef(TypedDict):
    OriginAccessControlConfig: OriginAccessControlConfigTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class OriginAccessControlTypeDef(TypedDict):
    Id: str
    OriginAccessControlConfig: NotRequired[OriginAccessControlConfigTypeDef]


class UpdateOriginAccessControlRequestRequestTypeDef(TypedDict):
    OriginAccessControlConfig: OriginAccessControlConfigTypeDef
    Id: str
    IfMatch: NotRequired[str]


class CreatePublicKeyRequestRequestTypeDef(TypedDict):
    PublicKeyConfig: PublicKeyConfigTypeDef


class GetPublicKeyConfigResultTypeDef(TypedDict):
    PublicKeyConfig: PublicKeyConfigTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class PublicKeyTypeDef(TypedDict):
    Id: str
    CreatedTime: datetime
    PublicKeyConfig: PublicKeyConfigTypeDef


class UpdatePublicKeyRequestRequestTypeDef(TypedDict):
    PublicKeyConfig: PublicKeyConfigTypeDef
    Id: str
    IfMatch: NotRequired[str]


class CustomErrorResponsesOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[CustomErrorResponseTypeDef]]


class CustomErrorResponsesTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[CustomErrorResponseTypeDef]]


class CustomHeadersOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[OriginCustomHeaderTypeDef]]


class CustomHeadersTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[OriginCustomHeaderTypeDef]]


class CustomOriginConfigOutputTypeDef(TypedDict):
    HTTPPort: int
    HTTPSPort: int
    OriginProtocolPolicy: OriginProtocolPolicyType
    OriginSslProtocols: NotRequired[OriginSslProtocolsOutputTypeDef]
    OriginReadTimeout: NotRequired[int]
    OriginKeepaliveTimeout: NotRequired[int]


class VpcOriginEndpointConfigOutputTypeDef(TypedDict):
    Name: str
    Arn: str
    HTTPPort: int
    HTTPSPort: int
    OriginProtocolPolicy: OriginProtocolPolicyType
    OriginSslProtocols: NotRequired[OriginSslProtocolsOutputTypeDef]


class ListDistributionsByCachePolicyIdResultTypeDef(TypedDict):
    DistributionIdList: DistributionIdListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDistributionsByKeyGroupResultTypeDef(TypedDict):
    DistributionIdList: DistributionIdListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDistributionsByOriginRequestPolicyIdResultTypeDef(TypedDict):
    DistributionIdList: DistributionIdListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDistributionsByResponseHeadersPolicyIdResultTypeDef(TypedDict):
    DistributionIdList: DistributionIdListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDistributionsByVpcOriginIdResultTypeDef(TypedDict):
    DistributionIdList: DistributionIdListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class EncryptionEntityOutputTypeDef(TypedDict):
    PublicKeyId: str
    ProviderId: str
    FieldPatterns: FieldPatternsOutputTypeDef


class EndPointTypeDef(TypedDict):
    StreamType: str
    KinesisStreamConfig: NotRequired[KinesisStreamConfigTypeDef]


FieldPatternsUnionTypeDef = Union[FieldPatternsTypeDef, FieldPatternsOutputTypeDef]


class FunctionAssociationsOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[FunctionAssociationTypeDef]]


class FunctionAssociationsTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[FunctionAssociationTypeDef]]


class RestrictionsOutputTypeDef(TypedDict):
    GeoRestriction: GeoRestrictionOutputTypeDef


GeoRestrictionUnionTypeDef = Union[GeoRestrictionTypeDef, GeoRestrictionOutputTypeDef]


class GetDistributionRequestDistributionDeployedWaitTypeDef(TypedDict):
    Id: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetInvalidationRequestInvalidationCompletedWaitTypeDef(TypedDict):
    DistributionId: str
    Id: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetStreamingDistributionRequestStreamingDistributionDeployedWaitTypeDef(TypedDict):
    Id: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetKeyGroupConfigResultTypeDef(TypedDict):
    KeyGroupConfig: KeyGroupConfigOutputTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class KeyGroupTypeDef(TypedDict):
    Id: str
    LastModifiedTime: datetime
    KeyGroupConfig: KeyGroupConfigOutputTypeDef


HeadersUnionTypeDef = Union[HeadersTypeDef, HeadersOutputTypeDef]


class InvalidationBatchOutputTypeDef(TypedDict):
    Paths: PathsOutputTypeDef
    CallerReference: str


class InvalidationListTypeDef(TypedDict):
    Marker: str
    MaxItems: int
    IsTruncated: bool
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[InvalidationSummaryTypeDef]]


class KGKeyPairIdsTypeDef(TypedDict):
    KeyGroupId: NotRequired[str]
    KeyPairIds: NotRequired[KeyPairIdsTypeDef]


class SignerTypeDef(TypedDict):
    AwsAccountNumber: NotRequired[str]
    KeyPairIds: NotRequired[KeyPairIdsTypeDef]


class KeyValueStoreAssociationsOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[KeyValueStoreAssociationTypeDef]]


class KeyValueStoreAssociationsTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[KeyValueStoreAssociationTypeDef]]


class LambdaFunctionAssociationsOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[LambdaFunctionAssociationTypeDef]]


class LambdaFunctionAssociationsTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[LambdaFunctionAssociationTypeDef]]


class ListCloudFrontOriginAccessIdentitiesRequestListCloudFrontOriginAccessIdentitiesPaginateTypeDef(
    TypedDict
):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDistributionsRequestListDistributionsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListInvalidationsRequestListInvalidationsPaginateTypeDef(TypedDict):
    DistributionId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListKeyValueStoresRequestListKeyValueStoresPaginateTypeDef(TypedDict):
    Status: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPublicKeysRequestListPublicKeysPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStreamingDistributionsRequestListStreamingDistributionsPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class MonitoringSubscriptionTypeDef(TypedDict):
    RealtimeMetricsSubscriptionConfig: NotRequired[RealtimeMetricsSubscriptionConfigTypeDef]


class OriginAccessControlListTypeDef(TypedDict):
    Marker: str
    MaxItems: int
    IsTruncated: bool
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[OriginAccessControlSummaryTypeDef]]


class OriginGroupFailoverCriteriaOutputTypeDef(TypedDict):
    StatusCodes: StatusCodesOutputTypeDef


class OriginGroupMembersOutputTypeDef(TypedDict):
    Quantity: int
    Items: List[OriginGroupMemberTypeDef]


class OriginGroupMembersTypeDef(TypedDict):
    Quantity: int
    Items: Sequence[OriginGroupMemberTypeDef]


OriginSslProtocolsUnionTypeDef = Union[OriginSslProtocolsTypeDef, OriginSslProtocolsOutputTypeDef]
PathsUnionTypeDef = Union[PathsTypeDef, PathsOutputTypeDef]


class PublicKeyListTypeDef(TypedDict):
    MaxItems: int
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[PublicKeySummaryTypeDef]]


class QueryArgProfilesOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[QueryArgProfileTypeDef]]


class QueryArgProfilesTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[QueryArgProfileTypeDef]]


QueryStringCacheKeysUnionTypeDef = Union[
    QueryStringCacheKeysTypeDef, QueryStringCacheKeysOutputTypeDef
]
QueryStringNamesUnionTypeDef = Union[QueryStringNamesTypeDef, QueryStringNamesOutputTypeDef]
ResponseHeadersPolicyAccessControlAllowHeadersUnionTypeDef = Union[
    ResponseHeadersPolicyAccessControlAllowHeadersTypeDef,
    ResponseHeadersPolicyAccessControlAllowHeadersOutputTypeDef,
]
ResponseHeadersPolicyAccessControlAllowMethodsUnionTypeDef = Union[
    ResponseHeadersPolicyAccessControlAllowMethodsTypeDef,
    ResponseHeadersPolicyAccessControlAllowMethodsOutputTypeDef,
]
ResponseHeadersPolicyAccessControlAllowOriginsUnionTypeDef = Union[
    ResponseHeadersPolicyAccessControlAllowOriginsTypeDef,
    ResponseHeadersPolicyAccessControlAllowOriginsOutputTypeDef,
]


class ResponseHeadersPolicyCorsConfigOutputTypeDef(TypedDict):
    AccessControlAllowOrigins: ResponseHeadersPolicyAccessControlAllowOriginsOutputTypeDef
    AccessControlAllowHeaders: ResponseHeadersPolicyAccessControlAllowHeadersOutputTypeDef
    AccessControlAllowMethods: ResponseHeadersPolicyAccessControlAllowMethodsOutputTypeDef
    AccessControlAllowCredentials: bool
    OriginOverride: bool
    AccessControlExposeHeaders: NotRequired[
        ResponseHeadersPolicyAccessControlExposeHeadersOutputTypeDef
    ]
    AccessControlMaxAgeSec: NotRequired[int]


ResponseHeadersPolicyAccessControlExposeHeadersUnionTypeDef = Union[
    ResponseHeadersPolicyAccessControlExposeHeadersTypeDef,
    ResponseHeadersPolicyAccessControlExposeHeadersOutputTypeDef,
]


class ResponseHeadersPolicyCustomHeadersConfigOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[ResponseHeadersPolicyCustomHeaderTypeDef]]


class ResponseHeadersPolicyCustomHeadersConfigTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[ResponseHeadersPolicyCustomHeaderTypeDef]]


class ResponseHeadersPolicyRemoveHeadersConfigOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[ResponseHeadersPolicyRemoveHeaderTypeDef]]


class ResponseHeadersPolicyRemoveHeadersConfigTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[ResponseHeadersPolicyRemoveHeaderTypeDef]]


class ResponseHeadersPolicySecurityHeadersConfigTypeDef(TypedDict):
    XSSProtection: NotRequired[ResponseHeadersPolicyXSSProtectionTypeDef]
    FrameOptions: NotRequired[ResponseHeadersPolicyFrameOptionsTypeDef]
    ReferrerPolicy: NotRequired[ResponseHeadersPolicyReferrerPolicyTypeDef]
    ContentSecurityPolicy: NotRequired[ResponseHeadersPolicyContentSecurityPolicyTypeDef]
    ContentTypeOptions: NotRequired[ResponseHeadersPolicyContentTypeOptionsTypeDef]
    StrictTransportSecurity: NotRequired[ResponseHeadersPolicyStrictTransportSecurityTypeDef]


class StreamingDistributionSummaryTypeDef(TypedDict):
    Id: str
    ARN: str
    Status: str
    LastModifiedTime: datetime
    DomainName: str
    S3Origin: S3OriginTypeDef
    Aliases: AliasesOutputTypeDef
    TrustedSigners: TrustedSignersOutputTypeDef
    Comment: str
    PriceClass: PriceClassType
    Enabled: bool


StagingDistributionDnsNamesUnionTypeDef = Union[
    StagingDistributionDnsNamesTypeDef, StagingDistributionDnsNamesOutputTypeDef
]
StatusCodesUnionTypeDef = Union[StatusCodesTypeDef, StatusCodesOutputTypeDef]


class StreamingDistributionConfigOutputTypeDef(TypedDict):
    CallerReference: str
    S3Origin: S3OriginTypeDef
    Comment: str
    TrustedSigners: TrustedSignersOutputTypeDef
    Enabled: bool
    Aliases: NotRequired[AliasesOutputTypeDef]
    Logging: NotRequired[StreamingLoggingConfigTypeDef]
    PriceClass: NotRequired[PriceClassType]


class UntagResourceRequestRequestTypeDef(TypedDict):
    Resource: str
    TagKeys: TagKeysTypeDef


class TagsOutputTypeDef(TypedDict):
    Items: NotRequired[List[TagTypeDef]]


class TagsTypeDef(TypedDict):
    Items: NotRequired[Sequence[TagTypeDef]]


TrustedKeyGroupsUnionTypeDef = Union[TrustedKeyGroupsTypeDef, TrustedKeyGroupsOutputTypeDef]
TrustedSignersUnionTypeDef = Union[TrustedSignersTypeDef, TrustedSignersOutputTypeDef]


class VpcOriginListTypeDef(TypedDict):
    Marker: str
    MaxItems: int
    IsTruncated: bool
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[VpcOriginSummaryTypeDef]]


class ListAnycastIpListsResultTypeDef(TypedDict):
    AnycastIpLists: AnycastIpListCollectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ForwardedValuesOutputTypeDef(TypedDict):
    QueryString: bool
    Cookies: CookiePreferenceOutputTypeDef
    Headers: NotRequired[HeadersOutputTypeDef]
    QueryStringCacheKeys: NotRequired[QueryStringCacheKeysOutputTypeDef]


class ParametersInCacheKeyAndForwardedToOriginOutputTypeDef(TypedDict):
    EnableAcceptEncodingGzip: bool
    HeadersConfig: CachePolicyHeadersConfigOutputTypeDef
    CookiesConfig: CachePolicyCookiesConfigOutputTypeDef
    QueryStringsConfig: CachePolicyQueryStringsConfigOutputTypeDef
    EnableAcceptEncodingBrotli: NotRequired[bool]


class OriginRequestPolicyConfigOutputTypeDef(TypedDict):
    Name: str
    HeadersConfig: OriginRequestPolicyHeadersConfigOutputTypeDef
    CookiesConfig: OriginRequestPolicyCookiesConfigOutputTypeDef
    QueryStringsConfig: OriginRequestPolicyQueryStringsConfigOutputTypeDef
    Comment: NotRequired[str]


class AllowedMethodsTypeDef(TypedDict):
    Quantity: int
    Items: Sequence[MethodType]
    CachedMethods: NotRequired[CachedMethodsUnionTypeDef]


class CreateCloudFrontOriginAccessIdentityResultTypeDef(TypedDict):
    CloudFrontOriginAccessIdentity: CloudFrontOriginAccessIdentityTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetCloudFrontOriginAccessIdentityResultTypeDef(TypedDict):
    CloudFrontOriginAccessIdentity: CloudFrontOriginAccessIdentityTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCloudFrontOriginAccessIdentityResultTypeDef(TypedDict):
    CloudFrontOriginAccessIdentity: CloudFrontOriginAccessIdentityTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListCloudFrontOriginAccessIdentitiesResultTypeDef(TypedDict):
    CloudFrontOriginAccessIdentityList: CloudFrontOriginAccessIdentityListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListConflictingAliasesResultTypeDef(TypedDict):
    ConflictingAliasesList: ConflictingAliasesListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ContentTypeProfileConfigOutputTypeDef(TypedDict):
    ForwardWhenContentTypeIsUnknown: bool
    ContentTypeProfiles: NotRequired[ContentTypeProfilesOutputTypeDef]


ContentTypeProfilesUnionTypeDef = Union[
    ContentTypeProfilesTypeDef, ContentTypeProfilesOutputTypeDef
]
TrafficConfigTypeDef = TypedDict(
    "TrafficConfigTypeDef",
    {
        "Type": ContinuousDeploymentPolicyTypeType,
        "SingleWeightConfig": NotRequired[ContinuousDeploymentSingleWeightConfigTypeDef],
        "SingleHeaderConfig": NotRequired[ContinuousDeploymentSingleHeaderConfigTypeDef],
    },
)


class CachePolicyCookiesConfigTypeDef(TypedDict):
    CookieBehavior: CachePolicyCookieBehaviorType
    Cookies: NotRequired[CookieNamesUnionTypeDef]


class CookiePreferenceTypeDef(TypedDict):
    Forward: ItemSelectionType
    WhitelistedNames: NotRequired[CookieNamesUnionTypeDef]


class OriginRequestPolicyCookiesConfigTypeDef(TypedDict):
    CookieBehavior: OriginRequestPolicyCookieBehaviorType
    Cookies: NotRequired[CookieNamesUnionTypeDef]


class ListKeyValueStoresResultTypeDef(TypedDict):
    KeyValueStoreList: KeyValueStoreListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOriginAccessControlResultTypeDef(TypedDict):
    OriginAccessControl: OriginAccessControlTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetOriginAccessControlResultTypeDef(TypedDict):
    OriginAccessControl: OriginAccessControlTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateOriginAccessControlResultTypeDef(TypedDict):
    OriginAccessControl: OriginAccessControlTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePublicKeyResultTypeDef(TypedDict):
    PublicKey: PublicKeyTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetPublicKeyResultTypeDef(TypedDict):
    PublicKey: PublicKeyTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePublicKeyResultTypeDef(TypedDict):
    PublicKey: PublicKeyTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


CustomErrorResponsesUnionTypeDef = Union[
    CustomErrorResponsesTypeDef, CustomErrorResponsesOutputTypeDef
]
CustomHeadersUnionTypeDef = Union[CustomHeadersTypeDef, CustomHeadersOutputTypeDef]


class OriginOutputTypeDef(TypedDict):
    Id: str
    DomainName: str
    OriginPath: NotRequired[str]
    CustomHeaders: NotRequired[CustomHeadersOutputTypeDef]
    S3OriginConfig: NotRequired[S3OriginConfigTypeDef]
    CustomOriginConfig: NotRequired[CustomOriginConfigOutputTypeDef]
    VpcOriginConfig: NotRequired[VpcOriginConfigTypeDef]
    ConnectionAttempts: NotRequired[int]
    ConnectionTimeout: NotRequired[int]
    OriginShield: NotRequired[OriginShieldTypeDef]
    OriginAccessControlId: NotRequired[str]


class VpcOriginTypeDef(TypedDict):
    Id: str
    Arn: str
    Status: str
    CreatedTime: datetime
    LastModifiedTime: datetime
    VpcOriginEndpointConfig: VpcOriginEndpointConfigOutputTypeDef


class EncryptionEntitiesOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[EncryptionEntityOutputTypeDef]]


class CreateRealtimeLogConfigRequestRequestTypeDef(TypedDict):
    EndPoints: Sequence[EndPointTypeDef]
    Fields: Sequence[str]
    Name: str
    SamplingRate: int


class RealtimeLogConfigTypeDef(TypedDict):
    ARN: str
    Name: str
    SamplingRate: int
    EndPoints: List[EndPointTypeDef]
    Fields: List[str]


class UpdateRealtimeLogConfigRequestRequestTypeDef(TypedDict):
    EndPoints: NotRequired[Sequence[EndPointTypeDef]]
    Fields: NotRequired[Sequence[str]]
    Name: NotRequired[str]
    ARN: NotRequired[str]
    SamplingRate: NotRequired[int]


class EncryptionEntityTypeDef(TypedDict):
    PublicKeyId: str
    ProviderId: str
    FieldPatterns: FieldPatternsUnionTypeDef


FunctionAssociationsUnionTypeDef = Union[
    FunctionAssociationsTypeDef, FunctionAssociationsOutputTypeDef
]


class RestrictionsTypeDef(TypedDict):
    GeoRestriction: GeoRestrictionUnionTypeDef


class CreateKeyGroupResultTypeDef(TypedDict):
    KeyGroup: KeyGroupTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetKeyGroupResultTypeDef(TypedDict):
    KeyGroup: KeyGroupTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class KeyGroupSummaryTypeDef(TypedDict):
    KeyGroup: KeyGroupTypeDef


class UpdateKeyGroupResultTypeDef(TypedDict):
    KeyGroup: KeyGroupTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class CachePolicyHeadersConfigTypeDef(TypedDict):
    HeaderBehavior: CachePolicyHeaderBehaviorType
    Headers: NotRequired[HeadersUnionTypeDef]


class OriginRequestPolicyHeadersConfigTypeDef(TypedDict):
    HeaderBehavior: OriginRequestPolicyHeaderBehaviorType
    Headers: NotRequired[HeadersUnionTypeDef]


class InvalidationTypeDef(TypedDict):
    Id: str
    Status: str
    CreateTime: datetime
    InvalidationBatch: InvalidationBatchOutputTypeDef


class ListInvalidationsResultTypeDef(TypedDict):
    InvalidationList: InvalidationListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ActiveTrustedKeyGroupsTypeDef(TypedDict):
    Enabled: bool
    Quantity: int
    Items: NotRequired[List[KGKeyPairIdsTypeDef]]


class ActiveTrustedSignersTypeDef(TypedDict):
    Enabled: bool
    Quantity: int
    Items: NotRequired[List[SignerTypeDef]]


class FunctionConfigOutputTypeDef(TypedDict):
    Comment: str
    Runtime: FunctionRuntimeType
    KeyValueStoreAssociations: NotRequired[KeyValueStoreAssociationsOutputTypeDef]


KeyValueStoreAssociationsUnionTypeDef = Union[
    KeyValueStoreAssociationsTypeDef, KeyValueStoreAssociationsOutputTypeDef
]
LambdaFunctionAssociationsUnionTypeDef = Union[
    LambdaFunctionAssociationsTypeDef, LambdaFunctionAssociationsOutputTypeDef
]


class CreateMonitoringSubscriptionRequestRequestTypeDef(TypedDict):
    DistributionId: str
    MonitoringSubscription: MonitoringSubscriptionTypeDef


class CreateMonitoringSubscriptionResultTypeDef(TypedDict):
    MonitoringSubscription: MonitoringSubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetMonitoringSubscriptionResultTypeDef(TypedDict):
    MonitoringSubscription: MonitoringSubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListOriginAccessControlsResultTypeDef(TypedDict):
    OriginAccessControlList: OriginAccessControlListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class OriginGroupOutputTypeDef(TypedDict):
    Id: str
    FailoverCriteria: OriginGroupFailoverCriteriaOutputTypeDef
    Members: OriginGroupMembersOutputTypeDef
    SelectionCriteria: NotRequired[OriginGroupSelectionCriteriaType]


OriginGroupMembersUnionTypeDef = Union[OriginGroupMembersTypeDef, OriginGroupMembersOutputTypeDef]


class CustomOriginConfigTypeDef(TypedDict):
    HTTPPort: int
    HTTPSPort: int
    OriginProtocolPolicy: OriginProtocolPolicyType
    OriginSslProtocols: NotRequired[OriginSslProtocolsUnionTypeDef]
    OriginReadTimeout: NotRequired[int]
    OriginKeepaliveTimeout: NotRequired[int]


class VpcOriginEndpointConfigTypeDef(TypedDict):
    Name: str
    Arn: str
    HTTPPort: int
    HTTPSPort: int
    OriginProtocolPolicy: OriginProtocolPolicyType
    OriginSslProtocols: NotRequired[OriginSslProtocolsUnionTypeDef]


class InvalidationBatchTypeDef(TypedDict):
    Paths: PathsUnionTypeDef
    CallerReference: str


class ListPublicKeysResultTypeDef(TypedDict):
    PublicKeyList: PublicKeyListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class QueryArgProfileConfigOutputTypeDef(TypedDict):
    ForwardWhenQueryArgProfileIsUnknown: bool
    QueryArgProfiles: NotRequired[QueryArgProfilesOutputTypeDef]


QueryArgProfilesUnionTypeDef = Union[QueryArgProfilesTypeDef, QueryArgProfilesOutputTypeDef]


class CachePolicyQueryStringsConfigTypeDef(TypedDict):
    QueryStringBehavior: CachePolicyQueryStringBehaviorType
    QueryStrings: NotRequired[QueryStringNamesUnionTypeDef]


class OriginRequestPolicyQueryStringsConfigTypeDef(TypedDict):
    QueryStringBehavior: OriginRequestPolicyQueryStringBehaviorType
    QueryStrings: NotRequired[QueryStringNamesUnionTypeDef]


class ResponseHeadersPolicyCorsConfigTypeDef(TypedDict):
    AccessControlAllowOrigins: ResponseHeadersPolicyAccessControlAllowOriginsUnionTypeDef
    AccessControlAllowHeaders: ResponseHeadersPolicyAccessControlAllowHeadersUnionTypeDef
    AccessControlAllowMethods: ResponseHeadersPolicyAccessControlAllowMethodsUnionTypeDef
    AccessControlAllowCredentials: bool
    OriginOverride: bool
    AccessControlExposeHeaders: NotRequired[
        ResponseHeadersPolicyAccessControlExposeHeadersUnionTypeDef
    ]
    AccessControlMaxAgeSec: NotRequired[int]


ResponseHeadersPolicyCustomHeadersConfigUnionTypeDef = Union[
    ResponseHeadersPolicyCustomHeadersConfigTypeDef,
    ResponseHeadersPolicyCustomHeadersConfigOutputTypeDef,
]
ResponseHeadersPolicyRemoveHeadersConfigUnionTypeDef = Union[
    ResponseHeadersPolicyRemoveHeadersConfigTypeDef,
    ResponseHeadersPolicyRemoveHeadersConfigOutputTypeDef,
]


class ResponseHeadersPolicyConfigOutputTypeDef(TypedDict):
    Name: str
    Comment: NotRequired[str]
    CorsConfig: NotRequired[ResponseHeadersPolicyCorsConfigOutputTypeDef]
    SecurityHeadersConfig: NotRequired[ResponseHeadersPolicySecurityHeadersConfigTypeDef]
    ServerTimingHeadersConfig: NotRequired[ResponseHeadersPolicyServerTimingHeadersConfigTypeDef]
    CustomHeadersConfig: NotRequired[ResponseHeadersPolicyCustomHeadersConfigOutputTypeDef]
    RemoveHeadersConfig: NotRequired[ResponseHeadersPolicyRemoveHeadersConfigOutputTypeDef]


class StreamingDistributionListTypeDef(TypedDict):
    Marker: str
    MaxItems: int
    IsTruncated: bool
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[StreamingDistributionSummaryTypeDef]]


class OriginGroupFailoverCriteriaTypeDef(TypedDict):
    StatusCodes: StatusCodesUnionTypeDef


class GetStreamingDistributionConfigResultTypeDef(TypedDict):
    StreamingDistributionConfig: StreamingDistributionConfigOutputTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResultTypeDef(TypedDict):
    Tags: TagsOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAnycastIpListRequestRequestTypeDef(TypedDict):
    Name: str
    IpCount: int
    Tags: NotRequired[TagsTypeDef]


class TagResourceRequestRequestTypeDef(TypedDict):
    Resource: str
    Tags: TagsTypeDef


TagsUnionTypeDef = Union[TagsTypeDef, TagsOutputTypeDef]


class StreamingDistributionConfigTypeDef(TypedDict):
    CallerReference: str
    S3Origin: S3OriginTypeDef
    Comment: str
    TrustedSigners: TrustedSignersUnionTypeDef
    Enabled: bool
    Aliases: NotRequired[AliasesUnionTypeDef]
    Logging: NotRequired[StreamingLoggingConfigTypeDef]
    PriceClass: NotRequired[PriceClassType]


class ListVpcOriginsResultTypeDef(TypedDict):
    VpcOriginList: VpcOriginListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CacheBehaviorOutputTypeDef(TypedDict):
    PathPattern: str
    TargetOriginId: str
    ViewerProtocolPolicy: ViewerProtocolPolicyType
    TrustedSigners: NotRequired[TrustedSignersOutputTypeDef]
    TrustedKeyGroups: NotRequired[TrustedKeyGroupsOutputTypeDef]
    AllowedMethods: NotRequired[AllowedMethodsOutputTypeDef]
    SmoothStreaming: NotRequired[bool]
    Compress: NotRequired[bool]
    LambdaFunctionAssociations: NotRequired[LambdaFunctionAssociationsOutputTypeDef]
    FunctionAssociations: NotRequired[FunctionAssociationsOutputTypeDef]
    FieldLevelEncryptionId: NotRequired[str]
    RealtimeLogConfigArn: NotRequired[str]
    CachePolicyId: NotRequired[str]
    OriginRequestPolicyId: NotRequired[str]
    ResponseHeadersPolicyId: NotRequired[str]
    GrpcConfig: NotRequired[GrpcConfigTypeDef]
    ForwardedValues: NotRequired[ForwardedValuesOutputTypeDef]
    MinTTL: NotRequired[int]
    DefaultTTL: NotRequired[int]
    MaxTTL: NotRequired[int]


class DefaultCacheBehaviorOutputTypeDef(TypedDict):
    TargetOriginId: str
    ViewerProtocolPolicy: ViewerProtocolPolicyType
    TrustedSigners: NotRequired[TrustedSignersOutputTypeDef]
    TrustedKeyGroups: NotRequired[TrustedKeyGroupsOutputTypeDef]
    AllowedMethods: NotRequired[AllowedMethodsOutputTypeDef]
    SmoothStreaming: NotRequired[bool]
    Compress: NotRequired[bool]
    LambdaFunctionAssociations: NotRequired[LambdaFunctionAssociationsOutputTypeDef]
    FunctionAssociations: NotRequired[FunctionAssociationsOutputTypeDef]
    FieldLevelEncryptionId: NotRequired[str]
    RealtimeLogConfigArn: NotRequired[str]
    CachePolicyId: NotRequired[str]
    OriginRequestPolicyId: NotRequired[str]
    ResponseHeadersPolicyId: NotRequired[str]
    GrpcConfig: NotRequired[GrpcConfigTypeDef]
    ForwardedValues: NotRequired[ForwardedValuesOutputTypeDef]
    MinTTL: NotRequired[int]
    DefaultTTL: NotRequired[int]
    MaxTTL: NotRequired[int]


class CachePolicyConfigOutputTypeDef(TypedDict):
    Name: str
    MinTTL: int
    Comment: NotRequired[str]
    DefaultTTL: NotRequired[int]
    MaxTTL: NotRequired[int]
    ParametersInCacheKeyAndForwardedToOrigin: NotRequired[
        ParametersInCacheKeyAndForwardedToOriginOutputTypeDef
    ]


class GetOriginRequestPolicyConfigResultTypeDef(TypedDict):
    OriginRequestPolicyConfig: OriginRequestPolicyConfigOutputTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class OriginRequestPolicyTypeDef(TypedDict):
    Id: str
    LastModifiedTime: datetime
    OriginRequestPolicyConfig: OriginRequestPolicyConfigOutputTypeDef


AllowedMethodsUnionTypeDef = Union[AllowedMethodsTypeDef, AllowedMethodsOutputTypeDef]


class ContentTypeProfileConfigTypeDef(TypedDict):
    ForwardWhenContentTypeIsUnknown: bool
    ContentTypeProfiles: NotRequired[ContentTypeProfilesUnionTypeDef]


class ContinuousDeploymentPolicyConfigOutputTypeDef(TypedDict):
    StagingDistributionDnsNames: StagingDistributionDnsNamesOutputTypeDef
    Enabled: bool
    TrafficConfig: NotRequired[TrafficConfigTypeDef]


class ContinuousDeploymentPolicyConfigTypeDef(TypedDict):
    StagingDistributionDnsNames: StagingDistributionDnsNamesUnionTypeDef
    Enabled: bool
    TrafficConfig: NotRequired[TrafficConfigTypeDef]


CachePolicyCookiesConfigUnionTypeDef = Union[
    CachePolicyCookiesConfigTypeDef, CachePolicyCookiesConfigOutputTypeDef
]
CookiePreferenceUnionTypeDef = Union[CookiePreferenceTypeDef, CookiePreferenceOutputTypeDef]
OriginRequestPolicyCookiesConfigUnionTypeDef = Union[
    OriginRequestPolicyCookiesConfigTypeDef, OriginRequestPolicyCookiesConfigOutputTypeDef
]


class OriginsOutputTypeDef(TypedDict):
    Quantity: int
    Items: List[OriginOutputTypeDef]


class CreateVpcOriginResultTypeDef(TypedDict):
    VpcOrigin: VpcOriginTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVpcOriginResultTypeDef(TypedDict):
    VpcOrigin: VpcOriginTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetVpcOriginResultTypeDef(TypedDict):
    VpcOrigin: VpcOriginTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateVpcOriginResultTypeDef(TypedDict):
    VpcOrigin: VpcOriginTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class FieldLevelEncryptionProfileConfigOutputTypeDef(TypedDict):
    Name: str
    CallerReference: str
    EncryptionEntities: EncryptionEntitiesOutputTypeDef
    Comment: NotRequired[str]


class FieldLevelEncryptionProfileSummaryTypeDef(TypedDict):
    Id: str
    LastModifiedTime: datetime
    Name: str
    EncryptionEntities: EncryptionEntitiesOutputTypeDef
    Comment: NotRequired[str]


class CreateRealtimeLogConfigResultTypeDef(TypedDict):
    RealtimeLogConfig: RealtimeLogConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetRealtimeLogConfigResultTypeDef(TypedDict):
    RealtimeLogConfig: RealtimeLogConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RealtimeLogConfigsTypeDef(TypedDict):
    MaxItems: int
    IsTruncated: bool
    Marker: str
    Items: NotRequired[List[RealtimeLogConfigTypeDef]]
    NextMarker: NotRequired[str]


class UpdateRealtimeLogConfigResultTypeDef(TypedDict):
    RealtimeLogConfig: RealtimeLogConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


EncryptionEntityUnionTypeDef = Union[EncryptionEntityTypeDef, EncryptionEntityOutputTypeDef]
RestrictionsUnionTypeDef = Union[RestrictionsTypeDef, RestrictionsOutputTypeDef]


class KeyGroupListTypeDef(TypedDict):
    MaxItems: int
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[KeyGroupSummaryTypeDef]]


CachePolicyHeadersConfigUnionTypeDef = Union[
    CachePolicyHeadersConfigTypeDef, CachePolicyHeadersConfigOutputTypeDef
]
OriginRequestPolicyHeadersConfigUnionTypeDef = Union[
    OriginRequestPolicyHeadersConfigTypeDef, OriginRequestPolicyHeadersConfigOutputTypeDef
]


class CreateInvalidationResultTypeDef(TypedDict):
    Location: str
    Invalidation: InvalidationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetInvalidationResultTypeDef(TypedDict):
    Invalidation: InvalidationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StreamingDistributionTypeDef(TypedDict):
    Id: str
    ARN: str
    Status: str
    DomainName: str
    ActiveTrustedSigners: ActiveTrustedSignersTypeDef
    StreamingDistributionConfig: StreamingDistributionConfigOutputTypeDef
    LastModifiedTime: NotRequired[datetime]


class FunctionSummaryTypeDef(TypedDict):
    Name: str
    FunctionConfig: FunctionConfigOutputTypeDef
    FunctionMetadata: FunctionMetadataTypeDef
    Status: NotRequired[str]


class FunctionConfigTypeDef(TypedDict):
    Comment: str
    Runtime: FunctionRuntimeType
    KeyValueStoreAssociations: NotRequired[KeyValueStoreAssociationsUnionTypeDef]


class OriginGroupsOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[OriginGroupOutputTypeDef]]


CustomOriginConfigUnionTypeDef = Union[CustomOriginConfigTypeDef, CustomOriginConfigOutputTypeDef]


class CreateVpcOriginRequestRequestTypeDef(TypedDict):
    VpcOriginEndpointConfig: VpcOriginEndpointConfigTypeDef
    Tags: NotRequired[TagsTypeDef]


class UpdateVpcOriginRequestRequestTypeDef(TypedDict):
    VpcOriginEndpointConfig: VpcOriginEndpointConfigTypeDef
    Id: str
    IfMatch: str


class CreateInvalidationRequestRequestTypeDef(TypedDict):
    DistributionId: str
    InvalidationBatch: InvalidationBatchTypeDef


class FieldLevelEncryptionConfigOutputTypeDef(TypedDict):
    CallerReference: str
    Comment: NotRequired[str]
    QueryArgProfileConfig: NotRequired[QueryArgProfileConfigOutputTypeDef]
    ContentTypeProfileConfig: NotRequired[ContentTypeProfileConfigOutputTypeDef]


class FieldLevelEncryptionSummaryTypeDef(TypedDict):
    Id: str
    LastModifiedTime: datetime
    Comment: NotRequired[str]
    QueryArgProfileConfig: NotRequired[QueryArgProfileConfigOutputTypeDef]
    ContentTypeProfileConfig: NotRequired[ContentTypeProfileConfigOutputTypeDef]


class QueryArgProfileConfigTypeDef(TypedDict):
    ForwardWhenQueryArgProfileIsUnknown: bool
    QueryArgProfiles: NotRequired[QueryArgProfilesUnionTypeDef]


CachePolicyQueryStringsConfigUnionTypeDef = Union[
    CachePolicyQueryStringsConfigTypeDef, CachePolicyQueryStringsConfigOutputTypeDef
]
OriginRequestPolicyQueryStringsConfigUnionTypeDef = Union[
    OriginRequestPolicyQueryStringsConfigTypeDef, OriginRequestPolicyQueryStringsConfigOutputTypeDef
]
ResponseHeadersPolicyCorsConfigUnionTypeDef = Union[
    ResponseHeadersPolicyCorsConfigTypeDef, ResponseHeadersPolicyCorsConfigOutputTypeDef
]


class GetResponseHeadersPolicyConfigResultTypeDef(TypedDict):
    ResponseHeadersPolicyConfig: ResponseHeadersPolicyConfigOutputTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class ResponseHeadersPolicyTypeDef(TypedDict):
    Id: str
    LastModifiedTime: datetime
    ResponseHeadersPolicyConfig: ResponseHeadersPolicyConfigOutputTypeDef


class ListStreamingDistributionsResultTypeDef(TypedDict):
    StreamingDistributionList: StreamingDistributionListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


OriginGroupFailoverCriteriaUnionTypeDef = Union[
    OriginGroupFailoverCriteriaTypeDef, OriginGroupFailoverCriteriaOutputTypeDef
]


class CreateStreamingDistributionRequestRequestTypeDef(TypedDict):
    StreamingDistributionConfig: StreamingDistributionConfigTypeDef


StreamingDistributionConfigUnionTypeDef = Union[
    StreamingDistributionConfigTypeDef, StreamingDistributionConfigOutputTypeDef
]


class UpdateStreamingDistributionRequestRequestTypeDef(TypedDict):
    StreamingDistributionConfig: StreamingDistributionConfigTypeDef
    Id: str
    IfMatch: NotRequired[str]


class CacheBehaviorsOutputTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[List[CacheBehaviorOutputTypeDef]]


class CachePolicyTypeDef(TypedDict):
    Id: str
    LastModifiedTime: datetime
    CachePolicyConfig: CachePolicyConfigOutputTypeDef


class GetCachePolicyConfigResultTypeDef(TypedDict):
    CachePolicyConfig: CachePolicyConfigOutputTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOriginRequestPolicyResultTypeDef(TypedDict):
    OriginRequestPolicy: OriginRequestPolicyTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetOriginRequestPolicyResultTypeDef(TypedDict):
    OriginRequestPolicy: OriginRequestPolicyTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


OriginRequestPolicySummaryTypeDef = TypedDict(
    "OriginRequestPolicySummaryTypeDef",
    {
        "Type": OriginRequestPolicyTypeType,
        "OriginRequestPolicy": OriginRequestPolicyTypeDef,
    },
)


class UpdateOriginRequestPolicyResultTypeDef(TypedDict):
    OriginRequestPolicy: OriginRequestPolicyTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


ContentTypeProfileConfigUnionTypeDef = Union[
    ContentTypeProfileConfigTypeDef, ContentTypeProfileConfigOutputTypeDef
]


class ContinuousDeploymentPolicyTypeDef(TypedDict):
    Id: str
    LastModifiedTime: datetime
    ContinuousDeploymentPolicyConfig: ContinuousDeploymentPolicyConfigOutputTypeDef


class GetContinuousDeploymentPolicyConfigResultTypeDef(TypedDict):
    ContinuousDeploymentPolicyConfig: ContinuousDeploymentPolicyConfigOutputTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContinuousDeploymentPolicyRequestRequestTypeDef(TypedDict):
    ContinuousDeploymentPolicyConfig: ContinuousDeploymentPolicyConfigTypeDef


class UpdateContinuousDeploymentPolicyRequestRequestTypeDef(TypedDict):
    ContinuousDeploymentPolicyConfig: ContinuousDeploymentPolicyConfigTypeDef
    Id: str
    IfMatch: NotRequired[str]


class ForwardedValuesTypeDef(TypedDict):
    QueryString: bool
    Cookies: CookiePreferenceUnionTypeDef
    Headers: NotRequired[HeadersUnionTypeDef]
    QueryStringCacheKeys: NotRequired[QueryStringCacheKeysUnionTypeDef]


class FieldLevelEncryptionProfileTypeDef(TypedDict):
    Id: str
    LastModifiedTime: datetime
    FieldLevelEncryptionProfileConfig: FieldLevelEncryptionProfileConfigOutputTypeDef


class GetFieldLevelEncryptionProfileConfigResultTypeDef(TypedDict):
    FieldLevelEncryptionProfileConfig: FieldLevelEncryptionProfileConfigOutputTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class FieldLevelEncryptionProfileListTypeDef(TypedDict):
    MaxItems: int
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[FieldLevelEncryptionProfileSummaryTypeDef]]


class ListRealtimeLogConfigsResultTypeDef(TypedDict):
    RealtimeLogConfigs: RealtimeLogConfigsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class EncryptionEntitiesTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[EncryptionEntityUnionTypeDef]]


class ListKeyGroupsResultTypeDef(TypedDict):
    KeyGroupList: KeyGroupListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateStreamingDistributionResultTypeDef(TypedDict):
    StreamingDistribution: StreamingDistributionTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateStreamingDistributionWithTagsResultTypeDef(TypedDict):
    StreamingDistribution: StreamingDistributionTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetStreamingDistributionResultTypeDef(TypedDict):
    StreamingDistribution: StreamingDistributionTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateStreamingDistributionResultTypeDef(TypedDict):
    StreamingDistribution: StreamingDistributionTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFunctionResultTypeDef(TypedDict):
    FunctionSummary: FunctionSummaryTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFunctionResultTypeDef(TypedDict):
    FunctionSummary: FunctionSummaryTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class FunctionListTypeDef(TypedDict):
    MaxItems: int
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[FunctionSummaryTypeDef]]


class PublishFunctionResultTypeDef(TypedDict):
    FunctionSummary: FunctionSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TestResultTypeDef(TypedDict):
    FunctionSummary: NotRequired[FunctionSummaryTypeDef]
    ComputeUtilization: NotRequired[str]
    FunctionExecutionLogs: NotRequired[List[str]]
    FunctionErrorMessage: NotRequired[str]
    FunctionOutput: NotRequired[str]


class UpdateFunctionResultTypeDef(TypedDict):
    FunctionSummary: FunctionSummaryTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFunctionRequestRequestTypeDef(TypedDict):
    Name: str
    FunctionConfig: FunctionConfigTypeDef
    FunctionCode: BlobTypeDef


class UpdateFunctionRequestRequestTypeDef(TypedDict):
    Name: str
    IfMatch: str
    FunctionConfig: FunctionConfigTypeDef
    FunctionCode: BlobTypeDef


class OriginTypeDef(TypedDict):
    Id: str
    DomainName: str
    OriginPath: NotRequired[str]
    CustomHeaders: NotRequired[CustomHeadersUnionTypeDef]
    S3OriginConfig: NotRequired[S3OriginConfigTypeDef]
    CustomOriginConfig: NotRequired[CustomOriginConfigUnionTypeDef]
    VpcOriginConfig: NotRequired[VpcOriginConfigTypeDef]
    ConnectionAttempts: NotRequired[int]
    ConnectionTimeout: NotRequired[int]
    OriginShield: NotRequired[OriginShieldTypeDef]
    OriginAccessControlId: NotRequired[str]


class FieldLevelEncryptionTypeDef(TypedDict):
    Id: str
    LastModifiedTime: datetime
    FieldLevelEncryptionConfig: FieldLevelEncryptionConfigOutputTypeDef


class GetFieldLevelEncryptionConfigResultTypeDef(TypedDict):
    FieldLevelEncryptionConfig: FieldLevelEncryptionConfigOutputTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class FieldLevelEncryptionListTypeDef(TypedDict):
    MaxItems: int
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[FieldLevelEncryptionSummaryTypeDef]]


QueryArgProfileConfigUnionTypeDef = Union[
    QueryArgProfileConfigTypeDef, QueryArgProfileConfigOutputTypeDef
]


class ParametersInCacheKeyAndForwardedToOriginTypeDef(TypedDict):
    EnableAcceptEncodingGzip: bool
    HeadersConfig: CachePolicyHeadersConfigUnionTypeDef
    CookiesConfig: CachePolicyCookiesConfigUnionTypeDef
    QueryStringsConfig: CachePolicyQueryStringsConfigUnionTypeDef
    EnableAcceptEncodingBrotli: NotRequired[bool]


class OriginRequestPolicyConfigTypeDef(TypedDict):
    Name: str
    HeadersConfig: OriginRequestPolicyHeadersConfigUnionTypeDef
    CookiesConfig: OriginRequestPolicyCookiesConfigUnionTypeDef
    QueryStringsConfig: OriginRequestPolicyQueryStringsConfigUnionTypeDef
    Comment: NotRequired[str]


class ResponseHeadersPolicyConfigTypeDef(TypedDict):
    Name: str
    Comment: NotRequired[str]
    CorsConfig: NotRequired[ResponseHeadersPolicyCorsConfigUnionTypeDef]
    SecurityHeadersConfig: NotRequired[ResponseHeadersPolicySecurityHeadersConfigTypeDef]
    ServerTimingHeadersConfig: NotRequired[ResponseHeadersPolicyServerTimingHeadersConfigTypeDef]
    CustomHeadersConfig: NotRequired[ResponseHeadersPolicyCustomHeadersConfigUnionTypeDef]
    RemoveHeadersConfig: NotRequired[ResponseHeadersPolicyRemoveHeadersConfigUnionTypeDef]


class CreateResponseHeadersPolicyResultTypeDef(TypedDict):
    ResponseHeadersPolicy: ResponseHeadersPolicyTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetResponseHeadersPolicyResultTypeDef(TypedDict):
    ResponseHeadersPolicy: ResponseHeadersPolicyTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


ResponseHeadersPolicySummaryTypeDef = TypedDict(
    "ResponseHeadersPolicySummaryTypeDef",
    {
        "Type": ResponseHeadersPolicyTypeType,
        "ResponseHeadersPolicy": ResponseHeadersPolicyTypeDef,
    },
)


class UpdateResponseHeadersPolicyResultTypeDef(TypedDict):
    ResponseHeadersPolicy: ResponseHeadersPolicyTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class OriginGroupTypeDef(TypedDict):
    Id: str
    FailoverCriteria: OriginGroupFailoverCriteriaUnionTypeDef
    Members: OriginGroupMembersUnionTypeDef
    SelectionCriteria: NotRequired[OriginGroupSelectionCriteriaType]


class StreamingDistributionConfigWithTagsTypeDef(TypedDict):
    StreamingDistributionConfig: StreamingDistributionConfigUnionTypeDef
    Tags: TagsUnionTypeDef


class DistributionConfigOutputTypeDef(TypedDict):
    CallerReference: str
    Origins: OriginsOutputTypeDef
    DefaultCacheBehavior: DefaultCacheBehaviorOutputTypeDef
    Comment: str
    Enabled: bool
    Aliases: NotRequired[AliasesOutputTypeDef]
    DefaultRootObject: NotRequired[str]
    OriginGroups: NotRequired[OriginGroupsOutputTypeDef]
    CacheBehaviors: NotRequired[CacheBehaviorsOutputTypeDef]
    CustomErrorResponses: NotRequired[CustomErrorResponsesOutputTypeDef]
    Logging: NotRequired[LoggingConfigTypeDef]
    PriceClass: NotRequired[PriceClassType]
    ViewerCertificate: NotRequired[ViewerCertificateTypeDef]
    Restrictions: NotRequired[RestrictionsOutputTypeDef]
    WebACLId: NotRequired[str]
    HttpVersion: NotRequired[HttpVersionType]
    IsIPV6Enabled: NotRequired[bool]
    ContinuousDeploymentPolicyId: NotRequired[str]
    Staging: NotRequired[bool]
    AnycastIpListId: NotRequired[str]


class DistributionSummaryTypeDef(TypedDict):
    Id: str
    ARN: str
    Status: str
    LastModifiedTime: datetime
    DomainName: str
    Aliases: AliasesOutputTypeDef
    Origins: OriginsOutputTypeDef
    DefaultCacheBehavior: DefaultCacheBehaviorOutputTypeDef
    CacheBehaviors: CacheBehaviorsOutputTypeDef
    CustomErrorResponses: CustomErrorResponsesOutputTypeDef
    Comment: str
    PriceClass: PriceClassType
    Enabled: bool
    ViewerCertificate: ViewerCertificateTypeDef
    Restrictions: RestrictionsOutputTypeDef
    WebACLId: str
    HttpVersion: HttpVersionType
    IsIPV6Enabled: bool
    Staging: bool
    OriginGroups: NotRequired[OriginGroupsOutputTypeDef]
    AliasICPRecordals: NotRequired[List[AliasICPRecordalTypeDef]]
    AnycastIpListId: NotRequired[str]


CachePolicySummaryTypeDef = TypedDict(
    "CachePolicySummaryTypeDef",
    {
        "Type": CachePolicyTypeType,
        "CachePolicy": CachePolicyTypeDef,
    },
)


class CreateCachePolicyResultTypeDef(TypedDict):
    CachePolicy: CachePolicyTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetCachePolicyResultTypeDef(TypedDict):
    CachePolicy: CachePolicyTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCachePolicyResultTypeDef(TypedDict):
    CachePolicy: CachePolicyTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class OriginRequestPolicyListTypeDef(TypedDict):
    MaxItems: int
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[OriginRequestPolicySummaryTypeDef]]


class ContinuousDeploymentPolicySummaryTypeDef(TypedDict):
    ContinuousDeploymentPolicy: ContinuousDeploymentPolicyTypeDef


class CreateContinuousDeploymentPolicyResultTypeDef(TypedDict):
    ContinuousDeploymentPolicy: ContinuousDeploymentPolicyTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetContinuousDeploymentPolicyResultTypeDef(TypedDict):
    ContinuousDeploymentPolicy: ContinuousDeploymentPolicyTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateContinuousDeploymentPolicyResultTypeDef(TypedDict):
    ContinuousDeploymentPolicy: ContinuousDeploymentPolicyTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


ForwardedValuesUnionTypeDef = Union[ForwardedValuesTypeDef, ForwardedValuesOutputTypeDef]


class CreateFieldLevelEncryptionProfileResultTypeDef(TypedDict):
    FieldLevelEncryptionProfile: FieldLevelEncryptionProfileTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetFieldLevelEncryptionProfileResultTypeDef(TypedDict):
    FieldLevelEncryptionProfile: FieldLevelEncryptionProfileTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFieldLevelEncryptionProfileResultTypeDef(TypedDict):
    FieldLevelEncryptionProfile: FieldLevelEncryptionProfileTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListFieldLevelEncryptionProfilesResultTypeDef(TypedDict):
    FieldLevelEncryptionProfileList: FieldLevelEncryptionProfileListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


EncryptionEntitiesUnionTypeDef = Union[EncryptionEntitiesTypeDef, EncryptionEntitiesOutputTypeDef]


class ListFunctionsResultTypeDef(TypedDict):
    FunctionList: FunctionListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TestFunctionResultTypeDef(TypedDict):
    TestResult: TestResultTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


OriginUnionTypeDef = Union[OriginTypeDef, OriginOutputTypeDef]


class CreateFieldLevelEncryptionConfigResultTypeDef(TypedDict):
    FieldLevelEncryption: FieldLevelEncryptionTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetFieldLevelEncryptionResultTypeDef(TypedDict):
    FieldLevelEncryption: FieldLevelEncryptionTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFieldLevelEncryptionConfigResultTypeDef(TypedDict):
    FieldLevelEncryption: FieldLevelEncryptionTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListFieldLevelEncryptionConfigsResultTypeDef(TypedDict):
    FieldLevelEncryptionList: FieldLevelEncryptionListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class FieldLevelEncryptionConfigTypeDef(TypedDict):
    CallerReference: str
    Comment: NotRequired[str]
    QueryArgProfileConfig: NotRequired[QueryArgProfileConfigUnionTypeDef]
    ContentTypeProfileConfig: NotRequired[ContentTypeProfileConfigUnionTypeDef]


ParametersInCacheKeyAndForwardedToOriginUnionTypeDef = Union[
    ParametersInCacheKeyAndForwardedToOriginTypeDef,
    ParametersInCacheKeyAndForwardedToOriginOutputTypeDef,
]


class CreateOriginRequestPolicyRequestRequestTypeDef(TypedDict):
    OriginRequestPolicyConfig: OriginRequestPolicyConfigTypeDef


class UpdateOriginRequestPolicyRequestRequestTypeDef(TypedDict):
    OriginRequestPolicyConfig: OriginRequestPolicyConfigTypeDef
    Id: str
    IfMatch: NotRequired[str]


class CreateResponseHeadersPolicyRequestRequestTypeDef(TypedDict):
    ResponseHeadersPolicyConfig: ResponseHeadersPolicyConfigTypeDef


class UpdateResponseHeadersPolicyRequestRequestTypeDef(TypedDict):
    ResponseHeadersPolicyConfig: ResponseHeadersPolicyConfigTypeDef
    Id: str
    IfMatch: NotRequired[str]


class ResponseHeadersPolicyListTypeDef(TypedDict):
    MaxItems: int
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[ResponseHeadersPolicySummaryTypeDef]]


OriginGroupUnionTypeDef = Union[OriginGroupTypeDef, OriginGroupOutputTypeDef]


class CreateStreamingDistributionWithTagsRequestRequestTypeDef(TypedDict):
    StreamingDistributionConfigWithTags: StreamingDistributionConfigWithTagsTypeDef


class DistributionTypeDef(TypedDict):
    Id: str
    ARN: str
    Status: str
    LastModifiedTime: datetime
    InProgressInvalidationBatches: int
    DomainName: str
    DistributionConfig: DistributionConfigOutputTypeDef
    ActiveTrustedSigners: NotRequired[ActiveTrustedSignersTypeDef]
    ActiveTrustedKeyGroups: NotRequired[ActiveTrustedKeyGroupsTypeDef]
    AliasICPRecordals: NotRequired[List[AliasICPRecordalTypeDef]]


class GetDistributionConfigResultTypeDef(TypedDict):
    DistributionConfig: DistributionConfigOutputTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class DistributionListTypeDef(TypedDict):
    Marker: str
    MaxItems: int
    IsTruncated: bool
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[DistributionSummaryTypeDef]]


class CachePolicyListTypeDef(TypedDict):
    MaxItems: int
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[CachePolicySummaryTypeDef]]


class ListOriginRequestPoliciesResultTypeDef(TypedDict):
    OriginRequestPolicyList: OriginRequestPolicyListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ContinuousDeploymentPolicyListTypeDef(TypedDict):
    MaxItems: int
    Quantity: int
    NextMarker: NotRequired[str]
    Items: NotRequired[List[ContinuousDeploymentPolicySummaryTypeDef]]


class CacheBehaviorTypeDef(TypedDict):
    PathPattern: str
    TargetOriginId: str
    ViewerProtocolPolicy: ViewerProtocolPolicyType
    TrustedSigners: NotRequired[TrustedSignersUnionTypeDef]
    TrustedKeyGroups: NotRequired[TrustedKeyGroupsUnionTypeDef]
    AllowedMethods: NotRequired[AllowedMethodsUnionTypeDef]
    SmoothStreaming: NotRequired[bool]
    Compress: NotRequired[bool]
    LambdaFunctionAssociations: NotRequired[LambdaFunctionAssociationsUnionTypeDef]
    FunctionAssociations: NotRequired[FunctionAssociationsUnionTypeDef]
    FieldLevelEncryptionId: NotRequired[str]
    RealtimeLogConfigArn: NotRequired[str]
    CachePolicyId: NotRequired[str]
    OriginRequestPolicyId: NotRequired[str]
    ResponseHeadersPolicyId: NotRequired[str]
    GrpcConfig: NotRequired[GrpcConfigTypeDef]
    ForwardedValues: NotRequired[ForwardedValuesUnionTypeDef]
    MinTTL: NotRequired[int]
    DefaultTTL: NotRequired[int]
    MaxTTL: NotRequired[int]


class DefaultCacheBehaviorTypeDef(TypedDict):
    TargetOriginId: str
    ViewerProtocolPolicy: ViewerProtocolPolicyType
    TrustedSigners: NotRequired[TrustedSignersUnionTypeDef]
    TrustedKeyGroups: NotRequired[TrustedKeyGroupsUnionTypeDef]
    AllowedMethods: NotRequired[AllowedMethodsUnionTypeDef]
    SmoothStreaming: NotRequired[bool]
    Compress: NotRequired[bool]
    LambdaFunctionAssociations: NotRequired[LambdaFunctionAssociationsUnionTypeDef]
    FunctionAssociations: NotRequired[FunctionAssociationsUnionTypeDef]
    FieldLevelEncryptionId: NotRequired[str]
    RealtimeLogConfigArn: NotRequired[str]
    CachePolicyId: NotRequired[str]
    OriginRequestPolicyId: NotRequired[str]
    ResponseHeadersPolicyId: NotRequired[str]
    GrpcConfig: NotRequired[GrpcConfigTypeDef]
    ForwardedValues: NotRequired[ForwardedValuesUnionTypeDef]
    MinTTL: NotRequired[int]
    DefaultTTL: NotRequired[int]
    MaxTTL: NotRequired[int]


class FieldLevelEncryptionProfileConfigTypeDef(TypedDict):
    Name: str
    CallerReference: str
    EncryptionEntities: EncryptionEntitiesUnionTypeDef
    Comment: NotRequired[str]


class OriginsTypeDef(TypedDict):
    Quantity: int
    Items: Sequence[OriginUnionTypeDef]


class CreateFieldLevelEncryptionConfigRequestRequestTypeDef(TypedDict):
    FieldLevelEncryptionConfig: FieldLevelEncryptionConfigTypeDef


class UpdateFieldLevelEncryptionConfigRequestRequestTypeDef(TypedDict):
    FieldLevelEncryptionConfig: FieldLevelEncryptionConfigTypeDef
    Id: str
    IfMatch: NotRequired[str]


class CachePolicyConfigTypeDef(TypedDict):
    Name: str
    MinTTL: int
    Comment: NotRequired[str]
    DefaultTTL: NotRequired[int]
    MaxTTL: NotRequired[int]
    ParametersInCacheKeyAndForwardedToOrigin: NotRequired[
        ParametersInCacheKeyAndForwardedToOriginUnionTypeDef
    ]


class ListResponseHeadersPoliciesResultTypeDef(TypedDict):
    ResponseHeadersPolicyList: ResponseHeadersPolicyListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class OriginGroupsTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[OriginGroupUnionTypeDef]]


class CopyDistributionResultTypeDef(TypedDict):
    Distribution: DistributionTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDistributionResultTypeDef(TypedDict):
    Distribution: DistributionTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDistributionWithTagsResultTypeDef(TypedDict):
    Distribution: DistributionTypeDef
    Location: str
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetDistributionResultTypeDef(TypedDict):
    Distribution: DistributionTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDistributionResultTypeDef(TypedDict):
    Distribution: DistributionTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDistributionWithStagingConfigResultTypeDef(TypedDict):
    Distribution: DistributionTypeDef
    ETag: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListDistributionsByAnycastIpListIdResultTypeDef(TypedDict):
    DistributionList: DistributionListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDistributionsByRealtimeLogConfigResultTypeDef(TypedDict):
    DistributionList: DistributionListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDistributionsByWebACLIdResultTypeDef(TypedDict):
    DistributionList: DistributionListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDistributionsResultTypeDef(TypedDict):
    DistributionList: DistributionListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListCachePoliciesResultTypeDef(TypedDict):
    CachePolicyList: CachePolicyListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListContinuousDeploymentPoliciesResultTypeDef(TypedDict):
    ContinuousDeploymentPolicyList: ContinuousDeploymentPolicyListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


CacheBehaviorUnionTypeDef = Union[CacheBehaviorTypeDef, CacheBehaviorOutputTypeDef]
DefaultCacheBehaviorUnionTypeDef = Union[
    DefaultCacheBehaviorTypeDef, DefaultCacheBehaviorOutputTypeDef
]


class CreateFieldLevelEncryptionProfileRequestRequestTypeDef(TypedDict):
    FieldLevelEncryptionProfileConfig: FieldLevelEncryptionProfileConfigTypeDef


class UpdateFieldLevelEncryptionProfileRequestRequestTypeDef(TypedDict):
    FieldLevelEncryptionProfileConfig: FieldLevelEncryptionProfileConfigTypeDef
    Id: str
    IfMatch: NotRequired[str]


OriginsUnionTypeDef = Union[OriginsTypeDef, OriginsOutputTypeDef]


class CreateCachePolicyRequestRequestTypeDef(TypedDict):
    CachePolicyConfig: CachePolicyConfigTypeDef


class UpdateCachePolicyRequestRequestTypeDef(TypedDict):
    CachePolicyConfig: CachePolicyConfigTypeDef
    Id: str
    IfMatch: NotRequired[str]


OriginGroupsUnionTypeDef = Union[OriginGroupsTypeDef, OriginGroupsOutputTypeDef]


class CacheBehaviorsTypeDef(TypedDict):
    Quantity: int
    Items: NotRequired[Sequence[CacheBehaviorUnionTypeDef]]


CacheBehaviorsUnionTypeDef = Union[CacheBehaviorsTypeDef, CacheBehaviorsOutputTypeDef]


class DistributionConfigTypeDef(TypedDict):
    CallerReference: str
    Origins: OriginsUnionTypeDef
    DefaultCacheBehavior: DefaultCacheBehaviorUnionTypeDef
    Comment: str
    Enabled: bool
    Aliases: NotRequired[AliasesUnionTypeDef]
    DefaultRootObject: NotRequired[str]
    OriginGroups: NotRequired[OriginGroupsUnionTypeDef]
    CacheBehaviors: NotRequired[CacheBehaviorsUnionTypeDef]
    CustomErrorResponses: NotRequired[CustomErrorResponsesUnionTypeDef]
    Logging: NotRequired[LoggingConfigTypeDef]
    PriceClass: NotRequired[PriceClassType]
    ViewerCertificate: NotRequired[ViewerCertificateTypeDef]
    Restrictions: NotRequired[RestrictionsUnionTypeDef]
    WebACLId: NotRequired[str]
    HttpVersion: NotRequired[HttpVersionType]
    IsIPV6Enabled: NotRequired[bool]
    ContinuousDeploymentPolicyId: NotRequired[str]
    Staging: NotRequired[bool]
    AnycastIpListId: NotRequired[str]


class CreateDistributionRequestRequestTypeDef(TypedDict):
    DistributionConfig: DistributionConfigTypeDef


DistributionConfigUnionTypeDef = Union[DistributionConfigTypeDef, DistributionConfigOutputTypeDef]


class UpdateDistributionRequestRequestTypeDef(TypedDict):
    DistributionConfig: DistributionConfigTypeDef
    Id: str
    IfMatch: NotRequired[str]


class DistributionConfigWithTagsTypeDef(TypedDict):
    DistributionConfig: DistributionConfigUnionTypeDef
    Tags: TagsUnionTypeDef


class CreateDistributionWithTagsRequestRequestTypeDef(TypedDict):
    DistributionConfigWithTags: DistributionConfigWithTagsTypeDef
