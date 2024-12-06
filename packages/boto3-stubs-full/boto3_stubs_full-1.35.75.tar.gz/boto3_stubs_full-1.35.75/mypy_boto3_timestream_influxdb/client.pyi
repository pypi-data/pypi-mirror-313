"""
Type annotations for timestream-influxdb service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_timestream_influxdb.client import TimestreamInfluxDBClient

    session = Session()
    client: TimestreamInfluxDBClient = session.client("timestream-influxdb")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import ListDbInstancesPaginator, ListDbParameterGroupsPaginator
from .type_defs import (
    CreateDbInstanceInputRequestTypeDef,
    CreateDbInstanceOutputTypeDef,
    CreateDbParameterGroupInputRequestTypeDef,
    CreateDbParameterGroupOutputTypeDef,
    DeleteDbInstanceInputRequestTypeDef,
    DeleteDbInstanceOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetDbInstanceInputRequestTypeDef,
    GetDbInstanceOutputTypeDef,
    GetDbParameterGroupInputRequestTypeDef,
    GetDbParameterGroupOutputTypeDef,
    ListDbInstancesInputRequestTypeDef,
    ListDbInstancesOutputTypeDef,
    ListDbParameterGroupsInputRequestTypeDef,
    ListDbParameterGroupsOutputTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDbInstanceInputRequestTypeDef,
    UpdateDbInstanceOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("TimestreamInfluxDBClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class TimestreamInfluxDBClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TimestreamInfluxDBClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#close)
        """

    def create_db_instance(
        self, **kwargs: Unpack[CreateDbInstanceInputRequestTypeDef]
    ) -> CreateDbInstanceOutputTypeDef:
        """
        Creates a new Timestream for InfluxDB DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/client/create_db_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#create_db_instance)
        """

    def create_db_parameter_group(
        self, **kwargs: Unpack[CreateDbParameterGroupInputRequestTypeDef]
    ) -> CreateDbParameterGroupOutputTypeDef:
        """
        Creates a new Timestream for InfluxDB DB parameter group to associate with DB
        instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/client/create_db_parameter_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#create_db_parameter_group)
        """

    def delete_db_instance(
        self, **kwargs: Unpack[DeleteDbInstanceInputRequestTypeDef]
    ) -> DeleteDbInstanceOutputTypeDef:
        """
        Deletes a Timestream for InfluxDB DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/client/delete_db_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#delete_db_instance)
        """

    def get_db_instance(
        self, **kwargs: Unpack[GetDbInstanceInputRequestTypeDef]
    ) -> GetDbInstanceOutputTypeDef:
        """
        Returns a Timestream for InfluxDB DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/client/get_db_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#get_db_instance)
        """

    def get_db_parameter_group(
        self, **kwargs: Unpack[GetDbParameterGroupInputRequestTypeDef]
    ) -> GetDbParameterGroupOutputTypeDef:
        """
        Returns a Timestream for InfluxDB DB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/client/get_db_parameter_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#get_db_parameter_group)
        """

    def list_db_instances(
        self, **kwargs: Unpack[ListDbInstancesInputRequestTypeDef]
    ) -> ListDbInstancesOutputTypeDef:
        """
        Returns a list of Timestream for InfluxDB DB instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/client/list_db_instances.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#list_db_instances)
        """

    def list_db_parameter_groups(
        self, **kwargs: Unpack[ListDbParameterGroupsInputRequestTypeDef]
    ) -> ListDbParameterGroupsOutputTypeDef:
        """
        Returns a list of Timestream for InfluxDB DB parameter groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/client/list_db_parameter_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#list_db_parameter_groups)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        A list of tags applied to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#list_tags_for_resource)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Tags are composed of a Key/Value pairs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the tag from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#untag_resource)
        """

    def update_db_instance(
        self, **kwargs: Unpack[UpdateDbInstanceInputRequestTypeDef]
    ) -> UpdateDbInstanceOutputTypeDef:
        """
        Updates a Timestream for InfluxDB DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/client/update_db_instance.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#update_db_instance)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_db_instances"]
    ) -> ListDbInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_db_parameter_groups"]
    ) -> ListDbParameterGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/client/#get_paginator)
        """
