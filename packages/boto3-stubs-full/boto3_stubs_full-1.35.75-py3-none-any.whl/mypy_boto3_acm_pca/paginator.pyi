"""
Type annotations for acm-pca service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_acm_pca.client import ACMPCAClient
    from mypy_boto3_acm_pca.paginator import (
        ListCertificateAuthoritiesPaginator,
        ListPermissionsPaginator,
        ListTagsPaginator,
    )

    session = Session()
    client: ACMPCAClient = session.client("acm-pca")

    list_certificate_authorities_paginator: ListCertificateAuthoritiesPaginator = client.get_paginator("list_certificate_authorities")
    list_permissions_paginator: ListPermissionsPaginator = client.get_paginator("list_permissions")
    list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListCertificateAuthoritiesRequestListCertificateAuthoritiesPaginateTypeDef,
    ListCertificateAuthoritiesResponseTypeDef,
    ListPermissionsRequestListPermissionsPaginateTypeDef,
    ListPermissionsResponseTypeDef,
    ListTagsRequestListTagsPaginateTypeDef,
    ListTagsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListCertificateAuthoritiesPaginator", "ListPermissionsPaginator", "ListTagsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListCertificateAuthoritiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/paginator/ListCertificateAuthorities.html#ACMPCA.Paginator.ListCertificateAuthorities)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/paginators/#listcertificateauthoritiespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCertificateAuthoritiesRequestListCertificateAuthoritiesPaginateTypeDef
        ],
    ) -> _PageIterator[ListCertificateAuthoritiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/paginator/ListCertificateAuthorities.html#ACMPCA.Paginator.ListCertificateAuthorities.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/paginators/#listcertificateauthoritiespaginator)
        """

class ListPermissionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/paginator/ListPermissions.html#ACMPCA.Paginator.ListPermissions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/paginators/#listpermissionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPermissionsRequestListPermissionsPaginateTypeDef]
    ) -> _PageIterator[ListPermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/paginator/ListPermissions.html#ACMPCA.Paginator.ListPermissions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/paginators/#listpermissionspaginator)
        """

class ListTagsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/paginator/ListTags.html#ACMPCA.Paginator.ListTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/paginators/#listtagspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTagsRequestListTagsPaginateTypeDef]
    ) -> _PageIterator[ListTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/paginator/ListTags.html#ACMPCA.Paginator.ListTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/paginators/#listtagspaginator)
        """
