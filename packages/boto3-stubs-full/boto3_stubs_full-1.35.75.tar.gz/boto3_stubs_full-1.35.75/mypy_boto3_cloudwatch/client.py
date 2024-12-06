"""
Type annotations for cloudwatch service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloudwatch.client import CloudWatchClient

    session = Session()
    client: CloudWatchClient = session.client("cloudwatch")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    DescribeAlarmHistoryPaginator,
    DescribeAlarmsPaginator,
    DescribeAnomalyDetectorsPaginator,
    GetMetricDataPaginator,
    ListDashboardsPaginator,
    ListMetricsPaginator,
)
from .type_defs import (
    DeleteAlarmsInputRequestTypeDef,
    DeleteAnomalyDetectorInputRequestTypeDef,
    DeleteDashboardsInputRequestTypeDef,
    DeleteInsightRulesInputRequestTypeDef,
    DeleteInsightRulesOutputTypeDef,
    DeleteMetricStreamInputRequestTypeDef,
    DescribeAlarmHistoryInputRequestTypeDef,
    DescribeAlarmHistoryOutputTypeDef,
    DescribeAlarmsForMetricInputRequestTypeDef,
    DescribeAlarmsForMetricOutputTypeDef,
    DescribeAlarmsInputRequestTypeDef,
    DescribeAlarmsOutputTypeDef,
    DescribeAnomalyDetectorsInputRequestTypeDef,
    DescribeAnomalyDetectorsOutputTypeDef,
    DescribeInsightRulesInputRequestTypeDef,
    DescribeInsightRulesOutputTypeDef,
    DisableAlarmActionsInputRequestTypeDef,
    DisableInsightRulesInputRequestTypeDef,
    DisableInsightRulesOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableAlarmActionsInputRequestTypeDef,
    EnableInsightRulesInputRequestTypeDef,
    EnableInsightRulesOutputTypeDef,
    GetDashboardInputRequestTypeDef,
    GetDashboardOutputTypeDef,
    GetInsightRuleReportInputRequestTypeDef,
    GetInsightRuleReportOutputTypeDef,
    GetMetricDataInputRequestTypeDef,
    GetMetricDataOutputTypeDef,
    GetMetricStatisticsInputRequestTypeDef,
    GetMetricStatisticsOutputTypeDef,
    GetMetricStreamInputRequestTypeDef,
    GetMetricStreamOutputTypeDef,
    GetMetricWidgetImageInputRequestTypeDef,
    GetMetricWidgetImageOutputTypeDef,
    ListDashboardsInputRequestTypeDef,
    ListDashboardsOutputTypeDef,
    ListManagedInsightRulesInputRequestTypeDef,
    ListManagedInsightRulesOutputTypeDef,
    ListMetricsInputRequestTypeDef,
    ListMetricsOutputTypeDef,
    ListMetricStreamsInputRequestTypeDef,
    ListMetricStreamsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    PutAnomalyDetectorInputRequestTypeDef,
    PutCompositeAlarmInputRequestTypeDef,
    PutDashboardInputRequestTypeDef,
    PutDashboardOutputTypeDef,
    PutInsightRuleInputRequestTypeDef,
    PutManagedInsightRulesInputRequestTypeDef,
    PutManagedInsightRulesOutputTypeDef,
    PutMetricAlarmInputRequestTypeDef,
    PutMetricDataInputRequestTypeDef,
    PutMetricStreamInputRequestTypeDef,
    PutMetricStreamOutputTypeDef,
    SetAlarmStateInputRequestTypeDef,
    StartMetricStreamsInputRequestTypeDef,
    StopMetricStreamsInputRequestTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
)
from .waiter import AlarmExistsWaiter, CompositeAlarmExistsWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("CloudWatchClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    DashboardInvalidInputError: Type[BotocoreClientError]
    DashboardNotFoundError: Type[BotocoreClientError]
    InternalServiceFault: Type[BotocoreClientError]
    InvalidFormatFault: Type[BotocoreClientError]
    InvalidNextToken: Type[BotocoreClientError]
    InvalidParameterCombinationException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    LimitExceededFault: Type[BotocoreClientError]
    MissingRequiredParameterException: Type[BotocoreClientError]
    ResourceNotFound: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class CloudWatchClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#close)
        """

    def delete_alarms(
        self, **kwargs: Unpack[DeleteAlarmsInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/delete_alarms.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#delete_alarms)
        """

    def delete_anomaly_detector(
        self, **kwargs: Unpack[DeleteAnomalyDetectorInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified anomaly detection model from your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/delete_anomaly_detector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#delete_anomaly_detector)
        """

    def delete_dashboards(
        self, **kwargs: Unpack[DeleteDashboardsInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes all dashboards that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/delete_dashboards.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#delete_dashboards)
        """

    def delete_insight_rules(
        self, **kwargs: Unpack[DeleteInsightRulesInputRequestTypeDef]
    ) -> DeleteInsightRulesOutputTypeDef:
        """
        Permanently deletes the specified Contributor Insights rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/delete_insight_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#delete_insight_rules)
        """

    def delete_metric_stream(
        self, **kwargs: Unpack[DeleteMetricStreamInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Permanently deletes the metric stream that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/delete_metric_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#delete_metric_stream)
        """

    def describe_alarm_history(
        self, **kwargs: Unpack[DescribeAlarmHistoryInputRequestTypeDef]
    ) -> DescribeAlarmHistoryOutputTypeDef:
        """
        Retrieves the history for the specified alarm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/describe_alarm_history.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#describe_alarm_history)
        """

    def describe_alarms(
        self, **kwargs: Unpack[DescribeAlarmsInputRequestTypeDef]
    ) -> DescribeAlarmsOutputTypeDef:
        """
        Retrieves the specified alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/describe_alarms.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#describe_alarms)
        """

    def describe_alarms_for_metric(
        self, **kwargs: Unpack[DescribeAlarmsForMetricInputRequestTypeDef]
    ) -> DescribeAlarmsForMetricOutputTypeDef:
        """
        Retrieves the alarms for the specified metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/describe_alarms_for_metric.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#describe_alarms_for_metric)
        """

    def describe_anomaly_detectors(
        self, **kwargs: Unpack[DescribeAnomalyDetectorsInputRequestTypeDef]
    ) -> DescribeAnomalyDetectorsOutputTypeDef:
        """
        Lists the anomaly detection models that you have created in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/describe_anomaly_detectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#describe_anomaly_detectors)
        """

    def describe_insight_rules(
        self, **kwargs: Unpack[DescribeInsightRulesInputRequestTypeDef]
    ) -> DescribeInsightRulesOutputTypeDef:
        """
        Returns a list of all the Contributor Insights rules in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/describe_insight_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#describe_insight_rules)
        """

    def disable_alarm_actions(
        self, **kwargs: Unpack[DisableAlarmActionsInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disables the actions for the specified alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/disable_alarm_actions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#disable_alarm_actions)
        """

    def disable_insight_rules(
        self, **kwargs: Unpack[DisableInsightRulesInputRequestTypeDef]
    ) -> DisableInsightRulesOutputTypeDef:
        """
        Disables the specified Contributor Insights rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/disable_insight_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#disable_insight_rules)
        """

    def enable_alarm_actions(
        self, **kwargs: Unpack[EnableAlarmActionsInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables the actions for the specified alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/enable_alarm_actions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#enable_alarm_actions)
        """

    def enable_insight_rules(
        self, **kwargs: Unpack[EnableInsightRulesInputRequestTypeDef]
    ) -> EnableInsightRulesOutputTypeDef:
        """
        Enables the specified Contributor Insights rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/enable_insight_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#enable_insight_rules)
        """

    def get_dashboard(
        self, **kwargs: Unpack[GetDashboardInputRequestTypeDef]
    ) -> GetDashboardOutputTypeDef:
        """
        Displays the details of the dashboard that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_dashboard.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#get_dashboard)
        """

    def get_insight_rule_report(
        self, **kwargs: Unpack[GetInsightRuleReportInputRequestTypeDef]
    ) -> GetInsightRuleReportOutputTypeDef:
        """
        This operation returns the time series data collected by a Contributor Insights
        rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_insight_rule_report.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#get_insight_rule_report)
        """

    def get_metric_data(
        self, **kwargs: Unpack[GetMetricDataInputRequestTypeDef]
    ) -> GetMetricDataOutputTypeDef:
        """
        You can use the <code>GetMetricData</code> API to retrieve CloudWatch metric
        values.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_metric_data.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#get_metric_data)
        """

    def get_metric_statistics(
        self, **kwargs: Unpack[GetMetricStatisticsInputRequestTypeDef]
    ) -> GetMetricStatisticsOutputTypeDef:
        """
        Gets statistics for the specified metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_metric_statistics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#get_metric_statistics)
        """

    def get_metric_stream(
        self, **kwargs: Unpack[GetMetricStreamInputRequestTypeDef]
    ) -> GetMetricStreamOutputTypeDef:
        """
        Returns information about the metric stream that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_metric_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#get_metric_stream)
        """

    def get_metric_widget_image(
        self, **kwargs: Unpack[GetMetricWidgetImageInputRequestTypeDef]
    ) -> GetMetricWidgetImageOutputTypeDef:
        """
        You can use the <code>GetMetricWidgetImage</code> API to retrieve a snapshot
        graph of one or more Amazon CloudWatch metrics as a bitmap image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_metric_widget_image.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#get_metric_widget_image)
        """

    def list_dashboards(
        self, **kwargs: Unpack[ListDashboardsInputRequestTypeDef]
    ) -> ListDashboardsOutputTypeDef:
        """
        Returns a list of the dashboards for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/list_dashboards.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#list_dashboards)
        """

    def list_managed_insight_rules(
        self, **kwargs: Unpack[ListManagedInsightRulesInputRequestTypeDef]
    ) -> ListManagedInsightRulesOutputTypeDef:
        """
        Returns a list that contains the number of managed Contributor Insights rules
        in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/list_managed_insight_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#list_managed_insight_rules)
        """

    def list_metric_streams(
        self, **kwargs: Unpack[ListMetricStreamsInputRequestTypeDef]
    ) -> ListMetricStreamsOutputTypeDef:
        """
        Returns a list of metric streams in this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/list_metric_streams.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#list_metric_streams)
        """

    def list_metrics(
        self, **kwargs: Unpack[ListMetricsInputRequestTypeDef]
    ) -> ListMetricsOutputTypeDef:
        """
        List the specified metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/list_metrics.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#list_metrics)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Displays the tags associated with a CloudWatch resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#list_tags_for_resource)
        """

    def put_anomaly_detector(
        self, **kwargs: Unpack[PutAnomalyDetectorInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates an anomaly detection model for a CloudWatch metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/put_anomaly_detector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#put_anomaly_detector)
        """

    def put_composite_alarm(
        self, **kwargs: Unpack[PutCompositeAlarmInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates a <i>composite alarm</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/put_composite_alarm.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#put_composite_alarm)
        """

    def put_dashboard(
        self, **kwargs: Unpack[PutDashboardInputRequestTypeDef]
    ) -> PutDashboardOutputTypeDef:
        """
        Creates a dashboard if it does not already exist, or updates an existing
        dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/put_dashboard.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#put_dashboard)
        """

    def put_insight_rule(
        self, **kwargs: Unpack[PutInsightRuleInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a Contributor Insights rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/put_insight_rule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#put_insight_rule)
        """

    def put_managed_insight_rules(
        self, **kwargs: Unpack[PutManagedInsightRulesInputRequestTypeDef]
    ) -> PutManagedInsightRulesOutputTypeDef:
        """
        Creates a managed Contributor Insights rule for a specified Amazon Web Services
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/put_managed_insight_rules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#put_managed_insight_rules)
        """

    def put_metric_alarm(
        self, **kwargs: Unpack[PutMetricAlarmInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates an alarm and associates it with the specified metric, metric
        math expression, anomaly detection model, or Metrics Insights query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/put_metric_alarm.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#put_metric_alarm)
        """

    def put_metric_data(
        self, **kwargs: Unpack[PutMetricDataInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Publishes metric data to Amazon CloudWatch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/put_metric_data.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#put_metric_data)
        """

    def put_metric_stream(
        self, **kwargs: Unpack[PutMetricStreamInputRequestTypeDef]
    ) -> PutMetricStreamOutputTypeDef:
        """
        Creates or updates a metric stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/put_metric_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#put_metric_stream)
        """

    def set_alarm_state(
        self, **kwargs: Unpack[SetAlarmStateInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Temporarily sets the state of an alarm for testing purposes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/set_alarm_state.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#set_alarm_state)
        """

    def start_metric_streams(
        self, **kwargs: Unpack[StartMetricStreamsInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts the streaming of metrics for one or more of your metric streams.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/start_metric_streams.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#start_metric_streams)
        """

    def stop_metric_streams(
        self, **kwargs: Unpack[StopMetricStreamsInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops the streaming of metrics for one or more of your metric streams.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/stop_metric_streams.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#stop_metric_streams)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified CloudWatch resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_alarm_history"]
    ) -> DescribeAlarmHistoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_alarms"]) -> DescribeAlarmsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_anomaly_detectors"]
    ) -> DescribeAnomalyDetectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_metric_data"]) -> GetMetricDataPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_dashboards"]) -> ListDashboardsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_metrics"]) -> ListMetricsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["alarm_exists"]) -> AlarmExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["composite_alarm_exists"]
    ) -> CompositeAlarmExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/client/#get_waiter)
        """
