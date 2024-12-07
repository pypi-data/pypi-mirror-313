"""
Type annotations for rolesanywhere service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rolesanywhere/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_rolesanywhere.client import IAMRolesAnywhereClient
    from mypy_boto3_rolesanywhere.paginator import (
        ListCrlsPaginator,
        ListProfilesPaginator,
        ListSubjectsPaginator,
        ListTrustAnchorsPaginator,
    )

    session = Session()
    client: IAMRolesAnywhereClient = session.client("rolesanywhere")

    list_crls_paginator: ListCrlsPaginator = client.get_paginator("list_crls")
    list_profiles_paginator: ListProfilesPaginator = client.get_paginator("list_profiles")
    list_subjects_paginator: ListSubjectsPaginator = client.get_paginator("list_subjects")
    list_trust_anchors_paginator: ListTrustAnchorsPaginator = client.get_paginator("list_trust_anchors")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListCrlsResponseTypeDef,
    ListProfilesResponseTypeDef,
    ListRequestListCrlsPaginateTypeDef,
    ListRequestListProfilesPaginateTypeDef,
    ListRequestListSubjectsPaginateTypeDef,
    ListRequestListTrustAnchorsPaginateTypeDef,
    ListSubjectsResponseTypeDef,
    ListTrustAnchorsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListCrlsPaginator",
    "ListProfilesPaginator",
    "ListSubjectsPaginator",
    "ListTrustAnchorsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListCrlsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/paginator/ListCrls.html#IAMRolesAnywhere.Paginator.ListCrls)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rolesanywhere/paginators/#listcrlspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRequestListCrlsPaginateTypeDef]
    ) -> _PageIterator[ListCrlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/paginator/ListCrls.html#IAMRolesAnywhere.Paginator.ListCrls.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rolesanywhere/paginators/#listcrlspaginator)
        """

class ListProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/paginator/ListProfiles.html#IAMRolesAnywhere.Paginator.ListProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rolesanywhere/paginators/#listprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRequestListProfilesPaginateTypeDef]
    ) -> _PageIterator[ListProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/paginator/ListProfiles.html#IAMRolesAnywhere.Paginator.ListProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rolesanywhere/paginators/#listprofilespaginator)
        """

class ListSubjectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/paginator/ListSubjects.html#IAMRolesAnywhere.Paginator.ListSubjects)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rolesanywhere/paginators/#listsubjectspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRequestListSubjectsPaginateTypeDef]
    ) -> _PageIterator[ListSubjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/paginator/ListSubjects.html#IAMRolesAnywhere.Paginator.ListSubjects.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rolesanywhere/paginators/#listsubjectspaginator)
        """

class ListTrustAnchorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/paginator/ListTrustAnchors.html#IAMRolesAnywhere.Paginator.ListTrustAnchors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rolesanywhere/paginators/#listtrustanchorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRequestListTrustAnchorsPaginateTypeDef]
    ) -> _PageIterator[ListTrustAnchorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/paginator/ListTrustAnchors.html#IAMRolesAnywhere.Paginator.ListTrustAnchors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rolesanywhere/paginators/#listtrustanchorspaginator)
        """
