"""
Type annotations for verifiedpermissions service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_verifiedpermissions/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_verifiedpermissions.client import VerifiedPermissionsClient
    from mypy_boto3_verifiedpermissions.paginator import (
        ListIdentitySourcesPaginator,
        ListPoliciesPaginator,
        ListPolicyStoresPaginator,
        ListPolicyTemplatesPaginator,
    )

    session = Session()
    client: VerifiedPermissionsClient = session.client("verifiedpermissions")

    list_identity_sources_paginator: ListIdentitySourcesPaginator = client.get_paginator("list_identity_sources")
    list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
    list_policy_stores_paginator: ListPolicyStoresPaginator = client.get_paginator("list_policy_stores")
    list_policy_templates_paginator: ListPolicyTemplatesPaginator = client.get_paginator("list_policy_templates")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListIdentitySourcesInputListIdentitySourcesPaginateTypeDef,
    ListIdentitySourcesOutputTypeDef,
    ListPoliciesInputListPoliciesPaginateTypeDef,
    ListPoliciesOutputTypeDef,
    ListPolicyStoresInputListPolicyStoresPaginateTypeDef,
    ListPolicyStoresOutputTypeDef,
    ListPolicyTemplatesInputListPolicyTemplatesPaginateTypeDef,
    ListPolicyTemplatesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListIdentitySourcesPaginator",
    "ListPoliciesPaginator",
    "ListPolicyStoresPaginator",
    "ListPolicyTemplatesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListIdentitySourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/paginator/ListIdentitySources.html#VerifiedPermissions.Paginator.ListIdentitySources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_verifiedpermissions/paginators/#listidentitysourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIdentitySourcesInputListIdentitySourcesPaginateTypeDef]
    ) -> _PageIterator[ListIdentitySourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/paginator/ListIdentitySources.html#VerifiedPermissions.Paginator.ListIdentitySources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_verifiedpermissions/paginators/#listidentitysourcespaginator)
        """

class ListPoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/paginator/ListPolicies.html#VerifiedPermissions.Paginator.ListPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_verifiedpermissions/paginators/#listpoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPoliciesInputListPoliciesPaginateTypeDef]
    ) -> _PageIterator[ListPoliciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/paginator/ListPolicies.html#VerifiedPermissions.Paginator.ListPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_verifiedpermissions/paginators/#listpoliciespaginator)
        """

class ListPolicyStoresPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/paginator/ListPolicyStores.html#VerifiedPermissions.Paginator.ListPolicyStores)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_verifiedpermissions/paginators/#listpolicystorespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPolicyStoresInputListPolicyStoresPaginateTypeDef]
    ) -> _PageIterator[ListPolicyStoresOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/paginator/ListPolicyStores.html#VerifiedPermissions.Paginator.ListPolicyStores.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_verifiedpermissions/paginators/#listpolicystorespaginator)
        """

class ListPolicyTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/paginator/ListPolicyTemplates.html#VerifiedPermissions.Paginator.ListPolicyTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_verifiedpermissions/paginators/#listpolicytemplatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPolicyTemplatesInputListPolicyTemplatesPaginateTypeDef]
    ) -> _PageIterator[ListPolicyTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/paginator/ListPolicyTemplates.html#VerifiedPermissions.Paginator.ListPolicyTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_verifiedpermissions/paginators/#listpolicytemplatespaginator)
        """
