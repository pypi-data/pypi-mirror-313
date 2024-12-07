"""
Type annotations for cloudwatch service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_cloudwatch.client import CloudWatchClient
    from mypy_boto3_cloudwatch.paginator import (
        DescribeAlarmHistoryPaginator,
        DescribeAlarmsPaginator,
        DescribeAnomalyDetectorsPaginator,
        GetMetricDataPaginator,
        ListDashboardsPaginator,
        ListMetricsPaginator,
    )

    session = Session()
    client: CloudWatchClient = session.client("cloudwatch")

    describe_alarm_history_paginator: DescribeAlarmHistoryPaginator = client.get_paginator("describe_alarm_history")
    describe_alarms_paginator: DescribeAlarmsPaginator = client.get_paginator("describe_alarms")
    describe_anomaly_detectors_paginator: DescribeAnomalyDetectorsPaginator = client.get_paginator("describe_anomaly_detectors")
    get_metric_data_paginator: GetMetricDataPaginator = client.get_paginator("get_metric_data")
    list_dashboards_paginator: ListDashboardsPaginator = client.get_paginator("list_dashboards")
    list_metrics_paginator: ListMetricsPaginator = client.get_paginator("list_metrics")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeAlarmHistoryInputDescribeAlarmHistoryPaginateTypeDef,
    DescribeAlarmHistoryOutputTypeDef,
    DescribeAlarmsInputDescribeAlarmsPaginateTypeDef,
    DescribeAlarmsOutputTypeDef,
    DescribeAnomalyDetectorsInputDescribeAnomalyDetectorsPaginateTypeDef,
    DescribeAnomalyDetectorsOutputTypeDef,
    GetMetricDataInputGetMetricDataPaginateTypeDef,
    GetMetricDataOutputTypeDef,
    ListDashboardsInputListDashboardsPaginateTypeDef,
    ListDashboardsOutputTypeDef,
    ListMetricsInputListMetricsPaginateTypeDef,
    ListMetricsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeAlarmHistoryPaginator",
    "DescribeAlarmsPaginator",
    "DescribeAnomalyDetectorsPaginator",
    "GetMetricDataPaginator",
    "ListDashboardsPaginator",
    "ListMetricsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeAlarmHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/DescribeAlarmHistory.html#CloudWatch.Paginator.DescribeAlarmHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/paginators/#describealarmhistorypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeAlarmHistoryInputDescribeAlarmHistoryPaginateTypeDef]
    ) -> _PageIterator[DescribeAlarmHistoryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/DescribeAlarmHistory.html#CloudWatch.Paginator.DescribeAlarmHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/paginators/#describealarmhistorypaginator)
        """

class DescribeAlarmsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/DescribeAlarms.html#CloudWatch.Paginator.DescribeAlarms)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/paginators/#describealarmspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeAlarmsInputDescribeAlarmsPaginateTypeDef]
    ) -> _PageIterator[DescribeAlarmsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/DescribeAlarms.html#CloudWatch.Paginator.DescribeAlarms.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/paginators/#describealarmspaginator)
        """

class DescribeAnomalyDetectorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/DescribeAnomalyDetectors.html#CloudWatch.Paginator.DescribeAnomalyDetectors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/paginators/#describeanomalydetectorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeAnomalyDetectorsInputDescribeAnomalyDetectorsPaginateTypeDef]
    ) -> _PageIterator[DescribeAnomalyDetectorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/DescribeAnomalyDetectors.html#CloudWatch.Paginator.DescribeAnomalyDetectors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/paginators/#describeanomalydetectorspaginator)
        """

class GetMetricDataPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/GetMetricData.html#CloudWatch.Paginator.GetMetricData)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/paginators/#getmetricdatapaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetMetricDataInputGetMetricDataPaginateTypeDef]
    ) -> _PageIterator[GetMetricDataOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/GetMetricData.html#CloudWatch.Paginator.GetMetricData.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/paginators/#getmetricdatapaginator)
        """

class ListDashboardsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/ListDashboards.html#CloudWatch.Paginator.ListDashboards)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/paginators/#listdashboardspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDashboardsInputListDashboardsPaginateTypeDef]
    ) -> _PageIterator[ListDashboardsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/ListDashboards.html#CloudWatch.Paginator.ListDashboards.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/paginators/#listdashboardspaginator)
        """

class ListMetricsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/ListMetrics.html#CloudWatch.Paginator.ListMetrics)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/paginators/#listmetricspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMetricsInputListMetricsPaginateTypeDef]
    ) -> _PageIterator[ListMetricsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/ListMetrics.html#CloudWatch.Paginator.ListMetrics.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/paginators/#listmetricspaginator)
        """
