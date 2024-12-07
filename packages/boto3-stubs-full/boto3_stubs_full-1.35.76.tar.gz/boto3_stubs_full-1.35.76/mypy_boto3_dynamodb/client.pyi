"""
Type annotations for dynamodb service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_dynamodb.client import DynamoDBClient

    session = Session()
    client: DynamoDBClient = session.client("dynamodb")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListBackupsPaginator,
    ListTablesPaginator,
    ListTagsOfResourcePaginator,
    QueryPaginator,
    ScanPaginator,
)
from .type_defs import (
    BatchExecuteStatementInputRequestTypeDef,
    BatchExecuteStatementOutputTypeDef,
    BatchGetItemInputRequestTypeDef,
    BatchGetItemOutputTypeDef,
    BatchWriteItemInputRequestTypeDef,
    BatchWriteItemOutputTypeDef,
    CreateBackupInputRequestTypeDef,
    CreateBackupOutputTypeDef,
    CreateGlobalTableInputRequestTypeDef,
    CreateGlobalTableOutputTypeDef,
    CreateTableInputRequestTypeDef,
    CreateTableOutputTypeDef,
    DeleteBackupInputRequestTypeDef,
    DeleteBackupOutputTypeDef,
    DeleteItemInputRequestTypeDef,
    DeleteItemOutputTypeDef,
    DeleteResourcePolicyInputRequestTypeDef,
    DeleteResourcePolicyOutputTypeDef,
    DeleteTableInputRequestTypeDef,
    DeleteTableOutputTypeDef,
    DescribeBackupInputRequestTypeDef,
    DescribeBackupOutputTypeDef,
    DescribeContinuousBackupsInputRequestTypeDef,
    DescribeContinuousBackupsOutputTypeDef,
    DescribeContributorInsightsInputRequestTypeDef,
    DescribeContributorInsightsOutputTypeDef,
    DescribeEndpointsResponseTypeDef,
    DescribeExportInputRequestTypeDef,
    DescribeExportOutputTypeDef,
    DescribeGlobalTableInputRequestTypeDef,
    DescribeGlobalTableOutputTypeDef,
    DescribeGlobalTableSettingsInputRequestTypeDef,
    DescribeGlobalTableSettingsOutputTypeDef,
    DescribeImportInputRequestTypeDef,
    DescribeImportOutputTypeDef,
    DescribeKinesisStreamingDestinationInputRequestTypeDef,
    DescribeKinesisStreamingDestinationOutputTypeDef,
    DescribeLimitsOutputTypeDef,
    DescribeTableInputRequestTypeDef,
    DescribeTableOutputTypeDef,
    DescribeTableReplicaAutoScalingInputRequestTypeDef,
    DescribeTableReplicaAutoScalingOutputTypeDef,
    DescribeTimeToLiveInputRequestTypeDef,
    DescribeTimeToLiveOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    ExecuteStatementInputRequestTypeDef,
    ExecuteStatementOutputTypeDef,
    ExecuteTransactionInputRequestTypeDef,
    ExecuteTransactionOutputTypeDef,
    ExportTableToPointInTimeInputRequestTypeDef,
    ExportTableToPointInTimeOutputTypeDef,
    GetItemInputRequestTypeDef,
    GetItemOutputTypeDef,
    GetResourcePolicyInputRequestTypeDef,
    GetResourcePolicyOutputTypeDef,
    ImportTableInputRequestTypeDef,
    ImportTableOutputTypeDef,
    KinesisStreamingDestinationInputRequestTypeDef,
    KinesisStreamingDestinationOutputTypeDef,
    ListBackupsInputRequestTypeDef,
    ListBackupsOutputTypeDef,
    ListContributorInsightsInputRequestTypeDef,
    ListContributorInsightsOutputTypeDef,
    ListExportsInputRequestTypeDef,
    ListExportsOutputTypeDef,
    ListGlobalTablesInputRequestTypeDef,
    ListGlobalTablesOutputTypeDef,
    ListImportsInputRequestTypeDef,
    ListImportsOutputTypeDef,
    ListTablesInputRequestTypeDef,
    ListTablesOutputTypeDef,
    ListTagsOfResourceInputRequestTypeDef,
    ListTagsOfResourceOutputTypeDef,
    PutItemInputRequestTypeDef,
    PutItemOutputTypeDef,
    PutResourcePolicyInputRequestTypeDef,
    PutResourcePolicyOutputTypeDef,
    QueryInputRequestTypeDef,
    QueryOutputTypeDef,
    RestoreTableFromBackupInputRequestTypeDef,
    RestoreTableFromBackupOutputTypeDef,
    RestoreTableToPointInTimeInputRequestTypeDef,
    RestoreTableToPointInTimeOutputTypeDef,
    ScanInputRequestTypeDef,
    ScanOutputTypeDef,
    TagResourceInputRequestTypeDef,
    TransactGetItemsInputRequestTypeDef,
    TransactGetItemsOutputTypeDef,
    TransactWriteItemsInputRequestTypeDef,
    TransactWriteItemsOutputTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateContinuousBackupsInputRequestTypeDef,
    UpdateContinuousBackupsOutputTypeDef,
    UpdateContributorInsightsInputRequestTypeDef,
    UpdateContributorInsightsOutputTypeDef,
    UpdateGlobalTableInputRequestTypeDef,
    UpdateGlobalTableOutputTypeDef,
    UpdateGlobalTableSettingsInputRequestTypeDef,
    UpdateGlobalTableSettingsOutputTypeDef,
    UpdateItemInputRequestTypeDef,
    UpdateItemOutputTypeDef,
    UpdateKinesisStreamingDestinationInputRequestTypeDef,
    UpdateKinesisStreamingDestinationOutputTypeDef,
    UpdateTableInputRequestTypeDef,
    UpdateTableOutputTypeDef,
    UpdateTableReplicaAutoScalingInputRequestTypeDef,
    UpdateTableReplicaAutoScalingOutputTypeDef,
    UpdateTimeToLiveInputRequestTypeDef,
    UpdateTimeToLiveOutputTypeDef,
)
from .waiter import TableExistsWaiter, TableNotExistsWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("DynamoDBClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BackupInUseException: Type[BotocoreClientError]
    BackupNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConditionalCheckFailedException: Type[BotocoreClientError]
    ContinuousBackupsUnavailableException: Type[BotocoreClientError]
    DuplicateItemException: Type[BotocoreClientError]
    ExportConflictException: Type[BotocoreClientError]
    ExportNotFoundException: Type[BotocoreClientError]
    GlobalTableAlreadyExistsException: Type[BotocoreClientError]
    GlobalTableNotFoundException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    ImportConflictException: Type[BotocoreClientError]
    ImportNotFoundException: Type[BotocoreClientError]
    IndexNotFoundException: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InvalidExportTimeException: Type[BotocoreClientError]
    InvalidRestoreTimeException: Type[BotocoreClientError]
    ItemCollectionSizeLimitExceededException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    PointInTimeRecoveryUnavailableException: Type[BotocoreClientError]
    PolicyNotFoundException: Type[BotocoreClientError]
    ProvisionedThroughputExceededException: Type[BotocoreClientError]
    ReplicaAlreadyExistsException: Type[BotocoreClientError]
    ReplicaNotFoundException: Type[BotocoreClientError]
    ReplicatedWriteConflictException: Type[BotocoreClientError]
    RequestLimitExceeded: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TableAlreadyExistsException: Type[BotocoreClientError]
    TableInUseException: Type[BotocoreClientError]
    TableNotFoundException: Type[BotocoreClientError]
    TransactionCanceledException: Type[BotocoreClientError]
    TransactionConflictException: Type[BotocoreClientError]
    TransactionInProgressException: Type[BotocoreClientError]

class DynamoDBClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DynamoDBClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#close)
        """

    def batch_execute_statement(
        self, **kwargs: Unpack[BatchExecuteStatementInputRequestTypeDef]
    ) -> BatchExecuteStatementOutputTypeDef:
        """
        This operation allows you to perform batch reads or writes on data stored in
        DynamoDB, using PartiQL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/batch_execute_statement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#batch_execute_statement)
        """

    def batch_get_item(
        self, **kwargs: Unpack[BatchGetItemInputRequestTypeDef]
    ) -> BatchGetItemOutputTypeDef:
        """
        The <code>BatchGetItem</code> operation returns the attributes of one or more
        items from one or more tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/batch_get_item.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#batch_get_item)
        """

    def batch_write_item(
        self, **kwargs: Unpack[BatchWriteItemInputRequestTypeDef]
    ) -> BatchWriteItemOutputTypeDef:
        """
        The <code>BatchWriteItem</code> operation puts or deletes multiple items in one
        or more tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/batch_write_item.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#batch_write_item)
        """

    def create_backup(
        self, **kwargs: Unpack[CreateBackupInputRequestTypeDef]
    ) -> CreateBackupOutputTypeDef:
        """
        Creates a backup for an existing table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/create_backup.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#create_backup)
        """

    def create_global_table(
        self, **kwargs: Unpack[CreateGlobalTableInputRequestTypeDef]
    ) -> CreateGlobalTableOutputTypeDef:
        """
        Creates a global table from an existing table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/create_global_table.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#create_global_table)
        """

    def create_table(
        self, **kwargs: Unpack[CreateTableInputRequestTypeDef]
    ) -> CreateTableOutputTypeDef:
        """
        The <code>CreateTable</code> operation adds a new table to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/create_table.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#create_table)
        """

    def delete_backup(
        self, **kwargs: Unpack[DeleteBackupInputRequestTypeDef]
    ) -> DeleteBackupOutputTypeDef:
        """
        Deletes an existing backup of a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/delete_backup.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#delete_backup)
        """

    def delete_item(
        self, **kwargs: Unpack[DeleteItemInputRequestTypeDef]
    ) -> DeleteItemOutputTypeDef:
        """
        Deletes a single item in a table by primary key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/delete_item.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#delete_item)
        """

    def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyInputRequestTypeDef]
    ) -> DeleteResourcePolicyOutputTypeDef:
        """
        Deletes the resource-based policy attached to the resource, which can be a
        table or stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/delete_resource_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#delete_resource_policy)
        """

    def delete_table(
        self, **kwargs: Unpack[DeleteTableInputRequestTypeDef]
    ) -> DeleteTableOutputTypeDef:
        """
        The <code>DeleteTable</code> operation deletes a table and all of its items.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/delete_table.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#delete_table)
        """

    def describe_backup(
        self, **kwargs: Unpack[DescribeBackupInputRequestTypeDef]
    ) -> DescribeBackupOutputTypeDef:
        """
        Describes an existing backup of a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/describe_backup.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#describe_backup)
        """

    def describe_continuous_backups(
        self, **kwargs: Unpack[DescribeContinuousBackupsInputRequestTypeDef]
    ) -> DescribeContinuousBackupsOutputTypeDef:
        """
        Checks the status of continuous backups and point in time recovery on the
        specified table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/describe_continuous_backups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#describe_continuous_backups)
        """

    def describe_contributor_insights(
        self, **kwargs: Unpack[DescribeContributorInsightsInputRequestTypeDef]
    ) -> DescribeContributorInsightsOutputTypeDef:
        """
        Returns information about contributor insights for a given table or global
        secondary index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/describe_contributor_insights.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#describe_contributor_insights)
        """

    def describe_endpoints(self) -> DescribeEndpointsResponseTypeDef:
        """
        Returns the regional endpoint information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/describe_endpoints.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#describe_endpoints)
        """

    def describe_export(
        self, **kwargs: Unpack[DescribeExportInputRequestTypeDef]
    ) -> DescribeExportOutputTypeDef:
        """
        Describes an existing table export.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/describe_export.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#describe_export)
        """

    def describe_global_table(
        self, **kwargs: Unpack[DescribeGlobalTableInputRequestTypeDef]
    ) -> DescribeGlobalTableOutputTypeDef:
        """
        Returns information about the specified global table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/describe_global_table.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#describe_global_table)
        """

    def describe_global_table_settings(
        self, **kwargs: Unpack[DescribeGlobalTableSettingsInputRequestTypeDef]
    ) -> DescribeGlobalTableSettingsOutputTypeDef:
        """
        Describes Region-specific settings for a global table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/describe_global_table_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#describe_global_table_settings)
        """

    def describe_import(
        self, **kwargs: Unpack[DescribeImportInputRequestTypeDef]
    ) -> DescribeImportOutputTypeDef:
        """
        Represents the properties of the import.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/describe_import.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#describe_import)
        """

    def describe_kinesis_streaming_destination(
        self, **kwargs: Unpack[DescribeKinesisStreamingDestinationInputRequestTypeDef]
    ) -> DescribeKinesisStreamingDestinationOutputTypeDef:
        """
        Returns information about the status of Kinesis streaming.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/describe_kinesis_streaming_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#describe_kinesis_streaming_destination)
        """

    def describe_limits(self) -> DescribeLimitsOutputTypeDef:
        """
        Returns the current provisioned-capacity quotas for your Amazon Web Services
        account in a Region, both for the Region as a whole and for any one DynamoDB
        table that you create there.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/describe_limits.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#describe_limits)
        """

    def describe_table(
        self, **kwargs: Unpack[DescribeTableInputRequestTypeDef]
    ) -> DescribeTableOutputTypeDef:
        """
        Returns information about the table, including the current status of the table,
        when it was created, the primary key schema, and any indexes on the table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/describe_table.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#describe_table)
        """

    def describe_table_replica_auto_scaling(
        self, **kwargs: Unpack[DescribeTableReplicaAutoScalingInputRequestTypeDef]
    ) -> DescribeTableReplicaAutoScalingOutputTypeDef:
        """
        Describes auto scaling settings across replicas of the global table at once.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/describe_table_replica_auto_scaling.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#describe_table_replica_auto_scaling)
        """

    def describe_time_to_live(
        self, **kwargs: Unpack[DescribeTimeToLiveInputRequestTypeDef]
    ) -> DescribeTimeToLiveOutputTypeDef:
        """
        Gives a description of the Time to Live (TTL) status on the specified table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/describe_time_to_live.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#describe_time_to_live)
        """

    def disable_kinesis_streaming_destination(
        self, **kwargs: Unpack[KinesisStreamingDestinationInputRequestTypeDef]
    ) -> KinesisStreamingDestinationOutputTypeDef:
        """
        Stops replication from the DynamoDB table to the Kinesis data stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/disable_kinesis_streaming_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#disable_kinesis_streaming_destination)
        """

    def enable_kinesis_streaming_destination(
        self, **kwargs: Unpack[KinesisStreamingDestinationInputRequestTypeDef]
    ) -> KinesisStreamingDestinationOutputTypeDef:
        """
        Starts table data replication to the specified Kinesis data stream at a
        timestamp chosen during the enable workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/enable_kinesis_streaming_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#enable_kinesis_streaming_destination)
        """

    def execute_statement(
        self, **kwargs: Unpack[ExecuteStatementInputRequestTypeDef]
    ) -> ExecuteStatementOutputTypeDef:
        """
        This operation allows you to perform reads and singleton writes on data stored
        in DynamoDB, using PartiQL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/execute_statement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#execute_statement)
        """

    def execute_transaction(
        self, **kwargs: Unpack[ExecuteTransactionInputRequestTypeDef]
    ) -> ExecuteTransactionOutputTypeDef:
        """
        This operation allows you to perform transactional reads or writes on data
        stored in DynamoDB, using PartiQL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/execute_transaction.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#execute_transaction)
        """

    def export_table_to_point_in_time(
        self, **kwargs: Unpack[ExportTableToPointInTimeInputRequestTypeDef]
    ) -> ExportTableToPointInTimeOutputTypeDef:
        """
        Exports table data to an S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/export_table_to_point_in_time.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#export_table_to_point_in_time)
        """

    def get_item(self, **kwargs: Unpack[GetItemInputRequestTypeDef]) -> GetItemOutputTypeDef:
        """
        The <code>GetItem</code> operation returns a set of attributes for the item
        with the given primary key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/get_item.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#get_item)
        """

    def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyInputRequestTypeDef]
    ) -> GetResourcePolicyOutputTypeDef:
        """
        Returns the resource-based policy document attached to the resource, which can
        be a table or stream, in JSON format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/get_resource_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#get_resource_policy)
        """

    def import_table(
        self, **kwargs: Unpack[ImportTableInputRequestTypeDef]
    ) -> ImportTableOutputTypeDef:
        """
        Imports table data from an S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/import_table.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#import_table)
        """

    def list_backups(
        self, **kwargs: Unpack[ListBackupsInputRequestTypeDef]
    ) -> ListBackupsOutputTypeDef:
        """
        List DynamoDB backups that are associated with an Amazon Web Services account
        and weren't made with Amazon Web Services Backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/list_backups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#list_backups)
        """

    def list_contributor_insights(
        self, **kwargs: Unpack[ListContributorInsightsInputRequestTypeDef]
    ) -> ListContributorInsightsOutputTypeDef:
        """
        Returns a list of ContributorInsightsSummary for a table and all its global
        secondary indexes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/list_contributor_insights.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#list_contributor_insights)
        """

    def list_exports(
        self, **kwargs: Unpack[ListExportsInputRequestTypeDef]
    ) -> ListExportsOutputTypeDef:
        """
        Lists completed exports within the past 90 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/list_exports.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#list_exports)
        """

    def list_global_tables(
        self, **kwargs: Unpack[ListGlobalTablesInputRequestTypeDef]
    ) -> ListGlobalTablesOutputTypeDef:
        """
        Lists all global tables that have a replica in the specified Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/list_global_tables.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#list_global_tables)
        """

    def list_imports(
        self, **kwargs: Unpack[ListImportsInputRequestTypeDef]
    ) -> ListImportsOutputTypeDef:
        """
        Lists completed imports within the past 90 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/list_imports.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#list_imports)
        """

    def list_tables(
        self, **kwargs: Unpack[ListTablesInputRequestTypeDef]
    ) -> ListTablesOutputTypeDef:
        """
        Returns an array of table names associated with the current account and
        endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/list_tables.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#list_tables)
        """

    def list_tags_of_resource(
        self, **kwargs: Unpack[ListTagsOfResourceInputRequestTypeDef]
    ) -> ListTagsOfResourceOutputTypeDef:
        """
        List all tags on an Amazon DynamoDB resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/list_tags_of_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#list_tags_of_resource)
        """

    def put_item(self, **kwargs: Unpack[PutItemInputRequestTypeDef]) -> PutItemOutputTypeDef:
        """
        Creates a new item, or replaces an old item with a new item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/put_item.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#put_item)
        """

    def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyInputRequestTypeDef]
    ) -> PutResourcePolicyOutputTypeDef:
        """
        Attaches a resource-based policy document to the resource, which can be a table
        or stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/put_resource_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#put_resource_policy)
        """

    def query(self, **kwargs: Unpack[QueryInputRequestTypeDef]) -> QueryOutputTypeDef:
        """
        You must provide the name of the partition key attribute and a single value for
        that attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/query.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#query)
        """

    def restore_table_from_backup(
        self, **kwargs: Unpack[RestoreTableFromBackupInputRequestTypeDef]
    ) -> RestoreTableFromBackupOutputTypeDef:
        """
        Creates a new table from an existing backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/restore_table_from_backup.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#restore_table_from_backup)
        """

    def restore_table_to_point_in_time(
        self, **kwargs: Unpack[RestoreTableToPointInTimeInputRequestTypeDef]
    ) -> RestoreTableToPointInTimeOutputTypeDef:
        """
        Restores the specified table to the specified point in time within
        <code>EarliestRestorableDateTime</code> and
        <code>LatestRestorableDateTime</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/restore_table_to_point_in_time.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#restore_table_to_point_in_time)
        """

    def scan(self, **kwargs: Unpack[ScanInputRequestTypeDef]) -> ScanOutputTypeDef:
        """
        The <code>Scan</code> operation returns one or more items and item attributes
        by accessing every item in a table or a secondary index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/scan.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#scan)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associate a set of tags with an Amazon DynamoDB resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#tag_resource)
        """

    def transact_get_items(
        self, **kwargs: Unpack[TransactGetItemsInputRequestTypeDef]
    ) -> TransactGetItemsOutputTypeDef:
        """
        <code>TransactGetItems</code> is a synchronous operation that atomically
        retrieves multiple items from one or more tables (but not from indexes) in a
        single account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/transact_get_items.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#transact_get_items)
        """

    def transact_write_items(
        self, **kwargs: Unpack[TransactWriteItemsInputRequestTypeDef]
    ) -> TransactWriteItemsOutputTypeDef:
        """
        <code>TransactWriteItems</code> is a synchronous write operation that groups up
        to 100 action requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/transact_write_items.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#transact_write_items)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the association of tags from an Amazon DynamoDB resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#untag_resource)
        """

    def update_continuous_backups(
        self, **kwargs: Unpack[UpdateContinuousBackupsInputRequestTypeDef]
    ) -> UpdateContinuousBackupsOutputTypeDef:
        """
        <code>UpdateContinuousBackups</code> enables or disables point in time recovery
        for the specified table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/update_continuous_backups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#update_continuous_backups)
        """

    def update_contributor_insights(
        self, **kwargs: Unpack[UpdateContributorInsightsInputRequestTypeDef]
    ) -> UpdateContributorInsightsOutputTypeDef:
        """
        Updates the status for contributor insights for a specific table or index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/update_contributor_insights.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#update_contributor_insights)
        """

    def update_global_table(
        self, **kwargs: Unpack[UpdateGlobalTableInputRequestTypeDef]
    ) -> UpdateGlobalTableOutputTypeDef:
        """
        Adds or removes replicas in the specified global table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/update_global_table.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#update_global_table)
        """

    def update_global_table_settings(
        self, **kwargs: Unpack[UpdateGlobalTableSettingsInputRequestTypeDef]
    ) -> UpdateGlobalTableSettingsOutputTypeDef:
        """
        Updates settings for a global table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/update_global_table_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#update_global_table_settings)
        """

    def update_item(
        self, **kwargs: Unpack[UpdateItemInputRequestTypeDef]
    ) -> UpdateItemOutputTypeDef:
        """
        Edits an existing item's attributes, or adds a new item to the table if it does
        not already exist.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/update_item.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#update_item)
        """

    def update_kinesis_streaming_destination(
        self, **kwargs: Unpack[UpdateKinesisStreamingDestinationInputRequestTypeDef]
    ) -> UpdateKinesisStreamingDestinationOutputTypeDef:
        """
        The command to update the Kinesis stream destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/update_kinesis_streaming_destination.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#update_kinesis_streaming_destination)
        """

    def update_table(
        self, **kwargs: Unpack[UpdateTableInputRequestTypeDef]
    ) -> UpdateTableOutputTypeDef:
        """
        Modifies the provisioned throughput settings, global secondary indexes, or
        DynamoDB Streams settings for a given table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/update_table.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#update_table)
        """

    def update_table_replica_auto_scaling(
        self, **kwargs: Unpack[UpdateTableReplicaAutoScalingInputRequestTypeDef]
    ) -> UpdateTableReplicaAutoScalingOutputTypeDef:
        """
        Updates auto scaling settings on your global tables at once.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/update_table_replica_auto_scaling.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#update_table_replica_auto_scaling)
        """

    def update_time_to_live(
        self, **kwargs: Unpack[UpdateTimeToLiveInputRequestTypeDef]
    ) -> UpdateTimeToLiveOutputTypeDef:
        """
        The <code>UpdateTimeToLive</code> method enables or disables Time to Live (TTL)
        for the specified table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/update_time_to_live.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#update_time_to_live)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_backups"]) -> ListBackupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tables"]) -> ListTablesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_of_resource"]
    ) -> ListTagsOfResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["query"]) -> QueryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["scan"]) -> ScanPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["table_exists"]) -> TableExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["table_not_exists"]) -> TableNotExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/client/#get_waiter)
        """
