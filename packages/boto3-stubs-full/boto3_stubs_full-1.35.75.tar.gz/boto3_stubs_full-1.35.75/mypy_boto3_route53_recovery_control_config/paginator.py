"""
Type annotations for route53-recovery-control-config service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_route53_recovery_control_config.client import Route53RecoveryControlConfigClient
    from mypy_boto3_route53_recovery_control_config.paginator import (
        ListAssociatedRoute53HealthChecksPaginator,
        ListClustersPaginator,
        ListControlPanelsPaginator,
        ListRoutingControlsPaginator,
        ListSafetyRulesPaginator,
    )

    session = Session()
    client: Route53RecoveryControlConfigClient = session.client("route53-recovery-control-config")

    list_associated_route53_health_checks_paginator: ListAssociatedRoute53HealthChecksPaginator = client.get_paginator("list_associated_route53_health_checks")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_control_panels_paginator: ListControlPanelsPaginator = client.get_paginator("list_control_panels")
    list_routing_controls_paginator: ListRoutingControlsPaginator = client.get_paginator("list_routing_controls")
    list_safety_rules_paginator: ListSafetyRulesPaginator = client.get_paginator("list_safety_rules")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAssociatedRoute53HealthChecksRequestListAssociatedRoute53HealthChecksPaginateTypeDef,
    ListAssociatedRoute53HealthChecksResponseTypeDef,
    ListClustersRequestListClustersPaginateTypeDef,
    ListClustersResponseTypeDef,
    ListControlPanelsRequestListControlPanelsPaginateTypeDef,
    ListControlPanelsResponseTypeDef,
    ListRoutingControlsRequestListRoutingControlsPaginateTypeDef,
    ListRoutingControlsResponseTypeDef,
    ListSafetyRulesRequestListSafetyRulesPaginateTypeDef,
    ListSafetyRulesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAssociatedRoute53HealthChecksPaginator",
    "ListClustersPaginator",
    "ListControlPanelsPaginator",
    "ListRoutingControlsPaginator",
    "ListSafetyRulesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAssociatedRoute53HealthChecksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListAssociatedRoute53HealthChecks.html#Route53RecoveryControlConfig.Paginator.ListAssociatedRoute53HealthChecks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/paginators/#listassociatedroute53healthcheckspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListAssociatedRoute53HealthChecksRequestListAssociatedRoute53HealthChecksPaginateTypeDef
        ],
    ) -> _PageIterator[ListAssociatedRoute53HealthChecksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListAssociatedRoute53HealthChecks.html#Route53RecoveryControlConfig.Paginator.ListAssociatedRoute53HealthChecks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/paginators/#listassociatedroute53healthcheckspaginator)
        """


class ListClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListClusters.html#Route53RecoveryControlConfig.Paginator.ListClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/paginators/#listclusterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListClustersRequestListClustersPaginateTypeDef]
    ) -> _PageIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListClusters.html#Route53RecoveryControlConfig.Paginator.ListClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/paginators/#listclusterspaginator)
        """


class ListControlPanelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListControlPanels.html#Route53RecoveryControlConfig.Paginator.ListControlPanels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/paginators/#listcontrolpanelspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListControlPanelsRequestListControlPanelsPaginateTypeDef]
    ) -> _PageIterator[ListControlPanelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListControlPanels.html#Route53RecoveryControlConfig.Paginator.ListControlPanels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/paginators/#listcontrolpanelspaginator)
        """


class ListRoutingControlsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListRoutingControls.html#Route53RecoveryControlConfig.Paginator.ListRoutingControls)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/paginators/#listroutingcontrolspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRoutingControlsRequestListRoutingControlsPaginateTypeDef]
    ) -> _PageIterator[ListRoutingControlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListRoutingControls.html#Route53RecoveryControlConfig.Paginator.ListRoutingControls.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/paginators/#listroutingcontrolspaginator)
        """


class ListSafetyRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListSafetyRules.html#Route53RecoveryControlConfig.Paginator.ListSafetyRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/paginators/#listsafetyrulespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSafetyRulesRequestListSafetyRulesPaginateTypeDef]
    ) -> _PageIterator[ListSafetyRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListSafetyRules.html#Route53RecoveryControlConfig.Paginator.ListSafetyRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/paginators/#listsafetyrulespaginator)
        """
