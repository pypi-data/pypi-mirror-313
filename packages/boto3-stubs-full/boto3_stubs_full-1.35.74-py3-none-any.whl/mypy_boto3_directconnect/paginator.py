"""
Type annotations for directconnect service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_directconnect/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_directconnect.client import DirectConnectClient
    from mypy_boto3_directconnect.paginator import (
        DescribeDirectConnectGatewayAssociationsPaginator,
        DescribeDirectConnectGatewayAttachmentsPaginator,
        DescribeDirectConnectGatewaysPaginator,
    )

    session = Session()
    client: DirectConnectClient = session.client("directconnect")

    describe_direct_connect_gateway_associations_paginator: DescribeDirectConnectGatewayAssociationsPaginator = client.get_paginator("describe_direct_connect_gateway_associations")
    describe_direct_connect_gateway_attachments_paginator: DescribeDirectConnectGatewayAttachmentsPaginator = client.get_paginator("describe_direct_connect_gateway_attachments")
    describe_direct_connect_gateways_paginator: DescribeDirectConnectGatewaysPaginator = client.get_paginator("describe_direct_connect_gateways")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeDirectConnectGatewayAssociationsRequestDescribeDirectConnectGatewayAssociationsPaginateTypeDef,
    DescribeDirectConnectGatewayAssociationsResultTypeDef,
    DescribeDirectConnectGatewayAttachmentsRequestDescribeDirectConnectGatewayAttachmentsPaginateTypeDef,
    DescribeDirectConnectGatewayAttachmentsResultTypeDef,
    DescribeDirectConnectGatewaysRequestDescribeDirectConnectGatewaysPaginateTypeDef,
    DescribeDirectConnectGatewaysResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeDirectConnectGatewayAssociationsPaginator",
    "DescribeDirectConnectGatewayAttachmentsPaginator",
    "DescribeDirectConnectGatewaysPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeDirectConnectGatewayAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/paginator/DescribeDirectConnectGatewayAssociations.html#DirectConnect.Paginator.DescribeDirectConnectGatewayAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_directconnect/paginators/#describedirectconnectgatewayassociationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDirectConnectGatewayAssociationsRequestDescribeDirectConnectGatewayAssociationsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeDirectConnectGatewayAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/paginator/DescribeDirectConnectGatewayAssociations.html#DirectConnect.Paginator.DescribeDirectConnectGatewayAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_directconnect/paginators/#describedirectconnectgatewayassociationspaginator)
        """


class DescribeDirectConnectGatewayAttachmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/paginator/DescribeDirectConnectGatewayAttachments.html#DirectConnect.Paginator.DescribeDirectConnectGatewayAttachments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_directconnect/paginators/#describedirectconnectgatewayattachmentspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDirectConnectGatewayAttachmentsRequestDescribeDirectConnectGatewayAttachmentsPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeDirectConnectGatewayAttachmentsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/paginator/DescribeDirectConnectGatewayAttachments.html#DirectConnect.Paginator.DescribeDirectConnectGatewayAttachments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_directconnect/paginators/#describedirectconnectgatewayattachmentspaginator)
        """


class DescribeDirectConnectGatewaysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/paginator/DescribeDirectConnectGateways.html#DirectConnect.Paginator.DescribeDirectConnectGateways)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_directconnect/paginators/#describedirectconnectgatewayspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeDirectConnectGatewaysRequestDescribeDirectConnectGatewaysPaginateTypeDef
        ],
    ) -> _PageIterator[DescribeDirectConnectGatewaysResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/paginator/DescribeDirectConnectGateways.html#DirectConnect.Paginator.DescribeDirectConnectGateways.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_directconnect/paginators/#describedirectconnectgatewayspaginator)
        """
