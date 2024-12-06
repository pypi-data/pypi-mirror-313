"""
Type annotations for s3control service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_s3control.client import S3ControlClient

    session = Session()
    client: S3ControlClient = session.client("s3control")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListAccessPointsForObjectLambdaPaginator, ListCallerAccessGrantsPaginator
from .type_defs import (
    AssociateAccessGrantsIdentityCenterRequestRequestTypeDef,
    CreateAccessGrantRequestRequestTypeDef,
    CreateAccessGrantResultTypeDef,
    CreateAccessGrantsInstanceRequestRequestTypeDef,
    CreateAccessGrantsInstanceResultTypeDef,
    CreateAccessGrantsLocationRequestRequestTypeDef,
    CreateAccessGrantsLocationResultTypeDef,
    CreateAccessPointForObjectLambdaRequestRequestTypeDef,
    CreateAccessPointForObjectLambdaResultTypeDef,
    CreateAccessPointRequestRequestTypeDef,
    CreateAccessPointResultTypeDef,
    CreateBucketRequestRequestTypeDef,
    CreateBucketResultTypeDef,
    CreateJobRequestRequestTypeDef,
    CreateJobResultTypeDef,
    CreateMultiRegionAccessPointRequestRequestTypeDef,
    CreateMultiRegionAccessPointResultTypeDef,
    CreateStorageLensGroupRequestRequestTypeDef,
    DeleteAccessGrantRequestRequestTypeDef,
    DeleteAccessGrantsInstanceRequestRequestTypeDef,
    DeleteAccessGrantsInstanceResourcePolicyRequestRequestTypeDef,
    DeleteAccessGrantsLocationRequestRequestTypeDef,
    DeleteAccessPointForObjectLambdaRequestRequestTypeDef,
    DeleteAccessPointPolicyForObjectLambdaRequestRequestTypeDef,
    DeleteAccessPointPolicyRequestRequestTypeDef,
    DeleteAccessPointRequestRequestTypeDef,
    DeleteBucketLifecycleConfigurationRequestRequestTypeDef,
    DeleteBucketPolicyRequestRequestTypeDef,
    DeleteBucketReplicationRequestRequestTypeDef,
    DeleteBucketRequestRequestTypeDef,
    DeleteBucketTaggingRequestRequestTypeDef,
    DeleteJobTaggingRequestRequestTypeDef,
    DeleteMultiRegionAccessPointRequestRequestTypeDef,
    DeleteMultiRegionAccessPointResultTypeDef,
    DeletePublicAccessBlockRequestRequestTypeDef,
    DeleteStorageLensConfigurationRequestRequestTypeDef,
    DeleteStorageLensConfigurationTaggingRequestRequestTypeDef,
    DeleteStorageLensGroupRequestRequestTypeDef,
    DescribeJobRequestRequestTypeDef,
    DescribeJobResultTypeDef,
    DescribeMultiRegionAccessPointOperationRequestRequestTypeDef,
    DescribeMultiRegionAccessPointOperationResultTypeDef,
    DissociateAccessGrantsIdentityCenterRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAccessGrantRequestRequestTypeDef,
    GetAccessGrantResultTypeDef,
    GetAccessGrantsInstanceForPrefixRequestRequestTypeDef,
    GetAccessGrantsInstanceForPrefixResultTypeDef,
    GetAccessGrantsInstanceRequestRequestTypeDef,
    GetAccessGrantsInstanceResourcePolicyRequestRequestTypeDef,
    GetAccessGrantsInstanceResourcePolicyResultTypeDef,
    GetAccessGrantsInstanceResultTypeDef,
    GetAccessGrantsLocationRequestRequestTypeDef,
    GetAccessGrantsLocationResultTypeDef,
    GetAccessPointConfigurationForObjectLambdaRequestRequestTypeDef,
    GetAccessPointConfigurationForObjectLambdaResultTypeDef,
    GetAccessPointForObjectLambdaRequestRequestTypeDef,
    GetAccessPointForObjectLambdaResultTypeDef,
    GetAccessPointPolicyForObjectLambdaRequestRequestTypeDef,
    GetAccessPointPolicyForObjectLambdaResultTypeDef,
    GetAccessPointPolicyRequestRequestTypeDef,
    GetAccessPointPolicyResultTypeDef,
    GetAccessPointPolicyStatusForObjectLambdaRequestRequestTypeDef,
    GetAccessPointPolicyStatusForObjectLambdaResultTypeDef,
    GetAccessPointPolicyStatusRequestRequestTypeDef,
    GetAccessPointPolicyStatusResultTypeDef,
    GetAccessPointRequestRequestTypeDef,
    GetAccessPointResultTypeDef,
    GetBucketLifecycleConfigurationRequestRequestTypeDef,
    GetBucketLifecycleConfigurationResultTypeDef,
    GetBucketPolicyRequestRequestTypeDef,
    GetBucketPolicyResultTypeDef,
    GetBucketReplicationRequestRequestTypeDef,
    GetBucketReplicationResultTypeDef,
    GetBucketRequestRequestTypeDef,
    GetBucketResultTypeDef,
    GetBucketTaggingRequestRequestTypeDef,
    GetBucketTaggingResultTypeDef,
    GetBucketVersioningRequestRequestTypeDef,
    GetBucketVersioningResultTypeDef,
    GetDataAccessRequestRequestTypeDef,
    GetDataAccessResultTypeDef,
    GetJobTaggingRequestRequestTypeDef,
    GetJobTaggingResultTypeDef,
    GetMultiRegionAccessPointPolicyRequestRequestTypeDef,
    GetMultiRegionAccessPointPolicyResultTypeDef,
    GetMultiRegionAccessPointPolicyStatusRequestRequestTypeDef,
    GetMultiRegionAccessPointPolicyStatusResultTypeDef,
    GetMultiRegionAccessPointRequestRequestTypeDef,
    GetMultiRegionAccessPointResultTypeDef,
    GetMultiRegionAccessPointRoutesRequestRequestTypeDef,
    GetMultiRegionAccessPointRoutesResultTypeDef,
    GetPublicAccessBlockOutputTypeDef,
    GetPublicAccessBlockRequestRequestTypeDef,
    GetStorageLensConfigurationRequestRequestTypeDef,
    GetStorageLensConfigurationResultTypeDef,
    GetStorageLensConfigurationTaggingRequestRequestTypeDef,
    GetStorageLensConfigurationTaggingResultTypeDef,
    GetStorageLensGroupRequestRequestTypeDef,
    GetStorageLensGroupResultTypeDef,
    ListAccessGrantsInstancesRequestRequestTypeDef,
    ListAccessGrantsInstancesResultTypeDef,
    ListAccessGrantsLocationsRequestRequestTypeDef,
    ListAccessGrantsLocationsResultTypeDef,
    ListAccessGrantsRequestRequestTypeDef,
    ListAccessGrantsResultTypeDef,
    ListAccessPointsForObjectLambdaRequestRequestTypeDef,
    ListAccessPointsForObjectLambdaResultTypeDef,
    ListAccessPointsRequestRequestTypeDef,
    ListAccessPointsResultTypeDef,
    ListCallerAccessGrantsRequestRequestTypeDef,
    ListCallerAccessGrantsResultTypeDef,
    ListJobsRequestRequestTypeDef,
    ListJobsResultTypeDef,
    ListMultiRegionAccessPointsRequestRequestTypeDef,
    ListMultiRegionAccessPointsResultTypeDef,
    ListRegionalBucketsRequestRequestTypeDef,
    ListRegionalBucketsResultTypeDef,
    ListStorageLensConfigurationsRequestRequestTypeDef,
    ListStorageLensConfigurationsResultTypeDef,
    ListStorageLensGroupsRequestRequestTypeDef,
    ListStorageLensGroupsResultTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResultTypeDef,
    PutAccessGrantsInstanceResourcePolicyRequestRequestTypeDef,
    PutAccessGrantsInstanceResourcePolicyResultTypeDef,
    PutAccessPointConfigurationForObjectLambdaRequestRequestTypeDef,
    PutAccessPointPolicyForObjectLambdaRequestRequestTypeDef,
    PutAccessPointPolicyRequestRequestTypeDef,
    PutBucketLifecycleConfigurationRequestRequestTypeDef,
    PutBucketPolicyRequestRequestTypeDef,
    PutBucketReplicationRequestRequestTypeDef,
    PutBucketTaggingRequestRequestTypeDef,
    PutBucketVersioningRequestRequestTypeDef,
    PutJobTaggingRequestRequestTypeDef,
    PutMultiRegionAccessPointPolicyRequestRequestTypeDef,
    PutMultiRegionAccessPointPolicyResultTypeDef,
    PutPublicAccessBlockRequestRequestTypeDef,
    PutStorageLensConfigurationRequestRequestTypeDef,
    PutStorageLensConfigurationTaggingRequestRequestTypeDef,
    SubmitMultiRegionAccessPointRoutesRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAccessGrantsLocationRequestRequestTypeDef,
    UpdateAccessGrantsLocationResultTypeDef,
    UpdateJobPriorityRequestRequestTypeDef,
    UpdateJobPriorityResultTypeDef,
    UpdateJobStatusRequestRequestTypeDef,
    UpdateJobStatusResultTypeDef,
    UpdateStorageLensGroupRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("S3ControlClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    BucketAlreadyExists: Type[BotocoreClientError]
    BucketAlreadyOwnedByYou: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    IdempotencyException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    JobStatusException: Type[BotocoreClientError]
    NoSuchPublicAccessBlockConfiguration: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]


class S3ControlClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        S3ControlClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#close)
        """

    def associate_access_grants_identity_center(
        self, **kwargs: Unpack[AssociateAccessGrantsIdentityCenterRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associate your S3 Access Grants instance with an Amazon Web Services IAM
        Identity Center instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/associate_access_grants_identity_center.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#associate_access_grants_identity_center)
        """

    def create_access_grant(
        self, **kwargs: Unpack[CreateAccessGrantRequestRequestTypeDef]
    ) -> CreateAccessGrantResultTypeDef:
        """
        Creates an access grant that gives a grantee access to your S3 data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/create_access_grant.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#create_access_grant)
        """

    def create_access_grants_instance(
        self, **kwargs: Unpack[CreateAccessGrantsInstanceRequestRequestTypeDef]
    ) -> CreateAccessGrantsInstanceResultTypeDef:
        """
        Creates an S3 Access Grants instance, which serves as a logical grouping for
        access grants.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/create_access_grants_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#create_access_grants_instance)
        """

    def create_access_grants_location(
        self, **kwargs: Unpack[CreateAccessGrantsLocationRequestRequestTypeDef]
    ) -> CreateAccessGrantsLocationResultTypeDef:
        """
        The S3 data location that you would like to register in your S3 Access Grants
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/create_access_grants_location.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#create_access_grants_location)
        """

    def create_access_point(
        self, **kwargs: Unpack[CreateAccessPointRequestRequestTypeDef]
    ) -> CreateAccessPointResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/create_access_point.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#create_access_point)
        """

    def create_access_point_for_object_lambda(
        self, **kwargs: Unpack[CreateAccessPointForObjectLambdaRequestRequestTypeDef]
    ) -> CreateAccessPointForObjectLambdaResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/create_access_point_for_object_lambda.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#create_access_point_for_object_lambda)
        """

    def create_bucket(
        self, **kwargs: Unpack[CreateBucketRequestRequestTypeDef]
    ) -> CreateBucketResultTypeDef:
        """
        This action creates an Amazon S3 on Outposts bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/create_bucket.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#create_bucket)
        """

    def create_job(
        self, **kwargs: Unpack[CreateJobRequestRequestTypeDef]
    ) -> CreateJobResultTypeDef:
        """
        This operation creates an S3 Batch Operations job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/create_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#create_job)
        """

    def create_multi_region_access_point(
        self, **kwargs: Unpack[CreateMultiRegionAccessPointRequestRequestTypeDef]
    ) -> CreateMultiRegionAccessPointResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/create_multi_region_access_point.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#create_multi_region_access_point)
        """

    def create_storage_lens_group(
        self, **kwargs: Unpack[CreateStorageLensGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a new S3 Storage Lens group and associates it with the specified Amazon
        Web Services account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/create_storage_lens_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#create_storage_lens_group)
        """

    def delete_access_grant(
        self, **kwargs: Unpack[DeleteAccessGrantRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the access grant from the S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_access_grant.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_access_grant)
        """

    def delete_access_grants_instance(
        self, **kwargs: Unpack[DeleteAccessGrantsInstanceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes your S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_access_grants_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_access_grants_instance)
        """

    def delete_access_grants_instance_resource_policy(
        self, **kwargs: Unpack[DeleteAccessGrantsInstanceResourcePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the resource policy of the S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_access_grants_instance_resource_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_access_grants_instance_resource_policy)
        """

    def delete_access_grants_location(
        self, **kwargs: Unpack[DeleteAccessGrantsLocationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters a location from your S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_access_grants_location.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_access_grants_location)
        """

    def delete_access_point(
        self, **kwargs: Unpack[DeleteAccessPointRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_access_point.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_access_point)
        """

    def delete_access_point_for_object_lambda(
        self, **kwargs: Unpack[DeleteAccessPointForObjectLambdaRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_access_point_for_object_lambda.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_access_point_for_object_lambda)
        """

    def delete_access_point_policy(
        self, **kwargs: Unpack[DeleteAccessPointPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_access_point_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_access_point_policy)
        """

    def delete_access_point_policy_for_object_lambda(
        self, **kwargs: Unpack[DeleteAccessPointPolicyForObjectLambdaRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_access_point_policy_for_object_lambda.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_access_point_policy_for_object_lambda)
        """

    def delete_bucket(
        self, **kwargs: Unpack[DeleteBucketRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This action deletes an Amazon S3 on Outposts bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_bucket.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_bucket)
        """

    def delete_bucket_lifecycle_configuration(
        self, **kwargs: Unpack[DeleteBucketLifecycleConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This action deletes an Amazon S3 on Outposts bucket's lifecycle configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_bucket_lifecycle_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_bucket_lifecycle_configuration)
        """

    def delete_bucket_policy(
        self, **kwargs: Unpack[DeleteBucketPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This action deletes an Amazon S3 on Outposts bucket policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_bucket_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_bucket_policy)
        """

    def delete_bucket_replication(
        self, **kwargs: Unpack[DeleteBucketReplicationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation deletes an Amazon S3 on Outposts bucket's replication
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_bucket_replication.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_bucket_replication)
        """

    def delete_bucket_tagging(
        self, **kwargs: Unpack[DeleteBucketTaggingRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This action deletes an Amazon S3 on Outposts bucket's tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_bucket_tagging.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_bucket_tagging)
        """

    def delete_job_tagging(
        self, **kwargs: Unpack[DeleteJobTaggingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the entire tag set from the specified S3 Batch Operations job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_job_tagging.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_job_tagging)
        """

    def delete_multi_region_access_point(
        self, **kwargs: Unpack[DeleteMultiRegionAccessPointRequestRequestTypeDef]
    ) -> DeleteMultiRegionAccessPointResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_multi_region_access_point.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_multi_region_access_point)
        """

    def delete_public_access_block(
        self, **kwargs: Unpack[DeletePublicAccessBlockRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_public_access_block.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_public_access_block)
        """

    def delete_storage_lens_configuration(
        self, **kwargs: Unpack[DeleteStorageLensConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_storage_lens_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_storage_lens_configuration)
        """

    def delete_storage_lens_configuration_tagging(
        self, **kwargs: Unpack[DeleteStorageLensConfigurationTaggingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_storage_lens_configuration_tagging.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_storage_lens_configuration_tagging)
        """

    def delete_storage_lens_group(
        self, **kwargs: Unpack[DeleteStorageLensGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an existing S3 Storage Lens group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/delete_storage_lens_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#delete_storage_lens_group)
        """

    def describe_job(
        self, **kwargs: Unpack[DescribeJobRequestRequestTypeDef]
    ) -> DescribeJobResultTypeDef:
        """
        Retrieves the configuration parameters and status for a Batch Operations job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/describe_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#describe_job)
        """

    def describe_multi_region_access_point_operation(
        self, **kwargs: Unpack[DescribeMultiRegionAccessPointOperationRequestRequestTypeDef]
    ) -> DescribeMultiRegionAccessPointOperationResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/describe_multi_region_access_point_operation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#describe_multi_region_access_point_operation)
        """

    def dissociate_access_grants_identity_center(
        self, **kwargs: Unpack[DissociateAccessGrantsIdentityCenterRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Dissociates the Amazon Web Services IAM Identity Center instance from the S3
        Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/dissociate_access_grants_identity_center.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#dissociate_access_grants_identity_center)
        """

    def get_access_grant(
        self, **kwargs: Unpack[GetAccessGrantRequestRequestTypeDef]
    ) -> GetAccessGrantResultTypeDef:
        """
        Get the details of an access grant from your S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_access_grant.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_access_grant)
        """

    def get_access_grants_instance(
        self, **kwargs: Unpack[GetAccessGrantsInstanceRequestRequestTypeDef]
    ) -> GetAccessGrantsInstanceResultTypeDef:
        """
        Retrieves the S3 Access Grants instance for a Region in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_access_grants_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_access_grants_instance)
        """

    def get_access_grants_instance_for_prefix(
        self, **kwargs: Unpack[GetAccessGrantsInstanceForPrefixRequestRequestTypeDef]
    ) -> GetAccessGrantsInstanceForPrefixResultTypeDef:
        """
        Retrieve the S3 Access Grants instance that contains a particular prefix.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_access_grants_instance_for_prefix.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_access_grants_instance_for_prefix)
        """

    def get_access_grants_instance_resource_policy(
        self, **kwargs: Unpack[GetAccessGrantsInstanceResourcePolicyRequestRequestTypeDef]
    ) -> GetAccessGrantsInstanceResourcePolicyResultTypeDef:
        """
        Returns the resource policy of the S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_access_grants_instance_resource_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_access_grants_instance_resource_policy)
        """

    def get_access_grants_location(
        self, **kwargs: Unpack[GetAccessGrantsLocationRequestRequestTypeDef]
    ) -> GetAccessGrantsLocationResultTypeDef:
        """
        Retrieves the details of a particular location registered in your S3 Access
        Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_access_grants_location.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_access_grants_location)
        """

    def get_access_point(
        self, **kwargs: Unpack[GetAccessPointRequestRequestTypeDef]
    ) -> GetAccessPointResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_access_point.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_access_point)
        """

    def get_access_point_configuration_for_object_lambda(
        self, **kwargs: Unpack[GetAccessPointConfigurationForObjectLambdaRequestRequestTypeDef]
    ) -> GetAccessPointConfigurationForObjectLambdaResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_access_point_configuration_for_object_lambda.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_access_point_configuration_for_object_lambda)
        """

    def get_access_point_for_object_lambda(
        self, **kwargs: Unpack[GetAccessPointForObjectLambdaRequestRequestTypeDef]
    ) -> GetAccessPointForObjectLambdaResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_access_point_for_object_lambda.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_access_point_for_object_lambda)
        """

    def get_access_point_policy(
        self, **kwargs: Unpack[GetAccessPointPolicyRequestRequestTypeDef]
    ) -> GetAccessPointPolicyResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_access_point_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_access_point_policy)
        """

    def get_access_point_policy_for_object_lambda(
        self, **kwargs: Unpack[GetAccessPointPolicyForObjectLambdaRequestRequestTypeDef]
    ) -> GetAccessPointPolicyForObjectLambdaResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_access_point_policy_for_object_lambda.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_access_point_policy_for_object_lambda)
        """

    def get_access_point_policy_status(
        self, **kwargs: Unpack[GetAccessPointPolicyStatusRequestRequestTypeDef]
    ) -> GetAccessPointPolicyStatusResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_access_point_policy_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_access_point_policy_status)
        """

    def get_access_point_policy_status_for_object_lambda(
        self, **kwargs: Unpack[GetAccessPointPolicyStatusForObjectLambdaRequestRequestTypeDef]
    ) -> GetAccessPointPolicyStatusForObjectLambdaResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_access_point_policy_status_for_object_lambda.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_access_point_policy_status_for_object_lambda)
        """

    def get_bucket(
        self, **kwargs: Unpack[GetBucketRequestRequestTypeDef]
    ) -> GetBucketResultTypeDef:
        """
        Gets an Amazon S3 on Outposts bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_bucket.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_bucket)
        """

    def get_bucket_lifecycle_configuration(
        self, **kwargs: Unpack[GetBucketLifecycleConfigurationRequestRequestTypeDef]
    ) -> GetBucketLifecycleConfigurationResultTypeDef:
        """
        This action gets an Amazon S3 on Outposts bucket's lifecycle configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_bucket_lifecycle_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_bucket_lifecycle_configuration)
        """

    def get_bucket_policy(
        self, **kwargs: Unpack[GetBucketPolicyRequestRequestTypeDef]
    ) -> GetBucketPolicyResultTypeDef:
        """
        This action gets a bucket policy for an Amazon S3 on Outposts bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_bucket_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_bucket_policy)
        """

    def get_bucket_replication(
        self, **kwargs: Unpack[GetBucketReplicationRequestRequestTypeDef]
    ) -> GetBucketReplicationResultTypeDef:
        """
        This operation gets an Amazon S3 on Outposts bucket's replication configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_bucket_replication.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_bucket_replication)
        """

    def get_bucket_tagging(
        self, **kwargs: Unpack[GetBucketTaggingRequestRequestTypeDef]
    ) -> GetBucketTaggingResultTypeDef:
        """
        This action gets an Amazon S3 on Outposts bucket's tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_bucket_tagging.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_bucket_tagging)
        """

    def get_bucket_versioning(
        self, **kwargs: Unpack[GetBucketVersioningRequestRequestTypeDef]
    ) -> GetBucketVersioningResultTypeDef:
        """
        This operation returns the versioning state for S3 on Outposts buckets only.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_bucket_versioning.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_bucket_versioning)
        """

    def get_data_access(
        self, **kwargs: Unpack[GetDataAccessRequestRequestTypeDef]
    ) -> GetDataAccessResultTypeDef:
        """
        Returns a temporary access credential from S3 Access Grants to the grantee or
        client application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_data_access.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_data_access)
        """

    def get_job_tagging(
        self, **kwargs: Unpack[GetJobTaggingRequestRequestTypeDef]
    ) -> GetJobTaggingResultTypeDef:
        """
        Returns the tags on an S3 Batch Operations job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_job_tagging.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_job_tagging)
        """

    def get_multi_region_access_point(
        self, **kwargs: Unpack[GetMultiRegionAccessPointRequestRequestTypeDef]
    ) -> GetMultiRegionAccessPointResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_multi_region_access_point.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_multi_region_access_point)
        """

    def get_multi_region_access_point_policy(
        self, **kwargs: Unpack[GetMultiRegionAccessPointPolicyRequestRequestTypeDef]
    ) -> GetMultiRegionAccessPointPolicyResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_multi_region_access_point_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_multi_region_access_point_policy)
        """

    def get_multi_region_access_point_policy_status(
        self, **kwargs: Unpack[GetMultiRegionAccessPointPolicyStatusRequestRequestTypeDef]
    ) -> GetMultiRegionAccessPointPolicyStatusResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_multi_region_access_point_policy_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_multi_region_access_point_policy_status)
        """

    def get_multi_region_access_point_routes(
        self, **kwargs: Unpack[GetMultiRegionAccessPointRoutesRequestRequestTypeDef]
    ) -> GetMultiRegionAccessPointRoutesResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_multi_region_access_point_routes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_multi_region_access_point_routes)
        """

    def get_public_access_block(
        self, **kwargs: Unpack[GetPublicAccessBlockRequestRequestTypeDef]
    ) -> GetPublicAccessBlockOutputTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_public_access_block.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_public_access_block)
        """

    def get_storage_lens_configuration(
        self, **kwargs: Unpack[GetStorageLensConfigurationRequestRequestTypeDef]
    ) -> GetStorageLensConfigurationResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_storage_lens_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_storage_lens_configuration)
        """

    def get_storage_lens_configuration_tagging(
        self, **kwargs: Unpack[GetStorageLensConfigurationTaggingRequestRequestTypeDef]
    ) -> GetStorageLensConfigurationTaggingResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_storage_lens_configuration_tagging.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_storage_lens_configuration_tagging)
        """

    def get_storage_lens_group(
        self, **kwargs: Unpack[GetStorageLensGroupRequestRequestTypeDef]
    ) -> GetStorageLensGroupResultTypeDef:
        """
        Retrieves the Storage Lens group configuration details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_storage_lens_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_storage_lens_group)
        """

    def list_access_grants(
        self, **kwargs: Unpack[ListAccessGrantsRequestRequestTypeDef]
    ) -> ListAccessGrantsResultTypeDef:
        """
        Returns the list of access grants in your S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/list_access_grants.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#list_access_grants)
        """

    def list_access_grants_instances(
        self, **kwargs: Unpack[ListAccessGrantsInstancesRequestRequestTypeDef]
    ) -> ListAccessGrantsInstancesResultTypeDef:
        """
        Returns a list of S3 Access Grants instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/list_access_grants_instances.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#list_access_grants_instances)
        """

    def list_access_grants_locations(
        self, **kwargs: Unpack[ListAccessGrantsLocationsRequestRequestTypeDef]
    ) -> ListAccessGrantsLocationsResultTypeDef:
        """
        Returns a list of the locations registered in your S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/list_access_grants_locations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#list_access_grants_locations)
        """

    def list_access_points(
        self, **kwargs: Unpack[ListAccessPointsRequestRequestTypeDef]
    ) -> ListAccessPointsResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/list_access_points.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#list_access_points)
        """

    def list_access_points_for_object_lambda(
        self, **kwargs: Unpack[ListAccessPointsForObjectLambdaRequestRequestTypeDef]
    ) -> ListAccessPointsForObjectLambdaResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/list_access_points_for_object_lambda.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#list_access_points_for_object_lambda)
        """

    def list_caller_access_grants(
        self, **kwargs: Unpack[ListCallerAccessGrantsRequestRequestTypeDef]
    ) -> ListCallerAccessGrantsResultTypeDef:
        """
        Use this API to list the access grants that grant the caller access to Amazon
        S3 data through S3 Access Grants.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/list_caller_access_grants.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#list_caller_access_grants)
        """

    def list_jobs(self, **kwargs: Unpack[ListJobsRequestRequestTypeDef]) -> ListJobsResultTypeDef:
        """
        Lists current S3 Batch Operations jobs as well as the jobs that have ended
        within the last 90 days for the Amazon Web Services account making the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/list_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#list_jobs)
        """

    def list_multi_region_access_points(
        self, **kwargs: Unpack[ListMultiRegionAccessPointsRequestRequestTypeDef]
    ) -> ListMultiRegionAccessPointsResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/list_multi_region_access_points.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#list_multi_region_access_points)
        """

    def list_regional_buckets(
        self, **kwargs: Unpack[ListRegionalBucketsRequestRequestTypeDef]
    ) -> ListRegionalBucketsResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/list_regional_buckets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#list_regional_buckets)
        """

    def list_storage_lens_configurations(
        self, **kwargs: Unpack[ListStorageLensConfigurationsRequestRequestTypeDef]
    ) -> ListStorageLensConfigurationsResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/list_storage_lens_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#list_storage_lens_configurations)
        """

    def list_storage_lens_groups(
        self, **kwargs: Unpack[ListStorageLensGroupsRequestRequestTypeDef]
    ) -> ListStorageLensGroupsResultTypeDef:
        """
        Lists all the Storage Lens groups in the specified home Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/list_storage_lens_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#list_storage_lens_groups)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResultTypeDef:
        """
        This operation allows you to list all the Amazon Web Services resource tags for
        a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#list_tags_for_resource)
        """

    def put_access_grants_instance_resource_policy(
        self, **kwargs: Unpack[PutAccessGrantsInstanceResourcePolicyRequestRequestTypeDef]
    ) -> PutAccessGrantsInstanceResourcePolicyResultTypeDef:
        """
        Updates the resource policy of the S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/put_access_grants_instance_resource_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#put_access_grants_instance_resource_policy)
        """

    def put_access_point_configuration_for_object_lambda(
        self, **kwargs: Unpack[PutAccessPointConfigurationForObjectLambdaRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/put_access_point_configuration_for_object_lambda.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#put_access_point_configuration_for_object_lambda)
        """

    def put_access_point_policy(
        self, **kwargs: Unpack[PutAccessPointPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/put_access_point_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#put_access_point_policy)
        """

    def put_access_point_policy_for_object_lambda(
        self, **kwargs: Unpack[PutAccessPointPolicyForObjectLambdaRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/put_access_point_policy_for_object_lambda.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#put_access_point_policy_for_object_lambda)
        """

    def put_bucket_lifecycle_configuration(
        self, **kwargs: Unpack[PutBucketLifecycleConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This action puts a lifecycle configuration to an Amazon S3 on Outposts bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/put_bucket_lifecycle_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#put_bucket_lifecycle_configuration)
        """

    def put_bucket_policy(
        self, **kwargs: Unpack[PutBucketPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This action puts a bucket policy to an Amazon S3 on Outposts bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/put_bucket_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#put_bucket_policy)
        """

    def put_bucket_replication(
        self, **kwargs: Unpack[PutBucketReplicationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This action creates an Amazon S3 on Outposts bucket's replication configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/put_bucket_replication.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#put_bucket_replication)
        """

    def put_bucket_tagging(
        self, **kwargs: Unpack[PutBucketTaggingRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This action puts tags on an Amazon S3 on Outposts bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/put_bucket_tagging.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#put_bucket_tagging)
        """

    def put_bucket_versioning(
        self, **kwargs: Unpack[PutBucketVersioningRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation sets the versioning state for S3 on Outposts buckets only.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/put_bucket_versioning.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#put_bucket_versioning)
        """

    def put_job_tagging(
        self, **kwargs: Unpack[PutJobTaggingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets the supplied tag-set on an S3 Batch Operations job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/put_job_tagging.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#put_job_tagging)
        """

    def put_multi_region_access_point_policy(
        self, **kwargs: Unpack[PutMultiRegionAccessPointPolicyRequestRequestTypeDef]
    ) -> PutMultiRegionAccessPointPolicyResultTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/put_multi_region_access_point_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#put_multi_region_access_point_policy)
        """

    def put_public_access_block(
        self, **kwargs: Unpack[PutPublicAccessBlockRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/put_public_access_block.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#put_public_access_block)
        """

    def put_storage_lens_configuration(
        self, **kwargs: Unpack[PutStorageLensConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/put_storage_lens_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#put_storage_lens_configuration)
        """

    def put_storage_lens_configuration_tagging(
        self, **kwargs: Unpack[PutStorageLensConfigurationTaggingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/put_storage_lens_configuration_tagging.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#put_storage_lens_configuration_tagging)
        """

    def submit_multi_region_access_point_routes(
        self, **kwargs: Unpack[SubmitMultiRegionAccessPointRoutesRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This operation is not supported by directory buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/submit_multi_region_access_point_routes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#submit_multi_region_access_point_routes)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Creates a new Amazon Web Services resource tag or updates an existing resource
        tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This operation removes the specified Amazon Web Services resource tags from an
        S3 resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#untag_resource)
        """

    def update_access_grants_location(
        self, **kwargs: Unpack[UpdateAccessGrantsLocationRequestRequestTypeDef]
    ) -> UpdateAccessGrantsLocationResultTypeDef:
        """
        Updates the IAM role of a registered location in your S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/update_access_grants_location.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#update_access_grants_location)
        """

    def update_job_priority(
        self, **kwargs: Unpack[UpdateJobPriorityRequestRequestTypeDef]
    ) -> UpdateJobPriorityResultTypeDef:
        """
        Updates an existing S3 Batch Operations job's priority.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/update_job_priority.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#update_job_priority)
        """

    def update_job_status(
        self, **kwargs: Unpack[UpdateJobStatusRequestRequestTypeDef]
    ) -> UpdateJobStatusResultTypeDef:
        """
        Updates the status for the specified job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/update_job_status.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#update_job_status)
        """

    def update_storage_lens_group(
        self, **kwargs: Unpack[UpdateStorageLensGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the existing Storage Lens group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/update_storage_lens_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#update_storage_lens_group)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_access_points_for_object_lambda"]
    ) -> ListAccessPointsForObjectLambdaPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_caller_access_grants"]
    ) -> ListCallerAccessGrantsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/client/#get_paginator)
        """
