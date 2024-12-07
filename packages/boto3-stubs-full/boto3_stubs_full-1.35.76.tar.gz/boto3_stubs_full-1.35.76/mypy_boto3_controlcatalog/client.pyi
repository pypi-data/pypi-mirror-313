"""
Type annotations for controlcatalog service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controlcatalog/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_controlcatalog.client import ControlCatalogClient

    session = Session()
    client: ControlCatalogClient = session.client("controlcatalog")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListCommonControlsPaginator,
    ListControlsPaginator,
    ListDomainsPaginator,
    ListObjectivesPaginator,
)
from .type_defs import (
    GetControlRequestRequestTypeDef,
    GetControlResponseTypeDef,
    ListCommonControlsRequestRequestTypeDef,
    ListCommonControlsResponseTypeDef,
    ListControlsRequestRequestTypeDef,
    ListControlsResponseTypeDef,
    ListDomainsRequestRequestTypeDef,
    ListDomainsResponseTypeDef,
    ListObjectivesRequestRequestTypeDef,
    ListObjectivesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ControlCatalogClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class ControlCatalogClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog.html#ControlCatalog.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controlcatalog/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ControlCatalogClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog.html#ControlCatalog.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controlcatalog/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controlcatalog/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controlcatalog/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controlcatalog/client/#close)
        """

    def get_control(
        self, **kwargs: Unpack[GetControlRequestRequestTypeDef]
    ) -> GetControlResponseTypeDef:
        """
        Returns details about a specific control, most notably a list of Amazon Web
        Services Regions where this control is supported.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/client/get_control.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controlcatalog/client/#get_control)
        """

    def list_common_controls(
        self, **kwargs: Unpack[ListCommonControlsRequestRequestTypeDef]
    ) -> ListCommonControlsResponseTypeDef:
        """
        Returns a paginated list of common controls from the Amazon Web Services
        Control Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/client/list_common_controls.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controlcatalog/client/#list_common_controls)
        """

    def list_controls(
        self, **kwargs: Unpack[ListControlsRequestRequestTypeDef]
    ) -> ListControlsResponseTypeDef:
        """
        Returns a paginated list of all available controls in the Amazon Web Services
        Control Catalog library.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/client/list_controls.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controlcatalog/client/#list_controls)
        """

    def list_domains(
        self, **kwargs: Unpack[ListDomainsRequestRequestTypeDef]
    ) -> ListDomainsResponseTypeDef:
        """
        Returns a paginated list of domains from the Amazon Web Services Control
        Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/client/list_domains.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controlcatalog/client/#list_domains)
        """

    def list_objectives(
        self, **kwargs: Unpack[ListObjectivesRequestRequestTypeDef]
    ) -> ListObjectivesResponseTypeDef:
        """
        Returns a paginated list of objectives from the Amazon Web Services Control
        Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/client/list_objectives.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controlcatalog/client/#list_objectives)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_common_controls"]
    ) -> ListCommonControlsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controlcatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_controls"]) -> ListControlsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controlcatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_domains"]) -> ListDomainsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controlcatalog/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_objectives"]) -> ListObjectivesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controlcatalog/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_controlcatalog/client/#get_paginator)
        """
