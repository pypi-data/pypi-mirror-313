"""
Type annotations for service-quotas service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_service_quotas.client import ServiceQuotasClient
    from mypy_boto3_service_quotas.paginator import (
        ListAWSDefaultServiceQuotasPaginator,
        ListRequestedServiceQuotaChangeHistoryByQuotaPaginator,
        ListRequestedServiceQuotaChangeHistoryPaginator,
        ListServiceQuotaIncreaseRequestsInTemplatePaginator,
        ListServiceQuotasPaginator,
        ListServicesPaginator,
    )

    session = Session()
    client: ServiceQuotasClient = session.client("service-quotas")

    list_aws_default_service_quotas_paginator: ListAWSDefaultServiceQuotasPaginator = client.get_paginator("list_aws_default_service_quotas")
    list_requested_service_quota_change_history_by_quota_paginator: ListRequestedServiceQuotaChangeHistoryByQuotaPaginator = client.get_paginator("list_requested_service_quota_change_history_by_quota")
    list_requested_service_quota_change_history_paginator: ListRequestedServiceQuotaChangeHistoryPaginator = client.get_paginator("list_requested_service_quota_change_history")
    list_service_quota_increase_requests_in_template_paginator: ListServiceQuotaIncreaseRequestsInTemplatePaginator = client.get_paginator("list_service_quota_increase_requests_in_template")
    list_service_quotas_paginator: ListServiceQuotasPaginator = client.get_paginator("list_service_quotas")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAWSDefaultServiceQuotasRequestListAWSDefaultServiceQuotasPaginateTypeDef,
    ListAWSDefaultServiceQuotasResponseTypeDef,
    ListRequestedServiceQuotaChangeHistoryByQuotaRequestListRequestedServiceQuotaChangeHistoryByQuotaPaginateTypeDef,
    ListRequestedServiceQuotaChangeHistoryByQuotaResponseTypeDef,
    ListRequestedServiceQuotaChangeHistoryRequestListRequestedServiceQuotaChangeHistoryPaginateTypeDef,
    ListRequestedServiceQuotaChangeHistoryResponseTypeDef,
    ListServiceQuotaIncreaseRequestsInTemplateRequestListServiceQuotaIncreaseRequestsInTemplatePaginateTypeDef,
    ListServiceQuotaIncreaseRequestsInTemplateResponseTypeDef,
    ListServiceQuotasRequestListServiceQuotasPaginateTypeDef,
    ListServiceQuotasResponseTypeDef,
    ListServicesRequestListServicesPaginateTypeDef,
    ListServicesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAWSDefaultServiceQuotasPaginator",
    "ListRequestedServiceQuotaChangeHistoryByQuotaPaginator",
    "ListRequestedServiceQuotaChangeHistoryPaginator",
    "ListServiceQuotaIncreaseRequestsInTemplatePaginator",
    "ListServiceQuotasPaginator",
    "ListServicesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAWSDefaultServiceQuotasPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListAWSDefaultServiceQuotas.html#ServiceQuotas.Paginator.ListAWSDefaultServiceQuotas)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listawsdefaultservicequotaspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListAWSDefaultServiceQuotasRequestListAWSDefaultServiceQuotasPaginateTypeDef
        ],
    ) -> _PageIterator[ListAWSDefaultServiceQuotasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListAWSDefaultServiceQuotas.html#ServiceQuotas.Paginator.ListAWSDefaultServiceQuotas.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listawsdefaultservicequotaspaginator)
        """


class ListRequestedServiceQuotaChangeHistoryByQuotaPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListRequestedServiceQuotaChangeHistoryByQuota.html#ServiceQuotas.Paginator.ListRequestedServiceQuotaChangeHistoryByQuota)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listrequestedservicequotachangehistorybyquotapaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListRequestedServiceQuotaChangeHistoryByQuotaRequestListRequestedServiceQuotaChangeHistoryByQuotaPaginateTypeDef
        ],
    ) -> _PageIterator[ListRequestedServiceQuotaChangeHistoryByQuotaResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListRequestedServiceQuotaChangeHistoryByQuota.html#ServiceQuotas.Paginator.ListRequestedServiceQuotaChangeHistoryByQuota.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listrequestedservicequotachangehistorybyquotapaginator)
        """


class ListRequestedServiceQuotaChangeHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListRequestedServiceQuotaChangeHistory.html#ServiceQuotas.Paginator.ListRequestedServiceQuotaChangeHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listrequestedservicequotachangehistorypaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListRequestedServiceQuotaChangeHistoryRequestListRequestedServiceQuotaChangeHistoryPaginateTypeDef
        ],
    ) -> _PageIterator[ListRequestedServiceQuotaChangeHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListRequestedServiceQuotaChangeHistory.html#ServiceQuotas.Paginator.ListRequestedServiceQuotaChangeHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listrequestedservicequotachangehistorypaginator)
        """


class ListServiceQuotaIncreaseRequestsInTemplatePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListServiceQuotaIncreaseRequestsInTemplate.html#ServiceQuotas.Paginator.ListServiceQuotaIncreaseRequestsInTemplate)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listservicequotaincreaserequestsintemplatepaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListServiceQuotaIncreaseRequestsInTemplateRequestListServiceQuotaIncreaseRequestsInTemplatePaginateTypeDef
        ],
    ) -> _PageIterator[ListServiceQuotaIncreaseRequestsInTemplateResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListServiceQuotaIncreaseRequestsInTemplate.html#ServiceQuotas.Paginator.ListServiceQuotaIncreaseRequestsInTemplate.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listservicequotaincreaserequestsintemplatepaginator)
        """


class ListServiceQuotasPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListServiceQuotas.html#ServiceQuotas.Paginator.ListServiceQuotas)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listservicequotaspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListServiceQuotasRequestListServiceQuotasPaginateTypeDef]
    ) -> _PageIterator[ListServiceQuotasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListServiceQuotas.html#ServiceQuotas.Paginator.ListServiceQuotas.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listservicequotaspaginator)
        """


class ListServicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListServices.html#ServiceQuotas.Paginator.ListServices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listservicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListServicesRequestListServicesPaginateTypeDef]
    ) -> _PageIterator[ListServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListServices.html#ServiceQuotas.Paginator.ListServices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_service_quotas/paginators/#listservicespaginator)
        """
