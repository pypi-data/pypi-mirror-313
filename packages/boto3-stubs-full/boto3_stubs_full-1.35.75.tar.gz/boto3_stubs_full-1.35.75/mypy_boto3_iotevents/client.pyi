"""
Type annotations for iotevents service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iotevents.client import IoTEventsClient

    session = Session()
    client: IoTEventsClient = session.client("iotevents")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    CreateAlarmModelRequestRequestTypeDef,
    CreateAlarmModelResponseTypeDef,
    CreateDetectorModelRequestRequestTypeDef,
    CreateDetectorModelResponseTypeDef,
    CreateInputRequestRequestTypeDef,
    CreateInputResponseTypeDef,
    DeleteAlarmModelRequestRequestTypeDef,
    DeleteDetectorModelRequestRequestTypeDef,
    DeleteInputRequestRequestTypeDef,
    DescribeAlarmModelRequestRequestTypeDef,
    DescribeAlarmModelResponseTypeDef,
    DescribeDetectorModelAnalysisRequestRequestTypeDef,
    DescribeDetectorModelAnalysisResponseTypeDef,
    DescribeDetectorModelRequestRequestTypeDef,
    DescribeDetectorModelResponseTypeDef,
    DescribeInputRequestRequestTypeDef,
    DescribeInputResponseTypeDef,
    DescribeLoggingOptionsResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetDetectorModelAnalysisResultsRequestRequestTypeDef,
    GetDetectorModelAnalysisResultsResponseTypeDef,
    ListAlarmModelsRequestRequestTypeDef,
    ListAlarmModelsResponseTypeDef,
    ListAlarmModelVersionsRequestRequestTypeDef,
    ListAlarmModelVersionsResponseTypeDef,
    ListDetectorModelsRequestRequestTypeDef,
    ListDetectorModelsResponseTypeDef,
    ListDetectorModelVersionsRequestRequestTypeDef,
    ListDetectorModelVersionsResponseTypeDef,
    ListInputRoutingsRequestRequestTypeDef,
    ListInputRoutingsResponseTypeDef,
    ListInputsRequestRequestTypeDef,
    ListInputsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutLoggingOptionsRequestRequestTypeDef,
    StartDetectorModelAnalysisRequestRequestTypeDef,
    StartDetectorModelAnalysisResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAlarmModelRequestRequestTypeDef,
    UpdateAlarmModelResponseTypeDef,
    UpdateDetectorModelRequestRequestTypeDef,
    UpdateDetectorModelResponseTypeDef,
    UpdateInputRequestRequestTypeDef,
    UpdateInputResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("IoTEventsClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]

class IoTEventsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTEventsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents.html#IoTEvents.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/close.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#close)
        """

    def create_alarm_model(
        self, **kwargs: Unpack[CreateAlarmModelRequestRequestTypeDef]
    ) -> CreateAlarmModelResponseTypeDef:
        """
        Creates an alarm model to monitor an AWS IoT Events input attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/create_alarm_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#create_alarm_model)
        """

    def create_detector_model(
        self, **kwargs: Unpack[CreateDetectorModelRequestRequestTypeDef]
    ) -> CreateDetectorModelResponseTypeDef:
        """
        Creates a detector model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/create_detector_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#create_detector_model)
        """

    def create_input(
        self, **kwargs: Unpack[CreateInputRequestRequestTypeDef]
    ) -> CreateInputResponseTypeDef:
        """
        Creates an input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/create_input.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#create_input)
        """

    def delete_alarm_model(
        self, **kwargs: Unpack[DeleteAlarmModelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an alarm model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/delete_alarm_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#delete_alarm_model)
        """

    def delete_detector_model(
        self, **kwargs: Unpack[DeleteDetectorModelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a detector model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/delete_detector_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#delete_detector_model)
        """

    def delete_input(self, **kwargs: Unpack[DeleteInputRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes an input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/delete_input.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#delete_input)
        """

    def describe_alarm_model(
        self, **kwargs: Unpack[DescribeAlarmModelRequestRequestTypeDef]
    ) -> DescribeAlarmModelResponseTypeDef:
        """
        Retrieves information about an alarm model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/describe_alarm_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#describe_alarm_model)
        """

    def describe_detector_model(
        self, **kwargs: Unpack[DescribeDetectorModelRequestRequestTypeDef]
    ) -> DescribeDetectorModelResponseTypeDef:
        """
        Describes a detector model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/describe_detector_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#describe_detector_model)
        """

    def describe_detector_model_analysis(
        self, **kwargs: Unpack[DescribeDetectorModelAnalysisRequestRequestTypeDef]
    ) -> DescribeDetectorModelAnalysisResponseTypeDef:
        """
        Retrieves runtime information about a detector model analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/describe_detector_model_analysis.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#describe_detector_model_analysis)
        """

    def describe_input(
        self, **kwargs: Unpack[DescribeInputRequestRequestTypeDef]
    ) -> DescribeInputResponseTypeDef:
        """
        Describes an input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/describe_input.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#describe_input)
        """

    def describe_logging_options(self) -> DescribeLoggingOptionsResponseTypeDef:
        """
        Retrieves the current settings of the AWS IoT Events logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/describe_logging_options.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#describe_logging_options)
        """

    def get_detector_model_analysis_results(
        self, **kwargs: Unpack[GetDetectorModelAnalysisResultsRequestRequestTypeDef]
    ) -> GetDetectorModelAnalysisResultsResponseTypeDef:
        """
        Retrieves one or more analysis results of the detector model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/get_detector_model_analysis_results.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#get_detector_model_analysis_results)
        """

    def list_alarm_model_versions(
        self, **kwargs: Unpack[ListAlarmModelVersionsRequestRequestTypeDef]
    ) -> ListAlarmModelVersionsResponseTypeDef:
        """
        Lists all the versions of an alarm model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/list_alarm_model_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#list_alarm_model_versions)
        """

    def list_alarm_models(
        self, **kwargs: Unpack[ListAlarmModelsRequestRequestTypeDef]
    ) -> ListAlarmModelsResponseTypeDef:
        """
        Lists the alarm models that you created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/list_alarm_models.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#list_alarm_models)
        """

    def list_detector_model_versions(
        self, **kwargs: Unpack[ListDetectorModelVersionsRequestRequestTypeDef]
    ) -> ListDetectorModelVersionsResponseTypeDef:
        """
        Lists all the versions of a detector model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/list_detector_model_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#list_detector_model_versions)
        """

    def list_detector_models(
        self, **kwargs: Unpack[ListDetectorModelsRequestRequestTypeDef]
    ) -> ListDetectorModelsResponseTypeDef:
        """
        Lists the detector models you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/list_detector_models.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#list_detector_models)
        """

    def list_input_routings(
        self, **kwargs: Unpack[ListInputRoutingsRequestRequestTypeDef]
    ) -> ListInputRoutingsResponseTypeDef:
        """
        Lists one or more input routings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/list_input_routings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#list_input_routings)
        """

    def list_inputs(
        self, **kwargs: Unpack[ListInputsRequestRequestTypeDef]
    ) -> ListInputsResponseTypeDef:
        """
        Lists the inputs you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/list_inputs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#list_inputs)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags (metadata) you have assigned to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#list_tags_for_resource)
        """

    def put_logging_options(
        self, **kwargs: Unpack[PutLoggingOptionsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets or updates the AWS IoT Events logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/put_logging_options.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#put_logging_options)
        """

    def start_detector_model_analysis(
        self, **kwargs: Unpack[StartDetectorModelAnalysisRequestRequestTypeDef]
    ) -> StartDetectorModelAnalysisResponseTypeDef:
        """
        Performs an analysis of your detector model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/start_detector_model_analysis.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#start_detector_model_analysis)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds to or modifies the tags of the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the given tags (metadata) from the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#untag_resource)
        """

    def update_alarm_model(
        self, **kwargs: Unpack[UpdateAlarmModelRequestRequestTypeDef]
    ) -> UpdateAlarmModelResponseTypeDef:
        """
        Updates an alarm model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/update_alarm_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#update_alarm_model)
        """

    def update_detector_model(
        self, **kwargs: Unpack[UpdateDetectorModelRequestRequestTypeDef]
    ) -> UpdateDetectorModelResponseTypeDef:
        """
        Updates a detector model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/update_detector_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#update_detector_model)
        """

    def update_input(
        self, **kwargs: Unpack[UpdateInputRequestRequestTypeDef]
    ) -> UpdateInputResponseTypeDef:
        """
        Updates an input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotevents/client/update_input.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/client/#update_input)
        """
