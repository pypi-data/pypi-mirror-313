"""
Type annotations for ssm-incidents service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ssm_incidents.client import SSMIncidentsClient
    from mypy_boto3_ssm_incidents.paginator import (
        GetResourcePoliciesPaginator,
        ListIncidentFindingsPaginator,
        ListIncidentRecordsPaginator,
        ListRelatedItemsPaginator,
        ListReplicationSetsPaginator,
        ListResponsePlansPaginator,
        ListTimelineEventsPaginator,
    )

    session = Session()
    client: SSMIncidentsClient = session.client("ssm-incidents")

    get_resource_policies_paginator: GetResourcePoliciesPaginator = client.get_paginator("get_resource_policies")
    list_incident_findings_paginator: ListIncidentFindingsPaginator = client.get_paginator("list_incident_findings")
    list_incident_records_paginator: ListIncidentRecordsPaginator = client.get_paginator("list_incident_records")
    list_related_items_paginator: ListRelatedItemsPaginator = client.get_paginator("list_related_items")
    list_replication_sets_paginator: ListReplicationSetsPaginator = client.get_paginator("list_replication_sets")
    list_response_plans_paginator: ListResponsePlansPaginator = client.get_paginator("list_response_plans")
    list_timeline_events_paginator: ListTimelineEventsPaginator = client.get_paginator("list_timeline_events")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetResourcePoliciesInputGetResourcePoliciesPaginateTypeDef,
    GetResourcePoliciesOutputTypeDef,
    ListIncidentFindingsInputListIncidentFindingsPaginateTypeDef,
    ListIncidentFindingsOutputTypeDef,
    ListIncidentRecordsInputListIncidentRecordsPaginateTypeDef,
    ListIncidentRecordsOutputTypeDef,
    ListRelatedItemsInputListRelatedItemsPaginateTypeDef,
    ListRelatedItemsOutputTypeDef,
    ListReplicationSetsInputListReplicationSetsPaginateTypeDef,
    ListReplicationSetsOutputTypeDef,
    ListResponsePlansInputListResponsePlansPaginateTypeDef,
    ListResponsePlansOutputTypeDef,
    ListTimelineEventsInputListTimelineEventsPaginateTypeDef,
    ListTimelineEventsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetResourcePoliciesPaginator",
    "ListIncidentFindingsPaginator",
    "ListIncidentRecordsPaginator",
    "ListRelatedItemsPaginator",
    "ListReplicationSetsPaginator",
    "ListResponsePlansPaginator",
    "ListTimelineEventsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetResourcePoliciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/paginator/GetResourcePolicies.html#SSMIncidents.Paginator.GetResourcePolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/paginators/#getresourcepoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetResourcePoliciesInputGetResourcePoliciesPaginateTypeDef]
    ) -> _PageIterator[GetResourcePoliciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/paginator/GetResourcePolicies.html#SSMIncidents.Paginator.GetResourcePolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/paginators/#getresourcepoliciespaginator)
        """

class ListIncidentFindingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/paginator/ListIncidentFindings.html#SSMIncidents.Paginator.ListIncidentFindings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/paginators/#listincidentfindingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIncidentFindingsInputListIncidentFindingsPaginateTypeDef]
    ) -> _PageIterator[ListIncidentFindingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/paginator/ListIncidentFindings.html#SSMIncidents.Paginator.ListIncidentFindings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/paginators/#listincidentfindingspaginator)
        """

class ListIncidentRecordsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/paginator/ListIncidentRecords.html#SSMIncidents.Paginator.ListIncidentRecords)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/paginators/#listincidentrecordspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIncidentRecordsInputListIncidentRecordsPaginateTypeDef]
    ) -> _PageIterator[ListIncidentRecordsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/paginator/ListIncidentRecords.html#SSMIncidents.Paginator.ListIncidentRecords.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/paginators/#listincidentrecordspaginator)
        """

class ListRelatedItemsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/paginator/ListRelatedItems.html#SSMIncidents.Paginator.ListRelatedItems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/paginators/#listrelateditemspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRelatedItemsInputListRelatedItemsPaginateTypeDef]
    ) -> _PageIterator[ListRelatedItemsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/paginator/ListRelatedItems.html#SSMIncidents.Paginator.ListRelatedItems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/paginators/#listrelateditemspaginator)
        """

class ListReplicationSetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/paginator/ListReplicationSets.html#SSMIncidents.Paginator.ListReplicationSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/paginators/#listreplicationsetspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListReplicationSetsInputListReplicationSetsPaginateTypeDef]
    ) -> _PageIterator[ListReplicationSetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/paginator/ListReplicationSets.html#SSMIncidents.Paginator.ListReplicationSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/paginators/#listreplicationsetspaginator)
        """

class ListResponsePlansPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/paginator/ListResponsePlans.html#SSMIncidents.Paginator.ListResponsePlans)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/paginators/#listresponseplanspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListResponsePlansInputListResponsePlansPaginateTypeDef]
    ) -> _PageIterator[ListResponsePlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/paginator/ListResponsePlans.html#SSMIncidents.Paginator.ListResponsePlans.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/paginators/#listresponseplanspaginator)
        """

class ListTimelineEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/paginator/ListTimelineEvents.html#SSMIncidents.Paginator.ListTimelineEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/paginators/#listtimelineeventspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTimelineEventsInputListTimelineEventsPaginateTypeDef]
    ) -> _PageIterator[ListTimelineEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/paginator/ListTimelineEvents.html#SSMIncidents.Paginator.ListTimelineEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_incidents/paginators/#listtimelineeventspaginator)
        """
