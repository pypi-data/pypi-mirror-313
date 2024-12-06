"""
Type annotations for cur service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cur.client import CostandUsageReportServiceClient

    session = Session()
    client: CostandUsageReportServiceClient = session.client("cur")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import DescribeReportDefinitionsPaginator
from .type_defs import (
    DeleteReportDefinitionRequestRequestTypeDef,
    DeleteReportDefinitionResponseTypeDef,
    DescribeReportDefinitionsRequestRequestTypeDef,
    DescribeReportDefinitionsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ModifyReportDefinitionRequestRequestTypeDef,
    PutReportDefinitionRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("CostandUsageReportServiceClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    DuplicateReportNameException: Type[BotocoreClientError]
    InternalErrorException: Type[BotocoreClientError]
    ReportLimitReachedException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class CostandUsageReportServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur.html#CostandUsageReportService.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CostandUsageReportServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur.html#CostandUsageReportService.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/client/#close)
        """

    def delete_report_definition(
        self, **kwargs: Unpack[DeleteReportDefinitionRequestRequestTypeDef]
    ) -> DeleteReportDefinitionResponseTypeDef:
        """
        Deletes the specified report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/client/delete_report_definition.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/client/#delete_report_definition)
        """

    def describe_report_definitions(
        self, **kwargs: Unpack[DescribeReportDefinitionsRequestRequestTypeDef]
    ) -> DescribeReportDefinitionsResponseTypeDef:
        """
        Lists the Amazon Web Services Cost and Usage Report available to this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/client/describe_report_definitions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/client/#describe_report_definitions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags associated with the specified report definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/client/#list_tags_for_resource)
        """

    def modify_report_definition(
        self, **kwargs: Unpack[ModifyReportDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Allows you to programmatically update your report preferences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/client/modify_report_definition.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/client/#modify_report_definition)
        """

    def put_report_definition(
        self, **kwargs: Unpack[PutReportDefinitionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a new report using the description that you provide.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/client/put_report_definition.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/client/#put_report_definition)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates a set of tags with a report definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a set of tags from a report definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/client/#untag_resource)
        """

    def get_paginator(
        self, operation_name: Literal["describe_report_definitions"]
    ) -> DescribeReportDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cur/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/client/#get_paginator)
        """
