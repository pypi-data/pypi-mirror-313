"""
Type annotations for kinesisanalyticsv2 service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kinesisanalyticsv2.client import KinesisAnalyticsV2Client

    session = Session()
    client: KinesisAnalyticsV2Client = session.client("kinesisanalyticsv2")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListApplicationOperationsPaginator,
    ListApplicationSnapshotsPaginator,
    ListApplicationsPaginator,
    ListApplicationVersionsPaginator,
)
from .type_defs import (
    AddApplicationCloudWatchLoggingOptionRequestRequestTypeDef,
    AddApplicationCloudWatchLoggingOptionResponseTypeDef,
    AddApplicationInputProcessingConfigurationRequestRequestTypeDef,
    AddApplicationInputProcessingConfigurationResponseTypeDef,
    AddApplicationInputRequestRequestTypeDef,
    AddApplicationInputResponseTypeDef,
    AddApplicationOutputRequestRequestTypeDef,
    AddApplicationOutputResponseTypeDef,
    AddApplicationReferenceDataSourceRequestRequestTypeDef,
    AddApplicationReferenceDataSourceResponseTypeDef,
    AddApplicationVpcConfigurationRequestRequestTypeDef,
    AddApplicationVpcConfigurationResponseTypeDef,
    CreateApplicationPresignedUrlRequestRequestTypeDef,
    CreateApplicationPresignedUrlResponseTypeDef,
    CreateApplicationRequestRequestTypeDef,
    CreateApplicationResponseTypeDef,
    CreateApplicationSnapshotRequestRequestTypeDef,
    DeleteApplicationCloudWatchLoggingOptionRequestRequestTypeDef,
    DeleteApplicationCloudWatchLoggingOptionResponseTypeDef,
    DeleteApplicationInputProcessingConfigurationRequestRequestTypeDef,
    DeleteApplicationInputProcessingConfigurationResponseTypeDef,
    DeleteApplicationOutputRequestRequestTypeDef,
    DeleteApplicationOutputResponseTypeDef,
    DeleteApplicationReferenceDataSourceRequestRequestTypeDef,
    DeleteApplicationReferenceDataSourceResponseTypeDef,
    DeleteApplicationRequestRequestTypeDef,
    DeleteApplicationSnapshotRequestRequestTypeDef,
    DeleteApplicationVpcConfigurationRequestRequestTypeDef,
    DeleteApplicationVpcConfigurationResponseTypeDef,
    DescribeApplicationOperationRequestRequestTypeDef,
    DescribeApplicationOperationResponseTypeDef,
    DescribeApplicationRequestRequestTypeDef,
    DescribeApplicationResponseTypeDef,
    DescribeApplicationSnapshotRequestRequestTypeDef,
    DescribeApplicationSnapshotResponseTypeDef,
    DescribeApplicationVersionRequestRequestTypeDef,
    DescribeApplicationVersionResponseTypeDef,
    DiscoverInputSchemaRequestRequestTypeDef,
    DiscoverInputSchemaResponseTypeDef,
    ListApplicationOperationsRequestRequestTypeDef,
    ListApplicationOperationsResponseTypeDef,
    ListApplicationSnapshotsRequestRequestTypeDef,
    ListApplicationSnapshotsResponseTypeDef,
    ListApplicationsRequestRequestTypeDef,
    ListApplicationsResponseTypeDef,
    ListApplicationVersionsRequestRequestTypeDef,
    ListApplicationVersionsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RollbackApplicationRequestRequestTypeDef,
    RollbackApplicationResponseTypeDef,
    StartApplicationRequestRequestTypeDef,
    StartApplicationResponseTypeDef,
    StopApplicationRequestRequestTypeDef,
    StopApplicationResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateApplicationMaintenanceConfigurationRequestRequestTypeDef,
    UpdateApplicationMaintenanceConfigurationResponseTypeDef,
    UpdateApplicationRequestRequestTypeDef,
    UpdateApplicationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("KinesisAnalyticsV2Client",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    CodeValidationException: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    InvalidApplicationConfigurationException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceProvisionedThroughputExceededException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnableToDetectSchemaException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]


class KinesisAnalyticsV2Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KinesisAnalyticsV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#close)
        """

    def add_application_cloud_watch_logging_option(
        self, **kwargs: Unpack[AddApplicationCloudWatchLoggingOptionRequestRequestTypeDef]
    ) -> AddApplicationCloudWatchLoggingOptionResponseTypeDef:
        """
        Adds an Amazon CloudWatch log stream to monitor application configuration
        errors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/add_application_cloud_watch_logging_option.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#add_application_cloud_watch_logging_option)
        """

    def add_application_input(
        self, **kwargs: Unpack[AddApplicationInputRequestRequestTypeDef]
    ) -> AddApplicationInputResponseTypeDef:
        """
        Adds a streaming source to your SQL-based Kinesis Data Analytics application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/add_application_input.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#add_application_input)
        """

    def add_application_input_processing_configuration(
        self, **kwargs: Unpack[AddApplicationInputProcessingConfigurationRequestRequestTypeDef]
    ) -> AddApplicationInputProcessingConfigurationResponseTypeDef:
        """
        Adds an <a>InputProcessingConfiguration</a> to a SQL-based Kinesis Data
        Analytics application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/add_application_input_processing_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#add_application_input_processing_configuration)
        """

    def add_application_output(
        self, **kwargs: Unpack[AddApplicationOutputRequestRequestTypeDef]
    ) -> AddApplicationOutputResponseTypeDef:
        """
        Adds an external destination to your SQL-based Kinesis Data Analytics
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/add_application_output.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#add_application_output)
        """

    def add_application_reference_data_source(
        self, **kwargs: Unpack[AddApplicationReferenceDataSourceRequestRequestTypeDef]
    ) -> AddApplicationReferenceDataSourceResponseTypeDef:
        """
        Adds a reference data source to an existing SQL-based Kinesis Data Analytics
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/add_application_reference_data_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#add_application_reference_data_source)
        """

    def add_application_vpc_configuration(
        self, **kwargs: Unpack[AddApplicationVpcConfigurationRequestRequestTypeDef]
    ) -> AddApplicationVpcConfigurationResponseTypeDef:
        """
        Adds a Virtual Private Cloud (VPC) configuration to the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/add_application_vpc_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#add_application_vpc_configuration)
        """

    def create_application(
        self, **kwargs: Unpack[CreateApplicationRequestRequestTypeDef]
    ) -> CreateApplicationResponseTypeDef:
        """
        Creates a Managed Service for Apache Flink application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/create_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#create_application)
        """

    def create_application_presigned_url(
        self, **kwargs: Unpack[CreateApplicationPresignedUrlRequestRequestTypeDef]
    ) -> CreateApplicationPresignedUrlResponseTypeDef:
        """
        Creates and returns a URL that you can use to connect to an application's
        extension.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/create_application_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#create_application_presigned_url)
        """

    def create_application_snapshot(
        self, **kwargs: Unpack[CreateApplicationSnapshotRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a snapshot of the application's state data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/create_application_snapshot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#create_application_snapshot)
        """

    def delete_application(
        self, **kwargs: Unpack[DeleteApplicationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/delete_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#delete_application)
        """

    def delete_application_cloud_watch_logging_option(
        self, **kwargs: Unpack[DeleteApplicationCloudWatchLoggingOptionRequestRequestTypeDef]
    ) -> DeleteApplicationCloudWatchLoggingOptionResponseTypeDef:
        """
        Deletes an Amazon CloudWatch log stream from an SQL-based Kinesis Data
        Analytics application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/delete_application_cloud_watch_logging_option.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#delete_application_cloud_watch_logging_option)
        """

    def delete_application_input_processing_configuration(
        self, **kwargs: Unpack[DeleteApplicationInputProcessingConfigurationRequestRequestTypeDef]
    ) -> DeleteApplicationInputProcessingConfigurationResponseTypeDef:
        """
        Deletes an <a>InputProcessingConfiguration</a> from an input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/delete_application_input_processing_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#delete_application_input_processing_configuration)
        """

    def delete_application_output(
        self, **kwargs: Unpack[DeleteApplicationOutputRequestRequestTypeDef]
    ) -> DeleteApplicationOutputResponseTypeDef:
        """
        Deletes the output destination configuration from your SQL-based Kinesis Data
        Analytics application's configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/delete_application_output.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#delete_application_output)
        """

    def delete_application_reference_data_source(
        self, **kwargs: Unpack[DeleteApplicationReferenceDataSourceRequestRequestTypeDef]
    ) -> DeleteApplicationReferenceDataSourceResponseTypeDef:
        """
        Deletes a reference data source configuration from the specified SQL-based
        Kinesis Data Analytics application's configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/delete_application_reference_data_source.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#delete_application_reference_data_source)
        """

    def delete_application_snapshot(
        self, **kwargs: Unpack[DeleteApplicationSnapshotRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a snapshot of application state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/delete_application_snapshot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#delete_application_snapshot)
        """

    def delete_application_vpc_configuration(
        self, **kwargs: Unpack[DeleteApplicationVpcConfigurationRequestRequestTypeDef]
    ) -> DeleteApplicationVpcConfigurationResponseTypeDef:
        """
        Removes a VPC configuration from a Managed Service for Apache Flink application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/delete_application_vpc_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#delete_application_vpc_configuration)
        """

    def describe_application(
        self, **kwargs: Unpack[DescribeApplicationRequestRequestTypeDef]
    ) -> DescribeApplicationResponseTypeDef:
        """
        Returns information about a specific Managed Service for Apache Flink
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/describe_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#describe_application)
        """

    def describe_application_operation(
        self, **kwargs: Unpack[DescribeApplicationOperationRequestRequestTypeDef]
    ) -> DescribeApplicationOperationResponseTypeDef:
        """
        Returns information about a specific operation performed on a Managed Service
        for Apache Flink application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/describe_application_operation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#describe_application_operation)
        """

    def describe_application_snapshot(
        self, **kwargs: Unpack[DescribeApplicationSnapshotRequestRequestTypeDef]
    ) -> DescribeApplicationSnapshotResponseTypeDef:
        """
        Returns information about a snapshot of application state data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/describe_application_snapshot.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#describe_application_snapshot)
        """

    def describe_application_version(
        self, **kwargs: Unpack[DescribeApplicationVersionRequestRequestTypeDef]
    ) -> DescribeApplicationVersionResponseTypeDef:
        """
        Provides a detailed description of a specified version of the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/describe_application_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#describe_application_version)
        """

    def discover_input_schema(
        self, **kwargs: Unpack[DiscoverInputSchemaRequestRequestTypeDef]
    ) -> DiscoverInputSchemaResponseTypeDef:
        """
        Infers a schema for a SQL-based Kinesis Data Analytics application by
        evaluating sample records on the specified streaming source (Kinesis data
        stream or Kinesis Data Firehose delivery stream) or Amazon S3 object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/discover_input_schema.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#discover_input_schema)
        """

    def list_application_operations(
        self, **kwargs: Unpack[ListApplicationOperationsRequestRequestTypeDef]
    ) -> ListApplicationOperationsResponseTypeDef:
        """
        Lists information about operations performed on a Managed Service for Apache
        Flink application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/list_application_operations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#list_application_operations)
        """

    def list_application_snapshots(
        self, **kwargs: Unpack[ListApplicationSnapshotsRequestRequestTypeDef]
    ) -> ListApplicationSnapshotsResponseTypeDef:
        """
        Lists information about the current application snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/list_application_snapshots.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#list_application_snapshots)
        """

    def list_application_versions(
        self, **kwargs: Unpack[ListApplicationVersionsRequestRequestTypeDef]
    ) -> ListApplicationVersionsResponseTypeDef:
        """
        Lists all the versions for the specified application, including versions that
        were rolled back.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/list_application_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#list_application_versions)
        """

    def list_applications(
        self, **kwargs: Unpack[ListApplicationsRequestRequestTypeDef]
    ) -> ListApplicationsResponseTypeDef:
        """
        Returns a list of Managed Service for Apache Flink applications in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/list_applications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#list_applications)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the list of key-value tags assigned to the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#list_tags_for_resource)
        """

    def rollback_application(
        self, **kwargs: Unpack[RollbackApplicationRequestRequestTypeDef]
    ) -> RollbackApplicationResponseTypeDef:
        """
        Reverts the application to the previous running version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/rollback_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#rollback_application)
        """

    def start_application(
        self, **kwargs: Unpack[StartApplicationRequestRequestTypeDef]
    ) -> StartApplicationResponseTypeDef:
        """
        Starts the specified Managed Service for Apache Flink application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/start_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#start_application)
        """

    def stop_application(
        self, **kwargs: Unpack[StopApplicationRequestRequestTypeDef]
    ) -> StopApplicationResponseTypeDef:
        """
        Stops the application from processing data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/stop_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#stop_application)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more key-value tags to a Managed Service for Apache Flink
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from a Managed Service for Apache Flink application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#untag_resource)
        """

    def update_application(
        self, **kwargs: Unpack[UpdateApplicationRequestRequestTypeDef]
    ) -> UpdateApplicationResponseTypeDef:
        """
        Updates an existing Managed Service for Apache Flink application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/update_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#update_application)
        """

    def update_application_maintenance_configuration(
        self, **kwargs: Unpack[UpdateApplicationMaintenanceConfigurationRequestRequestTypeDef]
    ) -> UpdateApplicationMaintenanceConfigurationResponseTypeDef:
        """
        Updates the maintenance configuration of the Managed Service for Apache Flink
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/update_application_maintenance_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#update_application_maintenance_configuration)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_application_operations"]
    ) -> ListApplicationOperationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_application_snapshots"]
    ) -> ListApplicationSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_application_versions"]
    ) -> ListApplicationVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#get_paginator)
        """
